from pedalboard.io import AudioFile

def open_file(file_path, samplerate):
    with AudioFile(file_path).resampled_to(samplerate) as f:
        audio = f.read(f.frames)
    return audio

def save_file(audio, file_path, samplerate, channels=1):
    with AudioFile(samplerate, 'w', file_path, channels) as f:
        f.write(audio)
