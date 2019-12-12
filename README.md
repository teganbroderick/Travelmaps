# TravelMaps

TravelMaps is a full stack web application that allows users to share travel recommendations and itineraries.

TravelMaps has a custom web interface that allows users to create dynamic maps with pointers to recommended places and add place-specific notes. Users can share a dynamic, read-only version their maps using a shareable link containing a unique identifier. An internal dashboard gathers data about trends across all users, such as popular travel destinations and recommended places, and displays the data on two charts and a heat map. The application has 94% test coverage using Python unittest.

This project was made at Hackbright Academy in San Francisco over four weeks in November 2019.

### Contents

* [Technologies](#techstack)
* [Installation](#installation)
* [Features](#features)
* [Features for Version 2.0](#futurefeatures)
* [About The Developer](#aboutme)

## <a name="techstack"></a>Technologies

Tech Stack: Python, JavaScript, HTML, CSS, Flask, Jinja, jQuery, AJAX, PostgreSQL, SQLAlchemy, Bootstrap, chart.js, unittest <br>
APIs: Google Maps JavaScript, Google Maps Places

## <a name="installation"></a>Installation

### Prerequisites

You must have the following installed to run TravelMaps:

- PostgreSQL
- Python 3.x
- API key for Google Maps JavaScript and Google Maps Places APIs

### Run TravelMaps on your local computer

Clone or fork repository:
```
$ git clone https://github.com/teganbroderick/Travelmaps
```
Create and activate a virtual environment inside your travelmaps directory:
```
$ virtualenv env
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Add your API key into the header scripts in static/templates/dashboard.html, map.html, profile.html, and share_map.html, eg:
<br><br>
![api](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/YOUR_API_KEY.png)

Create database 'travelmaps':
```
$ createdb travelmaps
```
Run model.py interactively in the terminal, and create database tables:
```
$ python3 -i model.py
>>> db.create_all()
>>> quit()
```
Run the app from the command line.
```
$ python server.py
```

## <a name="features"></a>Features

![Homepage](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/homepage.png)
<br>

#### Login/Sign Up <br>

![LoginSignup](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/login_signup.gif)
<br>

#### User Profile

A list of the user's maps is shown on the left hand side of the page. If the user has not made any maps yet, they prompted to get started by clicking the "Make New Map" button. A heat map visualizing all of the users saved places is shown on the right hand side of the page. <br><br>
New User:
![new_user](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/profilepage%20new%20user.png)
<br><br>
Established User:
![established_user](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/profilepage%20established%20user.png)

#### Make Maps

Users make individual maps and can opt to add a map description.
![makemap](http://g.recordit.co/qAINFJZ0EU.gif)

#### Search and Save Places to Map

Users search for places using the Google Maps Places api. A custom marker info-window allows users to view place information, add place-specific notes, and save the place to the map.
![searchadd](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/search_add_marker.gif)
<br>

#### Navigate between list of places and map

As markers are saved, a list of saved places is displayed on the left hand side of the page. Clicking on a place header in the list centers the map on that place marker, and opens another custom info-window displaying place information and a button that deletes the place from the map. Users can also click directly on a marker to view its info-window. Clicking on a website link in the list opens the website in a new browser tab.
![Navigate](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/navigate_map.gif)
<br>

#### Delete marker

Places can be deleted from a map by clicking on the "Delete location from map" button in a saved place info-window.
![delete](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/delete_marker.gif)
<br>

#### Share map

A dynamic, read-only version of each map can be shared across the web using a shareable link.
![Sharemap](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/share_map.gif)
<br>

#### Internal dashboard

An internal dashboard is visible only to 'staff users' of the site, as defined in my data model. The dashboard shows aggregated data about trends across all users, visualized in a table, two chart.js charts, and a google maps heat map. <br>

* The bar chart shows the top 10 places saved across all maps <br>
* The donut chart shows the top five types of places (as defined by Google Maps) saved across all maps
* The heat map shows the concentration of places saved across all Maps <br>
* The table shows user statistics

![dashboard](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/internal_dashboard.gif)

#### Logout
![logout](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/logout.gif)
<br>

## <a name="futurefeatures"></a>Features for Version 2.0

* Modify data model and map permissions to allow multiple users to contribute to a single map
* Export dashboard data to an excel, csv, or jpg file
* Add dashboard page with aggregated data for each individual user

## <a name="aboutme"></a>About the Developer

TravelMaps creator Tegan Broderick is a former art conservator and museum collections manager turned software engineer. This is her first fullstack project. She can be found on [LinkedIn](https://www.linkedin.com/in/teganbroderick/) and on [Github](https://github.com/teganbroderick).
