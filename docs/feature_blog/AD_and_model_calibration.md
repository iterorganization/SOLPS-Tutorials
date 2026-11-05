# AD and model calibration

/// warning | This feature blog entry introduces advanced concepts
The reader is assumed to know their way around the [Wide Grids SOLPS-ITER version](./Wide_grids.md).
///


## Motivation

SOLPS-ITER simulations (and users) suffer, among others, from two distinct problems:

1. SOLPS-ITER does not know the physics behind cross-field transport in the tokamak edge plasma. Instead, it assumes that the cross-field transport is purely diffusive (with a possible convective component) and that the user knows best which diffusion coefficients $D_\perp$, $\chi_e$ and $\chi_i$ to use.
2. SOLPS-ITER users usually achieve the desired simulation results, such as a match with experimental measurements, by iterating "run simulation - adjust inputs - run simulation". Finding the best set of input parameters is tedious, especially in H-mode. And then someone looks at your hard-won simulation and asks: "Okay, you used $D_\perp = 0.3$ m<sup>2</sup>s<sup>-1</sup>. But what if you changed that to $D_\perp = 0.6$ m<sup>2</sup>s<sup>-1</sup>? Would that still work? What are the uncertainties of your inputs?"

Let's call these problems the *diffusive ansatz* (choosing anomalous diffusion coefficients) and the *inverse problem* (choosing the best simulation inputs based on the desired solution).

