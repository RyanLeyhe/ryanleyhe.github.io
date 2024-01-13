import pygame, sys, asyncio

# game initialization
pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 800, 800 
screen = pygame.display.set_mode((screen_width, screen_height)) 

big_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

"""
# game variables
score = 0
top_score = 0
lives = 3
game_over = False
is_paused = False
"""

# timer
# current_seconds = 5
timer_text = big_font.render(f'Time: 5', True, 'White')
timer_text_rect = timer_text.get_rect()
timer_end_rect = pygame.Rect(250, 200, 400, 50)
# timer_start = True
pygame.time.set_timer(pygame.USEREVENT, 1000)

def pause():
    global is_paused
    is_paused = True

    while is_paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    is_paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill(('White'))
        message_to_screen_text1 = big_font.render('Paused', True, 'Blue')
        message_to_screen_text2 = small_font.render('Press C to continue or Q to quit', True, 'Blue')
        screen.blit(message_to_screen_text1, (320, 340))
        screen.blit(message_to_screen_text2, (230, 390))
        pygame.display.flip()  # Update the display
        clock.tick(60)  # Control frame rate (30 frames per second)

def bouncing_rect(game_state):
    game_state.moving_rect.x += game_state.xSpeed
    game_state.moving_rect.y += game_state.ySpeed

    # collision with screen borders
    if game_state.moving_rect.right >= screen_width or game_state.moving_rect.left <= 0:
        game_state.xSpeed *= -1
    if game_state.moving_rect.top <= 0:
        game_state.ySpeed *= -1
    if game_state.moving_rect.bottom >= screen_height:
        game_state.lives -= 1
        # pause()
        game_state.moving_rect.x, game_state.moving_rect.y = 350, 300
        if game_state.lives == 0:
            game_state.game_over = True
            game_state.xSpeed, game_state.ySpeed = 0, 0
            game_state.other_rect_speed = 0
        else:
            game_state.current_seconds = 5
            game_state.timer_start = True

    # moving other_rect
    game_state.other_rect.x += game_state.other_rect_speed
    if game_state.other_rect.right >= screen_width or game_state.other_rect.left <= 0:
        game_state.other_rect_speed *= -1
    if game_state.other_rect.left >= screen_width or game_state.other_rect.right <= 0:
        game_state.other_rect_speed *= -1

    # collision with other_rect
    collision_tolerance = 10
    if game_state.moving_rect.colliderect(game_state.other_rect):
        if abs(game_state.other_rect.top - game_state.moving_rect.bottom) < collision_tolerance and game_state.ySpeed > 0:
            game_state.ySpeed *= -1
            game_state.score += 1

        if abs(game_state.other_rect.bottom - game_state.moving_rect.top) < collision_tolerance and game_state.ySpeed < 0:
            game_state.ySpeed *= -1
            game_state.score += 1

        if abs(game_state.other_rect.right - game_state.moving_rect.left) < collision_tolerance and game_state.xSpeed < 0:
            game_state.xSpeed *= -1
            game_state.score += 1

        if abs(game_state.other_rect.left - game_state.moving_rect.right) < collision_tolerance and game_state.xSpeed > 0:
            game_state.xSpeed *= -1
            game_state.score += 1

"""
moving_rect = pygame.Rect(350, 350, 30, 30)
xSpeed, ySpeed = 5, 4

other_rect = pygame.Rect(300, 600, 200, 20)
other_rect_speed = 0

game_over_rect = pygame.Rect(275, 225, 250, 200)
# Calculate the border width
border_width = (215 - 200) // 2
# Create a blue border rectangle around the game_over_rect
game_over_border = pygame.Rect(game_over_rect.left - border_width,
                               game_over_rect.top - border_width,
                               game_over_rect.width + 2 * border_width,
                               game_over_rect.height + 2 * border_width)
"""

class GameState:
    def __init__(self):
        self.xSpeed, self.ySpeed = 5, 4
        self.other_rect_speed = 0
        self.lives = 3
        self.score = 0
        self.top_score = 0
        self.game_over = False
        self.is_paused = False
        self.current_seconds = 5
        self.timer_start = True

        self.moving_rect = pygame.Rect(350, 350, 30, 30)
        self.other_rect = pygame.Rect(300, 600, 200, 20)
        self.game_over_rect = pygame.Rect(275, 225, 250, 200)
        self.timer_end_rect = pygame.Rect(250, 200, 400, 50)

        # Calculate the border width
        border_width = (215 - 200) // 2
        # Create a blue border rectangle around the game_over_rect
        self.game_over_border = pygame.Rect(
            self.game_over_rect.left - border_width,
            self.game_over_rect.top - border_width,
            self.game_over_rect.width + 2 * border_width,
            self.game_over_rect.height + 2 * border_width
        )

async def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and game_state.timer_start:
                game_state.current_seconds -= 1
        
        # screen set up
        screen.fill((30, 30, 30))
        big_font = pygame.font.Font(None, 50)
        small_font = pygame.font.Font(None, 30)
        lives_text = small_font.render(f'Lives: {game_state.lives}', True, 'White')
        score_text = small_font.render(f'Score: {game_state.score}', True, 'White')
        screen.blit(lives_text, (10, 10))
        screen.blit(score_text, (10, 50))
        top_score_text = small_font.render(f'Best: {game_state.top_score}', True, 'White')
        screen.blit(top_score_text, (10, 90))

        # timer
        timer_text = big_font.render(f'Game starts in: {game_state.current_seconds}', True, 'White')
        screen.blit(timer_text, (250, 200))
        if game_state.current_seconds == 0:
            game_state.timer_start = False
            pygame.draw.rect(screen, (30, 30, 30), game_state.timer_end_rect)
            bouncing_rect(game_state)

        pygame.draw.rect(screen, (255, 255, 255), game_state.moving_rect)
        pygame.draw.rect(screen, 'White', game_state.other_rect)

        if game_state.is_paused:
            pause()

        if not game_state.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and game_state.other_rect.x > 0:
                game_state.other_rect.x -= 5
            if keys[pygame.K_RIGHT] and game_state.other_rect.x < screen_width - game_state.other_rect.width:
                game_state.other_rect.x += 5
            if keys[pygame.K_p]:
                pause()
        else:
            game_over_text = big_font.render('Game Over!', True, 'Blue')
            pygame.draw.rect(screen, 'Blue', game_state.game_over_border)
            pygame.draw.rect(screen, 'White', game_state.game_over_rect)
            screen.blit(game_over_text, (300, 300))
            restart_text = small_font.render('Press SPACE to restart', True, 'Blue')
            screen.blit(restart_text, (290, 350))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game_state.score = 0
                game_state.lives = 3
                game_state.game_over = False
                game_state.xSpeed, game_state.ySpeed = 5, 4
                game_state.other_rect_speed = 0
                game_state.moving_rect.x, game_state.moving_rect.y = 350, 300
                game_state.other_rect.x, game_state.other_rect.y = 300, 600
                game_state.current_seconds = 5
                game_state.timer_start = True
                if game_state.score > game_state.top_score:
                    game_state.top_score = game_state.score
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

if __name__ == "__main__":
    game_state = GameState()
    asyncio.run(main())