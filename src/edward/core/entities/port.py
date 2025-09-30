
### IMPORTS###
import pygame
import local_data
import mytext
import subroutines

def ports(window,canvas):
### 2 PYGAME INIT###
    pygame.init()
### 3 COLOR DEFINITIONS ###
    color_text = ('black')
    color_border = ('blue')
### 4. FONT DEFINITIONS ###
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    font20g = pygame.font.SysFont("Georgia", 20, bold=False)  ## clear, perhaps a little formal - the font selected
### 5 TEXT AND IMAGE POSITIONS ###

    rightpaneltext_x = 500
    rightpaneltext_y = 500
    rightpaneltext_w = 400
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

### 7 VARIABLE INITIATION ###
    menubutton_clicked = False
    running = True


### 8 IMAGE LOADING ###
    img2 = pygame.image.load('natlantictrimmedre.png')
    img2r = pygame.transform.scale(img2, (mapwidth, mapheight))  # map of north atlantic larger scale

###9 CREATION OF LISTS ###
    ship_list_selected = []
    ship_list_me = []
    ship_list_me = range(0, len(local_data.ship_data))
    port_list=[]
    destination_list=[]
    
   ### 11 RECTS ###
    port_text_rect = pygame.Rect(port_list_margin, port_list_start, port_list_width, port_list_height)
    menubuttontext_rect = pygame.Rect(port_list_margin, 800, port_list_width, port_list_height)

### 12 LOAD IMAGES ###


    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 1)
    canvas.blit(menubuttontext, menubuttontext_rect)
    
    canvas.blit(img2r, (0,0))  # blit map first
    ##################instantiate ships###########################
    for i in range(len(ship_list_me)):
        ship_list_selected.append(subroutines.Ship(ship_list_me[i]))  # instantiates ship
        port = ship_list_selected[i].port  # finds port
        port_list.append(ship_list_selected[i].port) # creates list of ports
        destination_list.append(ship_list_selected[i].destination)
   
    ports_unique_list = []
    [ports_unique_list.append(item) for item in port_list if item not in ports_unique_list]
    #print(ports_unique_list)
    destination_unique_list = []
    [destination_unique_list.append(item) for item in destination_list if item not in destination_unique_list]
    #print(destination_unique_list)
    for i in range(len(ports_unique_list)):
        port=( ports_unique_list[i] )
        for j in range(0, len(local_data.ports_waypoints_coord)):

            if local_data.ports_waypoints_coord[j][0] == port:
                port1got = True
                
                port_x = (local_data.ports_waypoints_coord[j][1])
                port_y = (local_data.ports_waypoints_coord[j][2])
                #print("got port 1", port,port_x,port_y)
                pygame.draw.circle(canvas, 'red',(port_x,port_y), 10)
    
    for i in range(len(destination_unique_list)):
        destination = (destination_unique_list[i])
        #print("destination from unique list", destination)
        for j in range(0, len(local_data.ports_waypoints_coord)):
            if local_data.ports_waypoints_coord[j][0] == destination:
                destinationgot = True
                port_x = (local_data.ports_waypoints_coord[j][1])
                port_y = (local_data.ports_waypoints_coord[j][2])
                pygame.draw.circle(canvas, 'blue', (port_x, port_y), 10)
   
    port_text = font20.render(" Ports: ", True, color_border)
    port_text_rect = pygame.Rect(port_list_margin, port_list_start, port_list_width, port_list_height)
    pygame.draw.rect(canvas, 'white', port_text_rect)
    pygame.draw.rect(canvas, "red", port_text_rect, 2)
    canvas.blit(port_text, port_text_rect)
    
    for i in range(0, len(ports_unique_list)):
       
        port_text = font20.render((ports_unique_list[i]), True, color_border)
        port_text_rect = pygame.Rect(port_list_margin, port_list_start+(i+1)*port_list_height, port_list_width, port_list_height)
        pygame.draw.rect(canvas, 'white', port_text_rect)
        pygame.draw.rect(canvas, "red", port_text_rect, 2)
        canvas.blit(port_text, port_text_rect)
    lenport = len(ports_unique_list)
    port_text = font20.render(" Destinations: " , True, color_border)
    port_text_rect = pygame.Rect(port_list_margin, port_list_start +(lenport+1)*port_list_height, port_list_width,
                                 port_list_height)
    
    pygame.draw.rect(canvas, 'white', port_text_rect)
    pygame.draw.rect(canvas, color_border, port_text_rect, 2)
    canvas.blit(port_text, port_text_rect)
    for i in range(0,len(destination_unique_list)):
        
        port_text = font20.render(destination_unique_list[i], True, color_border)
        port_text_rect = pygame.Rect(port_list_margin, port_list_start + (lenport + 2+i) * port_list_height,
                                     port_list_width,
                                     port_list_height)
       
        pygame.draw.rect(canvas, 'white', port_text_rect)
        pygame.draw.rect(canvas, color_border, port_text_rect, 2)
        canvas.blit(port_text, port_text_rect)

   
    textsurf = pygame.Rect(rightpaneltext_x, rightpaneltext_y, rightpaneltext_w, rightpaneltext_h)
    pygame.draw.rect(canvas, 'white', textsurf)  # blank bacground
    subroutines.blit_text_rect_tjh(canvas, mytext.mytext2, 'black', textsurf, font20g)

    pygame.draw.rect(canvas, "white", menubuttontext_rect)
    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 2)
    canvas.blit(menubuttontext, menubuttontext_rect)

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
       
            


