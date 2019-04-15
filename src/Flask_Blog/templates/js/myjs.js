// ***************************************************************** BUILD PAGE
// --------------------------------------------- Map section
var infowindow;
var infoWindow2;
var markersArray = [];

// Set up the map with desired properties
function myMap() {
  var myCenter = {lat: 53.349605, lng:-6.264175 };
  var mapCanvas = document.getElementById("map");
  var mapOptions = {center: myCenter, zoom: 14};
  var map = new google.maps.Map(mapCanvas, mapOptions);
  infowindow = new google.maps.InfoWindow({
    maxWidth: 355
  });

  testing(map);
  infoWindow2 = new google.maps.InfoWindow;

  // HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      infoWindow2.setPosition(pos);
      infoWindow2.setContent('Your Current Location');
      infoWindow2.open(map);
      map.setCenter(pos);
    }, function() {
      handleLocationError(true, infoWindow2, map.getCenter());
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow2, map.getCenter());
  }
}


function handleLocationError(browserHasGeolocation, infoWindow2, pos) {
  infoWindow2.setPosition(pos);
  infoWindow2.setContent(browserHasGeolocation ? 'Error: The Geolocation service failed.' : 'Error: Your browser doesn\'t support geolocation.');
  infoWindow2.open(map);
}


// Create listener to show marker-specific information on click
function popupDirections(marker) {
  google.maps.event.addListener(marker, 'click', function () {
    myFunction(marker.station_no);
    function myFunction(x) {
      $.getJSON($SCRIPT_ROOT + '/update', {
        post: x
      }, function(data) {
        var response=({{ data|safe }})
        var response = data;
        infowindow.setContent("Address: " + marker.addre +"<br>"+"Station No: " + response[1]+"<br>"+"Available Bikes: "+response[2]+"<br>"+"Available Bike Stands: "+response[3]);
        // Open infowindow at marker
        infowindow.open(map, marker);
      });
    }
  });
}


function testing(map) {
  $.getJSON($SCRIPT_ROOT + '/testing', {post: 0}, function(data2) {
    var response_testing= data2;
    myObj=response_testing;
    pass_data(myObj,map);
  });
}


function pass_data(myObj,map) {
  var lat=new Array(myObj.length);
  var long=new Array(myObj.length);

  // Get the list of latitude of stations
  for(var i=0;i<myObj.length;i++) {lat[i]=myObj[i][6];}
  // Get the list of longitude of stations
  for(var i=0;i<myObj.length;i++) {long[i]=myObj[i][7];}

  // Get the list of latitude and longitude of stations as a tuple
  var latlong=new Array(myObj.length);
  for(var i=0;i<myObj.length;i++) {latlong[i]=[lat[i],long[i]];}

  // Fetch the list of station names
  var address_2=new Array(myObj.length);
  var static_station_no=new Array(myObj.length);
  for(var i=0;i<myObj.length;i++) {address_2[i]=myObj[i][0];}

  // Create markers on map
  var station_num=new Array(myObj.length);
  for(var i=0;i<myObj.length;i++) {station_num[i]=myObj[i][5];}
  for(var j=0;j<latlong.length;j++) {
    var marker=new google.maps.Marker({
    position:new google.maps.LatLng(latlong[j][0],latlong[j][1]),
    map:map,
    addre:address_2[j],
    station_no:station_num[j]
    });

    popupDirections(marker);
    markersArray.push(marker);
  }
}


// Open marker infowindow if user clicks on station results
function clickMarker(stationName) {
  for (index in markersArray) {
    if (markersArray[index].addre == stationName) {
      google.maps.event.trigger(markersArray[index], 'click');
    }
  }
}


// ------------------------------ Time/weather section
// Show the current date
var today = new Date();
var day = today.getDate();
var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var month = monthNames[today.getMonth()];
var year = today.getFullYear();
var date = day + " " + month + " " + year + "<br>DUBLIN, IRELAND";
document.getElementById("date").innerHTML = date;

// Fetch real-time weather data on page load
$.getJSON("http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=a4822db1b5634c2e9e25209d1837cc69&units=metric",
  function(response_5) {
    document.getElementById("coverage").innerHTML = response_5.weather[0].main;
    document.getElementById("temp").innerHTML = response_5.main.temp + "°C";
    document.getElementById("wind").innerHTML = response_5.wind.speed + "km/h";
  })

