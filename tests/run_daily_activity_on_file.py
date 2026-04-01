"""
Run DailyActivityExtractorService on a specific transcript path.

Usage:
  python tests/run_daily_activity_on_file.py

Optionally set ALT_LLM_MODEL_NAME to choose a model config from JSON.
"""

import os
import sys
from pathlib import Path



def main() -> None:

    from src.models.llm_model import initialize_dspy
    from src.services.daily_activity_service import DailyActivityExtractorService
    from src.services.synthetic_qus_service import SyntheticQusService
    
    transcript_path = \
        "/Users/dlau/repos/batch-yt/transcripts/daily_activities/context_synth_qus.txt"
        # "/Users/dlau/repos/batch-yt/transcripts/daily_activities/ten_activities_three_lines.txt"

    model_name = "z-ai" # os.getenv("ALT_LLM_MODEL_NAME")
    initialize_dspy(model_name=model_name)

    # service = DailyActivityExtractorService()
    service = SyntheticQusService()
    activities = service.extract_and_save(transcript_path)

    out_path = Path(transcript_path).with_suffix(Path(transcript_path).suffix + ".activities.txt")

    print("Input transcript:", transcript_path)
    print("Output file:", str(out_path))
    print("Activities (comma-separated):", activities)


if __name__ == "__main__":
    main()


