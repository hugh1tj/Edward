import pygame
import local_data
import mytext
import subroutines
import weather_hazards
from subroutines import Insurer

import ports
import random
import astar
from spritesheet import Spritesheet
from tiles import *
import goinside
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
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    ship_detail_x=950
    ship_detail_y=500
    ship_detail_w=550
    ship_detail_h=500
    ship_detail_list=[]
    ship_detail_rect=pygame.Rect(ship_detail_x,ship_detail_y,ship_detail_w,ship_detail_h)
    ship_detail_list.append("Ship Details - for other ships click on ship name on top left")
    ship_detail_list.append("")
    ship_detail_list.append("The ship '" + str(ship_list_selected[selected_ship_number].ship_name) + "' is insured by " + str(ship_list_selected[selected_ship_number].ship_insurer)+ " at a premium of £"+str(ship_list_selected[selected_ship_number].ship_premium ))
    ship_detail_list.append("The total replacement value of this ship is estimated as £"+str(round(ship_list_selected[selected_ship_number].ship_value)))
    ship_detail_list.append(" and the cost of a significant repair as £"+str(round(ship_list_selected[selected_ship_number].ship_repair)))
    ship_detail_list.append("The ship plies between "+str(ship_list_selected[selected_ship_number].port)+ " and "+str(ship_list_selected[selected_ship_number].destination))
    go_miles=16*4* len(ship_list_selected[selected_ship_number].path_go) ### check the science
    ship_detail_list.append("Journey length is approximately "+str(go_miles) + " nautical miles.")
    ship_detail_list.append(" The total tonnage is "+str(ship_list_selected[selected_ship_number].tons) )
    ship_detail_list.append(" The age of the ship is " + str(ship_list_selected[selected_ship_number].age)+" years, and she was made in "+ str(ship_list_selected[selected_ship_number].place_of_build))
    ship_detail_list.append(" Current rig condition is rated as  " + str(ship_list_selected[selected_ship_number].rig_condition) + " and the hull condition rated as "+str(ship_list_selected[selected_ship_number].hull_condition))
    ship_detail_list.append("")
    ship_detail_list.append("BON VOYAGE !!!")
        
    
    #ship_detail_font=font20.render( ship_detail_text,True,'black')
    pygame.draw.rect(canvas, "white", ship_detail_rect)
    subroutines.blit_text(canvas,ship_detail_list,ship_detail_rect,'blue')  ### note blit_text uses a list


def ship_log_display(window, canvas,
                selected_ship_number,ship_log):  ### for part 2 aftership sails. Player clicks to display ship detail
    ship_list_selected = local_data.ship_list_selected  # retrieve mirror
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    ship_detail_x = 950
    ship_detail_y = 500
    ship_detail_w = 550
    ship_detail_h = 500
    
    ship_detail_rect = pygame.Rect(ship_detail_x, ship_detail_y, ship_detail_w, ship_detail_h)
    
    subroutines.blit_text(canvas, ship_log, ship_detail_rect, 'blue')  ### note blit_text uses a list

class Ship_Revenue(object):
        def __init__(self, x, y, w, h, text):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.text = text
            # print ("in Ship_Revenue", text)


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
                ship_list_selected[j].ship_log.append(
                    str(mytotal_time_months) + " months " + str(round(mytotal_time_days_res)) + " days ,"+ append_text)
                added=True
        elif append==True and time_stamp==False:
                ship_list_selected[j].ship_log.append(append_text)
        else:
            pass

        log_max_len=20
        if (len(ship_list_selected[j].ship_log) > log_max_len):
            ship_list_selected[j].ship_log.pop(3) # 3 fixed lines to start log
        return append
        #xnum+=1 #pygame.quit
            #pygame.time.delay(5000)

