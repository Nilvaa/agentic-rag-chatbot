import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

class WebSearchService:
    def __init__(self):
        api_key=os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY is not configured"
            )
        self.client=TavilyClient(api_key=api_key)

    def search(self,query:str,max_results:int=5):
        response=self.client.search(
            query=query,
            search_depth="basic",
            max_results=max_results
        )

        results=[]

        for result in response.get("results",[]):
            results.append({
                "title":result.get("title"),
                "url":result.get("url"),
                "content":result.get("content"),
                "score":result.get("score")
            })

            return results