import pygame
from problem import Bloxorz
import pygame.freetype
from iama.algorithms import uniform_cost_search


class Game:
    def __init__(self, surface, W_HEIGHT_SIZE, W_WIDTH_SIZE, level_number, show_hint = False):
        self.surface = surface
        self.W_HEIGHT_SIZE = W_HEIGHT_SIZE
        self.W_WIDTH_SIZE = W_WIDTH_SIZE
        self.CENTER_X = W_WIDTH_SIZE / 2
        self.CENTER_Y = W_HEIGHT_SIZE / 2
            
        self.problem = Bloxorz(level_number)
        self.state = self.problem.initial

        # drawing
        self.square_size = 50
        self.starting_x = self.CENTER_X - self.problem.level.size / 2 * self.square_size 
        self.starting_y = self.CENTER_Y - self.problem.level.size / 2 * self.square_size 
        self.ending_x = self.CENTER_X + self.problem.level.size / 2 * self.square_size 
        self.ending_y = self.CENTER_Y + self.problem.level.size / 2 * self.square_size 
        if self.starting_x < 190:
            self.starting_x = 190
            self.starting_y = 75
            self.ending_x = 690
            self.ending_y = 575
            self.square_size = (self.ending_x - self.starting_x)/self.problem.level.size

        self.unavailable_color = (10,10,10) 
        self.available_color = (50,50,100) 
        self.block_color = (150,150,150)
        self.hint_color = (255,128,0)
        self.goal_color = (252,25,25)
        self.line_color = (255,255,255)
        
        self.font = pygame.font.Font(None, 50)
        self.moves = 0
        self.over = False
        self.ESC = False

        self.hint = None
        self.show_hint = show_hint


    def process(self, events):
        self.process_input(events)
        self.draw()
        self.process_end()

    def process_input(self, events):
        for event in events:
            if (event.type == pygame.KEYDOWN):
                if not self.over and event.key == pygame.K_LEFT:
                    new_state = self.problem.do_action_if_possible(self.state, 'LEFT')
                    if(new_state is not None):
                        self.moves += 1
                        self.state = new_state
                        self.hint = None

                elif not self.over and event.key == pygame.K_RIGHT:
                    new_state = self.problem.do_action_if_possible(self.state, 'RIGHT')
                    if(new_state is not None):
                        self.moves += 1
                        self.state = new_state
                        self.hint = None

                elif not self.over and event.key == pygame.K_UP:
                    new_state = self.problem.do_action_if_possible(self.state, 'DOWN')
                    if(new_state is not None):
                        self.moves += 1
                        self.state = new_state
                        self.hint = None

                elif not self.over and event.key == pygame.K_DOWN:
                    new_state = self.problem.do_action_if_possible(self.state, 'UP')
                    if(new_state is not None):
                        self.moves += 1
                        self.state = new_state
                        self.hint = None

                elif not self.over and event.key == pygame.K_h and self.hint is None:
                    self.problem.initial = self.state
                    [goal_node, explored_ordered, timeMS] = uniform_cost_search(self.problem)
                    self.hint = goal_node.path()[1]

                elif event.key == pygame.K_ESCAPE:
                    self.ESC = True # Exit game

    def set_state(self, state, incremenet = 1):
        if not self.state.position == state.position:
            self.state = state
            self.moves += incremenet

    def process_end(self):
        if(self.state == self.problem.goal):
            self.over = True
            if self.moves > 0:
                text = self.font.render("Win at {} moves. Press ESC to go back.".format(self.moves), 230, (255, 255, 255))
            else:
                text = self.font.render("Press ESC to go back.", 230, (255, 255, 255))
            text_rect = text.get_rect(center=(self.W_WIDTH_SIZE/2, self.W_HEIGHT_SIZE - 35))
            self.surface.blit(text, text_rect)



    def draw(self):
        self.draw_grid()
        self.draw_map()
        self.draw_goal()
        self.draw_block()
        self.draw_hint()

    def draw_grid(self):
        x = self.starting_x
        y = self.starting_y
        
        for l in range(self.problem.level.size + 1):
            pygame.draw.line(self.surface, self.line_color, (x,self.starting_y),(x,self.ending_y))
            pygame.draw.line(self.surface, self.line_color, (self.starting_x,y),(self.ending_x,y))
            x += self.square_size
            y += self.square_size

    def draw_map(self):
        for x in range(self.problem.level.size):
            for y in range(self.problem.level.size):
                if(self.problem.level.is_tile_available(x,y)):
                    self.draw_map_square(x, y, self.available_color)
                else:
                    self.draw_map_square(x, y, self.unavailable_color)

    def draw_map_square(self, x, y, color):
        pygame.draw.rect(self.surface, color, (self.starting_x + 1 + x*self.square_size, self.starting_y + 1 + y*self.square_size, self.square_size - 1, self.square_size - 1))

    def draw_block(self):
        # Vertical
        if(len(self.state.position) == 2):
            x = self.state.position[0]
            y = self.state.position[1]
            self.draw_map_square(x, y, self.block_color)
        # Horizontal
        else:
            x1 = self.state.position[0]
            y1 = self.state.position[1]
            x2 = self.state.position[2]
            y2 = self.state.position[3]
            self.draw_map_square(x1, y1, self.block_color)
            self.draw_map_square(x2, y2, self.block_color)
            # Same Row
            if(x1 == x2):
                self.draw_map_square(x1, (y1+y2)/2, self.block_color)
            # Same Column
            else:
                self.draw_map_square((x1+x2)/2, y1, self.block_color)
    
    def draw_hint(self):
        if self.show_hint:
            if self.hint is not None:
                # Vertical
                if(len(self.hint.state.position) == 2):
                    x = self.hint.state.position[0]
                    y = self.hint.state.position[1]
                    self.draw_map_square(x, y, self.hint_color)
                # Horizontal
                else:
                    x1 = self.hint.state.position[0]
                    y1 = self.hint.state.position[1]
                    x2 = self.hint.state.position[2]
                    y2 = self.hint.state.position[3]
                    self.draw_map_square(x1, y1, self.hint_color)
                    self.draw_map_square(x2, y2, self.hint_color)
                    # Same Row
                    if(x1 == x2):
                        self.draw_map_square(x1, (y1+y2)/2, self.hint_color)
                    # Same Column
                    else:
                        self.draw_map_square((x1+x2)/2, y1, self.hint_color)
            elif self.hint is None and not self.over:
                text = self.font.render("Feeling Trapped? Press H for a hint.", 230, (255, 255, 255))
                text_rect = text.get_rect(center=(self.W_WIDTH_SIZE/2, self.W_HEIGHT_SIZE - 35))
                self.surface.blit(text, text_rect)
            
    def draw_goal(self):
        x = self.problem.goal.position[0]
        y = self.problem.goal.position[1]
        self.draw_map_square(x, y, self.goal_color)

    def should_quit(self):
        return self.ESC