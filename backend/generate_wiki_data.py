import base64
import json
import re

import requests
from bs4 import BeautifulSoup

from model.attack_style.attack_type import AttackType
from model.attack_style.weapon_category import WeaponCategory
from weapon import Weapon
from wiki_data import WikiData


class GenerateWikiData:
    @staticmethod
    def update_special_attack_json():
        special_attack_dict = GenerateWikiData.get_special_attack_weapons()
        with open("./wiki_data/special_attack.json", "w") as outfile:
            json.dump(special_attack_dict, outfile)

    @staticmethod
    def update_gear_slot_items_list():
        gear_slot_items = {}
        seen_item_names = []

        gear_slot_items_old = WikiData.get_gear_slot_items()

        for item_id, item in WikiData.items_json.items():
            try:
                slot = str(item["slot"])

                if slot not in gear_slot_items:
                    gear_slot_items[slot] = []

                if GenerateWikiData.is_filtered_item(item, item_id):
                    print("Filtered: " + item["name"])
                    continue

                cached_item = GenerateWikiData.get_cached_item(gear_slot_items_old, slot, item_id, item["name"])
                if cached_item:
                    if item["name"] not in seen_item_names:
                        gear_slot_items[slot].append(cached_item)
                        seen_item_names.append(item["name"])
                        print("Cached: " + item["name"])
                    continue

                if item["name"] not in seen_item_names:
                    item_dict = {
                        "name": item["name"],
                        "id": int(item_id),
                    }

                    attack_styles, attack_type = GenerateWikiData.get_attack_style_and_type(item)
                    if attack_styles:
                        item_dict["attackStyles"] = attack_styles
                    if attack_type:
                        item_dict["attackType"] = attack_type

                    special_attack_cost = WikiData.get_special_attack(item["name"])
                    if special_attack_cost:
                        item_dict["specialAttackCost"] = special_attack_cost

                    item_dict["icon"] = GenerateWikiData.get_item_encoded_image(item["name"])

                    gear_slot_items[slot].append(item_dict)
                    seen_item_names.append(item["name"])
                    print("Updated: " + item["name"])
            except Exception as e:
                print("Error with id: " + str(item_id) + ", name: " + item["name"])
                print(e)

        with open("./wiki_data/gear_slot_items.json", 'w') as json_file:
            json.dump(gear_slot_items, json_file)

    @staticmethod
    def get_cached_item(gear_slot_items_old, slot, item_id, item_name):
        if slot in gear_slot_items_old:
            for item in gear_slot_items_old[slot]:
                if str(item["id"]) == item_id:
                    if item_name == item["name"]:
                        return item
                    else:
                        return None

        return None

    @staticmethod
    def is_filtered_item(item, item_id):
        # teleport charges
        if re.match(r".*\(\d+\)", item["name"]):
            return "Shayzien" not in item["name"]

        # imbued ring charges
        if re.match(r".*\(i\d+\)", item["name"]):
            return True

        # heraldic helms
        if re.match(r".*\(h\d+\)", item["name"]):
            return "(h1)" not in item["name"]

        # team capes
        if re.match(r"Team-\d+ cape", item["name"]):
            return "Team-1 cape" not in item["name"]

        # inactive bowfa id
        if item_id == "25862":
            return True

        # no r str blowpipe
        if item_id == "12924":
            return True

        if "(uncharged)" in item["name"]:
            return True

        if "Wilderness Wars" in item["name"]:
            return True

        if "unobtainable item" in item["name"]:
            return True

        if "(Last Man Standing)" in item["name"]:
            return True

        # heraldic symbol items
        if any(symbol in item["name"] for symbol in
               ["(Asgarnia)", "(Dorgeshuun)", "(Dragon)", "(Fairy)", "(Guthix)", "(HAM)", "(Horse)", "(Jogre)",
                "(Kandarin)", "(Misthalin)", "(Money)", "(Saradomin)", "(Skull)", "(Varrock)", "(Zamorak)"]):
            return True

        # graceful variants
        if any(symbol in item["name"] for symbol in
               ["(Arceuus)", "(Piscarilius)", "(Lovakengj)", "(Shayzien)", "(Hosidius)", "(Agility Arena)"]):
            return True

        # barrows item degradation
        if any(number in item["name"] for number in ["0", "25", "50", "75", "100"]):
            if any(barrows in item["name"].lower() for barrows in
                   ["ahrim", "dharok", "guthan", "karil", "torag", "verac"]):
                return True

        # nightmare zone items
        if "(nz)" in item["name"]:
            return True

        return False

    @staticmethod
    def update_unique_npcs_json():
        seen_npc_name = []
        unique_npcs = []
        for npc_id, npc in WikiData.npcs_json.items():
            if npc.get("hitpoints", 0) == 0:
                continue

            npc_key = (
                    npc["name"] + "_" +
                    str(npc.get("combat", 0)) + "_" +
                    str(npc.get("hitpoints", 0)) + "_" +
                    str(npc.get("isTobHardMode", 0)) + "_" +
                    str(len(npc))
            )
            if npc_key not in seen_npc_name:
                npc["id"] = npc_id
                unique_npcs.append(npc)
                seen_npc_name.append(npc_key)

        unique_npcs = sorted(unique_npcs, key=lambda x: x["name"])

        npcs = {"unique_npcs": unique_npcs}
        with open("./wiki_data/unique_npcs.json", 'w') as json_file:
            json.dump(npcs, json_file)

    @staticmethod
    def get_attack_style_and_type(item):
        weapon_category_name = item.get("weaponCategory", None)
        attack_styles = None
        attack_type = None

        if weapon_category_name:
            weapon_category = WeaponCategory[weapon_category_name]

            attack_styles = [style.name for style in weapon_category.value]

            if weapon_category.value[-1].attack_type == AttackType.MAGIC:
                attack_type = "magic"
            elif weapon_category.value[0].attack_type in Weapon.MELEE_TYPES:
                attack_type = "melee"
            elif weapon_category.value[0].attack_type == AttackType.RANGED:
                attack_type = "ranged"

        return attack_styles, attack_type

    @staticmethod
    def get_item_encoded_image(name):
        url_name = name.replace(' ', '_')
        url = "https://oldschool.runescape.wiki/images/" + url_name + ".png"
        url2 = "https://oldschool.runescape.wiki/images/" + url_name + "_5.png"
        try:
            response = requests.get(url)
        except Exception as e:
            print(e)
            return

        if response.status_code == 404:
            try:
                response = requests.get(url2)
            except Exception as e:
                print(e)

        img = response.content
        return base64.b64encode(img).decode('utf-8')

    @staticmethod
    def get_special_attack_weapons() -> dict:
        url = 'https://oldschool.runescape.wiki/w/Special_attacks'
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        all_tables = soup.findAll('table', {'class': 'wikitable'})

        weapons = {}
        weapon_names = []
        for table in all_tables:
            for row in table.find_all('tr'):
                header = row.find_all('th')
                if len(header) == 1:
                    a_links = header[0].find_all('a')
                    weapon_names = set([link.attrs['title'] for link in a_links])
                else:
                    cells = row.find_all('td')
                    try:
                        energy = cells[2].text.strip()
                        energy = energy.replace('%', '')
                        try:
                            energy = int(energy)
                        except ValueError:
                            break
                    except IndexError:
                        return weapons

                    for name in weapon_names:
                        weapons[name] = energy
                    break


if __name__ == '__main__':
    GenerateWikiData.update_special_attack_json()
    GenerateWikiData.update_gear_slot_items_list()
    GenerateWikiData.update_unique_npcs_json()
