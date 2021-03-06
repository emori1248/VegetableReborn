
import random, os
import pygame


async def addCenteredTextToImage(content, size=30):

    # Check folders
    if not os.path.exists("img"):
        os.makedirs("img")
        return False # Images should never exist in a new folder

    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    # Set the environment variable to run SDL as headless
    os.putenv('SDL_VIDEODRIVER', 'dummy')

    pygame.init()
    WIDTH = 1920
    HEIGHT = 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont("Arial", size, bold=False, italic=True)

    # Grab and set a random background

    images = os.listdir("img")
    if (len(images) <= 0):
        return False
    imagedir = random.choice(os.listdir("img"))
    bg = pygame.image.load("img/" + imagedir)
    bg = pygame.transform.scale(bg, (1920, 1080))

    screen.blit(bg, (0, 0))
    text = font.render(content, 1, pygame.Color("black"))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)


    pygame.display.update()
    pygame.image.save(screen, "tmp/output.jpg")
    
    pygame.quit()
    return True