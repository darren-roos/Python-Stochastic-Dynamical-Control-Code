# plt.plotting and results analysis module
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy
import src.Ellipse as Ellipse

mpl.rc("figure", figsize=(6, 3))  # 6, 3


def plot_tracking1(ts, xs, ys, fmeans, us, obs, setpoint):

    tend = ts[-1]
    setpoints = numpy.ones(len(ts))*setpoint

    umax = max(abs(us))
    if umax == 0:
        subplt = 2
    else:
        subplt = 3

    mpl.rc("font", family="serif", serif="Computer Modern", size=8)
    mpl.rc("text", usetex=True)

    skipmeas = int(len(ts) / 80)
    skipmean = int(len(ts) / 40)
    plt.figure()
    plt.subplot(subplt, 1, 1)
    x1, = plt.plot(ts, xs[0, :], "k", linewidth=3)
    if obs == 2:  # plt.plot second measurement
        plt.plot(ts[::skipmeas], ys[0][::skipmeas], "kx", markersize=5, markeredgewidth=1)

    plt.plot(ts[::skipmean], fmeans[0][::skipmean], "bx", markersize=5, markeredgewidth=2)
    plt.plot(ts, setpoints, "g-", linewidth=3)
    plt.ylabel(r"C$_A$ [kmol.m$^{-3}$]")
    plt.locator_params(nbins=4)
    plt.legend([x1], ["Underlying model"], loc="best")
    plt.xlim([0, tend])
    # ylim([0, 1])

    plt.subplot(subplt, 1, 2)
    plt.plot(ts, xs[1, :], "k", linewidth=3)
    if obs == 1:
        y2, = plt.plot(ts[::skipmeas], ys[::skipmeas], "kx", markersize=5, markeredgewidth=1)
    else:
        y2, = plt.plot(ts[::skipmeas], ys[1][::skipmeas], "kx", markersize=5, markeredgewidth=1)

    k2, = plt.plot(ts[::skipmean], fmeans[1][::skipmean], "bx", markersize=5, markeredgewidth=2)
    plt.ylabel(r"T$_R$ [K]")
    plt.locator_params(nbins=4)
    plt.legend([k2, y2], ["Filtered mean", "Observations"], loc="best")
    plt.xlim([0, tend])
    # ylim([minimum(xs[2, :]), maximum(xs[2, :])])
    if subplt == 3:
        plt.subplot(subplt, 1, 3)
        plt.plot(ts, (1 / 60.0) * us)
        plt.xlim([0, tend])
        plt.ylabel("Q [kW]")

    plt.locator_params(nbins=4)
    plt.xlabel("Time [min]")


def plot_tracking(ts, xs, ys, fmeans, us, obs):
    tend = ts[-1]

    umax = max(abs(us))
    if umax == 0:
        subplt = 2
    else:
        subplt = 3
    
    mpl.rc("font", family="serif", serif="Computer Modern", size=8)
    mpl.rc("text", usetex=True)

    skipmeas = int(len(ts)/80)
    skipmean = int(len(ts)/40)
    plt.figure()
    ax = plt.subplot(subplt, 1, 1)
    x1, = plt.plot(ts, xs[0, :], "k", linewidth=3)
    if obs == 2:  # plt.plot second measurement
        plt.plot(ts[::skipmeas], ys[0][::skipmeas], "kx", markersize=5, markeredgewidth=1)

    plt.plot(ts[::skipmean], fmeans[0][::skipmean], "bx", markersize=5, markeredgewidth=2)
    plt.ylabel(r"C$_A$ [kmol.m$^{-3}$]")
    plt.locator_params(nbins=4)
    plt.legend([x1], ["Underlying model"], loc="best")
    plt.xlim([0, tend])
    plt.ylim(ymax=1.5)
    # ylim([0, 1])
    # plt.setp(ax.get_xticklabels(), visible=False)

    plt.subplot(subplt, 1, 2)
    plt.plot(ts, xs[1, :], "k", linewidth=3)
    if obs == 1:
        y2, = plt.plot(ts[::skipmeas], ys[::skipmeas], "kx", markersize=5, markeredgewidth=1)
    else:
        y2, = plt.plot(ts[::skipmeas], ys[1][::skipmeas], "kx", markersize=5, markeredgewidth=1)
    
    k2, = plt.plot(ts[::skipmean], fmeans[1][::skipmean], "bx", markersize=5, markeredgewidth=2)
    plt.ylabel(r"T$_R$ [K]")
    plt.locator_params(nbins=4)
    plt.legend([k2, y2], ["Filtered mean", "Observations"], loc="best")
    plt.xlim([0, tend])
    # plt.ylim([340, 420])

    if subplt == 3:
        plt.subplot(subplt, 1, 3)
        plt.plot(ts, (1/60.0)*us)
        plt.xlim([0, tend])
        plt.ylabel("Q [kW]")
    
    plt.locator_params(nbins=4)
    plt.xlabel("Time [min]")
    # plt.subplots_adjust(wspace=0, hspace=0)
    

