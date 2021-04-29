import scrapy
from scrapy.item import Item,Field

class MovieItem(Item):
    title = Field()
    released_year = Field()
    director = Field()
    rate = Field()
    description = Field()
    genres = Field()
    casts = Field()
    image_urls = Field()
    images=Field()