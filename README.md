# Welcome to Riot API Challenge 2.0

## Description
This website is an entry to Riot's API Challenge 2.0 by Doowey and TamePurpleLlamas <br/>
The purpose of this website is to compare AP Items from before and after patch 5.13, the "super mega large one that has a lot of AP item changes." It takes a look at some of the changes in item stats by analyzing hundreds of thousands of games, including item impact, item diversity, and changes in popularity and win rates of all items and champions. <br/>
The website is largely divided into three main parts - the home page, where every item is compared side-by-side; the champ page, where specific details involving how champions were impacted thanks to this change are listed; and the item page, where specific details and changes are listed. <br/>

## Requirements
Python 2.7

Django (1.8.3)

## Running the Django server
First, go into riot2 folder.

Then run 

```
python manage.py runserver
```

Then navigate to localhost:8000/pages/index on your browser

## Brief Overview of Codebase

getData.py : The program used to scrape data from the Riot API. It requires the input of an api key along with two files NA-5.11.json and NA-5.14.json containing a json style list of match ids (for our purposes we analyzed only NA data). 

riot2/pages/views.py : All the data input for the web pages is done here. Further documentation within the file. 

riot2/templates/pages : Contains all html templates

- itemPage.html : Item Page data, at url localhost:8000/pages/itemPage/{itemID}
- champPage.html : Champ Page data, at url localhost:8000/pages/champPage/{champID}
- index.html : Starting page at url localhost:8000/pages/index
- about.html : About page at url localhost:8000/pages/about

/pages/static contains external libraries, custom elements, images, and js/css files that are referenced by the html templates. 
