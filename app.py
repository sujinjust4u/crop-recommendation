from flask import Flask,request,render_template, jsonify
import numpy as np
import pandas
import sklearn
import pickle
import os
import google.generativeai as genai

# Configure Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    try:
        print("DEBUG: Checking available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"DEBUG: Available model: {m.name}")
    except Exception as e:
        print(f"DEBUG: Error listing models: {e}")

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1024,
    }
    model_genai = genai.GenerativeModel(
        model_name="gemini-flash-latest",
        generation_config=generation_config,
    )
else:
    model_genai = None
# importing model
model = pickle.load(open('model.pkl','rb'))
sc = pickle.load(open('standscaler.pkl','rb'))
ms = pickle.load(open('minmaxscaler.pkl','rb'))

# creating flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/predict",methods=['POST'])
def predict():
    try:
        N = float(request.form['Nitrogen'])
        P = float(request.form['Phosporus'])
        K = float(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['Ph'])
        rainfall = float(request.form['Rainfall'])

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        print(f"DEBUG: Inputs for prediction: {feature_list}")
        single_pred = np.array(feature_list).reshape(1, -1)

        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)
        prediction = model.predict(final_features)

        crop = prediction[0]
        result = "{} is the best crop to be cultivated right there".format(crop.capitalize())
        advice = get_agricultural_advice(crop, N, P, K, temp, humidity, ph, rainfall)
        return render_template('index.html',result = result, advice = advice)
    except Exception as e:
        return render_template('index.html', result=f"Error: {str(e)}")

def get_agricultural_advice(crop, N, P, K, temp, humidity, ph, rainfall):
    if not model_genai:
        return "Gemini API key not configured (GEMINI_API_KEY env var missing). Mock Advice: Ensure adequate water and standard NPK fertilizers for your crop."
    
    prompt = f"""
    You are an expert agricultural advisor. A machine learning model has recommended growing '{crop}' 
    based on the following soil and weather conditions:
    - Nitrogen: {N}
    - Phosphorous: {P}
    - Potassium: {K}
    - Temperature: {temp}°C
    - Humidity: {humidity}%
    - pH: {ph}
    - Rainfall: {rainfall} mm

    Please provide a short, actionable advice paragraph for the farmer. Include:
    1. A brief confirmation of why this crop is suitable.
    2. One or two best practices for cultivating this crop under these conditions.
    3. Any potential risks or diseases to watch out for.
    Keep it concise (around 3-4 sentences).
    """
    try:
        response = model_genai.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "🌱 AI Advice Tip: Based on your soil data, ensure consistent watering and consider a balanced fertilizer approach. (Note: AI rate limit reached, showing general tip)."
        return f"Error fetching advice: {str(e)}"

@app.route("/api/predict", methods=['POST'])
def predict_api():
    try:
        data = request.get_json()
        N = float(data['Nitrogen'])
        P = float(data['Phosporus'])
        K = float(data['Potassium'])
        temp = float(data['Temperature'])
        humidity = float(data['Humidity'])
        ph = float(data['Ph'])
        rainfall = float(data['Rainfall'])

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)
        prediction = model.predict(final_features)

        crop = prediction[0]
        advice = get_agricultural_advice(crop, N, P, K, temp, humidity, ph, rainfall)
        return jsonify({"success": True, "crop": crop, "advice": advice})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})




# python main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)