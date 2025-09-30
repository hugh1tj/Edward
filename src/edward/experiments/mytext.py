import pygame


mytext0 =('''This game is a simulation of Ship Insurance. It is based on the early beginnings of the insurance industry, when Edward Lloyd ran a coffee shop in London on the banks of the river Thames.
In this Basic Level there is just three Underwriters, and eight Ships and Ship Owners. One of the Underwriters is you - the player. The other Underwriters are computer players.
More advanced levels will include multiple Underwriters, Ship Owners with fleets of ships, and further development of the insurance market concept.  

The ships operate between various North Atlantic ports receiving revenue for the goods transported.During the journey there are several insurable perils: damage and even shipwrec due to hurricanes,storms, rocks, pirates, fog, icebergs,etc.
The ship owners are interested to insure against losses, and send their representatives (insurance brokers) to the Edward Lloyd's Coffeehouse to negotiate premiums. You, the player,
play the part of one of the insurers. What premium are you going to propose, and will you be prepared to negotiate. Beware - there are other insurers representatives in the Coffeehouse!''')

mytext1 = ('''This is the first in a series of educational games being developed by Hughes Consultancy and Research Ltd.
The purpose of the educational game series is to simulate real life decision making in a number of environments.
A common theme involves professional people taking educated risks.
Early versions will be developed with players working from one workstation. 
It is hoped to diversify into web based games where players can participate remotely.

Current intentions in the series are:
    1. Ship Insurance (Edward Lloyd;s Coffeehouse 1764 - This game)
    2. Property Damage Insurance in the context of crude oil exploration and production, and crude oil refining.
    3. Property Damage, Business Interruption and Liability Insurance in the context of chemicals manufacture. 
    4. Design and Operational Decisionmaking (crude oil refineries, mining ) 
    
The games are intended to be suitable as a training aid, as well as for the general enjoyment of those already familiar  with the businesses involved.
If you like the concept, and have a suggestion for a game, please write to:
        Trevor  at the following e-mail : trevor@trevorhughes.co.uk

We hope you enjoy the games and find them useful 
      Trevor, 
        for Hughes Consultancy and Research Ltd.''')

mytext2=('''Voyages take place between a number of UK ports and destination around the North Atlantic and Mediterranean. Those available for this simulation are listed to the left of the screen.
Manufactured goods such as cloth, machinery, are exported. Raw materials and foodstuffs such as sugar cane, fish etc are imported. 
For the purpose of this game the revenue received by the ship owners is estimated as 0.7 per ton for exports and 1.75 per ton for imports. ( See Sources and Historical Notes)''')

mytext3=('''Many thanks to the Caird Library at the Royal Maritime Museum, Greenwich for access to countless books and archives. 
Whilst no particular source was specifically available or copied the following sources were found particularly valuable:
Lloyds Register of Shipping
Merchant Sail by William Armstrong Fairburn, 1945
Merchant Sailing Ships 1775-1815
The cost of a 250 t ship was estimated as £ 3300. The law of six tenths was borrlwed from the chemical industry to simulate the costs of ships of other dimensions.
Exports from the americas were twice those of imports. An estimate has been made of £1.75 per tonnage for exports and 0.7 per tonnage for imports. 
 There are numerous references to ships being beached in rough weather and 'got off'. Therefore a ship which is beached is assumed to have minor damage, but delayed whlst it is pulled off.
  Ships encountering rocks are considered severely damaged. There is a chance that a ship passing through a region of hazard (storm, pirates etc) will receive damage or indeed become shipwrecked.
  No historical information was found on insurance premiums. Those used in this game tend to give the insurer a profit, but this is a game of risk!
  
  AI Generated photos and diagrams courtesy of Adobe Express/Firefly''')

mytext4=('''The above table shows typical data of interest to the insurers in Edward Lloyd's Coffeshop. 
The port and destination are considered in estimating the length and difficulty of the journeys underataken by the ship and the hazards which might be encounterred.
An older ship will be presumed to be more likely to fail en-route. Lloyds registers of the day list the condition of the rigging on a scale G,M or B (good, middling or bad)
 and the condition of the hull on a scale A,E,I,O, or U where A is the highest and U is the lowest coniditon. An estimate is indicated of the value of the exports and imports, 
 together with the cost of replacing the ship or a major rebuild. The place of build is also considered since the London underwriters considered home built ships to be more reliable.
 The ships actually used in the game are rendomly selected from the master list ''')

mytext5=('''The shortest route between two ports is calculated. For mathematically oriented readers, to programme uses the A* method, with a modification which weights cell to cell lengths
  increasing or decreasing the length according to ocean drift. It is harder sail against the Gulf Stream and much easier to sail along with the Gulf Stream for example.
  The map of the ocean drift can be displayed independently using the labelled button. The shortest path between ports is shown. Because of ocean drift influence the path to and from a particular port is different.
   Dark Blue Dots indicate route from Port to Destination, 
   Dark Red Dots indicate route from Destination to Port. 

When displaying Ocean Drift hover the mouse over each coloured zone to indicate the mapped drift type or hazard.''')


mytext6=('''The ships may encounter a variety of hazards en-route, including fog, icebergs, storms, hurricanes and pirates , depending on the location and time of year.
 A typical annual progression of hazards is shown here. Note that the speed of the simulation is greater than that of the game.''')

mytext7=('''In the game set up screen displayed at the start of the game, the number of ships and the number of insurers ( in addition to yourself) can be adjusted.
   For this demonstration screen 10 ships and 2 further insurers are used''')

mytextgoinside=('''You are greeting by Edward Lloyd himself as you enter the Coffee House. "Good Morning, Welcome to the Coffee House. 
 There are eight ships departing from these shores in the next few days. Better get circulating and make some deals. Two other insurers are already at work !!!"
 
 You look at the chronicle of ships due to sail, then adjust your risk preferences, and finally get down to offering premiums (click the buttons to the right)''')

adjust_pref=('''Click on Grid Button in table on left to change your risk preference.
Click on Grid Button below to change your % premium offer.
 Beware: Reduce your offer to gain more business, with the risk of losing money through claims,
 Increase your premium offer to gain greater income, at the risk of losing business''')

premiums_alt_error_text=("Error: You need to Offer Premiums first. Go back to Coffee House Menu")

mytext_setsail=("Sunny but cold day today. Nice sailing weather, but rumour is that storms are brewing")