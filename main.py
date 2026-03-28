
import os
import sys
from dotenv import load_dotenv
from agents.hate_speech_detector import HateSpeechDetector

# Load environment variables
load_dotenv()

def main():
    print("=" * 70)
    print("🔍 HATE SPEECH DETECTOR - Interactive Mode")
    print("=" * 70)
    print("\nInitializing detector...")
    
    try:
        detector = HateSpeechDetector()
        print("✅ Detector ready!\n")
    except ValueError as e:
        print(f"❌ Error: {e}")
        return 1
    
    print("Instructions:")
    print("  - Type your text to analyze for hate speech")
    print("  - Type 'quit' or 'exit' to stop")
    print("  - Type 'help' for example texts")
    print("-" * 70 + "\n")
    
    while True:
        try:
            user_input = input("Enter text to analyze (or 'quit' to exit): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Exiting detector. Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print("\nExample texts you can test:")
                print("  - 'This is a normal friendly message'")
                print("  - 'I absolutely love this product!'")
                print("  - 'Great day today!'")
                print()
                continue
            
            if not user_input:
                print("⚠️  Please enter some text to analyze.\n")
                continue
            
            print("\n⏳ Analyzing text...")
            result = detector.detect(user_input)
            
            print("\n" + "=" * 70)
            print("📊 ANALYSIS RESULT")
            print("=" * 70)
            print(f"Text: '{user_input}'")
            print(f"Status: {result['status']}")
            
            if result['status'] == 'success':
                hate_speech = "🚨 YES - HATE SPEECH DETECTED" if result['is_hate_speech'] else "✅ NO - Not hate speech"
                print(f"Hate Speech: {hate_speech}")
                print(f"Confidence: {result['confidence']:.1%}")
                print(f"Explanation: {result['explanation']}")
            else:
                print(f"Error: {result['explanation']}")
            
            print("=" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Detector stopped. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}\n")

if __name__ == "__main__":
    sys.exit(main())
