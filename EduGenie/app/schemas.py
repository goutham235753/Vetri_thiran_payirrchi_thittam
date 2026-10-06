from pydantic import BaseModel, Field

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
class TopicRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=1000)
class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)
class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str = ""
class QuizResponse(BaseModel):
    topic: str
    questions: list[QuizQuestion] = Field(min_length=1, max_length=3)
class TextResponse(BaseModel):
    result: str
class HealthResponse(BaseModel):
    status: str
    ai_configured: bool
    demo_mode: bool
