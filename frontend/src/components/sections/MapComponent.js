import React, { useState, useCallback, useEffect } from 'react';
import { GoogleMap, Marker, DirectionsRenderer, useJsApiLoader } from '@react-google-maps/api';
import Papa from "papaparse";
import footTrafficData from "../../files/foot_traffic_sites.csv"; 
import {
  Box,
  Button,
  Flex,
  Heading,
  Stack,
  Text,
  Input
} from "@chakra-ui/react";

// Set the initial center of the map
const center = {
  lat: 33.7501,  
  lng: -84.3885, 
};

const containerStyle = {
  width: '100%',
  height: '400px',
};

const MapComponent = () => {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: 'AIzaSyCUqJZsnM7GrrpcRbRaaEeTpVYERjBNxgs', 
    libraries: ['places'],
  });

  const [directionsResponse, setDirectionsResponse] = useState(null);
  const [markers, setMarkers] = useState([]);

  const addMarker = (location) => {
    setMarkers((current) => [...current, location]);
  };

  const calculateRoute = useCallback(() => {
    if (markers.length < 2) {
      return;
    }

    //const directionsService = new window.google.maps.DirectionsService();
    /**directionsService.route(
      {
        origin: markers[0],
        destination: markers[markers.length - 1],
        waypoints: markers.slice(1, -1).map((marker) => ({ location: marker, stopover: true })),
        //travelMode: window.google.maps.TravelMode.DRIVING,
      },
      //(result, status) => {
        //if (status === window.google.maps.DirectionsStatus.OK) {
          //setDirectionsResponse(result);
        //} else {
          //console.error(`Error fetching directions ${result}`);
        //}
      //}
    );
    */
  }, [markers]);

  useEffect(() => {
    if (markers.length > 1) {
      calculateRoute();
    }
  }, [markers, calculateRoute]);

  useEffect(() => {
    // Fetch and parse the CSV data
    fetch(footTrafficData) // Update with the correct path to the CSV file
    .then(response => response.text())
    .then(csvText => {
        Papa.parse(csvText, {
        header: false, // The CSV you provided doesn't have headers
        complete: (results) => {
            const data = results.data;
            // Extract only the name and address (first and second columns)
            const placeList = data.map(row => ({
            lat: parseFloat(row[2]),
            lng: parseFloat(row[3]),
            }));
            setMarkers(placeList);
        },
        });
    });
}, []);

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <Text color={"green"} display="block" fontWeight="bold" fontSize={40} fontFamily={"Trebuchet MS"} letterSpacing={-3}>
        route map
      </Text>

      <Box borderWidth="5px" borderColor="green.500" borderRadius="lg" overflow="hidden">
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={center}
          zoom={10}
          onClick={(e) => addMarker({ lat: e.latLng.lat(), lng: e.latLng.lng() })}
        >
          {markers.map((marker, index) => (
            <Marker key={index} position={marker} />
          ))}
          {directionsResponse && <DirectionsRenderer directions={directionsResponse} />}
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
        onClick={() => setMarkers([])}
        mt={3}
      >
        Clear Markers
      </Button>
    </div>
  );
};

export default MapComponent;
