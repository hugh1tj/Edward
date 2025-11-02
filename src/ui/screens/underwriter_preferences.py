import pygame
from ...data import local_data
from ...data import text_content as mytext
from ...models import subroutines
from . import ports
import random
from . import goinside
from decimal import Decimal


def under_prefsub(window,canvas,from_index):
    pygame.init()

    ### 3. COLOR DEFINITIONS ###
    color_text = 'black'
    color_border = 'blue'
    color_wash = 'white'
    color_header='red'
    ### 4. FONT DEFINITIONS ###
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    ### 5 TEXT POSITIONS ###
    paneltext_x = 800
    paneltext_y = 100
    paneltext_w = 700
    paneltext_h = 500
    list_margin = 5
    list_start = 50
    list_width = 180
    button_height = 25
    cell_width = 90  # for nested lists
    cell_height = 18
    marginx = 2
    marginy = 5
    title1_x=20
    title1_y=70
    title2_x=20
    title2_y=300
    gridoriginx,gridoriginy= 20,100
    gridwidth, gridheight = 700, 400

    ins_lists_pos=20,900
### 6 INITIAL TEXT

    pygame.display.set_caption("Underwriter Preferences")
    #title_text = font22.render(" Underwriter Risk Preferences", True, color_text)
    menubuttontext = font22.render(" Go back to Main Menu", True, color_text)
    coffee_menu_button_text=font22.render(" Go back to Coffee Shop Menu", True, color_text)
    premiumgotext = font22.render(" Go to Calculate Premiums", True, color_text)
    title1_text = font22.render("Set underwriter "+local_data.insurer_names[2]+" risk preferences in the Table Below", True, color_text)
    title2_text = font22.render("Current Risk Preferences of the other Insurers:", True, color_text)
### 7 VARIABLE INITIATIONS
    menubutton_clicked = False
    coffee_menu_button_clicked = False
# Button grid settings
    
    button_width = 120

### 11 RECTS
    menubuttontext_rect = pygame.Rect(list_margin, 900, 2*list_width, button_height)
    coffee_menu_button_rect = pygame.Rect(list_margin, 900, 2*list_width, button_height)
    premiumgotext_rect = pygame.Rect(list_margin, 850, list_width, button_height)
    textsurf_rect = pygame.Rect(paneltext_x, paneltext_y, paneltext_w, paneltext_h)
    title1_text_rect=pygame.Rect(title1_x,title1_y,550, button_height)
    pygame.draw.rect(canvas, color_wash, title1_text_rect)
    pygame.draw.rect(canvas, color_border, title1_text_rect, 1)
    canvas.blit(title1_text,title1_text_rect)
    title2_text_rect=pygame.Rect(title2_x,title2_y,400, button_height)
    pygame.draw.rect(canvas, color_wash, title2_text_rect)
    pygame.draw.rect(canvas, color_border, title2_text_rect, 1)
    canvas.blit(title2_text,title2_text_rect)
    pygame.draw.rect(canvas, color_wash, menubuttontext_rect)
    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 1)
    if from_index==0:
        canvas.blit(menubuttontext, menubuttontext_rect)
    else:
        canvas.blit(coffee_menu_button_text, coffee_menu_button_rect)
    canvas.blit(premiumgotext, premiumgotext_rect)
