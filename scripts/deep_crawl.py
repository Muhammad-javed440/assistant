import asyncio

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy


async def main():
    # Configure a 2-level deep crawl
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=2, include_external=False),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True,
    )

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun("https://panaversity.org/", config=config)

        print(f"Crawled {len(results)} pages in total")  #type:ignore

        # Access individual results
        for result in results[:3]:  # Show first 3 results  #type:ignore
            print(f"URL: {result.url}")
            print(f"Depth: {result.metadata.get('depth', 0)}")
            print(result.markdown)


if __name__ == "__main__":
    asyncio.run(main())