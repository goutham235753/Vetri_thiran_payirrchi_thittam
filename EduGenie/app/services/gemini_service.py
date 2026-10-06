import json
import re
from typing import Any
from google import genai
from google.genai import types
from app.config import Settings

class GeminiService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = genai.Client(api_key=settings.gemini_api_key) if settings.gemini_api_key else None

    def _ensure_available(self):
        if self.settings.demo_mode:
            return
        if self.client is None:
            raise RuntimeError("GEMINI_API_KEY is not configured. Add it to .env or enable DEMO_MODE=true.")

    def _generate(self, prompt: str, temperature: float = 0.4) -> str:
        self._ensure_available()
        if self.settings.demo_mode:
            return "Demo mode is enabled. Add a Gemini API key for real AI responses."
        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=temperature, max_output_tokens=2048),
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()

    def qna(self, question: str) -> str:
        prompt = f"""You are EduGenie, a friendly educational assistant. Answer the student's question accurately and concisely. Use simple language, define technical terms briefly, and use short examples when useful. Do not invent sources or claim certainty when uncertain.\n\nStudent question:\n{question}"""
        return f"[DEMO] Answer for: {question}" if self.settings.demo_mode else self._generate(prompt, 0.3)

    def explain(self, topic: str) -> str:
        prompt = f"""Explain the following topic for a student. Start with a one-sentence definition, then give a simple explanation, a small example or analogy, and 3 key points. Keep the wording easy to understand.\n\nTopic:\n{topic}"""
        return f"[DEMO] Simple explanation of {topic}." if self.settings.demo_mode else self._generate(prompt, 0.35)

    def summarize(self, text: str) -> str:
        prompt = f"""Summarize the following educational text in simple language. Keep important facts and remove repetition. Return 5-8 concise bullet points followed by a one-sentence revision summary.\n\nText:\n{text}"""
        return "[DEMO] Summary: " + text[:300] if self.settings.demo_mode else self._generate(prompt, 0.25)

    @staticmethod
    def _extract_json(text: str) -> Any:
        cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.I)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}|\[.*\]", cleaned, flags=re.S)
            if not match:
                raise RuntimeError("Gemini did not return valid quiz JSON.")
            return json.loads(match.group(0))

    def quiz(self, topic_or_text: str) -> dict[str, Any]:
        prompt = f"""Create exactly 3 multiple-choice questions for a student from the material below. Each question must have exactly 4 options and exactly one correct answer. The correct_answer must exactly match one option. Add a short explanation. Return ONLY valid JSON: {{\"questions\":[{{\"question\":\"...\",\"options\":[\"...\",\"...\",\"...\",\"...\"],\"correct_answer\":\"...\",\"explanation\":\"...\"}}]}}\n\nMaterial:\n{topic_or_text}"""
        if self.settings.demo_mode:
            return {"questions": [
                {"question":"Which learning activity does EduGenie support?","options":["Quiz generation","Cooking","Banking","Gaming only"],"correct_answer":"Quiz generation","explanation":"Quiz generation is one of EduGenie's documented features."},
                {"question":"Which backend framework is used by EduGenie?","options":["FastAPI","Django","Rails","Laravel"],"correct_answer":"FastAPI","explanation":"The supplied project documentation specifies FastAPI."},
                {"question":"Which model family powers the assistant?","options":["Gemini","Word2Vec","BERT only","SVM"],"correct_answer":"Gemini","explanation":"EduGenie is designed around Google's Gemini generative AI."}
            ]}
        data = self._extract_json(self._generate(prompt, 0.5))
        questions = data.get("questions") if isinstance(data, dict) else data
        if not isinstance(questions, list) or len(questions) != 3:
            raise RuntimeError("Quiz response must contain exactly 3 questions.")
        normalized=[]
        for q in questions:
            options=q.get("options", []); answer=q.get("correct_answer", "")
            if len(options)!=4 or answer not in options:
                raise RuntimeError("Quiz response contains invalid options/correct answer.")
            normalized.append({"question":str(q.get("question","")),"options":[str(x) for x in options],"correct_answer":str(answer),"explanation":str(q.get("explanation",""))})
        return {"questions":normalized}

    def learning_path(self, topic: str) -> str:
        prompt = f"""Create a personalized learning path for {topic}. Organize it from beginner to intermediate to advanced. For each level include estimated time, key topics, practice activities, and useful types of resources such as documentation, tutorials, books, or practice platforms. End with practical study tips. Keep it structured and easy to scan."""
        return f"[DEMO] Learning path for {topic}: Beginner → Intermediate → Advanced." if self.settings.demo_mode else self._generate(prompt, 0.45)
