/**
 * N5eB One-Shot : Les Feux Follets de Kawabe
 * Importeur : crée dans le monde les dossiers, objets, acteurs, journaux, tables et scènes du scénario.
 * Les classes, clans, historiques, techniques et armes des prétirés sont copiés depuis les
 * compendiums du système n5eb au moment de l'import, pour rester compatibles avec la version installée.
 */

const MODULE_ID = "n5eb-feux-follets";
const DATA_URL = `modules/${MODULE_ID}/data/adventure.json`;
const LOG = (...args) => console.log(`${MODULE_ID} |`, ...args);

/* -------------------------------------------- */
/*  Initialisation                              */
/* -------------------------------------------- */

Hooks.once("init", () => {
  game.settings.register(MODULE_ID, "importedVersion", {
    scope: "world",
    config: false,
    type: String,
    default: ""
  });

  game.settings.registerMenu(MODULE_ID, "importMenu", {
    name: "Les Feux Follets de Kawabe",
    label: "Importer / réimporter le scénario",
    hint: "Crée (ou recrée) les prétirés, PNJ, journaux, cartes et objets du one-shot dans ce monde.",
    icon: "fas fa-file-import",
    type: ImportMenu,
    restricted: true
  });
});

Hooks.once("ready", async () => {
  const module = game.modules.get(MODULE_ID);
  module.api = { importAdventure, removeAdventure, promptImport };
  if ( !game.user.isGM ) return;
  if ( game.system.id !== "n5eb" ) {
    ui.notifications.error("Les Feux Follets de Kawabe : ce module nécessite le système N5eB (n5eb).", { permanent: true });
    return;
  }
  if ( !game.settings.get(MODULE_ID, "importedVersion") ) promptImport();
});

/**
 * Entrée de menu dans les paramètres : ouvre simplement la boîte de dialogue d'import.
 */
class ImportMenu extends foundry.applications.api.ApplicationV2 {
  async render() {
    promptImport();
    return this;
  }
}

/* -------------------------------------------- */
/*  Boîte de dialogue                           */
/* -------------------------------------------- */

export async function promptImport() {
  const { DialogV2 } = foundry.applications.api;
  const already = !!game.settings.get(MODULE_ID, "importedVersion") || hasImportedDocuments();
  const content = `
    <p><strong>Les Feux Follets de Kawabe</strong> — one-shot N5eB pour 5 joueurs débutants.</p>
    <p>L'import va créer : 5 prétirés, les PNJ et adversaires, 4 scènes, les journaux du MJ et des joueurs,
    les aides de jeu, les objets du scénario et une table de rumeurs.</p>
    ${already ? `<p class="ffk-warning"><i class="fas fa-triangle-exclamation"></i> Le scénario semble déjà importé.
      Réimporter <strong>supprime puis recrée</strong> tous les documents du scénario (les modifications faites dessus seront perdues).</p>` : ""}
    <p>Les techniques, classes et clans sont copiés depuis les compendiums du système n5eb.</p>`;
  const choice = await DialogV2.wait({
    window: { title: "Importer le one-shot", icon: "fas fa-scroll" },
    content,
    rejectClose: false,
    buttons: [
      { action: "import", label: already ? "Réimporter" : "Importer", icon: "fas fa-file-import", default: true },
      { action: "later", label: "Plus tard", icon: "fas fa-clock" }
    ]
  });
  if ( choice === "import" ) return importAdventure({ replace: already });
}

/* -------------------------------------------- */
/*  Import                                      */
/* -------------------------------------------- */

function hasImportedDocuments() {
  return [game.actors, game.items, game.journal, game.scenes, game.tables]
    .some(c => c.some(d => d.getFlag(MODULE_ID, "imported")));
}

/**
 * Supprime tous les documents créés par ce module.
 */
export async function removeAdventure(data) {
  const ids = data ? collectIds(data) : null;
  const collections = [
    ["Scene", game.scenes], ["Actor", game.actors], ["Item", game.items],
    ["JournalEntry", game.journal], ["RollTable", game.tables], ["Folder", game.folders]
  ];
  for ( const [cls, collection] of collections ) {
    const toDelete = collection.filter(d => d.getFlag(MODULE_ID, "imported") || ids?.[cls]?.has(d.id)).map(d => d.id);
    if ( toDelete.length ) await getDocumentClass(cls).deleteDocuments(toDelete);
  }
}

