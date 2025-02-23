#!/usr/bin/env python 

import os
from fx import process_instrumental, process_vocals, sum_audio, process_buss
from utils import open_file, save_file

# Main processing block to demonstrate the effects chain
if __name__ == "__main__":
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
    inst_processed = process_instrumental(inst_audio, samplerate)

    vocal_audio = open_file(vocal_file, samplerate)
    vocal_processed = process_vocals(vocal_audio, samplerate) 

    summed_audios = sum_audio(inst_processed, vocal_processed)
    #buss = process_buss(summed_audios, samplerate)

    
    save_file(inst_processed, samplerate, output_instrumental_file)
    save_file(vocal_processed, samplerate, output_vocal_file)
    save_file(summed_audios, samplerate, output_summed_file)
    #save_file(buss, samplerate, output_buss_file)
    

    print("Audio processing complete! Processed files saved:")
    print(f"  Vocals: {output_vocal_file}")
    print(f"  Instrumental: {output_instrumental_file}")
    print(f"  Summed: {output_summed_file}")
