import pygame
import os
import sys
import draw


CLOCK = pygame.time.Clock()
hour, minute, second, text = 0, 0, 0, "0:0:0".rjust(3)
file_path = os.path.dirname(os.path.realpath(__file__))

def main():
    global hour, minute, second, text, file_path
    pygame.init()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    pygame.display.set_caption("NumPuz")
    screen = pygame.display.set_mode((600, 700))
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont("comicsansms", 30)
    numpuz = draw.drawNumPuzz(5, screen, font, file_path + "/images/puzzle_01.jpg")
    preview_on = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT and not numpuz.check_win() and not preview_on: 
                if second == 59:
                    second = 0
                    minute += 1
                    if minute == 59:
                        minute = 0
                        hour += 1
                second += 1
                text = f'{hour}:{minute}:{second}'.rjust(3)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                numpuz.move_blocks(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    hour, minute, second, text = 0, 0, 0, "0:0:0".rjust(3)
                    numpuz.generate()
                    numpuz.draw()
                if event.key == pygame.K_p:
                    preview_on = not preview_on
        
        screen.fill((255, 255, 255))
        screen.blit(font.render(text, True, (0, 0, 0)), (10, screen.get_height() - 50))
        if preview_on:
            numpuz.draw_preview()
        else:
            numpuz.draw()
        pygame.display.update()
        CLOCK.tick(60)
    pygame.quit()
    sys.exit()

main()