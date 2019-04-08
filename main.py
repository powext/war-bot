# Region class
class Region:
    def __init__(self, id, name, borders):
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
    
    def __str__(self):
        borders = " "
        for border in self.borders:
            borders = borders + str(border) + " "
        return "Regione nome: "+ self.name +" id: "+ str(self.id) +" borders: "+borders

# Territory class
class Territory:
    def __init__(self, id, name, borders):
        # id is used for index purpose
        self.id = id
        # name exists only for communication purpose
        self.name = name
        # region_id points the current region that owns this territory 
        self.region_id = id
        # borders is a list that contains all ids of the neighboring territories 
        self.borders = borders
    
    def __str__(self):
        borders = " "
        for border in self.borders:
            borders = borders + str(border) + " "
        return "Territorio nome: "+ self.name +" id: "+ str(self.id) +" borders: "+borders

import json
from random import randint

# regions is a list that contains all the regions loaded from data.json
regions = []
# territories is a list that contains all the territories loaded from data.json
territories = []
# territories_total is a variable that contains the total count of the territories 
territories_total = None
# victory is a flag that is True when the game ended
victory = False

# loading data from data.json
with open('data.json') as json_data:
    data = json.load(json_data)
    territories_total = data['territories']

    # loading regions, territories and borders
    for territory in data['regions']:
        borders = []
        for border in territory['borders']: 
            borders.append(border['id'])
        region = Region(territory['id'], territory['name'], borders.copy())
        regions.append(region)
        print(region)
        territory = Territory(territory['id'], territory['name'], borders.copy())
        territories.append(territory)
        print(territory)


    # game starts
    while not victory:

        # getting a random attacker region
        region_striker = regions[randint(1, territories_total)-1]
        print("Trovata regione: "+region_striker.name)

        #checking if this random attacker is still alive
        if region_striker.alive:
            print("Regione ancora in vita")
            # attacked is a flag that is True when the attacker has attacked
            attacked = False

            # attacking
            while not attacked:
                print("Cercando di attaccare")

                # getting a random border from region
                if len(region_striker.borders) > 1:
                    random_border = region_striker.borders[randint(1, len(region_striker.borders))-1]
                else:
                    random_border = region_striker.borders[0]
                territory_target = territories[random_border-1]
                region_target = regions[territory_target.region_id-1]
                print(region_striker.name+" ha scelto di attaccare: "+region_target.name+" sul territorio di: "+territory_target.name)

                if region_target.id != region_striker.id:
                    attacked = True
                    print("Attacco possibile")

                    # generating attacker victory possibilities
                    attacker_region_possibilities = (region_striker.territories * 100) / (region_striker.territories+region_target.territories)

                    # random attack score
                    attack = randint(1, 100)
                    print("Attacco: "+str(attack))

                    # checking who won
                    if attack<=attacker_region_possibilities:
                        # Cose da fare quando vince la regione attaccante
                        # - Aggiungere +1 ai territori conquistati alla regione vincente
                        # - Togliere -1 ai torritori conquistati alla regione sconfitta
                        # - Aggiungere i nuovi confini alla regione vincente
                        # - Rimuovere i vecchi confini alla regione sconfitta
                        # - Aggiornare la regione "padrona" nel territorio della battaglia

                        # attacker won
                        # updating attacker and defender
                        region_striker.territories += 1
                        region_target.territories -= 1
                        territory_target.region_id = region_striker.id

                        # adding new borders to winner attacker and removing
                        for newborder in territory_target.borders:
                            print("Aggiungo il confine: "+str(newborder)+" alla regione vincente")
                            region_striker.borders.append(newborder)

                        app = region_target.borders.copy()
                        for border in territory_target.borders:
                            for oldborder in region_target.borders:
                                if border == oldborder:
                                    print("Rimuovo il confine: "+str(oldborder)+" alla regione perdente")
                                    app.remove(oldborder)
                                    break
                        region_target.borders = app
                        # print("Regione attaccante: "+region_striker.name+" Regione difendente: "+region_target.name+" Vincente: "+region_striker.name+"\n")
                        print(region_striker)
                        print(region_target)
                        print("Attacco vincente!\n")
                        if region_target.territories == 0:
                            region_target.alive = False
                            print(region_target.name+" è stato completamente sconfitto!")
                        if region_striker.territories == territories_total:
                            print("Vince la battaglia: "+region_striker.name)
                            victory = True
                        
                    else:
                        # print("Regione attaccante: "+region_striker.name+" Regione difendente: "+region_target.name+" Vincente: "+region_target.name+"\n")
                        print("Attacco fallito!\n")
        else:
            print("Regione già eliminata\n")
                    