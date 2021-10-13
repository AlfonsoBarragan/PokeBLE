from enum import Enum

class Kind(Enum):
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

class Status(Enum):
    Paralizado = 1
    Envenenado = 2
    Quemado = 3
    Congelado = 4
    Confuso = 5