import os
import requests
from dotenv import load_dotenv

class HateSpeechDetectorAgent:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.endpoint = 'https://api.openrouter.ai/hate-speech-detection'  # Example endpoint

    def detect_hate_speech(self, text):
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        payload = {'text': text}
        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Raises an HTTPError if the response was an error
            result = response.json()
            return self.format_response(result)
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    def batch_detect(self, texts):
        results = []
        for text in texts:
            result = self.detect_hate_speech(text)
            results.append(result)
        return results

    def format_response(self, result):
        is_hate_speech = result.get('is_hate_speech', False)
        confidence_score = result.get('confidence_score', 0)
        classification_type = result.get('classification_type', 'unknown')
        explanation = result.get('explanation', 'No explanation provided')
        return {
            'is_hate_speech': is_hate_speech,
            'confidence_score': confidence_score,
            'classification_type': classification_type,
            'explanation': explanation
        }