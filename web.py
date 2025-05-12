from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from hate.pipeline.train_pipeline import TrainPipeline
from hate.pipeline.prediction_pipeline import PredictionPipeline
from hate.exception import CustomException
from hate.constants import *
import uvicorn
import sys

app = FastAPI()

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load templates from 'templates' directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": "", "input_text": ""})


@app.post("/predict", response_class=HTMLResponse)
async def predict_route(request: Request, text: str = Form(...)):
    try:
        obj = PredictionPipeline()
        result = obj.run_pipeline(text)
        return templates.TemplateResponse("index.html", {"request": request, "result": result, "input_text": text})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "result": f"Error: {str(e)}", "input_text": text})


@app.get("/train", response_class=HTMLResponse)
async def training(request: Request):
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return templates.TemplateResponse("index.html", {"request": request, "result": "Training successful!", "input_text": ""})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "result": f"Training Error: {str(e)}", "input_text": ""})


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
