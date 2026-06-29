def setting():
    window.blit(backGround, (0, 0))
    volumeProcent = volumeButton.move(window, "volume")
    frameProcent = frameButton.move(window, "frame")
    gameSettings.setVolume(volumeProcent)
    gameSettings.setFrame(frameProcent)
    volume = gameSettings.getVolume()
    soundMenu.set_volume(volume)
    soundGame.set_volume(volume)
    if menuButton.press(window):
        return "menu"
    return "setting"