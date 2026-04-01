"""
Runnable test for DailyActivityExtractorService without stubs.
Creates a temporary transcript, runs extraction, verifies output file
exists and contains a clean comma-separated list as per the DSPy signature.
"""

import os
from pathlib import Path
import tempfile

from src.models.llm_model import initialize_dspy
from src.services.daily_activity_service import DailyActivityExtractorService


def _is_clean_comma_separated_list(text: str) -> bool:
    """Validate that text is a clean comma-separated list with no extra prose."""
    if not text:
        return False
    if "\n" in text or "\r" in text:
        return False
    # Basic checks: has at least one comma and no bullet-like characters
    if "," not in text:
        return False
    if any(b in text for b in ("•", "- ", "\t", ";", "::")):
        return False
    items = [item.strip() for item in text.split(",")]
    if any(len(item) == 0 for item in items):
        return False
    return True


def test_daily_activity_extraction():
    print("Testing DailyActivityExtractorService...")

    # Initialize DSPy using model configs (optionally via env ALT_LLM_MODEL_NAME)
    model_name = os.getenv("ALT_LLM_MODEL_NAME")
    llm = initialize_dspy(model_name=model_name)
    print("✓ DSPy initialized")

    # Prepare a temporary transcript file with plausible daily routine mentions
    transcript_text = (
        "I usually wake up around 7am, then I make coffee and check emails. "
        "After that, I go to work, attend meetings, and write code. "
        "In the evening, I exercise, cook dinner, and read before bed."
    )
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tf:
        transcript_path = Path(tf.name)
        tf.write(transcript_text.encode("utf-8"))

    try:
        service = DailyActivityExtractorService()
        activities = service.extract_and_save(str(transcript_path))
        print(f"Activities returned: {activities}")

        # Verify output file exists
        out_path = transcript_path.with_suffix(transcript_path.suffix + ".activities.txt")
        assert out_path.exists() and out_path.is_file(), "Output activities file should exist"
        saved = out_path.read_text(encoding="utf-8").strip()

        # Returned string should match saved content (ignoring trailing newline)
        assert activities.strip() == saved, "Returned activities should equal saved content"

        # Validate clean comma-separated list per signature (no prose, just items)
        assert _is_clean_comma_separated_list(saved), "Saved activities must be a clean comma-separated list"

        # Extra: items should be non-empty after split/strip
        items = [i.strip() for i in saved.split(",")]
        assert all(items), "All list items must be non-empty after stripping"

        print("✓ Daily activity extraction test passed")
    finally:
        # Cleanup temp files
        try:
            transcript_path.unlink(missing_ok=True)
        except Exception:
            pass
        try:
            out_path = transcript_path.with_suffix(transcript_path.suffix + ".activities.txt")
            out_path.unlink(missing_ok=True)
        except Exception:
            pass


if __name__ == "__main__":
    test_daily_activity_extraction()

