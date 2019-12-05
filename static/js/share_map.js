"use strict";

function initAutocomplete() {

  // INSTANTIATE MAP
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    mapTypeId: 'roadmap'
  });

  // CENTER MAP
  // Find coordinates of last active place added, center map on those coordinates
  // If there are no places added yet, center map on SF
  function centerMap(response) {
      var centerCoords = {lat: response.latitude, lng: response.longitude};
      map.setCenter(centerCoords)
  }
 
  $.get('/get_last_place_added/', {map_id : map_id}, centerMap);
  
  // LOAD AND RENDER SAVED MARKERS
  // Array to save usermarkers
  var userMarkers = [];

  // Ajax call to get place information from server.py db, make markers, add markers to map
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

    // Define info windows for saved markers
    for (const marker of userMarkers) {
      const markerInfo = (`
        <div id="infowindow-content">
          <p id="marker_heading" class="title">${marker.title}</p>
          <p>
            Address: ${marker.address}<br>
            Website: ${marker.website} <br>
            User Notes: ${marker.user_notes}
        </div>
      `);

      const infoWindow = new google.maps.InfoWindow({
        content: markerInfo,
        height: 100,
        width: 200
      });
      
      // Event listener - click on marker, open infowindow
      marker.addListener('click', () => {
        infoWindow.open(map, marker);
      });
    }

  // CLICK ON PLACE NAME IN LIST - CENTER MAP ON MARKER, OPEN INFO WINDOW
  // Event listener
  $('a.place-name').on('click', function(evt) {
    evt.preventDefault();
    
    // Get name from text in link
    var placeToFind = $(this).data('name');

    // Find map marker in markers array with the same title
    var markerToClick;
    var markerCenterCoords;
    for (var i in userMarkers) {
      if(userMarkers[i].title === placeToFind) {
        // console.log(userMarkers[i]);
        markerToClick = userMarkers[i];
        markerCenterCoords = {lat: userMarkers[i].latitude, lng: userMarkers[i].longitude};
      }
    }
    // console.log(markerCenterCoords)
    // Center map on coords of markerToClick
    map.setCenter(markerCenterCoords)
    // Trigger click event on the markerToClick
    new google.maps.event.trigger(markerToClick, 'click');
  });

  }
}
