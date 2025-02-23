#!/usr/bin/env python

from fx import fx_compression, fx_eq4, fx_reverb, fx_delay, fx_highpass
from utils import open_file, save_file

# Main processing block to demonstrate the effects chain
if __name__ == "__main__":
    # Define input and output file paths.
    vocal_file = "../input_files/v.wav"
    instrumental_file = "../input_files/i.wav"
    output_vocal_file = "processed_vocal.wav"
    output_instrumental_file = "processed_instrumental.wav"

    # Load both vocal and instrumental files.
    vocals, sr_vocals = open_file(vocal_file)
    instrumental, sr_inst = open_file(instrumental_file)

    # Ensure that both files share the same sample rate.
    if sr_vocals != sr_inst:
        print("Error: Sample rates of input files do not match. Please use files with the same sample rate.")
        exit(1)
    sr = sr_vocals  # Use the common sample rate

    # ======================
    # Build effects chain for Vocals:
    #   1. Compression
    #   2. 4-Band EQ
    #   3. Reverb
    # ======================
    processed_vocals = fx_compression(vocals, sr, threshold=-18.0, ratio=3.0, attack=0.005, release=0.05)
    processed_vocals = fx_eq4(processed_vocals, sr, frequencies=[120, 400, 1500, 6000], gains=[2, -3, 3, 1], bandwidths=[1, 1, 1, 1])
    processed_vocals = fx_reverb(processed_vocals, sr, room_size=0.7, wet=0.4)

    # =============================
    # Build effects chain for Instrumental:
    #   1. Delay (with panning)
    #   2. Optional: High-pass filter to remove sub-bass rumble
    # =============================
    processed_instrumental = fx_delay(instrumental, sr, delay_time=0.4, pan=0.3, wet=0.5)
    processed_instrumental = fx_highpass(processed_instrumental, sr, cutoff=100)

    # Save the processed audio files.
    save_file(processed_vocals, sr, output_vocal_file)
    save_file(processed_instrumental, sr, output_instrumental_file)

    print("Audio processing complete! Processed files saved:")
    print(f"  Vocals: {output_vocal_file}")
    print(f"  Instrumental: {output_instrumental_file}")
