import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Random Letter Display")

# Set up fonts
font = pygame.font.Font(None, 100)

# Function to get a random letter
def get_random_letter():
    return chr(random.randint(65, 90))

# Points counter
points = 0
    
# Main game loop
while True:  
    # Get a random letter
    letter = get_random_letter()
    
    # Clear the screen
    screen.fill((0, 0, 0))

    # Render the letter
    text_surface = font.render(letter, True, (255, 255, 255))

    # Get a random position for the letter
    x_pos = random.randint(0, width - text_surface.get_width())
    y_pos = random.randint(0, height - text_surface.get_height())
    
    # Get the position to center the letter on the screen
    text_rect = text_surface.get_rect(topleft=(x_pos, y_pos))

    # Blit the letter onto the screen
    screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

    # Wait for user input
    waiting_for_input = True
    while waiting_for_input:   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Check if the pressed key matches the displayed letter
                    if event.unicode.isalpha() and event.unicode.upper() == letter:
                        print("Correct!")
                        points += 1
                        waiting_for_input = False  
                # Chec1k if the user pressed the escape key (end game)
                    elif event.key == pygame.K_ESCAPE:
                        waiting_for_input = False
                        pygame.quit()
                        # print('points is:', points)
                        sys.exit()
                    else:
                        print("Incorrect!") 
                        waiting_for_input = False  
                

    # Pause for a short time to show the correct letter before moving on
	# Pause before displaying next letter, but gets fater as points increase
    delayTime = 0
    if points == 0:
         delayTime = 1000
         pygame.time.delay(delayTime)
    else:
         if delayTime <= 600:
            pygame.time.delay(600)  
            waiting_for_input = False
         else:
             delayTime = 600 - (points * 10)
             pygame.time.delay(1000)
             #print('Delay time is', delayTime)
# This part will not be reached in this example, but it's good practice to include
pygame.quit()
sys.exit()