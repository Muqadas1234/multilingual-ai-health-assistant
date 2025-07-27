from flask import Flask, render_template, request, jsonify, send_file
import os
import uuid
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
from langdetect import detect
from groq import Groq
from utils import generate_pdf_report, text_to_speech

# 🌍 Load environment variables
load_dotenv()

# 🚀 Flask app init
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')

# 🤖 Groq client setup
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🧠 In-memory storage
conversations = {}
saved_chats = {}

# 🌐 Language detection
def detect_language(text):
    try:
        # Check for native Urdu script
        if detect(text) == 'ur':
            return 'ur'
        
        # Check for Roman Urdu (Urdu written in English letters)
        roman_urdu_words = [
            'main', 'mein', 'mujhe', 'mujhay', 'mera', 'meri', 'mere', 'ham', 'hum',
            'aap', 'tum', 'wo', 'ye', 'yeh', 'kya', 'kahan', 'kab', 'kaise', 'kyun',
            'hai', 'hain', 'tha', 'thi', 'the', 'raha', 'rahi', 'rahe', 'kar', 'karne',
            'dard', 'bimar', 'bemar', 'takleef', 'problem', 'masla', 'ilaaj', 'dawai',
            'doctor', 'daktar', 'hospital', 'aspatal', 'symptoms', 'alamat', 'behtar',
            'acha', 'acha hai', 'theek', 'theek hai', 'nahi', 'nahin', 'haan', 'han',
            'bilkul', 'zaroor', 'shayad', 'lagta', 'lagti', 'lagte', 'samajh', 'pata'
        ]
        
        text_lower = text.lower()
        urdu_word_count = sum(1 for word in roman_urdu_words if word in text_lower)
        
        # If more than 2 Roman Urdu words found, treat as Urdu
        if urdu_word_count >= 2:
            return 'ur_roman'
        
        return 'en'
    except:
        return 'en'

# 🧠 Check for mental health-related terms
def contains_mental_health_terms(text):
    terms = [
        'stress', 'anxiety', 'depression', 'panic', 'hopeless', 'worthless',
        'sad', 'lonely', 'overwhelmed', 'tired', 'sleep', 'insomnia', 'mood',
        'suicide', 'kill myself', 'end it all', 'no reason to live',
        'mental health', 'psychological', 'emotional', 'feeling down'
    ]
    return any(term in text.lower() for term in terms)



