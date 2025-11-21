import pygame
from ...data import local_data
from ...data import text_content as mytext
from ...models import subroutines
from . import weather_hazards
from ...models.subroutines import Insurer

from . import ports
import random
from ...utils import pathfinding as astar
from ...utils.spritesheet import Spritesheet
from ...utils.tiles import *
from . import goinside
import math




class Shiplog_Button(object):
    def __init__(self, x, y, w, h, text, rect_color, alt, clicked):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.rect_color = rect_color
        self.alt = alt  # alt is to distinguish between the two lines
        self.clicked = clicked
        # print ('in Ship_log_Button', text)

def ship_detail(window,canvas,selected_ship_number): ### for part 1 before ship sails. Player clicks to display ship detail
    ship_list_selected = local_data.ship_list_selected  # retrieve mirror
    color_border = 'blue'
    color_wash='white'
    font20g = pygame.font.SysFont("Georgia", 20, bold=False)
    ship_detail_x=900
    ship_detail_y=700
    ship_detail_w=600
    ship_detail_h=300
    ship_detail_list=[]
    ship_detail_rect=pygame.Rect(ship_detail_x,ship_detail_y,ship_detail_w,ship_detail_h)
    ship_detail_list.append(" Ship Details - for other ships click on ship name on top right")
    ship_detail_list.append("")
    if ship_list_selected[selected_ship_number].ship_premium==0:
         ship_detail_list.append("The ship '" + str(ship_list_selected[selected_ship_number].ship_name) + "' is sailing uninsured.")
    else:
         ship_detail_list.append(" The ship '" + str(ship_list_selected[selected_ship_number].ship_name) + "' is insured by " + str(ship_list_selected[selected_ship_number].ship_insurer)+ " at a premium of £"+str(ship_list_selected[selected_ship_number].ship_premium ))
    ship_detail_list.append(" The total replacement value of this ship is estimated as £"+str(round(ship_list_selected[selected_ship_number].ship_value)))
    ship_detail_list.append("  and the cost of a significant repair as £"+str(round(ship_list_selected[selected_ship_number].ship_repair)))
    ship_detail_list.append(" The ship plies between "+str(ship_list_selected[selected_ship_number].port)+ " and "+str(ship_list_selected[selected_ship_number].destination))
    go_miles=16*4* len(ship_list_selected[selected_ship_number].path_go) ### check the science
    ship_detail_list.append(" Journey length is approximately "+str(go_miles) + " nautical miles.")
    ship_detail_list.append(" The total tonnage is "+str(ship_list_selected[selected_ship_number].tons) )
    ship_detail_list.append(" The age of the ship is " + str(ship_list_selected[selected_ship_number].age)+" years, and she was made in "+ str(ship_list_selected[selected_ship_number].place_of_build))
    ship_detail_list.append(" Current rig condition is rated as  " + str(ship_list_selected[selected_ship_number].rig_condition))
    ship_detail_list.append(" and the hull condition rated as "+str(ship_list_selected[selected_ship_number].hull_condition))
    
    ship_detail_list.append("")
    ship_detail_list.append("BON VOYAGE !!!")
    #print("60 in ship detail",ship_list_selected[selected_ship_number].ship_name)
    
    #ship_detail_font=font20.render( ship_detail_text,True,'black')
    pygame.draw.rect(canvas, color_wash, ship_detail_rect)
    pygame.draw.rect(canvas, color_border, ship_detail_rect,2)
    subroutines.blit_text(canvas,ship_detail_list,ship_detail_rect,color_border)  ### note blit_text uses a list





def append_if(j, append_text,mytotal_time_months,mytotal_time_days_res,time_stamp):  # this subroutine only appends text if it is different from previous line/lines
        ship_list_selected = local_data.ship_list_selected  # retrieve mirror
        ship_log_len=len(ship_list_selected[j].ship_log)
        append=True
        numb_test=5 # number of log entries to be tested to see if appending would create a duplicate
        #while xnum<ship_log_len:
        for xnum in range(ship_log_len-1,ship_log_len-numb_test,-1):
            #print(xnum,ship_log_len)
            part_list=ship_list_selected[j].ship_log[xnum].split(',')
            part_list_len=len(part_list)
            if part_list_len>1:
                append_text_test=part_list[1]
            else:
                append_text_test=part_list[0]

            if (append_text ==append_text_test ) :
                append=False
        if append==True and time_stamp==True:
                ship_list_selected[j].ship_log.append(str(mytotal_time_months) + " months " + str(round(mytotal_time_days_res)) + " days ,"+append_text)
                local_data.master_log.append(str(mytotal_time_months) + " months " + str(round(mytotal_time_days_res)) + " days "+ ship_list_selected[j].ship_name+" "+append_text)
        elif append==True and time_stamp==False:
                ship_list_selected[j].ship_log.append(append_text)
                local_data.master_log.append(ship_list_selected[j].ship_name+ " "+append_text)
        else:
            pass

        log_max_len=20
        if (len(ship_list_selected[j].ship_log) > log_max_len):
            ship_list_selected[j].ship_log.pop(3) # 3 fixed lines to start log
        #print ("100 append text",ship_list_selected[j].ship_name, append_text)
        master_log_max_len=38
        if (len(local_data.master_log) > master_log_max_len):
            local_data.master_log.pop(1) # 1 fixed lines to start log



        return append
        

