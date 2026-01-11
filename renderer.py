from game_logic import BoardState
import pygame

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
            "PawnW" : pygame.image.load("images/white_pawn.png"),
            "PawnB" : pygame.image.load("images/black_pawn.png"),
            "BishopW": pygame.image.load("images/white_bishop.png"),
            "BishopB": pygame.image.load("images/black_bishop.png"),
            "RookW": pygame.image.load("images/white_rook.png"),
            "RookB": pygame.image.load("images/black_rook.png"),
            "QueenW": pygame.image.load("images/white_queen.png"),
            "QueenB": pygame.image.load("images/black_queen.png"),
            "KnightW": pygame.image.load("images/white_knight.png"),
            "KnightB": pygame.image.load("images/black_knight.png"),
            "KingW": pygame.image.load("images/white_king.png"),
            "KingB": pygame.image.load("images/black_king.png"),
            }

def draw():
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(screen, COLORS[(r+c)%2],(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
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
            else:
                board.move(selected[0], selected[1], row, col)
                selected = None

    draw()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()