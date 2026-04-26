# AI-Enhanced Crop Recommendation System 🌱

[![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)](https://www.docker.com/)
[![SDG](https://img.shields.io/badge/SDG-2_%7C_Zero_Hunger-green)](https://sdgs.un.org/goals/goal2)
[![AI](https://img.shields.io/badge/AI-Gemini_2.0_Flash-orange)](https://ai.google.dev/)

An intelligent agricultural tool that recommends the best crops for cultivation and provides personalized agricultural advice using Generative AI.

## 🚀 Features
- **Precision ML:** Predicts the most suitable crop based on NPK, temperature, humidity, pH, and rainfall.
- **✨ Agentic AI Advice:** Integrated with **Google Gemini** to provide real-time, personalized farming advice for each recommended crop.
- **REST API:** Ready-to-use JSON API endpoint for integration with mobile apps or IoT sensors.
- **Containerized:** Fully Dockerized for seamless deployment anywhere.

## 🌍 SDG Alignment
This project directly contributes to **SDG 2: Zero Hunger**. By helping farmers make data-driven decisions about which crops to plant and how to manage them, we can increase global food security and promote sustainable agriculture.

## 🛠️ Technology Stack
- **Backend:** Flask (Python)
- **Machine Learning:** Scikit-learn (Random Forest)
- **AI Engine:** Google Gemini API
- **Deployment:** Docker & DockerHub

## 📦 Getting Started

### Prerequisites
- Docker installed on your machine.
- A Google Gemini API Key.

### Running with Docker (Recommended)
1. Clone this repository:
   ```bash
   git clone https://github.com/sujinjust4u/crop-recommendation.git
   cd crop-recommendation
   ```
2. Open `build_and_run.sh` and add your `GEMINI_API_KEY`.
3. Run the automation script:
   ```bash
   ./build_and_run.sh
   ```
4. Access the app at **http://localhost:8080**

### Manual Installation
If you prefer to run it without Docker:
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your_key_here"
python app.py
```

## 🔌 API Documentation
**Endpoint:** `POST /api/predict`  
**Payload:**
```json
{
  "Nitrogen": 90,
  "Phosporus": 42,
  "Potassium": 43,
  "Temperature": 20.8,
  "Humidity": 82.0,
  "Ph": 6.5,
  "Rainfall": 202.9
}
```

## 📜 Credits
This project was based on the original repository: [611noorsaeed/Crop-Recommendation-System-Using-Machine-Learning](https://github.com/611noorsaeed/Crop-Recommendation-System-Using-Machine-Learning).

Modified and Enhanced by **sujinsp** as part of an AI-SDG initiative.
