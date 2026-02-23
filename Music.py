from pygame import mixer

class Music:
    def __init__(self, track):
         super().__init__()
         self.track = track
         mixer.init()
         mixer.music.load(self.track)
         mixer.music.play()