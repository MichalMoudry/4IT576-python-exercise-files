#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Balíček s poloprázdnými moduly tvořícími zárodek aplikace¤
a definujícími její základní architekturu a API.
Moduly obsahují všechny atributy definované v odpovídajících protokolech.

Oproti minulé verzi přibylo:
- Poloprázdné moduly definující základní architekturu a API.
"""
import dbg; dbg.start_pkg(0, __name__, __doc__)
############################################################################

# Následující moduly je třeba importovat až při spuštění kontroly typů
# from ..api.scenario import Scenario
# from ..api.interfaces import IGame


############################################################################

# Login autora/autorky programu zadaný VELKÝMI PÍSMENY
AUTHOR_ID = 'MOUM02'

# Jméno autora/autorky programu ve formátu PŘÍJMENÍ Křestní,
# tj. nejprve příjmení psané velkými písmeny a za ním křestní jméno,
# u nějž bude velké pouze první písmeno a ostatní písmena budou malá.
# Má-li autor programu více křestních jmen, může je uvést všechna.
AUTHOR_NAME = 'MOUDRÝ Michal'

# Jméno autora/autorky programu ve formátu PŘÍJMENÍ Křestní
# zapsané v jeho/jejím rodném jazyce
AUTHOR_ORIG_NAME = 'MOUDRÝ Michal'


# Zdroje, z nichž autor(ka) čerpal(a) při řešení úkolu
SOURCES = """\
-
"""

# Problémy, které se vyskytly při zpracování probrané látky a řešení DU
PROBLEMS = """\
Žádné
"""

# Poznámky a připomínky k výkladu
COMMENTS = """\
Žádné
"""



###########################################################################q

def all_scenarios() -> tuple['Scenario']:
    """Vrátí správně seřazenou n-tici definovaných scénářů.
    """
    from   .  import scenarios
    result = scenarios.SCENARIOS
    return result


def game() -> 'IGame':
    """Vrátí odkaz na objekt reprezentující hru.
    Tímto objektem je modul definující komunikační funkce hry
    """
    from . import main
    return main



############################################################################

def self_test():
    """Otestuje aktuální stav projektu.
    """
    from importlib  import import_module
    me = import_module(__package__)
    from ..tests    import test
    from ..tests    import Level
    #test(me, Level.MISTAKES)
    #test(me, Level.WHOLE)
    test(me, Level.z01)
        # architektury, tj. deklaraci navržených modulů a jejich atributů

# Test spustíte zadáním příkazů
# import game.a1c_architecture as at; at.self_test()



###########################################################################q
dbg.stop_mod(0, __name__)
