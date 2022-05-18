from telegram.ext.updater import Updater
from models import Player, Monster, combat

BOT_TOKEN = '1358072063:AAH8mkVR-ORnq9P-aDq_sMLdzgTjkHHD9mk'

if __name__ == '__main__':
    # updater = Updater(BOT_TOKEN, use_context=True)
    # dp = Updater.dispatcher
    pl = Player()
    pl.reputation_gain(600)
    en = Monster('Evil Witch', 25)
    
    combat(pl, en)
    
    #print(pl.base_stats)
    #print(en.base_stats)
    