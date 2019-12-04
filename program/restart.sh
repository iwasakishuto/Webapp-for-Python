#!/bin/bash
sudo systemctl stop uwsgi.service
sudo systemctl start uwsgi.service
echo "Restarted."
