'''
Version 4: 
Implementing difficulties
Final Version.
'''

import pygame
import sys
import random
import math

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("KeyAim Game")

        self.font = pygame.font.Font(None, 100)
        # Load button images 
        start_img = pygame.image.load('start_btn.png').convert_alpha()
        easy_img = pygame.image.load('easy_btn.png').convert_alpha()
        hard_img = pygame.image.load('hard_btn.png').convert_alpha()

        # Calculate the starting position to center the buttons
        button_width, button_height = start_img.get_width(), start_img.get_height()
        button_x = (width - button_width) // 2

        # Button instances
        self.start_button = Button(button_x - 5, 100, start_img)
        self.easy_button = Button(button_x - button_width + 150, 315, easy_img)
        self.hard_button = Button(button_x + button_width - 170, 315, hard_img)

        self.button_clicked = False  # Initialize the button_clicked attribute

    def display_letter(self, letter):
        self.screen.fill((0, 0, 0))  # Black background
        text_surface = self.font.render(letter, True, (255, 255, 255))
        x_pos = random.randint(0, self.width - text_surface.get_width())
        y_pos = random.randint(0, self.height - text_surface.get_height())
        text_rect = text_surface.get_rect(topleft=(x_pos, y_pos))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def draw_button(self):
        if not self.button_clicked:
            self.start_button.draw(self.screen)   
            self.easy_button.draw(self.screen)
            self.hard_button.draw(self.screen)      

    def get_clicked_button(self, pos):
        if self.start_button.rect.collidepoint(pos):
            print("Start button clicked!")
            return "start"
        elif self.easy_button.rect.collidepoint(pos):
            print("Easy button clicked!")
            return "easy"
        elif self.hard_button.rect.collidepoint(pos):
            print("Hard button clicked!")
            return "hard"
        else:
            return None
        
    def is_button_clicked(self, pos):
        if not self.button_clicked:
            if self.start_button.rect.collidepoint(pos):
                self.button_clicked = True  # Set the flag to indicate that the button has been clicked
                return True
            elif self.easy_button.rect.collidepoint(pos):
                self.button_clicked = True
                return True
            elif self.hard_button.rect.collidepoint(pos):
                self.button_clicked = True
                return True
        return False


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        # Draw button on the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))


class LetterGame:
    def __init__(self, width, height):
        pygame.init()

        self.display = Display(width, height)
        self.points = 0
        self.incorrect_tries = 0  # Counter for incorrect tries
        self.clock = pygame.time.Clock()
        self.game_started = False  # Flag to indicate whether the game has started

    def show_points(self):
        self.display.screen.fill((0, 0, 0))  # Black background
        text_surface = self.display.font.render(f"Points: {self.points}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.display.width // 2, self.display.height // 2))
        self.display.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def exit_game(self):
        # Let user exit the program by pressing escape
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()       

    def get_random_letter(self):
        return chr(random.randint(65, 90))
    
    def wait_for_input(self, letter, timeout): # This only runs when game starts 
        start_time = pygame.time.get_ticks()
        waiting_for_input = True

        while waiting_for_input and pygame.time.get_ticks() - start_time < timeout:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha() and event.unicode.upper() == letter:
                        print("Correct!")
                        self.points += 1
                        print("Points: ", self.points)
                        waiting_for_input = False
                    elif event.key == pygame.K_ESCAPE:
                        waiting_for_input = False
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                        self.show_points()
                        self.exit_game()
                    else:
                        print("Incorrect!")
                        self.incorrect_tries += 1  # Increment the counter for incorrect tries
                        waiting_for_input = False

            self.display.draw_button()
            pygame.display.flip()
            self.clock.tick(30)

        if waiting_for_input:
            print("Time's up! Incorrect!")
            self.incorrect_tries += 1 # Increment the counter for incorrect tries

    def play_game(self):
        # Show only the button when the game starts
        while not self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.display.is_button_clicked(event.pos):
                            button_pressed = self.display.get_clicked_button(event.pos)
                            print(f"Button Clicked: {button_pressed}") # Start of game and difficulty 
                            if button_pressed == "start":
                                self.difficulty = "normal"
                            elif button_pressed == "easy":
                                self.difficulty = "easy"
                            elif button_pressed == "hard":
                                self.difficulty = "hard"
                            self.game_started = True  # Set the flag to indicate that the game has started

            self.display.draw_button()
            pygame.display.flip()
            self.clock.tick(30)

        # Proceed to the actual game loop
        while True: # WHEN GAME STARTED 
            letter = self.get_random_letter()
            self.display.display_letter(letter)
            '''
            Start/Normal
            - Exponential decrease in time limit based on points (Decay rate is 0.1)
            - Incorrect ammount of tries before game over is 10 
            Easy
            - Constant timeLimit (of 3000)
            - Unlimited amount of tries 
            - Points are not counted when player pressed "Enter" IMPLEMENT LATER
            Hard
            - Exponential decrease in time limit based on points (Decay rate is 0.2) with a lower baseTime
            - Incorrect ammount of tries before game over is 5
            '''
            # Starter always has time limit as 5000 
            if self.points == 0: # Starter always as time limit 5000
                timeLimit = 5000
                self.wait_for_input(letter, timeLimit) # GOES TO WAIT INPUT AND CHECKS
            
            elif self.difficulty == "easy": # DONE But does not show points when "enter" is pressed 
                timeLimit = 3000
                print("Time limit: ", timeLimit)
                self.wait_for_input(letter, timeLimit)
            
            elif self.difficulty == "hard": # Decay works but does not end where user get 5 incorrect 
                # Set baseTime and decayRate 
                baseTime = 4000
                decayRate = 0.2  

                # Calculate timeLimit based on an exponential decrease
                timeLimit = max(500, int(baseTime * math.exp(-decayRate * self.points)))
                print("Time limit: ", timeLimit)
                self.wait_for_input(letter, timeLimit) # GOES TO WAIT INPUT AND CHECKS

            else: # setting for start/normal 
                # Set baseTime and decayRate 
                baseTime = 5000
                decayRate = 0.1  # Adjust this value based on the desired rate of decrease

                # Calculate timeLimit based on an exponential decrease
                timeLimit = max(700, int(baseTime * math.exp(-decayRate * self.points)))
                print("Time limit: ", timeLimit)
                self.wait_for_input(letter, timeLimit) # GOES TO WAIT INPUT AND CHECKS

            pygame.time.delay(800)  # Pause for a short time before the next letter


            # check when to end the game
            if self.difficulty == "easy":
                pass       
            
            elif self.difficulty == "hard": # works 
                if self.incorrect_tries >= 5:
                    # Display points in the middle of the screen
                    self.show_points()

                    self.exit_game()

            else: # Normal difficulty 
                # Display points in the middle of the screen
                if self.incorrect_tries >= 10:
                    self.show_points()

                    # Let user exit the program by pressing escape
                    self.exit_game()     


if __name__ == "__main__":
    game = LetterGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.play_game()
