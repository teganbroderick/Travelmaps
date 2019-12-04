"use strict";

// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.

// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

function initAutocomplete() {
  //INSTANTIATE MAP
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
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
        latitude: place.latitude,
        longitude: place.longitude,
        title: place.title,
        address: place.address,
        website: place.website,
        place_types: place.place_types,
        place_id: place.google_places_id,
        user_notes: place.user_notes,
        icon: {
        url: '/static/img/map_icon_red_black.png', 
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(20, 20)
      },
      map: map,
      }));
    }

    //INITIATE INFO WINDOWS FOR SAVED MARKERS
    for (const marker of userMarkers) {
      const UserMarkerInfo = (`
        <div id="infowindow-content">
          <p id="marker_heading" class="title">${marker.title}</p>
          <p>
            Address: ${marker.address}<br>
            Website: ${marker.website} <br>
            User Notes: ${marker.user_notes}
            
            <form action="/map/${map_id}/delete" method="POST">
            <input id="google-places-id" type="hidden" name="google_places_id" value="${marker.place_id}">
            <input id="delete-button "type="submit" value="Delete location from map">
          </form> 
        </div>
      `);

      const infoWindow = new google.maps.InfoWindow({
        content: UserMarkerInfo,
        height: 100,
        width: 200
      });
      
      //event listener - click on marker, open infowindow
      marker.addListener('click', () => {
        infoWindow.open(map, marker);
      });
    }
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


  //START NEW PLACES SEARCH
  //Array to save markers created from search box searches
  var markers = [];

  // Create the search box and link it to the UI element.
  var input = document.getElementById('pac-input');
  var searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // Clear out the old markers
    markers.forEach(function(marker) {
      marker.setMap(null);
    });

    // Push a marker to the map fo each place
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }

     //define icon
      var icon = {
        url: '/static/img/map_icon.svg', 
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(30, 30)
      };

      // Create a marker for each place
      markers.push(new google.maps.Marker({
        map: map,
        icon: icon,
        title: place.name,
        website: place.website,
        opening_hours: place.opening_hours,
        place_id: place.place_id,
        address: place.formatted_address,
        types: place.types,
        position: place.geometry.location
      }));

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);  

    //ADD INFO WINDOWS FOR RENDERED SEARCH MARKERS
    for (const marker of markers) {
      if (marker.website == undefined) {
        var markerWebsite = 'website not available'
      } else {
        var markerWebsite = marker.website
      }

      const markerInfo = (`
        <div id="infowindow-content">
          <p id="marker_heading" class="title">${marker.title}</p>
          <p>
            Address: ${marker.address}<br>
            Website: ${markerWebsite} <br>
          </p>
          <form action="/map/${map_id}/save" method="POST">
            <input id="title-field" type="hidden" name="title" value="${marker.title}">
            <input id="address-field" type="hidden" name="address" value="${marker.address}">
            <input id="website_field" type="hidden" name="website" value="${markerWebsite}">
            <input id="types" type="hidden" name="types" value="${marker.types}">
            <input id="google-places-id" type="hidden" name="google_places_id" value="${marker.place_id}">
            <input id="latitude-field" type="hidden" name="latitude" value="${marker.position.lat()}">
            <input id="longitude-field" type="hidden" name="longitude" value="${marker.position.lng()}">
            <input id="map-id-field" type="hidden" name="map_id" value="${map_id}">
            Notes: <br><textarea id="user-notes" name="user_notes" cols="50" rows="4" maxlength="300"></textarea> <br>
            <input class="submit-button "type="submit" value="Add location to map">
          </form> 
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
  });
  
  // _______________________________________________________________________
    //ajax call to save places to the database without reloading the window
    //WORK IN PROGRESS
    function handleSavePlaceRequest(evt) {
      evt.preventDefault();
      console.log('You are in the handle save place request function')
      const formData = {
        title: $('#title-field').val(),
        address: $('#address-field').val(),
        website: $('#website-field').val(),
        types: $('#types').val(),
        google_places_id: $('google_places_id').val(),
        latitiude: $('#latitude-field').val(),
        longitude: $('#longitude-field').val(),
        map_id: $('#map-id-field').val(),
        user_notes: $('#user-notes').val()
      };

      $.get('/save_location.json', formData, makeMarkers);
    }

    $('form.submit-button').on('submit', handleSavePlaceRequest);

}