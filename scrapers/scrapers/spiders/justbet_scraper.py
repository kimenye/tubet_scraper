import scrapy
import re
import dateparser
from scrapers.spiders.base import Base
from scrapy.http import Request

class Justbet(Base):
    name = "justbet"
    allowed_domains = ["justbet.co.ke"]
    start_urls = ["http://justbet.co.ke/index.php?option=com_justbet"]

    def parse(self, response):
        # We need this to obtain a referrer...
        yield scrapy.Request("http://justbet.co.ke/index.php?option=com_justbet&league=58",callback=self.parse_matches)

    def parse_matches(self, response):
        for match in response.xpath('//table[contains(@class, "razrada")]/tr'):
            match_id = match.xpath('td[1]/text()').extract()[0].strip()
            time_string = match.xpath('td[2]/text()').extract()[0].strip()
            date = dateparser.parse(time_string, settings={'PREFER_DATES_FROM': 'future'})

            odds = match.xpath('td[3]/table/tr')
            home_team = odds.xpath('td[1]/a[1]/span[1]/text()').extract()[0].strip()
            home_odds = odds.xpath('td[1]/a[1]/span[2]/text()').extract()[0].strip()
            draw_odds = odds.xpath('td[2]/a[1]/span[2]/text()').extract()[0].strip()
            away_team = odds.xpath('td[3]/a[1]/span[1]/text()').extract()[0].strip()
            away_odds = odds.xpath('td[3]/a[1]/span[2]/text()').extract()[0].strip()

            # print match_id, date, home_team, home_odds, draw_odds, away_team, away_odds
            yield self.build_item(match_id, home_team, away_team, home_odds, away_odds, draw_odds, date)
