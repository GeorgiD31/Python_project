import pygame
import random
import sys
import os
import time

# f checks which fruit has to spawn and stops the rest from spawning
# chance determines which fruit spawns
global score
global chance
global f
global game_over_check

game_over_check = False
f = 0
score = 0
chance = random.randint(0, 10)


class Snake:

    def __init__(self):
        self.body = [[5, 10], [6, 10], [7, 10]]
        self.direction = [0, 1]

    def draw(self):
        for part in self.body:
            part_draw = pygame.Rect(part[0] * grid_space_size, part[1] * grid_space_size, grid_space_size, grid_spaces)
            pygame.draw.rect(screen, (40, 40, 40), part_draw)

    def move(self):
        if self.direction[0] != 0 or self.direction[1] != 0:
            self.body.pop()
            self.body.insert(0, [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]])

    # adds 1 more part to the length of the snake
    def add(self):
        self.body.insert(0, [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]])

    def collision_with_body(self):

        global score
        global game_over_check

        for part in range(1, len(self.body)):
            if self.body[part] == self.body[0]:
                game_over_check = True
                break

    def wall_collision(self):
        global score
        global game_over_check

        if self.body[0][0] < 0 or self.body[0][0] >= grid_spaces:
            game_over_check = True

        if self.body[0][1] < 0 or self.body[0][1] >= grid_spaces:
            game_over_check = True


class Fruit:

    def __init__(self):
        self.x = random.randint(0, grid_spaces - 1)
        self.y = random.randint(0, grid_spaces - 1)
        self.color = (254, 95, 85)
        self.position = [self.x, self.y]
        self.score_given = 1

    def draw(self):

        fruit = pygame.Rect(self.position[0] * grid_spaces, self.position[1] * grid_spaces, grid_space_size,
                            grid_space_size)
        pygame.draw.rect(screen, self.color, fruit)


class SpeedFruit(Fruit):

    def __init__(self):
        Fruit.__init__(self)
        self.score_given = 2
        self.color = (255, 100, 0)
        Fruit.draw(self)

    # adds 2 to the length of the snake and speeds it up until it has eaten the next fruit and also gives +2 score
    def powerup(self):
        pygame.time.set_timer(Screen_Update, 70)
        snake.add()


class ShorteningFruit(Fruit):

    def __init__(self):
        Fruit.__init__(self)
        self.score_given = 2
        self.color = (100, 100, 255)
        Fruit.draw(self)

    # shortens the length of the snake and slows it down until it has eaten another fruit
    def powerup(self):
        if len(snake.body) > 2:
            snake.body.pop()
        pygame.time.set_timer(Screen_Update, 190)

def collision_fruit():
    global score
    global chance
    global f

    # checks for a collision between the snake and the fruit and then gives the fruit
    # a new position if a collision has occurred while also ensuring that the new position is not inside the snake
    if snake.body[0] == apple.position and f == 0:

        score += apple.score_given
        apple.x = random.randint(0, grid_spaces - 1)
        apple.y = random.randint(0, grid_spaces - 1)
        for part in snake.body:
            if apple.x == part[0] and apple.y == part[1]:
                apple.x = random.randint(0, grid_spaces - 1)
                apple.y = random.randint(0, grid_spaces - 1)

        apple.position = [apple.x, apple.y]
        chance = random.randint(0, 10)
        pygame.time.set_timer(Screen_Update, 120)
        snake.add()

    if snake.body[0] == apple2.position and f == 1:

        score += apple2.score_given
        apple2.x = random.randint(0, grid_spaces - 1)
        apple2.y = random.randint(0, grid_spaces - 1)
        for part in snake.body:
            if apple2.x == part[0] and apple2.y == part[1]:
                apple2.x = random.randint(0, grid_spaces - 1)
                apple2.y = random.randint(0, grid_spaces - 1)
        apple2.position = [apple2.x, apple2.y]
        chance = random.randint(0, 10)
        apple2.powerup()
        snake.add()

    if snake.body[0] == apple3.position and f == 2:

        score += apple3.score_given
        apple3.x = random.randint(0, grid_spaces - 1)
        apple3.y = random.randint(0, grid_spaces - 1)
        for part in snake.body:
            if apple3.x == part[0] and apple3.y == part[1]:
                apple3.x = random.randint(0, grid_spaces - 1)
                apple3.y = random.randint(0, grid_spaces - 1)
        apple3.position = [apple3.x, apple3.y]
        chance = random.randint(0, 10)
        apple3.powerup()


    return score


