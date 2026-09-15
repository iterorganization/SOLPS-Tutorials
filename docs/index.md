# Introduction

Welcome to **SOLPS Tutorials**, home to step-by-step guides on using the [SOLPS-ITER](https://github.com/iterorganization/SOLPS-ITER)<span class="material-symbols-outlined">open_in_new</span> transport code! Accessible documentation for beginners is our goal. As the main author, Kateřina Hromasová, says:
> "I want tutorials that are so easy to understand that I'll be able to use them out of the box after I come back from a three-year maternity leave."

The SOLPS Tutorials [webpage](https://solps-tutorials.readthedocs.io/) is compiled using [MkDocs](https://www.mkdocs.org/)<span class="material-symbols-outlined">open_in_new</span> from its source code, hosted on the [ITER Organisation GitHub](https://github.com/iterorganization/SOLPS-Tutorials)<span class="material-symbols-outlined">open_in_new</span>. If you wish to contribute, read the [Contribute](Contribute.md) tutorial.

![SOLPS Tutorials logo](img/logo/logo.png)

*SOLPS wiki logo: a supra-luminal unicorn ([why?](supplementary/Questions_and_answers.md#unicorn))*


## Navigating the wiki

The SOLPS wiki has three basic parts:

1. **My first SOLPS simulation**. This includes [installing SOLPS](installing/solps-iter-codebase.md), [creating a simulation](my_first_simulation/Creating_a_new_SOLPS-ITER_simulation.md), [running the simulation](my_first_simulation/Running_SOLPS-ITER.md), [processing its output](my_first_simulation/Processing_SOLPS-ITER_output.md) and [adjusting its input](my_first_simulation/Adjusting_SOLPS-ITER_input.md).

2. **Feature blog**, or making your SOLPS simulation more complex. This includes [diffusion coefficients](feature_blog/Diffusion_coefficients.md), [gas puffing and pumping](feature_blog/Gas_puffing_and_pumping.md), [impurities](feature_blog/Impurities.md), [drifts](feature_blog/Drifts.md), [wide grids](feature_blog/Wide_grids.md), and deep dives on [magnetic equilibrium reconstructions](feature_blog/Magnetic_equilibrium_reconstructions.md), [energy fluxes](feature_blog/Energy_fluxes_deep_dive.md) and [interpretative simulations](feature_blog/Interpretative_simulations_of_COMPASS.md).

3. **Supplementary material**, which helps you use SOLPS aside from the physics. This includes [SOLPS-ITER user wisdom](supplementary/SOLPS-ITER_user_wisdom.md), a [library](supplementary/Library.md), [remote access](supplementary/Remote_access.md), [common pitfalls](supplementary/Common_pitfalls.md), [questions and answers](supplementary/Questions_and_answers.md) and [B2.5 switch documentation](/solps-doc/extras/b2input).

When contributing to the wiki, please respect this underlying structure.


## First steps

/// warning | "I don't understand anything and I am scared."
We were scared, too, and we still don't understand much. SOLPS-ITER is, unfortunately, that kind of code. Give it time. Write to <span class="material-symbols-outlined">mail</span>[Kateřina](mailto:hromasova@ipp.cas.cz) if it isn't getting better. This wiki was written so that the first, terrible, fumbling year doesn't have to be as terrible and fumbling. If all else fails, thesis goals and employers can be changed. Don't let SOLPS ruin your sleep.
///

To familiarise yourself with SOLPS-ITER and this wiki, I suggest the following:

- To learn what SOLPS-ITER is and what it's for, read the [brief introduction to SOLPS-ITER](#brief_introduction) and skim the references therein (SOLPS-related theses and articles).

- So you aren't completely confused by SOLPS-ITER jargon, skim [SOLPS-ITER user wisdom](supplementary/SOLPS-ITER_user_wisdom.md), particularly the [Dictionary](supplementary/SOLPS-ITER_user_wisdom.md#dictionary).

- If you need to run SOLPS on a remote server (like the [EUROfusion Gateway](installing/solps-iter-codebase.md#eurofusion_gateway)), read up on the [basic techniques](supplementary/Remote_access.md#basic-techniques).

- [Install SOLPS-ITER](installing/solps-iter-codebase.md). Or better yet, don't install it but use the portable [container installation](installing/installing-in-container.md).

- [Create your first SOLPS-ITER simulation](my_first_simulation/Creating_a_new_SOLPS-ITER_simulation.md). Then continue down the list of tutorials on the left in the section *My first SOLPS-ITER simulation*.

- When faced with problems, try the search bar on the top right, [Questions and answers](supplementary/Questions_and_answers.md) or [Common pitfalls](supplementary/Common_pitfalls.md).


<a name="brief_introduction"></a>
## Brief introduction to SOLPS-ITER

SOLPS-ITER is a suite of codes (B2.5, EIRENE, DivGeo, Carre...) which performs 2D (toroidally symmetric) simulations of the tokamak edge plasma. Its strength is self-consistently modelling interaction between the plasma, neutrals and the wall. It is indispensable for predicting if future fusion reactors will melt their divertors or not.

/// hint | SOLPS is the workhorse of tokamak edge modelling!

If you're writing about SOLPS, you are legally required to call it a workhorse of some kind.
[[1]](http://dx.doi.org/10.1016/j.jnucmat.2014.10.012) <!-- Wiesen 2015 -->
[[2]](https://iopscience.iop.org/article/10.1088/1361-6587/ab1bba) <!-- Kukushkin 2019 -->
[[3]](https://doi.org/10.1016/j.nme.2019.100696)  <!-- Pitts 2019 -->
[[4]](https://infoscience.epfl.ch/entities/publication/6b5c5149-8aad-4857-87aa-e4514506f44c) <!-- Mirko Wensing PhD thesis -->
[[5]](https://doi.org/10.1088/1741-4326/ada048)  <!-- Moscheni 2025 -->
[[6]](https://iopscience.iop.org/article/10.1088/1741-4326/ac72b4/meta) <!-- Van Uytven 2022-->
[[7]](https://iopscience.iop.org/article/10.1088/1741-4326/adb3bb/meta) <!-- Bryant 2025 -->
[[8]](https://onlinelibrary.wiley.com/doi/epdf/10.1002/ctpp.202100190) <!-- Dekeyser 2022 -->
[[9]](https://www.sciencedirect.com/science/article/pii/S2352179118302011) <!-- Dekeyser 2019 -->
[[10]](https://iopscience.iop.org/article/10.1088/1741-4326/ae53f9/meta) <!-- Shtyrkhunov 2026 -->
[[11]](https://pure.tue.nl/ws/portalfiles/portal/340297879/1341596_-_Kobussen_S.P._-_MSc_thesis_Thesis_-_NF.pdf) <!-- Kobussen MSc thesis -->
[[12]](https://pure.tue.nl/ws/portalfiles/portal/389678988/1474820_-_Reinhoudt_S.P._-_MSc_thesis_report_-_MAP.pdf) <!-- Reinhoudt MSc thesis -->
///

**Essential SOLPS-ITER reading**:

- [[Wiesen 2015]](http://dx.doi.org/10.1016/j.jnucmat.2014.10.012)<span class="material-symbols-outlined">open_in_new</span> - you HAVE to cite this under any SOLPS-ITER results
- [[Reiter 2005]](https://www.tandfonline.com/doi/abs/10.13182/FST47-172)<span class="material-symbols-outlined">open_in_new</span> - you [HAVE to acknowledge this](https://eirene.de/cgi-bin/eirene/login.cgi)<span class="material-symbols-outlined">open_in_new</span> under any EIRENE results
- [[Bonnin 2016]](https://doi.org/10.1585/pfr.11.1403102)<span class="material-symbols-outlined">open_in_new</span> - recommended to cite under any SOLPS-ITER results

**Recommended SOLPS-ITER reading**:

- [[Schneider 2006]](https://onlinelibrary.wiley.com/doi/abs/10.1002/ctpp.200610001)<span class="material-symbols-outlined">open_in_new</span> - old but gentle and extensive review article
- [[Braginskii 1965]](https://static.ias.edu/pitp/2016/sites/pitp/files/braginskii_1965-1.pdf)<span class="material-symbols-outlined">open_in_new</span> - Braginskii equations are the beating heart of SOLPS-ITER
- [PhD thesis](https://www.researchgate.net/publication/376610776_Experimental_and_numerical_investigation_of_helium_exhaust_at_the_ASDEX_Upgrade_tokamak_with_full-tungsten_wall)<span class="material-symbols-outlined">open_in_new</span> of Antonello Zito
- [PhD thesis](files/Hromasova_PhD_thesis.pdf)<span class="material-symbols-outlined">download</span> of Kateřina Hromasová
- [PhD thesis study](files/Katkas_PhD_thesis_study.pdf)<span class="material-symbols-outlined">download</span> of Kateřina Hromasová, chapter *SOLPS-ITER*


/// tip | Your ad could be here!
Have you written about SOLPS-ITER, and believe it would be legible to a complete beginner? We want it here! Write to <span class="material-symbols-outlined">mail</span>[Kateřina](mailto:hromasova@ipp.cas.cz) or [contribute to the SOLPS wiki](https://repo.tok.ipp.cas.cz/solps/solps-doc#solps-doc)<span class="material-symbols-outlined">open_in_new</span>. Fight the pesky anxiety that no one's ever going to read your work! (We have evidence that more than one person has ever read the SOLPS wiki. [You are reading this right now.])
///

## Contributors

![Hall of fame](img/Hall_of_fame.jpg)

/// hint | Kateřina Hromasová <a href="https://orcid.org/0000-0001-9165-4816"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png"></a>

*"If you don't write it down, you'll forget it."*

Katka was two years into her PhD on SOLPS-ITER when she got married, agreed on three kids, and realised she'd better get started. To avoid forgetting everything, she began writing down all she knew. She shared her notes with her colleagues, got help putting them up on the internet, realised people outside IPP Prague actually read them... and that's how the SOLPS wiki was born.
///


/// hint | Jan Hečko <a href="https://orcid.org/0000-0002-7696-3626"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png"></a>
*"The smaller and easier a task is, the lower it is on my to-do list."*

Honza has awesome superpowers, such as understanding the SOLPS source code. He is responsible for the [installation tutorials](installing/solps-iter-codebase.md), the [B2.5 switch documentation](/solps-doc/extras/b2input) and the wiki formatting. He also wrote most of the [Gas puffing and pumping](feature_blog/Gas_puffing_and_pumping.md) and [Drifts](feature_blog/Drifts.md) tutorials.
///

To make it into the hall of fame, write at least one comprehensive tutorial and contribute to many others.

Other major contributors to the SOLPS wiki:

- **Aleš Podolník** <a href="https://orcid.org/0000-0003-1237-8812"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png"></a>, who wrote the [Energy fluxes deep dive](feature_blog/Energy_fluxes_deep_dive.md)

- **Daniel Švorc** <a href="https://orcid.org/0000-0002-5154-1240"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png"></a>, who assisted with the [Wide grids](feature_blog/Wide_grids.md) tutorial

We would also like to thank Xavier Bonnin, Irina Borodkina, David Coster, Michael Komm, Lukáš Kripner, Diana Naydenkova, Jakub Seidl, Oleg Shyshkin, Matěj Tomeš, David Tskhakaya, and Sven Wiesen.