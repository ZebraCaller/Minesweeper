import arcade
import random


# константы
SCREEN_TITLE = "Minesweeper" 
ROW_COUNT = 7  # количество строк на игровом поле
COLUMN_COUNT = 7  # количество столбцов на игровом поле
CELL_WIDTH = 100  # ширина одной ячейки
CELL_HEIGHT = 100  # высота одной ячейки
MARGIN = 2  # толщина границы (то есть линий между ячейками)
# ширина и высота окна
SCREEN_WIDTH = (CELL_WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (CELL_HEIGHT + MARGIN) * ROW_COUNT + MARGIN
MINES_COUNT = 10  # количество мин на игровом поле
ATTEMPTS = 10  # число попыток


class Minesweeper(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.closed = arcade.load_texture('empty.png')
        self.bomb = arcade.load_texture('bomb.png')
        self.cleared = arcade.load_texture('grass1.png')
        self.flag = arcade.load_texture('flag.png')
        self.game = True
        self.count = 0
        self.grid = []
        self.grid_bomb = []
        self.grid_clear = []

    def setup(self):
        "Расположение мин и трофея на игровой сетке"
        for i in range(ROW_COUNT):
            self.grid.append([])
            for b in range(COLUMN_COUNT):
                self.grid[i].append('closed')
#                for c in range(COLUMN_COUNT*COLUMN_COUNT-COLUMN_COUNT)

        count = 0
        while count < MINES_COUNT:
            row = random.randint(0, ROW_COUNT-1)
            column = random.randint(0, COLUMN_COUNT-1)
            if [row, column] not in self.grid_bomb:
                self.grid_bomb.append([row, column])
                count += 1

        
        

    def on_draw(self):
        "Отрисовка объектов"
        arcade.start_render()
        arcade.set_background_color(arcade.color.BLACK)
        for i in range(ROW_COUNT):
            for b in range(COLUMN_COUNT):
                color = (216, 255, 253)
                image = None
                x = (CELL_WIDTH + MARGIN) * b + CELL_WIDTH//2 + MARGIN
                y = (CELL_HEIGHT + MARGIN) * i + CELL_HEIGHT//2 + MARGIN
                if self.game:
                    if self.grid[i][b] == 'bomb':
                        color = (255, 0, 0)
                        image = self.bomb
                        self.game = False
                        #arcade.draw_texture_rectangle(x, y, CELL_WIDTH, CELL_HEIGHT, self.bomb)
                    elif self.grid[i][b] == 'clear':
                        color = (0, 255, 13)
                        image = self.cleared
                    elif self.grid[i][b] == 'closed':
                        image = self.closed
                    elif self.grid[i][b] == 'flag':
                        color = (216, 255, 253)
                        image = self.flag
                    arcade.draw_rectangle_filled(x, y, CELL_WIDTH, CELL_HEIGHT, color)    
                    if image != None:
                        arcade.draw_texture_rectangle(x, y, CELL_WIDTH, CELL_HEIGHT, image)
                    if self.grid[i][b] == 'clear':
                        bomb = self.get_bomb(i, b)
                        arcade.draw_text(f'{bomb}', x-7, y-15, arcade.color.BLACK, 25)
                    
                        
                else:
                    image = self.cleared
                    if [i, b] in self.grid_bomb:
                        image = self.bomb
                        color = (255, 0, 0)
                    arcade.draw_rectangle_filled(x, y, CELL_WIDTH, CELL_HEIGHT, color)
                    arcade.draw_texture_rectangle(x, y, CELL_WIDTH, CELL_HEIGHT, image)
    def on_mouse_press(self, x, y, button, modifiers):
        if self.game:
            row = y//(CELL_HEIGHT + MARGIN)
            column = x//(CELL_WIDTH + MARGIN)
            if arcade.MOUSE_BUTTON_RIGHT == button:
                self.grid[row][column] = 'flag'
            else:
                if [row, column] in self.grid_bomb:
                    self.grid[row][column] = 'bomb'
                    
                else:
                    self.grid[row][column] = 'clear'
                    self.count +=1
                    if self.count == ROW_COUNT*COLUMN_COUNT-MINES_COUNT:
                        print('u win')
                        self.game = False
            
                

    def get_bomb(self, row, column):
        count = 0
        for b_row, b_column in self.grid_bomb:
            if (b_row == row or b_row == row-1 or b_row == row+1) and (b_column == column or b_column == column-1 or b_column == column+1):
                count += 1 
        return count
game = Minesweeper(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
game.setup()
arcade.run()
