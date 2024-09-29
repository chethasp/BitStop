import React,  { useState, useEffect } from "react";
import Papa from "papaparse";
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
          <Input placeholder="Enter a city name" />
          <Input placeholder="Enter number of routes" type="number"/>
        </Stack>
        
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
            {ctaText}
          </Button>

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
          <Input placeholder="Email" />
          <Input placeholder="Address of Stop" type="number"/>
        
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
            Submit
          </Button>
          </Stack>
        </Flex>
      </Stack>

      <Box
        w={{ base: "100%", md: "40%" }} 
        mt={{ base: 8, md: 0 }} 
        p={4}
        borderWidth="1px"
        borderRadius="lg"
        boxShadow="lg"
        bg="gray.50"
        overflowY="auto" 
        maxH="70vh" 
      >
        <Heading as="h3" size="md" mb={4}>
          Available Stops
        </Heading>
        <Stack spacing={3}>
          {places.map((place, index) => (
            <Box key={index} p={2} borderBottom="1px solid" borderColor="gray.200">
              <Text fontWeight="bold">{place.name}</Text>
              <Text>{place.address}</Text>
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
