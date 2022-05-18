import math
import random

from logic import Combat

rep_tables = [
    0, 50, 100, 200,
    300, 400, 500,
    600, 850
]

base_stats_table = {
    'health': 0,
    'power': 0,
    'defence': 0,
    'accuracy': 0, # hit chance
    'speed': 0 # 1st attack chance
}


class Creature:
    skill_names = list()
    base_stats = base_stats_table
    name = 'default creature'
    reputation = 0
    money = 0
    level = 0 #TODO
    
    def make_stats(self):
        hp, pwr, deff, acc, spd = self.base_stats.values()
        
        hp = int(hp + self.level * 30)
        pwr = int(pwr + self.level * 5)
        deff = int(deff + self.level * 0.5)
        acc = float(acc + self.level * 0.005)
        spd = float(spd + self.level * 0.05)
        
        self.base_stats = {
            'health': hp,
            'power': pwr,
            'defence': deff,
            'accuracy': acc,
            'speed': spd
        }
        
        self.max_stats = self.base_stats.copy()
    
    def isalive(self):
        return (self.base_stats['health'] > 0) if 'health' in self.base_stats else False

    def levelup(self):
        pass
        
class Player(Creature):
    
    def reputation_gain(self, exp):
        print('You received %d REP' % exp)
        old_lvl = self.level
        self.reputation = self.reputation + exp
        self.level = len([x for x in rep_tables if self.reputation >= x])
        if self.level > old_lvl:
            self.levelup()
            
    def levelup(self):
        self.make_stats()
        print('You are now level %d' % self.level)


class Monster(Creature):
    def __init__(self, name, level):
        # Monster has fixed level
        self.level = level
        self.name = name
        self.make_stats()


def combat(a: Creature, b: Creature):
    c = Combat(a, b)
    if random.random() >= c.initiative:
        print('%s failed to attack first' % c.attacker.name)
        c.swap()
    
    c.make_turn()