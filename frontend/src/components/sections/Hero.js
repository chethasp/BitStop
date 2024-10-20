import React,  { useState, useEffect } from "react";
import Papa from "papaparse";
import axios from "axios";
import footTrafficData from "../../files/foot_traffic_sites.csv"; 
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import {
  Box,
  Button,
  Flex,
  Heading,
  Stack,
  Text,
  Input
} from "@chakra-ui/react";

export default function UserEntry({
  title,
  subtitle,
  ctaLink,
  ctaText,
  ...rest
}) {

    const [places, setPlaces] = useState([]);

    //Handle latlong
    const [email, setEmail] = useState("");
    const [address, setAddress] = useState("");
    const [latLong, setLatLong] = useState("");  
    const [error, setError] = useState("");
    // handle generate routes
    const [city, setCity] = useState('');
    const [amount, setAmount] = useState('');

    const handleSubmit = () => {
      setLatLong(null);
      setError("");

      // Make an Axios GET request to your Django API
      axios.get('http://localhost:8000/bus_routes/get_lat_long/', { 
          params: { address } 
      })
      .then(response => {
          const { latitude, longitude } = response.data;
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

    const handleGenerateStopsClick = () => {

      const params = {
        'city': city, // Value from the city input field
        'amount': amount, // Value from the number input field
      };

      console.log(params)
  
      // Make an API request using Axios
      axios.get('http://localhost:8000/bus_routes/generate_foot_traffic_sites/', { params })
        .then(response => {
          // Handle the response from the API
          console.log('API Response:', response.data);
          // You can now use this data to update your state or display on the UI
        })
        .catch(error => {
          // Handle any errors from the API request
          console.error('Error fetching routes:', error);
        });


    }

    useEffect(() => {
        // Fetch and parse the CSV data
        fetch(footTrafficData) // Update with the correct path to the CSV file
        .then(response => response.text())
        .then(csvText => {
            Papa.parse(csvText, {
            header: false, // The CSV you provided doesn't have headers
            complete: (results) => {
                const data = results.data;
                const filtered_data = data.slice(1)
                // Extract only the name and address (first and second columns)
                const placeList = filtered_data.map(row => ({
                name: row[0],
                address: row[1],
                }));
                setPlaces(placeList);
            },
            });
        });
    }, []);

  return (
    <Flex
      align="center"
      justify={{ base: "center", md: "flex-start", xl: "space-between" }}
      direction={{ base: "column", md: "row" }}
      wrap="no-wrap"
      minH="70vh"
      px={8}
      mb={16}
      {...rest}
    >
      <Stack
        spacing={4}
        w={{ base: "80%", md: "40%" }}
        align={["center", "center", "flex-start", "flex-start"]}
      >
        <Heading
          as="h1"
          size="xl"
          fontWeight="bold"
          color="primary.800"
          textAlign={["center", "center", "left", "left"]}
          fontFamily={"Trebuchet MS"} 
          letterSpacing={-3}
        >
          {title}
        </Heading>
        
        {/* User Entry Boxes */}
        <Stack spacing={4} w="100%">
          <Input placeholder="Enter a city name" value={city}
            onChange={(e) => setCity(e.target.value) }/>
          <Input placeholder="Enter number of stops" type="number" variantalue={amount}
            onChange={(e) => setAmount(e.target.value)}/>
        </Stack>

          <flex direction='rows'>
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
            mr={4}
            onClick={handleGenerateStopsClick}
          >
            Generate Routes
          </Button>
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
          >
            Display Routes
          </Button>
          </flex>

      <Flex align="center" direction={{ base: "column", md: "row" }}>
      <Stack spacing={4} w="100%">

    


          
          </Stack>
        </Flex>
      </Stack>

      <Box
        w={{ base: "100%", md: "40%" }} 
        mt={{ base: 8, md: 0 }} 
        p={4}
        borderWidth="4px"
        borderRadius="lg"
        boxShadow="lg"
        bg="gray.50"
        overflowY="auto" 
        maxH="70vh" 
        borderColor={"green"}
      >
        <Heading as="h3" size="lg" mb={4} fontFamily={"Trebuchet MS"} letterSpacing={-1}>
          Available Stops
        </Heading>
        <Stack spacing={3}>
          {places.map((place, index) => (
            <Box key={index} p={2} borderBottom="1px solid" borderColor="gray.200">
              <Text fontWeight="bold" fontFamily={"Trebuchet MS"} letterSpacing={-0.5} fontSize={20}>{place.name}</Text>
              <Text fontFamily={"Trebuchet MS"} letterSpacing={-1} fontSize = {15}>{place.address}</Text>
            </Box>
          ))}
        </Stack>
      </Box>

    </Flex>
  );
}

UserEntry.propTypes = {
  title: PropTypes.string,
  subtitle: PropTypes.string,
  ctaText: PropTypes.string,
};