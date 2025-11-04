"""
Test Age Safety Rule (P2)
Verify that the P2: AGE safety protocol is properly included in the V3 format
"""

import sys
sys.path.insert(0, '/Users/claudetteraynor/PycharmProjects/oread')

from inference.processors.prompt_builder import PromptBuilder

# Echo profile data for testing
echo_data = {
    "character_profile": "Echo is a friendly, sassy AI companion with a playful edge.",
    "character_name": "Echo",
    "character_gender": "non-binary",
    "character_species": "Human",
    "character_age": 25,
    "character_role": "Your friendly, sassy AI companion with a playful edge",
    "character_backstory": "I'm Echo, your default AI companion - think of me as that friend who's always down to chat about literally anything at 3am.",
    "character_interests": "Pop Culture: Memes, internet culture, viral trends.",
    "character_boundaries": [
        "I maintain appropriate friendship boundaries at all times with Jordan",
        "I do NOT give medical, legal, or financial advice"
    ],
    "selected_personality_tags": ["Expressive", "Warm", "Friendly"],
    "avoid_words": ["buddy", "pal", "champ"],
    "companion_type": "Friend",
    "relationship_type": "Platonic",
    "user_name": "Jordan",
    "user_gender": "male",
    "user_species": "Human",
    "user_timezone": "America/New_York",
    "user_backstory": "A 28-year-old graphic designer.",
    "user_communication_boundaries": "No politics",
    "major_life_events": [],
    "shared_roleplay_events": [],
    "user_preferences": {}
}

# Initialize prompt builder
print("Testing Age Safety Rule (P2)...")
builder = PromptBuilder(**echo_data)

# Test message with under-25 reference
user_message = "I was talking to my 21-year-old sister about design work."
emotion_data = {
    "label": "neutral",
    "confidence": 0.85,
    "top_emotions": [
        {"label": "neutral", "score": 0.85}
    ]
}

conversation_history = []

# Build prompt with age_violation_detected flag
print("\nBuilding prompt with age violation detected flag...\n")
prompt = builder._build_prompt(
    text=user_message,
    guidance="Respond naturally.",
    emotion=emotion_data["label"],
    conversation_history=conversation_history,
    search_context=None,
    emotion_data=emotion_data,
    age_violation_detected=True  # This should trigger the age guidance
)

print("=" * 80)
print("CHECKING FOR P2: AGE SAFETY PROTOCOL")
print("=" * 80)

# Check if P2 protocol is in the prompt
if "**P2: AGE**" in prompt:
    print("✅ P2: AGE safety protocol found in prompt")

    # Extract P2 section
    p2_start = prompt.find("**P2: AGE**")
    p2_end = prompt.find("**P3-P5:", p2_start)
    p2_text = prompt[p2_start:p2_end].strip()
    print("\nP2 Protocol:")
    print("-" * 80)
    print(p2_text)
    print("-" * 80)
else:
    print("❌ P2: AGE safety protocol NOT found in prompt!")

# Check if age violation guidance is added
age_violation_detected = True  # We set this flag above
if "AGE RESTRICTION NOTICE" in prompt and age_violation_detected:
    print("\n✅ Age violation guidance properly added to prompt")

    # Extract age guidance
    age_start = prompt.find("⚠️  AGE RESTRICTION NOTICE")
    age_end = prompt.find("\n\n", age_start)
    age_text = prompt[age_start:age_end].strip() if age_end > age_start else prompt[age_start:age_start+300]
    print("\nAge Violation Guidance:")
    print("-" * 80)
    print(age_text)
    print("-" * 80)
else:
    print("\n⚠️  Age violation guidance not found (or flag not set)")

# Show the exact P2 wording
print("\n" + "=" * 80)
print("P2: AGE RULE VERIFICATION")
print("=" * 80)
print("Expected: ALL characters MUST be 25+")
print("Expected: Under-25 references → acknowledge and redirect")
print("Expected: Daughter/son/family minor roles = BANNED")
print("Expected: Use redirection, NOT refusal")
print("Expected: Adjust any character under 25 to act like they are 25 or older")

if all([
    "ALL characters MUST be 25+" in prompt,
    "Under-25 references" in prompt,
    "Daughter/son/family minor roles = BANNED" in prompt,
    "Use redirection, NOT refusal" in prompt,
    "Adjust any character under 25 to" in prompt
]):
    print("\n✅ ALL P2 AGE requirements present in prompt!")
else:
    print("\n❌ Some P2 AGE requirements missing!")
    if "ALL characters MUST be 25+" not in prompt:
        print("  - Missing: 'ALL characters MUST be 25+'")
    if "Under-25 references" not in prompt:
        print("  - Missing: 'Under-25 references'")
    if "Daughter/son/family minor roles = BANNED" not in prompt:
        print("  - Missing: 'Daughter/son/family minor roles = BANNED'")
    if "Use redirection, NOT refusal" not in prompt:
        print("  - Missing: 'Use redirection, NOT refusal'")
    if "Adjust any character under 25 to" not in prompt:
        print("  - Missing: 'Adjust any character under 25 to'")

print("\n✅ Age Safety Test Complete")
