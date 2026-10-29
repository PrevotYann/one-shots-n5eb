"""Journaux visibles par les joueurs : guide du joueur et fiches des prétirés. Aides de jeu (images)."""
from content_mj import p, ul, ol, table
from ids import A, box

GUIDE = [
    ("bienvenue", "Bienvenue, ninja !", f"""
<h1>Bienvenue, ninja !</h1>
{p("Tu incarnes un <strong>genin</strong> de Konoha, le Village Caché de la Feuille. Tu viens de sortir de l'Académie, tu as ton bandeau frontal tout neuf, et aujourd'hui commence ta première vraie mission hors du village.",
   "Tu n'as pas besoin de connaître les règles pour jouer. Dis simplement au MJ ce que ton personnage veut faire : il te dira quand lancer les dés.")}
<h2>Les trois choses à savoir</h2>
{ol("<strong>Pour réussir une action</strong> difficile, lance 1d20 et ajoute le bonus de ta fiche. Plus c'est haut, mieux c'est.",
    "<strong>Ton chakra</strong> est l'énergie qui te permet de lancer des techniques (jutsu). Chaque technique en coûte un peu. Quand il n'y en a plus, il faut se reposer.",
    "<strong>Ton équipe</strong> est ta plus grande force. Un ninja seul est un ninja en danger !")}
<h2>Choisir son personnage</h2>
{table(["Personnage", "Style", "Difficulté"],
    [A("bunta", "Akimichi Bunta"), "Costaud, protège ses amis, frappe fort au corps à corps", "★☆☆ facile"],
    [A("kaito", "Hibana Kaito"), "Lance des techniques de feu dévastatrices, mais fragile", "★★☆ moyen"],
    [A("shizuka", "Nara Shizuka"), "Stratège, immobilise ses ennemis avec son ombre", "★★☆ moyen"],
    [A("tsumugi", "Fûma Tsumugi"), "Experte des armes de lancer, des pièges et des fils", "★★☆ moyen"],
    [A("momo", "Sakuraba Momo"), "Soigne ses amis et brise les illusions", "★☆☆ facile"],
)}
"""),
    ("combat", "Ton tour en combat", f"""
<h1>Ton tour en combat</h1>
{p("En combat, chacun joue à son tour. Pendant ton tour, tu peux faire <strong>tout ça</strong>, dans l'ordre que tu veux :")}
{table(["", "Quoi ?", "Exemples"],
    ["🏃", "<strong>Te déplacer</strong> (6 cases)", "courir, grimper, sauter, contourner un ennemi"],
    ["⚔️", "<strong>Une action</strong>", "attaquer avec une arme, lancer une technique, aider un allié, te cacher, utiliser un objet"],
    ["⚡", "<strong>Une action bonus</strong> (si une capacité le permet)", "certaines techniques, avaler une pilule"],
    ["🛡️", "<strong>Une réaction</strong> (une fois par round, même hors de ton tour)", "Technique de substitution, Technique du clonage"],
)}
<h2>Comment attaquer ?</h2>
{ol("Clique sur ton arme ou ta technique dans ta fiche.", "Choisis ta cible (le jeton de l'ennemi).", "Le système lance les dés pour toi : si ton résultat atteint la CA de l'ennemi, tu touches !", "Lance ensuite les dégâts.")}
<h2>Quand tu es blessé</h2>
{p("Tes <strong>points de vie (PV)</strong> baissent quand on te touche. À 0, tu tombes inconscient. Ne panique pas : tes amis peuvent te soigner (Momo !) ou te stabiliser.")}
{box("tip", p("Le meilleur conseil : <strong>parle avec ton équipe</strong>. « Shizuka, immobilise-le, je fonce ! » C'est comme ça qu'on gagne."), "Astuce")}
"""),
    ("chakra", "Le chakra et les techniques", f"""
<h1>Le chakra et les techniques</h1>
{p("Le chakra, c'est l'énergie du corps et de l'esprit mélangées. Les ninjas le « malaxent » avec des signes des mains pour créer des techniques.")}
{ul("Ta réserve de chakra est affichée sur ta fiche et sur ton jeton (la deuxième barre).",
    "Chaque technique indique son <strong>coût</strong> en chakra et son <strong>rang</strong> (E = très simple, D = niveau genin).",
    "<strong>Ninjutsu</strong> : techniques de chakra (feu, ombre, soins…).",
    "<strong>Genjutsu</strong> : illusions qui trompent l'esprit (clonage, transformation, libération).",
    "<strong>Taijutsu</strong> : techniques de combat au corps à corps.",
    "<strong>Bukijutsu</strong> : techniques d'armes (shuriken, fils…).")}
<h2>Se reposer</h2>
{ul("<strong>Repos court</strong> (1 heure) : tu peux dépenser des « dés de vie » pour regagner des PV et des « dés de chakra » pour regagner du chakra.",
    "<strong>Repos long</strong> (une nuit de sommeil) : tu récupères tout.")}
<h2>Les techniques que tout le monde connaît</h2>
{p("Tous les genin ont appris à l'Académie :")}
{ul("<strong>Technique du clonage</strong> : deux copies de toi apparaissent. Quand on t'attaque, tu peux faire rater l'ennemi en le trompant (il retire 1d6 à son attaque).",
    "<strong>Technique de transformation</strong> : tu prends l'apparence de quelqu'un ou de quelque chose. Parfait pour tromper un garde (+4 au test de Tromperie).")}
{box("tip", p("Les techniques sont affichées « nom français (nom anglais) ». Ouvre une technique pour lire son résumé <strong>« En bref »</strong>."), "Astuce")}
"""),
]


