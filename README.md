# AURA Elite ✨

## AI-Powered Luxury Beauty Concierge Platform

AURA Elite is an intelligent beauty-tech platform that helps users discover premium salons, receive personalized styling recommendations, analyze face shapes, and gain AI-powered insights from customer reviews.

Built with FastAPI, JavaScript, SQLite, and Google Gemini AI, AURA transforms salon discovery into a personalized luxury experience.

---

## 🚀 Features

### 💎 Premium Salon Discovery
- Browse 500+ Bangalore salons
- Advanced search and filtering
- Area-based salon discovery
- Price and rating filters
- Interactive salon exploration

### 📅 Smart Booking Experience
- Salon reservation management
- Upcoming bookings dashboard
- Booking history tracking
- Favorite salons collection

### ✨ AI Beauty Concierge
Get personalized salon recommendations based on:

- Budget
- Occasion
- Hair texture
- Preferred location

The AI concierge suggests salons and styling options tailored to user preferences.

### 📸 AI Face Shape Analyzer
Upload a selfie and receive:

- Face shape analysis
- Hairstyle recommendations
- Personalized beauty suggestions
- Styling guidance

### 🧠 AI Review Insights
Powered by Gemini AI:

- Customer sentiment analysis
- Review summarization
- Service quality insights
- Strength and weakness detection
- AI-generated salon recommendations

### ❤️ Personalized User Dashboard
- Saved salons
- Booking management
- Styling preferences
- AI-generated recommendations

---

## 🏗 System Architecture

```text
Frontend (HTML/CSS/JavaScript + Vite)
                 │
                 ▼
          FastAPI Backend
                 │
                 ▼
          SQLite Database
                 │
                 ▼
         Google Gemini AI
```

---

## 🛠 Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Vite

### Backend
- FastAPI
- Python

### Database
- SQLite
- SQLAlchemy

### AI Integration
- Google Gemini API

### Tools
- Git
- GitHub
- VS Code

---

## 📂 Project Structure

```text
AURA/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   │
│   ├── aura.db
│   ├── requirements.txt
│   └── seed.py
│
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/SrushtiH23/GlowAI.git

cd GlowAI
```

### Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend API:

```text
http://localhost:8000
```

API Documentation:

```text
http://localhost:8000/docs
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

## 🎯 Problem Statement

Finding the right salon often requires users to browse multiple platforms, compare reviews, evaluate service quality, and determine whether a salon matches their personal styling needs.

AURA Elite simplifies this process through AI-powered personalization, beauty consultation, review intelligence, and luxury salon discovery.

---

## 🌟 Key Highlights

✅ 500+ Bangalore Salon Listings

✅ AI Beauty Concierge

✅ Face Shape Analysis

✅ AI Review Intelligence

✅ Smart Booking Dashboard

✅ Personalized Recommendations

✅ FastAPI Backend

✅ Modern Luxury UI

---

## 📸 Screenshots

### Dashboard
Manage bookings, favorites, and personalized recommendations.

### Salon Discovery
Explore premium salons with advanced filtering and search.

### AI Concierge
Receive customized salon and styling recommendations.

### Face Shape Analyzer
Upload selfies and get hairstyle suggestions.

### AI Review Insights
Analyze customer reviews using Gemini AI.

---

## 🔮 Future Enhancements

- Real-time appointment booking
- Hairstyle visualization
- Virtual makeover simulation
- Skin analysis
- Loyalty rewards program
- Multi-city support
- Mobile application

---

## 👩‍💻 Author

**Srushti H**

Computer Science Engineering Student

GitHub: https://github.com/SrushtiH23

---

## 📄 License

This project is developed for educational, research, portfolio, and hackathon purposes.