function collectIds(data) {
  return {
    Scene: new Set(data.scenes.map(d => d._id)),
    Actor: new Set(data.actors.map(d => d._id)),
    Item: new Set(data.items.map(d => d._id)),
    JournalEntry: new Set(data.journals.map(d => d._id)),
    RollTable: new Set(data.tables.map(d => d._id)),
    Folder: new Set(data.folders.map(d => d._id))
  };
}

export async function importAdventure({ replace=false }={}) {
  if ( !game.user.isGM ) return;
  const notify = msg => ui.notifications.info(`Feux Follets : ${msg}`);
  let data;
  try {
    const response = await fetch(DATA_URL);
    data = await response.json();
  } catch(err) {
    console.error(err);
    ui.notifications.error("Feux Follets : impossible de lire les données du scénario.");
    return;
  }

  const missingPacks = ["n5eb.class", "n5eb.clan", "n5eb.jutsus", "n5eb.items", "n5eb.backgrounds", "n5eb.feats"]
    .filter(id => !game.packs.get(id));
  if ( missingPacks.length ) {
    ui.notifications.warn(`Feux Follets : compendiums introuvables (${missingPacks.join(", ")}). Les prétirés seront incomplets.`);
  }

  if ( replace ) {
    notify("suppression de l'ancien import…");
    await removeAdventure(data);
  }

  notify("création des dossiers…");
  // Les dossiers parents d'abord.
  const folders = [...data.folders].sort((a, b) => (a.folder ? 1 : 0) - (b.folder ? 1 : 0));
  for ( const f of folders ) await Folder.create(f, { keepId: true });

  notify("création des objets…");
  await safeCreateMany(Item, data.items);

  notify("création des personnages (copie des techniques depuis les compendiums)…");
  for ( const spec of data.actors ) {
    const actorData = await buildActor(spec, data.translations ?? {});
    await safeCreateActor(actorData);
  }

  notify("création des journaux…");
  await safeCreateMany(JournalEntry, data.journals);

  notify("création des tables…");
  await safeCreateMany(RollTable, data.tables);

  notify("création des scènes…");
  for ( const sceneSpec of data.scenes ) await createScene(sceneSpec);

  await game.settings.set(MODULE_ID, "importedVersion", game.modules.get(MODULE_ID).version);
  ui.notifications.info("Feux Follets : import terminé ! Ouvrez le journal « Lisez-moi (MJ) » pour commencer.", { permanent: true });
  game.journal.get(data.welcome)?.sheet.render(true);
}

async function safeCreateMany(cls, docs) {
  try {
    await cls.createDocuments(docs, { keepId: true });
  } catch(err) {
    console.error(`${MODULE_ID} | échec de création groupée ${cls.documentName}, nouvel essai un par un`, err);
    for ( const d of docs ) {
      try { await cls.create(d, { keepId: true }); }
      catch(e) {
        // Dernier recours pour un objet : sans ses activités (description seule).
        try {
          if ( !d.system?.activities ) throw e;
          const fallback = foundry.utils.deepClone(d);
          delete fallback.system.activities;
          await cls.create(fallback, { keepId: true });
        } catch(e2) { console.error(`${MODULE_ID} | impossible de créer ${d.name}`, e2); }
      }
    }
  }
}

/* -------------------------------------------- */
/*  Acteurs                                     */
/* -------------------------------------------- */

/**
 * Crée un acteur ; si un objet intégré pose problème, crée l'acteur sans lui puis ajoute les objets un à un.
 */
async function safeCreateActor(actorData) {
  try {
    return await Actor.create(actorData, { keepId: true });
  } catch(err) {
    console.warn(`${MODULE_ID} | création de ${actorData.name} en mode dégradé`, err);
  }
  const items = actorData.items ?? [];
  const actor = await Actor.create({ ...actorData, items: [] }, { keepId: true });
  for ( const item of items ) {
    try {
      await actor.createEmbeddedDocuments("Item", [item], { keepId: true });
    } catch(err) {
      // Dernier recours : l'objet sans ses activités (description seule).
      try {
        const fallback = foundry.utils.deepClone(item);
        delete fallback.system?.activities;
        await actor.createEmbeddedDocuments("Item", [fallback], { keepId: true });
      } catch(e) {
        console.error(`${MODULE_ID} | objet ignoré : ${item.name} (${actorData.name})`, e);
      }
    }
  }
  return actor;
}

