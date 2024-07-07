import pygame
from sys import exit
import random
from card import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1920, 1080))       #init pygame and create screen
pygame.display.set_caption("Crawler")
clock = pygame.time.Clock()
dt = 0

mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) # set the mouse pos to mouse

dealer = Dealer()
deck = dealer.makeStandardDeck()
hand = Deck()
playArea = Deck()                                                   #build the deck and shuffle it, assign assets
deck.shuffle()
for card in deck:
    card.setImage(pygame.image.load(f"./crawler/assets/{card.getRank()}_of_{card.getSuit()}.png"))
    card.getImage().convert()
    card.setRect(card.getImage().get_rect())

playButton = pygame.image.load("./crawler/assets/button_play.png")
playRect = playButton.get_rect()                                                     #make the play button
playRect.center = (screen.get_width() * 0.08, screen.get_height() * 0.85)

discardButton = pygame.image.load("./crawler/assets/button_discard.png")
discardRect = playButton.get_rect()                                                     #make the play button
discardRect.center = (screen.get_width() * 0.068, screen.get_height() * 0.92)

cardSound = pygame.mixer.Sound("./crawler/assets/cardDown.mp3")
pushSound = pygame.mixer.Sound("./crawler/assets/push.mp3")                           #load some sounds
victorySound = pygame.mixer.Sound("./crawler/assets/victory.mp3")
gameoverSound = pygame.mixer.Sound("./crawler/assets/gameover.mp3")

played = False
gameState = "draw"                                                                 #set initial variables outside of main loop



while True: #main loop
    for event in pygame.event.get(): #quit checker
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((20, 74, 34)) #refresh the background
    screen.blit(playButton, playRect)
    screen.blit(discardButton, discardRect)

    mouse = pygame.Rect(mousePos, (10,10)) #update the mouse hitbox
    mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) #update mouse position     
    currentlyPressed = pygame.mouse.get_pressed()[0] #check if buttoin is pressed

    if gameState == "draw": #drawing hand and setting positions
        if (deck.getDeckSize() + len(hand)) < 7:
            gameOverImage = pygame.image.load("./crawler/assets/gameover.png")
            gameOverRect = gameOverImage.get_rect()
            gameOverRect.center = (screen.get_width() / 2, screen.get_height() / 2)
            screen.blit(gameOverImage,gameOverRect)
            pygame.display.update()
            gameoverSound.play()
            pygame.time.delay(2500)
            pygame.quit()
            exit()

        while len(hand) < 7:
            hand.addCard(deck.draw())
        pusher = 0.0
        for card in hand: 
            card.getRect().center = (screen.get_width() * 0.20) + pusher, screen.get_height() * 0.85
            pusher = pusher + 200.0
        numSelected = 0
        gameState = "play"

    if gameState == "play": #player is allowed to select cards, if cards are selected and the play button is hit this state ends

        if mouse.colliderect(playRect) and currentlyPressed and not previouslyPressed: #if play butotn is pressed, check if cards are selected. if so play them. 
            handCopy = []
            handCopy = list(hand) #create a copy of the hand to avoid issues removing whilst iterating
            for card in handCopy:    
                if card.getSelected():
                    played = True
                    playArea.addCard(card)
                    hand.remove(card)
            for card in playArea:
                card.setBlit(True)

            if played == True:
                gameState = "evaluate"
                played = False


        if mouse.colliderect(discardRect) and currentlyPressed and not previouslyPressed: #if discard butotn is pressed,
            handCopy = list(hand)
            for card in handCopy:    
                if card.getSelected():
                    hand.remove(card)
            gameState = "draw"        
        
        
        
        for card in hand:            #draw the hand
            if card.getSelected():
                numSelected += 1
            if card.getBlit(): #when cards are first drawn blit with delay
                pygame.time.delay(175)
                screen.blit(card.getImage(), card.getRect())
                cardSound.play()
                pygame.display.update()
                card.setBlit(False)               
            else:
                screen.blit(card.getImage(), card.getRect()) #otherwise just blit

            if mouse.colliderect(card.getRect()) and currentlyPressed and not previouslyPressed: #if mouse is over the card and lclick
                numSelected = sum(1 for card in hand if card.getSelected())
                if card.getSelected(): #if its alreadt selected
                    card.getRect().y += 50
                    pushSound.play()
                    card.select() #unselects the card
                elif numSelected < 5: #otherwise select it
                    card.getRect().y -= 50
                    pushSound.play()
                    card.select()

    if gameState == "evaluate":   #check play area and score things
        
        pusher = 0.0
        for card in hand:
            screen.blit(card.getImage(), card.getRect())     #keep blitting the hand
        for card in playArea:             
            card.getRect().center = (screen.get_width() * 0.20) + pusher, screen.get_height() * 0.4         #blit the cards slowly first time
            pusher = pusher + 200.0 
            if card.getBlit():
                pygame.time.delay(175)
                screen.blit(card.getImage(), card.getRect())
                cardSound.play()
                pygame.display.update()
                card.setBlit(False)
                
            else: 
                screen.blit(card.getImage(), card.getRect())               #otherwise just blit
        scoreLogo = pygame.image.load(f"./crawler/assets/{playArea.evaluate()}.png")
        scoreRect = scoreLogo.get_rect()                                                     #make the play button
        scoreRect.center = (screen.get_width() / 2 , screen.get_height() / 2)
        screen.blit(scoreLogo,scoreRect)
        pygame.time.delay(175)
        victorySound.play()
        pygame.display.update()
        pygame.time.delay(800)
        playAreaCopy = list(playArea)
        for card in playAreaCopy:
            playArea.remove(card)
        gameState = "draw"

    previouslyPressed = currentlyPressed #stop mouse triggering every loop

    pygame.display.update() #update the display
    #pygame.display.flip() #???
    dt = clock.tick(60) / 1000 #delta time at 60fps

