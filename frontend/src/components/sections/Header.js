import React from "react";
import { Box, Flex, Text, Button } from "@chakra-ui/react";

const Header = (props) => {
  const [show, setShow] = React.useState(false);
  const toggleMenu = () => setShow(!show);

  return (
    <Flex
      as="nav"
      align="center"
      justify="flex-start"
      w="100%"
      mb={8}
      p={8}
    >

      <Box
        display={{ base: show ? "block" : "none", md: "block" }}
        flexBasis={{ base: "100%"}}
      >
        <Flex
          align="center"
          justify={["flex-start"]}
          direction={["column", "row", "row", "row"]}
          pt={[4, 4, 0, 0]}
        >
            <Text color={"green"} display="block" fontWeight="bold" fontSize={40}>
            bitstop    
            </Text>
        </Flex>
      </Box>
    </Flex>
  );
};

export default Header;