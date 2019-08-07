import requests
import json
import urllib3
from prettytable import PrettyTable

GUILD_URL = "https://swgoh.gg/api/guild/{}" # EDDP 8574 DO 52542
INTEREST_TOONS = ["DARTHMALAK","DARTHREVAN","JEDIKNIGHTREVAN","DARTHTRAYA","PADMEAMIDALA","GEONOSIANBROODALPHA","GRIEVOUS"]

def get_guild_data(guild_id):

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    get_raw = requests.get(GUILD_URL.format(guild_id), headers={"Content-Type":"application/json"}, verify=False)
    get_raw.raise_for_status()
    return get_raw.json()

def count_interest_toon(toons_map, toon_id, gear, zetas):

    key = toon_id + "#" + str(gear) + "#" + str(zetas)
    if key in toons_map:
        toons_map[key] = toons_map[key] + 1
    else:
        toons_map[key] = 1
    return toons_map

def make_pretty_table(names, quantity, gear, zetas):
    table = PrettyTable()
    table.add_column("Unit", names)
    table.add_column("Quantity", quantity)
    table.add_column("Gear", gear)
    table.add_column("Zetas", zetas)
    return table

def process(guild_id):

    response = get_guild_data(guild_id)
    toons_map = {}
    for p in response["players"]:

        for u in p["units"]:

            if u["data"]["base_id"] in INTEREST_TOONS:
                name = u["data"]["name"]
                gear = u["data"]["gear_level"]
                zetas = len(u["data"]["zeta_abilities"])
                toons_map = count_interest_toon(toons_map, name, gear, zetas)

    # print(json.dumps(toons_map, indent=4, sort_keys=True))
    guild_name = response["data"]["name"]
    print("======")
    print(guild_name)
    print("======")

    name_list = []
    quantity_list = []
    gear_list = []
    zetas_list = []
    last_name = None
    for k in sorted(toons_map.keys()):

        splitted_data = k.split("#")

        t_name = splitted_data[0]
        t_quantity = toons_map[k]
        t_gear = splitted_data[1]
        t_zetas = splitted_data[2]
        name_to_add = ""
        if t_name != last_name:
            last_name = t_name
            name_to_add = t_name

        name_list.append(name_to_add)
        quantity_list.append(t_quantity)
        gear_list.append(t_gear)
        zetas_list.append(t_zetas)
        
    print(make_pretty_table(name_list,quantity_list,gear_list,zetas_list))

if __name__ == "__main__":

    guild_1 = input("Insert Guild 1 ID: ")
    guild_2 = input("Insert Guild 2 ID: ")    
    process(guild_1)
    process(guild_2)

