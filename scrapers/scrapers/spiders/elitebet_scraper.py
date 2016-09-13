import scrapy
import re
import dateparser
from scrapy.http import FormRequest, Request
from scrapers.items import OddItem


class Elitebet(scrapy.Spider):
    name = "elitebet"
    allowed_domains=['elitebetkenya.com']
    # start_urls = ["http://www.elitebetkenya.com/coupon.php?lquery=England Premier League > Regular Seaso"]
    start_urls = ["http://www.elitebetkenya.com/coupon.php"]

    def parse(self, response):
        yield FormRequest.from_response(response, formname='topleagues', formdata={'lquery':'England Premier League > Regular Seaso'}, callback=self.parse_response)


    def parse_response(self, response):
        for row in response.xpath('//tr[contains(@class, "fixture")]'):

            #
            # Last updated 13/09/2016
            #
            # Quite a complicated parser. It requires both use of adjacent xpath and a submitted form
            #
            home_team = row.xpath('td/span[@class="home uc"]/text()').extract()[0]
            away_team = row.xpath('td/span[@class="away uc"]/text()').extract()[0]

            kick_off = row.xpath('td/text()[4]').extract()[0].strip()
            time = self.get_time(kick_off)

            odds = row.xpath('following-sibling::tr[2]')
            game_id = odds.xpath('td[3]/text()').extract()[0]

            home_odds = odds.xpath('td[4]/text()').extract()[0]
            draw_odds = odds.xpath('td[5]/text()').extract()[0]
            away_odds = odds.xpath('td[6]/text()').extract()[0]

            item = OddItem()
            item['date'] = time
            item['game_id'] = game_id
            item['home_team'] = home_team
            item['home_odds'] = home_odds
            item['draw_odds'] = draw_odds
            item['away_team'] = away_team
            item['away_odds'] = away_odds

            yield item

    def get_time(self, kick_off):
        raw_time = re.sub("KO: ", "", kick_off)
        return dateparser.parse(raw_time)