// function to call the weather forecast route every 5000 sec
var myVar=setInterval(myTimer,100000);
function myTimer() {
  $.getJSON($SCRIPT_ROOT + '/weather', {post: 0}, function(data) {
    var response_3=({{ data|safe }})
    var response_3 = data;
    document.getElementById("coverage").innerHTML = response_3[2];
    document.getElementById("temp").innerHTML = response_3[0] + "°C";
    document.getElementById("wind").innerHTML = response_3[1] + "km/h";
  })
}

// -------------------------------- user form section
// Change from real time to plan trip

var planTrip=document.getElementById("plantripBtn");
var realTime=document.getElementById("realtimeBtn");
var form=document.getElementById("form");

// Get weather forecast from OpenWeather API for day/time selected by user
function weatherForecast() {
  var dateInput = document.getElementById("date_select");
  var timeInput = document.getElementById("time_select");

  $.getJSON($SCRIPT_ROOT + '/plan_your_trip_weather_forecast', {post: dateInput.value + " " + timeInput.value}, function(data) {
    var response_4=({{ data|safe }})
    var response_4 = data;

    if (response_4 == null) {
      // Error handling for selected time
      document.getElementById("display_invalidtime").innerHTML = 'Please select a valid time.';
    } else {
      var x= response_4[0];
      var y= response_4[1];
      var z= response_4[2];
      var content = '\''  + x + "," + y + "," + z + "," + dateInput.value + "," + timeInput.value + '\'';
      form.innerHTML = '<p>Predicting availability for ' + dateInput.value.slice(-2) + '/' + dateInput.value.slice(5,7) + ' at ' + timeInput.value.slice(0,2) +'h.</p><div class="inputs"><div id="from"><span>FROM:</span><input id="searchTextField3" type="text" size="50" placeholder="Enter starting point" autocomplete="on" runat="server" onclick="initialize3(' + content + ')"/></div><div id="to"><span>TO:</span><input id="searchTextField4" type="text" size="50" placeholder="Enter ending point" autocomplete="on" runat="server" onclick="initialize4(' + content + ')" /></div></div>';
    }
  })
}

// Set selection options for date/time inputs
var dateNew = new Date();

// Create new date object after custom number of days have passed
Date.prototype.addDays = function(days) {
  var date = new Date(this.valueOf());
  date.setDate(date.getDate() + days);
  return date;
}

// Create options for five days  (up to weather forecast possibilities)
var dateNew1 = dateNew.addDays(1);
var dateNew2 = dateNew.addDays(2);
var dateNew3 = dateNew.addDays(3);
var dateNew4 = dateNew.addDays(4);
var dateNew5 = dateNew.addDays(5);

var ourdate = dateNew.getFullYear() + "-" + ("0"+(dateNew.getMonth()+1)).slice(-2) + "-" + ("0"+dateNew.getDate()).slice(-2);
var ourDate1 = dateNew1.getFullYear() + "-" + ("0"+(dateNew1.getMonth()+1)).slice(-2) + "-" + ("0"+dateNew1.getDate()).slice(-2);
var ourDate2 = dateNew2.getFullYear() + "-" + ("0"+(dateNew2.getMonth()+1)).slice(-2) + "-" + ("0"+dateNew2.getDate()).slice(-2);
var ourDate3 = dateNew3.getFullYear() + "-" + ("0"+(dateNew3.getMonth()+1)).slice(-2) + "-" + ("0"+dateNew3.getDate()).slice(-2);
var ourDate4 = dateNew4.getFullYear() + "-" + ("0"+(dateNew4.getMonth()+1)).slice(-2) + "-" + ("0"+dateNew4.getDate()).slice(-2);
var ourDate5 = dateNew5.getFullYear() + "-" + ("0"+(dateNew5.getMonth()+1)).slice(-2) + "-" + ("0"+dateNew5.getDate()).slice(-2);

// Display 'plan your trip' form with click
planTrip.onclick=function() {
  document.getElementById("sourceTitle").innerHTML='';
  document.getElementById("sourceList").innerHTML='';
  document.getElementById("destTitle").innerHTML='';
  document.getElementById("destList").innerHTML='';
  document.getElementById("dropup").style.display = "none";
  realTime.style.backgroundColor="#1a4a50";
  planTrip.style.backgroundColor="#2c7c87";
  form.innerHTML='<p>When will you need a bike?</p><div class="inputs"><span id="date_input">DATE:</span><select id="date_select"></select><span id="time">TIME:</span><select id="time_select"></select><button id="submit" type="submit" onclick="weatherForecast()">SUBMIT</button></div>'+'<p id="display_invalidtime"></p>';
  var dateInput = document.getElementById("date_select");
  dateInput.innerHTML += "<option value='"+ourdate+"'>"+ourdate.slice(-2) + '/' + ourdate.slice(5,7)+"</option><option value='"+ourDate1+"'>"+ourDate1.slice(-2) + '/' + ourDate1.slice(5,7)+"</option><option value='"+ourDate2+"'>"+ourDate2.slice(-2) + '/' + ourDate2.slice(5,7)+"</option><option value='"+ourDate3+"'>"+ourDate3.slice(-2) + '/' + ourDate3.slice(5,7)+"</option><option value='"+ourDate4+"'>"+ourDate4.slice(-2) + '/' + ourDate4.slice(5,7)+"</option>"
  var timeInput = document.getElementById("time_select");
  var hours = 0;
  for (var j = 0; j < 24; j++) {
    if (j % 3 == 0 && j != 0) {
      hours += 3;
    }
    var value = ('0' + hours + ':00:00').slice(-8);
    timeInput.innerHTML += "<option value='" + value + "'>" + j + ":00</option>";
  }
}

