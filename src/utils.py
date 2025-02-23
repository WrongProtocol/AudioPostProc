import librosa
import soundfile as sf

def open_file(file_path):
    """
    Load an audio file (.wav or .mp3) and return the audio data
    and sample rate. The returned audio is in shape (n_samples, channels)
    which is the expected format for Pedalboard processing.
    """
    # Load audio using librosa. Set mono=False to preserve stereo if present.
    audio, sr = librosa.load(file_path, sr=None, mono=False)
    
    # librosa.load returns mono as 1D and stereo as (channels, n_samples).
    # Convert to (n_samples, channels) if necessary.
    if audio.ndim == 1:
        audio = audio[:, None]
    elif audio.shape[0] > audio.shape[1]:
        # Likely in (channels, n_samples) format; transpose it.
        audio = audio.T
    return audio, sr

def save_file(audio, sr, file_path):
    """
    Save the processed audio to a file (.wav or .mp3). The file format
    is inferred from the file extension.
    """
    sf.write(file_path, audio, sr)
