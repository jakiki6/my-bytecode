red, green, blue = 0, 0, 0
x, y = 0, 0

width, height = 640, 480

initialized = False
screen = None

def init():
    import pygame
    global pygame
    global initialized, screen

    screen = pygame.display.set_mode((width, height))

    initialized = True

def draw():
    global initialized, screen
    if not initialized:
        init()

#    print((x, y), (red, green, blue))

    screen.set_at((x, y), (red, green, blue))

def refresh():
    global initialized, screen
    if not initialized:
        init()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    pass

def init_regs():
    global red, green, blue, x, y
    red, green, blue = 0, 0, 0
    x, y = 0, 0

def wipe():
    pass

def get_mouse():
    global initialized
    if not initialized:
        init()

    global pygame
    return pygame.mouse.get_pos()
