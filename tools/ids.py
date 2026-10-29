"""Identifiants déterministes et liens Foundry (@UUID) utilisés par les journaux."""
import hashlib
import string

_ALPHABET = string.ascii_letters + string.digits


def gid(key):
    """Identifiant Foundry stable (16 caractères) dérivé d'une clé lisible."""
    digest = hashlib.sha256(f"ffk:{key}".encode()).digest()
    return "".join(_ALPHABET[b % 62] for b in digest[:16])


def actor_id(key):
    return gid(f"actor.{key}")


def item_id(key):
    return gid(f"item.{key}")


def journal_id(key):
    return gid(f"journal.{key}")


def page_id(jkey, pkey):
    return gid(f"page.{jkey}.{pkey}")


def scene_id(key):
    return gid(f"scene.{key}")


def table_id(key):
    return gid(f"table.{key}")


def folder_id(key):
    return gid(f"folder.{key}")


# --- liens à insérer dans le HTML des journaux ---------------------------------

def A(key, label):
    return f"@UUID[Actor.{actor_id(key)}]{{{label}}}"


def I(key, label):
    return f"@UUID[Item.{item_id(key)}]{{{label}}}"


def J(jkey, pkey, label):
    return f"@UUID[JournalEntry.{journal_id(jkey)}.JournalEntryPage.{page_id(jkey, pkey)}]{{{label}}}"


def S(key, label):
    return f"@UUID[Scene.{scene_id(key)}]{{{label}}}"


def T(key, label):
    return f"@UUID[RollTable.{table_id(key)}]{{{label}}}"


SKILLS_FR = {
    "acr": "Acrobaties (Acrobatics)", "ath": "Athlétisme (Athletics)", "prc": "Perception",
    "inv": "Investigation", "ins": "Intuition (Insight)", "ste": "Discrétion (Stealth)",
    "per": "Persuasion", "itm": "Intimidation", "dec": "Tromperie (Deception)", "his": "Histoire (History)",
    "sur": "Survie (Survival)", "med": "Médecine (Medicine)", "ccl": "Contrôle du chakra (Chakra Control)",
    "ill": "Illusions", "nsh": "Ninshō (Ninshou)", "mar": "Arts martiaux (Martial Arts)",
    "slt": "Escamotage (Sleight of Hand)", "nat": "Nature", "ani": "Dressage (Animal Handling)",
}

ABILITIES_FR = {"str": "Force", "dex": "Dextérité", "con": "Constitution",
                "int": "Intelligence", "wis": "Sagesse", "cha": "Charisme"}


def SK(skill, dc):
    """Bouton de test de compétence cliquable + nom français."""
    return f"<strong>{SKILLS_FR[skill]}</strong> DD {dc} [[/skill skill={skill} dc={dc}]]"


def SV(ability, dc):
    """Bouton de jet de sauvegarde cliquable + nom français."""
    return f"<strong>sauvegarde de {ABILITIES_FR[ability]}</strong> DD {dc} [[/save ability={ability} dc={dc}]]"


def box(kind, html, title=None):
    titles = {
        "read": "À lire ou paraphraser à voix haute",
        "tip": "Conseil au MJ",
        "clue": "Indice",
        "fight": "Combat",
        "rule": "Règle",
        "secret": "Secret du MJ",
    }
    return (f'<div class="ffk-box ffk-{kind}"><p class="ffk-box-title">{title or titles[kind]}</p>{html}</div>')
