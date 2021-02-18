import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        #resize = curses.is_term_resized(life.rows, life.cols)
        #if resize is True:

        y, x = screen.getmaxyx()
        self.win = curses.newwin(y, x, 0, 0)
        h = life.rows + 2
        w = life.cols + 2
        for i in range(h):
            for j in range(w):
                if i == 0:
                    if j == 0 or j == w - 1:
                        self.win.addstr(0, j, "+")
                    else:
                        self.win.addstr(i, j, "-")
                elif i == h - 1:
                    if j == 0 or j == w - 1:
                        self.win.addstr(h - 1, j, "+")
                    else:
                        self.win.addstr(i, j, "-")
                else:
                    if j == 0 or j == w - 1:
                        self.win.addstr(i, j, "|")
        self.win.refresh()
        #self.win.getch()

        

    def draw_grid(self, screen) -> None:
        arr = life.curr_generation
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if arr[i][j] == 1:
                    self.win.addstr(i+1, j+1, "*")
        self.win.refresh()
        #self.win.getch()

    def run(self) -> None:
        screen = curses.initscr()
        while life.generations <= life.max_generations:
            self.draw_borders(screen)
            self.draw_grid(screen)
            life.step()
            self.win.refresh()        
        curses.endwin()


life = GameOfLife((24, 80), max_generations=500)
ui = Console(life)
ui.run()