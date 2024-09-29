import React, { useState, useCallback, useEffect } from 'react';
import { GoogleMap, Marker, DirectionsRenderer, useJsApiLoader } from '@react-google-maps/api';

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

    const directionsService = new window.google.maps.DirectionsService();
    directionsService.route(
      {
        origin: markers[0],
        destination: markers[markers.length - 1],
        waypoints: markers.slice(1, -1).map((marker) => ({ location: marker, stopover: true })),
        travelMode: window.google.maps.TravelMode.DRIVING,
      },
      (result, status) => {
        if (status === window.google.maps.DirectionsStatus.OK) {
          setDirectionsResponse(result);
        } else {
          console.error(`Error fetching directions ${result}`);
        }
      }
    );
  }, [markers]);

  useEffect(() => {
    if (markers.length > 1) {
      calculateRoute();
    }
  }, [markers, calculateRoute]);

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  return (
    <div>
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
      <div>
        <button onClick={() => setMarkers([])}>Clear Markers</button>
      </div>
    </div>
  );
};

export default MapComponent;
