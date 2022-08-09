import drawboard as db
import pygame
import sys
import math
import os
import random
from pygame.locals import *

SCREEN = pygame.display.set_mode((600, 650))
CLOCK = pygame.time.Clock()
score = 0
popup_panel = pygame.Rect(SCREEN.get_width() / 2 - 125, SCREEN.get_height() / 2 - 80, 250, 150)
file_path = os.path.dirname(os.path.realpath(__file__))
data_path = file_path + '/sudoku_data.txt'

running = {'main_menu': True}

def change_scene(scene: str):
    for i in range(len(running)):
        running[i] = False
    running[scene] = True

def main():
    pygame.init()
    pygame.display.set_caption("Sudoku")
    pygame.display.set_icon(pygame.image.load(file_path + '/images/icon.png'))
    SCREEN.fill((255, 255, 255))
    pygame.display.flip()
    main_menu()

def solve_sudoku():
    SCREEN.fill((255, 255, 255))
    
    change_scene('solve_sudoku')
    sudoku = db.Draw_board(SCREEN, (207, 232, 230), (60, 67, 77), file_path + '/Fonts/numberFont.ttf', SCREEN, data_path, (255, 221, 194), 9, 20)
    sudoku.draw_sudoku()
    # solve button
    solve_button = pygame.Rect(SCREEN.get_width() - 80, SCREEN.get_height() - 40, 75, 30)
    # back button
    back_button = pygame.Rect(20, SCREEN.get_height() - 40, 75, 30)
    # game loop
    while running['solve_sudoku']:
        for event in pygame.event.get():
            py_quit(event)
            event_handler(event, sudoku)
            sudoku.move_with_arrows(event)
        # buttons
        if not sudoku.checked:
            on_button_press(SCREEN, solve_button, 'Solve', 18, (143, 207, 202), (118, 151, 171), solved, sudoku)
        else:
            on_button_press(SCREEN, solve_button, 'Refresh', 18, (143, 207, 202), (118, 151, 171), sudoku.clear_board)
        on_button_press(SCREEN, back_button, 'back', 18, (143, 207, 202), (118, 151, 171), main_menu)

        pygame.display.update()
        pygame.display.flip()
        CLOCK.tick(60)

