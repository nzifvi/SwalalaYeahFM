from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import feedparser
from starlette.responses import FileResponse

app = FastAPI()

# This lets your webpage talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

class Scraper:
    def __init__(self, url):
        self.url = url

    @app.get("/news")
    def scrape(self, getAmount:int) -> list:
        feed = feedparser.parse(self.url)

        stories = []
        for entry in feed.entries[:getAmount]:
            stories.append({
                "title": entry.title,
                "summary": entry.summary
            })
        return stories

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

@app.get("/segment")
def get_segment():
    # get news
    feed = feedparser.parse("https://feeds.bbci.co.uk/news/rss.xml")
    stories = []
    for entry in feed.entries[:3]:
        stories.append({"title": entry.title, "summary": entry.summary})

    # build script
    script = build_script(stories)
    print(f"Speaking: {script}")

    # generate audio
    import soundfile as sf
    audio = tts.generate(script)
    sf.write("output.wav", audio.cpu().numpy(), 24000)

    return FileResponse("output.wav", media_type="audio/wav")

##
# title -> summary -> randomly selected phrase -> title -> summary -> randomly select phrase