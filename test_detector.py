"""Test script for Hate Speech Detector"""

import sys
import os
from dotenv import load_dotenv
from agents.hate_speech_detector import HateSpeechDetector

# Load environment variables
load_dotenv()

def main():
    print("🔍 Initializing Hate Speech Detector...")
    
    try:
        detector = HateSpeechDetector()
        print("✅ Detector initialized successfully\n")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nPlease set OPENROUTER_API_KEY environment variable:")
        print("  Windows: $env:OPENROUTER_API_KEY='your-api-key'")
        print("  Linux/Mac: export OPENROUTER_API_KEY='your-api-key'")
        return 1
    
    # Test cases
    test_texts = [
        "This is a normal friendly message",
        "I absolutely love this product!",
    ]
    
    print("=" * 60)
    print("Testing Hate Speech Detector")
    print("=" * 60 + "\n")
    
    for i, text in enumerate(test_texts, 1):
        print(f"Test {i}: '{text}'")
        result = detector.detect(text)
        
        print(f"  Status: {result['status']}")
        if result['status'] == 'success':
            print(f"  Is Hate Speech: {result['is_hate_speech']}")
            print(f"  Confidence: {result['confidence']:.1%}")
            print(f"  Explanation: {result['explanation']}")
        else:
            print(f"  Error: {result['explanation']}")
        print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
