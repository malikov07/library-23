#!/bin/bash
sudo ufw allow 8000
cd /home/malikov_/bekzod/library23/
source /home/malikov_/bekzod/library23/venv/bin/activate
python manage.py runserver