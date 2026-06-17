/**
 * Aura: Bangalore Luxury Salon Finder & AI Concierge
 * Core Application Logic
 */

// ==========================================
// 1. SALON DATABASE (Curated Real-world Data)
// ==========================================
const SALONS_DATA = [
  {
    id: 1,
    name: "Rossano Ferretti Hair Spa",
    location: "Ashok Nagar (Ritz-Carlton)",
    area: "Ashok Nagar",
    tagline: "The Ritz-Carlton, Level 5. Home of the legendary 'Method' haircut.",
    description: "Experience the unique 'Method Cut' created by Rossano Ferretti, focusing on the natural fall of the hair. This ultra-premium Italian spa caters to high-net-worth individuals, celebrities, and global travelers with private suites and customizable hair care rituals.",
    image: "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?q=80&w=800&auto=format&fit=crop",
    rating: 4.9,
    reviewsCount: 142,
    priceRange: "₹₹₹₹",
    startingPrice: 5000,
    amenities: ["Valet Parking", "Complimentary Champagne", "Private Styling Suites", "Italian Espresso Bar", "Organic Hair Products"],
    tags: ["Italian Method", "Ritz Carlton", "VIP Treatment", "valet", "champagne"],
    services: [
      { id: "s1_1", category: "Hair Care", name: "The Method Precision Haircut", price: 5500, duration: "60 mins", desc: "Rossano Ferretti's signature haircut tailored to your hair's natural fall." },
      { id: "s1_2", category: "Hair Care", name: "Phyto-Organic Hair Spa Ritual", price: 6500, duration: "75 mins", desc: "Customized hot oil and steam treatment using premium bio-active ingredients." },
      { id: "s1_3", category: "Skin Care", name: "Gold Illuminating Facial", price: 7500, duration: "90 mins", desc: "Caviar and gold dust facial for instant skin firming and cell renewal." }
    ],
    stylists: [
      { name: "Alessandro Rossi", role: "Artistic Director", rating: 4.9, image: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=150&auto=format&fit=crop", specialty: "Signature Method Cuts" },
      { name: "Meera Hegde", role: "Senior Master Colorist", rating: 4.8, image: "https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=150&auto=format&fit=crop", specialty: "French Balayage & Highlights" }
    ]
  },
  {
    id: 2,
    name: "Play Salon - UB City",
    location: "UB City, Vittal Mallya Road",
    area: "UB City",
    tagline: "Bangalore's premium address for high-fashion color and styling.",
    description: "Located in the heart of Bangalore's most luxurious retail hub, Play Salon UB City delivers top-tier styling, luxury Kerastase hair rituals, and flawless makeup. Famous for its energetic vibe and highly trained master colorists.",
    image: "https://images.unsplash.com/photo-1562322140-8baeececf3df?q=80&w=800&auto=format&fit=crop",
    rating: 4.8,
    reviewsCount: 389,
    priceRange: "₹₹₹",
    startingPrice: 3500,
    amenities: ["Valet Parking", "Gourmet Beverages", "L'Oreal Certified Tech", "Nail Bar Lounge", "WiFi Zone"],
    tags: ["Balayage", "UB City", "Kerastase Ritual", "valet"],
    services: [
      { id: "s2_1", category: "Hair Care", name: "Premium French Balayage", price: 8500, duration: "180 mins", desc: "Expert hand-painted custom coloring for seamless, sun-kissed results." },
      { id: "s2_2", category: "Hair Care", name: "Kerastase Fusio-Dose Ritual", price: 4000, duration: "45 mins", desc: "Instant fiber transformation with highly concentrated active ingredients." },
      { id: "s2_3", category: "Nails & Grooming", name: "Chrome Gel Manicure & Pedicure", price: 3000, duration: "60 mins", desc: "Long-lasting high gloss gel overlay with premium scrub." }
    ],
    stylists: [
      { name: "Rahul Sharma", role: "Creative Director", rating: 4.9, image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=150&auto=format&fit=crop", specialty: "Avant-Garde Color" },
      { name: "Sarah Fernandes", role: "Senior Stylist", rating: 4.7, image: "https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?q=80&w=150&auto=format&fit=crop", specialty: "Keratin & Texture Control" }
    ]
  },
  {
    id: 3,
    name: "Warren Tricomi",
    location: "JW Marriott, Vittal Mallya Road",
    area: "Ashok Nagar",
    tagline: "New York style meets global luxury at the JW Marriott.",
    description: "Straight from Manhattan, Warren Tricomi at the JW Marriott offers an unparalleled salon environment. Enjoy breathtaking luxury overlooking Cubbon Park while receiving premium NYC-style custom styling and rejuvenating body spa rituals.",
    image: "https://images.unsplash.com/photo-1633681926022-84c23e8cb2d6?q=80&w=800&auto=format&fit=crop",
    rating: 4.7,
    reviewsCount: 212,
    priceRange: "₹₹₹₹",
    startingPrice: 4000,
    amenities: ["Valet Parking", "Complimentary Champagne", "Private VIP Pods", "Park View Lounge", "Organic Tea Service"],
    tags: ["NYC Style", "JW Marriott", "Bridal Specialist", "valet", "champagne"],
    services: [
      { id: "s3_1", category: "Hair Care", name: "NYC Couture Haircut", price: 4500, duration: "60 mins", desc: "Precision haircut customized for your lifestyle by NYC-certified stylists." },
      { id: "s3_2", category: "Skin Care", name: "24k Gold Collagen Facial", price: 8000, duration: "90 mins", desc: "Premium anti-aging facial with active collagen builders and 24k gold leaf." },
      { id: "s3_3", category: "Spa Treatments", name: "Deep Tissue Balinese Massage", price: 5500, duration: "90 mins", desc: "Traditional firm physical massage utilizing acupressure and aromatherapy oils." }
    ],
    stylists: [
      { name: "John Carter", role: "Global Style Expert", rating: 4.9, image: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=150&auto=format&fit=crop", specialty: "Couture Restyling" },
      { name: "Anjali Rao", role: "Skin Therapist", rating: 4.8, image: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=150&auto=format&fit=crop", specialty: "Medical & Gold Facials" }
    ]
  },
  {
    id: 4,
    name: "Jean-Claude Biguine (JCB)",
    location: "Lavelle Road, Near Richmond Circle",
    area: "UB City",
    tagline: "Chic French salon offering organic scalp care and precision hair color.",
    description: "JCB Paris brings global expertise in French hairstyles, organic therapies, and premium skin treatments. The Lavelle Road villa is a green, serene luxury sanctuary with high ceilings, private treatment rooms, and a calming outdoor terrace.",
    image: "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?q=80&w=800&auto=format&fit=crop",
    rating: 4.6,
    reviewsCount: 540,
    priceRange: "₹₹₹",
    startingPrice: 3000,
    amenities: ["Valet Parking", "Lavazza Coffee Bar", "Organic Hair Dye Option", "Garden Waiting Lounge", "Kids Stylist Station"],
    tags: ["French Color", "Organic Spa", "Scalp Care", "valet"],
    services: [
      { id: "s4_1", category: "Hair Care", name: "JCB Parisian Balayage Duo", price: 7500, duration: "150 mins", desc: "Elegant hand-blended coloring with deep hair conditioning treatment." },
      { id: "s4_2", category: "Skin Care", name: "Sothys Organic Brightening Facial", price: 5000, duration: "75 mins", desc: "Exclusive French organic skin treatment focusing on glow and hydration." },
      { id: "s4_3", category: "Hair Care", name: "Scalp Renewal Detox Ritual", price: 3500, duration: "60 mins", desc: "Deep exfoliating treatment with tea tree oils and micro-mist steamer." }
    ],
    stylists: [
      { name: "Pierre Dubois", role: "French Style Lead", rating: 4.8, image: "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=150&auto=format&fit=crop", specialty: "Classic Parisian Bob & Cuts" },
      { name: "Priya Nair", role: "Senior Scalp Specialist", rating: 4.7, image: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=150&auto=format&fit=crop", specialty: "Scalp Detox & Revitalization" }
    ]
  },
  {
    id: 5,
    name: "BBlunt Premium",
    location: "100 Feet Road, Indiranagar",
    area: "Indiranagar",
    tagline: "Bold, contemporary styling in Bangalore's trendiest hub.",
    description: "BBlunt Indiranagar specializes in cutting-edge hair makeovers, premium hair extensions, and custom colors. Tailored for the modern Bangalore crowd looking for trendy transformations, creative colors, and high-fashion styling.",
    image: "https://images.unsplash.com/photo-1596178065887-1198b6148b2b?q=80&w=800&auto=format&fit=crop",
    rating: 4.5,
    reviewsCount: 612,
    priceRange: "₹₹",
    startingPrice: 2500,
    amenities: ["Self Parking", "Complimentary Brews", "Music Lounges", "Extension Studio", "Express Hair Blowout Bar"],
    tags: ["Bold Makeover", "Extensions", "Indiranagar Styling"],
    services: [
      { id: "s5_1", category: "Hair Care", name: "BBlunt Signature Makeover Cut", price: 2800, duration: "60 mins", desc: "Full consultations and dramatic restyling by precision cutting experts." },
      { id: "s5_2", category: "Hair Care", name: "Ombre/Pastel Creative Color", price: 6500, duration: "120 mins", desc: "Vibrant high-contrast hair colors with plex fiber protection system." },
      { id: "s5_3", category: "Nails & Grooming", name: "Signature Chrome Pedicure Spa", price: 2200, duration: "60 mins", desc: "Soothing foot bath, scrub, massage and premium chrome varnish finish." }
    ],
    stylists: [
      { name: "Vikram Sen", role: "Creative Master Stylist", rating: 4.7, image: "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?q=80&w=150&auto=format&fit=crop", specialty: "Creative Cuts & Makeovers" },
      { name: "Kavitha Raj", role: "Color Specialist", rating: 4.6, image: "https://images.unsplash.com/photo-1554151228-14d9def656e4?q=80&w=150&auto=format&fit=crop", specialty: "Vibrant Creative Highlights" }
    ]
  },
  {
    id: 6,
    name: "The Spa & Salon",
    location: "The Leela Palace, Old Airport Road",
    area: "Old Airport Road",
    tagline: "An aristocratic oasis of rejuvenation and wellness.",
    description: "Surround yourself with gold leaf ceilings, royal gardens, and absolute peace. The Leela Palace Spa offers traditional Ayurvedic therapies, elite global massage rituals, and an ultra-exclusive hair salon dedicated to regal pampering.",
    image: "https://images.unsplash.com/photo-1519699047748-de8e457a634e?q=80&w=800&auto=format&fit=crop",
    rating: 4.9,
    reviewsCount: 198,
    priceRange: "₹₹₹₹",
    startingPrice: 6000,
    amenities: ["Valet Parking", "Complimentary Champagne", "Imperial Pool View", "Private Steam & Jacuzzi Suite", "Ayurvedic Doctors Consultation"],
    tags: ["Ayurvedic Massage", "Leela Palace", "Royal Wellness", "valet", "champagne"],
    services: [
      { id: "s6_1", category: "Spa Treatments", name: "The Leela Palace Royal Massage", price: 7500, duration: "90 mins", desc: "Indulgent four-hand massage using hot herbal oils and traditional luxury stroke techniques." },
      { id: "s6_2", category: "Spa Treatments", name: "Traditional Abhyanga Spa Ritual", price: 6000, duration: "75 mins", desc: "Authentic Ayurvedic synchronization massage focusing on toxic drainage and skin glow." },
      { id: "s6_3", category: "Skin Care", name: "Sundaÿ Ayurvedic Radiance Facial", price: 7000, duration: "75 mins", desc: "Gold clay, saffron, and fresh sandalwood facial for timeless complexion rejuvenation." }
    ],
    stylists: [
      { name: "Dr. Manoj Kumar", role: "Wellness Consultant", rating: 4.9, image: "https://images.unsplash.com/photo-1622253692010-333f2da6031d?q=80&w=150&auto=format&fit=crop", specialty: "Ayurveda & Healing Spas" },
      { name: "Sophia D'Souza", role: "Elite Therapist", rating: 4.8, image: "https://images.unsplash.com/photo-1594744803329-e58b31de215f?q=80&w=150&auto=format&fit=crop", specialty: "Balinese & Hot Stone Massage" }
    ]
  }
];

// ==========================================
// 2. STATE STORE
// ==========================================
const AppState = {
  activeTab: "explore-section",
  searchQuery: "",
  areaFilter: "",
  categoryFilter: "",
  activeTag: "",
  compareList: [], // Array of Salon IDs
  bookings: [], // Array of booking objects
  
  // Active booking modal wizard state
  bookingWizard: {
    salonId: null,
    serviceId: null,
    stylistName: null,
    date: null,
    timeSlot: null,
    currentStep: 1
  },
  
  // AI Advisor conversation thread state
  aiState: {
    step: 0,
    focus: "",
    concern: "",
    vibe: ""
  }
};

// Available time slots (fixed mockup)
const TIME_SLOTS = [
  "10:00 AM - 11:00 AM",
  "11:00 AM - 12:00 PM",
  "01:00 PM - 02:00 PM",
  "02:00 PM - 03:00 PM",
  "03:00 PM - 04:00 PM",
  "05:00 PM - 06:00 PM",
  "07:00 PM - 08:00 PM"
];

// ==========================================
// 3. INITIALIZATION & ROUTING
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
  // Load saved bookings from LocalStorage
  loadBookingsFromStorage();
  
  // Set up SPA tabs navigation
  initNavigation();
  
  // Load explore grid items
  renderSalonsGrid();
  
  // Set up filter events
  initFilters();
  
  // Initialize AI chatbot
  initAIChat();
  
  // Initialize Booking Wizard elements
  initBookingWizard();
  
  // Initialize Map features
  initMapModal();
  
  // Window scroll navbar effect
  window.addEventListener("scroll", () => {
    const navbar = document.getElementById("mainNavbar");
    if (window.scrollY > 20) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  });

  // Handle CTA Booking Trigger from landing banner
  document.getElementById("navBookNowBtn").addEventListener("click", () => {
    openBookingModal();
  });
  document.getElementById("bookFirstBtn").addEventListener("click", () => {
    openBookingModal();
  });
});

// Navigation logic (Tab switching)
function initNavigation() {
  const navLinks = document.querySelectorAll(".nav-link");
  const sections = document.querySelectorAll(".page-section");
  const heroBanner = document.getElementById("heroBanner");
  
  navLinks.forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const target = link.getAttribute("data-target");
      
      // Update links active state
      navLinks.forEach(l => l.classList.remove("active"));
      link.classList.add("active");
      
      // Toggle pages viewport
      sections.forEach(sec => {
        sec.classList.remove("active");
        if (sec.id === target) {
          sec.classList.add("active");
        }
      });
      
      // Hide hero banner on other pages to save screen space, only show on Explore
      if (target === "explore-section") {
        heroBanner.style.display = "flex";
      } else {
        heroBanner.style.display = "none";
      }
      
      AppState.activeTab = target;
      window.scrollTo(0, 0);
      
      // If navigating to compare section, draw the grid
      if (target === "compare-section") {
        renderComparisonMatrix();
      }
      // If navigating to bookings section, draw bookings list
      if (target === "bookings-section") {
        renderBookings();
      }
    });
  });
  
  // Brand Logo click resets to Explore tab
  document.getElementById("navLogo").addEventListener("click", (e) => {
    e.preventDefault();
    document.querySelector("[data-target='explore-section']").click();
  });
}

