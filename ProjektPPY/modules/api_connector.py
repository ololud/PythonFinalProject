import requests
from ProjektPPY.modules.data_reader import loadingData
from ProjektPPY.modules.panda_transofrmator import panda_transformator


def api_reader(title):
    adres = "https://openlibrary.org/search.json?title=" + title.replace(" ", "+")
    data = requests.get(adres)
    status = data.status_code
    if(status != 200):
        return None

    data_json = data.json()

    if(int(data_json["numFound"]) < 1):
        return None

    data_doc = data_json["docs"][0]

    data_final = {"access": data_doc["ebook_access"],
                  "edition_count": data_doc["edition_count"],
                  "first_edition": data_doc["first_publish_year"]}

    return data_final


def add_fields_from_api(data_frame):
    data_frame["ebook_access"] = None
    data_frame["edition_count"]= None
    data_frame["first_publish_year"] = None

    data_frame = panda_transformator(loadingData())
    for i, book in data_frame.iterrows():
        tytul = book.get("Title")
        row_api_data = api_reader(tytul)

        if(row_api_data is None):
            continue

        data_frame.at[i, "ebook_access"] = row_api_data.get("access")
        data_frame.at[i, "edition_count"] = row_api_data.get("edition_count")
        data_frame.at[i, "first_publish_year"] = row_api_data.get("first_edition")

    return data_frame
