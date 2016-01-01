Folder Structure
================

/journal    (http://larkin.kidmondo.com/journals/posts?page=1)
    - title: string
    - date: date
    - milestone: array
    - body: string
    - tags: string (comma separated)

/gallery    (http://larkin.kidmondo.com/journals/gallery)
    albums
    - title: string
    - desccription: string
    - captured_date: string
        photo(s)
        - album_id:
        - title: string
        - caption(opt): string
        - image_url: string url (should be downloaded)

/about      (http://larkin.kidmondo.com/journals/about)
    name: string
    nickname: string
    profile_photo_url: string (download)
    sex: string
    dob: mm/dd/yyyy
    current_weight: string
    current_height: string
    current_hair_type: string
    current_hair_color: string
    current_eye_color: string
    bio: string
    greek_zodiac_sign: string
    chinese_zodiac_sign: string
    birth_stone: string
    birth_flower: string
    day_of_history: wiki url
    birthdays: wiki url



/growth     (http://larkin.kidmondo.com/journals/growth?year=1) 1 == 0-12 months
    /weight
        age: int (months)
        pounds: int
        ounces: int
        percentile: int (percents)
    /height
        age: int (months)
        inches: float
        percentile: int (percents)

    /dental
        left_forms:
            Central Incisor (8-12 mo.)
            Lateral Incisor (9-13 mo.)
            Cuspid (16-22 mo.)
            First Molar (13-19 mo.)
            Second Molar (25-33 mo.)
            Second Molar (25-31 mo.)
            First Molar (14-18 mo.)
            Cuspid (17-23 mo.)
            Lateral Incisor (10-16 mo.)
            Central Incisor (6-10 mo.)

        right_forms:
            Central Incisor (8-12 mo.)
            Lateral Incisor (9-13 mo.)
            Cuspid (16-22 mo.)
            First Molar (13-19 mo.)
            Second Molar (25-33 mo.)
            Second Molar (25-31 mo.)
            First Molar (14-18 mo.)
            Cuspid (17-23 mo.)
            Lateral Incisor (10-16 mo.)
            Central Incisor (6-10 mo.)



/health     (http://larkin.kidmondo.com/journals/health)
    general information:
        primary_doctor: string
        primary_doctor_address: string
        primary_doctor_phone: string
        blood_type: string
        notes: string

    medical_notes:
        type: string ()
                <select id="medical_note_category" name="medical_note[category]"><option value="illness">illness</option>
                <option value="immunization">immunization</option>
                <option value="checkup">checkup</option>
                <option value="doctor visit">doctor visit</option>
                <option value="dental">dental</option>
                <option value="medicine">medicine</option>
                <option value="other">other</option></select>

        title: string
        created_date: date
        description: string

    food_notes:
        title: string
        created_date: date
        details: string



/timeline?
index.html

