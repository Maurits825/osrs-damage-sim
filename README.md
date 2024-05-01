Note: This version is no longer being maintained, checkout [osrs-damage-sim-go](https://github.com/Maurits825/osrs-damage-sim-go).

[![Checks](https://github.com/Maurits825/osrs-damage-sim/actions/workflows/osrs-dmg-sim-test.yml/badge.svg)](https://github.com/Maurits825/osrs-damage-sim/actions/workflows/osrs-dmg-sim-test.yml) [![Checks](https://github.com/Maurits825/osrs-damage-sim/actions/workflows/web-app-test.yml/badge.svg)](https://github.com/Maurits825/osrs-damage-sim/actions/workflows/web-app-test.yml)

# Osrs Damage Sim
Damage simulator for OSRS with a angular web app frontend.

# Start

## Environment Setup
### Python Backend
- navigate to osrs-damage-sim/backend
- create a virtual environment `python -m venv ./venv`
- activate venv `. venv/Scripts/activate`
- install dev dependencies `pip install -r requirements/dev.txt`
- run start.sh `. start.sh`
- osrs-dmg-sim should now be [runing locally](http://127.0.0.1:5000/status)

### Angular Frontend
- navigate to osrs-damage-sim/frontend/osrs-damage-sim
- install dependencies `npm install`
- start web app `npm start`

## Run
- run `start.sh` in the root directory to start both the python flask server and the angular web app.
