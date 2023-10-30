import random

# creating deck of cards and shuffling it
card_categories = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
card_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

def start_game():
    # shuffles the deck
    deck = [(card, category) for category in card_categories for card in card_list]
    random.shuffle(deck)

    # while loop to get all players
    sign_up_list = []
    add_player = True

    while add_player:
        name = input('Enter your name: ')
        sign_up_list.append(name)
        
        answer = input('\nIs there another player (y/n)? ')
        if answer.lower().startswith('y'):
            print()
            continue
        else:
            add_player = False
    print(f'\nNumber of players: {len(sign_up_list)}')


    # creating dict objects for each player
    players = []
    for player in sign_up_list:
            players.append(
                {
                    "Name": player,
                    "Hand": [],
                    "Hand2": [],
                    "Natural": False,
                    "Insurance": False,
                    "Split": False,
                    "DoubleDown": False,
                    "Surrender": False
                }
            )
    
    # creating a dealer object
    players.append(
        {
            "Name": "Dealer",
            "Hand": [],
            "Natural": False
        }
    )
    
    # dealing two cards to each player and dealer
    for i in range(2):
        for person in players:
            person["Hand"].append(deck.pop(0))
    
    return players, deck

# checks dealer's up card for possible insurance or natural blackjack
def check_face_up(player):
    if player["Hand"][0][0] == "A":
        return "A"
    elif player["Hand"][0][0] in ['10', 'J', 'Q', 'K']:
        return "ten-card"
    else:
        return False

# checks if the current player is a dealer
def isDealer(player):
    if player["Name"] == 'Dealer':
        return True
    else:
        return False

# revealing deals
def display_hand(player, reveal=False):
    if not isDealer(player):
        for card in player['Hand']:
            print(card)
    else:
        if reveal:
            print('\nDealer\'s cards are: ')
            for card in player['Hand']:
                print(card)
        else:
            print(f"\nDealer's cards:\n{player['Hand'][0]}\nUnknown")

# deals extra card
def hit(player, deck: list):
    player["Hand"].append(deck.pop(0))

# get total value of deal
def get_total(player):
    card_list = [card[0] for card in player["Hand"]]
    # ace moved to last to better sum total of deal and determine soft value
    if 'A' in card_list:
        card_list.append(card_list.pop(card_list.index('A')))
    total = 0
    for card in card_list:
        # A = 1 or 11
        if card == 'A':
            # for dealers if an 11 Ace gets them a bust deal, then Ace becomes 1
            if isDealer(player) and total + 11 > 21:
                total += 1
            elif isDealer(player) and 17 <= total + 11 <= 21:
                total += 11
            # ace will always be 11 unless the total value is over 21,
            # then treated as 1
            elif not isDealer(player) and total + 11 > 21:
                total += 1
            else:
                total+= 11
        # 2-9
        elif '2' <= card <= '9':
            total += int(card)
        # 10-K
        else:
            total += 10 
    return total

# dealer takes his turn
def dealer_turn(dealer, deck:list):
    if dealer["Natural"]:
        return
    else:
        while True:
            if get_total(dealer) < 17:
                hit(dealer, deck)
            elif 17<= get_total(dealer) <= 21:
                if get_total(dealer) == 21:
                    print('\nDealer drew a blackjack!')
                    break
                else:
                    break
            else:
                break
        display_hand(dealer, reveal=True)

# shows the results of the cards dealt to each person
def get_result(players):
    for player in players:
        if isDealer(player):
            break
        elif player["Surrender"]:
            print(f'{player["Name"]} surrendered.')
        # if the current player already lost by drawing a bust
        elif get_total(player) > 21:
            continue
        # if the dealer has a natural blackjack
        elif players[-1]["Natural"]:
            continue
        # if dealer doesn't have natural blackjack
        elif not players[-1]["Natural"]:
            # rewards player if they have a natural blackjack
            if player["Natural"]:
                continue
            # compares results of player's hand vs dealer's hand
            else:
                if get_total(players[-1]) > 21:
                    print(f'\n{player["Name"]}, you won! The dealer dealt a bust.')
                elif get_total(player) > get_total(players[-1]):
                    print(f'\n{player["Name"]}, you won! You dealt higher than the dealer.')
                elif get_total(player) == get_total(players[-1]):
                    print(f'\n{player["Name"]}, you drawed with the dealer.')
                elif get_total(player) < get_total(players[-1]):
                    print(f'\n{player["Name"]}, you lose. You dealt lower than the dealer')
        
                print(f'Your deal total: {get_total(player)}')
                print(f'Dealer\'s deal total: {get_total(players[-1])}')
