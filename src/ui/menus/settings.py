import pygame
from ...models import subroutines
from ...data import local_data
from ...data import text_content

def settings_sub(window,canvas):
    pygame.init()
    
    button_height = 30
    button_width = 110
    list_margin_x,list_margin_y=20,40
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    font22g = pygame.font.SysFont("Georgia", 22, bold=False)  ## clear, perhaps a little formal - the font selected
    color_text='black'
    color_border='blue'
    color_header='red'
    color_wash='white'
    

    menubuttontext = font22g.render(" Go back to Main Menu", True, color_text)
    menubuttontext_rect = pygame.Rect(list_margin_x, 700, 3*button_width, button_height)
    pygame.draw.rect(canvas,color_wash,menubuttontext_rect)
    pygame.draw.rect(canvas,color_border,menubuttontext_rect,2)
    canvas.blit(menubuttontext, menubuttontext_rect)

###--------------------------BID DELAY SELECTION ----------------------------------------------------------
    # create a grid of buttons for bid_delay select
    bid_delay_button=[]
    bid_delay_button_rect=[]
    bid_delay_ROWS=5
    bid_delay_COLS=2
    bid_delay_origin_x,bid_delay_origin_y=20,50
    bid_delay_title_y=bid_delay_origin_y-30
    bid_delay_title_text = font22g.render(" Select Delay whilst Bidding", True, color_text)
    bid_delay_title_rect = pygame.Rect(bid_delay_origin_x, bid_delay_title_y, 3* 
                                       button_width, button_height)
    pygame.draw.rect(canvas,color_wash,bid_delay_title_rect)
    pygame.draw.rect(canvas,color_border,bid_delay_title_rect,2)
    canvas.blit(bid_delay_title_text, bid_delay_title_rect)

    rightpaneltext_x=650
    rightpaneltext_y=30 
    rightpaneltext_w=400 
    rightpaneltext_h=100
    textsurf = pygame.Rect(rightpaneltext_x, rightpaneltext_y, rightpaneltext_w, rightpaneltext_h)

    subroutines.blit_text_rect_tjh(canvas, text_content.bidding_settings_text, 'white', textsurf, font20)
    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 1)
    canvas.blit(menubuttontext, menubuttontext_rect)




    #print (local_data.bid_delay_labels[0])
    for row in range(0,bid_delay_ROWS):
        for col in range(0,bid_delay_COLS):
            if col==0:
                text=str(local_data.bid_delay_labels[row])
                rect_color=color_header
            else:
                text=" -"
                rect_color=color_border
            if row==0 and col>0:
                text="Set"
                rect_color=color_header
            rect=subroutines.Button(bid_delay_origin_x+ col*button_width,bid_delay_origin_y+row*button_height,button_width,button_height, text,rect_color,False)
            bid_delay_button.append(rect)
            i=subroutines.grid_to_i(row,col,bid_delay_ROWS,bid_delay_COLS)
            bid_delay_button_rect.append(subroutines.Button.button_rect_blit(bid_delay_button[i],canvas, rect_color,color_text,color_wash))
    pygame.display.update()
    ### retrieve default bid_delay and display
    bid_label=str(local_data.bid_delay_default) # loads default setting
    for row in range(0,bid_delay_ROWS):
        ibid=subroutines.grid_to_i(row,0,bid_delay_ROWS,bid_delay_COLS)
        xbid=subroutines.grid_to_i(row,1,bid_delay_ROWS,bid_delay_COLS)
        #print("54 bid delay button,label",bid_delay_button[ibid].text,bid_label)
        #print("55 len bid delay button,label",len(bid_delay_button[ibid].text),len(bid_label))
        #print("56 type bid delay button,label",type(bid_delay_button[ibid].text),type(bid_label))
        if bid_delay_button[ibid].text==bid_label:
            #print("58 bid identity",bid_delay_button[xbid].text)
            bid_delay_button[xbid].text=" Y"
            #print("60 bid identity",bid_delay_button[xbid].text)
            
        else:
            bid_delay_button[xbid].text==" -"
        bid_delay_button_rect[xbid]=subroutines.Button.button_rect_blit(bid_delay_button[xbid],canvas,rect_color,color_text,color_wash)
        #pygame.draw.rect(canvas,color_text,bid_delay_button_rect[xbid],3)