###-------------------------for risk preferences selection-------------------
# Create a grid of buttons 8 x 6 for risk preferences
    subroutines.blit_text_rect_tjh(canvas, mytext.adjust_pref, color_wash, textsurf_rect, font22)
    risk_select_ROWS,risk_select_COLS = len(local_data.risk_list_labels), len(local_data.risk_pref_labels)
    risk_pref_button = []
    risk_pref_rect = []
    button_width_w=160
    button_width_n=70
    for row in range(0,risk_select_ROWS):
        for col in range(0,risk_select_COLS):
            if col == 0:
                text = str(local_data.risk_list_labels[row])
                rect_color = color_header
                button_width_rp=button_width_w
                gridoriginx_rp=gridoriginx
            elif row==0 and col>0:
                text=str(local_data.risk_pref_labels[col])
                rect_color=color_header
                button_width_rp=button_width_n
                gridoriginx_rp=gridoriginx+button_width_w+(col-1)*button_width_n
            else:
                text = " 0"
                rect_color = color_border
                button_width_rp=button_width_n
                gridoriginx_rp=gridoriginx+button_width_w+(col-1)*button_width_n
          
            
            rect = subroutines.Button(gridoriginx_rp,gridoriginy+ row * button_height, button_width_rp, button_height, text,rect_color, False) # gridorigins adjusted to avoid overwriting
            risk_pref_button.append(rect)
            i=subroutines.grid_to_i(row, col, risk_select_ROWS, risk_select_COLS)
        
            risk_pref_rect.append(subroutines. Button.button_rect_blit(risk_pref_button[i], canvas,rect_color, color_text, color_wash))
   
    
    ###---------------------------------------------------------------------------------------------------------------------
    ###  DISPLAY MY ALGO DEFAULT PREFERENCES ON GRID###
    m=2 # myalgo
    
    for c in range(1,len(local_data.insurer_data_labels)):

        clabel=local_data.insurer_data_labels[local_data.insurer_data[m][c]]
        #print("122 clabel",clabel,"m",m)

        for row in range(0,risk_select_ROWS):
            i=subroutines.grid_to_i(row, 0, risk_select_ROWS, risk_select_COLS) # risk factors are in col 0
            #print ("126 risk pref button",risk_pref_button[i].text)
            if risk_pref_button[i].text==clabel:
                #print("128 found match",risk_pref_button[i].text)
                x=subroutines.grid_to_i(row,c,risk_select_ROWS,risk_select_COLS)
                risk_pref_button[x].text="  1"
               
                risk_pref_rect[x] = subroutines.Button.button_rect_blit(risk_pref_button[x], canvas, "grey", "black", "white")
                pygame.draw.rect(canvas, "black", risk_pref_rect[x], 3)
   
    
    
    ###---------------------------------------------------------------------------------------------------------
            #### DISPLAY PREFERENCES AS ONE LINE FOR ALGO 1 and 2###
    gridoriginy_uprefs=title2_y+ 2*button_height
    for m in range(0,2):
        for row in range(0, 3):
            for col in range(0, len(local_data.insurer_data[m])):
                if row == 0 and col==0:
                    text= font22.render("Underwriter", True, color_text)
                    
                    rect_color = color_header
                elif row==0 and col==1:
                    text = font22.render(local_data.insurer_names[m], True, color_text)
                    rect_color = color_header
                elif row==1 and col==0:
                    text = font22.render("Preferences", True, color_text)
                    rect_color = color_header
                elif row==0 and col>1:
                    text = font22.render(" ", True, color_text)
                    rect_color = color_header
                elif row==2 and col==0:
                    text=font22.render(" ",True,color_text)
                elif row == 1 and col>0:
                    text = font22.render(str(local_data.risk_pref_labels[col]), True, color_text)
                    rect_color = color_header
                else:
                    key=local_data.insurer_data[m][col]
                    risk=local_data.insurer_data_labels[key]

                    text = font22.render(str(risk), True, color_text)
                    rect_color = color_border
            
                rect = pygame.Rect(gridoriginx + col * button_width, gridoriginy_uprefs + row * button_height+m*4*button_height,
                                       button_width, button_height)
                pygame.draw.rect(canvas, color_wash, rect)
                pygame.draw.rect(canvas, color_border, rect, 2)
                canvas.blit(text, rect)
   
    

            ### draw grid of buttons 2 x 5 for premium percent selection
    
    # create a 2 col x 8 row grid for premium preference for MyAlgo
    buttonp = []
    buttontextp_rect = []
    ROWSP = 9
    COLSP = 2
    gridoriginpx = 850
    gridoriginpy = 350

    for rowp in range(0, ROWSP):
        for colp in range(0, COLSP):
                if rowp==0 and colp==0:
                    text = " Underwriter"
                    rect_color = color_header
                elif rowp==0 and colp==1:
                    text=" "+local_data.insurer_names[2]
                elif colp == 0 and rowp>0:
                    text = str(local_data.premium_select_labels[rowp])
                    rect_color = color_header
                elif colp==1 and (rowp==0 or rowp==1):
                    text = " "
                    rect_color = color_header
                else:
                    text = " "+str(0)
                    rect_color = color_border
                rect = subroutines.Button(gridoriginpx + colp * button_width, gridoriginpy + rowp * button_height,
                                              button_width, button_height, text, rect_color, False)

                buttonp.append(rect)
                ip = subroutines.grid_to_i(rowp, colp, ROWSP, COLSP)
                
                buttontextp_rect.append(
                subroutines.Button.button_rect_blit(buttonp[ip], canvas, rect_color, color_text, color_wash))
    
            ### display preference premium
    clabelp = str(10) # default premium

    for rowp in range(2, ROWSP):
            ip = subroutines.grid_to_i(rowp, 0, ROWSP, COLSP)
            xp = subroutines. grid_to_i(rowp, 1, ROWSP, COLSP)
            #print ("button ip",ip,"button xp",xp,"button ip text",buttonp[ip].text,"button xp text",buttonp[xp].text)
            if buttonp[ip].text == clabelp:

                buttonp[xp].text = str(" ")+str(1)
                #print("within button ip", ip, "button xp", xp, "button ip text", buttonp[ip].text, "button xp text",
                      #buttonp[xp].text)
            else:
                buttonp[xp].text = str(" ")+str(0)
            buttontextp_rect[xp] = subroutines.Button.button_rect_blit(buttonp[xp], canvas, rect_color, color_text,
                                                                       color_wash)
            pygame.draw.rect(canvas, color_border, buttontextp_rect[xp], 2)
    pygame.display.update()

    local_data.myalgo_premium = 0

    
    
