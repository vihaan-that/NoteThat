import { useState, useEffect } from "react";

export function useMediaQuery(query) {
  const [matches, setMatches] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    
    // Check if window is defined (client-side)
    if (typeof window !== "undefined") {
      const media = window.matchMedia(query);
      
      // Set initial value
      setMatches(media.matches);
      
      // Create event listener
      const listener = () => setMatches(media.matches);
      
      // Add listener
      media.addEventListener("change", listener);
      
      // Clean up
      return () => media.removeEventListener("change", listener);
    }
  }, [query]);

  // Return false during SSR to avoid hydration mismatch
  return mounted ? matches : false;
}

// Predefined breakpoints
export const breakpoints = {
  sm: "(min-width: 640px)",
  md: "(min-width: 768px)",
  lg: "(min-width: 1024px)",
  xl: "(min-width: 1280px)",
  "2xl": "(min-width: 1536px)",
  iphone: "(max-width: 428px)",
  portrait: "(orientation: portrait)",
  landscape: "(orientation: landscape)",
};
