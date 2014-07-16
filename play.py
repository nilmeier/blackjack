"""Play Module:  Classes for Player, Dealer, and Game"""
# Follows example given in 
# "Python programming for the Absolute Beginner,(Ch.9), 3rd Ed." by M. Dawson

# main routine is in Game.play()
# additional functions, such as banks/betting, insurance, splitting, double down 
# and blackjack payouts added by J. Nilmeier

from cards import *


class Player(Hand):
    """ A (blackjack) player for a game. """
    def __init__(self,name,nchips):
        """Initializes Player"""
        ## Name.
        self.name=name                 
        ## Chips in player bank.
        self.nchips=nchips             
        ## Amount of bet.
        self.bet=0                     
        ## Amount of insurance bet.
        self.ins_bet=0                 
        ## True if hand is split from original. 
        self.split=False               
        ## True if player is doubling down.
        self.doubledown=False      
        ## List of cards.
        self.cards=[]

    def is_hitting(self): 
        """
        Prompts for a hit unless a rule is applied:
          -score=21
          -after a double down deal
        """ 
        if (self.total==21 or self.doubledown):  
            response="n"
        else:
            response = ask_yes_no( self.name + " has "+str(self)+ ", do you want a hit? (Y/N): ")
        if (response=="n"): 
            print self.name+ " has "+ str(self) +", and stands\n"
        return response == "y"

    def bust(self):
        """Outputs bust then calls lose().""" 
        print(self.name+" busts.")
        self.lose()

    def lose(self):
        """Loses and prints (no bank update required)."""
        #jn print(self.name+ " loses.  bank:dd %d\n"%self.nchips)
        print self.name+ " has "+ str(self) +", and loses.   bank: %d\n"%(self.nchips)
 
    def win(self):
        """Wins, prints, and updates bank.  Includes blackjack payout if needed (2:1)"""
        if self.is_blackjack():
           self.nchips+=3*self.bet
           print self.name+ " has "+ str(self) +"..blackjack!, and wins.    bank: %d\n"%(self.nchips)
        else:
            self.nchips+=2*self.bet
            print self.name + " has "+ str(self) +", and wins.    bank: %d\n"%(self.nchips)

    def push(self):
        """Pushes, prints, and updates bank.""" 
        self.nchips+=self.bet
        print self.name+ " has "+ str(self) +", and pushes.  bank: %d\n"%(self.nchips)
         
    def placeBet(self,bet):
        """
        Takes bet amount from bank and adds to (total) bet amount.  
        Total bet is incremented to allow for double down.
        """
        self.nchips-=bet
        self.bet+=bet
    
    def placeInsuranceBet(self,ins_bet):
        """Takes insurance bet from bank."""
        self.nchips-=ins_bet
        self.ins_bet=ins_bet

    def payInsuranceBet(self):
        """Pays insurance back to bank and reinitializes insurance bet.""" 
        self.nchips+=2*self.ins_bet 
        self.ins_bet=0

    def setSplitHand(self):
        """Identifies whetjer player was created from a split hand (deleted every round)"""
        self.split=True 

    def setDoubledownHand(self):
        """Identifies player as hitting with a doubledown option (forced to stay after 1 hit) ."""
        self.doubledown=True

class Dealer(Hand):
    """ A blackjack Dealer. """
    def __init__(self,name):
        """Initializes Dealer"""
        ## Name.
        self.name=name
        ## List of cards.
        self.cards=[]

    def is_hitting(self):
        """Dealer follows unprompted rules for hitting and staying listed here."""
        return self.total < 17

    def bust(self):
        """Dealer busts and outputs string."""
        print self.name + " busts with "+ str(self)

    def flip_first_card(self):
        """Dealer flips his first card to be ether visible or invisible"""
        first_card = self.cards[0]
        first_card.flip()


