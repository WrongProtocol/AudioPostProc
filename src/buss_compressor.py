# Carmine Silano
# Feb 23, 2025
# using techniques learned from Thomas Scott Stillwell

import numpy as np

def buss_compressor(samplerate, audio_array, threshold_db=-20, ratio=4, attack_us=20000, release_ms=250, mix_percent=100):
    """
    Apply compression ratio using dynamic range compression.

    Parameters:
        samplerate (int): The sample rate of the audio.
        audio_array (np.ndarray): A NumPy array containing the audio signal (NxC, where N=frames, C=channels).
        threshold_db (float): Compression threshold in dB.
        ratio (float): Compression ratio (default 4:1).
        attack_us (float): Attack time in microseconds (default 20ms).
        release_ms (float): Release time in milliseconds (default 250ms).
        mix_percent (float): Wet/dry mix percentage (default 100% compressed).

    Returns:
        np.ndarray: The compressed audio signal.
    """
    # Constants
    log2db = 8.6858896380650365530225783783321  # Conversion factor from linear to dB
    db2log = 0.11512925464970228420089957273422  # Conversion factor from dB to linear

    # Convert parameters
    attack_time = attack_us / 1_000_000  # Convert attack time from microseconds to seconds
    release_time = release_ms / 1_000  # Convert release time from milliseconds to seconds
    mix = mix_percent / 100  # Normalize the mix percentage to a fraction

    # Coefficients for smoothing (attack and release)
    atcoef = np.exp(-1 / (attack_time * samplerate))  # Attack coefficient
    relcoef = np.exp(-1 / (release_time * samplerate))  # Release coefficient

    # Compression threshold in linear scale
    threshv = np.exp(threshold_db * db2log)  # Convert threshold from dB to linear scale

    # Ensure input is stereo (Nx2)
    if len(audio_array.shape) != 2 or audio_array.shape[1] != 2:
        raise ValueError("Input audio_array must be a stereo (Nx2) NumPy array.")

    # Initialize state variables for signal tracking
    rundb = 0  # Running average of the signal level in dB
    runave = 0  # Running average of the squared signal level

    # Create a copy of the original audio to store the output
    output_audio = np.copy(audio_array)

    # Process each sample of stereo audio (left and right channels)
    for i in range(audio_array.shape[0]):
        ospl0, ospl1 = audio_array[i, 0], audio_array[i, 1]  # Original samples (L & R)
        aspl0, aspl1 = abs(ospl0), abs(ospl1)  # Absolute values of the original samples

        # Compute the signal level
        maxspl = max(aspl0, aspl1) ** 2  # Maximum squared value between left and right channels
        runave = maxspl + relcoef * (runave - maxspl)  # Smoothed running average of the squared signal level
        det = np.sqrt(max(0, runave))  # RMS estimate of the signal level

        # Compute the gain reduction needed to bring the signal below the threshold
        overdb = max(0, log2db * np.log(det / threshv))  # Gain reduction in dB if signal is above threshold

        # Apply attack and release smoothing to the gain reduction
        if overdb > rundb:
            rundb = overdb + atcoef * (rundb - overdb)  # Attack phase
        else:
            rundb = overdb + relcoef * (rundb - overdb)  # Release phase

        # Compute the compression gain reduction
        gr = -rundb * (ratio - 1) / ratio  # Gain reduction in dB
        grv = np.exp(gr * db2log)  # Convert gain reduction from dB to linear scale

        # Apply the gain reduction with mix control (parallel compression)
        output_audio[i, 0] = ospl0 * grv * mix + ospl0 * (1 - mix)  # Left channel output
        output_audio[i, 1] = ospl1 * grv * mix + ospl1 * (1 - mix)  # Right channel output

    return output_audio
