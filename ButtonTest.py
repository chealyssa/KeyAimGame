import pygame 

SHeight = 900
SWidth = 1500

screen = pygame.display.set_mode((SWidth, SHeight))
pygame.display.set_caption("Button Test")

start_img = pygame.image.load('start_btn.png').convert_alpha()


# button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

start_button = Button(960, 540, start_img)


# game loop
run = True
while run:
    screen.fill((0, 0, 0))  # Black background

    start_button.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
