from pymongo import MongoClient

MONGO_HOST='mongodb://localhost/twootdb'

client = MongoClient(MONGO_HOST)
db = client.twootdb 
collections = ['amtrak']#,'Trend2','Trend3','Trend4', 'Trend5']
sentimentLabels = { 'positive': 1, 'neutral': 0, 'negative': -1 }

def userSentiment():
    
    for collection in collections:
        cursor = db[collection].find()
        uniqueUserSentiment = []
        uniqueUserRatio = [] #follower:friend ratio
        for document in cursor:
            if document['user.id'] in uniqueUserSentiment: #we don't have to check in both dicts since both kave the unique id as key
                uniqueUserSentiment[document['user.id']] += sentimentLabels[document['label']]
            else:
                uniqueUserSentiment[document['user.id']] = sentimentLabels[document['label']]
                uniqueUserRatio[document['user.id']] = document['user.followers_count'] / document['user.friend_count']

        #User Sentiment
        print("Below is the sentiment of the users around the topic : " + collection)
        for i,user in enumerate(uniqueUserSentiment):
            print([user], user[i])

        #User follower to friend ratio
        print("Below is the follower to friend ratio of the users that posted about the topic : " + collection)
        for i,user in enumerate(uniqueUserRatio):
            print([user], user[i])    


def main():

    userSentiment()


if __name__ == "__main__":
    main()