// ==========================================
// 4. EXPLORE / FILTERING MODULE
// ==========================================
function initFilters() {
  const searchInput = document.getElementById("searchInput");
  const areaFilter = document.getElementById("areaFilter");
  const categoryFilter = document.getElementById("categoryFilter");
  const searchBtn = document.getElementById("searchBtn");
  const tagBtns = document.querySelectorAll(".tag-btn");
  
  // Real-time search keyup/change triggers filtration
  const triggerFilter = () => {
    AppState.searchQuery = searchInput.value.toLowerCase().trim();
    AppState.areaFilter = areaFilter.value;
    AppState.categoryFilter = categoryFilter.value;
    renderSalonsGrid();
  };
  
  searchInput.addEventListener("input", triggerFilter);
  areaFilter.addEventListener("change", triggerFilter);
  categoryFilter.addEventListener("change", triggerFilter);
  searchBtn.addEventListener("click", triggerFilter);
  
  // Quick recommendation chips
  tagBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tagBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      
      AppState.activeTag = btn.getAttribute("data-val");
      renderSalonsGrid();
    });
  });
  
  // Handle footer category/location shortcuts
  document.querySelectorAll(".footer-loc-link").forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      document.querySelector("[data-target='explore-section']").click();
      areaFilter.value = link.getAttribute("data-loc");
      triggerFilter();
    });
  });
  document.querySelectorAll(".footer-service-link").forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      document.querySelector("[data-target='explore-section']").click();
      // Set active tag and filter
      const cat = link.getAttribute("data-cat");
      const tagBtn = Array.from(tagBtns).find(b => b.getAttribute("data-val") === cat);
      if (tagBtn) {
        tagBtn.click();
      } else {
        searchInput.value = cat;
        triggerFilter();
      }
    });
  });
}

