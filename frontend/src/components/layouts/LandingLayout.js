import React from "react";
import Header from "../sections/Header";
import MapComponent from '../sections/MapComponent';
import {
  Box,
  Button,
  Flex,
  Heading,
  Stack,
  Text,
  Input
} from "@chakra-ui/react";


export default function LandingLayout(props) {
  return (
    <Flex
      direction="column"
      align="left"
      maxW={{ xl: "1200px" }}
      m="0 auto"
      {...props}
    >
      <Header />
      {props.children}

      <div>
      <Text as="h1"
          size="xl"
          fontWeight="bold"
          color="primary.800"
          textAlign={["center", "center", "left", "left"]}
          fontFamily={"Trebuchet MS"} 
          letterSpacing={-3}
      >Bus Routes</Text>
      <MapComponent />
      </div>

    </Flex>
    
  );
}