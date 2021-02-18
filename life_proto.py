import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = (width, height)
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()
            self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        a = []
        wt = self.cell_width
        ht = self.cell_height
        if randomize == True:
            for i in range(ht):
                a.append([])
                for j in range(wt):
                    a[i].append(random.randint(0, 1))
        else:
            for i in range(ht):
                a.append([])
                for j in range(wt):
                    a[i].append(0)
        self.grid = a
        return self.grid

    def draw_grid(self) -> None:
        g = self.grid
        x = 0
        y = 0 
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if g[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, x + self.cell_size, y + self.cell_size))
                if g[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, x + self.cell_size, y + self.cell_size))
                if j == self.cell_width - 1:
                    x = 0
                    y += self.cell_size
                else:
                    x +=self.cell_size
        pass


    def get_neighbours(self, cell: Cell) -> Cells:
        g = self.grid
        i1 = cell[0]
        j1 = cell[1]
        arr = []
        for i in range(i1-1, i1+2):
            for j in range(j1-1, j1+2):
                if i>=0 and j>=0 and i<self.cell_height and j<self.cell_width:
                    if i1==i and j1==j:
                        None
                    else:
                        arr.append(g[i][j])
        return arr
                
    def get_next_generation(self) -> Grid:
        g = self.grid
        new_g = [[0 for j in range(len(g[i]))] for i in range(len(g))]
        #new_g = g
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                a = self.get_neighbours((i, j))
                if g[i][j] == 1:
                    if (sum(a)<2 or sum(a)>3):
                        new_g[i][j] = 0
                    else:
                        new_g[i][j] = 1
                elif g[i][j] == 0 and sum(a) == 3:
                    new_g[i][j] = 1
                else:
                    new_g[i][j]=g[i][j]
        self.grid=new_g
        return self.grid
                    
                

if __name__ == '__main__':
    from pprint import pprint as pp
    game = GameOfLife(320, 280, 20)
    grid = game.create_grid(randomize=True)
    pp(grid)
    print()
    pp(game.get_neighbours((5,5)))
    print()
    pp(game.get_next_generation())
    game.run()