# setting class
class parameters():
        """
        
        """
        def __init__(self):
            """
            
            """
            self.frame = 60
            self.volume = 0.1
            self.resolution = (1920, 1080)

        def getFrame(self):
            """
            
            """
            return self.frame

        def getVolume(self):
            """
            
            """
            return self.volume
        
        def getResolution(self):
            """
            
            """
            return self.resolution

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
        
        def setResolution(self):
            """
            
            """
            if self.resolution == (1920, 1080):
                self.resolution = (1920, 1080)
            return self.resolution



    

