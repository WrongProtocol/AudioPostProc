#!/usr/bin/env python 

import os
from fx import process_instrumental, process_vocals, sum_audio, process_buss
import numpy as np
from utils import open_file, save_file

# Define input and output file paths.
vocal_file = "../input_files/v.wav"
instrumental_file = "../input_files/i.wav"
output_vocal_file = "../output/processed_vocal.wav"
output_instrumental_file = "../output/processed_instrumental.wav"
output_summed_file = "../output/summed.wav"
output_buss_file = "../output/processed_buss.wav"
samplerate = 44100.0

# Ensure the output directory exists
output_dir = os.path.dirname(output_instrumental_file)
os.makedirs(output_dir, exist_ok=True)

inst_audio = open_file(instrumental_file, samplerate)
print("Inst Shape at input:", inst_audio.shape)
print("Inst Type at input:", inst_audio.dtype)
print("Inst Max at input:", np.max(inst_audio))
print("Inst Min at input:", np.min(inst_audio))

inst_processed = process_instrumental(inst_audio, samplerate)
print("Inst Shape after processing:", inst_processed.shape)
print("Inst Type after processing:", inst_processed.dtype)
print("Inst Max after processing:", np.max(inst_processed))
print("Inst Min after processing:", np.min(inst_processed))

vocal_audio = open_file(vocal_file, samplerate)
print("Vox Shape at input:", vocal_audio.shape)
print("Vox Type at input:", vocal_audio.dtype)
print("Vox Max at input:", np.max(vocal_audio))
print("Vox Min at input:", np.min(vocal_audio))

vocal_processed = process_vocals(vocal_audio, samplerate) 
print("Vox Shape after processing:", vocal_processed.shape)
print("Vox Type after processing:", vocal_processed.dtype)
print("Vox Max after processing:", np.max(vocal_processed))
print("Vox Min after processing:", np.min(vocal_processed))

summed_audios = sum_audio(inst_processed, vocal_processed)
print("summed_audios shape:", summed_audios.shape)

#reshape data
summed_audios = np.squeeze(summed_audios)  # Remove dimensions of size 1
print("Summed audio After squeeze:", summed_audios.shape)

if len(summed_audios.shape) == 1:  # If mono (N,)
    print("audios were mono, stacking to make stereo")
    summed_audios = np.stack([summed_audios, summed_audios], axis=1)  # Convert to (N,2)

print("Shape before compression:", summed_audios.shape)
summed_audios = summed_audios.astype(np.float32)
print("Converted audio to float32")

print(f"Before Buss Comp: Audio dtype: {summed_audios.dtype}, Shape: {summed_audios.shape}, Size (MB): {summed_audios.nbytes / 1e6:.2f}MB")
buss = process_buss(summed_audios, samplerate)
print(f"Buss output Audio dtype: {buss.dtype}, Shape: {buss.shape}, Size (MB): {buss.nbytes / 1e6:.2f}MB")

print("Processed files saving:")
save_file(inst_processed, samplerate, output_instrumental_file, channels=2)
print(f"  Instrumental: {output_instrumental_file}")
save_file(vocal_processed, samplerate, output_vocal_file, channels=2)
print(f"  Vocals: {output_vocal_file}")
save_file(summed_audios, samplerate, output_summed_file, channels=2)
print(f"  Summed: {output_summed_file}")
save_file(buss, samplerate, output_buss_file, channels=2)
print(f"  Buss: {output_buss_file}")






