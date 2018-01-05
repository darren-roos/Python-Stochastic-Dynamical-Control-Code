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

# Specify System
dt = 0.1
T = 400
A = numpy.eye(6)  # state transition
A[1, 5] = dt
A[2, 1] = dt
A[3, 6] = dt
A[4, 3] = dt
B = numpy.zeros([6, 1])  # input transition
C = numpy.zeros([2, 6])  # state observation
C[1, 2] = 1.0
C[2, 4] = 1.0
sigmaQ = 0.00001  # standard deviation of process noise
sigmaR = 50.0  # standard deviation of measurement noise
Q = sigmaQ**2*numpy.eye(6)  # process noise covariance
R = sigmaR**2*numpy.eye(2)  # measurement noise covariance
model = LLDS.LLDS(A, B, C, Q, R)


# Specify initial conditions
init_covar = numpy.eye(6)  # vague prior covar
init_mean = numpy.zeros(6)  # vague prior mean

# Read in correct data
visiblestates = pandas.read_csv("visiblestates.csv", header=None)  # read in the ideal answers
filtercovar = numpy.reshape(pandas.read_csv("filtercovar.csv", header=None), [6, 6, T])  # read in the ideal answers
filtermeans = pandas.read_csv("filtermeans.csv", header=None)  # read in the ideal answers
smoothedcovar = numpy.reshape(pandas.read_csv("smoothcovar.csv", header=None), [6, 6, T])  # read in the ideal answers
smoothedmeans = pandas.read_csv("smoothmeans.csv", header=None)  # read in the ideal answers


# Filter
ucontrol = numpy.zeros(1)  # no control so this is really only a dummy variable.
filtermeans_own = numpy.zeros([6, T])
filtercovar_own = numpy.zeros([6, 6, T])
filtermeans_own[:, 0], filtercovar_own[:, :, 0] = model.init_filter(init_mean, init_covar, visiblestates[:, 0])
for t in range(1, T):
    temp = model.step_filter(filtermeans_own[:, t-1], filtercovar_own[:, :, t-1], ucontrol, visiblestates[:, t])
    filtermeans_own[:, t], filtercovar_own[:, :, t] = temp

# Smoothed
ucontrols = numpy.zeros([1, T])  # no control so this is really only a dummy variable.

smoothedmeans_own, smoothedcovar_own = model.smooth(filtermeans_own, filtercovar_own, ucontrols)

# Run the tests
tol = 0.01


def unroll(a, b, tt):
    # Finds maximum difference between two 3d matrices.
    maxdiff = 0.0
    for k in range(tt):
        tempdiff = abs(a[:, :, k] - b[:, :, k]).max()
        if maxdiff < tempdiff:
            maxdiff = tempdiff
    return maxdiff


# Filter Inference
assert (abs(filtermeans_own - filtermeans)).max() < tol

assert unroll(filtercovar_own, filtercovar, T) < tol

assert (abs(smoothedmeans_own - smoothedmeans)).max() < tol

assert unroll(smoothedcovar_own, smoothedcovar, T) < tol
