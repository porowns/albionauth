from albion.models import Craft, PlayerCraft

t_data = []
c_data = []
buildings = ['Hunter', 'Mage', 'Warrior', 'Toolmaker']
for building in buildings:
    crafts = Craft.objects.filter(building=building)
    for craft in crafts:
        playercrafts = PlayerCraft.objects.filter(craft__item=craft).all()
        c_data.append([craft, playercrafts])
    t_data.append([building, c_data])
    c_data = []
for item in t_data:
    print(item[1])
