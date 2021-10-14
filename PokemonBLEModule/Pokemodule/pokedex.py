from Pokemodule.pokemon import Pokemon
from Pokemodule.attacks import Attack

from enum import Enum

# KINDS

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
    Kindpedia.Acero: {
                    'effective_to': [Kindpedia.Hada, Kindpedia.Hielo, Kindpedia.Roca],
                    'non_effective': [Kindpedia.Acero, Kindpedia.Agua, Kindpedia.Tierra, Kindpedia.Fuego]
                },

    Kindpedia.Agua: {
                    'effective_to': [Kindpedia.Fuego, Kindpedia.Tierra, Kindpedia.Roca],
                    'non_effective': [Kindpedia.Agua, Kindpedia.Dragon, Kindpedia.Planta]
                },

    Kindpedia.Bicho: {
                    'effective_to': [Kindpedia.Planta, Kindpedia.Psiquico, Kindpedia.Siniestro],
                    'non_effective': [Kindpedia.Acero, Kindpedia.Fantasma, Kindpedia.Fuego, Kindpedia.Hada, 
                                      Kindpedia.Lucha, Kindpedia.Veneno, Kindpedia.Volador]
                },

    Kindpedia.Dragon: {
                    'effective_to': [Kindpedia.Dragon],
                    'non_effective': [Kindpedia.Acero],
                    'inmune_to':[Kindpedia.Hada]
                },

    Kindpedia.Electrico: {
                        'effective_to': [Kindpedia.Agua, Kindpedia.Volador, Kindpedia.Roca],
                        'non_effective': [Kindpedia.Dragon, Kindpedia.Electrico, Kindpedia.Planta],
                        'inmune_to': [Kindpedia.Tierra]
                    },

    Kindpedia.Fantasma: {
                        'effective_to': [Kindpedia.Fantasma, Kindpedia.Psiquico],
                        'non_effective': [Kindpedia.Siniestro],
                        'inmune_to': [Kindpedia.Normal]
                    },

    Kindpedia.Fuego: {
                    'effective_to': [Kindpedia.Acero, Kindpedia.Bicho, Kindpedia.Hielo, Kindpedia.Planta],
                    'non_effective': [Kindpedia.Agua, Kindpedia.Dragon, Kindpedia.Fuego, Kindpedia.Roca]
                },

    Kindpedia.Hada: {
                    'effective_to': [Kindpedia.Dragon, Kindpedia.Lucha, Kindpedia.Siniestro],
                    'non_effective': [Kindpedia.Acero, Kindpedia.Fuego, Kindpedia.Veneno]
                },

    Kindpedia.Hielo: {
                    'effective_to': [Kindpedia.Dragon, Kindpedia.Planta, Kindpedia.Tierra, Kindpedia.Volador],
                    'non_effective': [Kindpedia.Fuego, Kindpedia.Agua, Kindpedia.Acero, Kindpedia.Hielo]
                },

    Kindpedia.Lucha: {
                    'effective_to': [Kindpedia.Acero, Kindpedia.Hielo, Kindpedia.Normal, Kindpedia.Roca, Kindpedia.Siniestro],
                    'non_effective': [Kindpedia.Bicho, Kindpedia.Hada, Kindpedia.Psiquico, Kindpedia.Veneno, Kindpedia.Volador],
                    'inmune_to': [Kindpedia.Fantasma]
                },

    Kindpedia.Normal: {
                    'effective_to': [],
                    'non_effective': [Kindpedia.Acero, Kindpedia.Roca],
                    'inmune_to': [Kindpedia.Fantasma]
                },

    Kindpedia.Planta: {
                    'effective_to': [Kindpedia.Agua, Kindpedia.Tierra, Kindpedia.Roca],
                    'non_effective': [Kindpedia.Fuego, Kindpedia.Acero, Kindpedia.Dragon, 
                                      Kindpedia.Bicho, Kindpedia.Planta, Kindpedia.Veneno,
                                      Kindpedia.Volador]
                },

    Kindpedia.Psiquico: {
                    'effective_to': [Kindpedia.Lucha, Kindpedia.Veneno],
                    'non_effective': [Kindpedia.Acero, Kindpedia.Psiquico],
                    'inmune_to': [Kindpedia.Siniestro]
                },

    Kindpedia.Roca: {
                    'effective_to': [Kindpedia.Fuego, Kindpedia.Bicho, Kindpedia.Hielo, Kindpedia.Volador],
                    'non_effective': [Kindpedia.Acero, Kindpedia.Lucha, Kindpedia.Tierra]
                },

    Kindpedia.Siniestro: {
                    'effective_to': [Kindpedia.Fantasma, Kindpedia.Psiquico],
                    'non_effective': [Kindpedia.Hada, Kindpedia.Lucha, Kindpedia.Siniestro]
                },

    Kindpedia.Tierra: {
                    'effective_to': [Kindpedia.Fuego, Kindpedia.Acero, Kindpedia.Electrico, Kindpedia.Roca, Kindpedia.Veneno],
                    'non_effective': [Kindpedia.Bicho, Kindpedia.Planta],
                    'inmune_to': [Kindpedia.Volador]
                },

    Kindpedia.Veneno: {
                    'effective_to': [Kindpedia.Hada, Kindpedia.Planta],
                    'non_effective': [Kindpedia.Fantasma, Kindpedia.Roca, Kindpedia.Tierra,
                                      Kindpedia.Veneno],
                    'inmune_to': [Kindpedia.Acero]
                },

    Kindpedia.Volador: {
                    'effective_to': [Kindpedia.Bicho, Kindpedia.Lucha, Kindpedia.Planta],
                    'non_effective': [Kindpedia.Acero, Kindpedia.Electrico, Kindpedia.Roca]
                }

}


