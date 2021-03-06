"""
Konstanty pro textové výstupy aplikace.
"""

# Konstanty pro textové výstupy aplikace
UNKNOWN_COMMAND = "Neznámý příkaz"
AVAILABLE_COMMANDS = ("Příkazy, které lze zadat:\n"
"- jdi [místo]\n"
"    • Přesune hráče do specifikovaného prostoru\n"
"- zvedni [věc]\n"
"    • Přidá určený předmět do batohu\n"
"- přehled\n"
"    • Zobrazí přehled hráče a jeho průběhu\n"
"- otevři [místnost]\n"
"    • Tento příkaz se pokusí o otevření předmětu nebo místnosti\n"
"- polož [věc]\n"
"    • Položí předmět\n"
"- použij [věc] [cíl]\n"
"    • Použije zadanou věc na určený cíl\n"
"- ?\n"
"    • Příkaz pro vyvolání nápovědy\n"
"- oslov [osoba]\n"
"    • Pokusí se o oslovení objektu v místnosti\n"
"- ukončit_rozhovor\n"
"    • Příkaz pro ukončení rozhovoru, pokud nějaký probíhá\n"
"- konec\n"
"    • Tento příkaz ukončí hru\n")
WELCOME_MESSAGE = (
"Vítejte ve hře Halo, kdy vaším cílem je se dostat "
"do místnosti 'The Maw',\npřičemž pro úspěšné dokončení hry je "
"třeba donést tzv. Index a \npoužít ho na postavu Arbiter, kdy Index se "
"nachází v zamčené knihovně,\ntedy je třeba knihovnu odemknout a sebrat"
" Index do batohu.\n\nPro zobrazení nápovědy je třeba zadat příkaz: ?."
)
END_TALK_TEXT = "Rozhovor byl úspěšně ukončen."
ITEM_TAKE_TEXT = "Předmět byl zvednut"
GAME_END = "Hra byla ukončena"
ROOM_MOVE = "Proběhl přesun na:"
NEIGHBOURING_ROOMS_TEXT = "Sousední místnosti:"

## Errors
EMPTY_COMMAND = "Prázdný příkaz"
WRONG_NEIGHBOUR = "Zadané místo není sousedem"
OBJECT_NOT_PRESENT = "Objekt není v této místnosti"
WRONG_START_TEXT = ("Prvním příkazem není startovací příkaz.\n"
"Hru, která neběží, lze spustit pouze startovacím příkazem.\n")
COMMAND_MISSING_PARAMS = "Příkazu chybí požadované parametry"
WRONG_ARGUMENT = "Špatný argument parametru"
ITEM_NOT_IN_BAG = "Předmět není v batohu"
BAG_FULL = "Váš batoh je plný"
WRONG_ITEM_TARGET = "Špatný cíl použití věci"
UNUSEABLE_ITEM = "Tuto věc nelze použít"
OPEN_WRONG_COND = "Tato místnost není zavřená nebo ani neexistuje"
ROOM_IS_LOCKED = "Místnost je zamčená"
MISSING_KEY = "Nemáte potřebný klíč v batohu"
UNMOVABLE_ITEM = "Předmět nelze zvednout"
END_TALK_WRONG_COND = "V tuto chvíli neprobíhá rozhovor"
UNABLE_TO_DISPLAY_OVERVIEW = "V tuto chvíli nelze zobrazit přehled"