def score_print():

    global score
    # Displays the score on the screen
    font = pygame.font.Font('freesansbold.ttf', 24)
    text_score = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text_score, (10, 10))


def game_over():
    global score

    # resets everything to the starting value
    snake.body = [[5, 10], [6, 10], [7, 10]]
    snake.direction = [0, 1]
    apple.x = random.randint(0, grid_spaces - 1)
    apple.y = random.randint(0, grid_spaces - 1)
    apple.position = [apple.x, apple.y]
    apple2.x = random.randint(0, grid_spaces - 1)
    apple2.y = random.randint(0, grid_spaces - 1)
    apple2.position = [apple2.x, apple2.y]
    apple3.x = random.randint(0, grid_spaces - 1)
    apple3.y = random.randint(0, grid_spaces - 1)
    apple3.position = [apple3.x, apple3.y]
    score = 0
    pygame.time.set_timer(Screen_Update, 120)


def save_game():
    global score
    # Saves the coordinates of each of the snake's body parts as well as it's direction and the score
    # The direction and score are the last 3 numbers in the saved line (direction last 2 and score the previous one)
    with open("Snake_Saves.txt", "a+") as file:
        for part in snake.body:
            for number in part:
                file.write(str(number) + " ")
        file.write(str(score) + " ")
        for digit in snake.direction:
            file.write(str(digit) + " ")
        file.write("\n")
    file.close()


def load_game(file_number):
    global score
    global game_over_check
    file_path = 'Snake_Saves.txt'
    if os.stat(file_path).st_size == 0:
        print('File is empty')
    else:
        pygame.time.set_timer(Screen_Update, 120)
        i = 0
        with open("Snake_Saves.txt", "r") as file:
            lines = file.readlines()
            if file_number <= len(lines):
                game_over_check = False
                snake.body = []
                if file_number != 0 :
                    line = lines[int(file_number)-1]
                else:
                    line = lines[int(file_number)]

                number_list = line.split()
                while i < (len(number_list) - 3):
                    snake.body.append([int(number_list[i]), int(number_list[i + 1])])
                    i += 2
                score = int(number_list[len(number_list)-3])
            else:
                print("Wrong input no such save")
        file.close()


def leaderboard():
    score_list = []
    file_path = 'Snake_Saves.txt'
    # checks if the file is empty
    if os.stat(file_path).st_size == 0:
        print('No current saves')

    with open("Snake_Saves.txt", "r") as file:
        lines = file.readlines()
        # fills a list with all the scores
        for line in lines:
            number_list = line.split()
            local_score = int(number_list[len(number_list)-3])
            score_list.append(local_score)

        score_list.sort(reverse=True)
        # checks for the 10 highest scores and if there are less than 10 it displays all the scores in descending order
        if len(score_list) > 10:
            for i in range(0, 10):
                print("Top score {0}: {1}".format((i + 1), score_list[i]))
        else:
            for i in range(0, len(score_list)):
                print("Top score {0}: {1}".format((i + 1), score_list[i]))


# Sets up the playing space
grid_space_size = 25
grid_spaces = 25

pygame.init()
screen = pygame.display.set_mode((grid_space_size * grid_spaces, grid_space_size * grid_spaces))

clock = pygame.time.Clock()

apple = Fruit()
apple2 = SpeedFruit()
apple3 = ShorteningFruit()
snake = Snake()

Screen_Update = pygame.USEREVENT
pygame.time.set_timer(Screen_Update, 120)

