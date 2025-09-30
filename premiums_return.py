### IMPORTS ###
import pygame
import local_data
import text
import subroutines
import ports
import random
import sys


def premiums_return_sub(window,canvas):
    pygame.init()
    print ("doing something")
    color_text = ('black')
    color_border = ('blue')
    color_wash = ('white')
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)

    ### 6 INITIAL TEXT ###
    title1_text = font22.render("Premiums Offered", True, color_text)
    title2_text = font22.render("Premiums Agreed", True, color_text)
    title3_text = font22.render("Remaining Book Value", True, color_text)
    cell_height = 20
    marginx = 20
    marginy = 20
    size_canv = canvas.get_size()
    size_width = size_canv[0] - 2 * marginx  # for a
    cell_width_title = 200

    menubuttontext = font22.render(" Go back to Main Menu", True, color_text)
    menubutton_clicked = False
    menubuttontext_rect = pygame.Rect(marginx, 900, cell_width_title, cell_height)
    pygame.draw.rect(canvas, color_wash, menubuttontext_rect, )
    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 1)
    canvas.blit(menubuttontext, menubuttontext_rect)
    window.blit(canvas, (0, 0))
    pygame.display.update()
    end_of_bidding=False
    m=0
    mmax=100000
    while end_of_bidding==False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                menubutton_clicked = True if menubuttontext_rect.collidepoint(event.pos) else False
            if menubutton_clicked == True:
                import main
                main_menu()
