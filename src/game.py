import pygame
from sys import exit
import random
from card import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Crawler")
clock = pygame.time.Clock()
dt = 0

mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) # set the mouse pos to mouse

dealer = Dealer()
deck = dealer.makeStandardDeck()
hand = Deck()
playArea = Deck()
deck.shuffle()
for card in deck:
    card.setImage(pygame.image.load(f"./crawler/assets/{card.getRank()}_of_{card.getSuit()}.png"))
    card.getImage().convert()
    card.setRect(card.getImage().get_rect())

previous_time = pygame.time.get_ticks()

playButton = pygame.image.load("./crawler/assets/playButton.png")
playRect = playButton.get_rect()
playRect.center = (screen.get_width() * 0.08, screen.get_height() * 0.85)

cardSound = pygame.mixer.Sound("./crawler/assets/cardDown.mp3")
pushSound = pygame.mixer.Sound("./crawler/assets/push.mp3")

played = False
gameState = "draw"


while True: #main loop
    for event in pygame.event.get(): #quit checker
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((20, 74, 34)) #refresh the background
    screen.blit(playButton, playRect)

    mouse = pygame.Rect(mousePos, (10,10)) #update the mouse hitbox
    mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) #update mouse position     
    currentlyPressed = pygame.mouse.get_pressed()[0]

    if gameState == "draw":
        while len(hand) < 7:
            hand.addCard(deck.draw())
        pusher = 0.0
        for card in hand: 
            card.getRect().center = (screen.get_width() * 0.20) + pusher, screen.get_height() * 0.85
            pusher = pusher + 200.0
        numSelected = 0
        gameState = "play"

    if gameState == "play":

        if mouse.colliderect(playRect) and currentlyPressed and not previouslyPressed:
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

        numSelected = 0
        for card in hand:
            if card.getSelected():
                numSelected += 1
            if card.getBlit():
                pygame.time.delay(200)
                screen.blit(card.getImage(), card.getRect())
                cardSound.play()
                pygame.display.update()
                card.setBlit(False)               
            else:
                screen.blit(card.getImage(), card.getRect())
            if mouse.colliderect(card.getRect()) and currentlyPressed and not previouslyPressed: #if mouse is over the card and lclick
                #card.getRect().center = mousePos
                if card.getSelected():
                    card.getRect().y += 50
                    pushSound.play()
                    card.select()
                elif numSelected < 5:
                    card.getRect().y -= 50
                    pushSound.play()
                    card.select()


    if gameState == "evaluate":
        pusher = 0.0


        for card in hand:
            screen.blit(card.getImage(), card.getRect())
        
        for card in playArea:
             
            card.getRect().center = (screen.get_width() * 0.20) + pusher, screen.get_height() * 0.4
            pusher = pusher + 200.0 
            if card.getBlit():
                pygame.time.delay(200)
                screen.blit(card.getImage(), card.getRect())
                cardSound.play()
                pygame.display.update()
                card.setBlit(False)
                
            else:
                screen.blit(card.getImage(), card.getRect())    


        

    previouslyPressed = currentlyPressed #stop mouse triggering whilst held

    pygame.display.update() #update the display
    #pygame.display.flip() #???
    dt = clock.tick(60) / 1000 #delta time at 60fps

