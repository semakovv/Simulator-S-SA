import json

class saveManager():
    """
    
    """
    def __init__(self):
        """
        
        """
        self.nodesStages = {}
        self.nodesMashnes = {}
        self.save = {}
        self.stage = None
        self.jsonPathStages = "data/stages.json"
        self.jsonPathMashines = "data/mashines.json"
        self.jsonPathSaves = "saves/save.json"

        with open(self.jsonPathSaves, 'r', encoding='utf-8') as f:
                self.save = json.load(f)
        with open(self.jsonPathStages, 'r', encoding='utf-8') as f:
                self.nodesStages = json.load(f)
        with open(self.jsonPathMashines, 'r', encoding='utf-8') as f:
                self.nodesMashnes = json.load(f)

        self.countStages = len(self.nodesStages)
        # print(self.countStages)

    def _loadSave(self):
        """
        
        """
        for i in range(1, self.countStages):
            self.stage = self.nodesStages[f"stage{i}"]["name"]
            if self.nodesStages[self.stage]["result"] == "True" and self.nodesMashnes[self.stage]["result"] == "True":
                continue
            if self.nodesStages[self.stage]["result"] == "False" or self.nodesMashnes[self.stage]["result"] == "False":
                self.save["stage"] = self.nodesStages[self.stage]["name"]
                break
            if self.nodesStages[self.stage]["result"] == "End" and self.nodesMashnes[self.stage]["result"] == "End":
                self.save["stage"] = "stage1"
                self._resetSave()
        with open(self.jsonPathSaves, 'w', encoding='utf-8') as f:
                json.dump(self.save, f, indent=4)
        # print(self.save, self.stage)

    def downloadSave(self):
        """
        
        """
        self._loadSave()
        return self.save["stage"] 
    
    def _resetSave(self):
        """
         
        """
        with open(self.jsonPathSaves, 'w', encoding='utf-8') as f:
                json.dump(self.save, f, indent=4)
        with open('data/mashines_backup.json', 'r') as src:
            backup = json.load(src)
        with open('data/mashines.json', 'w') as dst:
            json.dump(backup, dst, indent=4)
        with open(self.jsonPathSaves, 'w', encoding='utf-8') as f:
            json.dump(self.save, f, indent=4)