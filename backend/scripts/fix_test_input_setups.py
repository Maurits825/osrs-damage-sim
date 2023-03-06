import json


def fix():
    with open("tests/resources/spec_input_setups.json") as f:
        input_setups = json.load(f)
        new_input_setups = {}
        for setup_name in input_setups:
            old_input_setup = input_setups[setup_name]
            old_input_setup["inputGearSetups"][0]["fillGearSetups"] = [old_input_setup["inputGearSetups"][0]["fillGearSetups"]]
            new_input_setups[setup_name] = old_input_setup

    with open("tests/resources/spec_input_setups_new.json", "w") as f:
        f.write(json.dumps(new_input_setups))


fix()
