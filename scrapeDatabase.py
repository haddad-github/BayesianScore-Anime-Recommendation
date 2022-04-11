from jikanpy import Jikan
import csv
#Database last updated: 5 April 2022

jikan = Jikan()
ani = jikan.anime

#Goes through all myanimelist.com/anime/{number} and passes if anime is not found
def writeToCSV():
    with open('anime_db.csv', 'a', newline='') as file:
        write = csv.writer(file, delimiter=",")
        for i in range(0, 52000):
            try:
                id_anime = i
                type_show = ani(i)['type']  #TV or Movie, etc.
                title = ani(i)['title']  #anime title
                syn = ani(i)['synopsis']  #synopsis
                eps = ani(i)['episodes']  #n. of episodes
                score = ani(i)['score']  #score
                scored_by = ani(i)['scored_by']  #number of raters
                rank = ani(i)['rank']  #anime's ranking
                pop = ani(i)['popularity']  #popularity
                url = f"https://myanimelist.net/anime/{id_anime}" #MAL url

                write.writerow([id_anime, type_show, title, syn, eps, score, scored_by, rank, pop, url])
                #For debugging reasons
                print(id_anime)
            except:
                pass


writeToCSV()
