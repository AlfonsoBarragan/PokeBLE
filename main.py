from copy import deepcopy
from Pokemodule.combat_manager import CombatManager
from Pokemodule.pokedex import *

bletly_2 = deepcopy(bletly)
bletly_2.name = 'blet'
bletly_2.attributes['speed'] = 7000

combat = CombatManager({}, {}, [bletly, bletly_2], [], [])
combat.attacks_selected = [bletly.attacks[1], bletly_2.attacks[3]]

combat.exec_combat()

print('{} has {} HP'.format(combat.pokemons_on_combat[0].name, combat.pokemons_on_combat[0].attributes['health']))
print('{} has {} HP'.format(combat.pokemons_on_combat[1].name, combat.pokemons_on_combat[1].attributes['health']))
