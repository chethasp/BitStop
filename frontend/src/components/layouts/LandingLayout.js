import React from "react";
import { Flex } from "@chakra-ui/react";
import Header from "../sections/Header";
import MapComponent from '../sections/MapComponent';


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
      <h1 color="green">Bus Routes</h1>
      <MapComponent />
      </div>

    </Flex>
    
  );
}