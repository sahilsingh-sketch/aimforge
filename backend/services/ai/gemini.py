import time
import json
import logging
import requests
from backend.core.config import settings
from backend.services.ai.base import AIProvider, FatalProviderError
from backend.services.ai.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class GeminiProvider(AIProvider):
    @property
    def name(self) -> str:
        return "gemini"

    def generate(self, prompt: str) -> dict:
        has_key = bool(settings.GEMINI_API_KEY)
        logger.info(f"[{self.name.capitalize()}] API Key loaded: {has_key}")
        logger.info(f"[{self.name.capitalize()}] Prompt size: {len(prompt)} characters")
        
        if not has_key:
            error_msg = f"{self.name.capitalize()} Error:\n- Exception: ValueError('GEMINI_API_KEY is missing')\n- HTTP Status: N/A\n- Response Body: N/A"
            raise Exception(error_msg)
        
        model_name = "gemini-3.6-flash"
        logger.info(f"[{self.name.capitalize()}] Model: {model_name}")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "generationConfig": {"responseMimeType": "application/json"}
        }
        
        logger.info(f"[CELERY] Gemini request started")
        start_time = time.time()
        try:
            resp = requests.post(url, json=payload, timeout=(10, 60))
            duration = time.time() - start_time
            logger.info(f"[CELERY] Gemini response received in {duration:.2f} seconds")
            
            if not resp.ok:
                if resp.status_code in [400, 401, 402, 403, 404]:
                    raise FatalProviderError(f"{self.name.capitalize()} Fatal Error:\n- HTTP Status: {resp.status_code}\n- Response Body: {resp.text}")
                error_msg = f"{self.name.capitalize()} Error:\n- Exception: HTTPError\n- HTTP Status: {resp.status_code}\n- Response Body: {resp.text}"
                raise Exception(error_msg)
            
            data = resp.json()
            content = data['candidates'][0]['content']['parts'][0]['text']
            content = content.replace("```json", "").replace("```", "").strip()
            
            logger.info(f"[{self.name.capitalize()}] JSON parsing started")
            parsed_json = json.loads(content)
            logger.info(f"[{self.name.capitalize()}] JSON parsing completed")
            return parsed_json
        except requests.exceptions.Timeout:
            logger.error(f"[{self.name.capitalize()}] Connection/Read Timeout exceeded (60s).")
            raise Exception(f"{self.name.capitalize()} Error:\n- Exception: Timeout\n- HTTP Status: N/A\n- Response Body: N/A")
        except FatalProviderError:
            raise
        except Exception as e:
            if "Request duration:" not in str(e) and "Error:" not in str(e):
                duration = time.time() - start_time
                logger.info(f"[{self.name.capitalize()}] Request duration: {duration:.2f} seconds")
                error_msg = f"{self.name.capitalize()} Error:\n- Exception: {str(e)}\n- HTTP Status: N/A\n- Response Body: N/A"
                raise Exception(error_msg)
            raise e

    def chat(self, messages: list) -> str:
        has_key = bool(settings.GEMINI_API_KEY)
        if not has_key:
            raise FatalProviderError(f"{self.name.capitalize()} Fatal Error: GEMINI_API_KEY is missing")
            
        model_name = "gemini-3.6-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
        
        # Convert standard messages to Gemini format
        system_instruction = ""
        gemini_contents = []
        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            else:
                gemini_contents.append({"role": "model" if msg["role"] == "assistant" else "user", "parts": [{"text": msg["content"]}]})
        
        payload = {
            "contents": gemini_contents,
        }
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}
            
        try:
            resp = requests.post(url, json=payload, timeout=(10, 60))
            if not resp.ok:
                if resp.status_code in [400, 401, 402, 403, 404]:
                    raise FatalProviderError(f"{self.name.capitalize()} Fatal Error:\n- HTTP Status: {resp.status_code}\n- Response Body: {resp.text}")
                raise Exception(f"HTTPError: {resp.status_code} {resp.text}")
            
            data = resp.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        except requests.exceptions.Timeout:
            raise Exception(f"{self.name.capitalize()} Chat Timeout")
        except FatalProviderError:
            raise
        except Exception as e:
            raise Exception(f"{self.name.capitalize()} Chat Error: {str(e)}")

