import pedalboard
import numpy as np
from pedalboard import Compressor, Delay, Reverb, HighpassFilter

def fx_compression(audio, sr, threshold=-20.0, ratio=4.0, attack=0.01, release=0.1):
    """
    Apply a compression effect to the audio signal.
    Parameters:
      threshold: dB level where compression begins.
      ratio: Compression ratio (e.g., 4:1).
      attack: Attack time in seconds.
      release: Release time in seconds.
    """
    # Convert attack and release to milliseconds (as required by the effect).
    compressor = Compressor(
        threshold_db=threshold,
        ratio=ratio,
        attack_ms=int(attack * 1000),
        release_ms=int(release * 1000)
    )
    return compressor(audio, sr)

def fx_eq4(audio, sr, frequencies=[100, 500, 2000, 8000], gains=[0, 0, 0, 0], bandwidths=[1.0, 1.0, 1.0, 1.0]):
    """
    Apply a 4-band equalizer effect to the audio.
    Parameters:
      frequencies: A list of center frequencies (in Hz) for each band.
      gains: A list of gain values (in dB) for each band.
      bandwidths: A list of Q factors (bandwidths) for each band.
    Note: This function assumes that Pedalboard supports a 4-band EQ.
          If not, the function will print a warning and return the original audio.
    """
    try:
        # Hypothetical import and usage; adjust based on your Pedalboard version.
        from pedalboard import EQ
        eq = EQ()
        # Configure each EQ band.
        for freq, gain, bw in zip(frequencies, gains, bandwidths):
            eq.set_gain_at_frequency(freq, gain, q=bw)
        return eq(audio, sr)
    except ImportError:
        print("EQ effect not supported in this version of Pedalboard. Skipping EQ effect.")
        return audio

def fx_delay(audio, sr, delay_time=0.5, pan=0.5, wet=0.5):
    """
    Apply a delay effect to the audio signal.
    Parameters:
      delay_time: The delay time in seconds.
      pan: Stereo pan for the delayed signal (0.0 = left, 1.0 = right, 0.5 = center).
      wet: Mix level of the delayed signal (0.0 dry, 1.0 fully wet).
    Note: Pedalboard's Delay effect does not natively support panning.
          Here we apply a simple post-delay pan adjustment for stereo audio.
    """
    delay = Delay(delay_seconds=delay_time, feedback=0.3, mix=wet)
    delayed = delay(audio, sr)
    
    # If the audio is stereo, adjust the left/right levels to simulate panning.
    if delayed.shape[1] == 2:
        left = delayed[:, 0] * (1 - pan)
        right = delayed[:, 1] * pan
        delayed = np.stack([left, right], axis=1)
    return delayed

def fx_reverb(audio, sr, room_size=0.5, wet=0.5):
    """
    Apply a reverb effect to the audio signal.
    Parameters:
      room_size: Simulated size of the room (affects reverb tail).
      wet: Mix level of the reverberated signal (0.0 dry, 1.0 fully wet).
    Uses default parameters if not specified.
    """
    reverb = Reverb(room_size=room_size, mix=wet)
    return reverb(audio, sr)

# Additional example: high-pass filter to remove low-end rumble.
def fx_highpass(audio, sr, cutoff=80):
    """
    Apply a high-pass filter to the audio to remove unwanted low frequencies.
    Parameter:
      cutoff: Frequency (in Hz) below which frequencies will be attenuated.
    """
    highpass = HighpassFilter(cutoff_frequency_hz=cutoff)
    return highpass(audio, sr)