# 🤖 Generate AI response using Groq
def get_ai_response(symptoms, language='en'):
    # Enhanced prompt to handle different types of health questions
    base_prompt = {
        'en': f"""You are a comprehensive medical AI assistant. Based on the user's question, provide appropriate medical guidance:

USER QUESTION: {symptoms}

RESPONSE GUIDELINES:
- For symptoms: Provide diagnosis, treatments, precautions, risk level, when to seek help
- For medicine questions: Explain dosage, side effects, safety, interactions
- For diet/lifestyle: Provide dietary advice, exercise recommendations, lifestyle tips
- For mental health: Offer support, coping strategies, when to seek professional help
- For child health: Provide age-appropriate advice, safety considerations
- For emergency questions: Assess urgency, provide immediate action steps
- For chronic conditions: Offer management strategies, monitoring advice
- For women's health: Provide gender-specific guidance
- For elderly care: Consider age-related factors, medication management
- For general wellness: Offer preventive health advice

Always include appropriate disclaimers and encourage professional medical consultation when needed.""",

        'ur': f"""آپ ایک جامع طبی AI اسسٹنٹ ہیں۔ صارف کے سوال کے مطابق مناسب طبی رہنمائی فراہم کریں:

صارف کا سوال: {symptoms}

جواب کی رہنمائی:
- علامات کے لیے: تشخیص، علاج، احتیاطی تدابیر، خطرے کی سطح، ڈاکٹر سے کب رجوع کرنا ہے
- دوائی کے سوالات کے لیے: خوراک، مضر اثرات، حفاظت، تعاملات کی وضاحت
- غذا/طرز زندگی کے لیے: غذائی مشورے، ورزش کی تجاویز، طرز زندگی کی تجاویز
- ذہنی صحت کے لیے: مدد، نمٹنے کی حکمت عملیاں، پیشہ ورانہ مدد کب حاصل کریں
- بچوں کی صحت کے لیے: عمر کے مطابق مشورے، حفاظتی تدابیر
- ہنگامی سوالات کے لیے: فوری ضرورت کا اندازہ، فوری کارروائی کے اقدامات
- دائمی حالات کے لیے: انتظام کی حکمت عملیاں، نگرانی کے مشورے
- خواتین کی صحت کے لیے: صنفی مخصوص رہنمائی
- بزرگوں کی دیکھ بھال کے لیے: عمر سے متعلق عوامل، دوائی کا انتظام
- عمومی صحت کے لیے: روک تھام کی صحت کے مشورے

ہمیشہ مناسب وارننگ شامل کریں اور ضرورت پڑنے پر پیشہ ورانہ طبی مشاورت کی حوصلہ افزائی کریں۔""",

        'ur_roman': f"""You are a comprehensive medical AI assistant. The user is asking in Roman Urdu (Urdu written in English letters). 
Please respond in the same style - using Roman Urdu (English letters) but with Urdu grammar and expressions.

USER QUESTION: {symptoms}

RESPONSE GUIDELINES:
- Respond in Roman Urdu (English letters) with Urdu grammar
- For symptoms: Provide diagnosis, treatments, precautions, risk level, when to seek help
- For medicine questions: Explain dosage, side effects, safety, interactions
- For diet/lifestyle: Provide dietary advice, exercise recommendations, lifestyle tips
- For mental health: Offer support, coping strategies, when to seek professional help
- For child health: Provide age-appropriate advice, safety considerations
- For emergency questions: Assess urgency, provide immediate action steps
- For chronic conditions: Offer management strategies, monitoring advice
- For women's health: Provide gender-specific guidance
- For elderly care: Consider age-related factors, medication management
- For general wellness: Offer preventive health advice

Use natural Roman Urdu expressions like: "Aap ko ye masla hai", "Is ka ilaaj ye hai", "Doctor se rabta karein"
Always include appropriate disclaimers and encourage professional medical consultation when needed."""
    }

    try:
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": base_prompt.get(language, base_prompt['en'])}],
            temperature=0.7,
            max_tokens=1000
        )
        content = response.choices[0].message.content.strip()

        if contains_mental_health_terms(symptoms):
            if language == 'ur_roman':
                content += "\n\n🧠 Mental Health Support:\nAgar aap tension, stress ya anxiety feel kar rahe hain to kisi trusted person se baat karein. Aap akela nahi hain. Mental health professional se rabta karne ka sochiye."
            else:
                content += "\n\n🧠 Mental Health Support:\nIf you're feeling overwhelmed, stressed, or anxious, talk to someone you trust. You're not alone. Consider reaching out to a mental health professional for support."

        # Add appropriate follow-up suggestions based on question type
        if any(word in symptoms.lower() for word in ['medicine', 'medication', 'pill', 'drug', 'dawai', 'dawa']):
            if language == 'ur_roman':
                content += "\n\n💬 Follow-up Suggestion: Kya aap ko koi allergy hai ya aap koi aur dawai le rahe hain?"
            else:
                content += "\n\n💬 Follow-up Suggestion: Do you have any allergies or are you taking other medications?"
        elif any(word in symptoms.lower() for word in ['child', 'baby', 'kid', 'bacha', 'bachi']):
            if language == 'ur_roman':
                content += "\n\n💬 Follow-up Suggestion: Aap ke bache ki umar kya hai aur abhi kya symptoms hain?"
            else:
                content += "\n\n💬 Follow-up Suggestion: How old is your child and what are their current symptoms?"
        elif any(word in symptoms.lower() for word in ['emergency', 'serious', 'hospital', 'ambulance', 'emergency', 'serious']):
            if language == 'ur_roman':
                content += "\n\n💬 Follow-up Suggestion: Kya aap ko koi severe symptoms hain jaise chest pain ya breathing problem?"
            else:
                content += "\n\n💬 Follow-up Suggestion: Are you experiencing any severe symptoms like chest pain or difficulty breathing?"
        else:
            if language == 'ur_roman':
                content += "\n\n💬 Follow-up Suggestion: Kya aap ko koi aur symptoms ya concerns hain?"
            else:
                content += "\n\n💬 Follow-up Suggestion: Do you have any other symptoms or concerns?"
        return content

    except Exception as e:
        print(f"[GROQ API Error] {e}")
        return "⚠️ Sorry, I couldn't process your request."

# 🌐 Homepage
@app.route('/')
def index():
    return render_template('chat.html')

