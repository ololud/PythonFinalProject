import json
import re
import os
import pandas as pd


def loadingData():
    foundFile = None
    DATA_FOLDER_NAME = '..\\data'
    CONFIG_FILE_PATH = "..\\config.json"

    configFile = open(CONFIG_FILE_PATH, "r", encoding="utf-8")
    config = json.load(configFile)
    formats = config['acceptable_formats']
    patterns = []
    full_data_frame = []

    for i in range(len(formats)):
        patterns.append(re.compile(formats[i]))

    for file in os.listdir(DATA_FOLDER_NAME):
        if os.path.isdir(os.path.join(DATA_FOLDER_NAME, file)):
            continue
        flaga = False
        for pattern in patterns:
            if pattern.fullmatch(file):
                flaga = True
        if not flaga:
            os.remove(os.path.join(DATA_FOLDER_NAME, file))
        else:
            foundFile = os.path.join(DATA_FOLDER_NAME, file)
            if (foundFile.endswith(".csv")):
                data_frame = pd.read_csv(foundFile)
                full_data_frame.append(data_frame)
            if (foundFile.endswith(".xlsx")):
                data_frame = pd.read_excel(foundFile)
                full_data_frame.append(data_frame)

    if full_data_frame:
        return pd.concat(full_data_frame, ignore_index=True)
    else:
        raise FileNotFoundError("Nie znaleziono prawidłowego pliku")
