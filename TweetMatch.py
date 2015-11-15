import random
from TwitterAPI import TwitterAPI
api = TwitterAPI('ha6n4e9gtH493V7fM8BI40ah4', 'TJNFLmXroylT0WVOohZnCAwp2gDHGWgzmnUDgKps4pKa2h42zy', '3845649433-jU8cxYET5DHYHSjzxfVwpntNYCX5ttvfUn8Fxx7', 'AOo8swxsjLhFoOUktJrlMHODVKzWjVh5KECcgU57d1Pci')
twitterData = api.request('lists/statuses', {'owner_screen_name':'samisjewish', 'slug':'TMcelebrities', 'count':'20'})

class Game:
    def __init__(self, users, tweets):
        self.users = users
        self.tweets = tweets
        self.correct_guesses = 0
        self.incorrect_guesses = 0

    def __str__(self):
        return "{0} correct guesses, {1} incorrect guesses".format(self.correct_guesses, self.incorrect_guesses)

    def remainingTweets(self):
        return len(self.tweets)

    def drawCard(self):
        return Card(self)

    def takeTurn(self):
        if self.remainingTweets() == 0:
            self.endGame()
        else:
            card = self.drawCard()
            print(card.tweet_text)
            print("(1) {0} \n(2) {1} \n(3) {2} \n(4) {3}").format(card.users[0], card.users[1], card.users[2], card.users[3])
            while True:
                guess = raw_input("Who tweeted it?  ")
                try:
                    assert int(guess) in range(1,5)
                    if card.isCorrect(int(guess)):
                        print("Correct!")
                        self.correct_guesses += 1
                    else:
                        print("Wrong!")
                        self.incorrect_guesses += 1
                    break
                except (NameError, ValueError, AssertionError):
                    print(repr(guess) + " is not a valid answer")
            self.takeTurn()


    def beginGame(self):
        self.takeTurn()

    def endGame(self):
        print(self)

class Card:
    # Each card represents a tweet and a set of users to choose from
    def __init__(self, Game):
        self.game = Game
        self.tweet = Game.tweets.pop()
        self.tweet_text = self.tweet['text']
        self.correct_user = self.tweet['user']['screen_name']
        self.users = self.chooseRandomUsers() + [self.correct_user]
        random.shuffle(self.users)

    def chooseRandomUsers(self):
        # Returns 3 random users that are not the correct_user
        users_copy = self.game.users.copy()
        users_copy.discard(self.correct_user)
        return random.sample(users_copy, 3)

    def isCorrect(self, guess):
        return self.users[guess - 1] == self.correct_user

def parseTwitterData(data):
    # returns a tuple in the form (<users>, <tweets>)
    users = set()
    tweets = []
    for tweet in twitterData:
        users.add(tweet['user']['screen_name'])
        tweets.append(tweet)
    return (users, tweets)

# Example Game
users, tweets = parseTwitterData(twitterData)
game = Game(users, tweets)
game.beginGame()