// Display 'real time' form with click
realTime.onclick=function() {
  document.getElementById("sourceTitle").innerHTML='';
  document.getElementById("sourceList").innerHTML='';
  document.getElementById("destTitle").innerHTML='';
  document.getElementById("destList").innerHTML='';
  document.getElementById("dropup").style.display = "none";
  realTime.style.backgroundColor="#2c7c87";
  planTrip.style.backgroundColor="#1a4a50";
  form.innerHTML='<p>Need a bike right now?</p><div class="inputs"><div id="from"><span>FROM:</span><input id="searchTextField" type="text" size="50" placeholder="Enter starting point" autocomplete="on" runat="server" onclick="initialize()"/></div><div id="to"><span>TO:</span><input id="searchTextField2" type="text" size="50" placeholder="Enter ending point" autocomplete="on" runat="server" onclick="initialize2()" /></div></div>'
}


// ************************************************************* FUNCTIONALITY

// Find closest station corresponding to user-selected source and destination
function getDistanceFromLatLonInKm(latitude,longitude,m,station_no_bikes_avail_stand,address_2,latlong) {
  // Initialize variables
  var x= latitude;
  var y=longitude;
  var closest_location;
  var min=0;
  var axis=0;
  var value=0;
  var dist_array=new Array(latlong.length);

  // Compute distance using Cartesian formula
  for(var i=0;i<latlong.length;i++) {
    axis=((x-latlong[i][0])*(x-latlong[i][0]))+((y-latlong[i][1])*(y-latlong[i][1]))
    value=Math.sqrt(axis);
    dist_array[i]=value;
  }
  var min = Math.min.apply(Math, dist_array);
  var idx=dist_array.indexOf(Math.min.apply(null,dist_array));
  var idx_second_min_dist =dist_array.indexOf (Math.min.apply(null, dist_array.filter(n => n != min)));
  var nearest_station=address_2[idx];
  var second_nearest_station=address_2[idx_second_min_dist];

  // Display result on modal
  // Flag m used for divide source and destination requests
  if (m==0) {
    // Source
    var bike_available_nearest_station= station_no_bikes_avail_stand[idx][1];
    var bike_available_second_near_station=station_no_bikes_avail_stand[idx_second_min_dist][1];
    if (bike_available_nearest_station>0 ||bike_available_second_near_station>0) {
      document.getElementById("sourceTitle").innerHTML="Nearest stations to your source<br><span class='availableBrackets'>(Available bikes)</span>";
      document.getElementById("sourceList").innerHTML="<span onclick=\"clickMarker('"+nearest_station+"')\">"+nearest_station+"</span> ("+bike_available_nearest_station+")<br><span onclick=\"clickMarker('"+second_nearest_station+"')\">"+second_nearest_station+"</span> ("+bike_available_second_near_station+")";
    } else {
      document.getElementById("sourceTitle").innerHTML="The two nearest stations to your location seems to be busy. Try again in few minutes!!";
      document.getElementById("sourceList").innerHTML= " ";
    }
  } else {
    // Destination
    var bike_stand_available_nearest_station= station_no_bikes_avail_stand[idx][2];
    var bike_stand_available_second_near_station=station_no_bikes_avail_stand[idx_second_min_dist][2];
    if (bike_stand_available_nearest_station>0 || bike_stand_available_second_near_station>0 ) {
      document.getElementById("destTitle").innerHTML="Nearest stations to your destination<br><span class='availableBrackets'>(Available stands)</span>";
      document.getElementById("destList").innerHTML="<span onclick=\"clickMarker('"+nearest_station+"')\">"+nearest_station+"</span> ("+bike_stand_available_nearest_station+")<br><span onclick=\"clickMarker('"+second_nearest_station+"')\">"+second_nearest_station+"</span> ("+bike_stand_available_second_near_station+")";
    } else {
      document.getElementById("destTitle").innerHTML="The two nearest stations to your location seems to be busy. Try again in few minutes!!";
      document.getElementById("destList").innerHTML= " ";
    }
  }
  document.getElementById("dropup").style.display = "block";
}

