import numpy as np
import pandas as pd
import cv2
import pytesseract
import os
from glob import glob
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')

#get a list of paths of every jpeg images
imgPaths = glob('./base/Selected/*.jpeg')

allBusinessCard = pd.DataFrame(columns=['id', 'text'])
for imgPath in tqdm(imgPaths, desc="BusinessCard"):
    imgPath = imgPaths[0]
    _, filename = os.path.split(imgPath)

    #extract data and text
    img_cv = cv2.imread(imgPath)
    text_cv = pytesseract.image_to_string(img_cv)
    data = pytesseract.image_to_data(img_cv)
    
    # convert to pandas
    dataList = list(map(lambda x: x.split('\t'),data.split('\n') ))
    df = pd.DataFrame(dataList[1:],columns=dataList[0])
    df.dropna(inplace=True)
    print(df)

    # need to get the rows when conf( confirmation ) is > 30 (% chance to get the good value)
    # 1 : convert all confs to integer
    df['conf'] = df['conf'].astype(int)
    # get the values 
    useFulData = df.query('conf > 30')

    # extract the text in another dataFrame
    businessCard = pd.DataFrame()
    businessCard['text'] = useFulData['text']
    # businessCard['conf'] = useFulData['conf']
    businessCard['id'] = filename
    # print(businessCard)

    #concat
    allBusinessCard=pd.concat((allBusinessCard, businessCard))

print(allBusinessCard)
allBusinessCard.to_csv('businessCard.csv',index=False)