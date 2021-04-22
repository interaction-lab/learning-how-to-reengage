import math
import pyaudio     #sudo apt-get install python-pyaudio
import playsound    #pip install playsound

PyAudio = pyaudio.PyAudio     #initialize pyaudio

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



    def generateWhiteNoise(self, level):
        freq = level * 200
        for x in xrange(self.numframe):
            self.wave = self.wave + chr(int(math.sin(x / ((self.Bitrate / freq) / math.pi)) * 127 + 128))
        for x in xrange(self.restframe):
            self.wave = self.wave + chr(128)
        stream.write(self.wave)
        stream.stop_stream()
    def playClick(self):
        playsound.playsound('click.mp3', True)

noi = noise()
#play one Click
noi.playClick()
#play a white noise at a level
noi.generateWhiteNoise(1)
