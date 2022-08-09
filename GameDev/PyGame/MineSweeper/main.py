import pygame
import sys
import os
import draw_board as db
import random

file_path = os.path.dirname(os.path.realpath(__file__))
flag_image = pygame.image.load(file_path + '/Images/flag.png')
mine_image = pygame.image.load(file_path + '/Images/mine.png')
icon_image = pygame.image.load(file_path + '/Images/logo.png')
CLOCK = pygame.time.Clock()
SCENE = {'menu': True, 'game': False, 'end': False}

pygame.init()
screen = pygame.display.set_mode((600, 600))
color_hue = -1
size_input = 10
difficulty_input = size_input + size_input // 5
color_randomize = False
board = db.Draw(screen=screen, size=15, difficulty=20, mine_image=mine_image, flag_image=flag_image, color_block_1_hsv=(color_hue, 13, 92), color_block_2_hsv=(202, 28, 93))

def main():
    global file_path, mine_image, flag_image, icon_image, board, screen, color_hue, color_randomize
    screen.fill((255, 255, 255))
    pygame.display.set_caption('MineSweeper')
    pygame.display.set_icon(icon_image)
    pygame.display.flip()
    hour_min_sec, time_display = [0, 0, 0], "0:0:0".rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    
    db.Draw(screen=screen, size=4, color_block_1_hsv=(0, 13, 92), color_block_2_hsv=(0, 28, 92)).draw_board()
    while True:
        if SCENE['menu']:
            start_menu()
        elif SCENE['game']:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if color_randomize or color_hue == -1:
                            color_hue = random.randint(0, 360)
                        board = db.Draw(screen=screen, size=size_input, difficulty=difficulty_input, mine_image=mine_image, flag_image=flag_image, color_block_1_hsv=(color_hue, 13, 92), color_block_2_hsv=(color_hue, 28, 93))
                        board.draw_board()
                    elif event.key == pygame.K_ESCAPE:
                        if board.game_state == 'won' or board.game_state == 'lost':
                            change_scene('menu')
                        elif board.game_state == 'paused': 
                            board.game_state = 'playing'
                            board.draw_board()
                        elif board.game_state == 'playing': 
                            board.game_state = 'paused' 
                    elif event.key == pygame.K_c:
                        color_randomize = not color_randomize
                    elif event.key == pygame.K_r:
                        hour_min_sec, time_display = [0, 0, 0], '0:0:0'.rjust(3)
                time_display = update_timer(event, hour_min_sec, board)
                board.event_handler(event)
            pause_menu(400, 200, time_display, board, color_hue)
            if board.game_state == 'won' or board.game_state == 'lost':
                score_popup(350, 200, time_display, board, color_hue)
                
        pygame.display.update()
        CLOCK.tick(60)
    pygame.quit()
    sys.exit()  

def update_timer(event, hour_min_sec: [int], board):
    if event.type == pygame.USEREVENT and board.game_state == 'playing' and len(board.revealed_blocks) > 0: 
        if hour_min_sec[2] == 59:
            hour_min_sec[2] = 0
            hour_min_sec[1] += 1
            if hour_min_sec[1] == 59:
                hour_min_sec[1] = 0
                hour_min_sec[0] += 1
        hour_min_sec[2] += 1
    return f'{hour_min_sec[0]}:{hour_min_sec[1]}:{hour_min_sec[2]}'.rjust(3)

def score_popup(width, height, time_display, board, color_hue = 255):
    global screen
    bg = pygame.Rect(screen.get_width() / 2 - width/2, screen.get_height() / 2 - height/2, width, height)
    pygame.draw.rect(screen, board.hsv_to_rgb((color_hue, 28, 30)), (screen.get_width() / 2 - width/2, screen.get_height() / 2 - height/2, width, height), 0, 5)
    font = pygame.font.SysFont('arial', 30)
    if board.game_state == 'won':
        text = font.render('You Won!', True, board.hsv_to_rgb((color_hue, 28, 93)))
    elif board.game_state == 'lost':
        text = font.render('You Lost!', True, board.hsv_to_rgb((color_hue, 60, 90)))
    time_text = font.render('Time: ' + str(time_display), True, board.hsv_to_rgb((color_hue, 28, 93)))
    screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, screen.get_height() / 2 - text.get_height() - time_text.get_height() / 2))
    screen.blit(time_text, (screen.get_width() / 2 - time_text.get_width() / 2, screen.get_height() / 2 - time_text.get_height() + text.get_height() + 20))

