import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Р Р°Р·РјРµСЂ РєР»РµС‚РѕС‡РЅРѕРіРѕ РїРѕР»СЏ
        self.rows, self.cols = size
        # РџСЂРµРґС‹РґСѓС‰РµРµ РїРѕРєРѕР»РµРЅРёРµ РєР»РµС‚РѕРє
        self.prev_generation = self.create_grid()
        # РўРµРєСѓС‰РµРµ РїРѕРєРѕР»РµРЅРёРµ РєР»РµС‚РѕРє
        self.curr_generation = self.create_grid(randomize=randomize)
        # РњР°РєСЃРёРјР°Р»СЊРЅРѕРµ С‡РёСЃР»Рѕ РїРѕРєРѕР»РµРЅРёР№
        self.max_generations = max_generations
        # РўРµРєСѓС‰РµРµ С‡РёСЃР»Рѕ РїРѕРєРѕР»РµРЅРёР№
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        a = []
        wt = self.rows
        ht = self.cols
        if randomize == True:
            for i in range(wt):
                a.append([])
                for j in range(ht):
                    a[i].append(random.randint(0, 1))
        else:
            for i in range(wt):
                a.append([])
                for j in range(ht):
                    a[i].append(0)
        return a

    def get_neighbours(self, cell: Cell) -> Cells:
        g = self.curr_generation
        i1 = cell[0]
        j1 = cell[1]
        arr = []
        for i in range(i1-1, i1+2):
            for j in range(j1-1, j1+2):
                if i>=0 and j>=0 and i<self.rows and j<self.cols:
                    if i1==i and j1==j:
                        None
                    else:
                        arr.append(g[i][j])
        return arr

    def get_next_generation(self) -> Grid:
        g = self.curr_generation
        new_g = [[0 for j in range(len(g[i]))] for i in range(len(g))]
        for i in range(self.rows):
            for j in range(self.cols):
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
        self.curr_generation=new_g
        return self.curr_generation

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations+=1
        return self.curr_generation
        

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.generations <= self.max_generations:
            return True
        else:
            return False
        

    @property
    def is_changing(self) -> bool:
        if self.prev_generation == self.curr_generation:
            return False
        else:
            return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open('grid.txt', 'r') as f:
            mylist = [i.split() for i in f]
            mylist1 = [list(str(mylist[i][0])) for i in range(len(mylist))]
            mylist2 = [[int(j) for j in mylist1[i]] for i in range(len(mylist1))]
            return mylist2
        

    def save(self, filename: pathlib.Path) -> None:
        found = open('saves.txt', 'w')
        number = [''.join(map(str, self.curr_generation[i])) for i in range(len(self.curr_generation))]
        number1 = '\n'.join(number)
        found.write(str(number1))   
        found.close()
                   
        
life = GameOfLife((5, 5))
print(life.curr_generation)
print(life.from_file('grid.txt'))
print(life.save('saves.txt'))

"""    
life = GameOfLife.from_file('glider.txt')
print(life.curr_generation)
for _ in range(4):
    life.step()
print(life.curr_generation)
life.save(pathlib.Path('glider-4-steps.txt'))
"""