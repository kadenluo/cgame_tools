pipenv --python 3.10
pipenv install
pipenv run pyinstaller --console --onefile --distpath ./ ./tools.py
pause
