### IMPORTS ###
import pygame
from ...data import local_data
from ...data import text_content as mytext
from ...models import subroutines
import random
import math

def weather_sub(window,canvas): # allows calling from main menu without goinside
    pygame.init()
   
    
    color_text = ('black')
    color_border = ('blue')
    color_dest = ('red')
    color_wash = "white"
    port_list_start = 50
    #width_text = 800  # width of left panel of text
    #height_text = 700  # width of right panel of text
    mapwidth = 1500
    mapheight = mapwidth * .765  # empirical
    img2 = pygame.image.load('src/assets/images/natlantictrimmedre.png')
    img2r = pygame.transform.scale(img2, (mapwidth, mapheight))  # map of north atlantic larger scale
    canvas.blit(img2r, (0, 0))  # blit map first
    
    window.blit(canvas, (0, 0))
    pygame.display.update()
    #pygame.time.delay(10000) for debug
    from_index=0
    weather_sub_sub(window,canvas,img2r)
    
def weather_sub_sub(window,canvas,img2r):
    #print("in weather_sub_sub")
    window.blit(canvas, (0, 0))
    pygame.display.update()
    rightpaneltext_x = 500  # for textsurf
    rightpaneltext_y = 800
    rightpaneltext_w = 700
    rightpaneltext_h = 500
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    
    #pygame.time.delay(10000)# for debug
    port_list_margin = 5
    port_list_width = 200
    port_list_height = 25
    color_text = ('black')
    color_border = ('blue')
    color_dest = ('red')
    color_wash = "white"
    weather_disp_fract = 0.01  # fudge - needs some science
    running = True
    wind_speed_min = 24  # knots for windy events only
    weather_sep=0 # separates weater events
    game_speed_conv = 5000  # 25714 milliseconds game time equals one day of ship travel
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    
    
### 9 CREATION OF LISTS ###
    weather_events_list_len = (len(local_data.weather_events_list)) # instatiates all possible weather events
    weather_events_list = []
    for iw in range(len(local_data.weather_events_list)):
        weather_events_list.append(subroutines.Weather_event(iw))  # instantiates for all types of weather event
