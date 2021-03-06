#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Zadání domácího úkolu, v němž má student(ka) demonstrovat zvládnutí
doposud probrané látky prostřednictvím realizace hry Prší.
"""
import dbg; dbg.start_mod(1, __name__)
import random
###########################################################################q
# Identifikační a informační konstanty

# Login autora/autorky programu zadaný VELKÝMI PÍSMENY
AUTHOR_ID = 'MOUM02'

# Jméno autora/autorky programu ve formátu PŘÍJMENÍ Křestní
AUTHOR_NAME = 'MOUDRÝ Michal'

# Zdroje, z nichž autor(ka) čerpal(a) při řešení úkolu
SOURCES = """\
Prezentace - Wikipedia (pro pravidla hry Prší)
"""

# Problémy, které se vyskytly při zpracování probrané látky a řešení DU
PROBLEMS = """\
Žádné
"""

# Poznámky a připomínky k výkladu
COMMENTS = """\
Některé požadavky na funkce nedávají smysl (např. požadavek č. 4 u funkce
prepare(), kdy nemá smysl pracovat s nějakým "mezibalíkem", když můžu od
začátku pracovat se zamýchaným TALON, kdy v realitě potom co rozdám karty
a jednu dám na vršek (do té FACE_UP), a pak jednou kartou za druhou
nebudu plnit lízací balík na stole, ale prostě ho tam položím, tedy
metoda prepare() vyžaduje práci s balíčkem, který v reálném světě
neexistuje).
"""


###########################################################################q
# Konstanty

# Barvy karet
COLOR  = ('♠', '♣', '♥', '♦')
COLORS = len(COLOR)     # Pro testování lze hodnotu nastavit od 2 do 4

# Velikosti karet
VALUE  = ('7', '8', '9', 'X', 'J', 'Q', 'K', 'A')
VALUES = len(VALUE)     # Pro testování lze hodnotu nastavit od 2 do 8

# Počet rozdávaných karel
TO_DEAL = 4             # Pro testování lze hodnotu nastavit

# Balíček karet určených k "lízání" seřazených tak, že karta,
# která se má lízat, je vždy uvedena jako poslední (tj. je na konci seznamu).
TALON:list[str] = []

# Balíček odložených karet seřazených tak, že naposledy odložená karta
# je vždy uvedena jako poslední (tj. je na konci seznamu).
FACE_UP:list[str] = []

# Karty, které má v ruce hráč
USER:list[str] = []

# Karty, které má v ruce počítač
COMP:list[str] = []


###########################################################################q
# Abecedně seřazené pomocné proměnné

required_color:str = ""

###########################################################################q

###########################################################################q
# Abecedně seřazené pomocné funkce

def comp_turn_response(card: str) -> None:
    """
    Funkce pro zachycení situace, kdy počítač položí kartu na stůl.
    """
    print(f"\nPočítač dal {card}"+ 
    " na odkládací balíček")
    change_cards_deck(card, COMP, FACE_UP)
    handle_special_card(card, False, USER)

def compare_cards(card1: str, card2: str) -> bool:
    """
    Funkce pro porovnání, zda jsou karty mezi sebou kompatibilní.
    """
    if card1[0] in card2:
        return True
    elif card1[1] == required_color:
        return True
    else:
        return False

def fill_talon_deck(deck: list[str]) -> None:
    """
    Funkce pro naplnění lízacího balíčku.
    """
    for card in deck:
        TALON.append(card)

def get_available_colors(colors: int) -> list[str]:
    """
    Funkce pro získání povolených barev ve hře.
    """
    colors_list: list[str] = []
    for index, color in enumerate(COLOR):
        if index + 1 <= colors:
            colors_list.append(color)
    return colors_list

def get_available_values(value: int) -> list[str]:
    """
    Funkce pro získání povolených hodnot ve hře.
    """
    values_list: list[str] = []
    for index, val in enumerate(VALUE):
        if index + 1 <= value:
            values_list.append(val)
    return values_list

def get_face_up_last_card() -> str:
    """
    Funkce pro získání poslední karty z balíčku FACE_UP.
    """
    return FACE_UP[len(FACE_UP) - 1]

def get_random_card_from_deck(deck: list[str]) -> str:
    """
    Funkce, která vrátí náhodnou kartu z talónu.
    """
    card = deck[random.randint(0, len(deck) - 1)]
    return card

def get_turn_result() -> int:
    """
    Funkce pro získání výsledku kola hry Prší.
    """
    if len(USER) == 0:
        return -1
    elif len(COMP) == 0:
        return 1
    else:
        return 0

def handle_draw_two_action(card: str, is_user: bool,
opponent: list[str]) -> None:
    """
    Funkce pro realizaci akce na základě hrané sedmičky.
    """
    handle_empty_talon()
    if len(TALON) > 0:
        for draw in range(2):
            card = get_random_card_from_deck(TALON)
            change_cards_deck(card, TALON, opponent)
        if is_user:
            print("\nPočítač si lízl 2 karty")
        else:
            print("\nDostali jste dvě karty")

def handle_empty_talon() -> None:
    """
    Funkce pro vyřešení situace, kdy lízací balíček je prázdný
    """
    if len(TALON) == 0:
        last_card = get_face_up_last_card()
        face_up_length = len(FACE_UP) - 1
        for index, card in enumerate(FACE_UP):
            if index != face_up_length:
                TALON.append(card)
        FACE_UP.clear()
        FACE_UP.append(last_card)
        deck = shuffle_deck(TALON)
        TALON.clear()
        fill_talon_deck(deck)

def handle_special_card(card: str, is_user: bool,
opponent: list[str]) -> None:
    """
    Funkce pro zajištění speciálních efektů u karet.
    """
    if "7" in card:
        handle_draw_two_action(card, is_user, opponent)
    elif "A" in card:
        if is_user:
            print("\nPočítač vynechává kolo")
        else:
            print("\nVynecháváte kolo")
    # Změna hrané barvy.
    elif "Q" in card:
        if is_user:
            change_color_by_user()
        else:
            change_color_by_comp()
        print(f"\nZměna barvy na {required_color}")

def handle_card_draw(user_decision: int, computer_decision: int,
is_user_skipped: bool = False) -> None:
    """
    Funkce pro zachycení, zda si chce nějaká strana líznout kartu.
    """
    handle_empty_talon()
    card = ""
    if user_decision == -1 and len(TALON) > 0 and not(is_user_skipped):
        card = get_random_card_from_deck(TALON)
        print(f"\nDostali jste {card} do vaší ruky")
        change_cards_deck(card, TALON, USER)
    if computer_decision == -1 and len(TALON) > 0:
        card = get_random_card_from_deck(TALON)
        print("\nPočítač si lízl kartu z balíčku")
        change_cards_deck(card, TALON, COMP)

def handle_user_input(inpt: str) -> int:
    """
    Funkce pro zvládnutí vstupu uživatele.

    Vstup musí být číslo.
    """
    if inpt == "":
        return -1
    if inpt == "k":
        return -2
    elif inpt == "?":
        print_guide()
        return -5
    elif int(inpt) in range(1, len(USER) + 1):
        return int(inpt) - 1
    else:
        return -1

def change_cards_deck(card: str, orig: list[str],
destination: list[str]) -> None:
    """
    Funkce pro přesunutí karty z balíčku do libovolné destinace.
    """
    orig.remove(card)
    destination.append(card)
    if destination == FACE_UP:
        global required_color; required_color = card[1]

def change_color_by_user():
    """
    Funkce pro změnu požadované barvy ze strany uživatele.
    """
    is_color_selection = True
    while is_color_selection:
        try:
            print("Dostupné barvy:", COLOR)
            color_index = input("Vyberte novou barvu (1 - 4): ")
            color_index = int(color_index) - 1
            global required_color; required_color = COLOR[color_index]
            is_color_selection = False
        except:
            print("-- Zadejte správný vstup! --")

def change_color_by_comp():
    """
    Funkce pro změnu barvy ze strany počítače.
    """
    # Získat náhodnou barvu.
    color = COLOR[random.randint(0, len(COLOR) - 1)]
    global required_color; required_color = color

def initial_hand_fill(deck: list[str], to: list[str],
to_deal: int = TO_DEAL) -> None:
    """
    Funkce pro rozdání karet určité straně.
    """
    card = ""
    deck_length = len(deck)
    for i in range(to_deal):
        card = deck[deck_length - (i + 1)]
        change_cards_deck(card, deck, to)

def initial_deck_fill(deck: list[str], colors: list[str] = COLOR,
values: list[str] = VALUE) -> list[str]:
    """
    Funkce pro prvotní naplnění losovacího balíčku
    """
    for color in colors:
        for number in values:
            deck.append(f"{number}{color}")
    deck = shuffle_deck(deck)
    return deck

def shuffle_deck(deck: list[str]) -> list[str]:
    """
    Funkce pro zamýchání balíčku.
    """
    new_deck:list[str] = []
    while len(deck) > 0:
        random_card = get_random_card_from_deck(deck)
        change_cards_deck(random_card, deck, new_deck)
    return new_deck

def print_guide():
    """
    Funkce pro vypsání nápovědy uživateli.
    """
    print("")
    print("")
    print(50*"-", "Pravidla hry prší", 50*"-")
    print(f"- Každý hráč dostane do ruky {TO_DEAL} karet")
    print("- Kolo zahajuje vždy uživatel, a ne počítač")
    print("- Na odhazovací balíček se smí odhodit karta" +
    ", která má buď stejnou hodnotu anebo barvu, jako vrchní lícová karta")
    print("- Vítězem se stává hráč, který se zbaví všech karet")
    print("\n---- Speciální karty ----")
    print("- Pokud hráč zahraje sedmičku, následující hráč si" +
    " musí líznout dvě karty")
    print("\t- Sedmičku nelze přebíjet")
    print("- Pokud hráč zahraje eso, následující hráč nehraje")
    print("- Kartu svršek lze hrát na kartu libovolné barvy," +
    " vyjma sedmy či esa odehraného předcházejícím hráčem.") 
    print("\t- Pokud je tato karta odehrána, musí hráč, který" + 
    " svrška odehraje, zvolit barvu.")
    print(119*"-")

def print_state(prolog:str='nezadáno', level:int=1) -> None:
    """Pomocná funkce pro ladění, která vytiskne zadanou úvodní hlášku
    s prologem charakterizujícím místo, odkud byla zavolána,
    a za ní vytiskne přehled o stavu hry, tj. jednotlivé sady karet.
    """
    dbg.prDB(level,
       f'===== Stav hry {prolog}\n'
       f'   Uživatel {USER}\n'
       f'   Počítač  {COMP}\n'
       f'   Balík    {FACE_UP}\n'
       f'   Talón    {TALON}\n'
       f'{60*"-"}' )

def print_user_turn_info() -> None:
    """
    Funkce pro vypsání začátečních informací na začátku uživatelova
    tahu.
    """
    print(f"\n\nVaše karty: {USER}")
    print(60*"-")
    print(f"Počet karet počítače: {len(COMP)}")
    print(f"Odkládací balíček: ['{get_face_up_last_card()}'] " +
    f"(požadovaná barva: {required_color})")
    print(60*"-")
    print("Možnosti:")
    print(f"- Zahrát kartu (1 - {len(USER)})")
    print("- Líznout si kartu (0)")
    print("- Nápověda (?)")
    print("- Konec (k)")

def print_game_result(result: int) -> None:
    """
    Funkce pro vypsání výsledku hry.
    """
    if result == -1:
        print("Gratulujeme! Vyhráli jste hru.")
    else:
        print("Bohužel jste prohráli hru.")

def user_turn_response(card: str) -> None:
    """
    Funkce pro zachycení situace, kdy uživatel položil kartu na stůl.
    """
    change_cards_deck(card, USER, FACE_UP)
    print(f"\nZahráli jste {card}")
    handle_special_card(card, True, COMP)

###########################################################################q
# Požadované funkce

def prepare(colors:list[str] = COLOR, value:list[str] = VALUE,
to_deal: int = TO_DEAL) -> None:
    """Připraví karty pro další hru, tj.
    1. Připraví zamíchanou sadu (seznam) karet se zadaným počtem barev
       a zadaným počtem hodnot. Karty budou reprezentovány dvouznakovými
       stringy, v nichž bude prvním znakem některá z hodnot v konstantě
       VALUE a druhým znakem některý z obrazců v konstantě COLOR.
       Počet barev, počet hodnot a počet rozdávaných karet je zadán
       v konstantách COLORS, VALUES a TO_DEAL.
       Pro účely testování můžete jejich hodnoty snížit.
       Je-li požadovaných barev (COLORS) nebo hodnot (VALUES) méně,
       než je dálka příslušné n-tice, tak se přebírají od počátku
       seznamů COLOR a VALUE.
    2. Z konce tohoto seznamu rozdá počet karet zadaný konstantou TO_DEAL
       nejprve hráči a pak počítači.
    2. Přesune ze seznamu poslední kartu jako základ odkládacího balíku
       FACE_UP.
    4. Zbytkem seznamu naplní seznam TALON.
    """
    deck:list[str] = []
    deck = initial_deck_fill(deck, colors, value)
    initial_hand_fill(deck, USER, to_deal)
    initial_hand_fill(deck, COMP, to_deal)
    face_up_card = deck[len(deck) - 1]
    change_cards_deck(face_up_card, deck, FACE_UP)
    fill_talon_deck(deck)


def comp_turn() -> int:
    """Realizuje další tah počítače.
    Má-li počítač "v ruce" kartu se stejnou hodnotou či barvou,
    vrátí vrátí její index ve svém seznamu, aby ji bylo možné použít.
    Nemá-li takovou, vrátí -1, aby mu byla přidána karta z talónu.
    """
    index = 0
    face_up_last_card = get_face_up_last_card()
    selected_index = -1
    while index < len(COMP):
        if compare_cards(COMP[index], face_up_last_card):
            selected_index = index
            break
        index += 1
    return selected_index


def user_turn() -> int:
    """Realizuje komunikaci s uživatelem, který si má vybrat,
    zda některou ze svých karet odhodí, anebo si lízne další.
    Vrátí index uživatelovi karty, pokud se ji rozhodl odložit,
    anebo vrátí -1, pokud se uživatel rozhodl líznout další kartu.
    Při vybrání odkládané karty je třeba po návratu zkontrolovat,
    zda její hodnota či barva odpovídá kartě na balíčku.
    """
    print_user_turn_info()
    res = handle_user_input(input("Zadejte vaše rozhodnutí: "))
    print("")
    return res


def turn() -> int:
    """Nechá táhnout nejprve uživatele a poté počítač.
    Podle jejich odpovědi upraví příslušně obsah jednotlivých seznamů.
    Zůstanou-li hráčům v ruce karty, vrátí 0.
    Vyhraje-li uživatel, vrátí -1, vyhraje-li počítač, vrátí +1.
    """
    is_user_turn = True
    card = ""
    while is_user_turn:
        usr_turn = user_turn()
        # Normální tah.
        if usr_turn >= 0:
            face_up_last_card = get_face_up_last_card()
            card = USER[usr_turn]
            if compare_cards(card, face_up_last_card):
                user_turn_response(card)
                if card[0] == "7":
                    return get_turn_result()
                elif card[0] == "A":
                    return get_turn_result()
                is_user_turn = False
            else:
                print("\n--- Nehodná karta zvolena! ---")
        # Pokud uživatel chce ukončit hru.
        elif usr_turn == -1:
            is_user_turn = False
        elif usr_turn == -2:
            return 1
    computer_turn = comp_turn()
    card = COMP[computer_turn]
    if computer_turn != -1:
        comp_turn_response(card)
    handle_card_draw(usr_turn, computer_turn, (card[0] == "7" or card[0] == "A"))
    return get_turn_result()


def play(colors:int=4, value:int=8, to_deal:int=4) -> None:
    """Realizuje zjednodušenou verzi hry Prší se zadaným okrajovými
    podmínkami, tj. s kartami se zadaným počtem barev a hodnot a
    se zadaným počtem karet, které se mají na počátku každému hráči
    rozdat.
    """
    if (colors <= len(COLOR) and colors > 0
    ) and value <= len(VALUE) and value > 0:
        available_colors: list[str] = get_available_colors(colors)
        available_values: list[str] = get_available_values(value)
        prepare(available_colors, available_values, to_deal)
        game_progress = 0
        while game_progress == 0:
            game_progress = turn()
        print_game_result(game_progress)



###########################################################################q
# Testy

def test_prepare() -> None:
    """Prověrka definice funkce prepare()."""
    prepare()
    print_state("test_prepare()")
    face_up_res = True if len(FACE_UP) == 1 else False
    print("Test odkládacího balíčku:", f"{face_up_res}",
    f"\n\tVelikost odkládacího balíčku: {len(FACE_UP)} (očekáváno: 1)")
    user_hand_test = True if len(USER) == TO_DEAL else False
    print("Ruka uživatele test:", f"{user_hand_test}",
    f"\n\tDélka balíčku uživatele: {len(USER)} (očekáváno: {TO_DEAL})")
    computer_hand_test = True if len(COMP) == TO_DEAL else False
    print("Test ruky počítače:", f"{computer_hand_test}",
    f"\n\tDélka balíčku počítače: {len(COMP)} (očekáváno: {TO_DEAL})")
    deck_length = len(TALON) + len(FACE_UP)+ len(USER) + len(COMP)
    talon_test = True if deck_length == (VALUES * COLORS) else False
    print(f"Test lízacího balíčku: {talon_test}",
    f"\n\tDélka balíčku: {deck_length} (očekáváno: {VALUES * COLORS})")


def test_turn() -> None:
    """Prověrka kódu pro realizaci jednoho kola hry funkcí turn().
    """
    import builtins as b
    b_input = b.input
    b.input = dbg.input
    dbg.INPUTS = ('1', '0')
    dbg.TST = 1
    random.seed(42)
    dbg.TST = 1
    prepare()
    print(f"Výsledek kola: {turn()} (očekáváno: 0)")
    print_state("test_turn()")
    print("Je J♥ v odkládacím balíčku?", True if "J♥" in FACE_UP else False,
    "(očekáváno: True)")
    print("Bylo J♥ odebráno z ruky hráče?",
    True if not("J♥" in USER) else False, "(očekáváno: True)")
    user_orig_length = len(USER)
    talon_orig_length = len(TALON)
    turn()
    user_modified_length = len(USER)
    talon_modified_length = len(TALON)
    print(talon_orig_length, talon_modified_length)
    print(user_orig_length, user_modified_length)
    print("Nebyla přidána karta do balíčku uživatele?",
    True if user_orig_length == user_modified_length else False)
    b.input = b_input
    dbg.TST = 0


def test_play() -> None:
    """Prověrka funkce play() řešící odehrání hry.
    """
    import builtins as b
    b_input = b.input
    b.input = dbg.input
    dbg.INPUTS = ('1', '0', '2', '3', '1', '0', '2', '3', '1', '0',
    '2', '3', '1', '0', '52', '3', '1', '0', '4', '3', '1', '0', '2',
    '3', '4', '0', '2', '3', '1', '0', '2', '3', '1', '0', '2', '3',
    '1', '0', '2', '3', '1', '0', '2', '3', '1', '0', '2', '3', '1',
    '1', '1', '0', '')
    dbg.TST = 1
    random.seed(50)
    dbg.TST = 1
    play()
    b.input = b_input
    dbg.TST = 0


###########################################################################q
dbg.stop_mod(1, __name__)