# 💬 Chat Interaction Endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id') or str(uuid.uuid4())

        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        language = detect_language(user_message)
        ai_response = get_ai_response(user_message, language)

        emergency_contacts = []

        entry = {
            'id': len(conversations.get(conversation_id, [])) + 1,
            'user_message': user_message,
            'ai_response': ai_response,
            'language': language,
            'timestamp': datetime.now().isoformat()
        }

        conversations.setdefault(conversation_id, []).append(entry)

        return jsonify({
            'conversation_id': conversation_id,
            'response': ai_response,
            'timestamp': entry['timestamp'],
            'language': language
        })

    except Exception as e:
        print(f"[Chat Error] {e}")
        return jsonify({'error': str(e)}), 500

# 📄 Generate PDF Report
@app.route('/api/generate-pdf/<conversation_id>')
def generate_pdf(conversation_id):
    try:
        if conversation_id not in conversations:
            return jsonify({'error': 'Conversation not found'}), 404

        pdf_path = generate_pdf_report(conversations[conversation_id], conversation_id)
        return send_file(pdf_path, as_attachment=True,
                         download_name=f'health_report_{conversation_id}.pdf',
                         mimetype='application/pdf')
    except Exception as e:
        print(f"[PDF Error] {e}")
        return jsonify({'error': str(e)}), 500

# 📤 Share Report via WhatsApp
@app.route('/api/share-whatsapp/<conversation_id>')
def share_whatsapp(conversation_id):
    try:
        if conversation_id not in conversations:
            return jsonify({'error': 'Conversation not found'}), 404

        # Generate PDF first
        pdf_path = generate_pdf_report(conversations[conversation_id], conversation_id)
        
        # Create comprehensive WhatsApp share message
        conversation = conversations[conversation_id]
        first_message = conversation[0]['user_message'] if conversation else "Health Consultation"
        
        # Analyze conversation for key information
        total_messages = len(conversation)
        consultation_duration = "5-10 minutes"  # Estimated
        
        # Extract AI responses to find diagnosis and recommendations
        ai_responses = [entry['ai_response'] for entry in conversation if entry['ai_response']]
        
        # Create comprehensive report
        report = f"""🏥 AI Health Assistant - Medical Consultation Report

📅 Date: {datetime.now().strftime('%d %B %Y')}
⏰ Time: {datetime.now().strftime('%I:%M %p')}
🆔 Report ID: HC-{conversation_id[:8]}

👤 Patient Information:
• Primary Concern: {first_message[:100]}{'...' if len(first_message) > 100 else ''}
• Consultation Duration: {consultation_duration}
• Total Exchanges: {total_messages}

📊 Consultation Summary:"""

        # Add first few exchanges
        for i, entry in enumerate(conversation[:3], 1):
            report += f"""
{i}. Q: {entry['user_message'][:80]}{'...' if len(entry['user_message']) > 80 else ''}
   A: {entry['ai_response'][:120]}{'...' if len(entry['ai_response']) > 120 else ''}"""

        if len(conversation) > 3:
            report += f"""
... and {len(conversation) - 3} more exchanges

💊 Key Recommendations:"""

        # Extract key recommendations from AI responses
        for response in ai_responses[:2]:  # First 2 responses
            if 'treatment' in response.lower() or 'recommend' in response.lower():
                lines = response.split('\n')
                for line in lines:
                    if any(keyword in line.lower() for keyword in ['treatment', 'recommend', 'take', 'avoid', 'precaution']):
                        if len(line.strip()) > 10:
                            report += f"\n• {line.strip()[:100]}{'...' if len(line.strip()) > 100 else ''}"
                            break

        report += f"""

⚠️ Important Guidelines:
• Monitor symptoms closely
• Follow recommended treatments
• Seek medical help if symptoms worsen
• Keep this report for doctor consultation

🏥 Medical Disclaimer:
This report is generated by AI and is for informational purposes only. It should NOT replace professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for medical concerns.

📄 Full detailed PDF report available for download.
📞 Emergency: Call local emergency services if experiencing severe symptoms."""

        # Encode message for WhatsApp URL
        encoded_message = urllib.parse.quote(report)
        
        # Create WhatsApp share URL
        whatsapp_url = f"https://wa.me/?text={encoded_message}"
        
        return jsonify({
            'success': True,
            'whatsapp_url': whatsapp_url,
            'message': 'WhatsApp share link generated successfully'
        })
        
    except Exception as e:
        print(f"[WhatsApp Share Error] {e}")
        return jsonify({'error': str(e)}), 500



