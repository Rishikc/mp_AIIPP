'''
Created on Aug 20, 2014

@author: victorzhao
'''

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
# Store the message for indicating following steps, like Hit or Stand, New deal?
state = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, 
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        string = ' '
        for i in range(len(self.hand)):
            string += str(self.hand[i]) + ' '
        return 'Hand contains' + string    # return a string representation of a hand

    def add_card(self, card):
        self.hand.append(card)    # add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0  # compute the value of the hand, see Blackjack video
        num_ace = 0
        for i in range(len(self.hand)):
            if self.hand[i].rank == 'A':
                num_ace += 1
        for i in range(len(self.hand)):
                hand_value += VALUES[self.hand[i].rank]
        if num_ace == 0:
            return hand_value
        else:
             if hand_value + 10 <= 21:
                    return hand_value + 10
             else:
                    return hand_value              

    def draw(self, canvas, pos):
        for i in range(len(self.hand)):    # draw a hand on the canvas, use the draw method for cards
            self.hand[i].draw(canvas, [pos[0] + (CARD_SIZE[0] + 10) * i, pos[1]]) 
            
# define deck class 
class Deck:
    def __init__(self):
        self.deck_cards = []    # create a Deck object
        for i in range(4):
            for j in range(13):
                self.deck_cards.append(Card(SUITS[i], RANKS[j]))
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_cards) # use random.shuffle()

    def deal_card(self):
        """ This method will automatically test if the deck is empty, and refill it """
        if len(self.deck_cards) == 0:
            self.deck_cards = []    # create a Deck object
            for i in range(4):
                for j in range(13):
                    self.deck_cards.append(Card(SUITS[i], RANKS[j]))     
        return self.deck_cards.pop(len(self.deck_cards) - 1) # deal a card object from the deck
    
    def __str__(self):
        string = ' '
        for i in range(len(self.deck_cards)):
            string += str(self.deck_cards[i]) + ' '
        return 'Deck contains' + string # return a string representing the deck        



#define event handlers for buttons
def deal():
    global outcome, in_play, deck_inst, score, state, player_hand, dealer_hand

    # your code goes here
    # Pressing the "Deal" button in the middle of the round causes the player to lose the current round 
    if in_play == True:
        in_play = False
        score -= 1
        outcome = 'Dealer Wins'
        state = 'New deal?' 
        
    elif len(deck_inst.deck_cards) != 0:
        deck_inst.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(deck_inst.deal_card())
        dealer_hand.add_card(deck_inst.deal_card())
        player_hand.add_card(deck_inst.deal_card())
        dealer_hand.add_card(deck_inst.deal_card())
        state = 'Hit or stand?'
        outcome = ''
        in_play = True
        
    else:
        deck_inst = Deck()
        deck_inst.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(deck_inst.deal_card())
        dealer_hand.add_card(deck_inst.deal_card())
        player_hand.add_card(deck_inst.deal_card())
        dealer_hand.add_card(deck_inst.deal_card())
        state = 'Hit or stand?'
        outcome = ''
        in_play = True
    
    

def hit():
        # replace with your code below
    global in_play, outcome, score, state
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck_inst.deal_card())
        if player_hand.get_value() > 21:
    # if busted, assign a message to outcome, update in_play and score
            # print "You have busted"
            outcome = 'You have busted.'
            state = 'New deal?'
            score -= 1
            in_play = False
def stand():
        # replace with your code below
    global in_play, score, state, outcome
    if in_play == True:
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck_inst.deal_card())
    # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            outcome = 'Dealer busted'
            state = 'New deal?'
            score += 1
        elif player_hand.get_value() > dealer_hand.get_value():
            # print "Player Wins"
            outcome = 'Player Wins.'
            state = 'New deal?'
            score += 1
        else:
            # print "Dealer Wins"
            outcome = 'Dealer Wins.'
            state = 'New deal?'
            score -= 1
        in_play = False
        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    # card = Card("S", "A")
    # card.draw(canvas, [300, 300])
    
    canvas.draw_text(outcome, (300, 180), 20, 'White', 'serif')
    canvas.draw_text(state, (300, 380), 20, 'White', 'serif')
    canvas.draw_text('Dealer', (100, 180), 20, 'White', 'serif')
    canvas.draw_text('Player', (100, 380), 20, 'White', 'serif')
    canvas.draw_text('Blackjack', (60, 80), 50, 'Blue', 'serif')
    canvas.draw_text('Score: ' + str(score), (400, 50), 30, 'White', 'serif')
    dealer_hand.draw(canvas, [100, 200])
    player_hand.draw(canvas, [100, 400])
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [100 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_SIZE)
    
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deck_inst = Deck()
player_hand = Hand()
dealer_hand = Hand()

deal()
# outcome = 'You have busted'
frame.start()



# remember to review the gradic rubric