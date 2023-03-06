from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_compress import Compress

from damage_sim.damage_sim_runner import DamageSimRunner
from damage_sim.damage_sim_validation import DamageSimValidation
from input_setup.gear_setup_preset import GearSetupPreset
from input_setup.input_setup_converter import InputSetupConverter
from input_setup.rl_gear_input import RlGearInput
from wiki_data import WikiData

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200", "https://maurits825.github.io"])

app.config["COMPRESS_REGISTER"] = False  # disable default compression of all eligible requests
compress = Compress()
compress.init_app(app)

damage_sim_runner = DamageSimRunner()


@app.route("/status", methods=["GET"])
def get_status():
    status = "damage-sim server is running!"
    return {"status": status}


@app.route("/gear-slot-items", methods=["GET"])
@compress.compressed()
def get_gear_slot_items():
    return WikiData().get_gear_slot_items()


@app.route("/rl-gear", methods=["GET"])
def get_rl_gear():
    rl_gear_list = RlGearInput.get_gear()

    gear = {}
    for item_id in rl_gear_list:
        for slot, gear_slot_items in WikiData.gear_slot_items.items():
            if str(item_id) in gear_slot_items:
                gear[slot] = {
                    "name": gear_slot_items[str(item_id)]["name"],
                    "id": item_id
                }

    return gear


@app.route("/gear-setup-presets", methods=["GET"])
def get_gear_setup_presets():
    return GearSetupPreset.get_gear_setup_presets()


@app.route("/all-spells", methods=["GET"])
def get_all_spells():
    return WikiData.get_all_spells()


@app.route("/npcs", methods=["GET"])
@compress.compressed()
def get_npcs():
    return WikiData().get_unique_npcs()


@app.route("/run-damage-sim", methods=["POST"])
def run_damage_sim():
    json_request = request.get_json()

    if not DamageSimValidation.validate_setup(json_request):
        return {"error": "Invalid setup"}

    input_setup = InputSetupConverter.get_input_setup(json_request)
    damage_sim_results = damage_sim_runner.run(input_setup)

    return jsonify(damage_sim_results)