# 🔊 Text-to-Speech Endpoint
@app.route('/api/text-to-speech', methods=['POST'])
def tts():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        language = data.get('language', 'en')
        if not text:
            return jsonify({'error': 'Text required'}), 400
        audio_path = text_to_speech(text, language)
        return send_file(audio_path, as_attachment=True,
                         download_name=f'speech_{language}.mp3',
                         mimetype='audio/mpeg')
    except Exception as e:
        print(f"[TTS Error] {e}")
        return jsonify({'error': str(e)}), 500

# 💾 Save Chat
@app.route('/api/save-chat/<conversation_id>', methods=['POST'])
def save_chat(conversation_id):
    if conversation_id not in conversations:
        return jsonify({'error': 'Conversation not found'}), 404
    saved_id = str(uuid.uuid4())
    saved_chats[saved_id] = {
        'id': saved_id,
        'title': f"Consultation - {datetime.now().strftime('%Y-%m-%d %I:%M %p')}",
        'conversation': conversations[conversation_id].copy(),
        'saved_at': datetime.now().isoformat()
    }
    return jsonify({'saved_chat_id': saved_id, 'success': True})

# 📁 List All Saved Chats
@app.route('/api/saved-chats', methods=['GET'])
def list_saved_chats():
    return jsonify({'saved_chats': list(saved_chats.values())})

# 📄 Retrieve a Saved Chat
@app.route('/api/saved-chat/<saved_chat_id>', methods=['GET'])
def get_saved_chat(saved_chat_id):
    return jsonify({'saved_chat': saved_chats.get(saved_chat_id, {})})

# ❌ Delete a Saved Chat
@app.route('/api/delete-saved-chat/<saved_chat_id>', methods=['DELETE'])
def delete_saved_chat(saved_chat_id):
    if saved_chat_id in saved_chats:
        saved_chats.pop(saved_chat_id)
        return jsonify({'success': True})
    return jsonify({'error': 'Chat not found'}), 404

# 💊 Medicine Database Endpoint
@app.route('/api/medicine-info', methods=['POST'])
def get_medicine_info():
    try:
        data = request.get_json()
        medicine_name = data.get('medicine', '').strip()
        language = data.get('language', 'en')
        
        if not medicine_name:
            return jsonify({'error': 'Medicine name is required'}), 400

        # AI prompt for medicine information
        medicine_prompt = {
            'en': f"""You are a medical AI assistant specializing in medicine information. Provide comprehensive details for: {medicine_name}

Please provide:
1. Generic Name and Brand Names
2. What it's used for (indications)
3. How to take it (dosage instructions)
4. Common side effects
5. Serious side effects (when to stop)
6. Drug interactions (what to avoid)
7. Precautions and warnings
8. Storage instructions
9. Overdose symptoms
10. Pregnancy/Breastfeeding safety

Format as a structured response with clear sections.""",

            'ur': f"""آپ ایک طبی AI اسسٹنٹ ہیں جو دوائی کی معلومات میں مہارت رکھتے ہیں۔ اس دوائی کے لیے مکمل تفصیلات فراہم کریں: {medicine_name}

براہ کرم فراہم کریں:
1. جنریک نام اور برانڈ نام
2. یہ کس کے لیے استعمال ہوتی ہے
3. اسے کیسے لینا ہے (خوراک کی ہدایات)
4. عام مضر اثرات
5. سنگین مضر اثرات (کب روکنا ہے)
6. دوائی کے تعاملات (کیا بچنا ہے)
7. احتیاطی تدابیر اور وارننگ
8. ذخیرہ کرنے کی ہدایات
9. زیادہ خوراک کی علامات
10. حمل/دودھ پلانے کی حفاظت

واضح حصوں کے ساتھ منظم جواب کے طور پر فارمیٹ کریں۔""",

            'ur_roman': f"""You are a medical AI assistant specializing in medicine information. Provide comprehensive details for: {medicine_name}

Please provide in Roman Urdu (English letters with Urdu grammar):
1. Generic Name and Brand Names
2. What it's used for (indications)
3. How to take it (dosage instructions)
4. Common side effects
5. Serious side effects (when to stop)
6. Drug interactions (what to avoid)
7. Precautions and warnings
8. Storage instructions
9. Overdose symptoms
10. Pregnancy/Breastfeeding safety

Format as a structured response with clear sections in Roman Urdu style."""
        }

        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": medicine_prompt.get(language, medicine_prompt['en'])}],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content.strip()
        
        return jsonify({
            'success': True,
            'medicine_name': medicine_name,
            'information': content,
            'language': language
        })

    except Exception as e:
        print(f"[Medicine Info Error] {e}")
        return jsonify({'error': str(e)}), 500

