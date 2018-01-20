from preprocessing import parseTweets
import matplotlib.pyplot as plt

#Τhis function returns the 50 most used words and the whole list of unique wordσ
#and the times they appear in the collection and the collection's word count
def countUniqueWords(tweets):
    uniqueWords = {}
    wordCount = 0
    for tweet in tweets:            
        for word in tweet:
            wordCount += 1
            if word in uniqueWords:
                 uniqueWords[word] += 1
            else:
                 uniqueWords[word] = 1
    sortedWords = list(reversed(sorted(uniqueWords.items(), key = lambda x : x[1])))
    top50 = sortedWords[:50]
    return top50, sortedWords, wordCount

def doThePlots(collection, top50Words, words, wordC, count, zipf):
    #We display the Zipf diagram for the first 100 words, because the plot would be too crowded if we used all of the unique words and the shape of the result would not change
    allTheWords = [i[0] for i in words]
    allTheWordsC = [i[1] for i in words]
    
    wordCounts = [i[1] for i in top50Words]
    topWords = [i[0] for i in top50Words]
    
    plt.figure(1,figsize=(10,6))
    #Plotting the word count of the top 50 words
    plt.bar(topWords,wordCounts,align='center')
    plt.xticks(rotation='vertical')
    plt.title('top 50 word count for <' + collection+ '>')
    

    if zipf == True:
        #Plotting the zipf diagram curve in logarithmic scale
        plt.figure(2)
        plt.loglog(range(len(allTheWords)), allTheWordsC, linestyle='None', marker='.', label='empirical')
        plt.title('Zipf logarithmic scale for <' + collection + '>')
        #plt.legend()
    
    plt.show()
    
def main():
    
    collectionNames,collectionsWithStopwords,collectionsWithoutStopwords, dummy = parseTweets()
    print('-----------------------------------------------')
    print('Plots for collections before stopword removal' )
    print('-----------------------------------------------')
    for i,collection in enumerate(collectionsWithStopwords):    
        top50WordsWithoutStopwordRemoval, words, wordC = countUniqueWords(collection)
        doThePlots(collectionNames[i],top50WordsWithoutStopwordRemoval, words, wordC, i,True)
    print('-----------------------------------------------')
    print('Plots for collections after stopword removal' )
    print('-----------------------------------------------')
    for i,collection in enumerate(collectionsWithoutStopwords):    
        top50WordsWithStopwordRemoval, words, wordC = countUniqueWords(collection)
        doThePlots(collectionNames[i],top50WordsWithStopwordRemoval, words, wordC, i, False)

if __name__ == "__main__":
    main()