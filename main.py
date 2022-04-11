from scipy.stats import beta
from lexicalField import generateLexicon
import pickle

#Load database
def loadPickle(filename):
    with open(f'{filename}', 'rb') as handle:
        loaded_pickle = pickle.load(handle)
    return loaded_pickle

#Ask user for his word and returns lexical field regarding this word
def lexicon():
    return generateLexicon(input("What are you searching for?: "))

#Returns list of animes that fit the lexicon generated
#Search every synopsis of every anime and find the animes that have those words in it
#Returns the anime in a list of dictionaries with their name, upvotes and downvotes
def getAnimeListMatchWord():
    animes_found = []
    for anime in all_anime:
        for word in words:
            if word in all_anime[anime][2].lower().split() or word in all_anime[anime][1].lower().split():
                if all_anime[anime][1] not in animes_found:
                    if (all_anime[anime][0] == 'Music' or all_anime[anime][0] == 'Unknown') or (all_anime[anime][4] == '' or all_anime[anime][5] == ''):
                        pass
                    else:

                        #Pseudo upvote and downvote generated based on the idea that, for example:
                        #A score of 8.70 with 40 000 votes would mean that 0.87 * 40 000 are upvotes and (1-0.87) * 40 000 are downvotes
                        pseudo_upvote = (float(all_anime[anime][4]) / 10) * int(all_anime[anime][5])
                        pseudo_downvote = ((10 - (float(all_anime[anime][4]))) / 10) * int(all_anime[anime][5])

                        animes_found.append([all_anime[anime][1], pseudo_upvote, pseudo_downvote])

    return [dict(zip(['name','up','down'], a)) for a in animes_found]

#Removes the duplicates from the previously generated list of dictionaries of animes that matched the words
def uniqueAnimeListMatchWord():
    duped_list = getAnimeListMatchWord()
    return [i for n, i in enumerate(duped_list) if i not in duped_list[n + 1:]]

########ONE-TIME EXECUTION########
########GETS AVERAGE UPVOTES AND DOWNVOTES FOR ALL ANIME########
def getRelevantDatabaseLength():
    length = 0
    for anime in all_anime:
        if all_anime[anime][4] == '' or all_anime[anime][5] == '':
            pass
        else:
            length += 1

    return length

def getTotalAvgScoreAndVote():
    sumScore = 0
    sumVote = 0
    for anime in all_anime:
        if all_anime[anime][4] == '' or all_anime[anime][5] == '':
            pass
        else:
            sumScore += float(all_anime[anime][4])
            sumVote += float(all_anime[anime][5])

    return sumScore/length, sumVote/length

def getTotalUpDownAvg():
    avg_up = (avgScore/10) * avgVote
    avg_down = ((10-avgScore)/10) * avgVote
    return avg_up, avg_down
########ONE-TIME EXECUTION########

#Bayesian model applied
#Returns a list of all anime with their Bayesian ranking, sorted from best(1) to worst(0)
#Source: https://towardsdatascience.com/bayesian-ranking-system-77818e63b57b
def Bayesian():
    a0, b0 = (avg_up, avg_down)

    ranking_list = {}
    for i in range(len(anime_matched)):
        a = anime_matched[i]['up'] + a0
        b = anime_matched[i]['down'] + a0
        rank = beta.ppf(0.05, a, b)
        ranking_list[anime_matched[i]['name']] = anime_matched[i]['up'], anime_matched[i]['down'], round(rank, 7)

    skeys = sorted(ranking_list, key=lambda k: ranking_list[k][2], reverse=True)
    full_dict = {sk: ranking_list[sk] for sk in skeys}

    return full_dict

#Filters the Bayesian score by a threshold (whether bigger or smaller)
def sortBayesianScore(bigger_or_smaller_than, score_threshold):

    anime_list = []

    if bigger_or_smaller_than == "bigger":
        for i in bayesianScores:
            if bayesianScores[i][2] > score_threshold:
                anime_list.append(i)

    elif bigger_or_smaller_than == "smaller":
        for i in bayesianScores:
            if bayesianScores[i][2] < score_threshold:
                anime_list.append(i)

    return anime_list

#Load anime database from pickle file
all_anime = loadPickle('anime_db_pickle.pickle')

#Load lexical field of the chosen word
words = lexicon()

#Return the list of all animes that match the chosen word's lexical field
anime_matched = uniqueAnimeListMatchWord()

#Necessary data for Bayesian model; can be hard-coded if Database is unchanged
length = getRelevantDatabaseLength() #13106
avgScore = getTotalAvgScoreAndVote()[0] #6.443580039676509
avgVote = getTotalAvgScoreAndVote()[1] #29812.569739050818
avg_up = getTotalUpDownAvg()[0] #19209.967930201175
avg_down = getTotalUpDownAvg()[1] #10602.601808849642

#Gives every anime its Bayesian score and returns the listed sorted from best(1) to worst(0)
bayesianScores = Bayesian()

#Anime matches
matches = sortBayesianScore("bigger", 0.75)


#Print lexicon to see what words it searched for
#Print final matches
print("Searched for: "+str(words))
print("Recommended: "+str(matches))
