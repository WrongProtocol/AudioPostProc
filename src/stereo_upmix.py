# Carmine Silano
# Feb 24, 2025
# Implement a MonoToStereoUpmixer class that upmixes a mono signal to stereo 
# using a delay and sum technique.
# Technique learned from Michael Gruhn

import numpy as np
import math

class MonoToStereoUpmixer:
    def __init__(self, sample_rate, delay_ms=125):
        """
        Initialize the upmixer.

        Parameters:
            sample_rate (int): The sampling rate in Hz.
            delay_ms (float): Delay in milliseconds (default: 125ms).
        """
        self.sample_rate = sample_rate
        self.delay_ms = delay_ms
        
        # Calculate delay length in samples (bs) and cap at 500,000 samples.
        self.bs = int(math.floor(min(delay_ms * sample_rate / 1000, 500000)))
        
        # Allocate a delay buffer of size (bs * 2 + 1)
        self.buffer = np.zeros(self.bs * 2 + 1)
        
        # Initialize pointer into the buffer.
        self.ptr = 0
        
        # Unused extra tail size variable (from pseudocode).
        self.ext_tail_size = -1

    def process_sample(self, spl0):
        """
        Process a single mono sample and produce stereo output.

        Parameters:
            spl0: The mono input sample (ensured to be a scalar).

        Returns:
            tuple: (left, right) stereo output samples.
        """
        # Ensure spl0 is a scalar float.
        spl0 = float(spl0)
        
        # Store the current sample in the delay buffer at the current pointer.
        self.buffer[self.ptr] = spl0
        
        # Increment the pointer and wrap around if it reaches bs.
        self.ptr += 1
        if self.ptr >= self.bs:
            self.ptr = 0
        
        # Retrieve the delayed sample from the buffer.
        delayed = self.buffer[self.ptr]
        
        # Compute intermediate values.
        spl0_ = (spl0 * 2 + delayed) / 2
        spl1_ = (spl0 * 2 - delayed) / 2
        
        # Generate left and right channel outputs.
        left = (spl0_ + spl1_ / 2) / 1.5
        right = (spl1_ + spl0_ / 2) / 1.5
        
        return left, right

    def process_buffer(self, mono_buffer):
        """
        Process an entire mono buffer to produce stereo output.

        Parameters:
            mono_buffer (np.ndarray): Array of mono samples.

        Returns:
            np.ndarray: A 2D array of shape (n_samples, 2) with stereo output.
        """
        # Ensure that mono_buffer is a 1D array.
        if mono_buffer.ndim > 1:
            mono_buffer = mono_buffer.flatten()
            
        left_channel = np.zeros_like(mono_buffer)
        right_channel = np.zeros_like(mono_buffer)
        
        for i, sample in enumerate(mono_buffer):
            left, right = self.process_sample(sample)
            left_channel[i] = left
            right_channel[i] = right
        
        # Stack the two channels to form a stereo signal.
        stereo_output = np.stack((left_channel, right_channel), axis=1)
        return stereo_output
