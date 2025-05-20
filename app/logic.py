"""
Business logic for generating social media replies.
"""
import json
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from app.model import llm_model
from app.db.database import Database


async def analyze_post(platform: str, post_text: str) -> Dict[str, Any]:
    """
    Analyze a social media post to understand intent, sentiment, and topics.
    
    Args:
        platform: Social media platform
        post_text: Text of the post
        
    Returns:
        Dictionary containing analysis results
    """
    analyzer_prompt = f"""
    Analyze this social media post from {platform.upper()}:
    
    "{post_text}"
    
    Determine:
    1. Core intent (question, statement, complaint, request, etc.)
    2. Emotional tone (happy, frustrated, neutral, excited, etc.)
    3. Key topics mentioned (list the main 1-3 topics)
    4. Expected response type (information, sympathy, engagement, etc.)
    
    Format your response as JSON with these keys: "intent", "sentiment", "topics" (as a list), "response_type".
    Only include the JSON in your response, nothing else.
    """
    
    system_prompt = "You are an expert in social media communication analysis."
    
    analysis_text = await llm_model.generate_response(analyzer_prompt, system_prompt)
    
    # Extract JSON if needed
    try:
        if "```json" in analysis_text:
            analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
        elif "```" in analysis_text:
            analysis_text = analysis_text.split("```")[1].split("```")[0].strip()
            
        analysis_data = json.loads(analysis_text)
        
        # Ensure all keys are present
        required_keys = ["intent", "sentiment", "topics", "response_type"]
        for key in required_keys:
            if key not in analysis_data:
                analysis_data[key] = "unknown"
                
        # Ensure topics is a list
        if not isinstance(analysis_data["topics"], list):
            analysis_data["topics"] = [analysis_data["topics"]]
            
        return analysis_data
        
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing analysis: {e}")
        # Fallback result
        return {
            "intent": "unknown",
            "sentiment": "neutral",
            "topics": ["general"],
            "response_type": "engagement"
        }


