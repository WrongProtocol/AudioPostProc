from pedalboard import Pedalboard, Compressor, Gain, Chorus, LadderFilter, Phaser, Convolution, Reverb, Delay, Limiter
from pedalboard.io import AudioFile

def process_instrumental(audio, samplerate):
    fxchain = Pedalboard([
        Compressor(threshold_db=-18.0, 
                   ratio=3.0, 
                   attack_ms=5.0, 
                   release_ms=100.0),
        #Delay(delay_time=0.4, pan=0.3, wet=0.5),
        #Limiter()
    ])

    effected = fxchain(audio, samplerate)
    return effected