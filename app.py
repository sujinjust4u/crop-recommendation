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
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1024,
    }
    model_genai = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
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
    N = request.form['Nitrogen']
    P = request.form['Phosporus']
    K = request.form['Potassium']
    temp = request.form['Temperature']
    humidity = request.form['Humidity']
    ph = request.form['Ph']
    rainfall = request.form['Rainfall']

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)

    scaled_features = ms.transform(single_pred)
    final_features = sc.transform(scaled_features)
    prediction = model.predict(final_features)

    crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                 14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        result = "{} is the best crop to be cultivated right there".format(crop)
        advice = get_agricultural_advice(crop, N, P, K, temp, humidity, ph, rainfall)
    else:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
        advice = ""
    return render_template('index.html',result = result, advice = advice)

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
        return f"Error fetching advice: {str(e)}"

@app.route("/api/predict", methods=['POST'])
def predict_api():
    try:
        data = request.get_json()
        N = data['Nitrogen']
        P = data['Phosporus']
        K = data['Potassium']
        temp = data['Temperature']
        humidity = data['Humidity']
        ph = data['Ph']
        rainfall = data['Rainfall']

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)
        prediction = model.predict(final_features)

        crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                     8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                     14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                     19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            advice = get_agricultural_advice(crop, N, P, K, temp, humidity, ph, rainfall)
            return jsonify({"success": True, "crop": crop, "advice": advice})
        else:
            return jsonify({"success": False, "error": "Could not determine crop"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})




# python main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)