# 💊 Drug Interaction Checker
@app.route('/api/drug-interactions', methods=['POST'])
def check_drug_interactions():
    try:
        data = request.get_json()
        medicines = data.get('medicines', [])
        language = data.get('language', 'en')
        
        if not medicines or len(medicines) < 2:
            return jsonify({'error': 'At least 2 medicines required for interaction check'}), 400

        medicines_text = ', '.join(medicines)
        
        interaction_prompt = {
            'en': f"""You are a medical AI assistant specializing in drug interactions. Check for potential interactions between these medicines: {medicines_text}

Please provide:
1. Potential interactions between these medicines
2. Severity level (Low/Moderate/High/Severe)
3. What happens if taken together
4. Recommendations (avoid, monitor, separate timing)
5. Alternative medicines if needed
6. Symptoms to watch for
7. When to seek medical help

Format as a structured response with clear warnings.""",

            'ur': f"""آپ ایک طبی AI اسسٹنٹ ہیں جو دوائی کے تعاملات میں مہارت رکھتے ہیں۔ ان دوائیوں کے درمیان ممکنہ تعاملات چیک کریں: {medicines_text}

براہ کرم فراہم کریں:
1. ان دوائیوں کے درمیان ممکنہ تعاملات
2. شدت کی سطح (کم/درمیانی/زیادہ/شدید)
3. ایک ساتھ لینے پر کیا ہوتا ہے
4. سفارشات (بچنا، نگرانی، الگ وقت)
5. متبادل دوائیاں اگر ضروری ہوں
6. دیکھنے کی علامات
7. طبی مدد کب حاصل کریں

واضح وارننگ کے ساتھ منظم جواب کے طور پر فارمیٹ کریں۔""",

            'ur_roman': f"""You are a medical AI assistant specializing in drug interactions. Check for potential interactions between these medicines: {medicines_text}

Please provide in Roman Urdu:
1. Potential interactions between these medicines
2. Severity level (Low/Moderate/High/Severe)
3. What happens if taken together
4. Recommendations (avoid, monitor, separate timing)
5. Alternative medicines if needed
6. Symptoms to watch for
7. When to seek medical help

Format as a structured response with clear warnings in Roman Urdu style."""
        }

        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": interaction_prompt.get(language, interaction_prompt['en'])}],
            temperature=0.7,
            max_tokens=1200
        )
        
        content = response.choices[0].message.content.strip()
        
        return jsonify({
            'success': True,
            'medicines': medicines,
            'interactions': content,
            'language': language
        })

    except Exception as e:
        print(f"[Drug Interactions Error] {e}")
        return jsonify({'error': str(e)}), 500

