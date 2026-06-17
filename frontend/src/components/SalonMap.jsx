/**
 * SalonMap.jsx — Reusable Interactive Map for Salon Selection
 * Integrates Google Maps with custom dark styling, and falls back
 * to a styled interactive SVG map if the Google Maps API is unconfigured/offline.
 */

import React, { useState, useEffect, useRef } from "react";

export default function SalonMap({ salons, selectedSalon, onSelectSalon }) {
  const mapRef = useRef(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [useFallback, setUseFallback] = useState(false);
  
  // Google Maps instances
  const mapInstanceRef = useRef(null);
  const markersRef = useRef({});
  const infoWindowRef = useRef(null);

  // Fallback map states
  const [activeFallbackMarker, setActiveFallbackMarker] = useState(null);

  // Register select callback globally so the InfoWindow HTML can trigger React state
  useEffect(() => {
    window.selectSalonFromMap = (id) => {
      const salon = salons.find((s) => s.id === id);
      if (salon && onSelectSalon) {
        onSelectSalon(salon);
      }
    };
    return () => {
      delete window.selectSalonFromMap;
    };
  }, [salons, onSelectSalon]);

  // Load Google Maps Script
  useEffect(() => {
    const key = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || "";
    
    if (!key) {
      setUseFallback(true);
      return;
    }

    const scriptId = "google-maps-script";
    let script = document.getElementById(scriptId);

    const initializeMap = () => {
      setMapLoaded(true);
      setUseFallback(false);
    };

    if (window.google && window.google.maps) {
      initializeMap();
      return;
    }

    if (script) {
      script.addEventListener("load", initializeMap);
      script.addEventListener("error", () => setUseFallback(true));
      return;
    }

    script = document.createElement("script");
    script.id = scriptId;
    script.src = `https://maps.googleapis.com/maps/api/js?key=${key}`;
    script.async = true;
    script.defer = true;
    script.onload = initializeMap;
    script.onerror = () => setUseFallback(true);
    document.head.appendChild(script);

    return () => {
      // Keep script in head to prevent reloading on every mount
    };
  }, []);

  // Initialize and Update Google Map
  useEffect(() => {
    if (!mapLoaded || useFallback || !mapRef.current || salons.length === 0) return;

    const google = window.google;

    // Bangalore center coordinates
    const defaultCenter = { lat: 12.9715, lng: 77.6100 };

    if (!mapInstanceRef.current) {
      // 1. Create Map Instance
      mapInstanceRef.current = new google.maps.Map(mapRef.current, {
        center: defaultCenter,
        zoom: 12.5,
        styles: darkMapStyles,
        disableDefaultUI: false,
        zoomControl: true,
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: true,
      });

      // 2. Create Single Shared InfoWindow
      infoWindowRef.current = new google.maps.InfoWindow();
    }

    const map = mapInstanceRef.current;
    const infoWindow = infoWindowRef.current;

    // 3. Clear old markers
    Object.values(markersRef.current).forEach((marker) => marker.setMap(null));
    markersRef.current = {};

    // 4. Create markers for each salon
    salons.forEach((s) => {
      if (!s.latitude || !s.longitude) return;

      const markerPos = { lat: s.latitude, lng: s.longitude };

      // Custom marker icon (gold colored pin)
      const marker = new google.maps.Marker({
        position: markerPos,
        map: map,
        title: s.name,
        icon: {
          path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
          fillColor: "#c5a880",
          fillOpacity: 1,
          strokeColor: "#08080a",
          strokeWeight: 2,
          scale: 7,
        },
      });

      markersRef.current[s.id] = marker;

      // Click listener to open custom pop-up (InfoWindow)
      marker.addListener("click", () => {
        openInfoWindow(s, marker);
      });
    });

    // Fit map bounds to show all markers if not centering on specific salon
    if (!selectedSalon) {
      const bounds = new google.maps.LatLngBounds();
      let hasCoords = false;
      salons.forEach((s) => {
        if (s.latitude && s.longitude) {
          bounds.extend({ lat: s.latitude, lng: s.longitude });
          hasCoords = true;
        }
      });
      if (hasCoords) {
        map.fitBounds(bounds);
        // Avoid zooming too close
        google.maps.event.addListenerOnce(map, "bounds_changed", () => {
          if (map.getZoom() > 14) map.setZoom(14);
        });
      }
    }

  }, [mapLoaded, useFallback, salons]);

  // Handle selectedSalon updates (center map and open InfoWindow)
  useEffect(() => {
    if (useFallback || !mapInstanceRef.current || !selectedSalon) return;
    
    const google = window.google;
    const map = mapInstanceRef.current;
    const marker = markersRef.current[selectedSalon.id];

    if (marker && selectedSalon.latitude && selectedSalon.longitude) {
      map.panTo({ lat: selectedSalon.latitude, lng: selectedSalon.longitude });
      map.setZoom(14.5);
      openInfoWindow(selectedSalon, marker);
    }
  }, [selectedSalon, useFallback]);

  // InfoWindow builder helper
  const openInfoWindow = (salon, marker) => {
    const infoWindow = infoWindowRef.current;
    const map = mapInstanceRef.current;
    if (!infoWindow || !map) return;

    const directionsUrl = `https://www.google.com/maps/dir/?api=1&destination=${salon.latitude},${salon.longitude}`;
    const isSelected = selectedSalon?.id === salon.id;

    // Premium styled HTML string inside the popup
    const popupContent = `
      <div style="
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #fcfcfd;
        background: #121215;
        padding: 10px;
        border-radius: 8px;
        max-width: 260px;
      ">
        <div style="position: relative; border-radius: 6px; overflow: hidden; margin-bottom: 8px;">
          <img src="${salon.image_url}" alt="${salon.name}" style="width: 100%; height: 90px; object-fit: cover;" />
          <div style="position: absolute; top: 6px; right: 6px; background: rgba(0,0,0,0.85); padding: 2px 6px; border-radius: 4px; font-size: 10px; color: #c5a880; font-weight: 700;">
            ${salon.price_range}
          </div>
        </div>
        <h3 style="font-family: 'Playfair Display', serif; font-size: 14px; margin: 0 0 4px 0; color: #fcfcfd; font-weight: 600;">${salon.name}</h3>
        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #a1a1aa; margin-bottom: 8px;">
          <span>📍 ${salon.area}</span>
          <span style="color: #c5a880; font-weight: bold;">★ ${salon.rating}</span>
        </div>
        <div style="display: flex; gap: 8px; margin-top: 10px;">
          <a href="${directionsUrl}" target="_blank" rel="noopener noreferrer" style="
            flex: 1;
            background: #1a1a1f;
            border: 1px solid #26262b;
            color: #c5a880;
            text-align: center;
            padding: 6px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            text-decoration: none;
          ">
            Directions
          </a>
          <button onclick="window.selectSalonFromMap(${salon.id})" style="
            flex: 1.2;
            background: linear-gradient(135deg,#8a704c,#c5a880);
            border: none;
            color: #0e0e0e;
            padding: 6px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(197,168,128,0.15);
          ">
            ${isSelected ? "Selected ✓" : "Select & Book"}
          </button>
        </div>
      </div>
    `;

    infoWindow.setContent(popupContent);
    
    // Override styling of google infowindow card wrapper
    google.maps.event.addListenerOnce(infoWindow, "domready", () => {
      const iwOuter = document.querySelector(".gm-style-iw-c");
      const iwBackground = document.querySelector(".gm-style-iw-d");
      const iwCloseBtn = document.querySelector(".gm-style-iw-t");
      
      if (iwOuter) {
        iwOuter.style.background = "#121215";
        iwOuter.style.border = "1px solid #26262b";
        iwOuter.style.boxShadow = "0 8px 30px rgba(0,0,0,0.8)";
        iwOuter.style.padding = "0";
      }
      if (iwBackground) {
        iwBackground.style.overflow = "hidden";
        iwBackground.style.padding = "0";
      }
      
      // Select close button
      const closeImg = document.querySelector(".gm-ui-hover-effect");
      if (closeImg) {
        closeImg.style.top = "6px";
        closeImg.style.right = "6px";
        closeImg.style.background = "rgba(0,0,0,0.5)";
        closeImg.style.borderRadius = "50%";
        closeImg.querySelector("span").style.backgroundColor = "#fff";
      }
    });

    infoWindow.open(map, marker);
  };

  // ── FALLBACK INTERACTIVE MAP (SVG/CANVAS STYLE) ───────────────
  
  // Mapping coordinates of salons to local 500x400 map coordinates
  const mapCoordsToXY = (lat, lng) => {
    // Bangalore boundaries covering our seeded salons
    const latMin = 12.955;
    const latMax = 12.978;
    const lngMin = 77.590;
    const lngMax = 77.655;

    const xPct = (lng - lngMin) / (lngMax - lngMin);
    const yPct = 1 - (lat - latMin) / (latMax - latMin); // Flip Y for screen

    const padding = 50;
    const x = padding + xPct * (500 - padding * 2);
    const y = padding + yPct * (400 - padding * 2);
    return { x, y };
  };

  const handleFallbackMarkerClick = (salon) => {
    setActiveFallbackMarker(salon);
    onSelectSalon(salon);
  };

  // Sync active marker on fallback when selectedSalon props change
  useEffect(() => {
    if (useFallback && selectedSalon) {
      setActiveFallbackMarker(selectedSalon);
    }
  }, [selectedSalon, useFallback]);

  if (useFallback) {
    return (
      <div style={styles.fallbackContainer}>
        {/* Fallback Map Header */}
        <div style={styles.fallbackHeader}>
          <span style={styles.fallbackIndicator}>✨ Aura Interactive Map (Demo mode)</span>
          <p style={styles.fallbackSub}>Interactive Bangalore Luxury Grid representation</p>
        </div>

        {/* Map Vector Grid */}
        <div style={styles.mapGridWrap}>
          <svg viewBox="0 0 500 400" style={styles.svgMap}>
            {/* Grid Lines */}
            <defs>
              <pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse">
                <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#1d1d22" strokeWidth="0.8" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="#121215" />
            <rect width="100%" height="100%" fill="url(#grid)" />

            {/* Concentric Distance Rings */}
            <circle cx="200" cy="220" r="140" fill="none" stroke="rgba(197,168,128,0.03)" strokeWidth="1" strokeDasharray="5,5" />
            <circle cx="200" cy="220" r="80" fill="none" stroke="rgba(197,168,128,0.05)" strokeWidth="1" strokeDasharray="3,3" />

            {/* Stylized Transit / Main Roads */}
            <path d="M 40,220 L 460,220" stroke="#1e1e24" strokeWidth="3" opacity="0.6" />
            <path d="M 200,40 L 200,360" stroke="#1e1e24" strokeWidth="3" opacity="0.6" />
            <path d="M 40,40 L 460,360" stroke="#17171d" strokeWidth="1.5" opacity="0.4" />
            
            {/* Neighborhood Labels */}
            <text x="210" y="60" fill="#71717a" fontSize="10" fontWeight="bold" letterSpacing="1" opacity="0.5">ASHOK NAGAR</text>
            <text x="70" y="240" fill="#71717a" fontSize="10" fontWeight="bold" letterSpacing="1" opacity="0.5">UB CITY</text>
            <text x="350" y="160" fill="#71717a" fontSize="10" fontWeight="bold" letterSpacing="1" opacity="0.5">INDIRANAGAR</text>
            <text x="360" y="320" fill="#71717a" fontSize="10" fontWeight="bold" letterSpacing="1" opacity="0.5">OLD AIRPORT RD</text>

            {/* Road connection line */}
            <path d="M 120,210 L 210,210 L 390,180" fill="none" stroke="rgba(197,168,128,0.12)" strokeWidth="1" />

            {/* Salon Markers */}
            {salons.map((s) => {
              if (!s.latitude || !s.longitude) return null;
              const { x, y } = mapCoordsToXY(s.latitude, s.longitude);
              const isActive = activeFallbackMarker?.id === s.id;

              return (
                <g key={s.id} onClick={() => handleFallbackMarkerClick(s)} style={{ cursor: "pointer" }}>
                  {/* Glowing pulse rings */}
                  {isActive && (
                    <circle cx={x} cy={y} r="16" fill="rgba(197,168,128,0.18)" stroke="rgba(197,168,128,0.5)" strokeWidth="1">
                      <animate attributeName="r" values="8;18;8" dur="2s" repeatCount="indefinite" />
                      <animate attributeName="opacity" values="0.8;0;0.8" dur="2s" repeatCount="indefinite" />
                    </circle>
                  )}

                  {/* Marker Pin */}
                  <circle
                    cx={x}
                    cy={y}
                    r={isActive ? "7" : "5"}
                    fill={isActive ? "#e8d5b7" : "#c5a880"}
                    stroke="#08080a"
                    strokeWidth="1.5"
                    style={{ transition: "all 0.2s" }}
                  />
                  
                  {/* Salon Initial Label */}
                  <text
                    x={x + 10}
                    y={y + 4}
                    fill={isActive ? "#c5a880" : "#a1a1aa"}
                    fontSize="9"
                    fontWeight={isActive ? "700" : "500"}
                    style={{ transition: "all 0.2s" }}
                  >
                    {s.name.split(" ")[0]}
                  </text>
                </g>
              );
            })}
          </svg>

          {/* Active Marker Info Card (Popup Overlay) */}
          {activeFallbackMarker && (
            <div style={styles.fallbackPopup}>
              <button 
                onClick={() => setActiveFallbackMarker(null)} 
                style={styles.popupClose}
              >
                ×
              </button>
              
              <div style={styles.popupInner}>
                <img 
                  src={activeFallbackMarker.image_url} 
                  alt={activeFallbackMarker.name} 
                  style={styles.popupImg} 
                />
                <div style={styles.popupInfo}>
                  <div style={styles.popupNameRow}>
                    <h4 style={styles.popupTitle}>{activeFallbackMarker.name}</h4>
                    <span style={styles.popupPrice}>{activeFallbackMarker.price_range}</span>
                  </div>
                  <div style={styles.popupMeta}>
                    <span>📍 {activeFallbackMarker.area}</span>
                    <span style={{ color: "#c5a880" }}>★ {activeFallbackMarker.rating}</span>
                  </div>
                  <div style={styles.popupBtns}>
                    <a 
                      href={`https://www.google.com/maps/dir/?api=1&destination=${activeFallbackMarker.latitude},${activeFallbackMarker.longitude}`}
                      target="_blank" 
                      rel="noopener noreferrer"
                      style={styles.popupDirBtn}
                    >
                      Directions
                    </a>
                    <button 
                      onClick={() => onSelectSalon(activeFallbackMarker)}
                      style={styles.popupSelectBtn}
                    >
                      {selectedSalon?.id === activeFallbackMarker.id ? "Selected ✓" : "Select Salon"}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div style={styles.mapContainer}>
      <div ref={mapRef} style={{ width: "100%", height: "100%" }} />
    </div>
  );
}

// ── Google Maps dark theme JSON ────────────────────────────────
const darkMapStyles = [
  { elementType: "geometry", stylers: [{ color: "#121215" }] },
  { elementType: "labels.text.stroke", stylers: [{ color: "#121215" }] },
  { elementType: "labels.text.fill", stylers: [{ color: "#8a704c" }] },
  {
    featureType: "administrative.locality",
    elementType: "labels.text.fill",
    stylers: [{ color: "#c5a880" }],
  },
  {
    featureType: "poi",
    elementType: "labels.text.fill",
    stylers: [{ color: "#71717a" }],
  },
  {
    featureType: "poi.park",
    elementType: "geometry",
    stylers: [{ color: "#08080a" }],
  },
  {
    featureType: "poi.park",
    elementType: "labels.text.fill",
    stylers: [{ color: "#52525b" }],
  },
  {
    featureType: "road",
    elementType: "geometry",
    stylers: [{ color: "#26262b" }],
  },
  {
    featureType: "road",
    elementType: "geometry.stroke",
    stylers: [{ color: "#121215" }],
  },
  {
    featureType: "road",
    elementType: "labels.text.fill",
    stylers: [{ color: "#71717a" }],
  },
  {
    featureType: "road.highway",
    elementType: "geometry",
    stylers: [{ color: "#1a1a1f" }],
  },
  {
    featureType: "road.highway",
    elementType: "geometry.stroke",
    stylers: [{ color: "#121215" }],
  },
  {
    featureType: "road.highway",
    elementType: "labels.text.fill",
    stylers: [{ color: "#a1a1aa" }],
  },
  {
    featureType: "water",
    elementType: "geometry",
    stylers: [{ color: "#08080a" }],
  },
  {
    featureType: "water",
    elementType: "labels.text.fill",
    stylers: [{ color: "#3f3f46" }],
  },
];

// ── Styles ─────────────────────────────────────────────────────
const styles = {
  mapContainer: {
    width: "100%",
    height: "100%",
    minHeight: "450px",
    background: "#121215",
    borderRadius: "10px",
    overflow: "hidden",
    border: "1px solid #26262b",
  },
  fallbackContainer: {
    width: "100%",
    height: "100%",
    minHeight: "450px",
    background: "#121215",
    borderRadius: "10px",
    overflow: "hidden",
    border: "1px solid #26262b",
    display: "flex",
    flexDirection: "column",
    position: "relative",
    fontFamily: "'Plus Jakarta Sans', sans-serif",
  },
  fallbackHeader: {
    padding: "12px 16px",
    borderBottom: "1px solid #26262b",
    background: "#08080a",
  },
  fallbackIndicator: {
    display: "block",
    fontSize: "0.82rem",
    fontWeight: 700,
    color: "#c5a880",
    letterSpacing: "0.05em",
  },
  fallbackSub: {
    fontSize: "0.72rem",
    color: "#71717a",
    margin: "2px 0 0 0",
  },
  mapGridWrap: {
    position: "relative",
    flex: 1,
    overflow: "hidden",
    display: "flex",
  },
  svgMap: {
    width: "100%",
    height: "100%",
    minHeight: "360px",
    display: "block",
  },
  fallbackPopup: {
    position: "absolute",
    bottom: "16px",
    left: "16px",
    right: "16px",
    background: "#121215",
    border: "1px solid #26262b",
    borderRadius: "8px",
    padding: "12px",
    boxShadow: "0 8px 30px rgba(0,0,0,0.8)",
    animation: "fadeIn 0.3s ease-out",
    zIndex: 10,
  },
  popupClose: {
    position: "absolute",
    top: "6px",
    right: "10px",
    background: "transparent",
    border: "none",
    color: "#a1a1aa",
    fontSize: "1.1rem",
    cursor: "pointer",
    padding: "0",
  },
  popupInner: {
    display: "flex",
    gap: "12px",
    alignItems: "center",
  },
  popupImg: {
    width: "70px",
    height: "70px",
    objectFit: "cover",
    borderRadius: "6px",
    border: "1px solid #26262b",
  },
  popupInfo: {
    flex: 1,
  },
  popupNameRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "2px",
  },
  popupTitle: {
    fontFamily: "'Playfair Display', serif",
    fontSize: "0.92rem",
    margin: "0",
    fontWeight: 600,
    color: "#fcfcfd",
  },
  popupPrice: {
    fontSize: "0.7rem",
    color: "#c5a880",
    fontWeight: 700,
  },
  popupMeta: {
    display: "flex",
    justifyContent: "space-between",
    fontSize: "0.75rem",
    color: "#a1a1aa",
    marginBottom: "8px",
  },
  popupBtns: {
    display: "flex",
    gap: "6px",
  },
  popupDirBtn: {
    flex: 1,
    background: "#1a1a1f",
    border: "1px solid #26262b",
    color: "#c5a880",
    textDecoration: "none",
    textAlign: "center",
    padding: "5px",
    borderRadius: "4px",
    fontSize: "0.75rem",
    fontWeight: 600,
    display: "block",
  },
  popupSelectBtn: {
    flex: 1.2,
    background: "linear-gradient(135deg,#8a704c,#c5a880)",
    border: "none",
    color: "#0e0e0e",
    padding: "5px",
    borderRadius: "4px",
    fontSize: "0.75rem",
    fontWeight: 700,
    cursor: "pointer",
  },
};
