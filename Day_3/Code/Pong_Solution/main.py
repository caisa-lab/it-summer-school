import sys
from ball import Ball
from constants import *
from game import Game
from paddle import Paddle
import pygame
from button import *
pygame.init()
pygame.display.set_caption("Pong")

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def handle_paddle_movement(keys, game: Game):
    if keys[pygame.K_w] and game.left_paddle.y - game.left_paddle.VEL >= 0 : # check if you reached the borders
        game.left_paddle.move(up=True)
    if keys[pygame.K_s] and game.left_paddle.y + game.left_paddle.VEL + game.left_paddle.height <= HEIGHT: # take into account paddle height for the amount of movement
        game.left_paddle.move(up=False)
    """
    TODO: Make the right paddle move.
    Add here the conditions for the right paddle, moving with arrow keys up and down
    ...
    """
    if keys[pygame.K_UP] and game.right_paddle.y - game.right_paddle.VEL >= 0:
        game.right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and game.right_paddle.y + game.right_paddle.VEL + game.right_paddle.height <= HEIGHT:
        game.right_paddle.move(up=False)

    
def main():
    run = True
    clock = pygame.time.Clock() # relate the frames, so it can run the same everywhere
    AI_AGENT = False
    game = Game(paddle_vel=20, ball_vel=10, ai_agent=AI_AGENT)

    # main event loop that controls the game, and handles everything
    while run:
        clock.tick(FPS)
        
        game.check_winning()
        """
        TODO: Go into the game.draw function and draw the right score and the paddles
        """
        game.draw(WIN, SCORE_FONT)    
            
             
        for event in pygame.event.get(): # looping through the all different events like clicking, typing etc
            if event.type == pygame.QUIT: # if hit quit window
                run = False
                break

        if not game.won:
            buttons.empty()            
            keys = pygame.key.get_pressed()
            """
            TODO: Go into the function handle_paddle_movement() and implement how the right paddle moves.
            """
            handle_paddle_movement(keys, game)
            

            game.ball.move()
            """
            TODO: Go into the function handle_collision() and implement the logic and the corresponding functions that handle the collision.
            """
            game.handle_collision()

            game.left_paddle.predict(game.ball)

            game.check_score()

        pygame.display.update()

    
    game.quit()


if __name__ == '__main__':
    main()