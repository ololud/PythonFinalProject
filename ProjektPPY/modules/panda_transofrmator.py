import pandas as pd
import re

from ProjektPPY.modules.data_reader import loadingData


def panda_transformator(data_frame):

    data_frame = data_frame.dropna()

    data_frame = data_frame.loc[:, ~data_frame.columns.str.contains('internal', case=False)]

    data_frame["Name"] = data_frame["Name"].str.capitalize()
    data_frame["Surname"] = data_frame["Surname"].str.capitalize()

    pulshing_houses = ["penguin random house", "random house"]
    stephen_king_books = (data_frame["Name"] == "Stephen") & (data_frame["Surname"] == "King")
    data_frame["Publisher"] = data_frame["Publisher"].str.strip().str.lower()
    data_frame = data_frame[(data_frame["Publisher"].isin(pulshing_houses)) | stephen_king_books]

    data_frame = data_frame.drop_duplicates()

    return data_frame
