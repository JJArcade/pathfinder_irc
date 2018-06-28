from sopel import module
from roleplay import roleplay

rp = roleplay()
@module.commands("char_info", "info", "stats")
def printChar(bot, trigger):
    out = rp.printCharInfo(trigger.group(2))
    bot.reply(out)