def plot_state_space_switch(linsystems, xs):
    mpl.rc("font", family="serif", serif="Computer Modern", size=8)
    mpl.rc("text", usetex=True)
    plt.figure()  # Model and state space
    for k in range(len(linsystems)):
        plt.plot(linsystems[k].op[0], linsystems[k].op[1], "kx", markersize=5, markeredgewidth=1)
        plt.annotate(r"$M_" + str(k+1) + r"$",
                     xy=[linsystems[k].op[0], linsystems[k].op[1]],
                     xytext=[linsystems[k].op[0], linsystems[k].op[1]],
                     fontsize=12.0,
                     ha="center",
                     va="bottom")
        
    plt.plot(xs[0], xs[1], "k", linewidth=3)
    plt.plot(xs[0][0], xs[1][0], "ko", markersize=10, markeredgewidth=4)
    plt.plot(xs[0][-1], xs[1][-1], "kx", markersize=10, markeredgewidth=4)
    plt.xlim([-0.1, 1.1])
    plt.ylim([300, 550])
    plt.xlabel(r"C$_A$ [kmol.m$^{-3}$]")
    plt.ylabel(r"T$_R$ [K]")
    

def plot_switch_selection(numSwitches, strack, ts, cbaron):

    plt.figure()  # Model selection
    mpl.rc("font", family="serif", serif="Computer Modern", size=8)
    mpl.rc("text", usetex=True)
    axes = [None]*numSwitches
    im = 0
    width = 1
    for k in range(numSwitches):
        ax = plt.subplot(numSwitches, 1, k+1)
        axes[k] = ax
        if cbaron:
            im = plt.imshow([strack[k, :] * width], cmap="cubehelix_r",
                            vmin=0, vmax=1, interpolation="nearest", aspect="auto")
        else:
            im = plt.imshow([strack[k, :] * width], cmap="binary",
                            vmin=0.0, vmax=1, interpolation="nearest", aspect="auto")
        
        plt.tick_params(axis="y", which="both", left="off", right="off", labelleft="off")
        plt.tick_params(axis="x", which="both", bottom="off", labelbottom="off")
        plt.ylabel(r"$M_" + str(k+1) + r"$")

    plt.tick_params(axis="x", labelbottom="on")
    tempts = range(0, len(ts), int(len(ts)/10.0))
    temp = [None]*len(tempts)
    for lat in range(len(tempts)):
        temp[lat] = ts[tempts[lat]]

    plt.xticks(tempts, temp)

    if cbaron:
        plt.colorbar(im, ax=axes)
    
    plt.xlabel("Time [min]")


def plot_ellipses1(ts, xs, fmeans, fcovars, legloc):

    mpl.rc("font", family="serif", serif="Computer Modern", size=8)
    mpl.rc("text", usetex=True)
    N = len(ts)
    skip = int(len(ts)/40)
    plt.figure()
    b1 = 0.0
    for k in range(N):
        p1, p2 = Ellipse.ellipse(fmeans[:, k], fcovars[:, :, k])
        # b1, = plt.plot(p1, p2, "b")
        b1, = plt.fill(p1, p2, "b", edgecolor="none")
    
    x1, = plt.plot(xs[0, :], xs[1, :], "k", linewidth=3)
    f1, = plt.plot(fmeans[0][::skip], fmeans[1][::skip], "mx", markersize=5, markeredgewidth=2)
    plt.plot(xs[0, 0], xs[1, 0], "ko", markersize=10, markeredgewidth=4)
    plt.plot(xs[0, -1], xs[1, -1], "kx", markersize=10, markeredgewidth=4)
    plt.ylabel(r"T$_R$ [K]")
    plt.xlabel(r"C$_A$ [kmol.m$^{-3}$]")
    plt.legend([x1, f1, b1], ["Underlying model", "Filtered mean", r"90$\%$ Confidence region"], loc=legloc)


