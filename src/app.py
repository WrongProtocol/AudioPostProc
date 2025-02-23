#!/usr/bin/env python 

import os
from fx import process_instrumental
from utils import open_file, save_file

# Main processing block to demonstrate the effects chain
if __name__ == "__main__":
    # Define input and output file paths.
    vocal_file = "../input_files/v.wav"
    instrumental_file = "../input_files/i.wav"
    output_vocal_file = "../output/processed_vocal.wav"
    output_instrumental_file = "../output/processed_instrumental.wav"
    samplerate = 44100.0

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_instrumental_file)
    os.makedirs(output_dir, exist_ok=True)

    inst_audio = open_file(instrumental_file, samplerate)
    inst_processed = process_instrumental(inst_audio, samplerate)

    save_file(inst_processed, samplerate, output_instrumental_file)

    print("Audio processing complete! Processed files saved:")
    # print(f"  Vocals: {output_vocal_file}")
    print(f"  Instrumental: {output_instrumental_file}")
