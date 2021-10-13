#!/usr/bin/python3

"""Copyright (c) 2019, Douglas Otwell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import dbus

from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor
from Pokemodule import combat_manager
from Pokemodule.pokedex import *
from Pokemodule.poketools import Kind
import random

from copy import deepcopy
from dataclasses import asdict
import json

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

enemy_trainer = {
    'name': 'Doctorando Alfonso',
    'Pokemons': [Pok.bletly.value],
    'Frase_Inicio': 'Veamos que tal va ese cliente ble jeje',
    'Frase_Victoria': 'Buen intento, seguro que el proximo sera mejor',
    'Frase_Derrota': 'La virgen santa si que viene fuerte la juventud',
    'AI_Function': '',
}

ally_trainer = {}
new_pokes = []

def init_combats(n):
    combat_array = []

    for i in range(n):
        combat_array.append(combat_manager.CombatManager(enemy_trainer, ally_trainer, [enemy_trainer['Pokemons'][0]], [random.choice(enemy_trainer['Pokemons'][0].attacks)], [], 0))

    return combat_array

combat_array = init_combats(20)

class CombatAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("Combate")
        self.include_tx_power = True

class CombatInfoService(Service):
    COMBAT_INFO_SVC_UUID = "00000001-710e-4a5b-8d75-3e5b444bc3cf"

    def __init__(self, index, combat):
        self.combat = combat

        Service.__init__(self, index, self.COMBAT_INFO_SVC_UUID, True)
        self.add_characteristic(EnemyPokemonCharacteristic(self))
        self.add_characteristic(EntablishTrainerCharacteristic(self))
        self.add_characteristic(ChooseActionCharacteristic(self))

    def what_turn(self):
        return self.combat.turn_counter

class EnemyPokemonCharacteristic(Characteristic):
    ENEMY_POK_CHARACTERISTIC_UUID = "00000002-710e-4a5b-8d75-3e5b444bc3cf"

    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(
                self, self.ENEMY_POK_CHARACTERISTIC_UUID,
                ["notify", "read"], service)
        self.add_descriptor(EnemyPokDescriptor(self))

    def get_info(self):
        health = self.service.combat.pokemons_on_combat[0].attributes['health']
        kinds = self.service.combat.pokemons_on_combat[0].types

        str_format = '{} HP | '.format(health)
        for kind in kinds:
            str_format += '{} '.format(kind.name)

        final = []

        for c in str_format:
            final.append(dbus.Byte(c.encode()))

        return final

    def set_info_callback(self):
        if self.notifying:
            value = self.get_info()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_info()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_info_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_info()

        return value

class EnemyPokDescriptor(Descriptor):
    ENEMY_POK_DESCRIPTOR_UUID = "20000001-710e-4a5b-8d75-3e5b444bc3cf"
    ENEMY_POK_DESCRIPTOR_VALUE = "Enemy Pokemon Info (Health and Types)"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.ENEMY_POK_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.ENEMY_POK_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value

class ChooseActionCharacteristic(Characteristic):
    CHOOSE_ACTION_CHARACTERISTIC_UUID = "00000003-710e-4a5b-8d75-3e5b444bc3cf"
    
    def __init__(self, service):
            Characteristic.__init__(
                    self, self.CHOOSE_ACTION_CHARACTERISTIC_UUID,
                    ["read", "write"], service)
            self.add_descriptor(ChooseActionDescriptor(self, self.service.combat))

    def WriteValue(self, value, options):
        try:
            val = int(value[0])

            if val >= 0 and val < 5:

                if val == 0:

                    if int(value[1]) >= 0 and int(value[1]) <= len(self.service.combat.trainer_2['Pokemons']):
                        self.service.combat.pokemons_on_combat[1] = self.service.combat.trainer_2['Pokemons'][int(value[1])]
                else:
                    if len(self.service.combat.attacks_selected) < 2:
                        self.service.combat.attacks_selected.append(self.pokemons_on_combat[1].attacks[val])
                    
                    else:
                        self.service.combat.attacks_selected[1] = self.pokemons_on_combat[1].attacks[val]

        except Exception as e:
            print(e)

    def ReadValue(self, options):
        value = []

        desc = 'You choose the attack/action: {}'.format(self.service.combat.attacks_selected[1].name)

        for c in str_format:
            value.append(dbus.Byte(c.encode()))

        return value



class ChooseActionDescriptor(Descriptor):
    CHOOSE_ACTION_DESCRIPTOR_UUID = "30000001-710e-4a5b-8d75-3e5b444bc3cf"
    CHOOSE_ACTION_DESCRIPTOR_VALUE = "Actions to make on turn: "

    def __init__(self, characteristic, combat_ref):
        Descriptor.__init__(
                self, self.CHOOSE_ACTION_DESCRIPTOR_UUID,
                ["read"],
                characteristic)
        self.combat_ref = combat_ref

    def ReadValue(self, options):
        try:
            if len(self.combat_ref.pokemons_on_combat) > 1:
                if self.combat_ref.pokemons_on_combat[1] != 'CHOOSE ANOTHER POKEMON':
                    desc = self.CHOOSE_ACTION_DESCRIPTOR_VALUE

                    attacks = self.combat_ref.pokemons_on_combat[1].attacks

                    desc += '\n> [0] Change pokemon'
                    for index, attack in enumerate(attacks):
                        desc += '\n> [{}] {} | {} | {}'.format(index+1, attack.name, attack.pp, attack.desc)

                else:
                    desc = 'Your pokemon its faint, choose another in the appropiated characteristic!'

            else:
                desc = 'You should choose a pokemon before the attack!'

            value = []

            for c in desc:
                value.append(dbus.Byte(c.encode()))

            return value

        except Exception as e:
            print(e)

class ExecActionCharacteristic(Characteristic):
    CHOOSE_ACTION_CHARACTERISTIC_UUID = "00000005-710e-4a5b-8d75-3e5b444bc3cf"
    
    def __init__(self, service):
            Characteristic.__init__(
                    self, self.CHOOSE_ACTION_CHARACTERISTIC_UUID,
                    ["read", "write"], service)
            self.add_descriptor(ChooseActionDescriptor(self, self.service.combat))

    def WriteValue(self, value, options):
        self.service.combat.exec_combat()

    def ReadValue(self, options):
        value = []

        desc = 'You choose the attack/action: {}'.format(self.service.combat.attacks_selected[1].name)

        for c in str_format:
            value.append(dbus.Byte(c.encode()))

        return value

class ExecActionDescriptor(Descriptor):
    pass

class EntablishTrainerCharacteristic(Characteristic):
    TRAINER_CHARACTERISTIC_UUID = "00000004-710e-4a5b-8d75-3e5b444bc3cf"
    
    def __init__(self, service):
        Characteristic.__init__(
                self, self.TRAINER_CHARACTERISTIC_UUID,
                ["read", "write"], service)
        self.add_descriptor(EntablishTrainerDescriptor(self))
    
    def WriteValue(self, value, options):
        str_final = ''
        for element in value:
            str_final += str(element)

        try:
            dict_final = json.loads(str_final)
            pokemons_aux = []
            for pokemon_name in dict_final['Pokemons']:
                pokemons_aux.append(eval('deepcopy(Pok.{}.value)'.format(pokemon_name)))
            
            dict_final['Pokemons'] = pokemons_aux
            self.service.combat.trainer_2 = dict_final
            print('Added trainer!')

            if len(self.service.combat.pokemons_on_combat) == 1:
                self.service.combat.pokemons_on_combat.append(self.service.combat.trainer_2['Pokemons'][0])
            else:
                self.service.combat.pokemons_on_combat[1] = self.service.combat.trainer_2['Pokemons'][0]

        except Exception as e:
            print(e)
            
    def ReadValue(self, options):
        value = []

        if self.service.is_farenheit(): val = "F"
        else: val = "C"
        value.append(dbus.Byte(val.encode()))

        return value


class EntablishTrainerDescriptor(Descriptor):
    TRAINER_DESCRIPTOR_UUID = "40000001-710e-4a5b-8d75-3e5b444bc3cf"
    TRAINER_DESCRIPTOR_VALUE = "You should add a trainer in format JSON"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.TRAINER_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.TRAINER_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value

class DexService(Service):
    DEX_INFO_SVC_UUID = "00000006-710e-4a5b-8d75-3e5b444bc3cf"

    def __init__(self, index):

        Service.__init__(self, index, self.DEX_INFO_SVC_UUID, True)
        self.add_characteristic(ConsultPokemonCharacteristic(self))
        self.add_characteristic(ConsultAttackCharacteristic(self))

class ConsultPokemonCharacteristic(Characteristic):
    CONSULT_POK_CHARACTERISTIC_UUID = "60000001-710e-4a5b-8d75-3e5b444bc3cf"
    
    def __init__(self, service):
            Characteristic.__init__(
                    self, self.CONSULT_POK_CHARACTERISTIC_UUID,
                    ["read", "write"], service)
            self.add_descriptor(ConsultPokemonDescriptor(self))
            self.last_pok = ''

    def WriteValue(self, value, options):
        try:
            val = str(value).lower()

            self.last_pok = eval('Pok.{}.value'.format(val))

        except Exception as e:
            print(e)

    def ReadValue(self, options):
        value = []

    
        str_format = 'last Pokemon searched: {}'.format(self.last_pok)

        for c in str_format:
            value.append(dbus.Byte(c.encode()))

        return value

class ConsultPokemonDescriptor(Descriptor):
    POK_INFO_DESCRIPTOR_UUID = "61000001-710e-4a5b-8d75-3e5b444bc3cf"
    POK_INFO_DESCRIPTOR_VALUE = "Introduce the name of the pokemon to consult: "

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.POK_INFO_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        try:
            desc = POK_INFO_DESCRIPTOR_VALUE
            for index, pok in enumerate(Pok):
                desc += '\n [{}] {}'.format(index, pok.value.name)

            value = []

            for c in desc:
                value.append(dbus.Byte(c.encode()))

            return value

        except Exception as e:
            print(e)

class ConsultAttackCharacteristic(Characteristic):
    CONSULT_ATCK_CHARACTERISTIC_UUID = "60000002-710e-4a5b-8d75-3e5b444bc3cf"
    
    def __init__(self, service):
            Characteristic.__init__(
                    self, self.CONSULT_ATCK_CHARACTERISTIC_UUID,
                    ["read", "write"], service)
            self.add_descriptor(ConsultAttackDescriptor(self))
            self.last_pok = ''

    def WriteValue(self, value, options):
        try:
            val = str(value).lower()

            self.last_pok = eval('Attackpedia.{}.value'.format(val))

        except Exception as e:
            print(e)

    def ReadValue(self, options):
        value = []

        str_format = 'last Pokemon searched: {}'.format(self.last_pok)

        for c in str_format:
            value.append(dbus.Byte(c.encode()))

        return value

class ConsultAttackDescriptor(Descriptor):
    ATCK_INFO_DESCRIPTOR_UUID = "62000001-710e-4a5b-8d75-3e5b444bc3cf"
    ATCK_INFO_DESCRIPTOR_VALUE = "Introduce the name of the attack to consult: "

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.ATCK_INFO_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        try:
            desc = ATCK_INFO_DESCRIPTOR_VALUE
            for index, atck in enumerate(Attackpedia):
                desc += '\n [{}] {}'.format(index, atck.value.name)

            value = []

            for c in desc:
                value.append(dbus.Byte(c.encode()))

            return value

        except Exception as e:
            print(e)

class CreateService(Service):
    CREATE_SVC_UUID = "00000007-710e-4a5b-8d75-3e5b444bc3cf"

    def __init__(self, index):

        Service.__init__(self, index, self.CREATE_SVC_UUID, True)
        self.add_characteristic(CreatePokemonCharacteristic(self))
        self.add_characteristic(CreateAttackCharacteristic(self))

class CreatePokemonCharacteristic(Characteristic):
    CREATE_POK_CHARACTERISTIC_UUID = "70000001-710e-4a5b-8d75-3e5b444bc3cf"
    
    def __init__(self, service):
            Characteristic.__init__(
                    self, self.CREATE_POK_CHARACTERISTIC_UUID,
                    ["read", "write"], service)
            self.add_descriptor(CreatePokemonDescriptor(self))
            self.last_pok_added = ''

    def WriteValue(self, value, options):
        try:
            val = json.loads(str(value))
            eval('pokedex.Pok.{} = Pokemon({}, {}, {}, {}, {}, {})'.format(val['name'],
                                                                            val['level'],
                                                                            val['attributes'],
                                                                            val['types'],
                                                                            val['attacks'],
                                                                            val['status']))


            
        except Exception as e:
            print(e)

    def ReadValue(self, options):
        value = []

        str_format = 'last Pokemon added: {}'.format(self.last_pok_added)

        for c in str_format:
            value.append(dbus.Byte(c.encode()))

        return value

class CreatePokemonDescriptor(Descriptor):
    CREATE_POK_DESCRIPTOR_UUID = "71000001-710e-4a5b-8d75-3e5b444bc3cf"
    CREATE_POK_DESCRIPTOR_VALUE = "Give a JSON object to create a Pokemon"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.CREATE_POK_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        try:
            desc = POK_INFO_DESCRIPTOR_VALUE

            value = []

            for c in desc:
                value.append(dbus.Byte(c.encode()))

            return value

        except Exception as e:
            print(e)

class CreateAttackCharacteristic(Characteristic):
    CREATE_ATCK_CHARACTERISTIC_UUID = "70000002-710e-4a5b-8d75-3e5b444bc3cf"
    
    def __init__(self, service):
            Characteristic.__init__(
                    self, self.CREATE_ATCK_CHARACTERISTIC_UUID,
                    ["read", "write"], service)
            self.add_descriptor(ConsultAttackDescriptor(self))
            self.last_attack = ''

    def WriteValue(self, value, options):
        try:
            val = json.loads(str(value))

            self.last_pok = eval('Attackpedia.{}.value'.format(val))
            eval('pokedex.Attackpedia.{} = Attack({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(val['name'],
                                                                                                        val['desc'],
                                                                                                        bool(val['physical']),
                                                                                                        bool(val['special']),
                                                                                                        int(val['intensity']),
                                                                                                        int(val['accurated'])),
                                                                                                        bool(val['priority']),
                                                                                                        bool(val['makes_contact']),
                                                                                                        [eval('Kind.{}'.format(i)) for i in val['attack_type']],
                                                                                                        int(val['pp']),
                                                                                                        lambda cm, pf, pt: eval('{}'.format(val['effects'])))



        except Exception as e:
            print(e)

    def ReadValue(self, options):
        value = []

        str_format = 'last attack created: {}'.format(self.last_pok)

        for c in str_format:
            value.append(dbus.Byte(c.encode()))

        return value

class CreateAttackDescriptor(Descriptor):
    CREATE_ATCK_DESCRIPTOR_UUID = "72000001-710e-4a5b-8d75-3e5b444bc3cf"
    CREATE_ATCK_DESCRIPTOR_VALUE = "Introduce the name of the attack to create: "

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.ATCK_INFO_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        try:
            desc = CREATE_ATCK_DESCRIPTOR_VALUE

            value = []

            for c in desc:
                value.append(dbus.Byte(c.encode()))

            return value

        except Exception as e:
            print(e)


app = Application()

for i in range(2):
    app.add_service(CombatInfoService(i, combat_array[i]))

app.add_service(DexService(20))
app.add_service(CreateService(21))

app.register()

adv = CombatAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()
