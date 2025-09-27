# app.py
from flask import Flask, render_template, send_from_directory, request, jsonify
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Gemini client with your API key
# You can set the API key in two ways:
# 1. Set GEMINI_API_KEY in your .env file
# 2. Or replace os.getenv('GEMINI_API_KEY') with your actual API key string

# Option 1: Using environment variable (recommended)
gemini_client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Option 2: Hardcode your API key (less secure)
# gemini_client = genai.Client(api_key="your_actual_gemini_api_key_here")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/telemedicine')
def telemedicine():
    return render_template('telemedicine.html')

@app.route('/emergency')
def emergency():
    return render_template('emergency.html')

@app.route('/reminders')
def reminders():
    return render_template('reminders.html')

@app.route('/symptom-checker')
def symptom_checker():
    return render_template('symptom_checker.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/check-symptoms', methods=['POST'])
def check_symptoms():
    try:
        data = request.json
        symptoms = data.get('symptoms', '')
        
        if not symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Use Gemini AI to analyze symptoms with the new client format
        prompt = f"""Act as a medical assistant. The user reports these symptoms: {symptoms}. 

Please provide:
1. A brief assessment of 2-3 possible conditions (list most likely first)
2. When to seek immediate medical help (red flags)
3. Basic self-care recommendations
4. Suggested over-the-counter medications that might help

Keep the response under 250 words. Be compassionate and clear."""

        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",  # Using the flash model for speed
            contents=prompt
        )
        
        return jsonify({'diagnosis': response.text})
    
    except Exception as e:
        print(f"Error in symptom check: {str(e)}")
        return jsonify({'error': 'Failed to analyze symptoms. Please try again.'}), 500

@app.route('/health-tips', methods=['POST'])
def health_tips():
    try:
        data = request.json
        topic = data.get('topic', 'general health')
        
        # Get health tips using Gemini
        prompt = f"""Provide 3-5 practical health tips about {topic} for people in Uganda. 
        Include information relevant to tropical climates and local availability of resources.
        Keep each tip concise and actionable."""
        
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        return jsonify({'tips': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/medication-info', methods=['POST'])
def medication_info():
    try:
        data = request.json
        medication = data.get('medication', '')
        
        if not medication:
            return jsonify({'error': 'No medication specified'}), 400
        
        # Get information about medication
        prompt = f"""Provide information about {medication} including:
        1. Common uses and indications
        2. Typical dosage for adults
        3. Important side effects to watch for
        4. Drug interactions to be aware of
        5. Special precautions
        
        Keep the information clear and practical for patients."""
        
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        return jsonify({'information': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check if Gemini API key is set
    if not os.getenv('GEMINI_API_KEY') and "your_actual_gemini_api_key_here" in "your_actual_gemini_api_key_here":
        print("⚠️  WARNING: Gemini API key not set!")
        print("Please either:")
        print("1. Create a .env file with GEMINI_API_KEY=your_key_here")
        print("2. Or replace the api_key parameter in the genai.Client() call")
        print("The symptom checker will not work without a valid API key.")
    
    app.run(debug=True, port=5000, host='0.0.0.0')