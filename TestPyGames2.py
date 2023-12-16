'''
Implementing start button along with points and allowed incorect 
Introduced decay in timeLimit based on points
Organized by classes and functions
Along with point display at the end 
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
        pygame.display.set_caption("Random Letter Display")

        self.font = pygame.font.Font(None, 100)
        # Load button images 
        start_img = pygame.image.load('start_btn.png').convert_alpha()

        # Calculate the starting position to center the button
        button_x = (width - start_img.get_width()) // 2
        button_y = (height - start_img.get_height()) // 2

        # Button instance
        self.start_button = Button(button_x, button_y, start_img)
        self.button_clicked = False  # Flag to indicate whether the button has been clicked

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

    def is_button_clicked(self, pos):
        if not self.button_clicked and self.start_button.rect.collidepoint(pos):
            self.button_clicked = True  # Set the flag to indicate that the button has been clicked
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

    def get_random_letter(self):
        return chr(random.randint(65, 90))

    def wait_for_input(self, letter, timeout):
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
                    else:
                        print("Incorrect!")
                        self.incorrect_tries += 1  # Increment the counter for incorrect tries
                        waiting_for_input = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.display.is_button_clicked(event.pos):
                            print("Button Clicked!")
                            self.game_started = True  # Set the flag to indicate that the game has started
                            return  # Exit the function if the button is clicked

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
                            print("Button Clicked!")
                            self.game_started = True  # Set the flag to indicate that the game has started

            self.display.draw_button()
            pygame.display.flip()
            self.clock.tick(30)

        # Proceed to the actual game loop
        while True:
            letter = self.get_random_letter()
            self.display.display_letter(letter)
            if self.points == 0:
                timeLimit = 5000
                self.wait_for_input(letter, timeLimit)
            else:
                # Set baseTime and decayRate 
                baseTime = 5000
                decayRate = 0.1  # Adjust this value based on the desired rate of decrease

                # Calculate timeLimit based on an exponential decrease
                timeLimit = max(500, int(baseTime * math.exp(-decayRate * self.points)))
                print("Time limit: ", timeLimit)
                self.wait_for_input(letter, timeLimit)

            pygame.time.delay(800)  # Pause for a short time before the next letter

            # Check if the player has reached 10 incorrect tries
            if self.incorrect_tries >= 10:
                # Display points in the middle of the screen
                self.display.screen.fill((0, 0, 0))  # Black background
                text_surface = self.display.font.render(f"Points: {self.points}", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.display.width // 2, self.display.height // 2))
                self.display.screen.blit(text_surface, text_rect)
                pygame.display.flip()

                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

if __name__ == "__main__":
    game = LetterGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.play_game()
