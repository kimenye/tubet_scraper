import scrapy
from scrapers.items import OddItem

class Base(scrapy.Spider):

    def build_item(self, game_id, home_team, away_team, home_odds, away_odds, draw_odds, date):
        item = OddItem()
        item['date'] = date
        item['game_id'] = game_id
        item['home_team'] = home_team
        item['home_odds'] = home_odds
        item['draw_odds'] = draw_odds
        item['away_team'] = away_team
        item['away_odds'] = away_odds
        return item
