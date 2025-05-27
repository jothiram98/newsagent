from fastapi import FastAPI, UploadFile, File
from typing import List
import pandas as pd
import json
from src.newsagentpipeline import process_batch

app = FastAPI()

@app.post("/summarize/")
async def summarize_news(file: UploadFile = File(...)):
    # Read uploaded CSV file into pandas DataFrame
    df = pd.read_csv(file.file)
    if "Article" not in df.columns:
        return {"error": "CSV must contain an 'Article' column."}
    articles = df["Article"].tolist()
    output = process_batch(articles)
    return output