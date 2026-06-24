import json
import scrapy

class LemmyEndoSpider(scrapy.Spider):
    name = "lemmy_endo"
    
    # We use Lemmy's native API search endpoint instead of the web browser URL!
    start_urls = ["https://lemmy.world/api/v3/search?q=endometriosis&type_=Posts&sort=TopAll&limit=20"]

    def parse(self, response):
        raw_data = json.loads(response.text)
        
        # Note: The search endpoint returns a dictionary key called "posts"
        for item in raw_data.get("posts", []):
            yield {
                "title": item["post"]["name"],
                "author": item["creator"]["name"],
                "community": item["community"]["name"],  # Shows which community it was found in!
                "url": item["post"]["ap_id"],
                "score": item["counts"]["score"],
            }