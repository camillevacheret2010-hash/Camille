import discord
import os
import json
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
import random
load_dotenv()
import time
from discord.ext import tasks




BOOST_PRICES = {1:10000, 2:20000}
last_message_author = {}
DAILY_BASE = 500
JOB_INCOME = {0: 0, 1: 500, 2: 1500, 3: 3000, 4: 5000, 5: 7500, 6: 10500}
JOB_UPGRADE_PRICES = {0: 7500, 1: 12500, 2: 17500, 3: 22500, 4: 27500, 5: 32500}
SHOP_ITEMS = {
    "<:noyau_de_puissance:1516065680166879342> Noyau de puissance": 10000,
    "<:oeuf_de_dragon_epique:1516064792400629802> Œuf de dragon épique": 40000,
    "<:oeuf_de_dragon_rare:1516065280416284782> Œuf de dragon rare": 10000,
    "<:oeuf_de_dragon:1515707239737065563> Œuf de dragon": 5000,
    "🐐 Chèvre": 2500,
    "<:soupe_aux_epices:1515710241667285073> Soupe aux épices": 4000,
}

EGG_PROBAS = {
    "commun": [
        ("Commun", 79),
        ("Rare", 15),
        ("Épique", 5),
        ("Légendaire", 1)
    ],
    "rare": [
        ("Commun", 48),
        ("Rare", 40),
        ("Épique", 10),
        ("Légendaire", 2)
    ],
    "epique": [
        ("Rare", 70),
        ("Épique", 25),
        ("Légendaire", 5)
    ]
}


FISHING_RODS = {
    1: {"name": "Canne basique", "cooldown": 3600, "price": 0},
    2: {"name": "Canne solide", "cooldown": 1800, "price": 50000},
    3: {"name": "Canne indestructible", "cooldown": 900, "price": 75000},
}

FISH_LOOT = [
    ("🐟 Sardine", 70),
    ("🐠 Saumon", 20),
    ("🦀 Crabe", 9),
    ("🐡 Poisson d'or", 1)
]

FISH_PRICES = {
    "🐟 Sardine": 500,
    "🐠 Saumon": 2000,
    "🦀 Crabe": 5000,
    "🐡 Poisson d'or": 10000
}

EGG_ITEMS = {
    "commun": "<:oeuf_de_dragon:1515707239737065563> Œuf de dragon",
    "rare": "<:oeuf_de_dragon_rare:1516065280416284782> Œuf de dragon rare",
    "epique": "<:oeuf_de_dragon_epique:1516064792400629802> Œuf de dragon épique"
}

RI_TOKEN_REWARDS = {
    100: 1,
    1000: 2,
    5000: 3
}

RI_ROLE_IDS = {
    100: 1517879549369520139,     # rôle RI 100
    1000: 1517879625907310733,    # rôle RI 1000
    5000: 1517879670144503829,    # rôle RI 5000
    10000: 1517879699521540256    # rôle RI 10000
}


DRAGONS = {
    "Dragon de feu": (
        "<:feu:1516458328715169883> Dragon de feu\n"
        "Rareté : Commun\n"
        "Obtention : Œuf"
    ),
    "Dragon de poison": (
        "<:poison:1516458574232948968> Dragon de poison\n"
        "Rareté : Commun\n"
        "Obtention : Œuf"
    ),
    "Dragon de glace": (
        "<:glace:1516458617211977890> Dragon de glace\n"
        "Rareté : Commun\n"
        "Obtention : Œuf"
    ),
    "Dragon électrique": (
        "<:elec:1516458643435032787> Dragon électrique\n"
        "Rareté : Commun\n"
        "Obtention : Œuf"
    ),
    "Dragon d'eau": (
        "<:eau:1516465397950582896> Dragon d'eau\n"
        "Rareté : Commun\n"
        "Obtention : Œuf"
    ),
    "Dragon de sable": (
        "<:sable:1516465432670900416> Dragon de sable\n"
        "Rareté : Commun\n"
        "Obtention : Œuf"
    ),
    "Dragon des ombres": (
        "<:ombres:1516466733475692725> Dragon des ombres\n"
        "Rareté : Commun\n"
        "Obtention : Œuf"
    ),
    "Dragon de lumière": (
        "<:lumiere:1516468032900304946> Dragon de lumière\n"
        "Rareté : Commun\n"
        "Obtention : Œuf"
    ),
    "Dragon de vent": (
        "<:vent:1516459149624606841> Dragon de vent\n"
        "Rareté : Commun\n"
        "Obtention : Œuf"
    ),
    "Dragon de pierre": (
        "<:pierre:1516459120872394913> Dragon de pierre\n"
        "Rareté : Commun\n"
        "Obtention : Œuf"
    ),
    "Dragon d'argile": (
        "<:argile:1516465277129326732> Dragon d'argile\n"
        "Rareté : Commun\n"
        "Obtention : Hybride\n"
        "Parents : <:eau:1516465397950582896> Dragon d'eau & <:sable:1516465432670900416> Dragon de sable"
    ),
    "Dragon de cristal": (
        "<:crystal:1516465235794591916> Dragon de cristal\n"
        "Rareté : Commun\n"
        "Obtention : Hybride\n"
        "Parents : <:pierre:1516459120872394913> Dragon de pierre & <:glace:1516458617211977890> Dragon de glace"
    ),
    "Dragon de lave": (
        "<:lave:1516465317188993025> Dragon de lave\n"
        "Rareté : Commun\n"
        "Obtention : Hybride\n"
        "Parents : <:feu:1516458328715169883> Dragon de feu & <:pierre:1516459120872394913> Dragon de pierre"
    ),
    "Dragon spectral": (
        "<:spectral:1516466639716221199> Dragon spectral\n"
        "Rareté : Commun\n"
        "Obtention : Hybride\n"
        "Parents : <:ombres:1516466733475692725> Dragon des ombres & <:vent:1516459149624606841> Dragon du vent"
    ),
    "Dragon d'orage": (
        "<:spectral:1516466639716221199> Dragon d'orage\n"
        "Rareté : Commun\n"
        "Obtention : Hybride\n"
        "Parents : <:elec:1516458643435032787> Dragon électrique & <:vent:1516459149624606841> Dragon vent"
    ),
    "Dragon des cavernes": (
        "<:cavernes:1516467653219454986> Dragon des cavernes\n"
        "Rareté : Commun\n"
        "Obtention : Hybride\n"
        "Parents : <:pierre:1516459120872394913> Dragon de pierre & <:ombres:1516466733475692725> Dragon des ombres"
    ),
    "Dragon de poussière": (
        "<:poussiere:1516466371830223013> Dragon de poussière\n"
        "Rareté : Commun\n"
        "Obtention : Hybride\n"
        "Parents : <:vent:1516459149624606841> Dragon de vent & <:pierre:1516459120872394913> Dragon de pierre"
    ),
    "Dragon des vagues": (
        "<:vagues:1516497154934313101> Dragon des vagues\n"
        "Rareté : Commun\n"
        "Obtention : Hybride\n"
        "Parents : <:eau:1516465397950582896> Dragon d'eau & <:vent:1516459149624606841> Dragon de vent"
    ),
    "Dragon radioactif": (
        "<:radioactif:1516468277251936457> Dragon radioactif\n"
        "Rareté : Commun\n"
        "Obtention : Hybride\n"
        "Parents : <:poison:1516458574232948968> Dragon de poison & <:vent:1516459149624606841> Dragon de vent"
    ),
    "Dragon du soleil": (
        "<:soleil:1516465538988114021> Dragon du soleil\n"
        "Rareté : Rare\n"
        "Obtention : Œuf"
    ),
    "Dragon de lune": (
        "<:lune:1516465571187658904> Dragon de lune\n"
        "Rareté : Rare\n"
        "Obtention : Œuf"
    ),
    "Dragon de sang": (
        "<:sang:1516466216330461305> Dragon de sang\n"
        "Rareté : Rare\n"
        "Obtention : Œuf"
    ),
    "Dragon chromatique": (
        "<:chromatique:1516465473632600174> Dragon chromatique\n"
        "Rareté : Rare\n"
        "Obtention : Œuf"
    ),
    "Dragon corrompu": (
        "<:corrompu:1516465727232544919> Dragon corrompu\n"
        "Rareté : Rare\n"
        "Obtention : Œuf"
    ),
    "Dragon des cieux": (
        "<:cieux:1516468067113369691> Dragon des cieux\n"
        "Rareté : Rare\n"
        "Obtention : Œuf"
    ),
    "Dragon miroir": (
        "<:miroir:1516467444326338732> Dragon miroir\n"
        "Rareté : Rare\n"
        "Obtention : Hybride\n"
        "Parents : <:crystal:1516465235794591916> Dragon de cristal & <:ombres:1516466733475692725> Dragon des ombres"
    ),
    "Dragon possedé": (
        "<:possede:1516467205556932668> Dragon possedé\n"
        "Rareté : Rare\n"
        "Obtention : Hybride\n"
        "Parents : <:spectral:1516466639716221199> Dragon spectral & <:feu:1516458328715169883 Dragon de feu"
    ),
    "Dragon de métal": (
        "<:metal:1516466265349292253> Dragon de métal\n"
        "Rareté : Rare\n"
        "Obtention : Hybride\n"
        "Parents : <:pierre:1516459120872394913> Dragon de pierre & <:crystal:1516465235794591916> Dragon de cristal"
    ),
    "Dragon d'obsidienne": (
        "<:obsidienne:1516466517640876153> Dragon d'obsidienne\n"
        "Rareté : Rare\n"
        "Obtention : Hybride\n"
        "Parents : <:lave:1516465317188993025> Dragon de lave & <:eau:1516465397950582896> Dragon d'eau"
    ),
    "Dragon de terreur": (
        "<:terreur:1516466238203629578> Dragon de terreur\n"
        "Rareté : Rare\n"
        "Obtention : Hybride\n"
        "Parents : <:spectral:1516466639716221199> Dragon spectral & <:ombres:1516466733475692725> Dragon des ombres"
    ),
    "Dragon de plante": (
        "<:plante:1516465362768756787> Dragon de plante\n"
        "Rareté : Rare\n"
        "Obtention : Hybride\n"
        "Parents : <:argile:1516465277129326732> Dragon d'argile & <:eau:1516465397950582896> Dragon d'eau"
    ),
    "Dragon de la mer": (
        "<:mer:1516467412516474981> Dragon de la mer\n"
        "Rareté : Rare\n"
        "Obtention : Hybride\n"
        "Parents : <:vagues:1516497154934313101> Dragon des vagues & <:vent:1516459149624606841> Dragon de vent"
    ),
    "Dragon de diamant": (
        "<:diamant:1516468370445172756> Dragon de diamant\n"
        "Rareté : Rare\n"
        "Obtention : Hybride\n"
        "Parents : <:lave:1516465317188993025> Dragon de lave & <:crystal:1516465235794591916> Dragon de crystal"
    ),
    "Dragon des abysses": (
        "<:abysses:1516467472193028116> Dragon des abysses\n"
        "Rareté : Rare\n"
        "Obtention : Hybride\n"
        "Parents : <:ombres:1516466733475692725> Dragon des ombres & <:cavernes:1516467653219454986> Dragon des cavernes"
    ),
    "Grand Dragon Doré": (
        "<:dor:1516465064259883238> Grand Dragon Doré\n"
        "Rareté : Épique\n"
        "Obtention : Œuf"
    ),
    "Dragon d'automne": (
        "<:automne:1516467039391322112> Dragon d'automne\n"
        "Rareté : Épique\n"
        "Obtention : Œuf"
    ),
    "Dragon d'hiver": (
        "<:hiver:1516467101366358110> Dragon d'hiver\n"
        "Rareté : Épique\n"
        "Obtention : Œuf"
    ),
    "Dragon d'été": (
        "<:ete:1516467133163507764> Dragon d'été\n"
        "Rareté : Épique\n"
        "Obtention : Œuf"
    ),
    "Dragon de printemps": (
        "<:printemps:1516467069003235579> Dragon de printemps\n"
        "Rareté : Épique\n"
        "Obtention : Œuf"
    ),
    "Dragon musical": (
        "<:musical:1516469012135936080> Dragon musical\n"
        "Rareté : Épique\n"
        "Obtention : Œuf"
    ),
    "Dragon détruit": (
        "<:detruit:1516466796507431006> Dragon détruit\n"
        "Rareté : Épique\n"
        "Obtention : Hybride\n"
        "Parents : <:corrompu:1516465727232544919> Dragon corrompu & <:rate:1516465121398882304> Dragon raté"
    ),
    "Dragon de la nuit": (
        "<:nuit:1516467758018068653> Dragon de la nuit\n"
        "Rareté : Épique\n"
        "Obtention : Hybride\n"
        "Parents : <:ombres:1516466733475692725> Dragon des ombres & <:lune:1516465571187658904> Dragon de lune"
    ),
    "Dragon mécanique": (
        "<:mecanique:1516466450246799401> Dragon mécanique\n"
        "Rareté : Épique\n"
        "Obtention : Hybride\n"
        "Parents : Dragon de métal & Dragon éléctrique"
    ),
    "Dragon de rouille": (
        "<:rouille:1516466486804353206> Dragon de rouille\n"
        "Rareté : Épique\n"
        "Obtention : Hybride\n"
        "Parents : <:metal:1516466265349292253> Dragon de métal & <:eau:1516465397950582896> Dragon d'eau"
    ),
    "Dragon champignon": (
        "<:champignon:1516466761690648586> Dragon champignon\n"
        "Rareté : Épique\n"
        "Obtention : Hybride\n"
        "Parents : <:poison:1516458574232948968> Dragon de poison & <:plante:1516465362768756787> Dragon de plante"
    ),
    "Dragon pissenlit": (
        "<:pissenlit:1516467168022237385> Dragon pissenlit\n"
        "Rareté : Épique\n"
        "Obtention : Hybride\n"
        "Parents : <:plante:1516465362768756787> Dragon de plante & <:vent:1516459149624606841> Dragon de vent"
    ),
    "Dragon d'améthyste": (
        "<:amethyste:1516467723788357632> Dragon d'améthyste\n"
        "Rareté : Épique\n"
        "Obtention : Hybride\n"
        "Parents : <:crystal:1516465235794591916> Dragon de crystal & <:abysses:1516467472193028116> Dragon des abysses"
    ),
    "Dragon de fleur": (
        "<:fleur:1516465875769753830> Dragon de fleur\n"
        "Rareté : Épique\n"
        "Obtention : Hybride\n"
        "Parents : <:plante:1516465362768756787> Dragon de plante & <:eau:1516465397950582896> Dragon d'eau"
    ),
    "Dragon de pouvoir": (
        "<:pouvoir:1516467236666343535> Dragon de pouvoir\n"
        "Rareté : Épique\n"
        "Obtention : Hybride\n"
        "Parents : <:spectral:1516466639716221199> Dragon spectral & <:terreur:1516466238203629578> Dragon de terreur"
    ),
    "Dragon des nuages": (
        "<:nuages:1516468120078913776> Dragon des nuages\n"
        "Rareté : Épique\n"
        "Obtention : Hybride\n"
        "Parents : <:cieux:1516468067113369691> Dragon des cieux & <:vent:1516459149624606841> Dragon de vent"
    ),
    "Dragon du crépuscule": (
        "<:crepuscule:1516468179013210153> Dragon du crépuscule\n"
        "Rareté : Épique\n"
        "Obtention : Hybride\n"
        "Parents : <:cieux:1516468067113369691> Dragon des cieux & <:ombres:1516466733475692725> Dragon des ombres"
    ),
    "Dragon de l'aube": (
        "<:aube:1516468215860039805> Dragon de l'aube\n"
        "Rareté : Épique\n"
        "Obtention : Hybride\n"
        "Parents : <:cieux:1516468067113369691> Dragon des cieux & <:lumiere:1516468032900304946> Dragon de lumière"
    ),
    "Dragon ancestral": (
        "<:ancestral:1516468148436734112> Dragon ancestral\n"
        "Rareté : Légendaire\n"
        "Obtention : Œuf\n"
    ),
    "Dragon de corail": (
        "<:corail:1516467347769262211> Dragon de corail\n"
        "Rareté : Légendaire\n"
        "Obtention : Hybride\n"
        "Parents : <:mer:1516467412516474981> Dragon de la mer & <:plante:1516465362768756787> Dragon de plante"
    ),
    "Dragon diabolique": (
        "<:diabolique:1516530044938359074> Dragon diabolique\n"
        "Rareté : Légendaire\n"
        "Obtention : Hybride\n"
        "Parents : <:terreur:1516466238203629578> Dragon de terreur & <:sang:1516466216330461305> Dragon de sang"
    ),
    "Dragon arc-en-ciel": (
        "<:arc_en_ciel:1516466111602757733> Dragon arc-en-ciel\n"
        "Rareté : Légendaire\n"
        "Obtention : Hybride\n"
        "Parents : <:miroir:1516467444326338732> Dragon miroir & <:chromatique:1516465473632600174> Dragon chromatique"
    ),
    "Dragon caméléon": (
        "<:cameleon:1516465832345993431> Dragon caméléon\n"
        "Rareté : Légendaire\n"
        "Obtention : Hybride\n"
        "Parents : <:chromatique:1516465473632600174> Dragon chromatique & <:fleur:1516465875769753830> Dragon de fleur"
    ),
    "Dragon éclipse": (
        "<:eclipse:1516466858104979537> Dragon éclipse\n"
        "Rareté : Légendaire\n"
        "Obtention : Hybride\n"
        "Parents : <:soleil:1516465538988114021> Dragon de soleil & <:lune:1516465571187658904> Dragon de lune"
    ),
    "Dragon des aurores": (
        "<:aurores:1516467798430191646> Dragon des aurores\n"
        "Rareté : Légendaire\n"
        "Obtention : Hybride\n"
        "Parents : <:nuit:1516467758018068653> Dragon de nuit & <:soleil:1516465538988114021> Dragon de soleil"
    ),
    "Dragon des étoiles": (
        "<:etoile:1516468341659799813> Dragon des étoiles\n"
        "Rareté : Légendaire\n"
        "Obtention : Hybride\n"
        "Parents : <:cieux:1516468067113369691> Dragon des cieux & <:soleil:1516465538988114021> Dragon de soleil"
    ),
    "Dragon compacté": (
        "<:compacte:1517138088298676264> Dragon compacté\n"
        "Rareté : Légendaire\n"
        "Obtention : Hybride\n"
        "Parents : <:rate:1516465121398882304> Dragon raté ×15"
    ),
    "Dragon de l'espace": (
        "<:espace:1516467268165304491> Dragon de l'espace\n"
        "Rareté : Divin\n"
        "Obtention : Hybride\n"
        "Parents : <:eclipse:1516466858104979537> Dragon éclipse & <:arc_en_ciel:1516466111602757733> Dragon arc-en-ciel"
    ),
    "Dragon du temps": (
        "<:temps:1516467293037662321> Dragon du temps\n"
        "Rareté : Divin\n"
        "Obtention : Hybride\n"
        "Parents : <:ete:1516467133163507764> Dragon d'été & <:automne:1516467039391322112> Dragon d'automne & <:hiver:1516467101366358110> Dragon d'hiver &\n"
        "<:printemps:1516467069003235579> Dragon de printemps"
    ),
    "Dragon des galaxies": (
        "<:galaxie:1516468246247641320> Dragon des galaxies\n"
        "Rareté : Divin\n"
        "Obtention : Hybride\n"
        "Parents : <:etoile:1516468341659799813> Dragon des étoiles & <:lune:1516465571187658904> Dragon de la lune & <:soleil:1516465538988114021> Dragon de soleil"
    ),
    "Dragon de l'univers": (
        "<:univers:1516467318874439882> Dragon de l'univers\n"
        "Rareté : Unique\n"
        "Obtention : Hybride (Posseder tous les dragons du serveur hors raté et divins au stade maximal ainsi que 10 noyaux de puissance)\n"
    ),
    "Dragon raté": (
        "<:rate:1516465121398882304> Dragon raté\n"
        "Obtention : Hybridation raté (1 chance sur 5)\n"
    )
}