# 💊 Dosage Calculator
@app.route('/api/dosage-calculator', methods=['POST'])
def calculate_dosage():
    try:
        data = request.get_json()
        medicine_name = data.get('medicine', '').strip()
        age = data.get('age', 0)
        weight = data.get('weight', 0)
        condition = data.get('condition', '')
        language = data.get('language', 'en')
        
        if not medicine_name:
            return jsonify({'error': 'Medicine name is required'}), 400

        dosage_prompt = {
            'en': f"""You are a medical AI assistant specializing in dosage calculations. Calculate appropriate dosage for:

Medicine: {medicine_name}
Age: {age} years
Weight: {weight} kg
Condition: {condition}

Please provide:
1. Recommended dosage based on age and weight
2. How often to take it
3. Best time to take it
4. Duration of treatment
5. Adjustments for age/weight
6. Maximum daily dose
7. What to do if missed a dose
8. Signs of overdose
9. Special instructions for children/elderly
10. When to consult doctor for dosage changes

IMPORTANT: Always include disclaimer that this is for reference only and doctor's advice should be followed.""",

            'ur': f"""آپ ایک طبی AI اسسٹنٹ ہیں جو خوراک کی گنتی میں مہارت رکھتے ہیں۔ اس کے لیے مناسب خوراک کا حساب کریں:

دوائی: {medicine_name}
عمر: {age} سال
وزن: {weight} کلو
حالت: {condition}

براہ کرم فراہم کریں:
1. عمر اور وزن کے مطابق تجویز کردہ خوراک
2. کتنی بار لینا ہے
3. لینے کا بہترین وقت
4. علاج کی مدت
5. عمر/وزن کے لیے ترتیبات
6. روزانہ کی زیادہ سے زیادہ خوراک
7. اگر خوراک چھوٹ جائے تو کیا کرنا ہے
8. زیادہ خوراک کی علامات
9. بچوں/بزرگوں کے لیے خاص ہدایات
10. خوراک میں تبدیلی کے لیے ڈاکٹر سے کب مشورہ کریں

اہم: ہمیشہ وارننگ شامل کریں کہ یہ صرف حوالے کے لیے ہے اور ڈاکٹر کی مشورے پر عمل کرنا چاہیے۔""",

            'ur_roman': f"""You are a medical AI assistant specializing in dosage calculations. Calculate appropriate dosage for:

Medicine: {medicine_name}
Age: {age} years
Weight: {weight} kg
Condition: {condition}

Please provide in Roman Urdu:
1. Recommended dosage based on age and weight
2. How often to take it
3. Best time to take it
4. Duration of treatment
5. Adjustments for age/weight
6. Maximum daily dose
7. What to do if missed a dose
8. Signs of overdose
9. Special instructions for children/elderly
10. When to consult doctor for dosage changes

IMPORTANT: Always include disclaimer that this is for reference only and doctor's advice should be followed."""
        }

        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": dosage_prompt.get(language, dosage_prompt['en'])}],
            temperature=0.7,
            max_tokens=1200
        )
        
        content = response.choices[0].message.content.strip()
        
        return jsonify({
            'success': True,
            'medicine_name': medicine_name,
            'age': age,
            'weight': weight,
            'condition': condition,
            'dosage_info': content,
            'language': language
        })

    except Exception as e:
        print(f"[Dosage Calculator Error] {e}")
        return jsonify({'error': str(e)}), 500

# 🩺 AI-Powered Diagnostics Endpoints

@app.route('/api/symptom-analyzer', methods=['POST'])
def analyze_symptoms():
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', '')
        age = data.get('age', 0)
        gender = data.get('gender', '')
        medical_history = data.get('medical_history', '')
        language = data.get('language', 'en')
        
        if not symptoms:
            return jsonify({'error': 'Symptoms are required'}), 400
        
        prompt = f"""
        As an advanced medical AI diagnostician, analyze the following symptoms and provide comprehensive assessment:
        
        Patient Information:
        - Age: {age} years
        - Gender: {gender}
        - Symptoms: {symptoms}
        - Medical History: {medical_history}
        
        Please provide detailed analysis including:
        1. Possible conditions/diseases (with probability)
        2. Severity assessment (mild/moderate/severe)
        3. Urgency level (immediate/soon/routine)
        4. Recommended diagnostic tests
        5. Potential complications to watch for
        6. Immediate actions to take
        7. When to seek emergency care
        8. Preventive measures
        9. Lifestyle recommendations
        10. Follow-up timeline
        
        Respond in {language} language. Be thorough but accessible.
        """
        
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1200
        )
        
        result = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'analysis': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/disease-predictor', methods=['POST'])
def predict_disease():
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        risk_factors = data.get('risk_factors', [])
        age = data.get('age', 0)
        family_history = data.get('family_history', '')
        lifestyle = data.get('lifestyle', '')
        language = data.get('language', 'en')
        
        if not symptoms:
            return jsonify({'error': 'Symptoms are required'}), 400
        
        symptoms_text = ', '.join(symptoms) if isinstance(symptoms, list) else symptoms
        risk_factors_text = ', '.join(risk_factors) if isinstance(risk_factors, list) else risk_factors
        
        prompt = f"""
        As a medical AI specialist, assess disease risk based on the following comprehensive patient data:
        
        Patient Profile:
        - Age: {age} years
        - Current Symptoms: {symptoms_text}
        - Risk Factors: {risk_factors_text}
        - Family History: {family_history}
        - Lifestyle Factors: {lifestyle}
        
        Provide detailed risk assessment including:
        1. Most likely conditions (with risk percentages)
        2. Differential diagnosis (other possibilities)
        3. Risk stratification (low/medium/high)
        4. Contributing factors analysis
        5. Preventive measures
        6. Recommended screenings
        7. Lifestyle modifications
        8. Monitoring frequency
        9. Early warning signs
        10. Specialist consultation recommendations
        
        Respond in {language} language. Be comprehensive and evidence-based.
        """
        
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1200
        )
        
        result = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'prediction': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/genetic-risk-calculator', methods=['POST'])
