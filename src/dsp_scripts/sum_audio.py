# Carmine Silano
# Feb 23, 2025
# Summing two AudioFile objects together and returning an AudioFile object.

import numpy as np
def sum_audio_arrays(audio1, audio2, normalize=True):
    """
    Sum (mix) two NumPy audio arrays together and return the result.
    
    Parameters:
        audio1 (np.ndarray): First audio signal (NxC, where N=frames, C=channels).
        audio2 (np.ndarray): Second audio signal (NxC, where N=frames, C=channels).
        normalize (bool): If True, normalizes the mixed audio to prevent clipping.
    
    Returns:
        np.ndarray: The mixed audio signal as a NumPy array.
    """
    # Ensure both files have the same number of channels
    if audio1.shape[1] != audio2.shape[1]:
        raise ValueError("Number of channels do not match between audio arrays.")

    # Determine the maximum length
    max_len = max(audio1.shape[0], audio2.shape[0])

    # Pad or trim the shorter array to match the length
    def match_length(audio, target_length):
        if audio.shape[0] < target_length:
            pad_amount = target_length - audio.shape[0]
            return np.pad(audio, ((0, pad_amount), (0, 0)), mode='constant')
        else:
            return audio[:target_length]

    audio1 = match_length(audio1, max_len)
    audio2 = match_length(audio2, max_len)

    # Sum the two audio signals
    mixed_audio = audio1 + audio2

    # Normalize if necessary (prevent clipping)
    if normalize:
        peak = np.max(np.abs(mixed_audio))
        if peak > 1.0:
            mixed_audio /= peak

    return mixed_audio