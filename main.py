import random as r
import play as p
#import cards as c


def main():
    """Main function for blackjack game."""
    print("Welcome to blackjack!\n")
    again = None

    while again != "n":
        players = []
        again="n"

        # get number of players and number of decks in shoe:
        num = p.ask_number(question = "How many players? (1 - 5): ", low = 1, high = 5)
        ndecks = p.ask_number(question = "How many decks in shoe? (1 - 4): ", low = 1, high = 4)
        
        #get player names
        for i in range(num):
            name = raw_input("Player name: ")
            players.append(name)
        
        #play the game
        game=p.Game(players,ndecks)
        game.play()


#running main here:
main()
print("\n------- Thanks for playing! -------\n")
