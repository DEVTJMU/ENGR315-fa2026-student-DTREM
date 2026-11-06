import numpy as np
from scipy.stats import ttest_ind

"""
Two Sided Tests for Two Samples

Complete two_sided_tests() below. Each file holds one sample of numbers (one per line). The function compares the
first file of the first list with the first file of the second list, the second with the second, and so on, using a
two-sided t-test. It returns the pairs of file names where the null hypothesis (the means are equal) is rejected.

Use Welch's t-test (equal_var=False in ttest_ind) because the two samples in a pair may have different sizes and spreads.

Your function is tested on different random files than the ones in the self-check at the bottom of this
file, so it must use every parameter.

Submit this file to Gradescope.
"""


def write_to_csv(filename: str, data):
    """
    Write an array of data to a file
    :param filename: Name of file to be written
    :param data: An array type object for data to be written to file
    :return: None
    """
    try:
        file = open(filename, 'w')
    except FileNotFoundError:
        print('Could not open file ', filename, ' error!!')
        return

    for a in data:
        file.writelines(str(a) + '\n')

    file.close()


def two_sided_tests(_files1: list, _files2: list, _alpha: float):
    """
    Conduct a two-sided t-test on each pair of files. Null hypothesis is the means are equal.
    :param _files1: List of file names, the first sample of each pair. Assume they can be loaded directly as a numpy array
    :param _files2: List of file names, the second sample of each pair. Assume they can be loaded directly as a numpy array
    :param _alpha: Desired alpha value for t-test
    :return: A list of file pairs (tuples) where the null hypothesis is rejected
    """

    # list of file pairs where the null hypothesis is rejected
    reject_null_hypothesis = []

    # YOUR CODE HERE #
    for filename1, filename2 in zip(_files1, _files2):
        data1 = np.loadtxt(filename1)
        data2 = np.loadtxt(filename2)
        t_stat, p_value = ttest_ind(data1, data2, equal_var=False)

        if p_value < _alpha:
            reject_null_hypothesis.append((filename1, filename2))

    # return file pairs that were rejected
    return reject_null_hypothesis


if __name__ == "__main__":
    # Use this section to check your work. It is not graded and is not run by Gradescope.
    # The random seed makes the files the same every time it is run.
    np.random.seed(315)

    # number of samples for each file
    num_samples = 100
    std = 1

    # two samples from the same distribution, then samples that are well apart from each other
    write_to_csv('equal1.txt', np.random.normal(loc=0, scale=std, size=num_samples))
    write_to_csv('equal2.txt', np.random.normal(loc=0, scale=std, size=num_samples))
    write_to_csv('lesser1.txt', np.random.normal(loc=-1.0, scale=std, size=num_samples))
    write_to_csv('lesser2.txt', np.random.normal(loc=-2.0, scale=std, size=num_samples))
    write_to_csv('greater1.txt', np.random.normal(loc=1.0, scale=std, size=num_samples))
    write_to_csv('greater2.txt', np.random.normal(loc=2.0, scale=std, size=num_samples))

    # comparing each file with itself. The means cannot differ, so no pairs should be returned
    same_files = ['lesser1.txt', 'greater1.txt', 'equal1.txt']
    print('Same files. Expected: []. Result: ', two_sided_tests(_files1=same_files, _files2=same_files, _alpha=0.05))

    # file 1 of the first list is compared with file 1 of the second list, and so on
    first_files = ['lesser1.txt', 'lesser1.txt', 'greater1.txt', 'equal1.txt', 'equal1.txt']
    second_files = ['lesser2.txt', 'lesser1.txt', 'greater2.txt', 'lesser1.txt', 'equal2.txt']
    print('Different files. Expected: [(\'lesser1.txt\', \'lesser2.txt\'), (\'greater1.txt\', \'greater2.txt\'), '
          '(\'equal1.txt\', \'lesser1.txt\')]')
    print('Result: ', two_sided_tests(_files1=first_files, _files2=second_files, _alpha=0.05))
