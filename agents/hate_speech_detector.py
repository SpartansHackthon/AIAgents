"""Hate Speech Detector Agent

This script defines the Hate Speech Detector Agent that uses the OpenRouter API 
for detecting hate speech in the input text.

Usage:
    from agents.hate_speech_detector import HateSpeechDetector
    
    detector = HateSpeechDetector()
    result = detector.detect("Some input text")
    print(result)

Dependencies:
    - OpenRouter API
    - requests
    - python-dotenv
"""

import os
import requests
from typing import Dict, Any


class HateSpeechDetector:
    """Detects hate speech using OpenRouter API."""
    
    def __init__(self):
        """Initialize the detector with API key from environment."""
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
    
    def detect(self, text: str) -> Dict[str, Any]:
        """
        Detect hate speech in the given text.
        
        Args:
            text: The text to analyze for hate speech
            
        Returns:
            A dictionary containing:
                - is_hate_speech: Boolean indicating if hate speech was detected
                - confidence: Float between 0 and 1
                - explanation: String explaining the classification
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")
        
        prompt = f"""Analyze the following text for hate speech. Respond in JSON format with:
{{
    "is_hate_speech": boolean,
    "confidence": float (0-1),
    "explanation": "brief explanation"
}}

Text to analyze: {text}"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "HateSpeechDetector/1.0",
            "HTTP-Referer": "http://localhost",
            "X-Title": "HateSpeechDetector"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse JSON response
            import json
            analysis = json.loads(content)
            
            return {
                "text": text,
                "is_hate_speech": analysis.get("is_hate_speech", False),
                "confidence": analysis.get("confidence", 0.0),
                "explanation": analysis.get("explanation", "No explanation provided"),
                "status": "success"
            }
        
        except requests.exceptions.RequestException as e:
            return {
                "text": text,
                "is_hate_speech": None,
                "confidence": 0.0,
                "explanation": f"API request failed: {str(e)}",
                "status": "error"
            }
        except (json.JSONDecodeError, KeyError) as e:
            return {
                "text": text,
                "is_hate_speech": None,
                "confidence": 0.0,
                "explanation": f"Failed to parse API response: {str(e)}",
                "status": "error"
            }
