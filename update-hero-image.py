#!/usr/bin/python
# This script only handles a single file. It can be updated to loop through all docs
# Can use the following to download all discover articles locally.
# `gsutil -m cp -R gs://petcircle-graphic-artist-bucket/content/articles .`
#
# Usage: python update-hero-image.py article/10-frequent-kitten-questions.html
# Requirements: beautifulsoup - `pip install beautifulsoup4`
# Requirements: requests - `pip install requests`
# Requirements: image - `pip install image`

import sys
from bs4 import BeautifulSoup
from requests import get
from io import BytesIO
from PIL import Image
import os


folderName = 'articles_1_Feb'
updateFolderName = 'articles_1_Fen_updated'

print(os.getcwd()+'/'+folderName)

for fileToModify in os.listdir(os.getcwd()+'/'+folderName):

   with open(os.path.join(os.getcwd()+'/'+folderName, fileToModify)) as f: 

        print("fileToModify",fileToModify)
        fileContents = ''
        if fileToModify.endswith('.html'):

            with open("./"+folderName+"/"+fileToModify) as f:
                fileContents = f.read()
                # make it HTML so it can be parsed
                fileContents = '<html>' + fileContents + '</html>'

                soup = BeautifulSoup(fileContents, 'html.parser')

                heroImages = soup.find_all('img')


                for heroImage in heroImages:
                    # replace it with GCS url so we dont get blocked by CDN
                    URL = heroImage['src'].replace('www.petcircle.com.au', 'storage.googleapis.com')
                    # download image
                    print("URL",URL)
                    try:
                        res = get(URL, stream=True)
                        
                        img = Image.open(BytesIO(res.content))
                        width, height = img.size

                        heroImage['width'] = width
                        heroImage['height'] = height
                        # write to an updated directory

                        print("heroImage",heroImage)
                        outputFile = open(updateFolderName+'/' + fileToModify, "w")
                        outputFile.write(str(soup))
                        outputFile.close()
                    except:
                        print("image not found")

                    
