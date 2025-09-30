import pygame
import local_data
import astar
import random
import math
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
        pygame.draw.rect(screen, color_rect, button_rect, 2)
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
        self.hull_condition=self.hull_condition_base
        self.rig_condition=self.rig_condition_base
        # attributes calculated from ship_data
        if self.place_of_build == "Plantation":
            self.place_of_build_preference = 1
        else:
            self.place_of_build_preference = 0
        self.hull_speed_factor = 1
        self.rig_speed_factor = 1
        if self.rig_condition == "G":  # G,M,B
            self.rig_speed_factor = 1
        elif self.rig_condition == "M":
            self.rig_speed_factor = 0.7
        else:
            self.rig_speed_factor = 0.5
        if self.hull_condition == "A":
            self.hull_speed_factor = 1
        elif self.hull_condition == "E":
            self.hull_speed_factor = 0.8
        elif self.hull_condition == "I":
            self.hull_speed_factor = 0.6
        elif self.hull_condition == "O":
            self.hull_speed_factor = 0.5
        else:
            self.hull_speed_factor = 0.4

        self.ship_speed_pix = 16 * self.rig_speed_factor * self.hull_speed_factor  # pixels per hour (crosses one grid square per ship hour default, one grid square 2 naut miles ie 2 knots
        self.ship_speed_cond = self.ship_speed_pix / 8  # as kots prgramme resets according to weather conditions
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

        ### attributes initialised to Booleans
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
        self.damage_event_list = [] # holds a tuple of x,y and text for damamage event display


        ### revenue related attributes
        revenue_mult=local_data.revenue_mult
        exports = revenue_mult*0.7  # £ per ton for exports
        imports = revenue_mult*1.75  # £ per ton for imports
        self.revenue_out = self.tons * exports/self.haul
        self.revenue_in = self.tons * imports/self.haul
        self.revenue_accum = 0
        value = 3300  # £ for a 200 ton ship
        self.ship_value = value * ((self.tons / 200) ** 0.6)  # law of sixth tenths
        self.ship_repair=self.ship_value*.33
        self.ship_balance_ins = self.revenue_accum - self.ship_premium_accum
        self.ship_balance_unins = self.revenue_accum - self.ship_damage_accum

        ### other attrubutes
        self.marker_radius = 5
        self.ship_insurer = ""
        self.ship_event_y_list = []
        self.ship_log = ["Ship Log Details for ship " + self.ship_name,
                         "for other ships click on ship name buttons - top left", "This ship " + "is insured by " + str(
                self.ship_insurer) + " at a premium of £" + str(self.ship_premium),"Leaving Port Rig Condition:"+str(self.rig_condition_base)+ " Hull Condition:"+str(self.hull_condition_base)+" "+str(round(self.ship_speed_cond,1))+" knots"]
        return



    def ship_speed_reset(self, j):
        if self.rig_condition == "A":  # G,M,B
            self.rig_speed_factor = 1
        elif self.rig_condition == "M":
            self.rig_speed_factor = 0.7
        else:
            self.rig_speed_factor = 0.5
        if self.hull_condition == "A":
            self.hull_speed_factor = 1
        elif self.hull_condition == "E":
            self.hull_speed_factor = 0.8
        elif self.hull_condition == "I":
            self.hull_speed_factor = 0.6
        elif self.hull_condition == "O":
            self.hull_speed_factor = 0.5
        else:
            self.hull_speed_factor = 0.4
        self.base_speed = 2  # 2 knots
        self.ship_speed_pix = self.base_speed * 8 * self.rig_speed_factor * self.hull_speed_factor  # pixels per hour (crosses one grid square per ship hour default, one grid square 2 naut miles ie 2 knots
        self.ship_speed_cond = self.ship_speed_pix / 8  # as knots prgramme resets according to weather conditions
        return self.ship_speed_cond


    def ship_log_update(self, i):
        self.ship_log[0]="Ship Log Details for ship " + self.ship_name
        self.ship_log[1]=  "for other ships click on ship name buttons - top left"
        self.ship_log[2]= "This ship is insured by "+  str(
                self.ship_insurer) + " at a premium of £" + str(self.ship_premium)
        self.ship_log[3] = "Leaving Port Rig Condition:"+str(self.rig_condition)+ " Hull Condition:"+str(self.hull_condition) +" "+str(round(self.ship_speed_cond,1))+" knots"
        #self.ship_log = ["Ship Log Details for ship " + self.ship_name,
                         #"for other ships click on ship name buttons - top left", "This ship " + "is insured by " + str(
                #self.ship_insurer) + " at a premium of £" + str(self.ship_premium)]

    def ship_finance_update(self, i):
        self.ship_balance_ins = self.revenue_accum - self.ship_premium
        self.ship_balance_unins = self.revenue_accum - self.ship_damage_accum


    def ship_repair_sub(self, i):
        # print ("Ship Repair")
        self.hull_condition = local_data.ship_data[i][6]  # A,E, I O,U from best to worst
        self.rig_condition = local_data.ship_data[i][7]  # G, M,B from best to worst
        self.ship_speed_pix = 16 * self.rig_speed_factor * self.hull_speed_factor  # pixels per hour (crosses one grid square per ship hour default, one grid square 2 naut miles ie 2 knots
        self.ship_speed_cond = self.ship_speed_pix / 8  # as kots prgramme resets according to weather conditions
        if self.rig_condition == "A":  # G,M,B
            self.rig_speed_factor = 1
        elif self.rig_condition == "M":
            self.rig_speed_factor = 0.7
        else:
            self.rig_speed_factor = 0.5
        if self.hull_condition == "A":
            self.hull_speed_factor = 1
        elif self.hull_condition == "E":
            self.hull_speed_factor = 0.8
        elif self.hull_condition == "I":
            self.hull_speed_factor = 0.6
        elif self.hull_condition == "O":
            self.hull_speed_factor = 0.5
        else:
            self.hull_speed_factor = 0.4
        self.ship_log[3] = "Leaving Port after repair Rig Condition:" + str(self.rig_condition) + " Hull Condition:" + str(
            self.hull_condition) +" "+ str(round(self.ship_speed_cond,1)) + " knots"
        return self.ship_speed_cond

    def get_port(self, j):
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
        self.wind_speed_mi = local_data.weather_events_list[i][10]  # max wind speed in knots
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

    def drift_event(self, myinterval_days,j): # interval is passed as milliseconds

            ##### Randomise weather  trajectory within limits######

            #traj_boundary_plus=self.traj_boundary_plus
            #traj_boundary_minus=self.traj_boundary_minus
            traj_limit=10 # degrees
            #if self.trajectory<traj_boundary_plus:
                #self.trajectory=traj_boundary_plus
            #elif self.trajectory>traj_boundary_minus:
                #self.trajectory=traj_boundary_minus
            #else:
            self.trajectory = self.trajectory_base + random.randint(-traj_limit, +traj_limit)
            #if j==0:
                #print("trajectory degrees",self.trajectory)
            ####################################################
            myinterval_days=myinterval_days
            #print ('weather trajectory', self.trajectory)
            incr_x_naut=-myinterval_days*24*self.speed  * math.sin(self.trajectory * math.pi / 180) # speed is in knots, which equates to 1 pixel per second (see pseudocode)
            incr_y_naut = -myinterval_days * 24 * self.speed * math.cos(self.trajectory * math.pi / 180)
            incr_x=incr_x_naut/3 # as pixels
            incr_y=incr_y_naut/3
            self.event_x = self.event_x + incr_x # speed is in knots
            #print ('incr_x',incr_x,'incr y', incr_y)
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
        print ("in insurer reset")
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

