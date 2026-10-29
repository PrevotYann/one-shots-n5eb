/**
 * Compile data/adventure.json (écrit par tools/build.py) en compendium Adventure LevelDB
 * dans n5eb-feux-follets/packs/aventure, pour l'importeur d'aventure standard de Foundry.
 *
 * Les prétirés gardent leur description `_build` dans flags.n5eb-feux-follets.build :
 * scripts/main.mjs la lit après l'import pour copier classes, clans et techniques
 * depuis les compendiums du système n5eb installé.
 *
 * Usage : node tools/build_packs.mjs
 */
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import { compilePack } from "@foundryvtt/foundryvtt-cli";

const MODULE_ID = "n5eb-feux-follets";
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const MOD_DIR = path.join(ROOT, MODULE_ID);
const SRC = path.join(ROOT, "src", "packs", "aventure");
const OUT = path.join(MOD_DIR, "packs", "aventure");

const data = JSON.parse(fs.readFileSync(path.join(MOD_DIR, "data", "adventure.json"), "utf8"));
const manifest = JSON.parse(fs.readFileSync(path.join(MOD_DIR, "module.json"), "utf8"));

/** Identifiant Foundry stable dérivé d'une clé. */
const ALPHANUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
function stableId(key) {
  const bytes = crypto.createHash("sha256").update(`${MODULE_ID}:${key}`).digest();
  return Array.from(bytes.subarray(0, 16), b => ALPHANUM[b % ALPHANUM.length]).join("");
}

const now = Date.UTC(2026, 0, 1);
const stats = () => ({
  coreVersion: "14", systemId: "n5eb", systemVersion: manifest.relationships.systems[0].compatibility.minimum,
  createdTime: now, modifiedTime: now, lastModifiedBy: null
});

/* -------------------------------------------- */

const actors = data.actors.map(spec => {
  const actor = structuredClone(spec);
  if ( actor._build ) setModuleFlag(actor, "build", actor._build);
  delete actor._build;
  actor.items ??= [];
  return actor;
});
const actorsById = new Map(actors.map(a => [a._id, a]));

const scenes = data.scenes.map(spec => {
  const scene = structuredClone(spec);
  const tokenSpecs = scene._tokens ?? [];
  delete scene._tokens;
  scene.thumb ??= scene.background?.src ?? null;
  scene.tokens = tokenSpecs.map((t, i) => {
    const actor = actorsById.get(t.actor);
    if ( !actor ) throw new Error(`Jeton de ${scene.name} : acteur inconnu ${t.actor}`);
    const proto = structuredClone(actor.prototypeToken ?? {});
    delete proto.randomImg;
    return {
      ...proto,
      _id: stableId(`token:${scene._id}:${i}`),
      name: proto.name ?? actor.name,
      actorId: actor._id,
      actorLink: !!proto.actorLink,
      x: t.x, y: t.y,
      hidden: !!t.hidden
    };
  });
  return scene;
});

function setModuleFlag(doc, key, value) {
  doc.flags ??= {};
  doc.flags[MODULE_ID] ??= {};
  doc.flags[MODULE_ID][key] = value;
}

const adventureId = stableId("adventure");
const adventure = {
  _id: adventureId,
  _key: `!adventures!${adventureId}`,
  name: "Les Feux Follets de Kawabe",
  img: "modules/n5eb-feux-follets/assets/maps/village-kawabe.webp",
  caption: "One-shot N5eB — mission de rang C pour 5 genin de niveau 1 (3 à 4 heures).",
  description: `
<p><strong>Un village de pêcheurs demande l'aide de Konoha : chaque nuit, un mystérieux fantôme apparaît sur le lac Kagami.</strong></p>
<p><strong>Contenu importé :</strong> 5 prétirés, les PNJ et adversaires, 4 scènes avec leurs jetons, les journaux du MJ et des joueurs,
les aides de jeu, les objets du scénario et une table de rumeurs.</p>
<p>À la fin de l'import, les classes, clans, historiques, techniques et armes des prétirés sont copiés depuis les
compendiums du système N5eB installé.</p>
<p><em>Ouvrez ensuite le journal « Lisez-moi (MJ) ».</em></p>`,
  actors,
  items: data.items,
  journal: data.journals,
  scenes,
  tables: data.tables,
  folders: data.folders,
  macros: [], cards: [], playlists: [], combats: [],
  sort: 0,
  flags: { [MODULE_ID]: { version: manifest.version, welcome: data.welcome, translations: data.translations ?? {} } },
  _stats: stats()
};

/* -------------------------------------------- */
/*  Vérifications                               */
/* -------------------------------------------- */

const ID = /^[A-Za-z0-9]{16}$/;
const check = (docs, where) => {
  const seen = new Set();
  for ( const d of docs ) {
    if ( !ID.test(d._id) ) throw new Error(`Identifiant invalide ${d._id} (${where} ${d.name ?? ""})`);
    if ( seen.has(d._id) ) throw new Error(`Identifiant en double ${d._id} (${where})`);
    seen.add(d._id);
  }
};
for ( const key of ["actors", "items", "journal", "scenes", "tables", "folders"] ) check(adventure[key], key);
for ( const a of actors ) check(a.items, `actor ${a.name}`);
for ( const j of adventure.journal ) check(j.pages ?? [], `journal ${j.name}`);
for ( const s of scenes ) check(s.tokens, `scene ${s.name}`);

const folderIds = new Set(adventure.folders.map(f => f._id));
for ( const key of ["actors", "items", "journal", "scenes", "tables", "folders"] ) {
  for ( const d of adventure[key] ) {
    if ( d.folder && !folderIds.has(d.folder) ) throw new Error(`Dossier inconnu ${d.folder} (${d.name})`);
  }
}

const assets = [...JSON.stringify(adventure).matchAll(/modules\/n5eb-feux-follets\/([^"\\?#]+)/g)].map(m => m[1]);
const missing = [...new Set(assets)].filter(a => !fs.existsSync(path.join(MOD_DIR, a)));
if ( missing.length ) throw new Error(`Fichiers manquants : ${missing.join(", ")}`);

/* -------------------------------------------- */
/*  Écriture et compilation                     */
/* -------------------------------------------- */

fs.rmSync(SRC, { recursive: true, force: true });
fs.mkdirSync(SRC, { recursive: true });
fs.writeFileSync(path.join(SRC, `les-feux-follets-de-kawabe_${adventureId}.json`), `${JSON.stringify(adventure, null, 2)}\n`);
fs.rmSync(OUT, { recursive: true, force: true });
await compilePack(SRC, OUT);
console.log(`Aventure ${adventureId} : ${actors.length} acteurs, ${data.items.length} objets, `
  + `${data.journals.length} journaux, ${scenes.length} scènes, ${data.tables.length} table(s) -> ${OUT}`);
