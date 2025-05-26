# NewsAgent

**NewsAgent** is a Python-based pipeline for processing and summarizing news articles using advanced AI models. It reads a CSV file containing news article summaries, processes them in batch, and generates structured summaries and analytics.

---

## Project Structure

```
newsagent/
├── app.py
├── dataartifact/
│   └── news_articles_full.csv
├── src/
│   └── newsagentpipeline.py
├── requirements.txt
├── LICENSE
└── README.md
```

---

## How It Works

### 1. Data Input

- The project expects a CSV file (`news_articles_full.csv`) in the `dataartifact` folder.
- The CSV must have at least two columns: `S.NO` and `Article`.
- Each article is wrapped in double quotes to handle commas within the text.

### 2. Processing Pipeline

- The main script (`app.py`) reads the CSV using pandas.
- It extracts the `Article` column as a list.
- This list is passed to the `process_batch` function from `src/newsagentpipeline.py`.
- The pipeline uses AI models (via LangChain and OpenAI) to analyze and summarize each article.
- The output is saved as `Summary.json`.

### 3. Output

- The output JSON contains:
  - A list of structured reports for each article.
  - An overall summary with sentiment distribution and most common topics.

---

## Flowchart

```bash
+---------------------+
|  news_articles_full |
|      (CSV file)     |
+----------+----------+
           |
           v
+---------------------+
|   app.py (main)     |
| - Reads CSV         |
| - Extracts articles |
+----------+----------+
           |
           v
+-------------------------------+
| process_batch (pipeline)      |
| - AI summarization            |
| - Sentiment/topic extraction  |
+----------+--------------------+
           |
           v
+---------------------+
|   Summary.json      |
| (Structured output) |
+---------------------+
```

---

## Example Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place your CSV file:**
   - Save your news articles as `news_articles_full.csv` in the `dataartifact` folder.

3. **Run the pipeline:**
   ```bash
   python app.py
   ```

4. **Check the output:**
   - The results will be saved in `Summary.json`.

---

## Code Explanation

### `app.py`

```python
import json
import pandas as pd
from src.newsagentpipeline import process_batch, ChatOpenAI, PromptTemplate, Tool

if __name__ == "__main__":
    # Read the CSV file using pandas from the dataartifact folder
    df = pd.read_csv("dataartifact/news_articles_full.csv")
    articles = df["Article"].tolist()  # Extract the 'Article' column

    output = process_batch(articles)   # Process articles using the AI pipeline
    with open("Summary.json", "w") as f:
        json.dump(output, f, indent=2) # Save the output as JSON

    print("✅ Done. Output saved to Summary.json.")
```

- **Reads** the CSV file containing news articles.
- **Extracts** the articles as a list.
- **Processes** the articles in batch using the AI pipeline.
- **Saves** the structured summaries and analytics to `Summary.json`.

---

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies (LangChain, OpenAI, pandas, etc.)

---

## License

MIT License

---

## Notes

- Ensure your CSV is properly quoted to avoid parsing errors.
- The AI summarization uses OpenAI models via LangChain; set up your API keys as needed.