def plot_ellipses2(ts, xs, fmeans, fcovars,  line, sp, nf, sigma, pick, legloc):

    mpl.rc("font", family="serif", serif="Computer Modern", size=8)
    mpl.rc("text", usetex=True)
    N = len(ts)
    skip = int(len(ts)/40)

    if nf:
        plt.figure()  # only create a new plt.figure if required
    b1 = 0.0
    for k in range(N):
        p1, p2 = Ellipse.ellipse(fmeans[:, k], fcovars[:, :, k], sigma)
        # b1, = plt.plot(p1, p2, "b")
        b1, = plt.fill(p1, p2, "b", edgecolor="none")
    
    x1, = plt.plot(xs[0], xs[1], "k", linewidth=3)
    f1, = plt.plot(fmeans[0][::skip], fmeans[1][::skip], "mx", markersize=5, markeredgewidth=2)
    # plt.plot(xs[1, ::skip], xs[2, ::skip], "kx", markersize=5, markeredgewidth=2)
    plt.plot(xs[0, 0], xs[1, 0], "ko", markersize=10, markeredgewidth=4)
    plt.plot(xs[0, -1], xs[1, -1], "kx", markersize=10, markeredgewidth=4)

    # line = [b, c] => y + bx + c = 0
    # line => y = - bx - c

    lxs = numpy.array([x/100 for x in range(-10, 110, 5)])
    lys = -line[0]*lxs - line[1]
    plt.xlim([min(xs[0, :]-1e-1), max(xs[0, :]+1e-1)])
    plt.ylim([min(xs[1, :]-10), max(xs[1, :]+10)])
    plt.plot(lxs, lys, "r-")
    plt.xlim(xmin=0)

    plt.plot(sp[0], sp[1], "gx", markersize=8, markeredgewidth=4)

    plt.ylabel(r"T$_R$ [K]")
    plt.xlabel(r"C$_A$ [kmol.m$^{-3}$]")
    # conf = round((1 - exp(-sigma/2.0))*100.0, 3)
    # temp = latexstring(conf, "\%", "Confidence~Region")
    # legend([x1, f1, b1], [r"Underlying~Model", r"Filtered~Mean", temp], loc="best")
    if pick == 0:
        plt.legend([x1, f1, b1], ["Underlying model", "Filtered mean", r"90$\%$ Confidence region"], loc=legloc)
    elif pick == 1:
        plt.legend([x1, f1, b1], ["Underlying model", "Filtered mean", r"99$\%$ Confidence region"], loc=legloc)
    elif pick == 2:
        plt.legend([x1, f1, b1], ["Underlying model", "Filtered mean", r"99.9$\%$ Confidence region"], loc=legloc)
    else:
        plt.legend([x1, f1, b1], ["Underlying model", "Filtered mean", r"99.99$\%$ Confidence region"], loc=legloc)


def plot_ellipse_comp(f1means, f1covars, f2means, f2covars, xs, ts, sigma=4.605):

    N = len(ts)
    skip = int(len(ts)/30)
    plt.figure()
    mpl.rc("font", family="serif", serif="Computer Modern", size=8)
    mpl.rc("text", usetex=True)
    x1, = plt.plot(xs[0], xs[1], "k", linewidth=3)
    f1, = plt.plot(f1means[0][::skip], f1means[1][::skip], "yx", markersize=5, markeredgewidth=2)
    f2, = plt.plot(f2means[0][::skip], f2means[1][::skip], "gx", markersize=5, markeredgewidth=2)
    b1 = 0.0
    b2 = 0.0
    for k in range(N):
        p1, p2 = Ellipse.ellipse(f1means[:, k], f1covars[:, :, k], sigma)
        # b1, = plt.plot(p1, p2, "r")
        b1, = plt.fill(p1, p2, "r", edgecolor="none")

        p3, p4 = Ellipse.ellipse(f2means[:, k], f2covars[:, :, k], sigma)
        # b2, = plt.plot(p3, p4, "b")
        b2, = plt.fill(p3, p4, "b", edgecolor="none")

    plt.plot(xs[0, 0], xs[1, 0], "ko", markersize=10, markeredgewidth=4)
    plt.plot(xs[0, -1], xs[1, -1], "kx", markersize=10, markeredgewidth=4)
    plt.ylabel(r"T$_R$ [K]")
    plt.xlabel(r"C$_A$ [kmol.m$^{-3}$]")
    plt.legend([x1, f1, f2, b1, b2], ["Underlying model", "Particle filter", "Kalman filter",
                                      r"PF 90$\%$ Confidence region", r"KF 90$\%$ Confidence region"], loc="best")


