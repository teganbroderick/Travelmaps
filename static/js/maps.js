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
    zoom: 13,
    mapTypeId: 'roadmap'
  });

  // CENTER MAP
  //find coordinates of last active place added, center map on those coordinates
  //If there are no places added yet, center map on SF
  function centerMap(response) {
    console.log(response)
      var center_coords = {lat: response.latitude, lng: response.longitude};
      map.setCenter(center_coords)
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
            
            <form action="/map/${map_id}/delete" method="POST">
            <input id="google-places-id" type="hidden" name="google_places_id" value="${marker.place_id}">
            <input id="delete-button "type="submit" value="Delete location from map">
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
  }

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

    // Clear out the old markers. NB MIGHT WANT TO TURN THIS OFF
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
      // Code to use if opening hours are added back into the info window
      // if (marker.opening_hours == undefined) {
      //   var markerOpeningHours = 'opening hours not available'
      // } else {
      //   var markerOpeningHours = marker.opening_hours.weekday_text
      // }

      const markerInfo = (`
        <div id="infowindow-content">
          <p id="marker_heading" class="title">${marker.title}</p>
          <p>
            Address: ${marker.address}<br>
            Website: ${markerWebsite} <br>
            Types: ${marker.types}<br>
            Google Places ID: ${marker.place_id}<br>
            Latitude: ${marker.position.lat()} <br>
            Longitude: ${marker.position.lng()}
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
            Notes: <textarea id="user-notes" name="user_notes" cols="50" rows="4" maxlength="300"></textarea> <br>
            <input id="submit-button "type="submit" value="Add location to map">
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

    // //ajax call to save places to the database without reloading the window
    // //NOT WORKING
    // function handleSavePlaceRequest(evt) {
    //   evt.preventDefault();
      
      // const formData = {
      //   latitiude: $('#latitude-field').val(),
      //   longitude: $('#longitude-field').val(),
      //   title: $('#title-field').val(),
      //   map_id: $('#map-id-field').val()
      //   website: $('#website-id-field').val()
      //   opening_hours: $('#opening-hours').val()
      //   user_notes: $('#user-notes').val()
    //   };

    //   $.get('/save_location.json', formData, makeMarkers);
    // }

    // $('#submit-button').on('submit', handleSavePlaceRequest);

}