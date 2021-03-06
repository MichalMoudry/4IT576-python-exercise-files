#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Modul reprezentuje správce akcí, který řídí celkové chování
v závislosti na tom, je-li hra právě aktivní a rozhoduje,
která akce dostane na starost zpracování aktuálního příkazu.
Současně obsahuje definice všech akcí.
"""

import dbg
dbg.start_mod(0, __name__)
############################################################################

#from abc import ABC, abstractmethod

from .world import current_place
from .bag import BAG, BAG_MAX_CAPACITY
from . import world
from .action import Action
from .place import ROOM_KEY_PAIRING
from .item import TALKABLE, USEABLE, TARGETABLE
from .player import progress
from .item_constants import (
    ARBITER_2, FLOOD_2, INDEX_2, LIBRARY, LIBRARY_KEY_2, SHIELD_GENERATOR_2
)
from .conversation import answers, is_conversation_happening

from .actions_constants import *
from .text_constants import *

############################################################################

def execute_command(command:str) -> str:
    """Zpracuje zadaný příkaz a vrátí odpověď hry.
    Zadaný příkaz zanalyzuje a v závislosti na aktuální aktivitě hry
    rozhodne, která akce dostane na starost jeho zpracování.
    Vrátí odpověď hry na zadaný příkaz.
   """
    global is_conversation_happening
    command = command.strip()
    if command:
        if is_alive():
            if not is_conversation_happening or (
                command == END_TALK or command == OVERVIEW
            ):
                return append_action_history(execute_cmd(command))
            elif is_conversation_happening and (
                command != END_TALK or command != OVERVIEW
            ):
                answer = answers.get(command)
                if answer == None:
                    return "Na tento dotaz objekt nemá odpověď"
                return answer
        else:
            # Hra neběží
            return ("Prvním příkazem není startovací příkaz.\n" 
                    "Hru, která neběží, lze spustit pouze "
                    "startovacím příkazem.\n")
    else:
        if is_alive():
            return append_action_history(EMPTY_COMMAND)
        else:
            _start_game()
            return append_action_history(WELCOME_MESSAGE, True)

def _start_game() -> None:
    """
    Funkce pro odstartování hry.
    """
    from . import world
    world.initialize()
    from . import player
    player.initialize()

    global used_actions
    used_actions.clear()

    global _is_alive
    _is_alive = True
    

def is_alive() -> bool:
    """Vrátí informaci o tom, je-li hra živá = aktuálně spuštěná.
    Spuštěnou hru není možno pustit znovu.
    Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
    """
    return _is_alive


def _initialize():
    """V rámci startu hry inicializuje všechny potřebné objekty.
    """
    raise Exception(f'Ještě není plně implementováno')

############################################################################

def goto(arguments:tuple[str]) -> str:
    """Přesune hráče do zadaného sousedního prostoru.
    """
    if len(arguments) < 2:
        return COMMAND_MISSING_PARAMS
    dest_name = arguments[1].lower()
    dest_place = world._current_place.name2neighbor.get(dest_name.lower())
    if dest_place:
        if dest_place.is_locked:
            return ROOM_IS_LOCKED
        world._current_place = dest_place
        return (
            f"{ROOM_MOVE} {dest_place}\n\n"
            f"{NEIGHBOURING_ROOMS_TEXT}\n{world._current_place.neighbors}"
        )
    else:
        return WRONG_NEIGHBOUR


def take(arguments:tuple[str]) -> str:
    """Přesune zadaný objekt z aktuálního prostoru do batohu.
    """
    if len(arguments) < 2:
        return COMMAND_MISSING_PARAMS
    curr_place = current_place()
    item_name = arguments[1]
    item = curr_place.item(item_name)
    if item:
        if item.weight >= BAG_MAX_CAPACITY:
            return UNMOVABLE_ITEM
        if BAG.add_item(item):
            curr_place.remove_item(item_name)
            if item_name == LIBRARY_KEY_2:
                progress[DO_YOU_HAVE_LIBRARY_KEY] = "Ano"
            return f"{ITEM_TAKE_TEXT} ({item_name})"
        else:
            return BAG_FULL
    else:
        return OBJECT_NOT_PRESENT


def put(arguments:tuple[str]) -> str:
    """Přesune zadaný objekt z batohu do aktuálního prostoru.
    """
    if len(arguments) != 2:
        return COMMAND_MISSING_PARAMS
    item_name = arguments[1]
    item = BAG.item(item_name)
    if item:
        BAG.remove_item(item.name)
        current_place().add_item(item)
        if item_name == LIBRARY_KEY_2:
            progress[DO_YOU_HAVE_LIBRARY_KEY] = "Ne"
        return f"Věc ({item.name}) byla položena"
    else:
        return ITEM_NOT_IN_BAG


def help(arguments:tuple[str]) -> str:
    """Vrátí text jednoduché nápovědy popisující
    všechny dostupné příkazy.
    """
    res = [WELCOME_MESSAGE, "\n\n"]
    res.append("Příkazy, které lze zadat:\n")
    for action in _NAME_2_ACTION.values():
        res.append(f"- {action.name}{_ACTION_ARGUMENTS[action.name]}\n")
        res.append(f"    • {action.description}\n")
    return "".join(res)

def end(arguments:tuple[str]) -> str:
    """Ukončí hru a poděkuje hráči za hru.
    """
    global _is_alive
    _is_alive = False
    return GAME_END


############################################################################

def ns0(arguments:tuple[str]) -> str:
    """
    Nestandardní akce č. 0 - Přehled.
    """
    global is_conversation_happening
    if is_conversation_happening:
        return UNABLE_TO_DISPLAY_OVERVIEW
    result = [f"{10*'-'} {OVERVIEW} {10*'-'}", "\n"]
    bag_contents = []
    for item in BAG.items:
        bag_contents.append(f"'{item.name}'")
        bag_contents.append(", ")
    bag_contents.pop()
    result.append(f"- Obsah batohu: ({''.join(bag_contents)})\n")
    result.append("----- Postup -----\n")
    for key in progress:
        result.append(f"- {key} {progress[key]}\n")
    return "".join(result)

def ns1(arguments:tuple[str]) -> str:
    """Nestandardní akce číslo 1 - Otevření.
    """
    # Chyba, když uživ nezadal druhý parametr
    if len(arguments) != 2:
        return COMMAND_MISSING_PARAMS
    place_name = arguments[1]
    place_name = place_name.lower()
    # Získání prostoru
    place = world.place(place_name)
    if place == None:
        return OPEN_WRONG_COND
    # Kontrola, jestli je potřebný klíč v batohu
    required_key_name = ROOM_KEY_PAIRING.get(place_name)
    if not required_key_name:
        return OPEN_WRONG_COND
    required_key = BAG.item(required_key_name)
    if required_key == None:
        return MISSING_KEY
    # Pokus o otevření prostoru
    if place.is_locked:
        place.is_locked = False
        # Aktualizace stavu
        if place_name == LIBRARY:
            progress[IS_LIBRARY_OPEN] = "Ano"
        return f"Místnost ({place_name}) byla otevřena"
    else:
        return OPEN_WRONG_COND


def ns2(arguments:tuple[str]) -> str:
    """Nestandardní akce číslo 1 - Použití.
    """
    if len(arguments) != 3:
        return COMMAND_MISSING_PARAMS
    item_name = arguments[1]
    target_name = arguments[2]
    global _is_alive
    item = BAG.item(item_name)
    target = current_place().item(target_name)
    if item_name not in USEABLE:
        if handle_scenario_mistake(item_name, target_name):
            _is_alive = False
        return UNUSEABLE_ITEM
    elif target_name not in TARGETABLE:
        return WRONG_ITEM_TARGET
    elif item == None or target == None:
        return WRONG_ARGUMENT
    elif item_name == SHIELD_GENERATOR_2 and target_name != ME:
        return WRONG_ITEM_TARGET
    if item_name == INDEX_2 and target_name == ARBITER_2:
        _is_alive = False
    return f"Předmět ({item_name}) byl použit na {target_name}"


def ns3(arguments:tuple[str]) -> str:
    """Nestandardní akce číslo 1 - Oslovení.
    """
    if len(arguments) != 2:
        return COMMAND_MISSING_PARAMS
    target = arguments[1]
    item = current_place().item(target)
    global is_conversation_happening
    if is_conversation_happening:
        return "Už probíhá rozhovor"
    if not item:
        return "Tato osoba není v prostoru"
    if target not in TALKABLE:
        return "Tuto věc/postavu nelze oslovit"
    is_conversation_happening = True
    return (
        f"Pokoušíte se zeptat objektu {target}. Jaký je váš dotaz?"
    )


def ns4(arguments:tuple[str]) -> str:
    """Nestandardní akce číslo 1 - Ukončení rozhovoru.
    """
    global is_conversation_happening
    if not is_conversation_happening:
        return "V tuto chvíli neprobíhá rozhovor"
    is_conversation_happening = False
    return END_TALK_TEXT

############################################################################
# Vlastní funkce

def handle_scenario_mistake(item_name: str, target_name: str) -> bool:
    """
    Funkce pro zachycení chyby ve scénáři MISTAKES_NS.
    """
    if item_name == FLOOD_2 and target_name == ME:
        return True
    else:
        return False

def execute_cmd(command:str) -> str:
    """
    Funkce pro vykonání příkazu, přičemž vrací vhodnou odpověď.
    """
    command_parts = command.split()
    action_name = command_parts[0].lower()
    if action_name in _NAME_2_ACTION:
        add_action_to_history(action_name)
        return _NAME_2_ACTION[action_name]._execute(command_parts)
    else:
        return UNKNOWN_COMMAND

def add_action_to_history(action:str) -> None:
    """
    Funkce, která přidá akci do seznamu historie akcí.
    """
    global used_actions
    if not(action in used_actions):
        used_actions.append(action)
        used_actions.sort()

def get_action_history_as_string(is_first_step:bool = False) -> str:
    """
    Funkce, která vrátí historii akcí jako vhodný string.
    """
    global used_actions
    res = ["["]
    for action in used_actions:
        res.append(f"'{action}'")
        res.append(", ")
    if not is_first_step:
        res.pop()
    res.append("]")
    return "".join(res)

def append_action_history(string:str, is_first_step:bool = False) -> str:
    """
    Funkce, která vrátí původní vstup a k němu připnutou historii akcí.
    """
    res = [f"{string}\n\n", "§Doposud zadáno: "]
    res.append(get_action_history_as_string(is_first_step))
    return "".join(res)

############################################################################
_is_alive = False

_NAME_2_ACTION = {
    MOVE : Action(MOVE, "Přesune hráče do specifikovaného prostoru", goto),
    PICK_UP : Action(PICK_UP, "Přidá určený předmět do batohu", take),
    OVERVIEW : Action(
        OVERVIEW, "Zobrazí přehled hráče a jeho průběhu", ns0
    ),
    OPEN : Action(
        OPEN,
        "Tento příkaz se pokusí o otevření předmětu nebo místnosti",
        ns1
    ),
    PUT_DOWN : Action(PUT_DOWN, "Položí předmět", put),
    USE : Action(USE, "Použije zadanou věc na určený cíl", ns2),
    HELP : Action(HELP, "Příkaz pro vyvolání nápovědy", help),
    TALK : Action(TALK, "Pokusí se o oslovení objektu v místnosti", ns3),
    END_TALK : Action(
        END_TALK, "Příkaz pro ukončení rozhovoru, pokud nějaký probíhá", ns4
    ),
    END : Action(END, "Tento příkaz ukončí hru", end),
}

_ACTION_ARGUMENTS = {
    MOVE : " [místo]",
    PICK_UP : " [věc]",
    OVERVIEW : "",
    OPEN : " [místnost]",
    PUT_DOWN : " [věc]",
    USE : " [věc] [cíl]",
    HELP : "",
    TALK : " [osoba]",
    END_TALK : "",
    END : "",
}

used_actions:list[str] = []

############################################################################
dbg.stop_mod(0, __name__)
