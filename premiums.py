

### IMPORTS ###
import pygame
import local_data
import text
import subroutines
import ports
import random



def draw_grid(canvas, nested_list, cell_width, cell_height,marginx,marginy,table_start_y):
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    for row_index, row in enumerate(nested_list):
        # print(row_index,row)
        for col_index, item in enumerate(row):
            # print(col_index,item)
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

def premiums_sub (window, canvas):
    ###2  PYGAME INIT ###
    pygame.init()
    ### 3. COLOR DEFINITIONS ###
    color_text = ('black')
    color_border = ('blue')
    color_wash = ('white')
    ### 4. FONT DEFINITIONS ###
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)

    ### 5 TEXT POSITIONS ###
    rightpaneltext_x = 500
    rightpaneltext_y = 900
    rightpaneltext_w = 700
    rightpaneltext_h = 500
    port_list_margin = 5
    port_list_start = 50
    port_list_width = 200
    port_list_height = 25
    cell_width = 90 # for nested lists
    cell_height = 18
    marginx = 2
    marginy = 5
    # width_text = 800  # width of left panel of text
    # height_text = 700  # width of right panel of text

    ### 6 INITIAL TEXT ###
    title_text = font22.render("Premiums", True, color_text)
    menubuttontext = font22.render(" Go back to Main Menu", True, color_text)
    #premiums_log_text=font22.render(" Coffee House Events Log", True, color_text)
    
    ### 7 VARIABLE INITIATIONS ###
    #mapwidth = 1500
    #mapheight = mapwidth * .765  # empirical
    imax = 10  # number of ships for display in educational part
    kmax=len(local_data.insurer_data) #number of insurers default 3
    menubutton_clicked = False
    changeriskpreftext_clicked=False
    changerisk_show=False
    running = True
    prem_fract=0.1#fraction of ship value which is used for premium
    ### 8 IMAGE LOADING ###

    ### 9 lISTS ###
    premiums_log_list=[]
    ship_list_nested=[]
    ship_list_selected = []
    ship_list_me = []
    ship_list_me = (random.sample(range(0, len(local_data.ship_data)), imax))
    insurers_list=[]
    
    ### 10 OBJECTS ###
    for i in range(len(ship_list_me)):
        ship_list_selected.append(subroutines.Ship(ship_list_me[i]))  # instantiates ship
    for k in range(0,kmax):
        insurers_list.append(subroutines.Insurer(k)) # instatiates insurer
    premiums_log_list.append("Premiums Log List")
    ### 11 RECTS
    title_text_rect = pygame.Rect(port_list_margin, 0, port_list_width, port_list_height)
    pygame.draw.rect(canvas, "white", title_text_rect)
    pygame.draw.rect(canvas, color_border, title_text_rect, 1)
    canvas.blit(title_text, title_text_rect)
    menubuttontext_rect = pygame.Rect(port_list_margin, 900, port_list_width, port_list_height)
    premiums_log_text_rect = pygame.Rect(port_list_margin, 400, 500, 400)
    pygame.draw.rect(canvas, 'white', premiums_log_text_rect, 0)
    pygame.draw.rect(canvas, color_border, menubuttontext_rect, 1)
    
    canvas.blit(menubuttontext, menubuttontext_rect)
    #canvas.blit(premiums_log_text, premiums_log_text_rect)
    
    
    end_of_bidding=False
    display_marker=0
    
