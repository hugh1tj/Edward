### IMPORTS ###
import pygame
from ...data import local_data
from ...data import text_content as mytext
from ...models import subroutines
import random
from ...utils import pathfinding as astar
from ...utils.spritesheet import Spritesheet 
from ...utils.tiles import *


def calculate_route(window,canvas,port,destination):
    #print ("port in calculate route", port)
    ### COLOR DEFINITIONS ###
    color_text = ('black')
    color_ports = ('blue')
    color_destinations=('red')
    ### FONT DEFINITIONS ###
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    ### CREATION OF LISTS
    path_go = []
    path_back = []
   
    path = subroutines.find_route(port, destination)
    path_go = path[0]
    path_back = path[1]
   
    for k in range(0, len(path_go)):  # display paths
        point_x = path_go[k][0]
        point_y = path_go[k][1]
        # print('point x', point_x,' point y', point_y)

        pygame.draw.circle(canvas, "dark blue", (point_y * 16, point_x * 16), 4)
    for k in range(0, len(path_back)):  # display paths
        point_x = path_back[k][0]
        point_y = path_back[k][1]

        pygame.draw.circle(canvas, "dark red", (point_y * 16, point_x * 16), 4)
    return(path_go,path_back)
    
    
def routessub(window, canvas):
    
    pygame.init()
### 3 COLOR DEFINITION ###
    color_text = ('black')
    color_border = ('blue')
    color_dest=('red')
    color_wash = "white"
### 4.FONT DEFNITIONS###
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    font20g = pygame.font.SysFont("Georgia", 20, bold=False)

### 5 TEXT AND IMAGE POSITIONS ###

    rightpaneltext_x = 900
    rightpaneltext_y = 500
    rightpaneltext_w = 500
    rightpaneltext_h = 500
    port_list_margin = 5
    port_list_start = 50
    port_list_width = 200
    port_list_height = 25
    width_text = 800  # width of left panel of text
    height_text = 700  # width of right panel of text
    mapwidth = 1500
    mapheight = mapwidth * .765  # empirical

### 6 INITIAL TEXT ###
    menubuttontext = font22.render(" Go back to Main Menu", True, color_text)
    calculate_text=font22.render(" Click on Port and Destination to change route", True, color_text)
    port_title_text = font22.render(" Available Ports: ", True, color_text)
    dest_title_text=font22.render(" Available Destinations: ", True,color_text)
    port_selected_title_text = font22.render(" Showing Port: ", True, color_text)
    destination_selected_title_text = font22.render(" Showing Destination: ", True, color_text)
    port_out_title_text = font22.render(" Nautical Miles Out ", True, color_text)
    port_in_title_text = font22.render(" Nautical Miles In ", True, color_text)
    drift_button_text = font22.render(" Toggle to show ocean drift On/Off", True, color_text)
    
    
### 7 VARIABLE INITIATION ###
    menubutton_clicked = False
    drift_button_clicked = False
    running = True
    drift_show=True
### 8 IMAGE LOADING ###
    

    spritesheet = Spritesheet('src/assets/images/spritesheet.png')
    map_map = TileMap('src/assets/data/newmap6Sep2025.csv', spritesheet)
    #print(' map x ', local_data.mapx)
    img2 = pygame.image.load('src/assets/images/natlantictrimmedre.png')
    img2r = pygame.transform.scale(img2, (mapwidth, mapheight))  # map of north atlantic larger scale
    
### 9 CREATION OF LISTS ###
    ship_list_selected = []
    k=1
    #ship_list_me = (random.sample(range(0, len(local_data.ship_data)), k))
    
    ship_list_me = range(0, len(local_data.ship_data))
    port_list = []
    destination_list = []
    path_go = []
    path_back = []
    port_button = []
    port_button_text_rect = []
    destination_button = []
    destination_button_text_rect = []

