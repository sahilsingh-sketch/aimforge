import logging
import time
from backend.services.ai.gemini import GeminiProvider
from backend.services.ai.groq import GroqProvider
from backend.services.ai.deepseek import DeepSeekProvider
from backend.services.ai.base import FatalProviderError

logger = logging.getLogger(__name__)

class AIAnalysisService:
    def __init__(self):
        # The exact failover order: Gemini -> Groq -> DeepSeek
        self.providers = [
            GeminiProvider(),
            GroqProvider(),
            DeepSeekProvider()
        ]
        self.MAX_PROMPT_LENGTH = 100000

    def enforce_prompt_limit(self, prompt: str) -> str:
        """
        Validates prompt size. If it exceeds MAX_PROMPT_LENGTH, forcefully truncates the middle of the timeline
        so that early match info and late match info are preserved.
        """
        current_len = len(prompt)
        logger.info(f"[AI SERVICE] Raw Prompt Length: {current_len} characters")
        
        if current_len <= self.MAX_PROMPT_LENGTH:
            return prompt
            
        logger.warning(f"[AI SERVICE] Prompt length {current_len} exceeds {self.MAX_PROMPT_LENGTH} characters. Compressing...")
        
        # Simple heuristic: Keep first 7500 chars, and last 7500 chars.
        half = int(self.MAX_PROMPT_LENGTH / 2) - 50 # 50 chars for the truncation message
        
        truncated_prompt = (
            prompt[:half] + 
            "\n\n... [TIMELINE TRUNCATED DUE TO LENGTH LIMITS] ...\n\n" + 
            prompt[-half:]
        )
        
        logger.info(f"[AI SERVICE] Compressed Prompt Length: {len(truncated_prompt)} characters")
        return truncated_prompt

    def generate_gameplay_report(self, job_id: str, raw_prompt: str) -> dict:
        prompt = self.enforce_prompt_limit(raw_prompt)
        
        providers_attempted = []
        errors = {}

        for provider in self.providers:
            provider_name = provider.name
            providers_attempted.append(provider_name)
            logger.info(f"Trying {provider_name.capitalize()}...")
            
            # Phase 4: Exponential Backoff (3 attempts instead of 2 for better resilience)
            max_attempts = 3
            backoff_factor = 2
            
            for attempt in range(max_attempts):
                try:
                    logger.info(f"[AI SERVICE] {provider_name.capitalize()} request started (Attempt {attempt+1}/{max_attempts})")
                    final_data = provider.generate(prompt)
                    final_data['jobId'] = job_id
                    final_data['provider_used'] = provider_name
                    logger.info(f"[AI SERVICE] {provider_name.capitalize()} response received")
                    logger.info(f"{provider_name.capitalize()} Success")
                    return final_data
                    
                except Exception as e:
                    error_details = str(e)
                    logger.warning(f"{provider_name.capitalize()} Attempt {attempt+1} Failed: {error_details}")
                    
                    if attempt < max_attempts - 1:
                        sleep_time = backoff_factor ** attempt
                        logger.info(f"[AI SERVICE] Retrying {provider_name.capitalize()} in {sleep_time} seconds...")
                        time.sleep(sleep_time)
                    else:
                        errors[provider_name] = error_details
                        logger.error(f"{provider_name.capitalize()} Exhausted all retries.")

        # If all providers fail, return the fallback structured error
        logger.error("All AI providers failed.")
        return {
            "status": "failed",
            "stage": "AI_ANALYSIS",
            "provider_attempted": providers_attempted,
            "reason": errors
        }

    def chat_with_coach(self, messages: list) -> str:
        """
        Executes a chat request against the AI providers with a fallback mechanism.
        If a provider throws a FatalProviderError, it immediately skips retries for that provider
        and moves to the next one.
        """
        errors = {}

        for provider in self.providers:
            provider_name = provider.name
            logger.info(f"[{provider_name.capitalize()}] Chat attempt started...")
            
            max_attempts = 3
            backoff_factor = 2
            
            for attempt in range(max_attempts):
                try:
                    response_text = provider.chat(messages)
                    logger.info(f"[{provider_name.capitalize()}] Chat successful.")
                    return response_text
                except FatalProviderError as fe:
                    logger.warning(f"[{provider_name.capitalize()}] Fatal Error on attempt {attempt+1}: {str(fe)}. Skipping retries for this provider.")
                    errors[provider_name] = str(fe)
                    break # Break out of retry loop for this provider, move to next provider
                except Exception as e:
                    error_details = str(e)
                    logger.warning(f"[{provider_name.capitalize()}] Chat Attempt {attempt+1} Failed: {error_details}")
                    
                    if attempt < max_attempts - 1:
                        sleep_time = backoff_factor ** attempt
                        logger.info(f"[AI SERVICE] Retrying {provider_name.capitalize()} in {sleep_time} seconds...")
                        time.sleep(sleep_time)
                    else:
                        errors[provider_name] = error_details
                        logger.error(f"[{provider_name.capitalize()}] Chat Exhausted all retries.")

        logger.error(f"All AI providers failed for chat. Errors: {errors}")
        raise Exception("All AI providers failed to process the chat request.")

