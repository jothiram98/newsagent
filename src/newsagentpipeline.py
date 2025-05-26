# agents_news_pipeline.py
from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from collections import Counter
import json
import logging
import os

from dotenv import load_dotenv
load_dotenv()
import os

api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4", temperature=0,api_key=api_key,max_retries=3)

# Tool 1: Fact Extraction
fact_prompt = PromptTemplate.from_template("""
Extract key facts from this article. Return JSON with keys:
- who
- what
- when
- where

Article:
{input}
""")

def extract_facts(input):
    try:
        logging.info("Extracting facts from article.")
        return llm.predict(fact_prompt.format(input=input))
    except Exception as e:
        logging.error(f"Fact extraction failed: {e}")
        return json.dumps({"error": "Fact extraction failed", "note": str(e)})

fact_tool = Tool(name="FactExtractor", func=extract_facts, description="Extract who/what/when/where")

# Tool 2: Sentiment Analysis
sentiment_prompt = PromptTemplate.from_template("""
Analyze the overall sentiment of this article.
Return one word: positive, neutral, or negative.

Article:
{input}
""")

def analyze_sentiment(input):
    try:
        logging.info("Analyzing sentiment.")
        return llm.predict(sentiment_prompt.format(input=input)).strip().lower()
    except Exception as e:
        logging.error(f"Sentiment analysis failed: {e}")
        return "error"

sentiment_tool = Tool(name="SentimentAnalyzer", func=analyze_sentiment, description="Classify sentiment")

# Tool 3: Topic Classification
topic_prompt = PromptTemplate.from_template("""
Classify this article into topics from the list:
[politics, technology, sports, business, health, entertainment]

Return a JSON list of topics.

Article:
{input}
""")

def classify_topic(input):
    try:
        logging.info("Classifying topic.")
        return llm.predict(topic_prompt.format(input=input))
    except Exception as e:
        logging.error(f"Topic classification failed: {e}")
        return json.dumps(["error"])

topic_tool = Tool(name="TopicClassifier", func=classify_topic, description="Classify article topic(s)")

# Aggregator tool
def aggregate_all(fact, sentiment, topics):
    try:
        logging.info("Aggregating results.")
        agg_prompt = PromptTemplate.from_template("""
Combine the following results into a single JSON report:
- Facts: {fact}
- Sentiment: {sentiment}
- Topics: {topics}

If any field is missing, add "note": "Partial data available"

Return only JSON.
""")
        return llm.predict(agg_prompt.format(fact=fact, sentiment=sentiment, topics=topics))
    except Exception as e:
        logging.error(f"Aggregation failed: {e}")
        return json.dumps({"error": "Aggregation failed", "note": str(e)})

# LangChain Agent setup (no tools for aggregator, just final LLM call)
tools = [fact_tool, sentiment_tool, topic_tool]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Set up logging to file in logs folder
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Main processing function
def process_article(article_text):
    try:
        logging.info("Processing single article.")
        fact = extract_facts(article_text)
        sentiment = analyze_sentiment(article_text)
        topic = classify_topic(article_text)
        combined = aggregate_all(fact, sentiment, topic)
        return {"facts": fact, "sentiment": sentiment, "topics": topic, "report": combined}
    except Exception as e:
        logging.error(f"Failed processing: {str(e)}")
        return {"report": None, "error": str(e)}

# Batch processing with summary
def process_batch(articles):
    final_reports = []
    sentiments = []
    topic_counter = Counter()

    for i, article in enumerate(articles):
        logging.info(f"Processing article {i+1}/{len(articles)}")
        result = process_article(article)
        final_reports.append(result["report"])

        if result.get("sentiment"):
            sentiments.append(result["sentiment"])
        try:
            parsed_topics = json.loads(result["topics"]) if isinstance(result["topics"], str) else []
            topic_counter.update(parsed_topics)
        except Exception as e:
            logging.warning(f"Failed to parse topics for article {i+1}: {e}")

    summary = {
        "sentiment_distribution": dict(Counter(sentiments)),
        "most_common_topics": topic_counter.most_common(5)
    }

    return {"reports": final_reports, "summary": summary}
