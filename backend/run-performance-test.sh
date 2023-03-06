#!/bin/sh
export PYTHONUNBUFFERED=1
echo "Activating venv ..."
. venv/Scripts/activate
echo "Running performance tests ..."
python -m cProfile -o performance.prof tests/performance_test.py
snakeviz performance.prof
