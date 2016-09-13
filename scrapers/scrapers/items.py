# -*- coding: utf-8 -*-

import scrapy

class OddItem(scrapy.Item):
    date = scrapy.Field()
    game_id = scrapy.Field()
    home_team = scrapy.Field()
    home_odds = scrapy.Field()
    draw_odds = scrapy.Field()
    away_team = scrapy.Field()
    away_odds = scrapy.Field()
