import pygame
import math
from tkinter import *
from tkinter import messagebox as msgbox
from tkinter import ttk
from pygame.locals import *


# отрисовка стола
def draw_board(width, height, size):
    white = (255, 255, 255)
    brown = (166, 75, 0)
    color = white
    X = math.floor(width / size)
    Y = math.floor(height / size)
    board_surf = pygame.Surface((X * size, Y * size))
    for y in range(size):
        rectY = y * Y
        for x in range(size):
            rectX = x * X
            if (x + y) % 2 == 0:
                color = white
            elif (x + y) % 2 != 0:
                color = brown
            pygame.draw.rect(board_surf, color, (rectX, rectY, X, Y))
    return board_surf


# создание массива стола
def create_board(size):
    board = []
    t = 0
    for y in range(size):
        board.append([])
        for x in range(size):
            board[y].append(None)

    for y in range(0, math.floor(size / 2) - 1):
        for x in range(0, size):
            if t % 2 != 0:
                board[y][x] = ['black', 'piece']
            t += 1
        t += 1
    t = 0
    for y in range(math.floor(size / 2) + 1, size):
        for x in range(0, size):
            if (size // 2) % 2 != 0:
                if t % 2 != 0:
                    board[y][x] = ['white', 'piece']
            else:
                if t % 2 == 0:
                    board[y][x] = ['white', 'piece']
            t += 1
        t += 1
    return board


# отрисовка шашек
def draw_pieces(screen, board, width, height, size):
    recwidth = math.floor(width / size)
    recheight = math.floor(height / size)
    for y in range(size):
        for x in range(size):
            piece = board[y][x]
            if piece:
                color, type = piece
                pos = pygame.Rect(x * recwidth, y * recheight, recwidth, recheight)
                if color == "black":
                    black_piece = pygame.image.load('black.png').convert_alpha()
                    black_piece = pygame.transform.scale(black_piece, (recwidth, recheight))
                    screen.blit(black_piece, black_piece.get_rect(center=pos.center))
                    if piece[1] == 'queenPiece':
                        pygame.draw.circle(screen, Color(255, 255, 0),
                                           (x * recwidth + recwidth // 2, y * recheight + recheight // 2),
                                           recwidth // 4)
                else:
                    white_piece = pygame.image.load('white.png').convert_alpha()
                    white_piece = pygame.transform.scale(white_piece, (recwidth, recheight))
                    screen.blit(white_piece, white_piece.get_rect(center=pos.center))
                    if piece[1] == 'queenPiece':
                        pygame.draw.circle(screen, Color(255, 255, 0),
                                           (x * recwidth + recwidth // 2, y * recheight + recheight // 2),
                                           recwidth // 4)


# drag&drop отрисовка
def draw_drag(screen, board, drag_piece, width, height, size):
    recwidth = math.floor(width / size)
    recheight = math.floor(height / size)
    if drag_piece:
        piece, x, y = get_cursor_position(board, width, height, size)
        if x is not None:
            rect = (x * recwidth, y * recheight, recwidth, recheight)
            pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)

        color, type = drag_piece[0]
        pos = pygame.Vector2(pygame.mouse.get_pos())
        if color == 'black':
            black_piece = pygame.image.load('black.png').convert_alpha()
            black_piece = pygame.transform.scale(black_piece, (recwidth, recheight))
            black_piece.set_alpha(150)
            screen.blit(black_piece, black_piece.get_rect(center=pos))
        else:
            white_piece = pygame.image.load('white.png').convert_alpha()
            white_piece = pygame.transform.scale(white_piece, (recwidth, recheight))
            white_piece.set_alpha(150)

            screen.blit(white_piece, white_piece.get_rect(center=pos))
        drag_rect = pygame.Rect(drag_piece[1] * recwidth, drag_piece[2] * recheight, recwidth, recheight)
        pygame.draw.line(screen, pygame.Color('red'), drag_rect.center, pos)
        return (x, y)


# отрисовка рамки
def draw_selector(screen, piece, x, y, width, height, size):
    recwidth = math.floor(width / size)
    recheight = math.floor(height / size)
    if piece is not None:
        rect = (x * recwidth, y * recheight, recwidth, recheight)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)


# проверка позиции drag&drop
def check_drop_pos(board, drag_piece, drop_pos):
    old_x = drag_piece[1]
    old_y = drag_piece[2]
    new_x = drop_pos[0]
    new_y = drop_pos[1]
    if drop_pos != (old_x, old_y):
        if board[new_y][new_x] is None:
            return True
        else:
            return False
    else:
        return False


# получение всех доступных ходов для пешки и дамки
def get_valid_moves(board, drag_piece, size):
    cur_x = drag_piece[1]
    cur_y = drag_piece[2]
    pos = (cur_x, cur_y)
    valid_moves = []
    if drag_piece[0][1] == "piece":
        valid_moves.append(check_left(board, pos, drag_piece, None, size))
        valid_moves.append(check_right(board, pos, drag_piece, None, size))
    elif drag_piece[0][1] == "queenPiece":
        valid_moves.append(check_queen_left(board, pos, drag_piece, None, size, False))
        valid_moves.append(check_queen_left(board, pos, drag_piece, None, size, True))
        valid_moves.append(check_queen_right(board, pos, drag_piece, None, size, False))
        valid_moves.append(check_queen_right(board, pos, drag_piece, None, size, True))

    return valid_moves

#проверка возможности хода дамки влево, возвращает координату доступного хода/атаки
def check_queen_left(board, pos, drag_piece, last_piece, size, up):
    cur_x = pos[0]
    cur_y = pos[1]
    valid_moves = []
    if cur_x - 1 >= 0:
        if drag_piece[0][0] == 'white':
            if up:
                if cur_y - 1 >= 0:
                    if board[cur_y - 1][cur_x - 1] is None:
                        if last_piece is None:
                            return [cur_y - 1, cur_x - 1]
                        else:
                            return [cur_y - 1, cur_x - 1]
                    elif board[cur_y - 1][cur_x - 1][0] == 'white':
                        return None
                    elif board[cur_y - 1][cur_x - 1][0] == 'black':
                        if last_piece is None:
                            last_piece = board[cur_y - 1][cur_x - 1]
                            return check_queen_left(board, (cur_x - 1, cur_y - 1), drag_piece, last_piece, size, up)
                        else:
                            return None
                else:
                    return None
            else:
                if cur_y + 1 < size:
                    if board[cur_y + 1][cur_x - 1] is None:
                        if last_piece is None:
                            return [cur_y + 1, cur_x - 1]
                        else:
                            return [cur_y + 1, cur_x - 1]
                    elif board[cur_y + 1][cur_x - 1][0] == 'white':
                        return None
                    elif board[cur_y + 1][cur_x - 1][0] == 'black':
                        if last_piece is None:
                            last_piece = board[cur_y + 1][cur_x - 1]
                            return check_queen_left(board, (cur_x - 1, cur_y + 1), drag_piece, last_piece, size, up)
                        else:
                            return None
                else:
                    return None
        elif drag_piece[0][0] == 'black':
            if up:
                if cur_y - 1 >= 0:
                    if board[cur_y - 1][cur_x - 1] is None:
                        if last_piece is None:
                            return [cur_y - 1, cur_x - 1]
                        else:
                            return [cur_y - 1, cur_x - 1]
                    elif board[cur_y - 1][cur_x - 1][0] == 'black':
                        return None
                    elif board[cur_y - 1][cur_x - 1][0] == 'white':
                        if last_piece is None:
                            last_piece = board[cur_y - 1][cur_x - 1]
                            return check_queen_left(board, (cur_x - 1, cur_y - 1), drag_piece, last_piece, size, up)
                        else:
                            return None
                else:
                    return None
            else:
                if cur_y + 1 < size:
                    if board[cur_y + 1][cur_x - 1] is None:
                        if last_piece is None:
                            return [cur_y + 1, cur_x - 1]
                        else:
                            return [cur_y + 1, cur_x - 1]
                    elif board[cur_y + 1][cur_x - 1][0] == 'black':
                        return None
                    elif board[cur_y + 1][cur_x - 1][0] == 'white':
                        if last_piece is None:
                            last_piece = board[cur_y + 1][cur_x - 1]
                            return check_queen_left(board, (cur_x - 1, cur_y + 1), drag_piece, last_piece, size, up)
                        else:
                            return None
                else:
                    return None
        return valid_moves
    else:
        return None

#проверка возможности хода дамки вправо, возвращает координату доступного хода/атаки
def check_queen_right(board, pos, drag_piece, last_piece, size, up):
    cur_x = pos[0]
    cur_y = pos[1]
    valid_moves = []
    if cur_x + 1 < size:
        if drag_piece[0][0] == 'white':
            if up:
                if cur_y - 1 >= 0:
                    if board[cur_y - 1][cur_x + 1] is None:
                        if last_piece is None:
                            return [cur_y - 1, cur_x + 1]
                        else:
                            return [cur_y - 1, cur_x + 1]
                    elif board[cur_y - 1][cur_x + 1][0] == 'white':
                        return None
                    elif board[cur_y - 1][cur_x + 1][0] == 'black':
                        if last_piece is None:
                            last_piece = board[cur_y - 1][cur_x + 1]
                            return check_queen_right(board, (cur_x + 1, cur_y - 1), drag_piece, last_piece, size, up)
                        else:
                            return None
                else:
                    return None
            else:
                if cur_y + 1 < size:
                    if board[cur_y + 1][cur_x + 1] is None:
                        if last_piece is None:
                            return [cur_y + 1, cur_x + 1]
                        else:
                            return [cur_y + 1, cur_x + 1]
                    elif board[cur_y + 1][cur_x + 1][0] == 'white':
                        return None
                    elif board[cur_y + 1][cur_x + 1][0] == 'black':
                        if last_piece is None:
                            last_piece = board[cur_y + 1][cur_x + 1]
                            return check_queen_right(board, (cur_x + 1, cur_y + 1), drag_piece, last_piece, size, up)
                        else:
                            return None
                else:
                    return None
        elif drag_piece[0][0] == 'black':
            if up:
                if cur_y - 1 >= 0:
                    if board[cur_y - 1][cur_x + 1] is None:
                        if last_piece is None:
                            return [cur_y - 1, cur_x + 1]
                        else:
                            return [cur_y - 1, cur_x + 1]
                    elif board[cur_y - 1][cur_x + 1][0] == 'black':
                        return None
                    elif board[cur_y - 1][cur_x + 1][0] == 'white':
                        if last_piece is None:
                            last_piece = board[cur_y - 1][cur_x + 1]
                            return check_queen_right(board, (cur_x + 1, cur_y - 1), drag_piece, last_piece, size, up)
                        else:
                            return None
                else:
                    return None
            else:
                if cur_y + 1 < size:
                    if board[cur_y + 1][cur_x + 1] is None:
                        if last_piece is None:
                            return [cur_y + 1, cur_x + 1]
                        else:
                            return [cur_y + 1, cur_x + 1]
                    elif board[cur_y + 1][cur_x + 1][0] == 'black':
                        return None
                    elif board[cur_y + 1][cur_x + 1][0] == 'white':
                        if last_piece is None:
                            last_piece = board[cur_y + 1][cur_x + 1]
                            return check_queen_right(board, (cur_x + 1, cur_y + 1), drag_piece, last_piece, size, up)
                        else:
                            return None
                else:
                    return None
        return valid_moves
    else:
        return None

#проверка возможности хода обычной пешки влево, возвращает координату доступного хода/атаки
def check_left(board, pos, drag_piece, last_piece, size):
    cur_x = pos[0]
    cur_y = pos[1]
    valid_moves = []
    if (cur_x - 1) >= 0:
        if drag_piece[0][0] == 'white':
            if cur_y - 1 >= 0:
                if board[cur_y - 1][cur_x - 1] is None:
                    if last_piece is None:
                        return [cur_y - 1, cur_x - 1]
                    else:
                        return [cur_y - 1, cur_x - 1]
                elif board[cur_y - 1][cur_x - 1][0] == 'white':
                    return None
                elif board[cur_y - 1][cur_x - 1][0] == 'black':
                    if last_piece is None:
                        last_piece = board[cur_y - 1][cur_x - 1]
                        return check_left(board, (cur_x - 1, cur_y - 1), drag_piece, last_piece, size)
                    else:
                        return None
            else:
                return None

        elif drag_piece[0][0] == 'black':
            if cur_y + 1 < size:
                if board[cur_y + 1][cur_x - 1] is None:
                    if last_piece is None:
                        return [cur_y + 1, cur_x - 1]
                    else:
                        return [cur_y + 1, cur_x - 1]
                elif board[cur_y + 1][cur_x - 1][0] == 'black':
                    return None
                elif board[cur_y + 1][cur_x - 1][0] == 'white':
                    if last_piece is None:
                        last_piece = board[cur_y + 1][cur_x - 1]
                        return check_left(board, (cur_x - 1, cur_y + 1), drag_piece, last_piece, size)
                    else:
                        return None
            else:
                return None
        return valid_moves
    else:
        return None

#проверка возможности хода обычной пешки вправо, возвращает координату доступного хода/атаки
def check_right(board, pos, drag_piece, last_piece, size):
    cur_x = pos[0]
    cur_y = pos[1]
    valid_moves = []
    if (cur_x + 1) < size:
        if drag_piece[0][0] == 'white':
            if cur_y - 1 >= 0:
                if board[cur_y - 1][cur_x + 1] is None:
                    if last_piece is None:
                        return [cur_y - 1, cur_x + 1]
                    else:
                        return [cur_y - 1, cur_x + 1]
                elif board[cur_y - 1][cur_x + 1][0] == 'white':
                    return None
                elif board[cur_y - 1][cur_x + 1][0] == 'black':
                    if last_piece is None:
                        last_piece = board[cur_y - 1][cur_x + 1]
                        return check_right(board, (cur_x + 1, cur_y - 1), drag_piece, last_piece, size)
                    else:
                        return None
            else:
                return None

        elif drag_piece[0][0] == 'black':
            if cur_y + 1 < size:
                if board[cur_y + 1][cur_x + 1] is None:
                    if last_piece is None:
                        return [cur_y + 1, cur_x + 1]
                    else:
                        return [cur_y + 1, cur_x + 1]
                elif board[cur_y + 1][cur_x + 1][0] == 'black':
                    return None
                elif board[cur_y + 1][cur_x + 1][0] == 'white':
                    if last_piece is None:
                        last_piece = board[cur_y + 1][cur_x + 1]
                        return check_right(board, (cur_x + 1, cur_y + 1), drag_piece, last_piece, size)
                    else:
                        return None
            else:
                return None
        return valid_moves
    else:
        return None

#проверка достигла ли пешка вражеского нулевого поля, чтобы стать дамкой
def check_queen(x, y, board, size):
    piece_color = board[y][x][0]
    print(piece_color)
    if piece_color == 'white':
        if y == 0:
            return True
        else:
            return False
    elif piece_color == 'black':
        if y == size - 1:
            return True
        else:
            return False

#отрисовка доступных ходов
def draw_moves(screen, moves, width, height, size):
    if moves is not None:
        recwidth = math.floor(width / size)
        recheight = math.floor(height / size)
        for move in moves:
            x = move[0]
            y = move[1]
            pygame.draw.circle(screen, (0, 0, 255), (x * recwidth + recwidth // 2, y * recheight + recheight // 2),
                               recwidth // 2)
    else:
        pass

#получение массива ходов атаки после сруба одной пешки

def get_attack_moves(board, drag_piece, size):
    valid_moves = get_valid_moves(board, drag_piece, size)
    moves = [move for move in valid_moves if move is not None]
    valid_moves.clear()
    for move in moves:
        print(move)
        if abs(move[1] - drag_piece[1]) > 1:
            y = move[0]
            x = move[1]
            valid_moves.append([x, y])
    return valid_moves

# проверка хода на атаку, если длина хода больше 1, то возвращает позициую атакованой пешки
def check_attack(new_x, new_y, old_x, old_y):
    buf_x = new_x - old_x
    buf_y = new_y - old_y
    # print(abs(buf_x))
    # print(abs(buf_y))
    if abs(buf_x) > 1:
        buf_x = new_x - buf_x // 2
        buf_y = new_y - buf_y // 2

        return [buf_x, buf_y]
    else:
        return None


# получение позиции курсора
def get_cursor_position(board, width, height, size):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    x = int(mouse_pos[0] // math.floor(width / size))
    y = int(mouse_pos[1] // math.floor(height / size))
    try:
        if x >= 0 and y >= 0: return board[y][x], x, y
    except IndexError:
        pass
    return None, None, None


# проверка победы
def check_win(board):
    if not (any(['black', 'piece'] in sublist for sublist in board) or any(
            ['black', 'queenPiece'] in sublist for sublist in board)):
        return 'white'
    elif not (any(['white', 'piece'] in sublist for sublist in board) or any(
            ['white', 'queenPiece'] in sublist for sublist in board)):
        return 'black'

#сообщение о победе
def msg_win(winner):
    Tk().wm_withdraw()
    if winner == 'white':
        msgbox.showinfo('Победа!', 'победила сторона белых')
    elif winner == 'black':
        msgbox.showinfo('Победа!', 'победила сторона белых')
    exit()


def main(size):
    # здесь происходит инициализация
    pygame.init()
    width = 800
    height = 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Шашки')
    clock = pygame.time.Clock()
    running = True
    drag_piece = None
    drop_pos = None
    xy_moves = None
    #очерёдность хода
    A = 'white'
    B = 'black'
    d = {A: B, B: A}
    toggle = A
    jump_turn = 0
    # создание доски
    board_list = create_board(size)
    board_surf = draw_board(width, height, size)

    # главный цикл
    while running:
        if check_win(board_list):
            winner = check_win(board_list)
            msg_win(winner)

        piece, x, y = get_cursor_position(board_list, width, height, size)
        # цикл обработки событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if piece is not None:
                    drag_piece = piece, x, y
                    if drag_piece[0][0] == toggle:
                        moves = get_valid_moves(board_list, drag_piece, size) #доступные ходы
                        if jump_turn == 0:
                            xy_moves = [[move[1], move[0]] for move in moves if move is not None] #обработанный массив доступных ходов

            if event.type == pygame.MOUSEBUTTONUP:
                if xy_moves is not None:
                    if drop_pos:
                        piece, old_x, old_y = drag_piece
                        new_x, new_y = drop_pos
                        if check_drop_pos(board_list, drag_piece, drop_pos):
                            try:
                                exist = xy_moves.index([new_x, new_y])
                            except ValueError:
                                exist = None
                            if exist is not None: #существует ли ход, которым хочет сходить игрок в массиве доступных ходов
                                attacked_pos = check_attack(new_x, new_y, old_x, old_y)
                                board_list[new_y][new_x] = piece #перемещение пешки
                                board_list[old_y][old_x] = None #перемещение пешки
                                if attacked_pos is not None: #если ход был атакующим
                                    drag_piece = piece, new_x, new_y #обновляем переменную, чтобы получить координаты пешки после хода
                                    board_list[attacked_pos[1]][attacked_pos[0]] = None #уничтожаем атакованную пешку
                                    xy_moves = get_attack_moves(board_list, drag_piece, size) #проверяем есть ли ещё доступные ходы атаки
                                    if not xy_moves: #если нету, то заканчиваем ход
                                        jump_turn = 0
                                        toggle = d[toggle]
                                    else:
                                        jump_turn += 1 #если есть, то ход текущей стороны продолжается

                                else:
                                    toggle = d[toggle] #смена хода

                                if check_queen(new_x, new_y, board_list, size): #проверка достигла ли пешка нулевого поля вражеской стороны
                                    board_list[new_y][new_x][1] = 'queenPiece'
                if jump_turn == 0:
                    xy_moves = None
                drag_piece = None #сброс переменных
                drop_pos = None
        #все функции отрисовки
        screen.blit(board_surf, (0, 0))
        draw_pieces(screen, board_list, width, height, size) #отрисовка шашек
        draw_selector(screen, piece, x, y, width, height, size) #отрисовка рамки выбора
        draw_moves(screen, xy_moves, width, height, size) #отрисовка доступных ходов
        drop_pos = draw_drag(screen, board_list, drag_piece, width, height, size) #отрисовка drag&drop
        # обновление экрана
        clock.tick(60)
        pygame.display.update()

#что делать при закрытии окна выбора размерности
def on_closing():
    exit()

#функция отвечающая на принятую размерность поля и передающая её в основное тело игры
def close():
    global sizeField
    sizeField = combobox.get()
    root.destroy()


if __name__ == '__main__':
    sizeField = 6
    root = Tk()
    root.geometry('200x150')
    root.protocol("WM_DELETE_WINDOW", on_closing)
    l = Label(root, text='Выберите размерность поля')
    l.grid(column=0, row=0)
    combobox = ttk.Combobox(root, values=[4, 6, 8, 10, 12])
    combobox.grid(column=0, row=1)
    combobox.current(1)
    enter_button = Button(root, text='Принять', command=close)
    enter_button.grid(column=0, row=2)
    root.mainloop()
    main(int(sizeField))
