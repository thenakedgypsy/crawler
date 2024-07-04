import random


class Card:
    def __init__(self, suit, rank): #initialise a card with a suit and rank
        self.__suit = suit
        self.__rank = rank
        self.__selected = False

    def setSuit(self, suit): # sets the card suit
        self.__suit = suit
        
    def getSuit(self): #returns the card suit
        return self.__suit
    
    def setRank(self, rank): #sets the card rank
        self.__rank = rank

    def getRank(self): #returns the card rank
        return self.__rank
    
    def setImage(self, image):
        self.image = image

    def getImage(self):
        return self.image
    
    def setRect(self, rect):
        self.rect = rect

    def getRect(self):
        return self.rect#
    
    def select(self):
        if self.__selected:
            self.__selected = False
        else:
            self.__selected = True

    def getSelected(self):
        return self.__selected

class Deck:
    def __init__(self):#initialises object with a list
        self.__cardsInDeck = []

    def getDeck(self): #returns the list of cards 
        return self.__cardsInDeck

    def addCard(self,card): #adds a card to the deck
        self.__cardsInDeck.append(card)

    def getCard(self,index): #returns a card at index
        return self.__cardsInDeck[index]
    
    def shuffle(self): #shuffles the deck
        random.shuffle(self.__cardsInDeck)
    
    def discard(self,index): #removes a card from the deck at index
        del self.__cardsInDeck[index]

    def getDeckSize(self): #returns the number of cards in the deck
        return len(self.__cardsInDeck) -1

    def draw(self): #returns the top card of the deck or prints an error
        if self.getDeckSize() >= 0:
            return self.__cardsInDeck.pop()
        else:
            raise Exception("Empty Deck")  
    
    def printDeck(self): #prints each card in the deck
        for card in self.getDeck():
            card.printCard()

    def __iter__(self): #makes the deck iterable
        return iter(self.__cardsInDeck)
    
    def __len__(self):
        return len(self.__cardsInDeck)


class Dealer():

    def makeStandardDeck(self):   #makes a standard deck
        deck = Deck()
        suitList = ["spades","hearts","diamonds","clubs"]
        rankList = ["ace","2","3","4","5","6","7","8","9","10","jack","queen","king"]
        for suit in suitList:
            for rank in rankList:
                card = Card(suit,rank)
                deck.addCard(card)
        return deck

class Hand(Deck): 
    pass

class PlayArea(Deck): 
    pass





