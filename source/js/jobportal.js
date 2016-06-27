/*
 * jobportal.js
 * Copyleft (ↄ) 2016 kirch <kirch@arp>
 *
 * Distributed under terms of the NPL (Necessary Public License) license.
 */

// (function(window, undefined) {

// this app depends on jQuery & google maps API
var map, infowindow, directionsService, directionsRenderer, geocoder, home, markers = [];

function initialize() {
  directionsService = new google.maps.DirectionsService;
  directionsRenderer = new google.maps.DirectionsRenderer;
  geocoder = new google.maps.Geocoder();
  var opts = {
    zoom: 2,
    center: new google.maps.LatLng(0, 0),
    mapTypeControl: false,
    mapTypeId: 'map_style'
  };

  var darkMode = new google.maps.StyledMapType(
    [
      {
        "featureType": "all",
        "elementType": "labels.text.fill",
        "stylers": [
          {
            "color": "#ffffff"
          }
        ]
      },
      {
        "featureType": "all",
        "elementType": "labels.text.stroke",
        "stylers": [
          {
            "color": "#000000"
          },
          {
            "lightness": 13
          }
        ]
      },
      {
        "featureType": "administrative",
        "elementType": "geometry.fill",
        "stylers": [
          {
            "color": "#000000"
          }
        ]
      },
      {
        "featureType": "administrative",
        "elementType": "geometry.stroke",
        "stylers": [
          {
            "color": "#144b53"
          },
          {
            "lightness": 14
          },
          {
            "weight": 1.4
          }
        ]
      },
      {
        "featureType": "landscape",
        "elementType": "all",
        "stylers": [
          {
            "color": "#08304b"
          }
        ]
      },
      {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [
          {
            "color": "#0c4152"
          },
          {
            "lightness": 5
          }
        ]
      },
      {
        "featureType": "road.highway",
        "elementType": "geometry.fill",
        "stylers": [
          {
            "color": "#000000"
          }
        ]
      },
      {
        "featureType": "road.highway",
        "elementType": "geometry.stroke",
        "stylers": [
          {
            "color": "#0b434f"
          },
          {
            "lightness": 25
          }
        ]
      },
      {
        "featureType": "road.arterial",
        "elementType": "geometry.fill",
        "stylers": [
          {
            "color": "#000000"
          }
        ]
      },
      {
        "featureType": "road.arterial",
        "elementType": "geometry.stroke",
        "stylers": [
          {
            "color": "#0b3d51"
          },
          {
            "lightness": 16
          }
        ]
      },
      {
        "featureType": "road.local",
        "elementType": "geometry",
        "stylers": [
          {
            "color": "#000000"
          }
        ]
      },
      {
        "featureType": "transit.line",
        "elementType": "geometry.fill",
        "stylers": [
          {
            "color": "#146474"
          }
        ]
      },
      {
        "featureType": "water",
        "elementType": "all",
        "stylers": [
          {
            "color": "#021019"
          }
        ]
      }
    ],
    {name: "Dark"}
  );

  map = new google.maps.Map(document.getElementById('map'), opts);

  map.mapTypes.set('map_style', darkMode);
  map.setMapTypeId('map_style');

  infowindow = new google.maps.InfoWindow({maxWidth: 400});
  directionsRenderer.setMap(map);
  directionsRenderer.setOptions({suppressMarkers: true, polylineOptions: { strokeColor: "cyan" }});
  $('#search').show();
  var control = document.getElementById('search');
  control.style.left="10px";
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(control);
  $('#loading').hide();
}

function handleForm(evt) {
  evt.preventDefault();
  for ( var i in markers){
    markers[i].setMap(null);
  }
  markers = [];
  var query = $("#query").val();
  home = $("#address").val();
  codeAddress(home, function(address) {
    if (address) {
      getJobs(query, address);
    } else {
      console.log("failed coding address");
    }
  });
}

