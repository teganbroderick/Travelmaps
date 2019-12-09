# TravelMaps

TravelMaps is a full stack web application that allows users to share travel recommendations and itineraries. A custom web interface allows users to create dynamic maps with pointers to recommended places, and add place-specific notes. Users can share a read-only version of their maps across the web via a map-specific url. An internal dashboard gathers data about trends across all users, such as popular travel destinations and recommended places, and displays the data on two charts and a heat map. The application has 94% test coverage using Python unittest.

This project was made at Hackbright Academy in San Francisco over four weeks in Novermber 2019.

## Contents
* [Technologies](#techstack)
* [Features](#features)
* [Features fo Version 2.0](#futurefeatures)
* [About The Developer](#aboutme)

## <a name="techstack"></a>Technologies
Tech Stack: Python, JavaScript, HTML, CSS, Flask, Jinja, jQuery, AJAX, PostgreSQL, SQLAlchemy, Bootstrap, chart.js, unittest <br>
APIs: Google Maps JavaScript, Google Maps Places

## <a name="features"></a>Features
![Homepage](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/homepage.png)
<br>

#### Login/Sign Up <br>
![LoginSignup](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/login_signup.gif)
<br>

#### User Profile
A list of the user's maps is shown on the left hand side of the page. If the user has not made any maps yet, the user is prompted to get started by clicking the "Make New Map" button. A heat map showing the concentration of all of the users saved places is shown on the right hand side of the page. <br><br>
New User:
![new_user](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/profilepage%20new%20user.png)
<br><br>
Established User:
![established_user](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/profilepage%20established%20user.png)

#### Make Maps
Users can make unlimited individual maps with optional descriptions
![makemap](http://g.recordit.co/qAINFJZ0EU.gif)

#### Search and Save Places to Map
Users search for places using the Google Maps Places api. A custom marker info-window allows users to view place information, add place-specific notes, and save the marker to the map.
![searchadd](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/search_add_marker.gif)
<br>

#### Navigate between list of places and map
As markers are saved, a list of saved places is displayed on the left hand side of the page. Clicking on a place header in the list centers the map on that place marker, and opens another custom info-window displaying place information and a button to optionally delete the place from the map. Users can also click directly on markers to view the infowindow. Clicking on a website link opens the website in a new browser tab.
![Navigate](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/navigate_map.gif)
<br>

#### Delete marker
Places can be deleted from a map by clicking on the Delete location from map button in a saved place info-window.
![delete](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/delete_marker.gif)
<br>

#### Share map
A dynamic, read-only version of each map can be shared across the web using a shareable link.
![Sharemap](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/share_map.gif)
<br>

#### Internal dashboard
An internal dashboard is visible only to ‘staff users’ of the site as defined in my data model. The dashboard shows aggregated data about trends across all users, visualized in a table, two chart.js charts, and a google maps heat map.
![dashboard](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/internal_dashboard.gif)

#### Logout
![logout](https://raw.githubusercontent.com/teganbroderick/Travelmaps/master/static/img/logout.gif)
<br>
## <a name="futurefeatures"></a>Features for Version 2.0
* Modify data model and map permissions to allow multiple users to contribute to a single map
* Export dashboard data to an excel, csv, or jpg file
* Add dashboard page with aggregated data for each individual user

## <a name="aboutme"></a>About the Developer
TravelMaps creator Tegan Broderick is a former objects conservator turned software engineer. This is her first fullstack project. She can be found on LinkedIn <a href="https://www.linkedin.com/in/teganbroderick/ ">here</a>.
