import pygame
import random
import os
import playsound
pygame.init()


# colors
white = (122, 245, 147)
red = (255, 0, 0)
black = (0, 0, 0)
# Creating pygame window
screen_width = 800
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
#Background Image
backgimg = pygame.image.load('bg.jpg')
backgimg = pygame.transform.scale(backgimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((111, 104, 252))
        text_screen("Welcome To Snakes", black, 200, 220)
        text_screen("Press space bar to Play", black, 180, 270)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('background.mp3')
                    pygame.mixer.music.play()
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    exit_game = True

        pygame.display.update()
        clock.tick(60)

# Game Loop
def game_loop():
    # Game Specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 35
    velocity_x = 0
    velocity_y = 0

    food_x = random.randint(0, screen_width / 2)
    food_y = random.randint(0, screen_height / 2)
    score = 0
    init_velocity = 4
    snake_size = 23
    fps = 60

    snk_list = []
    snk_length = 1

    if (not os.path.exists("score.txt")):
        with open('score.txt', 'w') as f:
            f.write("0")
    with open("score.txt", 'r') as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            with open("score.txt",'w') as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            gameWindow.blit(backgimg, (0,0))
            text_screen("Game Over..!! press Enter to continue", red, 55, 270)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
                    if event.key == pygame.K_ESCAPE:
                        exit_game = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_ESCAPE:
                        welcome()

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<9 and abs(snake_y - food_y)<9:
                food_x = random.randint(0, screen_width / 2)
                food_y = random.randint(0, screen_height / 2)
                score += 10
                snk_length += 5
                if score>int(hiscore):
                    hiscore = score

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('exxplosion.mp3')
                pygame.mixer.music.play()
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('exxplosion.mp3')
                pygame.mixer.music.play()

            gameWindow.fill(white)
            gameWindow.blit(backgimg, (0,0))
            text_screen("Score: " + str(score) + "   Hiscore: " + str(hiscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
