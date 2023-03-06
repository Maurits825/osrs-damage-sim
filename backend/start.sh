#!/bin/sh
export PYTHONUNBUFFERED=1
export FLASK_APP=damage_sim.damage_sim_server.py
. venv/Scripts/activate
flask run
