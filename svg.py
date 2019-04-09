import random, json, xml.dom.minidom, os.path
from random import randint

doc = xml.dom.minidom.parse('italy.svg')

def reset(regions):
    elements = doc.getElementsByTagName('path')

    for region in regions:
        for pathid in region.pathids:
            for i in range(len(elements)):
                if elements[i].attributes['id'].value == pathid:
                    elements[i].attributes['fill'].value = ""+ region.color 

    write(0)
    pass

def update_territory_color(new_owner, territory, round):
    elements = doc.getElementsByTagName('path')
    for pathid in territory.pathids:
        for i in range(len(elements)):
                if elements[i].attributes['id'].value == pathid:
                    elements[i].attributes['fill'].value = ""+ new_owner.color
    write(round)
    pass

def write(round):
    svg = open(os.path.join("output/", str(round)+".svg"), "w")
    svg.write(doc.toxml())
    svg.close()
    pass

def generate_colors(n):
    with open('colors.json') as json_data:
        data = json.load(json_data)
        colors = data['colors']
    return [x['hex'] for x in colors]
