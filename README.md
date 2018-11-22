
# Convert CSV file to Conferences DO

Requires python2.7


* `conf-acm`: contains the images 
* `conf-acm.csv`: contains the metadata and the image name

```shell
> pip install -r requirements.txt
> python main.py
```

Default export is to `output`

## Docker 

You can also run it through Docker 
Just create a local directory with the name `output`

```shell
> mkdir output
> docker build -t acm-conferences-generation .
> docker run -it --rm --name generate-do -v `pwd`/output:/generation/output acm-conferences-generation
```

# Collect CSV data

Install chrome plugin Web Scraper
https://chrome.google.com/webstore/detail/web-scraper/jnhgnonknehpejjnehehllkliplmbmhn

Create a new sitemap  by importing  [sitemapper.json](/npolyzotisatypon/acm-conferences-generation/blob/master/sitemapper.json)

Run sitemap generation and export data
You then have to download the images with new filenames (TBC)