function getJobs(query, address){
  var filtered = address.filter(function(i) { return (i.types[0] == "locality"); }) || [0];
  var location = filtered[0].hasOwnProperty('long_name') ? filtered[0].long_name : '';
  $.get("http://tools.jkirchartz.com/jobportal.json?q=" + query + "&l=" + location)
  .done(function(data) {
    for (var i in data.results) {
      var markerImg = generateMarker();
      var marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(data.results[i].latitude, data.results[i].longitude),
        icon: markerImg.icon,
        shadow: markerImg.shadow
      });
      markers.push(marker);
      var mode = $('#mode').val();
      var modes = { 'TRANSIT': '&dirflg=r', 'DRIVING': '', 'WALKING': '&dirflg=w', 'BICYCING': '&dirflg=b'};
      var content = ["<div id='content'><h1 id='firstHeading' class='firstHeading'>",
        data.results[i].jobtitle,
      "</h1><div id='bodyContent'><p>",
      data.results[i].snippet,
      "</p><a href='",
      data.results[i].url,
      "' target='_blank'>View Job Posting</a>&nbsp;",
      "<a href='https://maps.google.com/?saddr=",
      home.toString().replace(/[\s()]/gi, ''),
      "&daddr=",
      data.results[i].latitude, ",", data.results[i].longitude,
      modes[mode],
      "' target='_blank'>View Directions Details</a></div>"
      ].join('');
      map.setZoom(10);
      google.maps.event.addListener(marker, 'click', (function(marker,content,infowindow) {
        return function() {
          infowindow.close();
          directions(home, marker.position, infowindow);
          infowindow.setContent(content);
          infowindow.open(map,marker);
        };
      })(marker, content, infowindow));
    }
  });
}

function generateMarker(type) {
  var pinColor;
  switch((type || '').toLowerCase()) {
    case "home":
      pinColor = "FF7569";
    break;
    default:
      pinColor = "7569FF";
    break;
  }
  var charts_api = "http://chart.apis.google.com/chart?";
  var pinImage = new google.maps.MarkerImage(charts_api + "chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
                                             new google.maps.Size(21, 34),
  new google.maps.Point(0,0),
  new google.maps.Point(10, 34));
  var pinShadow = new google.maps.MarkerImage(charts_api + "chst=d_map_pin_shadow",
                                              new google.maps.Size(40, 37),
  new google.maps.Point(0, 0),
  new google.maps.Point(12, 35));

  return { icon: pinImage, shadow: pinShadow };
}


function codeAddress(address, callback) {
  geocoder.geocode( { 'address': address }, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      home = results[0].geometry.location;
      var markerImg = generateMarker("home");
      var marker = new google.maps.Marker({
        map: map,
        position: results[0].geometry.location,
        icon: markerImg.icon,
        shadow: markerImg.shadow
      });
      markers.push(marker);
      var infowindow = new google.maps.InfoWindow({
        content: "Your Home Location"
      });
      marker.addListener('click', function() {
        infowindow.open(map,marker);
      });
      callback(results[0].address_components);
    } else {
      console.warn("Unable to retreive address", status);
      alert("Cannot retreive location, aborting job search");
      callback(false);
    }
  });
}

function directions(origin, destination, infowindow){
  var mode = $("#mode").val();
  directionsService.route(
    {
      origin: origin || home, // form's home address, if origin not defined
      destination: destination, // job posting's latlong
      travelMode: mode,
    },
    function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        directionsRenderer.setDirections(response);
        $("#bodyContent").append([" <span class=distance>",
                                 response.routes[0].legs[0].distance.text,
                                 "</span>&nbsp;<span class=duration>",
                                 response.routes[0].legs[0].duration.text,
                                 "</span>"].join(""));

      } else {
        console.warn("Unable to retreive route", status);
      }
    });
}

$(function(){
  $('form#search').submit(handleForm);
});

// }(window));
