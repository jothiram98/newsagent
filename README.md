# NewsAgent

**NewsAgent** is a Python-based Agentic pipeline for processing and summarizing news articles using advanced AI models. It supports both batch processing via a script and real-time summarization via a FastAPI web service.

---

## Project Structure

```
newsagent/
├── app.py
├── dataartifact/
│   └── news_articles.csv
├── src/
│   ├── newsagentpipeline.py
│   └── fastapi_app.py
├── requirements.txt
├── LICENSE
└── README.md
```

---

## How It Works

### 1. Data Input

- The project expects a CSV file (e.g., `news_articles.csv`) in the `dataartifact` folder.
- The CSV must have at least two columns: `S.NO` and `Article`.
- Each article should be wrapped in double quotes to handle commas within the text.

### 2. Processing Pipeline

- The main script (`app.py`) reads the CSV using pandas.
- It extracts the `Article` column as a list.
- This list is passed to the `process_batch` function from `src/newsagentpipeline.py`.
- The pipeline uses AI models (via LangChain and OpenAI) to analyze and summarize each article.
- The output is saved as `Summary.json`.

### 3. FastAPI Integration

- The FastAPI app (`src/fastapi_app.py`) exposes an endpoint to upload a CSV and get summaries as a JSON response.
- This allows you to use the summarization pipeline as a web service.

---

## Flowchart

```bash
+---------------------+
|  news_articles.csv  |
|    (CSV file)       |
+----------+----------+
           |
           v
+---------------------+         +---------------------+
|   app.py (main)     |         |  fastapi_app.py     |
| - Reads CSV         |         |  (FastAPI endpoint) |
| - Extracts articles |         |  /summarize/        |
+----------+----------+         +----------+----------+
           |                              |
           v                              v
+-------------------------------+  +-------------------------------+
| process_batch (pipeline)      |  | process_batch (pipeline)      |
| - AI summarization            |  | - AI summarization            |
| - Sentiment/topic extraction  |  | - Sentiment/topic extraction  |
+----------+--------------------+  +----------+--------------------+
           |                              |
           v                              v
+---------------------+         +---------------------+
|   Summary.json      |         |   JSON Response     |
| (Structured output) |         | (Structured output) |
+---------------------+         +---------------------+
```

---

## Example Usage

### Batch Script

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place your CSV file:**
   - Save your news articles as `news_articles.csv` in the `dataartifact` folder.

3. **Run the pipeline:**
   ```bash
   python app.py
   ```

4. **Check the output:**
   - The results will be saved in `Summary.json`.

---

### FastAPI Web Service

1. **Install dependencies (if not already done):**
   ```bash
   pip install -r requirements.txt
   pip install fastapi uvicorn
   ```

2. **Run the FastAPI server:**
   ```bash
   uvicorn src.fastapi_app:app --reload
   ```

3. **Access the API docs:**
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

4. **Use the `/summarize/` endpoint:**
   - Upload a CSV file (with an `Article` column) using the interactive Swagger UI or via a tool like `curl` or Postman.
   - The API will return the summaries as a JSON response.

#### Example API Usage with `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/summarize/" -F "file=@dataartifact/news_articles.csv"
```

---

## Code Explanation

### `app.py`

```python
import json
import pandas as pd
from src.newsagentpipeline import process_batch, ChatOpenAI, PromptTemplate, Tool

if __name__ == "__main__":
    # Read the CSV file using pandas from the dataartifact folder
    df = pd.read_csv("dataartifact/news_articles.csv")
    articles = df["Article"].tolist()  # Extract the 'Article' column

    output = process_batch(articles)   # Process articles using the AI pipeline
    with open("Summary.json", "w") as f:
        json.dump(output, f, indent=2) # Save the output as JSON

    print("✅ Done. Output saved to Summary.json.")
```

### `src/fastapi_app.py`

```python
from fastapi import FastAPI, UploadFile, File
import pandas as pd
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
```

- **/summarize/**: Accepts a CSV file upload, processes the articles, and returns the summaries as JSON.

---

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies (LangChain, OpenAI, pandas, FastAPI, uvicorn, etc.)

---

## License

MIT License

---

## Notes

- Ensure your CSV is properly quoted to avoid parsing errors.
- The AI summarization uses OpenAI models via LangChain; set up your API keys as needed.
- If you want to contribute to the codebase please feel free to reach jothiramsanjeevi@gmail.com **Stay Hungry** **Stay Foolish**
