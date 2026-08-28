from abc import ABC, abstractmethod

class AIProvider(ABC):
    """
    Abstract base class for AI providers.
    All providers must implement the generate method which takes a structured prompt
    and returns a standardized JSON object matching the frontend coaching schema.
    """
    
class FatalProviderError(Exception):
    """Exception raised for fatal errors that should not be retried (e.g. 429 quota, context length limits)."""
    pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the provider (e.g. 'gemini', 'groq', 'deepseek')"""
        pass

    @abstractmethod
    def generate(self, prompt: str) -> dict:
        """
        Takes the telemetry prompt and generates the coaching report.
        Must raise an exception if it fails (e.g. timeout, invalid JSON, API error)
        so that the orchestration service can trigger failover.
        """
        pass

    @abstractmethod
    def chat(self, messages: list) -> str:
        """
        Takes a list of messages (e.g. [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}])
        and generates a single text response string.
        """
        pass
