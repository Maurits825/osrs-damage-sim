#!/bin/sh
(trap 'kill 0' SIGINT; (cd ./backend ; . start.sh) & (cd ./frontend/osrs-damage-sim ; . start.sh))