class Game(object):
    """A blackjack Game."""
    def __init__( self, names,ndecks ):
        """Initializes Game."""
        ## List of Players.
        self.players = []
        ## Number of decks in shoe.
        self.ndecks=ndecks 
        for name in names:
            player = Player(name,nchips=100)
            self.players.append(player)
        ## Creates Dealer
        self.dealer = Dealer("Dealer")
        ## Creates a Deck (actually a Shoe that can contain multiple decks)
        self.deck = Deck()
        for i_deck in range(self.ndecks): self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        """Creates a list of players that haven't busted."""
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        """
        Prompts for hit until player stays or busts.
        """
        while not player.is_busted() and player.is_hitting():
            
            self.deck.deal([player])

            if player.is_busted():
                player.bust()

    def play(self):
        """Main play routine.  finish_hand() called for second half of game play."""
        again = None
        while again != "n":
    
            # shuffling before deal if < 35 remaining after initial deal
            if (len(self.deck.cards)< (1+len(self.players) )*2 + 35 ):
                print str(len(self.deck.cards)) +" cards left...shuffling"
                self.deck.clear()
                for i_deck in range(self.ndecks): self.deck.populate()
                self.deck.shuffle()                
        
            # get bets before dealing
            for player in self.players:
               bet=ask_number(player.name +", what is your bet? (1-"+str(player.nchips)+"): ", low=1,high=int(player.nchips))
               player.placeBet(bet)
            
            # deal the cards
            self.deck.deal(self.players + [self.dealer], per_hand = 2)

            self.dealer.flip_first_card()        # hide dealer's first card
            
            # checking for dealer blackjack when ace is showing
            if (self.dealer.cards[1].rank=="A"):
                self.check_blackjack_and_finish_hand() 
            else:
               self.dealer.flip_first_card()    # reveal dealer's first card
               self.finish_hand()               # finish regular play
    

            # remove everyone's cards, split hands and bankrupt players
            remove_list=list(); i_p=0 #creating a list of items to remove
            for player in self.players:
                player.clear()                  # clearing player hand
                if player.nchips==0 and player.split==False:
                    print player.name +" is out of chips."
                    remove_list.append(player)
                if player.split:                # deleting split hands
                    remove_list.append(player)
                    self.players[i_p-1].nchips+=player.nchips
                i_p+=1

            for player in remove_list:
                self.players.remove(player)     # removing from list

            # clearing dealer hand
            self.dealer.clear()

            # summary before next round and prompt to continue
            print "--------- Going into next round ---------"
            for player in self.players:
                print player.name + ")   bank:  "  +str(player.nchips)  
            if (len(self.players)==0): 
                print "House wins.  No more players"
                again="n"
            else:
                again = ask_yes_no("\nanother game? (y/n): ")

    def finish_hand(self):
        """ 
        regular play after first deal has been handled in play() 
        """
        self.dealer.flip_first_card()    # hide dealer's first card

        # processing splittable hands
        print("\nDealer hand: \n" +str(self.dealer) )
        self.process_splits()

        # printing out hands after dealer blackjack processing and splitting
        print ""
        print "----------- After Deal ------------"
        for player in self.players:
            print player.name + ") bet:  "+ str(player.bet)+ "  bank:  "+ str(player.nchips)  
            print "        Cards:  "+ str(player)

        print ""
        print     "  Dealer hand:  "+ str(self.dealer)
        print "-----------------------------------"
        print""

        # offer double downs'
        self.offer_double_down()

        # deal additional cards to players
        for player in self.players:
            self.__additional_cards(player)

        self.dealer.flip_first_card()    # reveal dealer's first card

        if not self.still_playing:
            # since all players have busted, just show the dealer's hand
            print("\nDealer hand: \n" +str(self.dealer) )
        else:
            # deal additional cards to dealer
            print(self.dealer)
            self.__additional_cards(self.dealer)

            print "\n --Summary of Play against Dealer Hand --\n Dealer hand (Final):\n        " + str(self.dealer) 
            if self.dealer.is_busted():
                # everyone still playing wins if dealer busts.
                print("Dealer busts.\n")
                for player in self.still_playing:
                    player.win()
            else:
                # compare each player still playing to dealer
                print""
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                 
                    elif player.total < self.dealer.total:
                 
                        player.lose()
                     
                    else:  #tie in score (blackjack breaks a tie of 21)
                        if player.is_blackjack():
                            player.win()
                        else:    
                           player.push()


    def process_splits(self):
        """ 
        checks for hands that can be split, creates a duplicate player, takes a bet, 
        and deals an extra card to each hand. 
        """
        # prompting for split player, and making sure player can afford it.
        add_list=list(); i_p=0
        print "\n"+ "--------- Splitting Hands ---------"
        for player in self.players:
            if (player.is_splittable()): 
                print player.name+" has "+str(player) +":  this can be split (only once for now)"
                if (player.nchips>=player.bet): #you have to have money in the bank to split.
                   split = ask_yes_no("   "+player.name+":  do you want to split? (y/n): ")
                else:
                   split = "n"
                   print "but you don't have enough money to cover the split...sorry!"
                if split=="y":
                    add_list.append(i_p)
            i_p+=1
        if len(add_list)==0: print "No splits will be made this round."

        print       "-----------------------------------"


        #  create a split player
        reg_shift=0
        for addline in add_list:
            i_p=addline+reg_shift #reg shift is required for multiple player splits
            # get the data from the player that is splitting
            player_to_split = self.players[i_p]
            new_name = player_to_split.name + "-2"
            top_card = player_to_split.cards[0]
            
            # transferr the bet to split player
            bet_to_transfer=player_to_split.bet  
            self.players[i_p].nchips-= bet_to_transfer
            
            # create a new hand:
            new_split_player = Player(new_name,nchips=0)
            new_split_player.setSplitHand() #sets Hand with a boolean flag
            self.players.insert(i_p+1, new_split_player)
            self.players[i_p+1].cards=[] #same init issue as Games()
            self.players[i_p+1].bet=bet_to_transfer
            
            # give the new split hand the top card
            self.players[i_p].give(top_card,self.players[i_p+1])
      
            # deal one card to each of the new hands:
            self.deck.deal(self.players[i_p:i_p+2],per_hand=1) 
            reg_shift +=1
            
    def check_blackjack_and_finish_hand(self):
        """
        Screens for dealer blackjack, offers insurance, and returns 
        to normal play if no blackjack. 
        """
    
        print "Dealer hand:"
        print(self.dealer)
        print "\nInsurance is available if Dealer Ace is showing."
        for player in self.players:
            max_ins=min(player.nchips,player.bet)
            ins_bet = ask_number(player.name +" has "+str(player) + ", insurance (0-"+str(max_ins)+")? ",low=0,high=max_ins )
            player.placeInsuranceBet(ins_bet)

        # check for blackjack:
        self.dealer.flip_first_card()    # reveal dealer's first card
        
        print "Dealer hand:"
        print(self.dealer)
         
        if self.dealer.is_blackjack():
           print "Dealer blackjack!\n"
           for player in self.players:
               player.payInsuranceBet()
               print player.name + " has " + str(player.nchips)+" chips after insurance payout"  
               print player.name + " hand: " + str(player) +"\n"
  
               if player.is_blackjack():
                   print("even money insurance payout")
                   player.push()
               else:
                   player.lose()
        else:
            print "No dealer blackjack...insurance bets collected."
            # return to finishing regular play
            self.finish_hand()
    
    def offer_double_down(self):
       """
       To keep game play moving, we offer double downs to hands with 9,10,or 11 as score.  
       Also, player must be able to afford it.
       """

       print ""
       print "------- Double Down Offers --------"
       i_p=0;dd_count=0
       for player in self.players:
           if player.total>=9 and player.total<=11:
               doubledown = ask_yes_no("   "+player.name+" has "+str(player) +":  do you want to double down? (y/n): ")
               #extra bookkeepping for a split hand:
               if (doubledown=="y" and player.split):
                  player_orig=self.players[i_p-1]
                  if player_orig.nchips>=player.bet: #borrowing from original player
                      player.nchips+=player.bet
                      player_orig.nchips-=player.bet
                  else:  
                      print  player_orig.name+" bank ("+str(player_orig.nchips)+") not enough to cover bet..sorry!"
                      doubledown="n"
               #error handling for all hands (including fixed split hands)       
               if (doubledown=="y") and (player.nchips<player.bet):
                      print  player.name+" bank ("+str(player.nchips)+") not enough to cover bet..sorry!"
                      doubledown="n"

               #processing the double down if everything is in order
               if doubledown=="y":
                   dd_count+=1
                   player.placeBet(player.bet) #adding a bet to existing bet
                   player.setDoubledownHand()
                   self.deck.deal([player])
           i_p+=1   
       if (dd_count==0): print "No double downs will be made this round"
       print "-----------------------------------"
       print""                       

def ask_yes_no(question):
    """Ask a yes or no question."""
    response = None
    while response not in ("y", "n"):
        response = raw_input(question).lower()
    return response

def ask_number(question, low, high):
    """Ask for a number within a range."""
    response = None
    while response not in range(low, high+1):
        response = int(input(question))
    return response



if __name__ == "__main__":
    print("You ran this module directly (and did not 'import' it).")
    input("\n\nPress the enter key to exit.")