###----------------------SEASONAL WEATHER SEVERITY--------------------------------------------------
# create a grid of buttons for weather severity selection
    weather_severity_button=[]
    weather_severity_button_rect=[]
    weather_severity_ROWS=len(local_data.weather_severity_labels)
    weather_severity_COLS=len(local_data.weather_severity_headers)
    weather_severity_origin_x,weather_severity_origin_y=20,300
    weather_severity_title_y=weather_severity_origin_y-30
    weather_severity_title_text = font22g.render(" Select Weather Severity", True, color_text)
    weather_severity_title_rect = pygame.Rect(weather_severity_origin_x, weather_severity_title_y, 3* 
                                       button_width, button_height)
    pygame.draw.rect(canvas,color_wash,weather_severity_title_rect)
    pygame.draw.rect(canvas,color_border,weather_severity_title_rect,2)
    canvas.blit(weather_severity_title_text, weather_severity_title_rect)

    rightpaneltext_y=weather_severity_origin_y
    rightpaneltext_w=400 
    rightpaneltext_h=100
    textsurf = pygame.Rect(rightpaneltext_x, rightpaneltext_y, rightpaneltext_w, rightpaneltext_h)

    subroutines.blit_text_rect_tjh(canvas, text_content.weather_severity_text, color_wash, textsurf, font20)
    
   ### ---display weather severity grid----
    for row in range(0,weather_severity_ROWS):
        for col in range(0,weather_severity_COLS):
            if col==0:
                text=str(local_data.weather_severity_labels[row])
                rect_color=color_header
            else:
                text=" -"
                rect_color=color_border
            if row==0 and col>0:
                text=str(local_data.weather_severity_headers[col])
                rect_color=color_header
            rect=subroutines.Button(weather_severity_origin_x+ col*button_width,weather_severity_origin_y+row*button_height,button_width,button_height, text,rect_color,False)
            weather_severity_button.append(rect)
            i=subroutines.grid_to_i(row,col,weather_severity_ROWS,weather_severity_COLS)
            weather_severity_button_rect.append(subroutines.Button.button_rect_blit(weather_severity_button[i],canvas, rect_color,color_text,color_wash))
    pygame.display.update()
    
    weather_severity_status=[]
    weather_severity_status=local_data.weather_severity_default# loads default setting


    ### display weather severity defaults

    for col in range(1,weather_severity_COLS): # first row is headings with each row being different type of weather
        for row in range(1,weather_severity_ROWS):
            sev_label=weather_severity_status[col] # will be low, moderate or high as each row is selected
            isev=subroutines.grid_to_i(row,0,weather_severity_ROWS,weather_severity_COLS)
            #print("140 col,isev,button.text vs sev_label",col,isev,weather_severity_button[isev].text,sev_label)
            if weather_severity_button[isev].text==sev_label:
                xsev=subroutines.grid_to_i(row,col,weather_severity_ROWS,weather_severity_COLS)# col 0 is header
                weather_severity_button[xsev].text=" Y"
                #print("144 col,xsev,button.text vs ev_label",col,xsev,weather_severity_button[isev].text,sev_label)
                weather_severity_button_rect[xsev]=subroutines.Button.button_rect_blit(weather_severity_button[xsev],canvas,rect_color,color_text,color_wash)
                pygame.draw.rect(canvas,color_text,weather_severity_button_rect[xsev],2)
    pygame.display.update()


    window.blit(canvas, (0, 0))
    pygame.display.update()

    running =True

    while running:
        ### create bid_delay for use in premiums_alt
        for row in range (0,bid_delay_ROWS):
            ibid=subroutines.grid_to_i(row,0,bid_delay_ROWS,bid_delay_COLS)
            xbid=subroutines.grid_to_i(row,1,bid_delay_ROWS,bid_delay_COLS)
            if bid_delay_button[xbid].text==" Y":
                bid_name_select=str(local_data.bid_delay_labels[row])
                #print ("bid name select",bid_name_select)
                local_data.bid_delay_select="0"
                local_data.bid_delay_select=bid_name_select
                break
        ### create weather_severities_chosen for use in ships_set_sail
        
        local_data.weather_severities_chosen=[]
        for col in range(1,weather_severity_COLS): #col 0 is header , cols first to get chosen list in order of weather type
            for row in range (1,weather_severity_ROWS):# row 0 is header
           
                #print ("col",col, "weather severity ROWS",weather_severity_ROWS,"weatehr severity COLS",weather_severity_COLS)
                isev=subroutines.grid_to_i(row,col,weather_severity_ROWS,weather_severity_COLS)
                #print ("172 row,col, weather severity button[isev].text,isev",row,col,weather_severity_button[isev].text,isev)
                if weather_severity_button[isev].text==" Y":
                    #print ("174 row,col,weather severity button,isev",row,col,weather_severity_button[isev].text,isev)
                    xsev=subroutines.grid_to_i(row,0,weather_severity_ROWS,weather_severity_COLS)
                    weather_severity_selected=weather_severity_button[xsev].text
                    local_data.weather_severities_chosen.append(weather_severity_selected)
                             
        #print("severities chosen list",local_data.weather_severities_chosen)
        

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

                ### for bid_delay
                for row in range(1,bid_delay_ROWS):
                    ibid=subroutines.grid_to_i(row,1,bid_delay_ROWS,bid_delay_COLS)
                    #print("ibid",ibid)
                    bid_delay_button[ibid].clicked=True if bid_delay_button_rect[ibid].collidepoint(event.pos) else False
                    if bid_delay_button[ibid].clicked:
                        #print("92 clicked", bid_delay_button[ibid].text)
                        if bid_delay_button[ibid].text==" Y":
                            bid_delay_button[ibid].text=" -"
                            #print("95 in clicked", bid_delay_button[ibid].text)
                        else:
                            bid_delay_button[ibid].text=" Y"
                            #print("98 in clicked", bid_delay_button[ibid].text)
                            bid_delay_button_rect[ibid]=subroutines.Button.button_rect_blit(bid_delay_button[ibid],canvas, color_border,color_text,color_wash)
                          
                            
                ### find if any other buttons in bid delay pressed
                        for row in range (1, bid_delay_ROWS):
                            bid_test_pos=subroutines.grid_to_i(row,1,bid_delay_ROWS,bid_delay_COLS)
                            if ibid!= bid_test_pos: # if not the button pressed
                                bid_delay_button[bid_test_pos].text= " -"
                                bid_delay_button_rect[bid_test_pos]=subroutines.Button.button_rect_blit(bid_delay_button[bid_test_pos],canvas, color_border,color_text,color_wash)
                               
