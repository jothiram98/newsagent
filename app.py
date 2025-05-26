import json
from src.newsagentpipeline import (
    process_batch,
    ChatOpenAI,
    PromptTemplate,
    Tool
)

if __name__ == "__main__":
    articles = [
        "Apple released its latest iPhone 16 today, featuring AI-enhanced capabilities and a titanium frame.",
        "The local football team triumphed 3-1 over their rivals in the regional championship.",
        "A bill supporting green energy investment was passed by the senate yesterday in Washington."
    ]

    output = process_batch(articles)
    with open("Summary.json", "w") as f:
        json.dump(output, f, indent=2)

    print("✅ Done. Output saved to Summary.json.")