# Main loop
    running = True
    while running:
        

        ### CREAT MY ALGO PREFERENCE LIST FOR USE IN PREMIUMS_ALT
        local_data .inspref_list=[""]
        for col in range(1, risk_select_COLS): # COL PRIORITISES RANK
            for row in range(1, risk_select_ROWS):
        
                i=subroutines.grid_to_i(row, col, risk_select_ROWS, risk_select_COLS)
                if risk_pref_button[i].text=="  1":
                    #print (" i",i,"row",row,"col",col)
                    pref_name=str(local_data.risk_list_labels[row])
                    #print("pref name",pref_name)
                    local_data.inspref_list.append(pref_name)
        print ("250 inspref list",local_data.inspref_list)
        if len(local_data.inspref_list)<risk_select_COLS:
            local_data.inspref_list.append("")
        
        ###-----------------------------------------------------------------------------
        #### DISPLAY PREFERENCES AS ONE LINE FOR MYALGO###
        m=2
        for row in range(0, 3):
            for col in range(0, len(local_data.inspref_list)):
                if row == 0 and col==0:
                    text= font22.render("Underwriter", True, color_text)
                    rect_color = color_header
                elif row==0 and col==1:
                    text = font22.render(local_data.insurer_names[m], True, color_text)
                    rect_color = color_header
                elif row==1 and col==0:
                    text = font22.render("Preferences", True, color_text)
                    rect_color = color_header
                elif row==0 and col>1:
                    text = font22.render(" ", True, color_text)
                    rect_color = color_header
                elif row==2 and col==0:
                    text=font22.render(" ",True,color_text)
                elif row == 1 and col>0:
                    text = font22.render(str(local_data.risk_pref_labels[col]), True, color_text)
                    rect_color = color_header
                else:
                    key=local_data.inspref_list[col]
                    #risk=local_data.insurer_data_labels[key]
                    #text=font22.render("h",True,color_text)
                    text = font22.render(key, True, color_text)
                    rect_color = color_border
                rect = pygame.Rect(gridoriginx + col * button_width,gridoriginy_uprefs + row * button_height+m*4*button_height , button_width,button_height)
                pygame.draw.rect(canvas, color_wash, rect)
                pygame.draw.rect(canvas, color_border,rect,2)
                canvas.blit(text,rect)
        
        
        ### for premium preference table
        
        for rowp in range(0, ROWSP):
            #print ("in identifying pref namep")
            ip = subroutines.grid_to_i(rowp, 0, ROWSP, COLSP)
            xp = subroutines.grid_to_i(rowp, 1, ROWSP, COLSP)
            #print("button ip", ip, "button xp", xp, "button ip text", buttonp[ip].text, "button xp text",buttonp[xp].text)
            if buttonp[xp].text == str(" ")+str(1):
                pref_namep = str(local_data.premium_select_labels[rowp])
                local_data.myalgo_premium=pref_namep
                #print("rowp, premium preference", pref_namep,local_data.myalgo_premium)

        pygame.display.update()
        window.blit(canvas, (0, 0))
        pygame.display.flip()
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
                ###---------------------------RISK PREFERENCE BUTTONS CLICKED--------------------------------
                
                for row in range(1, risk_select_ROWS):
                    for col in range(1, risk_select_COLS):
                        i=subroutines.grid_to_i(row, col, risk_select_ROWS, risk_select_COLS)
                            #print ("i ",i,"row ",row,"col ",col)
                        risk_pref_button[i].clicked = True if risk_pref_rect[i].collidepoint(event.pos) else False
                        if risk_pref_button[i].clicked:
                            if risk_pref_button[i].text == "  1":
                                risk_pref_button[i].text = "  0"
                            else:
                                risk_pref_button[i].text = "  1"
                            risk_pref_rect[i] = subroutines.Button.button_rect_blit(risk_pref_button[i], canvas, color_border, color_text, color_wash)
                            pygame.draw.rect(canvas, color_text, risk_pref_rect[i], 2)

                           
                ### FIND COL AND ROW OF GRID BUTTON PRESSED ###
                            pos = subroutines.i_to_grid(i, risk_select_ROWS, risk_select_COLS)
                            row = pos[0]
                            col = pos[1]
                        #print("i", i, "row=", row, "col=", col)
                ### FIND IF ANY OTHER BUTTONS IN THE COLUMN ARE PRESSED ###
                            for x in range(2, risk_select_ROWS):

                                posc = subroutines. grid_to_i(x, col, risk_select_ROWS, risk_select_COLS)
                                #print("pos col", i,posc)
                                # print (button[pos].text)
                                if i != posc:  # if not the button pressed
                                    #print("pos col", i,posc)
                                    risk_pref_button[posc].text = "  0"
                                    risk_pref_rect[posc] = subroutines.Button.button_rect_blit(risk_pref_button[posc], canvas, color_border, "black", "white")
                                    pygame.draw.rect(canvas, "blue", risk_pref_rect[posc], 2)
                ### FIND IF ANY OTHER BUTTONS IN THE ROW ARE PRESSED
                            for x in range(1, risk_select_COLS):
                                posr = subroutines.grid_to_i(row, x, risk_select_ROWS, risk_select_COLS)
                            
                                if i != posr:  # if not the button pressed
                                    risk_pref_button[posr].text = "  0"
                                    risk_pref_rect[posr] = subroutines.Button.button_rect_blit(risk_pref_button[posr], canvas, "grey","black", "white")
                                    pygame.draw.rect(canvas, "blue", risk_pref_rect[posr], 2)
            
            ###------------------------------------------------------------------------------------------------------------------
            ### for premiums selection
                for rowp in range(1, ROWSP):
                    ip = subroutines.grid_to_i(rowp, 1, ROWSP, COLSP)

                    buttonp[ip].clicked = True if buttontextp_rect[ip].collidepoint(event.pos) else False
                    if buttonp[ip].clicked:
                        #print("in button has been clicked ", ip, "rowp ", rowp, "colp ", col, "text",buttonp[ip].text)
                        if buttonp[ip].text == " 1":
                            buttonp[ip].text = str(" ")+str(0)
                        else:
                            buttonp[ip].text = str(" ")+str(1)
                            #print ("clicked, ip,text",ip,buttonp[ip].clicked,buttonp[ip].text)
                            buttontextp_rect[ip] = subroutines.Button.button_rect_blit(buttonp[ip], canvas, "grey",
                                                                                             "black", "white")
                            pygame.draw.rect(canvas, "black", buttontextp_rect[ip], 3)
                                    ### FIND COL AND ROW OF GRID BUTTON PRESSED ###
                            poscp = subroutines.i_to_grid(ip, ROWSP, COLSP)
                            rowp = poscp[0]
                            colp = poscp[1]
                            #print("ip clicked", ip, "rowp=", rowp, "colp=", colp)
                                    ### FIND IF ANY OTHER BUTTONS IN THE COLUMN ARE PRESSED ###
                        for rowp in range(1, ROWSP):
                            testp = subroutines.grid_to_i(rowp, 1, ROWSP, COLSP)
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
    