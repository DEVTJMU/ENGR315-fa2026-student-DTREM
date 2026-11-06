import numpy as np
from scipy.stats import ttest_1samp

"""
One Sided Tests for One Sample

Complete one_sided_tests() below. Each file holds one sample of numbers (one per line). The function runs a
one-sided t-test on every file and returns the names of the files where the null hypothesis is rejected.

Your function is tested on different random files than the ones in the self-check at the bottom of this
file, so it must use every parameter: the list of files, the hypothesized mean, alpha and the side of the test.

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


def one_sided_tests(_files: list, _mean: float, _alpha: float, _less_than: bool):
    """
    Conduct a one-sided t-test on each file, either left-sided or right-sided. Null hypothesis is the means are equal.
    :param _files: List of file names to be tested. Assume they can be loaded directly as a numpy array
    :param _mean: The test statistic mean for the hypothesis
    :param _alpha: Desired alpha value for t-test
    :param _less_than: If true, then a left-sided (<) t-test is performed. Otherwise, a right-sided test (>)
    :return: A list of files where the null hypothesis is rejected
    """

    # list of files where the null hypothesis is rejected
    reject_null_hypothesis = []

    # YOUR CODE HERE #
    for filename in _files:
        data = np.loadtxt(filename)
        t_stat, two_sided_p = ttest_1samp(data, _mean)

        # Convert the two-sided p-value to the appropriate one-sided p-value.
        if _less_than:
            p_value = two_sided_p / 2 if t_stat < 0 else 1 - two_sided_p / 2
        else:
            p_value = two_sided_p / 2 if t_stat > 0 else 1 - two_sided_p / 2

        if p_value < _alpha:
            reject_null_hypothesis.append(filename)

    # return files that were rejected
    return reject_null_hypothesis


if __name__ == "__main__":
    # Use this section to check your work. It is not graded and is not run by Gradescope.
    # The random seed makes the files the same every time it is run.
    np.random.seed(315)

    # number of samples for each file
    num_samples = 100

    # parameters for the hypothesized distribution
    target_mu = 0
    target_std = 1

    # two samples with a mean that is less than the target, and two with a mean that is greater than the target
    less_than_distribution_one = np.random.normal(loc=target_mu - 0.5, scale=target_std, size=num_samples)
    less_than_distribution_two = np.random.normal(loc=target_mu - 1.0, scale=target_std, size=num_samples)
    greater_than_distribution_one = np.random.normal(loc=target_mu + 0.5, scale=target_std, size=num_samples)
    greater_than_distribution_two = np.random.normal(loc=target_mu + 1.0, scale=target_std, size=num_samples)

    # write samples to files
    write_to_csv('lesser1.txt', less_than_distribution_one)
    write_to_csv('lesser2.txt', less_than_distribution_two)
    write_to_csv('greater1.txt', greater_than_distribution_one)
    write_to_csv('greater2.txt', greater_than_distribution_two)

    # place one-sided test files in a list
    one_sided_test_files = ['lesser1.txt', 'lesser2.txt', 'greater1.txt', 'greater2.txt']

    # perform all left-sided tests
    left_sided_tests = one_sided_tests(_files=one_sided_test_files, _mean=target_mu, _alpha=0.05, _less_than=True)
    print('Left sided tests. Expected: [\'lesser1.txt\', \'lesser2.txt\']. Result: ', left_sided_tests)

    # perform all right-sided tests
    right_sided_tests = one_sided_tests(_files=one_sided_test_files, _mean=target_mu, _alpha=0.05, _less_than=False)
    print('Right sided tests. Expected: [\'greater1.txt\', \'greater2.txt\']. Result: ', right_sided_tests)
