from pedalboard.io import AudioFile


def open_file(file_path, samplerate):
    with AudioFile(file_path).resampled_to(samplerate) as f:
        audio = f.read(f.frames)
    return audio

def save_file(audio, file_path, samplerate):
    with AudioFile(samplerate, 'w', file_path, audio.shape[0]) as f:
        f.write(audio)
