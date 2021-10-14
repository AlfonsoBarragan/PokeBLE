from PokemonBLEModule.Pokemodule.combat_manager import CombatManager

def init_combats(n):
    combat_array = []

    for i in range(n):
        combat_array.append(combat_manager.CombatManager(enemy_trainer, ally_trainer, [enemy_trainer['Pokemons'][0]], [random.choice(enemy_trainer['Pokemons'][0].attacks)], [], 0))

    return combat_array

def main():

    combats_on_parallel = 1
    combat_array = init_combats(combats_on_parallel)
    
    app = Application()

    for i in range(combats_on_parallel):
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

if __name__:'__main__':
    main()