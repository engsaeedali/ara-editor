from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.graph import app_graph
from utils.logger_config import setup_logger

logger = setup_logger("main")

app = FastAPI(title="The Linguistic Engineer Agent", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    logger.info(f"Received chat request. Input length: {len(request.message)}")
    # Initial state
    initial_state = {
        "input_text": request.message,
        "current_text": request.message,
        "manuscript": "",
        "editor_notes": [],
        "revision_count": 0,
        "status": "processing",
        # Initialize new fields to avoid key errors if graph fails early
        "memory_context": [],
        "violations": [],
        "metric_scores": {}
    }
    
    try:
        # Run the graph
        logger.info("Invoking agent graph...")
        result = await app_graph.ainvoke(initial_state)
        logger.info("Agent graph execution completed successfully.")
        
        return {
            "manuscript": result.get("manuscript"),
            "editor_notes": result.get("editor_notes"),
            "metric_scores": result.get("metric_scores", {}),
            "violations": result.get("violations", []),
            "token_usage": result.get("token_usage", {}),
            "status": "completed"
        }
    except Exception as e:
        logger.error(f"Error during chat processing: {str(e)}", exc_info=True)
        raise e

from fastapi import File, UploadFile, HTTPException
from processors.document_processor import DocumentProcessor

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    logger.info(f"Received file upload: {file.filename}")
    if not file.filename.endswith(".docx"):
        logger.warning("Invalid file type uploaded.")
        raise HTTPException(status_code=400, detail="Only .docx files are supported")
    
    content = await file.read()
    extracted_text = DocumentProcessor.extract_text_from_docx(content)
    logger.info(f"Extracted {len(extracted_text)} characters from document.")
    
    if not extracted_text:
        raise HTTPException(status_code=400, detail="Could not extract text from document")

    # Run the graph on the extracted text
    initial_state = {
        "input_text": extracted_text,
        "current_text": extracted_text,
        "manuscript": "",
        "editor_notes": [],
        "revision_count": 0,
        "status": "processing",
        "memory_context": [],
        "violations": [],
        "metric_scores": {}
    }
    
    try:
        logger.info("Invoking agent graph for document...")
        result = await app_graph.ainvoke(initial_state)
        logger.info("Agent graph execution for document completed.")
        
        return {
            "manuscript": result.get("manuscript"),
            "editor_notes": result.get("editor_notes"),
            "metric_scores": result.get("metric_scores", {}),
            "violations": result.get("violations", []),
            "token_usage": result.get("token_usage", {}),
            "status": "completed",
            "original_text": extracted_text
        }
    except Exception as e:
        logger.error(f"Error during document processing: {str(e)}", exc_info=True)
        raise e

@app.get("/")
async def root():
    return {"message": "The Linguistic Engineer is Online", "status": "sovereign", "version": "v2"}
