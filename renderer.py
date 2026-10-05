import random

import pygame

from game_logic import BoardState

WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 8
COLORS = [(109, 129, 150), (210, 180, 140), (100, 100, 100)]
ROWS, COLS = 8, 8

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

board = BoardState()
selected = None

images = {
            "PawnW" : pygame.image.load("assets/images/white_pawn.bmp"),
            "PawnB" : pygame.image.load("assets/images/black_pawn.bmp"),
            "BishopW": pygame.image.load("assets/images/white_bishop.bmp"),
            "BishopB": pygame.image.load("assets/images/black_bishop.bmp"),
            "RookW": pygame.image.load("assets/images/white_rook.bmp"),
            "RookB": pygame.image.load("assets/images/black_rook.bmp"),
            "QueenW": pygame.image.load("assets/images/white_queen.bmp"),
            "QueenB": pygame.image.load("assets/images/black_queen.bmp"),
            "KnightW": pygame.image.load("assets/images/white_knight.bmp"),
            "KnightB": pygame.image.load("assets/images/black_knight.bmp"),
            "KingW": pygame.image.load("assets/images/white_king.bmp"),
            "KingB": pygame.image.load("assets/images/black_king.bmp"),
            }

captureSound = pygame.mixer.Sound("assets/sound/capture.mp3")
moveSound = pygame.mixer.Sound("assets/sound/move-self.mp3")

def draw_possible_moves(selected):
    legal = board.get_legal_moves(selected[0], selected[1])
    for move in legal:
        if board.getPiece(move[0], move[1]) is None:
            pygame.draw.circle(screen,COLORS[2],((move[1]*CELL_SIZE)+CELL_SIZE//2,(move[0]*CELL_SIZE)+CELL_SIZE//2),40)
        elif board.getPiece(move[0],move[1]).color != board.getPiece(selected[0],selected[1]).color:
            pygame.draw.circle(screen,COLORS[2],((move[1]*CELL_SIZE)+CELL_SIZE//2,(move[0]*CELL_SIZE)+CELL_SIZE//2),50, 8)

SQUARES = [pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE) 
           for r in range(ROWS) 
           for c in range(COLS) 
           ]

def draw():
    for r in range(ROWS):
        for c in range(COLS):
            color = COLORS[(r + c) % 2]
            pygame.draw.rect(screen, color, SQUARES[r * COLS + c])
    if selected:
        draw_possible_moves(selected)
    for r in range(ROWS):
        for c in range(COLS):
            piece = board.getPiece(r,c)
            if piece:
                screen.blit(images[piece.name + piece.color[0].upper()],(c*CELL_SIZE,r*CELL_SIZE))
                
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE
            if selected is None:
                piece = board.getPiece(row, col)
                if piece and piece.color == board.turn:
                    selected = (row, col)
                    
            elif selected == (row,col):
                selected = None

            elif board.getPiece(row, col) is not None and board.getPiece(selected[0], selected[1]).color == board.getPiece(row, col).color:
                selected = (row, col)

            else:
                legal_moves = board.get_legal_moves(selected[0], selected[1])

                if (row, col) in legal_moves:
                    board.simulate_move(selected[0], selected[1], row, col)
                    moves = board.get_all_legal_moves()
                    if moves:
                        start, peices = random.choice(moves)
                        end = random.choice(peices)
                        board.simulate_move(start[0], start[1], end[0], end[1])
                selected = None

                






    draw()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()