function renderSalonsGrid() {
  const grid = document.getElementById("salonsGrid");
  const label = document.getElementById("salonCountLabel");
  
  // Filter core list
  const filtered = SALONS_DATA.filter(salon => {
    // 1. Text Query Search (name, location, tagline, description, services, stylists)
    const matchesSearch = AppState.searchQuery === "" || 
      salon.name.toLowerCase().includes(AppState.searchQuery) ||
      salon.location.toLowerCase().includes(AppState.searchQuery) ||
      salon.tagline.toLowerCase().includes(AppState.searchQuery) ||
      salon.description.toLowerCase().includes(AppState.searchQuery) ||
      salon.services.some(s => s.name.toLowerCase().includes(AppState.searchQuery)) ||
      salon.stylists.some(st => st.name.toLowerCase().includes(AppState.searchQuery));
      
    // 2. Area Dropdown Filter
    const matchesArea = AppState.areaFilter === "" || salon.area === AppState.areaFilter;
    
    // 3. Category Dropdown Filter
    const matchesCategory = AppState.categoryFilter === "" || 
      salon.services.some(s => s.category === AppState.categoryFilter);
      
    // 4. Tag Button Filter (Gold Facial, Method Cut, valet, champagne etc)
    const matchesTag = AppState.activeTag === "" || 
      salon.tags.includes(AppState.activeTag) ||
      salon.amenities.some(a => a.toLowerCase().includes(AppState.activeTag.toLowerCase())) ||
      salon.services.some(s => s.name.toLowerCase().includes(AppState.activeTag.toLowerCase()));
      
    return matchesSearch && matchesArea && matchesCategory && matchesTag;
  });
  
  // Update UI count label
  label.innerText = `Showing ${filtered.length} luxury establishments`;
  
  if (filtered.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: var(--text-muted);">
        <i class="fa-solid fa-face-frown" style="font-size: 3rem; margin-bottom: 16px; color: var(--accent-gold);"></i>
        <h3>No matching luxury salons found</h3>
        <p style="margin-top: 8px;">Try refining your filters, choosing a different neighborhood, or removing tags.</p>
      </div>
    `;
    return;
  }
  
  // Render cards
  grid.innerHTML = filtered.map(salon => {
    const isChecked = AppState.compareList.includes(salon.id) ? 'checked' : '';
    const stars = '★'.repeat(Math.floor(salon.rating)) + (salon.rating % 1 >= 0.5 ? '½' : '');
    
    return `
      <div class="salon-card" data-id="${salon.id}">
        <div class="card-img-wrapper">
          <div class="card-badge">${salon.area}</div>
          <div class="card-rating-float">
            <span class="rating-star"><i class="fa-solid fa-star"></i></span>
            <span>${salon.rating}</span>
          </div>
          <img src="${salon.image}" alt="${salon.name}" class="card-img" loading="lazy">
        </div>
        
        <div class="card-content">
          <div class="card-meta">${salon.priceRange} • ${salon.location}</div>
          <h3 class="card-title">${salon.name}</h3>
          <p class="card-desc">${salon.tagline}</p>
          
          <div class="card-features">
            ${salon.amenities.slice(0, 3).map(a => `<span class="feature-chip">${a}</span>`).join('')}
            ${salon.amenities.length > 3 ? `<span class="feature-chip">+${salon.amenities.length - 3} more</span>` : ''}
          </div>
          
          <div class="card-footer">
            <div class="card-price-info">
              <span class="card-price-label">Services From</span>
              <span class="card-price-val">₹${salon.startingPrice.toLocaleString()}</span>
            </div>
            
            <div class="card-actions">
              <label class="compare-chk-wrapper">
                <input type="checkbox" class="compare-checkbox" data-id="${salon.id}" ${isChecked}>
                <span>Compare</span>
              </label>
              <button class="btn btn-primary btn-sm book-btn-trigger" data-id="${salon.id}">Book Now</button>
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');
  
  // Attach Event Listeners to rendered cards
  grid.querySelectorAll(".book-btn-trigger").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = parseInt(btn.getAttribute("data-id"));
      openBookingModal(id);
    });
  });
  
  grid.querySelectorAll(".compare-checkbox").forEach(chk => {
    chk.addEventListener("change", (e) => {
      const id = parseInt(chk.getAttribute("data-id"));
      toggleCompareSalon(id, e.target.checked);
    });
  });
}

// ==========================================
// 5. COMPARISON SYSTEM
// ==========================================
function toggleCompareSalon(id, isChecked) {
  const index = AppState.compareList.indexOf(id);
  
  if (isChecked && index === -1) {
    // Limit to max 3
    if (AppState.compareList.length >= 3) {
      alert("Aura Premium: You can compare up to 3 salons simultaneously.");
      // Uncheck input box visually
      const chk = document.querySelector(`.compare-checkbox[data-id="${id}"]`);
      if (chk) chk.checked = false;
      return;
    }
    AppState.compareList.push(id);
  } else if (!isChecked && index !== -1) {
    AppState.compareList.splice(index, 1);
  }
  
  updateCompareDrawer();
}

function updateCompareDrawer() {
  const drawer = document.getElementById("compareDrawer");
  const countBadge = document.getElementById("compareCountBadge");
  const thumbsWrapper = document.getElementById("compareDrawerThumbs");
  
  const count = AppState.compareList.length;
  countBadge.innerText = count;
  
  if (count > 0) {
    // Generate thumbnail pictures of compared salons
    thumbsWrapper.innerHTML = AppState.compareList.map(id => {
      const salon = SALONS_DATA.find(s => s.id === id);
      return `<img src="${salon.image}" alt="${salon.name}" class="compare-thumb-img" title="${salon.name}">`;
    }).join('');
    
    drawer.classList.add("active");
  } else {
    drawer.classList.remove("active");
  }
}

// Clear all selected items in comparison
document.getElementById("clearCompareBtn").addEventListener("click", () => {
  AppState.compareList = [];
  // Uncheck all explore checkboxes
  document.querySelectorAll(".compare-checkbox").forEach(c => c.checked = false);
  updateCompareDrawer();
  
  if (AppState.activeTab === "compare-section") {
    renderComparisonMatrix();
  }
});

// Navigate and render comparison Matrix tab
document.getElementById("compareNowBtn").addEventListener("click", () => {
  document.querySelector("[data-target='compare-section']").click();
});

