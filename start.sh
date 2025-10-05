#!/usr/bin/env bash
# Install Chrome
apt-get update
apt-get install -y wget unzip xvfb libxi6 libgconf-2-4
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb || apt-get -f install -y

# Start Flask app
export FLASK_APP=app.py
export FLASK_RUN_HOST=0.0.0.0
flask run
