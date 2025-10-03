
### 1 IMPORTS ###

import sys
import os
import pygame
from pygame.locals import *
import datetime
import time
import json
from ..data import local_data
from ..models import subroutines
from ..data import text_content as mytext
from ..ui.screens import ports
from ..ui.screens import goinside
from ..ui.screens import premiums_alt


def main_menu():

### 2 PYGAME INIT, WINDO AND CANVAS SISING
    pygame.init()
    clock = pygame.time.Clock()
    DISPLAY_W, DISPLAY_H = 1500, 1000
    window = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))
    canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
    pygame.display.set_caption("Edward Lloyd's Coffeehouse")
    #canvas = pygame.display.set_mode((width, height))
### 3. COLOR DEFITIONS###

    color_bg = ('black')
    color_text = ('white')
    color_border = ('blue')
    color_clickedbcg = ('grey')
    color_wash = "black"
### 4. FONT DEFINITIONS ###
    font18 = pygame.font.SysFont("Arial", 18, bold=False)
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)



    font20g = pygame.font.SysFont("Georgia", 20, bold=False)  ## clear, perhaps a little formal - the font selected
###5  TEXT POSITIONS ###
    width = 1500  # width of main frame
    height = 1000  # height of main frame
    buttonheight = 50
    buttonwidth = 300
    rightpanelimg_x = 800
    rightpanelimg_y = 50
    rightpanelimg_w = 500
    rightpanelimg_h = 400
    rightpaneltext_x = 700
    rightpaneltext_y = 500
    rightpaneltext_w = 700
    rightpaneltext_h = 500
    buttonstart_x = 50
    buttonstart_y = 50
###   6  INITIAL TEXT ###

### 7 VARIABLE INITIATIONS###


### 8 LISTS INITIATIONS ###
    button = []
    buttontext_rect = []
#############display buttons########################
    button_numb = len(local_data.button_names)
    for i in range(button_numb):
        button.append(
            subroutines.Button(buttonstart_x, (1 + i) * buttonstart_y, buttonwidth, buttonheight,
                           local_data.button_names[i][0],
                           local_data.button_names[i][1], "False"))
    for i in range(button_numb):
        if button[i].rect_color == 1:
            buttontext_rect.append(
                subroutines.Button.button_rect_blit(button[i], canvas, color_border, color_text, color_wash))
        else:
            buttontext_rect.append(subroutines.Button.button_rect_blit(button[i], canvas, color_bg, color_text, color_wash))
### 9 IMAGE LOADING
#################display coffee shop picture and caption###############
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # img1_path = os.path.join(base_dir, "Another Coffeehouse.png")
    img1 = pygame.image.load("src/assets/images/Another Coffeehouse.png")
    img1r = pygame.transform.scale(img1, (rightpanelimg_w, rightpanelimg_h))

    canvas.blit(img1r, (rightpanelimg_x, rightpanelimg_y))
    textsurf = Rect(rightpaneltext_x, rightpaneltext_y, rightpaneltext_w, rightpaneltext_h)
    subroutines.blit_text_rect_tjh(canvas, mytext.mytext0, 'white', textsurf, font20g)

