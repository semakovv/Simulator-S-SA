import pygame
import button

# setting class
class parameters():
        """
        
        """
        def __init__(self):
            """
            
            """
            self._frame = 60
            self._volume = 0.0
            self._resolution = (1980, 1020)

        def setFrame(self, frame):
            """
            
            """
            if 30 <= frame <= 144:
                self._frame = frame
            return self._frame

        def setVolume(self, volume):
            """
            
            """
            if 0.0 <= volume <= 1.0:
                self._volume = volume
            return self._volume
        
        def setResolution(self, resolution):
            """
            
            """
            pass

param = parameters()
param.setFrame(60)


    

