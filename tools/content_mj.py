"""Journaux du MJ : Lisez-moi, scénario complet, PNJ."""
from ids import A, I, J, S, T, SK, SV, box

SC = "scenario"   # clé du journal scénario
PN = "pnj"        # clé du journal PNJ
AJ = "aides"      # clé du journal aides de jeu
LM = "lisezmoi"


def p(*paras):
    return "".join(f"<p>{x}</p>" for x in paras)


def ul(*items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def ol(*items):
    return "<ol>" + "".join(f"<li>{x}</li>" for x in items) + "</ol>"


def table(head, *rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="ffk-table"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


# =========================================================================== #
#  00 · LISEZ-MOI                                                             #
# =========================================================================== #

LISEZMOI = [
    ("bienvenue", "Bienvenue, MJ !", f"""
<h1>Les Feux Follets de Kawabe</h1>
<p class="ffk-subtitle">One-shot N5eB · 5 genin de niveau 1 · 3 à 4 heures · idéal pour débuter</p>
{p("Ce module contient <strong>tout ce qu'il faut</strong> pour faire jouer une mission ninja complète, même si c'est votre première fois derrière l'écran : histoire, cartes, personnages prêts à jouer, adversaires, aides de jeu et objets.")}
<h2>L'histoire en deux phrases</h2>
{p("Le petit village de pêcheurs de Kawabe est hanté chaque nuit par un « fantôme du lac ». Les jeunes genin découvrent que le fantôme est en réalité un <strong>ninja déserteur</strong> payé par un <strong>marchand avide</strong> pour faire fuir les habitants et s'emparer d'un trésor caché sur une île.")}
<h2>Avant la partie (15 minutes)</h2>
{ol(
    "Lisez la page " + J(SC, "resume", "Résumé de l'histoire") + " : c'est la seule page à connaître par cœur.",
    "Parcourez rapidement les actes 1 à 4. Les encadrés colorés vous disent quoi lire, quoi faire et quand lancer les dés.",
    "Faites choisir un prétiré à chaque joueur (le journal <em>05 · Fiches des prétirés</em> est visible par les joueurs), puis donnez-leur la propriété de leur personnage : clic droit sur l'acteur → <em>Configurer les droits</em> → Propriétaire.",
    "Ouvrez la scène " + S("voyage", "Carte du voyage") + " pour commencer. Les autres scènes sont prêtes, avec les PNJ déjà placés (les adversaires sont cachés jusqu'au bon moment).",
    "Gardez sous la main le journal " + J(PN, "resume", "02 · Personnages non-joueurs") + " et la table " + T("rumeurs", "Rumeurs de Kawabe") + ".",
)}
<h2>Contenu du module</h2>
{table(["Type", "Contenu"],
    ["Prétirés", "5 genin de Konoha, niveau 1, fiches complètes (classe, clan, historique, techniques, équipement)"],
    ["PNJ", "Le chûnin Inaba Shûhei, les villageois de Kawabe, le marchand Kaneda"],
    ["Adversaires", "Brigands, Tonbi Gonza, les clones d'eau et Uramaru « le Fantôme du Lac »"],
    ["Scènes", "Carte du voyage · Le Pont de la Gorge · Le village de Kawabe · L'île des Lucioles"],
    ["Journaux", "Lisez-moi · Scénario · PNJ · Aides de jeu · Guide du joueur · Fiches des prétirés"],
    ["Objets", "Indices, talismans de luciole, onigiri, récompenses"],
    ["Table", "Rumeurs de Kawabe (1d8)"],
)}
{box("tip", p("Les noms des techniques et des capacités venant du système sont affichés en <strong>français suivi de l'anglais</strong>, par exemple « Katon : Boule de feu (Fire Release Fireball) ». Chaque description commence par un résumé « En bref » en français, suivi du texte officiel en anglais."))}
{box("rule", p("Le système N5eB est basé sur D&amp;D 5e. Les fiches affichent donc les compétences en anglais : la page " + J(LM, "regles", "Le jeu en 5 minutes") + " donne la traduction."))}
"""),
    ("regles", "Le jeu en 5 minutes", f"""
<h1>Le jeu en 5 minutes</h1>
<h2>Le principe : 1d20 + bonus</h2>
{p("Quand un personnage tente quelque chose de difficile, il lance <strong>un dé à 20 faces</strong> et ajoute le bonus indiqué sur sa fiche. S'il atteint ou dépasse le <strong>DD</strong> (degré de difficulté), c'est réussi.")}
{table(["Difficulté", "DD"], ["Facile", "10"], ["Moyenne", "12-13"], ["Difficile", "15"], ["Très difficile", "18"])}
{p("<strong>Avantage</strong> : on lance deux d20 et on garde le meilleur. <strong>Désavantage</strong> : on garde le pire. Donnez l'avantage quand les joueurs ont une bonne idée !")}
<h2>Les compétences (anglais → français)</h2>
{table(["Sur la fiche", "En français", "Exemple"],
    ["Perception", "Perception", "repérer un ennemi caché"],
    ["Investigation", "Investigation", "fouiller un bureau, analyser des traces"],
    ["Insight", "Intuition", "savoir si quelqu'un ment"],
    ["Stealth", "Discrétion", "se faufiler sans bruit"],
    ["Persuasion / Intimidation / Deception", "Persuasion / Intimidation / Tromperie", "convaincre, menacer, mentir"],
    ["Athletics / Acrobatics", "Athlétisme / Acrobaties", "nager, grimper / garder l'équilibre"],
    ["Chakra Control", "Contrôle du chakra", "marcher sur l'eau, résister à l'épuisement"],
    ["Ninshou", "Ninshō", "connaissances sur les ninjas et les techniques"],
    ["Illusions", "Illusions", "reconnaître ou briser un genjutsu"],
    ["Martial Arts", "Arts martiaux", "prises, projections, combat à mains nues"],
    ["Medicine / Survival / History", "Médecine / Survie / Histoire", "soigner / pister / se souvenir d'une légende"],
)}
<h2>Le combat</h2>
{ol(
    "Tout le monde lance l'<strong>initiative</strong> (bouton dans le Combat Tracker). On joue dans l'ordre, du plus haut au plus bas.",
    "À son tour, un personnage peut <strong>se déplacer</strong> (6 cases en général), faire <strong>une action</strong> (attaquer, lancer une technique, aider, se cacher…) et parfois une <strong>action bonus</strong>.",
    "Une <strong>réaction</strong> par round permet de répondre au tour d'un autre (exemple : la Technique de substitution).",
    "Pour toucher : 1d20 + bonus d'attaque contre la <strong>CA</strong> (classe d'armure) de la cible.",
    "À 0 points de vie (PV), un personnage tombe inconscient et fait des <strong>jets contre la mort</strong>. Un soin le relève immédiatement.",
)}
<h2>Le chakra et les techniques</h2>
{p("Chaque technique (jutsu) coûte des <strong>points de chakra</strong>, indiqués sur sa fiche. Le système les déduit automatiquement quand on l'utilise. À court de chakra, on se bat avec ses armes et sa tête !",
   "Les techniques ont un <strong>rang</strong> : E (très simple), D (genin), C, B, A, S (légendaire). Nos héros connaissent des techniques de rang E et D.",
   "<strong>Repos court</strong> (1 heure) : on peut dépenser des dés de vie (PV) et des dés de chakra pour récupérer. <strong>Repos long</strong> (une nuit) : on récupère tout.")}
<h2>Les états les plus utilisés dans ce scénario</h2>
{table(["Sur la fiche", "En français", "Effet simple"],
    ["Restrained", "Entravé", "vitesse 0, désavantage pour attaquer, on l'attaque avec avantage"],
    ["Prone", "À terre", "il faut utiliser du mouvement pour se relever"],
    ["Frightened", "Effrayé", "désavantage tant que la source de la peur est visible, ne peut pas s'en approcher"],
    ["Poisoned", "Empoisonné", "désavantage aux attaques et aux tests"],
    ["Blinded", "Aveuglé", "rate automatiquement ce qui demande la vue, désavantage pour attaquer"],
    ["Bleeding", "Saignement", "perd des PV à chaque tour jusqu'à être soigné"],
)}
{box("tip", p("La <strong>Volonté du Feu</strong> (le système l'affiche à la place de l'Inspiration) : quand un joueur fait quelque chose de courageux, drôle ou très « ninja », donnez-lui un point. Il pourra le dépenser pour obtenir l'avantage sur un jet. Maximum 3."))}
"""),
    ("conseils", "Conseils pour débuter", f"""
<h1>Conseils pour un premier MJ</h1>
{ul(
    "<strong>Vous n'avez pas besoin de tout savoir.</strong> En cas de doute sur une règle, décidez vite et gardez le rythme. Notez la question pour plus tard.",
    "<strong>Dites oui aux bonnes idées.</strong> Un genin qui se transforme en marchand pour entrer dans l'entrepôt ? Excellent ! Donnez un bonus ou l'avantage.",
    "<strong>Faites parler les PNJ.</strong> Chaque PNJ a une petite manie (voir le journal PNJ). Une voix, un geste, ça suffit.",
    "<strong>Partagez la lumière.</strong> Chaque prétiré a un moment où il brille (voir ci-dessous). Demandez souvent : « Et toi, que fais-tu ? »",
    "<strong>Personne n'est obligé de mourir.</strong> C'est une première mission : si un personnage tombe, il est assommé, pas tué (sauf si votre table préfère le danger).",
    "<strong>Les indices ne doivent jamais bloquer.</strong> Si les joueurs passent à côté d'un indice, un PNJ le leur donne. Voir " + J(SC, "indices", "Les indices") + ".",
)}
<h2>Le moment de gloire de chaque prétiré</h2>
{table(["Prétiré", "Il / elle brille quand…"],
    [A("bunta", "Akimichi Bunta"), "il protège les autres en combat, il soulève, pousse, enfonce une porte"],
    [A("kaito", "Hibana Kaito"), "il faut des dégâts : ses techniques de feu sont redoutables"],
    [A("shizuka", "Nara Shizuka"), "il faut immobiliser un ennemi (Possession de l'ombre) ou réfléchir à un plan"],
    [A("tsumugi", "Fûma Tsumugi"), "il faut toucher de loin, poser un piège, repérer un détail"],
    [A("momo", "Sakuraba Momo"), "quelqu'un est blessé, empoisonné, ou sous l'effet d'une illusion"],
)}
<h2>Rythme conseillé</h2>
{table(["Partie", "Durée", "Contenu"],
    ["Prologue", "15 min", "Présentation des personnages, ordre de mission"],
    ["Acte 1", "40 min", "Voyage et embuscade au pont (combat d'apprentissage)"],
    ["Acte 2", "60 min", "Enquête au village (indices, PNJ)"],
    ["Acte 3", "30 min", "La nuit des feux follets (genjutsu, clones d'eau)"],
    ["Acte 4", "50 min", "L'île des Lucioles (combat final)"],
    ["Épilogue", "10 min", "La fête des lanternes"],
)}
"""),
]


# =========================================================================== #
#  01 · SCÉNARIO                                                              #
# =========================================================================== #

SCENARIO = [
    ("resume", "Résumé de l'histoire", f"""
<h1>Résumé de l'histoire</h1>
{box("secret", p(
    "<strong>Ce qui se passe vraiment.</strong> Il y a deux cents ans, le seigneur Kagami a caché le trésor du village de Kawabe sous le vieux sanctuaire de l'<strong>île des Lucioles</strong>, au milieu du lac. Depuis, les villageois respectent l'île et n'y vont jamais.",
    "Il y a un mois, <strong>Kaneda Jûbei</strong>, un riche marchand de riz de la ville voisine, a trouvé un vieux plan de l'île. Il veut le trésor… et toutes les terres du village, qui sont les meilleures rizières de la région. Pour ça, il faut que les habitants partent.",
    "Il a engagé <strong>Uramaru Hisame</strong>, un ninja déserteur du Village Caché de la Brume (Kiri). Chaque nuit, Uramaru fait monter un brouillard magique, allume de faux feux follets bleus et plonge les villageois dans un genjutsu de terreur : c'est le « Fantôme du Lac ». Terrifiées, six familles ont déjà vendu leurs terres à Kaneda pour presque rien.",
    "La cheffe du village a envoyé une demande d'aide à Konoha. Uramaru l'a appris : il a payé des brigands, menés par <strong>Tonbi Gonza</strong>, pour arrêter les ninjas en chemin.",
    "Ce que Kaneda ignore : Uramaru compte bien <strong>garder le trésor pour lui</strong> et se débarrasser du marchand dès que le coffre sera sorti de terre."))}
<h2>Le déroulé</h2>
{table(["", "Où", "Ce qui se passe", "Scène"],
    ["Prologue", "Konoha", "Le chûnin Inaba Shûhei confie la mission : « chasser un fantôme » (rang D).", S("voyage", "Carte du voyage")],
    ["Acte 1", "Le Pont de la Gorge", "Embuscade de brigands. Shûhei est empoisonné : les genin sont seuls aux commandes.", S("pont", "Le Pont de la Gorge")],
    ["Acte 2", "Kawabe", "Enquête : le fantôme est un ninja, un déserteur de Kiri, payé par Kaneda.", S("village", "Le village de Kawabe")],
    ["Acte 3", "Kawabe, la nuit", "Le brouillard et les feux follets attaquent. Les genin brisent l'illusion et repoussent les clones d'eau.", S("village", "Le village de Kawabe")],
    ["Acte 4", "L'île des Lucioles", "Uramaru trahit Kaneda et s'empare du trésor. Combat final.", S("ile", "L'île des Lucioles")],
    ["Épilogue", "Kawabe", "La fête des lanternes : le village est sauvé.", ""],
)}
<h2>L'objectif des personnages</h2>
{ol("Découvrir qui est le Fantôme du Lac.", "Protéger les villageois.", "Arrêter le déserteur et rendre le trésor au village.")}
{box("tip", p("Si vous ne retenez qu'une chose : <strong>le fantôme est un ninja, le marchand est le commanditaire, le trésor est sur l'île.</strong> Tout le reste peut s'improviser."))}
"""),

    ("prologue", "Prologue : l'ordre de mission", f"""
<h1>Prologue : l'ordre de mission</h1>
<p><em>Konoha, le Village Caché de la Feuille. Un matin de fin d'été.</em></p>
{box("read", p(
    "Le soleil n'est levé que depuis une heure, mais le bureau des missions est déjà plein de bruit : des ninjas pressés, des piles de rouleaux, l'odeur du thé trop infusé.",
    "Vos senseis sont tous partis en mission longue. Alors, ce matin, on vous a réunis — cinq genin qui ne se connaissent pas tous très bien — devant un jeune chûnin aux cheveux en bataille et au gilet vert mal fermé.",
    "« Salut, les petits ! Je suis Inaba Shûhei, et pour les prochains jours, c'est moi votre chef. On a une mission de rang D : un village de pêcheurs, Kawabe, dit qu'il est hanté par un fantôme. Sûrement des gamins qui font des farces… Mais un client est un client ! Allez, présentez-vous. »"))}
<h2>1. Les présentations</h2>
{p("Demandez à chaque joueur de présenter son personnage en trois phrases : son nom, son apparence, et une chose qu'il veut prouver. Les fiches des prétirés donnent des idées. Shûhei réagit à chacun avec bonne humeur et un proverbe un peu raté (« Comme on dit : qui va lentement… arrive en retard ! »).")}
<h2>2. L'ordre de mission</h2>
{p("Shûhei tend l'ordre de mission. Montrez l'aide de jeu " + J(AJ, "ordre", "Ordre de mission") + " aux joueurs (bouton <em>Montrer aux joueurs</em> en haut de la page).")}
<h2>3. Questions des joueurs</h2>
{table(["Si les joueurs demandent…", "Shûhei répond…"],
    ["Où est Kawabe ?", "« À un jour et demi de marche vers l'est, au bord du lac Kagami. On passe par le Pont de la Gorge. »"],
    ["C'est dangereux ?", "« Un fantôme ? Pff. Les fantômes, ça n'existe pas. Enfin… je crois. »"],
    ["Combien ça paie ?", "« 15 000 ryôs pour l'équipe. C'est une mission de rang D, ne rêvez pas. »"],
    ["Qui a envoyé la demande ?", "« La cheffe du village, une certaine grand-mère Oume. Elle a payé avec les économies du village. »"],
)}
{box("tip", p("Montrez ensuite la scène " + S("voyage", "Carte du voyage") + " et passez à l'acte 1. Le prologue ne doit pas durer plus d'un quart d'heure."))}
"""),

    ("acte1", "Acte 1 : Le Pont de la Gorge", f"""
<h1>Acte 1 : Le Pont de la Gorge</h1>
<h2>La route (5 minutes)</h2>
{p("Le premier jour se passe sans problème. Le soir, autour du feu de camp, demandez à chaque joueur : <em>« Qu'est-ce que ton personnage raconte aux autres ce soir ? »</em> C'est l'occasion de jouer les liens entre personnages (voir les fiches des prétirés).")}
<h2>L'embuscade</h2>
{p("Ouvrez la scène " + S("pont", "Le Pont de la Gorge") + ". Placez les jetons des personnages à gauche de la carte, sur la route.")}
{box("read", p(
    "Le deuxième jour, vers midi, la route plonge dans une forêt épaisse et s'arrête net au bord d'une gorge profonde. Tout en bas, une rivière gronde. Un vieux pont de cordes et de planches se balance doucement au-dessus du vide.",
    "« Bon, un par un, et on ne regarde pas en bas ! » lance Shûhei en s'avançant sur le pont. Il n'a pas fait trois pas qu'un sifflement fend l'air. Shûhei porte la main à son cou, arrache une fine aiguille… et s'effondre à genoux sur les planches.",
    "De l'autre côté de la gorge, un homme maigre au long manteau gris se dresse sur un rocher. « Désolé, les mioches. Personne ne va à Kawabe. »"))}
{box("fight", p(
    "<strong>Adversaires :</strong> " + A("gonza", "Tonbi Gonza") + " (de l'autre côté du pont) et deux " + A("brigand", "brigands") + " : l'un caché derrière un rocher côté Kawabe, l'autre caché dans les arbres <em>derrière</em> les personnages (il surgit au premier round). Les jetons sont déjà placés et cachés : révélez-les au bon moment (clic droit → icône œil).",
    "<strong>Shûhei</strong> est empoisonné et à genoux au milieu du pont : il ne combat pas.",
    "<strong>Difficulté :</strong> facile. C'est le combat d'apprentissage : prenez le temps d'expliquer le tour de jeu (déplacement, action, action bonus)."))}
<h3>Tactique des ennemis</h3>
{ul(
    "<strong>Round 1 :</strong> Gonza lance ses senbon empoisonnés sur le personnage le plus proche du pont. Le brigand caché dans les arbres attaque le personnage le plus isolé (souvent celui qui soigne ou qui lance des techniques).",
    "<strong>Ensuite :</strong> les brigands frappent au tanto. Gonza utilise sa kusarigama (portée 3 cases) depuis le bout du pont.",
    "<strong>Fuite :</strong> quand les deux brigands sont hors de combat <em>ou</em> que Gonza tombe à 10 PV ou moins, il lance une bombe fumigène, saute dans la gorge en courant sur la paroi grâce au chakra, et crie : « Vous ne savez pas dans quoi vous mettez les pieds ! » Il reviendra à l'acte 4.",
)}
<h3>Le pont</h3>
{ul(
    "Traverser le pont en courant : " + SK("acr", 10) + ". En cas d'échec, le personnage tombe à terre sur les planches (pas dans le vide).",
    "Un personnage poussé ou projeté hors du pont peut se rattraper aux cordes avec une " + SV("dex", 12) + ". Sinon, il tombe dans la rivière : 3d6 dégâts, puis " + SK("ath", 12) + " pour nager jusqu'à la rive (il revient au combat 2 rounds plus tard).",
    "Couper les cordes du pont est une très mauvaise idée : Shûhei est dessus !",
)}
<h2>Après le combat</h2>
{p("Shûhei est pâle, en sueur, et son cou a gonflé. Un test de " + SK("med", 12) + " (ou une technique de soin de Momo) permet de ralentir le poison : il pourra marcher, lentement. Sans soin, il faut le porter (Bunta s'en charge sans problème).")}
{box("read", p("« Ce n'étaient pas… des voleurs ordinaires, souffle Shûhei. Ils nous attendaient. Votre mission vient de changer, les enfants. Si quelqu'un paie des brigands pour arrêter des ninjas… ce fantôme n'est pas une farce. Vous allez devoir prendre la tête. Moi… je vais faire une petite sieste. »"))}
<h3>Interroger un brigand</h3>
{p("Un brigand capturé parle facilement : " + SK("itm", 10) + " ou " + SK("per", 10) + ". Il sait que :")}
{ul(
    "« Un type nous a payés 300 ryôs chacun pour arrêter les ninjas de Konoha qui iraient à Kawabe. »",
    "« Gonza le connaît bien. Le type a un bandeau de ninja, mais avec le symbole rayé. Il ne parle que de l'île. »",
    "« Il fait froid quand il est là. Et il y a toujours du brouillard. »",
)}
{p("<strong>Butin :</strong> 60 ryôs et l'objet " + I("senbon_poison", "Senbon empoisonnés") + " (3 aiguilles).")}
{box("tip", p("Shûhei devient votre <strong>joker</strong> : installé à l'auberge de Kawabe, il peut donner un conseil quand les joueurs sont bloqués. Il ne participe plus aux combats (sauf si vous avez besoin d'un coup de main, voir " + J(SC, "difficulte", "Ajuster la difficulté") + ")."))}
"""),

    ("acte2", "Acte 2 : Kawabe, le village qui se vide", f"""
<h1>Acte 2 : Kawabe, le village qui se vide</h1>
{p("Ouvrez la scène " + S("village", "Le village de Kawabe") + ". Les numéros sur la carte correspondent aux lieux décrits dans les pages suivantes (double-cliquez sur une épingle de la carte pour ouvrir la page).")}
{box("read", p(
    "En fin d'après-midi, la forêt s'ouvre sur un grand lac aussi lisse qu'un miroir. Au bord, un village de maisons basses aux toits de tuiles rouges, des rizières vertes et un petit ponton de bois.",
    "Mais quelque chose cloche. La moitié des maisons ont leurs volets cloués. Pas un enfant ne joue dehors. Sur la place, une petite vieille appuyée sur une canne vous regarde arriver en tirant sur sa longue pipe.",
    "« Konoha ? Enfin ! Je suis Oume, la cheffe de ce village. Ou de ce qu'il en reste… »"))}
<h2>Ce que raconte la cheffe Oume</h2>
{ul(
    "« Depuis deux semaines, chaque nuit, un brouillard monte du lac. Des lumières bleues dansent au-dessus de l'eau. Puis le fantôme apparaît : une silhouette blanche, avec un masque, qui marche sur le lac. »",
    "« Il dit : <em>Partez, ou le lac vous engloutira.</em> Et ceux qui le regardent voient des choses horribles. Ils se réveillent le matin en pleurant. »",
    "« Six familles sont déjà parties. Elles ont toutes vendu leurs terres au même homme : Kaneda Jûbei, un marchand de riz. Il est si gentil… il paie même nos dettes. »",
    "« On a aussi volé deux barques au vieux Genji. »",
)}
<h2>L'arrivée de Kaneda</h2>
{p("Pendant la discussion, " + A("kaneda", "Kaneda Jûbei") + " arrive « par hasard », en souriant de toutes ses dents. Il est très aimable, offre des gâteaux de riz, et glisse : « Ce fantôme est dangereux, vous savez. Vous êtes si jeunes… Vous devriez rentrer chez vous. Moi, je ne fais qu'aider ces pauvres gens en rachetant leurs terres. » Un test d'" + SK("ins", 12) + " révèle qu'il est nerveux et qu'il regarde souvent l'île au milieu du lac.")}
<h2>L'enquête</h2>
{p("Les joueurs sont libres d'aller où ils veulent. Ils peuvent se séparer en petits groupes : c'est même conseillé, chacun aura son moment. Les lieux sont décrits dans les pages <em>Lieu 1</em> à <em>Lieu 8</em>, et le tableau " + J(SC, "indices", "Les indices") + " résume ce qu'on peut trouver.")}
{table(["N°", "Lieu", "PNJ", "Indice"],
    ["1", J(SC, "lieu1", "L'auberge du Héron"), "Sachi, Shûhei", "Rumeurs"],
    ["2", J(SC, "lieu2", "La maison de la cheffe"), "Oume", "Toutes les terres vendues à Kaneda"],
    ["3", J(SC, "lieu3", "La place et le puits"), "Tetsu", "A : le fantôme est un homme"],
    ["4", J(SC, "lieu4", "L'entrepôt de Kaneda"), "Mosuke", "C : le registre et la carte"],
    ["5", J(SC, "lieu5", "Le ponton de Genji"), "Genji", "A : traces de chakra sur l'eau"],
    ["6", J(SC, "lieu6", "Le petit sanctuaire"), "Ayame", "D : la légende, les talismans"],
    ["7", J(SC, "lieu7", "Les rizières"), "—", "B : le bandeau de Kiri"],
    ["8", J(SC, "lieu8", "Les maisons abandonnées"), "—", "E : les fausses lanternes"],
)}
{box("tip", p("Quand les joueurs ont trouvé 2 ou 3 indices, ou après environ une heure de jeu, la nuit tombe : passez à l'" + J(SC, "acte3", "acte 3") + ". Pas besoin d'avoir tout découvert !"))}
"""),

    ("lieu1", "Lieu 1 : L'auberge du Héron", f"""
<h1>Lieu 1 : L'auberge du Héron</h1>
{box("read", p("Une grande salle sombre qui sent le poisson grillé et la soupe miso. Des tables vides. Derrière le comptoir, une femme aux manches retroussées essuie le même bol depuis cinq minutes."))}
{p(A("sachi", "Sachi") + ", l'aubergiste, est la seule à ne pas avoir peur… ou presque. Elle offre une chambre gratuite aux ninjas (« Vous êtes mes seuls clients depuis dix jours ! ») et installe Shûhei dans un lit.")}
{ul(
    "<strong>Rumeurs :</strong> Sachi connaît tous les ragots. Lancez sur la table " + T("rumeurs", "Rumeurs de Kawabe") + " une ou deux fois.",
    "<strong>Ce qu'elle a vu :</strong> « Le fantôme ne vient jamais jusqu'ici, toujours du côté du lac. Et vous savez quoi ? Le brouillard sent le sel. Comme la mer. Alors que notre lac est d'eau douce. » (Un test de " + SK("nsh", 12) + " : les ninjas de Kiri, le Village de la Brume, sont célèbres pour leurs techniques de brouillard.)",
    "<strong>Repos :</strong> c'est ici que les personnages peuvent faire un repos court ou long.",
)}
{p("Sachi offre à l'équipe des " + I("onigiri", "onigiri de Sachi") + " pour la route (un par personnage).")}
"""),

    ("lieu2", "Lieu 2 : La maison de la cheffe", f"""
<h1>Lieu 2 : La maison de la cheffe Oume</h1>
{box("read", p("La plus grande maison du village. Des tatamis usés, un autel familial, une odeur de tabac. Sur la table basse, un grand registre du village est ouvert."))}
{p(A("oume", "La grand-mère Oume") + " montre volontiers le registre du village : il reste 9 familles sur 15. Les six familles parties ont toutes vendu à Kaneda, et toujours <strong>le lendemain d'une nuit de fantôme</strong>.")}
{ul(
    "Un test d'" + SK("inv", 10) + " : toutes les terres vendues entourent le ponton et donnent sur l'île. Kaneda achète les terres les plus proches de l'île en premier.",
    "« L'île des Lucioles ? Personne n'y va. C'est un lieu sacré. Le vieux sanctuaire du seigneur Kagami est là-bas. Demandez à la petite Ayame, au sanctuaire du village. »",
    "Si on lui parle du bandeau de Kiri ou du registre de Kaneda, elle tape sa canne par terre : « Ce serpent ! Il a payé un ninja pour nous faire peur ? »",
)}
"""),

    ("lieu3", "Lieu 3 : La place et le puits", f"""
<h1>Lieu 3 : La place du village et le puits</h1>
{box("read", p("Une place de terre battue autour d'un vieux puits de pierre. Un petit garçon, seul, lance des cailloux dans le seau. Il sursaute en vous voyant."))}
{p(A("tetsu", "Tetsu") + ", 8 ans, est le seul témoin à avoir vu le fantôme de près. Personne ne le croit, alors il ne veut plus en parler. Il faut gagner sa confiance : " + SK("per", 10) + ", ou une bonne idée (un tour de Transformation, un bonbon, jouer avec lui) fonctionne automatiquement.")}
{box("clue", p("<strong>Indice A — le fantôme est un homme.</strong> « Je l'ai vu ! Il marchait sur l'eau, puis il a trébuché et son masque est tombé. Il avait un visage normal ! Avec une cicatrice ici (il montre son menton). Après, il est monté dans la barque de papi Genji et il a ramé vers l'île. »"))}
{p("Tetsu est important pour l'acte 3 : le fantôme sait qu'il l'a vu sans masque et voudra l'enlever.")}
"""),

    ("lieu4", "Lieu 4 : L'entrepôt de Kaneda", f"""
<h1>Lieu 4 : L'entrepôt de riz de Kaneda</h1>
{box("read", p("Un long bâtiment neuf, avec un petit quai sur le lac. Des sacs de riz s'empilent devant la porte. Un jeune homme maigre à lunettes fait les cent pas en se rongeant les ongles."))}
{p(A("mosuke", "Mosuke") + ", le commis de Kaneda, garde l'entrée. Kaneda lui-même est souvent à l'intérieur, dans son bureau, ou se promène dans le village.")}
<h2>Entrer dans le bureau</h2>
{ul(
    "<strong>Par la ruse :</strong> se transformer en Kaneda (Technique de transformation) et entrer : " + SK("dec", 12) + " (le bonus de +4 de la Transformation s'applique).",
    "<strong>En douce :</strong> passer par la fenêtre arrière pendant que quelqu'un occupe Mosuke : " + SK("ste", 13) + ". Ouvrir le tiroir fermé : " + SK("slt", 12) + " (ou le forcer bruyamment).",
    "<strong>Par la peur :</strong> Mosuke est terrifié par le fantôme et par son patron. " + SK("itm", 12) + " ou " + SK("per", 13) + " : il craque et apporte lui-même le registre. « Je ne voulais pas ! Le patron a dit que personne ne serait blessé ! »",
)}
{box("clue", p("<strong>Indice C — le registre et la carte.</strong> Dans le tiroir, le " + I("registre", "registre de Kaneda") + " (voir l'aide de jeu " + J(AJ, "registre", "Page du registre") + ") montre des paiements réguliers à un certain « U. » pour du « brouillard », ainsi que l'achat de pelles et de cordes. Glissé dedans, un " + I("carte_ile", "plan de l'île") + " avec une croix près du sanctuaire (aide de jeu " + J(AJ, "carte", "Plan de l'île") + ")."))}
{p("Si les personnages se font prendre, Kaneda les met dehors en criant au scandale… et prévient Uramaru, qui sera plus méfiant à l'acte 4 (pas d'effet de surprise possible).")}
"""),

    ("lieu5", "Lieu 5 : Le ponton de Genji", f"""
<h1>Lieu 5 : Le ponton et la maison de Genji</h1>
{box("read", p("Un ponton de bois qui avance sur le lac. Au bout, une seule barque est attachée. Assis sur un tonneau, un vieil homme ridé recoud un filet en grognant."))}
{p(A("genji", "Le vieux Genji") + " est bourru mais honnête. « Mes deux barques ! Volées par le fantôme ! Il ne me reste que celle-là. »")}
{box("clue", p(
    "<strong>Indice A — traces sur l'eau.</strong> Au bout du ponton, " + SK("prc", 12) + " : des empreintes de pieds mouillées s'arrêtent au bord… et de légers ronds sur l'eau continuent vers l'île, comme si quelqu'un avait marché dessus.",
    "Un test de " + SK("ccl", 12) + " ou de " + SK("nsh", 10) + " confirme : c'est la technique de la <strong>marche sur l'eau</strong>. Le fantôme est un ninja !"))}
{p("Genji accepte de prêter sa dernière barque pour aller sur l'île si on lui promet de lui ramener les deux autres.")}
"""),

    ("lieu6", "Lieu 6 : Le petit sanctuaire", f"""
<h1>Lieu 6 : Le petit sanctuaire</h1>
{box("read", p("Sur une petite colline, un portail rouge (un torii) et un minuscule sanctuaire de bois. Une jeune fille en habit blanc et rouge balaie des feuilles qui n'existent pas, juste pour s'occuper les mains."))}
{p(A("ayame", "Ayame") + ", 16 ans, est la gardienne du sanctuaire. Elle connaît la légende du seigneur Kagami (montrez l'aide de jeu " + J(AJ, "legende", "La légende du seigneur Kagami") + "). Un test d'" + SK("his", 10) + " permet aussi de se souvenir de cette histoire.")}
{box("clue", p(
    "<strong>Indice D — la légende.</strong> « Le seigneur Kagami a caché le trésor du village sur l'île, sous la lanterne de son sanctuaire. Quand le village est en danger, le trésor doit l'aider. Mais depuis des années, plus personne n'allume la lanterne… et les lucioles ont disparu de l'île. »"))}
<h2>Les talismans de luciole</h2>
{p("Si les personnages promettent de protéger le village, Ayame leur confie trois " + I("talisman", "talismans de luciole") + ", des papiers sacrés de son grand-père. « Ils chassent la brume et les mauvais rêves. »")}
{box("tip", p("Les talismans sont la <strong>solution</strong> au brouillard d'Uramaru. Si les joueurs ne viennent pas au sanctuaire, Ayame peut les trouver à l'auberge, ou les donner après l'acte 3."))}
"""),

    ("lieu7", "Lieu 7 : Les rizières", f"""
<h1>Lieu 7 : Les rizières</h1>
{box("read", p("De grands carrés d'eau où pousse le riz, séparés par de petits talus de terre. Côté lac, les roseaux sont hauts et couchés par endroits, comme si quelqu'un y était passé souvent."))}
{box("clue", p(
    "<strong>Indice B — le bandeau de Kiri.</strong> En suivant le chemin écrasé dans les roseaux (" + SK("sur", 12) + " ou " + SK("inv", 12) + "), on trouve accroché à une branche un " + I("bandeau", "morceau de bandeau frontal") + " (aide de jeu " + J(AJ, "bandeau", "Bandeau rayé") + ").",
    "Un test de " + SK("nsh", 10) + " : le symbole (trois vagues) est celui de Kiri, le Village Caché de la Brume. Le grand trait qui le raye signifie que son propriétaire est un <strong>déserteur</strong>, un ninja qui a trahi son village."))}
"""),

    ("lieu8", "Lieu 8 : Les maisons abandonnées", f"""
<h1>Lieu 8 : Les maisons abandonnées</h1>
{box("read", p("Les maisons des familles parties. Volets cloués, jardins envahis d'herbes. Dans l'une d'elles, la porte n'est pas fermée."))}
{box("clue", p(
    "<strong>Indice E — les fausses lanternes.</strong> " + SK("inv", 10) + " : dans le grenier, quelqu'un a laissé des lanternes de papier bleu, des cerfs-volants noirs et un pot d'huile qui brûle avec une flamme bleue. Les « feux follets » sont des lanternes accrochées à des cerfs-volants, tirés depuis des barques !",
    "Des traces de bottes et des restes de repas : les brigands de Gonza ont dormi ici."))}
"""),

    ("indices", "Les indices", f"""
<h1>Les indices</h1>
{p("Les joueurs n'ont pas besoin de tout trouver. Voici ce qu'il faut absolument qu'ils comprennent avant l'acte 4, et comment les aider s'ils passent à côté.")}
{table(["Indice", "Ce que ça prouve", "Où", "Si les joueurs le ratent…"],
    ["A", "Le fantôme est un homme, un ninja", "Tetsu (3), le ponton (5)", "L'acte 3 le montre de toute façon : le fantôme lance des techniques ninja."],
    ["B", "C'est un déserteur de Kiri", "Les rizières (7)", "Shûhei reconnaît le brouillard de Kiri quand on lui décrit l'acte 3."],
    ["C", "Kaneda le paie ; ils fouillent l'île", "L'entrepôt (4)", "À l'acte 3, on voit Kaneda ramer en secret vers l'île."],
    ["D", "Le trésor est sous la lanterne de l'île", "Le sanctuaire (6)", "Ayame vient trouver les héros à l'auberge."],
    ["E", "Les feux follets sont des lanternes", "Maisons abandonnées (8)", "Pas indispensable, c'est un bonus."],
)}
{box("tip", p("La règle d'or : <strong>un indice raté ne bloque jamais l'histoire</strong>. Il devient juste plus tard, ou c'est un PNJ qui l'apporte."))}
"""),

    ("acte3", "Acte 3 : La nuit des feux follets", f"""
<h1>Acte 3 : La nuit des feux follets</h1>
{p("Restez sur la scène " + S("village", "Le village de Kawabe") + ". Baissez la lumière de la scène pour faire nuit (configuration de la scène → <em>Éclairage</em> → Obscurité vers 0,6).")}
{box("read", p(
    "La nuit est tombée. Les villageois se sont enfermés chez eux. Seuls les grillons chantent… puis se taisent d'un coup.",
    "Un brouillard blanc et froid monte du lac et avance sur le village comme une vague lente. Au-dessus de l'eau, des lumières bleues s'allument une à une et se mettent à danser.",
    "Une voix glaciale semble venir de partout à la fois : « Partez… ou le lac vous engloutira tous. »",
    "Et là-bas, sur la surface noire du lac, une silhouette blanche au visage masqué avance… en marchant sur l'eau."))}
<h2>1. Le genjutsu de terreur</h2>
{p("Chaque personnage qui voit le fantôme doit faire une " + SV("wis", 12) + ". En cas d'échec, il est <strong>Effrayé</strong> (Frightened) : il voit le lac se transformer en une gueule géante pleine de dents.")}
{ul(
    "À la fin de chacun de ses tours, un personnage effrayé peut refaire la sauvegarde pour se libérer.",
    "Un allié peut le secouer (une action, en le touchant) : il refait la sauvegarde avec l'avantage.",
    "La technique <strong>Libération (Release)</strong> ou un " + I("talisman", "talisman de luciole") + " brise l'illusion immédiatement.",
    "Un personnage qui dit « c'est une illusion ! » et réussit un test d'" + SK("ill", 12) + " peut refaire la sauvegarde avec l'avantage.",
)}
<h2>2. Les clones d'eau attaquent</h2>
{box("fight", p(
    "Lancez l'initiative. Quatre " + A("clone", "clones d'eau") + " sortent du lac (jetons cachés au bord de l'eau, à révéler). Ils ressemblent au fantôme. Leur but : <strong>attraper Tetsu</strong>, qui est sorti de chez lui en entendant les ninjas (placez son jeton sur la place, ou près des personnages).",
    "<strong>Règle des sbires :</strong> un clone d'eau a 1 PV. Le premier coup qui le touche le fait éclater en une gerbe d'eau.",
    "<strong>Enlèvement :</strong> si deux clones finissent leur tour à côté de Tetsu, ils l'attrapent et l'emportent vers le lac (4 cases par tour). Touchez un des deux clones pour le libérer.",
    "Au round 2, " + A("uramaru", "le Fantôme") + " (jeton caché sur le lac) lance une fois sa technique de shuriken d'eau sur le personnage le plus menaçant, puis reste à distance."))}
<h2>3. Le fantôme s'en va</h2>
{box("read", p(
    "Le dernier clone éclate. Sur le lac, le fantôme éclate d'un rire froid. « Des gamins de Konoha… Rentrez chez vous, petits. Avant l'aube, ce lac sera à moi. »",
    "Il fait un signe de la main, et le brouillard l'avale. Quand il se dissipe, il n'y a plus rien que le lac noir et, au loin, la silhouette sombre de l'île des Lucioles."))}
{ul(
    "<strong>Si Tetsu a été enlevé</strong>, il est emmené au camp de l'île : les héros doivent y aller tout de suite.",
    "<strong>Si Tetsu est sauvé</strong>, il se jette dans les bras de ses sauveurs. Un test de " + SK("prc", 12) + " permet de voir une barque partir en silence du quai de l'entrepôt : Kaneda rame vers l'île !",
    "« Avant l'aube » : les personnages ont le temps de faire un <strong>repos court</strong> (1 heure) à l'auberge avant de partir. Shûhei leur souhaite bonne chance : « Je suis fier de vous. Comme on dit… le poisson pourrit par la tête. Allez attraper la tête ! »",
)}
"""),

    ("acte4", "Acte 4 : L'île des Lucioles", f"""
<h1>Acte 4 : L'île des Lucioles</h1>
<h2>La traversée</h2>
{p("L'île est à environ 800 mètres du ponton. Deux façons d'y aller :")}
{ul(
    "<strong>La barque de Genji :</strong> deux personnages rament. Test de groupe d'" + SK("ath", 10) + " : si la moitié réussit, la barque avance vite et en silence.",
    "<strong>Marcher sur l'eau :</strong> c'est fatigant pour des genin ! " + SK("ccl", 12) + ". En cas d'échec, le personnage tombe à l'eau plusieurs fois et arrive trempé et essoufflé (il commence le combat avec 2 PV de moins).",
)}
{p("Pour approcher sans être vus : test de groupe de " + SK("ste", 12) + ". Si la moitié du groupe réussit (et que Kaneda n'a pas été alerté), les personnages ont un <strong>round de surprise</strong> : ils agissent avant que les ennemis ne réagissent.")}
<h2>Sur l'île</h2>
{p("Ouvrez la scène " + S("ile", "L'île des Lucioles") + ". Placez les personnages sur la plage, à l'ouest. Les lieux numérotés sont décrits dans les pages <em>Île 1</em> à <em>Île 5</em>.")}
{box("read", p(
    "La barque glisse sur la plage. L'île est silencieuse, noyée dans une brume légère. Un chemin de pierres plates mène vers un vieux portail rouge, puis vers les ruines d'un sanctuaire.",
    "Plus loin, une lueur de lanterne et le bruit des pelles. Puis un grincement de bois : un coffre qu'on ouvre.",
    "« De l'or… tout cet or… » La voix tremblante de Kaneda. Puis une autre voix, plus froide : « Merci pour ton aide, Kaneda-san. Ta part ? Le fond du trou. »",
    "Un cri, un bruit sourd : quelqu'un vient d'être poussé dans la fosse."))}
<h2>Le combat final</h2>
{box("fight", p(
    "<strong>Adversaires :</strong> " + A("uramaru", "Uramaru Hisame, le Fantôme du Lac") + " et deux " + A("brigand", "brigands") + " près de la fosse. Si Gonza s'est enfui à l'acte 1, " + A("gonza", "Tonbi Gonza") + " monte la garde au camp (jeton caché) avec les PV qu'il lui restait (ou 20 PV).",
    "<strong>Kaneda</strong> est au fond de la fosse, la jambe tordue. Il ne combat pas et supplie qu'on l'aide.",
    "<strong>Difficulté :</strong> difficile mais juste. Voir " + J(SC, "difficulte", "Ajuster la difficulté") + " si le combat tourne mal (ou trop bien)."))}
<h3>Tactique d'Uramaru</h3>
{ol(
    "<strong>Round 1 :</strong> il lance <em>Suiton : Brume cachée</em> (Hidden Mist) sur la zone et marque le personnage le plus dangereux. Il appelle deux clones d'eau (action bonus).",
    "<strong>Ensuite :</strong> il attaque les personnages fragiles (ceux qui lancent des techniques ou soignent) avec <em>Shuriken d'eau</em>, et utilise le <em>Fouet d'eau</em> pour tirer un personnage vers la fosse ou le lac.",
    "<strong>Réaction :</strong> une fois par combat, il utilise la Technique de substitution quand il va être touché (il est remplacé par une bûche).",
    "<strong>À 20 PV ou moins :</strong> il attrape le sac d'or et court vers le lac pour s'enfuir en marchant sur l'eau. Il faut l'arrêter avant qu'il atteigne l'eau (Possession de l'ombre, piège à fil, croc-en-jambe, Akimichi qui lui barre la route…).",
)}
<h3>La lanterne du sanctuaire</h3>
{p("Un personnage qui atteint la grande lanterne de pierre devant le sanctuaire (lieu 4) et l'allume (avec du feu, une technique Katon ou un talisman de luciole) déclenche le miracle de la légende : des centaines de lucioles s'envolent et la brume disparaît de l'île pour le reste de la nuit. <strong>Uramaru ne peut plus utiliser la Brume cachée.</strong>")}
<h2>La fin du combat</h2>
{ul(
    "<strong>Uramaru vaincu :</strong> il est ligoté. « Konoha… Je m'en souviendrai, petits. » Shûhei enverra un message au village pour qu'une équipe vienne le chercher.",
    "<strong>Uramaru s'enfuit :</strong> il laisse tomber le sac d'or dans sa fuite. La mission est quand même réussie, mais le danger n'est pas écarté (une bonne idée pour une prochaine aventure !).",
    "<strong>Kaneda :</strong> s'il est sauvé de la fosse, il fond en larmes et avoue tout. Il promet d'annuler les ventes et de rendre les terres. Les personnages peuvent le ramener à la cheffe Oume.",
)}
{p("<strong>Le trésor :</strong> le coffre contient le " + I("tresor", "trésor du seigneur Kagami") + " : de vieilles pièces d'or et un rouleau scellé. Sur le rouleau, une seule phrase : « Ce trésor appartient à Kawabe. Qu'il serve à reconstruire quand le malheur viendra. »")}
"""),

    ("ile1", "Île 1 : La plage", f"""
<h1>Île 1 : La plage d'accostage</h1>
{p("Une petite plage de sable gris. Les deux " + "barques volées" + " de Genji sont tirées sur le sable, cachées sous des branches. " + SK("prc", 10) + " : de nombreuses traces de pas vont et viennent vers l'est.")}
{p("Les personnages peuvent saboter les barques (Uramaru ne pourra plus fuir avec), ou les récupérer pour Genji.")}
"""),

    ("ile2", "Île 2 : Le torii", f"""
<h1>Île 2 : Le portail rouge (torii)</h1>
{p("Un vieux portail rouge écaillé, couvert de mousse. Entre ses piliers, Uramaru a tendu un fil presque invisible, relié à des clochettes.")}
{ul(
    "Repérer le fil : " + SK("prc", 13) + ". Tsumugi (spécialiste des fils et des armes) a l'avantage.",
    "Si le fil est touché, les clochettes sonnent : plus de surprise possible, et les brigands viennent voir.",
    "Contourner le torii par les buissons évite le piège, mais Ayame dirait que c'est très impoli envers les esprits…",
)}
"""),

    ("ile3", "Île 3 : Le camp", f"""
<h1>Île 3 : Le camp des brigands</h1>
{p("Deux tentes, un feu de camp, des sacs de riz volés et des cerfs-volants noirs avec des lanternes bleues (les « feux follets »).")}
{ul(
    "Si Gonza s'est enfui à l'acte 1, il est ici, assis près du feu, en train de soigner ses blessures. Il rejoint le combat dès qu'il entend du bruit.",
    "Si Tetsu a été enlevé, il est attaché près d'une tente, bâillonné mais indemne. Le libérer prend une action.",
    "Dans une tente : 120 ryôs, une " + I("onigiri", "boîte d'onigiri") + " et une bouteille de saké.",
)}
"""),

    ("ile4", "Île 4 : Le vieux sanctuaire", f"""
<h1>Île 4 : Le vieux sanctuaire du seigneur Kagami</h1>
{p("Un sanctuaire de bois noirci, à moitié écroulé. Devant les marches, une grande lanterne de pierre couverte de mousse : la lanterne de la légende.")}
{p("<strong>Rallumer la lanterne</strong> (une action, à côté de la lanterne) avec du feu, une technique de feu ou un talisman de luciole : des centaines de lucioles s'envolent. La brume disparaît de l'île jusqu'au matin et Uramaru ne peut plus lancer sa Brume cachée. Tous les alliés à moins de 6 cases regagnent 1d4 PV, émerveillés.")}
"""),

    ("ile5", "Île 5 : La fosse au trésor", f"""
<h1>Île 5 : La fosse au trésor</h1>
{p("Un trou de deux mètres de profondeur, creusé à côté du sanctuaire. Une échelle de corde descend au fond. Le coffre du seigneur Kagami est ouvert, rempli de vieilles pièces d'or.")}
{ul(
    "Tomber dans la fosse : 1d6 dégâts. En sortir sans l'échelle : " + SK("ath", 10) + ".",
    "Kaneda est au fond, la jambe tordue. Le remonter demande une action et un test d'" + SK("ath", 10) + " (Bunta réussit automatiquement).",
)}
"""),

    ("epilogue", "Épilogue : la fête des lanternes", f"""
<h1>Épilogue : la fête des lanternes</h1>
{box("read", p(
    "Le lendemain soir, pour la première fois depuis deux semaines, tout le village de Kawabe est dehors. Les familles qui étaient parties ont reçu un message et commencent à revenir.",
    "La grand-mère Oume a décidé d'organiser une fête. Chacun pose sur le lac une petite lanterne de papier avec une bougie, et des centaines de petites lumières dérivent vers l'île des Lucioles. Cette fois, ce sont de vraies lucioles qui dansent au-dessus de l'eau pour les accueillir.",
    "Shûhei, encore un peu pâle, lève son bol de thé : « À la meilleure équipe de genin que j'aie jamais eue ! Bon, c'est la seule… mais quand même ! »"))}
<h2>Les récompenses</h2>
{ul(
    "La cheffe Oume insiste : la mission sera payée comme une <strong>mission de rang C</strong> grâce au trésor retrouvé. 30 000 ryôs pour l'équipe.",
    "Chaque personnage reçoit un " + I("insigne", "insigne de Kawabe") + " : une petite luciole de bois sculpté.",
    "Ayame offre à chacun une pilule de chakra.",
    "Accordez un point de <strong>Volonté du Feu</strong> à chaque joueur.",
)}
<h2>Le mot de la fin</h2>
{p("Pour terminer, faites un tour de table : <em>« Qu'est-ce que ton personnage a appris pendant cette mission ? »</em> C'est le moment où chacun trouve un bout de son <strong>nindô</strong>, sa voie du ninja.")}
"""),

    ("difficulte", "Ajuster la difficulté", f"""
<h1>Ajuster la difficulté</h1>
{p("Les dés peuvent être cruels. Voici comment adapter les combats sans que les joueurs ne le remarquent.")}
<h2>Si c'est trop dur</h2>
{ul(
    "Les brigands sont lâches : ils s'enfuient quand ils sont à moitié de leurs PV.",
    "Uramaru se moque, parle beaucoup, et perd son tour à faire un discours.",
    "Gonza ne revient pas à l'acte 4.",
    "Uramaru s'enfuit dès 30 PV au lieu de 20.",
    "<strong>La cavalerie :</strong> au round 3, Shûhei arrive en titubant sur l'île et lance une boule de feu sur les brigands. « Je ne pouvais pas… rater ça ! » Puis il s'évanouit.",
    "Ayame, venue en cachette, rallume la lanterne du sanctuaire à la place des héros.",
)}
<h2>Si c'est trop facile</h2>
{ul(
    "Uramaru appelle deux clones d'eau supplémentaires à chaque round.",
    "Gonza arrive en renfort même s'il avait été capturé (ses complices l'ont libéré).",
    "Uramaru utilise le Fouet d'eau pour jeter un personnage dans le lac (" + SK("ath", 12) + " pour regagner la rive).",
)}
<h2>Et si un personnage tombe à 0 PV ?</h2>
{p("Il fait des jets contre la mort comme prévu par les règles. Mais pour une première partie, nous conseillons : un personnage à 0 PV est simplement <strong>assommé</strong> jusqu'à la fin du combat ou jusqu'à ce qu'on le soigne. Il se réveille avec 1 PV et une bonne bosse.")}
"""),
]


# =========================================================================== #
#  02 · PNJ                                                                   #
# =========================================================================== #

PNJ = [
    ("resume", "Tous les PNJ en un coup d'œil", f"""
<h1>Tous les PNJ en un coup d'œil</h1>
{table(["PNJ", "Qui ?", "Le jouer en une phrase"],
    [A("shuhei", "Inaba Shûhei"), "Chûnin de Konoha, chef d'escouade", "Optimiste, rate tous ses proverbes, devient le grand frère des héros."],
    [A("oume", "Grand-mère Oume"), "Cheffe de Kawabe, 74 ans", "Autoritaire, tape sa canne par terre quand elle s'énerve, fume la pipe."],
    [A("sachi", "Sachi"), "Aubergiste", "Bavarde, débrouillarde, connaît tous les ragots."],
    [A("tetsu", "Tetsu"), "Petit garçon de 8 ans", "Méfiant puis collant ; veut devenir ninja."],
    [A("genji", "Le vieux Genji"), "Pêcheur, 65 ans", "Grogne tout le temps, mais a un cœur d'or."],
    [A("ayame", "Ayame"), "Gardienne du sanctuaire, 16 ans", "Douce, rêveuse, parle aux esprits comme à des voisins."],
    [A("kaneda", "Kaneda Jûbei"), "Marchand de riz", "Sourire mielleux, se frotte les mains, transpire quand on le soupçonne."],
    [A("mosuke", "Mosuke"), "Commis de Kaneda", "Se ronge les ongles, prêt à tout avouer au moindre froncement de sourcils."],
    [A("gonza", "Tonbi Gonza"), "Chef des brigands", "Ricane, se croit plus malin que tout le monde, fuit dès que ça tourne mal."],
    [A("uramaru", "Uramaru Hisame"), "Déserteur de Kiri, le « Fantôme du Lac »", "Calme, méprisant, parle doucement comme un professeur ennuyé."],
)}
"""),
    ("shuhei", "Inaba Shûhei", f"""
<h1>{A("shuhei", "Inaba Shûhei")} — le chef d'escouade</h1>
{p("<strong>Apparence :</strong> 24 ans, cheveux en bataille, gilet de chûnin mal fermé, un bandeau de Konoha un peu de travers.",
   "<strong>Caractère :</strong> joyeux, confiant, un peu tête en l'air. Il adore les proverbes mais se trompe toujours (« L'habit ne fait pas le… poisson ? »).",
   "<strong>Rôle :</strong> empoisonné dès l'acte 1, il laisse les genin prendre les décisions. Au lit à l'auberge, il peut donner un conseil si les joueurs sont perdus.",
   "<strong>Ce qu'il sait :</strong> il reconnaît le brouillard de Kiri si on le lui décrit (« Brouillard salé, voix de partout… C'est une technique de la Brume. Faites attention : les ninjas de Kiri sont des tueurs silencieux. »).")}
"""),
    ("villageois", "Les habitants de Kawabe", f"""
<h1>Les habitants de Kawabe</h1>
<h2>{A("oume", "Grand-mère Oume")}</h2>
{p("Toute petite, toute ridée, mais tout le monde lui obéit. Elle se sent coupable d'avoir laissé partir six familles. Elle fait confiance aux ninjas, mais pas aux marchands. <em>Tic :</em> tape sa canne par terre. <em>Phrase :</em> « De mon temps, les fantômes avaient la politesse de rester morts ! »")}
<h2>{A("sachi", "Sachi")}</h2>
{p("40 ans, manches retroussées, rire sonore. Elle gère l'auberge seule depuis la mort de son mari. Elle nourrit tout le monde, même ceux qui ne peuvent pas payer. <em>Phrase :</em> « Mangez d'abord, vous aurez peur après ! »")}
<h2>{A("tetsu", "Tetsu")}</h2>
{p("8 ans, genoux écorchés, un bandeau en tissu qu'il a fabriqué lui-même. Son père est pêcheur. Il a vu le fantôme sans masque mais personne ne le croit. Il veut devenir ninja et s'attache vite aux héros.")}
<h2>{A("genji", "Le vieux Genji")}</h2>
{p("65 ans, peau tannée par le soleil, toujours un filet à la main. Il est furieux qu'on lui ait volé ses barques. <em>Phrase :</em> « Fantôme ou pas, je veux mes barques ! »")}
<h2>{A("ayame", "Ayame")}</h2>
{p("16 ans, gardienne du petit sanctuaire depuis la mort de son grand-père. Elle croit sincèrement aux esprits et à la légende du seigneur Kagami. Elle confie les talismans de luciole aux héros.")}
"""),
    ("mechants", "Kaneda, Gonza et Uramaru", f"""
<h1>Les responsables</h1>
<h2>{A("kaneda", "Kaneda Jûbei")} — le commanditaire</h2>
{p("Un homme rond en kimono de soie, des bagues à tous les doigts. Il n'est pas méchant comme un monstre : il est <strong>avide</strong>. Il s'est convaincu que « ces pauvres gens seront mieux ailleurs ». Il a peur d'Uramaru, mais il est trop tard pour reculer. S'il est sauvé par les héros, il regrette sincèrement.")}
<h2>{A("mosuke", "Mosuke")} — le commis</h2>
{p("Jeune homme maigre à lunettes. Il sait que son patron paie quelqu'un pour « le brouillard », mais pas plus. Il a honte et avoue tout à la première menace.")}
<h2>{A("gonza", "Tonbi Gonza")} — le chef des brigands</h2>
{p("Un ancien élève de l'Académie qui n'a jamais réussi l'examen de genin. Il déteste les ninjas « officiels ». Long manteau gris, kusarigama à la ceinture, aiguilles empoisonnées dans la manche. Lâche : il fuit dès qu'il est en difficulté.")}
<h2>{A("uramaru", "Uramaru Hisame")} — le Fantôme du Lac</h2>
{p("Un ancien chûnin de Kiri, 30 ans, cheveux gris-bleu, une cicatrice sur le menton. Il a déserté son village après avoir volé des rouleaux de techniques. Il porte un masque blanc et une cape claire pour jouer le fantôme.",
   "<strong>Ce qu'il veut :</strong> l'or du trésor, pour disparaître loin d'ici. Kaneda n'est pour lui qu'un outil.",
   "<strong>Comment le jouer :</strong> il ne crie jamais. Il parle lentement, comme un professeur ennuyé par de mauvais élèves. Il sous-estime les genin… jusqu'à ce qu'ils le blessent vraiment. Alors il perd son calme.")}
{box("tip", p("Uramaru est dangereux pour des genin de niveau 1. N'hésitez pas à le faire parler pendant le combat : chaque réplique laisse un peu de répit aux joueurs."))}
"""),
]
