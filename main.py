import pygame
from pygame.locals import *
import pygameMenu
from pygameMenu.locals import *
import os 
from game import Game
from algorithms import (AlgorithmMenu, AlgorithmShow)

# Global Variables
CURRENT_STATE = 'MENU' # Can be 'INGAME'
GAME = None

# Global Constants
# -----------------------------------------------------------------------------
## Graphics Related
COLOR_BACKGROUND = [15,125,117]
FPS = 60
H_SIZE = 650  # Height of window size
W_SIZE = 880  # Width of window size
## Game Related
NUMBER_OF_MAPS = 20
MAP = [1]
ALGORITHM = ['DFS']

## Fill map menu array.
MAP_MENU_ARRAY = []
for x in range(1, NUMBER_OF_MAPS + 1):
    MAP_MENU_ARRAY.append((str(x), x))

# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Main timer and game clock
clock = pygame.time.Clock()

# Create window
surface = pygame.display.set_mode((W_SIZE, H_SIZE))
pygame.display.set_caption('Bloxorz Menu')


# -----------------------------------------------------------------------------
# Main menu, pauses execution of the application
menu = pygameMenu.Menu(surface,
                       dopause=False,
                       enabled=False,
                       font=pygameMenu.fonts.FONT_NEVIS,
                       menu_alpha=90,
                       onclose=PYGAME_MENU_DISABLE_CLOSE,
                       title='Bloxorz Menu',
                       title_offsety=5,
                       window_height=H_SIZE,
                       window_width=W_SIZE
                       )


def change_map(value):
    MAP[0] = value


def change_algorithm(value):
    ALGORITHM[0] = value


# -----------------------------------------------------------------------------
# Free Play Select Map Menu

def free_play_map_chosen_function():
    global GAME, CURRENT_STATE
    menu.disable()
    menu.reset(5)
    surface.fill(COLOR_BACKGROUND)
    GAME = Game(surface, H_SIZE, W_SIZE, MAP[0], True)
    CURRENT_STATE = 'INGAME'
    pygame.mixer.music.load('assets/tetris.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)

    

free_play_menu = pygameMenu.Menu(surface,
                                dopause=False,
                                font=pygameMenu.fonts.FONT_FRANCHISE,
                                menu_color=(30, 50, 107),  # Background color
                                menu_color_title=(120, 45, 30),
                                onclose=PYGAME_MENU_DISABLE_CLOSE,  # Pressing ESC button does nothing
                                title='Free Play',
                                window_height=H_SIZE,
                                window_width=W_SIZE,
                                )

free_play_menu.add_selector('Map', MAP_MENU_ARRAY,
                                        onreturn=None,
                                        onchange=change_map)

free_play_menu.add_option('Start', free_play_map_chosen_function)
free_play_menu.add_option('Return to Menu', PYGAME_MENU_BACK)

# -----------------------------------------------------------------------------
# Algorithms Select Menu

def algorithm_map_chosen_function():
    global CURRENT_STATE, algorithm_menu
    menu.disable()
    menu.reset(5)
    algorithm_menu = AlgorithmMenu(surface, H_SIZE, W_SIZE, MAP[0], ALGORITHM[0])
    CURRENT_STATE = 'VIEWING_STATS_ALGORITHM'

algorithms_select_menu = pygameMenu.Menu(surface,
                                dopause=False,
                                font=pygameMenu.fonts.FONT_FRANCHISE,
                                menu_color=(27, 90, 26),  # Background color
                                menu_color_title=(120, 45, 30),
                                onclose=PYGAME_MENU_DISABLE_CLOSE,  # Pressing ESC button does nothing
                                title='Algorithms',
                                window_height=H_SIZE,
                                window_width=W_SIZE,
                                )

algorithms_select_menu.add_selector('Map', MAP_MENU_ARRAY,
                                        onreturn=None,
                                        onchange=change_map)

algorithms_select_menu.add_selector('Algorithm', 
                                        [('DFS', 'DFS'), ('BFS', 'BFS'), ('Iterative DFS', 'Iterative DFS'), ('Uniform Cost Search', 'Uniform Cost Search'), ('Best First Search #H1', 'Best First Search #H1') , ('Best First Search #H2', 'Best First Search #H2') , ('Best First Search #H3', 'Best First Search #H3'), ('A* #H1', 'A* #H1'), ('A* #H2', 'A* #H2') , ('A* #H3', 'A* #H3')],
                                        onreturn=None,
                                        onchange=change_algorithm)

algorithms_select_menu.add_option('Start', algorithm_map_chosen_function)
algorithms_select_menu.add_option('Return to Menu', PYGAME_MENU_BACK)


# Add options to main menu        
menu.add_option("Free Play", free_play_menu)  # Add free play menu
menu.add_option("Algorithms", algorithms_select_menu)  # Add free play menu
menu.add_option('Exit', PYGAME_MENU_EXIT)  # Add exit function
menu.enable()


# -----------------------------------------------------------------------------
# Main loop
if __name__== "__main__":
    while True:
        # Tick clock
        deltatime = clock.tick(60)

        # Paint background
        surface.fill(COLOR_BACKGROUND)

        # Game Events
        events = pygame.event.get()
        if(CURRENT_STATE == 'INGAME'):
            GAME.process(events)
            if GAME.should_quit():
                CURRENT_STATE = 'MENU'
                menu.enable()
                pygame.mixer.music.stop()
        elif CURRENT_STATE == 'VIEWING_STATS_ALGORITHM' :
            algorithm_menu.process(events)
            if algorithm_menu.should_quit():
                CURRENT_STATE = 'MENU'
                menu.enable()
            solution = algorithm_menu.show_solution()
            if solution is not None:
                CURRENT_STATE = 'VIEWING_ALGORITHM'
                algorithm_show = AlgorithmShow(surface, H_SIZE, W_SIZE, MAP[0], solution, "Level {}, Algorithm {}, Showing Solution".format(MAP[0], ALGORITHM[0]), 500)  
            explored_nodes = algorithm_menu.show_explored_nodes()
            if explored_nodes is not None:
                CURRENT_STATE = 'VIEWING_ALGORITHM'
                algorithm_show = AlgorithmShow(surface, H_SIZE, W_SIZE, MAP[0], explored_nodes, "Level {}, Algorithm {}, Showing Explored Nodes".format(MAP[0], ALGORITHM[0]), 150, False)
        elif CURRENT_STATE == 'VIEWING_ALGORITHM':
            algorithm_show.process(events, deltatime)
            if algorithm_show.should_quit():
                CURRENT_STATE = 'MENU'
                menu.enable()

        # Application events
        for event in events:
            if event.type == QUIT:
                exit()

        # Execute main from principal menu if is enabled
        menu.mainloop(events)

        # Flip surface
        pygame.display.flip()
