"use strict";

function initAutocomplete() {

  //INSTANTIATE MAP
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    mapTypeId: 'roadmap'
  });

  // CENTER MAP
  //find coordinates of last active place added, center map on those coordinates
  //If there are no places added yet, center map on SF
  function centerMap(response) {
      var centerCoords = {lat: response.latitude, lng: response.longitude};
      map.setCenter(centerCoords)
  }
 
  $.get('/get_last_place_added/', {map_id : map_id}, centerMap);
  
  //LOAD AND RENDER SAVED MARKERS
  //Array to save usermarkers
  var userMarkers = [];

  //ajax call to get place information from server.py db, add saved markers to map
  $.get('/get_places/', {map_id : map_id}, makeMarkers);

  function makeMarkers(response) {
    for (const place of response) {
      userMarkers.push(new google.maps.Marker({
        position: {
          lat: place.latitude,
          lng: place.longitude
        },
        title: place.title,
        address: place.address,
        website: place.website,
        place_types: place.place_types,
        place_id: place.google_places_id,
        user_notes: place.user_notes,
        icon: {
        url: '/static/img/map_icon_black.png', 
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(20, 20)
      },
      map: map,
      }));
    }

    //make info windows for saved markers
    //nb. need to add more columns to the db for address, types, website, opening hours, etc. 
        for (const marker of userMarkers) {
      const markerInfo = (`
        <div id="infowindow-content">
          <p id="marker_heading" class="title">${marker.title}</p>
          <p>
            Address: ${marker.address}<br>
            Website: ${marker.website} <br>
            Types: ${marker.place_types}<br>
            Google Places ID: ${marker.place_id}<br>
            Latitude: ${marker.position.lat()} <br>
            Longitude: ${marker.position.lng()}<br>
            User Notes: ${marker.user_notes}
        </div>
      `);

      const infoWindow = new google.maps.InfoWindow({
        content: markerInfo,
        height: 100,
        width: 200
      });
      
      //event listener - click on marker, open infowindow
      marker.addListener('click', () => {
        infoWindow.open(map, marker);
      });
    }

  //EVENT LISTENER for clicking on a place name in the list, opening corresponding marker info window
  $('a.place-name').on('click', function(evt) {
    evt.preventDefault();
    
    //print test strings
    console.log("User makers:", userMarkers);
    console.log("You are in the place name area");

    // get link data-name
    var placeToFind = $(this).data('name');
    console.log("Place to find: ", placeToFind);

    // find map marker in markers array with the same title
    var markerToClick;
    var markerCenterCoords;
    for (var i in userMarkers) {
      if(userMarkers[i].title === placeToFind) {
        console.log(userMarkers[i]);
        markerToClick = userMarkers[i];
        markerCenterCoords = {lat: userMarkers[i].latitude, lng: userMarkers[i].longitude};
      }
    }
    console.log(markerCenterCoords)
    //center map on coords of markerToClick
    map.setCenter(markerCenterCoords)
    //trigger click event on the markerToClick
    new google.maps.event.trigger(markerToClick, 'click');
  });

  //Add event listener for clicking on 'get sharable link' button
  $('#get-shareable-link').on('submit', () => {
    alert(window.location.href);
  })

  }
}
