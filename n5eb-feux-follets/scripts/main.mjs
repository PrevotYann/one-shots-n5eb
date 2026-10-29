/**
 * N5eB One-Shot : Les Feux Follets de Kawabe
 * Le scénario s'importe avec l'importeur d'aventure standard de Foundry (compendium « aventure »).
 * Après l'import, les classes, clans, historiques, techniques et armes des prétirés sont copiés depuis les
 * compendiums du système n5eb, pour rester compatibles avec la version installée.
 */

const MODULE_ID = "n5eb-feux-follets";
const ADVENTURE_PACK = `${MODULE_ID}.aventure`;

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
    hint: "Ouvre l'aventure du compendium : prétirés, PNJ, journaux, cartes et objets du one-shot.",
    icon: "fas fa-file-import",
    type: ImportMenu,
    restricted: true
  });
});

Hooks.once("ready", async () => {
  const module = game.modules.get(MODULE_ID);
  module.api = { openAdventure, completeActors };
  if ( !game.user.isGM ) return;
  if ( game.system.id !== "n5eb" ) {
    ui.notifications.error("Les Feux Follets de Kawabe : ce module nécessite le système N5eB (n5eb).", { permanent: true });
    return;
  }
  if ( !game.settings.get(MODULE_ID, "importedVersion") ) promptImport();
});

Hooks.on("importAdventure", async (adventure) => {
  if ( adventure.pack !== ADVENTURE_PACK ) return;
  await completeActors(adventure);
  await game.settings.set(MODULE_ID, "importedVersion", game.modules.get(MODULE_ID).version);
  ui.notifications.info("Feux Follets : import terminé ! Ouvrez le journal « Lisez-moi (MJ) » pour commencer.", { permanent: true });
  game.journal.get(adventure.getFlag(MODULE_ID, "welcome"))?.sheet.render(true);
});

/**
 * Entrée de menu dans les paramètres : ouvre simplement l'aventure.
 */
class ImportMenu extends foundry.applications.api.ApplicationV2 {
  async render() {
    openAdventure();
    return this;
  }
}

/* -------------------------------------------- */
/*  Boîte de dialogue                           */
/* -------------------------------------------- */

async function promptImport() {
  const { DialogV2 } = foundry.applications.api;
  const choice = await DialogV2.wait({
    window: { title: "Les Feux Follets de Kawabe", icon: "fas fa-scroll" },
    content: `
      <p><strong>Les Feux Follets de Kawabe</strong> — one-shot N5eB pour 5 joueurs débutants.</p>
      <p>Le scénario s'importe depuis le compendium <em>Les Feux Follets de Kawabe (Aventure)</em>.
      Vous pourrez aussi le rouvrir plus tard depuis l'onglet Compendiums ou les paramètres du module.</p>`,
    rejectClose: false,
    buttons: [
      { action: "open", label: "Ouvrir l'aventure", icon: "fas fa-file-import", default: true },
      { action: "later", label: "Plus tard", icon: "fas fa-clock" }
    ]
  });
  if ( choice === "open" ) return openAdventure();
}

/**
 * Ouvre la fiche d'import de l'aventure.
 */
export async function openAdventure() {
  const pack = game.packs.get(ADVENTURE_PACK);
  if ( !pack ) return ui.notifications.error("Feux Follets : compendium d'aventure introuvable.");
  const [adventure] = await pack.getDocuments();
  adventure?.sheet.render(true);
}

/* -------------------------------------------- */
/*  Prétirés                                    */
/* -------------------------------------------- */

/**
 * Complète les acteurs importés qui portent une description `build` (prétirés, adversaires construits sur une classe).
 * @param {Adventure} [adventure]  L'aventure importée (par défaut, celle du compendium du module).
 */
export async function completeActors(adventure) {
  if ( !game.user.isGM ) return;
  adventure ??= (await game.packs.get(ADVENTURE_PACK)?.getDocuments())?.[0];
  const translations = adventure?.getFlag(MODULE_ID, "translations") ?? {};
  const missingPacks = ["n5eb.class", "n5eb.clan", "n5eb.jutsus", "n5eb.items", "n5eb.backgrounds", "n5eb.feats"]
    .filter(id => !game.packs.get(id));
  if ( missingPacks.length ) {
    ui.notifications.warn(`Feux Follets : compendiums introuvables (${missingPacks.join(", ")}). Les prétirés seront incomplets.`);
  }
  const actors = game.actors.filter(a => a.getFlag(MODULE_ID, "build"));
  if ( !actors.length ) return;
  ui.notifications.info("Feux Follets : copie des techniques depuis les compendiums…");
  for ( const actor of actors ) {
    try {
      await completeActor(actor, translations);
    } catch(err) {
      console.error(`${MODULE_ID} | impossible de compléter ${actor.name}`, err);
    }
  }
}

async function completeActor(actor, translations) {
  // Retire les copies faites lors d'un import précédent.
  const previous = actor.items.filter(i => i.getFlag(MODULE_ID, "source")).map(i => i.id);
  if ( previous.length ) await actor.deleteEmbeddedDocuments("Item", previous);

  const spec = { system: actor.toObject().system, items: [], _build: actor.getFlag(MODULE_ID, "build") };
  const src = await buildActor(spec, translations);
  await addItems(actor, src.items);
  await actor.update({ system: src.system });
}

/**
 * Ajoute les objets d'un coup ; si l'un d'eux pose problème, les ajoute un à un.
 */
async function addItems(actor, items) {
  try {
    return await actor.createEmbeddedDocuments("Item", items, { keepId: true });
  } catch(err) {
    console.warn(`${MODULE_ID} | ajout des objets de ${actor.name} en mode dégradé`, err);
  }
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
        console.error(`${MODULE_ID} | objet ignoré : ${item.name} (${actor.name})`, e);
      }
    }
  }
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

    // Selon la version du système, les avancements sont un tableau ou un objet indexé par identifiant.
    const advancement = obj.system.advancement ?? [];
    for ( const adv of Array.isArray(advancement) ? advancement : Object.values(advancement) ) {
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
