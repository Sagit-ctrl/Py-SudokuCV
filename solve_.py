from init_ import *
from detect import *

class Board_Solve():

    def __init__(self):
        self.time_ = ''
        self.time__ = ''
        self.status = 'Input question!'

    def draw(self):
        SCREEN.fill(WHITE)
        displaySurface((WINDOWWIDTH, WINDOWHEIGHT), BLACK, SCREEN, 0, 0, True, 0, 0)

        for j in range(int(NUM_Y / 3)):
            for i in range(int(NUM_X / 3)):
                displaySurface((WIDTH * 3 + BLANK * 2, HEIGHT * 3 + BLANK * 2), SILVER, SCREEN, i, j)

        for j in range(NUM_Y):
            for i in range(NUM_X):
                displaySurface((WIDTH, HEIGHT), WHITE, SCREEN, i, j)

        display(20, self.status, RED, WINDOWWIDTH, 0, 100, WINDOWHEIGHT - 30)
        display(20, 'Problem solving time is: ' + self.time_ + ' = ' + str(self.time__) + ' ticks', RED, WINDOWWIDTH, 0, 100, WINDOWHEIGHT)

    def update(self, status):
        if status == 2:
            self.status = 'Complete problem solving!'

    def timeSolve(self, time_):
        self.time__ = time_
        self.time_ = changeTime(time_)

class Number_Solve():

    def __init__(self):
        self.position = decodeBoard(board_test)
        self.answer = BoardBase

    def draw(self):
        for j in range(NUM_X):
            for i in range(NUM_Y):
                x = BLANK * (i + 1) + WIDTH * i
                y = BLANK * (j + 1) + HEIGHT * j
                if self.answer[j][i] != 0:
                    display(30, self.answer[j][i], BLUE, WIDTH, x, HEIGHT, y)

        for j in range(NUM_X):
            for i in range(NUM_Y):
                x = BLANK * (i + 1) + WIDTH * i
                y = BLANK * (j + 1) + HEIGHT * j
                if self.position[j][i] != 0:
                    display(30, self.position[j][i], BLACK, WIDTH, x, HEIGHT, y)

    def solve_v1(self):
        find = find_empty(self.position)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.position, i, (row, col)):
                self.position[row][col] = i

                if solve(self.position):
                    return True

                self.position[row][col] = 0
        return False

board_solve = Board_Solve()
number_solve = Number_Solve()

def GameRun_Solve():

    board_solve.__init__()
    number_solve.__init__()
    board_solve.draw()

    stop_time_solve = 0
    start_time_solve = 0
    check_done = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if not check_done:
            start_time_solve = pygame.time.get_ticks()
            board_solve.draw()
            number_solve.solve_v1()
            board_solve.update(2)
            stop_time_solve = pygame.time.get_ticks()
            check_done = True

        board_solve.timeSolve(stop_time_solve - start_time_solve)
        board_solve.draw()
        number_solve.draw()

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    GameRun_Solve()