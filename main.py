from dotenv import dotenv_values
from telegram.ext.updater import Updater
from models import Player, Monster, Stats


config = dotenv_values()
BOT_TOKEN = config['BOT_TOKEN']

if __name__ == '__main__':
    # updater = Updater(BOT_TOKEN, use_context=True)
    # dp = Updater.dispatcher
    
    p1 = Player()
    p1.reputation_gain(21200)
    print(p1.stats.base)
    
    #print(pl.base_stats)
    #print(en.base_stats)
    