### 11 RECTS ###
    journey_time_text_rect = pygame.Rect(10, 5, 400, 25)
    mystarttime = pygame.time.get_ticks()
    mytime_last = mystarttime

    while running:
        #if from_index==1: # from goinside
        canvas.blit(img2r, (0, 0))  # blit map first

        window.blit(canvas, (0, 0)) # educational or goinside canvas
    ### TIME HANDLING ###
        mytime = pygame.time.get_ticks()
        mytotal_time = mytime - mystarttime
        myinterval = mytime - mytime_last  # as play milliseconds
        myinterval_days = myinterval / game_speed_conv
        #print ('mytintervaldays start',myinterval_days)
        mytotal_time_days = mytotal_time / game_speed_conv
        mytotal_time_months = int(mytotal_time_days / 30)
        mytotal_time_years = int(mytotal_time_months / 12)
        mytotal_time_months_res = mytotal_time_months - mytotal_time_years * 12
        mytotal_time_days_res = mytotal_time_days - mytotal_time_months * 30
        mytotal_time_years_res = mytotal_time_months - mytotal_time_years * 12
        pygame.draw.rect(canvas, 'white', journey_time_text_rect)  # avoid over writing previous entry

        journey_time_text = font20.render(str(mytotal_time_years) + " years" +
                                          "  " + str(mytotal_time_months_res) + " months " + str(
            round(mytotal_time_days_res, 1)) + " days ", True,
                                          color_text)
        pygame.draw.rect(canvas, color_border, journey_time_text_rect, 2)  # avoid over writing previous entry
        canvas.blit(journey_time_text, journey_time_text_rect)
       
        menubuttontext = font22.render(" Go back to Main Menu", True, color_text)
        menubutton_clicked = False
        menubuttontext_rect = pygame.Rect(port_list_margin, 800, port_list_width, port_list_height)
        pygame.draw.rect(canvas, "white", menubuttontext_rect)
        pygame.draw.rect(canvas, color_border, menubuttontext_rect, 2)
        canvas.blit(menubuttontext, menubuttontext_rect)

        for iw in range(len(weather_events_list)):
            # print(weather_events_list[iw].event_type)
            weather_slice = weather_events_list[iw].event_type[0:4]
            # print ("slice", weather_slice)
            weather_event_text = font20.render(weather_events_list[iw].event_type, True, color_text)
            # print("month, weather month end", weather_events_list[iw].event_type, mytotal_time_months,weather_events_list[iw].month_end_reset)
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
                #print ("myinterval days",myinterval_days, iw)
                position_tuple = weather_events_list[iw].drift_event(myinterval_days, iw)
                # print('position and wind speed ', position_tuple)
                weather_events_list[iw].event_x = position_tuple[0]
                weather_events_list[iw].event_y = position_tuple[1]
                # weather_events_list[iw].wind_speed_max= position_tuple[2]
                weather_events_list[iw].wind_speed = position_tuple[2]
                weather_events_list[iw].event_x_list.append(weather_events_list[iw].event_x)
                weather_events_list[iw].event_y_list.append(weather_events_list[iw].event_y)
                weather_events_list[iw].event_radius = weather_events_list[iw].starting_event_radius
                # print("weather events, type, wind speed, age, duration",weather_events_list[iw].event_type, weather_events_list[iw].wind_speed, weather_events_list[iw].age, weather_events_list[iw].duration)
                for ik in range(len(weather_events_list)):
                    dist_weather = math.sqrt(
                        (weather_events_list[iw].event_x - weather_events_list[ik].event_x) ** 2 + (
                                    weather_events_list[iw].event_y - weather_events_list[
                                ik].event_y) ** 2)  # find distance to other weather events
                    if dist_weather < (weather_events_list[iw].event_radius + weather_events_list[
                        ik].event_radius) + weather_sep:  # creates a separation of weather)sep
                        # weather_slice=weather_events_list[iw].event_type[0:4]
                        if (weather_events_list[ik].event_type[0:4] != "Pira" and weather_events_list[iw].event_type[
                                                                                  0:4] != "Pira"):
                            if weather_events_list[iw].event_type != weather_events_list[ik].event_type:
                                # print("distance weather - cancel weather event", weather_events_list[iw].event_type,weather_events_list[ik].event_type, dist_weather)
                                if weather_events_list[iw].event_radius >= weather_events_list[ik].event_radius:
                                    weather_events_list[
                                        ik].exists = False  # ends smaller of the two weather events by event radius
                                    weather_events_list[ik].ended = True
                                    weather_events_list[ik].reset(ik, mytotal_time_months)

                if (weather_events_list[iw].event_type == "Hurricane_cverde") or (
                        weather_events_list[iw].event_type == "Hurricane_carr") or (
                        weather_events_list[iw].event_type == "Storms_W") or (
                        weather_events_list[iw].event_type == "Storms_E"):
                    # print (weather_events_list[iw].event_type,"wind speed", weather_events_list[iw].wind_speed)

                    if (0 <= weather_events_list[iw].wind_speed < 34):
                        color_ring = 'black'
                        weather_events_list[iw].event_radius = weather_events_list[iw].starting_event_radius
                    elif (34 <= weather_events_list[iw].wind_speed < 64):
                        color_ring = 'blue'
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

                    pygame.draw.circle(canvas, color_ring,
                                       (weather_events_list[iw].event_x, weather_events_list[iw].event_y),
                                       weather_events_list[iw].event_radius, width=4)

                else:
                    pygame.draw.circle(canvas, 'blue',
                                       (weather_events_list[iw].event_x, weather_events_list[iw].event_y),
                                       weather_events_list[iw].starting_event_radius, width=4)
                # weather_events_list[iw].event_radius=event_radius
                weather_event_text_rect = pygame.Rect(weather_events_list[iw].event_x + 0,
                                                      weather_events_list[iw].event_y - 0, 100, 50)
                weather_event_text = font20.render(
                    (weather_events_list[iw].event_type[:len(weather_events_list[iw].event_type) - 2]), True,
                    color_text)
                canvas.blit(weather_event_text, weather_event_text_rect)
            ###############ensure weather events are separated ###########################################
        for iw in range(len(weather_events_list)):
            for ik in range(len(weather_events_list)):
                dist_weather = math.sqrt((weather_events_list[iw].event_x - weather_events_list[ik].event_x) ** 2 + (
                            weather_events_list[iw].event_y - weather_events_list[ik].event_y) ** 2)
                # weather_slice = weather_events_list[iw].event_type[0:4]
                if (weather_events_list[ik].event_type[0:3] != "Pir") and (weather_events_list[iw].event_type[
                                                                           0:3] != "Pir"):  # Pirates can coexist with other weather events

                    if dist_weather < (weather_events_list[iw].event_radius + weather_events_list[
                        ik].event_radius) + weather_sep:  # creates a separation
                        if weather_events_list[iw].event_type != weather_events_list[ik].event_type:
                            # print("distance weather",weather_events_list[iw].event_type,weather_events_list[ik].event_type,dist_weather)
                            if weather_events_list[iw].event_radius >= weather_events_list[ik].event_radius:
                                weather_events_list[
                                    ik].exists = False  # ends smaller of the two weather events by event radius
                                weather_events_list[ik].ended = True
                                weather_events_list[ik].reset(ik, mytotal_time_months)
        ###  displau data
        #subroutines.insurer_finances_nested_list_sub(window, canvas)
        #subroutines.ship_list_by_insurer_sub(window, canvas)
        textsurf = pygame.Rect(rightpaneltext_x, rightpaneltext_y, rightpaneltext_w, rightpaneltext_h)
        pygame.draw.rect(canvas, 'white', textsurf)  # blank bacground
        subroutines.blit_text_rect_tjh(canvas, mytext.mytext6, 'black', textsurf, font22)
        window.blit(canvas, (0, 0))

        pygame.display.update()

        mytime_last = mytime
        
        #if from_index==1:
            #print ("returning canvas")
            #return(canvas)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                    menubutton_clicked = True if menubuttontext_rect.collidepoint(event.pos) else False
            if menubutton_clicked == True:
                    from ...core.main import main_menu
                    main_menu()
        

                