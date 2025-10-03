
### IMPORTS ###
import pygame
from ...data import local_data
from ...models import subroutines
import random
from . import goinside

def premiums_alt_sub(window, canvas):
    pygame.init()
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    color_text = 'black'
    smax = 10  # number of ships for display in educational part
    local_data.smax = smax
    mmax = len(local_data.insurer_data)  # number of insurers default 3
    from_index = 0

    ship_list_me = (random.sample(range(0, len(local_data.ship_data)), smax))
    local_data.ship_list_me = ship_list_me
    ship_list_selected = []
    insurers_list = []
    for s in range(len(ship_list_me)):
        ship_list_selected.append(subroutines.Ship(ship_list_me[s]))  # instantiates ship
    local_data.ship_list_selected = ship_list_selected  # mirror
    for m in range(0, mmax):
        insurers_list.append(subroutines.Insurer(m))  # instantiates insurer
    local_data.insurers_list = insurers_list
    premiums_alt_sub_sub(window, canvas, ship_list_me, ship_list_selected, insurers_list, from_index)

def premiums_alt_sub_sub(window, canvas, ship_list_me, ship_list_selected, insurers_list, from_index):
    smax = local_data.smax
    slength = smax  # for adjusting length of premiums_offered_nested_list and display
    mmax = len(local_data.insurer_data)
    fail_round=True
    premium_below=-1
    ### 3. COLOR DEFINITIONS ###
    color_text = ('black')
    color_border = ('blue')
    color_wash = ('white')
    ### 4. FONT DEFINITIONS ###
    font20 = pygame.font.SysFont("Arial", 20, bold=False)
    font22 = pygame.font.SysFont("Arial", 22, bold=False)
    ### 6 INITIAL TEXT ###
    title0_text = font22.render("Ships Data", True, color_text)
    title1_text = font22.render("Premiums Offered", True, color_text)
    title2_text = font22.render("Premiums Agreed", True, color_text)
    title3_text = font22.render("Remaining Book Value", True, color_text)
    menubuttontext = font22.render(" Go back to Main Menu", True, color_text)
    menu_button_start_x = 800
    cell_width_title = 200
    cell_height_menu = 25
    cell_height = 20
    marginx = 20
    marginy = 20
    size_canv = canvas.get_size()
    size_width = size_canv[0] - 2 * marginx  # for a border
    coffee_menu_button_text = font22.render("Coffee Shop Menu", True, color_border)
    menubuttontext_rect = pygame.Rect(menu_button_start_x, 900, cell_width_title, cell_height_menu)
    coffee_menu_button_text_rect = pygame.Rect(menu_button_start_x, 900, cell_width_title, cell_height_menu)
    if from_index == 0:
        pygame.draw.rect(canvas, color_wash, menubuttontext_rect, )
        pygame.draw.rect(canvas, color_border, menubuttontext_rect, 1)
        canvas.blit(menubuttontext, menubuttontext_rect)
    else:
        pygame.draw.rect(canvas, color_wash, coffee_menu_button_text_rect, )
        pygame.draw.rect(canvas, color_border, coffee_menu_button_text_rect, 1)
        canvas.blit(coffee_menu_button_text, coffee_menu_button_text_rect)

    ### create list with dummy entries to create initial screen -
    insurer_premium_base_nested_list = []  # for table 0a
    cols_insurer = 3
    for myrows in range(0, 2):  # two row
        row = []
        for m in range(cols_insurer * mmax):
            # cellpos=str(s)+str(m)
            cellpos = ""
            row.append(cellpos)
        insurer_premium_base_nested_list.append(row)
    ### create premiums offered nested list TABLE 1
    premiums_offered_nested_list = []  # for 4 columns for each insurer , kmax rows
    cols_insurer = 4
    for s in range(0, smax + 2):  # two rows for headers
        row = []
        for m in range(cols_insurer * mmax):
            # cellpos=str(s)+str(m)
            cellpos = ""
            row.append(cellpos)
        premiums_offered_nested_list.append(row)
    ### create premiums accepted nested list table 2b
    premiums_accepted_nested_list = []  # for 2 columns for each insurer , kmax rows
    cols_insurer = 2
    s_accepted_list = int(smax * 0.6)  # contracts space needed for premiums_accepted
    for s in range(0, s_accepted_list + 2+2):  # two rows for headers + 2 rows padding
        row = []
        for m in range(0,cols_insurer * mmax):#with padding
            cellpos = ""
            row.append(cellpos)
        premiums_accepted_nested_list.append(row)
    ### create book value nested list table 3
    insurer_book_value_nested_list = []  # for 4 columns for each insurer , kmax rows
    cols_insurer = 1
    for i in range(0, 2):  # one rows for headers
        row = []
        for m in range(cols_insurer * mmax):
            # cellpos = str(m) + str(s)
            cellpos = ""
            row.append(cellpos)
        insurer_book_value_nested_list.append(row)
    ### create tables
    table0_start_y = 20  # ship data
    table0a_start_y = table0_start_y + (smax + 5) * cell_height  # for premium percentage and base book value
    table1_start_y = table0a_start_y + 4 * cell_height  # premiums offered

    table2b_start_y = table1_start_y + (smax + 6) * cell_height  # premiums accepted
    # table3_start_y = table2b_start_y + 4 * cell_height # residual book value
    table3_start_y = table2b_start_y  # same y for residual book value
    table3_start_x = 800
    cell_width_title = 200
    cell_width_t1 = size_width / (mmax * 4)
    padding_x = 3
    padding_y = 3
    x=0 # used as an index in the creation of lists
    title0_text_rect = pygame.Rect(marginx, 0, cell_width_title, cell_height)
    pygame.draw.rect(canvas, "white", title0_text_rect)
    pygame.draw.rect(canvas, color_border, title0_text_rect, 1)
    canvas.blit(title0_text, title0_text_rect)
    title1_text_rect = pygame.Rect(marginx, table1_start_y, cell_width_title, cell_height)
    table1_start_y = table1_start_y + 1 * cell_height
    pygame.draw.rect(canvas, "white", title1_text_rect)
    pygame.draw.rect(canvas, color_border, title1_text_rect, 1)
    canvas.blit(title1_text, title1_text_rect)
    ### 12 Table structure
    ### create table 0
    ship_list_nested = []
    ship_list_nested_with_title = []


    for i in range(len(ship_list_selected)):
        ship_list_nested.append(
            [ship_list_selected[i].ship_name, ship_list_selected[i].port, ship_list_selected[i].destination,
             ship_list_selected[i].tons,
             ship_list_selected[i].age, ship_list_selected[i].place_of_build, ship_list_selected[i].hull_condition,
             ship_list_selected[i].rig_condition,
             round(ship_list_selected[i].revenue_out), round(ship_list_selected[i].revenue_in),
             round(ship_list_selected[i].ship_value), round(ship_list_selected[i].ship_repair),
             ship_list_selected[i].haul,
             ship_list_selected[i].place_of_build_preference,
             round(ship_list_selected[i].ship_premium), ship_list_selected[i].ship_insurer])
    for i in range(len(ship_list_selected)):
        ship_list_nested_with_title.append(
            [ship_list_selected[i].ship_name, ship_list_selected[i].port, ship_list_selected[i].destination,
             ship_list_selected[i].tons,
             ship_list_selected[i].age, ship_list_selected[i].place_of_build, ship_list_selected[i].hull_condition,
             ship_list_selected[i].rig_condition,
             round(ship_list_selected[i].revenue_out), round(ship_list_selected[i].revenue_in),
             round(ship_list_selected[i].ship_value), round(ship_list_selected[i].ship_repair),
             ship_list_selected[i].haul,
             ship_list_selected[i].place_of_build_preference,
             round(ship_list_selected[i].ship_premium), ship_list_selected[i].ship_insurer])
    title_list1 = ["Ship Name", "Port ", "Destination", "Tons", "Age", "Place ", "Hull", "Rig ", "Revenue ", "Revenue",
                   "Cost of ", "Cost of"]
    title_list2 = ["", "of Origin", "", "", "", "of build", "condition", "condition", " going", "returning", "of build",
                   "of repair/refit"]

    ship_list_nested_with_title.insert(0, title_list2)
    ship_list_nested_with_title.insert(0, title_list1)
    table_start_x = 5
    subroutines.draw_grid_tjh(canvas, ship_list_nested_with_title, cell_width_t1, cell_height, padding_x, padding_y,
                              table0_start_y, table_start_x, 20, 2, 0)

    ### create table 0a on initial book value and premium percentage
    for m in range(0, mmax):
        insurer_premium_base_nested_list[0][m * 3 + 1] = "Initial Book Value"
        insurer_premium_base_nested_list[0][m * 3 + 2] = "Premium %"
        for x in range(0, 3):
            insurer_premium_base_nested_list[1][m * 3 + x] = local_data.insurer_premium_data[m][x]
        #premium_annual=local_data.insurer_premium_data[m][2]
        if m==2: #my algo
            if local_data.myalgo_premium == 0:
                premium_annual = local_data.insurer_premium_data[m][x]
            else:
                premium_annual = float(local_data.myalgo_premium)
                insurer_premium_base_nested_list[1][m * 3 + 2] = premium_annual

        title0a_text_rect = pygame.Rect(marginx, table0a_start_y, cell_width_title, cell_height)
        cell_width_t0a = cell_width_t1
        subroutines.draw_grid_tjh(canvas, insurer_premium_base_nested_list, cell_width_t0a, cell_height,
                                  padding_x,
                                  padding_y,
                                  table0a_start_y, table_start_x, 20, 2, 0)
    ### create table 1
    for m in range(0, mmax):
        premiums_offered_nested_list[0][m * 4] = local_data.insurer_data[m][0]
        premiums_offered_nested_list[1][m * 4] = "Ships"
        premiums_offered_nested_list[1][m * 4 + 1] = "Risk Factor"
        premiums_offered_nested_list[1][m * 4 + 2] = "Book factor"
        premiums_offered_nested_list[1][m * 4 + 3] = "Premium"
        for x in range(1, 4):
            premiums_offered_nested_list[0][m * 4 + x] = ""

    subroutines.draw_grid_tjh(canvas, premiums_offered_nested_list, cell_width_t1, cell_height, padding_x, padding_y,
                              table1_start_y, table_start_x, 20, 2, 0)

    ### create table 2b
    for m in range(0, mmax):
        premiums_accepted_nested_list[0][m * 2] = local_data.insurer_data[m][0]
        premiums_accepted_nested_list[1][m * 2] = "Ships"
        premiums_accepted_nested_list[1][m * 2 + 1] = "Premium"

        for x in range(1, 2):
            premiums_accepted_nested_list[0][m * 2 + x] = ""
    title2_text_rect = pygame.Rect(marginx, table2b_start_y, cell_width_title, cell_height)
    table2b_start_y = table2b_start_y + cell_height
    pygame.draw.rect(canvas, "white", title2_text_rect)
    pygame.draw.rect(canvas, color_border, title2_text_rect, 1)
    canvas.blit(title2_text, title2_text_rect)
    # cell_width_t2=size_width/(mmax*2)
    cell_width_t2 = cell_width_t1

    subroutines.draw_grid_with_blanks(canvas, premiums_accepted_nested_list, cell_width_t2, cell_height, padding_x,
                                      padding_y,
                                      table2b_start_y + cell_height, table_start_x, 20, 2, 0, color_bg="white")

    ###create table 3 residual book value
    title3_text_rect = pygame.Rect(table3_start_x, table3_start_y, cell_width_title, cell_height)
    table3_start_y = table3_start_y + cell_height  # to make room after title
    pygame.draw.rect(canvas, "white", title3_text_rect)
    pygame.draw.rect(canvas, color_border, title3_text_rect, 1)
    canvas.blit(title3_text, title3_text_rect)

    for m in range(0, mmax):
        insurer_book_value_nested_list[0][m] = local_data.insurer_data[m][0]  # insurer name
        insurer_book_value_nested_list[1][m] = insurers_list[m].initial_book_value
    cell_width_t3 = cell_width_t1
    subroutines.draw_grid_with_blanks(canvas, insurer_book_value_nested_list, cell_width_t3, cell_height, padding_x,
                                      padding_y,
                                      table3_start_y + cell_height, table3_start_x, 20, 2, 0, color_bg="white")
    window.blit(canvas, (0, 0))
    pygame.display.update()
    ### CREATE LIST OF SHIPS IN PREFERENCE ORDER FOR EACH INSURER ##
    for m in range(len(local_data.insurer_data)):
        preference_list = []
        ship_sorted_list = []
        preference_list = []
        clist=[]
        if m==2 and len(local_data.inspref_list)>0:
           for x in range(1,len(local_data.inspref_list)):
                    item=(subroutines.reverse_lookup(local_data.insurer_data_labels, local_data.inspref_list[x]))
                    if item is None:
                        item=(clist[0])
                    clist.append(item)
        else:
            for x in range(1,len(local_data.insurer_data[m])):
                    clist.append(local_data.insurer_data[m][x])

        for jx in range (len(clist),5):
            clist.append(clist[0])

        ship_sorted_list = sorted(ship_list_nested,
                                 key=lambda x: (x[clist[0]], x[clist[1]], x[clist[2]], x[clist[3]], x[clist[4]]))  # does for each insurer ]m'

        ### create preference list of ships for each insurer
        for s in range(len(ship_sorted_list)):
            insurers_list[m].preference_list.append(
                ship_sorted_list[s][
                    0])  ### the preferences of each insurer are listed ship name by ship name for insurer m
        ####LOAD TABLE 1 WITH INITIAL INSURER PREFERENCES
        for s in range(0, smax):
            ship_name = ship_sorted_list[s][0]
            premiums_offered_nested_list[s + 2][m * 4] = ship_name
            risk_factor = 1 + s * 0.1
            premiums_offered_nested_list[s + 2][m * 4 + 1] = round(risk_factor, 1)

            premium_annual=insurers_list[m].percent_premium
            if m==2: #myalgo
                if local_data.myalgo_premium==0:
                    premium_annual=(insurers_list[m].percent_premium)
                else:
                    premium_annual=float(local_data.myalgo_premium)
            for mo in range(0, mmax):  # to reset remaining book values at start of bidding round
                insurers_list[mo].insurer_reset(mo)
                print("282  m,remaining book value",m, insurers_list[mo].remaining_book_value)

            book_factor = round(insurers_list[m].initial_book_value / insurers_list[m].remaining_book_value, 2)
            print ("285 m",m,"book factor",book_factor,"initial/remaining book value",insurers_list[m].initial_book_value,insurers_list[m].remaining_book_value)
            premiums_offered_nested_list[s + 2][m * 4 + 2] = book_factor
            ship_value = ship_sorted_list[s][10]

            premium_offer = round(ship_value * risk_factor * book_factor * (premium_annual / 100))

            premiums_offered_nested_list[s + 2][m * 4 + 3] = premium_offer
            subroutines.draw_grid_with_blanks(canvas, premiums_offered_nested_list, cell_width_t1, cell_height,
                                              padding_x,
                                              padding_y, table1_start_y, table_start_x, 20, 2, 0, color_bg="white")
    window.blit(canvas, (0, 0))
    pygame.display.update()
    pygame.time.delay(5000)
    end_of_bidding = False
    ### START BIDDING ROUNDS
    m = 0
    insurer_not_list = []

    for mx in range(0, mmax):
        if mx != m:
            insurer_not_list.append(mx)  # FIND THE TWO INSURERS WHO ARE NOT IN THE CURRENT BIDDING ROUND FOR INSURER m
    s = 0  ### to pick up just first line in premiums offered nested list , and always pick from top
    round_count = 0
    accepted_total=0
    while accepted_total<smax:
        print("-----------------------------------------------------------------")
        #print ("line 305 at start of accepted total<smax - accepted total", accepted_total, "smax",smax)
        accepted=0

        while accepted!=2 or accepted_total<=smax:
            ship_name = premiums_offered_nested_list[s + 2][m * 4]
            premium_offered = premiums_offered_nested_list[s + 2][m * 4 + 3]
            insurer_name=insurers_list[m].insurer_name
            print("line 311 in accepted!=2 or accepted_total<smax ", "ship_name", ship_name, "m", m,"premium offered", premium_offered,"accepted",accepted,"accepted_total",accepted_total)
            subroutines.draw_grid_with_name_and_insurer(canvas, premiums_offered_nested_list, cell_width_t1, cell_height,
                                                padding_x,
                                                padding_y,
                                                table1_start_y, table_start_x, 20, 2, 0, ship_name,insurer_name)
            window.blit(canvas, (0, 0))
            pygame.display.update()
            srepl_list = []
            tries = 0
            pygame.time.delay(1000)
            ### CHECK THAT OTHER INSURERS HAVE NOT GIVEN A BETTER OFFER ###
            for mothernumb in range(0, len(insurer_not_list)):
                mother = insurer_not_list[mothernumb]  # retrieve each other insurer in turn
                print("insurer not list",insurer_not_list,"mother",mother )
                for smother in range(0, smax):
                    if premiums_offered_nested_list[smother + 2][m * 4] != "":  # finds length of current offered list
                        smothermax = smother+1

                for sdown in range (0,smothermax):
                    ship_name_other = premiums_offered_nested_list[sdown + 2][mother * 4]
                    #print("line 330 ship_name_other",ship_name_other,"sdown",sdown)
                    if ship_name == ship_name_other:
                        print("335 - m",m, "mother", mother, "sdown", sdown, "ship_name_other", ship_name_other,"premium offered other", premiums_offered_nested_list[sdown + 2][mother * 4 + 3])
                        tries += 1
                        premium_offered_other = premiums_offered_nested_list[sdown + 2][mother * 4 + 3]
                        if premium_offered <= premium_offered_other:
                            if premium_offered < insurers_list[m].remaining_book_value:
                                    accepted += 1  # two acceptances required for each other insurer, there is a better premium in the other insurer
                                    srepl_list.append(sdown) # place in list of ships in unsuccessful insurer
                                    print(" in line 339 insurer m wins once over other insurer - m", m,"other insurer -mother",mother, "premium offered", premium_offered, "ship name",ship_name,"accepted",accepted, "other insurer",mother)
                                    saccept=s
                        break
            if accepted !=2: # for all sdowns in other insurers there is a better premium
                if tries >= 2:
                    print("347 fail on s",s,"m",m)
                    fail_round=True
                    accepted=0
            else: # accepted == 2:
                print(" in line 349 accepted", accepted, "ship name", ship_name, "premium offered", premium_offered, "Insurer",m)
                fail_round=False
                accepted = 0  # to stop double counting

                accepted_total += 1  # to count that all ships have been covered
                premiums_accepted_nested_list[0 + round_count + 2][m * 2] = ship_name
                premiums_accepted_nested_list[0 + round_count + 2][m * 2 + 1] = premium_offered
                insurers_list[m].premiums_income_accum+= premium_offered  # oop
                insurers_list[m].remaining_book_value = insurers_list[m].remaining_book_value - premium_offered  # oop
                insurers_list[m].ships_insured_list.append(ship_name)
                ### FIND SUCCESSFUL SHIP IN SHIP LIST SELECTED TO UPDATE INSURED DATA
                for sfind in range(0, len(ship_list_selected)):
                    if ship_list_selected[sfind].ship_name == ship_name:
                        ship_list_selected[sfind].ship_insurer = insurers_list[m].insurer_name
                        ship_list_selected[sfind].ship_premium = premium_offered
                        break
                for mo in range(0, mmax):
                    insurers_list[mo].insurer_update
                #print("369 insurers book value nested list",insurer_book_value_nested_list)
                subroutines.draw_grid_tjh(canvas, insurer_book_value_nested_list, cell_width_t3, cell_height, padding_x,
                                          padding_y,
                                          table3_start_y + cell_height, table3_start_x, 20, 2, 0)
                window.blit(canvas, (0, 0))
                pygame.display.update()
                ### MOVE LIST ONE UP IN OFFERED LIST TO FILL SPACE OF SUCCESSFUl SHIP ACCEPTED ###
                for srepl in range(saccept, smax-1):
                    ship_name_below = premiums_offered_nested_list[srepl + 2 + 1][m * 4]
                    if ship_name_below != "":
                        for sv in range(0, smax):
                            ship_name_search = ship_sorted_list[sv][0]
                            if ship_name_below == ship_name_search:
                                ship_value_below = ship_sorted_list[sv][10]
                                book_factor = round(insurers_list[m].initial_book_value / insurers_list[m].remaining_book_value, 2)
                                if book_factor >3:
                                    book_factor = 3
                                risk_factor = premiums_offered_nested_list[srepl + 2 + 1][m * 4 + 1]
                                premium_below = round(ship_value_below * risk_factor * book_factor * (premium_annual / 100))
                                print("389 m",m,"ship_name_below",ship_name_below,"premium_below", premium_below)
                                break
                    else:
                        book_factor=""
                        ship_name_below=""
                        risk_factor=""
                        premium_below=0
                    premiums_offered_nested_list[srepl + 2][m * 4 + 2] = book_factor
                    premiums_offered_nested_list[srepl + 2][m * 4 + 1] = risk_factor
                    premiums_offered_nested_list[srepl + 2][m * 4] = ship_name_below
                    premiums_offered_nested_list[srepl + 2][m * 4 + 3] = premium_below
                premiums_offered_nested_list[smax+1][m * 4 + 3] = 0
                premiums_offered_nested_list[smax+1][m * 4 + 2] = ""
                premiums_offered_nested_list[smax+1][m * 4 + 1] = ""
                premiums_offered_nested_list[smax+1][m * 4] = ""

                                ### REMOVE FROM LIST OF UNSUCCESSFUL INSURERS AND MOVE ONE UP
                for mnotnumb in range(0, len(insurer_not_list)):
                    mnot = insurer_not_list[mnotnumb]
                    print("408 remove rom list of unsuccessful insurers - mnotnumber",mnotnumb,"mnot",mnot,"len srepl_list",len(srepl_list), "insurer not list",insurer_not_list)
                    print("409 srepl_list ",srepl_list)
                    sfromrepl=srepl_list[mnotnumb]  ## srepl_list stores number in list of ship in unsuccessful insurer
                    #for sreplother in range(sfromrepl, smax-1):
                    for sreplother in range(sfromrepl, smax):
                        print("413 sreplother",sreplother,"sfromrepl",sfromrepl)
                        if sreplother>=smax-1:
                            print("415 at print blank - sreplother",sreplother)
                            premiums_offered_nested_list[sreplother + 2][mnot * 4 + 2] = "" # book factor at end of list
                            premiums_offered_nested_list[sreplother + 2][mnot * 4 + 1] = "" # risk factor
                            premiums_offered_nested_list[sreplother + 2][mnot * 4] = "" # ship name below
                            premiums_offered_nested_list[sreplother + 2][mnot * 4 + 3] = 0 # premium below
                        else:
                            ship_name_below = premiums_offered_nested_list[sreplother + 2 + 1][mnot * 4]
                            if ship_name_below != "":
                                print( "423 ship_name_below",ship_name_below, "sreplother",sreplother)
                                #premiums_offered_nested_list[sreplother + 2][mnot * 4 + 2] = book_factor# book factor
                                #premiums_offered_nested_list[sreplother + 2][mnot * 4 + 1] = risk_factor# risk factor
                                for sothermoveup in range(0, smax):
                                    ship_name_search = ship_sorted_list[sothermoveup][0]
                                    if ship_name_below == ship_name_search:
                                        ship_value_below = ship_sorted_list[sothermoveup][10]
                                        book_factor = round(insurers_list[mnot].initial_book_value / insurers_list[
                                            mnot].remaining_book_value, 2)  #
                                        risk_factor = premiums_offered_nested_list[sreplother + 2 + 1][
                                            mnot * 4 + 1]  # risk factor
                                        print("439 risk factor", risk_factor)
                                        premiums_offered_nested_list[sreplother + 2][
                                            mnot * 4 + 2] = book_factor  # book factor
                                        premiums_offered_nested_list[sreplother + 2][
                                            mnot * 4 + 1] = risk_factor  # risk factor
                                        premium_below = round(ship_value_below * risk_factor * book_factor * premium_annual / 100)
                                        premiums_offered_nested_list[sreplother + 2][mnot * 4 + 3]=premium_below
                                        premiums_offered_nested_list[sreplother + 2][
                                            mnot * 4 + 2] = book_factor
                                        premiums_offered_nested_list[sreplother + 2][mnot * 4 + 1] = risk_factor
                                        premiums_offered_nested_list[sreplother + 2][mnot * 4] = ship_name_below
                                        premiums_offered_nested_list[sreplother + 2][mnot * 4 + 3] = premium_below
                            else:
                                print("447 at print blank next - sreplother", sreplother)
                                premiums_offered_nested_list[sreplother + 2][
                                        mnot * 4 + 2] = ""  # book factor at end of list
                                premiums_offered_nested_list[sreplother + 2][mnot * 4 + 1] = ""  # risk factor
                                premiums_offered_nested_list[sreplother + 2][mnot * 4] = ""  # ship name below
                                premiums_offered_nested_list[sreplother + 2][mnot * 4 + 3] = 0  # premium below
                        #premiums_offered_nested_list[sreplother + 2][mnot * 4 + 2] = book_factor
                        #premiums_offered_nested_list[sreplother + 2][mnot * 4 + 1] = risk_factor
                        #premiums_offered_nested_list[sreplother + 2][mnot * 4] = ship_name_below
                        #premiums_offered_nested_list[sreplother + 2][mnot * 4 + 3] = premium_below

                    #premiums_offered_nested_list[smax + 1][mnot * 4] = ""
                    #premiums_offered_nested_list[smax + 1][mnot * 4 + 3] =0# premium
                    #premiums_offered_nested_list[smax + 1][mnot * 4 + 2] = ""  # book factor
                    #premiums_offered_nested_list[smax + 1][mnot * 4 + 1] = ""  # risk factor
            #print ("line 425 finished round - ship name",ship_name, "fail_round",fail_round)
            print ("------------------------------------------------------------------")
            if fail_round==False:
                m = m + 1  # ends accepted== 2
                s=0 # restart from top of table
                if m == mmax:
                    m = 0
                    round_count += 1
                insurer_not_list = []

                for mx in range(0, mmax):
                    if mx != m:
                        insurer_not_list.append(
                            mx)  # FIND THE TWO INSURERS WHO ARE NOT IN THE CURRENT BIDDING ROUND FOR INSURER m

            else:#fail round = True
                smmax=0
                for sm in range (0,smax):
                    if premiums_offered_nested_list[sm + 1][m * 4] !="": # finds length of current offered list
                        smmax=sm
                print ("443 smmax",smmax,"m",m)
                if s<smmax:
                    s+=1
                    fail_round=False
                else:
                    m = m + 1
                    s=0
                    fail_round=False
                    if m == mmax:
                        m = 0
                        round_count += 1
                    insurer_not_list = []
            for mo in range(0, mmax):
                insurers_list[mo].insurer_update(mo)
                insurer_book_value_nested_list[1][mo] = insurers_list[mo].remaining_book_value
            subroutines.draw_grid_with_name(canvas, premiums_offered_nested_list, cell_width_t1, cell_height,
                                                padding_x, padding_y,
                                                table1_start_y, table_start_x, 20, 2, 0, ship_name)
            subroutines.draw_grid_with_blanks(canvas, premiums_accepted_nested_list, cell_width_t2, cell_height,
                                                  padding_x, padding_y,
                                                  table2b_start_y, table_start_x, 20, 2, 0, color_bg="white")
            subroutines.draw_grid_tjh(canvas, insurer_book_value_nested_list, cell_width_t3, cell_height, padding_x,
                                          padding_y,
                                          table3_start_y + cell_height, table3_start_x, 20, 2, 0)

            window.blit(canvas, (0, 0))
            pygame.display.update()
            #pygame.time.delay(30000)

            if accepted_total >= smax:
                print ("at end of bidding")
                end_of_bidding = True
                break

    running = True
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                if from_index == 0:
                    menubutton_clicked = True if menubuttontext_rect.collidepoint(event.pos) else False
                    if menubutton_clicked == True:
                        from ...core.main import main_menu
                        main_menu()
                else:
                    coffee_menu_button_clicked = True if coffee_menu_button_text_rect.collidepoint(event.pos) else False
                    if coffee_menu_button_clicked == True:

                        from_key=1 # indicates coming from premiums_alt
                        goinside.goinside_sub(window, canvas, from_key)