/**
 * Construit les données d'un acteur à partir de sa description.
 * La clé `_build` décrit ce qui doit être copié depuis les compendiums du système.
 */
async function buildActor(spec, translations) {
  const src = foundry.utils.deepClone(spec);
  const build = src._build;
  delete src._build;
  src.items ??= [];
  if ( !build ) return src;

  const level = build.level ?? 1;
  const choices = build.choices ?? [];
  const usedChoices = new Set();
  for ( const key of choices ) applyTraitKey(src, key);

  for ( const part of ["class", "race", "background"] ) {
    const ref = build[part];
    if ( !ref ) continue;
    const doc = await fromUuid(ref);
    if ( !doc ) {
      console.warn(`${MODULE_ID} | introuvable : ${ref}`);
      continue;
    }
    const obj = prepareItem(doc, ref, translations);
    obj._id = foundry.utils.randomID();
    if ( part === "class" ) obj.system.levels = level;

    for ( const adv of obj.system.advancement ?? [] ) {
      const advLevel = adv.level ?? null;
      switch ( adv.type ) {
        case "HitPoints":
        case "Chakra":
          if ( part !== "class" ) break;
          adv.value = {};
          for ( let l = 1; l <= level; l++ ) adv.value[l] = l === 1 ? "max" : "avg";
          break;
        case "Trait": {
          if ( (advLevel === null) || (advLevel > level) ) break;
          const grants = adv.configuration?.grants ?? [];
          const chosen = [...grants];
          for ( const key of grants ) applyTraitKey(src, key);
          for ( const choice of adv.configuration?.choices ?? [] ) {
            let remaining = choice.count ?? 0;
            for ( const key of choices ) {
              if ( remaining <= 0 ) break;
              if ( usedChoices.has(key) || chosen.includes(key) ) continue;
              if ( !(choice.pool ?? []).some(p => poolMatches(p, key)) ) continue;
              chosen.push(key);
              usedChoices.add(key);
              remaining--;
            }
          }
          adv.value = { chosen };
          break;
        }
        case "ItemGrant": {
          if ( (advLevel === null) || (advLevel > level) ) break;
          const added = {};
          for ( const entry of adv.configuration?.items ?? [] ) {
            if ( entry.optional ) continue;
            const granted = await fromUuid(entry.uuid);
            if ( !granted ) {
              console.warn(`${MODULE_ID} | objet accordé introuvable : ${entry.uuid}`);
              continue;
            }
            const it = prepareItem(granted, entry.uuid, translations);
            it._id = foundry.utils.randomID();
            foundry.utils.setProperty(it, "flags.n5eb.advancementOrigin", `${obj._id}.${adv._id}`);
            src.items.push(it);
            added[it._id] = entry.uuid;
          }
          adv.value = { added };
          break;
        }
      }
    }
    src.items.push(obj);
    if ( part === "race" ) foundry.utils.setProperty(src, "system.details.race", obj._id);
    if ( part === "background" ) foundry.utils.setProperty(src, "system.details.background", obj._id);
  }

  for ( const ref of build.items ?? [] ) {
    const doc = await fromUuid(ref.uuid);
    if ( !doc ) {
      console.warn(`${MODULE_ID} | introuvable : ${ref.uuid}`);
      continue;
    }
    const it = prepareItem(doc, ref.uuid, translations, ref);
    it._id = foundry.utils.randomID();
    src.items.push(it);
  }

  // Équipe les objets accordés par la classe ou l'historique (ex. l'armure de départ).
  for ( const id of build.equip ?? [] ) {
    const it = src.items.find(i => i.flags?.[MODULE_ID]?.source?.endsWith(`.${id}`));
    if ( it ) foundry.utils.setProperty(it, "system.equipped", true);
  }
  return src;
}

/**
 * Copie un document de compendium et lui applique la traduction / les surcharges du scénario.
 */
