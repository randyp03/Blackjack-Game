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
                    "Natural2": False,
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

# creates list to iterate through each hand if player chose to split
def split_creation(player):
    if player["Split"]:
        both_hands = [{"Which Hand": k, "Hand": player[k]} for k in player if k == "Hand" or k == "Hand2"]
        return both_hands
    else:
        return

# deals extra card
def hit(player_hand, deck: list):
    player_hand.append(deck.pop(0))

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

# player takes their turn
def player_turn(player, deck):
    # checks if player chose the option to split their pair
    if player["Split"]:
        both_hands = split_creation(player)
        # if player chose to split pair and both pairs were Aces, player is dealt one card for each hand
        if both_hands[0]["Hand"][0][0] == "A" and both_hands[1]["Hand"][0][0] == "A":
            print(f'\n{player["Name"]}, you drew two aces and decided to split. You will be dealt only one extra card.')
            for hand in both_hands:
                print(f'\n{player["Name"]}, dealer is now dealing to {hand["Which Hand"]}')
                hit(hand["Hand"], deck)
                print(f'\n{player["Name"]}, here is your new hand:')
                for card in hand["Hand"]:
                    print(card)
                if get_total(hand) == 21:
                    print('\nWow you got a blackjack! Lucky Lucky.')
        # if pairs aren't Aces, dealer will deal to each hand normally
        else:
            for hand in both_hands:
                print(f'\n{player["Name"]}, dealer is now dealing to {hand["Which Hand"]}')
                hit(hand["Hand"], deck)
                print(f'\n{player["Name"]}, here is your new hand:')
                for card in hand["Hand"]:
                    print(card)
                # Automatically end the player's turn if they draw a natural hand without splitting Aces
                if get_total(hand) == 21:
                    print('\nYou got blackjack!')
                    continue
                while True:
                    option = input('\nDo you want to stand or hit? ')
                    # ends player's turn if they decide to stand
                    if option.lower() == 'stand':
                        break
                    # draws another card if player decides to hit
                    elif option.lower() == 'hit':
                        hit(hand["Hand"], deck)
                        print(f'\n{player["Name"]}, here is your new hand:')
                        for card in hand["Hand"]:
                            print(card)
                        # Automatically end the player's turn if they draw a blackjack or bust
                        if get_total(hand) == 21:
                            print('\nYou got blackjack!')
                            break
                        elif get_total(hand) > 21:
                            print('\nBusted. You lose.')
                            break
                        else:
                            continue
                    else:
                        print('\nThat is not one of the options. Please try again.')
        # updates players hands after their turn is over
        player["Hand"] = both_hands[0]["Hand"]
        player["Hand2"] = both_hands[1]["Hand"]
    elif player["DoubleDown"]:
        print(f'\n{player["Name"]} the dealer will add one card, faced down, to your hand')
        hit(player["Hand"], deck)
    # if player didn't split pair or double down, play their turn normally
    else:
        while True:
            option = input('\nDo you want to stand or hit? ')
            # ends player's turn if they decide to stand
            if option.lower() == 'stand':
                break
            # draws another card if player decides to hit
            elif option.lower() == 'hit':
                hit(player["Hand"], deck)
                print(f'\n{player["Name"]}, here is your new hand:')
                display_hand(player)
                # Automatically end the player's turn if they draw a blackjack or bust
                if get_total(player) == 21:
                    print('\nYou got blackjack!')
                    break
                elif get_total(player) > 21:
                    print('\nBusted. You lose.')
                    break
                else:
                    continue
            else:
                print('\nThat is not one of the options. Please try again.')

