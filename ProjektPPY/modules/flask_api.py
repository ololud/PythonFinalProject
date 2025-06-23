import json
import os

import pandas as pd
from flask import Flask, request

from ProjektPPY.modules.api_connector import add_fields_from_api
from ProjektPPY.modules.data_reader import loadingData
from ProjektPPY.modules.panda_transofrmator import panda_transformator

DATA_BACKUP = '..\\data.json'
CONFIG_FILE = '..\\config.json'

def data_loader():
    data = loadingData()
    data_cleaned = panda_transformator(data)
    data_with_api_fields = add_fields_from_api(data_cleaned)
    return data_with_api_fields

if(os.path.exists(CONFIG_FILE)):
  with open(CONFIG_FILE, "r") as config:
    config_json = json.load(config)
    print("Wczytano config file")
else:
    config_json = {"Initial": True}
    print("Brak pliku config")

if (config_json.get("Initial") == True):
    data_frame = data_loader()
    print("Rozpoczeto pobieranie i transformacje danych")
else:
    if(os.path.exists(DATA_BACKUP)):
        with open(DATA_BACKUP) as data_from_file:
            data_frame = pd.read_json(data_from_file)
            print("Odczytano dane z pliku")
    else:
        print("Brak pliku z Backupem - rozpoczeto pobieranie i transformacje danych")
        data_frame = data_loader()

data_frame.to_json(DATA_BACKUP, orient="records", indent=2)


app = Flask(__name__)

@app.route("/autor", methods=["GET"])
def ksiazki_po_autorze():
    autor_i = request.args.get("imie", "").lower()
    autor_nazwisko = request.args.get("nazwisko", "").lower()

    wyniki = data_frame[data_frame["Name"].str.lower().eq(autor_i) &
                        data_frame["Surname"].str.lower().eq(autor_nazwisko)]\
        .to_json(orient="records")

    return wyniki

@app.route("/tytul", methods=["GET"])
def ksiazki_po_tytule():
    tytul = request.args.get("tytul", "").lower()
    wyniki = data_frame[data_frame["Title"].str.lower().str.contains(tytul)].to_json(orient="records")
    return wyniki

@app.route("/", methods=["GET"])
def wszystkie_ksiazki():
    return data_frame.to_json(orient="records")



if __name__ == '__main__':
    app.run(debug=True)
