import json
import pandas as pd
from src.newsagentpipeline import (
    process_batch,
    ChatOpenAI,
    PromptTemplate,
    Tool
)

if __name__ == "__main__":
    # Read the CSV file using pandas from the dataartifact folder
    df = pd.read_csv("dataartifact/news_articles.csv")
    articles = df["Article"].tolist()  # Use the correct column name "Article"

    output = process_batch(articles)
    with open("Summary.json", "w") as f:
        json.dump(output, f, indent=2)

    print("✅ Done. Output saved to Summary.json.")