# dealer takes his turn
def dealer_turn(dealer, deck:list):
    if dealer["Natural"]:
        return
    else:
        while True:
            if get_total(dealer) < 17:
                hit(dealer["Hand"], deck)
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
        # if the dealer has a natural blackjack
        elif players[-1]["Natural"]:
            continue
        # if dealer doesn't have natural blackjack
        elif not players[-1]["Natural"]:
            # checks if player decided to split their hand
            if player["Split"]:
                both_hands = split_creation(player)
                # if both player's split hands are naturals skip
                if player["Natural"] and player["Natural2"]:
                    continue
                # if the first split hand is a natural but the second isn't
                elif player["Natural"] and not player["Natural2"]:
                    print(f'\n{player["Name"]}, your first hand turned out to be a natural hand, but your second didn\'t.')
                    print(f'\nLet\'s see how your second hand performed.')
                    if get_total(both_hands[1]) > 21:
                        continue
                    if get_total(players[-1]) > 21:
                        print(f'\n{player["Name"]}, you won! The dealer dealt a bust.')
                    elif get_total(both_hands[1]) > get_total(players[-1]):
                        print(f'\n{player["Name"]}, you won! Your second hand dealt higher than the dealer.')
                    elif get_total(both_hands[1]) == get_total(players[-1]):
                        print(f'\n{player["Name"]}, your second hand drawed with the dealer.')
                    elif get_total(both_hands[1]) < get_total(players[-1]):
                        print(f'\n{player["Name"]}, you lose. Your second hand dealt lower than the dealer.')
        
                    print(f'Your deal total: {get_total(both_hands[1])}')
                    print(f'Dealer\'s deal total: {get_total(players[-1])}')
                # if the first split hand is not a natural but the second is
                elif not player["Natural"] and player["Natural2"]:
                    print(f'\n{player["Name"]}, your second hand turned out to be a natural hand, but your first didn\'t.')
                    print(f'\nLet\'s see how your first hand performed.')
                    if get_total(both_hands[0]) > 21:
                        continue
                    if get_total(players[-1]) > 21:
                        print(f'\n{player["Name"]}, you won! The dealer dealt a bust.')
                    elif get_total(both_hands[0]) > get_total(players[-1]):
                        print(f'\n{player["Name"]}, you won! Your first hand dealt higher than the dealer.')
                    elif get_total(both_hands[0]) == get_total(players[-1]):
                        print(f'\n{player["Name"]}, your first hand drawed with the dealer.')
                    elif get_total(both_hands[0]) < get_total(players[-1]):
                        print(f'\n{player["Name"]}, you lose. Your first hand dealt lower than the dealer.')
        
                    print(f'Your deal total: {get_total(both_hands[0])}')
                    print(f'Dealer\'s deal total: {get_total(players[-1])}')
                # if neither hand is a natural hand
                else:
                    print(f'\n{player["Name"]}, Let\'s see how each of your hands performed...')
                    for hand in both_hands:
                        if get_total(hand) > 21:
                            continue
                        if get_total(players[-1]) > 21:
                            print(f'\n{player["Name"]}, you won! The dealer dealt a bust.')
                        elif get_total(hand) > get_total(players[-1]):
                            print(f'\n{player["Name"]}, you won! {hand["Which Hand"]} dealt higher than the dealer.')
                        elif get_total(hand) == get_total(players[-1]):
                            print(f'\n{player["Name"]}, {hand["Which Hand"]} drawed with the dealer.')
                        elif get_total(hand) < get_total(players[-1]):
                            print(f'\n{player["Name"]}, you lose. {hand["Which Hand"]} dealt lower than the dealer.')

                        print(f'Your deal total: {get_total(hand)}')
                        print(f'Dealer\'s deal total: {get_total(players[-1])}')
            # rewards player if they have a natural blackjack
            elif player["Natural"]:
                continue
            # if player chooses to surrender their hand
            elif player["Surrender"]:
                print(f'{player["Name"]} surrendered.')
            # if the current player already lost by drawing a bust
            elif get_total(player) > 21:
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
                    print(f'\n{player["Name"]}, you lose. You dealt lower than the dealer.')
        
                print(f'Your deal total: {get_total(player)}')
                print(f'Dealer\'s deal total: {get_total(players[-1])}')
