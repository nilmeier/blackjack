"""Cards Module:  Base classes for hands, decks, and  cards, and operations such as dealing"""
# Follows example given in 
# "Python programming for the Absolute Beginner,(Ch.9), 3rd Ed." by M. Dawson

# Additional Functions added by J. Nilmeier



class Card(object):
    """ A playing card. """
    ## List of Cards with String Values.
    RANKS = ["A", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "J", "Q", "K"]
    ## List of Suits.         
    SUITS = ["c", "d", "h", "s"]

    ## Hard coded Value for Ace.
    ACE_VALUE=1
    def __init__(self, rank, suit, face_up = True):
        """Initializes Card."""
        ## Card value.
        self.rank = rank 
        ## Suit value.
        self.suit = suit
        ## Face up value (for flipping).
        self.is_face_up = face_up

    def __str__(self):
        """Returns an output string.""" 
        if self.is_face_up:
            rep = self.rank + self.suit
        else:
            rep = "XX"
        return rep

    def flip(self):
        """Flips card over (for dealer)."""
        self.is_face_up = not self.is_face_up

    @property
    def value(self):
        """Computes number value of card."""
        if self.is_face_up:
            v = Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v


class Hand(object):
    """ A hand of playing cards. """
    def __init__(self):
        """Initializes Hand with empty card array."""
        ## list for Card() object## list for Card() objects.
        self.cards = []
         
    def __str__(self):
        """Returns an output string.""" 
        if self.cards:
           rep = ""
           for card in self.cards:
               rep += str(card) + "  "
        else:
            rep = "<empty>"
        
        if self.total:
            rep += "totaling: (" + str(self.total) + ")"
        return rep

    def clear(self):
        """Clears cards in hand."""
        self.cards = []

    def add(self, card):
        """Adds a card to hand."""
        self.cards.append(card)

    def give(self, card, other_hand):
        """Gives a card from self to another hand."""
        self.cards.remove(card)
        other_hand.add(card)

    @property
    def total(self):     
        """Computes total value in hand."""
        # if a card in the hand has value of None, then total is None
        for card in self.cards:
            if not card.value:
                return None

        # add up card values, treat each Ace as 1
        t = 0
        for card in self.cards:
              t += card.value

        # determine if hand contains an Ace
        contains_ace = False
        for card in self.cards:
            if card.value == Card.ACE_VALUE:
                contains_ace = True

        # if hand contains Ace and total is low enough, treat Ace as 11
        if contains_ace and t <= 11:
            # add only 10 since we've already added 1 for the Ace
            t += 10

        return t

    def is_busted(self):
        """Returns true if hand is over 21."""
        return self.total > 21

    def is_blackjack(self):
        """Checks for blackjack."""
        blackjack=False
        if (self.total==21) and len(self.cards)==2: 
            blackjack=True
        return blackjack
    
    def is_splittable(self):
        """
        Checks to see if hand can be split (10s and facecards, along with matching number cards).
        """
        splittable=False
        is_1_face=False
        is_2_face=False
        v = self.cards[0].RANKS.index(self.cards[0].rank) + 1
        if v >= 10: 
            is_1_face=True  # must include 10s as faces
        v = self.cards[1].RANKS.index(self.cards[1].rank) + 1
        
        if v >= 10: 
            is_2_face=True
        
        if (len(self.cards)==2 and is_1_face and is_2_face):
            splittable=True

        #checking other ranks
        if(self.cards[0].rank==self.cards[1].rank): 
            splittable=True

        return splittable
    

class Deck(Hand):
   """ A deck of playing cards. """
   def populate(self):
       """Populates with 1 full, ordered deck (can be called multiple times)."""
       for suit in Card.SUITS:
           for rank in Card.RANKS:
               self.add(Card(rank, suit))

   def shuffle(self):
       """Shuffles deck (of any size)."""
       import random
       random.shuffle(self.cards)

   def deal(self, hands, per_hand = 1):
       """Deals 1 or more cards to a list of hands (players).""" 
       for rounds in range(per_hand):
           for hand in hands:
               if self.cards:
                   top_card = self.cards[0]
                   self.give(top_card, hand)
               else:
                   print("Can't continue deal. Out of cards!")


if __name__ == "__main__":
    """Main module not used."""
    print("This is a module with classes for playing cards.")
    input("\n\nPress the enter key to exit.")