// Fetch most recent availability and static data from database and call getDistance function
function myfunction_get_updated_available_bikes_and_stands(latitude,longitude,m) {
  $.getJSON($SCRIPT_ROOT + '/all_available_details', {post: 0}, function(data) {
    var response_2=({{ data|safe }})
    var response_2 = data;
    var common_station_no=new Array(response_2.length);
    for (var i=0;i<response_2.length;i++) {
      common_station_no[i]= response_2[i][0];
    }
    var station_no_bikes_avail_stand=new Array(common_station_no.length);
    for (var i=0;i<common_station_no.length;i++) {
      station_no_bikes_avail_stand[i]=[response_2[i][0],response_2[i][1],response_2[i][2]];
    }
    var address_2=new Array(common_station_no.length);
    for (var i=0;i<common_station_no.length;i++) {
      address_2[i]=response_2[i][3];
    }
    var lat=new Array(common_station_no.length);
    var long=new Array(common_station_no.length);

    // Get list of stations latitude
    for (var i=0;i<common_station_no.length;i++) {
      lat[i]=response_2[i][4];
    }
    // Get list of stations longitude
    for (var i=0;i<common_station_no.length;i++) {
      long[i]=response_2[i][5];
    }
    // Get list of latitude and longitude of stations as a tuple
    var latlong=new Array(common_station_no.length);
    for (var i=0;i<common_station_no.length;i++) {
      latlong[i]=[lat[i],long[i]];
    }

    getDistanceFromLatLonInKm(latitude,longitude,m,station_no_bikes_avail_stand,address_2,latlong);
  });
}


// Triggered whenever user clicks on "Enter starting point" field to enter the source --> 'real-time' mode
// Get latitude and longitude for the selected source address
function initialize() {
  var input = document.getElementById('searchTextField');
  var autocomplete = new google.maps.places.Autocomplete(input);
  google.maps.event.addListener(autocomplete, 'place_changed', function () {
      var place = autocomplete.getPlace();
      var latitude = place.geometry.location.lat();
      var longitude=place.geometry.location.lng();
      var m=0;
      myfunction_get_updated_available_bikes_and_stands(latitude,longitude,m);
  });
}


// Triggered whenever user clicks on "Enter ending point" field to enter the destination --> 'real-time' mode
// Get latitude and longitude for the selected destination address
function initialize2() {
  var input = document.getElementById('searchTextField2');
  var autocomplete = new google.maps.places.Autocomplete(input);
  google.maps.event.addListener(autocomplete, 'place_changed', function () {
    var place = autocomplete.getPlace();
    var latitude = place.geometry.location.lat();
    var longitude=place.geometry.location.lng();
    var m=1;
    myfunction_get_updated_available_bikes_and_stands(latitude,longitude,m);
  });
}

