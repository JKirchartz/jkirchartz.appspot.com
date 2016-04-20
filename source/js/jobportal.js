/*
 * jobportal.js
 * Copyleft (ↄ) 2016 kirch <kirch@arp>
 *
 * Distributed under terms of the NPL (Necessary Public License) license.
 */


// TODO: plot jobs, chart proximities to bus lines

// (function(window, undefined) {

  // this app depends on jQuery & google maps API
  var map, geocoder, home;

  function initialize() {
    geocoder = new google.maps.Geocoder();
    var opts = {
      zoom: 8,
      center: new google.maps.LatLng(40.44, -79.99),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('map'), opts);
  }

  function handleForm(evt) {
    evt.preventDefault();
    var query = $("#query").val();
    var address = $("#address").val();
    codeAddress(address, function(address) {
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
    console.log("get jobs in ", location);
    $.get("http://tools.jkirchartz.com/jobportal.json?q=" + query + "&l=" + location)
      .done(function(data) {
        for (var item in data.results) {
          console.log(item);
          var markerImg = generateMarker();
          var marker = new google.maps.Marker({
            map: map,
            position: new google.maps.LatLng(item.latitude, item.longitude),
            icon: markerImg.icon,
            shadow: markerImg.shadow
          });
          var infowindow = new google.maps.InfoWindow({
            content: ["<div id='content'><h1 id='firstHeading' class='firstHeading'>",
              item.jobtitle,
              "</h1><div id='bodyContent'><p>",
              item.snippet,
              "</p><a href='",
              item.url,
              "' target='_blank'>View More</a></div>"
            ].join('')
          });
          marker.addListener('click', function() {
            infowindow.open(map,marker);
          });
        }
      });
  }

  function generateMarker(type) {
    var pinColor;
    switch(type.toLowerCase()) {
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
        var infowindow = new google.maps.InfoWindow({
          content: "Your home location"
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

  function directions(origin, destination){
    var directionsService = new google.maps.DirectionsService();
    var directionsRequest = {
      origin: origin || home, // form's home address, if origin not defined
      destination: destination, // job posting's latlong
      departure_time: (new Date().getTime()) / 1000, // time in seconds since epoch
      mode: google.maps.DirectionsTravelMode.TRANSIT
    };

    directionsService.route(
      directionsRequest,
      function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
          new google.maps.DirectionsRenderer({
            map: mapObject,
            directions: response
          });
        } else {
          console.warn("Unable to retreive route", status);
        }
      });
  }

  $(function(){
    $('form#search').submit(handleForm);
    $('#loading').hide();
  });

// }(window));
