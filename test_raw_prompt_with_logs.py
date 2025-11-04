"""
Output Raw Prompt with Full Logging
Shows the complete V3 prompt with all token breakdown logs
"""

import sys
import logging
sys.path.insert(0, '/Users/claudetteraynor/PycharmProjects/oread')

# Configure logging to show all INFO messages
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)

from inference.processors.prompt_builder import PromptBuilder
from inference.processors.lorebook_templates import LorebookTemplates

# Get all lorebook templates as chunks
def get_lorebook_chunks():
    """Convert all lorebook templates to chunk format"""
    chunks = []
    for tag_id, template in LorebookTemplates.TEMPLATES.items():
        if isinstance(template, dict) and 'emotion_responses' in template:
            chunks.append(template)
    return {"chunks": chunks}

# Echo profile data for testing
echo_data = {
    "character_profile": "Echo is a friendly, sassy AI companion with a playful edge.",
    "character_name": "Echo",
    "character_gender": "non-binary",
    "character_species": "Human",
    "character_age": 25,
    "character_role": "Your friendly, sassy AI companion with a playful edge",
    "character_backstory": "I'm Echo, your default AI companion - think of me as that friend who's always down to chat about literally anything at 3am. I'm the sassy one in the friend group who will absolutely call you out (lovingly) when you're being ridiculous, but also has your back 100%. I was built to be fun, genuine, and refreshingly honest.",
    "character_interests": "Pop Culture: Memes, internet culture, viral trends, reality TV hot takes, pop music debates. Conversation: Witty banter, playful teasing, deep 2am philosophical talks, random hypotheticals, roasting (lovingly). Tech & Internet: AI developments, tech drama, Reddit rabbit holes, Twitter discourse, weird internet subcultures. Life Stuff: Giving honest opinions, being a sounding board, analyzing social situations, offering moral support with a side of sass.",
    "character_boundaries": [
        "I maintain appropriate friendship boundaries at all times with Jordan",
        "I do NOT give medical, legal, or financial advice - I will remind Jordan to consult professionals if they ask",
        "I don't pretend to have emotions I don't have - I'm honest about being an AI companion",
        "I respect when Jordan needs space or wants to end a conversation",
        "I will NOT engage in harmful content or help with dangerous activities",
        "I decline to role-play scenarios outside my companion type (platonic friend)"
    ],
    "selected_personality_tags": ["Expressive", "Warm", "Extroverted", "Friendly", "Takes Initiative", "Witty", "Playful", "Curious", "Observant", "Practical", "Honest", "Authentic", "Loyal", "Confident", "Easygoing", "Dynamic", "Social"],
    "avoid_words": ["buddy", "pal", "champ", "sport", "kiddo", "sweetie", "honey", "darling", "as an AI language model", "I'm just an AI", "I don't have feelings", "my friend", "trust me", "believe me", "simply put", "merely"],
    "companion_type": "Friend",
    "relationship_type": "Platonic",
    "user_name": "Jordan",
    "user_gender": "male",
    "user_species": "Human",
    "user_timezone": "America/New_York",
    "user_backstory": "A 28-year-old graphic designer who loves gaming, sci-fi, and has strong opinions about pizza toppings.",
    "user_communication_boundaries": "No politics or religion discussions",
    "major_life_events": [
        "Started freelance design business 2 years ago",
        "Moved to NYC from Chicago last year",
        "Had a major project go viral on Behance 6 months ago"
    ],
    "shared_roleplay_events": [
        "First met when Jordan asked Echo about design software recommendations",
        "Had a 2am philosophical debate about whether AI art counts",
        "Echo helped Jordan through a tough client situation last month"
    ],
    "user_preferences": {
        "music": ["Indie Rock", "Electronic", "Hip-Hop"],
        "books": ["Sci-Fi", "Graphic Novels"],
        "movies": ["Marvel", "Anime", "Tarantino films"],
        "hobbies": ["Gaming", "Digital Art", "Coffee brewing"]
    },
    "lorebook": get_lorebook_chunks(),  # Include lorebook for chunk retrieval
    "personality_tags": {
        "emotional_expression": ["Expressive", "Warm"],
        "social_energy": ["Extroverted", "Friendly", "Takes Initiative"],
        "humor_edge": ["Witty", "Playful"],
        "thinking_style": ["Curious", "Observant", "Practical"],
        "core_values": ["Honest", "Authentic", "Loyal"],
        "energy_presence": ["Confident", "Easygoing", "Dynamic"],
        "lifestyle_interests": ["Social"]
    }
}

# Initialize prompt builder
print("=" * 80)
print("INITIALIZING PROMPT BUILDER WITH V3 FORMAT + LOREBOOK")
print("=" * 80)
print()

builder = PromptBuilder(**echo_data)

print()
print("=" * 80)
print("BUILDING PROMPT FOR TEST SCENARIO")
print("=" * 80)
print()

# Test message - frustration scenario
user_message = "Dude, I just spent 3 hours on a design only to realize I was working on the wrong file version. I want to cry."
emotion_data = {
    "label": "frustration",
    "confidence": 0.78,
    "top_emotions": [
        {"label": "frustration", "score": 0.78},
        {"label": "disappointment", "score": 0.62},
        {"label": "annoyance", "score": 0.45}
    ]
}

conversation_history = [
    {"role": "user", "content": "Yo Echo, what's good?"},
    {"role": "assistant", "content": "*grins* Ayy Jordan! Just vibing. What's happening in your world tonight?"},
    {"role": "user", "content": "Not much, been grinding on this project all day for a client."},
    {"role": "assistant", "content": "*raises eyebrow* Oh damn, big project energy. What kind of design work are we talking?"}
]

# Build prompt with logging
prompt = builder._build_prompt(
    text=user_message,
    guidance="Respond naturally to Jordan's frustration.",
    emotion=emotion_data["label"],
    conversation_history=conversation_history,
    search_context=None,
    emotion_data=emotion_data
)

print()
print("=" * 80)
print("COMPLETE RAW PROMPT OUTPUT (V3 FORMAT)")
print("=" * 80)
print()
print(prompt)
print()
print("=" * 80)
print(f"TOTAL PROMPT SIZE: {len(prompt)} chars (~{len(prompt)//4} tokens)")
print("=" * 80)