// Find closest station corresponding to user-selected source
// According to ML model predict availability
function get_closest_distance_predicted_station(latitude,longitude,fore_temp,fore_weather,fore_wind,m,dayP,timeP) {
  var x = latitude;
  var y = longitude;
  var closest_location;
  var min = 0;
  var axis = 0;
  var value = 0;

  $.getJSON($SCRIPT_ROOT + '/all_available_details', {post: 0}, function(data) {
    var response_2=({{ data|safe }})
    var response_2 = data;
    var common_station_no=new Array(response_2.length);
    for (var i=0;i<response_2.length;i++) {
      common_station_no[i]= response_2[i][0];
    }
    var address_2=new Array(common_station_no.length);
    for (var i=0;i<common_station_no.length;i++) {
      address_2[i]=response_2[i][3];
    }
    var lat=new Array(common_station_no.length);
    var long=new Array(common_station_no.length);

    // Get list of stations latitude
    for (var i=0;i<common_station_no.length;i++) {
      lat[i]=response_2[i][4];
    }

    // Get list of stations longitude
    for(var i=0;i<common_station_no.length;i++) {
      long[i]=response_2[i][5];
    }

    // Get list of latitude and longitude of stations as a tuple
    var latlong=new Array(common_station_no.length);
    for(var i=0;i<common_station_no.length;i++) {
      latlong[i]=[lat[i],long[i]];
    }
    var dist_array=new Array(latlong.length);
    for (var i=0;i<latlong.length;i++) {
      axis=((x-latlong[i][0])*(x-latlong[i][0]))+((y-latlong[i][1])*(y-latlong[i][1]))
      value=Math.sqrt(axis);
      dist_array[i]=value;
    }

    var min = Math.min.apply(Math, dist_array);
    var idx=dist_array.indexOf(Math.min.apply(null,dist_array));
    var idx_second_min_dist =dist_array.indexOf (Math.min.apply(null, dist_array.filter(n => n != min)));
    var nearest_station=address_2[idx];
    var nearest_station_number = common_station_no[idx];
    var second_nearest_station=address_2[idx_second_min_dist];
    var second_nearest_station_number = common_station_no[idx_second_min_dist];
    var datePredict = new Date(parseInt(dayP.slice(0,4)), parseInt(dayP.slice(5,7)-1), parseInt(dayP.slice(8,10)));
    var timePredict = parseInt(timeP.slice(0,2));
    var weekDay = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"][datePredict.getDay()];
    var prediction_info_list = nearest_station_number+" "+second_nearest_station_number+" "+fore_temp+" "+fore_weather+" "+fore_wind+" "+m+" "+weekDay+" "+timePredict;

    myPrediction(prediction_info_list);

    // Trigger ML model and display result on HTML
    function myPrediction(prediction_info_list) {
      $.getJSON($SCRIPT_ROOT + '/prediction_model', {post: prediction_info_list}, function(data) {
        var response=({{ data|safe }})
        var response = data;
        var bike_nearest_station = response[0];
        var bike_available_2nd_nearest = response[1];
        if (m == 0) {
          document.getElementById("sourceTitle").innerHTML="Nearest stations to your source<br><span class='availableBrackets'>(Predicted available bikes)</span>";
          document.getElementById("sourceList").innerHTML="<span onclick=\"clickMarker('"+nearest_station+"')\">"+nearest_station+"</span> ("+bike_nearest_station+")<br><span onclick=\"clickMarker('"+second_nearest_station+"')\">"+second_nearest_station+"</span> ("+bike_available_2nd_nearest+")";
        } else {
          document.getElementById("destTitle").innerHTML="Nearest stations to your destination<br><span class='availableBrackets'>(Predicted available stands)</span>";
          document.getElementById("destList").innerHTML="<span onclick=\"clickMarker('"+nearest_station+"')\">"+nearest_station+"</span> ("+bike_nearest_station+")<br><span onclick=\"clickMarker('"+second_nearest_station+"')\">"+second_nearest_station+"</span> ("+bike_available_2nd_nearest+")";
        }
      })
    }
    document.getElementById("dropup").style.display = "block";
  });
}


// Triggered whenever user clicks on "Enter starting point" field to enter the source --> 'plan your trip' mode
// Get latitude and longitude for the selected source address
function initialize3(string_value) {
  var list_string_arr = string_value.split(',');
  var fore_temp = parseInt(list_string_arr[0]);
  var fore_weather = list_string_arr[1];
  var fore_wind = parseInt(list_string_arr[2]);
  var input = document.getElementById('searchTextField3');
  var autocomplete = new google.maps.places.Autocomplete(input);

  google.maps.event.addListener(autocomplete, 'place_changed', function () {
    var place = autocomplete.getPlace();
    var latitude = place.geometry.location.lat();
    var longitude=place.geometry.location.lng();
    var m=0;
    get_closest_distance_predicted_station(latitude,longitude,fore_temp,fore_weather,fore_wind,m,list_string_arr[3],list_string_arr[4]);
  });
}


// Triggered whenever user clicks on "Enter ending point" field to enter the destination --> 'plan your trip' mode
// Get latitude and longitude for the selected destination address
function initialize4(string_value) {
  var list_string_arr = string_value.split(',');
  var fore_temp = parseInt(list_string_arr[0]);
  var fore_weather = list_string_arr[1];
  var fore_wind = parseInt(list_string_arr[2]);
  var input = document.getElementById('searchTextField4');
  var autocomplete = new google.maps.places.Autocomplete(input);


  google.maps.event.addListener(autocomplete, 'place_changed', function () {
    var place = autocomplete.getPlace();
    var latitude = place.geometry.location.lat();
    var longitude=place.geometry.location.lng();
    var m=1;
    get_closest_distance_predicted_station(latitude,longitude,fore_temp,fore_weather,fore_wind,m,list_string_arr[3],list_string_arr[4]);
  });
}


// Add DOM event listener to window object for the load event
google.maps.event.addDomListener(window, 'load', initialize);
