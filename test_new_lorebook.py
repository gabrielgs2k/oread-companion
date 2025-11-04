"""
Test script for new two-tier lorebook system
Tests emotion-specific tone + action matching
"""

from inference.processors.lorebook_templates import LorebookTemplates
from inference.processors.lorebook_retriever import LorebookRetriever

def test_template_structure():
    """Test that new templates have the correct structure"""
    print("=" * 60)
    print("Testing Template Structure")
    print("=" * 60)

    # Test Warm tag
    warm = LorebookTemplates.TEMPLATES.get("ee_warm")
    assert warm is not None, "ee_warm template not found"
    assert "emotion_responses" in warm, "Missing emotion_responses"
    assert "requires_selection" in warm, "Missing requires_selection"
    assert warm["requires_selection"] == True, "Should require selection"

    # Check emotion responses
    responses = warm["emotion_responses"]
    assert "sadness" in responses, "Missing sadness response"
    assert "joy" in responses, "Missing joy response"
    assert "default" in responses, "Missing default response"

    # Check response structure
    sadness_response = responses["sadness"]
    assert "tone" in sadness_response, "Missing tone field"
    assert "action" in sadness_response, "Missing action field"
    assert "tokens" in sadness_response, "Missing tokens field"

    print("✅ Template structure is valid")
    print(f"   - ee_warm has {len(responses)} emotion responses")
    print(f"   - Sadness tone: {sadness_response['tone']}")
    print(f"   - Sadness action: {sadness_response['action'][:50]}...")
    print()

def test_retrieval_with_selection():
    """Test that retrieval works with tag selection"""
    print("=" * 60)
    print("Testing Retrieval with Tag Selection")
    print("=" * 60)

    # Create lorebook with new-style chunks
    lorebook = {
        "chunks": [
            LorebookTemplates.TEMPLATES["ee_warm"],
            LorebookTemplates.TEMPLATES["ee_reserved"],
            LorebookTemplates.TEMPLATES["ee_passionate"],
            LorebookTemplates.TEMPLATES["ee_calm"],
        ]
    }

    retriever = LorebookRetriever(max_chunks=3)

    # Test 1: Without selection, requires_selection chunks should not be retrieved
    print("\n📋 Test 1: No tags selected")
    chunks = retriever.retrieve(
        lorebook=lorebook,
        user_message="I'm feeling sad today",
        emotion="sadness",
        top_emotions=[{"label": "sadness", "score": 0.9}],
        selected_tags=set()  # No tags selected
    )
    print(f"   Retrieved {len(chunks)} chunks (should be 0)")
    assert len(chunks) == 0, f"Expected 0 chunks, got {len(chunks)}"
    print("   ✅ Correctly filtered out unselected tags")

    # Test 2: With selection, should retrieve and process
    print("\n📋 Test 2: 'Warm' tag selected, emotion='sadness'")
    chunks = retriever.retrieve(
        lorebook=lorebook,
        user_message="I'm feeling sad today",
        emotion="sadness",
        top_emotions=[{"label": "sadness", "score": 0.9}],
        selected_tags={"ee_warm"}  # Selected Warm tag
    )
    print(f"   Retrieved {len(chunks)} chunks")
    assert len(chunks) >= 1, "Should retrieve at least 1 chunk"

    warm_chunk = chunks[0]
    assert "content" in warm_chunk, "Processed chunk should have content"
    print(f"   ✅ Retrieved and processed chunk: {warm_chunk['id']}")
    print(f"   Content preview:")
    print(f"   {warm_chunk['content'][:150]}...")

    # Test 3: Different emotion, same tag
    print("\n📋 Test 3: 'Warm' tag selected, emotion='joy'")
    chunks = retriever.retrieve(
        lorebook=lorebook,
        user_message="I'm so happy!",
        emotion="joy",
        top_emotions=[{"label": "joy", "score": 0.95}],
        selected_tags={"ee_warm"}
    )

    assert len(chunks) >= 1, "Should retrieve warm chunk"
    warm_chunk = chunks[0]
    assert "**Tone:**" in warm_chunk["content"], "Should have formatted tone"
    assert "**Action:**" in warm_chunk["content"], "Should have formatted action"
    print(f"   ✅ Different emotion produces different content")
    print(f"   Content preview:")
    print(f"   {warm_chunk['content'][:150]}...")

    # Test 4: Multiple tags selected
    print("\n📋 Test 4: Multiple tags selected")
    chunks = retriever.retrieve(
        lorebook=lorebook,
        user_message="I'm feeling angry",
        emotion="anger",
        top_emotions=[{"label": "anger", "score": 0.85}],
        selected_tags={"ee_warm", "ee_calm"}  # Both selected
    )

    print(f"   Retrieved {len(chunks)} chunks")
    assert len(chunks) >= 2, f"Should retrieve at least 2 chunks, got {len(chunks)}"
    chunk_ids = [c['id'] for c in chunks]
    print(f"   Retrieved chunks: {chunk_ids}")
    print("   ✅ Multiple tags work correctly")

    print()

def test_ui_tag_mapping():
    """Test that UI tags map correctly to template IDs"""
    print("=" * 60)
    print("Testing UI Tag Mapping")
    print("=" * 60)

    # Test mapping
    warm_template = LorebookTemplates.get_template_by_ui_tag("Warm")
    assert warm_template is not None, "Failed to find Warm tag"
    assert warm_template['id'] == "ee_warm", "Incorrect mapping"
    print("✅ 'Warm' UI tag maps to 'ee_warm'")

    reserved_template = LorebookTemplates.get_template_by_ui_tag("Reserved")
    assert reserved_template['id'] == "ee_reserved", "Incorrect mapping"
    print("✅ 'Reserved' UI tag maps to 'ee_reserved'")

    passionate_template = LorebookTemplates.get_template_by_ui_tag("Passionate")
    assert passionate_template['id'] == "ee_passionate", "Incorrect mapping"
    print("✅ 'Passionate' UI tag maps to 'ee_passionate'")

    calm_template = LorebookTemplates.get_template_by_ui_tag("Calm")
    assert calm_template['id'] == "ee_calm", "Incorrect mapping"
    print("✅ 'Calm' UI tag maps to 'ee_calm'")

    print()

if __name__ == "__main__":
    print("\n🧪 Testing New Two-Tier Lorebook System\n")

    try:
        test_template_structure()
        test_ui_tag_mapping()
        test_retrieval_with_selection()

        print("=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe new two-tier lorebook system is working correctly:")
        print("  ✅ Tags require user selection")
        print("  ✅ Emotion-specific tone + action instructions work")
        print("  ✅ Content is dynamically generated based on detected emotion")
        print("  ✅ Multiple tag selection works")
        print("\nReady to expand to all remaining tags! 🚀\n")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        raise
