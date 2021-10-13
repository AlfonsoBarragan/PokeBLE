from dataclasses import dataclass

@dataclass
class Attack:


    name: str
    desc: str

    physical: bool
    special: bool

    intensity: int
    accurated: int

    priority: bool
    makes_contact: bool

    attack_type: list
    pp: int
    
    effects: callable
    