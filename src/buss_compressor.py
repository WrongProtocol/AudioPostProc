# Carmine Silano
# Feb 23, 2025
# using techniques learned from Thomas Scott Stillwell

import numpy as np
from pedalboard import AudioFile

def buss_compressor(samplerate, audio_file, threshold_db=-20, ratio=4, attack_us=20000, release_ms=250, mix_percent=100):
    """
    Apply a 4:1 compression ratio using dynamic range compression.
    
    Parameters:
        samplerate (int): The sample rate of the audio.
        audio_file (AudioFile): A Pedalboard AudioFile object.
        threshold_db (float): Compression threshold in dB.
        ratio (float): Compression ratio (default 4:1).
        attack_us (float): Attack time in microseconds (default 20ms).
        release_ms (float): Release time in milliseconds (default 250ms).
        mix_percent (float): Wet/dry mix percentage (default 100% compressed).
    
    Returns:
        np.ndarray: The compressed audio signal.
    """
    # Constants
    log2db = 8.6858896380650365530225783783321  # 20 / ln(10)
    db2log = 0.11512925464970228420089957273422  # ln(10) / 20 

    # Convert parameters
    attack_time = attack_us / 1000000  # Convert µs to seconds
    release_time = release_ms / 1000  # Convert ms to seconds
    mix = mix_percent / 100

    # Coefficients for smoothing
    atcoef = np.exp(-1 / (attack_time * samplerate))
    relcoef = np.exp(-1 / (release_time * samplerate))

    # Compression threshold in linear scale
    threshv = np.exp(threshold_db * db2log)
    
    # Load audio
    with audio_file as f:
        audio = f.read(f.frames)

    # Initialize state variables
    rundb = 0
    runave = 0

    # Process stereo audio sample-by-sample
    output_audio = np.copy(audio)

    for i in range(audio.shape[0]):
        ospl0, ospl1 = audio[i, 0], audio[i, 1]  # Original samples (L & R)
        aspl0, aspl1 = abs(ospl0), abs(ospl1)  # Absolute values

        # Compute signal level
        maxspl = max(aspl0, aspl1) ** 2
        runave = maxspl + relcoef * (runave - maxspl)  # Smooth signal tracking
        det = np.sqrt(max(0, runave))  # RMS estimate

        # Compute gain reduction
        overdb = max(0, log2db * np.log(det / threshv))

        # Attack and release smoothing
        if overdb > rundb:
            rundb = overdb + atcoef * (rundb - overdb)
        else:
            rundb = overdb + relcoef * (rundb - overdb)

        # Compute compression gain reduction
        gr = -rundb * (ratio - 1) / ratio
        grv = np.exp(gr * db2log)  # Convert dB to linear gain

        # Apply gain reduction with mix control
        output_audio[i, 0] = ospl0 * grv * mix + ospl0 * (1 - mix)
        output_audio[i, 1] = ospl1 * grv * mix + ospl1 * (1 - mix)

    return output_audio
