import numpy as np
from scipy import signal

def process_audio(audio, srate, drive=16.4, distortion=33, highpass=5000, wet_mix=-6, dry_mix=0):
    """
    Process a stereo audio signal by applying dynamic gain control combined with filtering,
    resulting in a mix of the original (dry) and processed (wet) signals. The effect is influenced
    by drive, distortion, and highpass filtering parameters.
    
    Parameters:
      audio    : ndarray
                 Input stereo audio array with shape (n_samples, 2). Each row contains two channels.
      srate    : int or float
                 The sampling rate in Hz.
      drive    : float, optional
                 Drive level in dB. Controls the threshold for gain reduction. (Default is 16.4)
      distortion : float, optional
                 Distortion parameter on a 0-100 scale. Affects the release time of the gain reduction. (Default is 33)
      highpass : float, optional
                 Highpass filter cutoff frequency in Hz for the wet signal path. (Default is 5000 Hz)
      wet_mix  : float, optional
                 Wet signal mix level in dB. (Default is -6 dB)
      dry_mix  : float, optional
                 Dry (unprocessed) signal mix level in dB. (Default is 0 dB)
                 
    Returns:
      ndarray: Processed stereo audio with the same shape as the input.
    """

    # Initialize the dynamic gain factor. This will be adjusted sample-by-sample.
    gain = 1
    
    # Constant used for decibel/exponential calculations.
    c = 8.65617025
    
    # A very small constant to avoid division by zero (not used directly below though).
    dc = 1e-30

    # Set the threshold in dB based on the drive parameter (inverting drive for threshold).
    threshDB = -drive
    # Convert the dB threshold into a linear scale using an exponential conversion.
    thresh = np.exp(threshDB / c)
    # Compression ratio (here fixed at 1:20, used to shape the gain reduction curve).
    ratio = 1 / 20

    # Calculate the release factor which controls the decay speed of gain reduction.
    # The distortion parameter (normalized from 0 to 1) is cubed and used to adjust the release time.
    release = np.exp(-60 / (np.power((1 - distortion) / 100, 3) * 500 * srate / 1000) / c)

    # Initialize two state variables (t0 and t1) for filtering; they are not used further in this code.
    t0 = t1 = 0

    # Calculate filter coefficients for a cascaded highpass filter:
    # blp is the coefficient derived from the highpass cutoff frequency.
    blp = -np.exp(-2 * np.pi * highpass * 3 / srate)
    # alp is the complementary coefficient ensuring the filter sums to unity.
    alp = 1 + blp

    # Compute wet and dry mix factors by converting the dB values to linear scale.
    # The wet factor also includes a compensation based on the threshold and compression ratio.
    wet = np.exp(wet_mix / c) / np.exp((threshDB - threshDB * ratio) / c)
    dry = np.exp(dry_mix / c)

    # Initialize the variable that will hold the gain computed per sample.
    seekGain = 1

    # Initialize filter state variables for a three-stage filter for each stereo channel.
    # t00, t01: first filter stage for left and right channels.
    # t10, t11: second filter stage for left and right channels.
    # t20, t21: third filter stage for left and right channels.
    t00, t01, t10, t11, t20, t21 = 0, 0, 0, 0, 0, 0

    # Process each sample in the audio buffer (assumes 'audio' is an array of [left, right] pairs).
    for i in range(len(audio)):
        # Extract left and right channel samples.
        spl0 = audio[i][0]
        spl1 = audio[i][1]
        
        # --- Filter Stage 1 ---
        # For left channel: update filter state t00 with current sample and compute intermediate s0.
        s0 = (t00 := alp * spl0 - blp * t00)
        # For right channel: update filter state t01 similarly.
        s1 = (t01 := alp * spl1 - blp * t01)
        
        # --- Filter Stage 2 ---
        # Process the intermediate signal from stage 1 through the second filter stage.
        s0 = (t10 := alp * s0 - blp * t10)
        s1 = (t11 := alp * s1 - blp * t11)
        
        # --- Filter Stage 3 ---
        # Final stage: subtract the filtered output from the original to obtain the processed signal.
        s0 = spl0 - (t20 := alp * s0 - blp * t20)
        s1 = spl1 - (t21 := alp * s1 - blp * t21)
        
        # Determine the instantaneous amplitude (as a simple approximation to RMS)
        # by taking the maximum absolute value of the two channels.
        rms = max(abs(spl0), abs(spl1))
        
        # Compute the desired gain (seekGain) based on the signal amplitude.
        # If the amplitude exceeds the threshold, apply a logarithmic compression curve;
        # otherwise, leave the gain unchanged.
        if rms > thresh:
            # Calculate a target gain based on the log of the rms value.
            seekGain = np.exp((threshDB + (np.log(rms) * c - threshDB) * ratio) / c) / rms
        else:
            seekGain = 1
        
        # Update the overall gain with a release factor, ensuring it decays gradually.
        gain = min(gain, release * seekGain)
        
        # Mix the dry (original) and wet (processed) signals.
        # The dry signal is scaled by the dry mix factor.
        # The wet signal is scaled by the computed gain and wet mix factor.
        audio[i][0] = spl0 * dry + s0 * gain * wet
        audio[i][1] = spl1 * dry + s1 * gain * wet

    # Return the processed audio array.
    return audio
