# Introduction

/// warning | This is the beta version of SOLPS Tutorials
Until this warning box disappears, it is possible that the documentation won't work correctly. Everything should be fixed at latest for the SOLPS Code Camp on 19-23 October 2026.
///


Welcome to **SOLPS Tutorials**, home to step-by-step guides on using the [SOLPS-ITER](https://github.com/iterorganization/SOLPS-ITER)<span class="material-symbols-outlined">open_in_new</span> transport code! Accessible documentation for beginners is our goal. As the main author, Kateřina Hromasová, says:
> "I want tutorials that are so easy to understand that I'll be able to use them out of the box after I come back from a three-year maternity leave."

The SOLPS Tutorials [webpage](https://solps-tutorials.readthedocs.io/) is compiled using [MkDocs](https://www.mkdocs.org/)<span class="material-symbols-outlined">open_in_new</span> from its source code, hosted on the [ITER Organisation GitHub](https://github.com/iterorganization/SOLPS-Tutorials)<span class="material-symbols-outlined">open_in_new</span>. If you wish to contribute, read the [Contribute](Contribute.md) tutorial.

![SOLPS Tutorials logo](img/logo/logo.png)

*SOLPS Tutorials logo: a supra-luminal unicorn ([why?](supplementary/SOLPS-ITER_user_wisdom.md#unicorn))*


## Navigating the tutorials

SOLPS Tutorials are sorted into three basic categories parts:

1. **My first SOLPS simulation**. This includes [installing SOLPS](installing/solps-iter-codebase.md), [creating a simulation](my_first_simulation/Creating_a_new_SOLPS-ITER_simulation.md), [running the simulation](my_first_simulation/Running_SOLPS-ITER.md), [processing its output](my_first_simulation/Processing_SOLPS-ITER_output.md) and [adjusting its input](my_first_simulation/Adjusting_SOLPS-ITER_input.md).

2. **Feature blog**, or making your SOLPS simulation more complex. This includes [diffusion coefficients](feature_blog/Diffusion_coefficients.md), [gas puffing and pumping](feature_blog/Gas_puffing_and_pumping.md), [impurities](feature_blog/Impurities.md), [drifts](feature_blog/Drifts.md), [wide grids](feature_blog/Wide_grids.md), and deep dives on [magnetic equilibrium reconstructions](feature_blog/Magnetic_equilibrium_reconstructions.md), [energy fluxes](feature_blog/Energy_fluxes_deep_dive.md) and [interpretative simulations](feature_blog/Interpretative_simulations_of_COMPASS.md).

3. **Supplementary material**, which helps you use SOLPS aside from the physics. This includes [SOLPS-ITER user wisdom](supplementary/SOLPS-ITER_user_wisdom.md), a [library](supplementary/Library.md), [remote access](supplementary/Remote_access.md), [common pitfalls](supplementary/Common_pitfalls.md), [questions and answers](supplementary/Questions_and_answers.md) and [B2.5 switch documentation](/solps-doc/extras/b2input).

When contributing to the tutorials, please respect this underlying structure.


## First steps

To familiarise yourself with SOLPS-ITER and SOLPS Tutorials, you can do the following:

- To learn what SOLPS-ITER is and what it's for, read the [brief introduction to SOLPS-ITER](#brief_introduction) and skim the references therein (SOLPS-related theses and articles).

- To become familiar with SOLPS-ITER jargon, skim [SOLPS-ITER user wisdom](supplementary/SOLPS-ITER_user_wisdom.md), particularly the [Dictionary](supplementary/SOLPS-ITER_user_wisdom.md#dictionary).

- If you need to run SOLPS on a remote server (like the [EUROfusion Gateway](installing/solps-iter-codebase.md#eurofusion_gateway)), read up on the [basic techniques](supplementary/Remote_access.md#basic-techniques) of remote access.

- [Install SOLPS-ITER](installing/solps-iter-codebase.md). Or better yet, use the portable [container installation](installing/installing-in-container.md).

- [Create your first SOLPS-ITER simulation](my_first_simulation/Creating_a_new_SOLPS-ITER_simulation.md). Then continue down the list of tutorials on the left in the section *My first SOLPS-ITER simulation*.

- When faced with problems, try the search bar on the top right, [Questions and answers](supplementary/Questions_and_answers.md) or [Common pitfalls](supplementary/Common_pitfalls.md).


<a name="brief_introduction"></a>
## Brief introduction to SOLPS-ITER

SOLPS-ITER is a suite of codes (B2.5, EIRENE, DivGeo, Carre...) which performs 2D (toroidally symmetric) simulations of the tokamak edge plasma. Its strength is self-consistently modelling interaction between the plasma, neutrals and the wall. It is indispensable for predicting if future fusion reactors will melt their divertors or not.

**Essential SOLPS-ITER reading**:

- [[Wiesen 2015]](http://dx.doi.org/10.1016/j.jnucmat.2014.10.012)<span class="material-symbols-outlined">open_in_new</span> - cite this under any SOLPS-ITER results
- [[Reiter 2005]](https://www.tandfonline.com/doi/abs/10.13182/FST47-172)<span class="material-symbols-outlined">open_in_new</span> - [acknowledge this](https://eirene.de/cgi-bin/eirene/login.cgi)<span class="material-symbols-outlined">open_in_new</span> under any EIRENE results
- [[Bonnin 2016]](https://doi.org/10.1585/pfr.11.1403102)<span class="material-symbols-outlined">open_in_new</span> - recommended to cite under any SOLPS-ITER results

**Recommended SOLPS-ITER reading**:

- [[Schneider 2006]](https://onlinelibrary.wiley.com/doi/abs/10.1002/ctpp.200610001)<span class="material-symbols-outlined">open_in_new</span> - old but gentle and extensive review article
- [[Braginskii 1965]](https://static.ias.edu/pitp/2016/sites/pitp/files/braginskii_1965-1.pdf)<span class="material-symbols-outlined">open_in_new</span> - Braginskii equations are the beating heart of SOLPS-ITER
- [PhD thesis](https://www.researchgate.net/publication/376610776_Experimental_and_numerical_investigation_of_helium_exhaust_at_the_ASDEX_Upgrade_tokamak_with_full-tungsten_wall)<span class="material-symbols-outlined">open_in_new</span> of Antonello Zito
- [PhD thesis](files/Hromasova_PhD_thesis.pdf)<span class="material-symbols-outlined">download</span> of Kateřina Hromasová


/// tip | Your documentation could be here!
Although SOLPS Tutorials does not aim to substitute existing SOLPS documentation, they do aspire to become its central hub. If you have written any sort of SOLPS-related documentation, consider [contributing to SOLPS Tutorials](Contribute.md) or adding your work to the [Useful links](supplementary/SOLPS-ITER_user_wisdom.md#useful-links) section.
///

## Contributors

/// hint | Kateřina Hromasová <a href="https://orcid.org/0000-0001-9165-4816"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png"></a>

*"If you don't write it down, you'll forget it."*

Katka was two years into her PhD on SOLPS-ITER when she got married, agreed on three kids, and realised she'd better get started. To avoid forgetting everything, she began writing down all she knew. She shared her notes with her colleagues, got help putting them up on the internet, realised people outside IPP Prague actually read them, rewrote them to pretend she was a professional... and that's how SOLPS Tutorials were born.
///


/// hint | Jan Hečko <a href="https://orcid.org/0000-0002-7696-3626"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png"></a>
*"The smaller and easier a task is, the lower it is on my to-do list."*

Honza has awesome superpowers, such as being one with the source code. He is responsible for the [installation tutorials](installing/solps-iter-codebase.md), the [B2.5 switch documentation](/solps-doc/extras/b2input) and the website formatting. He also wrote most of the [Gas puffing and pumping](feature_blog/Gas_puffing_and_pumping.md) and [Drifts](feature_blog/Drifts.md) tutorials, and he got the [Wide grids](feature_blog/Wide_grids.md) tutorial started.
///

Other major contributors to the Tutorials are:

- **Aleš Podolník** <a href="https://orcid.org/0000-0003-1237-8812"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png"></a> - wrote the [Energy fluxes deep dive](feature_blog/Energy_fluxes_deep_dive.md)

We would also like to thank, in alphabetic order, Xavier Bonnin, Irina Borodkina, David Coster, Michael Komm, Lukáš Kripner, Diana Naydenkova, Jakub Seidl, Oleg Shyshkin, Daniel Švorc, Matěj Tomeš, David Tskhakaya, and Sven Wiesen.