def damage_random_sub(i,iw,damage_text,mytotal_time_months, mytotal_time_days_res,weather_events_list,ship_list_selected,mmax,insurers_list): # ship i, weather event iw
    damage_random=10 # any integer
    #damage_increment=100 # may vary according to event
    damage_increment=local_data.damage_increment
    if damage_random == (random.randrange(0, weather_events_list[iw].rig_damage_risk))and ship_list_selected[i].ship_shipwreck==False:
        append_text1 = "rigging damaged in/by "+damage_text
        appendx=append_if(i, append_text1, mytotal_time_months, mytotal_time_days_res, time_stamp=True)

        ship_condition="Rigging"
        degrade_condition(i,ship_list_selected, ship_condition)
        append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + ship_list_selected[i].hull_condition + " "+ str(round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
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
        degrade_condition(i, ship_list_selected, ship_condition)
        append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + \
                      ship_list_selected[i].hull_condition +" "+ str(
            round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
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
        index=hull_conditions_list.index(prior_condition)
        if index<len(hull_conditions_list)-1:
            index+=+1
        ship_list_selected[i].hull_condition=(hull_conditions_list[index] )
    if ship_condition == "Rigging":
        rig_conditions_list = ['G','M','B']
        prior_condition = ship_list_selected[i].rig_condition
        index = rig_conditions_list.index(prior_condition)
        if index < len(rig_conditions_list)-1:
            index += 1
        ship_list_selected[i].rig_condition = (rig_conditions_list[index])

def ships_set_sail_sub(window, canvas,ship_list_me, ship_list_selected, insurers_list, from_index=1):
    #print("start ship sets sail", local_data.ship_list_selected[0].ship_name, ship_list_selected[0].ship_name,ship_list_selected[0].ship_insurer,local_data.ship_list_selected[0].ship_insurer)
    smax=local_data.smax
    ship_list_selected = local_data.ship_list_selected # retrieve mirror
    insurers_list = local_data.insurers_list # retrieve mirror
    mmax = local_data.mmax
    for m in range (0,mmax):
        insurers_list[m].insurer_update(m)
    mapwidth=1500
    mapheight=mapwidth*.75
    margin_x=0
    margin_y=0
    padding_x=2
    padding_y=0
    cell_width=100
    cell_height=25
    port_list_margin = 5
    port_list_start = 50
    port_list_width = 200
    port_list_height = 25
    w = 16 # for grid conversion
    h = 16
    insurer_finances_nested_list=[]
    insurer_finances_cell_width = 150
    insurer_finances_table_x = 5
    insurer_finances_table_y = 0
    menu_margin = 5
    menu_width = 200
    menu_height = 25
    color_bg = ('white')
    color_text = ('black')
    color_border = ('black')
    color_clickedbcg = ('grey')
    color_button=('blue')
    color_wash = "white"
    font18 = pygame.font.SysFont("Arial", 18, bold=False)
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    spritesheet = Spritesheet('spritesheet.png')

    map_map = TileMap('newmap6Sep2025.csv', spritesheet)
    grid = local_data.mapx
    # print(' map x ', local_data.mapx)
    img2 = pygame.image.load('natlantictrimmedre.png')
    img2r = pygame.transform.scale(img2, (mapwidth, mapheight))  # map of north atlantic larger scale
    canvas.blit(img2r, (margin_x, margin_y))
    map_map.draw_map(canvas)  ### use this to display drift, but not necessary for 'set sail'
    ###   constants to do with ship travel and weather

    
    angle_haz = 0  # for evasive action
    angle_avoid = 40
    distortion_factor = 1 # adjusted later for map distorition
    drift_speed = 0.1 # ocean drift master value - a bit of a fudge try to quantify
    weather_disp_fract = 0.01  # fudge - needs some science
    wind_speed_min = 24  # knots for windy events only
    #hazard_counter_max = 5
    convert_pixel = 16
    weather_sep = 0  # separates weater events
    game_speed_conv = 5000  # 25714 milliseconds game time equals one day of ship travel
    alimit = 1
    hazard_k=0 # used to ensure that only one set of damage incurred per grid square
    damage_increment = 100
    display_slist = False
    toggle_ship_insurer_button_clicked = False
    display_all_routes=True # for ship display , all routes or one set by ship log selected
    ### Display Calculating which is then overwritten by set sail
    set_sail_button_clicked = False
    set_sail_button_start_x = 5
    premiums_to_be_set_text=font22.render("  You need to negotiate premiums first !!!", True, 'red')
    set_sail_button_text = font22.render("Calculating Shortest Routes - please wait!!!", True, 'red')
    set_sail_button_text_rect = pygame.Rect(600, 400, 2.5 * menu_width, menu_height)
    pygame.draw.rect(canvas, "white", set_sail_button_text_rect)
    pygame.draw.rect(canvas, color_border, set_sail_button_text_rect, 2)
    premiums_set=False
    #print("insurer 0 ships insured list",insurers_list[0].ships_insured_list,"len",len(insurers_list[0].ships_insured_list))
    if len(insurers_list[0].ships_insured_list)>1:
        premiums_set=True
        canvas.blit(set_sail_button_text, set_sail_button_text_rect)
    else:
        premiums_set=False
        canvas.blit(premiums_to_be_set_text, set_sail_button_text_rect)
    ### Create ship log show buttons
    
    #Shiplog_Button.ship_log_button_display(window, canvas, ship_log_buttons_y=100)
    buttonstart_x = 5
    buttonstart_y = 0
    buttonheight = cell_height
    buttonwidth = 250
    button_names=[]
    button_names.append(["Ships Listed by Insurer",1],)
    button_names.append([" Click on Ship for Ship Data",1],)
    #print ("mmax",mmax,"smax",smax)
    #print("285 ship sets sail", local_data.ship_list_selected[0].ship_name, ship_list_selected[0].ship_name,ship_list_selected[0].ship_insurer )
    for m in range (0,mmax):
        insurer_name=insurers_list[m].insurer_name
        insurer_text_raw=" Insurer: "+ insurer_name
        button_names.append([insurer_text_raw,1],)
        for sj in range(0,smax):
            #print("ship list selected ship insurer",ship_list_selected[sj].ship_insurer)
            if insurer_name==ship_list_selected[sj].ship_insurer:
                button_text_1_raw = "  Ship Name:  " + ship_list_selected[sj].ship_name
                button_names.append([button_text_1_raw,0])
                button_text_2_raw = "      " + ship_list_selected[sj].port+ " to "+ship_list_selected[sj].destination
                button_names.append([button_text_2_raw, 2])
    button = []
    buttontext_rect = []
    #############display buttons########################
    button_numb = len(button_names)
    for i in range(button_numb):
        button.append(
            subroutines.Button(buttonstart_x, buttonstart_y+i * buttonheight, buttonwidth, buttonheight,
                               button_names[i][0],
                               button_names[i][1], "False"))
        
    for i in range(button_numb):
        if button[i].rect_color == 1:
            buttontext_rect.append(
                subroutines.Button.button_rect_blit(button[i], canvas, color_border, color_text, color_wash))
        elif button[i].rect_color == 0:
            buttontext_rect.append(
                subroutines.Button.button_rect_blit(button[i], canvas, color_button, color_text, color_wash))
        else: # 2
            buttontext_rect.append(
                subroutines.Button.button_rect_blit(button[i], canvas, color_bg, color_text, color_wash))
    for i in range(button_numb):  # draw coloured circles
        for sj in range(0, smax):
            if ship_list_selected[sj].ship_name in button_names[i][0]:
                # print("found",ship_list_selected[sj].ship_name, button_names[i][0])
                ship_color = local_data.list_colors[sj]
                pygame.draw.circle(canvas, ship_color, (buttonstart_x + 200, buttonstart_y + i * buttonheight + 10), 8)
                
    ### Instantiate Weather Events ################################
    weather_events_list_len = (len(local_data.weather_events_list))  # instatiates all possible weather events
    weather_events_list = []

    for iw in range(len(local_data.weather_events_list)):
        weather_events_list.append(subroutines.Weather_event(iw))  # instantiates for all types of weather event


    ### display dots for ports and destinations########################
    for i in range(0,smax):
        ship_color = local_data.list_colors[i]

        ports_tuple = ship_list_selected[i].get_port(i)  # gets the x,y coordinates of the originating port
        #print ('ports_tuple', ports_tuple)
        #print('ports tuple',ship_list_selected[i].ports_tuple)
        ship_list_selected[i].ship_x_last=ship_list_selected[i].port_x # sets the initial conditions
        ship_list_selected[i].ship_y_last=ship_list_selected[i].port_y
        #ship_list_selected[i].wp_number = 0
        ship_list_selected[i].port_delay=i*2 # staggers departure of ships
        #print(ship_list_selected[i].ship_name, ship_list_selected[i].ports_tuple)
        pygame.draw.circle(canvas, 'blue', (ship_list_selected[i].ports_tuple[0]+margin_x, ship_list_selected[i].ports_tuple[1]+margin_y),
                           10)
        pygame.draw.circle(canvas, 'red', (ship_list_selected[i].ports_tuple[2]+margin_x, ship_list_selected[i].ports_tuple[3]+margin_y),
                           10)

        for k in range(0, len(ship_list_selected[i].path_go)-1):   # display paths
                #print("path go",ship_list_selected[i].path_go[k])
            point_x = ship_list_selected[i].path_go[k][0]
            point_y = ship_list_selected[i].path_go[k][1]
            point_x1=ship_list_selected[i].path_go[k+1][0]
            point_y1=ship_list_selected[i].path_go[k+1][1]
            pygame.draw.circle(canvas, ship_color, (point_y * 16, point_x * 16), 3)
            pygame.draw.line(canvas,ship_color,(point_y * 16, point_x * 16),(point_y1 * 16, point_x1 * 16), 1)
        for k in range(0, len(ship_list_selected[i].path_back)-1):
            point_x = ship_list_selected[i].path_back[k][0]
            point_y = ship_list_selected[i].path_back[k][1]
            point_x1 = ship_list_selected[i].path_back[k + 1][0]
            point_y1 = ship_list_selected[i].path_back[k + 1][1]
            pygame.draw.circle(canvas, ship_color, (point_y * 16, point_x * 16), 3)
            pygame.draw.line(canvas, ship_color, (point_y * 16, point_x * 16), (point_y1 * 16, point_x1 * 16), 1)

        window.blit(canvas, (0, 0))
        pygame.display.update()
    ###
    set_sail_button_clicked = False
    set_sail_button_start_x = 5
    if premiums_set==True:
        set_sail_button_text = font22.render("Click to Set Sail   !!!", True, 'red')
    else:
        set_sail_button_text = font22.render("Click to Return to Coffee Shop and negotiate premiums !!!", True, 'red')
    
    pygame.draw.rect(canvas, "white", set_sail_button_text_rect)
    pygame.draw.rect(canvas, color_border, set_sail_button_text_rect, 2)
    canvas.blit(set_sail_button_text, set_sail_button_text_rect)
    ship_detail(window, canvas, 1)  # default
    window.blit(canvas, (0, 0))
    pygame.display.update()
    set_sail_waiting=True
    while set_sail_waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                set_sail_waiting = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                for i in range(0, len(button_names)):  
                    button[i].clicked = True if buttontext_rect[i].collidepoint(event.pos) else False
                    if button[i].clicked == True:
                        for xl in range(button_numb):
                            for sj in range(0, smax):
                                if ship_list_selected[sj].ship_name in button_names[i][0]:
                                    selected_ship_number=sj
                                    ship_detail(window,canvas,selected_ship_number)
                    
                        
                window.blit(canvas, (0, 0))
                pygame.display.update()
                if set_sail_button_text_rect.collidepoint(event.pos) == True and premiums_set==True:
                    set_sail_waiting=False
                elif premiums_set==True:
                    set_sail_waiting=True
                else:
                    goinside.goinside_sub(window,canvas,from_key=1)
    ######## PART 2 - WHEN SET SAIL IS CLICKED....################################################################
    ### time handling
    
    mystarttime = pygame.time.get_ticks()
    mytime_last = mystarttime
    mytotal_time_years_last=-1 # to force paying premium when year =0
    selected_ship_number=0
    display_drift=True
    ship_log=[]
    running = True
    canvas_drift=canvas
    while running:
        # if from_index==1: # from goinside
        canvas.blit(img2r, (0, 0))  # blit map first each and every time otherwise weather events and ships blur tracking
        map_map.draw_map(canvas_drift)  # imports and displays sprites (from Tiles)
        if display_drift==True:
            map_map.draw_map(canvas_drift)



            mx, my = pygame.mouse.get_pos()
            #print ("mouse position",mx,my)

            if mx>1300:
                mxx=1300
            else:
                mxx=mx
            if my>950:
                myy=950
            else:
                myy=my
            mx_tile = int(mxx / 16)
            my_tile = int(myy / 16)
            gridtop = int(grid[my_tile][mx_tile])
                # print("gridtop", gridtop)
            gridtop_text_rect = pygame.Rect(mxx + 20, my, port_list_width,
                                                port_list_height)
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
            gridtop_text_rend = font22.render(gridtop_text, True, color_border)
            canvas_drift.blit(gridtop_text_rend, gridtop_text_rect)
            window.blit(canvas_drift, (0, 0))
                # pygame.display.flip()

        else:
            window.blit(canvas, (0, 0))
            grid = local_data.mapx
        window.blit(canvas, (0, 0))
        ### TIME HANDLING ###
        mytime = pygame.time.get_ticks()
        mytotal_time = mytime - mystarttime
        myinterval = mytime - mytime_last  # as play milliseconds
        myinterval_days = myinterval / game_speed_conv
        # print ('mytintervaldays start',myinterval_days)
        mytotal_time_days = mytotal_time / game_speed_conv
        mytotal_time_months = int(mytotal_time_days / 30)
        mytotal_time_years = int(mytotal_time_months / 12)
        mytotal_time_months_res = mytotal_time_months - mytotal_time_years * 12
        mytotal_time_days_res = mytotal_time_days - mytotal_time_months * 30
        mytotal_time_years_res = mytotal_time_months - mytotal_time_years * 12
        journey_time_text_rect = pygame.Rect(1100, 10, 350, 40)
        pygame.draw.rect(canvas, 'white', journey_time_text_rect)  # avoid over writing previous entry
        
        journey_time_text = font22.render("Time:  "+str(mytotal_time_years) + " years" +
                                          "  " + str(mytotal_time_months_res) + " months " + str(
            round(mytotal_time_days_res, 1)) + " days ", True,
                                          color_text)
        pygame.draw.rect(canvas, color_border, journey_time_text_rect, 2)  # avoid over writing previous entry
        canvas.blit(journey_time_text, journey_time_text_rect)

        ### return to coffee ship menu
        coffee_menu_button_text = font22.render("Coffee Shop Menu", True, color_border)
        coffee_menu_button_clicked = False
        coffee_menu_button_start_x=5
        coffee_menu_button_text_rect = pygame.Rect(menu_margin, 800, 3 * cell_width, cell_height)
        pygame.draw.rect(canvas, "white", coffee_menu_button_text_rect)
        pygame.draw.rect(canvas, color_border, coffee_menu_button_text_rect, 2)
        canvas.blit(coffee_menu_button_text, coffee_menu_button_text_rect)
        
        ### toggle switch for ship insurer list on or off
        toggle_ship_insurer_list_text = font22.render("Toggle List Ships Financial Statement On/Off", True, color_border)
        toggle_ship_insurer_list_text_rect = pygame.Rect(5, 850,4 * cell_width, cell_height )
        toggle_ship_insurer_button=False
        pygame.draw.rect(canvas, "white", toggle_ship_insurer_list_text_rect )
        pygame.draw.rect(canvas, color_border,toggle_ship_insurer_list_text_rect  , 2)
        canvas.blit(toggle_ship_insurer_list_text, toggle_ship_insurer_list_text_rect)

        ### toggle switch for drift map
        toggle_drift_map_text = font22.render("Toggle List of Coloured Drift Map On/Off", True, color_border)
        toggle_drift_map_text_rect = pygame.Rect(5, 900, 4 * cell_width, cell_height)
        toggle_drift_map_button = False
        pygame.draw.rect(canvas, "white", toggle_drift_map_text_rect)
        pygame.draw.rect(canvas, color_border, toggle_drift_map_text_rect, 2)
        canvas.blit(toggle_drift_map_text, toggle_drift_map_text_rect)

        ### toggle switch for routes display
        toggle_routes_display_text = font22.render("Toggle Routes Display - All/Selected", True, color_border)
        toggle_routes_display_text_rect = pygame.Rect(5, 950, 4 * cell_width, cell_height)
        toggle_routes_display_button = False
        pygame.draw.rect(canvas, "white", toggle_routes_display_text_rect)
        pygame.draw.rect(canvas, color_border, toggle_routes_display_text_rect, 2)
        canvas.blit(toggle_routes_display_text, toggle_routes_display_text_rect)


        ### Ship info and log buttons
        ### clear ship log display space
        ship_detail_x = 950
        ship_detail_y = 500
        ship_detail_w = 550
        ship_detail_h = 500
        ship_detail_rect = pygame.Rect(ship_detail_x, ship_detail_y, ship_detail_w, ship_detail_h)
        
        pygame.draw.rect(canvas, "white", ship_detail_rect)
        ###############create buttons
        buttonstart_x = 5
        buttonstart_y = 0
        buttonheight = 22
        buttonwidth = 250
        button_names = []
        button_names.append(["Ships Listed by Insurer", 1], )
        button_names.append([" Click on Ship for Ship Log", 1], )
        mmax=3
        for m in range(0, mmax):
            insurer_name = insurers_list[m].insurer_name
            insurer_text_raw = " Insurer: " + insurer_name
            button_names.append([insurer_text_raw, 1], )
            for sj in range(0, smax):
                #print("in ships listed by insurer mmax,smax time,insurer name, ship_insurer",mmax,smax, mytotal_time_months,insurer_name,ship_list_selected[sj].ship_insurer,ship_list_selected[sj].ship_name)
                if insurer_name == ship_list_selected[sj].ship_insurer:
                    button_text_1_raw = "  Ship Name:  " + ship_list_selected[sj].ship_name
                    button_names.append([button_text_1_raw, 0])
                    button_text_2_raw = "      " + ship_list_selected[sj].port + " to " + ship_list_selected[
                        sj].destination
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
                    subroutines.Button.button_rect_blit(button[i], canvas, color_border, color_text, color_wash))
            elif button[i].rect_color == 0:
                buttontext_rect.append(
                    subroutines.Button.button_rect_blit(button[i], canvas, color_button, color_text, color_wash))
            else:  # 2
                buttontext_rect.append(
                    subroutines.Button.button_rect_blit(button[i], canvas, color_bg, color_text, color_wash))
        for i in range(button_numb):
            for sj in range(0, smax):
                if ship_list_selected[sj].ship_name in button_names[i][0]:

                    ship_color = local_data.list_colors[sj]
                    pygame.draw.circle(canvas, ship_color, (buttonstart_x + 200, buttonstart_y + i * buttonheight + 10),
                                       8)
        ###  DEVELOP WEATHER EVENTS #######################################################################
        for iw in range(len(weather_events_list)):
            if mytotal_time_months >= weather_events_list[iw].month_start and mytotal_time_months_res <= \
                    weather_events_list[iw].month_end:  # event is in season

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
                # print ("myinterval days",myinterval_days, iw)
                position_tuple = weather_events_list[iw].drift_event(myinterval_days, iw)
                # print('position and wind speed ', position_tuple)
                weather_events_list[iw].event_x = position_tuple[0]
                weather_events_list[iw].event_y = position_tuple[1]
                # weather_events_list[iw].wind_speed_max= position_tuple[2]
                weather_events_list[iw].wind_speed = position_tuple[2]

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
                    pygame.draw.circle(canvas, 'blue',
                                       (weather_events_list[iw].event_x, weather_events_list[iw].event_y),
                                       weather_events_list[iw].starting_event_radius, width=4)

                weather_event_text_rect = pygame.Rect(weather_events_list[iw].event_x + 0,
                                                      weather_events_list[iw].event_y - 0, 100, 50)
                weather_event_text = font20.render(
                    (weather_events_list[iw].event_type[:len(weather_events_list[iw].event_type) - 2]), True,
                    color_text)
                canvas.blit(weather_event_text, weather_event_text_rect)

                                
        ### SHIPS)

        ### display log
        ship_list_selected[selected_ship_number].ship_log_update(selected_ship_number) # nucessary to load premium
        ship_log_display(window, canvas, selected_ship_number, ship_list_selected[selected_ship_number].ship_log)
        ### SHIP ROUTE
        
        ### START EXTENSIVE LOOP OF ALL SHIPS [I]###############
        for i in range(0,smax):
            ship_color = local_data.list_colors[i]




            #####################  pay annual premiums ######################
            if ship_list_selected[i].ship_premium_counter!=mytotal_time_years-1 and ship_list_selected[i].ship_shipwreck==False: ### time to pay premium
                ship_list_selected[i].ship_premium_accum+=ship_list_selected[i].ship_premium
                for m in range(0, mmax):
                    insurer_name = insurers_list[m].insurer_name
                    if insurer_name == ship_list_selected[i].ship_insurer:
                        insurers_list[m].premiums_income_accum = insurers_list[m].premiums_income_accum + ship_list_selected[i].ship_premium
                        insurers_list[m].premiums_income=ship_list_selected[i].ship_premium
            ship_list_selected[i].ship_premium_counter = mytotal_time_years - 1 ### ensure payment only once per year

            ## ship imagary is centralised within each grid, whose x,y is 0,0. add 8 pixels to centralise within the 16 x 16 grid square
            if ship_list_selected[i].ship_go == True:
                wp_last_x = 8 + ship_list_selected[i].path_go[ship_list_selected[i].ship_k][1] * convert_pixel  # as pixels
                wp_last_y = 8 + ship_list_selected[i].path_go[ship_list_selected[i].ship_k][0] * convert_pixel  # as pixels
                wp_next_x = 8 + ship_list_selected[i].path_go[ship_list_selected[i].ship_k + 1][
                    1] * convert_pixel  # as pixels
                wp_next_y = 8 + ship_list_selected[i].path_go[ship_list_selected[i].ship_k + 1][0] * convert_pixel
            else:
                if ship_list_selected[i].ship_k == 0:
                    ship_list_selected[i].ship_depart_time = mytotal_time
                # print(' depart time from destination', ship_list_selected[i].ship_name, ship_list_selected[i].ship_depart_time)
                wp_last_x = 8 + ship_list_selected[i].path_back[ship_list_selected[i].ship_k][
                    1] * convert_pixel  # as pixels
                wp_last_y = 8 + ship_list_selected[i].path_back[ship_list_selected[i].ship_k][
                    0] * convert_pixel  # as pixels
                wp_next_x = 8 + ship_list_selected[i].path_back[ship_list_selected[i].ship_k + 1][
                    1] * convert_pixel  # as pixels
                wp_next_y = 8 + ship_list_selected[i].path_back[ship_list_selected[i].ship_k + 1][0] * convert_pixel
        #print (ship_list_selected[i].ship_name,'i',i,'k',ship_list_selected[i].ship_k, 'wp_last/next' ,wp_last_x,wp_last_y, wp_next_x,wp_next_y)
            ship_list_selected[i].ship_weather_affected = False
            for iw in range(len(weather_events_list)):
                if weather_events_list[iw].exists == True:
                    dist_x = ship_list_selected[i].ship_x - weather_events_list[iw].event_x
                    dist_y = ship_list_selected[i].ship_y - weather_events_list[iw].event_y

                    distance = math.sqrt(dist_x ** 2 + dist_y ** 2)
                ################find extent to which within weather event circle and weather displacement###################
                    angle_to_event = math.atan2(dist_y, dist_x) * 180 / math.pi  # as degrees
                    fract_event_radius = distance / weather_events_list[iw].event_radius
                    wind_speed_fract = 1 - (
                            dist_x / (weather_events_list[iw].event_radius * math.cos(angle_to_event * math.pi / 180)))

                    if fract_event_radius < 1:  # ship within radius of event

                        wind_speed = wind_speed_min + (
                                weather_events_list[iw].wind_speed_max - wind_speed_min) * fract_event_radius

                        ship_list_selected[i].weather_disp_x = -weather_disp_fract * myinterval_days * (
                                    wind_speed * 24 * math.sin(angle_to_event * math.pi / 180)) * (1 - fract_event_radius)

                        ship_list_selected[i].weather_disp_y = weather_disp_fract * myinterval_days * (
                                wind_speed * 24 * math.cos(angle_to_event * math.pi / 180)) * (1 - fract_event_radius)
                    # print("weather disp x,y", weather_disp_x,  weather_disp_y)
                    else:
                        pass
                    # ship_list_selected[i].weather_disp_x=0
                    # ship_list_selected[i].weather_disp_y=0
                #############Consequences of proximity to weather event#####################
                ############### in fogs and storms navigation is very limited. Compas works but astrolabe does not since there is no sun or stars####
                ### ability of ship to chose a route whilst being tossed about in a storm is limited ###############
                ####### in iceberg seas ship will be navigating between iceberg risks ################
                    wind_mag=local_data.wind_mag # magnify wind effects
                    if (weather_events_list[iw].event_type[0:3] == 'Fog'):
                        if distance < weather_events_list[iw].event_radius:
                            if (weather_events_list[iw].event_type[len(weather_events_list[iw].event_type) - 1] == 'E'):
                                ship_list_selected[i].ship_infoge = True
                            else:
                                ship_list_selected[i].ship_infogw = True
                            append_text = 'encounters Fog'
                            #print(append_text)
                            append_if(i, append_text,mytotal_time_months,mytotal_time_days_res,time_stamp=True)
                            ship_list_selected[i].ship_speed_cond = 0
                            ship_list_selected[i].weather_disp_x = 0
                            ship_list_selected[i].weather_disp_y = 0
                            ship_list_selected[i].marker_radius = 10
                            #append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + ship_list_selected[i].hull_condition + " "+str(
                                #round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
                            #append_if(i, append_text, mytotal_time_months, mytotal_time_days_res, time_stamp=True)

                            damage_text="Fog"
                            damage_random_sub(i,iw,damage_text, mytotal_time_months, mytotal_time_days_res,weather_events_list,ship_list_selected,mmax,insurers_list)
                        else:
                            if (weather_events_list[iw].event_type[len(weather_events_list[iw].event_type) - 1] == 'E'):
                                ship_list_selected[i].ship_infoge = False
                            else:
                               ship_list_selected[i].ship_infogw = False

                    if (weather_events_list[iw].event_type[0:3] == 'Sto'):
                        if distance < weather_events_list[iw].event_radius:
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

                            ship_list_selected[i].weather_disp_y = wind_mag*weather_disp_fract * myinterval_days * (
                                wind_speed * 24 * math.cos(angle_to_event * math.pi / 180)) * (
                                                                       1 - fract_event_radius)

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
                            #append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + \
                                          #ship_list_selected[i].hull_condition + " " + str(
                                #round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
                            #append_if(i, append_text, mytotal_time_months, mytotal_time_days_res, time_stamp=True)
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
                            append_text = "encounters Icebergs"
                            
                            append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
                            ship_list_selected[i].ship_speed_cond = 0.3 * ship_list_selected[i].ship_speed_pix / 8
                            ship_list_selected[i].ship_inicebergs = False
                            ship_list_selected[i].marker_radius = 10
                            ship_list_selected[i].weather_disp_x = 0
                            ship_list_selected[i].weather_disp_y = 0
                            #append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + \
                                          #ship_list_selected[i].hull_condition + " "str(
                                #round(ship_list_selected[i].ship_speed_cond, 1)) + " knots "
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
                            ship_list_selected[i].ship_inicebergs == False)):
                        ship_list_selected[i].weather_disp_x = 0
                        ship_list_selected[i].weather_disp_y = 0
                    #print("ship not in weather event weather_disp 0")
                else:
                        ship_list_selected[i].ship_speed_reset(i)
                        #print("speed reset",ship_list_selected[i].ship_name,ship_list_selected[i].ship_speed_cond,ship_list_selected[i].ship_speed_pix)
                        ship_list_selected[i].marker_radius = 5

        ############## display path for troubleshooting#####################
            if display_all_routes==False: # display on route only
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


        ############# displacement due to ship speed###############
            fraction_x = wp_next_x-ship_list_selected[i].ship_x
            fraction_y = wp_next_y-ship_list_selected[i].ship_y
            v1=pygame.math.Vector2(ship_list_selected[i].ship_x,ship_list_selected[i].ship_y  )
            v2=pygame.math.Vector2(wp_next_x,wp_next_y )
            v3=v2-v1
            v3_magnitude=v3.magnitude()
            speed_interval=myinterval_days * 24 * ship_list_selected[i].ship_speed_cond/distortion_factor
            v3_move=v3*speed_interval/v3_magnitude

            move_x_naut=v3_move[0]
            move_y_naut=v3_move[1]

            ship_list_selected[i].move_x = move_x_naut / 3  # as pixels
            ship_list_selected[i].move_y = move_y_naut / 3

        #print(ship_list_selected[i].ship_name,move_x_naut,move_y_naut)

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
                pass
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
            ospeedr_x = ospeed_x * drift_speed
            ospeedr_y = ospeed_y * drift_speed
            #print('ospeed_x,y', ospeedr_x, ospeedr_y)

        ################map distortion effects###########################
        # southrn part of map is 1.6 times more difficult
            if ship_list_selected[i].ship_y > 700:
                distortion_factor = 1.6
            else:
                distortion_factor = 1

            ###################stagger departure or calculate new position#############################
            if (len(ship_list_selected[i].ship_log) == 0):
                append_text = ship_list_selected[i].ship_name + " in port"
                ship_list_selected[i].ship_log.append(append_text)
                append_text = "rig condition " + ship_list_selected[i].rig_condition + " hull condition " + \
                              ship_list_selected[i].hull_condition +  str(
                    round(ship_list_selected[i].ship_speed_cond, 1)+" knots " )
                ship_list_selected[i].ship_log.append(append_text)
            if ship_list_selected[i].ship_k == 0 and ship_list_selected[i].port_delay == 0:  # no port delay
                append_text = 'ship sets sail'
                append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
                ship_list_selected[i].ship_depart_time = mytotal_time
                ship_list_selected[i].ship_x = ship_list_selected[i].ship_x_last + ship_list_selected[
                    i].move_x + ospeedr_x + ship_list_selected[i].weather_disp_x
                ship_list_selected[i].ship_y = ship_list_selected[i].ship_y_last + ship_list_selected[
                    i].move_y + ospeedr_y + ship_list_selected[i].weather_disp_y

            elif ship_list_selected[i].ship_k == 0 and ship_list_selected[i].port_delay > mytotal_time_days:
                ship_list_selected[i].ship_depart_time = mytotal_time
                # delay in port
                ship_list_selected[i].ship_x = ship_list_selected[i].ship_x_last
                ship_list_selected[i].ship_y = ship_list_selected[i].ship_y_last
                append_text = ("waiting in port")
                append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
            elif ship_list_selected[i].ship_shipwreck==True:
                pygame.draw.circle(canvas, ship_color, (ship_list_selected[i].ship_x, ship_list_selected[i].ship_y),
                                   10)
                ship_event_text_rect = pygame.Rect( ship_list_selected[i].ship_x+ 0,
                                                       ship_list_selected[i].ship_y- 0, 100, 25)
                pygame.draw.rect(canvas, "light blue", ship_event_text_rect)
                ship_event_text = font18.render(ship_list_selected[i].ship_name+" Shipwreck", True,
                    color_text)
                canvas.blit(ship_event_text, ship_event_text_rect)
            else:  # new position 
                if ship_list_selected[i].ship_k == 0:
                    append_text = ("ship sets sail")
                    append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)

                 ##############################MOVE#####################################
                #print("at ship move", ship_list_selected[i].ship_name,ship_list_selected[i].ship_x, ship_list_selected[i].ship_y)
                ship_list_selected[i].ship_x = ship_list_selected[i].ship_x_last + ship_list_selected[
                    i].move_x + ospeedr_x + ship_list_selected[i].weather_disp_x
                ship_list_selected[i].ship_y = ship_list_selected[i].ship_y_last + ship_list_selected[
                    i].move_y + ospeedr_y + ship_list_selected[
                                                   i].weather_disp_y  # allowance for y direction being downwards is in the calculations
            #if (i==0): for troubleshooting
                #print( "move_x ",round(ship_list_selected[i].move_x,3),"ospeed_x", round(ospeedr_x,3),"weather_disp_x",round(ship_list_selected[i].weather_disp_x,3),"move_y ",round(ship_list_selected[i].move_y,3), "ospeed_y", round(ospeedr_y,3), "weather_disp_y", round(ship_list_selected[i].weather_disp_y,3))

            pygame.draw.circle(canvas, ship_color, (ship_list_selected[i].ship_x, ship_list_selected[i].ship_y),
                               ship_list_selected[i].marker_radius)

            #### EVALUATE FIXED HAZARDS AT NEW POSITION              ##############################

            gridx = round((ship_list_selected[i].ship_x - 8) / 16)  # grid squares origin are at the top left
            gridy = round((ship_list_selected[i].ship_y - 8) / 16)
            gridx_res = (ship_list_selected[i].ship_x - 8) % 16
            gridy_res = (ship_list_selected[i].ship_y - 8) % 16
            if abs(gridx-gridx0)>4 or abs(gridx-gridx1)>4 or abs(gridy-gridy0)>4 or abs(gridy-gridy1)>4:
                print('DEVIATION ERROR gridx', gridx,'grid_y', gridy, 'gridx0', gridx0,'gridy0', gridy0,'gridx1',gridx1,'gridy1',gridy1)
            if gridx<0:
                gridx=0
            if gridx>80:
                gridx=80
            if gridy<0:
                gridy=0
            if gridy>62:
                gridy=62

            pygame.draw.rect(canvas, "red", (gridx * 16, gridy * 16, w, h), 1)
            pygame.draw.rect(canvas, "blue", (gridx0 * 16, gridy0 * 16, w, h), 1)
            hazard_sq = int(grid[gridy][gridx])

            if ship_list_selected[i].ship_k != 0:
                if hazard_sq == 1:
                    append_text = ("encountered beach at coordinates " + str(
                        10 * round(ship_list_selected[i].ship_x / 10)) + ":" + str(
                        10 * round(ship_list_selected[i].ship_y / 10)))
                    
                    append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
                if hazard_sq == 2:
                    append_text = ("encountered rocks at coordinates " + str(
                        10 * round(ship_list_selected[i].ship_x / 10)) + ":" + str(
                        10 * round(ship_list_selected[i].ship_y / 10)))
                    
                    append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
                    
                if hazard_sq == 4:
                    append_text = ("encountered land at coordinates " + str(
                        10 * round(ship_list_selected[i].ship_x / 10)) + ":" + str(
                        10 * round(ship_list_selected[i].ship_y / 10)))
                    append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
                    
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


            ### UPDATE SHIP PROGRESS
            ship_list_selected[i].ship_x_last= ship_list_selected[i].ship_x
            ship_list_selected[i].ship_y_last = ship_list_selected[i].ship_y
            ship_list_selected[i].ship_event_x_list.append(ship_list_selected[i].ship_x) # event_x and event_y list hold actual track of ship
            ship_list_selected[i].ship_event_y_list.append(ship_list_selected[i].ship_y)
            ###########check if close to next way point move to next way point#####################
            if abs(fraction_x) < alimit and abs(fraction_y) < alimit:
                ship_list_selected[i].ship_k = ship_list_selected[i].ship_k + 1

            ################check if at destination#############
            if ship_list_selected[i].ship_go == True:
                if (ship_list_selected[i].ship_k >= len(ship_list_selected[i].path_go) - 1):  # test of destination
                    # print ('reached destination')
                    pygame.draw.circle(canvas, 'dark red', (ship_list_selected[i].ship_x, ship_list_selected[i].ship_y),
                                       10)
                    append_text = "reached destination - set sail for return"
                    
                    append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)

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
                    append_text = "any repairs required have been completed"
                    append_if(i, append_text, mytotal_time_months, mytotal_time_days_res,time_stamp=True)
            else:
                if (ship_list_selected[i].ship_k >= len(ship_list_selected[i].path_back) - 1):
                    pygame.draw.circle(canvas, 'dark red', (ship_list_selected[i].ship_x, ship_list_selected[i].ship_y),
                                       10)
                    ship_list_selected[i].ship_repair_sub(i)
                    ship_list_selected[i].ship_log.append(str(mytotal_time_months) + " months " + str(
                        round(mytotal_time_days_res, 1)) + " days "+ " any repairs completed ")
                    ship_list_selected[i].ship_event_x_list = []
                    ship_list_selected[i].ship_event_y_list = []
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
                    ###################draw actual progress of ship ##############################
            if display_all_routes==True:
                ishow=i
            else:
                ishow=selected_ship_number
            for k in range(len(ship_list_selected[ishow].ship_event_x_list)):  # to track actual progress of ship
                 pygame.draw.circle(canvas, ship_color, (ship_list_selected[ishow].ship_event_x_list[k], ship_list_selected[ishow].ship_event_y_list[k]), 2)
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
        ###  displau data#########################################
        ship_log_display(window, canvas, selected_ship_number, ship_log)
        insurer_finances_table_x = 400
        insurer_finances_table_y = 0
        subroutines.insurer_finances_nested_list_sub(window, canvas,insurer_finances_table_x,insurer_finances_table_y)
        if display_slist==True:
            #print("display s list")
            slist_x=500
            slist_y=140
            subroutines.ship_list_by_insurer_sub(window, canvas,color_bg,slist_y,slist_x)


        #### display which insurer has best finances
        mbalance_max=0
        mtop=0
        for m in range (0,mmax):
            if mbalance_max<insurers_list[m].balance:
                mbalance_max=insurers_list[m].balance
                mtop=m
            #print("insurer m, m balance , mbalance_max, mtop",m,insurers_list[m].balance,mbalance_max,mtop)
        insurer_winning_string=insurers_list[mtop].insurer_name+" insurer has the best finances"
        insurer_winning_text = font22.render(insurer_winning_string, True, 'red')
        insurer_winning_text_rect = pygame.Rect(500, 100, 2 * menu_width, menu_height)
        pygame.draw.rect(canvas, "white", insurer_winning_text_rect)
        pygame.draw.rect(canvas, color_border, insurer_winning_text_rect, 2)
        canvas.blit(insurer_winning_text, insurer_winning_text_rect)

        window.blit(canvas, (0, 0))
        pygame.display.update()
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


                window.blit(canvas, (0, 0))
                pygame.display.update()

                coffee_menu_button_clicked = True if coffee_menu_button_text_rect.collidepoint(event.pos) else False
                if coffee_menu_button_clicked == True:
                    goinside.goinside_sub(window,canvas,from_key=1)
                if toggle_ship_insurer_list_text_rect.collidepoint(event.pos) == True:
                    if display_slist==True:
                        display_slist = False
                    else:
                        display_slist = True
                if toggle_drift_map_text_rect.collidepoint(event.pos) == True:
                    if display_drift==True:
                        display_drift = False
                    else:
                        display_drift = True
                if toggle_routes_display_text_rect.collidepoint(event.pos) == True:
                    if display_all_routes==True:
                        display_all_routes = False
                    else:
                        display_all_routes = True