import random

# creating deck of cards and shuffling it
card_categories = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
card_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

def start_game(player_list: list, dealt_cards: dict):
    # shuffles the deck
    deck = [(card, category) for category in card_categories for card in card_list]
    random.shuffle(deck)

    # while loop to get all players
    add_player = True
    while add_player:
        name = input('Enter your name: ')
        player_list.append(name)
        
        answer = input('\nIs there another player (y/n): ')
        if answer.lower().startswith('y'):
            print()
            continue
        else:
            add_player = False
    print(f'\nNumber of players: {len(player_list)}\n')

    # sets the initial deal to everyone
    for player in player_list:
        dealt_cards[player] = []
    dealt_cards['Dealer'] = []
    for i in range(2):
        for person in dealt_cards:
            dealt_cards[person].append(deck.pop(0))
    
    return player_list, dealt_cards, deck

# revealing deals
def display_deal(dealt_cards: dict, player, reveal=False):
    if player != 'Dealer':
        for card in dealt_cards[player]:
            print(card)
    else:
        if reveal:
            print('\nDealer\'s cards are: ')
            for card in dealt_cards['Dealer']:
                print(card)
        else:
            print(f"Dealer's cards:\n{dealt_cards['Dealer'][0]}\nUnknown")

# deals extra card
def extra_deal(dealt_cards: dict, player, deck: list):
    dealt_cards[player].append(deck.pop(0))

# get total value of deal
def get_total(dealt_cards: dict, player):
    card_list = [card[0] for card in dealt_cards[player]]
    # ace moved to last to better sum total of deal and determine soft value
    if 'A' in card_list:
        card_list.append(card_list.pop(card_list.index('A')))
    total = 0
    for card in card_list:
        # A = 1 or 11
        if card == 'A':
            # for dealers if an 11 Ace gets them a bust deal, then Ace becomes 1
            if player == 'Dealer' and total + 11 > 21:
                total += 1
            elif player == 'Dealer' and 17 <= total + 11 <= 21:
                total += 11
            # ace will always be 11 unless the total value is over 21,
            # then treated as 1
            elif player != 'Dealer' and total + 11 > 21:
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
def dealer_turn(dealt_cards:dict, deck:list):
    while True:
        display_deal(dealt_cards,'Dealer', reveal=True)
        if get_total(dealt_cards, 'Dealer') < 17:
            extra_deal(dealt_cards, 'Dealer', deck)
        elif 17<= get_total(dealt_cards, 'Dealer') <= 21:
            break
        else:
            break

# shows the results of the cards dealt to each person
def get_result(player_list: list, dealt_cards:dict):
    for player in player_list:
        if get_total(dealt_cards, player) > 21:
            continue
        elif get_total(dealt_cards, player) < 21 and get_total(dealt_cards, 'Dealer') > 21:
            print(f'\n{player}, you won! The dealer dealt a bust.')
        elif get_total(dealt_cards, player) > get_total(dealt_cards, 'Dealer'):
            print(f'\n{player}, you won! You dealt higher than the dealer.')
        elif get_total(dealt_cards, player) == get_total(dealt_cards, 'Dealer'):
            print(f'\n{player}, you drawed with the dealer.')
        elif get_total(dealt_cards, player) < get_total(dealt_cards, 'Dealer'):
            print(f'\n{player}, you lose. You dealt lower than the dealer')
        
        print(f'Your deal total: {get_total(dealt_cards, player)}')
        print(f'Dealer\'s deal total: {get_total(dealt_cards, "Dealer")}')