import React from "react";

import Hero from "../components/sections/Hero";
import LandingLayout from "../components/layouts/LandingLayout";

export default function Landing() {
  return (
    <LandingLayout>
      <Hero
        title="Bus faster, bus quicker"
        ctaText="Generate a route map"
      />
    </LandingLayout>
  );
}