async def determine_strategy(
    platform: str, post_text: str, analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Determine the strategy for crafting a response.
    
    Args:
        platform: Social media platform
        post_text: Text of the post
        analysis: Analysis results
        
    Returns:
        Dictionary containing the strategy
    """
    strategy_prompt = f"""
    Given this analysis of a {platform.upper()} post:
    
    Post: "{post_text}"
    
    Analysis:
    - Intent: {analysis["intent"]}
    - Sentiment: {analysis["sentiment"]}
    - Topics: {', '.join(analysis["topics"])}
    - Expected response type: {analysis["response_type"]}
    
    Develop a strategy for a natural, human-like response that:
    1. Addresses the core intent
    2. Matches or appropriately responds to the emotional tone
    3. Feels authentic to {platform.upper()}'s communication style
    4. Avoids typical AI patterns (excessive formality, generic statements)
    
    Provide your strategy in JSON format with these keys:
    - "strategy_summary" (1-2 sentences)
    - "considerations" (list of 2-3 points)
    
    Only include the JSON in your response, nothing else.
    """
    
    # Platform-specific system prompts
    platform_prompts = {
        "twitter": "You are an expert in crafting authentic tweets and replies.",
        "linkedin": "You are an expert in professional LinkedIn communication.",
        "instagram": "You are an expert in Instagram communication style.",
        "facebook": "You are an expert in Facebook engagement.",
        "reddit": "You are an expert in Reddit-style communication."
    }
    
    system_prompt = platform_prompts.get(
        platform.lower(), 
        "You are an expert in social media communication."
    )
    
    strategy_text = await llm_model.generate_response(strategy_prompt, system_prompt)
    
    # Parse the response
    try:
        if "```json" in strategy_text:
            strategy_text = strategy_text.split("```json")[1].split("```")[0].strip()
        elif "```" in strategy_text:
            strategy_text = strategy_text.split("```")[1].split("```")[0].strip()
            
        strategy_data = json.loads(strategy_text)
        
        # Ensure required keys
        if "strategy_summary" not in strategy_data:
            strategy_data["strategy_summary"] = "Respond naturally to the post."
        if "considerations" not in strategy_data:
            strategy_data["considerations"] = ["Keep it authentic", "Address the main points"]
            
        return strategy_data
        
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing strategy: {e}")
        # Fallback strategy
        return {
            "strategy_summary": "Respond naturally to the post.",
            "considerations": ["Keep it authentic", "Address the main points"]
        }


async def generate_platform_reply(
    platform: str, 
    post_text: str, 
    analysis: Dict[str, Any], 
    strategy: Dict[str, Any]
) -> str:
    """
    Generate the final reply based on platform, analysis, and strategy.
    
    Args:
        platform: Social media platform
        post_text: Text of the post
        analysis: Analysis results
        strategy: Response strategy
        
    Returns:
        Generated reply text
    """
    # Platform-specific characteristics
    platform_characteristics = {
        "twitter": "brief (under 280 chars), conversational, often using hashtags, casual language",
        "linkedin": "professional but personable, thoughtful, industry-focused",
        "instagram": "visual-focused references, emoji-rich, positive, brief",
        "facebook": "personal, conversational, community-oriented, varied length",
        "reddit": "topic-focused, can reference subreddit culture, varying formality"
    }
    
    platform_style = platform_characteristics.get(
        platform.lower(), 
        "conversational, authentic, human-like"
    )
    
    considerations = ", ".join(strategy.get("considerations", ["Be authentic"]))
    
    generator_prompt = f"""
    Write a reply to this {platform.upper()} post:
    
    "{post_text}"
    
    Strategy: {strategy.get("strategy_summary", "Respond naturally")}
    
    Important considerations: {considerations}
    
    Your reply should:
    - Match {platform.upper()} style: {platform_style}
    - Sound like a real {platform.upper()} user (not an AI)
    - Respond to the post's intent ({analysis.get("intent")}) and tone ({analysis.get("sentiment")})
    - Be about the topics: {', '.join(analysis.get("topics", ["general"]))}
    - Provide a {analysis.get("response_type", "general")} type of response
    - Include natural human writing elements (conversational phrases, appropriate informality)
    - Avoid sounding too perfect, formal, or generic
    
    Write ONLY the reply text itself. Do not include explanations or analysis.
    """
    
    system_prompt = f"You are a regular {platform} user having a natural conversation. Write replies that sound like a real person, not an AI."
    
    reply_text = await llm_model.generate_response(generator_prompt, system_prompt)
    
    # Clean up the response to ensure it's just the reply
    reply_text = reply_text.strip()
    
    # Remove any explanatory text that might appear
    prefixes_to_remove = [
        "Reply:", "Here's my reply:", "Here is my reply:", 
        "Here's a reply:", "Here is a reply:"
    ]
    
    for prefix in prefixes_to_remove:
        if reply_text.startswith(prefix):
            reply_text = reply_text[len(prefix):].strip()
    
    return reply_text


async def generate_reply(
    platform: str, 
    post_text: str, 
    context: Optional[str] = None,
    include_analysis: bool = False
) -> Dict[str, Any]:
    """
    Main function to generate a human-like reply using a multi-stage approach.
    
    Args:
        platform: Social media platform
        post_text: Text of the post
        context: Optional additional context
        include_analysis: Whether to include analysis in the result
        
    Returns:
        Dictionary containing the reply and metadata
    """
    # Step 1: Analyze the post
    start_time = datetime.now(timezone.utc)
    analysis = await analyze_post(platform, post_text)
    print(f"Post analysis: {analysis}")
    print("\n")
    # Step 2: Determine response strategy
    strategy = await determine_strategy(platform, post_text, analysis)
    
    print(f"Response strategy: {strategy}")
    print("\n")
    # Step 3: Generate the actual reply
    reply_text = await generate_platform_reply(
        platform, post_text, analysis, strategy
    )
    print(f"Generated reply: {reply_text}")
    print("\n")
    # Prepare the complete response
    elapsed_time = (datetime.now(timezone.utc) - start_time).total_seconds()
    
    result = {
        "reply_text": reply_text,
        "platform": platform,
        "post_text": post_text,
        "created_at": datetime.now(timezone.utc),
        "metadata": {
            "generation_time": elapsed_time,
            "strategy": strategy.get("strategy_summary"),
            "model": "Google Gemini"
        }
    }
    
    # Include analysis if requested
    if include_analysis:
        result["analysis"] = analysis
    
    # Store in database (don't await, let it happen in background)
    await Database.store_reply(result)
    
    return result