from __future__ import print_function
from jinja2 import Environment, PackageLoader, select_autoescape

import argparse
import sys
import os
import shutil
import zipfile
import csv
import glob
import tempfile
import datetime
import urlparse

env = Environment(
    loader=PackageLoader('main', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)




# test_template=env.get_template("test.xml")
# print test_template.render(image_name="testmenow.jpg")

def process_row(imagedir,outputdir,prefix,row):
    title=row['conf-name']
    description=unicode(row['conf-desc'],'utf8')
    topic=row['confid'].lower()
    doi_suffix=('conf-'+topic).replace(' ','_')
    doi = prefix +'/'+doi_suffix
    conference_url=row['conf-url-href']
    event_url=row['event_url-href']
    event_id=urlparse.parse_qs(urlparse.urlparse(event_url.replace('"','')).query)["id"][0]

    #identify image
    matching_images=glob.glob(os.path.join(imagedir,row['web-scraper-order']+"-conf-image*.*"))
    if len(matching_images)>0:
        image_filename=matching_images[0]
        image_base_filename=os.path.basename(image_filename)
    else:
        image_filename=None
        image_base_filename=None
    if not image_filename:
        print("{} has no matching image ".format(topic))
    tempdir=tempfile.mkdtemp()
    doi_tmp_dir=os.path.join(tempdir,'conference-do-series_'+doi_suffix)
    #print doi_tmp_dir
    shutil.copytree('template_do',doi_tmp_dir)
    os.makedirs(os.path.join(doi_tmp_dir,doi_suffix,"meta"))

    meta_template=env.get_template("meta.xml")
    meta_xml=meta_template.render(title=title,description=description,topic=topic,doi=doi,image_filename=image_base_filename,
    conference_url=conference_url,
    legacy_event_id=event_id)

    with open(os.path.join(doi_tmp_dir,doi_suffix,"meta",doi_suffix+".xml"),'wb') as f:
        f.write(meta_xml.encode("utf-8"))
    if image_filename:
        shutil.copy(image_filename,os.path.join(doi_tmp_dir,doi_suffix,image_base_filename))
    zip_filename=create_zip(tempdir,doi_suffix)
    shutil.copy(zip_filename,os.path.join(outputdir,os.path.basename(zip_filename)))
    shutil.rmtree(tempdir)

def process_csv(args):

    skip_utf8_seek = 0
    filename=args.file
    with open(filename, "rb") as csvfile:
        csv_start = csvfile.read(3)
        if csv_start == b'\xef\xbb\xbf':
            skip_utf8_seek = 3


    with open(filename, "r") as csvfile:

        # remove ut-8 bon sig
        csvfile.seek(skip_utf8_seek)
        csv_reader=csv.DictReader(csvfile)
        for row in csv_reader:
            try:
                process_row(args.assetdir,args.outputdir,args.prefix,row)
            except Exception as e:
                import traceback
                traceback.print_exc()
                print("Unexpected error: {}", e)
                print(row.values())

def create_zip(output_dir,doi_ext):
    zipname = 'conference-do-series_' + doi_ext + '_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.zip'       
    zip_filename=os.path.join(output_dir,zipname)
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
            target = 'conference-do-series_' + doi_ext
            zip_root_dir=os.path.join(output_dir,target)
            for dirname, subdirs, files in os.walk(zip_root_dir):
                for filename in files:
                    zip_file_name=os.path.join(dirname, filename)   
                    zf.write(zip_file_name,zip_file_name.replace(zip_root_dir,''))
    return zip_filename

def main():
    # filename passde through args
    ap = argparse.ArgumentParser(description="Convert webscraper export file to DO submissions")
    ap.add_argument('-o','--outputdir', default="output", help="set output dir for all DOs to be generated")
    ap.add_argument('-p', '--prefix', default='10.1145', help="DOI prefix to use")
    ap.add_argument('-a', '--assetdir', default="conf-acm", help="set asset dir that contains exported images")
    ap.add_argument('-f', '--file', default='conf-acm.csv', help="export file")
    args = ap.parse_args()
    process_csv(args)


if __name__ == '__main__':
    main()
