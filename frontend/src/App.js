import './App.css';
import { ChakraProvider, Box, Flex, Text } from '@chakra-ui/react';

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Landing from "./pages/Landing";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />}>
        </Route>
      </Routes>
    </Router>

    /*
    <Flex direction="column" height="100vh" className='main'>
      <Box bg="teal.500" color="white" p={4}>
        <Text fontSize="xl" textAlign="left" >BITSTOP</Text>
      </Box>

      <Flex flex="1">
        <Box bg="gray.200" width="250px" p={4}>
          <Text fontSize="lg" mb={4}>Navigation</Text>
          <Text mb={2}>Link 1</Text>
          <Text mb={2}>Link 2</Text>
          <Text mb={2}>Link 3</Text>
        </Box>

        <Box flex="1" p={4}>
          <Text fontSize="lg">Main Content Area</Text>
        </Box>
      </Flex>
    </Flex>
    */
  );
}

export default App;
