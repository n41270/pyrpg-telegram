import math
import random

from logic import Combat

rep_tables = [round((4 * (i**3)) / 5) for i in range(1, 100)]

base_stats_table = {
    'health': 0,
    'power': 0,
    'defence': 0,
    'accuracy': 0, # hit chance
    'speed': 0 # 1st attack chance
}


class Creature:
    skill_names = list()
    stats = base_stats_table
    name = 'default creature'
    reputation = 0
    money = 0
    level = 0 #TODO
    
    def make_stats(self):
        hp, pwr, deff, acc, spd = self.stats.values()
        
        hp = int(hp + self.level * 30)
        pwr = int(pwr + self.level * 5)
        deff = roll_dice(3, 2, self.level)
        acc = roll_dice(3, 2, self.level)
        spd = roll_dice(1, 2) + math.log(self.level, 10)
        
        self.stats = {
            'health': hp,
            'power': pwr,
            'defence': deff,
            'accuracy': acc,
            'speed': spd
        }
        
        self.max_stats = dict(self.stats)
    
    def isalive(self):
        return (self.stats['health'] > 0) if 'health' in self.stats else False

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

def roll_dice(rolls, faces, modifier=0):
    value = 0
    for i in range(rolls):
        value += random.randrange(faces)

    return value + modifier