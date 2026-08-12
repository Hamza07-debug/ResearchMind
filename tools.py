from langchain.tools import tool

import os
import requests

from bs4 import BeautifulSoup
from requests import api
from tavily import TavilyClient
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str)-> str:
   """Search the web for recent and reliable information on a topic. Returns titles, URLs, snippets, and content."""
   results=tavily.search(
      query=query,
      max_results=7,
      days=30,               # only return results from the last 30 days
   )

   out=[]

   for r in results.get('results', []):
      title = r.get("title", "N/A")
      url = r.get("url", "N/A")
      snippet = r.get("snippet") or r.get("summary") or r.get("content") or ""
      content = r.get("content") or r.get("raw_content") or r.get("summary") or ""

      out.append(
            f"""
Title: {title}
URL: {url}
Snippet: {snippet}
Content: {content}

"""
      )

   return "\n----\n".join(out) if out else "No results found."


# debug: print(web_search.invoke("What are the latest news of war?"))


@tool
def scrape_url(url:str)-> str:
   "Scrape and returns clean text content from a given URL for deeper reading."

   try:
      resp=requests.get(url,timeout=8,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
      soup=BeautifulSoup(resp.content,"html.parser")
      for tag in soup(["script","style","nav","footer"]):
         tag.decompose()
      return soup.get_text(separator="\n",strip=True)[:2000]  # Limit to first 2000 characters for brevity
   except Exception as e:
      return f"Error scraping URL: {e}"


# debug: print(scrape_url.invoke("https://www.bbc.com/news/world-europe-66707416"))