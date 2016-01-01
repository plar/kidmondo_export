# Kidmondo Export

Export kidmondo account to your local drive

It is scrapy based scraper. It can export all data except videos because I don't have it in my account.

## How to use

1. Create python virtual enviroment. (ie: mkvirtualenv kidmondo)
2. Install dependencies

```bash
pip install -r reqs.txt
```

3. Run scrapy

```bash
scrapy crawl kidmondo -o target/kidmondo.json -t json -a username="kidomondo login" -a password="kidmondo password"
```
It will download all pages and images into target directory.

## TBD

I will create a static page generator for downloaded information