def fiche(key, name, title, quote, who, perso, role, moves, links, tips):
    return f"""
<h1>{A(key, name)}</h1>
<p class="ffk-subtitle">{title}</p>
<blockquote>« {quote} »</blockquote>
<h2>Qui es-tu ?</h2>
{p(*who)}
<h2>Ta personnalité</h2>
{ul(*perso)}
<h2>Ton rôle dans l'équipe</h2>
{p(role)}
<h2>Tes techniques et capacités, en clair</h2>
{table(["Nom", "Ce que ça fait"], *moves)}
<h2>Tes liens avec les autres</h2>
{ul(*links)}
{box("tip", ul(*tips), "Conseils pour bien jouer")}
"""


FICHES = [
    ("bunta", "Akimichi Bunta", fiche(
        "bunta", "Akimichi Bunta",
        "13 ans · Clan Akimichi · Spécialiste du taijutsu · « Le Rocher gourmand »",
        "Ventre plein, cœur vaillant !",
        ["Tu es le plus grand et le plus large de ta promotion. Ta grand-mère tient un petit restaurant à Konoha, et ton rêve est de devenir le premier ninja-cuisinier dont on chantera les recettes dans tout le pays.",
         "Comme tous les Akimichi, tu sais transformer les calories en chakra et faire grossir une partie de ton corps pour frapper plus fort."],
        ["Calme, lent à parler, mais jamais lent à agir quand un ami est en danger.",
         "Tu partages toujours ta nourriture (ce qui est une grande preuve d'amitié).",
         "Tu détestes qu'on gaspille de la nourriture… et qu'on s'en prenne aux plus petits."],
        "Tu es <strong>le rempart</strong>. Tu te places entre les ennemis et tes amis fragiles (Kaito, Momo), tu encaisses les coups et tu frappes fort au corps à corps. Hors combat, tu soulèves, tu pousses, tu enfonces les portes.",
        [["Coups de poing (brassards de combat)", "Ton attaque de base. Puissante grâce à ta Posture du poing de fer."],
         ["Expansion partielle", "Ton bras grossit : tu frappes à 2 cases de distance et tes coups font plus mal. Peut se payer en Calories."],
         ["Boulet humain", "Tu te transformes en boule et tu roules sur 6 cases en écrasant tout sur ton passage. Ton attaque la plus forte !"],
         ["Poing de fer", "Un coup surpuissant qui peut projeter l'ennemi en arrière."],
         ["Tourbillon de la feuille", "Un balayage qui fait tomber l'ennemi à terre."],
         ["Calories", "Une deuxième réserve d'énergie, propre aux Akimichi. Mange pour la remplir !"],
         ["Pause déjeuner", "Pendant un repos court, tu récupères plus de PV."]],
        ["<strong>Kaito</strong> : ton ami d'enfance. Il parle trop et fonce sans réfléchir ; tu es là pour le rattraper.",
         "<strong>Momo</strong> : tu lui gardes toujours une part de dessert. Elle te trouve rassurant."],
        ["Quand un ami est en danger, dis : « Derrière moi ! » et place-toi devant lui.",
         "Au début d'un combat difficile, lance l'Expansion partielle.",
         "Hors combat, propose à manger aux PNJ : ça ouvre bien des portes (et des cœurs)."])),

    ("kaito", "Hibana Kaito", fiche(
        "kaito", "Hibana Kaito",
        "12 ans · Sans clan · Spécialiste du ninjutsu · « L'Étincelle »",
        "Une seule étincelle suffit pour allumer un grand feu.",
        ["Tu n'as pas de clan, pas de famille célèbre, pas de technique secrète. Tu as été élevé par la boulangère de ton quartier, et tu as tout appris à force de travail.",
         "Ton élément, c'est le feu. Tu es le meilleur de ta promotion en ninjutsu, et tu comptes bien le prouver à tout le monde."],
        ["Bavard, fanfaron, toujours une blague (souvent mauvaise) à la bouche.",
         "Tu fonces d'abord et tu réfléchis après… parfois.",
         "Au fond, tu as peur de ne jamais être reconnu. Tu veux que les gens se souviennent de ton nom."],
        "Tu es <strong>le canon</strong>. Tes techniques de feu font énormément de dégâts. Mais tu es fragile : reste à distance, derrière Bunta, et vise les ennemis les plus dangereux.",
        [["Katon : Boule de feu", "Une grosse boule de feu qui brûle tous les ennemis dans une zone (ils peuvent l'esquiver à moitié)."],
         ["Katon : Trait de flamme", "Un jet de feu sur une seule cible. Énormes dégâts !"],
         ["Projectile de chakra", "Une bille de chakra pur, moins chère que tes techniques de feu."],
         ["Technique de substitution", "En réaction, quand on va te toucher : +3 à ta CA, et tu t'éloignes si l'attaque rate."],
         ["Ninjutsu raffiné", "Deux de tes ninjutsu (conseil : Boule de feu et Trait de flamme) peuvent faire un dé de dégâts en plus."],
         ["Récupération de chakra", "Une fois par repos court, une de tes techniques coûte moitié moins cher."],
         ["Vigilant", "Tu n'es jamais surpris et tu agis souvent en premier (+5 à l'initiative)."]],
        ["<strong>Bunta</strong> : ton meilleur ami depuis toujours. Le seul qui te supporte vraiment.",
         "<strong>Shizuka</strong> : ta rivale. Elle était première aux examens écrits, toi en ninjutsu. Tu veux l'impressionner (mais tu ne l'avoueras jamais)."],
        ["Garde ton chakra pour les combats importants : tes techniques coûtent cher.",
         "Combine-toi avec Shizuka : un ennemi immobilisé par son ombre ne peut pas esquiver ton feu !",
         "Ton feu peut aussi servir hors combat : allumer une lanterne, faire peur, éclairer…"])),

    ("shizuka", "Nara Shizuka", fiche(
        "shizuka", "Nara Shizuka",
        "13 ans · Clan Nara · Ninja éclaireur · « L'Ombre patiente »",
        "Laisse-moi réfléchir trois secondes.",
        ["Tu viens du clan Nara, célèbre pour ses stratèges et ses techniques d'ombre. Ton grand-père t'a appris le shôgi avant même que tu saches lire.",
         "Tu étais première aux examens écrits de l'Académie. Tu observes tout, tu remarques tout, et tu as toujours un plan (même deux)."],
        ["Calme, posée, un peu distante. Tu parles peu, mais quand tu parles, on t'écoute.",
         "Tu détestes te presser et tu détestes encore plus les plans improvisés.",
         "Tu caches ta gentillesse derrière un air blasé."],
        "Tu es <strong>la stratège</strong>. Tu immobilises l'ennemi le plus dangereux avec ta Possession de l'ombre, tu repères les pièges et les indices, et tu proposes les plans.",
        [["Possession de l'ombre", "Ton ombre attrape un ennemi : il est entravé et doit copier tes mouvements. Ta meilleure technique ! Attention : ne marche pas dans le noir complet."],
         ["Silhouette d'ombre", "Ton ombre se lève et prend ta forme. Parfait pour faire diversion."],
         ["Libération (Kai)", "Brise un genjutsu (une illusion) sur toi ou un allié. Très utile dans cette mission…"],
         ["Détection du chakra", "Tu sens la présence des autres ninjas autour de toi."],
         ["Coordination", "Au début d'un combat, tu donnes des ordres : tes alliés deviennent « Coordonnés » (2 fois par repos long)."],
         ["Posture de lancer", "Tes kunai et shuriken reviennent dans ta main, et tu vises loin sans pénalité."],
         ["À la hauteur", "Après une première tentative face à un défi, le MJ te donne un indice sur la manière de le surmonter."]],
        ["<strong>Kaito</strong> : ton rival bruyant. Il t'agace… mais il te fait rire, parfois.",
         "<strong>Tsumugi</strong> : la nouvelle. Elle est aussi précise que toi, ça t'intrigue."],
        ["Lance la Possession de l'ombre sur l'ennemi le plus fort, puis crie « Maintenant ! » à tes amis.",
         "Pendant l'enquête, pose des questions. Tu es la meilleure de l'équipe pour relier les indices.",
         "Dans la nuit et le brouillard, ton ombre est plus faible : allume une lumière !"])),

    ("tsumugi", "Fûma Tsumugi", fiche(
        "tsumugi", "Fûma Tsumugi",
        "13 ans · Clan Fûma · Spécialiste des armes · « Fil d'acier »",
        "Je ne rate jamais. Enfin… presque jamais.",
        ["Ta famille appartient au clan Fûma, des ninjas voyageurs qui sillonnent le Pays du Feu. Tes parents se sont installés à Konoha il y a un an seulement, et tu es encore « la nouvelle ».",
         "Tu as un fûma-shuriken (un grand shuriken pliable) que t'a offert ta mère, et tu collectionnes des grelots de tous les villages que tu as traversés."],
        ["Curieuse, souriante, tu racontes sans cesse des histoires de voyage (vraies ou presque).",
         "Un peu fière : tu détestes rater une cible.",
         "Tu as un accent de la campagne qui fait sourire les gens."],
        "Tu es <strong>la tireuse d'élite</strong>. Tu restes à distance et tu cribles les ennemis de shuriken. Tu poses des pièges avec tes fils, et tu repères les pièges des autres.",
        [["Fûma-shuriken", "Ton arme fétiche : un grand shuriken qui fait de gros dégâts à distance."],
         ["Shuriken et kunai", "Pour les attaques rapides. Tu en as plein !"],
         ["Pluie céleste", "Tes armes rebondissent en l'air et retombent en pluie sur une zone. Les ennemis touchés saignent."],
         ["Fente céleste", "Une ligne d'armes qui transperce tout sur son passage."],
         ["Tir double", "Ta prochaine attaque à distance devient deux attaques, sur deux cibles différentes."],
         ["Piège à fil", "Tu poses un piège invisible : l'ennemi qui marche dessus est entravé."],
         ["Précision immaculée", "Tu utilises ta Dextérité (ton point fort) pour tes attaques et techniques d'armes à distance."]],
        ["<strong>Momo</strong> : elle t'a soignée le jour de ton arrivée à Konoha. Depuis, vous êtes inséparables.",
         "<strong>Shizuka</strong> : elle t'observe tout le temps. Tu ne sais pas si elle t'aime bien ou si elle te soupçonne de quelque chose."],
        ["Reste loin des ennemis : tu es plus forte à distance.",
         "Pose un piège à fil là où l'ennemi va courir (sur le chemin de sa fuite, par exemple !).",
         "Tes yeux sont excellents : demande souvent au MJ si tu remarques quelque chose."])),

    ("momo", "Sakuraba Momo", fiche(
        "momo", "Sakuraba Momo",
        "12 ans · Sans clan · Ninja médecin · « Pétale guérisseur »",
        "Personne ne meurt pendant ma garde.",
        ["Ta mère est infirmière à l'hôpital de Konoha. Depuis toute petite, tu la regardes soigner les ninjas blessés, et tu as décidé de devenir ninja médecin.",
         "Petit secret : tu as peur du sang. Mais tu as appris à le cacher, parce que tes amis ont besoin de toi."],
        ["Douce et timide, mais têtue comme une mule quand il s'agit de soigner.",
         "Tu grondes tes amis quand ils prennent des risques idiots (surtout Kaito).",
         "Tu notes tout dans un petit carnet : les plantes, les blessures, les noms."],
        "Tu es <strong>la guérisseuse</strong>. Tu restes près de tes amis pour les soigner, tu brises les illusions, et tu analyses les poisons. Sans toi, l'équipe ne tiendra pas longtemps !",
        [["Iryô : Soin habile", "Ta technique de soin principale. En une action : un ami touché regagne beaucoup de PV. En action bonus : tous les amis proches regagnent 8 PV."],
         ["Iryô : Vitalité", "Pour pas cher : un ami gagne quelques PV temporaires (un bouclier de vie)."],
         ["Iryô : Élixir de soin", "Tu fabriques une fiole de soin qui guérit aussi le poison. Pratique à donner à l'avance !"],
         ["Libération (Kai)", "Brise une illusion sur toi ou un ami."],
         ["Ninjutsu médical", "Tu utilises ta Sagesse (ton point fort) pour tes techniques médicales."],
         ["Repos régénérant", "Pendant les repos, toi et tes amis regagnez 1d6 PV de plus."],
         ["Coup de main", "Tu peux aider un ami (lui donner l'avantage) en action bonus."],
         ["Trousse de médecine", "Pour stabiliser un blessé ou soigner un poison sans dépenser de chakra."]],
        ["<strong>Tsumugi</strong> : ta meilleure amie. Tu l'as soignée le jour de son arrivée.",
         "<strong>Bunta</strong> : il te garde toujours une part de dessert. Tu te sens en sécurité quand il est là."],
        ["Garde du chakra pour les soins : c'est ta mission principale.",
         "N'hésite pas à attaquer avec tes senbon quand personne n'est blessé.",
         "Dans cette mission, il y aura des illusions et du poison… tu vas être indispensable !"])),
]


AIDES = [
    ("ordre", "Ordre de mission", "assets/handouts/ordre-mission.svg",
     "Montrez cette aide de jeu pendant le prologue."),
    ("carte_voyage", "Carte du voyage", "assets/maps/carte-voyage.webp",
     "La route de Konoha à Kawabe."),
    ("legende", "La légende du seigneur Kagami", "assets/handouts/legende-kagami.svg",
     "Remise par Ayame au petit sanctuaire (lieu 6)."),
    ("bandeau", "Bandeau rayé", "assets/handouts/bandeau-kiri.svg",
     "Trouvé dans les roseaux des rizières (lieu 7)."),
    ("registre", "Page du registre de Kaneda", "assets/handouts/registre-kaneda.svg",
     "Trouvée dans le bureau de l'entrepôt (lieu 4)."),
    ("carte", "Plan de l'île", "assets/handouts/plan-ile.svg",
     "Glissé dans le registre de Kaneda (lieu 4)."),
]
