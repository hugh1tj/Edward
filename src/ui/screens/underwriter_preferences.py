import pygame
from ...data import local_data
from ...data import text_content as mytext
from ...models import subroutines
from . import ports
import random
from . import goinside
from decimal import Decimal

def i_to_grid(i, ROWS, COLS):  # including titles
    i = i
    row = int(i / COLS)  # firs)t col is zero
    #col = i - row * (ROWS - 1)
    col = i - row * (COLS)
    return row, col


def grid_to_i(row, col, ROWS, COLS):
    i = row*COLS+col

    return i

def under_prefsub(window,canvas,from_index):
    pygame.init()

    ### 3. COLOR DEFINITIONS ###
    color_text = ('black')
    color_border = ('blue')
    color_wash = ('white')
    ### 4. FONT DEFINITIONS ###
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    ### 5 TEXT POSITIONS ###
    paneltext_x = 800
    paneltext_y = 100
    paneltext_w = 700
    paneltext_h = 500
    port_list_margin = 5
    port_list_start = 50
    port_list_width = 200
    port_list_height = 25
    cell_width = 90  # for nested lists
    cell_height = 18
    marginx = 2
    marginy = 5
    gridoriginx,gridoriginy= 20,20
    gridwidth, gridheight = 700, 400
    ins_lists_pos=20,500
### 6 INITIAL TEXT

    pygame.display.set_caption("Underwriter Preferences")
    #title_text = font22.render("Underwriter Risk Preferences", True, color_text)
    menubuttontext = font22.render(" Go back to Main Menu", True, color_text)
    coffee_menu_button_text=font22.render(" Go back to Coffee Shop Menu", True, color_text)
    premiumgotext = font22.render(" Go to Calculate Premiums", True, color_text)
### 7 VARIABLE INITIATIONS
    menubutton_clicked = False
    coffee_menu_button_clicked = False
# Button grid settings
    ROWS, COLS = 8, 6
    button_width = gridwidth // COLS
    button_height = port_list_height


### 11 RECTS
    menubuttontext_rect = pygame.Rect(port_list_margin, 900, port_list_width, port_list_height)
    coffee_menu_button_rect = pygame.Rect(port_list_margin, 900, port_list_width, port_list_height)
    premiumgotext_rect = pygame.Rect(port_list_margin, 850, port_list_width, port_list_height)
    textsurf_rect = pygame.Rect(paneltext_x, paneltext_y, paneltext_w, paneltext_h)

