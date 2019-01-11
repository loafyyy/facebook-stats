#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 14:50:52 2018

@author: jackie
"""

# imports
import json
import os

import numpy as np 
import matplotlib.pyplot as plt
import datetime
from itertools import islice

import re
import nltk
from nltk.book import FreqDist # for frequency distribution
from nltk.corpus import stopwords
from nltk.stem.porter import *
stemmer = PorterStemmer()

# global variables
# for formatting text files
text_spacing = 12
max_length = text_spacing



# returns the first n items of the iterable as a list
def take(n, iterable):
    return list(islice(iterable, n))

 # takes in message timestamp in ms and converts it to a date
def timestamp_to_date(timestamp):
    date = datetime.datetime.fromtimestamp(int(timestamp / 1000))
    return date.date()

# sorts a dictionary in descending order by values
def sort_dict(d):
    return sorted(d, key = d.get, reverse = True)

# helper function to write statistics to text file
def sort_dict_and_write_to_textfile(dicts, textfile, sortby):
    global max_length
    global text_spacing
    d = sortby
    d_sorted = sort_dict(d)
    for group in d_sorted: 
        textfile.write(group.ljust(max_length))
        for d in dicts:  
            textfile.write(str(d[group]).ljust(text_spacing))
        textfile.write('\n')
        
# for language processing
# function to clean text
def review_to_words(raw_review):
    # 1. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", raw_review) 
    #
    # 2. Convert to lower case, split into individual words
    words = letters_only.lower().split()
    #
    # 3. Remove Stopwords. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 4. Remove stop words
    meaningful_words = [w for w in words if not w in stops]  #returns a list 
    #
    # 5. Stem words. Need to define porter stemmer above
    singles = [stemmer.stem(word) for word in meaningful_words]
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return(" ".join(singles))  
        
# takes in list of messages where each message/element is a string
# 'top' is number of most frequent words to return
def word_freq(chat, top):
    
    # create one list of all words used
    all_words = []
    for message in chat:
        all_words = all_words + message.split()
    fdist = FreqDist(all_words)
    most_common_words = fdist.most_common(top)
    return most_common_words

        
##############################  PROGRAM STARTS HERE ##############################        

my_name = input('What is your Facebook name?\n')
rootdir = os.path.dirname(os.path.realpath(__file__)) + '/messages/inbox'

# what kind of statistics should be shown
mode_message = 'What kind of statistics do you want to see?\n' + \
             'Enter "1" for number of messages\n' + \
             'Enter "2" for messages over time with friend/group\n' + \
             'Enter "3" for language usage with friend/group\n'
             
mode = int(input(mode_message))
while mode not in [1, 2, 3]:
    print('Invalid input!!!')
    mode = int(input(mode_message))

# dictionaries with messages sent/received data
stats_messages_total = {}
stats_messages_sent = {}
stats_messages_received = {}
stats_messages_percent = {}
now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M')

# number of messages sent over time
stats_messages_over_time = {}

# for analysis on language usage
stats_my_messages = {}
stats_groups_messages = {}


# obtain messenger data from json files
for subdir, dirs, files in os.walk(rootdir):
    
    for file in files:
        
        filename = os.path.join(subdir, file)
        
        if file == 'message.json':
            
            with open(filename) as f:
                message = json.load(f)
                
                # chat title should be friend or group name, otherwise it is chat with self
                group = my_name 
                if 'title' in message:
                    group = message['title']                    
                    
                messages = message['messages']
                stats_messages_total[group] = len(messages) # count all messages in chat
                
                messages_sent_count = 0 # count number of messages sent to friend/group
                messages_received_count = 0 # count number of messages received from friend/group
                time_data = [] # number of messages per day over time
                
                my_messages = [] # messages I sent in the chat
                groups_messages = [] # messages others sent in the chat
                
                for m in messages:
                    
                    if 'sender_name' in m:
                        if m['sender_name'] == my_name:
                            messages_sent_count = messages_sent_count + 1
                            if 'content' in m:
                                my_messages.append(m['content'])
                            
                        else:
                            messages_received_count = messages_received_count + 1
                            if 'content' in m:
                                groups_messages.append(m['content'])
                    
                    # get time series data from messages
                    time = int(m['timestamp_ms'])
                    time_data.append(time)

                stats_messages_sent[group] = messages_sent_count
                stats_messages_received[group] = messages_received_count
                stats_messages_over_time[group] = time_data
                stats_my_messages[group] = my_messages
                stats_groups_messages[group] = groups_messages
                
 
# find percentage of messages sent in chat
for group in stats_messages_sent:
    message_difference = stats_messages_sent[group] - stats_messages_received[group]
    message_percent = int(round((stats_messages_sent[group] / stats_messages_total[group]) * 100))
    stats_messages_percent[group] = message_percent 


# print number of messages data to text file and display bar graph
if mode == 1:
    textfile_messages = open(now + "_stats_messages.txt", "w")
    max_length = len(max(list(stats_messages_total.keys()), key = len)) + 2
    textfile_messages.write('Group'.ljust(max_length) + 'Total'.ljust(text_spacing) + 'Sent'.ljust(text_spacing) + 'Received'.ljust(text_spacing) + 'Sent (%)'.ljust(text_spacing) + '\n')
    dicts = [stats_messages_total, stats_messages_sent, stats_messages_received, 
             stats_messages_percent]
    
    sortby_message = 'What do you want to sort by?\n' + \
             'Enter "1" for total messages\n' + \
             'Enter "2" for messages sent\n' + \
             'Enter "3" for messages received\n'
             
    sortby = int(input(sortby_message))
    
    # find how to sort statistics    
    while sortby not in [1, 2, 3]:
        print('Invalid input!!!')
        sortby = int(input(sortby_message))
        
    sortby_dict = dicts[sortby - 1]        
        
    # write statistics to text file
    sort_dict_and_write_to_textfile(dicts, textfile_messages, sortby_dict)
    
    # show figures for data
    n = 10;
    groups = take(n, sort_dict(sortby_dict))
    
    # data to plot
    sent = []
    received = []
    for group in groups:
        sent.append(stats_messages_sent[group])
        received.append(stats_messages_received[group])
    ind = np.arange(n) # the x locations for the groups
    width = 0.3 # the width of the bars
    
    p1 = plt.bar(ind, sent, width)
    p2 = plt.bar(ind, received, width, bottom = sent)
    
    title = 'total messages'
    if sortby == 1:
        title = 'total messages'
    elif sortby == 2:
        title = 'messages sent'
    elif sortby == 3:
        title = 'messages received'
        
    plt.title('Top ' + str(n) + ' chats ordered by ' + title)
    plt.ylabel('Number of messages')
    plt.xlabel('Friend/group')
    plt.xticks(ind, groups)
    plt.xticks(rotation = 90)
    plt.legend((p1[0], p2[0]), ('Sent', 'Received'))
    plt.show()
    
    # close text file
    textfile_messages.close()
    print('Check folder for text file with detailed statistics\n')
    
    
# plot time series of number of messages over time with friend/group  
elif mode == 2:
    
    message = 'Which friend/group do you want to examine?\n'
    friend_of_interest = input(message)
    while friend_of_interest not in stats_messages_over_time.keys():
        print("Can't find friend/group in your messages. Please check your spelling!!!")
        friend_of_interest = input(message)
    
    time_data = stats_messages_over_time[friend_of_interest]
    # print date of first message
    y, binEdges = np.histogram(time_data, bins = 'fd') # Freedman Diaconis Estimator for number of bins
    bincenters = binEdges[:-1]
    timecenters = [timestamp_to_date(time) for time in bincenters]
    plt.plot(timecenters, y)
    plt.xticks(rotation = 90)
    plt.xlabel('Date')
    plt.ylabel('Number of messages')
    plt.title('Messages over time with ' + friend_of_interest)
    plt.show()
    print('Your first message with ' + friend_of_interest + ' was on ' + str(timestamp_to_date(time_data[-1])))
   
    
# find top words used in chat with friend/group    
elif mode == 3:
    
    textfile_language = open(now + "_stats_language.txt", "w")
    message = 'Which friend/group do you want to examine?\n'
    friend_of_interest = input(message)
    while friend_of_interest not in stats_my_messages.keys():
        print("Can't find friend/group in your messages. Please check your spelling!!!")
        friend_of_interest = input(message)
    
    my_messages = stats_my_messages[friend_of_interest]
    friends_messages = stats_groups_messages[friend_of_interest]
                        
    # clean messenger chat text
    processed_wmn = [review_to_words(text) for text in my_messages]
    processed_wmn_friend = [review_to_words(text) for text in friends_messages]
                                
    # write to text file with top words statistics
    n = 50 # number of top words to show
    my_top_words = word_freq(processed_wmn, n)
    friends_top_words = word_freq(processed_wmn_friend, n)
    max_len_word = len(max([str(word) for word in my_top_words], key = len)) + 2
    textfile_language.write('My top words'.ljust(max_len_word))
    textfile_language.write(friend_of_interest + "'s top words")
    textfile_language.write('\n')
    for i in range(n):
        textfile_language.write(str(my_top_words[i]).ljust(max_len_word))
        textfile_language.write(str(friends_top_words[i]))       
        textfile_language.write('\n')
    print('Check folder for text file with detailed statistics\n')
    
    # close text file
    textfile_language.close()

print('Done!')