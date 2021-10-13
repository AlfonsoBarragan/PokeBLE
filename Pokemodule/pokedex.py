from Pokemodule.pokemon import Pokemon
from Pokemodule.attacks import Attack

from Pokemodule.poketools import *
from enum import Enum

# ATTACKS

class Attackpedia(Enum):

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


class Pokepedia(Enum):
    bletly = Pokemon('Bletly', 20, {'health': 35,
                                'attack': 15,
                                'defense': 14,
                                'spe_attack': 38, 
                                'spe_defense': 17,
                                'speed': 33,
                                'acc': 1
                                },
                (Kind.Fantasma, Kind.Veneno),
                [Attackpedia.payback, Attackpedia.hex_att, Attackpedia.lick, Attackpedia.confuse_air],
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

class Kindpedia(Enum):
    Acero = 0
    Agua = 1
    Bicho = 2
    Dragon = 3
    Electrico = 4
    Fantasma = 5
    Fuego = 6
    Hada = 7
    Hielo = 8
    Lucha = 9
    Normal = 10
    Planta = 11
    Psiquico = 12
    Roca = 13
    Siniestro = 14
    Tierra = 15
    Veneno = 16
    Volador = 17

dict_kind_table = {
    Kind.Acero: {
                    'effective_to': [Kind.Hada, Kind.Hielo, Kind.Roca],
                    'non_effective': [Kind.Acero, Kind.Agua, Kind.Tierra, Kind.Fuego]
                },

    Kind.Agua: {
                    'effective_to': [Kind.Fuego, Kind.Tierra, Kind.Roca],
                    'non_effective': [Kind.Agua, Kind.Dragon, Kind.Planta]
                },

    Kind.Bicho: {
                    'effective_to': [Kind.Planta, Kind.Psiquico, Kind.Siniestro],
                    'non_effective': [Kind.Acero, Kind.Fantasma, Kind.Fuego, Kind.Hada, 
                                      Kind.Lucha, Kind.Veneno, Kind.Volador]
                },

    Kind.Dragon: {
                    'effective_to': [Kind.Dragon],
                    'non_effective': [Kind.Acero],
                    'inmune_to':[Kind.Hada]
                },

    Kind.Electrico: {
                        'effective_to': [Kind.Agua, Kind.Volador, Kind.Roca],
                        'non_effective': [Kind.Dragon, Kind.Electrico, Kind.Planta],
                        'inmune_to': [Kind.Tierra]
                    },

    Kind.Fantasma: {
                        'effective_to': [Kind.Fantasma, Kind.Psiquico],
                        'non_effective': [Kind.Siniestro],
                        'inmune_to': [Kind.Normal]
                    },

    Kind.Fuego: {
                    'effective_to': [Kind.Acero, Kind.Bicho, Kind.Hielo, Kind.Planta],
                    'non_effective': [Kind.Agua, Kind.Dragon, Kind.Fuego, Kind.Roca]
                },

    Kind.Hada: {
                    'effective_to': [Kind.Dragon, Kind.Lucha, Kind.Siniestro],
                    'non_effective': [Kind.Acero, Kind.Fuego, Kind.Veneno]
                },

    Kind.Hielo: {
                    'effective_to': [Kind.Dragon, Kind.Planta, Kind.Tierra, Kind.Volador],
                    'non_effective': [Kind.Fuego, Kind.Agua, Kind.Acero, Kind.Hielo]
                },

    Kind.Lucha: {
                    'effective_to': [Kind.Acero, Kind.Hielo, Kind.Normal, Kind.Roca, Kind.Siniestro],
                    'non_effective': [Kind.Bicho, Kind.Hada, Kind.Psiquico, Kind.Veneno, Kind.Volador],
                    'inmune_to': [Kind.Fantasma]
                },

    Kind.Normal: {
                    'effective_to': [],
                    'non_effective': [Kind.Acero, Kind.Roca],
                    'inmune_to': [Kind.Fantasma]
                },

    Kind.Planta: {
                    'effective_to': [Kind.Agua, Kind.Tierra, Kind.Roca],
                    'non_effective': [Kind.Fuego, Kind.Acero, Kind.Dragon, 
                                      Kind.Bicho, Kind.Planta, Kind.Veneno,
                                      Kind.Volador]
                },

    Kind.Psiquico: {
                    'effective_to': [Kind.Lucha, Kind.Veneno],
                    'non_effective': [Kind.Acero, Kind.Psiquico],
                    'inmune_to': [Kind.Siniestro]
                },

    Kind.Roca: {
                    'effective_to': [Kind.Fuego, Kind.Bicho, Kind.Hielo, Kind.Volador],
                    'non_effective': [Kind.Acero, Kind.Lucha, Kind.Tierra]
                },

    Kind.Siniestro: {
                    'effective_to': [Kind.Fantasma, Kind.Psiquico],
                    'non_effective': [Kind.Hada, Kind.Lucha, Kind.Siniestro]
                },

    Kind.Tierra: {
                    'effective_to': [Kind.Fuego, Kind.Acero, Kind.Electrico, Kind.Roca, Kind.Veneno],
                    'non_effective': [Kind.Bicho, Kind.Planta],
                    'inmune_to': [Kind.Volador]
                },

    Kind.Veneno: {
                    'effective_to': [Kind.Hada, Kind.Planta],
                    'non_effective': [Kind.Fantasma, Kind.Roca, Kind.Tierra,
                                      Kind.Veneno],
                    'inmune_to': [Kind.Acero]
                },

    Kind.Volador: {
                    'effective_to': [Kind.Bicho, Kind.Lucha, Kind.Planta],
                    'non_effective': [Kind.Acero, Kind.Electrico, Kind.Roca]
                }

}

class Strong(Enum):
    Neutral = 1
    Efectivo = 2
    SuperEfectivo = 4
    PocoEfectivo = 0.5
    NadaEfectivo = 0.25
    Inmune = 0

class Statuspedia(Enum):
    Paralizado = 1
    Envenenado = 2
    Quemado = 3
    Congelado = 4
    Confuso = 5