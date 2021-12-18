import pygame, sys, random
from pygame.locals import *
import sqlite3

# Tạo sẵn các màu sắc
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (253, 37, 62)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
SILVER = (215, 215, 215)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
MAROON = (128, 0, 0)
PURPLE = (128, 0, 128)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
ORANGE = (255, 140, 0)
OCEAN = (102, 255, 255)
EMPTY = (0, 0, 0, 0)
# Thông số cơ bản của màn hình hiển thị
WIDTH = 50
HEIGHT = 50
BLANK = 5
NUM_X = 9
NUM_Y = 9
WINDOWHEIGHTADD = NUM_Y*HEIGHT + (NUM_Y + 1)*BLANK + 100
WINDOWWIDTH = NUM_X*WIDTH + (NUM_X + 1)*BLANK
WINDOWHEIGHT = NUM_Y*HEIGHT + (NUM_Y + 1)*BLANK
# Thông số cơ bản của game
BoardBase = \
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

testBo = (15, '053891472148276953972453168896724315735169824421385697289637541517948236364512789', '653891472148276953972453168896724315735169824421385697289637541517948236364512789', 13)

pygame.init()
FPS = 6
fpsClock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHTADD), SRCALPHA, pygame.RESIZABLE)
# programIcon = pygame.image.load('image/icon.jpg')
# pygame.display.set_icon(programIcon)
pygame.display.set_caption('Sudoku')

# Các hàm hiển thị
def color():
    x = random.randrange(0, 10)
    list_color = [BLACK, RED, GREEN, BLUE, YELLOW, MAGENTA, MAROON, PURPLE, TEAL, NAVY, ORANGE]
    color = list_color[x]
    return color

def display(font_size, status, font_color, X1, X2, Y1, Y2, relative = False, posxInpt = 0, posyInpt = 0):
    status = str(status)
    font = pygame.font.SysFont('consolas', font_size)
    surface = font.render(status, True, font_color)
    size = surface.get_size()
    if relative:
        posx = posxInpt
        posy = posyInpt
    else:
        posx = (X1 - size[0]) / 2 + X2
        posy = (Y1 - size[1]) / 2 + Y2
    SCREEN.blit(surface, (posx, posy))
    return [posx, posy]

def displayImage(name_file, scaleX, scaleY, X1, X2, Y1, Y2, relative = False, posx = 0, posy = 0):
    surface = pygame.image.load('image/' + str(name_file))
    surface = pygame.transform.scale(surface, (scaleX, scaleY))
    size = surface.get_size()
    if relative:
        posx = posx
        posy = posy
    else:
        posx = (X1 - size[0]) / 2 + X2
        posy = (Y1 - size[1]) / 2 + Y2
    SCREEN.blit(surface, (posx, posy))
    return [posx, posy]

def displayRect(font_size, status, font_color, X1, X2, Y1, Y2, relative = False, posxInpt = 0, posyInpt = 0):
    status = str(status)
    font = pygame.font.SysFont('consolas', font_size)
    surface = font.render(status, True, font_color)
    size = surface.get_size()
    if relative:
        posx = posxInpt
        posy = posyInpt
    else:
        posx = (X1 - size[0]) / 2 + X2
        posy = (Y1 - size[1]) / 2 + Y2
    SCREEN.blit(surface, (posx, posy))

    a, b, c, d = posx - size[0] / 2, posy - size[1] / 2, 2 * size[0], 2 * size[1]
    pygame.draw.rect(SCREEN, color(), (a, b, c, d), 2)

    return [a, a + c, b, b + d]

def choice_color(number):
    list_color = [BLACK, RED, GREEN, BLUE, YELLOW, MAGENTA, MAROON, PURPLE, TEAL, NAVY, ORANGE]
    return list_color[number]

def displaySurface(size, color, surface_mom, i, j, relative = False, posxInpt = 0, posyInpt = 0):
    surface_name = pygame.surface.Surface(size, flags=0)
    surface_name.fill(color)
    if relative:
       posx = posxInpt
       posy = posyInpt
    else:
        posx = size[0] * i + BLANK * (i + 1)
        posy = size[1] * j + BLANK * (j + 1)
    surface_mom.blit(surface_name, (posx, posy))

