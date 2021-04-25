import math
import time
import pyaudio     #sudo apt-get install python-pyaudio
import playsound    #pip install playsound
import pygame
#from audioplayer import AudioPlayer
PyAudio = pyaudio.PyAudio     #initialize pyaudio
pygame.mixer.init()


class noise:
    def __init__(self, samplerate = 42100,length = 1):
        self.Bitrate = samplerate  # number of frames per second/frameset.
        self.frequency = 500
        self.length = length

        self.numframe = int ( self.Bitrate * self.length)
        self.restframe = self.numframe % self.Bitrate
        #use pyaudio to play white noise stream
        self.p = PyAudio()
        self.stream = self.p.open(format = self.p.get_format_from_width(1),
                channels = 1,
                rate = self.Bitrate,
                output = True)

        self.wave = ''



    # lvl is the base multiplier for frequency (pitch, by 200)
    # generates a sign wave at the frequency and add to wave
    # alternate between 50% to 100% (0.5 frequency vs 1 frequency)
    # length of segment is defined in initialization
    def generateWhiteNoise(self, level):
        freq = level * 200
        for x in iter(range(int(self.numframe/4))):
            self.wave = self.wave + chr(int(math.sin(x / ((self.Bitrate / freq) / math.pi)) * 127 + 128))

        for x in iter(range(int(self.numframe/4))):
            self.wave = self.wave + chr(int(math.sin(x / ((self.Bitrate / freq/2) / math.pi)) * 127 + 128))

        for x in iter(range(int(self.numframe/4))):
            self.wave = self.wave + chr(int(math.sin(x / ((self.Bitrate / freq) / math.pi)) * 127 + 128))

        for x in iter(range(int(self.numframe/4))):
            self.wave = self.wave + chr(int(math.sin(x / ((self.Bitrate / freq/2) / math.pi)) * 127 + 128))

        self.stream.write(self.wave)
        #self.stream.stop_stream()
    # def playClick(self):
    #     # playsound.playsound('click.mp3', True)
    #     AudioPlayer("click.mp3").play(block=True)
def playClickForSec(times = 1,lvl = 1):
        if lvl == 1:
            pygame.mixer.music.load("click_slow.mp3")
        elif (lvl == 2):
            pygame.mixer.music.load("click.mp3")
        elif (lvl == 3):
            pygame.mixer.music.load("click_fast.mp3")
        pygame.mixer.music.play(-1, 0.0)
        time.sleep(times)


noi = noise()
#play one Click
# playClickForSec(1,1)
# playClickForSec(2,2)
# playClickForSec(3,3)
#play a white noise at a level
noi.generateWhiteNoise(1)

# pygame.mixer.music.play(-1, 0.0)
# time.sleep(5)
