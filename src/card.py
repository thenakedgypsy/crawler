import random


class Card:
    def __init__(self, suit, rank): #initialise a card with a suit and rank
        self.__suit = suit
        self.__rank = rank
        self.altValue = None
        self.__selected = False
        if self.__rank == "ace":
            self.value = 14
        elif self.__rank == "king":
            self.value = 13
        elif self.__rank == "queen":
            self.value = 12
        elif self.__rank == "jack":
            self.value = 11
        else:
            self.value = int(self.getRank())
        self.firstBlit = True

    def getValue(self):#returns the value
        return self.value
    
    def setValue(self, value):
        self.value = value

    def setSuit(self, suit): # sets the card suit
        self.__suit = suit
        
    def getSuit(self): #returns the card suit
        return self.__suit
    
    def setRank(self, rank): #sets the card rank
        self.__rank = rank

    def getRank(self): #returns the card rank
        return self.__rank
    
    def setImage(self, image): #sets an image to this card
        self.image = image

    def getImage(self):#returns the image of this card
        return self.image
    
    def setRect(self, rect):#sets its shape
        self.rect = rect

    def getRect(self): #returrns its shape
        return self.rect#
    
    def select(self):#sets the card as selected or unselected
        if self.__selected:
            self.__selected = False
        else:
            self.__selected = True

    def getSelected(self): #returns the selection state
        return self.__selected
    
    def __lt__(self,other): #lessthan
        return self.value < other.value
    
    def __eq__(self,other):
        if self.getSuit() == other.getSuit():
            return self.getRank() == other.getRank()

    def getBlit(self): #check the status of the "FirstBlit variable. True = needs first time blit, False = already blitted"
        return self.firstBlit
    
    def setBlit(self, bool): #takes a bool and updates FirstBlit 
        self.firstBlit = bool
    


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

    def remove(self,card):
        if card in self.__cardsInDeck:
            self.__cardsInDeck.remove(card)
        else:
            raise Exception("Deck does not contain that card")

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
    
    def evaluate(self): #checks for all handtypes
        if self.flushCheck() and self.straightCheck():
            return "straightflush"
        elif self.flushCheck():
            return "flush"
        elif self.straightCheck():
            return "straight"
        elif self.fourCheck():
            return "fourkind"
        elif self.fullHouseCheck():
            return "fullhouse"
        elif self.twoPairCheck():
            return "twopair"
        elif self.threeCheck():
            return "threekind"
        elif self.twoCheck():
            return "pair"
        else:
            return "highcard"

    def twoPairCheck(self):
        valueCounts = {}
        for card in self.__cardsInDeck:
            value = card.getValue()
            if value in valueCounts:
                valueCounts[value] +=1
            else:
                valueCounts[value] = 1
        pairs = 0
        for count in valueCounts.values():
            if count >= 2:
                pairs +=1
        if pairs >= 2:
            return True
        else:
            return False
                
    def fullHouseCheck(self):
        valueCounts = {}
        for card in self.__cardsInDeck:
            value = card.getValue()
            if value in valueCounts:
                valueCounts[value] +=1
            else:
                valueCounts[value] = 1
        pairs = 0
        trips = 0
        for count in valueCounts.values():
            if count == 2:
                pairs +=1
            if count == 3:
                trips +=1
        if pairs >= 1 and trips >= 1:
            return True
        else:
            return False


    def fourCheck(self): #checks for fourofakind
        for card in self.__cardsInDeck:
            cardsSame = 0
            searchedRank = card.getRank()
            for card in self.__cardsInDeck:
                if card.getRank() == searchedRank:
                    cardsSame +=1
            if cardsSame == 4:
                return True
            return False 

    def threeCheck(self): #checks for three of a kind
        for card in self.__cardsInDeck:
            cardsSame = 0
            searchedRank = card.getRank()
            for card in self.__cardsInDeck:
                if card.getRank() == searchedRank:
                    cardsSame +=1
            if cardsSame == 3:
                return True
            return False       
        
    def twoCheck(self): #checks for a pair
        for card in self.__cardsInDeck:
            cardsSame = 0
            searchedRank = card.getRank()
            for card in self.__cardsInDeck:
                if card.getRank() == searchedRank:
                    cardsSame +=1
            if cardsSame == 2:
                return True
            return False       

    def flushCheck(self): #checks for a flush
        numSame = 0
        suit = self.__cardsInDeck[0].getSuit()
        for card in self.__cardsInDeck:
            if card.getSuit() == suit:
                numSame +=1
        if numSame == 5:
            return True
        return False
    
    def straightCheck(self): # Checks for a straight
        sortedDeck = sorted(self.__cardsInDeck, key=lambda card: card.getValue())
        inSeries = 0

        # check for a normal straight
        for i in range(len(sortedDeck) - 1):
            if sortedDeck[i].getValue() + 1 == sortedDeck[i+1].getValue(): 
                inSeries += 1
            else:
                inSeries = 0

        if inSeries >= 4:  # If there are 5 cards in series
            return True

        # check for Ace low straight
        for card in sortedDeck:
            if card.getValue() == 14:  # 14 is the normal value for Ace, doesnt need resetting as cards are binned afterwards
                card.setValue(1)

        reSortedDeck = sorted(sortedDeck, key=lambda card: card.getValue())
        inSeries = 0

        for i in range(len(reSortedDeck) - 1):
            if reSortedDeck[i].getValue() + 1 == reSortedDeck[i+1].getValue(): 
                inSeries += 1
            else:
                inSeries = 0
        print(inSeries)
        if inSeries >= 4:  # If there are 5 cards in series  
            return True

        return False
    
             

class Dealer(): #dealer class for creating decks

    def makeStandardDeck(self):   #makes a standard deck
        deck = Deck()
        suitList = ["spades","hearts","diamonds","clubs"]
        rankList = ["ace","2","3","4","5","6","7","8","9","10","jack","queen","king"]
        for suit in suitList:
            for rank in rankList:
                card = Card(suit,rank)
                deck.addCard(card)
        return deck

                                   






