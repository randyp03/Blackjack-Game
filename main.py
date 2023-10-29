# Blackjack

import game_functions

running = True

input('Welcome! Press Enter/Return to begin game ')
print()

# main game
while running:
    player_list = []
    dealt_cards = {}
    
    player_list, dealt_cards, deck = game_functions.start_game(player_list, dealt_cards)

    # each player takes their turn before dealer
    for player in player_list:
        game_functions.display_deal(dealt_cards, 'Dealer')
        print(f'\n{player}, here is your hand:')
        game_functions.display_deal(dealt_cards, player)

        # checks if the player's hand is a natural
        if game_functions.get_total(dealt_cards, player) == 21:
            print('You got blackjack!')
            break
        else: 
            while True:
                option = input('\nDo you want to stand or hit? ')
                if option.lower() == 'stand':
                    break
                elif option.lower() == 'hit':
                    game_functions.extra_deal(dealt_cards, player, deck)
                    print(f'\n{player}, here is your new hand:')
                    for card in dealt_cards[player]:
                        print(card)
                    # Automatically end the player's turn if their hand is a bust
                    if game_functions.get_total(dealt_cards,player) > 21:
                        print('\nBusted. You lose.')
                        break
                    else:
                        continue
                else:
                    print('\nThat is not one of the options. Please try again.')

    game_functions.dealer_turn(dealt_cards, deck)

    game_functions.get_result(player_list,dealt_cards)
    
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