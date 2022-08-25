import sys
from constants import * 
from paddle import AiPaddle, Paddle
from ball import Ball
from button import * 

class Game:
    def __init__(self, paddle_vel=4, ball_vel=5, ai_agent=True):
        Paddle.VEL = paddle_vel
        Ball.INIT_VEL = ball_vel
        
        self.ai_agent = ai_agent

        if ai_agent:
            self.left_paddle = AiPaddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        else:
            self.left_paddle  = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        
        self.right_paddle  = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)    
        self.left_score = 0
        self.right_score = 0
        self.won = False
    
    def increase_ball_vel(self):
        self.ball.increase_vel()
        
    def increase_paddles_vel(self):
        self.left_paddle.increase_vel()
        self.right_paddle.increase_vel()
    
    def draw(self, win, score_font):
        win.fill(BLACK) # draw background

        self.ball.draw(win) # draw ball

        for i in range(10, HEIGHT, HEIGHT//20): # drawing the dots in the middle which are small rectangles
            if i % 2 == 1:
                continue
            pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20)) # width of the rect is 5, we start it not right in the middle, but minus 5

        left_score_text = score_font.render(f"{self.left_score}", 1, WHITE)
        win.blit(left_score_text, (WIDTH * (1/4) - left_score_text.get_width()//2, 20))
        
        """
        TODO: Draw the right score
        Hint: This is similar to the left score, but be careful of the coordinates  
        """
        right_score_text = score_font.render(f"{self.right_score}", 1, WHITE)
        win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))
        """
        TODO: Go to the function draw_paddles() and draw the paddles 
        """
        self.draw_paddles(win)

        
        
        
        if self.won:
            text = score_font.render(self.win_text, 1, WHITE)
            _, _, text_w, text_h = text.get_rect()
            
            text_y = HEIGHT//2 - text.get_height() // 2
            
            if 'left' in self.win_text.lower():
                text_x = WIDTH//4 - text.get_width()//2
                win.blit(text, (text_x, text_y))
                
            else:
                text_x = int(0.75 * WIDTH) - text.get_width()//2
                win.blit(text, (text_x, text_y))
            
            if len(buttons) == 0:
                _ = Button((text_x + 50, text_y + 80, text_w, text_h), "PLAY AGAIN!", 30, command=lambda: self.reset(), colors="white on black", hover_colors="black on white", borderc=(255,255,255))
                _ = Button((text_x + 50, text_y + 200, text_w, text_h), "QUIT!", 30, command=lambda: self.quit(), colors="white on black", hover_colors="black on white", borderc=(255,255,255))
            buttons.update(win)    
            buttons.draw(win)

    def draw_paddles(self, win):
        """
        TODO: For each of the paddles (right and left) use the paddle.draw() function.
        """
        paddles = [self.left_paddle, self.right_paddle]
        for paddle in paddles:
            paddle.draw(win)

    def handle_collision(self):
        # collision with border
        if self.check_border_collision():
            """
            TODO: Implement the logic if the ball hits the border

            To complete this, you need to also fill the following function:
            check_border_collision()

            Hint: If the ball hits the wall, change y direction of the ball 
            """
            self.ball.y_vel *= -1 # change y direction of the ball when ball hits wall
        else:
            """
            TODO: Implement the logic in the case where the ball hits the paddle
            - Check which way the ball is going to decide with which paddle you are colliding with
            - If the ball goes to the left, check if it collides with the left paddle and then update ball velocity
            - Similarly, if the ball goes to the right, check if it collides with the right paddle and then update ball velocity

            To complete this, you need to also fill the following functions:
            check_collision_paddle_left()
            check_collision_paddle_right()
            handle_ball_vel()
            """
            
            if self.ball.x_vel < 0: # check if which way the ball is going to decide with which paddle you colliding
                if self.check_collision_paddle_left():
                    self.handle_ball_vel(self.left_paddle)
            else:
                if self.check_collision_paddle_right():
                    
                    self.handle_ball_vel(self.right_paddle)                    
            
        self.increase_game_vel()       

    def increase_game_vel(self):
        if (self.left_paddle.hits + 1) % 5 == 0:         
                self.increase_ball_vel()
                self.increase_paddles_vel() 

    def handle_ball_vel(self, paddle: Paddle):
        """
        TODO: Implement the change of the ball's velocity
        Update the paddle.hits variable
        Change the x velocity of the ball
        Change the y velocity of the ball
        """
        paddle.hits += 1
        self.ball.x_vel *= -1
        
        reduction_factor = (PADDLE_HEIGHT / 2) / abs(self.ball.x_vel)
        middle_y = paddle.y + paddle.height / 2
        difference_in_y = middle_y - self.ball.y
        y_vel = difference_in_y / reduction_factor
        self.ball.y_vel = -1 * y_vel
        
    def check_collision_paddle_left(self):
        if self.ball.y >= self.left_paddle.y and self.ball.y < self.left_paddle.y + self.left_paddle.height:
            if self.ball.x - self.ball.radius <= self.left_paddle.x + self.left_paddle.width:
                return True
        return False
    
    def check_collision_paddle_right(self):
        """
        TODO: Implement condition logic to check if the ball collided with left paddle
        Hint: Be careful of the coordinates of the ball circumference and the right paddle borders
        """
        if self.ball.y >= self.right_paddle.y and self.ball.y < self.right_paddle.y + self.right_paddle.height:
            if self.ball.x + self.ball.radius >= self.right_paddle.x:
                return True
        return False

    
    def check_border_collision(self):
        """
        TODO: Complete the function check_collision_border_down()
        """
        return self.check_collision_border_up() or self.check_collision_border_down()
    
    def check_collision_border_up(self):
        if self.ball.y - self.ball.radius <= 0:
            return True
        return False

    def check_collision_border_down(self):
        """
        TODO: Implement condition logic to check if the ball collided with border up
        """
        if self.ball.y + self.ball.radius >= HEIGHT:
            return True
        return False

    def check_score(self):
        if self.ball.x < 0:
            self.right_score += 1
            self.ball.reset()
        elif self.ball.x > WIDTH:
            self.left_score += 1
            self.ball.reset()

    def check_winning(self):
        if self.left_score >= WINNING_SCORE:
            self.win_text = "Left Player Won!"
            self.won = True
        elif self.right_score >= WINNING_SCORE:
            self.won = True
            self.win_text = "Right Player Won!"
        
    def reset(self):
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.won = False
        self.win_text = None
        
    def quit(self):
        pygame.quit()
        sys.exit()
        