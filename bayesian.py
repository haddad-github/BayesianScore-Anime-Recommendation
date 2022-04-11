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

#for i in bayesian_list:
    #print(i)

# x = np.linspace(0, 1, 1001)
#
# a0, b0 = (upsAvg,downsAvg)
# ranking_list = {}
# for i in range(len(animes)):
#     a = animes[i]['up'] + a0
#     b = animes[i]['down'] + a0
#     b1 = beta.pdf(x, a, b)
#     rank = beta.ppf(0.05, a, b)
#     ranking_list[animes[i]['name']] = animes[i]['up'], animes[i]['down'], round(rank, 7)
#
# skeys = sorted(ranking_list, key=lambda k: ranking_list[k][2])
# newd = {sk: ranking_list[sk] for sk in skeys}
#
# print(newd)

# # sum_rating = 31710.460000000003
# # length = 4969
# # # with open('test_db.csv', 'r') as csv_file:
# # #     csv_reader = csv.reader(csv_file)
# # #     #length = sum(1 for line in csv_file)
# # #
# # #     score = 5
# # #     scored_by = 6
# # #     for line in csv_reader:
# # #         if line[score] != "":
# # #             sum_rating += float(line[score])
# #
# # # average_rating = sum_rating/length
# # average_rating = 6.381658281344335
# # # print(sum_rating, length, average_rating)
# #
# #
# # movies_arr =[]
# #
# # sum_up = 0
# # sum_down = 0
# # with open('test_db.csv', 'r') as csv_file:
# #     csv_reader = csv.reader(csv_file)
# #
# #     title = 2; score = 5; scored_by = 6
# #
# #     for line in csv_reader:
# #         if line[score] != "" or line[scored_by] != "":
# #
# #             pseudo_upvote = (float(line[score])/10)*int(line[scored_by])
# #             pseudo_downvote = ((10-(float(line[score])))/10)*int(line[scored_by])
# #
# #             movies_arr.append([line[title],pseudo_upvote,pseudo_downvote])
# #
# #             sum_up += pseudo_upvote
# #             sum_down += pseudo_downvote
# #
# # #print(movies_arr)
# #
# # #avg_up = sum_up/length
# # #avg_down = sum_down/length
# #
# # avg_up = 16981.81303360839
# # avg_down = 5048.737177701758
# #
# # # movies_arr = [
# # #         ['Witch Hunter Robin', (7.26/10)*41227, ((10-7.26)/10 * 41227)],
# # #         ['Strike Witches', (6.97/10)*64908, ((10-6.97)/10 * 64908)],
# # #         ['Battle Spirits', (6.97/10)*1072, ((10-6.97)/10 * 1072)],
# # #         ['Megami-sama! Movie', (7.55/10)*21785, ((10-7.55)/10*21785)],
# # #         ['Lodoss-tou Senki', (7.37/10)*22052, ((10-7.37)/10*22052)],
# # #                ]
# # #
# # print(movies_arr)
# # #
# movies= [dict(zip(['name','up','down'], a)) for a in movies_arr]
# #
# x = np.linspace(0, 1, 1001)
# #
# # plt.figure(dpi = 80)
# # axes = plt.gca(frameon=False)
# #
# #
# # Prior information, movies tend to be more average and less extreme
# a0, b0 = (avg_up,avg_down)
#
# ranking_list = {}
# for i in range(len(movies)):
#     a = movies[i]['up'] + a0
#     b = movies[i]['down'] + a0
#     b1 = beta.pdf(x, a, b)
#
#     #p = axes.plot(x, b1, linewidth=0.5)
#     #p[0].set_label(f"{movies[i]['name']}  {movies[i]['up']}:{movies[i]['down']}" )
#     #axes.fill_between(x, b1, alpha=0.4)
#
#     rank = beta.ppf(0.05, a, b)
#     #axes.axvline(x=rank, ymin=0, ymax=1, color=p[0].get_color(), linewidth=1)
#
#     #print(f"{movies[i]['name']}  {movies[i]['up']}:{movies[i]['down']} rank: {rank:0.2f}")
#     ranking_list[movies[i]['name']] = movies[i]['up'], movies[i]['down'], round(rank,7)
#
# #print(ranking_list)
#
# #sortedranking = sorted(ranking_list, key=lambda x: ranking_list[x][2])
#
# skeys = sorted(ranking_list, key=lambda k: ranking_list[k][2])
# newd = {sk: ranking_list[sk] for sk in skeys}
#
# print(newd)
#
# # axes.grid(b=None, which='major', axis='both')
# #
# # if a0 > 5:
# #     axes.set_xlim(0.4, 0.8)
# #
# # plt.legend()
# # plt.show()