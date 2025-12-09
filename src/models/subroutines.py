import pygame
from ..data import local_data
from ..utils import pathfinding as astar
import random
import math
from datetime import datetime

class Button(object):
    def __init__(self, x, y, w, h, text, rect_color, clicked):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text

        self.rect_color = rect_color
        self.clicked = False
        return

    def button_rect_blit(self,screen, color_rect,color_text,color_wash):
        #print(self.x, self.y, self.w, self.h)
        button_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        font22 = pygame.font.SysFont("Arial", 22, bold=False)
        font20 = pygame.font.SysFont("Arial", 20, bold=False)
        #color_text = ('white')
        #color_text=('orange')
        button_text = font22.render(self.text, True, color_text)
        pygame.draw.rect(screen, color_wash, button_rect, )  # erases any visible data
        if color_rect=='red':
            pygame.draw.rect(screen, color_rect, button_rect, 3)
        else:
            pygame.draw.rect(screen, color_rect, button_rect, 1)
        screen.blit(button_text, button_rect)
        return (button_rect)


def blit_text_rect_tjh(surface, text, color, rect, font ):
    words = [word.split() for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    #max_width, max_height = surface.get_size()
    rect = pygame.Rect(rect)
    #, y = pos
    #print (words)
    y = rect.top
    x=rect.left
    width, height = rect.size
    for line in words:
        #print(line)
        for word in line:
            #print(word)
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            #print(word_width, word_height)
            if x + word_width >= rect.right:
                x = rect.left  # Reset the x.
                y += word_height  # Start on new row.

            surface.blit(word_surface, (x, y))

            x += word_width + space
            #print (x)
        x = rect.left  # Reset the x.
        y += word_height  # Start on new row.


class Ship():
    def __init__(self, i):
        # Attributes loaded from ship_data
        self.ship_name = local_data.ship_data[i][0]
        self.port = local_data.ship_data[i][1]
        self.destination = local_data.ship_data[i][2]
        self.tons = local_data.ship_data[i][3]
        self.age = local_data.ship_data[i][4]
        self.place_of_build = local_data.ship_data[i][5]
        self.hull_condition_base = local_data.ship_data[i][6]  # A,E, I O,U from best to worst
        self.rig_condition_base = local_data.ship_data[i][7]  # G, M,B from best to worst
        self.haul = local_data.ship_data[i][8]  # short or long haul
        self.revenue_direct = local_data.ship_data[i][9]  # indicator of max revenue direction either 1 being max on first leg or 2 max on second leg
        self.hull_condition=self.hull_condition_base
        self.rig_condition=self.rig_condition_base
        # attributes calculated from ship_data
        if self.place_of_build == "Plantation":
            self.place_of_build_preference = 1
        else:
            self.place_of_build_preference = 0
      
        ### Attributes inititialised to zero
        self.port_x = 0
        self.port_y = 0
        self.destination_x = 0
        self.destination_y = 0
        self.ship_x_last = 0
        self.ship_y_last = 0
        self.ship_x = 0
        self.ship_y = 0
        #self.wp_number = 0
        self.ports_tuple = 0  # stores port and destination x,y's in a 4 position tuple
        self.ship_k = 0
        self.ship_depart_time = 0
        self.ship_arrive_time = 0
        self.ship_outbound_time = 0
        self.ship_inbound_time = 0
        self.port_delay = 0
        self.move_x = 0
        self.move_y = 0
        self.weather_disp_x = 0
        self.weather_disp_y = 0
        self.ship_hazard_counter = 0
        self.ship_premium = 0
        self.ship_premium_accum=0
        self.ship_premium_counter = 0  # so as to pay only once per year
        self.ship_damage_accum = 0
        self.ship_current_region = "Unknown"  # Track current region for ship
        self.ship_speed_cond_base=0

        ### attributes initialised to Booleans
        ship_wait=False
        self.ship_go = True
        self.ship_infoge = False
        self.ship_infogw = False
        self.ship_instorme = False
        self.ship_instormw = False
        self.ship_inicebergs = False
        self.ship_inhurricanee = False
        self.ship_inhurricanew = False
        self.ship_inpiratese = False
        self.ship_inpiratesw = False
        self.ship_shipwreck=False
        #self.clicked = False
        #self.log_entry = True
        ### attributes initialised as lists
        self.path_go = []
        self.path_back = []
        self.ship_event_x_list = []
        self.ship_event_y_list = []
        self.damage_event_list = [] # holds a tuple of x,y and text for damage event display


        ### revenue related attributes
        revenue_mult=local_data.revenue_mult
        if self.revenue_direct==2: # eg direction of first leg is into London, London is destination
       
            exports = revenue_mult*1.75  # £ per ton for exports e.g. from Jamaica to London
            imports = revenue_mult*0.7  # £ per ton for imports in to port e.g. Jamaica
        else:
            exports = revenue_mult*0.7  # £ per ton for exports e.g from London to Jamaica
            imports = revenue_mult*1.75  # £ per ton for imports e.g from Jamaica into London

        self.revenue_out = self.tons * exports/self.haul
        self.revenue_in = self.tons * imports/self.haul
        self.revenue_accum = 0
        value = 3300  # £ for a 200 ton ship
        self.ship_value = round(value * ((self.tons / 200) ** 0.6) ) # law of sixth tenths
        self.ship_repair=self.ship_value*.33
        self.ship_balance_ins = self.revenue_accum - self.ship_premium_accum
        self.ship_balance_unins = self.revenue_accum - self.ship_damage_accum
        self_ship_value_remain=0

        ### other attrubutes
        self.marker_radius = 5
        self.ship_insurer = ""
        self.ship_event_y_list = []
        
        if self.ship_premium==0:

            self.ship_log = ["Ship Log Details for ship " + self.ship_name,
                         "for other ships click on ship name buttons - top right", "This ship " + "has not been insured. " ,"Leaving Port Rig Condition:"+str(self.rig_condition_base)+ " Hull Condition:"+str(self.hull_condition_base)]
        else:
            
            self.ship_log = ["Ship Log Details for ship " + self.ship_name,
                         "for other ships click on ship name buttons - top right", "This ship " + "is insured by " + str(
                self.ship_insurer) + " at a premium of £" + str(self.ship_premium),"Leaving Port Rig Condition:"+str(self.rig_condition_base)+ " Hull Condition:"+str(self.hull_condition_base)]
        
        return
    
    



    def ship_log_update(self, i):
        self.ship_log[0]="Ship Log Details for ship " + self.ship_name
        self.ship_log[1]=  "for other ships click on ship name buttons - top right"
        self.ship_speed_cond_base=ship_speed_calculate(self.rig_condition_base,self.hull_condition_base)
        ship_speed_cond=ship_speed_calculate(self.rig_condition,self.hull_condition)
        if self.ship_premium==0:
            #self.ship_log[2]="X" # for debugging
            self.ship_log[2] =" This ship has not been insured. "
           
        else:
            #self.ship_log[2]="Y" # for debugging
            self.ship_log[2] = "This ship is insured by " + str(self.ship_insurer)  + " at a premium of £" + str(self.ship_premium)
        
        self.ship_log[3]="Leaving Port Rig Condition:"+str(self.rig_condition_base)+ " Hull Condition:"+str(self.hull_condition_base)+" "+str(round(self.ship_speed_cond_base,1))+" knots"
        
        return

    def ship_finance_update(self, i):
        self.ship_balance_ins = self.revenue_accum - self.ship_premium_accum
        self.ship_balance_unins = self.revenue_accum - self.ship_damage_accum


    def ship_repair_sub(self, i):
        # print ("Ship Repair")
        self.hull_condition = local_data.ship_data[i][6]  # A,E, I O,U from best to worst
        self.rig_condition = local_data.ship_data[i][7]  # G, M,B from best to worst
        #self.ship_speed_pix = 16 * self.rig_speed_factor * self.hull_speed_factor  # pixels per hour (crosses one grid square per ship hour default, one grid square 2 naut miles ie 2 knots
        #self.ship_speed_cond = self.ship_speed_pix / 8  # as kots prgramme resets according to weather conditions
        ship_speed_cond=ship_speed_calculate(self.rig_condition,self.hull_condition)
        self.ship_log[3] = "Leaving Port after repair Rig Condition:" + str(self.rig_condition) + " Hull Condition:" + str(
            self.hull_condition) +" "+ str(round(ship_speed_cond,1)) + " knots"
        self.ship_value_remain=self.ship_value
        return ship_speed_cond

    def get_port(self, j): # creates ports tuple of port and destination and runs astar
        #print('self name', self.ship_name, 'self port', self.port, 'self destination', self.destination)
        port = self.port
        #print ("port",port)
        destination = self.destination
        port1got = False
        port2got = False
        #print('len', len(local_data.ports_waypoints_coord))
        for i in range(0, len(local_data.ports_waypoints_coord)):

            if local_data.ports_waypoints_coord[i][0] == port:
                port1got = True
               # print("got port 1", self.port)
                self.port_x = (local_data.ports_waypoints_coord[i][1])
                self.port_y = (local_data.ports_waypoints_coord[i][2])
            else:
                pass
                #port1got = False
                #print ("port 1 not found")
            if local_data.ports_waypoints_coord[i][0] == destination:
                port2got = True
                #print("got port 2", self.destination)
                self.destination_x = (local_data.ports_waypoints_coord[i][1])
                self.destination_y = (local_data.ports_waypoints_coord[i][2])

            else:
                pass
                # port2got = False
                # print ("port 2 not found")
            # print (port1got, port2got)
            self.ports_tuple = self.port_x, self.port_y, self.destination_x, self.destination_y

            if(port1got == True) and (port2got == True):
            #print ('running astar')
                astar.main_astar(int(self.port_x / 16), int(self.port_y / 16), int(self.destination_x / 16),
                                 int(self.destination_y / 16))
                self.path_go=local_data.path_local
            #print(' path go ', self.path_go)
            #print('length path_go', len(self.path_go))
                astar.main_astar( int(self.destination_x / 16),
                             int(self.destination_y / 16),int(self.port_x / 16), int(self.port_y / 16),)
                self.path_back = local_data.path_local
            #print(' path go ', self.path_go)
            #print ('path back ', self.path_back)

def ship_speed_calculate(rig_condition, hull_condition):
        if rig_condition == "G":  # G,M,B
            rig_speed_factor = 1
        elif rig_condition == "M":
            rig_speed_factor = 0.7
        else: # B
            rig_speed_factor = 0.5
        if hull_condition == "A":
            hull_speed_factor = 1
        elif hull_condition == "E":
            hull_speed_factor = 0.8
        elif hull_condition == "I":
            hull_speed_factor = 0.6
        elif hull_condition == "O":
            hull_speed_factor = 0.5
        else: # U
            hull_speed_factor = 0.4
        base_speed = local_data.base_speed # 2 knots
        ship_speed_pix = base_speed * 8 * rig_speed_factor * hull_speed_factor  # pixels per hour (crosses one grid square per ship hour default, one grid square 2 naut miles ie 2 knots
        ship_speed_cond = ship_speed_pix / 8  # as knots programme; resets according to weather conditions
       
        return (ship_speed_cond)




class Weather_event():

    def __init__(self, i):
        ### attributes loaded directly from data file
        self.event_type = local_data.weather_events_list[i][0]
        self.month_start = local_data.weather_events_list[i][1]
        self.month_end = local_data.weather_events_list[i][2]
        self.duration = 30*local_data.weather_events_list[i][5] # converts to days
        self.trajectory_base = local_data.weather_events_list[i][6]
        self.speed = local_data.weather_events_list[i][7]
        self.traj_boundary_plus = local_data.weather_events_list[i][8]
        self.traj_boundary_minus = local_data.weather_events_list[i][9]
        self.wind_speed_min = local_data.weather_events_list[i][10]  # min wind speed in knots
        self.wind_speed_max = local_data.weather_events_list[i][11]  # max wind speed in knots
        self.starting_event_radius = local_data.weather_events_list[i][12]
        self.rig_damage_risk=local_data.weather_events_list[i][13]
        self.hull_damage_risk=local_data.weather_events_list[i][14]
        self.shipwreck_damage_risk=local_data.weather_events_list[i][15]
        self.trajectory = self.trajectory_base
        ##### Randomise initial x and y within limits
        x_limit=16
        y_limit=16 # one tile
        self.event_x = local_data.weather_events_list[i][3]+random.randint(-x_limit,x_limit) # randomise initial location
        self.event_y = local_data.weather_events_list[i][4]+random.randint(-y_limit,y_limit)
        ### attributes initialised to zero
        self.started_days = 0
        self.age = 0
        self.wind_speed=0
        self.event_radius=0
        ###attributes assigned as Boolean
        self.in_season=False
        self.started=False
        self.exists=False
        self.ended=True
        ### attributes initialised as lists
        self.event_x_list=[]
        self.event_y_list=[]

        self.month_end_reset=-1

    def reset (self,i, mytotal_time_months):
        self.trajectory_base = local_data.weather_events_list[i][6]
        self.tractory=self.trajectory_base # allows random actual trajectories within +/- traj_limit
        self.speed = local_data.weather_events_list[i][7]
        ##### Randomise initial x and y within limits
        x_limit = 16
        y_limit = 16  # one tile
        self.event_x = local_data.weather_events_list[i][3] + random.randint(-x_limit, x_limit)  # randomise initial location
        self.event_y = local_data.weather_events_list[i][4] + random.randint(-y_limit, y_limit)
        self.in_season = False
        self.started = False
        self.exists = False
        self.ended = True
        self.started_days = 0
        self.age = 0
        self.event_x_list = []
        self.event_y_list = []
        self.wind_speed_max =  local_data.weather_events_list[i][11]# max wind speed in knots
        self.wind_speed=0 # knots init
        self.month_end_reset =mytotal_time_months
        #print ("in weather reset")
    
    def weather_settings_update(self,iw):
        
        weather_settings=local_data.weather_severities_chosen
        weather_severity_headers=local_data.weather_severity_headers  
    
        #print ("weather event slice",weather_slice)
        for xw in range(0,len(weather_severity_headers)):
            weather_header_slice=weather_severity_headers[xw][1:4]
            #print("weather header slice",weather_header_slice)
            if self.event_type[0:3]==weather_header_slice:
                #print ("match found", weather_header_slice)
                weather_item_chosen_severity=weather_settings[xw-1]# -1 because weather severities chosen has a blank in the first entry
                #print("chosen severity",weather_item_chosen_severity)
                if weather_item_chosen_severity=="Low":
                        self.duration=self.duration * local_data.weather_severity_default[0] # converts to days and adjusts for severity
                        self.wind_speed_max= self.wind_speed_max* local_data.weather_severity_default[0]
                        self.rig_damage_risk=self.rig_damage_risk*local_data.weather_severity_default[0]
                        self.hull_damage_risk=self.hull_damage_risk*local_data.weather_severity_default[0]
                        self.shipwreck_damage_risk=self.shipwreck_damage_risk*local_data.weather_severity_default[0]

                elif weather_item_chosen_severity=="Severe":
                        
                        self.duration=self.duration * local_data.weather_severity_default[1] # converts to days and adjusts for severity
                        self.wind_speed_max= self.wind_speed_max* local_data.weather_severity_default[1]
                        self.rig_damage_risk=self.rig_damage_risk*local_data.weather_severity_default[1]
                        self.hull_damage_risk=self.hull_damage_risk*local_data.weather_severity_default[1]
                        self.shipwreck_damage_risk=self.shipwreck_damage_risk*local_data.weather_severity_default[1]

                else:
                        pass

    def drift_event(self, myinterval_days,j): # interval is passed as milliseconds

            ##### Randomise weather  trajectory within limits######

            traj_limit=10 # degrees
            self.trajectory = self.trajectory_base + random.randint(-traj_limit, +traj_limit)
            
            ####################################################
            fudge=0.1 # speed was too high to be debugged
            incr_x_naut=fudge*(-myinterval_days)*24*self.speed  * math.sin(self.trajectory * math.pi / 180) # speed is in knots, which equates to 1 pixel per second (see pseudocode)
            incr_y_naut =fudge*( -myinterval_days) * 24 * self.speed * math.cos(self.trajectory * math.pi / 180)
            incr_x=incr_x_naut/3 # as pixels
            incr_y=incr_y_naut/3
            self.event_x = self.event_x + incr_x # speed is in knots
            #print ('weather drift event incr_x',incr_x,'incr y', incr_y, "speed",self.speed,"myinterval_days",myinterval_days)
            self.event_y = self.event_y + incr_y
            # Calculate wind speed with a peak in the middle of duration
            event_fraction=self.age/self.duration
            periphery_speed=24 # perphery wind speed in k nots
            if self.wind_speed_max>24:# to apply to hurricanes and storms only
                if event_fraction<.5:
                    self.wind_speed=periphery_speed+((self.wind_speed_max-periphery_speed)*(event_fraction)/0.5)#
                else:
                    self.wind_speed =periphery_speed+((self.wind_speed_max-periphery_speed)*(1-event_fraction)/0.5)

            return (self.event_x, self.event_y, self.wind_speed)


class Insurer():

    def __init__(self, i):

        self.insurer_name = local_data.insurer_data[i][0]
        self.initial_book_value = local_data.insurer_premium_data[i][1]
        self.percent_premium=local_data.insurer_premium_data[i][2]
        #self.remaining_book_value = 4000
        self.preference_list=[]
        #self.premium_list=[]
        self.ships_insured_list=[]
        #self.premiums_income=self.initial_book_value-self.remaining_book_value
        self.premiums_income=0
        self.premiums_income_accum=0
        self.claims = 0
        self.balance = self.premiums_income_accum-self.claims
        self.remaining_book_value =  self.initial_book_value-self.premiums_income_accum
      
        
        


    def insurer_update(self,i):
        #print("in update i",i)

        self.balance = self.premiums_income_accum - self.claims
        self.remaining_book_value = self.initial_book_value - self.premiums_income_accum
        #print ("in update remaining book value",self.remaining_book_value, "initial book value",self.initial_book_value,"premiums_income_accum",self.premiums_income_accum)
    def insurer_reset(self,i):
        #print ("in insurer reset")
        self.claims=0
        self.premiums_income=0
        self.premiums_income_accum=0
        self.remaining_book_value=self.initial_book_value


        
def find_route(port,destination): ### note this method is also coded as a method for Ship Class - some redundancy here
    for i in range(0, len(local_data.ports_waypoints_coord)):

        if local_data.ports_waypoints_coord[i][0] == port:
            port1got = True
            #print("got port 1", port)
            port_x = (local_data.ports_waypoints_coord[i][1])
            port_y = (local_data.ports_waypoints_coord[i][2])
        else:
            pass
            # port1got = False
            # print ("port 1 not found")
        if local_data.ports_waypoints_coord[i][0] == destination:
            port2got = True
            #print("got port 2", destination)
            destination_x = (local_data.ports_waypoints_coord[i][1])
            destination_y = (local_data.ports_waypoints_coord[i][2])

        else:
            pass
            # port2got = False
            # print ("port 2 not found")
        # print (port1got, port2got)

    if (port1got == True) and (port2got == True):
        # print ('running astar')
        astar.main_astar(int(port_x / 16), int(port_y / 16), int(destination_x / 16),
                         int(destination_y / 16))
        path_go = local_data.path_local
        # print(' path go ', self.path_go)
        # print('length path_go', len(self.path_go))
        astar.main_astar(int(destination_x / 16),
                         int(destination_y / 16), int(port_x / 16), int(port_y / 16), )
        path_back = local_data.path_local
        # print(' path go ', self.path_go)
        # print ('path back ', self.path_back)
    return(path_go,path_back)


def draw_grid(canvas, nested_list, cell_width, cell_height,marginx,marginy,table_start_y):
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    for row_index, row in enumerate(nested_list):
        #print("row index","row",row)
        for col_index, item in enumerate(row):
            #print("col index",col_index,"item",item)
            # Calculate position
            x = col_index * (cell_width + marginx) + marginx
            y = table_start_y + row_index * (cell_height + marginx) + marginy

            # Draw cell

            pygame.draw.rect(canvas, 'white', (x, y, cell_width, cell_height))
            if row_index == 0 or row_index == 1:
                pygame.draw.rect(canvas, 'red', (x, y, cell_width, cell_height), 2)
            else:
                pygame.draw.rect(canvas, 'blue', (x, y, cell_width, cell_height), 2)

            # Render text
            text = font22.render(str(item), True, 'black')
            text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
            canvas.blit(text, text_rect)

def draw_grid_tjh(canvas, nested_list, cell_width, cell_height,paddingx,paddingy,table_start_y,table_start_x,font_num,row_head,col_head):# m font is int 20,22,row_head is number
    #of rows which should have red border and col_head number of columns which should have red border
    if font_num == 22:
        font_use = pygame.font.SysFont("Arial", 22, bold=False)
    else:
        font_use = pygame.font.SysFont("Arial", 20, bold=False)
    for row_index, row in enumerate(nested_list):
        #print("row index","row",row)
        for col_index, item in enumerate(row):
            #print("col index",col_index,"item",item)
            # Calculate position
            x = table_start_x+col_index * (cell_width + paddingx) + paddingx
            y = table_start_y + row_index * (cell_height + paddingy) + paddingy

            # Draw cell

            pygame.draw.rect(canvas, 'white', (x, y, cell_width, cell_height))
            if row_index <= row_head-1 or col_index<=col_head-1:
                pygame.draw.rect(canvas, 'red', (x, y, cell_width, cell_height), 2)
            else:
                pygame.draw.rect(canvas, 'blue', (x, y, cell_width, cell_height), 2)

            # Render text
            text = font_use.render(str(item), True, 'black')
            text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
            canvas.blit(text, text_rect)

def draw_one_column_list(canvas, one_column_list, cell_width, cell_height,paddingy,table_start_y,table_start_x,row_head):#row_head is number of rows of headings to be in red

    font_use = pygame.font.SysFont("Arial", 20, bold=False)
    for row_index, row in enumerate(one_column_list):
        #print(" in one col - row index","row",row)
        
        x = table_start_x
        y = table_start_y + row_index * (cell_height + paddingy) + paddingy

        width=1
        color_bg='black'
        back_color = 'blue'
        if str(row)=="":
                
            width = 1
            back_color = color_bg
            pygame.draw.rect(canvas,'black', (x, y, cell_width, cell_height))

        else:
            width=2
            back_color = 'blue'
            pygame.draw.rect(canvas, 'white', (x, y, cell_width, cell_height))
            
        if row_index<=row_head-1:
            if str(row)=="":
                   pygame.draw.rect(canvas, 'black', (x, y, cell_width, cell_height))  
            else:
                    pygame.draw.rect(canvas, 'red', (x, y, cell_width, cell_height),width)
        else:
                pygame.draw.rect(canvas, back_color, (x, y, cell_width, cell_height),width)
            # Render text
        text = font_use.render(str(row), True, 'black')
        text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
        canvas.blit(text, text_rect)

def draw_grid_with_blanks(canvas, nested_list, cell_width, cell_height,paddingx,paddingy,table_start_y,table_start_x,font_num,row_head,col_head,color_bg):# m font is int 20,22,row_head is number
    #of rows which should have red border and col_head number of columns which should have red border
    #print("sub 501 nested list",nested_list)
    if font_num == 22:
        font_use = pygame.font.SysFont("Arial", 22, bold=False)
    else:
        font_use = pygame.font.SysFont("Arial", 20, bold=False)
    for row_index, row in enumerate(nested_list):
        #print("row index","row",row)
        for col_index, item in enumerate(row):
            #print("col index",col_index,"item",item)
            # Calculate position
            x = table_start_x+col_index * (cell_width + paddingx) + paddingx
            y = table_start_y + row_index * (cell_height + paddingy) + paddingy

            # Draw cell
            if str(item)=="":
                width = 1
                back_color = color_bg
                pygame.draw.rect(canvas,color_bg, (x, y, cell_width, cell_height))

            else:
                width=2
                back_color = 'blue'
                pygame.draw.rect(canvas, 'white', (x, y, cell_width, cell_height))
            if row_index <= row_head-1 or col_index<=col_head-1:
                pygame.draw.rect(canvas, 'red', (x, y, cell_width, cell_height),width)
            else:
                pygame.draw.rect(canvas, back_color, (x, y, cell_width, cell_height),width)

            # Render text
            text = font_use.render(str(item), True, 'black')
            text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
            canvas.blit(text, text_rect)

def draw_grid_with_bolded(canvas, nested_list, cell_width, cell_height,paddingx,paddingy,table_start_y,table_start_x,font_num,row_head,col_head,color_bg):
    # makes bold all insurer names
    
    if font_num == 22:
        font_use = pygame.font.SysFont("Arial", 22, bold=False)
    else:
        font_use = pygame.font.SysFont("Arial", 20, bold=False)
    for row_index, row in enumerate(nested_list):
        #print("row index","row",row)
        for col_index, item in enumerate(row):
            #print("col index",col_index,"item",item)
            # Calculate position
            x = table_start_x+col_index * (cell_width + paddingx) + paddingx
            y = table_start_y + row_index * (cell_height + paddingy) + paddingy

            # Draw cell
            if str(item)=="":
                width = 1
                back_color = color_bg
                pygame.draw.rect(canvas,color_bg, (x, y, cell_width, cell_height))

            else:
                width=2
                back_color = 'blue'
                pygame.draw.rect(canvas, 'white', (x, y, cell_width, cell_height))
            if row_index <= row_head-1 or col_index<=col_head-1:
                pygame.draw.rect(canvas, 'red', (x, y, cell_width, cell_height),width)
            else:
                pygame.draw.rect(canvas, back_color, (x, y, cell_width, cell_height),width)

            # Render text
            if str(item)=="Stern" or str(item)=="Bartholomew"or str(item)=="Ledger" or str(item)=="Uninsured" :
                font_use = pygame.font.SysFont("Arial", 20, bold=True)
            else:
                font_use = pygame.font.SysFont("Arial", 20, bold=False)
            text = font_use.render(str(item), True, 'black')
            text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
            canvas.blit(text, text_rect)


def draw_grid_with_name(canvas, nested_list, cell_width, cell_height,paddingx,paddingy,table_start_y,table_start_x,font_num,row_head,col_head, ship_name_sub):# m font is int 20,22,row_head is number
    #of rows which should have red border and col_head number of columns which should have red border
    if font_num == 22:
        font_use = pygame.font.SysFont("Arial", 22, bold=False)
    else:
        font_use = pygame.font.SysFont("Arial", 20, bold=False)
    for row_index, row in enumerate(nested_list):
        #print("row index","row",row)
        for col_index, item in enumerate(row):
            #print("col index",col_index,"item",item)
            # Calculate position
            x = table_start_x+col_index * (cell_width + paddingx) + paddingx
            y = table_start_y + row_index * (cell_height + paddingy) + paddingy
            #print(str(item))
            # Draw cell
            if str(item)=="" or str(item)=="0":
                pygame.draw.rect(canvas, 'black', (x, y, cell_width, cell_height))
                width=1
                back_color='black'
            else:
                width=2
                back_color = 'blue'
                pygame.draw.rect(canvas, 'white', (x, y, cell_width, cell_height))
            if str(item)==ship_name_sub:
                width=2
                back_color='blue'
                pygame.draw.rect(canvas, back_color, (x, y, cell_width, cell_height))
            if row_index <= row_head-1 or col_index<=col_head-1:
                pygame.draw.rect(canvas, 'red', (x, y, cell_width, cell_height),width)
            else:
                pygame.draw.rect(canvas, back_color, (x, y, cell_width, cell_height),width)

            # Render text
            text = font_use.render(str(item), True, 'black')
            text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
            canvas.blit(text, text_rect)

def draw_grid_with_name_and_insurer(canvas, nested_list, cell_width, cell_height,paddingx,paddingy,table_start_y,table_start_x,font_num,row_head,col_head, ship_name_sub, insurer_name):# m font is int 20,22,row_head is number
    #of rows which should have red border and col_head number of columns which should have red border
    if font_num == 22:
        font_use = pygame.font.SysFont("Arial", 22, bold=False)
    else:
        font_use = pygame.font.SysFont("Arial", 20, bold=False)
    text_color_def='black'

    for row_index, row in enumerate(nested_list):

        for col_index, item in enumerate(row):

            x = table_start_x+col_index * (cell_width + paddingx) + paddingx
            y = table_start_y + row_index * (cell_height + paddingy) + paddingy
            #print(str(item))
            # Draw cell
            if str(item)==""or str(item)=="0":
                pygame.draw.rect(canvas, 'black', (x, y, cell_width, cell_height))
                width=1
                back_color='black'
            else:
                width=2
                back_color = 'blue'
                pygame.draw.rect(canvas, 'white', (x, y, cell_width, cell_height))
            if str(item)==ship_name_sub:
                width=2
                back_color='aqua'
                pygame.draw.rect(canvas, back_color, (x, y, cell_width, cell_height))
            if str(item) == insurer_name:
                width = 2
                back_color = 'gold'
                pygame.draw.rect(canvas, back_color, (x, y, cell_width, cell_height))
            if row_index <= row_head-1 or col_index<=col_head-1:
                pygame.draw.rect(canvas, 'red', (x, y, cell_width, cell_height),width)
            else:
                pygame.draw.rect(canvas, back_color, (x, y, cell_width, cell_height),width)

            text = font_use.render(str(item), True, text_color_def)
            text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
            canvas.blit(text, text_rect)



def reverse_lookup(d, value):
    for key, val in d.items():
        if val == value:
            return key
    return None  # Return None if the value is not found

def blit_text(surface, text_lines, rect, color):  # prints a list as text with a new line for each line entry
        #print ("text lines",text_lines)
        yq = rect.top
        line_spacing = -2
        font20g = pygame.font.SysFont("Georgia", 20, bold=False)
        for line in text_lines:
            text_surface = font20g.render(line, True, color)
            surface.blit(text_surface, (rect.left, yq))
            yq += font20g.get_linesize() + line_spacing


def i_to_grid(i, ROWS, COLS):  # including titles
    i = i
    row = int(i / COLS)  # firs)t col is zero
    #col = i - row * (ROWS - 1)
    col = i - row * (COLS)
    return row, col


def grid_to_i(row, col, ROWS, COLS):
    i = row*COLS+col

    return i

def insurer_finances_nested_list_sub(window,canvas,insurer_finances_table_x,insurer_finances_table_y = 0):
    padding_x = 2
    padding_y = 0
    mmax = local_data.mmax
    insurers_list = local_data.insurers_list  # retrieve mirror
    for m in range (0,mmax):
        insurers_list[m].insurer_update(m)
    insurer_finances_nested_list=[]
    cell_height = 25

    insurer_finances_cell_width = 150
    ins_table_title="Insurer","Finances"
    ins_row_title1 = "Insurer"
    rows_list0 = []
    rows_list1 = []
    rows_list2 = []
    rows_list3 = []
    rows_list4 = []
    rows_list0.append(ins_table_title)
    rows_list1.append(ins_row_title1)
    for m in range(0, mmax):
        rows_list1.append(insurers_list[m].insurer_name)
    ins_row_title2 = "Premiums Income"
    rows_list2.append(ins_row_title2)
    for m in range(0, mmax):
        rows_list2.append(insurers_list[m].premiums_income_accum)
    ins_row_title3 = "Claims"
    rows_list3.append(ins_row_title3)
    for m in range(0, mmax):
        rows_list3.append(round(insurers_list[m].claims))
    ins_row_title4 = "Balance"
    rows_list4.append(ins_row_title4)
    for m in range(0, mmax):
        rows_list4.append(round(insurers_list[m].balance))
    insurer_finances_nested_list.append(rows_list0)
    insurer_finances_nested_list.append(rows_list1)
    insurer_finances_nested_list.append(rows_list2)
    insurer_finances_nested_list.append(rows_list3)
    insurer_finances_nested_list.append(rows_list4)
    draw_grid_tjh(canvas, insurer_finances_nested_list, insurer_finances_cell_width, cell_height,
                              padding_x,
                              padding_y,
                              insurer_finances_table_y, insurer_finances_table_x, 20, 2, 0)

    ### display finances
def finances_sub(window,canvas):
    
    insurer_table_x,insurer_table_y=20,50

    slist_x,slist_y=20,200
    slist_w,slist_h=900,600
   

    color_bg='black'
    color_border='blue'
    color_wash='white'
    font20g = pygame.font.SysFont("Georgia", 20, bold=False)
    finances_rect=(insurer_table_x,insurer_table_y,slist_w,slist_h)
    pygame.draw.rect(canvas,color_wash,finances_rect)
    pygame.draw.rect(canvas,color_border,finances_rect,2)
    finances_text=""
   
    finances_text_rend=font20g.render(finances_text,True,color_bg)
    canvas.blit(finances_text_rend, finances_rect)

   
    #### INSURERS TABLE
    padding_x = 2
    padding_y = 0
    mmax = local_data.mmax
    insurers_list = local_data.insurers_list  # retrieve mirror
    for m in range (0,mmax):
        insurers_list[m].insurer_update(m)
    insurer_finances_nested_list=[]
    cell_height = 25

    insurer_finances_cell_width = 150
    ins_table_title0='Insurer Finances:'
    ins_row_title1 = "Insurer Name"
    
    
    rows_list0 = []
    rows_list1 = []
    rows_list2 = []
    rows_list3 = []
    rows_list4 = []
    rows_list0.append(ins_table_title0)
    rows_list1.append(ins_row_title1)
    for m in range(0, mmax):
        rows_list1.append(insurers_list[m].insurer_name)
    ins_row_title2 = "Premiums Income"
    rows_list2.append(ins_row_title2)
    for m in range(0, mmax):
        rows_list2.append(insurers_list[m].premiums_income_accum)
    ins_row_title3 = "Claims"
    rows_list3.append(ins_row_title3)
    for m in range(0, mmax):
        rows_list3.append(round(insurers_list[m].claims))
    ins_row_title4 = "Balance"
    rows_list4.append(ins_row_title4)
    ins_bal_win=-100000 # given that insurers can lose monety
    ins_bal_win_name=""
    for m in range(0, mmax):
        rows_list4.append(round(insurers_list[m].balance))
        if insurers_list[m].balance>ins_bal_win:
            ins_bal_win=insurers_list[m].balance
            ins_bal_win_name=insurers_list[m].insurer_name

    insurer_finances_nested_list.append(rows_list0)   
    insurer_finances_nested_list.append(rows_list1)
    insurer_finances_nested_list.append(rows_list2)
    insurer_finances_nested_list.append(rows_list3)
    insurer_finances_nested_list.append(rows_list4)
    draw_grid_tjh(canvas, insurer_finances_nested_list, insurer_finances_cell_width, cell_height,
                              padding_x,
                              padding_y,
                              insurer_table_y, insurer_table_x, 20, 2, 0)
    
    ###SHIPS TABLE
    slist = []
    slist.append(["Ships Listed", "Premium Paid", "Damage/Claims"," Revenue","Balance"])
    slist.append(["by Insurer","","",""])
    mmax = local_data.mmax
    smax=local_data.smax
    ship_list_selected=local_data.ship_list_selected
    #print ("ship list selected)",ship_list_selected)
    insurers_list = local_data.insurers_list  # retrieve mirror
    insurer_finances_cell_width = 150
    cell_height = 20
    padding_x = 0
    padding_y = 0
    #insurer_finances_table_x = 5
    #print (smax,mmax,insurers_list)
    for m in range(0, mmax):

        insurer_name = insurers_list[m].insurer_name
        slist.append([insurer_name, ""])

        for sj in range(0, smax):
            ship_list_selected[sj].ship_finance_update(sj)
            #print(ship_list_selected[sj].ship_insurer)
            if insurer_name == ship_list_selected[sj].ship_insurer:
               
                slist.append([ship_list_selected[sj].ship_name,  ship_list_selected[sj].ship_premium_accum,round(ship_list_selected[sj].ship_damage_accum),round(ship_list_selected[sj].revenue_accum),round(ship_list_selected[sj].ship_balance_ins)])
        #slist.append(["", ""])
    slist.append(["Uninsured",""])
    for sj in range(0,smax):
            if ship_list_selected[sj].ship_insurer=="Uninsured":
                slist.append([ship_list_selected[sj].ship_name,  ship_list_selected[sj].ship_premium_accum,round(ship_list_selected[sj].ship_damage_accum),round(ship_list_selected[sj].revenue_accum),round(ship_list_selected[sj].ship_balance_unins)])
                

    #print ("slist",slist)
    slist_nested = slist
    #slist_y = 200
   
    draw_grid_with_bolded(canvas, slist_nested, insurer_finances_cell_width, cell_height,
                                      padding_x,
                                      padding_y,
                                      slist_y,slist_x , 20, 2, 0,color_wash)
    
    insurer_win_flash_x=50
    insurer_win_flash_y=500

    insurer_win_flash_rect=(insurer_win_flash_x,insurer_win_flash_y,400,40)
    pygame.draw.rect(canvas,color_wash,insurer_win_flash_rect)
    pygame.draw.rect(canvas,color_border,insurer_win_flash_rect,2)
    insurer_win_flash_text="Winning Insurer at this point: "+ ins_bal_win_name
   
    insurer_win_flash_text_rend=font20g.render(insurer_win_flash_text,True,color_bg)
    canvas.blit(insurer_win_flash_text_rend, insurer_win_flash_rect)
    ### DISPLAYS SHIP WITH BEST FINANCE
    ship_win_flash_x=50
    ship_win_flash_y= insurer_win_flash_y+50

    win_balance=-10000 #since early balances can be negative
    #ship_win_name="J"
    ship_balance_to_use=0 # according to whether ship is insured or not
   

    for sw in range (0,smax):

        if ship_list_selected[sw].ship_premium>0: # insured ship
            ship_balance_to_use=ship_list_selected[sw].ship_balance_ins
        else:
            ship_balance_to_use=ship_list_selected[sw].ship_balance_unins
        if ship_balance_to_use>win_balance:
                win_balance=ship_balance_to_use
      
                ship_win_name=ship_list_selected[sw].ship_name



    ship_win_flash_rect=(ship_win_flash_x,ship_win_flash_y,400,40)
    pygame.draw.rect(canvas,color_wash,ship_win_flash_rect)
    pygame.draw.rect(canvas,color_border,ship_win_flash_rect,2)
    ship_win_flash_text="Winning Ship at this point: "+ ship_win_name
   
    ship_win_flash_text_rend=font20g.render(ship_win_flash_text,True,color_bg)
    canvas.blit(ship_win_flash_text_rend, ship_win_flash_rect)

    win_flash_rect=(ship_win_flash_x,ship_win_flash_y+50,400,40)
    pygame.draw.rect(canvas,color_wash,win_flash_rect)
    #pygame.draw.rect(canvas,color_wash,win_flash_rect,2)
    win_flash_text="* A winner with a negative balance has lost less money"
   
    win_flash_text_rend=font20g.render(win_flash_text,True,color_bg)
    canvas.blit(win_flash_text_rend, win_flash_rect)

def master_log_sub(window,canvas):
    master_log_x,master_log_y=10,50
    master_log_w,master_log_h=1000,790
   
    color_bg='black'
    color_border='blue'
    color_wash='white'
    font20g = pygame.font.SysFont("Georgia", 20, bold=False)
    master_log_rect=pygame.Rect(master_log_x,master_log_y,master_log_w,master_log_h)
    pygame.draw.rect(canvas,color_wash,master_log_rect)
    pygame.draw.rect(canvas,color_border,master_log_rect,2)

    
    blit_text(canvas, local_data.master_log, master_log_rect, color_border)  ### note blit_text uses a list
    
def insurer_master_log_sub(window,canvas):
    insurer_master_log_x,insurer_master_log_y=10,50
    insurer_master_log_w,insurer_master_log_h=1100,780
   
    color_bg='black'
    color_border='blue'
    color_wash='white'
    font20g = pygame.font.SysFont("Georgia", 20, bold=False)
    insurer_master_log_rect=pygame.Rect(insurer_master_log_x,insurer_master_log_y,insurer_master_log_w,insurer_master_log_h)
    pygame.draw.rect(canvas,color_wash,insurer_master_log_rect)
    pygame.draw.rect(canvas,color_border,insurer_master_log_rect,2)

    
    blit_text(canvas,local_data.insurer_master_log, insurer_master_log_rect, color_border)  ### note blit_text uses a list

def bid_flash(canvas,bid_flash_text,bid_flash_x,bid_flash_y,alt):
            width=400
            height=30
            bid_flash_rect=pygame.Rect(bid_flash_x, bid_flash_y,width,height)
           
            pygame.draw.rect(canvas, "white", bid_flash_rect)
            if alt==0:
                pygame.draw.rect(canvas,'blue',bid_flash_rect,1)
                canvas.blit(bid_flash_text, bid_flash_rect)
            else:
                pygame.draw.rect(canvas,'gold',bid_flash_rect)
            
                canvas.blit(bid_flash_text, bid_flash_rect)


def won_flash(canvas,won_flash_text,won_flash_x,won_flash_y,alt):
            width=400
            height=30
            won_flash_rect=pygame.Rect(won_flash_x, won_flash_y,width,height)
           
            pygame.draw.rect(canvas, "white", won_flash_rect)
            if alt==0:
                pygame.draw.rect(canvas,'blue',won_flash_rect,1)
                canvas.blit(won_flash_text, won_flash_rect)
            else:
                pygame.draw.rect(canvas,'darkblue',won_flash_rect,5)
            
                canvas.blit(won_flash_text, won_flash_rect)      

def pulser(last_second): # note this replace pygame.time which works from the time the pygame is initiated. Python datetime.now is more uiversal - preparing for multiple users
    #print("last_second-i",last_second)
    pulse=0
    current_timestamp=datetime.now()
    timestamp_s=current_timestamp.timestamp()
    timestamp_string = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    this_second=int(timestamp_s)
    if this_second!=last_second:
        pulse=this_second-last_second
        #print("pulse",pulse)
        last_second=this_second
    #print(timestamp_string)
    #print (timestamp_s)
        #print("last_second -o",last_second)
    return(last_second,pulse)

      