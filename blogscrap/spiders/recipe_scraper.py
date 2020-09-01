import scrapy
import unicodedata

class RecipeScraper(scrapy.Spider):

    name = "recipe"
    start_urls = ['https://manjuvinodzkitchen.blogspot.com/',]


    def parse(self, response):
        blog_pages = response.xpath('//*[@id="ArchiveList"]//*[@class="archivedate"]/a/@href')
        print("Inside parse")
        yield from response.follow_all(blog_pages, self.parse_recipe_pages)


    def parse_recipe_pages(self, response):
        recipe_page_links = response.css('.post-title a')
        yield from response.follow_all(recipe_page_links, self.parse_recipe)

    
    def parse_recipe(self, response):
        
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
    
        def extract_with_xpath(query):
            return response.xpath(query).get(default='').strip()

        def extract_with_xpath_all(query):
            return response.xpath(query).getall()
        
        title = extract_with_xpath('//div[@class="post"]/div/h3/text()')
        posted_date = extract_with_xpath('//*[@class="post-header"]//span/a/time/@datetime')
        heading = extract_with_css('div.post-body div span span::text')
        images = [image for image in extract_with_xpath_all('//div[@class="post-body entry-content float-container"]//a/@href') if '.jpg' in image]
        post_body = [ unicodedata.normalize('NFKD', data.strip()) for data in extract_with_xpath_all('//div[@class="post-body entry-content float-container"]//*[not(self::script)]/text()') if data.strip()]
        labels = [*extract_with_xpath_all('//div[@class="post-footer-line post-footer-line-2"]/span/a/text()')]

        yield {
            'title': title,
            'posted_date': posted_date,
            'heading': heading,
            'images': images,
            'post_body': post_body,
            'labels': labels
            }