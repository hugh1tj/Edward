mapx=[]
path_local=[]



button_names=[['Click to select menu item - Information Pages:',0],['Background to this series of games',1], # 0,1
              [" Ports, Cargo and Revenue ",1], # 2
              [" Ship Construction and State of Repair ",1],[" Shipping Routes and Ocean Drift ",1],#3,4
             
              [" Weather and other hazards",1],#5
              ["Setting Underwriter Risk Preferences", 1],  # 6
              [" Coffeehouse - negotiating premiums",1],#,7
              ["Sources and historical notes",1],#8,
              ["Settings",1],#9
              [" ",0],#10
              ["Click to enter the Coffeehouse and start the game: ",0], #11
              [" Enter Edward Lloyd's Coffeehouse",1],[" Quit",1]]#12,13
# second parameter indicates whether the button should have a border

goinside_button_names = [['Click the Buttons Below', 0],['Chronicle of Ships due to Sail', 1], ['Adjust Your Risk Preferences', 1],  # 0,1
                [" Circulate around and Offer Premiums", 1],["Ships set sail",1]]  # 2

# second parameter indicates whether the button should have a border





ship_data=[
    ['Albermarle','London','Philadelphia',300,21,'Spanish','A','G',1],
    ['Albion','London','Jamaica',300,0,'Hull','E','M',1],
    ['Amelia','London','New York',180,0,'Plantation','A','G',1],
    ['Ann','London','Quebec',100,2,'Plantation','A','G',1],
    ['St Ann','London','Jamaica',200,11,'Philadelphia','I','M',1],
    ['Benevolence','London','Virginia',280,4,'Scarborough','A','M',1],
    ['Betty','Liverpool','Barbados',120,3,'Plantation','A','G',1],
    ['Boyd','London','Virginia',150,3,'Plantation','E','M',1],
    ['Britannia','London','Greenland',370,14,'Dutch','E','M',1],
    ['Dawkins','London','Jamaica',250,15,'London','E','M',1],
    ['Diamond','London','Gibraltar',60,0,'Poole','A','G',2],
    ['Diana','London','Guadeloupe',220,2,'London','A','M',1],
    ['Diligence','London','Venice',120,0,'London','A','G',2],
    ['Dispatch','Liverpool','Boston',130,12,'Plantation','O','M',1],
    ['Dove','London','Naples',250,15,'Plantation','E','M',2],
    ['Dunbar','London','New York',120,4,'Plantation','E','M',1],# New York via Madeira
    ['Elizabeth','London','Jamaica',200,6,'Plantation','E','M',1],#via Madeira
    ['Elliott','Liverpool','Newfoundland',80,8,'London','I','M',1],
    ['Engrantz','Hull','Stavanger',160,11,'Norway','A','G',2],
    ['Experiment','London','Senegal',140,0,'America','E','M',1],
    ['Martin','Liverpool','Angola',180,15,'British','I','M',1]
    ]# Ship Name, Port of Origin, Destination, tons, age, place of build, hull condition, rig condition, 1=long haul / 2- short haul

ports_waypoints_coord=[                         # as now picked out by mouse over 1300 x 1000 pixel map
                                                # third element is whether of not the location is a port (=1) or waypoint(=2) (not used)
         ['London',1000,309,1],
         ['Thames Estuary',1016, 299,2],
         ['Skagerak',1086,196,2],
         ['Copenhagen',1113, 240,2],
         ['Riga',1210,233,1],
         ['St Petersburg',1290,149,1],
         ['Stavanger',1055,163,1 ],
         ['Rotterdam',1036,291,1],
         ['Dover WP',999,329,2],
         ['Ushant',925,368,2],
         ['Philadelphia',225, 498,1],
         ['Barbados',380, 803,1],
         ['Angola',1100, 950,1],
         ['Jamaica',187,750,1],# with x direction first - which is x coord equivalent to longitude
        ['New York',245, 480,1],
        ['Quebec', 280,375,1],
        ['Virginia',208,531,1], #norfolk
        ['Greenland',476,98,1], #nuuk
        ['Liverpool',950,280,1],
        ['Madeira',713,516,1],
        ['Gibraltar',934,545,1],
        ['Guadeloupe', 340,780,1],
        ['Venice', 1135,415,1],
        ['Boston', 274,457,1],
        ['Naples',1119,472,1],
        ['Newfoundland',402,388,1],
        ['Hull',999,270,1],
        ['Senegal',810,803,1],
    ['TestPoint1',300,600,1],
    ['TestPoint2',800,200,1],
    ['TestPoint3',700,200,1],
    ['TestPoint4',600,200,1],
         ]
list_colors=['dark red','red','green','blue','dark orange','dark blue','dark green', 'black']
list_tile_id=[' ','Beach','Rocks','No Significant Ocean Drift', 'Land', 'Labrador and Canaries Currents: N to S', 'Gulf Steam : SW to NE','North Atlantic Drift:  W to E', 'North Equatorial Current : E to W']