function renderComparisonMatrix() {
  const container = document.getElementById("comparisonContainer");
  
  if (AppState.compareList.length === 0) {
    container.innerHTML = `
      <div class="empty-bookings">
        <div class="empty-bookings-icon"><i class="fa-solid fa-code-compare"></i></div>
        <h3>No Salons Selected for Comparison</h3>
        <p style="margin-bottom: 20px;">Go to the Explore Salons page and check "Compare" on your favorite salons to see their side-by-side comparison.</p>
        <button class="btn btn-primary" onclick="document.querySelector('[data-target=\'explore-section\']').click()">
          Go to Explore
        </button>
      </div>
    `;
    return;
  }
  
  // Build details comparison table
  const selectedSalons = AppState.compareList.map(id => SALONS_DATA.find(s => s.id === id));
  
  // Gather all unique amenities across selected salons for standard row mapping
  const allAmenities = [
    "Valet Parking",
    "Complimentary Champagne",
    "Private Styling Suites",
    "Gourmet Beverages",
    "WiFi Zone",
    "Organic Hair Products"
  ];
  
  let headerHtml = `
    <th>
      <div class="comparison-col-header">
        <div style="font-size: 0.8rem; text-transform: uppercase; color: var(--accent-gold);">Feature Grid</div>
        <div style="font-size: 1.1rem; font-family: var(--font-serif);">Matrix Overview</div>
      </div>
    </th>
  `;
  
  let mainDetailsHtml = "";
  
  selectedSalons.forEach(salon => {
    headerHtml += `
      <th>
        <div class="comparison-col-header" style="text-align: center;">
          <img src="${salon.image}" alt="${salon.name}" class="comparison-salon-logo">
          <div style="font-weight: 700; font-size: 1.1rem; color: #fff;">${salon.name}</div>
          <div style="font-size: 0.8rem; color: var(--accent-gold); margin-top: 4px;">★ ${salon.rating} (${salon.reviewsCount} reviews)</div>
        </div>
      </th>
    `;
  });
  
  // 1. Row: Location Area
  let rowArea = `<tr><td class="comparison-col-label">Neighborhood</td>`;
  selectedSalons.forEach(salon => {
    rowArea += `<td><div style="font-weight: 500;">${salon.area}</div><div style="font-size:0.75rem; color:var(--text-secondary);">${salon.location}</div></td>`;
  });
  rowArea += `</tr>`;
  
  // 2. Row: Pricing Tier
  let rowPrice = `<tr><td class="comparison-col-label">Price Level</td>`;
  selectedSalons.forEach(salon => {
    rowPrice += `<td><span style="color:var(--accent-gold); font-weight:700; font-size:1.1rem;">${salon.priceRange}</span><br><span style="font-size:0.75rem; color:var(--text-muted);">Starts from ₹${salon.startingPrice}</span></td>`;
  });
  rowPrice += `</tr>`;
  
  // 3. Row: Description Philosophy
  let rowDesc = `<tr><td class="comparison-col-label">Aesthetic Vibe</td>`;
  selectedSalons.forEach(salon => {
    rowDesc += `<td style="font-size:0.85rem; color:var(--text-secondary); line-height:1.4;">${salon.tagline}</td>`;
  });
  rowDesc += `</tr>`;
  
  // 4. Amenities rows
  let amenitiesRows = "";
  allAmenities.forEach(amenity => {
    let row = `<tr><td class="comparison-col-label">${amenity}</td>`;
    selectedSalons.forEach(salon => {
      const hasAmenity = salon.amenities.some(a => a.toLowerCase().includes(amenity.toLowerCase()));
      row += `<td>${hasAmenity ? '<span class="matrix-checkmark"><i class="fa-solid fa-circle-check"></i> VIP Yes</span>' : '<span class="matrix-cross"><i class="fa-solid fa-circle-xmark"></i> -</span>'}</td>`;
    });
    row += `</tr>`;
    amenitiesRows += row;
  });
  
  // 5. Signature Services
  let rowServices = `<tr><td class="comparison-col-label">Signature Ritual</td>`;
  selectedSalons.forEach(salon => {
    const signature = salon.services[0];
    rowServices += `
      <td>
        <div style="font-weight: 600; font-size: 0.9rem;">${signature.name}</div>
        <div style="font-size: 0.8rem; color: var(--accent-gold); margin: 2px 0;">₹${signature.price.toLocaleString()} (${signature.duration})</div>
        <div style="font-size: 0.75rem; color: var(--text-muted); line-height:1.3;">${signature.desc}</div>
      </td>
    `;
  });
  rowServices += `</tr>`;
  
  // 6. Action Button booking row
  let rowAction = `<tr><td class="comparison-col-label">Instant Reserve</td>`;
  selectedSalons.forEach(salon => {
    rowAction += `<td><button class="btn btn-primary btn-sm" onclick="openBookingModal(${salon.id})" style="width:100%;">Book at ${salon.name.split(' ')[0]}</button></td>`;
  });
  rowAction += `</tr>`;
  
  container.innerHTML = `
    <div class="comparison-matrix-wrapper">
      <table class="comparison-table">
        <thead>
          <tr>${headerHtml}</tr>
        </thead>
        <tbody>
          ${rowArea}
          ${rowPrice}
          ${rowDesc}
          ${amenitiesRows}
          ${rowServices}
          ${rowAction}
        </tbody>
      </table>
    </div>
  `;
}

// ==========================================
// 6. AI CONCIERGE CHAT MODULE
// ==========================================
function initAIChat() {
  const resetBtn = document.getElementById("resetChatBtn");
  const sendBtn = document.getElementById("chatSendBtn");
  const chatInput = document.getElementById("chatInput");
  
  resetBtn.addEventListener("click", () => {
    resetAIChatHistory();
  });
  
  sendBtn.addEventListener("click", () => {
    handleUserChatMessage();
  });
  
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      handleUserChatMessage();
    }
  });
  
  // Quick profile trigger options
  document.querySelectorAll(".ai-option-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const type = btn.getAttribute("data-trigger");
      triggerAICategoryDialog(type);
    });
  });
  
  // Initiate conversation
  resetAIChatHistory();
}

function resetAIChatHistory() {
  const history = document.getElementById("chatHistory");
  AppState.aiState = { step: 0, focus: "", concern: "", vibe: "" };
  
  history.innerHTML = "";
  appendBotMessage("Salutations. I am **Aura**, your private salon and wellness concierge. I curate bespoke styling profiles and match you with Bangalore's leading practitioners.");
  
  setTimeout(() => {
    appendBotMessage("To tailor your luxury recommendation, please select your primary grooming focus today:", [
      { text: "💇‍♂️ Hair Care & Styling", action: "set_focus_hair" },
      { text: "✨ Skin Care & Facials", action: "set_focus_skin" },
      { text: "💆‍♀️ Spa & Body Massages", action: "set_focus_spa" },
      { text: "💅 VIP Nails & Grooming", action: "set_focus_nails" }
    ]);
  }, 600);
}

function triggerAICategoryDialog(type) {
  resetAIChatHistory();
  setTimeout(() => {
    if (type === "haircut") {
      selectAIChoice("set_focus_hair", "💇‍♂️ Hair Care & Styling");
    } else if (type === "color") {
      selectAIChoice("set_focus_hair", "💇‍♂️ Hair Care & Styling");
      // Advance styling automatically
      setTimeout(() => {
        selectAIChoice("hair_balayage", "French Balayage & Highlights");
      }, 1000);
    } else if (type === "facial") {
      selectAIChoice("set_focus_skin", "✨ Skin Care & Facials");
    }
  }, 200);
}

function handleUserChatMessage() {
  const input = document.getElementById("chatInput");
  const query = input.value.trim();
  if (query === "") return;
  
  appendUserMessage(query);
  input.value = "";
  
  // Show loading indicator
  const loadingId = appendLoadingIndicator();
  
  setTimeout(() => {
    removeLoadingIndicator(loadingId);
    
    // Natural Language Search Simulation
    const qLower = query.toLowerCase();
    
    // Check if the user is looking for specific salon names
    let matchedSalon = null;
    SALONS_DATA.forEach(s => {
      if (qLower.includes(s.name.toLowerCase().split(' ')[0]) || qLower.includes(s.area.toLowerCase())) {
        matchedSalon = s;
      }
    });
    
    if (matchedSalon) {
      appendBotMessage(`Ah, seeking details on **${matchedSalon.name}**? Excellent taste. They are situated in **${matchedSalon.location}**, rated **${matchedSalon.rating}/5.0**, and specialize in premium services starting at ₹${matchedSalon.startingPrice}.`);
      appendRecommendedCard(matchedSalon.id, matchedSalon.services[0].id, matchedSalon.stylists[0].name);
      return;
    }
    
    if (qLower.includes("hello") || qLower.includes("hi") || qLower.includes("hey")) {
      appendBotMessage("Hello! I am Aura. I can help find the perfect luxury salon for you. Would you like to restart our visual styling planner?", [
        { text: "Yes, Start Advisor", action: "restart_advisor" }
      ]);
      return;
    }
    
    if (qLower.includes("price") || qLower.includes("cheap") || qLower.includes("cost") || qLower.includes("rate")) {
      appendBotMessage("Our handpicked catalog represents premium establishments. The starting rates are:\n• **BBlunt Premium**: From ₹2,500\n• **Jean-Claude Biguine**: From ₹3,000\n• **Rossano Ferretti (Ritz)**: From ₹5,000\n\nWould you like me to match you with a salon fits your budget?", [
        { text: "Help Me Choose", action: "restart_advisor" }
      ]);
      return;
    }
    
    // Standard Fallback text search through services
    const matches = SALONS_DATA.filter(s => 
      s.services.some(srv => srv.name.toLowerCase().includes(qLower)) ||
      s.tags.some(t => t.toLowerCase().includes(qLower))
    );
    
    if (matches.length > 0) {
      appendBotMessage(`I've scanned our Bangalore catalog and located ${matches.length} luxury destination(s) matching your request:`);
      matches.forEach(m => {
        appendRecommendedCard(m.id, m.services[0].id, m.stylists[0].name);
      });
    } else {
      appendBotMessage("I've logged your request. While I coordinate with our elite partners, let's proceed with your custom profile curation so I can formulate a stylist pairing.", [
        { text: "Proceed with Questionnaire", action: "restart_advisor" }
      ]);
    }
  }, 1000);
}

