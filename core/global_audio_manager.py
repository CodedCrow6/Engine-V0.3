import pygame as pg
from core.config import sound_config

class GlobalAudioManager:
    def __init__(self, game):
        self.game = game
        self.audio_managers = []
        self.sound_fx_cache = []
        self.playlist_cache = []
        self.master_audio_config = sound_config
        self.volume = sound_config['Master Volume']
        self.muted = sound_config['Muted']


    def set_master_volume(self, volume):
        if self.volume != volume and volume > 0 and volume <= 100 and self.muted == False:
            self.volume = volume

    def mute(self):
        if self.muted :
            self.volume = 0

    def add_manager(self,managed_object,ID):
        audio_manager = 
