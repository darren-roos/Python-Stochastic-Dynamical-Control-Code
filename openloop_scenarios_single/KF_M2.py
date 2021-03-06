# Inference using one linear model measuring only temperature

import matplotlib.pyplot as plt
import numpy
import openloop.params
import src.LLDS as LLDS
import src.Results as Results
import scipy.stats

tend = 50

params = openloop.params.Params(tend)
init_state = numpy.array([0.5, 400])

# Specify the linear model
linsystems = params.cstr_model.get_nominal_linear_systems(params.h)
opoint = 1  # which nominal model to use
A = linsystems[opoint].A
B = linsystems[opoint].B
b = linsystems[opoint].b

lin_cstr = LLDS.LLDS(A, B, params.C2, params.Q, params.R2)  # KF object

# Plant initialisation
params.xs[:, 0] = init_state
params.linxs[:, 0] = init_state - b

# Simulate plant
state_noise_dist = scipy.stats.multivariate_normal(cov=params.Q)  # state distribution
meas_noise_dist = scipy.stats.multivariate_normal(cov=lin_cstr.R)  # measurement distribution
params.ys2[:, 0] = params.C2 @ params.xs[:, 0] + meas_noise_dist.rvs()  # measure from actual plant

# Filter setup
kfmeans = numpy.zeros([2, params.N])
kfcovars = numpy.zeros([2, 2, params.N])
init_mean = init_state - b

# First time step
kfmeans[:, 0], kfcovars[:, :, 0] = lin_cstr.init_filter(init_mean, params.init_state_covar, params.ys2[:, 0]-b)

for t in range(1, params.N):
    params.xs[:, t] = params.cstr_model.run_reactor(params.xs[:, t-1], params.us[t-1], params.h)
    params.xs[:, t] += state_noise_dist.rvs()
    params.ys2[:, t] = params.C2 @ params.xs[:, t] + meas_noise_dist.rvs()  # measured from actual plant
    params.linxs[:, t], _ = lin_cstr.step(params.linxs[:, t-1], params.us[t-1])
    temp = lin_cstr.step_filter(kfmeans[:, t-1], kfcovars[:, :, t-1], params.us[t-1], params.ys2[:, t] - b)
    kfmeans[:, t], kfcovars[:, :, t] = temp

for i in range(len(params.linxs[0])):
    params.linxs[:, i] += b
    kfmeans[:, i] += b

# Plot results

Results.plot_ellipses1(params.ts, params.xs, kfmeans, kfcovars, "lower left")

Results.plot_tracking(params.ts, params.xs, params.ys2, kfmeans, params.us, 2)

plt.show()
avediff = Results.calc_error(params.xs, kfmeans)