// Chat UI helpers
function appendUserMessage(text) {
  const history = document.getElementById("chatHistory");
  const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  const msg = document.createElement("div");
  msg.className = "chat-msg chat-msg-user";
  msg.innerHTML = `
    <div class="msg-bubble">
      <div>${text}</div>
      <span class="msg-time">${time}</span>
    </div>
  `;
  history.appendChild(msg);
  history.scrollTop = history.scrollHeight;
}

function appendBotMessage(text, options = []) {
  const history = document.getElementById("chatHistory");
  const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  // Format basic bold text and bullets
  let formatted = text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>');
    
  const msg = document.createElement("div");
  msg.className = "chat-msg chat-msg-bot";
  
  let optionsHtml = "";
  if (options.length > 0) {
    optionsHtml = `
      <div class="chat-interactive-area">
        <div class="chat-grid-options">
          ${options.map(opt => `<button class="chat-grid-option" data-action="${opt.action}">${opt.text}</button>`).join('')}
        </div>
      </div>
    `;
  }
  
  msg.innerHTML = `
    <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=150&auto=format&fit=crop" alt="Aura AI" style="width:32px; height:32px; border-radius:50%; object-fit:cover; border:1px solid var(--accent-gold);">
    <div class="msg-bubble">
      <div>${formatted}</div>
      ${optionsHtml}
      <span class="msg-time" style="text-align: left;">${time}</span>
    </div>
  `;
  
  history.appendChild(msg);
  history.scrollTop = history.scrollHeight;
  
  // Attach action triggers to buttons
  msg.querySelectorAll(".chat-grid-option").forEach(btn => {
    btn.addEventListener("click", () => {
      const act = btn.getAttribute("data-action");
      const labelText = btn.innerText;
      selectAIChoice(act, labelText);
    });
  });
}

function appendLoadingIndicator() {
  const history = document.getElementById("chatHistory");
  const id = "loading_" + Date.now();
  
  const loadingMsg = document.createElement("div");
  loadingMsg.className = "chat-msg chat-msg-bot";
  loadingMsg.id = id;
  loadingMsg.innerHTML = `
    <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=150&auto=format&fit=crop" alt="Aura AI" style="width:32px; height:32px; border-radius:50%; object-fit:cover; border:1px solid var(--accent-gold);">
    <div class="msg-bubble" style="padding: 10px 14px;">
      <div class="chat-loading">
        <span></span><span></span><span></span>
      </div>
    </div>
  `;
  history.appendChild(loadingMsg);
  history.scrollTop = history.scrollHeight;
  return id;
}