# Create a grid of buttons 8 x 6 for risk premferences
    button = []
    buttontext_rect = []
    pygame.draw.rect(canvas, "white", menubuttontext_rect)
    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 1)
    if from_index==0:
        canvas.blit(menubuttontext, menubuttontext_rect)
    else:
        canvas.blit(coffee_menu_button_text, coffee_menu_button_rect)
    canvas.blit(premiumgotext, premiumgotext_rect)

    subroutines.blit_text_rect_tjh(canvas, mytext.adjust_pref, 'white', textsurf_rect, font22)

    for row in range(0,ROWS):
        for col in range(0,COLS):

            if col == 0:
                text = str(local_data.risk_list_labels[row])
                rect_color = "red"
            else:
                text = " 0"
                rect_color = "blue"
            if row == 0 and col > 0:
                text = str(local_data.risk_pref_title_labels[col])
                rect_color = "red"
            if row == 1 and col > 0:
                text = str(local_data.risk_pref_labels_1[col])
                rect_color = "red"

            rect = subroutines.Button(gridoriginx+col * button_width,gridoriginy+ row * button_height, button_width, button_height, text,rect_color, False)

            button.append(rect)
            i=grid_to_i(row, col, ROWS, COLS)
            #print("i ",i,"row ",row,"col ",col)
            buttontext_rect.append(subroutines. Button.button_rect_blit(button[i], canvas,rect_color, "black", "white"))
    pygame.display.update()
    ###  DISPLAY MY ALGO DEFAULT PREFERENCES On grid###
    m=2 # myalgo
    for c in range(1,len(local_data.insurer_data_labels)):

        clabel=local_data.insurer_data_labels[local_data.insurer_data[m][c]]
        #print("clabel",clabel)

        for row in range(0,ROWS):
            i=grid_to_i(row, 0, ROWS, COLS)
            if button[i].text==clabel:
                x=grid_to_i(row,c,ROWS,COLS)
                button[x].text="  1"
                #print("Rows",ROWS,"Cols",COLS,"x",x)
                buttontext_rect[x] = subroutines.Button.button_rect_blit(button[x], canvas, "grey", "black", "white")
                pygame.draw.rect(canvas, "black", buttontext_rect[x], 3)
    #print ("lenbutton",len(button))
    #inspref_list=[]
            #### DISPLAY PREFERENCES AS ONE LINe FOR ALGO 1###
    m=0
    for row in range(0, 3):
        for col in range(0, len(local_data.insurer_data[m])):
                #print("len insurer data",len(local_data.insurer_data[m]))
        
                if row == 0:
                    text = font22.render(str(local_data.algo1[col]), True, "black")
                    rect_color = "red"
                if row == 1:
                    text = font22.render(str(local_data.risk_pref_labels_1[col]), True, "black")
                    rect_color = "red"
                if row == 2 and col==0:
                    text = font22.render("", True, "black")
                if row == 2 and col>0:
                    key=local_data.insurer_data[m][col]

                    risk=local_data.insurer_data_labels[key]

                    text = font22.render(str(risk), True, "black")
                    rect_color = "red"
                rect = pygame.Rect(gridoriginx + col * button_width, 600 + row * button_height,
                                       button_width, button_height)
                pygame.draw.rect(canvas, "white", rect)
                pygame.draw.rect(canvas, "blue", rect, 2)
                canvas.blit(text, rect)
    #### DISPLAY PREFERENCES AS ONE LINe FOR ALGO 2###
    m = 1
    for row in range(0, 3):
        for col in range(0, len(local_data.insurer_data[m])):
            if row == 0:
                text = font22.render(str(local_data.algo2[col]), True, "black")
                rect_color = "red"
            if row == 1:
                text = font22.render(str(local_data.risk_pref_labels_1[col]), True, "black")
                rect_color = "red"
            if row == 2 and col == 0:
                text = font22.render("", True, "black")
            if row == 2 and col > 0:
                key = local_data.insurer_data[m][col]
                #print("m, key", m,key)
                risk = local_data.insurer_data_labels[key]
                text = font22.render(str(risk), True, "black")
                rect_color = "red"
            rect = pygame.Rect(gridoriginx + col * button_width, 700 + row * button_height,
                               button_width, button_height)
            pygame.draw.rect(canvas, "white", rect)
            pygame.draw.rect(canvas, "blue", rect, 2)
            canvas.blit(text, rect)

            ### draw grid of buttons 2 x 5 for premium percent selection

    # create a 2 col x 8 row grid for premium preference for MyAlgo
    buttonp = []
    buttontextp_rect = []
    ROWSP = 8
    COLSP = 2
    gridoriginpx = 850
    gridoriginpy = 550

    for rowp in range(0, ROWSP):
        for colp in range(0, COLSP):
                if colp == 0:
                        # print ("row p",rowp, ROWSP)
                    text = str(local_data.premium_select_labels[rowp])
                    rect_color = "red"
                else:
                    text = str(0)
                    rect_color = "blue"
                rect = subroutines.Button(gridoriginpx + colp * button_width, gridoriginpy + rowp * button_height,
                                              button_width, button_height, text, rect_color, False)

                buttonp.append(rect)
                ip = grid_to_i(rowp, colp, ROWSP, COLSP)
                    # print("ip ",ip,"rowp ",rowp,"colp ",colp)
                buttontextp_rect.append(
                subroutines.Button.button_rect_blit(buttonp[ip], canvas, rect_color, "black", "white"))

            ### display preference premium
    clabelp = str(10)

    for rowp in range(0, ROWSP):
            ip = grid_to_i(rowp, 0, ROWSP, COLSP)
            xp = grid_to_i(rowp, 1, ROWSP, COLSP)
            #print ("button ip",ip,"button xp",xp,"button ip text",buttonp[ip].text,"button xp text",buttonp[xp].text)
            if buttonp[ip].text == clabelp:

                buttonp[xp].text = str(1)
                #print("within button ip", ip, "button xp", xp, "button ip text", buttonp[ip].text, "button xp text",
                      #buttonp[xp].text)
            else:
                buttonp[xp].text = str(0)
            buttontextp_rect[xp] = subroutines.Button.button_rect_blit(buttonp[xp], canvas, rect_color, "black",
                                                                       "white")
            pygame.draw.rect(canvas, "white", buttontextp_rect[xp], 3)
    pygame.display.update()

    local_data.myalgo_premium = 0
