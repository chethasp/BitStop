import React from "react";

import Hero from "../components/sections/Hero";
import LandingLayout from "../components/layouts/LandingLayout";
import MapComponent from "../components/sections/MapComponent";

export default function Landing() {
  return (
    <LandingLayout>
      <Hero
        title="A better way to bus."
        ctaText="Generate a route map"
      />
      <MapComponent/>
    </LandingLayout>

  );
}