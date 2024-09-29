import React, { useState, useCallback, useEffect } from 'react';
import { GoogleMap, Marker, DirectionsRenderer, useJsApiLoader } from '@react-google-maps/api';
import Papa from "papaparse";
import footTrafficData from "../../files/foot_traffic_sites.csv"; 
import {
  Box,
  Button,
  Text
} from "@chakra-ui/react";
import axios from "axios"

// Set the initial center of the map
let center = {
  lat: 33.7501,  
  lng: -84.3885, 
};

const containerStyle = {
  width: '100%',
  height: '400px',
};

// Define some colors for the routes
const routeColors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF'];

const MapComponent = () => {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: 'AIzaSyCfPMzELQgSjAnG9GkiMyeef8TL7gTycF4', 
    libraries: ['places'],
  });

  const [directionsResponses, setDirectionsResponses] = useState([]);
  const [markers, setMarkers] = useState([]);
  const [places, setPlaces] = useState([]);

  //Handle latlong
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");
  const [latLong, setLatLong] = useState(null);  
  const [error, setError] = useState("");
  // handle generate routes
  const [city, setCity] = useState('');
  const [amount, setAmount] = useState('');

  const addMarker = (location) => {
    setMarkers((current) => [...current, location]);
  };

  const calculateRoutes = useCallback(() => {
    if (!isLoaded) {
      console.error("Google Maps API not loaded yet.");
      return; // Ensure the API is loaded
    }

    if (markers.length < 2) {
      console.warn("Not enough markers to calculate routes.");
      return; // Need at least two markers to calculate a route
    }

    const directionsService = new window.google.maps.DirectionsService();
    const responses = []; // Store all responses for multiple routes

    // Iterate through markers to calculate routes between each consecutive pair
    for (let index = 0; index < markers.length - 1; index++) {
      const origin = markers[index];
      const destination = markers[index + 1];

      console.log(`Calculating route from ${JSON.stringify(origin)} to ${JSON.stringify(destination)}`);

      directionsService.route(
        {
          origin: origin,
          destination: destination,
          travelMode: window.google.maps.TravelMode.DRIVING,
        },
        (result, status) => {
          if (status === window.google.maps.DirectionsStatus.OK) {
            console.log(`Successfully fetched directions from ${origin} to ${destination}`);
            responses.push({ result, color: routeColors[index % routeColors.length] });
            if (responses.length === markers.length - 1) { // All routes calculated
              setDirectionsResponses(responses);
            }
          } else {
            console.error(`Error fetching directions from ${origin} to ${destination}: ${status}`);
          }
        }
      );
    }
  }, [markers, isLoaded]);

  useEffect(() => {
    if (markers.length > 1) {
      calculateRoutes();
    }
  }, [markers, calculateRoutes]);

  useEffect(() => {
    // Fetch and parse the CSV data
    fetch(footTrafficData) // Update with the correct path to the CSV file
    .then(response => response.text())
    .then(csvText => {
      Papa.parse(csvText, {
        header: false, // The CSV you provided doesn't have headers
        complete: (results) => {
          const data = results.data;
          // Extract only the latitude and longitude (third and fourth columns)
          const placeList = data.map(row => ({
            lat: parseFloat(row[2]),
            lng: parseFloat(row[3]),
          })).filter(place => !isNaN(place.lat) && !isNaN(place.lng)); // Ensure valid coordinates

          console.log("Markers from CSV:", placeList);
            center = {lat: placeList.at(1).lat, lng: placeList.at(1).lng}
          setMarkers(placeList);
        },
      });
    });
  }, []);

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  

  const handleSubmit = () => {
    setLatLong(null);
    setError("")
    console.log("button clicked")

    // Make an Axios GET request to your Django API
    axios.get('http://localhost:8000/bus_routes/get_lat_long/', { 
        params: { address } 
    })
    .then(response => {
        const { latitude, longitude } = response.data;
        addMarker({ lat: latitude, lng: longitude })
        center = {lat: latitude, lng: longitude}
        setLatLong({ latitude, longitude });  
    })
    .catch(error => {
        if (error.response) {
            setError(error.response.data.error); 
        } else {
            setError("An unexpected error occurred.");
        }
    });
  };

  return (

    <div>

      <Text color={"green"} display="block" fontWeight="bold" fontSize={40} fontFamily={"Trebuchet MS"} letterSpacing={-3}>
        Route Map
      </Text>

      <Box borderWidth="5px" borderColor="green.500" borderRadius="lg" overflow="hidden">
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={center}
          zoom={10}
          //onClick={(e) => addMarker({ lat: e.latLng.lat(), lng: e.latLng.lng() })}
        >
          {markers.map((marker, index) => (
            <Marker key={index} position={marker} />
          ))}

          {/* Render directions for each route */}
          {directionsResponses.map((directions, index) => (
            <DirectionsRenderer
              key={index}
              directions={directions.result}
              options={{
                polylineOptions: {
                  strokeColor: directions.color,
                  strokeWeight: 4,
                },
              }}
            />
          ))}
        </GoogleMap>
      </Box>

      <Button
        colorScheme="primary"
        backgroundColor="green"
        borderRadius="5px"
        py="4"
        px="4"
        lineHeight="1"
        size="md"
        fontFamily={"Trebuchet MS"} 
        letterSpacing={-0.5}
        onClick={() => {
          setMarkers([]);
          setDirectionsResponses([]); // Clear directions when clearing markers
        }}
        mt={3}
      >
        Clear Markers
      </Button>
      <box borderWidth="5px" borderColor="green.500" borderRadius="lg" overflow="hidden">

      <Flex align="center" direction={{ base: "column", md: "row" }}>
      <Stack spacing={4} w="100%">

      <br></br>
  


<Heading
    as="h1"
    size="xl"
    fontWeight="bold"
    color="primary.800"
    textAlign={["center", "center", "left", "left"]}
    fontFamily={"Trebuchet MS"} 
    letterSpacing={0.5}
  >
    Suggest a Stop
  </Heading>
    <Input placeholder="Email" value={email}
      onChange={(e) => setEmail(e.target.value)}/>
    <Input placeholder="Address of Stop" value={address}
      onChange={(e) => setAddress(e.target.value)}/>
  
  <Button
      colorScheme="primary"
      backgroundColor="green"
      borderRadius="8px"
      py="4"
      px="4"
      lineHeight="1"
      size="md"
      fontFamily={"Trebuchet MS"} 
      letterSpacing={-0.5}
      onClick={handleSubmit}
    >
      Submit
    </Button>

    </Stack>

</Flex>
</box>

    </div>
  );
};

export default MapComponent;
