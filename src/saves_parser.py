import json

class saveManager():
    """
    
    """
    def __init__(self):
        """
        
        """
        self.stage = "end"
        self.jsonPath = "saves/save.json"
    
    def loadSave(self):
        """
        
        """
        with open(self.jsonPath, 'r', encoding='utf-8') as f:
                self.stage = json.load(f)

    def downloadSaves(self):
        """
        
        """
        return self.stage
    
    def resetSaves(self):
        """
         
        """
        if self.stage == "end":
            with open('data/mashines_backup.json', 'r') as src:
                backup = json.load(src)
            with open('data/mashines.json', 'w') as dst:
                json.dump(backup, dst, indent=4)
            self.stage = "stage1"