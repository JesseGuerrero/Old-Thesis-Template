# from mutation_operators.dataset import *
# with open("../data/humanCOCOTestSmall.txt", "r") as f:
#     data = parseTxt1ByCaption(f.readlines(), False)
#     dataset = Dataset(data, ["humanCOCOTestSmall"])
#     dataset.setRootDir("./mutations/")
#     print(dataset)
#     dataset.saveToFile()
import json
with open("./mutation_data/adjectives.txt", "r") as f:
    lines = f.readlines()
    text = []
    for line in lines:
        text.append(line.replace("\n", ""))
    diction = {}
    diction["adjective"] = text
    with open("mutation_data/random_adjectives.json", "w") as f:
        json.dump(diction, f)