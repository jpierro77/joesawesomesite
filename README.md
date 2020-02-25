# JoesAwesomeSite

JoesAwesomesite is a simple django site with purpose of providing a visible demonstration of my web development knowledge
and skill. The site currently contains two apps, RankLists and CalorieCounter, and also features contains account
creation and management features.

## Usage
JoesAwesomeSite is being hosted [here](http://45.79.200.38). Below are details for using each feature of the site.

### RankLists
RankLists allow users to list some of their favorite items of a certain topic, can be books, movies, foods etc.,
and assist the user to ranking the items without much thought. Users are then able to submit pictures of their lists to twitter. The user can also make lists that anyone can add items to and vote on.

#### Creating a ranklist:
The first box displays the RankList, and the second box is for creation of the Ranklist. The Ranklist is given a title and a type of either Personal, or Master List, and then the last input are items that are added into the list.

#### Personal Lists
Personal Lists are lists that only one user (the creator of the list) can add items to and vote on. After the user adds their items to the list, they can click the Start Vote button and vote between each item compared with every other one in the list. After voting is completed the list can be saved.

##### Posting personal lists to twitter
Personal Lists can be shared to twitter from the page they are being viewed on. Personal lists are accessed from a user's profile.

#### Master Lists
These are lists that one user initially creates and adds items to, and then any user is allowed to add items to the list, and vote afterward. Once two items are added to a master list, it can be saved.


### Calories

Calories allows users to track their food's calories against either a daily limit or requirement (depending on goal). Users can click on a 
calendar and add and edit foods they have consumed for that day. Then the daily calorie total is displayed on the calendar after the user
saves their food list.

#### Health Profile:
The first box is a health profile, which calculates the user's BMR(Basal Metabolic Rate) and daily calorie limits based on their height, 
weight, age, gender, physical activity level, and weekly weight gain or loss goal.

#### Calendar:
The second box is a calendar where the user that allows users to click on dates and add foods that they have consumed to that day. The daily
calories are added up, recorded, saved and displayed for each date the user adds foods to.

### User Accounts
In order to fully use all of the features of the site, such as saving RankLists and tracking daily food consumption, 
users can set up accounts. Only username and passwords are required to make these accounts, they are then able to customize a profile page 
as well. 


### Directories
User profiles and Master Lists are all listed on the Directories page.


## Contributing
This is an individual portfolio project


## Sources Used
### Ranklists
[Tweepy](https://www.tweepy.org/) for Twitter API

[html2canvas](https://html2canvas.hertzen.com/) for saving images to be posted to twitter

### Calories
[FullCalendar](https://fullcalendar.io/)