# Hàm xử lý số liệu
def check_pos_mouse(pos):
    check_pos_position = False
    check_pos = []

    for i in range(NUM_X + 1):
        for j in range(NUM_Y + 1):
            x = BLANK * (i + 1) + WIDTH * i
            y = BLANK * (j + 1) + HEIGHT * j
            if x > pos[0] and y > pos[1] and check_pos_position == False:
                check_pos = [i - 1, j - 1]
                check_pos_position = True
    if check_pos_position == True:
        return check_pos
    else:
        return -1

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0
    return False

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None

def encodeBoard(bo):
    text = ''
    for row in range(9):
        for column in range(9):
            text += str(bo[row][column])
    return text

def decodeBoard(text):
    inpt = list(text)
    base = \
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    i = 0
    for row in range(9):
        for column in range(9):
            base[row][column] = int(inpt[i])
            i += 1
    # for i in range(len(base)):
    #     print(base[i])
    # print('\n')
    return base

def addSource2Databas(source, answer):
    min = 1000
    record = readSqliteTable()
    x = len(record)
    check = False
    count = 0

    for i in range(x):
        if record[i][3] <= min:
            min = record[i][3]

    for i in range(x):
        if source == record[i][1]:
            check = True
            print('Already exist source')

    for i in range(len(source)):
        if source[i] != '0':
            count += 1
            if source[i] != answer[i]:
                check = True
                print('Wrong source')

    if count <= 13 or count >= 30:
        check = True

    if source != answer and not check:
        InsertbyQueryPython(x, source, answer, min)

def changeTime(realtime):
    second_after_process = int(realtime / 1000)
    minute = int(second_after_process / 60)
    second = second_after_process - minute * 60
    if minute < 10:
        if second < 10:
            time = '0' + str(minute) + ':' + '0' + str(second)
        else:
            time = '0' + str(minute) + ':' + str(second)
    else:
        if second < 10:
            time = str(minute) + ':' + '0' + str(second)
        else:
            time = str(minute) + ':' + str(second)
    return time

def createBoard():
    record = readSqliteTable()
    x = len(record)
    min = 1000
    for i in range(x):
        if record[i][3] <= min:
            min = record[i][3]
    while True:
        boardIndex = random.randrange(0, x, 1)
        if record[boardIndex][3] == min:
            time_use = record[boardIndex][3] + 1
            updateSqliteTable(boardIndex, time_use)
            return record[boardIndex]

def find_around(bo, i, j):
    m = i % 3
    n = j % 3
    if m == 0 and n == 0:
        return [
            bo[i][j + 1], bo[i][j + 2],
            bo[i + 1][j], bo[i + 1][j + 1], bo[i + 1][j + 2],
            bo[i + 2][j], bo[i + 2][j + 1], bo[i + 2][j + 2]
        ]

    if m == 0 and n == 1:
        return [
            bo[i][j - 1], bo[i][j + 1],
            bo[i + 1][j - 1], bo[i + 1][j], bo[i + 1][j + 1],
            bo[i + 2][j - 1], bo[i + 2][j], bo[i + 2][j + 1]
        ]

    if m == 0 and n == 2:
        return [
            bo[i][j - 2], bo[i][j - 1],
            bo[i + 1][j - 2], bo[i + 1][j - 1], bo[i + 1][j],
            bo[i + 2][j - 2], bo[i + 2][j - 1], bo[i + 2][j]
        ]

    if m == 1 and n == 0:
        return [
            bo[i - 1][j], bo[i - 1][j + 1], bo[i - 1][j + 2],
            bo[i][j + 1], bo[i][j + 2],
            bo[i + 1][j], bo[i + 1][j + 1], bo[i + 1][j + 2]
        ]

    if m == 1 and n == 1:
        return [
            bo[i - 1][j - 1], bo[i - 1][j], bo[i - 1][j + 1],
            bo[i][j - 1], bo[i][j + 1],
            bo[i + 1][j - 1], bo[i + 1][j], bo[i + 1][j + 1]
        ]

    if m == 1 and n == 2:
        return [
            bo[i - 1][j - 2], bo[i - 1][j - 1], bo[i - 1][j],
            bo[i][j - 2], bo[i][j - 1],
            bo[i + 1][j - 2], bo[i + 1][j - 1], bo[i + 1][j]
        ]

    if m == 2 and n == 0:
        return [
            bo[i - 2][j], bo[i - 2][j + 1], bo[i - 2][j + 2],
            bo[i - 1][j], bo[i - 1][j + 1], bo[i - 1][j + 2],
            bo[i][j + 1], bo[i][j + 2]
        ]

    if m == 2 and n == 1:
        return [
            bo[i - 2][j - 1], bo[i - 2][j], bo[i - 2][j + 1],
            bo[i - 1][j - 1], bo[i - 1][j], bo[i - 1][j + 1],
            bo[i][j - 1], bo[i][j + 1]
        ]

    if m == 2 and n == 2:
        return [
            bo[i - 2][j - 2], bo[i - 2][j - 1], bo[i - 2][j],
            bo[i - 1][j - 2], bo[i - 1][j - 1], bo[i - 1][j],
            bo[i][j - 2], bo[i][j - 1]
        ]

