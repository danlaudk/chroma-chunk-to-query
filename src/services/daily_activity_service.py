"""
Service for extracting daily activities from a transcript using DSPy Predict
and saving the result to a file corresponding to the transcript file.
"""

from pathlib import Path

import dspy
from pydantic import BaseModel


class DailyActivitiesSignature(dspy.Signature):
    """Extract concise daily activities from a transcript.

    transcript_text: The full transcript content to analyze.
    activities: A concise, comma-separated list of daily activities only. No prose.
    """

    transcript_text = dspy.InputField()
    activities = dspy.OutputField(desc=(
        "Comma-separated activities only (e.g., 'make coffee, go to work')."
        " No explanations, no bullets, no extra text."
    ))


class DailyActivityExtractorService(BaseModel):
    """Wraps DSPy's Predict to extract activities and write them to disk."""

    def _predict(self) -> dspy.Predict:
        # Uses globally configured LM (configured elsewhere via initialize_dspy)
        return dspy.Predict(DailyActivitiesSignature)

    def extract_and_save(self, transcript_path: str) -> str:
        """Extract activities from the given transcript and save alongside it.

        Returns the exact string written to the file.
        """
        transcript_file = Path(transcript_path)
        if not transcript_file.exists() or not transcript_file.is_file():
            raise FileNotFoundError(f"Transcript not found: {transcript_file}")

        transcript_text = transcript_file.read_text(encoding="utf-8")

        predictor = self._predict()
        result = predictor(transcript_text=transcript_text)
        activities: str = (result.activities or "").strip()

        # Derive output path: <name>.activities.txt next to transcript
        out_path = transcript_file.with_suffix(transcript_file.suffix + ".activities.txt")
        out_path.write_text(activities + ("\n" if not activities.endswith("\n") else ""), encoding="utf-8")

        return activities


