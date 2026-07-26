# PlacementPro 🚀

AI-powered placement preparation platform with comprehensive features for job seekers.

## ✨ Features

- **AI-Powered Interview Prep**: Generate role-specific questions with company insights
- **Resume Analysis**: ATS-optimized resume feedback and suggestions
- **Coding Challenges**: Topic-based coding problems with hints and solutions
- **Aptitude Tests**: Category-based aptitude questions with explanations
- **System Design**: Practice system design problems
- **Cover Letter Generation**: AI-generated cover letters tailored to job descriptions
- **Gamification**: XP, levels, and leaderboards to track progress
- **Placement Prediction**: ML-based placement probability predictions
- **Multi-Tier Plans**: Free, Premium, Pro, and Enterprise plans

## 🏗️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: MongoDB with Motor async driver
- **Cache**: Redis (optional, falls back to in-memory)
- **AI**: OpenRouter API with multiple model fallbacks
- **Auth**: JWT with HTTP-only cookies
- **Rate Limiting**: In-memory with Redis support
- **Payment**: PayPal integration

### Frontend
- **Framework**: React with Vite
- **Styling**: Modern CSS with responsive design
- **State Management**: React Context API

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB (local or Atlas)
- Redis (optional)
- Docker & Docker Compose (optional)

## 🚀 Quick Start

### Option 1: Docker (Recommended)

