from dataclasses import dataclass
from Pokemodule.poketools import *

import random

@dataclass
class CombatManager():

    trainer_1: dict
    trainer_2: dict

    pokemons_on_combat: list
    attacks_selected: list

    battleground_cond: list
    turn_counter: int

    def exec_combat(self):
        # while trainers have pokemons
        log_combat = ''
        if len(self.pokemons_on_combat) == 2 and len(self.attacks_selected): 
            if 'CHOOSE ANOTHER POKEMON' not in self.pokemons_on_combat:
                second = [0, 1]

                first = self.turn_sequence()
                print(first)

                second.remove(first) 
                second = second[0]

                log_combat += '{} ataca primero!'.format(self.pokemons_on_combat[first].name)
                self.exec_attack(first, second)

                if not (self.pokemons_on_combat[second].is_faint()):
                    log_combat += '{} ataca ahora!'.format(self.pokemons_on_combat[second].name)
                    self.exec_attack(second, first)

    def turn_sequence(self):
        if self.attacks_selected[0].priority == self.attacks_selected[1].priority:
            return self.choose_fast_pokemon()
        else:
            if self.attacks_selected[0].priority:
                return 0
            else: 
                return 1

    def choose_fast_pokemon(self):
        if self.pokemons_on_combat[0].attributes['speed'] < self.pokemons_on_combat[1].attributes['speed']:
            return 1
        elif self.pokemons_on_combat[0].attributes['speed'] > self.pokemons_on_combat[1].attributes['speed']:
            return 0
        else:
            return random.randint(0, 1)

    def exec_attack(self, pokemon_from, pokemon_to):
        # compute damage
        self.attacks_selected[pokemon_from].effects(self, pokemon_from, pokemon_to)

        if self.pokemons_on_combat[pokemon_to].is_faint():
            self.pokemons_on_combat[pokemon_to] = 'CHOOSE ANOTHER POKEMON'

    def compute_damage(self, pokemon_from:int, pokemon_to:int):

        if (self.attacks_selected[pokemon_from].physical and self.attacks_selected[pokemon_from].special):
            attack_kind = 'both'
        else:
            if self.attacks_selected[pokemon_from].physical:
                attack_kind = 'phy'
            else:
                attack_kind = 'spe'
        
        princ_damage = ((((self.pokemons_on_combat[pokemon_from].level * 2) / 5) + 2) * 
                        self.attacks_selected[pokemon_from].intensity)

        if attack_kind == 'phy':
            att_def_bonificator = (self.pokemons_on_combat[pokemon_from].attributes['attack'] / 
                                    self.pokemons_on_combat[pokemon_to].attributes['defense'])

        elif attack_kind == 'spe':
            att_def_bonificator = (self.pokemons_on_combat[pokemon_from].attributes['spe_attack'] / 
                                    self.pokemons_on_combat[pokemon_to].attributes['spe_defense'])

        else:
            att_def_bonificator = ((self.pokemons_on_combat[pokemon_from].attributes['attack'] + 
                                    self.pokemons_on_combat[pokemon_from].attributes['spe_attack']) / 
                                    (self.pokemons_on_combat[pokemon_to].attributes['defense'] + 
                                    self.pokemons_on_combat[pokemon_to].attributes['spe_defense']))

        princ_damage *= att_def_bonificator

        princ_damage /= 50

        princ_damage += 2

        its_crit = random.randint(1,20)
        
        if its_crit == 20:
            princ_damage *= 1.5

        princ_damage *= random.uniform(0.85, 1.00)

        princ_damage *= self.compute_effectiviness(pokemon_from, pokemon_to).value

        if self.check_stab(pokemon_from):
            princ_damage *= 1.5
        
        return int(princ_damage)


    def compute_effectiviness(self, pokemon_from, pokemon_to):
        attack_kind = self.attacks_selected[pokemon_from].attack_type
        
        if len(attack_kind) == 1:
            attack_kind = attack_kind[0]
            effectiveness = dict_kind_table[attack_kind]

            defense_kinds = self.pokemons_on_combat[pokemon_to].types
            presence = []

            if len(defense_kinds) == 1:
                for effective in effectiveness:
                    if defense_kinds[0] in effectiveness[effective]:
                        presence.append(effective)
            else:
                for effective in effectiveness:
                    if defense_kinds[0] in effectiveness[effective]:
                        presence.append(effective)

                    if defense_kinds[1] in effectiveness[effective]:
                        presence.append(effective)

        if 'inmune_to' in presence:
            return Strong(0)
        else:
            effective = presence.count('effective_to')
            non_effective = presence.count('non_effective')

            if effective - non_effective > 0:
                return Strong(effective*2)
            elif effective - non_effective < 0:
                return Strong(1/non_effective)
            else: 
                return Strong(1)
                
    def check_stab(self, pokemon_from):
        attack_kind = self.attacks_selected[pokemon_from].attack_type
        pokemon_kind = self.pokemons_on_combat[pokemon_from].types

        if len(attack_kind) == 1:
            if attack_kind in pokemon_kind:
                return True
        else:
            if attack_kind[0] in pokemon_kind:
                return True

            if attack_kind[1] in pokemon_kind:
                return True

        return False