def damage_random_sub(i,iw,damage_text,mytotal_time_months, mytotal_time_days_res,weather_events_list,ship_list_selected,mmax,insurers_list): # ship i, weather event iw
    damage_random=10 # any integer
    #damage_increment=100 # may vary according to event
    damage_increment=local_data.damage_increment
    if damage_random == (random.randrange(0, weather_events_list[iw].rig_damage_risk))and ship_list_selected[i].ship_shipwreck==False:
        append_text1 = "rigging damaged in/by "+damage_text
        appendx=append_if(i, append_text1, mytotal_time_months, mytotal_time_days_res, time_stamp=True)

        ship_condition="Rigging"
        prior_condition=ship_list_selected[i].rig_condition
        degrade_condition(i,ship_list_selected, ship_condition)
        append_text = "prior rig condition: "+ prior_condition+" degraded rig condition " + ship_list_selected[i].rig_condition + " "+ str(round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
        appendy=append_if(i, append_text, mytotal_time_months, mytotal_time_days_res, time_stamp=True)
        if appendx == True and appendy==True:
            ship_list_selected[i].ship_damage_accum = ship_list_selected[
                                                      i].ship_damage_accum + damage_increment
            if ship_list_selected[i].ship_damage_accum >= ship_list_selected[
                                                      i].ship_value:
                ship_list_selected[i].ship_damage_accum >= ship_list_selected[
                    i].ship_value # cap ship damage at total value of ship
        #print("rigging random damage",ship_list_selected[i].ship_name,ship_list_selected[i].ship_damage_accum)
            append_text2="rigging damage"
            ship_list_selected[i].damage_event_list.append([ship_list_selected[i].ship_x, ship_list_selected[i].ship_y,append_text2])
            for m in range(0, mmax):
                insurer_name = insurers_list[m].insurer_name
                if insurer_name == ship_list_selected[i].ship_insurer:
                    insurers_list[m].claims = insurers_list[m].claims + damage_increment
    if damage_random == (random.randrange(0, weather_events_list[iw].hull_damage_risk))and ship_list_selected[i].ship_shipwreck==False:
        append_text1 = "hull damaged from collision due to " + damage_text
        appendx=append_if(i, append_text1, mytotal_time_months, mytotal_time_days_res, time_stamp=True)
        ship_condition="Hull"
        prior_condition=ship_list_selected[i].hull_condition
        degrade_condition(i, ship_list_selected, ship_condition)
        append_text ="prior hull condition: "+prior_condition+  " degraded hull condition " + ship_list_selected[i].hull_condition + " "+ str(round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
        appendy=append_if(i, append_text, mytotal_time_months, mytotal_time_days_res, time_stamp=True)
        if appendx==True and appendy==True:
            if ship_list_selected[i].ship_damage_accum >= ship_list_selected[
                                                      i].ship_damage_accum + damage_increment:
                ship_list_selected[i].ship_damage_accum >= ship_list_selected[
                    i].ship_value  # cap ship damage at total value of ship
        #print("hull random damage", ship_list_selected[i].ship_name, ship_list_selected[i].ship_damage_accum)
            append_text2="hull damage_"
            ship_list_selected[i].damage_event_list.append([ship_list_selected[i].ship_x, ship_list_selected[i].ship_y,append_text2])
            for m in range(0, mmax):
                insurer_name = insurers_list[m].insurer_name
                if insurer_name == ship_list_selected[i].ship_insurer:
                    insurers_list[m].claims = insurers_list[m].claims + damage_increment
    if damage_random == (random.randrange(0, weather_events_list[iw].shipwreck_damage_risk))and ship_list_selected[i].ship_shipwreck==False:
        append_text = "SHIPWRECK due to "+damage_text
        append_if(i, append_text, mytotal_time_months, mytotal_time_days_res, time_stamp=True)
        ship_list_selected[i].ship_damage_accum = ship_list_selected[
                                                      i].ship_value  ### total loss of ship
        print (ship_list_selected[i].ship_name, append_text)
        #print("shipwreck random damage", ship_list_selected[i].ship_name, ship_list_selected[i].ship_damage_accum)
        ship_list_selected[i].ship_shipwreck=True
        for m in range(0, mmax):
            insurer_name = insurers_list[m].insurer_name
            if insurer_name == ship_list_selected[i].ship_insurer:
                insurers_list[m].claims = insurers_list[m].claims + ship_list_selected[
                                                      i].ship_value

def degrade_condition(i,ship_list_selected,ship_condition):  # reduces hull or rig conditions by one grade , unless it is the lowest grade
    if ship_condition=="Hull":
        hull_conditions_list=['A','E','I','O','U']
        prior_condition=ship_list_selected[i].hull_condition
        #print(" 175  prior hull condition",prior_condition)
        index=hull_conditions_list.index(prior_condition)
        if index<len(hull_conditions_list)-1:
            index+=+1
        ship_list_selected[i].hull_condition=(hull_conditions_list[index] )
        #print(" 180 degraded hull  condition",ship_list_selected[i].hull_condition)
    if ship_condition == "Rigging":
        rig_conditions_list = ['G','M','B']
        prior_condition = ship_list_selected[i].rig_condition
        #print(" 184  prior rig condition",prior_condition)
        index = rig_conditions_list.index(prior_condition)
        if index < len(rig_conditions_list)-1:
            index += 1
        ship_list_selected[i].rig_condition = (rig_conditions_list[index])
        #print(" 189 degraded rig  condition",ship_list_selected[i].rig_condition)

def ships_set_sail_sub(window, canvas, ship_list_selected, insurers_list):
    #print("198 start ship sets sail", local_data.ship_list_selected[0].ship_name, ship_list_selected[0].ship_name,ship_list_selected[0].ship_insurer,local_data.ship_list_selected[0].ship_insurer)
    premiums_set=local_data.premiums_set
     
    smax=local_data.smax
    ship_list_selected = local_data.ship_list_selected # retrieve mirror
    insurers_list = local_data.insurers_list # retrieve mirror
    mmax = local_data.mmax
    for m in range (0,mmax):
        insurers_list[m].insurer_update(m)
    mapwidth=1500
    mapheight=mapwidth*.75
    margin_x=0;margin_y=0
   
    cell_width=100;cell_height=25
    menu_margin = 5
    menu_width = 200
    menu_height = 25
    color_wash = 'white'
    color_text = 'black'
    color_border = 'blue'
    color_bg='white'
    color_button='blue'
    color_header='red'
    
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    font20g = pygame.font.SysFont("Georgia", 20, bold=False) 
    
    spritesheet = Spritesheet('src/assets/images/spritesheet.png')
    wc,hc=canvas.get_size()
    drift_drift = pygame.Surface((wc, hc))# for debugging
    drift_drift.fill('white')

    map_map = TileMap('src/assets/data/newmap6Sep2025.csv', spritesheet)
    grid = local_data.mapx
    # print(' map x ', local_data.mapx)
    img2 = pygame.image.load('src/assets/images/natlantictrimmedre.png')
    img2r = pygame.transform.scale(img2, (mapwidth, mapheight))  # map of north atlantic larger scale
    canvas.blit(img2r, (margin_x, margin_y))
    map_map.draw_map(drift_drift)  # imports and displays sprites (from Tiles)
    
    premiums_to_be_set_text=font22.render("  You need to negotiate premiums first !!!", True, color_text)
    set_sail_button_text = font22.render(" Click to prepare routes -", True,color_text)
    set_sail_button_text_rect = pygame.Rect(600, 400, 2.5 * menu_width, menu_height)
    set_sail_button_drift_text_rect=pygame.Rect(600, 400, 2.5 * menu_width, menu_height)
    pygame.draw.rect(canvas, color_wash, set_sail_button_text_rect)
    pygame.draw.rect(canvas, color_border, set_sail_button_text_rect, 2)
    pygame.draw.rect(drift_drift, color_wash, set_sail_button_text_rect)
    pygame.draw.rect(drift_drift, color_border, set_sail_button_text_rect, 2)
    if premiums_set==True:
        canvas.blit(set_sail_button_text, set_sail_button_text_rect)
        drift_drift.blit(set_sail_button_text, set_sail_button_text_rect)
    else:
        premiums_set=False
        canvas.blit(premiums_to_be_set_text, set_sail_button_text_rect)
        drift_drift.blit(premiums_to_be_set_text, set_sail_button_text_rect)
  
 
    ### Create ship detail show buttons
    
    buttonstart_x = 1250
    buttonstart_y = 20
    buttonheight = cell_height
    buttonwidth = 250
    buttonheight = 22
    button_names=[]
    button_names.append(["     Ships Listed by Insurer",1],)
    button_names.append(["     Click on Ship for Ship Data",1],)
   
    for m in range (0,mmax):
        insurer_name=insurers_list[m].insurer_name
        insurer_text_raw=" by Insurer "+ insurer_name+":"
        button_names.append([insurer_text_raw,1],)
        for sj in range(0,smax):
            #print("ship list selected ship insurer",ship_list_selected[sj].ship_insurer)
            if insurer_name==ship_list_selected[sj].ship_insurer:
                button_text_1_raw = "     Ship Name:  " + ship_list_selected[sj].ship_name
                button_names.append([button_text_1_raw,0])
                button_text_2_raw = "     " + ship_list_selected[sj].port+ " to "+ship_list_selected[sj].destination
                button_names.append([button_text_2_raw, 2])
    button_names.append([" Uninsured:",1],)
    for sj in range(0,smax):
            if ship_list_selected[sj].ship_insurer=="Uninsured":
                button_text_1_raw = "     Ship Name:  " + ship_list_selected[sj].ship_name
                button_names.append([button_text_1_raw,0])
                button_text_2_raw = "     " + ship_list_selected[sj].port+ " to "+ship_list_selected[sj].destination
                button_names.append([button_text_2_raw, 2])
    button = []
    buttontext_rect = []
    button_drift_text_rect=[]
    #############display buttons########################
    selected_ship_number=1 # default selected ship number
    set_sail_waiting=True
    #print ("283 button names",button_names)
    while set_sail_waiting:
        button_numb = len(button_names)
        for i in range(button_numb):
            button.append(
                subroutines.Button(buttonstart_x, buttonstart_y+i * buttonheight, buttonwidth, buttonheight,
                               button_names[i][0],
                               button_names[i][1], "False"))
        
        for i in range(button_numb):
            if button[i].rect_color == 1: # headers
                buttontext_rect.append(subroutines.Button.button_rect_blit(button[i], canvas, color_border, color_text, color_wash))
                button_drift_text_rect.append(subroutines.Button.button_rect_blit(button[i], drift_drift, color_border, color_text, color_wash))
            elif button[i].rect_color == 0:
                buttontext_rect.append(
                    subroutines.Button.button_rect_blit(button[i], canvas, color_button, color_text, color_wash))
                button_drift_text_rect.append(subroutines.Button.button_rect_blit(button[i], drift_drift, color_button, color_text, color_wash))
            else: # 2
                buttontext_rect.append(
                    subroutines.Button.button_rect_blit(button[i], canvas, color_bg, color_text, color_wash))
                button_drift_text_rect.append(subroutines.Button.button_rect_blit(button[i], drift_drift, color_bg, color_text, color_wash))
        for i in range(button_numb):  # draw coloured circles
            for sj in range(0, smax):
                if ship_list_selected[sj].ship_name in button_names[i][0]:
                # print("found",ship_list_selected[sj].ship_name, button_names[i][0])
                    ship_color = local_data.list_colors[sj]
                    pygame.draw.circle(canvas, ship_color, (buttonstart_x+8, buttonstart_y + i * buttonheight + 10), 8)
                    pygame.draw.circle(drift_drift, ship_color, (buttonstart_x+8, buttonstart_y + i * buttonheight + 10), 8)
          
        
        ### display menu buttons ################################
        ### return to coffee ship menu
        coffee_menu_button_text = font22.render("Coffee Shop Menu", True, color_border)
        coffee_menu_button_clicked = False
        coffee_menu_button_text_rect = pygame.Rect(menu_margin, 930, 3 * cell_width, cell_height)
        pygame.draw.rect(canvas, color_wash, coffee_menu_button_text_rect)
        pygame.draw.rect(canvas, color_border, coffee_menu_button_text_rect, 2)
        canvas.blit(coffee_menu_button_text, coffee_menu_button_text_rect)
        pygame.draw.rect(drift_drift, color_wash, coffee_menu_button_text_rect)
        pygame.draw.rect(drift_drift, color_border, coffee_menu_button_text_rect, 2)
        drift_drift.blit(coffee_menu_button_text, coffee_menu_button_text_rect)



        ### toggle switch for drift map on or off
        toggle_drift_map_text = font22.render("Use Drift Map OR Ancient Map", True, color_border)
        toggle_drift_map_text_rect = pygame.Rect(5, 870,3 * cell_width, cell_height )
        pygame.draw.rect(canvas, color_wash, toggle_drift_map_text_rect )
        pygame.draw.rect(canvas, color_border,toggle_drift_map_text_rect  , 2)
        canvas.blit(toggle_drift_map_text,toggle_drift_map_text_rect)
        pygame.draw.rect(drift_drift, color_wash, toggle_drift_map_text_rect )
        pygame.draw.rect(drift_drift, color_border,toggle_drift_map_text_rect  , 2)
        drift_drift.blit(toggle_drift_map_text,toggle_drift_map_text_rect)
        
        ship_detail(window,canvas,selected_ship_number)
        ship_detail(window,drift_drift,selected_ship_number)
        display_drift=False
        display_select=True
        while display_select:
            if display_drift==True:
                window.blit(drift_drift, (0, 0))
            else:
                #print("371 no drift display")
                window.blit(canvas, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    pygame.quit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(0, len(button_names)):  
                        button[i].clicked = True if buttontext_rect[i].collidepoint(event.pos) else False
                        if button[i].clicked == True:
                            print("374 button i clicked",i)
                            for xl in range(button_numb):
                                #print("376 xl",xl)
                                for sj in range(0, smax):
                                    print ("377 found",ship_list_selected[sj].ship_name,button_names[i][0])
                                    if ship_list_selected[sj].ship_name in button_names[i][0]:
                                        #print ("379 found",ship_list_selected[sj].ship_name,button_names[i][0])
                                        selected_ship_number=sj

                                        ship_detail(window,canvas,selected_ship_number)
                                        ship_detail(window,drift_drift,selected_ship_number)
                                        break
            
                    coffee_menu_button_clicked = True if coffee_menu_button_text_rect.collidepoint(event.pos) else False
                    if coffee_menu_button_clicked == True:
                        goinside.goinside_sub(window,canvas,from_key=1)

                    prepare_routes_button_clicked=True if set_sail_button_text_rect.collidepoint(event.pos) else False
                    #prepare_routes_button_clicked = True if prepare_routes_text_rect.collidepoint(event.pos) else False
                    if prepare_routes_button_clicked == True:
                        display_select=False
                        prepare_routes(window,canvas, drift_drift,set_sail_button_text_rect,img2r,map_map,premiums_set,button,button_names,buttontext_rect,display_drift,selected_ship_number)
                    
                    if toggle_drift_map_text_rect.collidepoint(event.pos) == True:
                        if display_drift==True:
                            display_drift = False
                        else:
                            display_drift = True
                        #print("412 display_drift",display_drift)

def prepare_routes(window,canvas, drift_drift,set_sail_button_text_rect,img2r,map_map,premiums_set,button,button_names,buttontext_rect,display_drift,selected_ship_number):
    ship_list_selected = local_data.ship_list_selected # retrieve mirror  
    smax=local_data.smax
    button_numb = len(local_data.button_names)
    cell_width=100
    cell_height=25

    menu_margin = 5
    menu_width = 200
    menu_height = 25 
    toggle_drift_map_text_rect = pygame.Rect(5, 870,3 * cell_width, cell_height )
    coffee_menu_button_text_rect = pygame.Rect(menu_margin, 930, 3 * cell_width, cell_height)

    color_wash = 'white'
    color_text = 'black'
    color_border = 'blue'
    
    color_header='red'
    margin_x=0
    margin_y=0
    
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    font20g = pygame.font.SysFont("Georgia", 20, bold=False) 
        ### display dots for ports and destinations########################
    set_sail_button_text1 = font22.render(" Preparing Routes - Please Wait", True,color_text)
    set_sail_button_text2 = font22.render(" Preparing Routes - Please Wait ", True,color_text)
    set_sail_button_text_rect = pygame.Rect(600, 400, 2.5 * menu_width, menu_height)
    pygame.draw.rect(canvas, color_wash, set_sail_button_text_rect)
    pygame.draw.rect(canvas, color_border, set_sail_button_text_rect, 2)
    pygame.draw.rect(drift_drift, color_wash, set_sail_button_text_rect)
    pygame.draw.rect(drift_drift, color_border, set_sail_button_text_rect, 2)
    canvas.blit(set_sail_button_text1, set_sail_button_text_rect)
    drift_drift.blit(set_sail_button_text2, set_sail_button_text_rect)
    
    if display_drift==True: # to give immediate update before dots are plotted - which takes time
            window.blit(drift_drift, (0, 0))     
    else:
            window.blit(canvas, (0, 0))
    pygame.display.update()
    
    for i in range(0,smax):
    
        ship_color = local_data.list_colors[i]

        ship_list_selected[i].get_port(i)  # gets the x,y coordinates of the originating port and stores in ship_list_selected[i].ports_tuple[0]
        #print("433 ports tuple",ship_list_selected[i].ship_name, ship_list_selected[i].ports_tuple)
        ship_list_selected[i].ship_x_last=ship_list_selected[i].port_x # sets the initial conditions
        ship_list_selected[i].ship_y_last=ship_list_selected[i].port_y
        
        ship_list_selected[i].port_delay=i*2 # staggers departure of ships
    
        pygame.draw.circle(canvas, color_border, (ship_list_selected[i].ports_tuple[0]+margin_x, ship_list_selected[i].ports_tuple[1]+margin_y),
                        10)
        pygame.draw.circle(canvas, color_header, (ship_list_selected[i].ports_tuple[2]+margin_x, ship_list_selected[i].ports_tuple[3]+margin_y),
                        10)
        pygame.draw.circle(drift_drift, color_border, (ship_list_selected[i].ports_tuple[0]+margin_x, ship_list_selected[i].ports_tuple[1]+margin_y),
                        10)
        pygame.draw.circle(drift_drift, color_header, (ship_list_selected[i].ports_tuple[2]+margin_x, ship_list_selected[i].ports_tuple[3]+margin_y),
                        10)
        
        for k in range(0, len(ship_list_selected[i].path_go)-1):   # display paths as grid
                #print("path go",ship_list_selected[i].path_go[k])
            point_x = ship_list_selected[i].path_go[k][0]
            point_y = ship_list_selected[i].path_go[k][1]
            point_x1=ship_list_selected[i].path_go[k+1][0]
            point_y1=ship_list_selected[i].path_go[k+1][1]
            pygame.draw.circle(canvas, ship_color, (point_y * 16, point_x * 16), 3)
            pygame.draw.line(canvas,ship_color,(point_y * 16, point_x * 16),(point_y1 * 16, point_x1 * 16), 1)
            pygame.draw.circle(drift_drift, ship_color, (point_y * 16, point_x * 16), 3)
            pygame.draw.line(drift_drift,ship_color,(point_y * 16, point_x * 16),(point_y1 * 16, point_x1 * 16), 1)
        for k in range(0, len(ship_list_selected[i].path_back)-1):
            point_x = ship_list_selected[i].path_back[k][0]
            point_y = ship_list_selected[i].path_back[k][1]
            point_x1 = ship_list_selected[i].path_back[k + 1][0]
            point_y1 = ship_list_selected[i].path_back[k + 1][1]
            pygame.draw.circle(canvas, ship_color, (point_y * 16, point_x * 16), 3)
            pygame.draw.line(canvas, ship_color, (point_y * 16, point_x * 16), (point_y1 * 16, point_x1 * 16), 1)
            pygame.draw.circle(drift_drift, ship_color, (point_y * 16, point_x * 16), 3)
            pygame.draw.line(drift_drift, ship_color, (point_y * 16, point_x * 16), (point_y1 * 16, point_x1 * 16), 1)
        
    
    if premiums_set==True:
        set_sail_button_text = font22.render("               Click to Set Sail   !!!", True, color_header)
    else:
        set_sail_button_text = font22.render(" Click to Return to Coffee Shop and negotiate premiums !!!", True, color_header)
    
    pygame.draw.rect(canvas, color_wash, set_sail_button_text_rect)
    pygame.draw.rect(canvas, color_border, set_sail_button_text_rect, 2)
    canvas.blit(set_sail_button_text, set_sail_button_text_rect)
    pygame.draw.rect(drift_drift, color_wash, set_sail_button_text_rect)
    pygame.draw.rect(drift_drift, color_border, set_sail_button_text_rect, 2)
    drift_drift.blit(set_sail_button_text, set_sail_button_text_rect)
   
    
    if display_drift==True:
            window.blit(drift_drift,(0,0))
    else:
            window.blit(canvas, (0, 0))
    pygame.display.update()
    click_to_sail_wait=True
    while click_to_sail_wait==True:

        for event in pygame.event.get():
            #print("517 2nd event.get")
            if event.type == pygame.QUIT:
                click_to_sail_wait = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                for i in range(0, len(button_names)):  
                    button[i].clicked = True if buttontext_rect[i].collidepoint(event.pos) else False
                    if button[i].clicked == True:
                        for xl in range(button_numb):
                            for sj in range(0, smax):
                                if ship_list_selected[sj].ship_name in button_names[i][0]:
                                    selected_ship_number=sj
                                    print("519 selected ship number",sj)
                                    ship_detail(window,canvas,selected_ship_number)
                                    ship_detail(window,drift_drift,selected_ship_number)
                                    break
                    
                if display_drift==True:
                    window.blit(drift_drift,(0,0))
                else:
                    window.blit(canvas, (0, 0))
                pygame.display.update()     
               
                if set_sail_button_text_rect.collidepoint(event.pos) == True and premiums_set==True:
                    click_to_sail_wait=False
                    ship_display(window,canvas,drift_drift, img2r,display_drift,map_map)
                elif premiums_set==True:
                    click_to_sail_wait=True
                else:
                    goinside.goinside_sub(window,canvas,from_key=1)
                coffee_menu_button_clicked = True if coffee_menu_button_text_rect.collidepoint(event.pos) else False
                if coffee_menu_button_clicked == True:
                    goinside.goinside_sub(window,canvas,from_key=1)
                
                if toggle_drift_map_text_rect.collidepoint(event.pos) == True:
                    if display_drift==True:
                        display_drift = False
                    else:
                        display_drift = True
                    
   #-----------------SHIP DISPLAY-------------------------------------------------------------------------------


def ship_display(window,canvas,drift_drift, img2r,display_drift,map_map):
   
    ship_list_selected = local_data.ship_list_selected # retrieve mirror
    insurers_list = local_data.insurers_list # retrieve mirror
    smax=local_data.smax
    mmax=local_data.mmax
    selected_ship_number=0 # until selected
    
    ### Instantiate Weather Events ################################
    
    weather_events_list = []

    for iw in range(len(local_data.weather_events_list)):
        weather_events_list.append(subroutines.Weather_event(iw))  # instantiates for all types of weather event
       
    if (len(local_data.weather_severities_chosen)>0): # if weather severities have been adjusted in Settings
        for iw in range(len(local_data.weather_events_list)):
            weather_events_list[iw].weather_settings_update(iw)
    mapwidth=1500
    mapheight=mapwidth*.75
    margin_x=0
    margin_y=0
   
    cell_width=100
    cell_height=25

    menu_margin = 5
   
    convert_pixel = 16
    grid = local_data.mapx

    menu_margin = 5
    
    color_wash = 'white'
    color_text = 'black'
    color_border = 'blue'
    color_bg='white'
    color_button='blue'
    color_header='red'
    
    font18 = pygame.font.SysFont("Arial", 18, bold=False)
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    font20g = pygame.font.SysFont("Georgia", 20, bold=False) 

    weather_sep = 0  # separates weater events
    game_speed_conv = 5000  # equals milliseconds timeactual time which equals one day of ship travel as game time (was 25714)
    alimit = 1# for debugging
    hazard_k=0 # used to ensure that only one set of damage incurred per grid square
    
    display_finances = False
    display_master_log=False
    display_all_routes=True # for ship display , all routes or one set by ship log selected
    ship_wait=False # time for turnaroun
   
    hazard=0
    beached=False
    
    weather_state=False
    #print("604 display drift",display_drift)
    if display_drift==True:
        canvas_drift=drift_drift
        map_map.draw_map(canvas_drift)  # imports and displays sprites (from Tiles)
    else:
        canvas_drift=canvas
        canvas_drift.blit(img2r, (0, 0))  # blit map first each and every time otherwise weather events and ships blur tracking

    grid = local_data.mapx

        ### TIME HANDLING ###
    mystarttime=pygame.time.get_ticks()
    mytime_last=mystarttime
        # previous time settings using get_ticks and starttime
    
    for i in range(0,smax):
    #for i in range(0,1): # for debugging
        ship_color = local_data.list_colors[i]

        ports_tuple = ship_list_selected[i].get_port(i)  # gets the x,y coordinates of the originating port
    
        ship_list_selected[i].ship_x_last=ship_list_selected[i].port_x # sets the initial conditions
        ship_list_selected[i].ship_y_last=ship_list_selected[i].port_y
        ship_list_selected[i].ship_x=ship_list_selected[i].port_x # sets the initial conditions
        ship_list_selected[i].ship_y=ship_list_selected[i].port_y
        ship_list_selected[i].port_delay=i*2 # staggers departure of ships
        ship_x_last= ship_list_selected[i].ship_x_last
        ship_y_last= ship_list_selected[i].ship_y_last
        ship_x= ship_list_selected[i].ship_x
        ship_y= ship_list_selected[i].ship_y
        #print("649 ship_x_last", round(ship_x_last,1), "ship x ",round(ship_x,1)," ship_y_last", round(ship_y_last,1), "ship y ",round(ship_y,1))     
        pygame.draw.circle(canvas_drift, color_border, (ship_list_selected[i].ports_tuple[0]+margin_x, ship_list_selected[i].ports_tuple[1]+margin_y),
                        10)
        pygame.draw.circle(canvas_drift, color_header, (ship_list_selected[i].ports_tuple[2]+margin_x, ship_list_selected[i].ports_tuple[3]+margin_y),
                        10)
    window.blit(canvas_drift, (0, 0))
    pygame.display.update()
        
    running=True
    #------------------------------------RUNNING------------------------------------------------------
    while running:
        #print("628 display drift",display_drift)
        if display_drift==True:
            canvas_drift=drift_drift
            map_map.draw_map(canvas_drift)  # imports and displays sprites (from Tiles)
        else:
            canvas_drift=canvas
            canvas_drift.blit(img2r, (0, 0))  # blit map first each and every time otherwise weather events and ships blur tracking

        
        mytime = pygame.time.get_ticks()
        mytotal_time = mytime - mystarttime
        myinterval = mytime - mytime_last  # as play milliseconds
        myinterval_days = myinterval / game_speed_conv
        
        mytotal_time_days = mytotal_time / game_speed_conv
        mytotal_time_months = int(mytotal_time_days / 30)
        mytotal_time_years = int(mytotal_time_months / 12)
        mytotal_time_months_res = mytotal_time_months - mytotal_time_years * 12
        mytotal_time_days_res = mytotal_time_days - mytotal_time_months * 30
        mytotal_time_years_res = mytotal_time_months - mytotal_time_years * 12
        #print("665 myinterval ms",myinterval,"mytotal_time ms",mytotal_time,"my last time ms ",mytime_last,"interval_days",myinterval_days,"mytotal_time_days",mytotal_time_days,"mytotal_time_months",mytotal_time_months,"mytotal_time_days_res",mytotal_time_days_res,"mytotaltime_months_res",mytotal_time_months_res)
        
        gridtop_text_rend,gridtop_text_rect=get_current(grid)
        canvas_drift.blit(gridtop_text_rend, gridtop_text_rect)
        window.blit(canvas_drift,(0,0))
        journey_time_text_rect = pygame.Rect(5, 10, 350, 40)
        pygame.draw.rect(canvas_drift, color_wash, journey_time_text_rect)  # avoid over writing previous entry
    
        journey_time_text = font22.render("Time:  "+str(mytotal_time_years) + " years" +
                                          "  " + str(mytotal_time_months_res) + " months " + str(
            round(mytotal_time_days_res, 0)) + " days ", True,
                                          color_text)
        pygame.draw.rect(canvas_drift, color_border, journey_time_text_rect, 2)  # avoid over writing previous entry
        canvas_drift.blit(journey_time_text, journey_time_text_rect)
        window.blit(canvas_drift, (0, 0))
    
        ### return to coffee ship menu
        coffee_menu_button_text = font22.render("Coffee Shop Menu", True, color_border)
        coffee_menu_button_clicked = False
        coffee_menu_button_text_rect = pygame.Rect(menu_margin, 930, 3 * cell_width, cell_height)
        pygame.draw.rect(canvas_drift, color_wash, coffee_menu_button_text_rect)
        pygame.draw.rect(canvas_drift, color_border, coffee_menu_button_text_rect, 2)
        canvas_drift.blit(coffee_menu_button_text, coffee_menu_button_text_rect)
    
        ### toggle switch for ship insurer list on or off
        toggle_ship_insurer_list_text = font22.render("Toggle to see Insurers and Ships Gains and Losses: On/Off", True, color_border)
        toggle_ship_insurer_list_text_rect = pygame.Rect(5, 900,5 * cell_width, cell_height )
        toggle_ship_insurer_button=False
        pygame.draw.rect(canvas_drift, color_wash, toggle_ship_insurer_list_text_rect )
        pygame.draw.rect(canvas_drift, color_border,toggle_ship_insurer_list_text_rect  , 2)
        canvas_drift.blit(toggle_ship_insurer_list_text,toggle_ship_insurer_list_text_rect)

        ### toggle switch for ship all routes on or off
        all_routes_button_text = font22.render("All Routes/Selected Route", True, color_border)
        all_routes_button_clicked = False
        all_routes_button_start_x=5
        all_routes_button_text_rect = pygame.Rect(menu_margin, 840, 3 * cell_width, cell_height)
        pygame.draw.rect(canvas_drift, color_wash, all_routes_button_text_rect)
        pygame.draw.rect(canvas_drift, color_border, all_routes_button_text_rect, 2)
        canvas_drift.blit(all_routes_button_text, all_routes_button_text_rect)

        ### toggle switch to display master log
        master_log_button_text = font22.render("Toggle Master Log Display", True, color_border)
        master_log_button_clicked = False
        master_log_button_text_rect = pygame.Rect(menu_margin, 870, 3 * cell_width, cell_height)
        pygame.draw.rect(canvas_drift, color_wash, master_log_button_text_rect)
        pygame.draw.rect(canvas_drift, color_border, master_log_button_text_rect, 2)
        canvas_drift.blit(master_log_button_text, master_log_button_text_rect)


        buttonstart_x = 1250
        buttonstart_y = 20
        buttonheight = cell_height
        buttonwidth = 250
        buttonheight = 22
        
        button_names = []
        button_names.append(["     Ships Listed by Insurer", 1], )
        button_names.append(["     Click on Ship for Route", 1], )
        
        for m in range(0, mmax):
                insurer_name = insurers_list[m].insurer_name
                insurer_text_raw = " by Insurer " + insurer_name+":"
                button_names.append([insurer_text_raw, 1], )
                for sj in range(0, smax):
                    #print("in ships listed by insurer mmax,smax time,insurer name, ship_insurer",mmax,smax, mytotal_time_months,insurer_name,ship_list_selected[sj].ship_insurer,ship_list_selected[sj].ship_name)
                    if insurer_name == ship_list_selected[sj].ship_insurer:
                        button_text_1_raw = "     Ship Name:  " + ship_list_selected[sj].ship_name
                        button_names.append([button_text_1_raw, 0])
                        button_text_2_raw = "     " + ship_list_selected[sj].port + " to " + ship_list_selected[
                            sj].destination
                        button_names.append([button_text_2_raw, 2])
        button_names.append([" Uninsured:",1],)
        for sj in range(0,smax):
                if ship_list_selected[sj].ship_insurer=="Uninsured":
                        button_text_1_raw = "     Ship Name:  " + ship_list_selected[sj].ship_name
                        button_names.append([button_text_1_raw,0])
                        button_text_2_raw = "     " + ship_list_selected[sj].port+ " to "+ship_list_selected[sj].destination
                        button_names.append([button_text_2_raw, 2])
        button = []
        buttontext_rect = []
            #############display buttons########################
        button_numb = len(button_names)
        for i in range(button_numb):
            button.append(
                subroutines.Button(buttonstart_x, buttonstart_y + i * buttonheight, buttonwidth, buttonheight,
                                    button_names[i][0],
                                    button_names[i][1], "False"))

        for i in range(button_numb):
                if button[i].rect_color == 1:
                    buttontext_rect.append(
                        subroutines.Button.button_rect_blit(button[i], canvas_drift, color_border, color_text, color_wash))
                elif button[i].rect_color == 0:
                    buttontext_rect.append(
                        subroutines.Button.button_rect_blit(button[i], canvas_drift, color_button, color_text, color_wash))
                else:  # 2
                    buttontext_rect.append(
                        subroutines.Button.button_rect_blit(button[i], canvas_drift, color_bg, color_text, color_wash))
        for i in range(button_numb):
                for sj in range(0, smax):
                    if ship_list_selected[sj].ship_name in button_names[i][0]:

                        ship_color = local_data.list_colors[sj]
                        pygame.draw.circle(canvas_drift, ship_color, (buttonstart_x + 8, buttonstart_y + i * buttonheight + 10),
                                8)
       
            ### SHIP ROUTE
        
            ### START EXTENSIVE LOOP OF ALL SHIPS [I]###############
        for i in range(0,smax): 
        #for i in range(0,1): # for debugging
            ship_color = local_data.list_colors[i]
            #print("666 at start of big ship loop",ship_list_selected[i].ship_name)
            
            #print("671 ship_x_last", round(ship_x_last,1), "ship x ",round(ship_x,1)," ship_y_last", round(ship_y_last,1), "ship y ",round(ship_y,1))     

            #print("665 myinterval ms",myinterval,"mytotal_time ms",mytotal_time,"my last time ms ",mytime_last,"interval_days",myinterval_days,"mytotal_time_days",mytotal_time_days,"mytotal_time_months",mytotal_time_months,"mytotal_time_days_res",mytotal_time_days_res,"mytotaltime_months_res",mytotal_time_months_res)
            #print("674 ship_x_last", round(ship_x_last,1), "ship x ",round(ship_x,1)," ship_y_last", round(ship_y_last,1), "ship y ",round(ship_y,1))
            
            pygame.draw.circle(canvas_drift, ship_color, (ship_list_selected[i].ship_x, ship_list_selected[i].ship_y),
                                ship_list_selected[i].marker_radius)
            window.blit(canvas_drift, (0, 0))     # to capture ship at port

           
            #################  KEY SUBROUTINE CALLS  #########################
            pay_premium(i,mytotal_time_years)
            weather_development(canvas_drift,mytotal_time_months,mytotal_time_months_res,mytotal_time_days,mytotal_time_days_res,myinterval_days,weather_events_list)
            hazard=evaluate_hazards(canvas_drift,i,grid,mytotal_time_months,mytotal_time_days_res) # inserted to ensure that hazard is evaluated at current position
            if (hazard==1 or hazard==2 or hazard==4) and weather_state==True: # beached in storm or other weather event
                beached=True
            else:
                beached=False
            #print("660 beach cond,weather_state,hazard", ship_list_selected[i].ship_name,beached,weather_state,hazard)
            ship_x_last= ship_list_selected[i].ship_x_last
            ship_y_last= ship_list_selected[i].ship_y_last
            ship_x= ship_list_selected[i].ship_x
            ship_y= ship_list_selected[i].ship_y
            #print("714 ship_x_last", round(ship_x_last,1), "ship x ",round(ship_x,1)," ship_y_last", round(ship_y_last,1), "ship y ",round(ship_y,1))
            ship_waymarks_tuple=ship_waymarks(i,mytotal_time) # retrieves the waymarks for this stage of the ship's journey and if the ship has sailed from port or destination
            wp_next_x=ship_waymarks_tuple[2]
            wp_next_y=ship_waymarks_tuple[3]
            ship_sail_ok=ship_port_delay(i,canvas_drift, mytotal_time,mytotal_time_months,mytotal_time_days,mytotal_time_days_res,ship_color) # prevent ship from moving before allowed
            #print("820 ship name",ship_list_selected[i].ship_name,"ship sail ok",ship_sail_ok)
            if ship_sail_ok==True and beached==False and ship_wait==False: # and in water not beach, rocks, land in weather event and is not waiting at port
                move_sail_x,move_sail_y=ship_move_sail(i,myinterval_days,wp_next_x,wp_next_y)# calculates the amount by which the ship has moved ue to its own sail power
                move_drift_x,move_drift_y= ship_move_drift(i,myinterval_days,grid)# calculates how much the ship has moved due to ocean drift
                move_wind_x,move_wind_y,weather_state=ship_move_wind(i,mytotal_time_months,mytotal_time_days_res,myinterval_days,weather_events_list,mmax, insurers_list,hazard)
            else:
                append_text=("806 not allowed to move: ship_sail_ok"+str(ship_sail_ok)+"beached"+str(beached)+"wait"+str(ship_wait))
                append_if(i, append_text, mytotal_time_months, mytotal_time_days_res, time_stamp=True)
                move_sail_x=0
                move_sail_y=0
                move_drift_x=0
                move_drift_y=0
                move_wind_x=0
                move_wind_y=0
                ship_list_selected[i].weather_disp_x = 0;ship_list_selected[i].weather_disp_y = 0
            #print("812 move sail, x,y",ship_list_selected[i].ship_name,round(move_sail_x,3),round(move_sail_y,3),"drift",round(move_drift_x,3),round(move_drift_y,3),"wind",round(move_wind_x,3),round(move_wind_y,3),"beached",beached)
            ship_x=ship_x+move_sail_x+move_drift_x+move_wind_x           
            ship_y=ship_y+move_sail_y+move_drift_y+move_wind_y
            #print("796 at ship xy before ship_move_sail",ship_list_selected[i].ship_name,round(ship_list_selected[i].ship_x,1), round(ship_list_selected[i].ship_y,1))
            ship_list_selected[i].ship_x=ship_x
            ship_list_selected[i].ship_y=ship_y
            #print("798 at ship xy after ship_move_sail",ship_list_selected[i].ship_name,round(ship_list_selected[i].ship_x,1), round(ship_list_selected[i].ship_y,1))
            ship_list_selected[i].ship_x_last=ship_x
            ship_list_selected[i].ship_y_last=ship_y
            hazard=evaluate_hazards(canvas_drift,i,grid,mytotal_time_months,mytotal_time_days_res)
            if (hazard == 1) or (hazard == 2) or (hazard == 4):
            # Ship hit a barrier - revert to position before the move
            # This allows damage to be applied but stops the ship from continuing
                ship_list_selected[i].ship_x = ship_x_last  # Revert to position before move
                ship_list_selected[i].ship_y = ship_y_last  # Revert to position before move
                ship_list_selected[i].ship_x_last = ship_x_last  # Keep last position as the safe one
                ship_list_selected[i].ship_y_last = ship_y_last
                # Reset weather displacement to prevent continued pushing
                ship_list_selected[i].weather_disp_x = 0
                ship_list_selected[i].weather_disp_y = 0




            ship_list_selected[i].ship_x = ship_x_last  # Revert to position before move
            pygame.draw.circle(canvas_drift, ship_color, (ship_list_selected[i].ship_x, ship_list_selected[i].ship_y),
                                ship_list_selected[i].marker_radius)
            ###########check if close to next way point move to next way point#####################
                
            fraction_x = wp_next_x-ship_list_selected[i].ship_x
            fraction_y = wp_next_y-ship_list_selected[i].ship_y
            #print("727 fraction_x",fraction_x,"fraction_y",fraction_y)
            if abs(fraction_x) < alimit and abs(fraction_y) < alimit:
                #print("748 changing way point",ship_list_selected[i].ship_k,ship_list_selected[i].ship_k + 1)
        
                ship_list_selected[i].ship_k = ship_list_selected[i].ship_k + 1
            ### UPDATE SHIP PROGRESS
           
            ship_list_selected[i].ship_event_x_list.append(ship_list_selected[i].ship_x) # event_x and event_y list hold actual track of ship
            ship_list_selected[i].ship_event_y_list.append(ship_list_selected[i].ship_y)
            #print("729 ship_x_last", ship_list_selected[i].ship_x_last, "ship x ",ship_list_selected[i].ship_x,"912 ship_y_last", ship_list_selected[i].ship_y_last, "ship y ",ship_list_selected[i].ship_y)
            pygame.draw.circle(canvas_drift, ship_color, (ship_list_selected[i].ship_x, ship_list_selected[i].ship_y),
                                ship_list_selected[i].marker_radius)
            
                
            in_port=ship_destination_check(i,canvas_drift,mytotal_time,mytotal_time_months,mytotal_time_days_res)
            if in_port==True:
                if mytotal_time_days-ship_list_selected[i].ship_arrive_time<local_data. ship_turnaround_time:
                    append_text="ship turnaround - waiting in port"
                    append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
                    ship_list_selected[i].ship_wait=True
                else:
                    ship_list_selected[i].ship_wait=False
           
                    ###################draw actual progress of ship ##############################
            
            if display_all_routes==True:
                ishow=i
            else:
                ishow=selected_ship_number
            ship_color = local_data.list_colors[ishow]
                
            #print ("873 ishow at end of i loop",ishow)
            for k in range(len(ship_list_selected[ishow].ship_event_x_list)):  # to track actual progress of ship
                    #print("1327 tracking progress - k",k)
                    pygame.draw.circle(canvas_drift, ship_color, (ship_list_selected[ishow].ship_event_x_list[k], ship_list_selected[ishow].ship_event_y_list[k]), 2)
        
        if display_finances==True:
            #print("display finances")
            
            subroutines.finances_sub(window, canvas_drift)
        
        if display_master_log==True:
          
            
            subroutines.master_log_sub(window, canvas_drift)
        
          ### display log
        #selected_ship_number=0 # for proof testing
        ship_list_selected[selected_ship_number].ship_log_update(selected_ship_number) # necessary to load premium
        #print("ship log",ship_list_selected[selected_ship_number].ship_log)
        ship_log_display(canvas_drift, ship_list_selected[selected_ship_number].ship_log)
        #print("851 master_log ",local_data.master_log)
        
        window.blit(canvas_drift, (0, 0))     
        pygame.display.update()
        #print("860 at mytime_last")
        mytime_last = mytime
   
        

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    for i in range(0, len(button_names)):
                        button[i].clicked = True if buttontext_rect[i].collidepoint(event.pos) else False
                        if button[i].clicked == True:
                            for xl in range(button_numb):
                                for sj in range(0, smax):
                                    if ship_list_selected[sj].ship_name in button_names[i][0]:
                                        selected_ship_number = sj
                                        #print ("selected ship number", selected_ship_number, ship_list_selected[selected_ship_number].ship_name)
                                        break

                    window.blit(canvas_drift, (0, 0))
                    pygame.display.update()

                    coffee_menu_button_clicked = True if coffee_menu_button_text_rect.collidepoint(event.pos) else False
                    if coffee_menu_button_clicked == True:
                        goinside.goinside_sub(window,canvas,from_key=1)
                    if toggle_ship_insurer_list_text_rect.collidepoint(event.pos) == True:
                        if display_finances==True:
                            display_finances = False
                        else:
                            display_finances = True
                    
                    if master_log_button_text_rect.collidepoint(event.pos) == True:
                        if display_master_log==True:
                            display_master_log = False
                        else:
                            display_master_log = True
                   
                    if all_routes_button_text_rect.collidepoint(event.pos)==True:
                        if display_all_routes==True:
                            display_all_routes = False
                        else:
                            display_all_routes = True


def ship_move_sail(i,myinterval_days,wp_next_x,wp_next_y):
            ############# displacement due to ship speed###############
            fudge=1 # for debugging
            ship_list_selected = local_data.ship_list_selected  # retrieve mirror

            fraction_x = wp_next_x-ship_list_selected[i].ship_x
            fraction_y = wp_next_y-ship_list_selected[i].ship_y
            #print("1012 in ship_move_sail",ship_list_selected[i].ship_name,ship_list_selected[i].ship_x,ship_list_selected[i].ship_y,wp_next_x,wp_next_y)
            v1=pygame.math.Vector2(ship_list_selected[i].ship_x,ship_list_selected[i].ship_y  )
            v2=pygame.math.Vector2(wp_next_x,wp_next_y )
            v3=v2-v1
           
            v3_magnitude=v3.magnitude()
            # southern part of map is 1.6 times more difficult
            if ship_list_selected[i].ship_y > 700:
                distortion_factor = 1.6
            else:
                distortion_factor = 1
            speed_interval=fudge*myinterval_days * 24 * ship_list_selected[i].ship_speed_cond/distortion_factor
            v3_move=v3*speed_interval/v3_magnitude
            #print("1030 speed_interval",speed_interval,"v3 magnitude",v3_magnitude)
            #print ("1021 vectors 1,2,3,v3_move",v1,v2,v3,v3_move)
            move_x_naut=v3_move[0]
            move_y_naut=v3_move[1]

            move_sail_x = move_x_naut / 3  # as pixels
            move_sail_y = move_y_naut / 3

            return(move_sail_x,move_sail_y)

def weather_development(canvas,mytotal_time_months,mytotal_time_months_res,mytotal_time_days,mytotal_time_days_res,myinterval_days,weather_events_list):
    
    font20g = pygame.font.SysFont("Georgia", 20, bold=False)
   
    color_text = 'black'
    color_border = 'blue'
    
    for iw in range(len(weather_events_list)):
        #print("833 in weather",iw)
        if mytotal_time_months >= weather_events_list[iw].month_start and mytotal_time_months_res <= weather_events_list[iw].month_end:  # event is in season

            if mytotal_time_months != weather_events_list[
                iw].month_end_reset:  # does not allow recurrence in same month

                if mytotal_time_days_res >= random.randint(0, 30) and weather_events_list[
                    iw].exists == False:  # chooses random day in month to start the weather event

                    weather_events_list[iw].started_days = mytotal_time_days
                    weather_events_list[iw].started = True
                    weather_events_list[iw].exists = True  # exists and started - one can probably be removed.
        else:
                pass

        if weather_events_list[iw].exists == True:  # updates event age
            weather_events_list[iw].age = mytotal_time_days - weather_events_list[iw].started_days

            if weather_events_list[iw].age >= weather_events_list[iw].duration:  # event has reached age

                weather_events_list[iw].reset(iw, mytotal_time_months)  # sets data on event progress to zero
        else:  # possibly redundant
            weather_events_list[iw].ended = False

        if weather_events_list[iw].exists == True:
            #print ("859 in weather myinterval days",iw, myinterval_days)
            position_tuple = weather_events_list[iw].drift_event(myinterval_days, iw)
            # print('position and wind speed ', position_tuple)
            weather_events_list[iw].event_x = position_tuple[0]
            weather_events_list[iw].event_y = position_tuple[1]
            # weather_events_list[iw].wind_speed_max= position_tuple[2]
            weather_events_list[iw].wind_speed = position_tuple[2]
            wind_speed_min=weather_events_list[iw].wind_speed_min
            weather_events_list[iw].event_x_list.append(weather_events_list[iw].event_x)
            weather_events_list[iw].event_y_list.append(weather_events_list[iw].event_y)
            if weather_events_list[iw].wind_speed < wind_speed_min:
                weather_events_list[iw].event_radius = weather_events_list[iw].starting_event_radius
            elif (0 <= weather_events_list[iw].wind_speed < 34):
                    color_ring = 'blue'
                    weather_events_list[iw].event_radius = weather_events_list[iw].starting_event_radius

            elif (34 <= weather_events_list[iw].wind_speed < 64):
                    color_ring = 'black'
                    weather_events_list[iw].event_radius = weather_events_list[iw].starting_event_radius * 1.5

            elif (64 <= weather_events_list[iw].wind_speed < 83):
                    color_ring = 'orange'
                    weather_events_list[iw].event_radius = weather_events_list[iw].starting_event_radius * 2.0

            elif (83 <= weather_events_list[iw].wind_speed < 96):
                    color_ring = 'darkorange3'
                    weather_events_list[iw].event_radius = weather_events_list[iw].starting_event_radius * 2.5

            elif weather_events_list[iw].wind_speed >= 96:
                    color_ring = 'red'
                    weather_events_list[iw].event_radius = weather_events_list[iw].starting_event_radius * 3

            else:
                    pass

            for ik in range(len(weather_events_list)):
                weather_sep=0 # to be developed later
                dist_weather = math.sqrt(
                    (weather_events_list[iw].event_x - weather_events_list[ik].event_x) ** 2 + (
                            weather_events_list[iw].event_y - weather_events_list[
                        ik].event_y) ** 2)  # find distance to other weather events
                if dist_weather < (weather_events_list[iw].event_radius + weather_events_list[
                    ik].event_radius) + weather_sep:  # creates a separation of weather)sep
                    
                    if (weather_events_list[ik].event_type[0:4] != "Pira" and weather_events_list[iw].event_type[
                                                                            0:4] != "Pira"):
                        if weather_events_list[iw].event_type != weather_events_list[ik].event_type:
                            # print("distance weather - cancel weather event", weather_events_list[iw].event_type,weather_events_list[ik].event_type, dist_weather)
                            if weather_events_list[iw].event_radius >= weather_events_list[ik].event_radius:
                                weather_events_list[
                                    ik].exists = False  # ends smaller of the two weather events by event radius
                                weather_events_list[ik].ended = True
                                weather_events_list[ik].reset(ik, mytotal_time_months)

            if (weather_events_list[iw].event_type == "Hurricane_E") or (
                    weather_events_list[iw].event_type == "Hurricane_W") or (
                    weather_events_list[iw].event_type == "Storms_W") or (
                    weather_events_list[iw].event_type == "Storms_E"):
                #print (weather_events_list[iw].event_type,"wind speed", weather_events_list[iw].wind_speed,"color_ring", color_ring,"event radius",weather_events_list[iw].event_radius)

                pygame.draw.circle(canvas, color_ring,
                                (weather_events_list[iw].event_x, weather_events_list[iw].event_y),
                                weather_events_list[iw].event_radius, width=4)
            else:
                pygame.draw.circle(canvas, color_border,
                                (weather_events_list[iw].event_x, weather_events_list[iw].event_y),
                                weather_events_list[iw].starting_event_radius, width=4)

            weather_event_text_rect = pygame.Rect(weather_events_list[iw].event_x + 0,
                                                weather_events_list[iw].event_y - 0, 100, 50)
            weather_event_text = font20g.render(
                (weather_events_list[iw].event_type[:len(weather_events_list[iw].event_type) - 2]), True,
                color_text)
            canvas.blit(weather_event_text, weather_event_text_rect)

def ship_waymarks(i,mytotal_time):
 ## ship imagery is centralised within each grid, whose x,y is 0,0. add 8 pixels to centralise within the 16 x 16 grid square
                # go port
    ship_list_selected = local_data.ship_list_selected  # retrieve mirror
    convert_pixel=16
    if ship_list_selected[i].ship_go == True:
        wp_last_x = 8 + ship_list_selected[i].path_go[ship_list_selected[i].ship_k][1] * convert_pixel  # as pixels
        wp_last_y = 8 + ship_list_selected[i].path_go[ship_list_selected[i].ship_k][0] * convert_pixel  # as pixels
        wp_next_x = 8 + ship_list_selected[i].path_go[ship_list_selected[i].ship_k + 1][
                1] * convert_pixel  # as pixels
        wp_next_y = 8 + ship_list_selected[i].path_go[ship_list_selected[i].ship_k + 1][0] * convert_pixel
    else:
        if ship_list_selected[i].ship_k == 0:
            ship_list_selected[i].ship_depart_time = mytotal_time
            #print(' 687 depart time from destination', ship_list_selected[i].ship_name, ship_list_selected[i].ship_depart_time)
        wp_last_x = 8 + ship_list_selected[i].path_back[ship_list_selected[i].ship_k][
                1] * convert_pixel  # as pixels
        wp_last_y = 8 + ship_list_selected[i].path_back[ship_list_selected[i].ship_k][
                0] * convert_pixel  # as pixels
        wp_next_x = 8 + ship_list_selected[i].path_back[ship_list_selected[i].ship_k + 1][
                1] * convert_pixel  # as pixels
        wp_next_y = 8 + ship_list_selected[i].path_back[ship_list_selected[i].ship_k + 1][0] * convert_pixel
    #print ("965",ship_list_selected[i].ship_name,'i',i,'k',ship_list_selected[i].ship_k, 'wp_last/next' ,wp_last_x,wp_last_y, wp_next_x,wp_next_y)
    return(wp_last_x,wp_last_y,wp_next_x,wp_next_y)

def ship_port_delay(i,canvas, mytotal_time,mytotal_time_months,mytotal_time_days,mytotal_time_days_res,ship_color):
    ship_list_selected = local_data.ship_list_selected  # retrieve mirror
    font18 = pygame.font.SysFont("Arial", 18, bold=False)
    color_text='black'
    ship_sail_ok=False # ship no allowed to move until True
    port_wait=5 # days to turnaround ship
###################stagger departure or calculate new position#############################
    if (len(ship_list_selected[i].ship_log) == 0):
        append_text = ship_list_selected[i].ship_name + " in port"
        ship_list_selected[i].ship_log.append(append_text)
        append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + \
                        ship_list_selected[i].hull_condition +  str(
            round(ship_list_selected[i].ship_speed_cond, 1)+" knots " )
        ship_list_selected[i].ship_log.append(append_text)
    if ship_list_selected[i].ship_k == 0 and ship_list_selected[i].port_delay == 0:  # no port delay
        append_text = ' -ship sets sail'
        append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
        #print("append text",ship_list_selected[i].ship_name,append_text)
        ship_list_selected[i].ship_depart_time = mytotal_time
        #print (ship_list_selected[i].ship_name, append_text)
        ship_sail_ok=True
    elif ship_list_selected[i].ship_k == 0 and ship_list_selected[i].port_delay > mytotal_time_days:
        ship_list_selected[i].ship_depart_time = mytotal_time
        # delay in port
       
        append_text = ("waiting in port :"+ship_list_selected[i].port)
        append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
        #print("append text",ship_list_selected[i].ship_name,append_text)
        ship_sail_ok=False
        
   
    elif ship_list_selected[i].ship_shipwreck==True:
        pygame.draw.circle(canvas, ship_color, (ship_list_selected[i].ship_x, ship_list_selected[i].ship_y),
                            10)
        ship_event_text_rect = pygame.Rect( ship_list_selected[i].ship_x+ 0,
                                                ship_list_selected[i].ship_y- 0, 100, 25)
        pygame.draw.rect(canvas, "light blue", ship_event_text_rect)
        ship_event_text = font18.render(ship_list_selected[i].ship_name+" Shipwreck", True,
            color_text)
        canvas.blit(ship_event_text, ship_event_text_rect)
        ship_sail_ok=False
    else:  # new position 
        if ship_list_selected[i].ship_k == 0 and ship_list_selected[i].ship_go==True:
            append_text = ("-ship sets sail from "+ship_list_selected[i].port)
            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
        if ship_list_selected[i].ship_k == 0 and ship_list_selected[i].ship_go==False:
            append_text = ("-ship sets sail from "+ship_list_selected[i].destination)
            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)

        
        ship_sail_ok=True
    #print("975 ship_sail_ok",ship_sail_ok)
    return ship_sail_ok


def ship_destination_check(i,canvas,mytotal_time,mytotal_time_months,mytotal_time_days_res):
    ship_list_selected = local_data.ship_list_selected  # retrieve mirror
    in_port=False
     ################check if at destination#############
    if ship_list_selected[i].ship_go == True:
        if (ship_list_selected[i].ship_k >= len(ship_list_selected[i].path_go) - 1):  # test of destination
            #print ('1113 reached destination')
            in_port=True
            pygame.draw.circle(canvas, 'dark red', (ship_list_selected[i].ship_x, ship_list_selected[i].ship_y),
                            10)
            
            #print (ship_list_selected[i].ship_name, append_text)
            ship_list_selected[i].ship_k = 0  # resets waypoint counter
            ship_list_selected[i].ship_go = False
            ship_list_selected[i].ship_arrive_time = mytotal_time
            ship_list_selected[i].ship_outbound_time = round(
                (ship_list_selected[i].ship_arrive_time - ship_list_selected[i].ship_depart_time) * 0.2 / 1000,
                1) # check hardcoded conversion
            ship_list_selected[i].ship_depart_time = mytotal_time  # reset for return journey
            ship_list_selected[i].revenue_accum = ship_list_selected[i].revenue_accum + ship_list_selected[
                i].revenue_out
            #i = int(i)
            ship_list_selected[i].ship_repair_sub(i)
            
            append_text = "reached destination "+ship_list_selected[i].destination +" repairs and supplies in progress"
            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
            ship_list_selected[i].ship_event_x_list = [] # to track only half of journey, delete if full journey  to be tracked
            ship_list_selected[i].ship_event_y_list = []
    else:
        if (ship_list_selected[i].ship_k >= len(ship_list_selected[i].path_back) - 1):
            in_port=True
            pygame.draw.circle(canvas, 'dark red', (ship_list_selected[i].ship_x, ship_list_selected[i].ship_y),
                            10)
            
            
            append_text = "reached port "+ship_list_selected[i].destination
            
            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
            
            ship_list_selected[i].ship_event_x_list = []
            ship_list_selected[i].ship_event_y_list = []
            ship_list_selected[i].ship_repair_sub(i)
            ship_list_selected[i].damage_event_list=[]
            ship_list_selected[i].ship_k = 0
            ship_list_selected[i].ship_arrive_time = mytotal_time
            ship_list_selected[i].ship_go = True
            ship_list_selected[i].ship_inbound_time = round(
                (ship_list_selected[i].ship_arrive_time - ship_list_selected[i].ship_depart_time) * 0.2 / 1000,
                1)
            # print(ship_list_selected[i].ship_name," inbound ", ship_list_selected[i].ship_inbound_time,ship_list_selected[i].ship_arrive_time,ship_list_selected[i].ship_depart_time)
            ship_list_selected[i].ship_depart_time = mytotal_time  # reset for return journey
            ship_list_selected[i].revenue_accum = ship_list_selected[i].revenue_accum + ship_list_selected[
                i].revenue_in
            # print(ship_list_selected[i].ship_name + "  " + str(ship_list_selected[i].revenue_accum))
            
            
    return(in_port)

def get_current(grid):
    mx, my = pygame.mouse.get_pos()
    #print("1048 mx,my",mx,my)
    font22g = pygame.font.SysFont("Georgia", 22, bold=False)
    color_border='blue'
    list_width=300
    list_height=25
    #print("546 my,my mouse pos",mx,my)
    if mx>1000: mxx=1000
    else: mxx=mx
    if my>930: myy=930
    else: myy=my
    mx_tile = int(mxx / 16)
    my_tile = int(myy / 16)
    gridtop = int(grid[my_tile][mx_tile])
        # print("gridtop", gridtop)
    gridtop_text_rect = pygame.Rect(mxx + 20, myy, list_width,
                                        list_height)
    if gridtop==-1:
        gridtop_text=""
    else:
        gridtop_text = local_data.list_tile_id[gridtop]
    if gridtop == 5:
        if mxx > 600:
            gridtop_text = "Canaries Current"
        else:
            gridtop_text = "Labrador Current"

        #print("Gridtop", gridtop, gridtop_text)
    gridtop_text_rend = font22g.render(gridtop_text, True, color_border)
    return (gridtop_text_rend,gridtop_text_rect)

          

def ship_move_drift(i,myinterval_days,grid):
    ship_list_selected = local_data.ship_list_selected  # retrieve mirror   
    drift_speed=10 # a fudge , needs some science
  ######################dsplacement due to ocean drift================
    if ship_list_selected[
            i].ship_go == True:  # this works for ships on the astar route, but what about those which have been deviated due to a weather event
        gridx1 = ship_list_selected[i].path_go[ship_list_selected[i].ship_k + 1][1]  # next
        gridy1 = ship_list_selected[i].path_go[ship_list_selected[i].ship_k + 1][0]
        gridx0 = ship_list_selected[i].path_go[ship_list_selected[i].ship_k][1]  # current
        gridy0 = ship_list_selected[i].path_go[ship_list_selected[i].ship_k][0]
    else:
        gridx1 = ship_list_selected[i].path_back[ship_list_selected[i].ship_k + 1][1]
        gridy1 = ship_list_selected[i].path_back[ship_list_selected[i].ship_k + 1][0]
        gridx0 = ship_list_selected[i].path_back[ship_list_selected[i].ship_k][1]
        gridy0 = ship_list_selected[i].path_back[ship_list_selected[i].ship_k][0]

        #odrift1 = int(grid[gridy1][gridx1])
        #if (odrift1 == 1) or (odrift1 == 2) or (odrift1 == 4):
            #print("damaged on astar route ahead")

    odrift = int(grid[gridy0][gridx0])
    if (odrift == 1) or (odrift == 2) or (odrift == 4):
        ospeed_x=0;ospeed_y=0
        #print("damaged on astar route")
    if odrift == 5:  # north south
        ospeed_x = 0
        ospeed_y = 0.1
    elif odrift == 6:  # gulf
        ospeed_x = 0.1
        ospeed_y = -0.1
    elif odrift == 7:  # west east

        ospeed_x = 0.1
        ospeed_y = 0
    elif odrift == 8:  # east west
        ospeed_x = -0.1
        ospeed_y = 0
    else:
        ospeed_x = 0.1
        ospeed_y = 0.1
# print('odrift ref,x,y', odrift, ospeed_x, ospeed_y)
# ospeed_x=0 # to switch off drift
# ospeed_y=0
    ospeedr_x = ospeed_x * drift_speed*myinterval_days
    ospeedr_y = ospeed_y * drift_speed*myinterval_days
    #print('1251 i ospeed_x,y', i, ship_list_selected[i].ship_name,ospeedr_x, ospeedr_y)
    return(ospeedr_x,ospeedr_y)

def ship_move_wind(i,mytotal_time_months,mytotal_time_days_res,myinterval_days,weather_events_list,mmax, insurers_list,hazard):
#############Consequences of proximity to weather event#####################
############### in fogs and storms navigation is very limited. Compas works but astrolabe does not since there is no sun or stars####
### ability of ship to chose a route whilst being tossed about in a storm is limited ###############
####### in iceberg seas ship will be navigating between iceberg risks ################
    #print("1101 len weather list", len(weather_events_list))
    ship_list_selected = local_data.ship_list_selected  # retrieve mirror
    wind_mag=local_data.wind_mag # magnify wind effects
    weather_disp_fract = 0.01  # fudge - needs some science
    weather_state=False
    for iw in range(0,len(weather_events_list)):
        #print("1139 event type",i,weather_events_list[iw].event_type)
        if weather_events_list[iw].exists==True:
            
            #print("1142 event type exists",weather_events_list[iw].event_type)
            v1=pygame.math.Vector2(ship_list_selected[i].ship_x,ship_list_selected[i].ship_y)
            v2=pygame.math.Vector2(weather_events_list[iw].event_x,weather_events_list[iw].event_y)
            v3=v2-v1
            distance=v3.magnitude()
            fract_event_radius=1
            
            dist_x=ship_list_selected[i].ship_x-weather_events_list[iw].event_x
            dist_y=ship_list_selected[i].ship_y-weather_events_list[iw].event_y
            angle_to_event=math.atan2(dist_y,dist_x)*180/math.pi
            
            if weather_events_list[iw].event_radius>0 and distance<weather_events_list[iw].event_radius:
                fract_event_radius=abs((weather_events_list[iw].event_radius-distance)/weather_events_list[iw].event_radius)
                wind_speed=(weather_events_list[iw].wind_speed_max-weather_events_list[iw].wind_speed_min)*fract_event_radius
                
                if fract_event_radius<1: # ships is within weather event
                    #print ("1158 within weather event ",weather_events_list[iw].event_type)
                    weather_state=True
                    if (weather_events_list[iw].event_type[0:3] == 'Fog'):
                        if distance < weather_events_list[iw].event_radius:
                            if (weather_events_list[iw].event_type[len(weather_events_list[iw].event_type) - 1] == 'E'):
                                ship_list_selected[i].ship_infoge = True
                        else:
                            ship_list_selected[i].ship_infogw = True
                        
                        ship_list_selected[i].ship_speed_cond = 0
                        ship_list_selected[i].weather_disp_x = 0
                        ship_list_selected[i].weather_disp_y = 0
                        ship_list_selected[i].marker_radius = 10
                        #append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + ship_list_selected[i].hull_condition + " "+str(
                        #round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
                        #append_if(i, append_text, mytotal_time_months, mytotal_time_days_res, time_stamp=True)
                        append_text = 'encounters Fog - ship speed ' + str(round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
                        #print(append_text)
                        append_if(i, append_text,mytotal_time_months,mytotal_time_days_res,time_stamp=True)
                        damage_text="Fog"
                        damage_random_sub(i,iw,damage_text, mytotal_time_months, mytotal_time_days_res,weather_events_list,ship_list_selected,mmax,insurers_list)
                    else:
                        if (weather_events_list[iw].event_type[len(weather_events_list[iw].event_type) - 1] == 'E'):
                            ship_list_selected[i].ship_infoge = False
                        else:
                            ship_list_selected[i].ship_infogw = False

                    if (weather_events_list[iw].event_type[0:3] == 'Sto'):
                        #print("1153 about storms",weather_events_list[iw].event_radius,"distance",distance)
                        if distance < weather_events_list[iw].event_radius:
                            #print("1155 in storms")
                            if (weather_events_list[iw].event_type[len(weather_events_list[iw].event_type) - 1] == 'E'):
                                ship_list_selected[i].ship_instorme = True
                            else:
                                ship_list_selected[i].ship_instormw = True
                            append_text = "encounters Storms"
                            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)

                            ship_list_selected[i].ship_speed_cond = 0.5 * ship_list_selected[i].ship_speed_pix / 8
                            ship_list_selected[i].marker_radius = 10
                            ship_list_selected[i].weather_disp_x = -wind_mag*weather_disp_fract * myinterval_days * (
                            wind_speed * 24 * math.sin(angle_to_event * math.pi / 180)) * (
                                                            1 - fract_event_radius)

                            ship_list_selected[i].weather_disp_y = wind_mag*weather_disp_fract * myinterval_days * (wind_speed * 24 * math.cos(angle_to_event * math.pi / 180)) * (
                                                            1 - fract_event_radius)
                            
                            
                            #if i==0:
                                #print("1179",ship_list_selected[i].ship_name," v1",v1,"v2",v2,"v3",v3,"angle by atan",round(angle_to_event,3),"fract event radius",round(fract_event_radius,3),"wind speed",wind_speed," disp_x",round(ship_list_selected[i].weather_disp_x,3), "disp_y",round(ship_list_selected[i].weather_disp_y,3))
                            damage_text="Storm"
                            damage_random_sub(i, iw, damage_text, mytotal_time_months, mytotal_time_days_res,weather_events_list,ship_list_selected,mmax,insurers_list)
                        else:
                            if (weather_events_list[iw].event_type[len(weather_events_list[iw].event_type) - 1] == 'E'):
                                    ship_list_selected[i].ship_instorme = False
                            else:
                                ship_list_selected[i].ship_instormw = False

                    if (weather_events_list[iw].event_type[0:3] == 'Hur'):
                        if distance < weather_events_list[iw].event_radius:
                            if (weather_events_list[iw].event_type[len(weather_events_list[iw].event_type) - 1] == 'E'):
                                ship_list_selected[i].ship_inhurricanee = True
                            else:
                                ship_list_selected[i].ship_inhurricanew = True
                            append_text = "encounters Hurricane"
                            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)

                            ship_list_selected[i].ship_speed_cond = 0.4 * ship_list_selected[i].ship_speed_pix / 8
                            ship_list_selected[i].marker_radius = 10
                            ship_list_selected[i].weather_disp_x = -wind_mag*weather_disp_fract * myinterval_days * (
                            wind_speed * 24 * math.sin(angle_to_event * math.pi / 180)) * (
                                                            1 - fract_event_radius)

                            ship_list_selected[i].weather_disp_y = wind_mag*weather_disp_fract * myinterval_days * (
                            wind_speed * 24 * math.cos(angle_to_event * math.pi / 180)) * (
                                                            1 - fract_event_radius)
                            ship_list_selected[i].marker_radius = 10
                            append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + ship_list_selected[i].hull_condition + " " + str(round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
                            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res, time_stamp=True)
                            damage_text = "Hurricane"
                            damage_random_sub(i, iw, damage_text, mytotal_time_months, mytotal_time_days_res,weather_events_list,ship_list_selected,mmax,insurers_list)
                        else:
                            if (weather_events_list[iw].event_type[len(weather_events_list[iw].event_type) - 1] == 'E'):
                                ship_list_selected[i].ship_inhurricanee = False
                            else:
                                ship_list_selected[i].ship_inhurricanew = False

                    if (weather_events_list[iw].event_type == 'Icebergs'):
                        if distance < weather_events_list[iw].event_radius:
                            ship_list_selected[i].ship_inicebergs = True
                            append_text = "encounters Icebergs - ship speed" +str(round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
                
                            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
                            ship_list_selected[i].ship_speed_cond = 0.3 * ship_list_selected[i].ship_speed_pix / 8
                            ship_list_selected[i].ship_inicebergs = False
                            ship_list_selected[i].marker_radius = 10
                            ship_list_selected[i].weather_disp_x = 0
                            ship_list_selected[i].weather_disp_y = 0
                            append_text = "encounters Icebergs - ship speed" +str(round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
                
                            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
                            #append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + ship_list_selected[i].hull_condition + " "+str(round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
                            #append_if(i, append_text, mytotal_time_months, mytotal_time_days_res, time_stamp=True)
                            damage_text = "Icebergs"
                            damage_random_sub(i, iw, damage_text, mytotal_time_months, mytotal_time_days_res,
                                    weather_events_list, ship_list_selected, mmax, insurers_list)
                    else:
                        ship_list_selected[i].ship_inicebergs = False

                    if (weather_events_list[iw].event_type[0:3] == 'Pir'):
                        if distance < weather_events_list[iw].event_radius:
                                if (weather_events_list[iw].event_type[len(weather_events_list[iw].event_type) - 1] == 'E'):
                                    ship_list_selected[i].ship_inpiratese = True
                                    ship_list_selected[i].weather_disp_x = 0
                                    ship_list_selected[i].weather_disp_y = 0
                        else:
                            ship_list_selected[i].ship_piratesw = True
                            ship_list_selected[i].weather_disp_x = 0
                            ship_list_selected[i].weather_disp_y = 0
                            append_text = "encounters Pirates"
                            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
                        ship_list_selected[i].marker_radius = 10
                        damage_text = "Pirates"
                        damage_random_sub(i, iw, damage_text, mytotal_time_months, mytotal_time_days_res,weather_events_list,ship_list_selected,mmax,insurers_list)

                    else:
                        if (weather_events_list[iw].event_type[len(weather_events_list[iw].event_type) - 1] == 'E'):

                            ship_list_selected[i].ship_inpiratese = False
                        else:
                            ship_list_selected[i].ship_piratesw = False

                    if ((ship_list_selected[i].ship_inpiratese == False) and (
                        ship_list_selected[i].ship_inpiratesw == False) and (
                        ship_list_selected[i].ship_infoge == False) and (
                        ship_list_selected[i].ship_infogw == False) and (
                        ship_list_selected[i].ship_instorme == False) and (
                        ship_list_selected[i].ship_instormw == False) and (
                        ship_list_selected[i].ship_inhurricanee == False) and (
                        ship_list_selected[i].ship_inhurricanew == False) and (
                        ship_list_selected[i].ship_inicebergs == False)): # not affected by any weather events
                        ship_list_selected[i].weather_disp_x = 0
                        ship_list_selected[i].weather_disp_y = 0
                        #print("ship not in weather event weather_disp 0")
                    else:
                        ship_list_selected[i].ship_speed_reset(i)
                        #print("speed reset",ship_list_selected[i].ship_name,ship_list_selected[i].ship_speed_cond,ship_list_selected[i].ship_speed_pix)
                        ship_list_selected[i].marker_radius = 5

        move_wind_x= ship_list_selected[i].weather_disp_x
        move_wind_y= ship_list_selected[i].weather_disp_y
        
    
    return(move_wind_x,move_wind_y,weather_state)
        
        

def evaluate_hazards(canvas,i,grid,mytotal_time_months,mytotal_time_days_res):
 #### EVALUATE FIXED HAZARDS AT NEW POSITION              ##############################
    color_header='red'
    color_border='blue'
    w=16
    h=16
    ship_list_selected = local_data.ship_list_selected  # retrieve mirror
    gridx = round((ship_list_selected[i].ship_x - 8) / 16)  # grid squares origin are at the top left
    gridy = round((ship_list_selected[i].ship_y - 8) / 16)
    gridx_res = (ship_list_selected[i].ship_x - 8) % 16
    gridy_res = (ship_list_selected[i].ship_y - 8) % 16
    hazard_k=0
    if ship_list_selected[i].ship_go == True:  # this works for ships on the astar route, but what about those which have been deviated due to a weather event
        gridx1 = ship_list_selected[i].path_go[ship_list_selected[i].ship_k + 1][1]  # next
        gridy1 = ship_list_selected[i].path_go[ship_list_selected[i].ship_k + 1][0]
        gridx0 = ship_list_selected[i].path_go[ship_list_selected[i].ship_k][1]  # current
        gridy0 = ship_list_selected[i].path_go[ship_list_selected[i].ship_k][0]
    else:
        gridx1 = ship_list_selected[i].path_back[ship_list_selected[i].ship_k + 1][1]
        gridy1 = ship_list_selected[i].path_back[ship_list_selected[i].ship_k + 1][0]
        gridx0 = ship_list_selected[i].path_back[ship_list_selected[i].ship_k][1]
        gridy0 = ship_list_selected[i].path_back[ship_list_selected[i].ship_k][0]

    if abs(gridx-gridx0)>4 or abs(gridx-gridx1)>4 or abs(gridy-gridy0)>4 or abs(gridy-gridy1)>4:
        print('1290 DEVIATION ERROR',ship_list_selected[i].ship_name,' gridx', gridx,'grid_y', gridy, 'gridx0', gridx0,'gridy0', gridy0,'gridx1',gridx1,'gridy1',gridy1)
    if gridx<0: gridx=0
    if gridx>80: gridx=80
    if gridy<0: gridy=0
    if gridy>59: gridy=59
    #print("1198 gridx,y",gridx,gridy)
    pygame.draw.rect(canvas, color_header, (gridx * 16, gridy * 16, w, h), 1)
    pygame.draw.rect(canvas, color_border, (gridx0 * 16, gridy0 * 16, w, h), 1)
    hazard_sq = int(grid[gridy][gridx])

    if ship_list_selected[i].ship_k != 0:
        if hazard_sq == 1:
            append_text = ("encountered beach at coordinates " + str(
                10 * round(ship_list_selected[i].ship_x / 10)) + ":" + str(
                10 * round(ship_list_selected[i].ship_y / 10)))
            #print("append text",ship_list_selected[i].ship_name,append_text)
            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
        if hazard_sq == 2:
            append_text = ("encountered rocks at coordinates " + str(
                10 * round(ship_list_selected[i].ship_x / 10)) + ":" + str(
                10 * round(ship_list_selected[i].ship_y / 10)))
            #print("append text",ship_list_selected[i].ship_name,append_text)
            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
            
        if hazard_sq == 4:
            append_text = ("encountered land at coordinates " + str(
                10 * round(ship_list_selected[i].ship_x / 10)) + ":" + str(
                10 * round(ship_list_selected[i].ship_y / 10)))
            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
            #print("append text",ship_list_selected[i].ship_name,append_text)
        hazard_k_last=hazard_k
    if ((hazard_sq==1) or (hazard_sq==2) or (hazard_sq==4)) and ship_list_selected[i].ship_k != 0:
        hazard_k=ship_list_selected[i].ship_k
        if hazard_k !=hazard_k_last:
     # 1 beach, 2 rocks, 3 land
            if hazard_sq == 1:
                hazard_text="beaching"
                ship_condition="Hull"
                beaching_damage_increment=20
                append_text = ("ship damaged at " + str(10 * round(ship_list_selected[i].ship_x / 10)) + ":" + str(
                    10 * round(ship_list_selected[i].ship_y / 10)) + " due to " + hazard_text)  # rounds to nearest 10
                appendx=append_if(i, append_text, mytotal_time_months, mytotal_time_days_res, time_stamp=True)
                #print("append text",ship_list_selected[i].ship_name,append_text)
                append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + \
                ship_list_selected[i].hull_condition + " knots " + str(
                round(ship_list_selected[i].ship_speed_cond, 1))
                appendy=append_if(i, append_text, mytotal_time_months, mytotal_time_days_res, time_stamp=False)
                if appendx==True and appendy==True:
                    ship_list_selected[i].ship_damage_accum = ship_list_selected[
                                                            i].ship_damage_accum + beaching_damage_increment
                    degrade_condition(i, ship_list_selected, ship_condition)
                    ship_list_selected[i].ship_speed_reset(i)  # to modify speed in accordance with new ship condition

            if hazard_sq == 2:
                hazard_text="rocks"
                ship_condition = "Hull"
                rocks_damage_increment = 100
                append_text = (
                            "ship damaged at " + str(10 * round(ship_list_selected[i].ship_x / 10)) + ":" + str(
                        10 * round(ship_list_selected[
                                    i].ship_y / 10)) + " due to " + hazard_text)  # rounds to nearest 10
                appendx=append_if(i, append_text, mytotal_time_months, mytotal_time_days_res, time_stamp=False)
                append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + \
                            ship_list_selected[i].hull_condition + " knots " + str(
                    round(ship_list_selected[i].ship_speed_cond, 1))
                appendy = append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,
                                    time_stamp=False)

                if appendx==True and appendy==True:
                    degrade_condition(i, ship_list_selected, ship_condition)
                    ship_list_selected[i].ship_damage_accum = ship_list_selected[
                                                                i].ship_damage_accum + rocks_damage_increment

                    ship_list_selected[i].ship_speed_reset(i)  # to modify speed in accordance with new ship condition
        if hazard_sq == 4:
                hazard_text="land"
                ship_condition = "Hull"
                degrade_condition(i, ship_list_selected, ship_condition)
                rocks_damage_increment = 20
                ship_list_selected[i].ship_damage_accum = ship_list_selected[
                                                            i].ship_damage_accum + rocks_damage_increment
                appendx = append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,
                                    time_stamp=False)
                append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + \
                            ship_list_selected[i].hull_condition + " knots " + str(
                    round(ship_list_selected[i].ship_speed_cond, 1))
                appendy = append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,
                                    time_stamp=False)

                if appendx == True and appendy == True:
                    ship_list_selected[i].ship_damage_accum = ship_list_selected[
                                                                i].ship_damage_accum + rocks_damage_increment
                    degrade_condition(i, ship_list_selected, ship_condition)
                    ship_list_selected[i].ship_speed_reset(
                        i)  # to modify speed in accordance with new ship condition
                #print("hazard damage", ship_list_selected[i].ship_name, ship_list_selected[i].ship_damage_accum)
    return( hazard_sq)


