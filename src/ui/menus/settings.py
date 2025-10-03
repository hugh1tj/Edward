import pygame
from ...models import subroutines
from ...data import local_data

def settings_sub(window,canvas):
    pygame.init()
    button_height = 50
    button_width = 300
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 20, bold=False)
    panelimg_x = 20
    panelimg_y = 400
    panelimg_w = 500
    panelimg_h = 400
    panelimgr_x = 600
    panelimgr_y = 400
    panelimgr_w = 500
    panelimgr_h = 400
    paneltext_x = 20
    paneltext_y = 50
    paneltext_w = 700
    paneltext_h = 500
    buttonstart_x = 50
    buttonstart_y = 50
    list_margin_x = 20
    color_bg = ('black')
    color_text = ('white')
    color_border = ('black')
    color_clickedbcg = ('grey')
    color_button = ('blue')
    color_wash = "white"
    weather_button_rect=[]
    weather_events_default_list = []
    for iw in range(len(local_data.weather_events_list)):
        weather_events_default_list.append(subroutines.Weather_event(iw))  # instantiates for all types of weather event


    weather_buttons_list=[]
    weather_buttons_rect=[]
    ROWS=len(local_data.weather_events_list)
    COLS=len(local_data.weather_button_names)
    '''
    for row  in range(0,ROWS): 8 x 6
        for col in range(0,COLS):
            if row==0:
                weather_buttons_list.append(subroutines.Button(buttonstart_x+col*button_width,buttonstart_y+row*button_height,button_width,button_height,local_data.weather_events_list[row][0],color_button,"False"))
            if col==0:
                weather_buttons_list.append(subroutines.Button(buttonstart_x+col*button_width,buttonstart_y+row*button_height,button_width,button_height,local_data.weather_button_names[row],color_button,"False"))
            if row>0 and col>0:
                weather_buttons_list.append("-")


            igrid=subroutines.grid_to_i(row,col,ROWS,COLS)
            #print(weather_buttons_list[igrid])
            weather_buttons_rect.append(subroutines.Button.button_rect_blit(weather_buttons_list[igrid], canvas, color_border, color_text, color_wash))
   '''
    returnbuttontext = font22.render(" Adjustment of Settings will be available in the next Edition- return to Menu", True, color_text)
    returnbuttontext_rect = pygame.Rect(list_margin_x, 400, 3*button_width, button_height)
    canvas.blit(returnbuttontext, returnbuttontext_rect)

    menubuttontext = font20.render(" Go back to Main Menu", True, color_text)
    menubuttontext_rect = pygame.Rect(list_margin_x, 700, button_width, button_height)
    canvas.blit(menubuttontext, menubuttontext_rect)
    window.blit(canvas, (0, 0))
    pygame.display.update()

    running =True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                # sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                menubutton_clicked = True if menubuttontext_rect.collidepoint(event.pos) else False
                if menubutton_clicked == True:
                    from ...core.main import main_menu
                    main_menu()