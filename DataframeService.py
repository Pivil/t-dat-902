import os
import pandas as pd

class DataframeService:

    def getDataframeFromCsv(self):
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

    def getsavedDataframe(self):
        return pd.read_csv("./dataframes/dataframe_with_colors.csv")

    def saveDataframe(self, df):
        df.to_csv('./dataframes/dataframe_with_colors.csv', index=False)

    def getValueMap(self, df, column):
        uniq = df[column].unique()
        dict = {}
        i = 0
        for row in uniq:
            dict[row] = i
            i+=1
        dict['None'] = i
        return dict

    def splitGenre(self, genre, i):
        splitted = genre.split(',')
        if len(splitted) > i:
            return splitted[i]
        else:
            return None

    def splitColors(self, colors, i):
        splitted = colors.split(',')
        if len(splitted) > i:
            return splitted[i]
        else:
            return None

    def test(self, value, map):
        if value is None:
            return None
        return map.get(value)

    def replaceValueFromMap(self, df, column, map):
        df[column] = df[column].apply(lambda genre: self.test(genre, map))