function prepareItem(doc, uuid, translations, overrides={}) {
  const obj = doc.toObject();
  delete obj._id;
  delete obj.folder;
  delete obj.sort;
  delete obj.ownership;
  obj._stats = { compendiumSource: uuid };
  obj.flags ??= {};
  foundry.utils.setProperty(obj, `flags.${MODULE_ID}.source`, uuid);

  const tr = translations[doc.id] ?? translations[doc.name];
  const summary = overrides.summary ?? tr?.summary;
  const name = overrides.name ?? tr?.name;
  if ( name ) {
    obj.name = (tr?.keepOriginal !== false) && (name !== doc.name) ? `${name} (${doc.name})` : name;
  }
  if ( summary && obj.system?.description ) {
    const original = obj.system.description.value ?? "";
    obj.system.description.value = `<section class="ffk-summary"><p><strong>En bref :</strong> ${summary}</p></section>`
      + (original ? `<hr><p><em>Texte original (anglais) :</em></p>${original}` : "");
  }
  if ( overrides.quantity !== undefined ) foundry.utils.setProperty(obj, "system.quantity", overrides.quantity);
  if ( overrides.equipped !== undefined ) foundry.utils.setProperty(obj, "system.equipped", overrides.equipped);
  if ( overrides.system ) foundry.utils.mergeObject(obj.system, overrides.system);
  return obj;
}

function poolMatches(pool, key) {
  if ( pool === key ) return true;
  if ( pool.endsWith("*") ) return key.startsWith(pool.slice(0, -1));
  return false;
}

/**
 * Applique une clé de trait (« skills:prc », « saves:dex », « weapon:sim », « tool:kit:medicineKit »…)
 * directement aux données source de l'acteur, comme le ferait l'avancement Trait du système.
 */
function applyTraitKey(src, key) {
  const parts = key.split(":");
  const trait = parts[0];
  let path;
  try {
    path = globalThis.dnd5e?.documents?.Trait?.changeKeyPath?.(key);
  } catch(err) { path = null; }
  if ( !path ) path = fallbackKeyPath(trait, parts.at(-1));
  if ( !path ) return;
  const last = parts.at(-1);
  if ( (trait === "saves") || (trait === "skills") || (trait === "tool") ) {
    foundry.utils.setProperty(src, path, 1);
    if ( trait === "tool" ) {
      const ability = CONFIG.DND5E?.tools?.[last]?.ability;
      if ( ability && !foundry.utils.hasProperty(src, `system.tools.${last}.ability`) ) {
        foundry.utils.setProperty(src, `system.tools.${last}.ability`, ability);
      }
    }
    return;
  }
  const existing = foundry.utils.getProperty(src, path);
  const set = new Set(Array.isArray(existing) ? existing : existing instanceof Set ? Array.from(existing) : []);
  set.add(last);
  foundry.utils.setProperty(src, path, Array.from(set));
}

function fallbackKeyPath(trait, last) {
  switch ( trait ) {
    case "saves": return `system.abilities.${last}.proficient`;
    case "skills": return `system.skills.${last}.value`;
    case "tool": return `system.tools.${last}.value`;
    case "weapon": return "system.traits.weaponProf.value";
    case "armor": return "system.traits.armorProf.value";
    case "languages": return "system.traits.languages.value";
    case "dr": case "di": case "dv": case "ci": return `system.traits.${trait}.value`;
    default: return null;
  }
}

/* -------------------------------------------- */
/*  Scènes                                      */
/* -------------------------------------------- */

async function createScene(spec) {
  const data = foundry.utils.deepClone(spec);
  const tokenSpecs = data._tokens ?? [];
  delete data._tokens;
  data.tokens = [];
  for ( const t of tokenSpecs ) {
    const actor = game.actors.get(t.actor);
    if ( !actor ) continue;
    try {
      const td = await actor.getTokenDocument({ x: t.x, y: t.y, hidden: !!t.hidden });
      const obj = td.toObject();
      delete obj._id;
      data.tokens.push(obj);
    } catch(err) {
      console.warn(`${MODULE_ID} | jeton ignoré (${actor.name})`, err);
    }
  }
  let scene;
  try {
    scene = await Scene.create(data, { keepId: true });
  } catch(err) {
    console.error(`${MODULE_ID} | échec de création de la scène ${data.name}`, err);
    return;
  }
  try {
    const thumb = await scene.createThumbnail();
    await scene.update({ thumb: thumb.thumb });
  } catch(err) {
    LOG("miniature non générée pour", scene.name);
  }
}
