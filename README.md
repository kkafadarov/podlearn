# podlearn

## Environment setup
1. Make sure you have python3 installed
2. Create a `local` folder to hold your build/environment files
3. Instantiate a venv -> `python3 -m venv local/virtualenv`
4. Activate your venv -> `source local/virtualenv/bin/activate`
5. Install required packages -> `pip install -r requirements.txt`
6. Get someone to send you environment variables, then put them under `local/environment_variables.sh`

## Demo
1. Activate your virtualenv `source local/virtualenv/bin/activate`
2. Activate your environment variables `source local/environment_variables.sh`
2. Then run `python main.py`

You can also use `python listen_notes_api 'Episode Name' 'Show Name'` to play with the ListenNotes API
