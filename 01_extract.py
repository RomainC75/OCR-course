import PIL
import pytesseract
import cv2
import pandas as pd

img_cv = cv2.imread('./base/Selected/052.jpeg')
cv2.waitKey(0)
cv2.destroyAllWindows()

img_pl = PIL.Image.open('./base/Selected/052.jpeg')

#get text
text_cv = pytesseract.image_to_string(img_cv)
print(text_cv)

text_pl = pytesseract.image_to_string(img_pl)
print(text_pl)

#image to data
data = pytesseract.image_to_data(img_cv)
# print("type : ",type(data))
# data=data.split('\n')
print(data)
dataList = list(map(lambda x: x.split('\t'),data.split('\n') ))
print("datalist : ",dataList)
df = pd.DataFrame(dataList[1:],columns=dataList[0])
print("df : ", df)
print("df infos : ",df.info())

#drop missing in rows
df.dropna(inplace=True) 
# convert some values to int
col_int = ['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height']
df[col_int]=df[col_int].astype(int)
print(" int : ", df)

#draw the bording box
image = img_cv.copy()
level = 'word'
for l,x,y,w,h,c,txt in df[['level','left','top','width','height','conf','text']].values:
    # print(l,x,y,w,h)
    if level == 'page':
        if l==1:
            cv2.rectangle(img=image, pt1=(x,y),pt2=(x+w,y+w), color=(0,0,0), thickness=2)
        else:
            continue
    elif level =='block':
        if l==2:
            cv2.rectangle(img=image, pt1=(x,y),pt2=(x+w,y+w), color=(255,0,0), thickness=2)
        else:
            continue
    elif level =='para':
        if l==3:
            cv2.rectangle(img=image, pt1=(x,y),pt2=(x+w,y+w), color=(0,255,0), thickness=2)
        else:
            continue
    elif level =='line':
        if l==4:
            cv2.rectangle(img=image, pt1=(x,y),pt2=(x+w,y+w), color=(0,0,255), thickness=2)
        else:
            continue
    elif level =='word':
        if l==5:
            cv2.rectangle(img=image, pt1=(x,y),pt2=(x+w,y+w), color=(0,255,0), thickness=2)
            cv2.putText(image,txt,(x,y),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255))
        else:
            continue

cv2.imshow("bounding box", image)
cv2.waitKey(0)
cv2.destroyAllWindows()