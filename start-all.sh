#!/bin/bash

echo "Starting system..."

# Kill old processes
pkill -f app.py
pkill -f prometheus
pkill -f alertmanager

BASE_DIR="$PWD"

# Flask App
echo "Starting Flask app (5000)..."
cd "$BASE_DIR/app"
nohup python3 app.py > app.log 2>&1 &

# Prometheus
echo "Starting Prometheus (9090)..."
cd "$BASE_DIR/prometheus"
nohup ./prometheus --config.file=prometheus.yml > prom.log 2>&1 &

# Alertmanager
echo "Starting Alertmanager (9093)..."
cd "$BASE_DIR/alertmanager"
nohup ./alertmanager --config.file=alertmanager.yml > alert.log 2>&1 &

# Webhook
echo "Starting Webhook (5001)..."
cd "$BASE_DIR/webhook"
nohup python3 app.py > webhook.log 2>&1 &

echo " All services started!"
