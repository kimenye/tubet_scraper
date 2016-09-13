import scrapy
import re
import dateparser
from scrapers.items import OddItem

class Sportpesa(scrapy.Spider):
    name = "sportpesa"
    allowed_domains = ["sportpesa.com"]
    start_urls = ["https://www.sportpesa.com/games/league_games/67600/1"]

    def parse(self, response):
        for row in response.xpath('//*[@id="games_table"]/table/tbody/tr'):
            # a row contains multiple columns that have the following structure
            # This returns an array of yield items
            #
            # Last updated: 13/09/2016
            #
            # <tr>
            #   <td>Date</td> - 18-09-16 : dd-mm-yy
            #   <td>Time</td> - 22:00 : HH:mm
            #   <td>Game Id</td> - 2343
            #   <td>
            #       <span>Home Team</span> - Chelsea
            #       <span>
            #           <span>Home Odds</span> - 2.22
            #       </span>
            #   </td>
            #   <td>Draw Odds</td>
            #   <td>
            #       <span>Away Team</span> - Liverpool
            #       <span>
            #           <span>Away Odds</span> - 2.15
            #       </span>
            #   </td>
            # </tr>

            date = row.xpath('td[1]/text()').extract()[0]
            time = row.xpath('td[2]/text()').extract()[0]
            game_id = row.xpath('td[3]/text()').extract()[0]
            home_team = row.xpath('td[4]/span[1]/text()').extract()[0].strip()
            home_odds = row.xpath('td[4]/span[2]/span[1]/text()').extract()[0].strip()
            draw_odds = row.xpath('td[5]/text()').extract()[0]
            away_team = row.xpath('td[6]/span[1]/text()').extract()[0].strip()
            away_odds = row.xpath('td[6]/span[2]/span[1]/text()').extract()[0].strip()

            item = OddItem()
            item['date'] = self.get_time(date, time)
            item['game_id'] = game_id
            item['home_team'] = home_team
            item['home_odds'] = home_odds
            item['draw_odds'] = draw_odds
            item['away_team'] = away_team
            item['away_odds'] = away_odds

            yield item

    def get_time(self, date, time):
        raw_time = "%s %s" %(date,time)
        return dateparser.parse(raw_time)