def draw_grid_with_blanks(canvas, nested_list, cell_width, cell_height,paddingx,paddingy,table_start_y,table_start_x,font_num,row_head,col_head,color_bg):# m font is int 20,22,row_head is number
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
        font20 = pygame.font.SysFont("Arial", 20, bold=False)
        for line in text_lines:
            text_surface = font20.render(line, True, color)
            surface.blit(text_surface, (rect.left, yq))
            yq += font20.get_linesize() + line_spacing


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
    ins_row_title1 = "Insurer"
    rows_list1 = []
    rows_list2 = []
    rows_list3 = []
    rows_list4 = []
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
    insurer_finances_nested_list.append(rows_list1)
    insurer_finances_nested_list.append(rows_list2)
    insurer_finances_nested_list.append(rows_list3)
    insurer_finances_nested_list.append(rows_list4)
    draw_grid_tjh(canvas, insurer_finances_nested_list, insurer_finances_cell_width, cell_height,
                              padding_x,
                              padding_y,
                              insurer_finances_table_y, insurer_finances_table_x, 20, 2, 0)

    ### SHIP LIST BY INSURER
def ship_list_by_insurer_sub(window,canvas,color_bg,slist_x,slist_y):

    slist = []
    slist.append(["Ships Listed", "Premium Paid", "Damage/Claims"," Revenue","Balance","Theoretical Balance"])
    slist.append(["by Insurer","","","","if Insured", "if not insured"])
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
                #ship_list_selected[sj].ship_name, ship_list_selected[sj].ship_premium_accum, round(ship_list_selected[sj].revenue_accum), round(ship_list_selected[sj].ship_balance_ins), round(ship_list_selected[sj].ship_balance_unins))

                #print((ship_list_selected[sj].ship_damage_accum), round(ship_list_selected[sj].revenue_accum), round(
                    #ship_list_selected[sj].ship_balance_ins), round(ship_list_selected[sj].ship_balance_unins))
                # slist.append(["", ""])
                slist.append([ship_list_selected[sj].ship_name,  ship_list_selected[sj].ship_premium_accum,round(ship_list_selected[sj].ship_damage_accum),round(ship_list_selected[sj].revenue_accum),round(ship_list_selected[sj].ship_balance_ins),round(ship_list_selected[sj].ship_balance_unins)])
        #slist.append(["", ""])

    #print ("slist",slist)
    slist_nested = slist
    #slist_y = 200
    total_ins=0
    total_unins=0
    for sj in range (0,smax):
        total_ins+=ship_list_selected[sj].ship_balance_ins
        total_unins+=ship_list_selected[sj].ship_balance_unins

    if total_ins>total_unins:
        ship_ins_string="Insured Ship"
    else:
        ship_ins_string = "UnInsured Ship"
    slist.append([ship_ins_string, ""
                                   "Finances Better", "", "Total",
                  round(total_ins), round(total_unins)])
    draw_grid_with_blanks(canvas, slist_nested, insurer_finances_cell_width, cell_height,
                                      padding_x,
                                      padding_y,
                                      slist_x,slist_y , 20, 2, 0,color_bg)

