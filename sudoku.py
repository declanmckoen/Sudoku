from classes import *

pygame.init()

# screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
screen.fill(BG_COLOR)

def title_screen(screen):
    screen.fill(BG_COLOR)

    # initialize text font
    title_font = pygame.font.Font(None, 100)
    text_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 50)
    instruction_font = pygame.font.Font(None, 30)

    # initialize and draw title
    title_surf = title_font.render("Sudoku", 0, DARKENED_LINE_COLOR)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 2 * SQUARE_SIZE))
    screen.blit(title_surf, title_rect)

    # initialize and draw text
    text_surf = text_font.render("Please select a difficulty", 0, RED)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surf, text_rect)

    # initialize and draw instructions text
    r_instruction_surf = instruction_font.render("Press \"r\" to reset the board", 0, DARKENED_LINE_COLOR)
    e_instruction_surf = instruction_font.render("Press \"e\" to exit the game", 0, DARKENED_LINE_COLOR)
    m_instruction_surf = instruction_font.render("Press \"m\" to return to the main menu", 0, DARKENED_LINE_COLOR)
    r_instruction_rect = r_instruction_surf.get_rect(center=(WIDTH // 5 - 19, 15))
    e_instruction_rect = e_instruction_surf.get_rect(center=(WIDTH // 5 - 25, 35))
    m_instruction_rect = m_instruction_surf.get_rect(center=(WIDTH // 5 + 30, 55))
    screen.blit(r_instruction_surf, r_instruction_rect)
    screen.blit(e_instruction_surf, e_instruction_rect)
    screen.blit(m_instruction_surf, m_instruction_rect)

    # initialize buttons
    easy_surf = button_font.render("EASY", 0, BG_COLOR)
    medium_surf = button_font.render("MEDIUM", 0, BG_COLOR)
    hard_surf = button_font.render("HARD", 0, BG_COLOR)
    easy_bg = pygame.Surface((easy_surf.get_size()[0] + 20, easy_surf.get_size()[1] + 20))
    easy_bg.fill(BUTTON_COLOR)
    easy_bg.blit(easy_surf, (10, 10))
    medium_bg = pygame.Surface((medium_surf.get_size()[0] + 20, medium_surf.get_size()[1] + 20))
    medium_bg.fill(BUTTON_COLOR)
    medium_bg.blit(medium_surf, (10, 10))
    hard_bg = pygame.Surface((hard_surf.get_size()[0] + 20, hard_surf.get_size()[1] + 20))
    hard_bg.fill(BUTTON_COLOR)
    hard_bg.blit(hard_surf, (10, 10))

    # initialize button rectangles
    easy_rect = easy_surf.get_rect(center=(WIDTH // 2 - SQUARE_SIZE * 2, HEIGHT // 2 + SQUARE_SIZE))
    medium_rect = medium_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + SQUARE_SIZE))
    hard_rect = hard_surf.get_rect(center=(WIDTH // 2 + SQUARE_SIZE * 2, HEIGHT // 2 + SQUARE_SIZE))
    screen.blit(easy_bg, easy_rect)
    screen.blit(medium_bg, medium_rect)
    screen.blit(hard_bg, hard_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    return 30
                if medium_rect.collidepoint(event.pos):
                    return 40
                if hard_rect.collidepoint(event.pos):
                    return 50

        pygame.display.update()

def win_screen(screen):
    screen.fill(BG_COLOR)

    # initialize text font
    win_font = pygame.font.Font(None, 100)
    exit_font = pygame.font.Font(None, 50)

    # initialize and draw win text
    win_surf = win_font.render("Game Won!", 0, DARKENED_LINE_COLOR)
    win_rect = win_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 2 * SQUARE_SIZE))
    screen.blit(win_surf, win_rect)

    # initialize exit text
    exit_surf = exit_font.render("EXIT", 0, BG_COLOR)
    exit_bg = pygame.Surface((exit_surf.get_size()[0] + 20, exit_surf.get_size()[1] + 20))
    exit_bg.fill(BUTTON_COLOR)
    exit_bg.blit(exit_surf, (10, 10))

    # initialize and draw exit button
    exit_rect = exit_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(exit_bg, exit_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

def lose_screen(screen):
    screen.fill(BG_COLOR)

    # initialize text font
    lose_font = pygame.font.Font(None, 100)
    restart_font = pygame.font.Font(None, 50)

    # initialize and draw lose text
    lose_surf = lose_font.render("Game Over!", 0, DARKENED_LINE_COLOR)
    lose_rect = lose_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 2 * SQUARE_SIZE))
    screen.blit(lose_surf, lose_rect)

    # initialize restart text
    restart_surf = restart_font.render("Restart", 0, BG_COLOR)
    restart_bg = pygame.Surface((restart_surf.get_size()[0] + 20, restart_surf.get_size()[1] + 20))
    restart_bg.fill(BUTTON_COLOR)
    restart_bg.blit(restart_surf, (10, 10))

    # initialize and draw restart button
    restart_rect = restart_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(restart_bg, restart_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return title_screen(screen)

            pygame.display.update()

def main():
    # title screen
    removed_cells = title_screen(screen)

    # sudoku screen
    board = Board(WIDTH, HEIGHT, screen, removed_cells)
    board.draw()

    current_key = None
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.update_board()
                x, y = event.pos
                col, row = board.click(x, y)
                board.select(row, col)
            if event.type == pygame.KEYDOWN:
                board.update_board()

                # if event.key != pygame.K_RETURN and event.key != pygame.K_BACKSPACE:
                if 48 < event.key <= 59:
                    current_key = event.key
                if event.key == pygame.K_0:
                    board.select(row, col)
                if event.key == pygame.K_1:
                    board.select(row, col)
                    board.sketch(1)
                if event.key == pygame.K_2:
                    board.select(row, col)
                    board.sketch(2)
                if event.key == pygame.K_3:
                    board.select(row, col)
                    board.sketch(3)
                if event.key == pygame.K_4:
                    board.select(row, col)
                    board.sketch(4)
                if event.key == pygame.K_5:
                    board.select(row, col)
                    board.sketch(5)
                if event.key == pygame.K_6:
                    board.select(row, col)
                    board.sketch(6)
                if event.key == pygame.K_7:
                    board.select(row, col)
                    board.sketch(7)
                if event.key == pygame.K_8:
                    board.select(row, col)
                    board.sketch(8)
                if event.key == pygame.K_9:
                    board.select(row, col)
                    board.sketch(9)

                if event.key == pygame.K_LEFT and x > SQUARE_SIZE:
                    x -= SQUARE_SIZE
                    col, row = board.click(x, y)
                    board.select(row, col)
                if event.key == pygame.K_RIGHT and x < WIDTH - SQUARE_SIZE:
                    x += SQUARE_SIZE
                    col, row = board.click(x, y)
                    board.select(row, col)
                if event.key == pygame.K_UP and y > SQUARE_SIZE:
                    y -= SQUARE_SIZE
                    col, row = board.click(x, y)
                    board.select(row, col)
                if event.key == pygame.K_DOWN and y < HEIGHT - SQUARE_SIZE:
                    y += SQUARE_SIZE
                    col, row = board.click(x, y)
                    board.select(row, col)

                if event.key == pygame.K_r:
                    board.reset_to_original()
                    board.update_board()
                if event.key == pygame.K_e:
                    run = False
                if event.key == pygame.K_m:
                    removed_cells = title_screen(screen)
                    board = Board(WIDTH, HEIGHT, screen, removed_cells)
                    board.draw()

                if event.key == pygame.K_RETURN and current_key is not None:
                    board.select(row, col)
                    board.place_number(current_key - pygame.K_0)
                    board.update_board()
                    board.select(row, col)

                if event.key == pygame.K_BACKSPACE:
                    board.select(row, col)
                    board.clear()
                    board.update_board()
                    board.select(row, col)

        if board.is_full():
            if board.check_board():
                pygame.display.update()
                pygame.time.delay(1000)
                win_screen(screen)
            else:
                pygame.display.update()
                pygame.time.delay(1000)
                removed_cells = lose_screen(screen)
                board = Board(WIDTH, HEIGHT, screen, removed_cells)
                board.draw()

        pygame.display.update()


if __name__ == "__main__":
    main()