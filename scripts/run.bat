@echo off
cd /d "%USERPROFILE%\TheNEWs"
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
python -m trendradar %*
