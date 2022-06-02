import pymongo as pymongo
import os
import csv
import pandas as pd
from IPython.display import clear_output

from ImageService import ImageService
from ColorService import ColorService


class MongoService:
    collection = None

    def getCollection(self):
        if self.collection is None:
            client = pymongo.MongoClient("mongodb://root:root@ac-kve5mg7-shard-00-00.k1msk8b.mongodb.net:27017,ac-kve5mg7-shard-00-01.k1msk8b.mongodb.net:27017,ac-kve5mg7-shard-00-02.k1msk8b.mongodb.net:27017/?ssl=true&replicaSet=atlas-z304t2-shard-0&authSource=admin&retryWrites=true&w=majority")
            db = client["data"]
            self.collection = db["data"]

        return self.collection

    def getPandasFromCsv(self):
        list_id = []
        for dir in os.listdir("./Movie_Poster_Dataset"):
            try:
                if dir != ".DS_STORE":
                    for filename in os.listdir("./Movie_Poster_Dataset/" + dir):
                        list_id.append(filename[:-4])
            except NotADirectoryError:
                continue
        df = pd.read_csv("./IMDb movies.csv")
        return df.loc[df['imdb_title_id'].isin(list_id)]

    def getsavedPandas(self):
        return pd.read_csv("./dataframes/dataframe_with_colors.csv")

    def saveDataframe(self, df):
        df.to_csv('./dataframes/dataframe_with_colors.csv', index=True)

    def initDataFromCsv(self):
        list_id = []
        for dir in os.listdir("../Movie_Poster_Dataset"):
            try:
                if dir != ".DS_STORE":
                    for filename in os.listdir("../Movie_Poster_Dataset/" + dir):
                        list_id.append(filename[:-4])
            except NotADirectoryError:
                continue
        with open('../IMDb movies.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["imdb_title_id"] in list_id:
                    data = { "id": row["imdb_title_id"],
                             "year": row["year"],
                             "genre": row['genre']}
                    self.getCollection().insert_one(data)

    def upsert_data(self, data):
        self.getCollection().find_one_and_update(
            {"id" : data['id']},
            { "$set": {data['key'] : data['value']}}, upsert=True
        )

    def initDatabase(self):
        root_dir = "./Movie_Poster_Dataset"
        imageService = ImageService()
        colorService = ColorService()

        for dir in os.listdir(root_dir):
            if (dir == ".DS_Store"):
                continue
            size = len(os.listdir(root_dir + "/" + dir))
            i = 1
            for filename in os.listdir(root_dir + "/" + dir):
                clear_output(wait=True)
                print(str(i) + " / " + str(size) + ' (' + dir + ')')
                i += 1
                image_rgb = imageService.load_image(root_dir + "/" + dir + '/' + filename)
                main_colors = colorService.get_n_width_palette(5, image_rgb)
                main_colors_value = colorService.get_color_values(main_colors)
                main_colors_name = []
                for color in main_colors_value:
                    main_colors_name.append(colorService.convert_rgb_to_names(color))
                data = { "id": filename[:-4], "key": "main_colors", "value": main_colors_value}
                self.upsert_data(data)
                data = { "id": filename[:-4], "key": "main_colors_name", "value": main_colors_name}
                self.upsert_data(data)