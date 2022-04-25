from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt
import csv

#######ONE-TIME PER DATABASE SCRAPE########

#Gets number of rows in database (assuming no headers)
def getDatabaseLength(file):
    num_rows = 0
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            num_rows += 1

    return num_rows

#Gets sum of a column (assuming the column has numeric values only)
def getColumnSum(file, col):
    col_sum = 0
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            if line[col] != "":
                col_sum += float(line[col])

    return col_sum

#Takes total votes and rating; creates a pseudo upvote/downvote count
def getAnimesWithUpsAndDowns(file, title, score, scored_by):
    animeArray = []

    sum_up = 0
    sum_down = 0

    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            if line[score] != "" or line[scored_by] != "":

                pseudo_upvote = (float(line[score])/10)*int(line[scored_by])
                pseudo_downvote = ((10-(float(line[score])))/10)*int(line[scored_by])

                animeArray.append([line[title],pseudo_upvote,pseudo_downvote])

                sum_up += pseudo_upvote
                sum_down += pseudo_downvote

    return [dict(zip(['name','up','down'], a)) for a in animeArray], (sum_up, sum_down)

#Gets the average pseudo upvote/downvote for all the database
def getAnimeUpDownAverage():
    up_sum = getAnimesWithUpsAndDowns('test_db.csv', 2, 5, 6)[1][0]
    down_sum = getAnimesWithUpsAndDowns('test_db.csv', 2, 5, 6)[1][1]

    avg_up = up_sum/db_length
    avg_down = down_sum/db_length

    return avg_up, avg_down

#Bayesian algorithm on a list with a specific format:
# [{'name': 'Anime Title', 'up': Upvotes, 'down': Downvotes}
def Bayesian(animeList):
    a0, b0 = (upsAvg, downsAvg)

    ranking_list = {}
    for i in range(len(animeList)):
        a = animes[i]['up'] + a0
        b = animes[i]['down'] + a0
        rank = beta.ppf(0.05, a, b)
        ranking_list[animes[i]['name']] = animes[i]['up'], animes[i]['down'], round(rank, 7)

    skeys = sorted(ranking_list, key=lambda k: ranking_list[k][2], reverse=True)
    full_dict = {sk: ranking_list[sk] for sk in skeys}

    return full_dict

db_length = getDatabaseLength('test_db.csv')
sumScore = getColumnSum('test_db.csv', 5)
sumScoredBy = getColumnSum('test_db.csv', 6)

animes = getAnimesWithUpsAndDowns('test_db.csv', 2, 5, 6)[0]

upsAvg = getAnimeUpDownAverage()[0]
downsAvg = getAnimeUpDownAverage()[1]
#######ONE-TIME PER DATABASE SCRAPE########

#Insert list with following format: [{'name': 'Anime Title', 'up': Upvotes, 'down': Downvotes},
#Already sorted by best anime to worst anime
bayesian_list = Bayesian(animes)
print(bayesian_list)