### 11 RECTS ###

    port_selected_title_rect = pygame.Rect(rightpaneltext_x, port_list_start, port_list_width, port_list_height)
    destination_selected_title_rect = pygame.Rect(rightpaneltext_x + port_list_width, port_list_start, port_list_width,
                                        port_list_height)
    port_current_rect=pygame.Rect(rightpaneltext_x, port_list_start+port_list_height, port_list_width, port_list_height)
    destination_current_rect=pygame.Rect(rightpaneltext_x+port_list_width, port_list_start+port_list_height, port_list_width, port_list_height)
    
    port_out_title_rect = pygame.Rect(rightpaneltext_x, port_list_start+2*port_list_height, port_list_width,
                                              port_list_height)
    port_in_title_rect = pygame.Rect(rightpaneltext_x+port_list_width, port_list_start + 2*port_list_height, port_list_width,
                                 port_list_height)
    port_out_distance_rect = pygame.Rect(rightpaneltext_x, port_list_start + 3*port_list_height,
                                        port_list_width, port_list_height)
    port_in_distance_rect = pygame.Rect(rightpaneltext_x+port_list_width, port_list_start + 3 * port_list_height,
                                         port_list_width, port_list_height)
    calculate_text_rect=pygame.Rect(rightpaneltext_x, port_list_start + 5 * port_list_height,
                                         2*port_list_width, port_list_height)

    drift_button_text_rect=pygame.Rect(rightpaneltext_x, port_list_start + 7 * port_list_height,
                                         2*port_list_width, port_list_height)
    menubuttontext_rect = pygame.Rect(port_list_margin, 800, port_list_width, port_list_height)

    ### for title of panel of available ports
    port_title_text_rect = pygame.Rect(port_list_margin, port_list_start, port_list_width, port_list_height)

    canvas.blit(img2r, (0, 0))  # blit map first
    port="London" 
    destination="Jamaica" # default ports
    
    port_out_distance_text = font22.render(str(3 * 16 * len(path_go)), True, color_border)
    port_in_distance_text = font22.render(str(3 * 16 * len(path_back)), True, color_border)
    canvas_drift=canvas
    while running:

        
        canvas.blit(img2r, (0, 0))  # blit map first
        ###  INSERT DESCRIPTIVE TEXT
        textsurf = pygame.Rect(rightpaneltext_x, rightpaneltext_y, rightpaneltext_w, rightpaneltext_h)
        pygame.draw.rect(canvas, 'white', textsurf)  # blank bacground
        subroutines.blit_text_rect_tjh(canvas, mytext.mytext5, 'black', textsurf, font22)
        textsurf = pygame.Rect(rightpaneltext_x, rightpaneltext_y, rightpaneltext_w, rightpaneltext_h)
        pygame.draw.rect(canvas_drift, 'white', textsurf)  # blank bacground
        subroutines.blit_text_rect_tjh(canvas_drift, mytext.mytext5, 'black', textsurf, font22)
        #print ("drift show", drift_show)
        grid = local_data.mapx

        if drift_show==True:
            map_map.draw_map(canvas_drift)  # imports and displays sprites (from Tiles)
            
            mx, my = pygame.mouse.get_pos()
            if mx > 1300:
                mxx = 1300
            else:
                mxx = mx
            if my > 950:
                myy = 950
            else:
                myy = my
                
            mx_tile = int(mxx / 16)
            my_tile = int(myy / 16)
            gridtop = int(grid[my_tile][mx_tile])
            #print("gridtop", gridtop)
            gridtop_text_rect = pygame.Rect(mxx + 20, my, port_list_width,
                                                port_list_height)
            if gridtop==-1:
                gridtop_text=""
            else:
                gridtop_text = local_data.list_tile_id[gridtop]
            if gridtop==5:
                if mxx>600:
                    gridtop_text="Canaries Current"
                else:
                    gridtop_text="Labrador Current"
            #print("Gridtop", gridtop, gridtop_text)
            gridtop_text_rend= font20g.render(gridtop_text, True, color_border)
            textsurf = pygame.Rect(rightpaneltext_x, rightpaneltext_y, rightpaneltext_w, rightpaneltext_h)
            pygame.draw.rect(canvas_drift, 'white', textsurf)  # blank bacground
            subroutines.blit_text_rect_tjh(canvas_drift, mytext.mytext5, 'black', textsurf, font20g)
            canvas_drift.blit(gridtop_text_rend, gridtop_text_rect)
            window.blit(canvas_drift, (0, 0))
            #pygame.display.flip()
            
        else:
            window.blit(canvas, (0, 0))

            

        
    ##################instantiate ships in order to extract ports and destinations###########################
        for i in range(len(ship_list_me)):
            ship_list_selected.append(subroutines.Ship(ship_list_me[i]))  # instantiates all ships
            port_temp = ship_list_selected[i].port  # finds port
            port_list.append(ship_list_selected[i].port)  # creates list of ports
            destination_list.append(ship_list_selected[i].destination)

        ports_unique_list = []
        [ports_unique_list.append(item) for item in port_list if item not in ports_unique_list]
    # print(ports_unique_list)
        destination_unique_list = []
        [destination_unique_list.append(item) for item in destination_list if item not in destination_unique_list]
    # print(destination_unique_list)
    # SHOW PORTS as circles ###
        for i in range(len(ports_unique_list)):
            port_temp = (ports_unique_list[i])
            for j in range(0, len(local_data.ports_waypoints_coord)):

                if local_data.ports_waypoints_coord[j][0] == port_temp:
                    port1got = True

                    port_x = (local_data.ports_waypoints_coord[j][1])
                    port_y = (local_data.ports_waypoints_coord[j][2])
                
                    pygame.draw.circle(canvas, 'red', (port_x, port_y), 4)
                    if port==port_temp:
                        pygame.draw.circle(canvas, 'blue', (port_x, port_y), 10)

