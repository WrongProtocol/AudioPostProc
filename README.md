# Audio Post-Processing with Pedalboard and Custom Functions

This project provides a set of tools for audio post-processing using the Pedalboard library and some custom audio processing functions. 
It includes various audio effects, dynamic range compression, and stereo upmixing. The project is designed to process instrumental and vocal audio files, sum them together, and apply a buss compressor to the final mix.

## Project Structure

```
.gitignore
Dockerfile
input_files/
    i.wav
    v.wav
output/
    processed_buss.wav
    processed_instrumental.wav
    processed_vocal.wav
    summed.wav
src/
    app.py
    buss_compressor.py
    fx.py
    stereo_upmix.py
    sum_audio.py
    utils.py
```

## Files and Directories

- **input_files/**: Directory containing input audio files (`i.wav` for instrumental and `v.wav` for vocals).
- **output/**: Directory where processed audio files will be saved.
- **src/**: Directory containing the source code for audio processing.

### Source Files

- **src/app.py**: Main script that orchestrates the audio processing workflow.
- **src/buss_compressor.py**: Contains the `buss_compressor` function that applies dynamic range compression using Numba for JIT acceleration.
- **src/fx.py**: Defines various audio effects chains for processing instrumental and vocal audio.
- **src/stereo_upmix.py**: Implements the `MonoToStereoUpmixer` class for upmixing mono signals to stereo.
- **src/sum_audio.py**: Provides the `sum_audio_arrays` function to sum (mix) two audio signals.
- **src/utils.py**: Utility functions for opening and saving audio files.

## Dependencies

- Python 3.9
- Numba
- NumPy
- SciPy
- SoundFile
- Librosa
- Pedalboard

## Usage

1. Place your input audio files (`i.wav` and `v.wav`) in the input_files directory.
2. Run the main script:

```sh
python src/app.py
```

3. Processed audio files will be saved in the output directory.

## Functions and Classes

### `buss_compressor` (in src/buss_compressor.py)

Applies dynamic range compression to an audio signal using a buss compressor model.

### `MonoToStereoUpmixer` (in src/stereo_upmix.py)

Upmixes a mono signal to stereo using a delay and sum technique.

### `sum_audio_arrays` (in src/sum_audio.py)

Sums (mixes) two NumPy audio arrays together and returns the result.

### `process_instrumental` and `process_vocals` (in src/fx.py)

Defines the effects chains for processing instrumental and vocal audio.

### `open_file` and `save_file` (in src/utils.py)

Utility functions for opening and saving audio files.

## Author

WrongProtocol
