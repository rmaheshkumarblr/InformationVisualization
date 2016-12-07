## Get the virtual environment setup
pip install -r requirements.txt

## Start Server - Reload Automatically on Change ##
export FLASK_APP=server.py
export FLASK_DEBUG=1
python -m flask run