###-------------------------------------------------------------------------------------------------
                
                ### for weather severity
                
                for row in range(1,weather_severity_ROWS):
                    for col in range(1,weather_severity_COLS):
                        isev=subroutines.grid_to_i(row,col,weather_severity_ROWS,weather_severity_COLS)
                        #print("224 isev",isev)
                        weather_severity_button[isev].clicked=True if weather_severity_button_rect[isev].collidepoint(event.pos) else False
                        if weather_severity_button[isev].clicked:
                            #print("227 clcked isev",isev)
                       
                            if weather_severity_button[isev].text==" Y":
                                weather_severity_button[isev].text=" -"
                            
                            else:
                                weather_severity_button[isev].text=" Y"  
                            
                            weather_severity_button_rect[isev]=subroutines.Button.button_rect_blit(weather_severity_button[isev],canvas, color_border,color_text,color_wash)
                
                            
                ### find if any other buttons in the column of weather severity pressed

                            for xws in range(1,weather_severity_ROWS):
                                posws= subroutines.grid_to_i(xws,col, weather_severity_ROWS,weather_severity_COLS)#
                                if isev!=posws: #ie not the same key
                                    weather_severity_button[posws].text=" -"
                                    weather_severity_button_rect[posws]=subroutines.Button.button_rect_blit(weather_severity_button[posws],canvas, color_border,color_text,color_wash)

                 ### find if any other buttons in the row of weather severity pressed - not required for this application
                           # for xws in range(1,weather_severity_COLS):
                                #posws= subroutines.grid_to_i(row,xws, weather_severity_ROWS,weather_severity_COLS)#
                                #if isev!=posws: #ie not the same key
                                    #weather_severity_button[posws].text=" -"
                                    #weather_severity_button_rect[posws]=subroutines.Button.button_rect_blit(weather_severity_button[posws],canvas, color_border,color_text,color_wash)


                                
                            
                
            
        window.blit(canvas, (0, 0))
        pygame.display.update()
