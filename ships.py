
### IMPORTS ###
import pygame
import local_data
import mytext
import subroutines
import ports
import random

def ship_constr(window ,canvas):
###2  PYGAME INIT ###
    pygame.init()
### 3. COLOR DEFINITIONS ###
    color_text = ('black')
    color_border = ('blue')
### 4. FONT DEFINITIONS ###
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    font20g = pygame.font.SysFont("Georgia", 20, bold=False)  ## clear, perhaps a little formal - the font selected
### 5 TEXT POSITIONS ###
    rightpaneltext_x = 500
    rightpaneltext_y = 600
    rightpaneltext_w = 700
    rightpaneltext_h = 500
    port_list_margin = 5
    port_list_start = 50
    port_list_width = 200
    port_list_height = 25
    #width_text = 800  # width of left panel of text
    #height_text = 700  # width of right panel of text

### INITIAL TEXT ###
    title_text = font22.render("Data on Ships", True, color_text)
    menubuttontext = font22.render(" Go back to Main Menu", True, color_text)
### 7 VARIABLE INITIATIONS ###
    mapwidth = 1500
    mapheight = mapwidth * .765  # empirical
    k = 15  # number of ships for display in educational part
    menubutton_clicked = False
    running = True
### 8 IMAGE LOADING ###

### 9 lISTS ###
    nested_list = []
    ship_list_selected = []
    ship_list_me = []
    ship_list_me = (random.sample(range(0, len(local_data.ship_data)), k))

### 10 OBJECTS ###
    for i in range(len(ship_list_me)):
        ship_list_selected.append(subroutines.Ship(ship_list_me[i]))  # instantiates ship
    
   ### 11 RECTS
    title_text_rect = pygame.Rect(port_list_margin, 0, port_list_width, port_list_height)
    pygame.draw.rect(canvas, "white", title_text_rect)
    pygame.draw.rect(canvas, color_border, title_text_rect,1)
    canvas.blit(title_text, title_text_rect)
    menubuttontext_rect = pygame.Rect(port_list_margin, 800, port_list_width, port_list_height)
    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 1)
    canvas.blit(menubuttontext, menubuttontext_rect)

    ##################instantiate ships###########################

    for i in range(len(ship_list_me)):
        nested_list.append([ship_list_selected[i].ship_name,ship_list_selected[i].port,ship_list_selected[i].destination, ship_list_selected[i].tons,
                            ship_list_selected[i].age,ship_list_selected[i].place_of_build, ship_list_selected[i].hull_condition, ship_list_selected[i].rig_condition,
                            round(ship_list_selected[i].revenue_out),round(ship_list_selected[i].revenue_in), round(ship_list_selected[i].ship_value), round(ship_list_selected[i].ship_repair) ])
        #nested_list.append(ship_list_selected[i].port)
    
    title_list1=["Ship Name", "Port ", "Destination", "Tons", "Age", "Place ", "Hull", "Rig ", "Revenue ", "Revenue", "Cost of ", "Cost of"]
    title_list2 = ["", "of Origin", "", "", "", "of build", "condition","condition", " going", "returning", "of build","of repair/refit"]

    print ('ship_list_selected',ship_list_selected)
    #nested_list=local_data.ship_data
    #nested_list=ship_list_selected   
    nested_list.insert(0,title_list2)
    nested_list.insert(0, title_list1)
        
   
    cell_width = 110
    cell_height = 25
    marginx = 2
    marginy=5
    table_start_y=50
    subroutines.draw_grid(canvas,nested_list,cell_width,cell_height,marginx,marginy,table_start_y)


    #draw_grid(canvas,nested_list)
    pygame.draw.rect(canvas, "white", menubuttontext_rect)
    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 2)
    canvas.blit(menubuttontext, menubuttontext_rect)

    textsurf = pygame.Rect(rightpaneltext_x, rightpaneltext_y, rightpaneltext_w, rightpaneltext_h)
    subroutines.blit_text_rect_tjh(canvas, mytext.mytext4, 'white',textsurf, font20g)



    window.blit(canvas, (0, 0))
    pygame.display.flip()

    while running:

        window.blit(canvas, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                menubutton_clicked = True if menubuttontext_rect.collidepoint(event.pos) else False
            if menubutton_clicked == True:
                from main import main_menu
                main_menu()