### SHOW PREMiUMS ### 
    while end_of_bidding==False:
        #print ('c',c)
        table_start_y=40
        for m in range(len(local_data.insurer_data)): # blit book values
       
            insurer= local_data.insurer_data[m][0]
            insurer_text = font22.render("Insurer " + insurer + "  Remaining Book Value: " + str(round(insurers_list[m].book_value)), True, color_text)
            insurer_text_rect = pygame.Rect(port_list_margin, table_start_y+m*port_list_height, 3*port_list_width, port_list_height)

            #table_start_y = table_start_y + port_list_height
            pygame.draw.rect(canvas, color_wash, insurer_text_rect)
            pygame.draw.rect(canvas, color_border, insurer_text_rect, 1)
            canvas.blit(insurer_text, insurer_text_rect)

        table_start_y = table_start_y + (m)*port_list_height
        for m in range(len(local_data.insurer_data)):

            ship_list_nested=[] # clears the list for each insurer
            preference_list=[]
            ship_list_insurer=[]
           
            for i in range(len(ship_list_me)):
                #print("insured",ship_list_selected[i].ship_name, ship_list_selected[i].ship_insurer)
                #if (ship_list_selected[i].ship_insurer==""):
                
                ship_list_nested.append(
           
                [ship_list_selected[i].ship_name, ship_list_selected[i].port, ship_list_selected[i].destination,
                ship_list_selected[i].tons,
                ship_list_selected[i].age, ship_list_selected[i].place_of_build, ship_list_selected[i].hull_condition,
                ship_list_selected[i].rig_condition,
                round(ship_list_selected[i].revenue_out), round(ship_list_selected[i].revenue_in),
                round(ship_list_selected[i].ship_value), round(ship_list_selected[i].ship_repair),ship_list_selected[i].haul,
                round(ship_list_selected[i].ship_premium), ship_list_selected[i].ship_insurer])

                ship_list_insurer.append(

                    [ship_list_selected[i].ship_name, ship_list_selected[i].port, ship_list_selected[i].destination,
                     ship_list_selected[i].tons,
                     ship_list_selected[i].age, ship_list_selected[i].place_of_build,
                     ship_list_selected[i].hull_condition,
                     ship_list_selected[i].rig_condition,
                     round(ship_list_selected[i].revenue_out), round(ship_list_selected[i].revenue_in),
                     round(ship_list_selected[i].ship_value), round(ship_list_selected[i].ship_repair),
                     ship_list_selected[i].haul,
                     round(ship_list_selected[i].ship_premium), ship_list_selected[i].ship_insurer])
    ### INSURER ALGORITHM###
            
            if m==2:
                if (len(local_data.inspref_list)>1):  # check to see if MyAlgo has been set with values other than default
                    #print ("inspref list",local_data.inspref_list)
                    key1 = local_data.inspref_list[1]
                    c1=subroutines.reverse_lookup(local_data.insurer_data_labels,key1)
                    key2=local_data.inspref_list[2]
                    c2 = subroutines.reverse_lookup(local_data.insurer_data_labels, key2)
                    key3=local_data.inspref_list[3]
                    c3 = subroutines.reverse_lookup(local_data.insurer_data_labels, key3)
                    key4=local_data.inspref_list[4]
                    c4 = subroutines.reverse_lookup(local_data.insurer_data_labels, key4)
                    key5=local_data.inspref_list[5]
                    c5 = subroutines.reverse_lookup(local_data.insurer_data_labels, key5)
                    #c5=local_data.insurer_data_labels[key5]
                    #c2 = local_data.inspref_list[2]
                    #c3 = local_data.inspref_list[3]
                    #c4 = local_data.inspref_list[4]
                    #c5 = local_data.inspref_list[5]
                else:
                    c1 = local_data.insurer_data[m][1]
                    c2 = local_data.insurer_data[m][2]
                    c3 = local_data.insurer_data[m][3]
                    c4 = local_data.insurer_data[m][4]
                    c5 = local_data.insurer_data[m][5]
            else:
                c1=local_data.insurer_data[m][1]
                #print ("c1 default",c1)
                c2=local_data.insurer_data[m][2]
                c3=local_data.insurer_data[m][3]
                c4=local_data.insurer_data[m][4]
                c5=local_data.insurer_data[m][5]
           
            ship_sorted_list = sorted(ship_list_nested, key=lambda x: (x[c1],x[c2],x[c3],x[c4],x[c5]))
            for c in range(len(ship_sorted_list)):
                insurers_list[m].preference_list.append(ship_sorted_list[c][0])  ### the preferences of each insurer are listed ship by ship 
                ship_value=ship_sorted_list[c][11]
                premium_fraction=0.1+0.01*c
                print ("premium fraction", ship_sorted_list[c][0], premium_fraction)
                premium=ship_value*premium_fraction
                insurers_list[m].premium_list.append(premium)
            print("insurers list m",m, insurers_list[m].preference_list)
            print ("insurers premium list m",m, insurers_list[m].premium_list)
            title_list1_prem = ["Ship Name", "Port ", "Destination", "Tons", "Age", "Place ", "Hull", "Rig ", "Revenue ", "Revenue",
                   "Cost of ", "Cost of", "Haul", "Premium", "Insurer"]
            title_list2_prem = ["", "of Origin", "", "", "", "of build", "condition", "condition", " going", "returning", "of build",
                   "of repair/refit", "","",""]

            ship_sorted_list.insert(0, title_list2_prem)
            ship_sorted_list.insert(0, title_list1_prem)
            ### ship sorted list is not blitted
        ship_list_insurer= sorted(ship_list_nested, key=lambda x: (x[14]))
        title_list1_prem = ["Ship Name", "Port ", "Destination", "Tons", "Age", "Place ", "Hull", "Rig ", "Revenue ",
                            "Revenue",
                            "Cost of ", "Cost of", "Haul", "Premium", "Insurer"]
        title_list2_prem = ["", "of Origin", "", "", "", "of build", "condition", "condition", " going", "returning",
                            "of build",
                            "of repair/refit", "", "", ""]

        ship_list_insurer.insert(0, title_list2_prem)
        ship_list_insurer.insert(0, title_list1_prem)
        table_start_y = table_start_y + 60
        draw_grid(canvas, ship_list_insurer, cell_width, cell_height, marginx, marginy,table_start_y)
