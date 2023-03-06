import json

from wiki_data import WikiData


GEAR_SETUP_PRESET_ICON = "./gear_setup_presets/gear_setup_presets-icons.json"


class GearSetupPreset:
    gear_setup_presets = json.load(open(GEAR_SETUP_PRESET_ICON))

    @staticmethod
    def get_gear_setup_presets():
        return GearSetupPreset.gear_setup_presets

    @staticmethod
    def generate_gear_setup_presets():
        gear_presets = []
        all_items = WikiData.items_json

        with open("./gear_setup_presets/gear.json") as json_file:
            gear_setup_presets = json.load(json_file)

        for gear_preset in gear_setup_presets:
            gear_slot = all_items[str(gear_preset["iconId"])]["slot"]
            for item in WikiData.get_gear_slot_items()[str(gear_slot)]:
                if item["id"] == gear_preset["iconId"]:
                    gear_presets.append({
                        "name": gear_preset["name"],
                        "gearIds": gear_preset["gearIds"],
                        "icon": item["icon"],
                        "attackType": gear_preset["attackType"]
                    })

        with open(GEAR_SETUP_PRESET_ICON, 'w') as json_file:
            json.dump(gear_presets, json_file)


if __name__ == '__main__':
    GearSetupPreset.generate_gear_setup_presets()
