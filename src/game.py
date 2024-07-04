import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Crawler")
clock = pygame.time.Clock()
dt = 0


player_pos = pygame.Vector2(screen.get_width() / 2, 1000)
ball_pos = pygame.Vector2(screen.get_width() // 2, screen.get_height() //2)
ball_hb_pos = pygame.Vector2((screen.get_width() // 2) - 15 , (screen.get_height() //2) - 15)
ball_direction = pygame.Vector2(screen.get_width() / 2, 1080)


while True:
    for event in pygame.event.get(): #quit checker
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    screen.fill("black")

    paddle = pygame.Rect(player_pos,(80,20))
    ball_hitbox = pygame.Rect(ball_hb_pos, (30,30))
    pygame.draw.rect(screen, "white", paddle)

    pygame.draw.circle(screen, "white", ball_pos, 20)
    pygame.draw.rect(screen,"red", ball_hitbox)

    isMovingLeft = False
    ifMovingRight = False
    isStationary = True

    keys = pygame.key.get_pressed()  
    if keys[pygame.K_a]:
        if player_pos.x >= 20:
            player_pos.x -= 500 * dt
            isMovingLeft = True
    if keys[pygame.K_d]:
        if player_pos.x <= 1840:
            player_pos.x += 500 * dt
            isMovingRight = True

    if ball_hitbox.colliderect(paddle):
        ball_direction = pygame.Vector2(screen.get_width() / 2, 10)
    if ball_hitbox.y <= 1:
        ball_direction = pygame.Vector2(screen.get_width() / 2, 1080)
    if ball_hitbox.y >= (screen.get_height() - 50):
        pygame.quit()
        exit()       
    
    ball_pos = ball_pos.move_towards(ball_direction, 5)
    ball_hb_pos.x = ball_pos.x - 15
    ball_hb_pos.y = ball_pos.y - 15

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()