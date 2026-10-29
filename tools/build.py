"""Construit le module « Les Feux Follets de Kawabe » en conservant les illustrations finales.

Usage : python tools/build.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import art  # noqa: E402
from content_joueurs import AIDES, FICHES, GUIDE  # noqa: E402
from content_mj import LISEZMOI, PNJ, SCENARIO, p  # noqa: E402
from ids import (actor_id, folder_id, gid, item_id, journal_id, page_id,  # noqa: E402
                 scene_id, table_id, J)

MODULE_ID = "n5eb-feux-follets"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD_DIR = os.path.join(ROOT, MODULE_ID)
WEB = f"modules/{MODULE_ID}"
FLAGS = {MODULE_ID: {"imported": True}}

# Compendiums du système n5eb
def CLS(i): return f"Compendium.n5eb.class.Item.{i}"
def CLAN(i): return f"Compendium.n5eb.clan.Item.{i}"
def JUT(i): return f"Compendium.n5eb.jutsus.Item.{i}"
def ITM(i): return f"Compendium.n5eb.items.Item.{i}"
def BG(i): return f"Compendium.n5eb.backgrounds.Item.{i}"
def FEAT(i): return f"Compendium.n5eb.feats.Item.{i}"


# --------------------------------------------------------------------------- #
#  Traductions des documents copiés depuis le système (par identifiant)        #
# --------------------------------------------------------------------------- #

TR = {
    # Classes, clans, historiques
    "Ipg5bKh1zS3Yfn2I": ("Spécialiste du taijutsu", "Le maître du combat à mains nues : beaucoup de PV, des coups puissants et des taijutsu à coût fixe."),
    "n5ebNinSpec00001": ("Spécialiste du ninjutsu", "Le spécialiste des techniques de chakra : beaucoup de chakra, peu de PV."),
    "6TxLk91QYckjBOY8": ("Ninja éclaireur", "Le ninja polyvalent : exploration, pistage, armes et quelques techniques."),
    "jBWRb3PE7vc3fiH5": ("Spécialiste des armes", "Le maître des armes ninja : précision, techniques d'armes (bukijutsu)."),
    "55ZGaTkWJHT0mQmp": ("Ninja médecin", "Le soigneur de l'équipe : techniques médicales, trousse de médecine, soins pendant les repos."),
    "V9y2Nb2LH8qpEVyB": ("Clan Akimichi", "Clan noble de Konoha qui transforme les calories en chakra et peut faire grossir son corps."),
    "oO0kK6HZshBbz7YP": ("Clan Nara", "Clan de stratèges de Konoha qui manipule les ombres."),
    "2QbtB7Qvz6uOOZVW": ("Clan Fûma", "Clan voyageur du Pays du Feu, maître des armes de lancer et du fûma-shuriken."),
    "YWIfpZ862Gc9GfSA": ("Sans clan", "Pas de technique héréditaire, mais un potentiel sans limite et beaucoup de travail."),
    "n5ebHardWork0001": ("Travailleur acharné", "Tu t'es entraîné plus que tout le monde."),
    "JfooXW5qno1hSYX0": ("Fauteur de troubles", "Les bêtises, c'est ta spécialité."),
    "n5ebGenius000001": ("Génie", "Tu apprends tout plus vite que les autres."),
    "C0QdlDm3fhlaRFOV": ("Voyageuse", "Tu as parcouru le pays avant de t'installer à Konoha."),
    "n5ebStudent00001": ("Élève", "Tu as été formée par un maître dont le nom ouvre des portes."),
    # Capacités de classe
    "ITK8bVvZelagkGvm": ("Défense martiale", "Sans armure, ta CA = 10 + bonus de maîtrise + modificateur de Dextérité."),
    "Nz7RMFTPquBcxxSX": ("Technique à mains nues", "Avec tes poings ou des armes de taijutsu (brassards, griffes…), tu peux utiliser la Force ou la Dextérité, et tes coups font au moins 1d6."),
    "S1TglFLRvVSLZHNL": ("Technique martiale", "Tes taijutsu ont un coût fixe : rang D = 3 chakra, rang C = 5 chakra (sans autre réduction possible)."),
    "n5ebChakraRec001": ("Récupération de chakra", "Une fois par repos court, divise par deux le coût d'un ninjutsu que tu lances."),
    "n5ebRefinedNin01": ("Ninjutsu raffiné", "Choisis 2 ninjutsu connus (conseil : Boule de feu et Trait de flamme). Quand tu les lances : +1 dé de dégâts OU +1 au DD de sauvegarde."),
    "n5ebJutsuCast001": ("Lancer de jutsu", "DD et attaque des jutsu : ninjutsu = Intelligence, genjutsu = Sagesse, taijutsu = Force (8 + maîtrise + modificateur)."),
    "Soj9dv9tqNAqOEJa": ("Posture de combat", "Tu choisis une posture de combat (déjà ajoutée à ta fiche : Posture de lancer)."),
    "Lu39Nfrk9EucVw0H": ("Explorateur habile", "Tu es à l'aise partout. Au niveau 1, tu gagnes « Avisé »."),
    "7K90kY2uxXjw0baT": ("Avisé", "Tu gagnes la maîtrise d'une compétence (Survie)."),
    "K0bKAkvwDWznmQcf": ("Arme de prédilection", "Ton arme fétiche (le fûma-shuriken) gagne +1 à l'attaque et aux dégâts, y compris pour tes bukijutsu."),
    "ujnh7kWBDywvfMWl": ("Ninjutsu médical", "Tu peux apprendre les techniques médicales et utiliser la Sagesse pour elles. Tes tests de Médecine peuvent utiliser l'Intelligence ou la Sagesse."),
    "7Z1YQpJRuycomV2w": ("Repos régénérant", "Quand toi ou un allié que tu peux toucher regagnez des PV à la fin d'un repos, ajoutez 1d6 PV."),
    # Capacités de clan
    "WFtHgPA6CAdIV8W0": ("Calories", "Tu as des Calories (niveau + modificateur de Constitution = 4). Tu peux les dépenser pour activer des techniques et capacités de ton clan. Tu en récupères pendant les repos."),
    "DV3Bhzvj8VS0H37O": ("Techniques du clan Akimichi", "Tu as accès aux techniques secrètes du clan Akimichi."),
    "D26xtOUO4g9qbaWw": ("Pause déjeuner", "Pendant un repos court, tu regagnes des PV en plus : deux fois tes Calories restantes."),
    "85tRdNGxWhIe2dGp": ("Coordination", "Quand tu lances l'initiative, utilise ta réaction pour coordonner tes alliés : ils gagnent l'état Coordonné jusqu'à la fin du combat. 2 fois par repos long."),
    "lqbvjUEk5ktcuOkx": ("Technique préparée", "Tu connais une technique Nara de rang D en plus (Possession de l'ombre), gratuitement."),
    "8sqcPPmPlxJ122FM": ("Techniques des ombres", "Tu as accès aux techniques secrètes du clan Nara."),
    "vMR5vcJeBP0NTVxY": ("Maison des dagues volantes", "Tu as accès aux techniques secrètes du clan Fûma."),
    "WP0zEQzpdnxK9uL8": ("Outils spécialisés", "Tu peux attacher des parchemins explosifs à n'importe quelle arme de lancer, pas seulement aux kunai."),
    "uMVSdxivIZJlmAEA": ("Précision immaculée", "Pour tes attaques d'armes à distance et tes bukijutsu à distance, tu utilises la Dextérité au lieu de la Force."),
    "rn1jqlhChIc4yGLV": ("Culture générale", "Les scores minimum pour apprendre les techniques sont réduits de 2 pour toi."),
    "Fnxo89RdbJoWu6HX": ("Héritage ordinaire", "Tu ne peux pas prendre de dons de clan."),
    "9GmvKDPSCV6AhlWt": ("Autodidacte", "Tu gagnes la maîtrise d'une compétence au choix (déjà appliquée)."),
    "HbufUByLUsGAYYu3": ("Concentration inébranlable", "Tu gagnes un don au choix (déjà ajouté à ta fiche)."),
    "vBFiBGjqhfiusygI": ("Bosseur", "Tu gagnes plus d'argent de ton historique et ses deux bonus."),
    # Capacités d'historique
    "kgBQltygakR8Z1sT": ("Concentration et ténacité", "Tu sympathises vite avec les gens aussi travailleurs que toi et tu connais plein de livres d'entraînement."),
    "Zuxrk9eVPuDUV7uD": ("Pitoyable", "Les gens te pardonnent tes maladresses… par pitié."),
    "120D3JmCjUL6lRIZ": ("À la hauteur", "Après une première tentative face à un défi (réussie ou ratée), le MJ te donne un indice sur la manière de le surmonter."),
    "GpzJzxYe9vZAEHac": ("L'étrangère", "Ton accent et tes manières intriguent : les curieux veulent entendre tes histoires, ce qui t'ouvre des portes."),
    "Rl80ezLojwOsoWCj": ("Le nom du maître", "Le nom de ton maître (l'hôpital de Konoha) t'ouvre des portes auprès des ninjas et des temples."),
    # Postures et dons
    "IAEgy6JAlOt7zaIo": ("Posture du poing de fer", "Tes coups à mains nues font 1d6, et 1d8 avec des brassards de combat si tu utilises la Force. Dégâts doublés contre les objets et structures."),
    "W1TUDekIuPnH3ytk": ("Posture de lancer", "Tes armes de lancer reviennent dans ta main, et tu tires à longue portée sans désavantage. Après un tir réussi, avantage au corps à corps contre la même cible."),
    "sRoQ7vCFNbEleJDX": ("Vigilant", "+5 à l'initiative, tu ne peux pas être surpris, et tu sens les signes des mains lancés à moins de 18 m."),
    "Yeh4JFD3KNNC57po": ("Coup de main", "Tu peux utiliser l'action Aider en action bonus, de plus loin, et aider deux alliés à la fois."),
    # Techniques
    "q2WQkOpq8aKFxlko": ("Expansion partielle", "Ton bras grossit : tes coups à mains nues portent à 2 cases (3 m) et font 1d8. Payable en Calories."),
    "8eUQXRxm0FUtrfQS": ("Boulet humain", "Tu roules en boule sur 6 cases en ligne droite : 2d12 + Force à la cible, et 4d6 (sauvegarde de Dextérité pour moitié) aux créatures sur ton chemin."),
    "l0QX3psUUpyGVwi5": ("Poing de fer", "Attaque de taijutsu : dégâts à mains nues + 2d6, et la cible est projetée en arrière si elle rate une sauvegarde de Force."),
    "chWVfsHZGnobmVkF": ("Tourbillon de la feuille", "Balayage : sauvegarde de Dextérité ou la cible tombe à terre."),
    "n5ebCloneTech001": ("Technique du clonage", "Deux copies de toi apparaissent. En réaction, l'attaquant retire 1d6 à son jet (un clone disparaît)."),
    "n5ebTransform001": ("Technique de transformation", "Tu prends une autre apparence. +4 (ou +2 sans changement de voix) pour tromper quelqu'un."),
    "LCYW9NuTbdNEwNPQ": ("Katon : Boule de feu", "Boule de feu de 4,5 m de rayon à 18 m : 4d6+4 de feu, sauvegarde de Dextérité pour moitié."),
    "4nltiAgOOWDNDrxj": ("Katon : Trait de flamme", "Attaque de ninjutsu à distance : 3d10+3 de feu."),
    "K3rH0D6QyGgjQVvZ": ("Projectile de chakra", "Attaque de ninjutsu à distance : 3d6 de force (ou de feu pour un utilisateur de Katon)."),
    "n5ebJutsuSubst01": ("Technique de substitution", "Réaction quand tu vas subir des dégâts : +3 CA jusqu'à ton prochain tour ; si l'attaque rate, tu te déplaces de la moitié de ta vitesse."),
    "kxjJzHLePuiaDd6e": ("Possession de l'ombre", "Sauvegarde de Dextérité ou la cible est entravée et imite tes mouvements. Elle peut se libérer avec une sauvegarde de Force à son tour. Portée réduite dans la pénombre, impossible dans le noir."),
    "tiapKIdzyFd6Iew7": ("Silhouette d'ombre", "Ton ombre se dresse et prend ta forme pour faire diversion, même quand tu es caché."),
    "Odgir3CfeTCO2Ygp": ("Libération (Kai)", "Brise un genjutsu sur toi ou une cible : test d'Illusions avec avantage contre le DD du genjutsu."),
    "rJGBb5PfcuUcvhWf": ("Détection du chakra", "Pendant la durée, action bonus : test de Perception pour sentir le chakra des créatures à moins de 9 m."),
    "YKL7T1VtNVrJI7WB": ("Pluie céleste", "Tes armes retombent en pluie sur une zone : dégâts de l'arme + 1d10 et Saignement, sauvegarde de Constitution pour moitié."),
    "KrbXs6WAaGbjjq2L": ("Fente céleste", "Une ligne d'armes transperce tout : dégâts de l'arme + 2d8, sauvegarde de Dextérité pour moitié."),
    "IBwhzXtrBqVXsNv6": ("Tir double", "Ta prochaine attaque à distance ce tour-ci est doublée : une seconde attaque sur une autre cible."),
    "WonJOQgBwx9lGWIC": ("Piège à fil", "Piège dans une zone de 4,5 m : la créature qui entre fait une sauvegarde de Dextérité ou est entravée (sauvegarde de Force à chaque tour pour se libérer)."),
    "PPoAeuRgMFcZ5tFE": ("Iryô : Soin habile", "Action : 3d8 PV à une créature touchée. Action bonus : 8 PV à tous les alliés choisis à moins de 4,5 m. Tour complet : 3d8+5 PV à tous à moins de 9 m."),
    "xu4zHFDk38yJIy3L": ("Iryô : Vitalité", "Une créature touchée gagne 1d4 + ton modificateur en PV temporaires jusqu'à la fin de son prochain tour."),
    "OGpiNPXJvzamIOZA": ("Iryô : Élixir de soin", "Crée une fiole : boire (une action) rend 3d4+3 PV et soigne le poison ou 2 rangs de Saignement."),
    "32N0GDKp7H9HjA2N": ("Suiton : Brume cachée", "Un brouillard épais : on ne voit pas à plus de 1,5 m, désavantage pour attaquer. Le lanceur voit toujours la créature « marquée »."),
    "kWnb8fhy4e6N3tSh": ("Suiton : Shuriken d'eau", "Attaque de ninjutsu à distance : 4d4 de froid. Près d'un lac : une seconde attaque sur une autre cible."),
    "tC0Im49BgM14w91E": ("Suiton : Fouet d'eau", "Attaque de ninjutsu au corps à corps : 2d6 de froid, la cible est tirée de 3 m vers le lanceur."),
    # Équipement
    "RbcM59vdQ9ZgYBKV": ("Kunai", "Couteau ninja : corps à corps ou lancer (9 m / 18 m), 1d4 perforants."),
    "YReiEBmBtKhLaoxF": ("Shuriken", "Étoile de lancer ninja."),
    "AqeyHEGdWCFAqWP0": ("Senbon", "Fines aiguilles de lancer, idéales pour viser les points vitaux."),
    "HbrlOL6HWNiuNaiU": ("Tantô", "Petit sabre."),
    "TXvRdUiQQuxwTgyF": ("Fûma-shuriken", "Grand shuriken pliable du clan Fûma : gros dégâts à distance."),
    "7JdFwOiRWfq35OWT": ("Brassards de combat", "Protections d'avant-bras pour frapper plus fort à mains nues."),
    "uKuifTHmF5GNrmI3": ("Fil de combat", "Fil d'acier ninja pour attacher, piéger ou tirer."),
    "UGGW1wNtVXUSj9vL": ("Kusarigama", "Faucille reliée à une chaîne lestée."),
    "DSk0IwDZwsVVOMW0": ("Veste de combat", "Le gilet protecteur des ninjas (armure intermédiaire)."),
    "PXA5xkWhB5D1y2ZL": ("Tissu matelassé", "Vêtements renforcés (armure légère)."),
    "DiHt2oXGIiOv0VNf": ("Bombe fumigène", "Action : lance-la à 9 m, la fumée masque complètement une zone de 7,5 m de rayon."),
    "oNAY6p1RBBrDSaBH": ("Parchemin éclair", "Action : lance-le à 9 m, sauvegarde de Sagesse ou aveuglé jusqu'à la fin de son tour (3 m de rayon)."),
    "geBv2yJWYcICS06g": ("Pilule de sang", "Action bonus : regagne des PV."),
    "gsidqkpuoeCo7OCj": ("Pilule de chakra", "Action bonus : regagne du chakra."),
    "NijK86qNzaHagxIh": ("Trousse de médecine", "Pour stabiliser un blessé et soigner sans chakra."),
    "hJoSys7R14ImfKOs": ("Parchemin de jutsu (rang D)", None),
    "pkQ0PqJ3pPmphWBU": ("Jeu de poids d'entraînement", None),
    "JwGv4iXrtcoKT7Ak": ("Livres de stratégie d'entraînement", None),
    "jC6LbSiISA80tw54": ("Tenue d'entraînement", None),
    "n5ebWalletBasic0": ("Bourse", None),
    "xHE6XKVR38rZZeLV": ("Vêtements simples", None),
    "4tZVWFVUJyOMxQQU": ("Kit de faussaire", None),
    "mY7BwUCBHWmJkcrr": ("Bingo Book (carnet des ninjas recherchés)", None),
    "Xopd9t8Hlz7iJtW9": ("Parchemin vierge", None),
    "2tKNVlG8vOhOham6": ("Carte mal dessinée", None),
    "fCbwEbwS1LaS2qfq": ("Petit bijou", None),
    "0eMzz4NG8lzaDRJl": ("Parchemin explosif", "Un parchemin qui explose : à lancer, à poser en piège ou à attacher à une arme de lancer."),
    "uRGWwZOZgtHeKBbF": ("Livres d'enseignement", None),
    "hT4Gdr2lbrkoQpq9": ("Dernière lettre du maître", None),
    "bikW2HKpo0Bv77fZ": ("Rouleau", None),
}


def translations():
    out = {}
    for k, (name, summary) in TR.items():
        out[k] = {"name": name}
        if summary:
            out[k]["summary"] = summary
    return out


# --------------------------------------------------------------------------- #
#  Dossiers                                                                    #
# --------------------------------------------------------------------------- #

def folder(key, name, type_, color, parent=None, sort=0):
    return {"_id": folder_id(key), "name": name, "type": type_, "color": color,
            "folder": folder_id(parent) if parent else None, "sort": sort, "flags": FLAGS}


FOLDERS = [
    folder("actors", "Feux Follets de Kawabe", "Actor", "#7a2b1d"),
    folder("pj", "Prétirés", "Actor", "#2d6a4f", "actors", 1),
    folder("allies", "Alliés et villageois", "Actor", "#3a6ea5", "actors", 2),
    folder("ennemis", "Adversaires", "Actor", "#8b1e1e", "actors", 3),
    folder("items", "Feux Follets de Kawabe", "Item", "#7a2b1d"),
    folder("journal", "Feux Follets de Kawabe", "JournalEntry", "#7a2b1d"),
    folder("scenes", "Feux Follets de Kawabe", "Scene", "#7a2b1d"),
    folder("tables", "Feux Follets de Kawabe", "RollTable", "#7a2b1d"),
]


# --------------------------------------------------------------------------- #
#  Objets du scénario                                                          #
# --------------------------------------------------------------------------- #

def img(path):
    # Les illustrations finales WebP remplacent les SVG de travail sans modifier
    # les identifiants des acteurs, objets, pages ou scènes.
    if path.endswith(".svg"):
        final = os.path.splitext(path)[0] + ".webp"
        if os.path.isfile(os.path.join(MOD_DIR, final)):
            path = final
    return f"{WEB}/{path}"


def activity(key, type_, **data):
    aid = gid(f"act.{key}")
    base = {"_id": aid, "type": type_, "sort": 0}
    base.update(data)
    return {aid: base}


def world_item(key, name, type_, image, desc, system=None):
    sysdata = {"description": {"value": desc, "chat": ""}}
    sysdata.update(system or {})
    return {"_id": item_id(key), "name": name, "type": type_, "img": image, "folder": folder_id("items"),
            "system": sysdata, "flags": FLAGS}


ITEMS = [
    world_item("onigiri", "Onigiri de Sachi", "consumable", img("assets/items/onigiri.svg"),
               p("Une boule de riz encore tiède, avec une prune salée au milieu. Préparée par Sachi, l'aubergiste de Kawabe.",
                 "<strong>Action bonus :</strong> on mange l'onigiri et on regagne 1d4+1 PV. Pour Bunta, l'onigiri rend aussi 1 Calorie."),
               {"quantity": 5, "type": {"value": "food", "subtype": ""},
                "uses": {"max": "1", "spent": 0, "recovery": [], "autoDestroy": True},
                "activities": activity("onigiri.heal", "heal", name="Manger",
                                       activation={"type": "bonus", "value": 1},
                                       consumption={"targets": [{"type": "itemUses", "value": "1", "target": ""}]},
                                       healing={"number": 1, "denomination": 4, "bonus": "1", "types": ["healing"]},
                                       target={"affects": {"type": "self"}})}),
    world_item("talisman", "Talismans de luciole", "consumable", img("assets/items/talisman.svg"),
               p("Trois bandes de papier sacré couvertes d'écritures dorées, confiées par Ayame, la gardienne du sanctuaire.",
                 "<strong>Action :</strong> on lève le talisman et on le déchire. Une lumière douce de lucioles se répand à 6 m (4 cases) autour de soi : le brouillard (Brume cachée) se dissipe dans cette zone et tous les genjutsu sur les créatures de son choix dans la zone prennent fin (Effrayé par le Fantôme, par exemple).",
                 "Un talisman peut aussi servir à <strong>rallumer la lanterne du sanctuaire</strong> de l'île des Lucioles."),
               {"quantity": 1, "type": {"value": "trinket", "subtype": ""},
                "uses": {"max": "3", "spent": 0, "recovery": [], "autoDestroy": True},
                "activities": activity("talisman.use", "utility", name="Déchirer un talisman",
                                       activation={"type": "action", "value": 1},
                                       consumption={"targets": [{"type": "itemUses", "value": "1", "target": ""}]})}),
    world_item("senbon_poison", "Senbon empoisonnés", "consumable", img("assets/items/poison.svg"),
               p("Trois fines aiguilles enduites d'un poison verdâtre, récupérées sur les brigands de la Gorge.",
                 "<strong>Action :</strong> enduire une arme ou lancer une aiguille. La prochaine créature touchée fait une sauvegarde de Constitution DD 12 ou est <strong>Empoisonnée</strong> pendant 1 heure."),
               {"quantity": 3, "type": {"value": "poison", "subtype": ""}}),
    world_item("bandeau", "Morceau de bandeau rayé", "loot", img("assets/items/bandeau.svg"),
               p("Un morceau de bandeau frontal bleu foncé avec une plaque de métal. Le symbole (trois vagues) est celui de <strong>Kiri</strong>, le Village Caché de la Brume, rayé d'un grand trait : la marque d'un déserteur.",
                 "Aide de jeu : " + J("aides", "bandeau", "Bandeau rayé")),
               {"quantity": 1}),
    world_item("registre", "Registre de Kaneda", "loot", img("assets/items/registre.svg"),
               p("Un registre de comptes relié de cuir. Une page montre des paiements réguliers à un certain « U. » pour du « brouillard », et des achats de pelles et de cordes.",
                 "Aide de jeu : " + J("aides", "registre", "Page du registre")),
               {"quantity": 1}),
    world_item("carte_ile", "Plan de l'île", "loot", img("assets/items/carte_ile.svg"),
               p("Un plan grossier de l'île des Lucioles, avec une croix rouge près du vieux sanctuaire.",
                 "Aide de jeu : " + J("aides", "carte", "Plan de l'île")),
               {"quantity": 1}),
    world_item("tresor", "Trésor du seigneur Kagami", "loot", img("assets/items/tresor.svg"),
               p("Un coffre rempli de vieilles pièces d'or (l'équivalent de 50 000 ryôs) et un rouleau scellé : « Ce trésor appartient à Kawabe. Qu'il serve à reconstruire quand le malheur viendra. »",
                 "Il doit être rendu à la cheffe Oume."),
               {"quantity": 1, "price": {"value": 50000, "denomination": "ryo"}}),
    world_item("insigne", "Insigne de Kawabe", "loot", img("assets/items/insigne.svg"),
               p("Une petite luciole de bois sculpté, offerte par les habitants de Kawabe aux genin qui ont sauvé leur village.",
                 "Tant que vous la portez, les habitants de Kawabe vous accueilleront toujours comme des héros."),
               {"quantity": 1}),
]


# --------------------------------------------------------------------------- #
#  Acteurs                                                                     #
# --------------------------------------------------------------------------- #

def abilities(s, d, c, i, w, ch):
    return {k: {"value": v} for k, v in zip(["str", "dex", "con", "int", "wis", "cha"], [s, d, c, i, w, ch])}


def token(key, name, link=True, disposition=1):
    return {
        "name": name,
        "texture": {"src": img(f"assets/tokens/{key}.svg")},
        "actorLink": link,
        "disposition": disposition,
        "displayName": 30,
        "displayBars": 40 if link else 20,
        "bar1": {"attribute": "attributes.hp"},
        "bar2": {"attribute": "attributes.chakra"},
        "sight": {"enabled": False},
    }


def fiche_link(key, name):
    return f"<p>Fiche de présentation : {J('fiches', key, name)}</p>"


def pregen(key, name, abil, hp, chakra, build, bio, details, currency=50, ac=None):
    system = {
        "abilities": abil,
        "attributes": {"hp": {"value": hp}, "chakra": {"value": chakra}, "movement": {"walk": 30, "units": "ft"}},
        "details": {"biography": {"value": bio + fiche_link(key, name), "public": bio}, **details},
        "currency": {"ryo": currency},
    }
    if ac:
        system["attributes"]["ac"] = ac
    return {
        "_id": actor_id(key), "name": name, "type": "character", "img": img(f"assets/tokens/{key}.svg"),
        "folder": folder_id("pj"), "ownership": {"default": 2},
        "prototypeToken": token(key, name.split(" ", 1)[1]),
        "system": system, "flags": FLAGS, "items": [], "_build": build,
    }


def ref(uuid, quantity=None, equipped=None, **kw):
    r = {"uuid": uuid}
    if quantity is not None:
        r["quantity"] = quantity
    if equipped is not None:
        r["equipped"] = equipped
    r.update(kw)
    return r


ACADEMIE = [ref(JUT("n5ebCloneTech001")), ref(JUT("n5ebTransform001"))]

PREGENS = [
    pregen("bunta", "Akimichi Bunta", abilities(16, 13, 16, 8, 12, 10), hp=15, chakra=9,
           ac={"calc": "custom", "formula": "10 + @prof + @abilities.dex.mod"},
           build={"level": 1, "class": CLS("Ipg5bKh1zS3Yfn2I"), "race": CLAN("V9y2Nb2LH8qpEVyB"),
                  "background": BG("n5ebHardWork0001"),
                  "choices": ["skills:ccl", "skills:prc", "skills:ins"],
                  "items": [ref(CLAN("q2WQkOpq8aKFxlko")), ref(CLAN("8eUQXRxm0FUtrfQS")),
                            ref(JUT("l0QX3psUUpyGVwi5")), ref(JUT("chWVfsHZGnobmVkF")), *ACADEMIE,
                            ref(FEAT("IAEgy6JAlOt7zaIo")),
                            ref(ITM("7JdFwOiRWfq35OWT"), equipped=True), ref(ITM("RbcM59vdQ9ZgYBKV"), quantity=5),
                            ref(ITM("geBv2yJWYcICS06g"), quantity=1)]},
           bio=p("13 ans. Le plus grand et le plus large de sa promotion. Sa grand-mère tient un petit restaurant à Konoha ; il rêve de devenir le premier ninja-cuisinier célèbre du pays.",
                 "Calme, lent à parler, jamais lent à agir quand un ami est en danger. Il partage toujours sa nourriture.",
                 "<em>« Ventre plein, cœur vaillant ! »</em>"),
           details={"age": "13 ans", "gender": "Garçon", "hair": "Châtains, en épis", "eyes": "Marron",
                    "height": "1,70 m", "trait": "Calme et protecteur, partage toujours sa nourriture.",
                    "ideal": "Protéger les plus petits.", "bond": "Sa grand-mère et ses recettes.",
                    "flaw": "Ne supporte pas qu'on gaspille la nourriture."}),
    pregen("kaito", "Hibana Kaito", abilities(8, 14, 14, 17, 10, 12), hp=8, chakra=14,
           build={"level": 1, "class": CLS("n5ebNinSpec00001"), "race": CLAN("YWIfpZ862Gc9GfSA"),
                  "background": BG("JfooXW5qno1hSYX0"),
                  "choices": ["skills:ccl", "skills:prc", "skills:ste", "skills:inv", "skills:acr", "skills:itm", "skills:ath"],
                  "equip": ["PXA5xkWhB5D1y2ZL"],
                  "items": [ref(JUT("LCYW9NuTbdNEwNPQ")), ref(JUT("4nltiAgOOWDNDrxj")), ref(JUT("K3rH0D6QyGgjQVvZ")),
                            ref(JUT("n5ebJutsuSubst01")), *ACADEMIE, ref(FEAT("sRoQ7vCFNbEleJDX")),
                            ref(ITM("HbrlOL6HWNiuNaiU"), equipped=True), ref(ITM("RbcM59vdQ9ZgYBKV"), quantity=5)]},
           bio=p("12 ans. Sans clan, élevé par la boulangère de son quartier. Le meilleur de sa promotion en ninjutsu, maître du feu.",
                 "Bavard, fanfaron, fonce d'abord et réfléchit après. Au fond, il a peur de ne jamais être reconnu.",
                 "<em>« Une seule étincelle suffit pour allumer un grand feu. »</em>"),
           details={"age": "12 ans", "gender": "Garçon", "hair": "Rouges, ébouriffés", "eyes": "Ambre",
                    "height": "1,48 m", "trait": "Bavard et fanfaron.", "ideal": "Être reconnu par tout le village.",
                    "bond": "La boulangère qui l'a élevé.", "flaw": "Fonce sans réfléchir."}),
    pregen("shizuka", "Nara Shizuka", abilities(10, 14, 12, 17, 13, 9), hp=9, chakra=11,
           build={"level": 1, "class": CLS("6TxLk91QYckjBOY8"), "race": CLAN("oO0kK6HZshBbz7YP"),
                  "background": BG("n5ebGenius000001"),
                  "choices": ["skills:prc", "skills:ste", "skills:ccl", "skills:nat", "skills:ill", "skills:nsh", "skills:sur"],
                  "items": [ref(CLAN("kxjJzHLePuiaDd6e")), ref(CLAN("tiapKIdzyFd6Iew7")), ref(JUT("Odgir3CfeTCO2Ygp")),
                            ref(JUT("rJGBb5PfcuUcvhWf")), *ACADEMIE, ref(FEAT("W1TUDekIuPnH3ytk")),
                            ref(ITM("DSk0IwDZwsVVOMW0"), equipped=True),
                            ref(ITM("RbcM59vdQ9ZgYBKV"), quantity=5, equipped=True), ref(ITM("YReiEBmBtKhLaoxF"), quantity=10),
                            ref(ITM("DiHt2oXGIiOv0VNf"), quantity=1)]},
           bio=p("13 ans. Du clan Nara, célèbre pour ses stratèges et ses techniques d'ombre. Première aux examens écrits de l'Académie.",
                 "Calme, posée, un peu distante. Elle déteste se presser et les plans improvisés.",
                 "<em>« Laisse-moi réfléchir trois secondes. »</em>"),
           details={"age": "13 ans", "gender": "Fille", "hair": "Noirs, en queue de cheval haute", "eyes": "Gris",
                    "height": "1,55 m", "trait": "Observe tout, parle peu.", "ideal": "Un bon plan évite les blessures.",
                    "bond": "Son grand-père, qui lui a appris le shôgi.", "flaw": "Paralysée quand il faut improviser."}),
    pregen("tsumugi", "Fûma Tsumugi", abilities(14, 17, 13, 10, 13, 8), hp=11, chakra=9,
           build={"level": 1, "class": CLS("jBWRb3PE7vc3fiH5"), "race": CLAN("2QbtB7Qvz6uOOZVW"),
                  "background": BG("C0QdlDm3fhlaRFOV"),
                  "choices": ["skills:acr", "skills:ste", "skills:sur"],
                  "items": [ref(CLAN("YKL7T1VtNVrJI7WB")), ref(CLAN("KrbXs6WAaGbjjq2L")), ref(JUT("IBwhzXtrBqVXsNv6")),
                            ref(JUT("WonJOQgBwx9lGWIC")), *ACADEMIE,
                            ref(ITM("DSk0IwDZwsVVOMW0"), equipped=True), ref(ITM("TXvRdUiQQuxwTgyF"), equipped=True),
                            ref(ITM("YReiEBmBtKhLaoxF"), quantity=10, equipped=True), ref(ITM("RbcM59vdQ9ZgYBKV"), quantity=5),
                            ref(ITM("uKuifTHmF5GNrmI3"))]},
           bio=p("13 ans. Du clan Fûma, des ninjas voyageurs. Installée à Konoha depuis un an seulement, elle est encore « la nouvelle ».",
                 "Curieuse, souriante, raconte sans cesse des histoires de voyage. Elle collectionne les grelots et déteste rater une cible.",
                 "<em>« Je ne rate jamais. Enfin… presque jamais. »</em>"),
           details={"age": "13 ans", "gender": "Fille", "hair": "Brun clair, deux tresses avec des grelots", "eyes": "Verts",
                    "height": "1,52 m", "trait": "Curieuse et conteuse.", "ideal": "Trouver un endroit où elle se sent chez elle.",
                    "bond": "Le fûma-shuriken offert par sa mère.", "flaw": "Trop fière de sa précision."}),
    pregen("momo", "Sakuraba Momo", abilities(10, 12, 14, 13, 17, 10), hp=10, chakra=12,
           build={"level": 1, "class": CLS("55ZGaTkWJHT0mQmp"), "race": CLAN("YWIfpZ862Gc9GfSA"),
                  "background": BG("n5ebStudent00001"),
                  "choices": ["skills:ins", "skills:prc", "skills:per", "skills:ani", "skills:nat", "skills:ill"],
                  "items": [ref(JUT("PPoAeuRgMFcZ5tFE")), ref(JUT("xu4zHFDk38yJIy3L")), ref(JUT("OGpiNPXJvzamIOZA")),
                            ref(JUT("Odgir3CfeTCO2Ygp")), *ACADEMIE, ref(FEAT("Yeh4JFD3KNNC57po")),
                            ref(ITM("DSk0IwDZwsVVOMW0"), equipped=True),
                            ref(ITM("AqeyHEGdWCFAqWP0"), quantity=10, equipped=True), ref(ITM("RbcM59vdQ9ZgYBKV"), quantity=3),
                            ref(ITM("geBv2yJWYcICS06g"), quantity=3)]},
           bio=p("12 ans. Fille d'une infirmière de l'hôpital de Konoha, elle veut devenir ninja médecin. Secret : elle a peur du sang.",
                 "Douce et timide, mais têtue comme une mule quand il s'agit de soigner.",
                 "<em>« Personne ne meurt pendant ma garde. »</em>"),
           details={"age": "12 ans", "gender": "Fille", "hair": "Roses, coupés au carré", "eyes": "Noisette",
                    "height": "1,45 m", "trait": "Douce, timide, têtue.", "ideal": "Sauver tout le monde.",
                    "bond": "Sa mère infirmière.", "flaw": "A peur du sang (et le cache)."}),
]


def npc(key, name, folder_key, abil, hp, ac, cr, bio, *, chakra=0, link=True, disposition=-1,
        skills=(), items=(), features=(), speed=30):
    system = {
        "abilities": abil,
        "attributes": {"hp": {"value": hp, "max": hp, "formula": ""}, "ac": {"calc": "flat", "flat": ac},
                       "chakra": {"value": chakra, "max": chakra}, "movement": {"walk": speed, "units": "ft"}},
        "details": {"cr": cr, "biography": {"value": bio, "public": ""}, "type": {"value": "humanoid", "subtype": ""}},
        "traits": {"size": "med", "languages": {"value": ["common"]}},
        "skills": {s: {"value": 1} for s in skills},
        "currency": {"ryo": 0},
    }
    return {
        "_id": actor_id(key), "name": name, "type": "npc", "img": img(f"assets/tokens/{key}.svg"),
        "folder": folder_id(folder_key), "ownership": {"default": 0},
        "prototypeToken": token(key, name, link=link, disposition=disposition),
        "system": system, "flags": FLAGS, "items": list(features),
        "_build": {"items": list(items)} if items else None,
    }


def feature(key, name, desc, image=None, activities=None):
    it = {"_id": gid(f"feat.{key}"), "name": name, "type": "feat", "img": image or img("assets/items/capacite.svg"),
          "system": {"description": {"value": desc, "chat": ""}, "type": {"value": "monster", "subtype": ""}}}
    if activities:
        it["system"]["activities"] = activities
    return it


def attack_act(key, name, ability, kind, number, denom, dtype, rng=None, bonus="@mod"):
    data = dict(name=name, activation={"type": "action", "value": 1},
                attack={"ability": ability, "bonus": "", "flat": False, "type": {"value": kind, "classification": "weapon"}},
                damage={"includeBase": False, "parts": [{"number": number, "denomination": denom, "bonus": bonus, "types": [dtype]}]})
    if rng:
        data["range"] = {"override": True, "value": str(rng), "units": "ft"}
    return activity(key, "attack", **data)


def save_act(key, name, ability, dc, activation="action", **extra):
    return activity(key, "save", name=name, activation={"type": activation, "value": 1},
                    save={"ability": [ability], "dc": {"calculation": "", "formula": str(dc)}}, **extra)


NPCS = [
    npc("shuhei", "Inaba Shûhei", "allies", abilities(12, 15, 14, 14, 12, 13), 38, 14, 3,
        p("Chûnin de Konoha, 24 ans, chef d'escouade de la mission. Optimiste, rate tous ses proverbes.",
          "Empoisonné à l'acte 1, il reste à l'auberge de Kawabe et sert de « joker » au MJ (conseils, renfort d'urgence)."),
        chakra=30, disposition=1, skills=("prc", "nsh", "ccl"),
        items=[ref(ITM("RbcM59vdQ9ZgYBKV"), quantity=5, equipped=True), ref(JUT("LCYW9NuTbdNEwNPQ"))],
        features=[feature("shuhei.poison", "Empoisonné (acte 1)",
                          p("Depuis l'embuscade du pont, Shûhei est empoisonné : il ne peut pas combattre normalement.",
                            "Renfort d'urgence (voir « Ajuster la difficulté ») : une seule fois, il peut lancer une Boule de feu avant de s'évanouir."))]),
    npc("oume", "Grand-mère Oume", "allies", abilities(6, 8, 10, 14, 16, 14), 6, 10, 0,
        p("Cheffe du village de Kawabe, 74 ans. Autoritaire, fume la pipe, tape sa canne par terre quand elle s'énerve."),
        disposition=1, skills=("ins", "his", "per")),
    npc("sachi", "Sachi", "allies", abilities(11, 12, 12, 11, 13, 14), 8, 10, 0,
        p("Aubergiste du Héron, 40 ans. Bavarde, débrouillarde, connaît tous les ragots."), disposition=1, skills=("ins",)),
    npc("tetsu", "Tetsu", "allies", abilities(7, 14, 10, 10, 12, 12), 4, 11, 0,
        p("8 ans, fils de pêcheur. Seul témoin à avoir vu le fantôme sans masque. Veut devenir ninja."),
        disposition=1, skills=("ste", "prc"), speed=25),
    npc("genji", "Le vieux Genji", "allies", abilities(12, 10, 12, 10, 13, 8), 9, 10, 0,
        p("Pêcheur, 65 ans. Bourru, honnête. On lui a volé deux barques."), disposition=1, skills=("sur", "nat")),
    npc("ayame", "Ayame", "allies", abilities(9, 12, 10, 12, 15, 13), 6, 10, 0,
        p("Gardienne du petit sanctuaire, 16 ans. Douce et rêveuse, connaît la légende du seigneur Kagami."),
        disposition=1, skills=("his", "ins", "ill")),
    npc("kaneda", "Kaneda Jûbei", "ennemis", abilities(9, 10, 10, 14, 11, 15), 9, 10, 0,
        p("Marchand de riz de Sakaimachi. Sourire mielleux, bagues à tous les doigts. Le commanditaire du « fantôme ». Ne combat pas."),
        disposition=0, skills=("dec", "per", "ins")),
    npc("mosuke", "Mosuke", "allies", abilities(8, 11, 10, 13, 10, 9), 5, 10, 0,
        p("Commis de Kaneda. Peureux, honteux, avoue tout à la première menace."), disposition=0, skills=("inv",)),
    npc("brigand", "Brigand de la Gorge", "ennemis", abilities(12, 14, 12, 9, 10, 9), 13, 12, 0.25,
        p("Un voyou engagé par Gonza. Lâche : s'enfuit souvent quand il est à moitié de ses PV."),
        link=False, skills=("ste", "itm"),
        items=[ref(ITM("HbrlOL6HWNiuNaiU"), equipped=True), ref(ITM("RbcM59vdQ9ZgYBKV"), quantity=3, equipped=True)],
        features=[feature("brigand.lache", "Lâche",
                          p("Quand il tombe à 6 PV ou moins, ou quand son chef s'enfuit, le brigand essaie de fuir. S'il est coincé, il se rend."))]),
    npc("gonza", "Tonbi Gonza", "ennemis", abilities(13, 15, 14, 10, 11, 10), 30, 13, 1,
        p("Chef des brigands, « le Milan ». Ancien élève de l'Académie qui n'a jamais réussi l'examen de genin. Ricane, se croit malin, fuit quand ça tourne mal."),
        chakra=10, skills=("ste", "prc", "dec"),
        items=[ref(ITM("UGGW1wNtVXUSj9vL"), equipped=True), ref(ITM("DiHt2oXGIiOv0VNf"), quantity=1)],
        features=[
            feature("gonza.multi", "Attaques multiples", p("Gonza fait deux attaques : deux avec sa kusarigama, ou deux senbon empoisonnés.")),
            feature("gonza.senbon", "Senbon empoisonnés",
                    p("<strong>Attaque à distance :</strong> +4 au toucher, portée 9 m (6 cases). 1d4+2 perforants.",
                      "La cible fait une sauvegarde de Constitution DD 12 ou elle est <strong>Empoisonnée</strong> jusqu'à la fin du combat."),
                    img("assets/items/poison.svg"),
                    {**attack_act("gonza.senbon.atk", "Lancer un senbon", "dex", "ranged", 1, 4, "piercing", rng=30),
                     **save_act("gonza.senbon.save", "Poison (sauvegarde)", "con", 12, activation="special")}),
            feature("gonza.fuite", "Fuite du Milan",
                    p("Quand ses brigands sont hors de combat ou qu'il tombe à 10 PV ou moins, Gonza lance sa bombe fumigène (action bonus) et s'enfuit en courant sur les parois grâce au chakra.")),
        ]),
    npc("clone", "Clone d'eau", "ennemis", abilities(12, 14, 10, 10, 10, 10), 1, 12, 0,
        p("Une copie d'Uramaru faite d'eau. Elle éclate en une gerbe d'eau au premier coup reçu."),
        link=False, skills=("ath",),
        items=[ref(ITM("RbcM59vdQ9ZgYBKV"), quantity=1, equipped=True)],
        features=[feature("clone.sbire", "Sbire",
                          p("Le clone a 1 PV : n'importe quelle attaque réussie ou sauvegarde ratée le détruit. Il ne peut pas lancer de techniques."),
                          img("assets/items/eau.svg")),
                  feature("clone.saisir", "Saisir",
                          p("<strong>Action :</strong> le clone attrape une créature de taille moyenne ou plus petite à côté de lui. Deux clones ensemble peuvent emporter un enfant (4 cases par tour). Toucher un des clones libère la victime."),
                          img("assets/items/eau.svg"))]),
    npc("uramaru", "Uramaru Hisame", "ennemis", abilities(12, 16, 14, 15, 13, 12), 60, 14, 3,
        p("Ancien chûnin de Kiri, déserteur, 30 ans. Cheveux gris-bleu, cicatrice au menton, masque blanc et cape claire pour jouer le « Fantôme du Lac ».",
          "Calme et méprisant. Il veut l'or du trésor et compte se débarrasser de Kaneda."),
        chakra=30, skills=("ste", "dec", "ccl", "ill", "nsh"),
        items=[ref(ITM("RbcM59vdQ9ZgYBKV"), quantity=6, equipped=True),
               ref(JUT("32N0GDKp7H9HjA2N")), ref(JUT("kWnb8fhy4e6N3tSh")), ref(JUT("tC0Im49BgM14w91E")), ref(JUT("n5ebJutsuSubst01"))],
        features=[
            feature("uramaru.multi", "Attaques multiples", p("Uramaru fait deux attaques de kunai, <strong>ou</strong> une attaque de kunai et lance une technique.")),
            feature("uramaru.clones", "Clones d'eau (Mizu Bunshin)",
                    p("<strong>Action bonus (recharge 5-6) :</strong> deux " + "clones d'eau" + " sortent de l'eau ou du brouillard à côté d'Uramaru (utilisez l'acteur « Clone d'eau »). Jamais plus de 4 clones en même temps. Au premier round du combat final, la technique est disponible."),
                    img("assets/items/eau.svg")),
            feature("uramaru.feux", "Genjutsu des feux follets",
                    p("<strong>Action (une fois par nuit) :</strong> toutes les créatures de son choix qui le voient, à moins de 18 m, font une sauvegarde de Sagesse DD 12 ou sont <strong>Effrayées</strong> pendant 1 minute (nouvelle sauvegarde à la fin de chacun de leurs tours). La technique Libération (Kai) ou un talisman de luciole met fin à l'effet."),
                    img("assets/items/lumiere.svg"),
                    save_act("uramaru.feux.save", "Terreur du lac", "wis", 12)),
            feature("uramaru.eau", "Marche sur l'eau", p("Uramaru marche sur l'eau comme sur la terre ferme.")),
            feature("uramaru.fuite", "Déserteur prudent",
                    p("À 20 PV ou moins, Uramaru attrape le sac d'or et court vers le lac pour s'enfuir. Il ne se bat jusqu'au bout que s'il est coincé.")),
        ]),
]

ACTORS = PREGENS + NPCS


# --------------------------------------------------------------------------- #
#  Journaux                                                                    #
# --------------------------------------------------------------------------- #

def text_page(jkey, pkey, name, html, sort):
    return {"_id": page_id(jkey, pkey), "name": name, "type": "text", "sort": sort,
            "title": {"show": False, "level": 1}, "text": {"content": html, "format": 1}}


def image_page(jkey, pkey, name, src, caption, sort):
    return {"_id": page_id(jkey, pkey), "name": name, "type": "image", "sort": sort, "src": img(src),
            "title": {"show": True, "level": 1}, "image": {"caption": caption}}


def journal(key, name, pages, default_ownership=0, sort=0):
    return {"_id": journal_id(key), "name": name, "folder": folder_id("journal"), "sort": sort,
            "ownership": {"default": default_ownership}, "flags": FLAGS, "pages": pages}


def text_journal(key, name, entries, ownership=0, sort=0):
    return journal(key, name, [text_page(key, k, n, h, (i + 1) * 100000) for i, (k, n, h) in enumerate(entries)],
                   ownership, sort)


JOURNALS = [
    text_journal("lisezmoi", "00 · Lisez-moi (MJ)", LISEZMOI, sort=100),
    text_journal("scenario", "01 · Scénario — Les Feux Follets de Kawabe", SCENARIO, sort=200),
    text_journal("pnj", "02 · Personnages non-joueurs", PNJ, sort=300),
    journal("aides", "03 · Aides de jeu (à montrer aux joueurs)",
            [image_page("aides", k, n, src, cap, (i + 1) * 100000) for i, (k, n, src, cap) in enumerate(AIDES)], sort=400),
    text_journal("guide", "04 · Guide du joueur", GUIDE, ownership=2, sort=500),
    text_journal("fiches", "05 · Fiches des prétirés", FICHES, ownership=2, sort=600),
]


# --------------------------------------------------------------------------- #
#  Tables                                                                      #
# --------------------------------------------------------------------------- #

RUMEURS = [
    "« Le fantôme, c'est l'esprit du seigneur Kagami qui protège son trésor ! » (à moitié vrai : il y a bien un trésor)",
    "« Kaneda achète toutes les terres. Il paraît qu'il paie bien… enfin, pas si bien que ça. » (vrai)",
    "« Les lumières bleues sentent l'huile brûlée, comme une lampe. » (vrai : ce sont des lanternes)",
    "« Le vieux Genji jure que le fantôme lui a volé ses barques. Un fantôme qui a besoin d'une barque ? » (vrai)",
    "« Tetsu dit qu'il a vu le fantôme sans masque, mais personne ne le croit. » (vrai)",
    "« Le fantôme mange les enfants qui sortent la nuit ! » (faux)",
    "« Des hommes armés campaient près de la Gorge, la semaine dernière. » (vrai : les brigands de Gonza)",
    "« La petite Ayame parle aux lucioles. Elle dit qu'elles reviendront quand on rallumera la lanterne. » (vrai, d'une certaine façon…)",
]

TABLES = [{
    "_id": table_id("rumeurs"), "name": "Rumeurs de Kawabe", "folder": folder_id("tables"),
    "img": "icons/svg/d20-grey.svg", "formula": "1d8", "replacement": True, "displayRoll": True,
    "description": "Ce que racontent les habitants de Kawabe (et Sachi, l'aubergiste).",
    "flags": FLAGS,
    "results": [{"_id": gid(f"rumeur.{i}"), "type": "text", "name": f"Rumeur {i + 1}", "description": r,
                 "range": [i + 1, i + 1], "weight": 1, "drawn": False} for i, r in enumerate(RUMEURS)],
}]


# --------------------------------------------------------------------------- #
#  Scènes                                                                      #
# --------------------------------------------------------------------------- #

def tok(key, c, r, hidden=False):
    return {"actor": actor_id(key), "x": int(c * art.G), "y": int(r * art.G), "hidden": hidden}


def note(jkey, pkey, n, c, r, text):
    return {"entryId": journal_id(jkey), "pageId": page_id(jkey, pkey), "x": int(c * art.G), "y": int(r * art.G),
            "texture": {"src": img(f"assets/icons/note-{n}.svg")}, "iconSize": 64, "text": text, "fontSize": 28}


def scene(key, name, bg, w, h, grid=True, darkness=0.0, tokens=(), notes=(), sort=0):
    return {
        "_id": scene_id(key), "name": name, "folder": folder_id("scenes"), "sort": sort, "navigation": True,
        "navOrder": sort, "background": {"src": img(bg)}, "width": w, "height": h, "padding": 0,
        "grid": {"type": 1 if grid else 0, "size": art.G, "distance": 5, "units": "ft",
                 "color": "#000000", "alpha": 0.15},
        "tokenVision": False, "fog": {"exploration": False},
        "environment": {"darknessLevel": darkness},
        "flags": FLAGS, "_tokens": list(tokens), "notes": list(notes),
    }


PJ_KEYS = ["bunta", "kaito", "shizuka", "tsumugi", "momo"]

SCENES = [
    scene("voyage", "0 · Carte du voyage", "assets/maps/carte-voyage.webp", 2400, 1600, grid=False, sort=1,
          notes=[note("scenario", "prologue", 1, 2.4, 6.4, "Prologue : Konoha"),
                 note("scenario", "acte1", 2, 11.4, 6.2, "Acte 1 : le pont"),
                 note("scenario", "acte2", 3, 16.2, 7.6, "Acte 2 : Kawabe"),
                 note("scenario", "acte4", 4, 21.1, 9.5, "Acte 4 : l'île")]),
    scene("pont", "1 · Le Pont de la Gorge", "assets/maps/pont-gorge.webp", 3000, 2000, sort=2,
          tokens=[*(tok(k, 2 + (i % 3), 9 + (i // 3)) for i, k in enumerate(PJ_KEYS)),
                  tok("shuhei", 14, 9),
                  tok("gonza", 22, 9, hidden=True), tok("brigand", 19, 7, hidden=True), tok("brigand", 8, 6, hidden=True)],
          notes=[note("scenario", "acte1", 1, 15, 12, "L'embuscade")]),
    scene("village", "2 · Le village de Kawabe", "assets/maps/village-kawabe.webp", 4000, 3000, sort=3,
          tokens=[*(tok(k, 1 + (i % 3), 14 + (i // 3)) for i, k in enumerate(PJ_KEYS)),
                  tok("oume", 16, 13), tok("sachi", 8, 13.6), tok("tetsu", 20, 16), tok("genji", 31, 16),
                  tok("ayame", 8, 25), tok("kaneda", 25, 9), tok("mosuke", 24, 9),
                  tok("clone", 31, 22, True), tok("clone", 32, 24, True), tok("clone", 33, 20, True),
                  tok("clone", 31, 26, True), tok("uramaru", 36, 23, True)],
          notes=[note("scenario", "lieu1", 1, 9, 9.3, "1. L'auberge du Héron"),
                 note("scenario", "lieu2", 2, 18.5, 5.8, "2. La maison de la cheffe"),
                 note("scenario", "lieu3", 3, 20.5, 13.2, "3. La place et le puits"),
                 note("scenario", "lieu4", 4, 25.5, 2.3, "4. L'entrepôt de Kaneda"),
                 note("scenario", "lieu5", 5, 33, 15.4, "5. Le ponton de Genji"),
                 note("scenario", "lieu6", 6, 5.7, 21.3, "6. Le petit sanctuaire"),
                 note("scenario", "lieu7", 7, 20, 23.3, "7. Les rizières"),
                 note("scenario", "lieu8", 8, 3.5, 2.3, "8. Maisons abandonnées"),
                 note("scenario", "acte3", 9, 34, 25, "Acte 3 : la nuit")]),
    scene("ile", "3 · L'île des Lucioles (nuit)", "assets/maps/ile-lucioles.webp", 3600, 3000, darkness=0.45, sort=4,
          tokens=[*(tok(k, 6 + (i % 2), 13 + i) for i, k in enumerate(PJ_KEYS)),
                  tok("uramaru", 26, 18), tok("brigand", 21, 16), tok("brigand", 25, 21.4),
                  tok("kaneda", 22.4, 19.2), tok("gonza", 16, 8.6, hidden=True), tok("tetsu", 18.5, 8, hidden=True)],
          notes=[note("scenario", "ile1", 1, 7.5, 10.5, "1. La plage"),
                 note("scenario", "ile2", 2, 13, 12.2, "2. Le torii"),
                 note("scenario", "ile3", 3, 16.1, 11.6, "3. Le camp"),
                 note("scenario", "ile4", 4, 26.8, 8.6, "4. Le vieux sanctuaire"),
                 note("scenario", "ile5", 5, 23.5, 22, "5. La fosse au trésor")]),
]


# --------------------------------------------------------------------------- #
#  Visuels                                                                     #
# --------------------------------------------------------------------------- #

TOKENS = {
    "bunta": ("BU", "Bunta", "#b5651d", "秋道"), "kaito": ("KA", "Kaito", "#d03a1f", "火花"),
    "shizuka": ("SH", "Shizuka", "#3d4a5c", "奈良"), "tsumugi": ("TS", "Tsumugi", "#2f7d6d", "風魔"),
    "momo": ("MO", "Momo", "#d977a0", "桜庭"), "shuhei": ("IS", "Shûhei", "#4f7a3a", "因幡"),
    "oume": ("OU", "Oume", "#7a6a8a", "梅"), "sachi": ("SA", "Sachi", "#a36a3f", "幸"),
    "tetsu": ("TE", "Tetsu", "#5b8bb5", "鉄"), "genji": ("GE", "Genji", "#6d5a43", "源"),
    "ayame": ("AY", "Ayame", "#c43c4b", "菖蒲"), "kaneda": ("KJ", "Kaneda", "#b8962e", "金田"),
    "mosuke": ("MS", "Mosuke", "#8a8f6a", "茂助"), "brigand": ("BR", "Brigand", "#5a4b3c", "賊"),
    "gonza": ("TG", "Gonza", "#6b5b4b", "鳶"), "clone": ("CE", "Clone", "#4f8fbf", "水"),
    "uramaru": ("UH", "Fantôme", "#e8eef2", "霧"),
}
HOSTILE = {"brigand", "gonza", "clone", "uramaru"}
ITEM_ICONS = {
    "onigiri": ("飯", "#6b8f3a"), "talisman": ("札", "#b8962e"), "bandeau": ("霧", "#26324a"),
    "registre": ("帳", "#7a4b2a"), "carte_ile": ("図", "#8a6a3a"), "tresor": ("宝", "#b4231e"),
    "insigne": ("蛍", "#3a6ea5"), "poison": ("毒", "#4a7a2a"), "eau": ("水", "#3a7ab5"),
    "lumiere": ("灯", "#5a4a8a"), "capacite": ("技", "#555555"),
}


def build_art():
    manifest = os.path.join(MOD_DIR, "assets", "art-manifest.json")
    if os.path.isfile(manifest):
        with open(manifest, encoding="utf-8") as f:
            assets = json.load(f)["assets"]
        missing = [a["path"] for a in assets
                   if not os.path.isfile(os.path.join(MOD_DIR, a["path"]))]
        if missing:
            raise FileNotFoundError("Illustrations finales manquantes : " + ", ".join(missing))
        print(f"Illustrations finales conservées : {len(assets)} fichiers.")
        return
    raise FileNotFoundError("assets/art-manifest.json absent : exécutez python tools/final_art.py pour restaurer les illustrations finales.")


def build_placeholder_art():
    """Ancien générateur, conservé comme référence ; refuse d'écraser l'art final."""
    if os.path.isfile(os.path.join(MOD_DIR, "assets", "art-manifest.json")) or os.path.isfile(os.path.join(MOD_DIR, "assets", "tokens", "bunta.webp")):
        raise RuntimeError("Les illustrations finales ne doivent pas être remplacées par des visuels provisoires.")
    a = os.path.join(MOD_DIR, "assets")
    art.map_travel(os.path.join(a, "maps", "carte-voyage.webp"))
    art.map_bridge(os.path.join(a, "maps", "pont-gorge.webp"))
    art.map_village(os.path.join(a, "maps", "village-kawabe.webp"))
    art.map_island(os.path.join(a, "maps", "ile-lucioles.webp"))
    for key, (ini, name, color, kanji) in TOKENS.items():
        art.token_svg(os.path.join(a, "tokens", f"{key}.svg"), ini, name, color, kanji, hostile=key in HOSTILE)
    # Le fantôme : jeton clair, texte foncé lisible quand même (contour noir)
    for n in range(1, 10):
        art.note_icon_svg(os.path.join(a, "icons", f"note-{n}.svg"), n)
    for key, (glyph, color) in ITEM_ICONS.items():
        art.item_icon_svg(os.path.join(a, "items", f"{key}.svg"), glyph, color)
    h = os.path.join(a, "handouts")
    os.makedirs(h, exist_ok=True)
    art.handout_svg(os.path.join(h, "ordre-mission.svg"), "Ordre de mission — Rang D", [
        "**Village Caché de la Feuille — Bureau des missions",
        "",
        "**Client : la cheffe Oume, village de Kawabe",
        "(au bord du lac Kagami, à un jour et demi à l'est).",
        "",
        "**Demande :",
        "« Un fantôme hante notre lac chaque nuit. Il fait",
        "fuir nos familles. Envoyez-nous des ninjas pour",
        "le chasser et rassurer le village. »",
        "",
        "**Équipe : Inaba Shûhei (chûnin, chef)",
        "Akimichi Bunta · Hibana Kaito · Nara Shizuka",
        "Fûma Tsumugi · Sakuraba Momo",
        "",
        "**Paiement : 15 000 ryôs.",
        "__Départ immédiat. Bonne chance !",
    ], height=1000, seal="火")
    art.handout_svg(os.path.join(h, "legende-kagami.svg"), "La légende du seigneur Kagami", [
        "Il y a deux cents ans, quand la guerre approchait,",
        "le bon seigneur Kagami rassembla l'or du village",
        "et le cacha sur l'île au milieu du lac.",
        "",
        "Sur son sanctuaire, il posa une lanterne de pierre",
        "et demanda aux lucioles de veiller sur l'île.",
        "",
        "« Tant que la lanterne brillera, les lucioles",
        "danseront. Et quand Kawabe sera dans le malheur,",
        "l'or qui dort sous la lanterne l'aidera. »",
        "",
        "__Depuis bien des années, plus personne n'allume",
        "__la lanterne… et les lucioles ont disparu.",
    ], height=820, seal="鏡")
    art.handout_svg(os.path.join(h, "registre-kaneda.svg"), "Registre de Kaneda — dépenses", [
        "**Mois du Héron",
        "3e jour — Pelles (6), cordes (4) .......... 1 200 ryôs",
        "5e jour — U., 1er versement (brouillard) ... 20 000 ryôs",
        "9e jour — Terres de la famille Hoshi ...... 8 000 ryôs",
        "11e jour — U., 2e versement (brouillard) .. 20 000 ryôs",
        "12e jour — Terres des familles Mori, Ida .. 15 000 ryôs",
        "14e jour — Brigands de G. (la Gorge) ...... 1 500 ryôs",
        "15e jour — Terres des familles Sato, Ueno 12 000 ryôs",
        "",
        "__Dans la marge, d'une écriture pressée :",
        "« U. dit qu'il faut encore trois nuits.",
        "Le coffre est sous la lanterne. Ne rien dire",
        "à Mosuke. » — et un dessin de l'île.",
    ], height=820)
    art.handout_headband(os.path.join(h, "bandeau-kiri.svg"))
    art.handout_island_map(os.path.join(h, "plan-ile.svg"))


# --------------------------------------------------------------------------- #
#  Assemblage                                                                  #
# --------------------------------------------------------------------------- #

def main():
    build_art()
    actors = []
    for a in ACTORS:
        a = dict(a)
        if not a.get("_build"):
            a.pop("_build", None)
        actors.append(a)
    data = {
        "version": "1.0.0",
        "welcome": journal_id("lisezmoi"),
        "translations": translations(),
        "folders": FOLDERS,
        "items": ITEMS,
        "actors": actors,
        "journals": JOURNALS,
        "tables": TABLES,
        "scenes": SCENES,
    }
    out = os.path.join(MOD_DIR, "data", "adventure.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    print(f"OK : {len(actors)} acteurs, {len(ITEMS)} objets, {len(JOURNALS)} journaux, "
          f"{sum(len(j['pages']) for j in JOURNALS)} pages, {len(SCENES)} scènes -> {out}")


if __name__ == "__main__":
    main()
