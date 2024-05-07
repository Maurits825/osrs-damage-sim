import copy
import json

def fix1(file, input_setups):
    new_input_setups = {}
    for setup_name in input_setups:
        old_input_setup = input_setups[setup_name]

        input_setup_fixed = copy.deepcopy(old_input_setup)
        input_setup_fixed["globalSettings"]["coxScaling"] = {
            "partyMaxCombatLevel": 126,
            "partyAvgMiningLevel": 99,
            "partyMaxHpLevel": 99,
            "isChallengeMode": old_input_setup["globalSettings"].get("isCoxChallengeMode", False)
        }
        try:
            del input_setup_fixed["globalSettings"]["isCoxChallengeMode"]
        except KeyError:
            pass

        input_setup_fixed["inputGearSetups"] = []
        input_setup_fixed["inputGearSetups"].append(
            {
                "gearSetupSettings": old_input_setup["inputGearSetups"][0]["gearSetupSettings"],
                "gearSetup": old_input_setup["inputGearSetups"][0]["mainGearSetup"]
            }
        )
        if isinstance(input_setup_fixed["inputGearSetups"][0]["gearSetup"]["blowpipeDarts"], int):
            input_setup_fixed["inputGearSetups"][0]["gearSetup"]["blowpipeDarts"] = {
                "id": input_setup_fixed["inputGearSetups"][0]["gearSetup"]["blowpipeDarts"]
            }

        if "expectedDps" in old_input_setup:
            del input_setup_fixed["expectedDps"]
            new_input_setups[setup_name] = {
                "expectedDps": old_input_setup["expectedDps"],
                "inputSetup": input_setup_fixed,
            }
        else:
            new_input_setups[setup_name] = {
                "inputSetup": input_setup_fixed,
            }
    with open(file, "w") as f:
        f.write(json.dumps(new_input_setups))


def fix():
    files = [
        "input_setups.json",
        "spec_input_setups.json",
        "performance_test_input_setups.json"
    ]

    for file in files:
        with open("../resources/" + file) as f:
            input_setups = json.load(f)
            fix1(file, input_setups)


def add_new_field():
    files = [
        "input_setups.json",
        "spec_input_setups.json",
        "performance_test_input_setups.json"
    ]

    for file in files:
        with open("../resources/" + file) as f:
            input_setups = json.load(f)
            new_input_setups = {}
            for setup_name in input_setups:
                old_input_setup = input_setups[setup_name]
                new_input_setups[setup_name] = old_input_setup
                new_input_setups[setup_name]["globalSettings"]["overlyDraining"] = False

        with open(file, "w") as f:
            f.write(json.dumps(new_input_setups))


fix()
#add_new_field()
