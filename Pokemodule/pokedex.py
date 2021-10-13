from Pokemodule.pokemon import Pokemon
from Pokemodule.attacks import Attack

from Pokemodule.poketools import *
from enum import Enum

# ATTACKS

payback = Attack('Payback', 'Si no ataca primero dobla la potencia', 
                    True, False, 50, 100, False, True, [Kind.Siniestro], 10, 
                    lambda cm, pf, pt: payback_effect_funct(cm, pf, pt))

def payback_effect_funct(combat_manager, pokemon_from, pokemon_to):
    first = combat_manager.turn_sequence()
    if first != pokemon_from:
        combat_manager.attacks_selected[pokemon_from].intensity = 100

    dmg = combat_manager.compute_damage(pokemon_from, pokemon_to)
    combat_manager.pokemons_on_combat[pokemon_to].substract_hp(dmg)

    combat_manager.attacks_selected[pokemon_from].intensity = 50
    
    print('{} damage done!'.format(dmg))


hex_att = Attack('Hex', '', 
                    True, False, 65, 100, False, False, [Kind.Fantasma], 10, 
                    lambda cm, pf, pt: hex_effect_funct(cm, pf, pt))

def hex_effect_funct(combat_manager, pokemon_from, pokemon_to):
    if combat_manager.pokemons_on_combat[pokemon_to].status != []:
        combat_manager.attacks_selected[pokemon_from].intensity = 130

    dmg = combat_manager.compute_damage(pokemon_from, pokemon_to)
    combat_manager.pokemons_on_combat[pokemon_to].substract_hp(dmg)

    print('{} damage done!'.format(dmg))

    
    combat_manager.attacks_selected[pokemon_from].intensity = 65


lick = Attack('Lenguetazo', '',
                    True, False, 30, 100, False, True, [Kind.Fantasma], 30, 
                    lambda cm, pf, pt: lick_effect_funct(cm, pf, pt))

def lick_effect_funct(combat_manager, pokemon_from, pokemon_to):
    status_prob = random.randint(1,3)

    if status_prob == 3:
        combat_manager.pokemons_on_combat[pokemon_to].status.append(Status.Paralizado)

    dmg = combat_manager.compute_damage(pokemon_from, pokemon_to)
    combat_manager.pokemons_on_combat[pokemon_to].substract_hp(dmg)
    print('{} damage done!'.format(dmg))
    

confuse_air = Attack('Aire confuso', '', 
                    True, False, 0, 100, False, False, [Kind.Fantasma], 10, 
                    lambda cm, pf, pt: confuse_air_effect_funct(cm, pf, pt))

def confuse_air_effect_funct(combat_manager, pokemon_from, pokemon_to):
    combat_manager.pokemons_on_combat[pokemon_to].status.append(Status.Confuso)

# POKEMONS


class Pok(Enum):
    bletly = Pokemon('Bletly', 20, {'health': 35,
                                'attack': 15,
                                'defense': 14,
                                'spe_attack': 38, 
                                'spe_defense': 17,
                                'speed': 33,
                                'acc': 1
                                },
                (Kind.Fantasma, Kind.Veneno),
                [payback, hex_att, lick, confuse_air],
                []
                )

    ardum = Pokemon('Ardum', 20, {'health': 46,
                              'attack': 28,
                              'defense': 37,
                              'spe_attack': 25, 
                              'spe_defense': 32,
                              'speed': 17,
                              'acc': 1
                              },
                (Kind.Acero, Kind.Psiquico),
                [],
                [])

    solmergle = Pokemon('Solmergle', 20, {'health': 61,
                              'attack': 30,
                              'defense': 23,
                              'spe_attack': 26, 
                              'spe_defense': 31,
                              'speed': 41,
                              'acc': 1
                              },
                (Kind.Acero, Kind.Fuego),
                [],
                [])

    mamioswine = Pokemon('Mamioswine', 34, {'health': 128,
                              'attack': 103,
                              'defense': 69,
                              'spe_attack': 62, 
                              'spe_defense': 55,
                              'speed': 68,
                              'acc': 1
                              },
                (Kind.Acero, Kind.Psiquico),
                [],
                [])
