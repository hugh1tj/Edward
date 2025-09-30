import premiums_alt
import pygame
import local_data
import mytext
import subroutines
import random
import ships_set_sail
import premiums_alt

import underwriter_preferences



def goinside_sub(window, canvas,from_key):
    pygame.init()
    DISPLAY_W, DISPLAY_H = 1500, 1000
    window = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))
    canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))

    # canvas = pygame.display.set_mode((width, height))
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
    basic_font = pygame.font.Font('freesansbold.ttf', 32)
    font20g = pygame.font.SysFont("Georgia", 20, bold=False)  ## clear, perhaps a little formal - the font selected
    ###5  TEXT POSITIONS ###
    width = 1500  # width of main frame
    height = 1000  # height of main frame
    button_height = 50
    button_width = 300
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
    buttonstartx = 800
    buttonstarty = 50
    list_margin_x = 20
    ###   6  INITIAL TEXT ###
    pygame.display.set_caption("Edward LLoyd's Coffeehouse")
    menubuttontext = font22.render(" Go back to Main Menu", True, color_text)
    menubuttontext_rect = pygame.Rect(list_margin_x, 900, button_width, button_height)
    ### 7 VARIABLE INITIATIONS###
    smax = 8  # number of ships for play
    local_data.smax = smax  # set local data mirro

    ### 8 LISTS INITIATIONS and Local Data Mirror Creations ###
    goinside_button = []
    goinside_buttontext_rect = []
    if from_key==0: # coming from main menu
        #if len(local_data.ship_list_me) !=smax:  # local data mirror has not been set
        ship_list_me = []
        #local_data.ship_list_me = []  #
        ship_list_me = (random.sample(range(0, len(local_data.ship_data)),smax))

        ship_list_selected = []
        local_data.ship_list_selected = []  # mirror
        for i in range(len(ship_list_me)):
            ship_list_selected.append(subroutines.Ship(ship_list_me[i]))  # instantiates ship
        local_data.ship_list_selected = ship_list_selected  # mirror
        insurers_list = []
        mmax = 3  # number of insurers
        local_data.mmax = mmax
        if len(local_data.insurers_list) == 0:  # local data mirror has not been set
            insurers_list = []
            local_data.insurers_list = []
        for m in range(0, mmax):
            insurers_list.append(subroutines.Insurer(m))  # instantiates insurer
            local_data.insurers_list.append(insurers_list[m])



    else: # coming from premiums al
         ship_list_me=local_data.ship_list_me
         ship_list_selected = local_data.ship_list_selected
         insurers_list = local_data.insurers_list




    ship_nested_list = []
    #############display buttons########################
    goinside_button_numb = len(local_data.goinside_button_names)
    for i in range(goinside_button_numb):
        goinside_button.append(
            subroutines.Button(buttonstartx, (1 + i) * buttonstarty, button_width, button_height,
                               local_data.goinside_button_names[i][0],
                               local_data.goinside_button_names[i][1], "False"))
    for i in range(goinside_button_numb):
        if goinside_button[i].rect_color == 1:
            goinside_buttontext_rect.append(
                subroutines.Button.button_rect_blit(goinside_button[i], canvas, color_border, color_text, color_wash))
        else:
            goinside_buttontext_rect.append(
                subroutines.Button.button_rect_blit(goinside_button[i], canvas, color_bg, color_text, color_wash))
    ### 9 IMAGE LOADING
    #################display coffee shop picture and caption###############
    img1 = pygame.image.load(r"C:\Users\Welcme\PycharmProjects\Edward Lloyds Coffeehouse Project 1\Two business men.png")
    img1r = pygame.transform.scale(img1, (panelimg_w, panelimg_h))

    canvas.blit(img1r, (panelimg_x, panelimg_y))
    img2 = pygame.image.load(r"C:\Users\Welcme\PycharmProjects\Edward Lloyds Coffeehouse Project 1\Watching Ships Set Sail.png")
    img2r = pygame.transform.scale(img2, (panelimgr_w, panelimgr_h))
    canvas.blit(img2r, (panelimgr_x, panelimgr_y))




    textsurf = pygame.Rect(paneltext_x, paneltext_y, paneltext_w, paneltext_h)
    subroutines.blit_text_rect_tjh(canvas, mytext.mytextgoinside, 'white', textsurf, font22)
    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 1)
    canvas.blit(menubuttontext, menubuttontext_rect)

    textsurf = pygame.Rect(700, 800, paneltext_w, paneltext_h)
    subroutines.blit_text_rect_tjh(canvas, mytext.mytext_setsail, 'white', textsurf, font22)

    ##############################instiate ships######################################

    #ship_list_selected = local_data.ship_list_selected  # retrieves mirror
    for i in range(len(local_data.ship_list_me)):
        ship_nested_list.append(
            [ship_list_selected[i].ship_name, ship_list_selected[i].port, ship_list_selected[i].destination,
             ship_list_selected[i].tons,
             ship_list_selected[i].age, ship_list_selected[i].place_of_build, ship_list_selected[i].hull_condition,
             ship_list_selected[i].rig_condition,
             round(ship_list_selected[i].revenue_out), round(ship_list_selected[i].revenue_in),
             round(ship_list_selected[i].ship_value), round(ship_list_selected[i].ship_repair)])

    title_list1 = ["Ship Name", "Port ", "Destination", "Tons", "Age", "Place ", "Hull", "Rig ", "Revenue ", "Revenue",
                   "Cost of ", "Cost of"]
    title_list2 = ["", "of Origin", "", "", "", "of build", "condition", "condition", " going", "returning", "of build",
                   "of repair/refit"]

    ship_nested_list.insert(0, title_list2)
    ship_nested_list.insert(0, title_list1)

    local_data.premiums_alt_status = False
    local_data.ships_instantiated_status = True

    window.blit(canvas, (0, 0))
    pygame.display.update()
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                #sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(goinside_button_numb):
                    goinside_button[i].clicked = True if goinside_buttontext_rect[i].collidepoint(event.pos) else False
                    if goinside_button[i].clicked == True:
                        pass
                menubutton_clicked = True if menubuttontext_rect.collidepoint(event.pos) else False
                if menubutton_clicked == True:
                    from main import main_menu
                    main_menu()

            if goinside_button[1].clicked:  # shows ships and ports
                canvas.fill('black')
                show_ships(window, canvas, ship_nested_list)

            if goinside_button[2].clicked:  # allows MyAlgo to adjust preferences
                canvas.fill('black')
                underwriter_preferences.under_prefsub(window, canvas, from_index=1)

            if goinside_button[3].clicked:  # negotiate premiums and set sail
                canvas.fill('black')
                premiums_alt.premiums_alt_sub_sub(window, canvas, ship_list_me,ship_list_selected,insurers_list,from_index=1)

            if goinside_button[4].clicked:  # set sial
                canvas.fill('black')
                ships_set_sail.ships_set_sail_sub(window, canvas,ship_list_me,ship_list_selected,insurers_list,from_index=1)


