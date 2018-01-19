#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from preprocessing import parseTweets
import matplotlib.pyplot as plt

#this function returns the 50 most used words and the whole list of unique word
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
    sortedWords = sorted(uniqueWords.items(), key = lambda x : x[1])
    sortedWords = list(reversed(sortedWords))
    top50 = sortedWords[:50]
    return top50, sortedWords, wordCount

def doThePlots(collection, top50Words, words, wordC, count):
    words100 = words[:100]
    allTheWords = [i[0] for i in words100]
    allTheWordsC = [i[1] for i in words100]
    
    wordCounts = [i[1] for i in top50Words]
    topWords = [i[0] for i in top50Words]
    
    plt.figure(1)
    #plotting the word count of the top 50 words
    plt.bar(topWords,wordCounts,align='center')
    plt.xticks(rotation='vertical')
    plt.title('Word Counts for <' + collection+ '>')
    
    plt.figure(2)
    #plotting the Zipf diagram
    plt.plot(range(len(allTheWords)), allTheWordsC, color='red')
    plt.title('Zipf for <' + collection + '>')

    #plotting the zipf diagram curve in loglog scale
    plt.figure(3)
    plt.loglog(range(len(allTheWords)), allTheWordsC)
    plt.title('Zipf logarithmic scale for <' + collection + '>')
    
    plt.show()
    
def main():
    
    collectionNames,collectionsWithStopwords,collectionsWithoutStopwords, dummy = parseTweets()
    print('-----------------------------------------------')
    print('Plots for collections before stopword removal' )
    print('-----------------------------------------------')
    for i,collection in enumerate(collectionsWithStopwords):    
        top50WordsWithoutStopwordRemoval, words, wordC = countUniqueWords(collection)
        doThePlots(collectionNames[i],top50WordsWithoutStopwordRemoval, words, wordC, i)
    print('-----------------------------------------------')
    print('Plots for collections after stopword removal' )
    print('-----------------------------------------------')
    for i,collection in enumerate(collectionsWithoutStopwords):    
        top50WordsWithStopwordRemoval, words, wordC = countUniqueWords(collection)
        doThePlots(collectionNames[i],top50WordsWithStopwordRemoval, words, wordC, i)

if __name__ == "__main__":
    main()