The good news is that, one, a lot of people are tackling the inverse problem [[Carli 2026 preprint](https://arxiv.org/pdf/2609.27435)<span class="material-symbols-outlined">open_in_new</span>, Sec. 2.1], and two, a particular branch of SOLPS-ITER takes on both problems at once. This is the **algorithmic differentiation (AD) branch `feature/ad-wg`**. This tutorial is about using this branch to make SOLPS-ITER simulations.

/// hint | Further reading
- S. Carli, [Calibration of cross-field transport models in SOLPS-ITER on the TCV-X21 case](https://arxiv.org/pdf/2609.27435)<span class="material-symbols-outlined">open_in_new</span>, preprint
- [SOLPS-ITER manual](../supplementary/SOLPS-ITER_user_wisdom.md#rtfm), chapter 10 *Sensitivity calculation and optimization in B2.5*
///


## Introduction

### The K-model

The $\kappa$-model is a fully fledged alternative to the diffusive ansatz. It supplements the set of B2.5 equations with a new equation, which solves for a new plasma parameter: the turbulent kinetic energy $\kappa$. This new basic plasma parameter is, like density or temperature, defined on the entire 2D grid of B2.5. It captures the average strength of turbulence passing through each cell and can be used to calculate diffusion coefficients. For example,

$$D_\perp = C_D \frac{\kappa / m_i}{\sqrt{\kappa/m_i}/\rho_L + C_S \left|S_{mean}\right|} + D_{min}$$

where $m_i$ is the ion mass, $\rho_L$ is the local Larmor radius, $S_{mean} = \nabla_r V_{E \times B, \perp}$ is the radial shear of the diamagnetic $E \times B$ velocity... and $C_D$ and $C_S$ are free parameters.

Yeah, it isn't for free. You've just got rid of free parameters $D_\perp$, $\chi_e$ and $\chi_i$, and you're already saddled with *ten* new free parameters: $C_D$, $C_S$, $C_{\chi,e}$, $C_{\chi,i}$, $C_\nu$, $C_\kappa$, $C_{ie}$, $C_{\sigma_\parallel,1}$, $C_{\sigma_\parallel,2}$ and $C_\eta$. At least these are constants, while diffusivities often vary radially. And at any rate, you don't need to worry about setting their values. The built-in algorithmic differentiation and model calibration will do it for you!

/// hint | Further reading
- R. Coosemans et al, [A new mean-field plasma edge transport model based on turbulent kinetic energy and enstrophy](https://onlinelibrary.wiley.com/doi/abs/10.1002/ctpp.201900156)<span class="material-symbols-outlined">open_in_new</span>, Contributions to Plasma Physics **60** (2020) e201900156
- R. Coosemans et al, [Turbulent kinetic energy in 2D isothermal interchange-dominated scrape-off layer ExB drift turbulence: Governing equation and relation to particle transport](https://pubs.aip.org/aip/pop/article/28/1/012302/1032004)<span class="material-symbols-outlined">open_in_new</span>, Physics of Plasmas **28** (2021) 012302
- R. Coosemans et al, [Bayesian analysis of turbulent transport coefficients in 2D interchange dominated ExB turbulence involving flow shear](https://iopscience.iop.org/article/10.1088/1742-6596/1785/1/012001/meta)<span class="material-symbols-outlined">open_in_new</span>, Journal of Physics: Conference Series **1785** (2021) 012001
- R. Coosemans et al, [A self-consistent mean-field model for turbulent particle and heat transport in 2D interchange-dominated electrostatic ExB turbulence in a sheath-limited scrape-off layer](https://onlinelibrary.wiley.com/doi/abs/10.1002/ctpp.202100193)<span class="material-symbols-outlined">open_in_new</span>, Contributions to Plasma Physics **62** (2022) e202100193
- W. Dekeyser et al, [A self-consistent K-model for anomalous transport due to electrostatic, interchange-dominated ExB drift turbulence in the scrape-off layer and implementation in SOLPS-ITER](https://onlinelibrary.wiley.com/doi/abs/10.1002/ctpp.202100190)<span class="material-symbols-outlined">open_in_new</span>, Contributions to Plasma Physics (2022) e202100190
- R. Coosemans et al, [Mean-field transport equations and energy theorem for plasma edge turbulent transport](https://doi.org/10.1017/S0022377824000163)<span class="material-symbols-outlined">open_in_new</span>, Journal of Plasma Physics **90** (2024) 905900202
///


### Algorithmic differentiation and model calibration

Algorithmic differentiation and model calibration is a method to formalise and automatise the iterative search for optimal simulation inputs. It involves differentiating the SOLPS-ITER equations using an automatic algorithm, hence algorithmic differentiation, and calibrating input parameters of the SOLPS model of plasma, hence model calibration.

When a SOLPS-ITER user is gauging the match of their simulation outputs to experimental data, they usually use the metric of the eye. In Czech, it's called "kouknu, vidim" ("I look, I see"). It's cheap and easy, but only qualitative. A more rigorous approach is to use a **cost function**. A cost function compares experimental and simulation data and mashes them all together to produce a number, for example by calculating the root mean square. The lower this number is, the better the simulation matches the experiment. Thus, searching for the optimal SOLPS inputs becomes *finding a minimum of the cost function*.

Say you already have an initial SOLPS simulation, the first converged solution with rough guesses for densities, powers and diffusivities. In the manual tuning approach, you'd pick one or two input parameters and adjust them according to your intuition. For example:

> "The target temperature is high. I'll raise the separatrix density by 10 % to increase the target density and decrease the target temperature. I'll also increase $D_\perp$ by 50 % to have a flatter upstream $n_e$ profile".

AD does something similar, except it orients itself with the **gradient of the cost function**. The gradient can calculated with the so-called *adjoint method* or the *tangent method*, in both cases using a Jacobian of the B2.5 equations themselves. Esentially, the algorithm differentiates each equation in the code with regard to each SOLPS input parameter. When this Jacobian is evaluated at the point of your initial simulation, it tells you how to change the inputs so that the new solution has a lower cost function value (moving down the gradient). The Jacobian is huge, but it only need be calculated once for a given set of equations. Then, the algorithm automatically iterates "run simulation - adjust inputs so cost function value falls - run simulation" until you have a solution that matches the experimental data as well as it can.

The real implementation is, of course, more complicated. It involves uncertainty quantification (UQ), so if you know the uncertainty of your diagnostics measurements, you get errorbars not only on simulation inputs but also on its results. You can choose which parameters to optimise for and which to keep constant, since some may compensate for each other. You can choose which diagnostics to compare against, and what weight you'll give to each measurement. But the essential thing to remember about AD is that it helps you find the optimal input parameters to match the desired plasma solution, and it does so by differentiating the B2.5 equations.

/// hint | Further reading
- M. Baelmans et al, [Efficient parameter estimation in 2D transport models based on an adjoint formalism](https://iopscience.iop.org/article/10.1088/0741-3335/56/11/114009/meta)<span class="material-symbols-outlined">open_in_new</span>, Plasma Physics and Controlled Fusion **56** (2014) 114009
- S. Carli et al, [Bayesian MAP-estimation of turbulence model parameters using Algorithmic Differentiation in SOLPS-ITER](https://www.researchgate.net/profile/Stefano-Carli-2/publication/357363647_Bayesian_maximum_a_posteriori-estimation_of_k_turbulence_model_parameters_using_algorithmic_differentiation_in_SOLPS-ITER/links/61dc0c7b323a2268f99462dc/Bayesian-maximum-a-posteriori-estimation-of-k-turbulence-model-parameters-using-algorithmic-differentiation-in-SOLPS-ITER.pdf)<span class="material-symbols-outlined">open_in_new</span>, preprint
- S. Carli et al, [Algorithmic Differentiation for adjoint sensitivity calculation in plasma edge codes](https://www.sciencedirect.com/science/article/pii/S0021999123004989)<span class="material-symbols-outlined">open_in_new</span>, Journal of Computational Physics **491** (2023) 112403
- S. Carli et al, [Sensitivity analysis of plasma edge code parameters through algorithmic differentiation](https://www.sciencedirect.com/science/article/pii/S2352179118302321)<span class="material-symbols-outlined">open_in_new</span>, Nuclear Materials and Energy **18** 6-11
- N. Horsten et al, [Sensitivity calculation for Monte Carlo particle simulations of neutrals in the plasma edge](https://onlinelibrary.wiley.com/doi/abs/10.1002/ctpp.202300138)<span class="material-symbols-outlined">open_in_new</span>, Contributions to Plasma Physics **64** (2024) e202300138
///



## What you need to know before starting

- It is only available for the wide-grid version of SOLPS-ITER
- Read the documentation in the [SOLPS-ITER manual](#rtfm), section “Sensitivity calculation and optimization in B2.5”
- The AD code is almost always NOT in sync with the standard B2.5 code. With ‘sync’ I mean that the AD code is built upon a version of B2.5 at a certain commit (where the `feature/ad-wg` branch is). So, if you recently introduced a new feature, or you are interested in a certain bug fix that happened *after* the current `feature/ad-wg` branch, you need to re-differentiate B2.5 to produce a new version of the AD code. To do so, you can try on your own based on the documentation (see "Expert mode for AD" section in the [SOLPS-ITER manual](#rtfm)), and/or you can contact the KU Leuven group or S. Carli for support.
- You cannot use EIRENE, only (advanced) fluid neutrals. What you can do however, is optimize with fluid neutrals and then use the obtained parameters in your EIRENE run. They will likely need some adjustments but at least you don’t start from scratch. Alternatively, you can use the Bayesian optimization approach of S. Soldat (not public yet) [Soldat 2024](https://dspace.cvut.cz/server/api/core/bitstreams/5be84f4a-9029-4f6b-b9f7-b7c3ca2f24eb/content)<span class="material-symbols-outlined">open_in_new</span>, or the iterative scheme proposed by Antonello Zito (also not public) [Zito 2021](https://iopscience.iop.org/article/10.1088/1361-6587/abfcb6)<span class="material-symbols-outlined">open_in_new</span>,
- You need to have an already existing case which is converging or converged, i.e. residuals decrease towards machine precision. If your case has high, stagnating residuals, you can probably still use the AD code but be aware that the adjoint mode will likely not work as expected so better use the tangent one.
- At the moment (October 2026), for truly unstructured grids coming from GOAT, the cost function definition needs to be adjusted/verified

## Tips to set up and run your optimization

/// tip | Get started
Step-by-step instructions how to set up and run AD and model calibration are given in the [SOLPS-ITER manual](../supplementary/SOLPS-ITER_user_wisdom.md#rtfm), chapter 10 *Sensitivity calculation and optimization in B2.5*. This tutorial contains comments and tips on the workflow therein.
///

The experimental data for the cost function needs to be ‘cut’ so that no points lie outside of the related SOLPS-ITER mesh domain, otherwise the code will stop with error. If you chose to map target quantities to the OMP, this is done using $\psi$ and not the radial coordinate.

Since you already have a converging case, it is recommended that the initial guess `x0` specified in `b2.optimization.parameters` is whatever value you are currently using in your converging case. Setting these values in `b2.optimization.parameters` overwrites said values set in the usual input files (e.g. `b2mn.dat` , `b2.transport.parameters`, etc.).

At the beginning of the optimization, i.e. the first 10-ish optimization iterations, you are likely far from the optimum and as such you don’t need very precise gradients to take a good step towards the optimum. Therefore, you don’t need to fully converge SOLPS to machine precision for each optimization iteration. Later on in the optimization precision matters more and so to reach/fulfill strict optimization convergence tolerances (i.e. gradient being close to zero) you likely need to fully converge SOLPS to get precise gradients and cost function.

Reaching zero gradient is numerically extremely challenging so setting convergence tolerance of $10^{-4} – 10^{-6}$ is reasonable.

## How do I continue an optimization that has not reached convergence?

If the optimization ended successfully because it reached the max number of iterations required, then copy-paste `b2fstate` into `b2fstati`. Then, you’ll need to manually replace the initial guess `x0` in your `b2.optimization.parameters` with whatever parameter value was last printed in `run.log` (see for this documentation on scripts `run_info`, `results_tao.sh`, `result_bfgs.sh`, or use `$grep -i tao run.log`). The picture below shows the result of the command `$grep -i tao run.log` on a possible optimization.

![AD parameters values](../img/AD_find_parameters_values.png)

/// warning | Beware!
When you restart your optimization the BFGS matrix and history are emptied, and the gradient (depending on which optimizer and options you are using) is re-normalized using the first gradient computed in the re-started case: this means that even though the gradient may be small in magnitude, the line-search may attempt too large steps, and therefore crash! See below on common pitfalls on how to deal with this.
///

## How to interpret the optimization output printed in `run.log`?

The pics below are the outcome of `$grep -i tao run.log`

![AD run.log 1](../img/AD_run_dot_log_1.png)
![AD run.log 2](../img/AD_run_dot_log_2.png)

## How to interpret residuals plots?

The first figure below is the outcome of `resall_D` on an optimization case for which 8000 B2.5 iterations per optimization iteration are used. B2.5 will write in `b2ftrace` the residuals both when it computes the gradient and when it performs a linesearch attempt. The sudden jumps in the residuals are normal, and are a consequence of the linesearch. 

Take for example the first optimization iteration: 
- the optimizer will first of all compute the gradient with the initial guess $x_0$, and converge for 8000 iterations
- then it will attempt a new value $x_1\neq x_0$, which the current plasma state does not satisfy, hence the jump in residuals. The linesearch also converges for 8000 iterations.
- If the linesearch is successful, then the gradient is computed for the same $x_1$ just attempted, therefore no jumps in the residuals! 

Note for example towards the right of the figure the three linesearch attempts: each of them converges for 8000 iterations, and only the third is successful and allows the gradient computation. This type of plot will be the same when using tangent or adjoint AD.

![AD residuals 1](../img/AD_residuals_1.png)

Turning now to the plot of the residuals of the differentiated equations, the figure below shows the case when using tangent AD, obtained with `resall_D_diff`. The plot refers to the same optimization as above, but is slightly different now, because B2.5 writes this residual information in `b2ftraced` only when the gradient computation routine is called. However, the iteration counter keeps increasing even if the routine is not called, which causes the ‘gaps’ where the last residual of the previous gradient computation is connected with a straight line to the first residual of the new gradient computation. Note how the three linesearch attempts on the right of the figure leave a larger gap.

![AD residuals 2](../img/AD_residuals_2.png)

For adjoint AD one uses instead the `res_adj script`: the figure will show a single line instead of one line for each equation solved and no gaps since the adjoint code writes this information directly in `run.log`.

## How do I know if my optimization was successful?

Do `$tail PETSC-TAO.OUT` after running the script `result_tao.sh`, the outcome is something like the picture below. 

![AD optimization summary](../img/AD_optimization_summary.png)

A converged case will show something like this, with convergence being either because of tolerance or maximum iteration count. Failure of the optimization means Line Search Failure. When B2.5 itself crashes with `xerrab` there is no additional output from the optimization.

## Some common pitfalls and suggestions

Commons cause for optimization to crash is that the optimizer attempts too large steps in the linesearch and B2.5 crashes. To deal with these see the [SOLPS-ITER manual](#rtfm), section “Run an optimization” or Appendix A of the paper [Carli 2026](https://arxiv.org/abs/2609.27435)<span class="material-symbols-outlined">open_in_new</span>: 
- one can typically reduce the maximum step size that the line search will attempt (default is 1) (This feature seems no longer present in more recent versions of PETSc/TAO, e.g. `3.15.1`. One ‘hotfix’ to avoid poorly scaled steps is `-tao_bqnls_mat_lmvm_scale_type NONE`, but this might be undesirable); 
- and/or gradually modify the model parameters from their value at the previous iteration to the new value;
- and/or reset drifts to a lower percentage strength and gradually increase them back to 100%.

Line Search Failure happens when the optimizer, with the current value of the gradient, cannot find a point along the gradient direction wrt which the cost function decreases. This often is caused by incomplete convergence of B2.5, so increasing `b2mndr_ntim` can help.

Also, if your simulation crashed or failed with Line Search Failure, you can still continue it: if you enabled saving the `b2fstate` file after each optimization iteration (see [SOLPS-ITER manual](#rtfm)), then you can pick the last successful optimization step by inspecting `run.log`, using the `b2fstate` saved at that iteration (found in `b2mn.exe.dir`) and copy-pasting into `b2.optimization.parameters` the parameters value at that specific iteration (see above on how to continue an optimization).

/// warning | Beware!
Restarting from the last successful step means, as explained above, that the BFGS matrix and history, and gradient normalization are reinitialized!
///

## Tips to re-differentiate the code

After the code has been re-differentiated and postprocessed (see again [SOLPS-ITER manual](#rtfm)), it is useful to just use the program `meld` to compare the new differentiated code and the old, or the differentiated code produced by Tapenade and the one postprocessed with scripts, to spot where differences appear and possible bugs. Since the differentiation introduces some bugs in the code, these have been automatized in a set of scripts. When differentiating a new B2.5 version some of these automatized bug fixes may fail or may not be sufficient, that is why `meld` comes useful. This was especially the case for routine `b2mod_driver_diff.F90` for adjoint AD, where extensive adjustments to the differentiated code are needed.
The best strategy to follow when re-differentiating the code is:
1. Differentiate in tangent (vector) mode: this is the easiest one, if this doesn’t work, forget about adjoint. Then compare old and new tangent code for possible differences/bugs.
2. Verify correctness of the tangent derivatives against finite differences (FD) (use the provided example case `$SOLPSTOP/runs/examples/COMPASS_sensitivity` and `COMPASS_sensitivity_D+T`). Typical accuracy of AD vs FD which can be obtained is $10^{-5}-10^{-8}$ in relative error (see [Carli 2023](https://www.sciencedirect.com/science/article/abs/pii/S0021999123004989)<span class="material-symbols-outlined">open_in_new</span>). If one specific parameter gives much lower sensitivity accuracy first check if its relative sensitivity $\frac{\partial \mathcal J}{\partial x_i } \frac{x_i}{\mathcal J}$ (with $\mathcal J$ the cost function and $x_i$ the model parameter) is much smaller compared to the others, if so, then the difference is very likely due to numerical truncation. If not, first check that the FD cases for this specific parameter are correctly setup and converged. If still persists, then there is likely a bug in the tangent code.
3. Verify that the optimization works as before on at least one example case
4. Differentiate in adjoint mode and compare old and new tangent code for possible differences/bugs.
5. Compare adjoint AD vs tangent AD sensitivities: these should reach almost machine precision accuracy $10^{-11}-10^{-14}$. If one specific parameter gives much lower sensitivity accuracy wrt tangent AD then it is likely that there is a bug in the adjoint (or tangent) code.

## Comparison of performance of built-in BFGS method vs PETSc/TAO BFGS method

The following table provides a comparison of the performance of the built-in BFGS method against the default PETSc/TAO (hereafter abbreviated in TAO) BFGS one (PETSc/TAO version `3.20.6`). In the table it is referred to the example cases distributed with SOLPS as:
- REG = `example_optim_reg_dna_hce_necore`
- DRIFT = `example_optim_reg_drift`
- CORR = `example_optim_map_dna_sigma_corr`
- GAUSS = `example_optim_map_dna_hce_gauss_prior`

If under a specific example case you see `tol = 1e-5` it means that for the built-in BFGS it was needed to lower the optimization convergence tolerance from `1e-4` to `1e-5` to obtain decent results (TAO still uses `1e-4`). Similarly, if you see `25 max iter` it means that the maximum number of optimization iterations allowed was increased for the built-in BFGS to obtain decent results. The other quantities should be self-explanatory: h0 = `lbfgs_h0_type`, theta  = `lbfgs_theta`; mem = `lbfgs_memsize`; max it = stopped because the maximum number of optimization iterations was reached; tol = stopped because one of the optimization convergence tolerances was met (doesn’t matter which one); LSF = Line Search Failure. The number between parenthesis indicate the number of optimization iterations needed to reach that specific result.

Color coding for *quality of result* i.e. how the built-in BFGS result compares against that of TAO (and of the synthetic data, since TAO is already pretty good).

![AD optimizer color coding](../img/AD_table_BFGS_color_coding.png)

![AD optimizer comparison](../img/AD_table_BFGS.png)

So overall, one can see that TAO performs better than the built-in BFGS one, both in terms of quality of result and also in iterations required to reach that result. The only exception is for example case GAUSS with h0=1, theta=0 and memsize=5/10, for which the built-in BFGS converges in 18 iterations wihile TAO in 24. Also, one can see that the best parameter set for the built-in BFGS is quite case-dependent. Overall, if using the built-in BFGS the scalar scaling version (`lbfgs_h0_type=0`) with larger memory (`lbfgs_memsize=10`) sems to give more consistent and better results compared to diagonal scaling `lbfgs_h0_type=1`, so these are set as default parameters until otherwise proven.
