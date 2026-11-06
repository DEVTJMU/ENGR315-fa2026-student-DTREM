import numpy as np
from scipy import signal as scipy_signal
from scipy.signal import find_peaks
from ekg_testbench import EKGTestBench


def detect_heartbeats(filepath):
    """
    Perform analysis to detect location of heartbeats.
    Returns the filtered ECG signal and detected heartbeat indices.
    """
    if filepath == '':
        return list()

    # Load CSV data, skipping the two header rows
    data = np.loadtxt(filepath, delimiter=',', skiprows=2)

    # First column is time; second column is the ECG signal
    time = data[:, 0]
    signal = data[:, 1]

    # Calculate sampling frequency from time values
    fs = 1.0 / np.median(np.diff(time))

    # Remove any DC offset
    signal = signal - np.mean(signal)

    # Bandpass filter: retain frequencies between 5 and 15 Hz
    sos = scipy_signal.butter(
        2, [5, 15], btype='bandpass', fs=fs, output='sos'
    )
    filtered = scipy_signal.sosfiltfilt(sos, signal)

    # Differentiate the filtered signal
    derivative = np.gradient(filtered) * fs

    # Square the derivative
    squared = derivative ** 2

    # Moving-window integration (150 ms)
    window_size = int(round(0.150 * fs))
    integration_kernel = np.ones(window_size) / window_size
    integrated = np.convolve(
        squared, integration_kernel, mode='same'
    )

    # Adaptive peak detection
    # Minimum separation of 250 ms between detected beats
    min_distance = int(0.250 * fs)

    # Use a robust signal range rather than half the global maximum
    lower = np.percentile(integrated, 25)
    upper = np.percentile(integrated, 95)
    prominence = max((upper - lower) * 0.10, 1e-12)

    candidates, _ = find_peaks(
        integrated,
        distance=min_distance,
        prominence=prominence
    )

    # Refine each candidate to the nearest R-wave peak
    # within an 80 ms window in the filtered ECG signal
    search_radius = int(0.080 * fs)
    beats = []

    for peak in candidates:
        start = max(0, peak - search_radius)
        end = min(len(filtered), peak + search_radius + 1)

        # Find the largest absolute ECG deflection
        local_peak = start + np.argmax(np.abs(filtered[start:end]))
        beats.append(local_peak)

    beats = np.array(sorted(set(beats)), dtype=int)

    # Return filtered ECG and detected heartbeat indices
    return filtered, beats

    """
    Perform analysis to detect location of heartbeats
    :param filepath: A valid path to a CSV file of heart beats
    :return: signal: a signal that will be plotted
    beats: the indices of detected heartbeats
    """
    if filepath == '':
        return list()

    # import the CSV file using numpy
    path = filepath

    # load data in matrix from CSV file; skip first two rows
    data = np.loadtxt(path, delimiter=',', skiprows=2)

    # save each vector as own variable
    signal = data[:, 0]  # Example: assuming the first column is the signal

    # identify one column to process. Call that column signal

    signal = -1 * signal  # invert the signal if necessary

    # pass data through LOW PASS FILTER (OPTIONAL)
    sos = scipy_signal.butter(2, 15, btype='low', fs=360, output='sos')
    signal = scipy_signal.sosfiltfilt(sos, signal)

    # pass data through HIGH PASS FILTER (OPTIONAL) to create BAND PASS result
    sos = scipy_signal.butter(2, 5, btype='high', fs=360, output='sos')
    signal = scipy_signal.sosfiltfilt(sos, signal)

    # pass data through differentiator
    derivative_kernel = np.array([-1, -2, 0, 2, 1], dtype=float) * (360 / 8.0)
    signal = np.convolve(signal, derivative_kernel, mode='same')

    # pass data through square function
    signal = signal ** 2

    # pass through moving average window
    window_size = max(1, int(round(0.150 * 360)))
    integration_kernel = np.ones(window_size, dtype=float) / window_size
    signal = np.convolve(signal, integration_kernel, mode='same')

    # use find_peaks to identify peaks within averaged/filtered data
    # save the peaks result and return as part of testbench result

    ## your code here peaks,_ = find_peaks(....)
    peaks, _ = find_peaks(signal, height=np.max(signal)*0.5)

    beats = peaks  # save the peaks result and return as part of testbench result

    # do not modify this line
    return signal, beats


# when running this file directly, this will execute first
if __name__ == "__main__":

    # place here so doesn't cause import error
    import matplotlib.pyplot as plt

    # database name
    database_name = 'mitdb_201'

    # set to true if you wish to generate a debug file
    file_debug = False

    # set to true if you wish to print overall stats to the screen
    print_debug = True

    # set to true if you wish to show a plot of each detection process
    show_plot = False

    ### DO NOT MODIFY BELOW THIS LINE!!! ###

    # path to ekg folder
    import os

    path_to_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../data/ekg/")
    ) + os.sep

    # select a signal file to run
    signal_filepath = path_to_folder + database_name + ".csv"

    # call main() and run against the file. Should return the filtered
    # signal and identified peaks
    (signal, peaks) = detect_heartbeats(signal_filepath)

    # stop with a clear message if detect_heartbeats() is not finished yet
    if peaks is None:
        raise SystemExit("detect_heartbeats() returned None for beats. Finish the steps above and return the peak indices.")

    # matched is a list of (peak, annotation) pairs; unmatched is a list of peaks that were
    # not matched to any annotation; and remaining is annotations that were not matched.
    annotation_path = path_to_folder + database_name + "_annotations.txt"
    tb = EKGTestBench(annotation_path)
    peaks_list = peaks.tolist()
    (matched, unmatched, remaining) = tb.generate_stats(peaks_list)

    # if was matched, then is true positive
    true_positive = len(matched)

    # if response was unmatched, then is false positive
    false_positive = len(unmatched)

    # whatever remains in annotations is a missed detection
    false_negative = len(remaining)

    # calculate f1 score
    f1 = true_positive / (true_positive + 0.5 * (false_positive + false_negative))

    # if we wish to show the resulting plot
    if show_plot:
        # make a nice plt of results
        plt.title('Signal for ' + database_name + " with detections")

        plt.plot(signal, label="Filtered Signal")
        plt.plot(peaks, signal[peaks], 'p', label='Detected Peaks')

        true_annotations = np.asarray(tb.annotation_indices)
        plt.plot(true_annotations, signal[true_annotations], 'o', label='True Annotations')

        plt.legend()

        # uncomment line to show the plot
        plt.show()

    # if we wish to save all the stats to a file
    if file_debug:
        # print out more complex stats to the debug file
        debug_file_path = database_name + "_debug_stats.txt"
        debug_file = open(debug_file_path, 'w')

        # print out indices of all false positives
        debug_file.writelines("-----False Positives Indices-----\n")
        for fp in unmatched:
            debug_file.writelines(str(fp) + "\n")

        # print out indices of all false negatives
        debug_file.writelines("-----False Negatives Indices-----\n")
        for fn in remaining:
            debug_file.writelines(str(fn.sample) + "\n")

        # close file that we writing
        debug_file.close()

    if print_debug:
        print("-------------------------------------------------")
        print("Database|\t\tTP|\t\tFP|\t\tFN|\t\tF1")
        print(database_name, "|\t\t", true_positive, "|\t", false_positive, '|\t', false_negative, '|\t', round(f1, 3))
        print("-------------------------------------------------")

    print("Done!")
