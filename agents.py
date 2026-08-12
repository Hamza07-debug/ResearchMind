from langgraph.prebuilt import create_react_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv
from datetime import datetime
from langchain_core.rate_limiters import InMemoryRateLimiter

# Load environment variables
load_dotenv()

# Initialize an in-memory rate limiter (max 1 request per 2 seconds) to avoid Mistral API 429s
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.5,
)

# Initialize Mistral LLM with the rate limiter
llm = ChatMistralAI(
    model_name='mistral-large-latest',
    temperature=0.7,
    rate_limiter=rate_limiter
)

def build_search_agent():
    current_date = datetime.now().strftime("%B %d, %Y")
    return create_react_agent(
        model=llm,
        tools=[web_search],
        prompt=(
            f"You are an expert research assistant. Today's date is {current_date}. "
            f"Your job is to find the most recent and up-to-date information available. "
            f"Always include the current year or 'latest' in your search queries to ensure recency. "
            f"Prefer results from the last 30 days. Discard any outdated or stale information."
        )
    )

def build_reader_agent():
    current_date = datetime.now().strftime("%B %d, %Y")
    return create_react_agent(
        model=llm,
        tools=[scrape_url],
        prompt=f"You are an expert research assistant. The current date is {current_date}. Always ensure your information is up to date relative to this date."
    )

# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are an expert research writer. Write clear, structured and insightful reports.'),
    ('human', 'Write a detailed research report on the topic below.\n\nTopic: {topic}\n\nResearch Gathered:\n{research}\n\nStructure the report as:\n- Introduction\n- Key Findings (minimum 3 well-explained points)\n- Conclusion\n- Sources (list all URLs found in the research)\n\nBe detailed, factual and professional.')
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a sharp and constructive research critic. Be honest and specific.'),
    ('human', 'Review the research report below and evaluate it strictly.\n\nReport:\n{report}\n\nRespond in this exact format:\n\nScore: X/10\n\nStrengths:\n- ...\n- ...\n\nAreas to Improve:\n- ...\n- ...\n\nSpecific Suggestions:\n- ...\n- ...\n\nKeep your feedback clear, actionable, and concise.')
])

critic_chain = critic_prompt | llm | StrOutputParser()
