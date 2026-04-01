"""
Service for extracting daily activities from a transcript using DSPy Predict
and saving the result to a file corresponding to the transcript file.
"""

from pathlib import Path

import dspy
from pydantic import BaseModel


class SyntheticQusSignature(dspy.Signature):
    """Extract concise daily activities from a transcript.

    transcript_text: The full transcript content to analyze.
    questions: diverse synthetic questions followed only by the actual moderator's question.
    """

    transcript_text = dspy.InputField()
    questions = dspy.OutputField(desc=(
        "Questions in German then moderator's question, verbatim"
        "Per moderator and interviewee chunk, Five Synthetic questions in German motivating the chunk, followed only by the actual moderator's question."
        " Make the questions in the moment and as if they were a part of a potential dialogue, but in lay language. Each set of five quetsions should be inspired from diverse situations in regular life"
    ))


class SyntheticQusService(BaseModel):
    """Wraps DSPy's Predict to extract activities and write them to disk."""

    def _predict(self) -> dspy.Predict:
        # Uses globally configured LM (configured elsewhere via initialize_dspy)
        return dspy.Predict(SyntheticQusSignature)

    def extract_and_save(self, transcript_path: str) -> str:
        # """Extract activities from the given transcript and save alongside it.
        """create synthetic questions from the transcript , and save alongside it.

        Returns the exact string written to the file.
        """
        transcript_file = Path(transcript_path)
        if not transcript_file.exists() or not transcript_file.is_file():
            raise FileNotFoundError(f"Transcript not found: {transcript_file}")

        transcript_text = transcript_file.read_text(encoding="utf-8")

        predictor = self._predict()
        result = predictor(transcript_text=transcript_text)
        activities: str = (result.questions or "").strip()

        # Derive output path: <name>.activities.txt next to transcript
        out_path = transcript_file.with_suffix(transcript_file.suffix + ".activities.txt")
        out_path.write_text(activities + ("\n" if not activities.endswith("\n") else ""), encoding="utf-8")

        return activities