# The game will crash if the file is empty but has a \n added
# The file must either be completely empty with only one single line in it or have something saved
leaderboard()
while True:
    row = 0
    pygame.display.set_caption('Snake')
    screen.fill((104,115,122))
    grass_color = (120, 137, 143)
    for row in range(grid_spaces):
        if row % 2 == 0:
            for column in range(grid_spaces):
                if column % 2 == 0:
                    grass_rect = pygame.Rect(column * grid_space_size, row * grid_space_size, grid_space_size,
                                             grid_space_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
                else:
                    grass_rect = pygame.Rect(column * grid_space_size, (row + 1) * grid_space_size, grid_space_size,
                                             grid_space_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    snake.draw()

    if chance < 6:
        apple.draw()
        f = 0
    elif chance >= 6 and chance < 9:
        apple2.draw()
        f = 1
    else:
        apple3.draw()
        f = 2
    # Displays a message to tell the player to move if he has loaded a file
    if snake.direction[0] == 0 and snake.direction[1] == 0:
        font_resume_play = pygame.font.Font('freesansbold.ttf', 32)
        text_resume_play = font_resume_play.render("Move to start playing", True, (255, 255, 255))
        text_rect3 = text_resume_play.get_rect(center=((grid_space_size * grid_spaces) / 2,((grid_space_size * grid_spaces) / 2)))
        screen.blit(text_resume_play, text_rect3)

    score_print()
    pygame.display.update()
    clock.tick(60)
    if game_over_check is False:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == Screen_Update:
                snake.move()

            if event.type == pygame.KEYDOWN:

                # MOVEMENT
                # Moves the snake in different directions with the arrows

                if event.key == pygame.K_UP:
                    if snake.body[1][1] != snake.body[0][1] - 1:
                        snake.direction[1] = -1
                        snake.direction[0] = 0

                if event.key == pygame.K_RIGHT:
                    if snake.body[1][0] != snake.body[0][0] + 1:
                        snake.direction[0] = 1
                        snake.direction[1] = 0

                if event.key == pygame.K_DOWN:
                    if snake.body[1][1] != snake.body[0][1] + 1:
                        snake.direction[1] = 1
                        snake.direction[0] = 0

                if event.key == pygame.K_LEFT:
                    if snake.body[1][0] != snake.body[0][0] - 1:
                        snake.direction[0] = -1
                        snake.direction[1] = 0

                # Saves the game when S is pressed
                if event.key == pygame.K_s:
                    save_game()
                # loads the last save
                # others saves can be accessed when the game is over
                # You have to press a button to move after loading a file
                if event.key == pygame.K_l:
                    snake.direction = [0, 0]
                    load_game(1)
        snake.collision_with_body()
        snake.wall_collision()
        collision_fruit()

    else:

        while game_over_check:
            #displays a message if the player has lost the game
            pygame.display.update()
            font_Game_over = pygame.font.Font('freesansbold.ttf', 32)
            font_resume = pygame.font.Font('freesansbold.ttf', 22)
            text_over = font_Game_over.render("Game Over", True, (255, 255, 255))
            text_resume = font_resume.render("Press Space to continue", True, (255, 255, 255))
            text_rect = text_over.get_rect(center=((grid_space_size * grid_spaces) / 2,
                                                   (grid_space_size * grid_spaces) / 2))
            text_rect2 = text_over.get_rect(center=((grid_space_size * grid_spaces) / 2 - 40,
                                                    ((grid_space_size * grid_spaces) / 2)+40))
            screen.blit(text_over, text_rect)
            screen.blit(text_resume, text_rect2)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    # resets the game
                    if event.key == pygame.K_SPACE:
                        game_over()
                        game_over_check = False

                    # loads a save
                    if event.key == pygame.K_l:
                        # Enters which save will be loaded
                        # The save will have to be loaded through the terminal by typing the number of which save you
                        # want to load
                        # You have to press a button to move after loading a file
                        file_number = input("Enter number: ")
                        if file_number.isdigit() == True:
                            file_number = int(file_number)
                            time.sleep(5)
                            snake.direction = [0, 0]
                            load_game(file_number)
                        else:
                            print("Wrong input, you need to enter only digits")
