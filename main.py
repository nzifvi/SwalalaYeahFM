import feedparser
import Speaker
import app
import time

speaker = Speaker.Speaker("uncle_fu")
scraper1 = app.Scraper("https://feeds.bbci.co.uk/news/rss.xml")

lastSampleTime            = time.time()
sampleWaitPeriodInSeconds = 360

stories = scraper1.scrape(4)
speaker.mergeStories(
    speaker.parseStories(stories)
)
speaker.speak("AudioFiles/output")

#while(True):
#    currentTime    = time.time()
#    speakerContent = None
#    if currentTime - lastSampleTime >= sampleWaitPeriodInSeconds:
#        stories = scraper1.scrape()
#        speaker.speak(
#            speaker.speak(
#                speaker.mergeStories(
#                    speaker.parseStories(stories)
#                ),
#            ),
#            "output.wav"
#        )
#        lastSampleTime = currentTime