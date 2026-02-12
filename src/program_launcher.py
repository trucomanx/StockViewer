#!/usr/bin/python3

'''
## ubuntu ##
python3 -m venv venv-temporal
source venv-temporal/bin/activate
pip install --upgrade pip

## windows ##
python -m venv venv-temporal
venv-temporal\Scripts\activate
python -m pip install --upgrade pip


pip install pyinstaller pyinstaller-hooks-contrib
pip install -r requirements.txt
cd src

## windows ##
python -m PyInstaller --onefile --windowed --name stock_viewer --add-data "stock_viewer/icons;icons" --collect-all PyQt5 program_launcher.py

## ubuntu ##
python3 -m PyInstaller --onefile --windowed --name stock_viewer --add-data "stock_viewer/icons:icons" --collect-all PyQt5 program_launcher.py

'''

from stock_viewer.prog_viewer import main

if __name__ == "__main__":
    main()