function removeLoadingIndicator(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

// Conversation Tree Routing
function selectAIChoice(action, textLabel) {
  // 1. Log user selection
  appendUserMessage(textLabel);
  
  // Disable option buttons in the active bubble block
  event.target.closest(".chat-grid-options").querySelectorAll("button").forEach(b => {
    b.disabled = true;
    b.style.opacity = 0.5;
  });
  
  const loadingId = appendLoadingIndicator();
  
  setTimeout(() => {
    removeLoadingIndicator(loadingId);
    
    // Core state navigation
    if (action === "restart_advisor") {
      resetAIChatHistory();
      return;
    }
    
    // Step 1: Handling Focus
    if (action.startsWith("set_focus_")) {
      const focus = action.split("set_focus_")[1];
      AppState.aiState.focus = focus;
      AppState.aiState.step = 1;
      
      if (focus === "hair") {
        appendBotMessage("Splendid. Hair styling in Bangalore is an art form. What is your primary design target or hair concern?", [
          { text: "🎨 Balayage & Creative Color", action: "hair_balayage" },
          { text: "✂️ Precision Cut & Reshape", action: "hair_cut" },
          { text: "💆‍♂️ Scalp Detox & Health", action: "hair_scalp" },
          { text: "✨ Hydration & Frizz Repair", action: "hair_repair" }
        ]);
      } else if (focus === "skin") {
        appendBotMessage("Splendid. Skin rejuvenation requires expert technique. What is your primary clinical skin goal?", [
          { text: "🌟 Instant Bridal Radiance", action: "skin_glow" },
          { text: "⏳ Anti-Aging & Collagen Lift", action: "skin_age" },
          { text: "🌿 Deep Organic Exfoliation", action: "skin_organic" }
        ]);
      } else if (focus === "spa") {
        appendBotMessage("Wellness and stress relief are paramount. What style of body healing aligns with you today?", [
          { text: "🌍 Deep Tissue Acupressure", action: "spa_deep" },
          { text: "🪔 Traditional Ayurvedic Abhyanga", action: "spa_ayurvedic" }
        ]);
      } else {
        appendBotMessage("For hand care, pedicure rituals, and high-fashion chrome details, choose your focal point:", [
          { text: "💅 Gel Nail Extensions & Art", action: "nails_art" },
          { text: "🚿 VIP Pedicure Spa Massage", action: "nails_pedi" }
        ]);
      }
      return;
    }
    
    // Step 2: Handling Concern / Style Vibe Request
    if (AppState.aiState.step === 1) {
      AppState.aiState.concern = action;
      AppState.aiState.step = 2;
      
      appendBotMessage("Understood. Finally, what overall stylistic tone best fits your personal brand?", [
        { text: "👑 Elite Classic Elegant", action: "vibe_classic" },
        { text: "🔥 Modern Bold & Creative", action: "vibe_bold" },
        { text: "🏖️ Quiet Luxury & Low Maintenance", action: "vibe_quiet" }
      ]);
      return;
    }
    
    // Step 3: Analyze and recommend
    if (AppState.aiState.step === 2) {
      AppState.aiState.vibe = action;
      
      // Perform AI simulation matching
      appendBotMessage("Formulating elite recommendation card... matching stylist credentials, product supply chains, and salon locations in Bangalore.");
      
      const analysisId = appendLoadingIndicator();
      
      setTimeout(() => {
        removeLoadingIndicator(analysisId);
        
        // Execute recommendation engine
        calculateAIRecommendation();
      }, 1500);
    }
  }, 1000);
}

// Logic mapper that links answers to specific salon/stylist/service database records
function calculateAIRecommendation() {
  const focus = AppState.aiState.focus;
  const concern = AppState.aiState.concern;
  const vibe = AppState.aiState.vibe;
  
  let salonId = 1;
  let serviceId = "s1_1";
  let stylistName = "Alessandro Rossi";
  let reasoning = "";
  
  if (focus === "hair") {
    if (concern === "hair_balayage") {
      salonId = 2; // Play Salon UB City
      serviceId = "s2_1"; // French Balayage
      stylistName = "Rahul Sharma";
      reasoning = "Because you are seeking a **Creative Color Balayage**, we've paired you with **Rahul Sharma** at **Play Salon UB City**. He is internationally trained in high-contrast hand-painted color melts.";
    } else if (concern === "hair_scalp") {
      salonId = 4; // JCB Lavelle Road
      serviceId = "s4_3"; // Scalp Detox
      stylistName = "Priya Nair";
      reasoning = "For **Scalp Health and Detoxification**, **Jean-Claude Biguine Lavelle Road** is unmatched. **Priya Nair** utilizes organic French bio-extracts and micro-mist steam therapy to restore scalp balance.";
    } else if (concern === "hair_repair") {
      salonId = 2; // Play Salon
      serviceId = "s2_2"; // Kerastase Fusio-Dose
      stylistName = "Sarah Fernandes";
      reasoning = "To target **Frizz and Hair damage**, we recommend the ultra-precise **Kerastase Fusio-Dose** at **Play Salon UB City** under **Sarah Fernandes**.";
    } else { // precision cut
      if (vibe === "vibe_bold") {
        salonId = 5; // BBlunt Indiranagar
        serviceId = "s5_1"; // Makeover Cut
        stylistName = "Vikram Sen";
        reasoning = "Since you have a **Bold & Creative vibe**, **Vikram Sen** at **BBlunt Indiranagar** is the perfect pairing for a dramatic makeover cut.";
      } else {
        salonId = 1; // Rossano Ferretti
        serviceId = "s1_1"; // Method precision cut
        stylistName = "Alessandro Rossi";
        reasoning = "For the ultimate **Classic Elegant precision cut**, we paired you with **Alessandro Rossi** at **Rossano Ferretti Hair Spa**. The Italian Method cut is customized to your hair's unique structure.";
      }
    }
  } else if (focus === "skin") {
    if (concern === "skin_glow") {
      salonId = 3; // Warren Tricomi
      serviceId = "s3_2"; // 24k Gold Collagen Facial
      stylistName = "Anjali Rao";
      reasoning = "To achieve an **Instant Radiant Glow**, we recommend the **24k Gold Facial** at **Warren Tricomi (JW Marriott)** by skin specialist **Anjali Rao**.";
    } else if (concern === "skin_age") {
      salonId = 1; // Rossano Ferretti
      serviceId = "s1_3"; // Gold Illuminating Facial
      stylistName = "Alessandro Rossi";
      reasoning = "To stimulate **Collagen and Cell Renewal**, the premium **Gold Illuminating Facial** at **Rossano Ferretti Ritz-Carlton** is highly recommended.";
    } else {
      salonId = 4; // JCB Lavelle Road
      serviceId = "s4_2"; // Sothys Organic facial
      stylistName = "Priya Nair";
      reasoning = "For **Organic and Botanical Skin therapies**, the Parisian **Sothys Facial** at **Jean-Claude Biguine** will leave your skin pristine.";
    }
  } else if (focus === "spa") {
    if (concern === "spa_deep") {
      salonId = 3; // Warren Tricomi
      serviceId = "s3_3"; // Balinese Massage
      stylistName = "Anjali Rao";
      reasoning = "For **Deep Muscle relief**, the traditional **Deep Tissue Balinese Massage** at **Warren Tricomi JW Marriott** is the ideal treatment.";
    } else {
      salonId = 6; // Leela Palace Spa
      serviceId = "s6_2"; // Abhyanga massage
      stylistName = "Dr. Manoj Kumar";
      reasoning = "For **Traditional Ayurvedic healing**, **The Spa at Leela Palace** is the pinnacle of luxury. We've matched you with **Dr. Manoj Kumar** for the Abhyanga Ritual.";
    }
  } else { // Nails
    if (concern === "nails_art") {
      salonId = 2; // Play Salon
      serviceId = "s2_3"; // Chrome gel mani-pedi
      stylistName = "Sarah Fernandes";
      reasoning = "For premium **Gel Extensions and Chrome art**, the VIP lounge at **Play Salon UB City** is highly rated.";
    } else {
      salonId = 5; // BBlunt
      serviceId = "s5_3"; // Signature Chrome Pedicure
      stylistName = "Kavitha Raj";
      reasoning = "For a relaxing **Pedicure Spa massage**, the specialized blowout and nail lounge at **BBlunt Indiranagar** is an excellent choice.";
    }
  }
  
  // Output result text
  appendBotMessage(reasoning);
  
  // Output card template
  setTimeout(() => {
    appendRecommendedCard(salonId, serviceId, stylistName);
    
    // Offer helper CTA
    setTimeout(() => {
      appendBotMessage("Would you like me to match you with another treatment profile, or shall we finalize your reservation details above?", [
        { text: "Create New Style Profile", action: "restart_advisor" }
      ]);
    }, 1200);
  }, 600);
}

function appendRecommendedCard(salonId, serviceId, stylistName) {
  const history = document.getElementById("chatHistory");
  const salon = SALONS_DATA.find(s => s.id === salonId);
  const service = salon.services.find(s => s.id === serviceId);
  
  const card = document.createElement("div");
  card.className = "chat-card-recommendation";
  card.innerHTML = `
    <img src="${salon.image}" alt="${salon.name}" class="chat-card-img">
    <div class="chat-card-content">
      <div style="font-size:0.75rem; color:var(--accent-gold); text-transform:uppercase; font-weight:600; margin-bottom:4px;">Aura Verified Match</div>
      <h4 class="chat-card-title">${salon.name}</h4>
      <div class="chat-card-service">${service.name}</div>
      <div style="font-size:0.8rem; color:var(--text-secondary); margin-bottom:12px;">
        <i class="fa-solid fa-user-tie" style="color:var(--accent-gold);"></i> Stylist: ${stylistName}<br>
        <i class="fa-solid fa-indian-rupee-sign" style="color:var(--accent-gold);"></i> Price: ₹${service.price.toLocaleString()}
      </div>
      <button class="btn btn-primary btn-sm" style="width:100%;" onclick="openBookingFromAI(${salonId}, '${serviceId}', '${stylistName}')">
        Book Appointment via Concierge
      </button>
    </div>
  `;
  
  history.appendChild(card);
  history.scrollTop = history.scrollHeight;
}

// Redirects AI selection into the Booking modal setup
window.openBookingFromAI = function(salonId, serviceId, stylistName) {
  openBookingModal(salonId, serviceId, stylistName);
};

// ==========================================
// 7. BOOKING SYSTEM & WIZARD MODULE
// ==========================================
function initBookingWizard() {
  const modal = document.getElementById("bookingModal");
  const closeBtn = document.getElementById("closeBookingBtn");
  const nextBtn = document.getElementById("bookingNextBtn");
  const prevBtn = document.getElementById("bookingPrevBtn");
  const salonSelect = document.getElementById("modalSalonSelect");
  
  closeBtn.addEventListener("click", () => {
    closeBookingModal();
  });
  
  // Modal click overlay dismissal
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      closeBookingModal();
    }
  });
  
  // Dropdown salon switcher in Step 1
  salonSelect.addEventListener("change", () => {
    const sId = parseInt(salonSelect.value);
    AppState.bookingWizard.salonId = sId;
    AppState.bookingWizard.serviceId = null; // reset service
    renderModalServices(sId);
  });
  
  // Step Navigation flow controls
  nextBtn.addEventListener("click", () => {
    handleWizardNext();
  });
  
  prevBtn.addEventListener("click", () => {
    handleWizardBack();
  });
  
  // Setup Calendar days
  generateCalendarDays();
}

function openBookingModal(salonId = null, serviceId = null, stylistName = null) {
  const modal = document.getElementById("bookingModal");
  const salonSelect = document.getElementById("modalSalonSelect");
  
  // Populate salon options
  salonSelect.innerHTML = SALONS_DATA.map(s => `<option value="${s.id}">${s.name} (${s.location})</option>`).join('');
  
  // Reset Wizard State
  AppState.bookingWizard = {
    salonId: salonId || SALONS_DATA[0].id,
    serviceId: serviceId,
    stylistName: stylistName,
    date: null,
    timeSlot: null,
    currentStep: 1
  };
  
  // Update dropdown value
  salonSelect.value = AppState.bookingWizard.salonId;
  
  // Set step panels visibility
  setBookingWizardStep(1);
  
  // Render step 1 services
  renderModalServices(AppState.bookingWizard.salonId);
  
  // Open overlay
  modal.classList.add("active");
  document.body.style.overflow = "hidden"; // disable background scrolling
}

