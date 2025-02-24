# Carmine Silano
# Feb 24, 2025
# Implement a distortion exciter effect that applies dynamic gain control combined with filtering.
# The effect is applied to a stereo audio signal and returns the processed audio.
# The technique is based on the work of Michael Gruhn.
# Rewritten to use Numba for JIT acceleration which made a HUGE difference in speed.

import numpy as np
from numba import njit

@njit
def distortion_exciter(audio, srate, drive=16.4, distortion=33, highpass=5000, wet_mix=-6, dry_mix=0):
    """
    Process a stereo audio signal by applying dynamic gain control combined with filtering,
    resulting in a mix of the original (dry) and processed (wet) signals.
    
    Parameters:
      audio    : ndarray
                 Input stereo audio array with shape (n_samples, 2).
      srate    : int or float
                 The sampling rate in Hz.
      drive    : float, optional
                 Drive level in dB. (Default is 16.4)
      distortion : float, optional
                 Distortion parameter on a 0-100 scale. (Default is 33)
      highpass : float, optional
                 Highpass filter cutoff frequency in Hz. (Default is 5000 Hz)
      wet_mix  : float, optional
                 Wet signal mix level in dB. (Default is -6 dB)
      dry_mix  : float, optional
                 Dry (unprocessed) signal mix level in dB. (Default is 0 dB)
                 
    Returns:
      ndarray: Processed stereo audio with the same shape as the input.
    """
    # Constants for decibel/exponential calculations.
    c = 8.65617025
    threshDB = -drive
    thresh = np.exp(threshDB / c)
    ratio = 1.0 / 20.0

    # Compute the release factor based on the distortion parameter.
    release = np.exp(-60 / (np.power((1 - distortion) / 100, 3) * 500 * srate / 1000) / c)
    
    # Calculate filter coefficients for a cascaded highpass filter.
    blp = -np.exp(-2 * np.pi * highpass * 3 / srate)
    alp = 1 + blp

    # Compute wet and dry mix factors.
    wet = np.exp(wet_mix / c) / np.exp((threshDB - threshDB * ratio) / c)
    dry = np.exp(dry_mix / c)
    
    gain = 1.0
    seekGain = 1.0

    # Initialize filter state variables for three filter stages.
    t00 = 0.0
    t01 = 0.0
    t10 = 0.0
    t11 = 0.0
    t20 = 0.0
    t21 = 0.0

    n_samples = audio.shape[0]
    for i in range(n_samples):
        # Extract left and right channel samples.
        spl0 = audio[i, 0]
        spl1 = audio[i, 1]
        
        # --- Filter Stage 1 ---
        t00 = alp * spl0 - blp * t00
        s0 = t00
        t01 = alp * spl1 - blp * t01
        s1 = t01
        
        # --- Filter Stage 2 ---
        t10 = alp * s0 - blp * t10
        s0 = t10
        t11 = alp * s1 - blp * t11
        s1 = t11
        
        # --- Filter Stage 3 ---
        t20 = alp * s0 - blp * t20
        s0 = spl0 - t20
        t21 = alp * s1 - blp * t21
        s1 = spl1 - t21
        
        # Compute the instantaneous amplitude.
        rms = abs(spl0)
        if abs(spl1) > rms:
            rms = abs(spl1)
        
        # Compute the desired gain based on the signal amplitude.
        if rms > thresh:
            seekGain = np.exp((threshDB + (np.log(rms) * c - threshDB) * ratio) / c) / rms
        else:
            seekGain = 1.0
        
        gain = min(gain, release * seekGain)
        
        # Mix the dry (original) and wet (processed) signals.
        audio[i, 0] = spl0 * dry + s0 * gain * wet
        audio[i, 1] = spl1 * dry + s1 * gain * wet

    return audio
