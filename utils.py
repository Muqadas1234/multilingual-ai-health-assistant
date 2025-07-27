import os
import tempfile
from datetime import datetime
from gtts import gTTS
import uuid
import requests
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 🧾 PDF Report Generator
def generate_pdf_report(conversation, conversation_id):
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, f"health_report_{conversation_id}.pdf")

    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # Styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, alignment=1, spaceAfter=30, textColor=colors.darkblue)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Heading2'], fontSize=16, spaceAfter=20, textColor=colors.green)
    normal_style = ParagraphStyle('NormalText', parent=styles['Normal'], fontSize=12, spaceAfter=12, leading=16)
    disclaimer_style = ParagraphStyle('Disclaimer', parent=styles['Normal'], fontSize=10, spaceAfter=10, leading=14, textColor=colors.red, backColor=colors.lightyellow)

    # Header
    story.append(Paragraph("🏥 Health Consultation Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}", normal_style))
    story.append(Spacer(1, 20))

    # Disclaimer
    disclaimer = """
    ⚠️ This AI-generated report is for informational purposes only.
    It is NOT a substitute for professional medical advice, diagnosis, or treatment.
    Always consult a licensed physician or qualified healthcare provider.
    """
    story.append(Paragraph(disclaimer, disclaimer_style))
    story.append(Spacer(1, 30))

    # Conversation entries
    if not conversation:
        story.append(Paragraph("No conversation data found.", normal_style))
    else:
        for i, entry in enumerate(conversation, 1):
            story.append(Paragraph(f"🗂️ Consultation #{i}", subtitle_style))
            timestamp = entry.get('timestamp', 'Unknown Time')
            story.append(Paragraph(f"⏰ Time: {timestamp}", normal_style))
            story.append(Spacer(1, 10))

            story.append(Paragraph("🧍 User Symptoms:", normal_style))
            story.append(Paragraph(entry.get('user_message', 'N/A'), normal_style))
            story.append(Spacer(1, 10))

            story.append(Paragraph("🤖 AI Analysis & Suggestions:", normal_style))
            for section in entry.get('ai_response', '').split('\n\n'):
                if section.strip():
                    highlight = any(k in section.lower() for k in ['diagnosis', 'treatment', 'precautions', 'risk'])
                    story.append(Paragraph(f"<b>{section}</b>" if highlight else section, normal_style))
                    story.append(Spacer(1, 8))

            lang = entry.get('language', 'en')
            story.append(Paragraph(f"🌐 Language: {'Urdu' if lang == 'ur' else 'English'}", normal_style))
            story.append(Spacer(1, 30))

    # Tips
    story.append(Paragraph("💡 General Health Tips:", subtitle_style))
    for tip in [
        "• Exercise regularly and eat a balanced diet.",
        "• Stay hydrated and get enough sleep.",
        "• Avoid smoking and excessive alcohol.",
        "• Keep medical checkups up to date.",
        "• Track your symptoms and medications."
    ]:
        story.append(Paragraph(tip, normal_style))
        story.append(Spacer(1, 5))

    try:
        doc.build(story)
        return pdf_path
    except Exception as e:
        print(f"[PDF Error] {e}")
        raise Exception("PDF generation failed.")

# 🔊 Convert AI response to speech
def text_to_speech(text, language='en'):
    """Converts a given text to speech and saves as MP3 in temp directory."""
    temp_dir = tempfile.gettempdir()
    filename = f"speech_{uuid.uuid4().hex[:8]}.mp3"
    path = os.path.join(temp_dir, filename)

    lang_map = {'en': 'en', 'ur': 'ur'}

    try:
        tts = gTTS(text=text, lang=lang_map.get(language, 'en'), slow=False)
        tts.save(path)
        return path
    except Exception as e:
        print(f"[TTS Error] {e}")
        raise Exception("Failed to convert text to speech.")



# 🌍 Get City From IP (fallback if geolocation fails)
def get_user_location_from_ip(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        res.raise_for_status()
        return res.json().get("city", "Pakistan")
    except Exception as e:
        print(f"[IP Lookup Error] {e}")
        return "Pakistan"

# 🧹 Clean up old PDF and MP3 temp files
def cleanup_temp_files():
    temp_dir = tempfile.gettempdir()
    now = datetime.now()

    for fname in os.listdir(temp_dir):
        fpath = os.path.join(temp_dir, fname)
        try:
            ctime = datetime.fromtimestamp(os.path.getctime(fpath))
            if (fname.startswith('health_report_') and fname.endswith('.pdf') and (now - ctime).total_seconds() > 86400) or \
               (fname.startswith('speech_') and fname.endswith('.mp3') and (now - ctime).total_seconds() > 3600):
                os.remove(fpath)
        except Exception:
            continue
