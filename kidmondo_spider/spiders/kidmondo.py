# -*- coding: utf-8 -*-
import re

import json
from scrapy.contrib.exporter import BaseItemExporter

from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
import scrapy

from kidmondo_spider.items import *

class UnicodeJsonLinesItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.file = file
        self.encoder = json.JSONEncoder(ensure_ascii=False, **kwargs)

    def export_item(self, item):
        itemdict = dict(self._get_serialized_fields(item))
        self.file.write(self.encoder.encode(itemdict) + '\n')


class KSpider(InitSpider):

    name = "kidmondo"
    login_page = "http://abc.kidmondo.com/session/new"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def init_request(self):
        # This function is called before crawling starts.
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        # Generate a login request.
        return FormRequest.from_response(response, formdata={'email': self.username, 'password': self.password}, callback=self.check_login_response)

    def check_login_response(self, response):
        # Check the response returned by a login request to see if we are successfully logged in.

        if "Welcome back," in response.body:
            self.log("Logged in!")
            self.initialized()
            yield self.make_requests_from_url("http://abc.kidmondo.com/")
        else:
            self.log("Wrong username/password :(")

    def parse(self, response):
        for kid in response.xpath('//*[@id="main_content"]/ol/li[@class="each_kid"]'):

            kid_name = kid.xpath('dl/dt/a/text()').extract()[0]
            kid_url = kid.xpath('dl/dt/a/@href').extract()[0]
            print "name (url) %s (%s)" % (kid_name, kid_url)

            kid_id=re.search("http\:\/\/(.+)\.kidmondo\.com", kid_url).group(1)
            meta=dict(kid_url=kid_url, kid_id=kid_id)

            kid_journal_url = kid.xpath('ul/li[1]/a[2]/@href').extract()[0]
            print "diary %s"    % (kid_journal_url)
            yield Request(kid_journal_url, callback=self.parse_posts, meta=meta)

            kid_gallery_url = kid.xpath('ul/li[2]/a[2]/@href').extract()[0]
            print "gallery %s"  % (kid_gallery_url)
            yield Request(kid_gallery_url, callback=self.parse_albums, meta=meta)

            kid_about_url = kid.xpath('ul/li[3]/a[2]/@href').extract()[0]
            #print "about %s"    % (kid_about_url)
            yield Request(kid_about_url, callback=self.parse_about, meta=meta)

            kid_growth_url = kid.xpath('ul/li[4]/a[2]/@href').extract()[0]
            print "growth %s"   % (kid_growth_url)
            yield Request(kid_growth_url, callback=self.parse_growth_pages, meta=meta)

            kid_height_url = "%s/height" % kid_growth_url
            print "height %s"   % (kid_height_url)
            yield Request(kid_height_url, callback=self.parse_height_pages, meta=meta)

            kid_dental_url = "%s/dental" % kid_growth_url
            print "dental %s"   % (kid_dental_url)
            yield Request(kid_dental_url, callback=self.parse_dental, meta=meta)

            kid_health_url = "%s" % kid.xpath('ul/li[5]/a[2]/@href').extract()[0]
            print "health %s"   % (kid_health_url)
            yield Request(kid_health_url, callback=self.parse_health, meta=meta)

            kid_health_food_url = "%s/food" % kid_health_url
            print "health food %s"   % (kid_health_food_url)
            yield Request(kid_health_food_url, callback=self.parse_health_food, meta=meta)


    def parse_albums(self, response):
        visited = set()
        for a in response.xpath('//div[contains(@class, "photo_album")]/dl/dt/a/@href'):
            album_rel_url = a.extract()
            album_url = "%s%s" % (response.meta['kid_url'], album_rel_url)
            if album_url in visited:
                continue
            visited.add(album_url)

            # "/journals/gallery/photo_albums/oliver-s-album/larkin" -> oliver-s-album
            response.meta['album_id'] = album_rel_url.split('/')[4]

            yield Request(album_url, callback=self.parse_album, meta=response.meta)

    def parse_album(self, response):
        a = KAlbum()
        a['kid_id'] = response.meta['kid_id']
        a['album_id'] = response.meta['album_id']
        a['title'] = response.xpath('//*[@id="main_content"]/h2/text()').extract()[0].strip().encode("utf-8")
        a['description'] = response.xpath('//*[@id="album_thumbnail"]/dd[2]/text()').extract()[0].strip().encode("utf-8")
        yield a

        for p in response.xpath('//div[contains(@class, "photo")]'):
            #http://s3.amazonaws.com/kidmondo-production/images/3286232/LYUBIMOVANATALIA20111011152840733_thumb.jpg
            #print p
            photo_url = "%s%s" % (response.meta['kid_url'], p.xpath('.//dl/dt/a/@href').extract()[0])
            #print photo_url
            yield Request(photo_url, callback=self.parse_album_photo, meta=response.meta)


    def parse_album_photo(self, response):
        photo = KPhoto()
        photo['kid_id'] = response.meta['kid_id']
        photo['album_id'] = response.meta['album_id']
        photo['photo_id'] = response.url.split('/')[-1]
        photo['title']   = response.xpath('//*[@id="main_content"]/div/h2/text()').extract()[0].strip().encode("utf-8")
        try:
            photo['caption'] = response.xpath('//*[@id="main_content"]/div/p[@class="caption"]/text()').extract()[0].strip().encode("utf-8")
        except:
            photo['caption'] = ''

        photo['image_full_url'] = response.xpath('//*[@id="fullsize"]/dd/div/img/@src').extract()[0]
        photo['image_full_url'] = photo['image_full_url'].replace("_show.", ".")
        photo['image_urls'] = [photo['image_full_url']]
        yield photo

