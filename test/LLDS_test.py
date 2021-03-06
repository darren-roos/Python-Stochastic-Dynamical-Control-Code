# Linear Latent Dynamic Models
# u   u
# |   |
# h - h -> ...
# |   |
# o   o
# Tests for the Kalman type models.
# All tests are compared to code supplied by:
# Bayesian Reasoning and Machine Learning
# by David Barber
# Website: http://www0.cs.ucl.ac.uk/staff/d.barber/brml/
# The example is taken from Example 24.4
# The functions were all compared to his demo program in Matlab:
# demoLDSTracking.m

import src.LLDS as LLDS
import numpy
import pandas
import pathlib

# Specify System
dt = 0.1
T = 400
A = numpy.eye(6)  # state transition
A[0, 4] = dt
A[1, 0] = dt
A[2, 5] = dt
A[3, 2] = dt
B = numpy.zeros(6)  # input transition
C = numpy.zeros([2, 6])  # state observation
C[0, 1] = 1.0
C[1, 3] = 1.0
sigmaQ = 0.00001  # standard deviation of process noise
sigmaR = 50.0  # standard deviation of measurement noise
Q = sigmaQ**2*numpy.eye(6)  # process noise covariance
R = sigmaR**2*numpy.eye(2)  # measurement noise covariance
model = LLDS.LLDS(A, B, C, Q, R)


# Specify initial conditions
init_covar = numpy.eye(6)  # vague prior covar
init_mean = numpy.zeros(6)  # vague prior mean

# Read in correct data
visiblestates_path = pathlib.Path("visiblestates.csv")
if visiblestates_path.is_file():
    visiblestates = pandas.read_csv("visiblestates.csv", header=None).as_matrix()  # read in the ideal answers
    filtercovar_file = pandas.read_csv("filtercovar.csv", header=None).as_matrix()
    filtercovar = numpy.reshape(filtercovar_file, [6, 6, T], order='F')  # read in the ideal answers
    filtermeans = pandas.read_csv("filtermeans.csv", header=None).as_matrix()  # read in the ideal answers
    smoothedcovar_file = pandas.read_csv("smoothcovar.csv", header=None).as_matrix()
    smoothedcovar = numpy.reshape(smoothedcovar_file, [6, 6, T], order='F')  # read in the ideal answers
    smoothedmeans = pandas.read_csv("smoothmeans.csv", header=None).as_matrix()  # read in the ideal answers
else:
    visiblestates = pandas.read_csv("test/visiblestates.csv", header=None).as_matrix()  # read in the ideal answers
    filtercovar_file = pandas.read_csv("test/filtercovar.csv", header=None).as_matrix()
    filtercovar = numpy.reshape(filtercovar_file, [6, 6, T], order='F')  # read in the ideal answers
    filtermeans = pandas.read_csv("test/filtermeans.csv", header=None).as_matrix()  # read in the ideal answers
    smoothedcovar_file = pandas.read_csv("test/smoothcovar.csv", header=None).as_matrix()
    smoothedcovar = numpy.reshape(smoothedcovar_file, [6, 6, T], order='F')  # read in the ideal answers
    smoothedmeans = pandas.read_csv("test/smoothmeans.csv", header=None).as_matrix()  # read in the ideal answers

tol = 0.01


def test_filter():
    ucontrol = numpy.zeros(1)  # no control so this is really only a dummy variable.
    filtermeans_own = numpy.zeros([6, T])
    filtercovar_own = numpy.zeros([6, 6, T])
    filtermeans_own[:, 0], filtercovar_own[:, :, 0] = model.init_filter(init_mean, init_covar, visiblestates[:, 0])
    for t in range(1, T):
        temp = model.step_filter(filtermeans_own[:, t-1], filtercovar_own[:, :, t-1], ucontrol, visiblestates[:, t])
        filtermeans_own[:, t], filtercovar_own[:, :, t] = temp

    assert (abs(filtermeans_own - filtermeans)).max() < tol

    assert (abs(filtercovar_own - filtercovar)).max() < tol

    return filtermeans_own, filtercovar_own


def test_smooth():
    ucontrols = numpy.zeros([1, T])  # no control so this is really only a dummy variable.

    filtermeans_own, filtercovar_own = test_filter()

    smoothedmeans_own, smoothedcovar_own = model.smooth(filtermeans_own, filtercovar_own, ucontrols)

    assert (abs(smoothedmeans_own - smoothedmeans)).max() < tol

    assert (abs(smoothedcovar_own - smoothedcovar)).max() < tol


if __name__ == '__main__':
    test_filter()
    test_smooth()
