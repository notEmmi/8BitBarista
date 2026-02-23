from enum import Enum
from pygame import mixer

# master, music, sfx
volumes = [.5, 1, 1]

# rain, shaders, shake
booleanSettings = [True, True, False]

class TextureQuality(Enum):
    Low = 0,
    Med = 1,
    High = 2

textureQualitySettings = [False, False, True]

muteMasterVolumeToggleContainer = [0.0]

def updateMasterVolume(value):
    if not isinstance(value, float) and not isinstance(value, int): return
    volumes[0] = value
    print(f"master volume (volumes[0]): {volumes[0]}")
    mixer.music.set_volume(volumes[0] * volumes[1])
    print(f"updated music to {volumes[0] * volumes[1]} (volumes[0] * volumes[1])")
    for i in range(mixer.get_num_channels()):
        mixer.Channel(i).set_volume(volumes[0] * volumes[2])
        print(f"updated SFX to {volumes[0] * volumes[2]} (volumes[0] * volumes[2])")

def updateSFXVolume(value):
    pass
    """
    if not isinstance(value, float) and not isinstance(value, int): return
    volumes[2] = value
    for i in range(mixer.get_num_channels()):
        mixer.Channel(i).set_volume(volumes[0] * volumes[2])
        print(f"updated SFX to {volumes[0] * volumes[2]} (volumes[0] * volumes[2])")
    """

def updateMusicVolume(value):
    if not isinstance(value, float) and not isinstance(value, int): return
    volumes[1] = value
    mixer.music.set_volume(volumes[0] * volumes[1])
    print(f"updated music to {volumes[0] * volumes[1]} (masterVolume * volumes[1])")

def updateTextureQuality(quality):
    if not isinstance(quality, str): return
    for element in textureQualitySettings: element = False
    desiredIndex = TextureQuality[quality].value
    if isinstance(desiredIndex, tuple): textureQualitySettings[desiredIndex[0]] = True
    else: textureQualitySettings[desiredIndex] = True
    print(f"updated texture quality to {TextureQuality[quality].name}")

def updateRainAnimations(value):
    if not isinstance(value, bool): return
    booleanSettings[0] = value
    print(f"updated rainAnimations to {booleanSettings[0]}")

def updateShaders(value):
    if not isinstance(value, bool): return
    booleanSettings[1] = value
    print(f"updated shaders to {booleanSettings[1]}")

def updateScreenShake(value):
    if not isinstance(value, bool): return
    booleanSettings[2] = value
    print(f"updated rainAnimations to {booleanSettings[2]}")

def toggleMuteMasterVolume():
    if (volumes[0] != 0.0):
        muteMasterVolumeToggleContainer[0] = volumes[0]
        volumes[0] = 0.0
    else:
        tempMasterVolume = muteMasterVolumeToggleContainer[0]
        if (volumes[0] != 0.0): muteMasterVolumeToggleContainer[0] = volumes[0]
        volumes[0] = tempMasterVolume
    updateMasterVolume(volumes[0])