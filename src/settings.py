# setting class
class parameters():
        """
        
        """
        def __init__(self):
            """
            
            """
            self.frame = 60
            self.volume = 0.0

        def getFrame(self):
            """
            
            """
            return self.frame

        def getVolume(self):
            """
            
            """
            return self.volume

        def setFrame(self, procent):
            """
            
            """
            self.frame = int(30 + (procent / 100) * (144 - 30))
            return self.frame
        
        def setVolume(self, procent):
            """
            
            """
            self.volume = procent / 100.0
            return self.volume


    

