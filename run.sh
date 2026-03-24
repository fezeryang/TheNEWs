#!/bin/bash
cd ~/TheNEWs
if [ -d venv ]; then
    source venv/bin/activate
fi
python -m trendradar "$@"
