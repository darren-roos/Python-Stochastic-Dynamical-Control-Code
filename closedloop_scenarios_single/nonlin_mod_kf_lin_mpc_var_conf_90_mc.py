# Linear Plant controlled with a linear MPC using a KF to estimate the state.
# Stochastic constraints.

import closedloop_scenarios_single.lin_mpc_var_conf

closedloop_scenarios_single.lin_mpc_var_conf.main(90, mcN=200, linear=False)
