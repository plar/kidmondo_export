# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KPost(scrapy.Item):

    def __init__(self):
        scrapy.Item.__init__(self)
        self['object_type'] = "post"

    object_type = scrapy.Field()

    kid_id = scrapy.Field()
    post_id = scrapy.Field()
    post_by = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    milestone = scrapy.Field()
    body = scrapy.Field()
    tags = scrapy.Field()
    is_private = scrapy.Field()


class KAlbum(scrapy.Item):
    def __init__(self):
        scrapy.Item.__init__(self)
        self['object_type'] = "album"

    object_type = scrapy.Field()

    kid_id = scrapy.Field()
    album_id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    captured_date = scrapy.Field()


class KPhoto(scrapy.Item):
    def __init__(self):
        scrapy.Item.__init__(self)
        self['object_type'] = "photo"

    object_type = scrapy.Field()

    kid_id = scrapy.Field()
    album_id = scrapy.Field()
    photo_id = scrapy.Field()
    title = scrapy.Field()
    caption = scrapy.Field()
    comments = scrapy.Field()
    image_full_url = scrapy.Field()  # download it!
    image_urls = scrapy.Field()
    images = scrapy.Field()


class KAbout(scrapy.Item):
    def __init__(self):
        scrapy.Item.__init__(self)
        self['object_type'] = "about"

    object_type = scrapy.Field()

    kid_id = scrapy.Field()
    name = scrapy.Field() #: string
    nickname = scrapy.Field() #: string
    profile_photo_url = scrapy.Field() #: string (download)
    sex = scrapy.Field() #: string
    dob = scrapy.Field() #: mm/dd/yyyy
    current_weight = scrapy.Field() #: string
    current_height = scrapy.Field() #: string
    current_hair_type = scrapy.Field() #: string
    current_hair_color = scrapy.Field() #: string
    current_eye_color = scrapy.Field() #: string
    bio = scrapy.Field() #: string
    greek_zodiac_sign = scrapy.Field() #: string
    chinese_zodiac_sign = scrapy.Field() #: string
    birth_stone = scrapy.Field() #: string
    birth_flower = scrapy.Field() #: string
    day_of_history = scrapy.Field() #: wiki url
    birthdays = scrapy.Field() #: wiki url


class KWeight(scrapy.Item):
    def __init__(self):
        scrapy.Item.__init__(self)
        self['object_type'] = "weight"

    object_type = scrapy.Field()

    kid_id = scrapy.Field()
    age = scrapy.Field() #: int (months)
    pounds = scrapy.Field() #: int
    ounces = scrapy.Field() #: int
    percentile = scrapy.Field() #: int (percents)


class KHeight(scrapy.Item):
    def __init__(self):
        scrapy.Item.__init__(self)
        self['object_type'] = "height"

    object_type = scrapy.Field()
    kid_id = scrapy.Field()
    age = scrapy.Field() #: int (months)
    inches = scrapy.Field() #: float
    percentile = scrapy.Field() #: int (percents)


class KDental(scrapy.Item):
    def __init__(self):
        scrapy.Item.__init__(self)
        self['object_type'] = "dental"

    object_type = scrapy.Field()
    kid_id = scrapy.Field()
    left_top_central_incisor = scrapy.Field()   # (8-12 mo.)
    left_top_lateral_incisor = scrapy.Field()   # (9-13 mo.)
    left_top_cuspid = scrapy.Field()            # (16-22 mo.)
    left_top_first_molar = scrapy.Field()       # (13-19 mo.)
    left_top_second_molar = scrapy.Field()      # (25-33 mo.)
    left_bottom_second_molar = scrapy.Field()      # (25-31 mo.)
    left_bottom_first_molar = scrapy.Field()       # (14-18 mo.)
    left_bottom_cuspid = scrapy.Field()            # (17-23 mo.)
    left_bottom_lateral_incisor = scrapy.Field()   # (10-16 mo.)
    left_bottom_central_incisor = scrapy.Field()   # (6-10 mo.)

    right_top_central_incisor = scrapy.Field()   # (8-12 mo.)
    right_top_lateral_incisor = scrapy.Field()   # (9-13 mo.)
    right_top_cuspid = scrapy.Field()            # (16-22 mo.)
    right_top_first_molar = scrapy.Field()       # (13-19 mo.)
    right_top_second_molar = scrapy.Field()      # (25-33 mo.)
    right_bottom_second_molar = scrapy.Field()      # (25-31 mo.)
    right_bottom_first_molar = scrapy.Field()       # (14-18 mo.)
    right_bottom_cuspid = scrapy.Field()            # (17-23 mo.)
    right_bottom_lateral_incisor = scrapy.Field()   # (10-16 mo.)
    right_bottom_central_incisor = scrapy.Field()   # (6-10 mo.)


class KHealthGeneral(scrapy.Item):
    def __init__(self):
        scrapy.Item.__init__(self)
        self['object_type'] = "health_general"

    object_type = scrapy.Field()
    kid_id = scrapy.Field()
    primary_doctor = scrapy.Field()  #: string
    primary_doctor_address = scrapy.Field()  #: string
    primary_doctor_phone = scrapy.Field()  #: string
    blood_type = scrapy.Field()  #: string


class KHealthMedicalNote(scrapy.Item):
    def __init__(self):
        scrapy.Item.__init__(self)
        self['object_type'] = "medical_note"

    object_type = scrapy.Field()
    kid_id = scrapy.Field()
    note_type = scrapy.Field()   # string ()
                            # <select id="medical_note_category" name="medical_note[category]"><option value="illness">illness</option>
                            # <option value="immunization">immunization</option>
                            # <option value="checkup">checkup</option>
                            # <option value="doctor visit">doctor visit</option>
                            # <option value="dental">dental</option>
                            # <option value="medicine">medicine</option>
                            # <option value="other">other</option></select>

    title = scrapy.Field()          #: string
    created_date = scrapy.Field()   #: date
    description = scrapy.Field()    #: string


class KHealthFoodNote(scrapy.Item):
    def __init__(self):
        scrapy.Item.__init__(self)
        self['object_type'] = "food_note"

    object_type = scrapy.Field()
    kid_id = scrapy.Field()
    title = scrapy.Field()          #: string
    created_date = scrapy.Field()   #: date
    details = scrapy.Field()        #: string