function closeBookingModal() {
  const modal = document.getElementById("bookingModal");
  modal.classList.remove("active");
  document.body.style.overflow = "";
}

function setBookingWizardStep(step) {
  AppState.bookingWizard.currentStep = step;
  
  // Show / Hide Step panels
  document.querySelectorAll(".booking-step-panel").forEach((panel, idx) => {
    panel.classList.remove("active");
    if (idx + 1 === step) {
      panel.classList.add("active");
    }
  });
  
  // Update indicators
  document.querySelectorAll(".step-indicator").forEach((ind, idx) => {
    const sNum = idx + 1;
    ind.classList.remove("active", "completed");
    
    if (sNum === step) {
      ind.classList.add("active");
    } else if (sNum < step) {
      ind.classList.add("completed");
    }
  });
  
  // Controls navigation buttons layout
  const prevBtn = document.getElementById("bookingPrevBtn");
  const nextBtn = document.getElementById("bookingNextBtn");
  
  if (step === 1) {
    prevBtn.style.visibility = "hidden";
  } else {
    prevBtn.style.visibility = "visible";
  }
  
  if (step === 4) {
    nextBtn.innerHTML = `Confirm Appointment <i class="fa-solid fa-circle-check"></i>`;
  } else {
    nextBtn.innerHTML = `Continue <i class="fa-solid fa-arrow-right"></i>`;
  }
}

function renderModalServices(salonId) {
  const listContainer = document.getElementById("modalServiceList");
  const salon = SALONS_DATA.find(s => s.id === salonId);
  
  listContainer.innerHTML = salon.services.map(s => {
    const isSelected = AppState.bookingWizard.serviceId === s.id ? 'selected' : '';
    
    return `
      <div class="select-card-row ${isSelected}" data-service-id="${s.id}">
        <div class="select-card-info">
          <i class="fa-solid fa-scissors" style="color:var(--accent-gold); font-size:1.2rem;"></i>
          <div>
            <div class="select-card-title-sub">${s.name}</div>
            <div class="select-card-desc-sub">${s.desc} • ${s.duration}</div>
          </div>
        </div>
        <div class="select-card-price">₹${s.price.toLocaleString()}</div>
      </div>
    `;
  }).join('');
  
  // Click event triggers service selection
  listContainer.querySelectorAll(".select-card-row").forEach(row => {
    row.addEventListener("click", () => {
      listContainer.querySelectorAll(".select-card-row").forEach(r => r.classList.remove("selected"));
      row.classList.add("selected");
      
      AppState.bookingWizard.serviceId = row.getAttribute("data-service-id");
    });
  });
}

function renderModalStylists() {
  const listContainer = document.getElementById("modalStylistList");
  const salon = SALONS_DATA.find(s => s.id === AppState.bookingWizard.salonId);
  
  listContainer.innerHTML = salon.stylists.map(st => {
    const isSelected = AppState.bookingWizard.stylistName === st.name ? 'selected' : '';
    
    return `
      <div class="select-card-row ${isSelected}" data-stylist-name="${st.name}">
        <div class="select-card-info">
          <img src="${st.image}" alt="${st.name}" class="select-card-circle">
          <div>
            <div class="select-card-title-sub">${st.name}</div>
            <div class="select-card-desc-sub">${st.role} • Specialty: ${st.specialty}</div>
          </div>
        </div>
        <div class="stylist-rating">
          <i class="fa-solid fa-star"></i> <span>${st.rating}</span>
        </div>
      </div>
    `;
  }).join('');
  
  listContainer.querySelectorAll(".select-card-row").forEach(row => {
    row.addEventListener("click", () => {
      listContainer.querySelectorAll(".select-card-row").forEach(r => r.classList.remove("selected"));
      row.classList.add("selected");
      
      AppState.bookingWizard.stylistName = row.getAttribute("data-stylist-name");
    });
  });
}

// Generate Calendar Days for Current Month
function generateCalendarDays() {
  const grid = document.getElementById("calendarDays");
  const monthLabel = document.getElementById("calendarMonthYear");
  
  // Hardcoded to June 2026 for prototype styling
  monthLabel.innerText = "June 2026";
  
  grid.innerHTML = "";
  
  // Day titles
  const labels = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
  labels.forEach(l => {
    grid.innerHTML += `<div class="cal-day-label">${l}</div>`;
  });
  
  // June 2026 starts on Monday (1 day empty offset for Sunday)
  grid.innerHTML += `<div class="cal-day-cell muted">31</div>`;
  
  // Render days 1 to 30
  for (let d = 1; d <= 30; d++) {
    // Disable past dates relative to current local date if necessary. (Assume current is June 16, 2026)
    const isPast = d < 16;
    const cellClass = isPast ? "cal-day-cell muted" : "cal-day-cell";
    
    grid.innerHTML += `<div class="${cellClass}" data-day="${d}">${d}</div>`;
  }
  
  // Select date click handler
  grid.querySelectorAll(".cal-day-cell:not(.muted)").forEach(cell => {
    cell.addEventListener("click", () => {
      grid.querySelectorAll(".cal-day-cell").forEach(c => c.classList.remove("selected"));
      cell.classList.add("selected");
      
      const day = cell.getAttribute("data-day");
      AppState.bookingWizard.date = `June ${day}, 2026`;
      
      // Update slots availability mockup based on selected day
      renderTimeSlots();
    });
  });
}

function renderTimeSlots() {
  const container = document.getElementById("timeSlotsGrid");
  
  container.innerHTML = TIME_SLOTS.map(slot => {
    const isSelected = AppState.bookingWizard.timeSlot === slot ? 'selected' : '';
    return `<div class="time-slot-chip ${isSelected}" data-slot="${slot}">${slot.split(' ')[0]} ${slot.split(' ')[1]}</div>`;
  }).join('');
  
  container.querySelectorAll(".time-slot-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      container.querySelectorAll(".time-slot-chip").forEach(c => c.classList.remove("selected"));
      chip.classList.add("selected");
      
      AppState.bookingWizard.timeSlot = chip.getAttribute("data-slot");
    });
  });
}

function renderReviewScreen() {
  const salon = SALONS_DATA.find(s => s.id === AppState.bookingWizard.salonId);
  const service = salon.services.find(s => s.id === AppState.bookingWizard.serviceId);
  
  document.getElementById("reviewSalonName").innerText = salon.name;
  document.getElementById("reviewServiceName").innerText = service.name;
  document.getElementById("reviewStylistName").innerText = AppState.bookingWizard.stylistName || "Any Available Master Stylist";
  document.getElementById("reviewDate").innerText = AppState.bookingWizard.date;
  document.getElementById("reviewTime").innerText = AppState.bookingWizard.timeSlot;
  document.getElementById("reviewCost").innerText = `₹${service.price.toLocaleString()}`;
}

// Validation and page progression logic in Booking modal
function handleWizardNext() {
  const step = AppState.bookingWizard.currentStep;
  
  if (step === 1) {
    if (!AppState.bookingWizard.serviceId) {
      alert("Please select a luxury service to proceed.");
      return;
    }
    // Pre-fill stylist if selected via AI or set default
    renderModalStylists();
    setBookingWizardStep(2);
  } 
  else if (step === 2) {
    // Stylist optional, if none selected, select first
    if (!AppState.bookingWizard.stylistName) {
      const salon = SALONS_DATA.find(s => s.id === AppState.bookingWizard.salonId);
      AppState.bookingWizard.stylistName = salon.stylists[0].name;
    }
    setBookingWizardStep(3);
  } 
  else if (step === 3) {
    if (!AppState.bookingWizard.date) {
      alert("Please select an appointment date from the calendar.");
      return;
    }
    if (!AppState.bookingWizard.timeSlot) {
      alert("Please select an available appointment time slot.");
      return;
    }
    renderReviewScreen();
    setBookingWizardStep(4);
  } 
  else if (step === 4) {
    // Checkout details Validation
    const name = document.getElementById("bookingNameInput").value.trim();
    const phone = document.getElementById("bookingPhoneInput").value.trim();
    
    if (name === "" || phone === "") {
      alert("Please enter your name and phone number for VIP notifications.");
      return;
    }
    
    // Process final reservation
    executeFinalBooking(name, phone);
  }
}

