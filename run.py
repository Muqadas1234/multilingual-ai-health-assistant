#!/usr/bin/env python3
"""
Multilingual AI Health Assistant - Startup Script
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'groq', 'python-dotenv', 'gtts', 
        'reportlab', 'pillow', 'langdetect', 'requests', 'tavily-python'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
            return False
    
    return True

def check_config():
    """Check if configuration file exists"""
    config_files = ['.env', 'config.env']
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ Configuration file found: {config_file}")
            return True
    
    print("⚠️  No configuration file found")
    print("📝 Creating config.env with template...")
    
    config_template = """# AI API Configuration
GROQ_API_KEY=your_groq_api_key_here

# App Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Optional: Tavily Search API (if using)
TAVILY_API_KEY=your_tavily_api_key_here
"""
    
    try:
        with open('config.env', 'w') as f:
            f.write(config_template)
        print("✅ config.env created successfully!")
        print("📝 Please edit config.env and add your API keys before running the app")
        return False
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return False

def check_api_keys():
    """Check if API keys are configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv('config.env')
        
        groq_key = os.getenv('GROQ_API_KEY')
        tavily_key = os.getenv('TAVILY_API_KEY')
        
        if not groq_key or groq_key == 'your_groq_api_key_here':
            groq_configured = False
        else:
            groq_configured = True
            
        if not tavily_key or tavily_key == 'your_tavily_api_key_here':
            tavily_configured = False
        else:
            tavily_configured = True
        
        if groq_configured:
            print("✅ Groq API key configured")
        else:
            print("⚠️  Groq API key not configured")
            
        if tavily_configured:
            print("✅ Tavily API key configured")
        else:
            print("⚠️  Tavily API key not configured")
        
        if not groq_configured:
            print("\n⚠️  Warning: No AI API keys configured!")
            print("The app will work with fallback responses, but AI features will be limited.")
            print("Please add your API keys to config.env for full functionality.")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking API keys: {e}")
        return False

def main():
    """Main startup function"""
    print("🏥 Multilingual AI Health Assistant")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("\n⚙️  Checking configuration...")
    if not check_config():
        print("\n📝 Setup Instructions:")
        print("1. Edit config.env and add your API keys")
        print("2. Run this script again")
        sys.exit(1)
    
    print("\n🔑 Checking API keys...")
    check_api_keys()
    
    print("\n🚀 Starting the application...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 