def ship_log_display(canvas,ship_log):  ### for part 2 aftership sails. Player clicks to display ship detail
    
    #ship_list_selected = local_data.ship_list_selected  # retrieve mirror
    #font20 = pygame.font.SysFont("Arial", 20, bold=False)
    color_wash='white'
    color_border='blue'
    ship_detail_x = 900
    ship_detail_y = 700
    ship_detail_w = 600
    ship_detail_h = 300
    
    ship_detail_rect = pygame.Rect(ship_detail_x, ship_detail_y, ship_detail_w, ship_detail_h)
    pygame.draw.rect(canvas, color_wash, ship_detail_rect)
    pygame.draw.rect(canvas, color_border, ship_detail_rect,2)
    subroutines.blit_text(canvas, ship_log, ship_detail_rect, color_border)  ### note blit_text uses a list
            
    #####################  pay annual premiums ######################
def pay_premium(i,mytotal_time_years):
    ship_list_selected = local_data.ship_list_selected  # retrieve mirror
    insurers_list=local_data.insurers_list
    mmax=local_data.mmax
    if ship_list_selected[i].ship_premium_counter!=mytotal_time_years-1 and ship_list_selected[i].ship_shipwreck==False: ### time to pay premium
        ship_list_selected[i].ship_premium_accum+=ship_list_selected[i].ship_premium
        for m in range(0, mmax):
            insurer_name = insurers_list[m].insurer_name
            if insurer_name == ship_list_selected[i].ship_insurer:
                insurers_list[m].premiums_income_accum = insurers_list[m].premiums_income_accum + ship_list_selected[i].ship_premium
                insurers_list[m].premiums_income=ship_list_selected[i].ship_premium
        ship_list_selected[i].ship_premium_counter = mytotal_time_years - 1 ### ensure payment only once per year