# kid_id = scrapy.Field()
#     album_id = scrapy.Field()
#     photo_id = scrapy.Field()
#     title = scrapy.Field()
#     caption = scrapy.Field()
#     image_url = scrapy.Field()  # download it!





    def parse_posts(self, response):
        for post in self.parse_posts_page(response):
            yield post

        visited = set()
        for p in response.xpath('//*[@id="main_content"]/div[@class="pagination"]/a[starts-with(@href, "/journals/posts?page=")]'):
            next_page = p.xpath('.//@href').extract()[0]
            next_page_url = "%s%s" % (response.meta['kid_url'], next_page)
            if next_page_url in visited:
                continue
            visited.add(next_page_url)
            yield Request(next_page_url, callback=self.parse_posts_page, meta=response.meta)


    def parse_posts_page(self, response):

        for p in response.xpath('//*[@id="main_content"]/div[@class="post"]'):
            post = KPost()
            post['kid_id'] = response.meta['kid_id']
            post['title'] = p.xpath('h2/a[1]/text()').extract()[0].encode("utf-8")

            post['post_id'] = re.search("\/journals\/posts\/(\d+)\/edit", p.xpath('h2/a[2]/@href').extract()[0]).group(1)
            post['date'] = p.xpath('.//span[@class="publish_date"]/text()').extract()[0].encode("utf-8")

            body = [para.strip().encode("utf-8") for para in p.xpath('.//*[position()>2 and not(@class="post_meta")]/text()').extract()]
            post['body'] = body

            post_metas = p.xpath('.//p[@class="post_meta"]/text()').extract()[0].strip().split("|")

            post['is_private'] = is_private = False if "Posted by" in post_metas[0] else True

            try:
                post['post_by'] = post_metas[0].split("post by" if is_private else "Posted by")[-1].strip()
            except:
                post['post_by'] = ""

            post['tags'] = ", ".join(p.xpath('.//a[starts-with(@href, "/journals/diary/tags/")]/text()').extract()).encode("utf-8")


            # TBD: comments

            yield post



    def parse_about(self, response):
        about = KAbout()
        about['kid_id'] = response.meta['kid_id']
        about['name'] = response.xpath('//*[@id="main_content"]/dl/dd[2]/text()').extract()
        about['nickname'] = response.xpath('//*[@id="main_content"]/dl/dd[3]/text()').extract()
        about['sex'] = response.xpath('//*[@id="main_content"]/dl/dd[4]/text()').extract()
        about['dob'] = response.xpath('//*[@id="main_content"]/dl/dd[6]/text()').extract()
        about['current_weight'] = response.xpath('//*[@id="main_content"]/dl/dd[7]/text()').extract()
        about['current_height'] = response.xpath('//*[@id="main_content"]/dl/dd[8]/text()').extract()
        about['current_hair_type'] = response.xpath('//*[@id="main_content"]/dl/dd[9]/text()').extract()
        about['current_hair_color'] = response.xpath('//*[@id="main_content"]/dl/dd[10]/text()').extract()
        about['current_eye_color'] = response.xpath('//*[@id="main_content"]/dl/dd[11]/text()').extract()

        about['bio'] = response.xpath('//*[@id="main_content"]/dl/dd[12]/text()').extract()
        about['greek_zodiac_sign'] = response.xpath('//*[@id="main_content"]/dl/dd[13]/text()').extract()
        about['chinese_zodiac_sign'] = response.xpath('//*[@id="main_content"]/dl/dd[14]/text()').extract()
        about['birth_stone'] = response.xpath('//*[@id="main_content"]/dl/dd[15]/text()').extract()
        about['birth_flower'] = response.xpath('//*[@id="main_content"]/dl/dd[16]/text()').extract()
        about['day_of_history'] = response.xpath('//*[@id="main_content"]/dl/dd[17]/a/@href').extract()
        about['birthdays'] = response.xpath('//*[@id="main_content"]/dl/dd[18]/a/@href').extract()

        for key, value in about.items():
            if isinstance(value, list):
                if len(value) > 0:
                    about[key] = value[0]
                else:
                    about[key] = ""

        #profile_photo_url = scrapy.Field() #: string (download)

        yield about


    def parse_growth_pages(self, response):
        for wm in response.xpath('//*[@id="sub_nav_tabs"]/li'):
            growth_url = "%s%s" % (response.meta['kid_url'], wm.xpath('.//a/@href').extract()[0])
            yield Request(growth_url, callback=self.parse_growth, meta=response.meta)


    def parse_growth(self, response):
        year = int(response.url.split('/journals/growth?year=')[1]) - 1
        yxp = response.xpath('//*/table[@id="year_%s"]' % (year + 1))
        cur_month = None
        for month in yxp.xpath('thead/tr/th/text()').extract():
            print month
            if cur_month is None:
                cur_month = 0
            else:
                w = KWeight()
                w['kid_id'] = response.meta['kid_id']
                w['age'] = (year*12) + cur_month + (1 if year > 0 else 0)

                try:
                    w['pounds'] = yxp.xpath('tbody/tr[1]/td[%s]/text()' % (cur_month + 1 + 1)).extract()[0]
                except:
                    w['pounds'] = ""

                try:
                    w['ounces'] = yxp.xpath('tbody/tr[2]/td[%s]/text()' % (cur_month + 1 + 1)).extract()[0]
                except:
                    w['ounces'] = ""
                try:
                    w['percentile'] = yxp.xpath('tbody/tr[3]/td[%s]/text()' % (cur_month + 1 + 1)).extract()[0]
                except:
                    w['percentile'] = ""

                cur_month += 1

                yield w


    def parse_height_pages(self, response):
        for wh in response.xpath('//*[@id="sub_nav_tabs"]/li'):
            height_url = "%s%s" % (response.meta['kid_url'], wh.xpath('.//a/@href').extract()[0])
            print height_url
            yield Request(height_url, callback=self.parse_height, meta=response.meta)


    def parse_height(self, response):
        year = int(response.url.split('/journals/growth/height?year=')[1]) - 1

        yxp = response.xpath('//*[@id="height_measurements"]/div/form/table')
        cur_month = None
        for month in yxp.xpath('thead/tr/th/text()').extract():
            print month

            if cur_month is None:
                cur_month = 0
            else:
                h = KHeight()
                h['kid_id'] = response.meta['kid_id']
                h['age'] = (year*12) + cur_month + (1 if year > 0 else 0)

                try:
                    h['inches'] = yxp.xpath('tbody/tr[1]/td[%s]/text()' % (cur_month + 1 + 1)).extract()[0]
                except:
                    h['inches'] = ""

                try:
                    h['percentile'] = yxp.xpath('tbody/tr[2]/td[%s]/text()' % (cur_month + 1 + 1)).extract()[0]
                except:
                    h['percentile'] = ""

                cur_month += 1

                yield h


    def parse_dental(self, response):
        d = KDental()
        d['kid_id'] = response.meta['kid_id']

        d['left_top_central_incisor'] = response.xpath('//*[@id="left_forms"]/dd[1]/text()').extract()[0].strip()
        d['left_top_lateral_incisor'] = response.xpath('//*[@id="left_forms"]/dd[2]/text()').extract()[0].strip()
        d['left_top_cuspid'] = response.xpath('//*[@id="left_forms"]/dd[3]/text()').extract()[0].strip()
        d['left_top_first_molar'] = response.xpath('//*[@id="left_forms"]/dd[4]/text()').extract()[0].strip()
        d['left_top_second_molar'] = response.xpath('//*[@id="left_forms"]/dd[5]/text()').extract()[0].strip()
        d['left_bottom_second_molar'] = response.xpath('//*[@id="left_forms"]/dd[6]/text()').extract()[0].strip()
        d['left_bottom_first_molar'] = response.xpath('//*[@id="left_forms"]/dd[7]/text()').extract()[0].strip()
        d['left_bottom_cuspid'] = response.xpath('//*[@id="left_forms"]/dd[8]/text()').extract()[0].strip()
        d['left_bottom_lateral_incisor'] = response.xpath('//*[@id="left_forms"]/dd[9]/text()').extract()[0].strip()
        d['left_bottom_central_incisor'] = response.xpath('//*[@id="left_forms"]/dd[10]/text()').extract()[0].strip()

        d['right_top_central_incisor'] = response.xpath('//*[@id="right_forms"]/dd[1]/text()').extract()[0].strip()
        d['right_top_lateral_incisor'] = response.xpath('//*[@id="right_forms"]/dd[2]/text()').extract()[0].strip()
        d['right_top_cuspid'] = response.xpath('//*[@id="right_forms"]/dd[3]/text()').extract()[0].strip()
        d['right_top_first_molar'] = response.xpath('//*[@id="right_forms"]/dd[4]/text()').extract()[0].strip()
        d['right_top_second_molar'] = response.xpath('//*[@id="right_forms"]/dd[5]/text()').extract()[0].strip()
        d['right_bottom_second_molar'] = response.xpath('//*[@id="right_forms"]/dd[6]/text()').extract()[0].strip()
        d['right_bottom_first_molar'] = response.xpath('//*[@id="right_forms"]/dd[7]/text()').extract()[0].strip()
        d['right_bottom_cuspid'] = response.xpath('//*[@id="right_forms"]/dd[8]/text()').extract()[0].strip()
        d['right_bottom_lateral_incisor'] = response.xpath('//*[@id="right_forms"]/dd[9]/text()').extract()[0].strip()
        d['right_bottom_central_incisor'] = response.xpath('//*[@id="right_forms"]/dd[10]/text()').extract()[0].strip()

        yield d


    def parse_health(self, response):
        hg = KHealthGeneral()
        hg['kid_id'] = response.meta['kid_id']

        try:
            hg['primary_doctor'] = response.xpath('//*[@id="important_information"]/dl/dd[1]/text()').extract()[0].strip()
        except:
            hg['primary_doctor'] = ''

        try:
            hg['primary_doctor_address'] = [ln.strip() for ln in response.xpath('//*[@id="important_information"]/dl/dd[2]/p/text()').extract()]
        except:
            hg['primary_doctor_address'] = ''

        try:
            hg['primary_doctor_phone'] = response.xpath('//*[@id="important_information"]/dl/dd[3]/text()').extract()[0].strip()
        except:
            hg['primary_doctor_phone'] = ''

        try:
            hg['blood_type'] = response.xpath('//*[@id="important_information"]/dl/dd[4]/text()').extract()[0].strip()
        except:
            hg['blood_type'] = ''
        yield hg


        for row in response.xpath('//*[@class="medical_note"]'):

            hmn = KHealthMedicalNote()
            hmn['kid_id'] = response.meta['kid_id']
            hmn['note_type'] = row.xpath('.//td[1]/text()').extract()[0].strip()
            hmn['title'] = row.xpath('.//td[2]/text()').extract()[0].strip()
            hmn['created_date'] = row.xpath('.//td[3]/text()').extract()[0].strip()
            hmn['description'] = row.xpath('.//td[4]/text()').extract()[0].strip()
            yield hmn


    def parse_health_food(self, response):

        print "parse_health_food", response.xpath('//*[@class="food_note"]')

        for row in response.xpath('//*[@class="food_note"]'):

            hfn = KHealthFoodNote()
            hfn['kid_id'] = response.meta['kid_id']
            hfn['title'] = row.xpath('.//td[1]/text()').extract()[0].strip()
            hfn['created_date'] = row.xpath('.//td[2]/text()').extract()[0].strip()
            hfn['details'] = [ln.strip() for ln in row.xpath('.//td[3]/text()').extract() if ln and ln.strip()]

            yield hfn


