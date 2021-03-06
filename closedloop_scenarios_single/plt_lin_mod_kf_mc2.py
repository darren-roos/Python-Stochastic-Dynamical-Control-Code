# Plot the Linear Model KF MC results
import matplotlib as mpc
import matplotlib.pyplot as plt
import numpy
import pandas
import src.Results as Results

# mcN = 50
# include("lin_mod_kf_lin_mpc_mean_mc.jl")
# include("lin_mod_kf_lin_mpc_var_conf_90_mc.jl")
# include("lin_mod_kf_lin_mpc_var_conf_99_mc.jl")
# include("lin_mod_kf_lin_mpc_var_conf_999_mc.jl")

mpc.rc("font", family="serif", serif="Computer Modern", size=12)
mpc.rc("text", usetex=True)

mc1 = abs(pandas.read_csv("linmod_kf_mean_mc2.csv", header=None).as_matrix())
mc2 = abs(pandas.read_csv("linmod_kf_var90_mc2.csv", header=None).as_matrix())
mc3 = abs(pandas.read_csv("linmod_kf_var99_mc2.csv", header=None).as_matrix())
mc4 = abs(pandas.read_csv("linmod_kf_var999_mc2.csv", header=None).as_matrix())


rows, cols = mc1.shape  # all will have the same dimension
ts = [x/10 for x in range(801)]

# Now plot 90 % confidence regions!
plt.figure()
plt.subplot(4, 1, 1)  # mean
for k in range(cols):
    plt.plot(ts, mc1[:, k], "k-", linewidth=0.5)

plt.plot(ts, numpy.ones(rows)*0.49, "g-", linewidth=3.0)
plt.ylabel(r"C$_A$ (I)")
plt.locator_params(nbins=4)

plt.subplot(4, 1, 2)  # 90%
for k in range(cols):
    plt.plot(ts, mc2[:, k], "k-", linewidth=0.5)

plt.plot(ts, numpy.ones(rows)*0.49, "g-", linewidth=3.0)
plt.ylabel(r"C$_A$ (II)")
plt.locator_params(nbins=4)

plt.subplot(4, 1, 3)  # 99%
for k in range(cols):
    plt.plot(ts, mc3[:, k], "k-", linewidth=0.5)

plt.plot(ts, numpy.ones(rows)*0.49, "g-", linewidth=3.0)
plt.ylabel(r"C$_A$ (III)")
plt.locator_params(nbins=4)

plt.subplot(4, 1, 4)  # 99.9%
for k in range(cols):
    plt.plot(ts, mc4[:, k], "k-", linewidth=0.5)

plt.plot(ts, numpy.ones(rows)*0.49, "g-", linewidth=3.0)
plt.ylabel(r"C$_A$ (IV)")
plt.locator_params(nbins=4)
plt.xlabel("Time [min]")

A = 412
mcerr1 = 0
for k in range(cols):
    mcerr1 += abs(Results.calc_error3(mc1[-100:-1, k], A))

print("The average MC error is:", mcerr1/cols)

mcerr2 = 0
for k in range(cols):
    mcerr2 += abs(Results.calc_error3(mc2[-100:-1, k], A))

print("The average MC error is:", mcerr2/cols)

mcerr3 = 0
for k in range(cols):
    mcerr3 += abs(Results.calc_error3(mc3[-100:-1, k], A))

print("The average MC error is:", mcerr3/cols)

mcerr4 = 0
for k in range(cols):
    mcerr4 += abs(Results.calc_error3(mc4[-100:-1, k], A))

print("The average MC error is:", mcerr4/cols)

plt.show()