def plot_tracking_break(ts, xs, xsb, ys, fmeans, obs):

    tend = ts[-1]
    skipm = int(len(ts)/80)
    plt.figure()  # plt.plot filtered results
    mpl.rc("font", family="serif", serif="Computer Modern", size=8)
    mpl.rc("text", usetex=True)
    plt.subplot(2, 1, 1)
    x1, = plt.plot(ts, xs[0, :], "k", linewidth=3)
    plt.plot(ts, xsb[0, :], "g--", linewidth=3)
    if obs == 2:
        plt.plot(ts[::skipm], ys[0][::skipm], "kx", markersize=5, markeredgewidth=1)
    
    k1, = plt.plot(ts, fmeans[0, :], "r--", linewidth=3)
    plt.ylabel(r"C$_A$ [kmol.m$^{-3}$]")
    plt.locator_params(nbins=4)
    plt.legend([x1, k1], ["Underlying model", "Filtered mean"], loc="best")
    plt.xlim([0, tend])
    plt.subplot(2, 1, 2)
    plt.plot(ts, xs[1, :], "k", linewidth=3)
    x2nf, = plt.plot(ts, xsb[1, :], "g--", linewidth=3)
    if obs == 1:
        y2, = plt.plot(ts[::skipm], ys[::skipm], "kx", markersize=5, markeredgewidth=1)
    else:
        y2, = plt.plot(ts[::skipm], ys[1][::skipm], "kx", markersize=5, markeredgewidth=1)
    
    plt.plot(ts, fmeans[1, :], "r--", linewidth=3)
    plt.ylabel(r"T$_R$ [K]")
    plt.locator_params(nbins=4)
    plt.xlabel("Time [min]")
    plt.legend([y2, x2nf], ["Observations", "Underlying model w/o fault"], loc="best")
    plt.xlim([0, tend])
    

def plot_tracking_two_filters(ts, xs, ys, f1means, f2means):

    skipm = int(len(ts)/80)
    skip = int(len(ts)/40)
    tend = ts[-1]
    plt.figure()  # plt.plot filtered results
    mpl.rc("font", family="serif", serif="Computer Modern", size=8)
    mpl.rc("text", usetex=True)
    plt.subplot(2, 1, 1)
    x1, = plt.plot(ts, xs[0, :], "k", linewidth=3)
    k1, = plt.plot(ts[::skip], f1means[0][::skip], "rx", markersize=5, markeredgewidth=2)
    plt.plot(ts[::skipm], ys[0][::skipm], "kx", markersize=5, markeredgewidth=1)
    plt.plot(ts[::skip], f2means[0][::skip], "bx", markersize=5, markeredgewidth=2)
    plt.ylabel(r"C$_A$ [kmol.m$^{-3}$]")
    plt.legend([x1, k1], ["Underlying model", "Particle filter"], loc="best", ncol=2)
    plt.xlim([0, tend])
    plt.subplot(2, 1, 2)
    plt.plot(ts, xs[1, :], "k", linewidth=3)
    y2, = plt.plot(ts[::skipm], ys[1][::skipm], "kx", markersize=5, markeredgewidth=1)
    plt.plot(ts[::skip], f1means[1][::skip], "rx", markersize=5, markeredgewidth=2)
    k22, = plt.plot(ts[::skip], f2means[1][::skip], "bx", markersize=5, markeredgewidth=2)
    plt.ylabel(r"T$_R$ [K]")
    plt.xlabel("Time [min]")
    plt.legend([y2, k22], ["Observations", "Kalman filter"], loc="best", ncol=2)
    plt.xlim([0, tend])
    

