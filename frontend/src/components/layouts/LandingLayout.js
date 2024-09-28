import React from "react";
import { Flex } from "@chakra-ui/react";
import Header from "../sections/Header";

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
    </Flex>
  );
}