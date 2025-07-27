#!/usr/bin/env python3
"""
Test script for Multilingual AI Health Assistant
"""

import requests
import json
import time

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/health')
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Groq Available: {data.get('groq_available', 'Unknown')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is the app running?")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint with fallback response"""
    try:
        # Test English message
        data = {
            'message': 'I have a headache and fever',
            'conversation_id': 'test-123'
        }
        
        response = requests.post(
            'http://localhost:5000/api/chat',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat endpoint working")
            print(f"   Conversation ID: {result.get('conversation_id')}")
            print(f"   Language: {result.get('language')}")
            print(f"   Response length: {len(result.get('response', ''))} characters")
            return True
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat test error: {e}")
        return False

def test_urdu_chat():
    """Test Urdu language support"""
    try:
        # Test Urdu message
        data = {
            'message': 'میرے سر میں درد ہے',
            'conversation_id': 'test-urdu-123'
        }
        
        response = requests.post(
            'http://localhost:5000/api/chat',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Urdu chat working")
            print(f"   Language detected: {result.get('language')}")
            return True
        else:
            print(f"❌ Urdu chat failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Urdu test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Multilingual AI Health Assistant")
    print("=" * 50)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    if not test_health_endpoint():
        print("❌ Health test failed. Make sure the app is running.")
        return
    
    # Test English chat
    print("\n2. Testing English chat...")
    if not test_chat_endpoint():
        print("❌ English chat test failed.")
        return
    
    # Test Urdu chat
    print("\n3. Testing Urdu chat...")
    if not test_urdu_chat():
        print("❌ Urdu chat test failed.")
        return
    
    print("\n🎉 All tests passed!")
    print("✅ The application is working correctly")
    print("\n📱 You can now:")
    print("   - Open http://localhost:5000 in your browser")
    print("   - Start chatting with the AI health assistant")
    print("   - Test both English and Urdu languages")
    print("   - Generate PDF reports and voice output")

if __name__ == '__main__':
    main() 