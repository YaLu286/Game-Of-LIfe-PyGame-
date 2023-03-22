import random 
import sys
import pygame
from pygame.locals import *

DARK_PURPLE = (102, 9, 101)

class GameOfLife :
    def __init__(self, screen,  width: int = 800, heigth: int = 600, cell_size: int = 20, game_speed: int = 5) :
        self.width = width
        self.heigth = heigth
        self.cell_size = cell_size 
        
        self.screen_size = width, heigth
        self.screen = screen
        # pygame.display.set_mode(self.screen_size)
        
        self.cell_width = self.width / self.cell_size
        self.cell_heigth = self.heigth / self.cell_size

        self.game_speed = game_speed
    

    def draw_lines(self) :
        for x in range(0, self.width, self.cell_size) :
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.heigth))

        for y in range(0, self.heigth, self.cell_size) :
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y),(self.width, y))
        
        pygame.draw.rect(self.screen, DARK_PURPLE, 
                                    (self.width * 0.96, self.heigth / 3, 4, self.heigth / 3))
        pygame.draw.circle(self.screen, DARK_PURPLE, (self.width * 0.96 + 2, self.heigth / 3 * 2 - self.game_speed * self.heigth / 120) , 6, width=0)

        if self.paused :
            pygame.draw.rect(self.screen, DARK_PURPLE, (self.width / 2 - 16, self.heigth / 2 - 20, 8, 40))
            pygame.draw.rect(self.screen, DARK_PURPLE, (self.width / 2 + 8, self.heigth / 2 - 20, 8, 40))
    
    
    def game(self) :
        # pygame.init()
        self.screen.fill(pygame.Color('white'))
        clock = pygame.time.Clock()
        running = True
        self.paused = False
        self.create_grid(1)
        while running :
            for event in pygame.event.get() :
                if event.type == QUIT :
                    sys.exit()
                if event.type == KEYDOWN :
                    if event.key == pygame.K_SPACE :
                        self.paused = not self.paused
                    if event.key == pygame.K_ESCAPE :
                        running = False
                        gui.game_start = False
                if event.type == MOUSEBUTTONDOWN :
                    if event.button == 1 :
                        j, i = event.pos
                        i = int(i / self.cell_size)
                        j = int(j / self.cell_size)
                        if self.grid[i][j] == 0 : 
                            self.grid[i][j] = 1
                        else :
                            self.grid[i][j] = 0
                    elif event.button == 4:  
                        self.game_speed = self.game_speed + 0.5  if self.game_speed < 40 else 40
                    elif event.button == 5:
                        self.game_speed = self.game_speed - 0.5 if self.game_speed > 0.5 else 0.5
            
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            if not self.paused :
                self.next_generation()
            clock.tick(self.game_speed)
        gui.main_menu()

    
    def next_generation(self) :
        next_gen_grid = [ [0]*self.grid_cols for i in range(self.grid_rows) ]
        for i in range(self.grid_rows) :
            for j in range(self.grid_cols) :
                sum = 0 
                for k in range(i - 1, i + 2) :
                    for m in range(j - 1, j + 2) :
                        if (k > (self.grid_rows - 1)) : 
                            k = 0
                        if (m > (self.grid_cols - 1)) : 
                            m = 0
                        sum += self.grid[k][m]
                if self.grid[i][j] == 1:        
                    sum = sum - 1
                next_gen_grid[i][j] = self.check_cell_status(self.grid[i][j], sum)
        self.grid = next_gen_grid


    def check_cell_status(self, cur_stat, sum) :
        next_gen_stat = 0
        if cur_stat == 1 :
                if 2 <= sum <= 3 : 
                    next_gen_stat = 1
        elif cur_stat == 0 :
            if sum == 3 :
                next_gen_stat = 1
        return next_gen_stat
    
    def create_grid(self, randomize: bool=False) :
        self.grid_rows = int(self.heigth / self.cell_size)
        self.grid_cols = int(self.width / self.cell_size)
        self.grid = [ [0]*self.grid_cols for i in range(self.grid_rows) ]
        
        if randomize :
            for i in range(self.grid_rows) :
                for j in range(self.grid_cols) :
                    self.grid[i][j] = random.choice([1,0])
        else :
            for i in range(int(self.grid_rows)) :
                for j in range(self.grid_cols) :
                    self.grid[i][j] = 0
    

    def draw_grid(self) :
        for i in range(self.grid_rows) :
            for j in range(self.grid_cols) :
                if self.grid[i][j] : 
                    # pygame.draw.rect(self.screen, pygame.Color('blue'), 
                                    # (j * self.cell_size + 1, i * self.cell_size  + 1, 
                                    #  self.cell_size - 1, self.cell_size - 1))
                    pygame.draw.circle(self.screen, pygame.Color('purple'), ((j + 0.5) * self.cell_size, (i + 0.5) * self.cell_size ) , self.cell_size / 2 , width = int (self.cell_size / 3))
                else :
                    pygame.draw.rect(self.screen, pygame.Color('white'), 
                                    (j * self.cell_size + 1, i * self.cell_size + 1, 
                                     self.cell_size - 1, self.cell_size - 1))

                                                                                                                                         
                                                
