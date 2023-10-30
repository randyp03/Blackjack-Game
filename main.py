# Blackjack

import game_functions

running = True

input('Welcome! Press Enter/Return to begin game ')
print()

# main game
while running:
    
    # starts the game by creating players, and dealing cards
    players, deck = game_functions.start_game()

    # check if there is possibility of dealer having natural hand and opening up chance for insurance bets if Ace-up
    if game_functions.check_face_up(players[-1]) == 'A' or game_functions.check_face_up(players[-1]) == 'ten-card':
        game_functions.display_hand(players[-1])
        # check if possibility of insurance
        if game_functions.check_face_up(players[-1]) == 'A':
            print("\nDealer has an ace up. Dealer has opened the option for insurance.")
            for player in players:
                if game_functions.isDealer(player):
                    break
                else:
                    has_insurance = input(f'\n{player["Name"]}, do you want to place an insurance bet (y/n)? ')
                    if has_insurance.lower().startswith('y'):
                        player["Insurance"] = True
                        print(f'\n{player["Name"]} has placed insurance')
        # after insurance bets are placed, check if dealer has blackjack
        print("\nDealer will check if they have a natural hand")
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
                print(f'\n{player["Name"]}, you also got natural blackjack! Lucky you.')
                continue
            else:
                print(f'\n{player["Name"]}, you don\'t have a natural hand. Tough luck.')
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
            # checks if the player has option to split their pair
            elif player["Hand"][0][0] == player["Hand"][1][0]:
                split_pair = input(f'\nDo you want to split your pair (y/n)? ')
                # if player chooses to split pair,
                # remove second card from original hand and place into second hand
                if split_pair.lower().startswith('y'):
                    player["Split"] = True
                    print('\nYou have chosen to split your pair.')
                    player["Hand2"].append(player["Hand"].pop(1))
                    game_functions.player_turn(player, deck)
                # if player rejects split option, play hand normally
                elif split_pair.lower().startswith('n'):
                    print('\nYou have chosen not to split your pair')
                    game_functions.player_turn(player, deck)
                # game will automatically reject split option if player presses wrong key
                else:
                    print('\nThat is not one of the options. You will automatically reject split option.')
                    game_functions.player_turn(player, deck)
            # if player doesn't have natural blackjack and can't split their pair, play their turn normally
            else: 
                game_functions.player_turn(player, deck)

    # dealer has their turn
    game_functions.dealer_turn(players[-1], deck)
    # gets result of comparing the player vs the dealer
    game_functions.get_result(players)
    
    while True:
        play_again = input('\nDo you want to play again (y/n)? ')
        if play_again.lower().startswith('y'):
            break
        elif play_again.lower().startswith('n'):
            print('\nThanks for playing!')
            running=False
            break
        else:
            print('\nPlease enter one of the two option')