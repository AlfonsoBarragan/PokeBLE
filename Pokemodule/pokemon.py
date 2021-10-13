from dataclasses import dataclass

@dataclass
class Pokemon:

    name: str
    level: int
    attributes: dict
    types: list

    attacks: list
    status: list

    def get_hp(self) -> int:
        return self.attributes['health']

    def substract_hp(self, damage):
        self.attributes['health'] = self.attributes['health'] - damage
        if self.attributes['health'] <= 0:
            self.attributes['health'] = 0

    def lower_stats(self, quantity, stat):
        self.attributes[stat] = self.attributes[stat] * (1 - (0.25 * quantity))

    def up_stats(self, quantity, stat):
        self.attributes[stat] = self.attributes[stat] * (1 + (0.25 * quantity))

    def is_faint(self) -> bool:
        if self.attributes['health'] <= 0:
            return True

        else:
            return False
