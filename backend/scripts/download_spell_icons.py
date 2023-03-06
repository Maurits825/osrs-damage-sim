import requests

from wiki_data import WikiData

all_spells = WikiData.magic_spells["all_spells"]
image_url = "https://oldschool.runescape.wiki/images/Wind_Strike.png"
for spell in all_spells:
    image_url = "https://oldschool.runescape.wiki/images/" + spell.replace(' ', '_') + ".png"
    img_data = requests.get(image_url).content
    with open("./magic_spells/" + spell + ".png", 'wb') as handler:
        handler.write(img_data)