DRAGONCOLLEC = {
    "Dragon de feu": {
        "emoji": "<:feu:1516458328715169883>",
        "rarete": "Commun",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon de glace": {
        "emoji": "<:glace:1516458617211977890>",
        "rarete": "Commun",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon de poison": {
        "emoji": "<:poison:1516458574232948968>",
        "rarete": "Commun",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon électrique": {
        "emoji": "<:elec:1516458643435032787>",
        "rarete": "Commun",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon d'eau": {
        "emoji": "<:eau:1516465397950582896>",
        "rarete": "Commun",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon de sable": {
        "emoji": "<:sable:1516465432670900416>",
        "rarete": "Commun",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon des ombres": {
        "emoji": "<:ombres:1516466733475692725>",
        "rarete": "Commun",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon de lumière": {
        "emoji": "<:lumiere:1516468032900304946>",
        "rarete": "Commun",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon de vent": {
        "emoji": "<:vent:1516459149624606841>",
        "rarete": "Commun",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon de pierre": {
        "emoji": "<:pierre:1516459120872394913>",
        "rarete": "Commun",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon d'argile": {
        "emoji": "<:argile:1516465277129326732>",
        "rarete": "Commun",
        "obtention": "Hybride",
        "parents": ["Dragon d'eau", "Dragon de sable"]
    },

    "Dragon de cristal": {
        "emoji": "<:crystal:1516465235794591916>",
        "rarete": "Commun",
        "obtention": "Hybride",
        "parents": ["Dragon de glace", "Dragon de pierre"]
    },

    "Dragon de lave": {
        "emoji": "<:lave:1516465317188993025>",
        "rarete": "Commun",
        "obtention": "Hybride",
        "parents": ["Dragon de feu", "Dragon de pierre"]
    },

    "Dragon spectral": {
        "emoji": "<:spectral:1516466639716221199>",
        "rarete": "Commun",
        "obtention": "Hybride",
        "parents": ["Dragon des ombres", "Dragon de vent"]
    },

    "Dragon d'orage": {
        "emoji": "<:orage:1516466828015177970>",
        "rarete": "Commun",
        "obtention": "Hybride",
        "parents": ["Dragon électrique", "Dragon de vent"]
    },

    "Dragon des cavernes": {
        "emoji": "<:cavernes:1516467653219454986>",
        "rarete": "Commun",
        "obtention": "Hybride",
        "parents": ["Dragon de pierre", "Dragon des ombres"]
    },

    "Dragon de poussière": {
        "emoji": "<:poussiere:1516466371830223013>",
        "rarete": "Commun",
        "obtention": "Hybride",
        "parents": ["Dragon de pierre", "Dragon de vent"]
    },

    "Dragon des vagues": {
        "emoji": "<:vagues:1516497154934313101>",
        "rarete": "Commun",
        "obtention": "Hybride",
        "parents": ["Dragon d'eau", "Dragon de vent"]
    },

    "Dragon radioactif": {
        "emoji": "<:radioactif:1516468277251936457>",
        "rarete": "Commun",
        "obtention": "Hybride",
        "parents": ["Dragon de poison", "Dragon de vent"]
    },

    "Dragon du soleil": {
        "emoji": "<:soleil:1516465538988114021>",
        "rarete": "Rare",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon de la lune": {
        "emoji": "<:lune:1516465571187658904>",
        "rarete": "Rare",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon de sang": {
        "emoji": "<:sang:1516466216330461305>",
        "rarete": "Rare",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon chromatique": {
        "emoji": "<:chromatique:1516465473632600174>",
        "rarete": "Rare",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon corrompu": {
        "emoji": "<:corrompu:1516465727232544919>",
        "rarete": "Rare",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon des cieux": {
        "emoji": "<:cieux:1516468067113369691>",
        "rarete": "Rare",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon miroir": {
        "emoji": "<:miroir:1516467444326338732>",
        "rarete": "Rare",
        "obtention": "Hybride",
        "parents": ["Dragon de cristal", "Dragon des ombres"]
    },

    "Dragon possédé": {
        "emoji": "<:possede:1516467205556932668>",
        "rarete": "Rare",
        "obtention": "Hybride",
        "parents": ["Dragon spectral", "Dragon de feu"]
    },

    "Dragon de métal": {
        "emoji": "<:metal:1516466265349292253>",
        "rarete": "Rare",
        "obtention": "Hybride",
        "parents": ["Dragon de pierre", "Dragon de cristal"]
    },

    "Dragon d'obsidienne": {
        "emoji": "<:obsidienne:1516466517640876153>",
        "rarete": "Rare",
        "obtention": "Hybride",
        "parents": ["Dragon de lave", "Dragon d'eau"]
    },

    "Dragon de terreur": {
        "emoji": "<:terreur:1516466238203629578>",
        "rarete": "Rare",
        "obtention": "Hybride",
        "parents": ["Dragon spectral", "Dragon des ombres"]
    },

    "Dragon de plante": {
        "emoji": "<:plante:1516465362768756787>",
        "rarete": "Rare",
        "obtention": "Hybride",
        "parents": ["Dragon d'argile", "Dragon d'eau"]
    },

    "Dragon de la mer": {
        "emoji": "<:mer:1516467412516474981>",
        "rarete": "Rare",
        "obtention": "Hybride",
        "parents": ["Dragon des vagues", "Dragon de vent"]
    },

    "Dragon de diamant": {
        "emoji": "<:diamant:1516468370445172756>",
        "rarete": "Rare",
        "obtention": "Hybride",
        "parents": ["Dragon de lave", "Dragon de cristal"]
    },

    "Dragon des abysses": {
        "emoji": "<:abysses:1516467472193028116>",
        "rarete": "Rare",
        "obtention": "Hybride",
        "parents": ["Dragon des cavernes", "Dragon des ombres"]
    },

    "Grand Dragon Doré": {
        "emoji": "<:dor:1516465064259883238>",
        "rarete": "Épique",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon de l'automne": {
        "emoji": "<:automne:1516467039391322112>",
        "rarete": "Épique",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon de l'hiver": {
        "emoji": "<:hiver:1516467101366358110>",
        "rarete": "Épique",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon de l'été": {
        "emoji": "<:ete:1516467133163507764>",
        "rarete": "Épique",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon du printemps": {
        "emoji": "<:printemps:1516467069003235579>",
        "rarete": "Épique",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon musical": {
        "emoji": "<:musical:1516469012135936080>",
        "rarete": "Épique",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon détruit": {
        "emoji": "<:detruit:1516466796507431006>",
        "rarete": "Épique",
        "obtention": "Hybride",
        "parents": ["Dragon corrompu", "Dragon raté"]
    },

    "Dragon de la nuit": {
        "emoji": "<:nuit:1516467758018068653>",
        "rarete": "Épique",
        "obtention": "Hybride",
        "parents": ["Dragon des ombres", "Dragon de la lune"]
    },

    "Dragon mécanique": {
        "emoji": "<:mecanique:1516466450246799401>",
        "rarete": "Épique",
        "obtention": "Hybride",
        "parents": ["Dragon de métal", "Dragon électrique"]
    },

    "Dragon de rouille": {
        "emoji": "<:rouille:1516466486804353206>",
        "rarete": "Épique",
        "obtention": "Hybride",
        "parents": ["Dragon de métal", "Dragon d'eau"]
    },

    "Dragon champignon": {
        "emoji": "<:champignon:1516466761690648586>",
        "rarete": "Épique",
        "obtention": "Hybride",
        "parents": ["Dragon de poison", "Dragon de plante"]
    },

    "Dragon pissenlit": {
        "emoji": "<:pissenlit:1516467168022237385>",
        "rarete": "Épique",
        "obtention": "Hybride",
        "parents": ["Dragon de plante", "Dragon de vent"]
    },

    "Dragon d'améthyste": {
        "emoji": "<:amethyste:1516467723788357632>",
        "rarete": "Épique",
        "obtention": "Hybride",
        "parents": ["Dragon de cristal", "Dragon des abysses"]
    },

    "Dragon de fleur": {
        "emoji": "<:fleur:1516465875769753830>",
        "rarete": "Épique",
        "obtention": "Hybride",
        "parents": ["Dragon de plante", "Dragon d'eau"]
    },

    "Dragon de pouvoir": {
        "emoji": "<:pouvoir:1516467236666343535>",
        "rarete": "Épique",
        "obtention": "Hybride",
        "parents": ["Dragon spectral", "Dragon de terreur"]
    },

    "Dragon des nuages": {
        "emoji": "<:nuages:1516468120078913776>",
        "rarete": "Épique",
        "obtention": "Hybride",
        "parents": ["Dragon des cieux", "Dragon de vent"]
    },

    "Dragon du crépuscule": {
        "emoji": "<:crepuscule:1516468179013210153>",
        "rarete": "Épique",
        "obtention": "Hybride",
        "parents": ["Dragon des cieux", "Dragon des ombres"]
    },

    "Dragon de l'aube": {
        "emoji": "<:aube:1516468215860039805>",
        "rarete": "Épique",
        "obtention": "Hybride",
        "parents": ["Dragon des cieux", "Dragon de lumière"]
    },

    "Dragon ancestral": {
        "emoji": "<:ancestral:1516468148436734112>",
        "rarete": "Légendaire",
        "obtention": "Œuf",
        "parents": None
    },

    "Dragon de corail": {
        "emoji": "<:corail:1516467347769262211>",
        "rarete": "Légendaire",
        "obtention": "Hybride",
        "parents": ["Dragon de la mer", "Dragon de plante"]
    },

    "Dragon diabolique": {
        "emoji": "<:diabolique:1516530044938359074>",
        "rarete": "Légendaire",
        "obtention": "Hybride",
        "parents": ["Dragon de terreur", "Dragon de sang"]
    },

    "Dragon arc-en-ciel": {
        "emoji": "<:arc_en_ciel:1516466111602757733>",
        "rarete": "Légendaire",
        "obtention": "Hybride",
        "parents": ["Dragon miroir", "Dragon chromatique"]
    },

    "Dragon caméléon": {
        "emoji": "<:cameleon:1516465832345993431>",
        "rarete": "Légendaire",
        "obtention": "Hybride",
        "parents": ["Dragon de fleur", "Dragon chromatique"]
    },

    "Dragon éclipse": {
        "emoji": "<:eclipse:1516466858104979537>",
        "rarete": "Légendaire",
        "obtention": "Hybride",
        "parents": ["Dragon de la lune", "Dragon du soleil"]
    },

    "Dragon des aurores": {
        "emoji": "<:aurores:1516467798430191646>",
        "rarete": "Légendaire",
        "obtention": "Hybride",
        "parents": ["Dragon de la nuit", "Dragon du soleil"]
    },

    "Dragon des étoiles": {
        "emoji": "<:etoile:1516468341659799813>",
        "rarete": "Légendaire",
        "obtention": "Hybride",
        "parents": ["Dragon des cieux", "Dragon du soleil"]
    },

    "Dragon compacté": {
        "emoji": "<:compacte:1517138088298676264>",
        "rarete": "Légendaire",
        "obtention": "Hybride",
        "parents": ["Dragon raté"] * 15
    },

    "Dragon de l'espace": {
        "emoji": "<:espace:1516467268165304491>",
        "rarete": "Divin",
        "obtention": "Hybride",
        "parents": ["Dragon arc-en-ciel", "Dragon éclipse"]
    },

    "Dragon du temps": {
        "emoji": "<:temps:1516467293037662321>",
        "rarete": "Divin",
        "obtention": "Hybride",
        "parents": ["Dragon de l'automne", "Dragon de l'hiver", "Dragon de l'été", "Dragon du printemps"]
    },

    "Dragon des galaxies": {
        "emoji": "<:galaxie:1516468246247641320>",
        "rarete": "Divin",
        "obtention": "Hybride",
        "parents": ["Dragon des étoiles", "Dragon de la lune", "Dragon du soleil"]
    },

    "Dragon de l'univers": {
        "emoji": "<:univers:1516467318874439882>",
        "rarete": "Unique",
        "obtention": "Hybride",
        "parents": [
            "Dragon de feu", "Dragon de glace", "Dragon de poison", "Dragon électrique",
            "Dragon d'eau", "Dragon de sable", "Dragon des ombres", "Dragon de lumière",
            "Dragon de vent", "Dragon de pierre", "Dragon d'argile", "Dragon de cristal",
            "Dragon de lave", "Dragon spectral", "Dragon d'orage", "Dragon des cavernes",
            "Dragon de poussière", "Dragon des vagues", "Dragon radioactif", "Dragon du soleil",
            "Dragon de la lune", "Dragon de sang", "Dragon chromatique", "Dragon corrompu",
            "Dragon des cieux", "Dragon miroir", "Dragon possédé", "Dragon de métal",
            "Dragon d'obsidienne", "Dragon de terreur", "Dragon de plante", "Dragon de la mer",
            "Dragon de diamant", "Dragon des abysses", "Grand Dragon Doré", "Dragon de l'automne",
            "Dragon de l'hiver", "Dragon de l'été", "Dragon du printemps", "Dragon musical",
            "Dragon détruit", "Dragon de la nuit", "Dragon mécanique", "Dragon de rouille",
            "Dragon champignon", "Dragon pissenlit", "Dragon d'améthyste", "Dragon de fleur",
            "Dragon de pouvoir", "Dragon des nuages", "Dragon du crépuscule", "Dragon de l'aube",
            "Dragon ancestral", "Dragon de corail", "Dragon diabolique", "Dragon arc-en-ciel",
            "Dragon caméléon", "Dragon éclipse", "Dragon des aurores", "Dragon des étoiles",
            "Dragon compacté"
        ]
    },

    "Dragon raté": {
        "emoji": "<:rate:1516465121398882304>",
        "rarete": "Commun",
        "obtention": "Hybride",
        "parents": None
    }
}




