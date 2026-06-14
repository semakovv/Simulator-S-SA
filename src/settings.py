# setting class
class parameters():
        """
        
        """
        def __init__(self):
            """
            
            """
            self._frame = 60
            self._volume = 0.5
            self._resolution = (1920, 1080)

        def getFrame(self):
            return self._frame

        def getVolume(self):
            return self._volume

        def setFrame(self, procent):
            """
            
            """
            self._frame = int(30 + (procent / 100) * (144 - 30))
            return self._frame
        
        def setVolume(self, procent):
            """
            
            """
            self._volume = procent / 100.0
            return self._volume
        
        def setResolution(self):
            """
            
            """
            if self._resolution == (1920, 1080):
                self._resolution = (1920, 1080)
            return self._resolution



    

