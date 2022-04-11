import csv
import pickle

def searchAndReturnAnimes():
    with open('anime_db.csv', 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)

        id = 0; type = 1; title = 2; synopsis = 3; score = 4; eps = 5; scored_by = 6; rank = 7; pop = 8; url = 9

        animes = {}
        for line in csv_reader:
                animes[line[id]] = line[type], line[title], line[synopsis], line[score], line[eps], line[scored_by], line[rank], line[pop], line[url]
        return animes

#Create pickle files
def createPickle(output_name, variable):
    with open(f'{output_name}.pickle', 'wb') as handle:
        pickle.dump(variable, handle, protocol=pickle.HIGHEST_PROTOCOL)

# #Testing purposes
def loadPickle(filename):
    with open(f'{filename}', 'rb') as handle:
        loaded_pickle = pickle.load(handle)
    return loaded_pickle