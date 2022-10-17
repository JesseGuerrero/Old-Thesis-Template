import json

jsonFile = open('captions_train2017.json')
jsonData = json.load(jsonFile)
outData = open('humanCOCOTest.txt','w')

captionDict = {}
for i, caption in enumerate(jsonData['annotations']):
    if(caption['image_id'] < 10_000):
        captionDict[caption['image_id']] = []
for i, caption in enumerate(jsonData['annotations']):
    if(caption['image_id'] < 10_000):
        captionDict[caption['image_id']].append(caption['caption'])
# print(captionDict)
captionkeys = []
for key in captionDict.keys():
    captionkeys.append(key)
captionkeys.sort()
for key in captionkeys:
    sentence = " ".join(captionDict[key])
    sentence = sentence.replace("\n", "").replace(",", "").replace(".", "").replace("'", "").lower()
    outData.write(str(key) + ":" + str(sentence) + "\n")



