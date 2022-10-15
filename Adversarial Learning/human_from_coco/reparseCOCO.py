import json

jsonFile = open('captions_train2017.json')
jsonData = json.load(jsonFile)
outData = open('humanCOCO.txt','w')

captionDict = {}
for i, caption in enumerate(jsonData['annotations']):
    captionDict["000000" + str(caption['image_id'])] = []
for i, caption in enumerate(jsonData['annotations']):
    captionDict["000000" + str(caption['image_id'])].append(caption['caption'])
# print(captionDict)
for key, value in captionDict.items():
    sentence = " ".join(value)
    sentence = sentence.replace("\n", "").replace(",", "").replace(".", "").replace("'", "").lower()
    outData.write(str(key) + ":" + str(sentence) + "\n")