##############################show logo######################################


    # logoimg_path = os.path.join(base_dir, "Logo.jpg")
    logoimg = pygame.image.load("src/assets/images/Logo.jpg")
    #logoimgr = pygame.transform.scale(img, (600, 400))
    canvas.blit(logoimg, (50, 900))

    window.blit(canvas, (0, 0))
    pygame.display.update()
    running = True

    while running:

        for event in pygame.event.get():
            #print("event type", event.type)
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(button_numb):

                    button[i].clicked = True if buttontext_rect[i].collidepoint(event.pos) else False
                    if button[i].clicked == True:
                        print(i)

                if button[1].clicked:  # Background to this series of game
                    print("page 1")
                    page_1(window, canvas)

                if button[2].clicked:  # Ports Cargo and Revenu
                    ports.ports(window, canvas)

                if button[3].clicked:  # Ship Construction and State of Repair
                    from ..ui.screens import ships

                    canvas.fill('black')
                    ships.ship_constr(window, canvas)

                if button[4].clicked:  # Shipping Routes and Ocean Drift
                    from ..ui.screens import routes

                    canvas.fill('black')
                    routes.routessub(window, canvas)

                if button[5].clicked:  # Weather and other hazards
                    from ..ui.screens import weather_hazards

                    canvas.fill('black')
                    weather_hazards.weather_sub(window, canvas)

                if button[6].clicked:  # Setting underwriter risk preference
                    from ..ui.screens import underwriter_preferences

                    canvas.fill('black')
                    underwriter_preferences.under_prefsub(window, canvas,
                                                  from_index=0)  # from index shows subroutine that request is coming from main menu

                if button[7].clicked:  # Coffeehouse - negoatiating premiums
            # import premiums_alt
                    from ..ui.screens import premiums_alt

                    canvas.fill('black')
                    #print("back here")
                    premiums_alt.premiums_alt_sub(window, canvas)
            # premiums_return.premiums_return_sub(window,canvas)
                    button[7].clicked = False  # I don't know why this should be necessary

                if button[8].clicked:  # Sources and historic notes
                    page_3(window, canvas)

                if button[9].clicked:  # Sources and historic notes
                    from ..ui.menus import settings
                    canvas.fill('black')
                    settings.settings_sub(window, canvas)

        # button 10 and 11 are inactive

                if button[12].clicked:  # start the game
                    from ..ui.screens import goinside

                    canvas.fill('black')
                    from_key=0# indicates coming direct from main menu
                    goinside.goinside_sub(window, canvas,from_key)

                if button[13].clicked:
                    pygame.quit()
                    sys.exit()

    clock.tick(1)
    pygame.display.update()


def page_1(window, canvas):  # BACKGROUND TO THIS SERIES OF GAMES
    #print("in page 1")
    ### 3 COLOR DEFINITIONS ###
    color_bg = ('black')
    color_text = ('white')
    color_border = ('blue')
    color_clickedbcg = ('grey')

    ### 4 FONT DEFINITIONS ###
    font20s = pygame.font.SysFont("Segoe", 20, bold=False)# blocky
    font20c = pygame.font.SysFont("Calibri", 20, bold=False)# spindly
    font20v = pygame.font.SysFont("Verdana", 20, bold=False)# clear , a bit clinical
    font20g = pygame.font.SysFont("Georgia", 20, bold=False) ## clear, perhaps a little formal - the font selected
    font20r = pygame.font.SysFont("Roboto", 20, bold=False) ## no this font looks congested
    font20os = pygame.font.SysFont("Open Sans", 20, bold=False) ## no this font is blocky
    font20l = pygame.font.SysFont("Lato", 20, bold=False)# also blocky
    font20p = pygame.font.SysFont("Poppins", 20, bold=False) # blocky
    font18 = pygame.font.SysFont("Arial", 18, bold=False)
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    ### 5 TEXT PISITIONS ###

    width = 1500  # width of main frame
    height = 1000  # height of main frame
    width_text = 900  # width of left panel of text
    height_text = 700
    buttonheight = 50
    leftpaneltext_x = 100
    leftpaneltext_y = 150
    leftpaneltext_w = 900
    leftpaneltext_h = 500
    buttonwidth = 150
    ### 7 VARIABLE INITIATION ###scz
    running = True
    menubutton_clicked = False
    ### INITIAL TEXT ###
    menubuttontext = font22.render(" Go back to Main Menu", True, color_text)

    canvas.fill('black')

    ### 11 RECTS ###

    menubuttontext_rect = Rect(buttonwidth, height - 2 * buttonheight, 1.5 * buttonwidth, buttonheight)

    ### 12 IMAGE LOADING ###
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # balance_img_path = os.path.join(base_dir, "Risk Reward Balance.png")
    balance_img = pygame.image.load("src/assets/images/Risk Reward Balance.png")
    balance_imgr = pygame.transform.scale(balance_img, (300, 300))
    ### 11 RECTS ###
    textsurf = Rect(leftpaneltext_x, leftpaneltext_y, leftpaneltext_w, leftpaneltext_h)
    subroutines.blit_text_rect_tjh(canvas, mytext.mytext1, 'white', textsurf, font20g)
    canvas.blit(balance_imgr, (leftpaneltext_x + leftpaneltext_w, 50))
    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 1)
    canvas.blit(menubuttontext, menubuttontext_rect)

    # logoimg_path = os.path.join(base_dir, "Logo.jpg")
    logoimg = pygame.image.load("src/assets/images/Logo.jpg")
    # logoimgr = pygame.transform.scale(img, (600, 400))
    canvas.blit(logoimg, (900, 900))

    window.blit(canvas, (0, 0))
    pygame.display.update()

    while running:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                running = False

            if event1.type == pygame.MOUSEBUTTONDOWN:
                menubutton_clicked = True if menubuttontext_rect.collidepoint(event1.pos) else False
            if menubutton_clicked == True:
                main_menu()