def show_ships(window, canvas, ship_nested_list):
    ### 3 COLOR DEFINITIONS
    color_bg = ('black')
    color_text = ('black')
    color_border = ('blue')
    color_clickedbcg = ('grey')
    color_wash = "black"
    ### 4. FONT DEFINITIONS
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    ### 5 TEXT AND IMAGE POSITIONS
    list_margin_x = 20
    list_width = 200
    list_height = 25
    port_list_start_y = 400
    map_top_left_y = 400
    map_top_left_x = 500
    cell_width = 110
    cell_height = 25
    marginx = 2
    marginy = 5
    table_start_y = 50
    port_list_width = 200
    port_list_height = 25
    ports_title_x = map_top_left_x + 20
    ports_title_y = map_top_left_y + 50

    ### 6. INITIAL TEXT
    title_text = font22.render("Data on Ships", True, color_text)
    menubuttontext = font22.render(" Go back to Coffee Shop Menu", True, color_text)
    ports_title_text = font22.render(" Ports and Destinations", True, color_text)
    ### 7. VARIABLE INITIATION

    ### 8. IMAGE LOADING
    img2 = pygame.image.load('natlantictrimmedre.png')
    contraction_x = 0.5
    contraction_y = contraction_x
    mapwidth = 1500 * contraction_x
    mapheight = mapwidth * 0.75
    img2r = pygame.transform.scale(img2, (mapwidth, mapheight))  # map of north atlantic larger scale
    ### 9 CREATION OF LISTS
    ports_list = []
    destinations_list = []
    # print ("Ship 2",subroutines.Ship(2).port)
    for i in range(len(ship_nested_list)):
        # port = subroutines.Ship(i).port # finds port
        port = ship_nested_list[i][1]  # nested list has two title headers
        # destination = subroutines.Ship(i).destination
        destination = ship_nested_list[i][2]  # nested list has two title headers
        ports_list.append(port)  # creates list of ports
        destinations_list.append(destination)
    ports_unique_list = []
    [ports_unique_list.append(item) for item in ports_list if item not in ports_unique_list]
    print(ports_unique_list)
    destination_unique_list = []
    [destination_unique_list.append(item) for item in destinations_list if item not in destination_unique_list]
    print(destination_unique_list)
    ### RECTS
    title_text_rect = pygame.Rect(list_margin_x, 0, list_width, list_height)
    menubuttontext_rect = pygame.Rect(list_margin_x, 800, list_width * 1.5, list_height)
    port_text_rect = pygame.Rect(list_margin_x, port_list_start_y, port_list_width, port_list_height)
    ports_title_text_rect = pygame.Rect(ports_title_x, ports_title_y, port_list_width, port_list_height)
    ### DEVELOP CANVAS
    canvas.blit(img2r, (map_top_left_x, map_top_left_y))  # blit map first
    pygame.draw.rect(canvas, "white", title_text_rect)
    pygame.draw.rect(canvas, color_border, title_text_rect, 1)
    canvas.blit(title_text, title_text_rect)

    pygame.draw.rect(canvas, "white", ports_title_text_rect)
    pygame.draw.rect(canvas, color_border, ports_title_text_rect, 1)
    canvas.blit(ports_title_text, ports_title_text_rect)

    subroutines.draw_grid(canvas, ship_nested_list, cell_width, cell_height, marginx, marginy, table_start_y)

    pygame.draw.rect(canvas, "white", menubuttontext_rect)
    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 2)
    canvas.blit(menubuttontext, menubuttontext_rect)
    menubutton_clicked = False

    ### DRAW PORTS AND DESTINATIONS

    for i in range(len(ports_unique_list)):
        port = (ports_unique_list[i])
        for j in range(0, len(local_data.ports_waypoints_coord)):

            if local_data.ports_waypoints_coord[j][0] == port:
                port1got = True
                port_x = contraction_x * (local_data.ports_waypoints_coord[j][1]) + map_top_left_x
                port_y = contraction_y * (local_data.ports_waypoints_coord[j][2]) + map_top_left_y

                pygame.draw.circle(canvas, 'red', (port_x, port_y), 10)

    for i in range(len(destination_unique_list)):
        destination = (destination_unique_list[i])
        # print("destination from unique list", destination)
        for j in range(0, len(local_data.ports_waypoints_coord)):
            if local_data.ports_waypoints_coord[j][0] == destination:
                destinationgot = True
                port_x = contraction_x * (local_data.ports_waypoints_coord[j][1]) + map_top_left_x
                port_y = contraction_y * (local_data.ports_waypoints_coord[j][2]) + map_top_left_y
                pygame.draw.circle(canvas, 'blue', (port_x, port_y), 10)

    window.blit(canvas, (0, 0))
    pygame.display.flip()
    running = True
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
                goinside_sub(window, canvas)