def changeDatabase(name, time, bo, realtime):
    insert_check = False
    data = readSqliteTableRank()
    print(data)
    endid = len(data) - 1
    if endid == 0:
        pass
    else:
        for i in range(endid):
            deleteSqliteRecordRank(i)

    for i in range(len(data)):
        if realtime <= data[i][4] and not insert_check:
            data.insert(i, (0, name, time, bo, realtime))
            insert_check = True

    print(data)
    for i in range(len(data)):
        InsertbyQueryPythonRank(i, data[i][1], data[i][2], data[i][3], data[i][4])
    print(readSqliteTableRank())

# Hàm database
def CreateDatabase():
    try:
        sqliteConnection = sqlite3.connect('sudoku.db')
        cursor = sqliteConnection.cursor()
        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def CreateTable():
    try:
        sqliteConnection = sqlite3.connect('sudoku.db')
        sqlite_create_table_query = '''CREATE TABLE Source_Sudoku(
                                    id INTEGER PRIMARY KEY,
                                    source TEXT NOT NULL,
                                    answer TEXT NOT NULL,
                                    time_use INTEGER NOT NULL
                                    );'''

        cursor = sqliteConnection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def InsertbyQueryPython(id, source, answer, time_use = 0):
    try:
        sqliteConnection = sqlite3.connect('sudoku.db')
        cursor = sqliteConnection.cursor()
        sqlite_insert_with_param = """INSERT INTO Source_Sudoku
                          (id, source, answer, time_use) 
                          VALUES (?, ?, ?, ?);"""
        data_tuple = (id, source, answer, time_use)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Insert OK", id)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def readSqliteTable():
    try:
        sqliteConnection = sqlite3.connect('sudoku.db')
        cursor = sqliteConnection.cursor()
        sqlite_select_query = """SELECT * from Source_Sudoku"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        # print("Total rows are:  ", len(records))
        return records
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def updateSqliteTable(id, time_use):
    try:
        sqliteConnection = sqlite3.connect('sudoku.db')
        cursor = sqliteConnection.cursor()
        sql_update_query = """Update Source_Sudoku set time_use = ? where id = ?"""
        data = (time_use, id)
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        print("Record Updated successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def deleteSqliteRecord(id):
    try:
        sqliteConnection = sqlite3.connect('sudoku.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_update_query = """DELETE from Source_Sudoku where id = ?"""
        cursor.execute(sql_update_query, (id,))
        sqliteConnection.commit()
        print("Record deleted successfully")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete reocord from a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

# Hàm lấy tên
def name(SCREEN, color, fpsClock, FPS, WINWIDTH, WINHEIGHT):
    text = ''
    check_empty = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                check_empty = False
                if event.key == K_a:
                    text += 'a'
                if event.key == K_b:
                    text += 'b'
                if event.key == K_c:
                    text += 'c'
                if event.key == K_d:
                    text += 'd'
                if event.key == K_e:
                    text += 'e'
                if event.key == K_f:
                    text += 'f'
                if event.key == K_g:
                    text += 'g'
                if event.key == K_h:
                    text += 'h'
                if event.key == K_i:
                    text += 'i'
                if event.key == K_j:
                    text += 'j'
                if event.key == K_k:
                    text += 'k'
                if event.key == K_l:
                    text += 'l'
                if event.key == K_m:
                    text += 'm'
                if event.key == K_n:
                    text += 'n'
                if event.key == K_o:
                    text += 'o'
                if event.key == K_p:
                    text += 'p'
                if event.key == K_q:
                    text += 'q'
                if event.key == K_r:
                    text += 'r'
                if event.key == K_s:
                    text += 's'
                if event.key == K_t:
                    text += 't'
                if event.key == K_u:
                    text += 'u'
                if event.key == K_v:
                    text += 'v'
                if event.key == K_w:
                    text += 'w'
                if event.key == K_x:
                    text += 'x'
                if event.key == K_y:
                    text += 'y'
                if event.key == K_z:
                    text += 'z'
                if event.key == K_0:
                    text += '0'
                if event.key == K_1:
                    text += '1'
                if event.key == K_2:
                    text += '2'
                if event.key == K_3:
                    text += '3'
                if event.key == K_4:
                    text += '4'
                if event.key == K_5:
                    text += '5'
                if event.key == K_6:
                    text += '6'
                if event.key == K_7:
                    text += '7'
                if event.key == K_8:
                    text += '8'
                if event.key == K_9:
                    text += '9'
                if event.key == K_SPACE:
                    text += ' '
                if event.key == K_BACKSPACE:
                    text = text[:-1]
                if event.key == K_RETURN:
                    if text == '':
                        check_empty = True
                    else:
                        return str(text)

        back = pygame.image.load('image/back3.jpg')
        back = pygame.transform.scale(back, (WINWIDTH, WINHEIGHT))
        SCREEN.blit(back, (0, 0))

        font = pygame.font.SysFont('consolas', 30)
        surface = font.render('What is your name?', True, color)
        size = surface.get_size()
        posx = (WINWIDTH - size[0])/2
        posy = (WINHEIGHT - size[1])/2 - WINHEIGHT/5
        SCREEN.blit(surface, (posx, posy))

        text = text.casefold()
        text = text.capitalize()
        font = pygame.font.SysFont('consolas', 40)
        surface = font.render("{}".format(text), True, (255,   0,   0))
        size = surface.get_size()
        posx = (WINWIDTH - size[0]) / 2
        posy = (WINHEIGHT - size[1]) / 2
        SCREEN.blit(surface, (posx, posy))

        if check_empty == True:
            font = pygame.font.SysFont('consolas', 30)
            surface = font.render('Your name is empty', True, (255, 0, 0))
            size = surface.get_size()
            posx = (WINWIDTH - size[0]) / 2
            posy = (WINHEIGHT - size[1]) / 2 + WINHEIGHT / 5
            SCREEN.blit(surface, (posx, posy))

            font = pygame.font.SysFont('consolas', 10)
            surface = font.render('Press a letter to hide this messenge', True, (255, 0, 0))
            size = surface.get_size()
            posx = (WINWIDTH - size[0]) / 2
            posy = (WINHEIGHT - size[1]) / 2 + WINHEIGHT / 5 + size[1] * 3
            SCREEN.blit(surface, (posx, posy))

        pygame.display.update()
        fpsClock.tick(FPS)

# Hàm database rank
def CreateDatabaseRank():
    try:
        sqliteConnection = sqlite3.connect('sudoku.db')
        cursor = sqliteConnection.cursor()
        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def CreateTableRank():
    try:
        sqliteConnection = sqlite3.connect('sudoku.db')
        sqlite_create_table_query = '''CREATE TABLE Rank_Sudoku(
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    time TEXT NOT NULL,
                                    bo INTEGER NOT NULL, 
                                    realtime INTEGER NOT NULL
                                    );'''

        cursor = sqliteConnection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def InsertbyQueryPythonRank(id, name, time, bo, realtime):
    try:
        sqliteConnection = sqlite3.connect('sudoku.db')
        cursor = sqliteConnection.cursor()
        sqlite_insert_with_param = """INSERT INTO Rank_Sudoku
                          (id, name, time, bo, realtime) 
                          VALUES (?, ?, ?, ?, ?);"""
        data_tuple = (id, name, time, bo, realtime)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Insert OK", id)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def readSqliteTableRank():
    try:
        sqliteConnection = sqlite3.connect('sudoku.db')
        cursor = sqliteConnection.cursor()
        sqlite_select_query = """SELECT * from Rank_Sudoku"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        # print("Total rows are:  ", len(records))
        return records
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def deleteSqliteRecordRank(id):
    try:
        sqliteConnection = sqlite3.connect('sudoku.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_update_query = """DELETE from Rank_Sudoku where id = ?"""
        cursor.execute(sql_update_query, (id,))
        sqliteConnection.commit()
        print("Record deleted successfully")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete reocord from a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")