def calculate_genetic_risk():
    try:
        data = request.get_json()
        family_history = data.get('family_history', {})
        age = data.get('age', 0)
        ethnicity = data.get('ethnicity', '')
        lifestyle = data.get('lifestyle', {})
        language = data.get('language', 'en')
        
        if not family_history:
            return jsonify({'error': 'Family history is required'}), 400
        
        prompt = f"""
        As a genetic health AI specialist, analyze genetic risk factors based on family history:
        
        Patient Information:
        - Age: {age} years
        - Ethnicity: {ethnicity}
        - Family History: {family_history}
        - Lifestyle Factors: {lifestyle}
        
        Provide comprehensive genetic risk assessment including:
        1. Inherited disease risks
        2. Genetic predisposition analysis
        3. Risk percentages for various conditions
        4. Age-related risk factors
        5. Ethnicity-specific risks
        6. Preventive genetic testing recommendations
        7. Family screening suggestions
        8. Lifestyle risk modifications
        9. Early detection strategies
        10. Genetic counseling recommendations
        
        Respond in {language} language. Be thorough and sensitive to family concerns.
        """
        
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1200
        )
        
        result = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'genetic_risk': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mental-health-assessment', methods=['POST'])
def assess_mental_health():
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        mood_changes = data.get('mood_changes', '')
        sleep_patterns = data.get('sleep_patterns', '')
        stress_levels = data.get('stress_levels', '')
        life_events = data.get('life_events', '')
        language = data.get('language', 'en')
        
        if not symptoms:
            return jsonify({'error': 'Mental health symptoms are required'}), 400
        
        symptoms_text = ', '.join(symptoms) if isinstance(symptoms, list) else symptoms
        
        prompt = f"""
        As a mental health AI specialist, conduct a comprehensive mental health assessment:
        
        Patient Mental Health Profile:
        - Current Symptoms: {symptoms_text}
        - Mood Changes: {mood_changes}
        - Sleep Patterns: {sleep_patterns}
        - Stress Levels: {stress_levels}
        - Recent Life Events: {life_events}
        
        Provide detailed mental health analysis including:
        1. Potential mental health conditions
        2. Severity assessment (mild/moderate/severe)
        3. Risk factors identification
        4. Crisis assessment (if applicable)
        5. Coping strategies
        6. Professional help recommendations
        7. Self-care techniques
        8. Support system suggestions
        9. Emergency resources
        10. Follow-up care plan
        
        Respond in {language} language. Be compassionate and supportive.
        """
        
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1200
        )
        
        result = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'mental_health_assessment': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/child-health-monitor', methods=['POST'])
def monitor_child_health():
    try:
        data = request.get_json()
        child_age = data.get('child_age', 0)
        symptoms = data.get('symptoms', '')
        growth_concerns = data.get('growth_concerns', '')
        behavior_changes = data.get('behavior_changes', '')
        vaccination_status = data.get('vaccination_status', '')
        language = data.get('language', 'en')
        
        if not child_age or not symptoms:
            return jsonify({'error': 'Child age and symptoms are required'}), 400
        
        prompt = f"""
        As a pediatric AI specialist, provide comprehensive child health monitoring and assessment:
        
        Child Health Profile:
        - Age: {child_age} years/months
        - Current Symptoms: {symptoms}
        - Growth Concerns: {growth_concerns}
        - Behavior Changes: {behavior_changes}
        - Vaccination Status: {vaccination_status}
        
        Provide detailed pediatric assessment including:
        1. Age-appropriate health evaluation
        2. Growth and development assessment
        3. Symptom analysis for children
        4. Developmental milestones check
        5. Vaccination recommendations
        6. Nutritional guidance
        7. Safety recommendations
        8. Emergency warning signs
        9. Pediatrician consultation advice
        10. Parent education resources
        
        Respond in {language} language. Be child-friendly and parent-supportive.
        """
        
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1200
        )
        
        result = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'child_health_assessment': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 🩺 API Health Check
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

# 🧪 Run the Flask App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