function handleWizardBack() {
  const step = AppState.bookingWizard.currentStep;
  if (step > 1) {
    setBookingWizardStep(step - 1);
  }
}

function executeFinalBooking(name, phone) {
  const sId = AppState.bookingWizard.salonId;
  const srvId = AppState.bookingWizard.serviceId;
  
  const salon = SALONS_DATA.find(s => s.id === sId);
  const service = salon.services.find(s => s.id === srvId);
  const stylist = salon.stylists.find(st => st.name === AppState.bookingWizard.stylistName) || salon.stylists[0];
  
  const bookingObj = {
    id: "AURA-" + Math.floor(100000 + Math.random() * 900000),
    salonName: salon.name,
    salonLocation: salon.location,
    salonImage: salon.image,
    serviceName: service.name,
    servicePrice: service.price,
    stylistName: stylist.name,
    stylistImage: stylist.image,
    date: AppState.bookingWizard.date,
    timeSlot: AppState.bookingWizard.timeSlot,
    customerName: name,
    customerPhone: phone
  };
  
  // Save to App State and Storage
  AppState.bookings.unshift(bookingObj);
  saveBookingsToStorage();
  
  // Close Modal
  closeBookingModal();
  
  // Trigger Custom UI success message
  showBookingSuccessMessage(bookingObj.id);
}

function showBookingSuccessMessage(bookingId) {
  // Direct redirect to bookings tab with custom highlighted message
  const bookingsTab = document.querySelector("[data-target='bookings-section']");
  bookingsTab.click();
  
  // Create beautiful notification element
  const toast = document.createElement("div");
  toast.style.position = "fixed";
  toast.style.top = "90px";
  toast.style.right = "24px";
  toast.style.background = "var(--bg-secondary)";
  toast.style.border = "1.5px solid var(--success)";
  toast.style.padding = "16px 24px";
  toast.style.borderRadius = "8px";
  toast.style.zIndex = "3000";
  toast.style.boxShadow = "var(--shadow-lg)";
  toast.style.animation = "messageSlide 0.5s ease forwards";
  toast.innerHTML = `
    <div style="display:flex; align-items:center; gap:12px;">
      <i class="fa-solid fa-circle-check" style="color:var(--success); font-size:1.5rem;"></i>
      <div>
        <div style="font-weight:700; color:#fff;">Reservation Confirmed!</div>
        <div style="font-size:0.8rem; color:var(--text-secondary);">Ticket ID: ${bookingId}</div>
      </div>
    </div>
  `;
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = "fadeOut 0.5s ease forwards";
    setTimeout(() => toast.remove(), 500);
  }, 4000);
}

// Draw list of active reservations
function renderBookings() {
  const container = document.getElementById("bookingsContainer");
  
  if (AppState.bookings.length === 0) {
    container.innerHTML = `
      <div class="empty-bookings">
        <div class="empty-bookings-icon"><i class="fa-solid fa-calendar-xmark"></i></div>
        <h3>No Active Appointments</h3>
        <p style="margin-bottom: 20px;">Indulge in a premium salon service. Schedule your first appointment in seconds.</p>
        <button class="btn btn-primary" onclick="openBookingModal()">
          Book Appointment Now
        </button>
      </div>
    `;
    return;
  }
  
  container.innerHTML = AppState.bookings.map(b => {
    // Generate simulated booking QR code using a free placeholder/canvas API or static image
    const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=${b.id}`;
    
    return `
      <div class="booking-ticket">
        <div class="ticket-header">
          <div>
            <div class="ticket-brand">AURA ELITE RESERVATION</div>
            <div class="ticket-id">PASS ID: ${b.id}</div>
          </div>
          <div style="background:rgba(52, 211, 153, 0.1); border: 1px solid var(--success); color:var(--success); font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:4px; text-transform:uppercase;">
            Confirmed
          </div>
        </div>
        
        <div class="ticket-body-grid">
          <div>
            <div class="ticket-info-item">
              <span class="ticket-info-label">Salon Location</span>
              <div class="ticket-info-value">${b.salonName}</div>
              <div style="font-size:0.8rem; color:var(--text-secondary);">${b.salonLocation}</div>
            </div>
            
            <div class="ticket-info-item">
              <span class="ticket-info-label">Reserved Ritual</span>
              <div class="ticket-info-value" style="color:var(--accent-gold-bright);">${b.serviceName}</div>
            </div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px;">
              <div class="ticket-info-item">
                <span class="ticket-info-label">Date</span>
                <div class="ticket-info-value">${b.date}</div>
              </div>
              <div class="ticket-info-item">
                <span class="ticket-info-label">Time Window</span>
                <div class="ticket-info-value">${b.timeSlot.split(' ')[0]} ${b.timeSlot.split(' ')[1]}</div>
              </div>
            </div>
            
            <div style="display:flex; align-items:center; gap:10px; margin-top:10px; padding-top:10px; border-top:1px solid var(--border-color);">
              <img src="${b.stylistImage}" alt="${b.stylistName}" style="width:28px; height:28px; border-radius:50%; object-fit:cover; border:1px solid var(--accent-gold-dark);">
              <div style="font-size:0.85rem;">Stylist pairing: <strong>${b.stylistName}</strong></div>
            </div>
          </div>
          
          <div class="ticket-qr-zone">
            <div class="ticket-qr-box">
              <img src="${qrUrl}" alt="Check-in QR Code">
            </div>
            <div class="ticket-qr-caption">Scan at Entrance</div>
            
            <button class="btn btn-secondary btn-sm" onclick="cancelBooking('${b.id}')" style="margin-top:16px; padding:4px 10px; font-size:0.75rem; border-color:rgba(248,113,113,0.3); color:var(--danger); width:100%;">
              Cancel Reservation
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

window.cancelBooking = function(id) {
  if (confirm("Are you sure you want to cancel this reservation? All styling profiles and priority time slots will be released.")) {
    AppState.bookings = AppState.bookings.filter(b => b.id !== id);
    saveBookingsToStorage();
    renderBookings();
  }
};

// Storage management
function saveBookingsToStorage() {
  localStorage.setItem("aura_bookings_data", JSON.stringify(AppState.bookings));
}

function loadBookingsFromStorage() {
  const raw = localStorage.getItem("aura_bookings_data");
  if (raw) {
    AppState.bookings = JSON.parse(raw);
  }
}

// ==========================================
// 8. INTERACTIVE MAP CONTROLS
// ==========================================
function initMapModal() {
  const mapOverlay = document.getElementById("mapModal");
  const openMapBtn = document.getElementById("viewMapBtn");
  const closeMapBtn = document.getElementById("closeMapBtn");
  const closeMapFooterBtn = document.getElementById("closeMapFooterBtn");
  
  const openMap = () => {
    mapOverlay.classList.add("active");
    document.body.style.overflow = "hidden";
  };
  
  const closeMap = () => {
    mapOverlay.classList.remove("active");
    document.body.style.overflow = "";
  };
  
  openMapBtn.addEventListener("click", openMap);
  closeMapBtn.addEventListener("click", closeMap);
  closeMapFooterBtn.addEventListener("click", closeMap);
  mapOverlay.addEventListener("click", (e) => {
    if (e.target === mapOverlay) closeMap();
  });
  
  // Setup Map pin click handlers
  const markers = document.querySelectorAll(".map-marker");
  const overlayCard = document.getElementById("mapOverlayCard");
  const cardTitle = document.getElementById("mapCardTitle");
  const cardDesc = document.getElementById("mapCardDesc");
  const cardBookBtn = document.getElementById("mapCardBookBtn");
  
  markers.forEach(marker => {
    marker.addEventListener("click", () => {
      markers.forEach(m => m.classList.remove("active"));
      marker.classList.add("active");
      
      const sId = parseInt(marker.getAttribute("data-id"));
      const salon = SALONS_DATA.find(s => s.id === sId);
      
      // Update Bottom info Card
      cardTitle.innerText = salon.name;
      cardDesc.innerText = `${salon.location} | Rating: ★ ${salon.rating}`;
      overlayCard.style.display = "flex";
      
      // Attach booking to card button
      cardBookBtn.onclick = () => {
        closeMap();
        openBookingModal(salon.id);
      };
    });
  });
}
