import pygame
from sys import exit
import random
from card import *

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Crawler")
clock = pygame.time.Clock()
dt = 0

mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) # set the mouse pos to mouse

dealer = Dealer()
deck = dealer.makeStandardDeck()
hand = Deck()
deck.shuffle()
for card in deck:
    card.setImage(pygame.image.load(f"./crawler/assets/{card.getRank()}_of_{card.getSuit()}.png"))
    card.getImage().convert()
    card.setRect(card.getImage().get_rect())
while len(hand) < 7:
    hand.addCard(deck.draw())
pusher = 0.0
for card in hand: 
    card.getRect().center = (screen.get_width() * 0.20) + pusher, screen.get_height() * 0.85
    pusher = pusher + 200.0


numSelected = 0

while True: #main loop
    for event in pygame.event.get(): #quit checker
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill((20, 74, 34)) #refresh the background

    mouse = pygame.Rect(mousePos, (10,10)) #update the mouse hitbox
    mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) #update mouse position
        
    currentlyPressed = pygame.mouse.get_pressed()[0]

    for card in hand:
        screen.blit(card.getImage(), card.getRect())
        if mouse.colliderect(card.getRect()) and currentlyPressed and not previouslyPressed: #if mouse is over the card and lclick
            #card.getRect().center = mousePos
            if card.getSelected():
                card.getRect().y += 50
                card.select()
                numSelected -= 1
            elif numSelected < 5:
                numSelected += 1
                card.getRect().y -= 50
                card.select()

    previouslyPressed = currentlyPressed #stop mouse triggering whilst held

    pygame.display.update() #update the display
    #pygame.display.flip() #???
    dt = clock.tick(60) / 1000 #delta time at 60fps

