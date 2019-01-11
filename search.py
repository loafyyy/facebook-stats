#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 20:26:07 2019

@author: jackie
"""

# imports
import json
import os
import numpy as np 
import matplotlib.pyplot as plt
import datetime
from itertools import islice

# returns the first n items of the iterable as a list
def take(n, iterable):
    return list(islice(iterable, n))

# takes in message timestamp in ms and converts it to a date
def timestamp_to_date(timestamp):
    date = datetime.datetime.fromtimestamp(int(timestamp))
    return date.date()

# helper function to sort dictionary by values descending, and writes statistics to text file
# inputs: d is dictionary to sort, textfile is text file to write to
def sort_dict_and_write_to_textfile(d, textfile):
    d_sorted = sorted(d, key = d.get, reverse = True)
    for group in d_sorted:
        textfile.write('%s %s \n' % (group, d[group]))
    return d_sorted



##############################  PROGRAM STARTS HERE ##############################        

# dictionary with info on searches
stats_search = {} # item searched and dates of searches
stats_search_frequency = {} # item searched and number of searches
now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M')

# open search history json file
directory = os.path.dirname(os.path.realpath(__file__)) + '/search_history'
filename = 'your_search_history.json'
filepath = os.path.join(directory, filename)
print(filepath)

# what kind of statistics should be shown
mode_message = 'What kind of statistics do you want to see?\n' + \
             'Enter "1" for top searches\n' + \
             'Enter "2" for search over time for friend/group/item\n'
             
mode = int(input(mode_message))
while mode not in [1, 2]:
    print('Invalid input!!!')
    mode = int(input(mode_message))
    
    
# get search data from json file
earliest_search = -1
with open(filepath) as f:
    search_history = json.load(f)
    searches = search_history['searches']
        
    for search in searches:
        time_searched = search['timestamp']
        
        if 'data' in search:
            person_searched = search['data'][0]['text'].lower()
            if person_searched in stats_search:
                times_searched = stats_search[person_searched]
                times_searched.append(time_searched)
            else:
                stats_search[person_searched] = [time_searched]

    earliest_search_timestamp = searches[-1]['timestamp']
    earliest_search = timestamp_to_date(earliest_search_timestamp)
    
    

# statistics for most frequent searches
if mode == 1:
    
    # find number of times searched for each search item
    for person_searched in stats_search:
        num_searches = len(stats_search[person_searched])
        stats_search_frequency[person_searched] = num_searches
        
    # write searches to text file in descending order of times searched
    text_file_1 = open(now + "_stats_search_frequency.txt", "w")
    text_file_1.write('Earliest search date: %s \n' % earliest_search)
    text_file_1.write('Search, Number of times searched\n')
    stats_search_frequency_sorted = sort_dict_and_write_to_textfile(stats_search_frequency, text_file_1)
    
    # get search history for top n searches
    num_top_searches = 5
    top_searches = take(num_top_searches, stats_search_frequency_sorted)
    
    # get min and max time for purposes of defining bins in graph
    all_times = []
    earliest = -1
    latest = -1
    for person in top_searches:
        all_times = all_times + stats_search[person]
    earliest = min(all_times)
    latest = max(all_times)
    
    # plot searches over time for top searches
    plt.figure(figsize=(8, 8)) 
    for person in top_searches:
        searches = stats_search[person]
        latest_date = timestamp_to_date(latest)
        earliest_date = timestamp_to_date(earliest)
        num_months = (latest_date.year - earliest_date.year) * 12 + latest_date.month - earliest_date.month
        y, binEdges = np.histogram(searches, bins = 2 * num_months, range = (earliest, latest))
        bincenters = binEdges[:-1]
        timecenters = [timestamp_to_date(time) for time in bincenters]
        plt.plot(timecenters, y, label = person)
    
    plt.xticks(rotation = 90)
    plt.xlabel('Date')
    plt.ylabel('Number of searches')
    plt.title('Searches over time for top ' + str(num_top_searches) + ' most frequent searches')
    plt.legend()
    plt.show()   
    
    # close text file
    text_file_1.close()
    print('Check folder for text file with detailed statistics\n')


# searches over time for person of interest
elif mode == 2:
    
    message = 'Which friend/group/item searched do you want to examine?\n'
    person_of_interest = input(message).lower()
    while person_of_interest not in stats_search.keys():
        print("Can't find friend/group/item in your searches. Please check your spelling!!!")
        person_of_interest = input(message).lower()

    searches = stats_search[person_of_interest]
    y, binEdges = np.histogram(searches, bins = 'fd') # Freedman Diaconis Estimator for number of bins
    bincenters = binEdges[:-1]
    timecenters = [timestamp_to_date(time) for time in bincenters]
    plt.plot(timecenters, y)
    plt.xticks(rotation = 90)
    plt.xlabel('Date')
    plt.ylabel('Number of searches')
    plt.title('Searches over time for ' + person_of_interest)
    plt.show()
    
    print('Earliest search date: %s' % earliest_search)
    print('First time searched for ' + person_of_interest + ': ' + str(timecenters[0]))


print('Done!')