print("Lancement du bot...")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# on ready module

@bot.event
async def on_ready():
    print("Bot allumé !")
    # Synchroniser les commandes
    try:
        #sinc
        synced = await bot.tree.sync()
        print(f"Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        print(e)
    data = load_data()

    # --- Initialisation du système de combat ---
    if "combats" not in data:
        data["combats"] = {}

    save_data(data)
    try:
        check_combats.start()
    except RuntimeError:
        pass  # évite l'erreur si la task est déjà lancée

ALLOWED_GUILD_ID = 1494821494604435536  # ID de TON serveur

@bot.event
async def on_guild_join(guild):
    if guild.id != ALLOWED_GUILD_ID:
        await guild.leave()


# auto money on message 15/30

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    channel_id = str(message.channel.id)
    user_id = str(message.author.id)
    if last_message_author.get(channel_id) == user_id:
        last_message_author[channel_id] = user_id
        return await bot.process_commands(message)
    last_message_author[channel_id] = user_id
    data = load_data()
    user_data = get_user_data(data, user_id)
    longueur = len(message.content)
    if longueur < 5:
        gain_base = 15
    else:
        gain_base = 30
    gain_total = gain_base * user_data["boost"]
    user_data["money"] += gain_total
    save_data(data)
    await bot.process_commands(message)

# truc de copilot pour le fichier de bank ou economy

def load_data():
    try:
        with open("economy.json", "r", encoding="utf-8") as f:
            content = f.read().strip()

            # 🔥 Si le fichier est vide → on recrée une base propre
            if not content:
                print("⚠️ Fichier JSON vide, recréation...")
                return {}

            return json.loads(content)

    except json.JSONDecodeError:
        print("⚠️ JSON corrompu, recréation...")
        return {}

    except FileNotFoundError:
        print("⚠️ Fichier JSON introuvable, création...")
        return {}


def save_data(data):
    tmp_file = "economy_tmp.json"

    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    os.replace(tmp_file, "economy.json")


def get_user_data(data, user_id):
    user_id = str(user_id)

    # Création du joueur s'il n'existe pas
    if user_id not in data:
        data[user_id] = {
            "money": 0,
            "boost": 1,
            "job_level": 0,
            "last_daily": "",
            "inventory": [],

            # Ferme
            "farm": False,

            # Pêche
            "fishing_rod": 1,
            "last_fish": 0,
            "fish_inventory": [],

            # Dragons (liste de stades)
            "dragons": {},

            # Tokens (système RI)
            "tokens": 0,

            # Quêtes de progression
            "progress_quests": {
                "boost3": False,
                "forgeron4": False,
                "ferme": False,
                "fish10000": False,
                "canne_max": False
            }
        }
        return data[user_id]

    # --- MISE À JOUR DES ANCIENS JOUEURS (compatibilité) ---

    if "money" not in data[user_id]:
        data[user_id]["money"] = 0

    if "boost" not in data[user_id]:
        data[user_id]["boost"] = 1

    if "job_level" not in data[user_id]:
        data[user_id]["job_level"] = 0

    if "last_daily" not in data[user_id]:
        data[user_id]["last_daily"] = ""

    if "inventory" not in data[user_id]:
        data[user_id]["inventory"] = []

    # Ferme
    if "farm" not in data[user_id]:
        data[user_id]["farm"] = False

    # Pêche
    if "fishing_rod" not in data[user_id]:
        data[user_id]["fishing_rod"] = 1

    if "last_fish" not in data[user_id]:
        data[user_id]["last_fish"] = 0

    if "fish_inventory" not in data[user_id]:
        data[user_id]["fish_inventory"] = []

    # Dragons
    if "dragons" not in data[user_id]:
        data[user_id]["dragons"] = {}

    # Tokens
    if "tokens" not in data[user_id]:
        data[user_id]["tokens"] = 0


    # Sécurité : si l'utilisateur n'a pas encore la structure, on la crée
    if "progress_quests" not in data[user_id]:
        user_data["progress_quests"] = {
            "boost3": False,
            "forgeron4": False,
            "ferme": False,
            "fish10000": False,
            "canne_max": False
            }
    if "combats" not in data:
        data["combats"] = {}

    save_data(data)

    return data[user_id]





def add_item_to_inventory(data, user_id, item_name):
    user_data = get_user_data(data, user_id)
    user_data["inventory"].append(item_name)
    save_data(data)

def remove_item_from_inventory(data, user_id, item_name):
    user_data = get_user_data(data, user_id)
    if item_name in user_data["inventory"]:
        user_data["inventory"].remove(item_name)
        save_data(data)
        return True
    return False

async def autocomplete_items(interaction: discord.Interaction, current: str):
    suggestions = []

    for item in SHOP_ITEMS.keys():
        # Nettoyer le nom : enlever l'emoji au début
        clean_name = item.split(" ", 1)[1] if " " in item else item

        # Filtrer selon ce que tape l'utilisateur
        if current.lower() in clean_name.lower():
            suggestions.append(
                discord.app_commands.Choice(
                    name=clean_name,   # affiché dans Discord
                    value=item         # valeur réelle (avec emoji)
                )
            )

    return suggestions[:25]


async def autocomplete_inventory(interaction: discord.Interaction, current: str):
    data = load_data()
    user_data = get_user_data(data, interaction.namespace.membre.id)
    inventory = user_data["inventory"]

    # On stack pour éviter les doublons
    from collections import Counter
    stacked = Counter(inventory)

    return [
        discord.app_commands.Choice(name=f"{item} x{amount}", value=item)
        for item, amount in stacked.items()
        if current.lower() in item.lower()
    ][:25]

async def autocomplete_dragons(interaction: discord.Interaction, current: str):
    return [
        discord.app_commands.Choice(name=name, value=name)
        for name in DRAGONS.keys()
        if current.lower() in name.lower()
    ][:25]


import random

def get_random_fish():
    roll = random.randint(1, 100)
    cumulative = 0
    for fish, chance in FISH_LOOT:
        cumulative += chance
        if roll <= cumulative:
            return fish


@bot.event
async def on_member_update(before, after):

    # Chercher les rôles ajoutés
    new_roles = [r for r in after.roles if r not in before.roles]

    if not new_roles:
        return

    data = load_data()
    user_data = get_user_data(data, after.id)

    for role in new_roles:
        for ri_value, role_id in RI_ROLE_IDS.items():

            if role.id == role_id:

                tokens_to_add = RI_TOKEN_REWARDS[ri_value]

                # Ajouter les tokens
                user_data["tokens"] += tokens_to_add
                save_data(data)
                await complete_daily_quest(after.id, 16)

                # Message dans un salon (ou en MP)
                try:
                    await after.send(
                        f"🎉 Tu as reçu **{tokens_to_add} token(s)** 🪙"
                    )
                except:
                    pass  # si MP fermés

                # Optionnel : message dans un salon public
                # channel = bot.get_channel(ID_DU_SALON)
                # await channel.send(f"{after.mention} a gagné {tokens_to_add} tokens grâce au rôle RI {ri_value} !")

                break


import random

def tirer_rareté(type_oeuf):
    table = EGG_PROBAS[type_oeuf]
    roll = random.randint(1, 100)
    cumul = 0
    for rarete, chance in table:
        cumul += chance
        if roll <= cumul:
            return rarete

def tirer_dragon_selon_rareté(rarete):
    candidats = [
        nom for nom, info in DRAGONCOLLEC.items()
        if info["rarete"] == rarete and info["obtention"] == "Œuf"
    ]
    return random.choice(candidats) if candidats else None

RARETES_OEUFS = ["commun", "rare", "epique"]

async def autocomplete_rarete(interaction: discord.Interaction, current: str):
    return [
        discord.app_commands.Choice(name=r, value=r)
        for r in RARETES_OEUFS
        if current.lower() in r.lower()
    ]


# le bouton

class BoostButton(discord.ui.View):
    def __init__(self, owner_id, user_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.user_id = user_id

    @discord.ui.button(label="Acheter le boost", style=discord.ButtonStyle.gray)
    async def buy_boost(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("❌ Ce bouton ne t'appartient pas.", ephemeral=True)

        data = load_data()
        user_data = get_user_data(data, self.user_id)

        boost = user_data["boost"]
        money = user_data["money"]

        # Vérifier si un prix existe pour le prochain boost
        if boost not in BOOST_PRICES:
            return await interaction.response.send_message("❌ Tu as déjà le boost maximum !", ephemeral=True)

        price = BOOST_PRICES[boost]

        if money < price:
            return await interaction.response.send_message(
                f"❌ Il te faut **{price}💰** pour améliorer ton boost.",
                ephemeral=True
            )

        # Achat
        user_data["money"] -= price
        user_data["boost"] += 1
        save_data(data)

        # Quête progression
        if user_data["boost"] == 3:
            await complete_progress_quest(interaction.user.id, "boost3")

        # Quête journalière
        await complete_daily_quest(interaction.user.id, 11)

        # NOUVEL ÉTAT APRÈS ACHAT
        new_boost = user_data["boost"]

        if new_boost in BOOST_PRICES:
            new_price = BOOST_PRICES[new_boost]
            price_text = f"Prix du prochain boost : **{new_price}💰**"
        else:
            price_text = "🚀 Tu as déjà le boost maximum !"

        # NOUVEL EMBED
        embed = discord.Embed(
            title="Boost",
            description=(
                f"🔼 Boost actuel : **x{new_boost}**\n"
                f"{price_text}"
            ),
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        # Si boost max → retirer le bouton
        if new_boost not in BOOST_PRICES:
            self.clear_items()

        # Mettre à jour le message original
        await interaction.response.edit_message(embed=embed, view=self)


# le 2eme bouton

class JobUpgradeButton(discord.ui.View):
    def __init__(self, owner_id, user_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.user_id = user_id

    @discord.ui.button(label="Améliorer le métier", style=discord.ButtonStyle.gray)
    async def upgrade_job(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message(
                "❌ Ce bouton ne t'appartient pas.", ephemeral=True
            )

        data = load_data()
        user_data = get_user_data(data, self.user_id)

        level = user_data["job_level"]

        if level >= 6:
            return await interaction.response.send_message(
                "🔥 Tu as déjà le niveau maximum de Forgeron !", ephemeral=True
            )

        price = JOB_UPGRADE_PRICES[level]

        if user_data["money"] < price:
            return await interaction.response.send_message(
                f"❌ Il te faut **{price}💰** pour améliorer ton métier.",
                ephemeral=True
            )

        # Achat
        user_data["money"] -= price
        user_data["job_level"] += 1
        save_data(data)

        # Quête progression
        if user_data["job_level"] == 4:
            await complete_progress_quest(interaction.user.id, "forgeron4")

        # Quête journalière
        await complete_daily_quest(interaction.user.id, 9)

        # Nouveau niveau
        new_level = user_data["job_level"]

        # Déterminer le prix du prochain niveau
        if new_level < 6:
            new_price = JOB_UPGRADE_PRICES[new_level]
            price_text = f"💸 Prix du prochain niveau : **{new_price}💰**"
        else:
            price_text = "🔥 Tu as déjà le niveau maximum !"

        # NOUVEL EMBED
        embed = discord.Embed(
            title="🔨 Métier de Forgeron",
            description=(
                f"🔼 Niveau actuel : **{new_level}**\n"
                f"{price_text}"
            ),
            color=discord.Color.orange()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        # Si niveau max → retirer le bouton
        if new_level >= 6:
            self.clear_items()

        # Modifier le message original
        await interaction.response.edit_message(embed=embed, view=self)



class FarmButton(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    @discord.ui.button(label="Acheter la ferme (50 000💰)", style=discord.ButtonStyle.green)
    async def buy_farm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("❌ Ce bouton ne t'appartient pas.", ephemeral=True)

        data = load_data()
        user_data = get_user_data(data, interaction.user.id)

        if user_data["farm"]:
            return await interaction.response.send_message("🐐 Tu possèdes déjà la ferme !", ephemeral=True)

        if user_data["money"] < 50000:
            return await interaction.response.send_message("❌ Tu n'as pas assez d'argent pour acheter la ferme.", ephemeral=True)

        # Achat
        user_data["money"] -= 50000
        user_data["farm"] = True
        save_data(data)

        # Quêtes progression + journalière
        await complete_progress_quest(interaction.user.id, "ferme")
        await complete_daily_quest(interaction.user.id, 12)

        # NOUVEL EMBED APRÈS ACHAT
        embed = discord.Embed(
            title="🐐 Ferme",
            description=(
                "🐐 **Tu possèdes déjà la ferme !**\n"
                "Chaque jour, tu reçois **1 chèvre** dans ton `/daily`."
            ),
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        # On retire les boutons
        self.clear_items()

        # On MODIFIE le message original
        await interaction.response.edit_message(embed=embed, view=self)



class FishingUpgradeButton(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    @discord.ui.button(label="Améliorer la canne", style=discord.ButtonStyle.green)
    async def upgrade(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message(
                "❌ Ce bouton ne t'appartient pas.", ephemeral=True
            )

        data = load_data()
        user_data = get_user_data(data, interaction.user.id)

        rod = user_data["fishing_rod"]

        if rod >= 3:
            return await interaction.response.send_message(
                "🎣 Tu as déjà la canne maximale !", ephemeral=True
            )

        next_price = FISHING_RODS[rod + 1]["price"]

        if user_data["money"] < next_price:
            return await interaction.response.send_message(
                f"❌ Il te faut **{next_price}💰** pour améliorer ta canne.",
                ephemeral=True
            )

        # Achat
        user_data["money"] -= next_price
        user_data["fishing_rod"] += 1
        save_data(data)

        # Quête progression
        if user_data["fishing_rod"] == 3:
            await complete_progress_quest(interaction.user.id, "canne_max")

        # Quête journalière
        await complete_daily_quest(interaction.user.id, 10)

        # Nouveau niveau
        new_rod = user_data["fishing_rod"]

        # Déterminer le prix du prochain niveau
        if new_rod < 3:
            new_price = FISHING_RODS[new_rod + 1]["price"]
            price_text = f"💸 Prix du prochain niveau : **{new_price}💰**"
        else:
            price_text = "🎣 Tu as déjà la canne maximale !"

        # NOUVEL EMBED
        embed = discord.Embed(
            title="🎣 Canne à pêche",
            description=(
                f"🔼 Niveau actuel : **{new_rod}**\n"
                f"{price_text}"
            ),
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        # Si canne max → retirer le bouton
        if new_rod >= 3:
            self.clear_items()

        # Modifier le message original
        await interaction.response.edit_message(embed=embed, view=self)


class TaniereView(discord.ui.View):
    def __init__(self, pages, user):
        super().__init__(timeout=60)
        self.pages = pages
        self.index = 0
        self.user = user

    async def update(self, interaction):
        embed = self.pages[self.index]
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            return await interaction.response.send_message("❌ Ce menu ne t'appartient pas.", ephemeral=True)

        if self.index > 0:
            self.index -= 1
            await self.update(interaction)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            return await interaction.response.send_message("❌ Ce menu ne t'appartient pas.", ephemeral=True)

        if self.index < len(self.pages) - 1:
            self.index += 1
            await self.update(interaction)



# /argent
@bot.tree.command(name="argent", description="Voir ton argent ou celui d'un membre")
async def argent(interaction: discord.Interaction, membre: discord.Member | None = None):
    data = load_data()
    cible = membre or interaction.user
    user_id = str(cible.id)
    data = load_data()
    user_data = get_user_data(data, user_id)
    argent = user_data["money"]
    embedun = discord.Embed(title=f"Argent de {cible.display_name}", description=f"**{argent}** 💰", color=discord.Color.red())
    embedun.set_thumbnail(url=cible.display_avatar.url)
    await interaction.response.send_message(embed=embedun)

# /give

@bot.tree.command(name="give", description="Donner de l'argent à un membre (admin)")
async def give(interaction: discord.Interaction, membre: discord.Member, montant: int):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)
    if montant <= 0:
        return await interaction.response.send_message("❌ Le montant doit être supérieur à 0.", ephemeral=True)
    data = load_data()
    user_id = str(membre.id)
    data = load_data()
    user_data = get_user_data(data, user_id)
    user_data["money"] += montant
    save_data(data)
    embeddeux = discord.Embed(title="Give", description=f"{membre.mention} a reçu **{montant}** 💰 !", color=discord.Color.red())
    await interaction.response.send_message(embed=embeddeux)


# /remove

@bot.tree.command(name="remove", description="Retirer de l'argent à un membre (admin)")
async def remove(interaction: discord.Interaction, membre: discord.Member, montant: int):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)
    if montant <= 0:
        return await interaction.response.send_message("❌ Le montant doit être supérieur à 0.", ephemeral=True)
    data = load_data()
    user_id = str(membre.id)
    data = load_data()
    user_data = get_user_data(data, user_id)
    argent_actuel = user_data["money"]
    save_data(data)
    if argent_actuel - montant < 0:
        return await interaction.response.send_message(f"⚠️ {membre.mention} n'a pas assez d'argent pour retirer **{montant}** 💰.", ephemeral=True)
    user_data["money"] -= montant
    save_data(data)
    embedtrois = discord.Embed(title="Retrait d'argent", description=f"{montant} 💰 ont été retirées à {membre.mention}.", color=discord.Color.red())
    await interaction.response.send_message(embed=embedtrois)


# /boost
@bot.tree.command(name="boost", description="Voir et améliorer ton boost")
async def boost(interaction: discord.Interaction):
    user_id = interaction.user.id
    data = load_data()
    user_data = get_user_data(data, user_id)
    boost = user_data["boost"]
    # Déterminer le prix du prochain boost
    if boost in BOOST_PRICES:
        price = BOOST_PRICES[boost]
        price_text = f"Prix du prochain boost : **{price}** 💰"
    else:
        price_text = "🚀 Tu as déjà le boost maximum !"
    embedquatre = discord.Embed(title="Boost", description=(
        f"🔼 Boost actuel : **x{boost}**\n"
        f"{price_text}"
    ), color=discord.Color.gold())
    embedquatre.set_thumbnail(url=interaction.user.display_avatar.url)
    view = BoostButton(interaction.user.id, user_id)
    await interaction.response.send_message(embed=embedquatre, view=view)

# /pay
@bot.tree.command(name="pay", description="Payer un membre avec ton argent")
async def pay(interaction: discord.Interaction, membre: discord.Member, montant: int):
    if montant <= 0:
        return await interaction.response.send_message("❌ Le montant doit être supérieur à 0.", ephemeral=True)
    if membre.id == interaction.user.id:
        return await interaction.response.send_message("❌ Tu ne peux pas te payer toi-même.", ephemeral=True)
    data = load_data()
    sender_id = str(interaction.user.id)
    receiver_id = str(membre.id)
    sender_data = get_user_data(data, sender_id)
    receiver_data = get_user_data(data, receiver_id)
    if sender_data["money"] < montant:
        return await interaction.response.send_message(f"❌ Tu n'as pas assez d'argent pour envoyer **{montant}** 💰.", ephemeral=True)
    sender_data["money"] -= montant
    receiver_data["money"] += montant
    save_data(data)
    embedcinq = discord.Embed(title="💸 Paiement effectué", description=(f"**{interaction.user.mention}** a envoyé **{montant}** 💰 à **{membre.mention}** !"), color=discord.Color.green())
    await interaction.response.send_message(embed=embedcinq)

# /daily

@bot.tree.command(name="daily", description="Récupère ton revenu quotidien")
async def daily(interaction: discord.Interaction):

    # Empêche l'erreur Unknown interaction
    await interaction.response.defer(ephemeral=False)

    user_id = interaction.user.id
    data = load_data()
    user_data = get_user_data(data, user_id)

    tz = pytz.timezone("Europe/Paris")
    today = datetime.now(tz).strftime("%Y-%m-%d")

    if user_data["last_daily"] == today:
        return await interaction.followup.send(
            "⏳ Tu as déjà récupéré ton daily aujourd'hui ! Reviens demain.",
            ephemeral=True
        )

    job_level = user_data["job_level"]
    job_bonus = JOB_INCOME.get(job_level, 0)
    total_income = DAILY_BASE + job_bonus

    # Gains d'argent
    user_data["money"] += total_income

    # Bonus ferme
    ferme_bonus = ""
    if user_data.get("farm", False):
        user_data["inventory"].append("🐐 Chèvre")
        ferme_bonus = "\nFerme : **1 chèvre** ajoutée à ton inventaire 🐐"

    user_data["last_daily"] = today
    save_data(data)

    embedsix = discord.Embed(
        title="💰 Revenu quotidien",
        description=(
            f"Revenu de base : **{DAILY_BASE}** 💰\n"
            f"Bonus métier (Forgeron niv. {job_level}) : **{job_bonus}** 💰\n"
            f"{ferme_bonus}\n"
            f"\n➡️ Total reçu : **{total_income}** 💰"
        ),
        color=discord.Color.green()
    )
    embedsix.set_thumbnail(url=interaction.user.display_avatar.url)

    await interaction.followup.send(embed=embedsix)


# /forgeron

@bot.tree.command(name="forgeron", description="Voir et améliorer ton métier de forgeron")
async def forgeron(interaction: discord.Interaction):
    user_id = interaction.user.id
    data = load_data()
    user_data = get_user_data(data, user_id)
    level = user_data["job_level"]
    if level < 6:
        price = JOB_UPGRADE_PRICES[level]
        price_text = f"💸 Prix du prochain niveau : **{price}** 💰"
    else:
        price_text = "🔥 Tu as déjà le niveau maximum !"
    embedsept = discord.Embed(title=f"🔨 Métier de Forgeron", description=(
        f"🔼 Niveau actuel : **{level}**\n"
        f"{price_text}"
    ), color=discord.Color.orange())
    embedsept.set_thumbnail(url=interaction.user.display_avatar.url)
    view = JobUpgradeButton(interaction.user.id, user_id)
    await interaction.response.send_message(embed=embedsept, view=view)

# /inventory

@bot.tree.command(name="inventaire", description="Affiche l'inventaire d'un membre")
async def inventaire(interaction: discord.Interaction, membre: discord.Member | None = None):

    # Si aucun membre n'est donné → on prend l'utilisateur
    cible = membre or interaction.user

    data = load_data()
    user_data = get_user_data(data, cible.id)
    inventory = user_data["inventory"]

    from collections import Counter
    stacked = Counter(inventory)

    if len(inventory) == 0:
        inv_text = "🕳️ Cet inventaire est vide."
    else:
        inv_text = "\n".join([f"- {item} x{amount}" for item, amount in stacked.items()])

    embed = discord.Embed(
        title=f"📦 Inventaire de {cible.display_name}",
        description=inv_text,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=cible.display_avatar.url)

    await interaction.response.send_message(embed=embed)


# /boutique

@bot.tree.command(name="boutique", description="Affiche la boutique du Donjon")
async def boutique(interaction: discord.Interaction):
    data = load_data()
    user_data = get_user_data(data, interaction.user.id)
    money = user_data["money"]

    embed = discord.Embed(
        title="🛒 Boutique du Donjon",
        description=f"Tu as **{money}💰**.\n\n/buy pour acheter des objets.",
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    for item_name, price in SHOP_ITEMS.items():
        embed.add_field(
            name=item_name,
            value=f"💰 **{price}**",
            inline=False
        )

    await interaction.response.send_message(embed=embed)


# /buy

@bot.tree.command(name="buy", description="Acheter un objet de la boutique")
@discord.app_commands.autocomplete(objet=autocomplete_items)
async def buy(interaction: discord.Interaction, objet: str, quantité: int = 1):

    if quantité <= 0:
        return await interaction.response.send_message(
            "❌ La quantité doit être d'au moins **1**.",
            ephemeral=True
        )

    if objet not in SHOP_ITEMS:
        return await interaction.response.send_message(
            "❌ Cet objet n'existe pas dans la boutique.",
            ephemeral=True
        )

    prix_unitaire = SHOP_ITEMS[objet]
    prix_total = prix_unitaire * quantité

    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    if user_data["money"] < prix_total:
        return await interaction.response.send_message(
            f"❌ Il te manque **{prix_total - user_data['money']}💰** pour acheter **{quantité}× {objet}**.",
            ephemeral=True
        )

    # Achat
    user_data["money"] -= prix_total
    for _ in range(quantité):
        user_data["inventory"].append(objet)

    save_data(data)
    if objet.startswith("<:noyau_de_puissance"):
        await complete_daily_quest(interaction.user.id, 7)

    embed = discord.Embed(
        title="🎉 Achat effectué",
        description=(
            f"Tu as acheté **{quantité}× {objet}** pour **{prix_total}💰** !"
        ),
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)

    
# /setboost

@bot.tree.command(name="setboost", description="Définir le boost d'un membre (admin)")
async def setboost(interaction: discord.Interaction, membre: discord.Member, niveau: int):

    # Vérification permissions admin
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            "❌ Tu n'as pas la permission d'utiliser cette commande.",
            ephemeral=True
        )

    # Vérification limites
    if niveau < 1 or niveau > 3:
        return await interaction.response.send_message(
            "❌ Le boost doit être compris entre **1 et 3**.",
            ephemeral=True
        )

    # Charger données
    data = load_data()
    user_data = get_user_data(data, membre.id)

    # Appliquer le boost
    user_data["boost"] = niveau
    save_data(data)

    # Embed de confirmation
    embed = discord.Embed(
        title="⚙️ Boost modifié",
        description=f"Le boost de {membre.mention} a été défini à **x{niveau}**.",
        color=discord.Color.orange()
    )
    embed.set_thumbnail(url=membre.display_avatar.url)

    await interaction.response.send_message(embed=embed)


# /setforgeron

@bot.tree.command(name="setforgeron", description="Définir le niveau de forgeron d'un membre (admin)")
async def setforgeron(interaction: discord.Interaction, membre: discord.Member, niveau: int):

    # Vérification permissions admin
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            "❌ Tu n'as pas la permission d'utiliser cette commande.",
            ephemeral=True
        )

    # Vérification limites
    if niveau < 0 or niveau > 6:
        return await interaction.response.send_message(
            "❌ Le niveau de forgeron doit être compris entre **0 et 6**.",
            ephemeral=True
        )

    # Charger données
    data = load_data()
    user_data = get_user_data(data, membre.id)

    # Appliquer le niveau
    user_data["job_level"] = niveau
    save_data(data)

    # Embed de confirmation
    embed = discord.Embed(
        title="⚒️ Métier modifié",
        description=f"Le métier de **Forgeron** de {membre.mention} a été défini au **niveau {niveau}**.",
        color=discord.Color.orange()
    )
    embed.set_thumbnail(url=membre.display_avatar.url)

    await interaction.response.send_message(embed=embed)


# /additem

@bot.tree.command(name="additem", description="Ajouter un objet de la boutique à l'inventaire d'un membre (admin)")
@discord.app_commands.autocomplete(objet=autocomplete_items)
async def additem(interaction: discord.Interaction, membre: discord.Member, objet: str):

    # Vérification permissions admin
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            "❌ Tu n'as pas la permission d'utiliser cette commande.",
            ephemeral=True
        )

    # Vérifier que l'objet existe
    if objet not in SHOP_ITEMS:
        return await interaction.response.send_message(
            "❌ Cet objet n'existe pas dans la boutique.",
            ephemeral=True
        )

    # Charger données
    data = load_data()
    user_data = get_user_data(data, membre.id)

    # Ajouter l'objet
    user_data["inventory"].append(objet)
    save_data(data)

    # Embed de confirmation
    embed = discord.Embed(
        title="📦 Objet ajouté",
        description=f"L'objet **{objet}** a été ajouté à l'inventaire de {membre.mention}.",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=membre.display_avatar.url)

    await interaction.response.send_message(embed=embed)

# /removeitem

@bot.tree.command(name="removeitem", description="Retirer un objet de l'inventaire d'un membre (admin)")
@discord.app_commands.autocomplete(objet=autocomplete_inventory)
async def removeitem(interaction: discord.Interaction, membre: discord.Member, objet: str):

    # Vérification permissions admin
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            "❌ Tu n'as pas la permission d'utiliser cette commande.",
            ephemeral=True
        )

    # Charger données
    data = load_data()
    user_data = get_user_data(data, membre.id)

    # Vérifier que l'objet est dans l'inventaire
    if objet not in user_data["inventory"]:
        return await interaction.response.send_message(
            f"❌ {membre.mention} ne possède pas cet objet.",
            ephemeral=True
        )

    # Retirer l'objet
    user_data["inventory"].remove(objet)
    save_data(data)

    # Embed de confirmation
    embed = discord.Embed(
        title="🗑️ Objet retiré",
        description=f"L'objet **{objet}** a été retiré de l'inventaire de {membre.mention}.",
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=membre.display_avatar.url)

    await interaction.response.send_message(embed=embed)


# /dracodex

@bot.tree.command(name="dracodex", description="Affiche les informations d'un dragon")
@discord.app_commands.autocomplete(dragon=autocomplete_dragons)
async def dracodex(interaction: discord.Interaction, dragon: str):

    if dragon not in DRAGONS:
        return await interaction.response.send_message(
            "❌ Ce dragon n'existe pas dans le Dracodex.",
            ephemeral=True
        )

    description = DRAGONS[dragon]

    embed = discord.Embed(
        title="Dracodex",
        description=description,
        color=discord.Color.orange()
    )

    await interaction.response.send_message(embed=embed)


# /ferme

@bot.tree.command(name="ferme", description="Voir ou acheter la ferme")
async def ferme(interaction: discord.Interaction):
    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    if user_data["farm"]:
        description = (
            "🐐 **Tu possèdes déjà la ferme !**\n"
            "Chaque jour, tu reçois **1 chèvre** dans ton `/daily`."
        )
        view = None
    else:
        description = (
            "🐐 **La ferme**\n"
            "Elle produit **1 chèvre par jour** dans ton `/daily`.\n\n"
            "Prix : **50 000💰**"
        )
        view = FarmButton(interaction.user.id)

    embed = discord.Embed(
        title="🐐 Ferme",
        description=description,
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    # 🔥 Correction : n'envoyer view QUE si elle existe
    if view is None:
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(embed=embed, view=view)


# /pêche

@bot.tree.command(name="pêche", description="Aller pêcher un poisson")
async def pêche(interaction: discord.Interaction):

    await interaction.response.defer(ephemeral=True)

    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    rod_level = user_data["fishing_rod"]
    rod_info = FISHING_RODS[rod_level]

    cooldown = rod_info["cooldown"]
    now = int(datetime.now().timestamp())

    # Vérifier cooldown
    if now - user_data["last_fish"] < cooldown:
        remaining = cooldown - (now - user_data["last_fish"])
        minutes = remaining // 60
        seconds = remaining % 60
        return await interaction.followup.send(
            f"⏳ Tu dois encore attendre **{minutes}m {seconds}s** avant de repêcher.",
            ephemeral=True
        )

    # Tirage du poisson
    fish = get_random_fish()
    user_data["fish_inventory"].append(fish)
    user_data["last_fish"] = now
    save_data(data)
    if fish in ["🦀 Crabe", "🐡 Poisson d'or"]:
        await complete_daily_quest(interaction.user.id, 13)
    if fish == "🐡 Poisson d'or":
        await complete_daily_quest(interaction.user.id, 14)

    await interaction.followup.send(
        f"🎣 Tu as pêché : **{fish}** !",
        ephemeral=True
    )

# /poissons

@bot.tree.command(name="poissons", description="Voir ton inventaire de poissons")
async def poissons(interaction: discord.Interaction):

    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    from collections import Counter
    fish_count = Counter(user_data["fish_inventory"])

    if not fish_count:
        desc = "🐟 Aucun poisson pour le moment."
    else:
        desc = "\n".join([f"{fish} × **{amount}**" for fish, amount in fish_count.items()])

    embed = discord.Embed(
        title="🐠 Inventaire de poissons",
        description=desc,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)

# /canne

@bot.tree.command(name="canne", description="Voir et améliorer ta canne à pêche")
async def canne(interaction: discord.Interaction):
    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    rod = user_data["fishing_rod"]

    if rod < 3:
        next_price = FISHING_RODS[rod + 1]["price"]
        price_text = f"💸 Prix du prochain niveau : **{next_price}💰**"
        view = FishingUpgradeButton(interaction.user.id)
    else:
        price_text = "🎣 Tu as déjà la canne maximale !"
        view = None

    embed = discord.Embed(
        title="🎣 Canne à pêche",
        description=(
            f"🔼 Niveau actuel : **{rod}**\n"
            f"{price_text}"
        ),
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    if view is None:
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(embed=embed, view=view)



# /vendre

@bot.tree.command(name="vendre", description="Vendre tous tes poissons")
async def vendre(interaction: discord.Interaction):

    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    fish_inv = user_data["fish_inventory"]

    if not fish_inv:
        return await interaction.response.send_message(
            "🐟 Tu n'as aucun poisson à vendre.",
            ephemeral=True
        )

    from collections import Counter
    fish_count = Counter(fish_inv)

    total_gain = 0
    details = ""

    for fish, amount in fish_count.items():
        if fish in FISH_PRICES:
            gain = FISH_PRICES[fish] * amount
            total_gain += gain
            details += f"{fish} × **{amount}** → **{gain}💰**\n"

    # Ajouter l'argent
    user_data["money"] += total_gain

    # Vider l'inventaire de poissons
    user_data["fish_inventory"] = []

    save_data(data)

    embed = discord.Embed(
        title="💰 Vente de poissons",
        description=(
            f"{details}\n"
            f"➡️ **Total gagné : {total_gain}💰**"
        ),
        color=discord.Color.gold()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)


# /tanière

@bot.tree.command(name="tanière", description="Voir ta tanière ou celle d'un autre membre")
@discord.app_commands.describe(membre="Le membre dont tu veux voir la tanière")
async def taniere(interaction: discord.Interaction, membre: discord.Member = None):

    cible = membre or interaction.user

    data = load_data()
    user_data = get_user_data(data, cible.id)

    dragons = user_data.get("dragons", {})

    if not dragons:
        msg = (
            f"🐣 **{cible.display_name}** ne possède aucun dragon."
            if membre else
            "🐣 Tu ne possèdes encore aucun dragon."
        )
        return await interaction.response.send_message(msg, ephemeral=True)

    # Construction des lignes
    lignes = []
    from collections import Counter

    for nom, stades in dragons.items():
        if nom not in DRAGONCOLLEC:
            continue

        emoji = DRAGONCOLLEC[nom]["emoji"]
        count = Counter(stades)

        for stade, qty in count.items():
            if qty == 1:
                lignes.append(f"{emoji} **{nom}** — [Stade {stade}]")
            else:
                lignes.append(f"{emoji} **{nom}** — [Stade {stade}] × **{qty}**")

    lignes.sort()

    # Pagination : 10 lignes par page
    pages = []
    chunk_size = 10

    for i in range(0, len(lignes), chunk_size):
        chunk = lignes[i:i + chunk_size]
        embed = discord.Embed(
            title=f"<:grotte:1517797646587265044> Tanière de {cible.display_name}",
            description="\n".join(chunk),
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=cible.display_avatar.url)
        embed.set_footer(text=f"Page {len(pages)+1}/{(len(lignes)-1)//chunk_size + 1}")
        pages.append(embed)

    view = TaniereView(pages, interaction.user)

    await interaction.response.send_message(embed=pages[0], view=view)




# /éclore

@bot.tree.command(name="éclore", description="Fait éclore un œuf de dragon")
@discord.app_commands.describe(rarete="commun / rare / epique")
@discord.app_commands.autocomplete(rarete=autocomplete_rarete)
async def eclore(interaction: discord.Interaction, rarete: str):

    rarete = rarete.lower()

    if rarete not in EGG_PROBAS:
        return await interaction.response.send_message(
            "❌ Rareté invalide. Choisis : commun, rare ou epique.",
            ephemeral=True
        )

    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    oeuf_item = EGG_ITEMS[rarete]

    if oeuf_item not in user_data["inventory"]:
        return await interaction.response.send_message(
            f"❌ Tu ne possèdes pas **{oeuf_item}**.",
            ephemeral=True
        )

    rarete_tirée = tirer_rareté(rarete)
    dragon = tirer_dragon_selon_rareté(rarete_tirée)

    if not dragon:
        return await interaction.response.send_message(
            "❌ Aucun dragon disponible pour cette rareté.",
            ephemeral=True
        )

    user_data["dragons"].setdefault(dragon, []).append(1)
    user_data["inventory"].remove(oeuf_item)
    save_data(data)
    if rarete == "commun":
        await complete_daily_quest(interaction.user.id, 3)
    elif rarete == "rare":
        await complete_daily_quest(interaction.user.id, 4)
    elif rarete == "epique":
        await complete_daily_quest(interaction.user.id, 5)


    emoji = DRAGONCOLLEC[dragon]["emoji"]

    embed = discord.Embed(
        title="🐣 Éclosion réussie !",
        description=(
            f"Ton œuf **{rarete}** a donné :\n\n"
            f"{emoji} **{dragon}**\n"
            f"Rareté : **{rarete_tirée}**\n"
            f"Stade : **1**"
        ),
        color=discord.Color.gold()
    )

    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="token", description="Affiche ton nombre de tokens ou celui d'un autre membre")
@discord.app_commands.describe(membre="Le membre dont tu veux voir les tokens")
async def token(interaction: discord.Interaction, membre: discord.Member = None):

    cible = membre or interaction.user

    data = load_data()
    user_data = get_user_data(data, cible.id)

    tokens = user_data.get("tokens", 0)

    # Message différent si on regarde quelqu'un d'autre
    if membre:
        titre = f"🪙 Tokens de {cible.display_name}"
        desc = f"{cible.mention} possède **{tokens} token(s)**."
    else:
        titre = "🪙 Tes tokens"
        desc = f"Tu possèdes **{tokens} token(s)**."

    embed = discord.Embed(
        title=titre,
        description=desc,
        color=discord.Color.gold()
    )

    embed.set_thumbnail(url=cible.display_avatar.url)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="token_echanger", description="Échange 20 tokens contre 50 000 pièces d'or")
async def token_echanger(interaction: discord.Interaction):

    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    # Vérification des tokens
    if user_data["tokens"] < 20:
        await interaction.response.send_message(
            "❌ Tu n'as pas assez de tokens. Il t'en faut **20** pour faire un échange.",
            ephemeral=True
        )
        return

    # Retirer 20 tokens
    user_data["tokens"] -= 20

    # Ajouter 20 000 argent
    user_data["money"] += 50000

    save_data(data)

    embed = discord.Embed(
        title="🪙 Échange réussi !",
        description=(
            "Tu as échangé **20 tokens** contre **50 000 pièces** !\n\n"
            "Merci pour ta fidélité dans le Donjon."
        ),
        color=discord.Color.gold()
    )

    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    await complete_daily_quest(interaction.user.id, 15)

    await interaction.response.send_message(embed=embed)

##############################################################

def parse_dragon_entry(entry: str):
    if "|" not in entry:
        return None, None

    parts = entry.split("|")
    if len(parts) != 2:
        return None, None

    nom = parts[0].strip()
    try:
        stade = int(parts[1].strip())
    except:
        return None, None

    return nom, stade


async def autocomplete_ton_dragon(interaction: discord.Interaction, current: str):
    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    results = []

    for nom, stades in user_data["dragons"].items():
        for stade in stades:
            entry = f"{nom} | {stade}"
            if current.lower() in entry.lower():
                results.append(discord.app_commands.Choice(name=entry, value=entry))

    return results[:25]


class ChoixDragonCibleSelect(discord.ui.Select):
    def __init__(self, user, cible, ton_nom, ton_stade, dragons_page):
        self.user = user
        self.cible = cible
        self.ton_nom = ton_nom
        self.ton_stade = ton_stade

        options = []
        for entry, uid in dragons_page:
            options.append(discord.SelectOption(label=entry, value=f"{entry}|UID_{uid}"))

        super().__init__(
            placeholder="Choisis le dragon de la cible",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ Ce menu n'est pas pour toi.", ephemeral=True)

        raw_value = self.values[0]
        clean_value = raw_value.rsplit("|UID_", 1)[0]

        son_nom, son_stade = parse_dragon_entry(clean_value)

        view = ConfirmationView(self.user, self.cible, self.ton_nom, self.ton_stade, son_nom, son_stade)

        embed = discord.Embed(
            title="🔄 Confirmation d'échange",
            description=(
                f"{self.user.mention} propose :\n"
                f"➡️ {self.ton_nom} [Stade {self.ton_stade}]\n\n"
                f"En échange de :\n"
                f"⬅️ {self.cible.mention} : {son_nom} [Stade {son_stade}]\n\n"
                f"En attente de confirmation de {self.cible.mention}…"
            ),
            color=discord.Color.orange()
        )

        await interaction.response.edit_message(embed=embed, view=view)





class ChoixDragonCibleView(discord.ui.View):
    def __init__(self, user, cible, ton_nom, ton_stade):
        super().__init__(timeout=1200)
        self.user = user
        self.cible = cible
        self.ton_nom = ton_nom
        self.ton_stade = ton_stade

        data = load_data()
        cible_data = get_user_data(data, cible.id)

        # Liste complète des dragons
        self.dragons = []
        uid = 0
        for nom, stades in cible_data["dragons"].items():
            for stade in stades:
                entry = f"{nom} | {stade}"
                self.dragons.append((entry, uid))
                uid += 1

        self.page = 0
        self.per_page = 25

        self.update_page()

    def update_page(self):
        start = self.page * self.per_page
        end = start + self.per_page
        dragons_page = self.dragons[start:end]

        self.clear_items()

        self.add_item(ChoixDragonCibleSelect(
            self.user, self.cible, self.ton_nom, self.ton_stade, dragons_page
        ))

        # Bouton précédent
        if self.page > 0:
            self.add_item(self.PreviousButton())

        # Bouton suivant
        if end < len(self.dragons):
            self.add_item(self.NextButton())

    class NextButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label="➡️ Page suivante", style=discord.ButtonStyle.blurple)

        async def callback(self, interaction: discord.Interaction):
            view: ChoixDragonCibleView = self.view
            view.page += 1
            view.update_page()
            await interaction.response.edit_message(view=view)

    class PreviousButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label="⬅️ Page précédente", style=discord.ButtonStyle.blurple)

        async def callback(self, interaction: discord.Interaction):
            view: ChoixDragonCibleView = self.view
            view.page -= 1
            view.update_page()
            await interaction.response.edit_message(view=view)



class ConfirmationView(discord.ui.View):
    def __init__(self, user, cible, ton_nom, ton_stade, son_nom, son_stade):
        super().__init__(timeout=1200)
        self.user = user
        self.cible = cible
        self.ton_nom = ton_nom
        self.ton_stade = ton_stade
        self.son_nom = son_nom
        self.son_stade = son_stade

    @discord.ui.button(label="Accepter", style=discord.ButtonStyle.green)
    async def accepter(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.cible.id:
            return await interaction.response.send_message("❌ Ce bouton n'est pas pour toi.", ephemeral=True)

        data = load_data()
        user_data = get_user_data(data, self.user.id)
        cible_data = get_user_data(data, self.cible.id)

        # Vérifications
        if self.ton_nom not in user_data["dragons"] or self.ton_stade not in user_data["dragons"][self.ton_nom]:
            return await interaction.response.send_message("❌ Le dragon du joueur n'existe plus.", ephemeral=True)

        if self.son_nom not in cible_data["dragons"] or self.son_stade not in cible_data["dragons"][self.son_nom]:
            return await interaction.response.send_message("❌ Ton dragon n'existe plus.", ephemeral=True)

        # ÉCHANGE
        user_data["dragons"][self.ton_nom].remove(self.ton_stade)
        if not user_data["dragons"][self.ton_nom]:
            del user_data["dragons"][self.ton_nom]

        cible_data["dragons"][self.son_nom].remove(self.son_stade)
        if not cible_data["dragons"][self.son_nom]:
            del cible_data["dragons"][self.son_nom]

        user_data["dragons"].setdefault(self.son_nom, []).append(self.son_stade)
        cible_data["dragons"].setdefault(self.ton_nom, []).append(self.ton_stade)

        save_data(data)

        embed = discord.Embed(
            title="✅ Échange réussi !",
            description=(
                f"{self.user.mention} reçoit : **{self.son_nom} [Stade {self.son_stade}]**\n"
                f"{self.cible.mention} reçoit : **{self.ton_nom} [Stade {self.ton_stade}]**"
            ),
            color=discord.Color.green()
        )

        await interaction.response.edit_message(embed=embed, view=None)



    @discord.ui.button(label="Refuser", style=discord.ButtonStyle.red)
    async def refuser(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.cible.id:
            return await interaction.response.send_message("❌ Ce bouton n'est pas pour toi.", ephemeral=True)

        embed = discord.Embed(
            title="❌ Échange refusé",
            description=f"{self.cible.mention} a refusé l'échange.",
            color=discord.Color.red()
        )

        await interaction.response.edit_message(embed=embed, view=None)




@bot.tree.command(name="dragon_echanger", description="Propose un échange de dragon à un joueur")
@discord.app_commands.describe(
    cible="Le joueur avec qui tu veux échanger",
    ton_dragon="Le dragon que TU donnes (ex: Dragon de feu | 1)"
)
@discord.app_commands.autocomplete(
    ton_dragon=autocomplete_ton_dragon
)
async def dragon_echanger(interaction: discord.Interaction, cible: discord.Member, ton_dragon: str):

    if cible.id == interaction.user.id:
        await interaction.response.send_message("❌ Tu ne peux pas échanger avec toi-même.", ephemeral=True)
        return

    ton_nom, ton_stade = parse_dragon_entry(ton_dragon)
    if not ton_nom:
        await interaction.response.send_message("❌ Format invalide. Utilise : `Nom | Stade`", ephemeral=True)
        return

    data = load_data()
    user_data = get_user_data(data, interaction.user.id)
    cible_data = get_user_data(data, cible.id)

    if ton_nom not in user_data["dragons"] or ton_stade not in user_data["dragons"][ton_nom]:
        await interaction.response.send_message("❌ Tu ne possèdes pas ce dragon.", ephemeral=True)
        return

    if not cible_data["dragons"]:
        await interaction.response.send_message(f"❌ {cible.display_name} n'a aucun dragon.", ephemeral=True)
        return

    view = ChoixDragonCibleView(interaction.user, cible, ton_nom, ton_stade)
    await interaction.response.send_message(
    f"Choisis maintenant **le dragon de {cible.display_name}** que tu veux recevoir :",
    view=view
)


async def autocomplete_ton_dragon(interaction: discord.Interaction, current: str):
    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    results = []

    for nom, stades in user_data["dragons"].items():
        for stade in stades:
            entry = f"{nom} | {stade}"
            if current.lower() in entry.lower():
                results.append(discord.app_commands.Choice(name=entry, value=entry))

    return results[:25]


class ConfirmationVenteView(discord.ui.View):
    def __init__(self, vendeur, cible, nom, stade, prix):
        super().__init__(timeout=60)
        self.vendeur = vendeur
        self.cible = cible
        self.nom = nom
        self.stade = stade
        self.prix = prix

    @discord.ui.button(label="Accepter", style=discord.ButtonStyle.green)
    async def accepter(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.cible.id:
            return await interaction.response.send_message("❌ Ce bouton n'est pas pour toi.", ephemeral=True)

        data = load_data()
        vendeur_data = get_user_data(data, self.vendeur.id)
        cible_data = get_user_data(data, self.cible.id)

        # Vérifier que le vendeur possède encore le dragon
        if self.nom not in vendeur_data["dragons"] or self.stade not in vendeur_data["dragons"][self.nom]:
            return await interaction.response.send_message("❌ Le vendeur n'a plus ce dragon.", ephemeral=True)

        # Vérifier que la cible a assez d'argent
        if cible_data["money"] < self.prix:
            return await interaction.response.send_message("❌ Tu n'as pas assez d'argent.", ephemeral=True)

        # TRANSFERT DU DRAGON
        vendeur_data["dragons"][self.nom].remove(self.stade)
        if not vendeur_data["dragons"][self.nom]:
            del vendeur_data["dragons"][self.nom]

        cible_data["dragons"].setdefault(self.nom, []).append(self.stade)

        # TRANSFERT D'ARGENT
        cible_data["money"] -= self.prix
        vendeur_data["money"] += self.prix

        save_data(data)

        embed = discord.Embed(
            title="💰 Vente réussie !",
            description=(
                f"{self.vendeur.mention} a vendu **{self.nom} [Stade {self.stade}]**\n"
                f"à {self.cible.mention} pour **{self.prix} pièces**."
            ),
            color=discord.Color.green()
        )

        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="Refuser", style=discord.ButtonStyle.red)
    async def refuser(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.cible.id:
            return await interaction.response.send_message("❌ Ce bouton n'est pas pour toi.", ephemeral=True)

        embed = discord.Embed(
            title="❌ Vente refusée",
            description=f"{self.cible.mention} a refusé la vente.",
            color=discord.Color.red()
        )

        await interaction.response.edit_message(embed=embed, view=None)


@bot.tree.command(name="dragon_vendre", description="Vends un dragon à un joueur")
@discord.app_commands.describe(
    cible="Le joueur à qui tu veux vendre ton dragon",
    ton_dragon="Le dragon que TU vends (ex: Dragon de feu | 1)",
    montant="Le prix de vente (0 = gratuit)"
)
@discord.app_commands.autocomplete(
    ton_dragon=autocomplete_ton_dragon
)
async def dragon_vendre(interaction: discord.Interaction, cible: discord.Member, ton_dragon: str, montant: int):

    if montant < 0:
        await interaction.response.send_message("❌ Le montant ne peut pas être négatif.", ephemeral=True)
        return

    if cible.id == interaction.user.id:
        await interaction.response.send_message("❌ Tu ne peux pas te vendre un dragon à toi-même.", ephemeral=True)
        return

    nom, stade = parse_dragon_entry(ton_dragon)
    if not nom:
        await interaction.response.send_message("❌ Format invalide. Utilise : `Nom | Stade`", ephemeral=True)
        return

    data = load_data()
    vendeur_data = get_user_data(data, interaction.user.id)

    # Vérifier que le vendeur possède le dragon
    if nom not in vendeur_data["dragons"] or stade not in vendeur_data["dragons"][nom]:
        await interaction.response.send_message("❌ Tu ne possèdes pas ce dragon.", ephemeral=True)
        return

    # Embed de demande
    embed = discord.Embed(
        title="💰 Proposition de vente",
        description=(
            f"{interaction.user.mention} veut te vendre :\n"
            f"➡️ **{nom} [Stade {stade}]**\n"
            f"💵 Prix : **{montant} pièces**\n\n"
            f"{cible.mention}, acceptes-tu ?"
        ),
        color=discord.Color.orange()
    )

    view = ConfirmationVenteView(interaction.user, cible, nom, stade, montant)

    await interaction.response.send_message(content=f"{cible.mention}", embed=embed, view=view)

async def autocomplete_ton_dragon(interaction: discord.Interaction, current: str):
    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    results = []

    for nom, stades in user_data["dragons"].items():
        for stade in stades:
            entry = f"{nom} | {stade}"
            if current.lower() in entry.lower():
                results.append(discord.app_commands.Choice(name=entry, value=entry))

    return results[:25]

def has_goat(user_data):
    inv = user_data.get("inventory", [])

    for entry in inv:

        # Cas 1 : string
        if isinstance(entry, str):
            if entry == "🐐 Chèvre":
                return True

        # Cas 2 : liste ou tuple
        elif isinstance(entry, (list, tuple)):
            if len(entry) >= 2:
                item, qty = entry[0], entry[1]
                if item == "🐐 Chèvre" and qty > 0:
                    return True
            elif len(entry) == 1:
                if entry[0] == "🐐 Chèvre":
                    return True

    return False


def remove_goat(user_data):
    inv = user_data.get("inventory", [])

    for i, entry in enumerate(inv):

        # Cas 1 : string → supprimer direct
        if isinstance(entry, str):
            if entry == "🐐 Chèvre":
                inv.pop(i)
                return

        # Cas 2 : liste ou tuple
        elif isinstance(entry, (list, tuple)):
            if len(entry) >= 2:
                item, qty = entry[0], entry[1]
                if item == "🐐 Chèvre":
                    if qty > 1:
                        inv[i][1] -= 1
                    else:
                        inv.pop(i)
                    return

            elif len(entry) == 1:
                if entry[0] == "🐐 Chèvre":
                    inv.pop(i)
                    return




STADE_MAX = 6

@bot.tree.command(name="nourrir", description="Nourrit un de tes dragons avec une chèvre")
@discord.app_commands.describe(
    dragon="Le dragon que tu veux nourrir (ex: Dragon de feu | 1)"
)
@discord.app_commands.autocomplete(
    dragon=autocomplete_ton_dragon
)
async def nourrir(interaction: discord.Interaction, dragon: str):

    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    # Vérifier chèvre
    if not has_goat(user_data):
        return await interaction.response.send_message(
            "❌ Tu n'as **aucune 🐐 Chèvre** dans ton inventaire.",
            ephemeral=True
        )

    # Parser
    nom, stade = parse_dragon_entry(dragon)
    if not nom:
        return await interaction.response.send_message(
            "❌ Format invalide. Utilise : `Nom | Stade`",
            ephemeral=True
        )

    # Vérifier possession
    if nom not in user_data["dragons"] or stade not in user_data["dragons"][nom]:
        return await interaction.response.send_message(
            f"❌ Tu ne possèdes pas **{nom}** au stade **{stade}**.",
            ephemeral=True
        )

    # Vérifier stade maximal
    if stade >= STADE_MAX:
        return await interaction.response.send_message(
            f"⚠️ **{nom}** est déjà au **stade maximal ({STADE_MAX})**.\n"
            "Tu ne peux plus le nourrir.",
            ephemeral=True
        )

    # --- NOURRIR LE DRAGON ---
    user_data["dragons"][nom].remove(stade)
    if not user_data["dragons"][nom]:
        del user_data["dragons"][nom]

    nouveau_stade = stade + 1
    user_data["dragons"].setdefault(nom, []).append(nouveau_stade)

    # Consommer une chèvre
    remove_goat(user_data)

    # Sauvegarder AVANT la quête
    save_data(data)

    # Valider la quête "augmenter un dragon d'un stade"
    await complete_daily_quest(interaction.user.id, 1)

    # Valider la quête "atteindre stade maximal"
    if nouveau_stade == STADE_MAX:
        await complete_daily_quest(interaction.user.id, 2)

    emoji = DRAGONCOLLEC[nom]["emoji"]

    embed = discord.Embed(
        title="🍖 Nourrissage réussi !",
        description=(
            f"{emoji} **{nom}** a été nourri avec une 🐐 Chèvre !\n\n"
            f"📈 Il passe de **Stade {stade}** → **Stade {nouveau_stade}**"
        ),
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed)


##################################################

def has_item(user_data, item_name, qty_needed=1):
    inv = user_data.get("inventory", [])

    for entry in inv:
        if isinstance(entry, str):
            if entry == item_name and qty_needed == 1:
                return True

        elif isinstance(entry, (list, tuple)):
            if len(entry) >= 2:
                if entry[0] == item_name and entry[1] >= qty_needed:
                    return True
            elif len(entry) == 1:
                if entry[0] == item_name and qty_needed == 1:
                    return True

    return False


def remove_item(user_data, item_name, qty=1):
    inv = user_data.get("inventory", [])

    for i, entry in enumerate(inv):

        if isinstance(entry, str):
            if entry == item_name and qty == 1:
                inv.pop(i)
                return

        elif isinstance(entry, (list, tuple)):
            if len(entry) >= 2 and entry[0] == item_name:
                if entry[1] > qty:
                    inv[i][1] -= qty
                else:
                    inv.pop(i)
                return

            elif len(entry) == 1 and entry[0] == item_name and qty == 1:
                inv.pop(i)
                return


def has_required_parents(user_data, dragon_name):
    parents = DRAGONCOLLEC[dragon_name]["parents"]

    missing = []
    low_stage = []

    for parent in parents:
        if parent not in user_data["dragons"]:
            missing.append(parent)
        else:
            if max(user_data["dragons"][parent]) < 3:
                low_stage.append(parent)

    if missing:
        return False, f"Tu n'as pas ces dragons : {', '.join(missing)}"

    if low_stage:
        return False, f"Ces dragons ne sont pas au stade 3 minimum : {', '.join(low_stage)}"

    return True, None


def reset_parents_to_stage_1(user_data, dragon_name):
    parents = DRAGONCOLLEC[dragon_name]["parents"]

    for parent in parents:
        if parent in user_data["dragons"]:
            stades = user_data["dragons"][parent]
            stades.remove(max(stades))
            stades.append(1)



async def autocomplete_hybride(interaction: discord.Interaction, current: str):
    results = []

    for nom, data in DRAGONCOLLEC.items():
        if data["obtention"] == "Hybride" and nom != "Dragon raté":
            if current.lower() in nom.lower():
                results.append(discord.app_commands.Choice(name=nom, value=nom))

    return results[:25]



@bot.tree.command(name="hybride", description="Crée un dragon hybride")
@discord.app_commands.describe(
    dragon="Le dragon hybride que tu veux créer"
)
@discord.app_commands.autocomplete(
    dragon=autocomplete_hybride
)
async def hybride(interaction: discord.Interaction, dragon: str):

    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    # Vérifier que le dragon existe
    if dragon not in DRAGONCOLLEC:
        await interaction.response.send_message("❌ Dragon inconnu.", ephemeral=True)
        return

    # Vérifier que c'est un hybride
    if DRAGONCOLLEC[dragon]["obtention"] != "Hybride":
        await interaction.response.send_message("❌ Ce dragon n'est pas un hybride.", ephemeral=True)
        return

    # Vérifier les parents
    ok, msg = has_required_parents(user_data, dragon)
    if not ok:
        await interaction.response.send_message(f"❌ {msg}", ephemeral=True)
        return

    # Cas spécial : Dragon de l'univers (ne rate jamais)
    if dragon == "Dragon de l'univers":

        item_name = "<:noyau_de_puissance:1516065680166879342> Noyau de puissance"

        if not has_item(user_data, item_name, 10):
            await interaction.response.send_message(
                "❌ Tu dois avoir **10 <:noyau_de_puissance:1516065680166879342> Noyaux de puissance**.",
                ephemeral=True
            )
            return

        remove_item(user_data, item_name, 10)

        user_data["dragons"].setdefault(dragon, []).append(1)
        save_data(data)

        emoji = DRAGONCOLLEC[dragon]["emoji"]

        embed = discord.Embed(
            title="🌌 Création divine !",
            description=(
                f"Tu as créé {emoji} **{dragon}** !\n"
                f"Les 10 noyaux ont été consommés.\n"
                f"Tes parents restent intacts."
            ),
            color=discord.Color.purple()
        )

        await interaction.response.send_message(embed=embed)
        return

    # Hybrides normaux → Soupe obligatoire
    soupe = "<:soupe_aux_epices:1515710241667285073> Soupe aux épices"

    if not has_item(user_data, soupe, 1):
        await interaction.response.send_message(
            "❌ Tu n'as pas de <:soupe_aux_epices:1515710241667285073> **Soupe aux épices**.",
            ephemeral=True
        )
        return

    # Consommer la soupe (réussite ou échec)
    remove_item(user_data, soupe, 1)

    # Tirage 1 chance sur 5
    if random.randint(1, 5) == 1:
        # ÉCHEC → Dragon raté
        user_data["dragons"].setdefault("Dragon raté", []).append(1)
        save_data(data)
        await complete_daily_quest(interaction.user.id, 8)

        embed = discord.Embed(
            title="💥 Hybridation ratée !",
            description=(
                "L'expérience a échoué...\n"
                "Tu obtiens un <:rate:1516465121398882304> **Dragon raté**.\n"
                "Tes parents ne sont pas affectés."
            ),
            color=discord.Color.red()
        )

        await interaction.response.send_message(embed=embed)
        return

    # RÉUSSITE → Dragon hybride normal
    reset_parents_to_stage_1(user_data, dragon)
    user_data["dragons"].setdefault(dragon, []).append(1)

    save_data(data)
    await complete_daily_quest(interaction.user.id, 6)


    emoji = DRAGONCOLLEC[dragon]["emoji"]

    embed = discord.Embed(
        title="🧪 Hybridation réussie !",
        description=(
            f"Tu as créé {emoji} **{dragon}** !\n"
            f"Il apparaît au **stade 1**.\n"
            f"Tes parents ont été remis au **stade 1**."
        ),
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed)


from discord import app_commands
from discord.ui import View, Button
import discord

# ID du rôle @evenements
EVENEMENT_ROLE_ID = 1497882093500371109


@bot.tree.command(name="drop", description="Lance un drop (admin uniquement)")
@app_commands.checks.has_permissions(administrator=True)
async def drop(interaction: discord.Interaction):

    role = interaction.guild.get_role(EVENEMENT_ROLE_ID)
    if role is None:
        return await interaction.response.send_message(
            "❌ Le rôle @evenements est introuvable. Vérifie l'ID.",
            ephemeral=True
        )

    # Embed du drop
    embed = discord.Embed(
        title="🎁 DROP !",
        description="Le premier qui clique sur le bouton gagne **1 token** !",
        color=discord.Color.gold()
    )

    # View sécurisée
    class DropView(View):
        def __init__(self):
            super().__init__(timeout=None)
            self.claimed = False  # verrou anti-double clic

        @discord.ui.button(label="Réclamer 🎉", style=discord.ButtonStyle.green)
        async def claim(self, interaction2: discord.Interaction, button: discord.ui.Button):

            # Vérrouillage : si déjà pris → impossible
            if self.claimed:
                return await interaction2.response.send_message(
                    "❌ Le drop a déjà été récupéré.",
                    ephemeral=True
                )

            self.claimed = True  # verrou activé

            # On retire le bouton immédiatement
            self.clear_items()

            # Donner le token
            data = load_data()
            user_data = get_user_data(data, interaction2.user.id)
            user_data["tokens"] = user_data.get("tokens", 0) + 1
            save_data(data)
            await complete_daily_quest(interaction2.user.id, 17)


            # Embed final
            embed_final = discord.Embed(
                title="🎉 Drop récupéré !",
                description=f"{interaction2.user.mention} a gagné **1 token** !",
                color=discord.Color.green()
            )

            await interaction2.response.edit_message(embed=embed_final, view=None)

    # Message public avec ping du rôle
    await interaction.response.send_message(
        content=f"{role.mention} **DROP DISPONIBLE !**",
        embed=embed,
        view=DropView()
    )


def get_hdv(data):
    if "hdv" not in data:
        data["hdv"] = []
    return data["hdv"]


class PaginationView(discord.ui.View):
    def __init__(self, pages, user):
        super().__init__(timeout=60)
        self.pages = pages
        self.user = user
        self.index = 0

    async def update(self, interaction):
        await interaction.response.edit_message(embed=self.pages[self.index], view=self)

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.gray)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ Ce menu n'est pas pour toi.", ephemeral=True)

        if self.index > 0:
            self.index -= 1
            await self.update(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.gray)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ Ce menu n'est pas pour toi.", ephemeral=True)

        if self.index < len(self.pages) - 1:
            self.index += 1
            await self.update(interaction)
        else:
            await interaction.response.defer()


@bot.tree.command(name="hdv", description="Affiche les offres de l'Hôtel des Ventes")
async def hdv(interaction: discord.Interaction):

    data = load_data()
    hdv_list = get_hdv(data)

    if not hdv_list:
        return await interaction.response.send_message(
            "🏪 L'Hôtel des Ventes est vide.",
            ephemeral=True
        )

    pages = []
    chunk_size = 10

    for i in range(0, len(hdv_list), chunk_size):
        chunk = hdv_list[i:i+chunk_size]

        desc = ""
        for offer in chunk:
            vendeur = interaction.guild.get_member(offer["vendeur"])
            vendeur_name = vendeur.display_name if vendeur else "Inconnu"

            emoji = DRAGONCOLLEC[offer["nom"]]["emoji"]

            desc += (
                f"🆔 **{offer['id']}** — {emoji} **{offer['nom']}** [Stade {offer['stade']}]\n"
                f"💰 Prix : **{offer['prix']}**\n"
                f"👤 Vendeur : {vendeur_name}\n\n"
            )

        embed = discord.Embed(
            title="🏪 Hôtel des Ventes",
            description=desc,
            color=discord.Color.gold()
        )

        pages.append(embed)

    view = PaginationView(pages, interaction.user)
    await interaction.response.send_message(embed=pages[0], view=view)


@bot.tree.command(name="hdv_place", description="Place un dragon en vente à l'Hôtel des Ventes")
@discord.app_commands.describe(
    dragon="Le dragon à vendre (ex: Dragon de feu | 1)",
    prix="Le prix de vente"
)
@discord.app_commands.autocomplete(dragon=autocomplete_ton_dragon)
async def hdv_place(interaction: discord.Interaction, dragon: str, prix: int):

    if prix < 0:
        return await interaction.response.send_message("❌ Le prix ne peut pas être négatif.", ephemeral=True)

    nom, stade = parse_dragon_entry(dragon)
    if not nom:
        return await interaction.response.send_message("❌ Format invalide.", ephemeral=True)

    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    # Vérifier possession
    if nom not in user_data["dragons"] or stade not in user_data["dragons"][nom]:
        return await interaction.response.send_message("❌ Tu ne possèdes pas ce dragon.", ephemeral=True)

    # Retirer le dragon
    user_data["dragons"][nom].remove(stade)
    if not user_data["dragons"][nom]:
        del user_data["dragons"][nom]

    # Ajouter au HDV
    hdv_list = get_hdv(data)
    new_id = (max([o["id"] for o in hdv_list]) + 1) if hdv_list else 1

    hdv_list.append({
        "id": new_id,
        "vendeur": interaction.user.id,
        "nom": nom,
        "stade": stade,
        "prix": prix
    })

    save_data(data)

    await interaction.response.send_message(
        f"🏪 Ton dragon **{nom} [Stade {stade}]** a été mis en vente pour **{prix} pièces** !"
    )


async def autocomplete_hdv_remove(interaction, current):
    data = load_data()
    hdv_list = get_hdv(data)

    results = []
    for offer in hdv_list:
        if offer["vendeur"] == interaction.user.id:
            label = f"{offer['id']} — {offer['nom']} | {offer['stade']}"
            if current.lower() in label.lower():
                results.append(discord.app_commands.Choice(name=label, value=str(offer["id"])))

    return results[:25]


@bot.tree.command(name="hdv_remove", description="Retire une de tes offres du HDV")
@discord.app_commands.autocomplete(offer_id=autocomplete_hdv_remove)
async def hdv_remove(interaction: discord.Interaction, offer_id: str):

    offer_id = int(offer_id)

    data = load_data()
    hdv_list = get_hdv(data)

    offer = next((o for o in hdv_list if o["id"] == offer_id), None)

    if not offer or offer["vendeur"] != interaction.user.id:
        return await interaction.response.send_message("❌ Offre introuvable.", ephemeral=True)

    # Rendre le dragon
    user_data = get_user_data(data, interaction.user.id)
    user_data["dragons"].setdefault(offer["nom"], []).append(offer["stade"])

    # Retirer du HDV
    hdv_list.remove(offer)
    save_data(data)

    await interaction.response.send_message(
        f"🔙 Tu as récupéré **{offer['nom']} [Stade {offer['stade']}]**."
    )


async def autocomplete_hdv_buy(interaction, current):
    data = load_data()
    hdv_list = get_hdv(data)

    results = []
    for offer in hdv_list:
        label = f"{offer['id']} — {offer['nom']} | {offer['stade']} — {offer['prix']} pièces"
        if current.lower() in label.lower():
            results.append(discord.app_commands.Choice(name=label, value=str(offer["id"])))

    return results[:25]


@bot.tree.command(name="hdv_buy", description="Achète une offre du HDV")
@discord.app_commands.autocomplete(offer_id=autocomplete_hdv_buy)
async def hdv_buy(interaction: discord.Interaction, offer_id: str):

    offer_id = int(offer_id)

    data = load_data()
    hdv_list = get_hdv(data)

    offer = next((o for o in hdv_list if o["id"] == offer_id), None)

    if not offer:
        return await interaction.response.send_message("❌ Offre introuvable.", ephemeral=True)

    if offer["vendeur"] == interaction.user.id:
        return await interaction.response.send_message("❌ Tu ne peux pas acheter ta propre offre.", ephemeral=True)

    acheteur = get_user_data(data, interaction.user.id)
    vendeur = get_user_data(data, offer["vendeur"])

    if acheteur["money"] < offer["prix"]:
        return await interaction.response.send_message("❌ Tu n'as pas assez d'argent.", ephemeral=True)

    # Transfert argent
    acheteur["money"] -= offer["prix"]
    vendeur["money"] += offer["prix"]

    # Transfert dragon
    acheteur["dragons"].setdefault(offer["nom"], []).append(offer["stade"])

    # Retirer du HDV
    hdv_list.remove(offer)
    save_data(data)

    await interaction.response.send_message(
        f"🎉 Tu as acheté **{offer['nom']} [Stade {offer['stade']}]** pour **{offer['prix']} pièces** !"
    )


def get_daily_quests(data):
    if "daily_quests" not in data:
        data["daily_quests"] = {
            "date": "1970-01-01",
            "quests": [],
            "completed": {}
        }
    return data["daily_quests"]


DAILY_QUEST_POOL = [
    {"id": 1, "name": "Augmenter un dragon d'un stade", "reward": 1},
    {"id": 2, "name": "Augmenter un dragon à son stade maximal", "reward": 2},
    {"id": 3, "name": "Faire éclore un œuf commun", "reward": 1},
    {"id": 4, "name": "Faire éclore un œuf rare", "reward": 1},
    {"id": 5, "name": "Faire éclore un œuf épique", "reward": 2},
    {"id": 6, "name": "Créer un hybride", "reward": 1},
    {"id": 7, "name": "Acheter un noyau de puissance", "reward": 1},
    {"id": 8, "name": "Obtenir un dragon raté", "reward": 2},
    {"id": 9, "name": "Augmenter son niveau de forgeron", "reward": 2},
    {"id": 10, "name": "Augmenter le niveau de sa canne à pêche", "reward": 2},
    {"id": 11, "name": "Augmenter son niveau de boost", "reward": 2},
    {"id": 12, "name": "Acheter la ferme", "reward": 3},
    {"id": 13, "name": "Pêcher un crabe ou un poisson doré", "reward": 1},
    {"id": 14, "name": "Pêcher un poisson doré", "reward": 2},
    {"id": 15, "name": "Échanger 20 tokens contre de l'argent", "reward": 2},
    {"id": 16, "name": "Remporter un token dans la route infinie", "reward": 1},
    {"id": 17, "name": "Remporter un drop", "reward": 1},
]

@bot.tree.command(name="quêtes_journalières", description="Génère les quêtes journalières (admin uniquement)")
@discord.app_commands.checks.has_permissions(administrator=True)

async def quetes_journalieres(interaction: discord.Interaction):

    data = load_data()
    dq = get_daily_quests(data)

    # Tirage aléatoire de 3 quêtes
    quests = random.sample(DAILY_QUEST_POOL, 3)

    dq["quests"] = quests
    dq["date"] = datetime.now().strftime("%Y-%m-%d")
    dq["completed"] = {}

    save_data(data)

    # Construction de l'embed
    desc = ""
    for q in quests:
        desc += f"• **{q['name']}** — 🎁 {q['reward']} token(s)\n"

    embed = discord.Embed(
        title="📅 Quêtes journalières",
        description=desc,
        color=discord.Color.blue()
    )

    await interaction.response.send_message(embed=embed)




async def complete_daily_quest(user_id, quest_id):
    data = load_data()
    dq = get_daily_quests(data)

    # Déjà complétée ?
    if str(user_id) in dq["completed"] and quest_id in dq["completed"][str(user_id)]:
        return False, "Déjà complétée."

    # Trouver la quête active
    quest = next((q for q in dq["quests"] if q["id"] == quest_id), None)
    if not quest:
        return False, "Cette quête n'est pas active aujourd'hui."

    # Récompense
    user_data = get_user_data(data, user_id)
    user_data["tokens"] = user_data.get("tokens", 0) + quest["reward"]

    # Marquer comme complétée
    dq["completed"].setdefault(str(user_id), []).append(quest_id)

    save_data(data)

    # --- ENVOI DU MP ---
    user = bot.get_user(user_id)
    if user:
        try:
            embed = discord.Embed(
                title="🎉 Quête journalière complétée !",
                description=(
                    f"Tu as terminé la quête :\n"
                    f"**{quest['name']}**\n\n"
                    f"🎁 Récompense : **{quest['reward']} token(s)**"
                ),
                color=discord.Color.green()
            )
            await user.send(embed=embed)
        except:
            pass

    return True, quest


PROGRESSION_QUESTS = {
    "boost3": {
        "name": "Avoir son boost niveau 3",
        "reward": "<:oeuf_de_dragon:1515707239737065563> Œuf de dragon"
    },
    "forgeron4": {
        "name": "Avoir son forgeron niveau 4",
        "reward": "<:oeuf_de_dragon_rare:1516065280416284782> Œuf de dragon rare"
    },
    "ferme": {
        "name": "Acheter la ferme",
        "reward": "<:oeuf_de_dragon_epique:1516064792400629802> Œuf de dragon épique"
    },
    "canne_max": {
        "name": "Avoir la canne à pêche niveau max",
        "reward": "🪙 3 tokens"
    }
}


async def complete_progress_quest(user_id, quest_key):
    data = load_data()
    user_data = get_user_data(data, user_id)

    # Déjà faite ?
    if user_data["progress_quests"].get(quest_key, False):
        return False

    # Marquer comme faite
    user_data["progress_quests"][quest_key] = True

    # Récompense
    reward = PROGRESSION_QUESTS[quest_key]["reward"]

    # Donner la récompense
    if "Œuf de dragon épique" in reward:
        user_data["inventory"].append("<:oeuf_de_dragon_epique:1516064792400629802> Œuf de dragon épique")
    elif "Œuf de dragon rare" in reward:
        user_data["inventory"].append("<:oeuf_de_dragon_rare:1516065280416284782> Œuf de dragon rare")
    elif "Œuf de dragon" in reward:
        user_data["inventory"].append("<:oeuf_de_dragon:1515707239737065563> Œuf de dragon")
    elif "2 tokens" in reward:
        user_data["tokens"] += 2
    elif "3 tokens" in reward:
        user_data["tokens"] += 3

    save_data(data)

    # MP
    user = bot.get_user(user_id)
    if user:
        try:
            await user.send(
                f"🎉 Tu as terminé la quête de progression : **{PROGRESSION_QUESTS[quest_key]['name']}** !\n"
                f"🎁 Récompense : **{reward}**"
            )
        except:
            pass

    return True


@bot.tree.command(name="quetes", description="Affiche ta progression dans les quêtes permanentes")
async def quetes(interaction: discord.Interaction):

    data = load_data()
    user_data = get_user_data(data, interaction.user.id)

    desc = ""

    for key, q in PROGRESSION_QUESTS.items():
        done = user_data["progress_quests"].get(key, False)
        status = "✅ Terminée" if done else "❌ Non terminée"
        desc += f"**{q['name']}**\n➡️ {status}\n🎁 Récompense : {q['reward']}\n\n"

    embed = discord.Embed(
        title="📘 Quêtes de progression",
        description=desc,
        color=discord.Color.blue()
    )

    await interaction.response.send_message(embed=embed)

#########################################

ID_SALON_GUERRE = 1498036546928902185





bot.run(os.getenv('DISCORD_TOKEN'))