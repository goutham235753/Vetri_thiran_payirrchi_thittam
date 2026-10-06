from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.config import get_settings
from app.schemas import HealthResponse, QuestionRequest, QuizResponse, TextRequest, TextResponse, TopicRequest
from app.services.gemini_service import GeminiService

settings=get_settings(); service=GeminiService(settings); STATIC_DIR=Path(__file__).resolve().parent/"static"
app=FastAPI(title="EduGenie API", description="Google Gemini powered learning assistant.", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=settings.cors_origins!="*", allow_methods=["*"], allow_headers=["*"])
def ai_error(exc): return HTTPException(status_code=502, detail=str(exc))
@app.get("/", include_in_schema=False)
async def index(): return FileResponse(STATIC_DIR/"index.html")
@app.get("/api/health", response_model=HealthResponse)
async def health(): return HealthResponse(status="ok", ai_configured=bool(settings.gemini_api_key), demo_mode=settings.demo_mode)
@app.post("/api/qna", response_model=TextResponse)
async def qna(request: QuestionRequest):
    try: return TextResponse(result=service.qna(request.question))
    except Exception as e: raise ai_error(e)
@app.post("/api/explain", response_model=TextResponse)
async def explain(request: TopicRequest):
    try: return TextResponse(result=service.explain(request.topic))
    except Exception as e: raise ai_error(e)
@app.post("/api/summarize", response_model=TextResponse)
async def summarize(request: TextRequest):
    try: return TextResponse(result=service.summarize(request.text))
    except Exception as e: raise ai_error(e)
@app.post("/api/quiz", response_model=QuizResponse)
async def quiz(request: TextRequest):
    try: return QuizResponse(topic=request.text, questions=service.quiz(request.text)["questions"])
    except Exception as e: raise ai_error(e)
@app.post("/api/learn/recommendations", response_model=TextResponse)
async def recommendations(request: TopicRequest):
    try: return TextResponse(result=service.learning_path(request.topic))
    except Exception as e: raise ai_error(e)
@app.post("/qna", response_model=TextResponse)
async def legacy_qna(request: QuestionRequest): return await qna(request)
@app.post("/explain", response_model=TextResponse)
async def legacy_explain(request: TopicRequest): return await explain(request)
@app.post("/summarize", response_model=TextResponse)
async def legacy_summarize(request: TextRequest): return await summarize(request)
@app.post("/quiz", response_model=QuizResponse)
async def legacy_quiz(request: TextRequest): return await quiz(request)
@app.get("/learn/recommendations", response_model=TextResponse)
async def legacy_recommendations(topic: str=Query(..., min_length=1, max_length=1000)): return await recommendations(TopicRequest(topic=topic))
