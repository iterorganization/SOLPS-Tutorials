# Drifts

/// warning | This feature blog entry introduces advanced concepts
The reader is assumed to know how to [create a simple SOLPS-ITER simulation](../my_first_simulation/Creating_a_new_SOLPS-ITER_simulation.md) and to possess some [user wisdom](../supplementary/SOLPS-ITER_user_wisdom.md).
///

## Motivation

Charged particles in non-uniform magnetic and electric fields are subject to drifts of the guiding centre. For SOLPS-ITER modelling, the most important drifts are the *diamagnetic drift* and the *ExB drift*. By default, however, B2.5 fluid equations include drifts implicitly as part of the mysterious "anomalous diffusion". This is because including them explicitly is computationally expensive and introduces numerical instabilities, possibly because a different solver must be used. Still, drifts effects can be important under certain conditions (small machine, low magnetic field...), and turning them on in SOLPS-ITER can help you get far closer match to experimental data. This feature blog entry explains how to enable them.

|                      Pros                      |                                   Cons                                    |
| ---------------------------------------------- | ------------------------------------------------------------------------- |
| Better match with experiment (potentially)     | Computationally expensive                                                 |
| Better accuracy of predictions (theoretically) | Emotionally expensive (numerical issues, results not guaranteed) |
| Dabbling with often ignored physics            | Definitely not a magical solution for everything                          |


This tutorial contains the following sections:

