# PokeBLE - Bluetooth Low Energy Protocol example with little monsters combat


![Last release](https://img.shields.io/badge/Last%20release-AutoCombat-09900c)
[![Package status](https://img.shields.io/badge/Package%20status-up%20to%20date!-blue)](https://github.com/AlfonsoBarragan/PokeBLE)
![Last commit](https://img.shields.io/github/last-commit/AlfonsoBarragan/PokeBLE)
![Coverage](https://img.shields.io/badge/Coverage-100%25-39b272)
[![License](https://img.shields.io/badge/License-GNU-brightgreen)](https://github.com/AlfonsoBarragan/Galfgets/blob/main/LICENSE)

This is a repo to make a funny example practice centered in the communication with Bluetooth Low Energy (BLE) protocol on the class. The BLE part of this project its based on the repo [cputemp](https://github.com/Douglas6/cputemp) by the user [Douglas6](https://github.com/Douglas6).

Now we will explain the contains of the repo, so I invite you in the incredible world of little monsters jeje.

<img src="./resources/ProfesorAlf.png" width="200" height="270" />

## Requirements
* [Python 3.7 or greater](https://www.python.org/)
    * [dbus](https://pypi.org/project/dbus-python/)

## What is inside of this repo?
```
-- PokeBLE
    |-- PokemonBLEModule
    |   |-- Bluetooth
    |   |   |-- advertisement.py
    |   |   |-- bletools.py
    |   |   |-- pokeserver.py
    |   |   `-- service.py
    |   `-- Pokemodule
    |       |-- attacks.py
    |       |-- combat_manager.py
    |       |-- pokedex.py
    |       `-- pokemon.py
    |-- resources
    |-- LICENSE
    `-- README.md
```

### PokemonBLEModule
This folder contains all the code relative to run the BLE server in class in order that the students can experiment the concepts explain interacting and communicating with it.

* Bluetooth; This subfolder contains all the classes needed to implement a BLE server general.
    * advertisement; In this python file there is the declared the implementation of the advertisement service of the bluetooth app.
    * bletools; In this python file are the functions used to take control about the Bluetooth hardware in other to perform the correct communication.
    * pokeserver; This python file contains the implementation of the BLE server, with all the services, characteristics and descriptors that it needs.
    * service; In this python file its declared all the classes about BLE protocol at high level of abstraction. In other words, this is the specification of the service, characteristic and descriptors objects.

* Pokemodule; This subfolder includes all the class structure to implement your own little monsters, its attacks and a way to store it in enumerations (this probably change in the future due to a loss efficiency).
    * attacks; Python file that includes a dataclass to implement attacks for the monsters.
    * combat_manager; Python file to implement the combat performs and all the factors that should be controlled (battleground conditions, turn sequence of the monsters, etc.) and/or computed (such damage, stab bonus on attacks, etc.)
    * pokedex; On this class its stored all the pokemons, attacks, types, type table and status. As well some utilities to computed different formulas on combat_manager.
    * pokemon; This python file includes another dataclass to implement the monsters itself.





