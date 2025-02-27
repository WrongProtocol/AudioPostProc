# Audio Post Processing using PedalBoard and Custom DSP Scripts

## Overview
This project focuses on audio post-processing using the PedalBoard library and custom Digital Signal Processing (DSP) scripts. The goal is to enhance and manipulate audio signals for various applications. This project was developed for post-processing low-quality generative music.

## Features
- **PedalBoard Integration**: Utilize the PedalBoard library to chain multiple audio effects.
- **Custom DSP Scripts**: Implement custom DSP algorithms to process audio signals.
- **Flexible Processing**: Easily switch between different effects and processing chains.

## Requirements
- Python 3.7+
- PedalBoard library
- NumPy
- SciPy

## Files and Directories

- **input_files/**: Directory containing input audio files (`i.wav` for instrumental and `v.wav` for vocals).
- **output/**: Directory where processed audio files will be saved.
- **src/**: Directory containing the source code for audio processing.

### Source Files

- **src/app.py**: Main script that orchestrates the audio processing workflow.
- **src/fx.py**: Defines various audio effects chains for processing instrumental and vocal audio.
- **src/utils.py**: Utility functions for opening and saving audio files.
- **src/dsp_scripts/buss_compressor.py**: Contains the [`buss_compressor`](src/dsp_scripts/buss_compressor.py) function that applies dynamic range compression using Numba for JIT acceleration.
- **src/dsp_scripts/distortion_exciter.py**: Contains the [`distortion_exciter`](src/dsp_scripts/distortion_exciter.py) function for applying distortion and excitation effects, JIT for acceleration.
- **src/dsp_scripts/saturator.py**: Contains the [`dynamic_saturator`](src/dsp_scripts/saturator.py) function for applying dynamic saturation effects.
- **src/dsp_scripts/stereo_upmix.py**: Implements the [`MonoToStereoUpmixer`](src/dsp_scripts/stereo_upmix.py) class for upmixing mono signals to stereo. JIT for acceleration.
- **src/dsp_scripts/sum_audio.py**: Provides the [`sum_audio_arrays`](src/dsp_scripts/sum_audio.py) function to sum (mix) two audio signals.

### Docker
The docker is just a basic environment to run code in (because I work on a windows box).   
I usually mount my code folder to /app
So then, I'd run this with python /app/src/app.py