def solved(sudoku: db.Draw_board):
    solve_text = sudoku.solve_my_sudoku()
    if solve_text == 'Solved!':
        text = pygame.font.Font(file_path + '/Fonts/numberFont.ttf', 25).render("Solved!", True, (109, 230, 76))
    else:
        text = pygame.font.Font(file_path + '/Fonts/numberFont.ttf', 25).render(solve_text, True, (255, 92, 92))
    SCREEN.blit(text, (SCREEN.get_width()//2 - text.get_width() / 2, SCREEN.get_height() - 40))

def difficulty_menu():
    SCREEN.fill((255, 255, 255))
    change_scene('difficulty_menu')
    # easy button
    easy_button = pygame.Rect(SCREEN.get_width() / 2 - 100, SCREEN.get_height() / 2 - 180, 200, 50)
    # medium button
    medium_button = pygame.Rect(SCREEN.get_width() / 2 - 100, SCREEN.get_height() / 2 - 120, 200, 50)
    # hard button
    hard_button = pygame.Rect(SCREEN.get_width() / 2 - 100, SCREEN.get_height() / 2 - 60, 200, 50)
    # extreme button
    extreme_button = pygame.Rect(SCREEN.get_width() / 2 - 100, SCREEN.get_height() / 2, 200, 50)
    # text
    select_difficulty_text = pygame.font.Font(file_path + '/Fonts/numberFont.ttf', 30).render("Select Difficulty", True, (143, 207, 202))
    select_difficulty_text_bg = pygame.font.Font(file_path + '/Fonts/numberFont.ttf', 30).render("Select Difficulty", True, (118, 151, 171))
    # back button
    back_button = pygame.Rect(20, SCREEN.get_height() - 40, 75, 30)
    # loop
    while running['difficulty_menu']:
        for event in pygame.event.get():
            py_quit(event)
        on_button_press(SCREEN, easy_button, 'Easy', 20, (143, 207, 202), (118, 151, 171), game, 'easy')
        on_button_press(SCREEN, medium_button, 'Medium', 20, (143, 207, 202), (118, 151, 171), game)
        on_button_press(SCREEN, hard_button, 'Hard', 20, (143, 207, 202), (118, 151, 171), game, 'hard')
        on_button_press(SCREEN, extreme_button, 'Extreme', 20, (143, 207, 202), (118, 151, 171), game, 'extreme')
        on_button_press(SCREEN, back_button, 'Back', 15, (143, 207, 202), (118, 151, 171), main_menu)
        SCREEN.blit(select_difficulty_text_bg, (SCREEN.get_width() / 2 - select_difficulty_text_bg.get_width() / 2 - 2, SCREEN.get_height() / 2 - select_difficulty_text_bg.get_height() / 2 + 100))
        SCREEN.blit(select_difficulty_text, (SCREEN.get_width() / 2 - select_difficulty_text.get_width() / 2, SCREEN.get_height() / 2 - select_difficulty_text.get_height() / 2 + 100))
        pygame.display.update()
        pygame.display.flip()
        CLOCK.tick(60)

def game(board_difficulty: str = 'medium'):
    SCREEN.fill((255, 255, 255))
    sudoku_data = []
    change_scene('game')

    difficulty = {'easy': 15, 'medium': 25, 'hard': 40, 'extreme': 60}
    
    sudoku = db.Draw_board(SCREEN, (207, 232, 230), (60, 67, 77), file_path + '/Fonts/numberFont.ttf', SCREEN, data_path, (255, 221, 194), 9, difficulty[board_difficulty])
    # check if file exists
    if os.path.exists(data_path) and os.path.getsize(data_path) > 0:
        sudoku.load_game(data_path)
    else:
        sudoku.generate(animate=True)
    # check button 
    check_button = pygame.Rect(SCREEN.get_width() - 80, SCREEN.get_height() - 40, 75, 30)
    # back button
    back_button = pygame.Rect(20, SCREEN.get_height() - 40, 75, 30)
    # new game button 
    new_game_button = pygame.Rect(100, SCREEN.get_height() - 40, 75, 30)
    # Save panel text
    save_text = pygame.font.SysFont('Arial', 18).render('Do you want to save?', True, (0, 0, 0))
    saved_text = pygame.font.SysFont('Arial', 18).render('saved', True, (143, 207, 202))
    # save button
    save_button = pygame.Rect(SCREEN.get_width() // 2 - 100, SCREEN.get_height() // 2 + 10, 75, 30)
    save_button_bottom = pygame.Rect(180, SCREEN.get_height() - 40, 75, 30)
    # don't save button
    dont_save_button = pygame.Rect(SCREEN.get_width() // 2 + 10, SCREEN.get_height() // 2 + 10, 100, 30)
    save_panel_visible = False
    # game loop
    while running['game']:
        if save_panel_visible:
            on_button_press(SCREEN, save_button, 'Save', 18, (143, 207, 202), (118, 151, 171), save_sudoku, sudoku)
            on_button_press(SCREEN, dont_save_button, 'Don\'t Save', 18, (143, 207, 202), (118, 151, 171), sys.exit)
            for event in pygame.event.get():
                py_quit(event)
        else:
            if not sudoku.checked:
                if sudoku.no_empty_blocks:
                    on_button_press(SCREEN, check_button, 'Check', 18, (143, 207, 202), (118, 151, 171), check_answer, sudoku)
                else:
                    pygame.draw.rect(SCREEN, (255, 255, 255), check_button)
            else:
                pygame.draw.rect(SCREEN, (255, 255, 255), check_button)
                checked_text = pygame.font.SysFont('Arial', 18).render('Checked', True, (143, 207, 202))
                SCREEN.blit(checked_text, (check_button.x + check_button.width / 2 - checked_text.get_width() / 2, check_button.y + check_button.height / 2 - checked_text.get_height() / 2))
            on_button_press(SCREEN, new_game_button, 'new', 18, (143, 207, 202), (118, 151, 171), sudoku.new_game, data_path, True)
            on_button_press(SCREEN, back_button, 'back', 18, (143, 207, 202), (118, 151, 171), main_menu)
            if not sudoku.saved:
                on_button_press(SCREEN, save_button_bottom, 'save', 18, (143, 207, 202), (118, 151, 171), sudoku.save_game, data_path)
            else:
                pygame.draw.rect(SCREEN, (255, 255, 255), save_button_bottom)
                SCREEN.blit(saved_text, (save_button_bottom.x + save_button_bottom.width / 2 - saved_text.get_width() / 2, save_button_bottom.y + save_button_bottom.height / 2 - saved_text.get_height() / 2))
            pygame.display.update()
            for event in pygame.event.get():
                event_handler(event, sudoku)
                sudoku.move_with_arrows(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        sudoku.save_game(data_path)
                    if event.key == pygame.K_RETURN:
                        check_answer(sudoku)
                    elif event.key == pygame.K_TAB:
                        sudoku.jump_to_next_empty_block()
                if event.type == pygame.QUIT:
                    if sudoku.saved:
                        pygame.quit()
                        sys.exit()
                    else:
                        pygame.draw.rect(SCREEN, (255, 255, 255), popup_panel, 0, 10)
                        SCREEN.blit(save_text, (SCREEN.get_width()//2 - save_text.get_width() / 2, SCREEN.get_height()//2 - 50))
                        save_panel_visible = True
        pygame.display.update()
        pygame.display.flip()
        CLOCK.tick(60)

def save_popup(sudoku, save_button, dont_save_button):
    on_button_press(SCREEN, save_button, 'Save', 18, (143, 207, 202), (118, 151, 171), save_sudoku, sudoku)
    on_button_press(SCREEN, dont_save_button, 'Don\'t Save', 18, (143, 207, 202), (118, 151, 171), sys.exit)
    if not popup_panel.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            return False
    return True 

def main_menu():
    SCREEN.fill((255, 255, 255))
    change_scene('main_menu')
    # sudoku logo
    sudoku_logo = pygame.image.load(file_path + '/images/sudokuLogo.png')
    sudoku_logo = pygame.transform.scale(sudoku_logo, (sudoku_logo.get_width(), sudoku_logo.get_height()))
    sudoku_logo.convert(SCREEN)
    # info button
    info_button = pygame.Rect(SCREEN.get_width() - 90, 20, 75, 30)
    # solve my sudoku button
    solve_sudoku_button = pygame.Rect(SCREEN.get_width() / 2 - 100, SCREEN.get_height() / 2, 200, 50)
    # start button
    start_button = pygame.Rect(SCREEN.get_width() / 2 - 100, SCREEN.get_height() / 2 + 60, 200, 50)
    # quit button
    quit_button = pygame.Rect(SCREEN.get_width() / 2 - 100, SCREEN.get_height() / 2 + 120, 200, 50)
    # loop
    frame = 0
    while running['main_menu']:
        for event in pygame.event.get():
            py_quit(event)
        on_image_press(SCREEN, '/images/info_button.png', info_button, 1, 3, '/images/info_hover.png', info_screen)
        on_button_press(SCREEN, solve_sudoku_button, 'Solve my Sudoku!', 18, (143, 207, 202), (118, 151, 171), solve_sudoku)
        if os.path.exists(data_path) and os.path.getsize(data_path) > 0:
            on_button_press(SCREEN, start_button, 'Continue', 18, (143, 207, 202), (118, 151, 171), game)
        else:
            on_button_press(SCREEN, start_button, 'Start', 25, (71, 71, 71), (145, 141, 141), difficulty_menu)
        on_button_press(SCREEN, quit_button, 'Quit', 20, (255, 103, 92), (255, 0, 0), pygame.quit)
        SCREEN.blit(sudoku_logo, (SCREEN.get_width()//2 - sudoku_logo.get_width()//2, SCREEN.get_height()//2 - sudoku_logo.get_height() - 50))
        pygame.display.update()
        CLOCK.tick(60)

def info_screen():
    SCREEN.fill((255, 255, 255))
    change_scene('info_screen')
    back_button = pygame.Rect(20, SCREEN.get_height() - 40, 75, 30)
    title_text = pygame.font.SysFont('Arial', 30).render('How to play?', True, (251, 242, 54))
    info_text = 'Sudoku is a logic puzzle where each row, column, and box contains\n all of the digits from 1 to 9. The objective is to fill each row, column, \nand box with the correct numbers.\nThe only rule is, you can\'t enter the numbers that already in the \nsame column, row, or block with the selected one!\n\nUse the arrow keys to select blocks\nor just use your mouse to pick, one.\n You can input a number between 1-9 on your keyboard.\nYou can also hit the tab key in order to move to the next empty block. \nUsing the enter key or check button will allow you to check your answer.\nDon\'t forget to save your progress! \nYou can also use the cntrl + s shortcut to save your game.'
    while running['info_screen']:
        for event in pygame.event.get():
            py_quit(event)
        SCREEN.blit(title_text, (20, 40))
        multiple_line_text(SCREEN, info_text, pygame.font.SysFont('Arial',18), (251, 134, 54), [20, 40 + title_text.get_height() + 20])
        on_button_press(SCREEN, back_button, 'Back', 18, (143, 207, 202), (118, 151, 171), main_menu)
        pygame.display.update()
        pygame.display.flip()
        CLOCK.tick(60)

def event_handler(event, sudoku):
    if event.type == pygame.KEYDOWN:
        if str(event.unicode) != '' and str(event.unicode) in ''.join(str(i) for i in range(1, sudoku.size + 1)):
            sudoku.input_num(int(event.unicode))
        if event.key == pygame.K_BACKSPACE:
            sudoku.remove_num()
        if event.key == pygame.K_r:
            sudoku.new_game(data_path)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if pygame.mouse.get_cursor()[0] < sudoku.size * sudoku.size and not sudoku.checked:
            sudoku.checked = False
            sudoku.select_block(pygame.mouse.get_pos())
    
def py_quit(event: pygame.event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

def check_answer(sudoku: db.Draw_board):
    if not sudoku.no_empty_blocks and not sudoku.checked:
        return
    score = sudoku.my_score((250, 182, 177), (184, 250, 177))
    score_text = pygame.font.Font(file_path + '/Fonts/numberFont.ttf', 20).render(('Score: ' + str(score)), True, (60, 67, 77))
    rect = pygame.Rect(SCREEN.get_width()//2, SCREEN.get_height() - 40, score_text.get_width(), score_text.get_height())
    pygame.draw.rect(SCREEN, (255, 255, 255), rect, 0, 10)
    SCREEN.blit(score_text, (SCREEN.get_width()//2, SCREEN.get_height() - 40))

def multiple_line_text(screen, text, font, color, pos: [int, int]):
    lines = text.split('\n')
    for line in lines:
        screen.blit(font.render(line, True, color), pos)
        pos[1] += font.get_height()

def on_button_press(screen: pygame.Surface, button_rect: pygame.Rect, button_str: str, font_size: int, color: tuple, hover_color: tuple, call_func: callable, *args):
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 0, 10)
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, hover_color, button_rect, 2, 10)
        button_text = pygame.font.SysFont('Arial', font_size).render(button_str, True, hover_color)
        if pygame.mouse.get_pressed()[0]:
            call_func(*args)
    else:
        pygame.draw.rect(screen, color, button_rect, 2, 10)
        button_text = pygame.font.SysFont('Arial', font_size).render(button_str, True, color)
    screen.blit(button_text, (button_rect.x + button_rect.width / 2 - button_text.get_width() / 2, button_rect.y + button_rect.height / 2 - button_text.get_height() / 2))
    pygame.display.update()

def on_image_press(screen: pygame.Surface, image: str, button_rect: pygame.Rect, scale_up: int, scale_down, hover_image: str, call_func: callable, *args):
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 0, 10)

    if hover_image == '':
        hover_image = image
    
    hover_image = pygame.image.load(file_path + hover_image).convert_alpha()
    hover_image = pygame.transform.scale(hover_image, ((hover_image.get_width() * scale_up) // scale_down, (hover_image.get_height() * scale_up) // scale_down))
    hover_image.convert(screen)

    img = pygame.image.load(file_path + image).convert_alpha()
    img = pygame.transform.scale(img, ((img.get_width() * scale_up) // scale_down, (img.get_height() * scale_up) // scale_down))
    img.convert(screen)
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        screen.blit(hover_image, (button_rect.x + button_rect.width / 2 - hover_image.get_width() / 2, button_rect.y + button_rect.height / 2 - hover_image.get_height() / 2))
        if pygame.mouse.get_pressed()[0]:
            call_func(*args)
    else:
        screen.blit(img, (button_rect.x + button_rect.width / 2 - img.get_width() / 2, button_rect.y + button_rect.height / 2 - img.get_height() / 2))
    pygame.display.update()
    
def save_sudoku(sudoku: db.Draw_board):
    sudoku.save_game(data_path)
    pygame.quit()
    sys.exit()

main()