# ATTACKS

class Attackpedia(Enum):

    payback = Attack('Payback', 'Si no ataca primero dobla la potencia', 
                        True, False, 50, 100, False, True, [Kindpedia.Siniestro], 10, 
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
                        True, False, 65, 100, False, False, [Kindpedia.Fantasma], 10, 
                        lambda cm, pf, pt: hex_effect_funct(cm, pf, pt))

    def hex_effect_funct(combat_manager, pokemon_from, pokemon_to):
        if combat_manager.pokemons_on_combat[pokemon_to].status != []:
            combat_manager.attacks_selected[pokemon_from].intensity = 130

        dmg = combat_manager.compute_damage(pokemon_from, pokemon_to)
        combat_manager.pokemons_on_combat[pokemon_to].substract_hp(dmg)

        print('{} damage done!'.format(dmg))

        
        combat_manager.attacks_selected[pokemon_from].intensity = 65


    lick = Attack('Lenguetazo', '',
                        True, False, 30, 100, False, True, [Kindpedia.Fantasma], 30, 
                        lambda cm, pf, pt: lick_effect_funct(cm, pf, pt))

    def lick_effect_funct(combat_manager, pokemon_from, pokemon_to):
        status_prob = random.randint(1,3)

        if status_prob == 3:
            combat_manager.pokemons_on_combat[pokemon_to].status.append(Statuspedia.Paralizado)

        dmg = combat_manager.compute_damage(pokemon_from, pokemon_to)
        combat_manager.pokemons_on_combat[pokemon_to].substract_hp(dmg)
        print('{} damage done!'.format(dmg))
        

    confuse_air = Attack('Aire confuso', '', 
                        True, False, 0, 100, False, False, [Kindpedia.Fantasma], 10, 
                        lambda cm, pf, pt: confuse_air_effect_funct(cm, pf, pt))

    def confuse_air_effect_funct(combat_manager, pokemon_from, pokemon_to):
        combat_manager.pokemons_on_combat[pokemon_to].status.append(Statuspedia.Confuso)

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
                (Kindpedia.Fantasma, Kindpedia.Veneno),
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
                (Kindpedia.Acero, Kindpedia.Psiquico),
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
                (Kindpedia.Acero, Kindpedia.Fuego),
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
                (Kindpedia.Acero, Kindpedia.Psiquico),
                [],
                [])

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