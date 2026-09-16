# SOLPS-ITER codebase

In this tutorial, you will learn:

- [How to obtain the SOLPS source code](#get-access-to-solps-iter)
- [Where you should install SOLPS](#where-and-how-to-install-solps-iter)
- [How to initiate the SOLPS work environment](#how-to-initiate-the-solps-iter-work-environment)
- [How to update SOLPS](#how-to-update-solps-iter)
- [The very basics of Git](#introduction-to-git)

/// tip | Official sources
This tutorial overlaps with section 1.1 *Obtaining and updating the code* of the [SOLPS manual](../supplementary/SOLPS-ITER_user_wisdom.md#rtfm) and the SOLPS-ITER repository [README](https://github.com/iterorganization/SOLPS-ITER/blob/master/README)<span class="material-symbols-outlined">open_in_new</span>.
///

## Get access to SOLPS-ITER

SOLPS-ITER is an open-source code developed by the ITER Organisation (IO) whose Responsible Officer (RO) is [Xavier Bonnin](https://www.researchgate.net/profile/X-Bonnin)<span class="material-symbols-outlined">open_in_new</span>. From spring 2026, its [source code](https://github.com/iterorganization/SOLPS-ITER)<span class="material-symbols-outlined">open_in_new</span> is publicly available at GitHub. To get access to SOLPS-ITER:

1. Write to Xavier Bonnin (<span class="material-symbols-outlined">mail</span> [xavier.bonnin@iter.org](mailto:xavier.bonnin@iter.org)) that you would like to use SOLPS-ITER. You will be added to the SOLPS mailing list (<span class="material-symbols-outlined">mail</span> [solps-iter@iter.org](mailto:solps-iter@iter.org)) and the SOLPS-ITER [Slack group](http://solps.slack.com/)<span class="material-symbols-outlined">open_in_new</span>.

2. Check if your institution is [affiliated to EIRENE](https://eirene.de/cgi-bin/eirene/write_temp.cgi?temp_dat=Licence/licence)<span class="material-symbols-outlined">open_in_new</span> and register on the EIRENE website to be licensed to use EIRENE, the Monte Carlo neutrals solver of SOLPS-ITER.

3. [Create a GitHub account](https://github.com/signup)<span class="material-symbols-outlined">open_in_new</span> if you don't already have one. Use your work credentials and affiliation if possible.

4. Generate a pair of [SSH keys](https://www.ssh.com/ssh/keygen/)<span class="material-symbols-outlined">open_in_new</span> (or use a pair already present in `~/.ssh`).

        cd ~/.ssh
        ssh-keygen -t rsa -C "your_email@institute.eu"

    Upload the public key to your GitHub [SSH keys list](https://github.com/settings/keys)<span class="material-symbols-outlined">open_in_new</span>. (That is, copy-paste the inside of the `id_rsa.pub` file there.)

5. Download the source code of SOLPS-ITER using Git.

        cd /path/to/solps
        git clone git@github.com:iterorganization/SOLPS-ITER.git

    Finally, "star" the [SOLPS-ITER GitHub package](https://github.com/iterorganization/SOLPS-ITER)<span class="material-symbols-outlined">open_in_new</span> by clicking the `Star` button on the top right. This will show the developers one more person cares, and you'll find the source code easier in the future.

Congratulations, you have the *source code* - mostly text files written in Fortran. To actually run SOLPS-ITER, you must first *compile* the source code, including all of SOLPS dependencies.

/// tip | Tip
Before you go on, skim the [Useful links](../supplementary/SOLPS-ITER_user_wisdom.md#useful-links) and browse the [SOLPS-ITER Confluence page](https://confluence.iter.org/spaces/IMP/pages/178135134/SOLPS-ITER)<span class="material-symbols-outlined">open_in_new</span>, just so you know they exist.
///


## Where and how to install SOLPS-ITER

The SOLPS-ITER code has a convoluted list of dependencies, which makes it complicated to install. We recommend one of two options:

1. Install SOLPS-ITER at a [properly configured site](#properly-configured-site) (EUROfusion Gateway, ITER computing clusters etc; see the list in section 1.3 *Initial set-up* of the [SOLPS manual](../supplementary/SOLPS-ITER_user_wisdom.md#rtfm)).
2. Use a [container installation](installing-in-container.md), which can be run anywhere.


### Properly configured site

A *properly configured site* is an HPC (High-Performance Computing) server where:

1. All required dependencies are installed
2. The site-specific configuration files have been committed to the main SOLPS-ITER repository


/// hint | Example of a properly configured site: EUROfusion Gateway <a name="eurofusion_gateway"></a>
- [EUROfusion Gateway](https://docs.hpc.cineca.it/specific_users/gateway.html)<span class="material-symbols-outlined">open_in_new</span> = HPC-CINECA cluster in Italy
- Available to all EUROfusion beneficiaries, no need to register any specific project (in contrast to e.g. [IT4I](https://www.it4i.cz/en)<span class="material-symbols-outlined">open_in_new</span>)
- Known under a variety of legacy names: Marconi, Marconi Gateway, Gateway, ITM etc. (`ITM` or `MARCONI` in the manual)
///

**How to install SOLPS-ITER at a properly configure site**:

1. Log into the site's command line.

        ssh -X username@my.server.eu

2. Download ("clone") the SOLPS repository to your directory of choice.
        
        cd /path/to/solps
        git clone ssh://git@git.iter.org/bnd/solps-iter.git

    /// tip | SSH authentication
    If you get the error
    ```
    Permission denied (publickey).
    fatal: Could not read from remote repository.

    Please make sure you have the correct access rights and the repository exists.
    ```
    ...you have not correctly set up [SSH key authentication](#get-access-to-solps-iter).
    ///

    /// note | The SOLPS-ITER installation directory matters
    At many servers, installing SOLPS-ITER into the `home` folder is not advisable. Computing clusters typically have a "slow memory" (`home`) which stores useful data and is backed up regularly, and a "fast memory" (`pfs`, `scratch`...) which serves for quick access to intermediate results during computation. If you install SOLPS-ITER into the "slow memory", your simulation will be slow and your IT department will be angry. Ask IT support or your colleagues for advice where best to install SOLPS-ITER.
    ///

3. Enter the newly cloned `solps-iter` repository and select your code version/branch. Available branches are listed on the [SOLPS-ITER GitHub wiki](https://github.com/iterorganization/SOLPS-ITER/wiki)<span class="material-symbols-outlined">open_in_new</span>. In case of doubt, use the `master` branch.
 
        cd solps-iter
        git checkout master  # master, develop, release/3.1.1 etc.

4. Initialise and update everything.

        git pull
        git submodule update --init


    /// warning | Do not check out individual submodules
    The [SOLPS manual](../supplementary/SOLPS-ITER_user_wisdom.md#rtfm) instructs to check out individual submodules:
    ```bash
    git checkout master
    cd modules/B2.5
    git checkout master
    cd ../Eirene
    git checkout master
    cd ../DivGeo
    git checkout master
    cd ../Carre
    git checkout master
    cd ../adas
    git checkout master
    ```
    This is not necessary, since  `git submodule update` has already done this. It has checked out each submodule at a specific commit as determined by a `.gitmodules` file, combining their versions "as the developer intended". Checking out the submodules individually only makes sense as a troubleshooting option, when you want to blindly incorporate bleeding edge changes (bug fixes) in submodules but the developers temporarily forgot to update `.gitmodules` in the main repository.
    ///

5. [Initiate the SOLPS work environment](#how-to-initiate-the-solps-iter-work-environment).

        tcsh
        source setup.csh

    /// warning | Optional: first setup
    The [SOLPS manual](../supplementary/SOLPS-ITER_user_wisdom.md#rtfm) instructs to run the command:
    ```
    first_setup
    ```
    We believe that this is intended only when setting up configuration of SOLPS-ITER on a completely new site. It generates default `setup/config` files if any are missing. But there is no harm in running it anyway.
    ///

6. Clean for good luck (especially if you've tried to compile SOLPS before) and compile SOLPS (recommended targets: `solps`, `solps_mpi`).

        gmake clean_solps
        gmake clean_solps_mpi
        gmake solps
        gmake solps_mpi

If everything ends without errors, congratulations, you have installed SOLPS-ITER!



### Installation guides

SOLPS Tutorials offer three installation guides in addition to [installing on a properly configured site](#properly-configured-site):

**[Installing SOLPS in a container](installing-in-container.md) - recommended**

- Quick and clean installation of SOLPS-ITER, portable to any site
- Pre-built containers with zero setup are available
- Requires [Apptainer](https://apptainer.org/)<span class="material-symbols-outlined">open_in_new</span> or [Docker](https://www.docker.com/resources/what-container/)<span class="material-symbols-outlined">open_in_new</span> software installed on the target machine. Apptainer is a fairly standard HPC software. Ask the respective IT support to install it if it is missing. Docker is a more common software, but it is not always available on HPC servers mainly due to security considerations.

**(Legacy) [Installing SOLPS at Soroban](legacy-installing-at-compass-soroban.md)**

- [Soroban](https://wiki.tok.ipp.cas.cz/index.php/Soroban_cluster)<span class="material-symbols-outlined">open_in_new</span> = IPP Prague cluster in Czechia, properly configured site since v3.0.9, supports **containers**
- Available to IPP Prague employees and students
- Known as `IPPCR` in the manual

**(Legacy) [Installing SOLPS at IT4I](legacy-installing-at-it4i.md)**

- [IT4Innovations](https://www.it4i.cz/en)<span class="material-symbols-outlined">open_in_new</span> (IT4I) = supercomputing centre in Czechia, supports **containers**
- Requires application for a 9-month project
- Servers are often upgraded, which may break things, but a container installation is resistant to this

**Compiling SOLPS elsewhere**: Discouraged for beginners. You can spend a lot of time installing SOLPS-ITER when you wanted to perform simulations of the edge plasma. If you absolutely must do it, get in touch with someone experienced (<span class="material-symbols-outlined">mail</span> [Jan Hečko](mailto:hecko@ipp.cas.cz), <span class="material-symbols-outlined">mail</span> [Xavier Bonnin](mailto:xavier.bonnin@iter.org), your local SOLPS guru). Look for the `SETUP/easybuild-local.sh` script in the SOLPS-ITER repository, which is currently the recommended tool for the job. It should install all the dependencies for you in the form of environmental modules. As for its documentation, there are comments in the script and there are a few words written about it in the [SOLPS-ITER GUI documentation](https://static.iter.org/imas/assets/solps-iter/html/howto/install.html#solps-iter-installation)<span class="material-symbols-outlined">open_in_new</span>.




## How to initiate the SOLPS-ITER work environment

Once you have [downloaded](#get-access-to-solps-iter) and [compiled](#properly-configured-site) SOLPS-ITER, you may proceed to run the code. In every session, you must first initiate the *SOLPS-ITER work environment*. This is done by running the `setup.csh` script, which sets up the necessary environment variables and commands.

1. Log in to the server where your SOLPS-ITER is installed.

    ```
    ssh -X username@my.server.eu
    ```
   
    Refer to [Remote access](../supplementary/Remote_access.md) for the particular address of your server.

    /// danger | IPP Prague
    When accessing the Soroban cluster at IPP Prague, additionally ask the resource management system `qsub` to assign you some computational power in an interactive job.
    ```bash
    qsub -IX
    ```
    ///

   
2. Enter your SOLPS-ITER installation folder (also known as `$SOLPSTOP` - that is SOLPS top, not SOLP stop).

    ```
    cd /path/to/solps/solps-iter
    ```

3. Initiate the `tcsh` shell.

    ```
    tcsh
    ```

4. Load the environment variables and commands.

    ```
    source setup.csh
    ```

5. If you're going to use DivGeo, Carre of Triang (building a new simulation), specify the device name.

    ```
    setenv DEVICE besttokamak
    ```

/// danger | IPP Prague
In case of error `module: command cannot be found`, open or create a `.tcshrc` file in your home directory and paste inside this line:
```
source /usr/share/modules/init/tcsh
```
Open a new command line and try initiating the SOLPS-ITER work environment again.
///


## How to update SOLPS-ITER

SOLPS-ITER is a living code which constantly receives tweaks and bug fixes, as evident from the [SOLPS user forums](https://confluence.iter.org/spaces/IMP/pages/178135134/SOLPS-ITER#SOLPSITER-UserForumdebriefings)<span class="material-symbols-outlined">open_in_new</span> which take place approximately once a month. Users that don't need a specific version of the code should, therefore, stay in touch with the latest developments by updating their code when a new `master` is released. This is usually commemorated by naming the new `master` with a version number, e.g. SOLPS-ITER 3.0.9, and publishing a document called [Release notes](https://confluence.iter.org/spaces/IMP/pages/178135134/SOLPS-ITER#SOLPSITER-Releasenotesanddescriptionsofimportantcodeupdates)<span class="material-symbols-outlined">open_in_new</span>.

There are two ways to update the code, a simple one and a manual one. They both begin with [initiating the SOLPS work environment](#how-to-initiate-the-solps-iter-work-environment).

### Simple version

> This is only available for `master` or `develop` branches.

Depending on whether you want to use the `master` or `develop` branch, [initiate the SOLPS work environment](#how-to-initiate-the-solps-iter-work-environment) and use the command
```
solps-iter_update
```
or
```
solps-iter_update_develop
```
and wait approx. 30 minutes. This will take care of everything, including the compilation of the newest version of the [SOLPS-ITER manual](../supplementary/SOLPS-ITER_user_wisdom.md#rtfm) (in `$SOLPSTOP/docs/solps/solps.pdf`). If you don't know the difference between the `master` and the `develop` branch, use the `master` branch. It is more stable, meaning it should not ever be in a broken/buggy state, and it is updated about twice a year (as of January 2026). The `develop` branch is updated more frequently, but it's usually still quite reliable.

### Advanced, high-control version

> These steps are derived from the installation steps of the [properly configured site](#properly-configured-site) described above. If you want to understand what's going on here, check out the [introduction to Git](#introduction-to-git).

1. Check whether you have modified any source code files in the SOLPS-ITER folder and not committed them.

    ```
    git status
    ```

    If there are any, use your Git knowledge to commit them, stash them, or discard the changes. New (untracked) files are usually not a problem.

1. (Optional) You may switch to a different branch if you want.

    ```
    git checkout feature/wg_workflow
    ```

1. Download any changes made to SOLPS-ITER since your last update.

    ```
    git pull  # Note that `git fetch` is called automatically by `git pull`
    git submodule update --init
    ```

1. Compile the code using `gmake` or `make`, depending on how many letters you feel like spelling today.

    /// note | Fun fact
    On most standard Linux distributions `make` = `gmake`, but in some exotic cases `make` points to something else, as [discussed here](https://stackoverflow.com/questions/1194957/what-is-the-difference-between-gmake-and-make)<span class="material-symbols-outlined">open_in_new</span>. Thus, `gmake` should be preferred, just to be on the safe side.
    ///   

    /// tip | Clean when switching branches
    When switching code branches or versions, it is highly recommended to clean everything up by building the corresponding `clean_*` targets (or simply `gmake clean_all`). It is usually not necessary when updating the same branch.
    ///

    Start with the necessary `depend` target and follow with any targets you need, usually named `solps_*`. For example:

    ```
    gmake depend
    gmake solps
    gmake solps_mpi
    ```

    The complete list of available compilation targets is available by running `gmake help`.


## Introduction to Git

If you don't know what Git is, these are the necessary basics.

Simply put, [Git](https://git-scm.com/)<span class="material-symbols-outlined">open_in_new</span> is a version-tracking system which allows multiple users to collaborate on a single project without getting in each other's way. It is immensely complex, best used from the command line, dauntingly inscrutable at first and delightfully rewarding once you master it. The SOLPS-ITER code is developed using Git.

/// tip | Where to learn Git
In addition to the guide below, there are many well-written [Git tutorials](https://www.atlassian.com/git)<span class="material-symbols-outlined">open_in_new</span> on the internet. Bookmark the [official Git docs](https://git-scm.com/docs)<span class="material-symbols-outlined">open_in_new</span>. Learning Git properly is a good investment of your time, as it is used everywhere these days.
///

The story goes like this. On the vast servers of GitHub, there is a [repository](https://github.com/iterorganization/SOLPS-ITER)<span class="material-symbols-outlined">open_in_new</span> containing the source code of SOLPS-ITER. The source code is mostly composed of text files written in various programming languages; there are also some pictures and other files. The source code is what Git keeps track of. It remembers what changes to the code who proposed, when and why, if they were accepted, how they were discussed, and so on.

Anyone can download the source code of SOLPS-ITER to their computer. The easiest way is to install Git (it comes preinstalled in many operating systems) and run the `git clone repository_location` command. This connects the computer to the central code repository (called "remote" repository, sometimes `origin`) and downloads a copy of the current version of the source code. Now, the source code is not enough to run SOLPS-ITER, just like the blueprint of a bed cannot be slept in. First, you must compile the code on your computer, from the local copy of the source code, using the `make` command. Downloading the source code is quick; compiling it takes hours. At the end of it, you have a living programme which can be used to run simulations.

As time goes on, your local copy of SOLPS-ITER will grow outdated. Updates to the "`master` branch" (the most trustworthy version of the code) come once in a few months, and they can contain important bug fixes and plasma physics updates.

/// tip | Why update SOLPS-ITER when a new `master` comes out?
If something isn't working in SOLPS and you try to submit a bug report or ask about it on the [SOLPS Slack](http://solps.slack.com/)<span class="material-symbols-outlined">open_in_new</span>, the first reply will be: "Are you using the current `master` version?"
/// 

To check whether an update is available, open a command line, go to your SOLPS-ITER installation directory (`$SOLPSTOP`) and run:

```
git fetch
```

This will download the newest *information* (but will not apply any changes) from the `origin` repository at ITER Organisation. Then run:

```
git status
```

This will inform you whether any updates are available. You might, for instance, see the output:

```
On branch master
Your branch is up-to-date with 'origin/master'.
```

This means there are no updates available and your code is still fresh. If, however, you see something like "you are 1 commit behind 'origin/master'", it's a good time to update the code, starting with

```
git pull
```

Additionally, you might see something like:

```
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)
  (commit or discard the untracked or modified content in submodules)

	modified:   modules/B2.5 (untracked content)
	modified:   modules/Carre (untracked content)
	modified:   modules/DivGeo (untracked content)
	modified:   modules/Eirene (untracked content)
	modified:   whereami

Untracked files:
  (use "git add <file>..." to include in what will be committed)

	SETUP/config.IT4ICZ.ifort64
	SETUP/config.SOROBAN.ifort64
	SETUP/setup.csh.IT4ICZ.ifort64
	SETUP/setup.csh.SOROBAN.ifort64
	dg.dgo
	dg.str
	dg.trg
	modules/Triang/config/config.IT4ICZ.ifort64
	modules/Triang/config/config.SOROBAN.ifort64
	modules/Uinp/config/config.IT4ICZ.ifort64
	modules/Uinp/config/config.SOROBAN.ifort64
	modules/amds/config/config.IT4ICZ.ifort64
	modules/amds/config/config.SOROBAN.ifort64
	modules/solps4-5/config/config.IT4ICZ.ifort64
	modules/solps4-5/config/config.SOROBAN.ifort64
	param.dg
	scripts/sorobansubmit

no changes added to commit (use "git add" and/or "git commit -a")
```

It seems daunting, but it is usually quite harmless. The thing is, SOLPS-ITER compilation is different on every machine. Since every environment is unique, it requires a different configuration for installing SOLPS-ITER. The list above mostly concerns configuration files for the Soroban and IT4Innovations server. They are an addition to the SOLPS-ITER source code, being used mainly during its compilation and setting up the SOLPS-ITER work environment. They don't interfere with SOLPS-ITER updates because Git is only concerned with the files it tracks (stored in the `origin` repository) and it leaves any extra files alone.