def page_3(window, canvas):  # sources and historic notes
    ### 3. COLOR DEFINITIONS ###
    color_bg = ('black')
    color_text = ('white')
    color_border = ('blue')
    color_clickedbcg = ('grey')
    ### 4. FONT DEFINITIONS ###
    font18 = pygame.font.SysFont("Arial", 18, bold=False)
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    font20g = pygame.font.SysFont("Georgia", 20, bold=False)  ## clear, perhaps a little formal - the font selected
    ### 5. TEXT AND IMAGE POSITIONS ###
    width = 1500  # width of main frame
    height = 1000  # height of main frame
    width_text = 800  # width of left panel of text
    height_text = 700  # width of right panel of text
    rightpanelimg_x = 800
    rightpanelimg_y = 50
    rightpanelimg_w = 500
    rightpanelimg_h = 400
    rightpaneltext_x = 100
    rightpaneltext_y = 100
    rightpaneltext_w = 700
    rightpaneltext_h = 500
    buttonwidth = 150
    buttonheight = 50
    ### 6 INITIAL TEXT ###
    menubuttontext = font22.render(" Go back to Main Menu", True, color_text)

    ### 7 VARIABLE INITIATION ###
    running = True
    menubutton_clicked = False
    ### 8 IMAGE LOADING ###
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # caird_img_path = os.path.join(base_dir, "Caird_library.jpg")
    img = pygame.image.load("src/assets/images/Caird_library.jpg")
    imgr = pygame.transform.scale(img, (600, 400))
    ### 11 RECTS ###
    menubuttontext_rect = Rect(buttonwidth, height - 2 * buttonheight, 1.5 * buttonwidth, buttonheight)
    textsurf = Rect(rightpaneltext_x, rightpaneltext_y, rightpaneltext_w, rightpaneltext_h)

    ### 12 LOAD IMAGES TO CANVAS ###
    canvas.fill(color_bg)
    canvas.blit(imgr, (width_text, 100))
    ### 13 ### DRAW RECTS ###

    subroutines.blit_text_rect_tjh(canvas, mytext.mytext3, 'white', textsurf, font20g)
    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 1)
    canvas.blit(menubuttontext, menubuttontext_rect)


    window.blit(canvas, (0, 0))
    pygame.display.update()
    while running:

        for event3 in pygame.event.get():
            if event3.type == pygame.QUIT:
                running = False

            if event3.type == pygame.MOUSEBUTTONDOWN:
                menubutton_clicked = True if menubuttontext_rect.collidepoint(event3.pos) else False
            if menubutton_clicked == True:
                main_menu()


# main_menu()  # Called from main.py launcher
