# Library

This document collects reading materials on SOLPS-ITER, mostly articles, and their brief descriptions. The collection is by no means complete. Submissions are welcome.


## Official SOLPS manuals

<a name="solps-manual"></a>

[**SOLPS-ITER manual**](SOLPS-ITER_user_wisdom.md#rtfm)

- Continually updated to reflect recent changes in SOLPS; find the version relevant to your installation in `$SOLPSTOP/docs/solps/solps.pdf`
- For convenience, the [3.0.9 manual](../files/SOLPS-ITER_manual_3.0.9.pdf)<span class="material-symbols-outlined">download</span> from December 2025 is shipped with the SOLPS wiki

**[DivGeo tutorial](../files/DivGeo_tutorial.pdf)**<span class="material-symbols-outlined">download</span>

- Illustrates basic DivGeo usage and mesh building
- Other DivGeo resources:
    - [SOLPS manual](SOLPS-ITER_user_wisdom.md#rtfm), appendix *DG manual*
    - DivGeo internal `Help` buttons
    - [User's Manual for DG](https://github.com/iterorganization/DivGeo/blob/d5a618f24efb0dd6bd1e0dd95be09f456a540e76/DOC/dg.pdf)<span class="material-symbols-outlined">open_in_new</span>
    - [Wide Grids DivGeo tutorial](https://user.iter.org/?uid=A78A4Y)<span class="material-symbols-outlined">open_in_new</span>

**[EIRENE manual](https://eirene.de/Documentation/eirene.pdf)**<span class="material-symbols-outlined">open_in_new</span>

- Useful for describing the contents of `input.dat` and outputting EIRENE results


## Annotated input files

[annotated_basic_b2mn.dat](../files/annotated_basic_b2mn.dat)<span class="material-symbols-outlined">download</span> 

[annotated_interesting_switches_in_b2mn.dat](../files/annotated_interesting_switches_in_b2mn.dat)<span class="material-symbols-outlined">download</span> 


## Main SOLPS-ITER publications

**S. Wiesen et al, [The new SOLPS-ITER package](https://www.sciencedirect.com/science/article/pii/S0022311514006965?via%3Dihub)<span class="material-symbols-outlined">open_in_new</span>, Journal of Nuclear Materials 463 (2015)**

- Official SOLPS-ITER paper, to be referenced in publications
- Compares the same runs made by SOLPS4.3 and SOLPS-ITER, gives some formulas for heat fluxes and defines convergence criteria. A longer, [report-like version](https://user.iter.org/?uid=LWXK4K)<span class="material-symbols-outlined">open_in_new</span> may be found among the ITER documents.

**X. Bonnin et al, [Presentation of the new SOLPS-ITER code package for tokamak plasma edge modelling](https://www.jstage.jst.go.jp/article/pfr/11/0/11_1403102/_article)<span class="material-symbols-outlined">open_in_new</span>, Plasma and Fusion Research 11 (2016)**

- Official SOLPS-ITER paper, to be referenced in publications
- SOLPS-ITER structure, Git version control, file description, workflow, plans for future improvements etc.

**D. Reiter et al, [The EIRENE and B2-EIRENE codes](https://doi.org/10.13182/FST47-172)<span class="material-symbols-outlined">open_in_new</span>, Fusion Science and Technology 2 (2005)**

 - Official EIRENE paper, to be acknowledged in publications according to the [EIRENE license](https://eirene.de/cgi-bin/eirene/write_temp.cgi?temp_dat=Licence/licence)<span class="material-symbols-outlined">open_in_new</span>



## Evolution of SOLPS

**<a name="braginskii"></a>S. I. Braginskii, [Transport Processes in Plasma](https://static.ias.edu/pitp/2016/sites/pitp/files/braginskii_1965-1.pdf)<span class="material-symbols-outlined">open_in_new</span>, Reviews of Plasma Physics 1 (1965)**

- When you hear of the Braginskii equations, this is what's referred to. Very detailed, humanely explained and surprisingly honest. A must-read for every transport code user.

**B. J. Braams, [A multi-fluid code for simulation of the edge plasma in tokamaks](https://github.com/iterorganization/SOLPS-ITER/blob/master/doc/BRAAMS_-_A_Multi-Fluid_Code_for_the_Simulation_of_the_Edge_Plasma_in_Tokamaks_-_NET_Report_1987.pdf)<span class="material-symbols-outlined">open_in_new</span>, NET report (1987)**

- A rather old but detailed resource on early SOLPS versions. Gives all the (then current) code equations and, delightfully, describes the variable in a nice comprehensive table. Describes discretization schemes and gives example boundary conditions. In appendix A, code subroutines and variables (such as `nx`, `sx`, `resco` and `fhe`) are described.

**V. A. Rozhansky et al, [Simulation of tokamak edge plasma including self-consistent electric fields](https://iopscience.iop.org/article/10.1088/0029-5515/41/4/305/meta)<span class="material-symbols-outlined">open_in_new</span>, Nuclear Fusion 41 (2001)**

- Description of B2.5 equations in SOLPS5.0. Were you wondering how drifts were implemented? Do you finally want to know what those "divergence-free terms" are? Read this.

**V. A. Rozhansky et al, [Potentials and currents in the edge tokamak plasma: simplified approach and comparison with two-dimensional modelling](https://iopscience.iop.org/article/10.1088/0029-5515/43/7/315)<span class="material-symbols-outlined">open_in_new</span>, Nuclear Fusion 43 (2003)**

- Compares calculation of edge plasma currents (calculating currents is about equivalent to calculating the plasma potential, and that can only be done believably by including the various drifts) on top of SOLPS5.0 using a 2D and a 1D model and finds good agreement. Breaks down the edge currents into individual components and provides formulas and commentaries on their magnitude and direction.

**R. Schneider et al, [Plasma Edge Physics with B2‐Eirene](https://onlinelibrary.wiley.com/doi/abs/10.1002/ctpp.200610001)<span class="material-symbols-outlined">open_in_new</span>, Contributions to Plasma Physics 46 (2006)**

- Textbook-like in length and explanation depth. Touches almost any aspect of transport code modelling you'd like. Recommended for beginners.

**V. A. Rozhansky et al, [New B2SOLPS5.2 transport code for H-mode regimes in tokamaks](https://iopscience.iop.org/article/10.1088/0029-5515/49/2/025007)<span class="material-symbols-outlined">open_in_new</span>, Nuclear Fusion 49 (2009)**

- A detailed description of B2.5 equations in SOLPS5.2 (and hopefully the current version of SOLPS-ITER). Answers the age-long question of "Whyd are there Pfirsch-Schlüter fluxes in the continuity equation instead of diamagnetic fluxes?". Refer here if you want to understand [B2.5 equations in SOLPS5.2](https://github.com/iterorganization/SOLPS-ITER/blob/master/doc/B2solps5.2_equations_2022.08.31.pdf)<span class="material-symbols-outlined">open_in_new</span>.

**S. Wiesen et al, [The new SOLPS-ITER package](https://www.sciencedirect.com/science/article/pii/S0022311514006965?via%3Dihub)<span class="material-symbols-outlined">open_in_new</span>, Journal of Nuclear Materials 463 (2015)**

- Compares the same runs made by SOLPS4.3 and SOLPS-ITER, gives some formulas for heat fluxes and defines convergence criteria. A longer, [report-like version](https://user.iter.org/?uid=LWXK4K)<span class="material-symbols-outlined">open_in_new</span> may be found among the ITER documents.

**X. Bonnin et al, [Presentation of the New SOLPS-ITER Code Package for Tokamak Plasma Edge Modelling](https://www.jstage.jst.go.jp/article/pfr/11/0/11_1403102/_article)<span class="material-symbols-outlined">open_in_new</span>, PFR 11 (2016)**

- SOLPS-ITER structure, Git version control, file description, workflow, plans for future improvements etc.



## Transport codes physics

**V. Kotov and D. Reiter, [Two-point analysis of the numerical modelling of detached divertor plasmas](https://iopscience.iop.org/article/10.1088/0741-3335/51/11/115002)<span class="material-symbols-outlined">open_in_new</span>, Plasma Physics and Controlled Fusion 51 (2009)**

- Derives a model very similar to Stangeby's two-point model based on SOLPS-ITER equations for momentum and energy transport, defines its own loss factors and calculates them for a density scan at AUG demonstrating the losses essential for achieving roll-over and detachment. Contains details on where to get the data from.

**P. C. Stangeby, [Basic physical processes and reduced models for plasma detachment](https://iopscience.iop.org/article/10.1088/1361-6587/aaacf6)<span class="material-symbols-outlined">open_in_new</span>, Plasma Physics and Controlled Fusion 60, 2018**

- All you want to know about detachment. Starts from the fact that the ITER divertor must survive the heat fluxes and erosion of its long DT operation, derives a lovely $T_e < 10$ eV criterion for the long-term divertor survival and discusses how to get there based on transport code simulations. Also introduces two-point model formatting (2PMF) to post-process and understand the simulation output.

**R. A. Pitts et al, [Physics basis for the first ITER tungsten divertor](https://www.sciencedirect.com/science/article/pii/S2352179119300237)<span class="material-symbols-outlined">open_in_new</span>, Nuclear Materials and Energy 20 (2019)**

- The holy grail of ITER divertor physics. Describes material limits of the tungsten divertor (steady-state, slow transients and fast transients) and how they're addressed in the ITER design. Discusses SOLPS4.3 and SOLPS-ITER simulations of ITER at length.

**J.-S. Park et al, [Assessment of ITER divertor performance during early operation phases](https://iopscience.iop.org/article/10.1088/1741-4326/abc1ce)<span class="material-symbols-outlined">open_in_new</span>, Nuclear Fusion 61, 2021**

- Density scan of pure-D, drift-less ITER plasmas of the PFPO-I stage. Finds that tungsten and beryllium-coated divertor have different molecular physics and that ITER target is well "insulated" from upstream, in that target conditions can change drastically and upstream remains the same.

**V. A. Rozhansky et al, [Potentials and currents in the edge tokamak plasma: simplified approach and comparison with two-dimensional modelling](https://iopscience.iop.org/article/10.1088/0029-5515/43/7/315)<span class="material-symbols-outlined">open_in_new</span>, Contributions to Plasma Physics 58 (2018)**

- Presents three simulations of AUG, with drifts and at three rates of nitrogen seeding, where the inner divertor is detached and the outer target gradually detaches. Shows that the parallel electric fields gradually decrease, the associated $E \times B$ drift decreases and the density maximum at the inner target moves from the SOL closer to the strike point. Also suggests the Pfirsch-Schlütter currents might create an instability in the cold divertor.

**V. Rozhansky et al, [Currents structure in the scrape-off layer of a tokamak](https://www.sciencedirect.com/science/article/pii/S2352179120301095?via%3Dihub)<span class="material-symbols-outlined">open_in_new</span>, Nuclear Materials and Energy 35 (2020)**

- Breaks down the SOL currents into three components: Pfirsch-Schlütter currents (AKA the currents closing the grad-B drift charge separation, but only above the X-point), thermoelectric currents (AKA the currents flowing from one divertor target to the other because of their temperature difference) and the plate closing currents (the currents closing the grad-B drift charge separation below the X-point and the currents compensating the neoclassical ion radial flow). Show these currents in Globus-M and ASDEX-U simulations and experiments.

**S. Carli et al, [Interchange-turbulence-based radial transport mode for SOLPS-ITER: A COMPASS case study](https://onlinelibrary.wiley.com/doi/epdf/10.1002/ctpp.201900155)<span class="material-symbols-outlined">open_in_new</span>, Contributions to Plasma Physics 60 (2020)**

- Extends SOLPS-ITER with a new quantity, the turbulent kinetic energy $k$, and uses it to self-consistently model $D_\perp$ based on the exchange turbulence. Compares classical ($D_\perp$ tuned manually) and self-consistent simulations and finds beautiful ballooning and satisfactory code-code-experiment agreement. The beginning of section 3 gives an exhaustive list of "technical parameters you need to say about your interpretative modelling simulation".






## Heat flux limiting

/// note | This is Kateřina's favourite topic
Kateřina has been writing an article on heat flux limiting since 2021. This is a fraction of her library. Feel free to add sections on your favourite SOLPS-related topics.
///

**W. Fundamenski, [Parallel heat flux limits in the tokamak scrape-off layer](https://iopscience.iop.org/article/10.1088/0741-3335/47/11/R01)<span class="material-symbols-outlined">open_in_new</span>, Plasma Physics and Controlled Fusion 47 (2005)**

-  Textbook-like review of the physics of heat flux limiters. The first paragraph in section *1.3 Historical overview* deserves a medal for its blatant honesty.
    
    > An applied plasma physicist attempting to model transport phenomena in a tokamak SOL is faced with a number of questions relating to parallel heat conduction in the long mean free path limit: How does $\chi_\sigma$ change with increasing $\lambda_{\sigma \sigma}$? When and by how much does it depart from $\chi_\sigma^{SH}$? How are $q_\sigma$ and $\nabla_\parallel T_\sigma$ related in this limit? Does the heat flux saturate at some value, e.g. the Maxwellian free streaming flux?

    And it goes *on*. It stops just short of: *Why did I choose to become a transport modeller? What is the meaning of life?*

**D. Tskhakaya, [On kinetic effects during parallel transport in the SOL](https://onlinelibrary.wiley.com/doi/abs/10.1002/ctpp.200810015)<span class="material-symbols-outlined">open_in_new</span>, Contributions to Plasma Physics 48 (2008)**

- Discussion of heat flux limiters in transport codes, from the perspective of kinetic (PIC) codes.

**J. Omotani and B. Dudson, [Non-local approach to kinetic effects on parallel transport in fluid models of the scrape-off layer](https://iopscience.iop.org/article/10.1088/0741-3335/55/5/055009)<span class="material-symbols-outlined">open_in_new</span>, Plasma Physics and Controlled Fusion 55 (2013)**

- Discussion of heat limiters in transport codes, from the perspective of a non-local model derived from hundreds of moments of the kinetic equation.

**M. Day et al, [The effect of heat flux limiting on divertor fluid models](https://onlinelibrary.wiley.com/doi/10.1002/ctpp.2150360259)<span class="material-symbols-outlined">open_in_new</span>, Contributions to Plasma Physics 36 (1996)**

- Criticizes heat flux limiters as a concept. My favourite bits are:

    > The limited heat flux is written as $q_e = \left( 1/q_s + 1/q_l\right)^{-1}$, which is an arbitrary interpolation between the free-streaming and Spitzer values.

    > The *ad-hoc* limiter is not derived from first principles and it introduces a poorly understood free parameter into the model.

 - Models the linear device PISCES-A with a homebrew 1D code, performs a sensitivity study of the electron heat flux limiter, finds a big impact on $n_e$ and $T_e$ and concludes heat flux limiting is unreliable, especially with predictive simulations. Lesson learned: do your sensitivity studies.

**R. H. Cohen and T. D. Rognlien, [Finite mean-free-path effects in tokamak Scrape-Off Layer](https://onlinelibrary.wiley.com/doi/epdf/10.1002/ctpp.2150340217)<span class="material-symbols-outlined">open_in_new</span>, Contributions to Plasma Physics 34 (1994)**

- Creates an analytical formula for electron parallel heat flux by patching up several known effects in the velocity space sorted by the mean free path, and compares its results for DIII-D-like plasmas to a Monte Carlo code. Gets "reasonable" agreement.


## Implementation and numerics details

**H. Bufferand et al, [Implementation of drift velocities and currents in SOLEDGE2D–EIRENE](https://www.sciencedirect.com/science/article/pii/S2352179116301946)<span class="material-symbols-outlined">open_in_new</span>, Nuclear Materials and Energy 12 (2017)**

- Describes SOLEDGE2D-EIRENE and not SOLPS-ITER, but presents a great derivation of fluid equations including drifts. It even includes a derivation why the divergence of the diamagnetic flux is equal to the divergence of the grad-B drift and explains the `(2dia)` terms found in the manual.

**E. Kaveeva, [Output_description.pdf](https://github.com/iterorganization/SOLPS-ITER/blob/master/doc/Output_description.pdf)<span class="material-symbols-outlined">open_in_new</span>**

- When you write the line
    
        'b2wdat_iout'    '4'
    
    into the `b2mn.dat` file, additional output will be produced. This document lists the variable names in this output and their prescriptions. Can be useful when you forget what `hx`, `bb` or `sna` are.

**Unknown authors, [B2solps5.2_equations_2022.08.31.pdf](https://github.com/iterorganization/SOLPS-ITER/blob/master/doc/B2solps5.2_equations_2022.08.31.pdf)<span class="material-symbols-outlined">open_in_new</span>** (and later versions)

- Equations used for solving the plasma state in B2.5. There are literally only equations, nearly no description of what the quantities are or mean. Decode it according to:
    - The manual, appendix C
    - [[Rozhansky 2009]](https://iopscience.iop.org/article/10.1088/0029-5515/49/2/025007)<span class="material-symbols-outlined">open_in_new</span>
    - [`$SOLPSTOP/modules/B2.5/src/documentation/b2cdcv.F`](https://github.com/iterorganization/B2.5/blob/cb7d15b2878074bb450666bebee4b1df02ef79e6/src/documentation/b2cdcv.F)<span class="material-symbols-outlined">open_in_new</span>



## Theses

Theses are good reading material because they are usually written by "beginners" transitioning to "capable users". As such, they are likely to contain both the basics and specialised results, as well as the path inbetween. For each thesis, highlight the most helpful part.

**Kateřina Hromasová, [Interpretative SOLPS-ITER transport simulations of the COMPASS tokamak edge plasma](../files/Hromasova_PhD_thesis.pdf) <span class="material-symbols-outlined">download</span> (PhD thesis, 2025)**

- Highlights:

    - Are you bothered that you can't match experimental profiles in interepretative SOLPS modelling without ad hoc radial shifts? Read chapter 4, *Magnetic equilibrium reconstruction inaccuracy*.
    - Interested in heat flux limiting? Read chapter 5, *Heat flux limiting*.
    - Would you like to know how well SOLPS-ITER reproduces the edge plasma of small tokamaks? Read chapter 6, *SOL transport regime*.

**Daniel Švorc, [Validation of tokamak equilibrium reconstructions using the SOLPS-ITER edge plasma transport code simulations](../files/Svorc_MSc_thesis.pdf)<span class="material-symbols-outlined">download</span> (MSc thesis, 2024)**

- Highlight: Did you know you can use SOLPS-ITER to decide which magnetic equilibrium reconstruction is better? You can even make better reconstructions with it!