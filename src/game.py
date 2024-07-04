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

image = pygame.image.load("./crawler/assets/EmptyCard.png") #load an image
image.convert() #convert image for quicker reading
image2 = pygame.image.load("./crawler/assets/EmptyCard2.png")
image2.convert()

#rect = image.get_rect() #get the rectangle of the image
#rect.center = screen.get_width() / 2, screen.get_height() /2 #put the card in the center

dealer = Dealer()
deck = dealer.makeStandardDeck()
hand = Deck()
x = 1
while x <= 7:
    hand.addCard(deck.draw())
    x += 1


i = 0.0
for card in hand:
    card.setImage(image)
    card.setRect(image.get_rect())
    card.getRect().center = (screen.get_width() * 0.20) + i, screen.get_height() * 0.85
    i = i + 200.0
    click = False


while True:
    for event in pygame.event.get(): #quit checker
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill((20, 74, 34)) #refresh the background

    currentlyPressed = pygame.mouse.get_pressed()[0]

    mouse = pygame.Rect(mousePos, (10,10)) #update the mouse hitbox
    mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) #update mouse position
    

    for card in hand:
        screen.blit(card.getImage(), card.getRect())
        if mouse.colliderect(card.getRect()) and currentlyPressed and not previouslyPressed: #if mouse is over the card and lclick
            #card.getRect().center = mousePos
            if card.getSelected():
                card.setImage(image)
                card.select()
            else:
                card.setImage(image2)
                card.select()

    previouslyPressed = currentlyPressed


    
    #screen.blit(image, rect) #draw the card
    #pygame.draw.rect(screen, "red", mouse) #draw the mouse hitbox


    

    pygame.display.update() #update the display
    #pygame.display.flip() #???
    dt = clock.tick(60) / 1000 #delta time at 60fps

