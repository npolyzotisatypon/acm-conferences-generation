
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