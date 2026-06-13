import pygame

# setting class
class parameters():
        """
        
        """
        def __init__(self, procent):
            """
            
            """
            self.procent = procent
            self._frame = 30
            self._volume = 0.5
            self._resolution = (1980, 1020)

        def setFrame(self):
            """
            
            """
            self._frame = ((self.procent * 120) / 100) + self._frame
            return self._frame
        
        def setVolume(self):
            """
            
            """
            self._volume = ((self.procent) / 100)
            return self._volume
        
        def setResolution(self, resolution):
            """
            
            """
            if self._resolution == (1980, 1020):
                self._resolution = (1980, 1020)
            return self._resolution



    

