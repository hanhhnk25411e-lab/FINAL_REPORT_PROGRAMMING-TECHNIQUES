import json
import os

class FileFactory:
    def writeData(self, path, arrData):
        data_to_save = [item.__dict__ for item in arrData]
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, default=str, ensure_ascii=False, indent=4)

    def readData(self,path,ClassName):
        if os.path.isfile(path) == False:
            return []
        with open(path, "r", encoding='utf-8') as file:
            content = file.read()
        if content.strip() == "":
            return []
        self.arrData = json.loads(content, object_hook=lambda d: ClassName(**d))
        return self.arrData