weather_events_list=[('Hurricane_E',7,11,720,800,2,80,2,60,70,24,100,60,100,800,10000),('Hurricane_W',5,9,400,800,1,0,1,-10,10,24,110,60,100,800,10000),('Storms_W',0,6,310,539,2,-45,1,-50,-40,24,60,50,500,1000,50000 ),('Storms_E',0,7,850,450,1.5,-45,1.5 ,-60,-40,24,50,50,500,1000,50000 ),
                   ('Icebergs_W',0,4,480,200,3,-160,0.5,-170,-180,0,0,50,10000,1000,2000 ),('Fog_W',0,4,479,399,1,40,0.5, 30,40,0, 0,50,1000,10000,50000),('Fog_E',0,4,1000,100,1,-140,0.9 ,-170,-180,0, 0,50,1000,10000,50000),('Pirates_E',0,12,850,590,9,0,0,0,0,0,0,70,1000,10000,30000),('Pirates_W',0,12,200,700,9,0,0 ,0,0,0, 0,70,1000,10000,20000)]
#weather_events_list=[('Hurricane_E',7,11,720,800,2,80,2,60,70,24,100,60,100,800,100),('Hurricane_W',5,9,400,800,1,0,1,-10,10,24,110,60,100,800,100),('Storms_W',0,6,310,539,2,-45,1,-50,-40,24,60,50,500,1000,500 ),('Storms_E',0,7,850,450,1.5,-45,1.5 ,-60,-40,24,50,50,500,1000,500 ),
                     #('Icebergs_W',0,4,480,200,3,-160,0.5,-170,-180,0,0,50,10000,1000,200 ),('Fog_W',0,4,479,399,1,40,0.5, 30,40,0, 0,50,1000,10000,500),('Fog_E',0,4,1000,100,1,-140,0.9 ,-170,-180,0, 0,50,1000,10000,500),('Pirates_E',0,12,850,590,9,0,0,0,0,0,0,70,1000,10000,300),('Pirates_W',0,12,200,700,9,0,0 ,0,0,0, 0,70,1000,10000,200)]

#name (0), month season start (1)#month season end(2), x (3), y (4), duration (5), trajectory (6),speed traverse knots (7), traj limit1(8), traj limit (9), min wind speed (10),
# max wind speed (11), starting event radius (12),risk of damage to rigging (13),risk of damage to hull, (14), risk of shipwreck (15)
# note use of trajectory limits discontinued
weather_button_names=['Season Start (month)','Season End (month)','Coordinate X Start','Coordinate Y Start','Duration (months)',
                             'Speed','Wind Speed min (knots)','Wind Speed max (knots)', 'Event Radius - Start','Damage Risk - Rigging','Damage_Risk - Hull','Shipwreck Risk']



insurer_premium_data=[('Algo1',6000,10),('Algo2',6000,9),('MyAlgo',6000,10)  ]
insurer_data=[('Algo1',4,6,7,13,8),('Algo2',12,7,6,13,4),('MyAlgo',12,7,6,4,13)]  # sort place in ship

# 1. name of insurer 2-6: risk preference references, 7. initial book value 8. % premium

insurer_data_labels={4:"Age",6:"Hull condition",7:"Rig Condition",8:"Revenue",12:"Long or Short Haul",13:"Place of Build"}
#insurer name followed by 5 preferences First,Second,Third, Fourth, Fifth . 1 is age, 2 is Place of Build, 3 is Hull Condition, 4 is Rig Condition and 5 is Shipping Route (Short Medkium and Long Hau)
# key [0. ship_list_selected[i].ship_name, 1. ship_list_selected[i].port, 2. ship_list_selected[i].destination,
#                 3. ship_list_selected[i].tons,
#                 4. ship_list_selected[i].age, 5. ship_list_selected[i].place_of_build, 6. ship_list_selected[i].hull_condition,
#                 7. ship_list_selected[i].rig_condition,
#                 8. round(ship_list_selected[i].revenue_out), 9. round(ship_list_selected[i].revenue_in),
#                 10. round(ship_list_selected[i].ship_value), 11. round(ship_list_selected[i].ship_repair)])
#                 12. Haul
#                  13. Place of build  as place_of_build_preference
risk_pref_labels_1 = ["Preference"," 1", " 2", " 3", " 4", " 5"]
risk_list_labels=["UnderWriter","Risk Factor","Age","Place of Build","Hull condition","Rig Condition","Revenue","Long or Short Haul"]
risk_pref_title_labels=[" Underwriter","MyAlgo", "Preferences", "", "", ""]
myalgo=["MyAlgo","","","","",""]
algo1=["Algo1","","","","",""]
algo2=["Algo2","","","","",""]
inspref_list=[]
myalgo_premium=0

ships_instantiated_status_list=[]
premiums_alt_status=[]# has premiums_alt been run?
stat_list=[]

#global storage for goinside
#global ship_list_me
ship_list_me=[]
#global ship_list_selected
ship_list_selected=[]
smax=8
mmax=3
insurers_list=[]
wind_mag=1.4
revenue_mult=3 # revenue multiplier
damage_increment=200

premium_select_labels=["Premium %",5,7.5,10,12.5,15,17.5,20]