def pause_menu(width, height, time_display, board: db.Draw, color_hue = 255):
    global screen
    if board.game_state != 'paused':
        return
    bg = pygame.Rect(screen.get_width() / 2 - width/2, screen.get_height() - height, width, height)
    pygame.draw.rect(screen, board.hsv_to_rgb((color_hue, 28, 30)), bg, 0, 5, 5, 5, 0, 0)
    font = pygame.font.SysFont('arial', 30)
    text = font.render('Paused', True, board.hsv_to_rgb((color_hue, 28, 93)))
    screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, bg.centery - 60))
    font = pygame.font.SysFont('arial', 20)
    main_menu_button = pygame.Rect(bg.centerx - width/2 + 30, bg.centery + 25, width - 60, 35)
    main_menu_text = font.render('Main Menu', True, board.hsv_to_rgb((color_hue, 16, 100)))
    screen.blit(main_menu_text, (main_menu_button.x + main_menu_button.width/2 - main_menu_text.get_width()/2, main_menu_button.y + main_menu_button.height/2 - main_menu_text.get_height()/2))
    pygame.draw.rect(screen, board.hsv_to_rgb((color_hue, 28, 93)), main_menu_button, 1, 5)
    font = pygame.font.SysFont('arial', 15)
    time_text = font.render('time: ' + str(time_display), True, board.hsv_to_rgb((color_hue, 28, 93)))
    if time_display and time_display != '0:0:0'.rjust(3):
        screen.blit(time_text, (main_menu_button.centerx - 40, main_menu_button.centery - 55, 20, 20))
    if main_menu_button.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            if color_randomize:
                color_hue = -1
            hour_min_sec = [0, 0, 0]
            time_display = '0:0:0'.rjust(3) 
            change_scene('menu') 

active_box = None

