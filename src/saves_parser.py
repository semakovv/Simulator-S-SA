import json

class saveManager():
    """
    
    """
    def __init__(self):
        """
        
        """
        self.nodesStages = {}
        self.nodesMachines = {}
        self.save = {}
        self.stage = None
        self.jsonPathStages = "data/stages.json"
        self.jsonPathMachines = "data/machines.json"
        self.jsonPathSaves = "saves/save.json"

        with open(self.jsonPathSaves, 'r', encoding='utf-8') as f:
                self.save = json.load(f)
        with open(self.jsonPathStages, 'r', encoding='utf-8') as f:
                self.nodesStages = json.load(f)
        with open(self.jsonPathMachines, 'r', encoding='utf-8') as f:
                self.nodesMachines = json.load(f)

        self.countStages = len(self.nodesStages)
        # print(self.countStages)

    def _loadSave(self):
        """
        
        """
        for i in range(1, self.countStages):
            self.stage = self.nodesStages[f"stage{i}"]["name"]
            if self.nodesStages[self.stage]["result"] == "True" and self.nodesMachines[self.stage]["result"] == "True":
                continue
            if self.nodesStages[self.stage]["result"] == "False" or self.nodesMachines[self.stage]["result"] == "False":
                self.save["stage"] = self.nodesStages[self.stage]["name"]
                break
            if self.nodesStages[self.stage]["result"] == "End" and self.nodesMachines[self.stage]["result"] == "End":
                self.save["stage"] = "stage1"
                self._resetSave()
        with open(self.jsonPathSaves, 'w', encoding='utf-8') as f:
                json.dump(self.save, f, indent=4)
        # print(self.save, self.stage)

    def downloadSave(self):
        """
        
        """
        with open(self.jsonPathStages, 'r', encoding='utf-8') as f:
            self.nodesStages = json.load(f)
        with open(self.jsonPathMachines, 'r', encoding='utf-8') as f:
            self.nodesMachines = json.load(f)
        self._loadSave()
        return self.save["stage"]
    
    def downloadGameEvent(self):
        with open(self.jsonPathStages, 'r', encoding='utf-8') as f:
            self.nodesStages = json.load(f)
        with open(self.jsonPathMachines, 'r', encoding='utf-8') as f:
            self.nodesMachines = json.load(f)
        self.stage = self.downloadSave()
        if self.nodesStages[self.stage]["result"] == "False":
            return "dialog"
        elif self.nodesMachines[self.stage]["result"] == "False":
            return "desktop"
    
    def _resetSave(self):
        """
         
        """
        with open(self.jsonPathSaves, 'w', encoding='utf-8') as f:
                json.dump(self.save, f, indent=4)
        with open('data/machines_backup.json', 'r') as src:
            backup = json.load(src)
        with open('data/machines.json', 'w') as dst:
            json.dump(backup, dst, indent=4)
        with open('data/stages_backup.json', 'r') as src:
            backup = json.load(src)
        with open('data/stages.json', 'w') as dst:
            json.dump(backup, dst, indent=4)

