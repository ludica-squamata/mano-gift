from engine.globs.event_dispatcher import EventDispatcher
from pygame.mixer import Sound, init as mixer_init
import pygame.mixer
from os import path, listdir, getcwd


class SoundManager:
    sounds = {}

    @classmethod
    def init(cls):
        mixer_init(channels=2)
        pygame.mixer.set_num_channels(1)
        base_ruta = path.join(getcwd(), 'data', 'sounds')
        for file in listdir(base_ruta):
            if file.endswith('.wav'):
                ruta = path.join(base_ruta, file)
                sound = Sound(ruta)
                cls.sounds[file.rstrip('.wav')] = sound

        EventDispatcher.register(cls.play_sound_event, 'PlaySound')

    @classmethod
    def play_sound_event(cls, event):
        if event.data['sound'] in cls.sounds:
            sound = cls.sounds[event.data['sound']]
            volume = float(event.data.get('volume', 1.0))
            sound.set_volume(volume)
            sound.play()

    @classmethod
    def play_sound_direct(cls, sound_name, volume=1.0):
        if sound_name in cls.sounds:
            sound = cls.sounds[sound_name]
            sound.set_volume(volume)
            sound.play()

    @classmethod
    def update(cls):
        pass


SoundManager.init()
