# Carmine Silano
# Feb 24, 2025
# Implement a MonoToStereoUpmixer class that upmixes a mono signal to stereo 
# using a delay and sum technique.
# Technique learned from Michael Gruhn

# Rewritten to use Numba for JIT acceleration which made a HUGE difference in speed.
# However, this inolved moving the process_buffer_stereo function outside the class definition.
# This is because Numba does not support class methods directly.

import numpy as np
import math
from numba import njit

@njit
def process_buffer_stereo(mono_buffer, bs, delay_buffer):
    # Determine the number of samples in the input mono signal.
    n = mono_buffer.shape[0]
    
    # Create an empty output array for the stereo signal.
    # The shape is (n, 2): one column for the left channel and one for the right.
    stereo_output = np.empty((n, 2), dtype=mono_buffer.dtype)
    
    # Initialize a pointer (index) for the circular delay buffer.
    ptr = 0
    
    # Process each sample in the mono input buffer.
    for i in range(n):
        # Retrieve the current mono sample.
        spl0 = mono_buffer[i]
        
        # Store the current sample into the delay buffer at the current pointer position.
        delay_buffer[ptr] = spl0
        
        # Move the pointer forward in the delay buffer.
        ptr += 1
        
        # If the pointer reaches the defined delay length (bs), wrap it around to the beginning.
        if ptr >= bs:
            ptr = 0
        
        # Retrieve the delayed sample from the delay buffer at the current pointer position.
        delayed = delay_buffer[ptr]
        
        # Calculate intermediate value spl0_ and spl1_.:
        # This is the average of (current sample multiplied by 2) and the delayed sample.
        spl0_ = (spl0 * 2 + delayed) / 2.0
        spl1_ = (spl0 * 2 - delayed) / 2.0
        
        # Compute the left and right channel output.
        # It is derived from spl0_ and a scaled version of spl1_.
        stereo_output[i, 0] = (spl0_ + spl1_ / 2.0) / 1.5
        stereo_output[i, 1] = (spl1_ + spl0_ / 2.0) / 1.5
    
    # Return the complete stereo output array.
    return stereo_output

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
        # Calculate delay length in samples (bs), capped at 500,000 samples.
        self.bs = int(math.floor(min(delay_ms * sample_rate / 1000, 500000)))
        # Allocate a delay buffer of size (bs * 2 + 1)
        self.delay_buffer = np.zeros(self.bs * 2 + 1, dtype=np.float64)

    def process_buffer(self, mono_buffer):
        """
        Process an entire mono buffer to produce stereo output.

        Parameters:
            mono_buffer (np.ndarray): 1D NumPy array of mono samples.

        Returns:
            np.ndarray: A 2D array of shape (n_samples, 2) with stereo output.
        """
        # Ensure the input is a 1D array.
        if mono_buffer.ndim > 1:
            mono_buffer = mono_buffer.flatten()
        return process_buffer_stereo(mono_buffer, self.bs, self.delay_buffer)