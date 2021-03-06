from random import random

class Combat:
    turn_number = 0
    winner = None
    
    def __init__(self, attacker, target):
        self.attacker = attacker
        self.target = target
    
    @property
    def hit_chance(self):
        a, t = [self.attacker, self.target]
        a_spd = a.stats['speed']
        a_acc = a.stats['accuracy']
        t_spd = t.stats['speed']
        t_acc = t.stats['accuracy']
        
        return 0.5 * (a_acc * 0.025) + (a_spd * 0.005) - (t_acc * 0.025) + (t_spd * 0.005)
    @property
    def initiative(self):
        return 0.5 * (self.attacker.stats['speed'] * 0.25) - (self.target.stats['speed'] * 0.25)
    
    def swap(self):
        _t = self.attacker
        self.attacker = self.target
        self.target = _t
        
    def attack(self):
        if random() >= self.hit_chance:
            a_dmg = self.attacker.stats['power']
            b_def = self.target.stats['defence']
            finaldmg = a_dmg * 0.2 - b_def
            
            if finaldmg < 0:
                finaldmg = 0
            
            self.target.stats['health'] -= finaldmg
            if self.target.stats['health'] < 0:
                self.target.stats['health'] = 0
            msg = '%s takes %d' % (self.target.name, finaldmg)
        else:
            msg = '%s misses' % self.attacker.name
        
        print(msg)
        print('[%s: %d/%d][%s: %d/%d]' % (
            self.attacker.name,
            self.attacker.stats['health'],
            self.attacker.stats['health'],
            self.target.name,
            self.target.stats['health'],
            self.target.stats['health'],
            ))
        
    def make_turn(self):
        self.attack()
        if all(x.isalive() for x in [self.attacker, self.target]):
            self.swap()
            self.turn_number += 1
            
            self.make_turn()
            
        else:
            if self.attacker.isalive():
                self.winner = self.attacker
            else:
                self.winner = self.target
                
            msg = '%s win a duel, ' % self.winner.name
            msg += 'finished in %d turns' % self.turn_number
            print(msg)