# 🏥 Multilingual AI Health Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

A sophisticated, production-ready AI-powered health assistant that provides intelligent medical diagnosis, treatment suggestions, and comprehensive health guidance in multiple languages. Features a modern WhatsApp-style chat interface, advanced AI diagnostics, medicine database, PDF report generation, and text-to-speech capabilities.

## 📋 Table of Contents

- [✨ Features](#-features)
- [👥 Team](#-team)
- [🏆 Hackathon Info](#-hackathon-info)
- [🛠️ Technologies Used](#️-technologies-used)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🎯 Usage Guide](#-usage-guide)
- [🏗️ Project Structure](#️-project-structure)
- [🔧 API Endpoints](#-api-endpoints)
- [🎨 UI/UX Features](#-uiux-features)
- [🤖 AI Capabilities](#-ai-capabilities)
- [📱 Responsive Design](#-responsive-design)
- [🔒 Security Features](#-security-features)
- [🧪 Testing](#-testing)
- [📄 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Features

### 🎯 Core Features
- **🤖 AI-Powered Health Assistant** - Intelligent symptom analysis and medical guidance
- **🌐 Multilingual Support** - English, Urdu (native script), and Roman Urdu with auto-detection
- **💬 Modern Chat Interface** - WhatsApp-style conversation format with real-time messaging
- **📄 PDF Report Generation** - Comprehensive health consultation reports
- **🔊 Text-to-Speech** - Voice output for accessibility and convenience
- **💊 Medicine Database** - Drug information, interactions, and dosage calculator
- **🩺 AI Diagnostics** - Symptom analyzer, disease predictor, genetic risk calculator
- **🧠 Mental Health Assessment** - Comprehensive mental health evaluation
- **👶 Child Health Monitor** - Pediatric health monitoring and guidance
- **💾 State Persistence** - Maintains conversation and modal states across page refreshes

### 🎨 User Interface Features
- **📱 Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **🎨 Modern UI/UX** - Beautiful gradient design with smooth animations
- **⚡ Real-time Updates** - Dynamic message handling and auto-scroll
- **🌍 Language Badges** - Visual indicators for detected language
- **⏰ Timestamps** - Real-time message timing and conversation history
- **🎯 Smart Input** - Auto-expanding text area with character counter
- **🔍 Search Functionality** - Medicine and symptom search capabilities

### 🔧 Technical Features
- **🔄 Auto-save** - Automatic state saving every 30 seconds
- **💾 Local Storage** - Persistent data storage across sessions
- **📊 Error Handling** - Comprehensive error management and fallbacks
- **🔒 Security** - Environment-based API key management
- **⚡ Performance** - Optimized for fast response times
- **🧪 Testing** - Built-in testing suite for all features

## 👥 Team

### 🏆 Hackathon Team Members

| Role                      | Name(s)                 | Contribution                                      |
|---------------------------|---------------------    |---------------------------------------------------|
| Team Lead & Full-Stack Dev| sir Ahmed Gul and Muqadas  | Backend API, AI Integration, Project Architecture |
| Frontend Developer        | Muqadas                 | UI/UX Design, Responsive Layout, JavaScript       |
| Testing & Deployment      | Ahmed Gul               | Deployment, Testing, Documentation                |
| Presentation              | Tehreem Rauop               | Final Presentation, Slides                        |
| Project Coordinator       | 	Shahzad Husaain                | Project Coordination                              |



🏆 Hackathon Info
🎯 Project Overview
Multilingual AI Health Assistant was developed during gen ai Hackathon by pak angles -

🎪 Demo
Live Demo: [https://910dea49-aae4-4053-bbdb-7bb354e84614-00-b71vrabkpkov.sisko.replit.dev/]

🛠️ Technologies Used

### Backend Technologies
- **Python 3.8+** - Core programming language
- **Flask 2.3.3** - Web framework for API development
- **Groq API** - Primary AI language model (llama3-70b-8192)
- **gTTS 2.4.0** - Google Text-to-Speech integration
- **ReportLab 4.0.4** - PDF generation and report creation
- **Pillow 10.0.1** - Image processing for reports
- **langdetect 1.0.9** - Language detection and classification
- **requests 2.31.0** - HTTP client for API calls
- **python-dotenv 1.0.0** - Environment variable management

### Frontend Technologies
- **HTML5** - Semantic markup and structure
- **CSS3** - Modern styling with gradients and animations
- **JavaScript (ES6+)** - Dynamic functionality and state management
- **Bootstrap 5.3.0** - Responsive UI framework
- **Font Awesome** - Icon library for UI elements
- **LocalStorage API** - Client-side data persistence
- **Web Speech API** - Browser-based speech recognition
- **ResponsiveVoice.js** - Enhanced text-to-speech capabilities

### Development & Deployment
- **Git** - Version control system
- **pip** - Python package management
- **Virtual Environment** - Isolated development environment
- **Windows Batch Scripts** - Easy startup for Windows users
- **Cross-platform Compatibility** - Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites
- **Python 3.8 or higher**
- **Groq API key** for AI functionality
- **Modern web browser** with JavaScript enabled

### One-Click Start (Windows)
```bash
# Simply double-click the start.bat file
start.bat
```

### Command Line Start
```bash
# Clone the repository
git clone <repository-url>
cd Multilingual_AI_Health_Assistant_Doc

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py

# Or directly
python app.py
```

## 📦 Installation

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd Multilingual_AI_Health_Assistant_Doc
```

### Step 2: Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
# Copy configuration template
cp config.env .env

# Edit .env file with your API keys
nano .env  # or use any text editor
```

### Step 4: Run Application
```bash
# Use the smart startup script
python run.py

# Or run directly
python app.py
```

### Step 5: Access Application
Open your browser and navigate to: `http://localhost:5000`

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Groq API key for AI responses | Yes | None |
| `FLASK_SECRET_KEY` | Flask application secret key | Yes | `default-secret-key` |
| `FLASK_ENV` | Flask environment mode | No | `development` |
| `TAVILY_API_KEY` | Tavily search API key | No | None |

### API Key Setup

#### Groq API
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up and get your API key
3. Add to your `.env` file: `GROQ_API_KEY=your_key_here`

## 🎯 Usage Guide

### Basic Health Consultation
1. **Start Chat**: Type your symptoms in the chat input
2. **Language Detection**: System automatically detects English or Urdu
3. **AI Analysis**: Receive comprehensive health analysis and recommendations
4. **Follow-up**: Ask additional questions for detailed guidance

### Advanced Features

#### Medicine Database
- **Drug Information**: Search for medicine details, side effects, and usage
- **Drug Interactions**: Check for potential drug interactions
- **Dosage Calculator**: Calculate appropriate dosages based on age and weight

#### AI Diagnostics
- **Symptom Analyzer**: Detailed symptom analysis and possible conditions
- **Disease Predictor**: Predict potential diseases based on symptoms
- **Genetic Risk Calculator**: Assess genetic risk factors
- **Mental Health Assessment**: Comprehensive mental health evaluation
- **Child Health Monitor**: Pediatric health monitoring and guidance

#### Report Generation
- **PDF Reports**: Download comprehensive health consultation reports
- **WhatsApp Sharing**: Share reports via WhatsApp
- **Voice Output**: Listen to AI responses using text-to-speech

### Example Conversations

**English:**
```
User: "I have a headache and fever for the past 2 days"
AI: [Provides diagnosis, treatment, precautions, and risk assessment]
```

**Urdu:**
```
User: "میرے سر میں درد ہے اور بخار بھی ہے"
AI: [Provides response in Urdu with medical analysis]
```

**Roman Urdu:**
```
User: "Mere sar mein dard hai aur bukhar bhi hai"
AI: [Provides response in Roman Urdu with medical analysis]
```

## 🏗️ Project Structure

```
Multilingual_AI_Health_Assistant_Doc/
├── app.py                     # Main Flask application
├── utils.py                   # Utility functions (PDF, TTS)
├── run.py                     # Smart startup script
├── requirements.txt           # Python dependencies
├── start.bat                  # Windows startup script
├── test_app.py               # Application testing
├── test_pdf.html             # PDF testing utility
├── README.md                 # This file
├── PROJECT_SUMMARY.md        # Project overview
├── config.env                # Environment configuration
├── templates/
│   └── chat.html             # Main chat interface
└── static/
    └── style.css             # CSS styling
```

## 🔧 API Endpoints

### Core Chat Endpoints
- `POST /api/chat` - Main chat endpoint for AI responses
- `GET /api/health` - Health check endpoint
- `POST /api/text-to-speech` - Text-to-speech conversion

### Report Management
- `GET /api/generate-pdf/<conversation_id>` - Generate PDF reports
- `GET /api/share-whatsapp/<conversation_id>` - Share via WhatsApp
- `POST /api/save-chat/<conversation_id>` - Save conversation
- `GET /api/saved-chats` - List saved conversations
- `GET /api/saved-chat/<saved_chat_id>` - Get specific saved chat
- `DELETE /api/delete-saved-chat/<saved_chat_id>` - Delete saved chat

### Medicine Database
- `POST /api/medicine-info` - Get medicine information
- `POST /api/drug-interactions` - Check drug interactions
- `POST /api/dosage-calculator` - Calculate dosages

### AI Diagnostics
- `POST /api/symptom-analyzer` - Analyze symptoms
- `POST /api/disease-predictor` - Predict diseases
- `POST /api/genetic-risk-calculator` - Calculate genetic risks
- `POST /api/mental-health-assessment` - Mental health evaluation
- `POST /api/child-health-monitor` - Child health monitoring

## 🎨 UI/UX Features

### Chat Interface
- **Modern Design**: Gradient backgrounds with smooth animations
- **Message Bubbles**: WhatsApp-style conversation format
- **Language Indicators**: Visual badges showing detected language
- **Timestamps**: Real-time message timing
- **Auto-scroll**: Automatically scrolls to new messages
- **Loading States**: Visual feedback during AI processing

### Input System
- **Smart Input**: Auto-expanding text area
- **Character Counter**: Real-time character count with limits
- **Enter to Send**: Quick message sending with Enter key
- **Voice Input**: Speech-to-text capabilities
- **Language Detection**: Automatic language recognition

### Action Buttons
- **📄 Download PDF**: Generate comprehensive health reports
- **🔊 Voice Output**: Listen to AI responses
- **🗑️ Clear Chat**: Reset conversation history
- **💾 Save Chat**: Save important conversations
- **📤 Share**: Share reports via WhatsApp
- **🌐 Language Selector**: Manual language override

## 🤖 AI Capabilities

### Medical Analysis
- **Symptom Analysis**: Intelligent diagnosis with confidence levels
- **Treatment Recommendations**: Suggested remedies and medications
- **Precautions**: Lifestyle and safety advice
- **Risk Assessment**: Low/Medium/High risk categorization
- **Emergency Guidance**: When to seek professional help

### Language Processing
- **English**: Full medical terminology and explanations
- **Urdu (Native)**: Complete Urdu script support
- **Roman Urdu**: Urdu written in English letters
- **Auto-detection**: Intelligent language recognition
- **Context Awareness**: Maintains conversation context

### Specialized Features
- **Pediatric Care**: Age-appropriate health guidance
- **Mental Health**: Comprehensive mental health support
- **Medication Management**: Drug information and interactions
- **Genetic Assessment**: Risk factor analysis
- **Emergency Response**: Urgent situation handling

## 📱 Responsive Design

### Device Compatibility
- **Desktop**: Full-featured experience with all capabilities
- **Tablet**: Optimized touch interface with gesture support
- **Mobile**: Streamlined mobile experience with essential features

### Breakpoints
- **Large Screens**: 1200px+ - Full layout with side panels
- **Medium Screens**: 768px-1199px - Compact layout
- **Small Screens**: 320px-767px - Mobile-optimized layout

### Accessibility Features
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: ARIA labels and semantic HTML
- **High Contrast Mode**: Enhanced visibility options
- **Reduced Motion**: Respects user motion preferences
- **Focus Indicators**: Clear focus states for navigation

## 🔒 Security Features

### Data Protection
- **Environment Variables**: Secure API key management
- **Input Validation**: Comprehensive input sanitization
- **Error Handling**: Secure error messages without data leakage
- **Session Management**: Secure conversation handling

### Privacy Features
- **Local Storage**: Client-side data persistence
- **No Data Logging**: Conversations not stored on server
- **Secure API Calls**: HTTPS-only API communication
- **Temporary Files**: Automatic cleanup of generated files

## 🧪 Testing

### Built-in Testing
```bash
# Run the test suite
python test_app.py
```

### Test Coverage
- **API Endpoints**: All endpoints tested for functionality
- **Language Detection**: English and Urdu detection accuracy
- **PDF Generation**: Report creation and download
- **Error Handling**: Graceful error management
- **UI Components**: Modal functionality and state management

### Manual Testing
- **Cross-browser Testing**: Chrome, Firefox, Safari, Edge
- **Device Testing**: Desktop, tablet, mobile devices
- **API Testing**: Direct API endpoint testing
- **Performance Testing**: Load and response time testing

## 📄 Documentation

### Code Documentation
- **Inline Comments**: Comprehensive code documentation
- **Function Documentation**: Detailed function descriptions
- **API Documentation**: Complete endpoint documentation
- **Configuration Guide**: Step-by-step setup instructions

### User Documentation
- **Usage Guide**: Complete user manual
- **Feature Overview**: Detailed feature descriptions
- **Troubleshooting**: Common issues and solutions
- **FAQ**: Frequently asked questions

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

### Code Standards
- **Python**: Follow PEP 8 style guidelines
- **JavaScript**: Use ES6+ standards with proper error handling
- **CSS**: Follow BEM methodology for class naming
- **HTML**: Use semantic HTML5 elements




## 🙏 Acknowledgments

- **Groq** for high-performance AI inference and llama3-70b-8192 model
- **Bootstrap** for the responsive UI framework
- **Font Awesome** for the icon library
- **Google** for text-to-speech capabilities

---

**⚠️ Medical Disclaimer**: This AI health assistant is for informational purposes only and should not replace professional medical advice. Always consult with qualified healthcare providers for medical decisions. 
