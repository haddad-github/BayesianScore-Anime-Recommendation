# Anime recommendation with lexical field and reduced bias by using Bayesian score
##### Source of the algorithm: https://towardsdatascience.com/bayesian-ranking-system-77818e63b57b

### How it was setup
The data was scraped using all anime data from MyAnimeList, using the Jikan API (https://jikan.moe/)
That database is stored in the anime_db.csv file and in the .pickle format for direct usage

Database format: 

##### anime_ID | show type | anime name | synopsis | number of episodes | rating | number of votes | ranking | popularity | myanimelist direct link

### How it works
1) A word is provided by the user

2) That word generates a list of closest related words based on https://relatedwords.org/api/related

3) That list of closest related words (lexical field) has each of its words pluralized (using pattern3.text.en module; *needs this fix before using: https://stackoverflow.com/questions/52161349/indentationerrorexpected-an-indented-block)

4) All the words in that list are then searched through all the anime's synopsises (and title); anime that have those words are held and stored

5) The matched anime are then subjected to a Bayesian model where number of ratings is taken into count with the score (ex: A show rated 9.7 with 10 votes is not better than a show rated 8.5 with 403000 votes)

6) After the Bayesian model is applied to the anime and they all have their Bayesian score, they're sorted from biggest Bayesian score (best; closest to 1) to lowest (worst; further from 1)

7) Only anime with a Bayesian score bigger than 0.75 will appear (this can simply be changed on 127 of main.py (you can put "smaller" for smaller than and you can change the threshold value)

### Limitations
1) The lexical field generated is not always optimal (ex: "love" will generate a lexicon that includes the word "emotion", which is too vague and misleads the search)

2) Certain words with double meaning can cause issues (ex: "matter" (as in universe matter) will pick up on "it doesn't matter" and "it matters")

3) I cannot confirm for sure that the Bayesian model applied is legitimate, since I am working for a score and not upvotes/downvotes; my manipulation could be erroneous, however the results seem to be in alignment with what is expected

4) Supports one word only as an input, instead of a sentence (ex: "love" vs "love story with betrayal")

### Potential future improvements
1) Creating an entire GUI with images/link/trailer video for the recommended anime

2) Generating a better lexical field and fix double meaning issues

3) Support more than one word as input

4) Maybe try to implement Sentiment Analysis to strengthen the search's confidence and even extract the theme from the synopsis rather than naively matching words
