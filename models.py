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

class Stats:
    def __init__(self, mStats):
        self.base = dict()
        self.set_base(mStats)
        
    def set_base(self, mStats):
        self.modifiers = dict()
        for stats, v in mStats.items():
            self.base[stats] = v
            
    def get_base(self, id):
        return self.base[id]
        
    def add_modifier(self, id, mModifier):
        self.modifiers[id] = {
            'add': mModifier['add'] if 'add' in mModifier else {},
            'mult': mModifier['mult'] if 'mult' in mModifier else {}
        }
        
    def del_modifier(self, id):
        del self.modifiers[id]
    
    def get(self, id):
        total = self.base[id] if id in self.base else 0
        multiplier = 0
        
        for k, v in self.modifiers.items():
            add_val = v['add'] if 'add' in v else []
            subtotal = add_val[id] if id in add_val else 0
            total += subtotal
            
            mult_val = v['mult'] if 'mult' in v else []
            multiplier += mult_val[id] if id in mult_val else 0

        return total + (total * multiplier)


class Creature:
    skill_names = list()
    stats = Stats(base_stats_table)
    name = 'default creature'
    level = 0
    
    def make_stats(self):
        growth_fast = roll_dice(5, 3)
        growth_slow = roll_dice(1, 2)
        growth_lvl = math.log(growth_fast, 6) * self.level ** 2
        growth_lvl = round(growth_lvl)

        hp, pwr, deff, acc, spd = self.stats.base.values()
        
        hp = int(hp + self.level * 30)
        pwr = int(pwr + self.level * 5)
        deff = roll_dice(3, 2, self.level) + growth_fast
        acc = roll_dice(3, 2, self.level) + growth_slow
        spd = roll_dice(1, 2) + math.log(self.level, 10)
        
        stats = {
            'health': hp,
            'power': pwr,
            'defence': deff,
            'accuracy': acc,
            'speed': spd
        }
        
        self.stats.set_base(stats)
    
    def isalive(self):
        return (self.stats['health'] > 0) if 'health' in self.stats else False

    def levelup(self):
        pass


class Player(Creature):
    reputation = 0
    
    @property
    def level(self):
        return len([x for x in rep_tables if self.reputation >= x])
    
    def reputation_gain(self, exp):
        print('You received %d REP' % exp)
        old_lvl = self.level
        self.reputation = self.reputation + exp
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
