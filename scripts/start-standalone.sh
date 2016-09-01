pip install -r ../requirements.txt
mongo createdb.js
cd ..
python src/stockreader.py config-standalone.toml &
