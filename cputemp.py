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
from Pokemodule.pokedex import Pok

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

        try:
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

        try:
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


class UnitCharacteristic(Characteristic):
    UNIT_CHARACTERISTIC_UUID = "00000003-710e-4a5b-8d75-3e5b444bc3cf"

    def __init__(self, service):
        Characteristic.__init__(
                self, self.UNIT_CHARACTERISTIC_UUID,
                ["read", "write"], service)
        self.add_descriptor(UnitDescriptor(self))

    def WriteValue(self, value, options):
        val = str(value[0]).upper()
        if val == "C":
            self.service.set_farenheit(False)
        elif val == "F":
            self.service.set_farenheit(True)

    def ReadValue(self, options):
        value = []

        if self.service.is_farenheit(): val = "F"
        else: val = "C"
        value.append(dbus.Byte(val.encode()))

        return value

class UnitDescriptor(Descriptor):
    UNIT_DESCRIPTOR_UUID = "2901"
    UNIT_DESCRIPTOR_VALUE = "Temperature Units (F or C)"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.UNIT_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.UNIT_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value

app = Application()
app.add_service(CombatInfoService(0, combat_array[0]))
app.register()

adv = CombatAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()