class GUI :
    def __init__(self, width: int = 800, heigth: int = 600) :
        self.width = width
        self.heigth = heigth
        
        self.screen_size = width, heigth
        self.screen = pygame.display.set_mode(self.screen_size)
    
        
    def main_menu (self) :
        pygame.init()
        pygame.display.set_caption("Game Of Life")
        self.screen.fill(pygame.Color('white'))
        running = True
        clock = pygame.time.Clock()
        game = GameOfLife(self.screen, 900, 600, 20)
        game_start = False
        select = 0 
        while running :
            for event in pygame.event.get() :
                if event.type == QUIT :
                    running = False
                if event.type == MOUSEMOTION :
                    x, y = event.pos
                    if (self.width / 3 < x < 2 / 3 * self.width) \
                        and (self.heigth / 2 < y < self.heigth / 2 + self.heigth / 10) :
                        select = 1 
                    elif (self.width / 3 < x < 2 / 3 * self.width) \
                        and (self.heigth / 2 +  self.heigth / 7 < y < self.heigth / 2 +  self.heigth / 7 + self.heigth / 10) :
                        select = 2
                    elif (self.width / 2 - self.width / 12 < x < self.width / 2 + self.width / 12) \
                        and (self.heigth / 2 + 2 * self.heigth / 7 < y < self.heigth / 2 + 2 * self.heigth / 7 + self.heigth / 10) :
                        select = 3
                    else :
                        select = 0
                if event.type == MOUSEBUTTONDOWN :
                    if event.button == 1 :
                        if select == 1 :
                            running = False
                            game_start = True
                        elif select == 2 :
                            pass
                        elif select == 3:
                            sys.exit()
            self.draw_main_menu(select)
            pygame.display.flip()
            clock.tick(60)
        if game_start :
            game.game()  

    
    def draw_main_menu(self, select) :
        pygame.draw.rect(self.screen, pygame.Color('purple'), (self.width / 3, self.heigth / 2, self.width / 3, self.heigth / 10  ))
        pygame.draw.rect(self.screen, pygame.Color('purple'), (self.width / 3, self.heigth / 2 +  self.heigth / 7, self.width / 3, self.heigth / 10  ))
        pygame.draw.rect(self.screen, pygame.Color('purple'), (self.width * 5 / 12, self.heigth / 2  + 2 * self.heigth / 7 , self.width / 6, self.heigth / 10  ))
        if select == 1 :
            pygame.draw.rect(self.screen, DARK_PURPLE, (self.width / 3, self.heigth / 2, self.width / 3, self.heigth / 10), 6)
        elif select == 2 :
            pygame.draw.rect(self.screen, DARK_PURPLE, (self.width / 3, self.heigth / 2 +  self.heigth / 7, self.width / 3, self.heigth / 10), 6)
        elif select == 3 :    
            pygame.draw.rect(self.screen, DARK_PURPLE, (self.width * 5 / 12, self.heigth / 2  + 2 * self.heigth / 7 , self.width / 6, self.heigth / 10), 6)
        pygame.font.init()
        
        font = pygame.font.SysFont('ubuntumono' , 50)
        gol_font = pygame.font.SysFont('ubuntumono', 72)
        gol_text = gol_font.render('Game Of Life', True, DARK_PURPLE)
        new_game_text = font.render('New Game', True, (72, 50, 72))
        settings_text = font.render('Settings', True, (72, 50, 72))
        exit_text = font.render('Exit', True, (72, 50, 72))
        
        gol_text_rect = gol_text.get_rect()
        gol_text_rect.center = (self.width / 2, self.heigth / 3 + self.heigth / 20 )
        new_game_text_rect = new_game_text.get_rect()
        new_game_text_rect.center = (self.width / 2, self.heigth / 2 + self.heigth / 20)
        settings_text_rect = settings_text.get_rect()
        settings_text_rect.center = (self.width / 2, self.heigth / 2 + self.heigth / 7  + self.heigth / 20)
        exit_text_rect = exit_text.get_rect()
        exit_text_rect.center = (self.width / 2, self.heigth / 2 + 2 * self.heigth / 7  + self.heigth / 20)
        
        self.screen.blit(gol_text, gol_text_rect)
        self.screen.blit(new_game_text, new_game_text_rect)
        self.screen.blit(settings_text, settings_text_rect)
        self.screen.blit(exit_text, exit_text_rect)
        


gui = GUI(900, 600)
gui.main_menu()




