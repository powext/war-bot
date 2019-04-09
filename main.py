# Region class
class Region:
    def __init__(self, id, name, borders, color, pathids):
        # id is used for index purpose
        self.id = id
        # name exists only for communication purpose
        self.name = name
        # territories is the number of territories that the reggion currently owns
        self.territories = 1
        # alive is a flags that is false if the region is dead (it doesn't own any terrytories)
        self.alive = True
        # borders is a list that contains all ids of the neighboring regions 
        self.borders = borders
        # region color diplayed in svg
        self.color = color
        # region path ids in the svg 
        self.pathids = pathids
    
    def __str__(self):
        borders = " "
        for border in self.borders:
            borders = borders + str(border) + " "
        return "Region name: "+ self.name +" id: "+ str(self.id) +" borders: "+borders

# Territory class
class Territory:
    def __init__(self, id, name, borders, pathids):
        # id is used for index purpose
        self.id = id
        # name exists only for communication purpose
        self.name = name
        # region_id points the current region that owns this territory 
        self.region_id = id
        # borders is a list that contains all ids of the neighboring territories 
        self.borders = borders
        # region path ids in the svg 
        self.pathids = pathids
    
    def __str__(self):
        borders = " "
        for border in self.borders:
            borders = borders + str(border) + " "
        return "Territory name: "+ self.name +" id: "+ str(self.id) +" borders: "+borders

import json, svg
from random import randint

# regions is a list that contains all the regions loaded from data.json
regions = []
# territories is a list that contains all the territories loaded from data.json
territories = []
# territories_total is a variable that contains the total count of the territories 
territories_total = None
# victory is a flag that is True when the game ended
victory = False
# current round
round = 0

# loading data from data.json
with open('data.json') as json_data:
    data = json.load(json_data)
    territories_total = data['territories']

    # creating regions, territories instances
    for territory in data['regions']:
        borders = []
        pathids = []
        for border in territory['borders']: 
            borders.append(border['id'])
        
        # generating a color for each region
        colors = svg.generate_colors(50)
        region_color = colors[randint(0, 200)]

        for pathid in territory['pathids']:
            pathids.append(pathid['id'])

        regions.append(Region(territory['id'], territory['name'], borders.copy(), region_color, pathids.copy()))
        territories.append(Territory(territory['id'], territory['name'], borders.copy(), pathids.copy()))      

    # init svg
    svg.reset(regions)

    # game starts
    while not victory:

        # getting a random attacker region
        region_striker = regions[randint(1, territories_total)-1]
        print("Trovata regione: "+region_striker.name)

        if region_striker.alive:
            # attacked is a flag that is True when the attacker has attacked
            attacked = False

            # attacking
            while not attacked:

                # getting a random border from region
                if len(region_striker.borders) > 1:
                    random_border = region_striker.borders[randint(1, len(region_striker.borders))-1]
                else:
                    random_border = region_striker.borders[0]
                territory_target = territories[random_border-1]
                region_target = regions[territory_target.region_id-1]

                if region_target.id != region_striker.id:
                    attacked = True

                    # generating attacker victory possibilities
                    attacker_region_possibilities = (region_striker.territories * 100) / (region_striker.territories+region_target.territories)

                    # random attack score
                    attack = randint(1, 100)

                    if attack<=attacker_region_possibilities:
                        # updating attacker and defencer instances
                        region_striker.territories += 1
                        region_target.territories -= 1
                        territory_target.region_id = region_striker.id

                        # updating svg
                        svg.update_territory_color(region_striker, territory_target, round)

                        # updating attacker and defencer borders
                        for newborder in territory_target.borders:
                            region_striker.borders.append(newborder)

                        app = region_target.borders.copy()
                        for border in territory_target.borders:
                            for oldborder in region_target.borders:
                                if border == oldborder:
                                    app.remove(oldborder)
                                    break
                        region_target.borders = app

                        if region_target.territories == 0:
                            region_target.alive = False
                        if region_striker.territories == territories_total:
                            print("The winner is: "+region_striker.name)
                            victory = True
                        round += 1
                    else:
                        round += 1
                    