def start_menu():
    global active_box, difficulty_input, size_input, color_hue, screen, board, flag_image, color_randomize
    
    # (pygame.draw.rect(screen, board.hsv_to_rgb((color_hue, 13, 92)), (screen.get_width()/i, screen.get_height()/j, screen.get_width()/4, screen.get_height()/4), 0) for i in range(4) for j in range(4))
    
    width, height = 400, 400
    bg = pygame.Rect(screen.get_width() / 2 - width / 2, screen.get_height() / 2 - 30, width, height)
    
    if size_input >= 2:
        db.Draw(screen=screen, size=size_input, color_block_1_hsv=(color_hue, 13, 92), color_block_2_hsv=(color_hue, 28, 93)).draw_board(False)
    
    pygame.draw.rect(screen, db.Draw(screen=screen).hsv_to_rgb((color_hue if color_hue != -1 else 0, 60, 30)), bg, 0, 5)
    
    color_inactive = db.Draw(screen=screen).hsv_to_rgb((color_hue if color_hue != -1 else 50, 20, 100))
    color_active = db.Draw(screen=screen).hsv_to_rgb((color_hue if color_hue != -1 else 60, 40, 100))
    
    font = pygame.font.SysFont('comicsans', 25)
    if size_input >= 2:
        dif_text = font.render('Difficulty: ' + str(difficulty_input) + f' (1 - {str(size_input ** 2 - 1)})', True, color_active if active_box == 'difficulty' else color_inactive) 
        dif_box = pygame.Rect(screen.get_width() / 2 - 150, screen.get_height() - 100, 200, 50)
        screen.blit(dif_text, dif_box)
    
    size_text = font.render('Size: ' + str(size_input) if size_input >= 1 else 'Size: (10)', True, color_active if active_box == 'size' else color_inactive)
    size_box = pygame.Rect(screen.get_width() / 2 - 150, screen.get_height() - 150, 200, 50)
    screen.blit(size_text, size_box)
    
    color_text = font.render('Color: Random (0~360)' if color_hue == -1 else 'Color: ' + str(color_hue), True, color_active if active_box == 'color' else color_inactive)
    color_box = pygame.Rect(screen.get_width() / 2 - 150, screen.get_height() - 200, 200, 50)
    
    box = pygame.Rect(color_box.right - 50, color_box.top, color_box.height, color_box.height)
    box2 = pygame.Rect(box.right, color_box.top, color_box.height, color_box.height)
    if color_hue != -1:
        pygame.draw.rect(screen, db.Draw(screen=screen).hsv_to_rgb((color_hue, 28, 93)), box, 0, 10)
        pygame.draw.rect(screen, db.Draw(screen=screen).hsv_to_rgb((color_hue, 13, 92)), box2, 0, 10)

    screen.blit(color_text, color_box)
    
    icon = pygame.transform.scale(flag_image, (flag_image.get_width() * 10, flag_image.get_height() * 10))
    screen.blit(icon, (screen.get_width() // 2 - icon.get_width() // 2 + 55, screen.get_height() // 2 - icon.get_height() // 2 - 150))
    # start button
    start_button = pygame.Rect(screen.get_width() // 2 - 50, screen.get_height() // 2, 100, 50)
    font = pygame.font.SysFont('comicsans', 30)
    screen.blit(font.render('Start', True, db.Draw(screen=screen).hsv_to_rgb((color_hue if color_hue != -1 else 56, 90, 80))), (start_button.centerx - font.size('Start')[0] // 2, start_button.centery - font.size('Start')[1] // 2))
    
    if size_input >= 2 and dif_box.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            active_box = 'difficulty'
            pygame.display.flip()
    elif size_box.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            active_box = 'size'
            pygame.display.flip()
    elif color_box.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            active_box = 'color'
            pygame.display.flip()
    
    if start_button.collidepoint(pygame.mouse.get_pos()):
        screen.blit(font.render('Start', True, db.Draw(screen=screen).hsv_to_rgb((color_hue if color_hue != -1 else 56, 100, 100))), (start_button.centerx - font.size('Start')[0] // 2, start_button.centery - font.size('Start')[1] // 2))
        if pygame.mouse.get_pressed()[0]:
            if color_hue == -1:
                color_randomize = True
                color_hue = random.randint(0, 360)
            else:
                color_randomize = False
            if size_input < 2:
                size_input = 10
            if difficulty_input == 0:
                difficulty_input = size_input + size_input // 5
            board = db.Draw(screen=screen, size=size_input, difficulty=difficulty_input, mine_image=mine_image, flag_image=flag_image, color_block_1_hsv=(color_hue, 13, 92), color_block_2_hsv=(color_hue, 28, 93))
            change_scene('game')
    
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if active_box == 'size':
            size_input = input_number(size_input, event, 30, 0)
            if difficulty_input > (size_input ** 2 - 1) or difficulty_input == 1:
                difficulty_input = size_input + size_input // 5
        elif active_box == 'difficulty':
            difficulty_input = input_number(difficulty_input, event, size_input ** 2 - 1, size_input + size_input // 5)
        elif active_box == 'color':
            color_hue = input_number(color_hue, event, 360, -1)
            

def input_number(number, event, limit = 10, default = 0):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            if len(str(number)) > 1 and number != default:
                number = int(str(number)[:-1])
            else:
                number = default
        elif event.unicode != '' and event.unicode in '1234567890' and int(str(number) + event.unicode) <= limit:
            if number == default:
                number = int(event.unicode)
            else:
                number = int(str(number) + event.unicode)
    return number
    
def change_scene(scene):
    global board
    for i in SCENE:
        SCENE[i] = False
    SCENE[scene] = True
    if scene == 'game':
        board.draw_board()
    elif scene == 'menu':
        main()
    

main()