- [Physics of tokamak drifts](#physics-of-tokamak-drifts)
- [Enable drifts](#enable-drifts-in-b2mndat) in `b2mn.dat` using the `b2news_fac*` switches
- [Modify boundary conditions](#modify-boundary-conditions-in-b2boundaryparameters) in `b2.boundary.parameters` to account for drifts
- [Apply speed-up schemes](#use-speed-up-schemes-in-b2numericsparameters) in `b2.numerics.parameters` to improve numerical stability and computational speed (under construction)
- [Run and troubleshoot](#run-and-troubleshoot) in case of crashes




## Physics of tokamak drifts

> <span class="material-symbols-outlined">construction</span> **TODO**: Describe more of drift physics than just the story of tildes.


In SOLPS-ITER literature and documentation, you'll encounter the diamagnetic drift under three names: the diamagnetic drift, the grad-B drift and the Pfirsch-Schlütter currents. Here's why.

The Braginskii equations, which lie at the heart of the B2.5 plasma solver, have the form *time derivative + divergence of flux = sources*. Drift terms appear mostly inside the divergences, as means of transporting particles, momentum and energy from cell to cell. As [[Rozhansky, 2001]](https://iopscience.iop.org/article/10.1088/0029-5515/41/4/305/meta)<span class="material-symbols-outlined">open_in_new</span> describes in section 2.1, one of these drift terms is the **diamagnetic drift**:

$$
V_\perp^{(dia)} = -\frac{1}{enB} \frac{1}{h_y} \frac{\partial (nT_i)}{\partial y}
\hspace{1cm}
\mathrm{and}
\hspace{1cm}
V_y^{(dia)} = \frac{B_z}{enB^2} \frac{1}{h_x} \frac{\partial (nT_i)}{\partial x}.
$$

This term is problematic when you put it inside a divergence, because first you differentiate the ion pressure $nT_i$ and then you have to differentiate it *again*. This causes numerical instabilities. Luckily, as [[Bufferand, 2016]](https://www.sciencedirect.com/science/article/pii/S2352179116301946)<span class="material-symbols-outlined">open_in_new</span> explains in formulas (11) and (12), the diamagnetic flux can be decomposed into two components: the so-called magnetization flux and the grad-B drift of the ion guiding centres. The magnetization flux divergence is, by definition, zero, and the second term in grad-B drift is usually negligible. This means that *inside the divergence*, the diamagnetic drift can be replaced by a part of the **grad-B drift**:

$$
\tilde{V}_\perp^{(dia)} = \frac{T_iB_z}{eb_z} \frac{1}{h_y} \frac{\partial}{\partial y} \left( \frac{1}{B^2} \right)
\hspace{1cm}
\mathrm{and}
\hspace{1cm}
\tilde{V}_y^{(dia)} = -\frac{T_iB_z}{e} \frac{1}{h_x} \frac{\partial}{\partial x} \left( \frac{1}{B^2} \right).
$$

This is great news! The magnetic field $B$ derivatives don't change between time steps because SOLPS-ITER is an electrostatic code, so you can just carefully precalculate them and get rid of the double differentiation. Or so they thought... until they tried modelling H-mode.

In formulas (7-9), [[Rozhansky, 2009]](https://iopscience.iop.org/article/10.1088/0029-5515/49/2/025007)<span class="material-symbols-outlined">open_in_new</span> describes the final transformation which was needed to facilitate drift simulations. It uses physics of the magnetic equilibrium. In a tokamak, the grad-B drift is vertical and of opposite direction for electrons and ions, so it causes vertical charge separation. The resulting electric field drives electric currents along the magnetic field lines. These are the **Pfirsch-Schlütter currents**, and their divergence is the same (taken negatively) as the divergence of the grad-B drift.

$\nabla( \textbf{j}_{grad-B} + \textbf{j}_{PS}) = 0$

Replacing the grad-B drift with Pfirsch-Schlütter currents inside divergences improves convergence further. This is why you'll encounter terms with "PSch" labels in the B2.5 equations, and why there are tildes ($\tilde{\Gamma}$) all over the place. The more tildes, the more numerical tricks have been applied to a quantity.

Agonisingly, the physical nature of these three phenomena is all different. Diamagnetic flows are cross-field and fluid, the grad-B drift is cross-field and for the guiding centre, and Pfirsch-Schlütter currents are parallel. If you calculate them on their own, their magnitude and direction is all different. The only thing they have in common is that their *divergence* is the same (save for the sign). So, keep in mind: inside divergences, diamagnetic, grad-B and Pfirsch-Schlütter are interchangeable, but if you're calculating real particle fluxes (like for energy convection), you have to use the entire diamagnetic drift formula.



## Enable drifts in `b2mn.dat`

Drift terms are enabled using 3 groups of switches in `b2mn.dat`, corresponding to 3 independent terms in the equations that can be activated:

- `b2news_facdrift`: diamagnetic terms, ion inertia current
- `b2news_facExB`: ExB drift terms
- `b2news_facvis`: drift viscosity

Each group contains 4 switches that are used to control a multiplicative factor $f$ in front of the term in the equation. The factor can be set to values in range $f \in [0.0, 1.0]$, where $0.0$ disables it and $1.0$ enables it completely. The switches are named as the name of the group + one of the following suffixes:

- `_start` - initial value, $f_0$
- `_target` - target value, $f_{target}$
- `_inc` - multiplicative increment, $f_{n+1} = A \cdot f_n$ on each timestep until $f_n = f_{target}$
- `_dec` - multiplicative decrement, applied when equations are not converging on that timestep

```{.fortran title="b2mn.dat"}
! A complete list, including the default values

'b2news_facdrift_start'  '0.0'
'b2news_facdrift_target' '0.0'
'b2news_facdrift_inc'    '1.0'
'b2news_facdrift_dec'    '0.0'

'b2news_facExB_start'    '0.0'
'b2news_facExB_target'   '0.0'
'b2news_facExB_inc'      '1.0'
'b2news_facExB_dec'      '0.0'

'b2news_facvis_start'    '0.0'
'b2news_facvis_target'   '0.0'
'b2news_facvis_inc'      '1.0'
'b2news_facvis_dec'      '0.0'
```

Possible approaches to setting the switches:

1. Constant profile $f(t)=const.$
    - Set `_inc = _dec = 1.0`, then $f_0 = f_n = f_{target}$ is kept during the whole run
    - Increase `_start = _target = 0.3` manually between runs (e.g. 0.3, 0.5, 0.7, 1.0)
1. Ramp-up profile, customize how steep
    - Set `_start = 0.1` (something small), `_target = 1.0`
    - Set `_inc = 1.5` (something larger than 1)
    - Set `_dec = 0.25` (something smaller than 1) as a fallback in case of divergence

/// note | Adjust your values
It's hard to say what are sensible values (1.5, 1.1, 1.0001) for any of the ramp-up parameters. It probably strongly differs from case to case and depends on the timestep. We recommend empirical research and trial & error.
///



## Modify boundary conditions in `b2.boundary.parameters`

This is the most complicated step, but at the same time, it might not be important to make the simulation stable (Honza's conjecture). It is, at any rate, important for the simulation to be physically correct. Most of the information here is based on the documentation of the boundary conditions and on the official example `ITER_2588_Donly_standalone_drifts` from the `solps-iter/examples` directory. Refer to that example for more details. See the [B2.5 switches](/solps-doc/extras/b2input) for a documentation on the boundary conditions. The main idea is:

- There are special versions of the sheath boundary conditions that are modified to properly account for drifts.
- It is advisable to use leakage conditions instead of decay lengths for the radial boundaries. But I'm not sure if that is important for drifts or just a good idea in general.

There are tables below that illustrate transition from "standard" BCs (i.e. those that I happened to be using) to the drift-enabled ones. If you happen to use different BCs, it might be best to check the official ITER example to get an accurate picture of what BCs need to be replaced in your case.

/// note | Adjust your values
The values for the BC parameters, such as the leakage factors, are taken directly from the ITER example. They might not be suitable for your case, so make sure to check them and adjust them accordingly.
///

**Boundaries `W` and `E` (divertor targets -> sheath):** Replace basic sheath conditions by a set of modified ones.

| variable | normal | drift-enabled | need to adjust `*par` |
| -------- | ------ | ------------- | --------------------- |
| `bcene`  | 3      | 15            | no                    |
| `bceni`  | 3      | 15            | no                    |
| `bcpot`  | 3      | 11            | no                    |
| `bccon`  | 3      | 14            | use 1.0               |
| `bcmom`  | 3      | 13            | no? (maybe use 0.0?)  |


**Boundaries `N` (radial from SOL and divertor region), `S` (radial from PFR):** Replace decay length conditions by leakage conditions. Leakage conditions are parametrized by a unit-less factor of thermal velocity, i.e. an even more arbitrary number. The important part is that it must be *negative* (and probably smaller than 1). Manual and (ITER) examples seem to be using:

- Neutrals: -0.01 or -0.001
- Ions/electrons: -0.01 for `bcene`/`bcini`, -0.001 for `bccon`

Additionally, in case of potential, make sure to use the zero gradient condition, `bcpot=2` with `potpar=0.0`.

| variable | normal | drift-enabled | need to adjust `*par` |
| -------- | ------ | ------------- | --------------------- |
| `bcene`  | 9      | 22            | yes (see above)       |
| `bceni`  | 9      | 22            | yes (see above)       |
| `bccon`  | 9      | 10            | yes (see above)       |
| `bcpot`  | 13     | 2             | use 0.0               |

**Boundary `S` (radial from core)**

This one might not be important, but the ITER example uses leakage condition for the core boundary with the continuity equation for neutral particles. The leakage factor used in the ITER example is a bit larger. I have no idea how to estimate it.

- Neutrals: -0.15

| variable | normal | drift-enabled | need to adjust `*par` |
| -------- | ------ | ------------- | --------------------- |
| `bccon`  | 8      | 10            | yes (see above)       |



## Use speed-up schemes in `b2.numerics.parameters`

> <span class="material-symbols-outlined">construction</span> This section is under construction.

## Run and troubleshoot

Under ideal circumstances, the simulation should run smoothly and converge to a solution. More often than not, it will crash. Refer to the troubleshooting checklist below even before you run your first simulation to save some trouble. Feel free to revisit it later if (when) you encounter crashes. There is a lot of moving parts and it is not always clear what could help. Try to prioritize the steps based on the given numbering, quickly go over all of them, and revisit each one later for a more thorough treatment. There are some opinionated hints at what seems to be sensible for the given step.

/// note | Code crash?
Crash in this context means rapid local increase/decrease in some of the plasma parameters and eventual numerical error, which causes the simulation to stop abruptly. In COMPASS simulations, it seems to be often connected to the currents in the divertor region. Refer to Common pitfalls: [Divergence](../supplementary/Common_pitfalls.md#divergence).
///

1. **Start from a converged case without drifts.** It always helps to start from something else than flat profiles.

1. **Start with a simpler simulation.** SOLPS runs with fluid neutrals both converge and crash faster, so running without Eirene at first can help you get acquainted with the process for a smaller computational cost. The same goes for impurities, puffing, and any other complicated stuff. Note that when you enable them later, you might need to redo the whole process from drift factor `0.0`. But with a bit of luck, the same settings (timestep, transport, mesh, ...) may work well, letting you to skip the hard part (not verified by experience, yet).

1. **Make the fluid mesh as even as possible.** Check the mesh for any large jumps in cell size. If needed, adjust the cell counts and their distribution to fix that and revisit later to do finer adjustments. Consider using finer mesh altogether, make sure to decrease the timestep accordingly in that case. I would not go far over something like 100x50 for a single-null scenario though.

1. **Increase the factors gradually.** Start with the manual approach, e.g. `0.3`, `0.5`, `0.7`, `1.0`. Let the simulation (almost) reach convergence between each step. Try decreasing the increment a bit if it does not work, but there's no sense in using an increment smaller than 0.1. There is also the ramp-up approach, but it seems to be useful only once you know what you are doing.

1. **Decrease the timestep.** Drift simulations typically require smaller $dt$, but it depends on the speed-up scheme settings (which locally decreases $dt$ by itself). It certainly does not make sense to go lower than `1e-7`, `1e-8`. At some point, it actually starts worsening the numerical instability again. And the simulation time becomes impractical, of course.

1. **Adjust the transport.** Experience says that drift simulations require modifications to their anomalous transport coefficients. It seems logical, since the drifts are actually one of the contributors to the "anomalous diffusion". But that would seem to dictate a strict decrease in the transport coefficients, which is not always the case. In any case, as you increase the drift factors, keep checking the resulting profiles and modify the transport coefficients to compensate. Otherwise the plasma parameters might get pushed far from the original state, possibly causing crashes due to "extreme" or "unrealistic" conditions. **This is what helped me to reach success in the end**, but you can spend an eternity by just looking for the proper non-crashing transport profiles, so it's best to leave any fine tuning as a last resort after you have visited the other options. Usually, it's a combination of all of them that helps.

Good luck!
