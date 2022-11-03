import json, os
class DataSet:
    '''
    {
        Unique_ID: [TEXT],
        Unique_ID: [TEXT],
        Unique_ID: [TEXT]
    }
    '''
    _data : dict
    _root_dir = "."
    #List of strings to add to file name
    _mutations : list

    def __init__(self, data : dict, mutations : list):
        self._data = data
        self._mutations = mutations

    def parseJSON1ByCaption(self, text) -> dict:
        pass
    def getData(self):
        return self._data
    def saveDataMutation(self, data : dict, mutation_append : list):
        self._data = data
        self._mutations.append(mutation_append)
    def determineFileName(self) -> str:
        base_name = ""
        for mutation in self._mutations:
            base_name = base_name + mutation
        file_name = base_name + ".json"
        files_in_directory = os.listdir(self._root_dir)
        for i in range(1, 10_000):
            if(file_name not in files_in_directory):
                break
            if(file_name in files_in_directory):
                file_name = base_name + str(i) + ".json"
        return self._root_dir + file_name
    def setRootDir(self, root : str):
        self._root_dir = root
    def save(self):
        with open(self.determineFileName(), "w") as outfile:
            json.dump(self._data, outfile)
        pass
    def __str__(self):
        return str(self._data)