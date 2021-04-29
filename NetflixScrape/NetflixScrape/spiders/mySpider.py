import scrapy
from .item import MovieItem

def_url = "https://flixable.com/pagination.php?originals=0&page="

# $ scrapy crawl netflixSpider -o Netflix_movie_list.csv --nolog


class MySpider(scrapy.Spider):
    name = "netflixSpider"
    max_page = 150

    # start_urls = [ def_url+str(i) for i in range(1,max_page+1)]
    # <<< FOR TEST
    start_urls = ["https://flixable.com/pagination.php?originals=0&page=1"]

    def parse(self, response):
        print(response.request.url)
        elements = response.xpath("//div[@class='card-body']/a/@href")

        elements = elements[:2]  ### <<< FOR TEST
        for link in elements:
            url = link.get()
            # print(link)
            detail_page = response.urljoin(url)
            # print(detail_page)
            yield scrapy.Request(detail_page, callback=self.parse2)

    def parse2(self, response):  # At detail page
        print(response.request.url)
        newMovie = MovieItem()

        movie_name = response.css('h1.title::text')
        # released_year = response.css('.card-category > span:nth-child(1)::text')
        # rate = response.css('.border::text')
        # description = response.css('p.card-description::text')
        newMovie['image_urls'] = response.xpath(
            "//img[contains(@class,'img poster')]").extract().first()
        
        elements = [
            movie_name,
            # released_year,
            # rate,
            # description,
            # image
        ]
        for i in elements:
            i = i.get()
            print(">>>> ", i)
        print('>>>>>',newMovie['image_urls'])
        newMovie['title'] = movie_name.get()
        # newMovie['released_year'] = released_year.get()
        # newMovie['rate'] = rate.get()
        # newMovie['description'] = description.get()
        # newMovie['director'] = response.xpath("//div[@class='col-lg-8']//p[contains(.,'Director')]//span[2]//a/text()").get()

        # genres = []
        # elements = response.xpath("//div[@class='col-lg-8']//p[contains(.,'Genres')]//span[2]//a/text()")
        # for i in elements:
        #     # print(">>>> ",i.get())
        #     genres.append(i.get())

        # cast = []
        # elements = response.xpath("//div[@class='col-lg-8']//p[contains(.,'Cast')]//span[2]//a/text()")
        # for i in elements:
        #     # print(">>>> ",i.get())
        #     cast.append(i.get())

        # genres = "/".join(genres)
        # # print(genres)

        # cast = "/".join(cast)
        # # print(cast)

        # newMovie['genres'] = genres
        # newMovie['casts'] = cast
        yield newMovie
