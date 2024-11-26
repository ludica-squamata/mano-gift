from engine.globs.event_dispatcher import EventDispatcher
from pygame.mixer import Sound, init as mixer_init
from os import path, listdir, getcwd


class SoundManager:
    sounds = {}

    @classmethod
    def init(cls):
        mixer_init(channels=1)
        base_ruta = path.join(getcwd(), 'data', 'sounds')
        for file in listdir(base_ruta):
            if file.endswith('.wav'):
                ruta = path.join(base_ruta, file)
                sound = Sound(ruta)
                cls.sounds[file.rstrip('.wav')] = sound

        EventDispatcher.register(cls.play_sound, 'PlaySound')

    @classmethod
    def play_sound(cls, event):
        if event.data['sound'] in cls.sounds:
            cls.sounds[event.data['sound']].play()

    @classmethod
    def play_direct_sound(cls, sound_name):
        if sound_name in cls.sounds:
            cls.sounds[sound_name].play()


SoundManager.init()
