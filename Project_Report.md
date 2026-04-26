# Project Report: AI-Enhanced Crop Recommendation System

## 1. Project Overview
This project is an advanced **Crop Recommendation System** designed to support **Sustainable Development Goal 2: Zero Hunger**. It leverages Machine Learning to recommend the best crops for cultivation based on soil and weather parameters, and integrates Agentic AI to provide personalized agricultural advice.

- **Original Base Repository:** [611noorsaeed/Crop-Recommendation-System-Using-Machine-Learning](https://github.com/611noorsaeed/Crop-Recommendation-System-Using-Machine-Learning)
- **Primary SDG:** SDG 2 (Zero Hunger) - By optimizing crop yields through data-driven decisions.

## 2. Core Implementations

### 2.1 Machine Learning Model
- **Algorithm:** RandomForestClassifier.
- **Features:** Nitrogen (N), Phosphorus (P), Potassium (K), Temperature, Humidity, pH, and Rainfall.
- **Improvements:**
    - The original model had classification mapping issues. We **retrained the model** directly from the `Crop_recommendation.csv` dataset.
    - Switched from integer-based labels to **direct string-based labels** (e.g., "rice", "maize") for 100% accuracy in output mapping.
    - Implemented double-scaling (MinMaxScaler followed by StandardScaler) to ensure feature consistency.

### 2.2 LLM / GenAI Integration (Agentic AI)
- **Inference Engine:** Google Gemini (using `google-generativeai` SDK).
- **Model used:** `gemini-2.0-flash` (with fallback to `gemini-flash-latest`).
- **Functionality:** When a crop is recommended, the system sends the soil/weather data to the LLM to generate **personalized agricultural advice**, including fertilizer tips and irrigation strategies.
- **Resilience:** Implemented error handling for rate limits (429 errors) and model availability (404 errors), including a fallback "Tip of the Day" mechanism.

### 2.3 Model Serving & API
- **Web Framework:** Flask (Python).
- **REST API:** Added a dedicated endpoint at `/api/predict` that accepts JSON data and returns structured crop recommendations and AI advice.
- **Port Mapping:** Configured to run on host port **8080** to avoid standard macOS port conflicts (AirPlay on port 5000).

### 2.4 Containerization
- **Technology:** Docker.
- **Container Base:** `python:3.9-slim`.
- **Automation:** Created a robust `build_and_run.sh` script that:
    - Builds the Docker image.
    - Automatically stops and removes existing containers to free up ports.
    - Injects the Gemini API key via environment variables safely.
    - Maps internal port 5000 to external port 8080.

## 3. Modifications Summary
| Component | Modification | Rationale |
| :--- | :--- | :--- |
| **Directory Structure** | Created `templates/` and `static/` folders. | Adhere to Flask conventions and fix `TemplateNotFound` errors. |
| **Data Types** | Forced float conversion for all inputs. | Fixed a bug where string inputs caused the model to return "Apple" for every request. |
| **Model Persistence** | Re-trained and re-pickled the model & scalers. | Resolved version mismatch (1.5.1 vs 1.3.2) and fixed label mapping. |
| **UI/UX** | Added a dark-themed, modern result card. | Improved the "premium" feel of the application. |
| **Automation** | Added `push_to_dockerhub.sh` and `push_to_github.sh`. | Simplified the deployment and version control workflow. |

## 4. How to Run
1. Clone the repository.
2. Add your `GEMINI_API_KEY` to the `build_and_run.sh` script.
3. Run: `./build_and_run.sh`
4. Access the app at: `http://localhost:8080`

## 5. Conclusion
By combining traditional ML classification with cutting-edge Generative AI, this application provides more than just a prediction—it provides a roadmap for farmers to achieve better yields, directly contributing to global food security.
