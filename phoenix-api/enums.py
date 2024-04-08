from enum import Enum


class Condition(str, Enum):
    GOOD = 'good'
    SECOND_HAND = 'second_hand'
    NEED_RENOVATION = 'need_renovation'


class EnergyLabel(str, Enum):
    A_PLUS_PLUS = 'a_plus_plus'
    A_PLUS = 'a_plus'
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'
    E = 'e'


class PropertyType(str, Enum):
    SALE = 'sale'
    RENT = 'rent'