'''

### retained for reinstallation
############## display path for troubleshooting#####################
    
if display_all_routes==False: # display one route only
    if i==selected_ship_number:
        for k in range(0, len(ship_list_selected[i].path_go) - 1):  # display paths
            point_x = ship_list_selected[i].path_go[k][0]
            point_y = ship_list_selected[i].path_go[k][1]
            point_x1 = ship_list_selected[i].path_go[k + 1][0]
            point_y1 = ship_list_selected[i].path_go[k + 1][1]
            pygame.draw.circle(canvas, ship_color, (point_y * 16, point_x * 16), 3)
            pygame.draw.line(canvas, ship_color, (point_y * 16, point_x * 16), (point_y1 * 16, point_x1 * 16), 1)
        for k in range(0, len(ship_list_selected[i].path_back) - 1):
            point_x = ship_list_selected[i].path_back[k][0]
            point_y = ship_list_selected[i].path_back[k][1]
            point_x1 = ship_list_selected[i].path_back[k + 1][0]
            point_y1 = ship_list_selected[i].path_back[k + 1][1]
            pygame.draw.circle(canvas, ship_color, (point_y * 16, point_x * 16), 3)
            pygame.draw.line(canvas, ship_color, (point_y * 16, point_x * 16), (point_y1 * 16, point_x1 * 16), 1)
    #window.blit(canvas, (0, 0))
    #pygame.display.update()
            
 
            if display_all_routes==False:
                ishow=selected_ship_number
                for k in range(len(ship_list_selected[ishow].damage_event_list)):  # display damage events , but only for selected ship to avoid clutter
                    #print(ishow,ship_list_selected[ishow].damage_event_list)
                    #print(ship_list_selected[ishow].damage_event_list[0])
                    #print(ship_list_selected[ishow].damage_event_list[1])
                    #print(ship_list_selected[ishow].damage_event_list[0][0])
                    damage_event_text_rect = pygame.Rect(ship_list_selected[ishow].damage_event_list[k][0] + 0,
                                                   ship_list_selected[ishow].damage_event_list[k][1], 100, 25)
                    pygame.draw.rect(canvas, "light blue", damage_event_text_rect)
                    pygame.draw.circle(canvas, ship_color, (ship_list_selected[ishow].damage_event_list[k][0], ship_list_selected[ishow].damage_event_list[k][1]), 2)
                    damage_event_text = font18.render(ship_list_selected[ishow].damage_event_list[k][2], True,color_text)
                    canvas.blit(damage_event_text, damage_event_text_rect)
    
      
    


        #### display which insurer has best finances
        mbalance_max=0
        mtop=0
        for m in range (0,mmax):
            if mbalance_max<insurers_list[m].balance:
                mbalance_max=insurers_list[m].balance
                mtop=m
            #print("insurer m, m balance , mbalance_max, mtop",m,insurers_list[m].balance,mbalance_max,mtop)
        insurer_winning_string=insurers_list[mtop].insurer_name+" insurer has the best finances"
        insurer_winning_text = font22.render(insurer_winning_string, True, color_header)
        insurer_winning_text_rect = pygame.Rect(500, 100, 2 * menu_width, menu_height)
        pygame.draw.rect(canvas, "white", insurer_winning_text_rect)
        pygame.draw.rect(canvas, color_border, insurer_winning_text_rect, 2)
        canvas.blit(insurer_winning_text, insurer_winning_text_rect)






#   displacement due to weather

'''