# Main loop
    running = True
    while running:
        #print("in running")
        # screen.fill(WHITE)
        ### MY ALGO PREFERENCE LIST
        local_data .inspref_list=[""]
        for col in range(1, COLS): # COL PRIORITISES RANK
            for row in range(2, ROWS):
        #for row in range(2, ROWS):
            #for col in range(1, COLS):
                i=grid_to_i(row, col, ROWS, COLS)
                if button[i].text=="  1":
                    #print (" i",i,"row",row,"col",col)
                    pref_name=str(local_data.risk_list_labels[row])
                    #print("pref name",pref_name)
                    local_data.inspref_list.append(pref_name)
        #print (local_data.inspref_list)
        if len(local_data.inspref_list)<COLS:
            local_data.inspref_list.append("")
        #### DISPLAY PREFERENCES AS ONE LINe FOR MYALGO###
        for row in range(0, 3):
            for col in range(0, len(local_data.inspref_list)):
                if row == 0 :

                    text = font22.render(str(local_data.myalgo[col]),True,"black")
                    rect_color = "red"
                if row == 1 :
                    text = font22.render(str(local_data.risk_pref_labels_1[col]),True,"black")
                    rect_color = "red"
                if row == 2:
                    text = font22.render(str(local_data.inspref_list[col]),True,"black")
                    rect_color = "red"
                rect = pygame.Rect(gridoriginx + col * button_width, ins_lists_pos[1] + row * button_height, button_width,button_height)
                pygame.draw.rect(canvas, "white", rect)
                pygame.draw.rect(canvas, "blue",rect,2)
                canvas.blit(text,rect)
        ### for premium preference table

        for rowp in range(0, ROWSP):
            #print ("in identifying pref namep")
            ip = grid_to_i(rowp, 0, ROWSP, COLSP)
            xp = grid_to_i(rowp, 1, ROWSP, COLSP)
            #print("button ip", ip, "button xp", xp, "button ip text", buttonp[ip].text, "button xp text",buttonp[xp].text)
            if buttonp[xp].text == str(1):
                pref_namep = str(local_data.premium_select_labels[rowp])
                local_data.myalgo_premium=pref_namep
                #print("rowp, premium preference", pref_namep,local_data.myalgo_premium)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if from_index==0:
                    menubutton_clicked = True if menubuttontext_rect.collidepoint(event.pos) else False
                    if menubutton_clicked == True:
                        from ...core.main import main_menu
                        main_menu()
                else:
                    coffee_menu_button_clicked = True if coffee_menu_button_rect.collidepoint(event.pos) else False
                    if coffee_menu_button_clicked == True:
                        #from ...core.main import main_menu
                        goinside.goinside_sub(window,canvas,from_key=1)
                for row in range(2, ROWS):
                    for col in range(1, COLS):
                        i=grid_to_i(row, col, ROWS, COLS)
                            #print ("i ",i,"row ",row,"col ",col)
                        button[i].clicked = True if buttontext_rect[i].collidepoint(event.pos) else False
                        if button[i].clicked:
                            if button[i].text == "  1":
                                button[i].text = "  0"
                            else:
                                button[i].text = "  1"
                            buttontext_rect[i] = subroutines.Button.button_rect_blit(button[i], canvas, "grey", "black", "white")
                            pygame.draw.rect(canvas, "black", buttontext_rect[i], 3)
                ### FIND COL AND ROW OF GRID BUTTON PRESSED ###
                            pos = i_to_grid(i, ROWS, COLS)
                            row = pos[0]
                            col = pos[1]
                        #print("i", i, "row=", row, "col=", col)
                ### FIND IF ANY OTHER BUTTONS IN THE COLUMN ARE PRESSED ###
                            for x in range(2, ROWS):

                                posc = grid_to_i(x, col, ROWS, COLS)
                                #print("pos col", i,posc)
                                # print (button[pos].text)
                                if i != posc:  # if not the button pressed
                                    #print("pos col", i,posc)
                                    button[posc].text = "  0"
                                    buttontext_rect[posc] = subroutines.Button.button_rect_blit(button[posc], canvas, "grey", "black", "white")
                                    pygame.draw.rect(canvas, "blue", buttontext_rect[posc], 2)
                ### FIND IF ANY OTHER BUTTONS IN THE ROW ARE PRESSED
                            for x in range(1, COLS):
                                posr = grid_to_i(row, x, ROWS, COLS)
                            #print("pos row",i, posr)
                            # print (button[pos].text)
                                if i != posr:  # if not the button pressed
                                    button[posr].text = "  0"
                                    buttontext_rect[posr] = subroutines.Button.button_rect_blit(button[posr], canvas, "grey","black", "white")
                                    pygame.draw.rect(canvas, "blue", buttontext_rect[posr], 2)
            ### for premiums selection
                for rowp in range(1, ROWSP):
                    ip = grid_to_i(rowp, 1, ROWSP, COLSP)

                    buttonp[ip].clicked = True if buttontextp_rect[ip].collidepoint(event.pos) else False
                    if buttonp[ip].clicked:
                        #print("in button has been clicked ", ip, "rowp ", rowp, "colp ", col, "text",buttonp[ip].text)
                        if buttonp[ip].text == str(1):
                            buttonp[ip].text = str(0)
                        else:
                            buttonp[ip].text = str(1)
                            #print ("clicked, ip,text",ip,buttonp[ip].clicked,buttonp[ip].text)
                            buttontextp_rect[ip] = subroutines.Button.button_rect_blit(buttonp[ip], canvas, "grey",
                                                                                             "black", "white")
                            pygame.draw.rect(canvas, "black", buttontextp_rect[ip], 3)
                                    ### FIND COL AND ROW OF GRID BUTTON PRESSED ###
                            poscp = i_to_grid(ip, ROWSP, COLSP)
                            rowp = poscp[0]
                            colp = poscp[1]
                            #print("ip clicked", ip, "rowp=", rowp, "colp=", colp)
                                    ### FIND IF ANY OTHER BUTTONS IN THE COLUMN ARE PRESSED ###
                        for rowp in range(1, ROWS):
                            testp = grid_to_i(rowp, 1, ROWSP, COLSP)
                                        # print("pos col", i,posc)
                                        # print (button[pos].text)
                            if ip != testp:  # if not the button pressed
                                    #print("not xp, testp", xp, testp)
                                    buttonp[testp].text = str(0)
                                    buttontextp_rect[testp] = subroutines.Button.button_rect_blit(buttonp[testp],
                                                                                                        canvas, "grey",
                                                                                                        "black",
                                                                                                        "white")
                                    pygame.draw.rect(canvas, "blue", buttontextp_rect[testp], 2)
                        #else:
                            #button[i].clicked = False
                            #buttontext_rect[i] = subroutines.Button.button_rect_blit(button[i], canvas, "red", "black", "white")
                            #pygame.draw.rect(canvas, "red", buttontext_rect[i], 2)
            #pygame.time.delay(10)

        
        window.blit(canvas, (0, 0))
        pygame.display.flip()
    