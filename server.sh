#!/bin/bash

activate() {
    . venv/bin/activate
}

echo "Entering virtual environment"
activate

echo "Using config from $CONFIG"

echo "Starting RQ server"
python3 ica/run_worker.py &

echo "Starting Flask server"
gunicorn main:app &

echo "Server listening at 127.0.0.1:8000"