def plot_kl_div(ts, kldiv, basediv, unidiv, logged):
    mpl.rc("font", family="serif", serif="Computer Modern", size=8)
    mpl.rc("text", usetex=True)

    plt.figure()
    if logged:
        kl, = plt.semilogy(ts, kldiv, "r", linewidth=3)
        gd, = plt.semilogy(ts, basediv, "b", linewidth=3)
        ud, = plt.semilogy(ts, unidiv, "g", linewidth=3)
    else:
        kl, = plt.plot(ts, kldiv, "r", linewidth=3)
        gd, = plt.plot(ts, basediv, "b", linewidth=3)
        ud, = plt.plot(ts, unidiv, "g", linewidth=3)
    
    plt.xlabel("Time [min]")
    plt.ylabel("Divergence [Nats]")
    plt.legend([kl, gd, ud], ["Approximation", "Baseline", "Uniform"], loc="best")
    

def calc_error(x, y):

    r, N = x.shape
    avediff1 = (1/N)*sum([abs((xt-yt) / xt) for xt, yt in zip(x[0], y[0])])*100
    avediff2 = (1/N)*sum([abs((xt-yt) / xt) for xt, yt in zip(x[1], y[1])])*100

    print("Average Concentration Error: ", round(avediff1, 4),  "%")
    print("Average Temperature Error: ", round(avediff2, 4), "%")
    return avediff1, avediff2


def calc_error1(x, y):

    r, N = numpy.shape(x)
    avediff1 = (1/N)*sum(abs(numpy.divide((x[0] - y), y)))*100
    print("Average Concentration Error: ", round(avediff1, 4),  "%")
    return avediff1


def calc_error2(x, y):

    r, N = len(x)
    avediff1 = (1/N)*sum(abs((x[0] - y)/y))*100

    return avediff1


def calc_error3(x, y):

    N = len(x)
    avediff1 = (1/N)*sum(abs((x - y)/y))*100

    return avediff1


def calc_energy(us, uss):
    N = len(us)
    avecost = (1/(60*N))*sum(abs(us-uss))
    print("Average Input (kW): ", avecost)
    return avecost


def check_constraint(ts, xs, line):
    """line = [b, c] => y + bx + c = 0
    line => y = - bx - c"""
    r, N = xs.shape
    conmargin = numpy.zeros([N])
    minneg = float("inf")
    minpos = float("inf")
    for k in range(N):
        temp = xs[1, k] + xs[0, k]*line[0] + line[1]
        if temp < 0:
            conmargin[k] = -abs(temp)/numpy.sqrt(line[0]**2 + 1)
            if minneg > abs(temp)/numpy.sqrt(line[0]**2 + 1):
                minneg = abs(temp)/numpy.sqrt(line[0]**2 + 1)
            
        else:
            conmargin[k] = abs(temp)/numpy.sqrt(line[0]**2 + 1)
            if minpos > abs(temp)/numpy.sqrt(line[0]**2 + 1):
                minpos = abs(temp)/numpy.sqrt(line[0]**2 + 1)

    print("Minimum Positive Clearance: ", minpos)
    print("Minimum Negative Clearance: ", minneg)

    plt.figure()
    mpl.rc("font", family="serif", size=8)
    mpl.rc("text", usetex=True)

    plt.plot(ts, numpy.zeros([N]), "r", linewidth=1)
    plt.plot(ts, conmargin, "k", linewidth=3)
    plt.xlabel(r"Time [min]")
    plt.ylabel(r"Clearance")
    

def get_mc_res(xs, sigmas, line, mcdistmat, counter, h):
    """line = [b, c] => y + bx + c = 0
    line => y = - bx - c"""
    d = numpy.array([line[0], 1])
    r, N = xs.shape
    negdist = 0
    timeviolated = 0
    for k in range(N):
        temp = xs[1, k] + xs[0, k]*line[0] + line[1]  # check constraint
        if temp < 0:
            negdist += -abs(temp)/numpy.sqrt(d @ sigmas[:, :, k] @ d)
            timeviolated += 1

    mcdistmat[0, counter] = negdist*h  # area integral
    mcdistmat[1, counter] = timeviolated*h  # in minutes
    return mcdistmat



