/**
 * Navbar.jsx — Responsive Glassmorphic Navigation
 * Desktop: Top sticky bar with user profile.
 * Mobile: Native-style bottom tab bar.
 */

import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const navItems = [
    { label: "Dashboard", path: "/", icon: "🏠" },
    { label: "Book", path: "/book", icon: "💇‍♂️" },
    { label: "AI Concierge", path: "/concierge", icon: "✨" },
    { label: "Face shape", path: "/face-analysis", icon: "📷" },
    { label: "AI Insights", path: "/reviews", icon: "💬" },
  ];

  const handleNavClick = (path) => {
    navigate(path);
  };

  const isActive = (path) => {
    if (path === "/") {
      return location.pathname === "/";
    }
    return location.pathname.startsWith(path);
  };

  if (isMobile) {
    // ── MOBILE BOTTOM NAVBAR ──────────────────────────────────────────
    return (
      <>
        {/* Mobile Header with Logo & Sign Out */}
        <div style={styles.mobileHeader}>
          <div style={styles.brand} onClick={() => navigate("/")}>
            <span style={styles.brandText}>AURA</span>
            <span style={styles.brandBadge}>Elite</span>
          </div>
          <button onClick={logout} style={styles.mobileLogoutBtn} aria-label="Sign Out">
            Sign Out
          </button>
        </div>

        {/* Mobile Bottom Tab Navigation */}
        <div style={styles.mobileNav}>
          {navItems.map((item) => {
            const active = isActive(item.path);
            return (
              <button
                key={item.label}
                onClick={() => handleNavClick(item.path)}
                style={{
                  ...styles.mobileBtn,
                  color: active ? "#c5a880" : "#71717a",
                }}
                aria-label={item.label}
              >
                <span style={styles.mobileIcon}>{item.icon}</span>
                <span style={{
                  ...styles.mobileLabel,
                  color: active ? "#c5a880" : "#71717a",
                  fontWeight: active ? "700" : "500",
                }}>{item.label.split(" ")[0]}</span>
              </button>
            );
          })}
        </div>
      </>
    );
  }

  // ── DESKTOP/TABLET TOP NAVBAR ──────────────────────────────────────
  return (
    <nav style={styles.desktopNav}>
      <div style={styles.navContainer}>
        {/* Brand */}
        <div style={styles.brand} onClick={() => navigate("/")}>
          <span style={styles.brandText}>AURA</span>
          <span style={styles.brandBadge}>Elite</span>
        </div>

        {/* Navigation Links */}
        <div style={styles.links}>
          {navItems.map((item) => {
            const active = isActive(item.path);
            return (
              <button
                key={item.label}
                onClick={() => handleNavClick(item.path)}
                style={{
                  ...styles.navLink,
                  color: active ? "#c5a880" : "#a1a1aa",
                  borderBottom: active ? "2px solid #c5a880" : "2px solid transparent",
                }}
              >
                {item.label}
              </button>
            );
          })}
        </div>

        {/* User profile / Logout */}
        <div style={styles.profileBox}>
          <div style={styles.avatar}>
            {user?.full_name ? user.full_name.slice(0, 2).toUpperCase() : "ME"}
          </div>
          <div style={styles.userInfo}>
            <span style={styles.userName}>{user?.full_name || "Member"}</span>
            <span style={styles.userRole}>Elite User</span>
          </div>
          <button onClick={logout} style={styles.logoutBtn} aria-label="Sign Out">
            Sign Out
          </button>
        </div>
      </div>
    </nav>
  );
}

const styles = {
  // Desktop Header
  desktopNav: {
    position: "sticky",
    top: 0,
    zIndex: 100,
    background: "rgba(18, 18, 21, 0.8)",
    backdropFilter: "blur(12px)",
    borderBottom: "1px solid #26262b",
    height: "72px",
    display: "flex",
    alignItems: "center",
    width: "100%",
  },
  navContainer: {
    maxWidth: "1200px",
    width: "100%",
    margin: "0 auto",
    padding: "0 24px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    boxSizing: "border-box",
  },
  brand: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    cursor: "pointer",
  },
  brandText: {
    fontFamily: "'Playfair Display', serif",
    fontSize: "1.3rem",
    fontWeight: 700,
    letterSpacing: "0.08em",
    background: "linear-gradient(135deg, #fff 30%, #c5a880 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },
  brandBadge: {
    fontSize: "0.65rem",
    fontWeight: 300,
    letterSpacing: "0.18em",
    textTransform: "uppercase",
    color: "#c5a880",
    border: "1px solid #423829",
    padding: "1px 6px",
    borderRadius: "3px",
  },
  links: {
    display: "flex",
    gap: "24px",
    height: "72px",
    alignItems: "center",
  },
  navLink: {
    background: "transparent",
    border: "none",
    fontSize: "0.9rem",
    fontWeight: 600,
    padding: "24px 4px 22px",
    cursor: "pointer",
    transition: "all 0.2s",
    fontFamily: "'Plus Jakarta Sans', sans-serif",
  },
  profileBox: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
  },
  avatar: {
    width: "36px",
    height: "36px",
    borderRadius: "50%",
    background: "linear-gradient(135deg, #8a704c, #c5a880)",
    color: "#0e0e0e",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "0.82rem",
    fontWeight: 700,
  },
  userInfo: {
    display: "flex",
    flexDirection: "column",
    textAlign: "left",
  },
  userName: {
    fontSize: "0.85rem",
    fontWeight: 700,
    color: "#fcfcfd",
  },
  userRole: {
    fontSize: "0.7rem",
    color: "#71717a",
  },
  logoutBtn: {
    background: "transparent",
    border: "1px solid #26262b",
    borderRadius: "6px",
    color: "#a1a1aa",
    fontSize: "0.78rem",
    fontWeight: 600,
    padding: "6px 12px",
    cursor: "pointer",
    fontFamily: "'Plus Jakarta Sans', sans-serif",
    marginLeft: "8px",
    transition: "all 0.2s",
  },

  // Mobile Bottom Tab Bar
  mobileNav: {
    position: "fixed",
    bottom: 0,
    left: 0,
    right: 0,
    height: "64px",
    background: "rgba(18, 18, 21, 0.92)",
    backdropFilter: "blur(16px)",
    borderTop: "1px solid #26262b",
    display: "flex",
    justifyContent: "space-around",
    alignItems: "center",
    zIndex: 1000,
    paddingBottom: "env(safe-area-inset-bottom, 0px)",
  },
  mobileBtn: {
    background: "transparent",
    border: "none",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: "4px",
    padding: "8px 0",
    flex: 1,
    cursor: "pointer",
  },
  mobileIcon: {
    fontSize: "1.35rem",
  },
  mobileLabel: {
    fontSize: "0.68rem",
    fontFamily: "'Plus Jakarta Sans', sans-serif",
    textTransform: "uppercase",
    letterSpacing: "0.03em",
  },
  mobileHeader: {
    position: "sticky",
    top: 0,
    zIndex: 100,
    background: "rgba(18, 18, 21, 0.85)",
    backdropFilter: "blur(12px)",
    borderBottom: "1px solid #26262b",
    height: "56px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 16px",
    width: "100%",
    boxSizing: "border-box",
  },
  mobileLogoutBtn: {
    background: "transparent",
    border: "1px solid #26262b",
    borderRadius: "6px",
    color: "#a1a1aa",
    fontSize: "0.75rem",
    fontWeight: 650,
    padding: "6px 12px",
    cursor: "pointer",
    fontFamily: "'Plus Jakarta Sans', sans-serif",
    transition: "all 0.2s",
  },
};
