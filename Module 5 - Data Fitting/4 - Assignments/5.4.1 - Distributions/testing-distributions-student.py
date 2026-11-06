import numpy as np
from scipy.stats import norm, expon
import matplotlib
import matplotlib.pyplot as plt
import platform

# a fix for Dr. Forsyth's computer
# https://stackoverflow.com/questions/56013105/matplotlib-plot-window-is-white-blank-without-showing-any-image
if platform.system() == 'Darwin':
    matplotlib.use('MacOSX')

"""
Testing Distributions

Complete the three functions below. Each one fits samples to a distribution, the same way as the lecture
example for Module 5.1 (distribution-fit.py).

Your functions are tested on different random samples than the ones at the bottom of this file, so they must work
for any samples they are given.

Submit this file to Gradescope.
"""


def fit_normal(_samples):
    """
    Fit samples to a normal distribution
    :param _samples: A numpy array of samples
    :return: A tuple (mean, standard deviation) of the fitted normal distribution
    """

    # Hint: norm.fit() returns the mean and standard deviation, as in the lecture example
    fitted_mean = None
    fitted_std = None

    # YOUR CODE HERE #
    fitted_mean, fitted_std = norm.fit(_samples)

    return fitted_mean, fitted_std


def fit_exponential(_samples):
    """
    Fit samples to an exponential distribution that starts at 0
    :param _samples: A numpy array of samples
    :return: The fitted beta (scale) of the exponential distribution
    """
    fit_beta = expon.fit(_samples, floc=0)[1]

    return fit_beta


def normal_range(_samples, _fraction):
    """
    Fit samples to a normal distribution, then find the range where a fraction of the values should fall
    :param _samples: A numpy array of samples
    :param _fraction: Fraction of values inside the range, e.g. 0.95 for the middle 95%
    :return: A tuple (lower, upper) for the middle _fraction of the fitted normal distribution
    """

    # Hint: fit the samples with your fit_normal() first, then use norm.interval() as in the lecture example
    lower = None
    upper = None

    # YOUR CODE HERE #
    fitted_mean, fitted_std = fit_normal(_samples)
    lower, upper = norm.interval(_fraction, loc=fitted_mean, scale=fitted_std)

    return lower, upper


if __name__ == "__main__":
    # Use this section to check your work. It is not graded and is not run by Gradescope.
    # The random seed makes the samples the same every time it is run.
    np.random.seed(315)

    """
    Part 1: fit a normal distribution
    """

    # desired average and standard deviation of the normal distribution
    desired_mu = 5
    desired_std = 12

    # generate samples with numpy
    normal_samples = np.random.normal(loc=desired_mu, scale=desired_std, size=1000)

    result = fit_normal(normal_samples)
    print('fit_normal(). Expected: (4.737, 11.910). Result:', result)

    if result[0] is not None:
        (sample_mean, sample_std_dev) = result

        # plot the fitted curve against the ideal curve
        x = np.linspace(start=-31, stop=41, num=10000)
        plt.plot(x, norm.pdf(x, loc=sample_mean, scale=sample_std_dev), label='Fitted Normal')
        plt.plot(x, norm.pdf(x, loc=desired_mu, scale=desired_std), label='Ideal Normal')
        plt.title('Fitted Normal Distribution for 1000 Sampled Points')
        plt.xlabel('X')
        plt.ylabel('Probability density')
        plt.legend()
        plt.show()

    """
    Part 2: fit an exponential distribution
    """

    # desired lambda, and the matching beta
    desired_lambda = 0.4
    desired_beta = 1 / desired_lambda

    # generate samples with numpy
    exponential_samples = np.random.exponential(scale=desired_beta, size=25)

    fit_beta = fit_exponential(exponential_samples)
    print('fit_exponential(). Expected: 2.551. Result:', fit_beta)

    if fit_beta is not None:
        # plot the fitted curve against the ideal curve
        x = np.linspace(start=0, stop=15, num=10000)
        plt.plot(x, expon.pdf(x, scale=fit_beta), label='Fitted Exponential')
        plt.plot(x, expon.pdf(x, scale=desired_beta), label='Ideal Exponential')
        plt.title('Fitted Exponential for 25 Sampled Points')
        plt.xlabel('X')
        plt.ylabel('Probability density')
        plt.legend()
        plt.show()

    """
    Part 3: the range where 95% of the values should fall
    """

    result = normal_range(normal_samples, 0.95)
    print('normal_range() for 95%. Expected: (-18.607, 28.081). Result:', result)

    if result[0] is not None:
        (lower, upper) = result
        inside = np.mean((normal_samples > lower) & (normal_samples < upper))
        print('Fraction of the samples inside that range:', inside)