### SHOW DESTINATIONS as circles ###
        for i in range(len(destination_unique_list)):
            destination_temp = (destination_unique_list[i])
        # print("destination from unique list", destination)
            for j in range(0, len(local_data.ports_waypoints_coord)):
                if local_data.ports_waypoints_coord[j][0] == destination_temp:
                    destinationgot = True
                    port_x = (local_data.ports_waypoints_coord[j][1])
                    port_y = (local_data.ports_waypoints_coord[j][2])
                    pygame.draw.circle(canvas, color_border, (port_x, port_y), 4)

                    if destination == destination_temp:
                        pygame.draw.circle(canvas, 'red', (port_x, port_y), 10)
    ### SETS TITLE FOR PANEL OF PORTS
        pygame.draw.rect(canvas, 'white', port_title_text_rect)
        pygame.draw.rect(canvas, color_border, port_title_text_rect, 2)
        canvas.blit(port_title_text, port_title_text_rect)
        #port_text_rect = pygame.Rect(port_list_margin, port_list_start, port_list_width, port_list_height)
### INSTANTIATE PORT BUTTONS ###
       
        lenport=(len(ports_unique_list))
        for i in range(0, lenport):
       
            port_button.append(subroutines.Button(port_list_margin,  port_list_start + (i + 1) * port_list_height,port_list_width,port_list_height ,ports_unique_list[i],"red", False))
       
        for i in range(0, lenport):
            port_button_text_rect.append(subroutines.Button.button_rect_blit(port_button[i], canvas, color_border,color_text,color_wash))
       
            port_button[i].clicked=False

### INSTANTIATE DESTINATION BUTTONS ###
        lendest=len(destination_unique_list)
        for i in range(0, lendest):
            destination_button.append(
                subroutines.Button(port_list_margin, port_list_start + (lenport + 2+i) * port_list_height, port_list_width,
                               port_list_height, destination_unique_list[i], "red", False))

        for i in range(0, lendest):
            destination_button_text_rect.append(
                subroutines.Button.button_rect_blit(destination_button[i], canvas, color_border, color_text, color_wash))
            destination_button[i].clicked =False
        ### SETS TITLE PANEL OF DESTINATIONS
        dest_title_text_rect = pygame.Rect(port_list_margin, port_list_start + (lenport + 1) * port_list_height, port_list_width,
                                 port_list_height)
