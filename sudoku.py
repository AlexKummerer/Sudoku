import pygame
import time

pygame.init()


WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600  # Adjust window size for side margins
GRID_WIDTH, GRID_HEIGHT = 480, 480  # Sudoku grid dimensions

# Screen dimensions
CELL_SIZE = GRID_WIDTH // 9
LINE_COLOR = (0, 0, 0)
MARGIN = (WINDOW_WIDTH - GRID_WIDTH) // 2  # Calculate the margin for centering

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
FONT = pygame.font.Font(None, 36)
HEADLINE_FONT = pygame.font.Font(None, 48)
MESSAGE_FONT = pygame.font.Font(None, 36)
SUGGESTION_FONT = pygame.font.Font(None, 24)


# Sample Sudoku board
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

initial_cells = [[bool(cell) for cell in row] for row in sudoku_board]

suggestions = [[[] for _ in range(9)] for _ in range(9)]


def draw_grid(screen):
    for x in range(0, GRID_WIDTH, CELL_SIZE):
        if x % (CELL_SIZE * 3) == 0:
            pygame.draw.line(
                screen,
                BLACK,
                (x + MARGIN, CELL_SIZE),
                (x + MARGIN, GRID_HEIGHT + CELL_SIZE),
                4,
            )
            pygame.draw.line(
                screen,
                BLACK,
                (MARGIN, x + CELL_SIZE),
                (GRID_WIDTH + MARGIN, x + CELL_SIZE),
                4,
            )
        else:
            pygame.draw.line(
                screen,
                GRAY,
                (x + MARGIN, CELL_SIZE),
                (x + MARGIN, GRID_HEIGHT + CELL_SIZE),
                1,
            )
            pygame.draw.line(
                screen,
                GRAY,
                (MARGIN, x + CELL_SIZE),
                (GRID_WIDTH + MARGIN, x + CELL_SIZE),
                1,
            )


def draw_numbers(screen, board):

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                num_text = FONT.render(
                    str(board[i][j]), True, BLACK if initial_cells[i][j] else BLUE
                )
                screen.blit(num_text, (j * CELL_SIZE + 80, i * CELL_SIZE + 70))


def get_cell_pos(mouse_pos):
    x, y = mouse_pos
    grid_x, grid_y = (x - MARGIN) // CELL_SIZE, (y - CELL_SIZE) // CELL_SIZE
    if 0 <= grid_x < 9 and 0 <= grid_y < 9:
        return grid_x, grid_y
    return None


def draw_suggestions(screen):
    """Draw suggestions in the cells."""
    for i in range(9):
        for j in range(9):
            if suggestions[i][j]:
                for num in suggestions[i][j]:
                    row = (num - 1) // 3
                    col = (num - 1) % 3

                    suggestion_text = SUGGESTION_FONT.render(str(num), True, GRAY)
                    screen.blit(
                        suggestion_text,
                        (
                            j * CELL_SIZE + col * 15 + 8 + MARGIN,
                            i * CELL_SIZE + row * 15 + 60,
                        ),
                    )


def draw_button(screen, rect, text):
    """Draw a button with text."""
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    button_text = FONT.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)


def draw_suggestion_mode(screen, suggestion_mode):
    """Draw the suggestion mode indicator."""
    mode_text = "Suggestions: ON" if suggestion_mode else "Suggestions: OFF"
    mode_color = GREEN if suggestion_mode else RED
    suggestion_mode_text = SUGGESTION_FONT.render(mode_text, True, mode_color)
    screen.blit(
        suggestion_mode_text, (WINDOW_WIDTH - suggestion_mode_text.get_width() - 10, 5)
    )


def draw_headline(screen):
    """Draw the headline."""
    headline_text = HEADLINE_FONT.render("Sudoku Game", True, BLACK)
    screen.blit(headline_text, (WINDOW_WIDTH // 2 - headline_text.get_width() // 2, 10))


def is_button_clicked(rect, pos):
    """Check if a button is clicked."""
    return rect.collidepoint(pos)


def draw_message(screen, message, color):
    """Draw a message on the screen."""
    message_text = MESSAGE_FONT.render(message, True, color)
    screen.blit(
        message_text,
        (WINDOW_WIDTH // 2 - message_text.get_width() // 2, WINDOW_HEIGHT - 100),
    )


def is_valid_board(board):

    def is_valid_block(block):
        print(block)
        nums = [num for num in block if num != 0]
        print(nums)
        return len(block) == len(set(nums))

    # check rows
    for row in board:
        print("Rows", row)
        if not is_valid_block(row):
            return False
    # check columns
    for col in range(9):
        if not is_valid_block([board[row][col] for row in range(9)]):
            return False

    # check 3x3 sub-grides
    for block_row in range(3):
        for block_col in range(3):
            block = [
                board[r][c]
                for r in range(block_row * 3, (block_row + 1) * 3)
                for c in range(block_col * 3, (block_col + 1) * 3)
            ]
            if not is_valid_block(block):
                return False

    return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()
    selected_cell = None
    running = True
    message = ""
    message_color = BLACK
    suggestion_mode = False

    # Button rect
    submit_button = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - 50, 100, 40)

    while running:
        screen.fill(WHITE)
        draw_headline(screen)
        draw_grid(screen)
        draw_numbers(screen, sudoku_board)
        draw_suggestions(screen)
        draw_button(screen, submit_button, "Submit")
        draw_message(screen, message, message_color)
        draw_suggestion_mode(screen, suggestion_mode)

        if selected_cell:
            pygame.draw.rect(
                screen,
                BLUE,
                (
                    selected_cell[0] * CELL_SIZE + MARGIN,
                    selected_cell[1] * CELL_SIZE + CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                ),
                3,
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_button_clicked(submit_button, mouse_pos):
                    if is_valid_board(sudoku_board):
                        message = "Congratulations! The board is correctly filled."
                        message_color = GREEN
                    else:
                        message = "There are errors in the board."
                        message_color = RED
                else:
                    cell_pos = get_cell_pos(mouse_pos)
                    if cell_pos and not initial_cells[cell_pos[1]][cell_pos[0]]:
                        selected_cell = cell_pos
                    else:
                        selected_cell = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    suggestion_mode = not suggestion_mode
                elif selected_cell:
                    x, y = selected_cell
                    if event.key == pygame.K_BACKSPACE or event.unicode == "0":
                        sudoku_board[y][x] = 0
                        suggestions[y][x] = []
                    elif event.unicode.isdigit() and int(event.unicode) in range(1, 10):
                        num = int(event.unicode)
                        if suggestion_mode:
                            if num in suggestions[y][x]:
                                suggestions[y][x].remove(num)
                            else:
                                suggestions[y][x].append(num)
                        else:
                            if not initial_cells[y][
                                x
                            ]:  # Check if the cell is not an initial cell
                                sudoku_board[y][x] = num
                                suggestions[y][
                                    x
                                ] = []  # Clear suggestions when a number is set

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == "__main__":
    main()