### DISPLAY INSURERS PREFERENCE LIST WITH PREMIUMS OFFERED ###


            
     ### Create list of first places ###
      
        for i in range(len(ship_list_me)):
            placement_list = []  # for line of uninsured entries
            for k in range(0,kmax):
                for ix in range(len(ship_list_me)):
                    if ship_list_selected[ix].ship_name==insurers_list[k].preference_list[i]:
                        if ship_list_selected[ix].ship_premium==0:  # ensure that only ships which have not yet been insured enter the placement list
                        
                            placement_list.append(insurers_list[k].preference_list[i])
            print ("placement_list i,k",i,k, placement_list)

    ### find ships in placement list with unique names (if any)
            ship_name_no_dup=[]
            seen=set()
    ### find unique entries in list of top ships
            ship_name_no_dup=[val for val in placement_list if val not in seen and (seen.add(val) or True)]
            print ("ships names extracted",ship_name_no_dup)
   
    ### find list of duplicates in top ships
            duplicates=[ii for ii in set(placement_list) if placement_list.count(ii)>1]  # find duplicate ship names
            print ("duplicates",duplicates)
            
           
            for ship in ship_name_no_dup:
                if ship not in duplicates:
                    print ("insured as unique name", ship)
                    
                    try:
                        position = placement_list.index(ship)
                        print(f"The position of the ship in list of insurers: {position}")
                    except ValueError:
                        print("The ship is not in the list.")
                    insurer=insurers_list[position].insurer_name
                    premiums_log_list.append(str(ship) +" selected by "+ str(insurer)+" Unique : Premium applied "+str(round(prem_fract*ship_list_selected[i].ship_value)))
                    print ("insurer ", insurers_list[position].insurer_name)
                    for i in range(len(ship_list_me)):
                        if ship_list_selected[i].ship_name == ship:
                            ship_list_selected[i].ship_premium = 0.1 * ship_list_selected[i].ship_value
                            insurers_list[position].book_value = insurers_list[position].book_value - ship_list_selected[
                                i].ship_premium
                       
                            ship_list_selected[i].ship_insurer=insurer
                if ship in duplicates:
                    print ("insured as duplicate", ship)
                    #try:
                        #position = placement_list.index(ship)  #using .index doesn't work because it onluy returns the first position
                        #print(f"The positions of the ship in the placement list are: {position}")
                    #except ValueError:
                        #print("The ship is not in the list.")
                    ans = {num: [ii for ii, x in enumerate(placement_list) if x == num] for num in set(placement_list)
                           if placement_list.count(num) > 1}  # find positions of ships with duplicate names
                    print(" positions of duplicates as dict", ans)
                    anslist = list(ans.values())
                    # print("anslist",anslist)
                    if len(anslist) > 0:
                        print("anslist0", anslist[0])
                        xbookvalue_max=0
                        xpos_max=0
                        for xpos in anslist[0]:
                            print("xpos", xpos)
                            xinsurer = insurers_list[xpos].insurer_name
                            print("an xinsurer in duplicates", xinsurer)
                            xbookvalue=insurers_list[xpos].book_value # differentiate duplicates by book value
                            if xbookvalue >= xbookvalue_max:
                                xbookvalue_max=xbookvalue
                                xinsurer_max=xinsurer
                                xpos_max=xpos
                            print("bookvalue max,xpos_max",xbookvalue_max,xpos_max)

                        print("the selected xinsurer in duplicates, xpos_max", xinsurer, xpos_max)
                        insurer=insurers_list[xpos_max].insurer_name
                       
                        premiums_log_list.append(
                            str(ship) + " selected by " + str(insurer) + " Duplicate : Premium applied " + str(
                                round(prem_fract * ship_list_selected[i].ship_value)))
                        print ("insurer ", insurers_list[xpos_max].insurer_name)
                    for i in range(len(ship_list_me)):
                        if ship_list_selected[i].ship_name == ship:
                            ship_list_selected[i].ship_premium =  0.1*ship_list_selected[i].ship_value
                            insurers_list[xpos_max].book_value = insurers_list[xpos_max].book_value - ship_list_selected[i].ship_premium
                            ship_list_selected[i].ship_insurer=insurer  
                    
        #if all ships insured or book value of insurers less than
        #end_of_bidding=True if
        prem_marker=True
        for i in range(len(ship_list_me)):
            print("premium ", ship_list_selected[i].ship_premium)
            if ship_list_selected[i].ship_premium==0:
                print(" ship with no insurance")
                prem_marker = False
        if insurers_list[position].book_value<6000: # temporary test
            end_of_bidding=True
        if prem_marker==True:
            display_marker=display_marker+1
        if display_marker>4:
            end_of_bidding=True
        
        pygame.draw.rect(canvas, "white", menubuttontext_rect)
        pygame.draw.rect(canvas, color_border, menubuttontext_rect, 2)
        canvas.blit(menubuttontext, menubuttontext_rect)
       
        textsurf = pygame.Rect(rightpaneltext_x, rightpaneltext_y, rightpaneltext_w, rightpaneltext_h)
        subroutines.blit_text_rect_tjh(canvas, text.mytext7, 'white', textsurf, font20)
        
        
        premiums_log_text=premiums_log_list
        subroutines.blit_text(canvas,premiums_log_text, premiums_log_text_rect, "blue")
        
        #canvas.blit(premiums_log_text, premiums_log_text_rect)
       

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
                #print ("in mousebuttondown")
               
                menubutton_clicked = True if menubuttontext_rect.collidepoint(event.pos) else False
            if menubutton_clicked == True:
                from main import main_menu
                main_menu()
                
                
            
           