# Blackjack

import game_functions, json

running = True

input('Welcome! Press Enter/Return to begin game ')
print()

# main game
while running:
    
    # starts the game by creating players, and dealing cards
    players, deck = game_functions.start_game()

    # check if possibility of insurance
    if game_functions.check_face_up(players[-1]) == 'A':
        game_functions.display_hand(players[-1])
        print("\nDealer has an ace up. Dealer has opened the option for insurance.")
        for player in players:
            if game_functions.isDealer(player):
                break
            else:
                has_insurance = input(f'\n{player["Name"]}, do you want to place an insurance bet (y/n)? ')
                if has_insurance.lower().startswith('y'):
                    player["Insurance"] = True
                    print(f'\n{player["Name"]} has placed insurance')

    # check if dealer has a natural blackjack
    if game_functions.check_face_up(players[-1]) == 'A' or game_functions.check_face_up(players[-1]) == 'ten-card':
        if game_functions.get_total(players[-1]) == 21:
            print("\nDealer has natural blackjack!")
            players[-1]["Natural"] = True
        # check if any players have made insurance bets
        for player in players:
            if game_functions.isDealer(player):
                break
            elif player["Insurance"] and players[-1]["Natural"]:
                print(f'\n{player["Name"]}, your decision for an insurance bet was lucky')
            elif player["Insurance"] and not players[-1]["Natural"]:
                print(f'\n{player["Name"]}, your insurance bet was good for nothing. Dummy.')
            else:
                continue

    # each player takes their turn before dealer
    for player in players:
        if game_functions.isDealer(player):
            break
        # if dealer has natural hand, immediately check if players also have natural hand
        elif players[-1]["Natural"]:
            # displaying dealer's full hand
            print(f'\nHere is the dealer\'s hand')
            game_functions.display_hand(players[-1], True)
            # displaying current player's hand
            print(f'\n{player["Name"]}, here is your hand:')
            game_functions.display_hand(player)
            # checking whether player also has natural hand
            if game_functions.get_total(player) == 21:
                player["Natural"] = True
                print(f'\n{player["Name"]}, You also got natural blackjack! Lucky you.')
                continue
            else:
                print(f'\n{player["Name"]}, You don\'t have a natural hand. Tough luck.')
                continue
        # if not dealer, and dealer doesn't have natural hand, proceed normally
        else:
            # display dealer's hand
            game_functions.display_hand(players[-1])
            # displaying current player's hand
            print(f'\n{player["Name"]}, here is your hand:')
            game_functions.display_hand(player)

            # checks if the player's hand is a natural blackjack
            if game_functions.get_total(player) == 21:
                player["Natural"] = True
                print(f'\n{player["Name"]}, you have a natural hand, and the dealer doesn\'t. You win!')
                continue
            else: 
                while True:
                    option = input('\nDo you want to stand or hit? ')
                    if option.lower() == 'stand':
                        break
                    elif option.lower() == 'hit':
                        game_functions.hit(player, deck)
                        print(f'\n{player["Name"]}, here is your new hand:')
                        for card in player["Hand"]:
                            print(card)
                        # Automatically end the player's turn if they draw a blackjack or bust
                        if game_functions.get_total(player) == 21:
                            print('\nYou got blackjack!')
                            break
                        elif game_functions.get_total(player) > 21:
                            print('\nBusted. You lose.')
                            break
                        else:
                            continue
                    else:
                        print('\nThat is not one of the options. Please try again.')

    # dealer has their turn
    game_functions.dealer_turn(players[-1], deck)
    # gets result of comparing the player vs the dealer
    game_functions.get_result(players)
    
    while True:
        play_again = input('\nDo you want to play again? (y/n)')
        if play_again.lower().startswith('y'):
            break
        elif play_again.lower().startswith('n'):
            print('\nThanks for playing!')
            running=False
            break
        else:
            print('\nPlease enter one of the two option')