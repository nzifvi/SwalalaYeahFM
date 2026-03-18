from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import feedparser

app = FastAPI()

# This lets your webpage talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

# Test route - visit localhost:8000/hello to check it works
@app.get("/hello")
def hello():
    return {"message": "backend is working!"}


# fetches latest news
@app.get("/news")
def get_news():
    feed = feedparser.parse("https://feeds.bbci.co.uk/news/rss.xml")

    stories = []
    for entry in feed.entries[:3]:  # just grab 3 stories
        stories.append({
            "title": entry.title,
            "summary": entry.summary
        })

    return {"stories": stories}