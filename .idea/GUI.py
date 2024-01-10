import pygame
import time

pygame.font.init()

class Grid:
    # Your Sudoku grid
    board = [
        [7, 6, 4, 5, 1, 2, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 1, 2, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, 2],
        [6, 8, 0, 9, 2, 0, 0, 0, 1],
        [0, 0, 2, 0, 4, 6, 0, 5, 0],
        [0, 0, 0, 6, 0, 7, 0, 4, 8],
        [8, 0, 5, 0, 0, 0, 0, 0, 6],
        [0, 7, 6, 0, 3, 8, 0, 0, 0]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.model = [[0 for _ in range(cols)] for _ in range(rows)]
        self.selected = None
        self.font = pygame.font.SysFont("comicsans", 40)

    def draw(self, window):
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1

            pygame.draw.line(window, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(window, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.draw_number(window, self.board[i][j], i, j)

        if self.selected:
            self.draw_selection(window, self.selected)

    def draw_number(self, window, num, row, col):
        font = self.font.render(str(num), True, (0, 0, 0))
        gap = self.width / 9
        x = col * gap + (gap / 2 - font.get_width() / 2)
        y = row * gap + (gap / 2 - font.get_height() / 2)
        window.blit(font, (x, y))

    def draw_selection(self, window, pos):
        pygame.draw.rect(window, (255, 0, 0), (pos[1] * (self.width / 9), pos[0] * (self.height / 9),
                                               self.width / 9, self.height / 9), 3)

    def is_valid_move(self, num, pos):
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.is_valid_move(i, (row, col)):
                self.board[row][col] = i

                if self.solve():
                    return True

                self.board[row][col] = 0
        return False

    def set_value(self, val):
        if self.selected:
            row, col = self.selected
            if self.board[row][col] == 0:
                self.board[row][col] = val

def main():
    width, height = 540, 540
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sudoku Solver")
    clock = pygame.time.Clock()
    running = True
    grid = Grid(9, 9, width, height)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                grid.selected = (pos[1] // (width // 9), pos[0] // (height // 9))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.solve()
                elif event.key == pygame.K_BACKSPACE:
                    grid.set_value(0)
                elif pygame.K_0 <= event.key <= pygame.K_9:
                    grid.set_value(event.key - pygame.K_0)

        window.fill((255, 255, 255))
        grid.draw(window)
        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

