# facebook-stats

## Messages.py

##### Features
1. Number of messages  
The program writes the statistics to a text file. The statistics show all the friends/groups you have messaged, the total number of messages in the chat, the number of messages you sent as well as a percentage, and the number of messages you received. You can choose to order by total messages, messages sent, or messages received. The program also displays a bar graph with your top 10 chats depending on what you choose to order by.

2. Messages over time with friend/group   
The program creates a line graph that shows the total messages over time in a chat with a particular friend/group. You can choose which friend/group to examine. The program also tells you the date of your first message with your friend/group. The dates in the graph are binned using the Freedman Diaconis Estimator.

3. Language usage with friend/group   
The program writes the statistics to a text file. The statistics show the top 50 most frequent words used for both you and your friend/group (the group's words don't include your messages). The nltk library was used to remove stop words (common words such as 'the', 'a', 'an', 'in') and the stemmer was used. Also, updates still need to be made to process messenger data, such as '[X] sent a sticker.' (i.e. 'sticker' may be in your top words used even though you didn't use that word - you just sent a lot of stickers).


##### How to use messages.py
1. Download this GitHub repository as a folder called 'facebook-stats'.  
2. Download your Facebook messenger data as a folder called 'messages'.  
    To download your Facebook messenger data:  
    a. Log into your Facebook account.  
    b. Go to 'Settings' -> 'Your Facebook Information' (3rd from the top in the menu on the left) -> 'Download Your Information'.  
    c. Set the 'Format' to 'JSON'. You can also set the 'Media Quality' to 'Low' if you want to speed up your download.  
    d. Under 'Your Information', click 'Deselect All' and only select 'Messages'. We only need Facebook messenger data for this program. However, you can download other information if you're interested.  
    e. Click 'Create File'. A zip file will be downloaded. This may take a while.  
    f. Unzip the downloaded file. Inside should be a folder called 'messages' (if the folder is called something else, make sure to rename it to 'messages'). This is the folder you need - it has all your Facebook messenger data.  
3. Place the downloaded folder from Step 2 (it should be called 'messages') into the downloaded folder from Step 1 (it should be called 'facebook-stats') . 
4. Make sure your chat folders are in facebook-stats/messages/inbox/ (you should see folders labeled with your friends' names)
5. Run messages.py



## Search.py

##### Features
1. Top searches  
The program writes the statistics to a text file. The statistics show all the friends/groups/items you have searched for and the total number of times you have searched for it. The most frequent searches appear at the top. At the top of the text file is the date of your earliest search in your search history (since you can delete your search history :0). The program also displays a line graph with your top 5 searches and the number of searches over time for these top searches. The dates are binned so that there are two bins per month.

2. Search over time for friend/group/item  
The program creates a line graph that shows the searches over time for a particular friend/group/item. You can choose which friend/group/item to examine. The program also tells you the date of your first search for your friend/group/item, as well as your earliest search in your search history (so you know the range of dates you're working with). The dates in the graph are binned using the Freedman Diaconis Estimator.

##### How to use search.py
1. Download this GitHub repository as a folder called 'facebook-stats'.
2. Download your Facebook search history data as a folder called 'search_history'.   
  To download your Facebook search history data, basically follow steps 2a. to 2f. in 'How to use messages.py', except check off 'Search History' instead of 'Messages' for step 2d. This option is under 'Information About You' near the bottom of the page. Inside the downloaded zip file should be a folder called 'search_history'. This is the folder you need - it has all your Facebook search history data.
3. Place the downloaded folder from Step 2 (it should be called 'search_history') into the downloaded folder from Step 1 (it should be called 'facebook-stats')
4. Make sure the following JSON file exists and the path is correct: facebook-stats/search_history/your_search_history.json
5. Run search.py
  