### DISLAY TITLE BOXES TO PANEL DESTINATIONS

        pygame.draw.rect(canvas, 'white', dest_title_text_rect)
        pygame.draw.rect(canvas, color_border, dest_title_text_rect, 2)
        canvas.blit(dest_title_text, dest_title_text_rect)

        for i in range(0, len(destination_unique_list)):
            port_text = font22.render(destination_unique_list[i], True, color_text)
            port_text_rect = pygame.Rect(port_list_margin, port_list_start + (lenport + 2 + i) * port_list_height,
                                     port_list_width,
                                     port_list_height)


            pygame.draw.rect(canvas, 'white', port_text_rect)
            pygame.draw.rect(canvas, color_border, port_text_rect, 2)
            canvas.blit(port_text, port_text_rect)
    
    ### INSERT RETURN TO MENU BUTTON AND CALCULATE DESCRITPTIVE TEXT
        pygame.draw.rect(canvas, "white", menubuttontext_rect)
        pygame.draw.rect(canvas, color_border, menubuttontext_rect, 2)
        canvas.blit(menubuttontext, menubuttontext_rect)
        pygame.draw.rect(canvas, "white", calculate_text_rect) #
        pygame.draw.rect(canvas, color_border, calculate_text_rect, 2)
        canvas.blit(calculate_text, calculate_text_rect)
        pygame.draw.rect(canvas, "white", drift_button_text_rect)  #
        pygame.draw.rect(canvas, color_border, drift_button_text_rect, 2)
        canvas.blit(drift_button_text, drift_button_text_rect)
        
        ############  Display of Port and Destination Selected and calculated miles
        
        port_current_text = font22.render(port, True, color_border)
        destination_current_text = font22.render(destination, True, color_border)

       
        port_out_distance_text = font22.render(str(3 * 16 * len(path_go)), True, color_border)
        port_in_distance_text = font22.render(str(3 * 16 * len(path_back)), True, color_border)
        pygame.draw.rect(canvas, 'white', port_selected_title_rect)
        pygame.draw.rect(canvas, color_border, port_selected_title_rect, 2)
        pygame.draw.rect(canvas, 'white', destination_selected_title_rect)
        pygame.draw.rect(canvas, color_border, destination_selected_title_rect, 2)
        pygame.draw.rect(canvas, 'white', port_current_rect)
        pygame.draw.rect(canvas, color_border, port_current_rect, 2)
        pygame.draw.rect(canvas, 'white', destination_current_rect)
        pygame.draw.rect(canvas, color_border, destination_current_rect, 2)

        pygame.draw.rect(canvas, 'white', port_out_title_rect)
        pygame.draw.rect(canvas, color_border, port_out_title_rect, 2)
        pygame.draw.rect(canvas, 'white', port_in_title_rect)
        pygame.draw.rect(canvas, color_border, port_in_title_rect, 2)
        pygame.draw.rect(canvas, 'white', port_out_distance_rect)
        pygame.draw.rect(canvas, color_border, port_out_distance_rect, 2)
        pygame.draw.rect(canvas, 'white', port_in_distance_rect)
        pygame.draw.rect(canvas, color_border, port_in_distance_rect, 2)

        canvas.blit(port_selected_title_text, port_selected_title_rect)
        canvas.blit(destination_selected_title_text, destination_selected_title_rect)

        canvas.blit(port_current_text, port_current_rect)
        canvas.blit(destination_current_text, destination_current_rect)
        canvas.blit(port_out_title_text, port_out_title_rect)
        canvas.blit(port_out_distance_text, port_out_distance_rect)
        canvas.blit(port_in_title_text, port_in_title_rect)
        canvas.blit(port_in_distance_text, port_in_distance_rect)
        path = calculate_route(window, canvas, port, destination)  # this subroutine plots and draws dots for  the path
        path_go = path[0]
        path_back = path[1]
        port_out_distance_text = font22.render(str(3 * 16 * len(path_go)), True, color_border)
        port_in_distance_text = font22.render(str(3 * 16 * len(path_back)), True, color_border)

        canvas.blit(port_out_distance_text, port_out_distance_rect)
        canvas.blit(port_in_distance_text, port_in_distance_rect)

        window.blit(canvas, (0, 0))

        pygame.display.update()
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                
                    for i in range(len(ports_unique_list)):
                        port_button[i].clicked = True if port_button_text_rect[i].collidepoint(event.pos) else False
                        if port_button[i].clicked == True:
                            #print("port button is clicked",ports_unique_list[i])
                            port=ports_unique_list[i]
                            #print ("port from mousedown ",port)
                            path = calculate_route(window, canvas, port, destination)
                            path_go = path[0]
                            path_back = path[1]
                            port_out_distance_text = font22.render(str(3 * 16 * len(path_go)), True, color_border)
                            port_in_distance_text = font22.render(str(3 * 16 * len(path_back)), True, color_border)

                            canvas.blit(port_out_distance_text, port_out_distance_rect)

                            canvas.blit(port_in_distance_text, port_in_distance_rect)

                            window.blit(canvas, (0, 0))
                            pygame.display.flip()
                            
                    for i in range(len(destination_unique_list)):
                        destination_button[i].clicked = True if destination_button_text_rect[i].collidepoint(event.pos) else False
                        if destination_button[i].clicked == True:
                            #print("destination button is clicked",destination_unique_list[i])
                            destination=destination_unique_list[i]
                            #print("destination ", destination)
                            path = calculate_route(window, canvas, port, destination)
                            path_go = path[0]
                            path_back = path[1]
                            port_out_distance_text = font22.render(str(3 * 16 * len(path_go)), True, color_border)
                            port_in_distance_text = font22.render(str(3 * 16 * len(path_back)), True, color_border)

                            canvas.blit(port_out_distance_text, port_out_distance_rect)

                            canvas.blit(port_in_distance_text, port_in_distance_rect)

                            window.blit(canvas, (0, 0))
                            pygame.display.flip()

                    menubutton_clicked = True if menubuttontext_rect.collidepoint(event.pos) else False
               
                    if menubutton_clicked == True:
                        from ...core.main import main_menu
                        main_menu()
                    
                    if drift_button_text_rect.collidepoint(event.pos)==True:
                        #print("drift button clicked")
                        if drift_show == True:
                            
                            drift_show = False
                        else:
                            drift_show = True
                    
                    #drift_button_clicked = True if drift_button_text_rect.collidepoint(event.pos) else False
                    
                        
                       
                    
                    
                    
        
        
       
        
