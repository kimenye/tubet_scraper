import scrapy
import re
import dateparser
from scrapers.items import OddItem

class Betin(scrapy.Spider):
    name = 'betin'
    start_urls = ['https://web.betin.co.ke/Controls/OddsEventExt.aspx?EventID=371']
    allowed_domains = 'web.betin.co.ke'

    def parse(self, response):
        for match in response.xpath('//div[contains(@class,"item")]'):
            game_id = match.xpath('div[2]/text()').extract()[0]
            hour = match.xpath('div[3]/span[1]/text()').extract()[0]
            day = match.xpath('div[3]/span[2]/text()').extract()[0]

            time = self.get_time(day, hour)

            teams = match.xpath('div[4]/text()').extract()[0].strip()
            teams = self.get_teams(teams)

            home_team = teams[0].strip()
            away_team = teams[1].strip()

            odds = match.xpath('div[6]/div[1]')

            home_odds = odds.xpath('div[1]/div[2]/text()').extract()[0]
            away_odds = odds.xpath('div[2]/div[2]/text()').extract()[0]
            draw_odds = odds.xpath('div[3]/div[2]/text()').extract()[0]

            # print game_id, time, home_team, away_team, home_odds, draw_odds, away_odds

            item = OddItem()
            item['date'] = time
            item['game_id'] = game_id
            item['home_team'] = home_team
            item['home_odds'] = home_odds
            item['draw_odds'] = draw_odds
            item['away_team'] = away_team
            item['away_odds'] = away_odds

            yield item

    def get_time(self, day, time):
        raw_time = "%s %s" %(day,time)
        return dateparser.parse(raw_time)

    def get_teams(self, teams):
        return teams.split('-')
