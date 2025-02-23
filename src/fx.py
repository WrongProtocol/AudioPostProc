from pedalboard import Pedalboard, Compressor, Distortion, HighShelfFilter, HighpassFilter, PeakFilter, Gain, Chorus, LadderFilter, Phaser, Convolution, Reverb, Delay, Limiter
from pedalboard.io import AudioFile
from buss_compressor import buss_compressor
from sum_audio import sum_audio_arrays

def process_instrumental(audio, samplerate):
    fxchain = Pedalboard([
        Compressor(threshold_db=-1.0, 
                   ratio=1.5, 
                   attack_ms=5.0, 
                   release_ms=100.0),
        HighpassFilter(cutoff_frequency_hz = 36),
        PeakFilter(cutoff_frequency_hz = 111, 
                   q = 0.8, 
                   gain_db = 2.7),
        PeakFilter(cutoff_frequency_hz = 406, 
                   q = 2.0, 
                   gain_db = -3.5),
        PeakFilter(cutoff_frequency_hz = 1434, 
                   q = 2.43, 
                   gain_db = -1.3),
        PeakFilter(cutoff_frequency_hz = 3007, 
                   q = 1.0, 
                   gain_db = -1.3),
        PeakFilter(cutoff_frequency_hz = 5220, 
                   q = 0.63, 
                   gain_db = -2.5),
        HighShelfFilter(cutoff_frequency_hz = 11000, 
                        gain_db = -4.3, 
                        q = 0.78),
        Distortion(drive_db=3),
        Gain(gain_db=3.0),
        Limiter(threshold_db=-0.1)
    ])

    effected = fxchain(audio, samplerate)
    return effected

def process_vocals(audio, samplerate):
    fxchain = Pedalboard([
        HighpassFilter(cutoff_frequency_hz = 100),
        PeakFilter(cutoff_frequency_hz = 271, 
                   q = 1.21, 
                   gain_db = -2.1),
        PeakFilter(cutoff_frequency_hz = 518, 
                   q = 0.31, 
                   gain_db = -0.6),
        PeakFilter(cutoff_frequency_hz = 949, 
                   q = 0.84, 
                   gain_db = -5.0),
        PeakFilter(cutoff_frequency_hz = 2696, 
                   q = 1.0, 
                   gain_db = -2.7),
        HighShelfFilter(cutoff_frequency_hz = 10334, 
                        gain_db = 1.1, 
                        q = 0.21),
        Delay(delay_seconds=0.06, 
              feedback=0, 
              mix=0.1),
        Reverb(room_size=0.5,
               damping=0.5,
               wet_level=0.2,
               dry_level=1.0,
               width=1.0,
               freeze_mode=0.0),
        Distortion(drive_db=.2),
        Gain(gain_db=3.0),
        Limiter(threshold_db=-0.1)
    ])

    effected = fxchain(audio, samplerate)
    return effected

def sum_audio(audio1, audio2):
    return sum_audio_arrays(audio1, audio2)

def process_buss(audio, samplerate):
    audio = buss_compressor(samplerate, audio, threshold_db=-20, ratio=4, attack_us=20000, release_ms=250, mix_percent=75)

    fxchain = Pedalboard([
        Limiter(threshold_db=-0.1)
    ])

    effected = fxchain(audio, samplerate)
    return effected

