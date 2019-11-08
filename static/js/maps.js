"use strict";

// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.

// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

function initAutocomplete() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 37.7749295, lng: -122.41941550000001},
    zoom: 13,
    mapTypeId: 'roadmap'
  });

  // Create the search box and link it to the UI element.
  var input = document.getElementById('pac-input');
  var searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  var markers = [];
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

    //Make array to save markers
    markers = [];

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }

     //changed icon to a red marker, rather than a different icon depending on the type of place
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
        place_id: place.place_id, //added code to get the place_id, address, and types to store in db later
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

    var userMarkers = []; //array for saved user markers

    //added code to make markers with infowindows,
    // and added more object attributes to info window display
    for (const marker of markers) {
        const markerInfo = (`
          <h4>${marker.title}</h4>
          <p>
            Google Places ID: ${marker.place_id}<br>
            Address: ${marker.address}<br>
            Types: ${marker.types}<br>
            Located at: <code>${marker.position.lat()}</code>,
            <code>${marker.position.lng()}</code>
          </p>
          <form action="/map/${map_id}/save">
            <input type="submit" value="Add location to map">
            <input type="hidden" name="latitude" value="${marker.position.lat()}">
            <input type="hidden" name="longitude" value="${marker.position.lng()}">
            <input type="hidden" name="title" value="${marker.title}">
          </form> 
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
}