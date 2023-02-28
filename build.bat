pipenv --python 3.10
pipenv install
pipenv run pyinstaller --noconsole --onefile --distpath ./ ./tools.py
