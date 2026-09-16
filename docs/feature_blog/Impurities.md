# Impurities

/// warning | This feature blog entry introduces advanced concepts
The reader is assumed to know how to [create a simple SOLPS-ITER simulation](../my_first_simulation/Creating_a_new_SOLPS-ITER_simulation.md) and to possess some [user wisdom](../supplementary/SOLPS-ITER_user_wisdom.md).
///

## Motivation

Real plasma in a tokamak includes a small (or not so small) concentration of impurities. Intrinsic impurities can be eroded from the plasma-facing components (C for graphite PFCs, W for tungsten PFCs, B from boronisation...) or desorb from poorly conditioned vacuum vessel walls (O from water vapour...). Seeded impurities are intentionally injected into the plasma, usually in the divertor volume to induce detachment (N in smaller machines, Ne and Ar in reactors...). Liquid metal divertors can release large quantities of liquid metals (Li, Sn...). Burning fusion plasmas are not only made-up of 50:50 D-T mix but also produce fusion reaction ash (He). Depending on the physics you wish to study and the required level of predictive power, one or many of these impurities need to be included in your SOLPS-ITER simulation.

This feature blog entry covers:

- [General advice on impurities](#general-advice-on-impurities)
- [Impurity seeding](#impurity-seeding)
- [Carbon sputtering](#carbon-sputtering)


## General advice on impurities

**Do you really need impurities?** Each ionisation state of the added impurity becomes an ion species to keep track of, increasing output file size, simulation complexity and runtime. Think carefully if you need the impurity.

/// hint | Example impurity: tungsten
Tungsten is a key impurity in core physics. Even a small concentration can kill a fusion reactor by decreasing the energy confinement time. The source of tungsten in tokamaks is sputtering from the walls, so one would think modelling tungsten with SOLPS-ITER is key. Not so. Tungsten concentrations in the SOL are typically so small that they don't affect the plasma solution. Tungsten has 75 charge states including neutrals, so it's quite impossible to model in SOLPS without charge bundling. And finally, tungsten concentrations/densities are so small in tokamaks that it's in the kinetic regime rather than highly collisional, so Braginskii equations are inadequate at describing its transport. You are much better off describing tungsten sputtering and transport with a dedicated kinetic code such as ERO2.0. SOLPS-ITER can provide ERO with the background plasma, which does not contain tungsten, and ERO can provide SOLPS with the power radiated by tungsten in the core, which translates into decreased power crossing the separatrix $P_{sep}$.
///

**Baby steps.** SOLPS-ITER works better (and faster) if the simulation complexity is increased gradually. Even when you're aiming to make a simulation with impurities from the start, begin by building a pure-D simulation. Let it converge, implement self-consistent particle balance using [gas puffing and pumping](Gas_puffing_and_pumping.md), let it converge, and only then add impurities. You'll save runtime and headache with divergence.

/// hint | Transferring `b2fstati`
You can use the initial plasma solution `b2fstati` without an impurity (but otherwise matching in grid dimensions etc.) and use it as basis for a run set up with impurities (starting from DivGeo). The impurities will be added automatically. Their initial plasma parameters will be the "flat profiles" solution specified by `b2ai.dat`.
///


/// hint | More resources
- [SOLPS Conversion Tutorial](https://iterorganization.sharepoint.com/:w:/r/sites/SOLPS-ITER/Shared%20Documents/General/Tutorials/2017_Bonnin_Conversion_tutorial.docx?d=w665bc959a164494eacab09fe6b4fb948&csf=1&web=1&e=CU7cNc)<span class="material-symbols-outlined">open_in_new</span>, section *Adding new species to a SOLPS-ITER run*
///


## Impurity seeding

Seeding impurities using gas puff is described in Gas puffing and pumping: [Impurity seeding](Gas_puffing_and_pumping.md#impurity-seeding).



## Carbon sputtering

/// tip | This section applies to most sputtered impurities
Adapt this tutorial for any sputtered impurity (boron, tungsten...) by adjusting the wall material composition in DivGeo.
///

Carbon is a typical intrinsic impurity of tokamaks with graphite divertors and targets, such as COMPASS. Graphite is a low-Z material, so it gets fully ionised in the core and doesn't cause terrible radiation losses. Graphite conducts heat well and evaporates before it melts. It's cheap, too. Unfortunately, carbon reacts with hydrogen too readily and was abandoned for fusion reactors in fear of uncontrollable tritium retention.

When setting up carbon as an intrinsic impurity in SOLPS-ITER simulations, keep in mind that it can be sputtered both physically and chemically.

During **physical sputtering**, ions or energetic neutrals hit the solid surface and dash out one or more atoms or ions from the surface. The yield of physical sputtering (number of atoms/ions sputtered per incident particle) depends on the energy of the incident particle, and is described by the Roth-Bogdansky formula in SOLPS-ITER [[Roth & Carcia-Rosales 1996](https://iopscience.iop.org/article/10.1088/0029-5515/36/12/I05)<span class="material-symbols-outlined">open_in_new</span>] [[EIRENE manual](https://eirene.de/Documentation/eirene.pdf)<span class="material-symbols-outlined">open_in_new</span>].

During **chemical sputtering**, complex chemical bonds are formed between the target atoms and the hydrogen/deuterium/tritium atoms recycling at the target. For example, carbon and hydrogen may form methane, which then evaporates from the target and is quickly broken down and ionised in the plasma. It is difficult to describe this process analytically, so SOLPS-ITER uses a constant chemical sputtering yield $\gamma_{chem} \sim 0.01$ (number of atoms sputtered per incident ion/neutral).


### Set up carbon sputtering

First, build and run the initial deuterium simulation. Aim only for a rough agreement with the desired plasma parameters, since the solution will cool down after carbon is added. Don't even think of tuning the diffusion coefficient profiles in H-mode. The desired output of this step is a `b2fstate` file containing a converged carbon-less solution.

Create a new simulation folder from scratch and its `baserun` and `run` subfolders. Copy the DivGeo file from your deuterium simulation into the carbon simulation. Select your `DEVICE` name and open the `.dg` file with DivGeo.

Select all the elements (`Ctrl+A`). Go to `Variables>General surface data` and browse all of the variables. In particular, you'll be interested in the physical and chemical sputtering settings. To turn on both physical and chemical sputtering of carbon, set:

Variable | Value | Meaning
--- | --- | ---
Wall Material | C | The first wall is made of carbon.
Wall Temperature | -0.026 | Particles desorbed from the wall will have a Maxwellian velocity distribution with the mean energy 0.026 eV = 28 °C. (Discuss the exact value with your experimentalists.)
Phys. sput. model | 2 | Use the standard physical sputtering model.
Phys. sput. factor | 1 | Don't artificially enhance or reduce physical sputtering yield.
Sputtered atom | -1 | Sputter atomic carbon from the wall and trace the sputtered atoms so they may enter the plasma.
Chem. sputter. | 1 | Use the standard chemical sputtering model.
Chem. sput. factor | 0.01 | Set the chemical sputtering yield to 0.01.

/// warning | Don't forget to click `Set` after changing every parameter!
If you change the parameter values first and then hit `Set` on one of them, all the other parameter values will reset. It's a good check to close the dialogue window, reopen it and check all the parameter values are as you like them.
///

Do the same for the divertor targets. Unselect all (`Ctrl+U`) and go to `Variables>Target specification>#1` and then `#2` and set the variables to the same values as above. Estimate the target temperature; for example, `-0.05` = 307 °C. There are switches in `b2mn.dat` which can calculate the target temperature self-consistently from its heat load, thickness, material and temperature on the cooled side, but the default setting is that the target/wall temperature is supplied by the user.

Go to `Variables>Add>Plasma species` and set `Species` to `C`. Leave the boundary conditions as they are, you'll change them later. `Commands>Check variables`, `Commands>Rebuild Carre objects`, `File>Save`, `File>Output`. Set up DivGeo links and [run Carre and Triang](../my_first_simulation/Creating_a_new_SOLPS-ITER_simulation.md#create-b25-grid-with-carre).

Import the grids into your DivGeo file and check that they look ok. They don't need to exactly match the grids of the deuterium simulation. In theory, if you used the same input (for instance setting `pasmin` in Carre), the grids should be identical. In practice, how am I supposed to remember how I built a grid two years ago?

[Procure input files](../my_first_simulation/Creating_a_new_SOLPS-ITER_simulation.md#procure-input-files) and set the same boundary conditions as in your deuterium simulation. To start with, use the same parameters for carbon as for deuterium (e.g. diffusion coefficients). The only difference is that we want the wall to be the only net source (and sink) of carbon. So, in `b2.boundary.parameters`, set the impurity `BCCON` at the core boundary to `8` and `CONPAR = 0.0` for all carbon charge states. This sets the particle flux across the core boundary to zero. Later, you can choose more realistic boundary conditions where there is an influx of C<sup>6+</sup> from the core and outflux of C<sup>4+</sup> and C<sup>5+</sup> into the core.

/// warning | Use the `stencil` boundary conditions files
Copy over the `stencil` files generated in the `baserun` rather than boundary condition files from your old, carbon-less simulation. The number of ion species is different, and though checking the text files line by line is a drag, typing in all the new ion species is even a bigger drag.

If you're using the `2*0.3` notation in `b2.transport.parameters` (see Q&A: [I copied `b2.transport.parameters` from the manual...](../supplementary/Questions_and_answers.md#transport-parameters-12s)), change the number before `*` accordingly. We're adding carbon here, which is 7 extra species (C<sup>0</sup>, C<sup>1+</sup>, ..., C<sup>6+</sup>), so `2` goes to `9`.
///

Make a dry run of SOLPS-ITER to check that everything is working. If no errors (especially regarding boundary condition files) appear, you're good to go and regulate the sputtering source.


### Control carbon sputtering

> <span class="material-symbols-outlined">construction</span> This tutorial was written in August 2021 and contains a workaround for a bug then present in the SOLPS-ITER master version. Hopefully sputtering presets have been fixed since then.

Sputtering is handled within B2.5 in standalone runs and by EIRENE in coupled runs. These processes are controlled by two independent sets of switches.

**Coupled B2.5+EIRENE simulation**: Sputtering switches are located in `input.dat` (or `input.json`). Find the section *6a. General data for reflection model*, which may look something like this:

    *** 6a. General data for reflection model
    T
    cpath modules/Eirene/Database/Surfacedata/TRIM/
    D_on_C
    C_on_C
    1.00000E+00 1.00000E+00
    1.00000E+00
    1.00000E+00
    1.00000E+00 1.66667E-01 1.66667E-01 1.66667E-01 1.66667E-01 1.66667E-01
    1.66667E-01 0.00000E+00 0.00000E+00 0.00000E+00 0.00000E+00
    1.00000E+00 5.00000E+01 1.00000E-01 0.00000E+00 0.00000E+00 0.00000E+00
    SURFMOD_1_CARBON_SPT_580K
     1    12    -1     0     1
    1.20600E+03-5.00000E-02 0.00000E+00 0.00000E+00 0.00000E+00-1.00000E+00
    1.00000E+00 1.00000E+00 1.00000E+00 1.00000E+00 5.00000E-01 1.00000E+00
    1.00000E+00 1.00000E+00 0.00000E+00 0.00000E+00 1.00000E+00
    SURFMOD_2_CARBON_SPT_1160K
     1     2     0     0     1
    1.20600E+03-1.00000E-01 0.00000E+00 0.00000E+00 0.00000E+00-1.00000E+00
    1.00000E+00 1.00000E+00 1.00000E+00 1.00000E+00 5.00000E-01 1.00000E+00
    1.00000E+00 1.00000E+00 0.00000E+00 0.00000E+00 1.00000E+00
    SURFMOD_3_CARBON_SPT_302K
     1    12    -1     0     1
    1.20600E+03-2.60000E-02 0.00000E+00 0.00000E+00 0.00000E+00-1.00000E+00
    1.00000E+00 1.00000E+00 1.00000E+00 1.00000E+00 5.00000E-01 1.00000E+00
    1.00000E+00 1.00000E+00 0.00000E+00 0.00000E+00 1.00000E+00

Your interest lies with the three paragraphs beginning with `SURFMOD`. These define three groups of structure elements with common sputtering properties. In this case, the first one are the divertor targets (temperature approx 300 °C), the second one is a mystery and the third one is the first wall (temperature approx 30 °C). If you've done everything correct, there should only be two paragraphs, `580K` and `302K`. If one of them is missing, check the DivGeo surface data and build the grids again. What the numbers inside these paragraphs mean is (mostly) described in the [EIRENE manual](http://eirene.de/Documentation/eirene.pdf)<span class="material-symbols-outlined">open_in_new</span>, *section 2.6 Input Data for Surface Interaction Models*. Every number in a `SURFMOD` paragraph denotes one variable, whose names are, in turn:

    SURFMOD_modname
    ILREF ILSPT ISRS ISRC
    ZNML EWALL EWBIN TRANSP(1 ,N) TRANSP(2 ,N) FSHEAT
    RECYCF RECYCT RECPRM EXPPL EXPEL EXPIL
    RECYCS RECYCC SPTPRM ESPUTS ESPUTC

At first glance (in the August 2021 version of the EIRENE manual and SOLPS-ITER), you will notice that there are actually 5 numbers in the first paragraph line, not 4. In such cases, the source code is the ultimate judge. As can be found in the source code of EIRENE, file `$SOLPSTOP/modules/Eirene/src/startup-routines/input.f`, the fifth variable is called `LCHSPNWL` and it concerns switching between SOLPS4.3 and SOLPS-ITER version 3.0.1 input format. Otherwise, the variable values should match some realistic physical picture of the tokamak first wall or divertor target.

Sputtering is mainly controlled by the variables `ILSPT`, `ISRS`, `ISRC`, `RECYCS` and `RECYCC`.

- `ILSPT` (here `12`) is composed of two numbers, `M = 1` and `N = 2`. It controls the sputtering model for chemical sputtering (`M = 1` stands for "constant chemical sputtering rate") and physical sputtering (`N = 2` stands for "modified Roth–Bogdansky formula for sputter yield").
- `ISRS` (here `-1`) controls physical sputtering. Its value here means, put simply, that physical sputtering is on and produces atoms of the same type as the wall/target material - carbon.
- `ISRC` (here `0`) controls chemical sputtering. Its value here means that chemical sputtering is off. This happens despite our previous effort to turn chemical sputtering on in DivGeo, and was the source of [much anguish](../supplementary/Common_pitfalls.md#divergence-hunt-1-carbon-sputtering) to me once. Set this number to `-1` in the first and third paragraph to turn chemical sputtering on and set it to produce atoms of the same type as the wall/target material - carbon.
**Important: substitute ` 0` for `-1`, including the space at the beginning.** The reason is that `input.dat` is very peculiar about its blank spaces. "Shifting" the rest of the line by one character will result in the `run.log` error `Fortran runtime error: Bad value during integer read`, as Fortran reads `-` as the next input value instead of `-1`.
- `RECYCS` (here `1.00000E+00`) can mean different things depending on which physical sputtering model was chosen in `ILSPT`. In our case, `RECYCS` is (probably) the physical sputtering yield, an additional multiplier to the atom flux calculated by the Roth–Bogdansky formula.
- `RECYCC` (here `1.00000E+00`) can mean different things depending on which chemical sputtering model was chosen in `ILSPT`. In our case, `RECYCC` is (probably) the chemical sputtering yield.

For starters, use `RECYCS = 1.0` and `RECYCC = 0.01` (chemical sputtering yield $\gamma_{chem}=0.01$). Once you have some carbon concentration diagnostics (such as spectroscopic measurements of its line radiation), adjust $\gamma_{chem}$ to yield the desired carbon content.


**Standalone B2.5 simulation**: I've never used these switches myself, but the appropriate set in `b2mn.dat` is probably:

```{.fortran title="b2mn.dat"}
! Common sputtering switches
'b2stbr_sput_dst' '2' ! sputtered ion species index is 2 = neutral carbon

! Physical sputtering switches
'b2stbr_sput_phys' '1.00' ! turn on physical sputtering and set the yield to 1.00

! Chemical sputtering switches
'b2stbr_sput_chem_model' '0' ! use the empirical formula for yield calculation
'b2stbr_sput_frc' '0.01' ! probably chemical sputtering yield; overridden by chemical_sputter_yield in b2.neutrals.parameters
```

Additionally, in `b2.neutrals.parameters` you may specify chemical sputtering yield individually for each structure element with the `chemical_sputter_yield` array, which will probably come predefined in `b2.neutrals.parameters.stencil`. The array index corresponds to the element numbers in DivGeo. Look for further information in `$SOLPSTOP/modules/B2.5/src/documentation/b2input.xml`. I have unfortunately found no other sputtering documentation.
