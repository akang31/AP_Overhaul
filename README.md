# Welcome to Riot API Challenge 2.0

## Description
This website is an entry to Riot's API Challenge 2.0 by Doowey and Tamepurplellamas <br/>
The purpose of this website is to compare AP Items from before and after patch 5.13, the "super mega large one that has a lot of AP item changes." It takes a look at some of the changes in item stats by analyzing hundreds of thousands of games, including item impact, item diversity, and changes in popularity and win rates of all items and champions. <br/>
The website is largely divided into three main parts - the home page, where every item is compared side-by-side; the champ page, where specific details involving how champions were impacted thanks to this change are listed; and the item page, where specific details and changes are listed. <br/>

## Running the Django server
First, go into riot2 folder.

Then run 

```
python manage.py runserver
```

Then navigate to localhost:8000/pages/index on your browser

## File structure
Under /riot2, there are two main folders to note: <br/>
/templates/pages contains all html templates (pages that are actually displayed to the user) <br/>
/pages/static contains external libraries, custom elements, and js/css files that are referenced by the html templates. 
