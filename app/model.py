"""
Model setup for LLM integration using Google's Gemini model.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage

from app.config import GEMINI_API_KEY, MODEL_NAME, MODEL_TEMPERATURE, MODEL_MAX_OUTPUT_TOKENS


class LLMModel:
    """
    Handles the LLM integration for generating replies.
    """
    
    def __init__(self):
        """Initialize the LLM model."""
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            google_api_key=GEMINI_API_KEY,
            temperature=MODEL_TEMPERATURE,
            max_output_tokens=MODEL_MAX_OUTPUT_TOKENS,
        )
    
    async def generate_response(self, prompt_message, system_prompt=None):
        """
        Generate a response from the LLM using the provided prompts.
        
        Args:
            prompt_message (str): The main prompt message to send to the LLM
            system_prompt (str, optional): The system prompt to use for context
            
        Returns:
            str: The generated response
        """
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        # Add the main prompt
        messages.append(HumanMessage(content=prompt_message))
        
        try:
            # Get response from the model
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            # Log the error and return a fallback message
            print(f"Error generating response: {e}")
            return "I couldn't generate a proper response at this time."


# Create a singleton instance of the LLM model
llm_model = LLMModel()