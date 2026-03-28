#!/bin/bash

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Install system tools manually:"
echo "- Prometheus"
echo "- Alertmanager"
echo "- Grafana"
echo "- Google Cloud CLI"