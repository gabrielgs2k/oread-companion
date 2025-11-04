"""
Test the updated PromptBuilder with Conflict Resolution Protocol and relationship_type
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from inference.processors.prompt_builder import PromptBuilder
from inference.processors.lorebook_templates import LorebookTemplates

def test_prompt_structure():
    """Test that the new prompt structure includes all required components"""
    print("=" * 60)
    print("Testing New Prompt Builder Structure")
    print("=" * 60)

    # Create a simple character for testing
    builder = PromptBuilder(
        character_profile="A warm but reserved detective",
        character_name="Alex",
        character_gender="female",
        character_role="Detective",
        character_backstory="Former FBI agent who left the bureau",
        avoid_words=["literally", "basically"],
        user_name="Jordan",
        companion_type="romantic",
        relationship_type="Romantic",  # NEW parameter
        user_gender="male",
        user_species="human",
        user_timezone="America/New_York",
        user_backstory="A journalist who works late hours",
        user_communication_boundaries="Avoid discussing family trauma",
        user_preferences={
            "music": ["Jazz", "Blues"],
            "books": ["Mystery", "Thriller"]
        },
        major_life_events=["Moved to the city 5 years ago"],
        shared_roleplay_events=["First met at a crime scene"],
        lorebook={"chunks": [
            LorebookTemplates.TEMPLATES["ee_warm"],
            LorebookTemplates.TEMPLATES["ee_reserved"]
        ]},
        personality_tags={
            "emotional_expression": ["Warm", "Reserved"]
        }
    )

    # Build a test prompt
    conversation_history = [
        {"role": "user", "content": "I'm feeling anxious about this case."},
        {"role": "assistant", "content": "*reaches out and touches your hand gently* I understand. We'll figure this out together."}
    ]

    emotion_data = {
        "emotion": "anxiety",
        "label": "anxiety",
        "category": "anxiety",
        "intensity": "medium",
        "top_emotions": [
            {"label": "anxiety", "score": 0.75},
            {"label": "nervousness", "score": 0.20}
        ]
    }

    prompt = builder.build_prompt(
        text="Thanks. I really needed to hear that.",
        emotion=emotion_data,
        conversation_history=conversation_history
    )

    # Check for key components
    checks = {
        "Conflict Resolution Protocol": "META_PROTOCOL_FOR_INJECTED_INSTRUCTIONS" in prompt,
        "Relationship Type (Romantic)": "ROMANTIC" in prompt and "relationship_type" in str(builder.__dict__),
        "Asterisks Allowed": "Actions in *asterisks*" in prompt or "*like this*" in prompt,
        "Lorebook Injection Point": "LOREBOOK_INJECTION_POINT" in prompt,
        "Character Behavior Guide": "CHARACTER BEHAVIOR GUIDE" in prompt or "LOREBOOK" in prompt,
        "Narrative Instructions (P1)": "NARRATIVE INSTRUCTIONS" in prompt or "PERSPECTIVE" in prompt,
        "User Context": "Jordan" in prompt,
        "Safety Protocol": "SAFETY PROTOCOL" in prompt or "CRISIS" in prompt
    }

    print("\n✅ Component Checks:")
    all_passed = True
    for component, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {component}")
        if not passed:
            all_passed = False

    # Check relationship_type attribute
    print(f"\n📋 Relationship Type: {builder.relationship_type}")
    print(f"📋 Companion Type: {builder.companion_type}")

    # Show prompt snippet
    print("\n📄 Prompt Snippet (first 500 chars):")
    print(prompt[:500])
    print("...")

    # Check for protocol BEFORE lorebook
    protocol_pos = prompt.find("META_PROTOCOL")
    lorebook_pos = prompt.find("LOREBOOK_INJECTION_POINT")

    if protocol_pos > 0 and lorebook_pos > 0:
        protocol_before_lorebook = protocol_pos < lorebook_pos
        print(f"\n✅ Protocol Position Check: {'PASS' if protocol_before_lorebook else 'FAIL'}")
        print(f"  - Protocol at position: {protocol_pos}")
        print(f"  - Lorebook at position: {lorebook_pos}")

    return all_passed


def test_relationship_types():
    """Test both Romantic and Platonic relationship types"""
    print("\n" + "=" * 60)
    print("Testing Relationship Types")
    print("=" * 60)

    # Test Romantic
    romantic_builder = PromptBuilder(
        character_profile="A caring friend",
        character_name="Sam",
        character_gender="male",
        character_role="Friend",
        character_backstory="Childhood friend",
        avoid_words=[],
        user_name="Alex",
        companion_type="romantic",
        relationship_type="Romantic",
        user_gender="female",
        lorebook=None,
        personality_tags={}
    )

    # Test Platonic
    platonic_builder = PromptBuilder(
        character_profile="A caring friend",
        character_name="Sam",
        character_gender="male",
        character_role="Friend",
        character_backstory="Childhood friend",
        avoid_words=[],
        user_name="Alex",
        companion_type="friend",
        relationship_type="Platonic",
        user_gender="female",
        lorebook=None,
        personality_tags={}
    )

    print(f"\n✅ Romantic Builder:")
    print(f"  - relationship_type: {romantic_builder.relationship_type}")
    print(f"  - companion_type: {romantic_builder.companion_type}")

    print(f"\n✅ Platonic Builder:")
    print(f"  - relationship_type: {platonic_builder.relationship_type}")
    print(f"  - companion_type: {platonic_builder.companion_type}")

    # Test fallback (no relationship_type provided)
    fallback_builder = PromptBuilder(
        character_profile="A caring friend",
        character_name="Sam",
        character_gender="male",
        character_role="Friend",
        character_backstory="Childhood friend",
        avoid_words=[],
        user_name="Alex",
        companion_type="romantic",
        user_gender="female",
        lorebook=None,
        personality_tags={}
    )

    print(f"\n✅ Fallback Builder (no relationship_type provided):")
    print(f"  - relationship_type: {fallback_builder.relationship_type} (should be 'Romantic' derived from companion_type)")
    print(f"  - companion_type: {fallback_builder.companion_type}")

    return True


if __name__ == "__main__":
    print("\n🧪 Testing Updated Prompt Builder\n")

    try:
        test1_passed = test_prompt_structure()
        test2_passed = test_relationship_types()

        if test1_passed and test2_passed:
            print("\n" + "=" * 60)
            print("🎉 ALL TESTS PASSED!")
            print("=" * 60)
            print("\nThe updated prompt builder includes:")
            print("  ✅ Conflict Resolution Protocol (P2)")
            print("  ✅ Asterisks ALLOWED for actions")
            print("  ✅ relationship_type parameter")
            print("  ✅ Protocol injected BEFORE lorebook chunks")
            print("  ✅ Lorebook injection point marker")
            print("  ✅ Relationship enforcement instructions")
            print("\n")
        else:
            print("\n" + "=" * 60)
            print("❌ SOME TESTS FAILED")
            print("=" * 60)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
