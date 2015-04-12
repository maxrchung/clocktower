import pygame
from pygame.locals import *
pygame.init()

class SoundManager:

    def __init__(self):
        pygame.mixer.init()
        self.musicIsPlaying = False
        self.musicIsPaused = False

        ## Play background music from __init__()

    def playSoundEffect(self, soundFile):
        soundEffect = pygame.mixer.Sound(soundFile)
        pygame.mixer.Sound.play(soundEffect)

    def playMusic(self, musicFile, numberOfLoops):
        pygame.mixer.music.load(musicFile)
        pygame.mixer.music.play(numberOfLoops)
        self.musicIsPlaying = True

    def setVolume(self, volume):
        if self.musicIsPlaying:
            pygame.mixer.music.set_volume(volume)
        else:
            print("Cannot set volume")
    
    def stopMusic(self):
        if self.musicIsPlaying:
            pygame.mixer.music.stop()
            self.musicIsPlaying = False
        else:
            print("Cannot stop.")

    def pauseMusic(self):
        if self.musicIsPlaying:
            pygame.mixer.music.pause()
            self.musicIsPlaying = False
            self.musicIsPaused = True
        else:
            print("Cannot pause.")

    def unPauseMusic(self):
        if self.musicIsPaused:
            pygame.mixer.music.unpause()
            self.musicIsPlaying = True
            self.musicIsPaused = False
        else:
            print("Cannot unpause.")

    def fadeOut(self, time):
        if self.musicIsPlaying:
            pygame.mixer.fadeout(time)
            self.musicIsPlaying = False
        else:
            print("Cannot fade out.")


