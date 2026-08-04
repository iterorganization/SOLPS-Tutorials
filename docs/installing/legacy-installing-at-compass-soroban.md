# Installing SOLPS-ITER at COMPASS (Soroban)

/// warning | This is a legacy tutorial
The instructions below are outdated and redundant! Since 2024 (SOLPS-ITER 3.0.9), COMPASS servers are a **properly configured site** and the [standard installation instructions](solps-iter-codebase.md#properly-configured-site) should be used.
///

This section offers two tutorials: one for the average user who just wants to install SOLPS-ITER at COMPASS and be done with it and another for COMPASS wizards who wish to tweak the configuration and libraries.

In April 2020, Aleš Podolník managed a great feat: he installed SOLPS-ITER at COMPASS. Since then he has created not only a central installation (located in `/scratch/solps/solps-iter` on all the Soroban nodes) but also this tutorial how each Soroban user can make their own installation. Both ways have their perks. The central installation allows users to run SOLPS-ITER out-of-the-box, without installing it or receiving access to the [SOLPS-ITER repository](https://git.iter.org/projects/BND/repos/solps-iter/browse)<span class="material-symbols-outlined">open_in_new</span>. Unfortunately, this isn't a good long-term solution. SOLPS-ITER doesn’t separate code and user data, and so all our grids are on the same heap in the `carre` submodule, all our runs are in the same `runs` folder etc., which will inadvertently lead to confusion. Additionally, it means we’re all stuck using the same version of SOLPS-ITER and that we can’t make changes in the code or update it as we like. Therefore, it is recommended for all who wish to get serious with SOLPS-ITER that they make their own installation.


## SOLPS-ITER installation for the average user

First, create your working directory, ideally in `/ansys/fast/$USER/solps`, in the fast storage space (it was initially created for ANSYS, however, it is large and IT has agreed to use it also for our purposes). In this tutorial, we use `soroban-front-01` for compilation.
```bash
ssh $USER@soroban-front-01    # the .tok.ipp.cas.cz part can be left out if you're using the COMPASS VPN, which you should be if you're outside the institute
mkdir /ansys/fast/$USER/solps
```

This is accessible from all workstations using the same path.

Go back to your working directory and try to clone the SOLPS-ITER repository from ITER:
```bash
git clone ssh://git@git.iter.org/bnd/solps-iter.git
```
If you get the error
```
Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights and the repository exists.
```
...you first need to set up SSH key authentication to identify your machine with your ITER user account. Go to [<span class="underline">https://git.iter.org/plugins/servlet/ssh/account/keys</span>](https://git.iter.org/plugins/servlet/ssh/account/keys)<span class="material-symbols-outlined">open_in_new</span>, log in and add a public key corresponding to a private key in your `~/.ssh/` folder. If you don't have any SSH keys generated yet, you can create them using
```bash
cd ~/.ssh
ssh-keygen -t rsa -C "your_email@example.com"
```
For added security, it is recommended to enter a non-empty private key passphrase. Once your keys are generated, upload (that is, copy-paste the inside of the `id_rsa.pub` file) your new public key to the public key list. Now the `git` command should work. Wait for a few minutes while everything is downloading.

Update the code to the latest version of the master branch (the default branch):
```bash
cd solps-iter
git submodule init
git submodule update
```
Wait for a bit again. You will be prompted to enter your key passphrase several times. The SOLPS manual then recommends to make sure that SOLPS-ITER and all its submodules (Carre, Divgeo, Adas...) are on their `master` branch:

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

We have later (03/2023) found out that the newest version of SOLPS does not converge old COMPASS-U runs. The following version is the last checked running version of SOLPS (later versions are up for investigation):

```bash
cd solps-iter
git checkout 3.0.8-29-gf89a6a23
cd modules/B2.5
git checkout 3.0.8-7-gaa9ddd5c
cd ../Eirene
git checkout 3.0.8-4-gaff74046
cd ../Carre
git checkout 3.0.8-4-g5da80da
cd ../DivGeo
git checkout 3.0.8-8-g6852ae9
```

Currently, all libraries and paths necessary for SOLPS are handled by modules. The only recommended option is `solps/intel_oneapi`. There are several other Intel modules, however, all of them have the downside of not being functional. All files related to those modules are stored in `/compass/Shared/Common/IT/SW/SOLPS/modules/MODULE_NAME`.


<a name="soroban_configuration_files"></a>
When everything's ready for installation, copy the COMPASS configuration files into your SOLPS-ITER repository. They are stored in module directory, e.g. for `solps/intel_oneapi`, the proper location is `/compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi/solps-local/`. Take care not to overwrite the `.git` subdirectory as well.
```bash
cp -r /compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi/solps-local/modules/ /ansys/fast/$USER/solps/solps-iter/
cp -r /compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi/solps-local/runs/ /ansys/fast/$USER/solps/solps-iter/
cp -r /compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi/solps-local/scripts/ /ansys/fast/$USER/solps/solps-iter/
cp -r /compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi/solps-local/SETUP/ /ansys/fast/$USER/solps/solps-iter/
cp /compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi/solps-local/whereami /ansys/fast/$USER/solps/solps-iter/
```

Check whether the `tcsh` shell recognizes the `module` command.
```bash
tcsh
module --help
```
If it does not, create a `.tcshrc` file in your home directory with the following content:
```bash
source /usr/share/modules/init/tcsh
```
If the file already exists, add this line to it. Now open `tcsh` again and initiate the SOLPS-ITER work environment.
```bash
source setup.csh
```
If this is your **first installation of SOLPS-ITER** at Soroban, run:
```
first_setup
```
(There are several reasons why one might want several installations of SOLPS-ITER in their file space. The most benign one is that you're running several SOLPS-ITER versions for their respective quirks. The most common one is that a previous installation stopped working and you're making a fresh start.)

Finally, compile SOLPS-ITER and it's parallelised version (MPI = Message Passing Interface).
```bash
make solps && make solps_mpi
```
Build both targets because single-threaded B2 is used by default by some scripts. The compilation may take a long time, around 1 hour. Don't mind the repeated `ifort: command line remark #10148: option '-vec_report0' not supported` warning - it concerns the unsuccessful writing of optimisation logs.

Congratulations, you have installed your very own copy of SOLPS-ITER on COMPASS!


## SOLPS-ITER installation for wizards

### Preparation

Create a directory for installation of libraries. This example shows how the `solps/intel_oneapi` module was prepared. We use one directory per module, in this case `/compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi`. There is an environment file containing all modules to be loaded in `/compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi/environment.sh`. Source this file before compilation.
```bash
cd /compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi
source environment.sh

```

An important notice is that everything necessary for compilation and also for code execution is in `/compass/Shared/Common/IT/SW/SOLPS/modules/modulefiles/intel_oneapi` (`modulefiles` is a symlink to module storage). For compilation, it is useful to set up some environment variables pointing to installation directories (and of course to create those directories).
```bash
export SOLPS_LOCAL=/compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi/local
export SOLPS_SW=/compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi/sw
mkdir -p $SOLPS_LOCAL
mkdir -p $SOLPS_SW
```
In this example, we will download libraries source files to `$SOLPS_SW` and install libraries to `$SOLPS_LOCAL/lib` as if it was `/usr/local`. The SOLPS directory will be `solps-iter` (located on our preferred server, i.e. `/ansys/fast/$USER/solps-iter` in this example). Although SOLPS supports multiple users, prefered mode of operation is one installation per user (so unless you share working directory with others, use something like `/ansys/fast/podolnik/solps-iter`).

If you plan to use your own copy of SOLPS even with installation of your libraries, use different directories using your user scratch space (but this is not recommended, I did it only for debugging of the library installation):

```bash
export SOLPS_LOCAL=/ansys/fast/$USER/solps/local
export SOLPS_SW=/ansys/fast/$USER/solps/sw
mkdir -p $SOLPS_LOCAL
mkdir -p $SOLPS_SW
```
To access some repositories, you need to obtain credentials to ITER infrastructure.

### Required libraries

The required libraries are listed in config and setup files. This is an attempt to install them here.

We’ll use our latest Intel compilers and some other libraries (in 05/2023, finally, this was updated to `intel_oneapi` as a main compiler. This is just a summary what is imported -- do not run these lines -- instead, for library compilation, just source the environment file `/compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi/environment.sh`. In case you are now compiling SOLPS itself, this is unnecessary, as everything is already present in `config.SOROBAN.csh`

```bash
module load intel_oneapi
module load mdsplus/7-1-13
module load netcdf/4.6.1
module load python/3.9-solps

export CC=icc
export FC=ifort
export F77=ifort
export CXX=icpc
```

**The system**

SOLPS contains a myriad of scripts written in C shell, however, it requires `tcsh` shell instead of pure `csh`. Thus it expects that both `/usr/bin/csh` and `/bin/csh` to be, in fact, `tcsh`. HPC infrastructure usually (Marconi, IT4I) obeys this rule. However, on local clusters, this may or may not be satisfied. This has already been fixed on Soroban.

The order of installation is important (GLI has to precede GR, since otherwise it links to improper version of libraries).

First, `solps-local` was cloned into module directory (`/compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi`). A branch with this module-specific configuration was created in [the repository](https://repo.tok.ipp.cas.cz/solps/solps-local)<span class="material-symbols-outlined">open_in_new</span>.

You can check `_makefiles` subdirectory for "proven" makefiles. There is also a configuration file `ncl/config/site.local` for configuration of NCL library.

**MSCL**

Can be downloaded from ITER git repository.
```bash
cd $SOLPS_SW
git clone ssh://git@git.iter.org/lib/mscl.git
```
And then installed using installation scripts. Let’s install the library into some arbitrary folder, let’s say `$SOLPS_LOCAL`.

Current version of the library is not compatible with SOLPS sources. We will have to use an older one (eg. installation at ITM uses a binary compiled 10 years ago).
```bash
cd mscl
git checkout a64eba15137
```
There can be an issue with C preprocessor (`cpp`), which prints out a copyright notice, which causes Fortran compiler to fail. You have to modify the makefile everywhere cpp is called. Changing `${CPP} -P -C` to `${CPP} -P` should do the trick. Now, you can compile it. It is also recommended to change the compiler in the Makefile to `icc` as it does not use the `CC` environment variable.
```bash
export OBJECTCODE=linux.ifort64
export SOLPS_LIB=$SOLPS_LOCAL/lib
mkdir -p $SOLPS_LIB
make
make install
```
Then it is necessary to include the proper linking path and flag to config and setup files.

For archiving purposes, here are the older instructions. Don't use them.
```bash
cd mscl
./bootstrap
./configure --prefix=$SOLPS_LOCAL
make
make check
make install
```

**GLI**

GR libraries need GLI to work. GLI can be downloaded from Jülich site. [https://pgi-jcns.fz-juelich.de/portal/pages/gli.html](https://pgi-jcns.fz-juelich.de/portal/pages/gli.html)<span class="material-symbols-outlined">open_in_new</span>
```bash
cd $SOLPS_SW
wget https://iffwww.iff.kfa-juelich.de/pub/gli/gli-4.5.30.tar.gz
tar -xzf gli-4.5.30.tar.gz
```
Compilation:
```bash
export CFLAGS=-DUSE_INTERP_RESULT
export CC=icc
cd gli/src
./configure --prefix=$SOLPS_SW/gli/install
```
Also the linker was set to `icc`.

The `USE_INTERP_RESULT` env. variable is necessary for correct compilation. We do not use local directory because gli does not install nicely.

Now, you have to modify makefile, replacing `-u MAIN__` by `-nofor-main` in cases when ifort is used for linking. Afterwards, proceed with make.
```bash
make
make install
```

**GR**

Can be downloaded from ITER git repository.

```bash
cd $SOLPS_SW
git clone ssh://git@git.iter.org/lib/gr-software.git
```
Path to GLI has to be specified inside the makefile:
```bash
GLI_HOME=${SOLPS_SW}/gli/install
```
Then, the library can be installed:
```bash
cd gr-software
export SOLPS_LIB=$SOLPS_LOCAL/lib
make linux.ifort64
```
The installation directory is `SOLPS_LIB`.

**NAG**

We do not have NAG, thus we will use MKL instead. See the config file update in further text.

**NCARG**

SOLPS also needs NCARG libraries (NCL and stuff). We were using precompiled binaries provided by NCL. This is the most tricky part.

Using precompiled libraries failed for Intel OneApi thus we decided to compile the NCARG library for ourselves from sources. Following steps were taken:

- Source the proper configuration (`/compass/Shared/Common/IT/SW/SOLPS/sw/environment.sh`).
- First, do everything in the [main documentation](http://ncl.ucar.edu/Download/build_from_src.shtml#CustomizeNCLBuildEnvironment)<span class="material-symbols-outlined">open_in_new</span> (especially the Customize... part).
- Check everything.
- Setup the `LINUX` (`config/LINUX`) configuration according to `/compass/Shared/Common/IT/SW/SOLPS/sw/ncl/src/ncl_config/LINUX`, mainly the paths:
```
#define LibSearchUser    -L/usr/lib64 -L/compass/Shared/Common/IT/SW/SOLPS/sw/ncl/system/lib64 -L/compass/Shared/Common/IT/SW/SOLPS/sw/ncl/system/lib64/hdf5/serial
#define IncSearchUser    -I/compass/Shared/Common/IT/SW/SOLPS/sw/ncl/system/include64 -I/usr/include -I/usr/include/freetype2 -I/usr/include/hdf5/serial
```
- Also do not forget to set `FC=ifort`.
- Run configure `./Configure -v`
    - Set proper paths, i.e.
    - Installation root: `/compass/Shared/Common/IT/SW/SOLPS/sw/ncl/local` (also known as `PREFIX` in other distributions, the base directory for installation)
    - Temporary path (whatever you have access to).
- Say no to all, except:
    - NetCDF4 (twice)
    - triangle (do not forget to adhere to instructions on copying the sources from the internet)
    - HDF5
- You should not have to modify paths if you have updated the `LINUX` configuration beforehand.
- `make Everything >& make-output &`
- `tail -f make-output`

These problems cost me a lot of effort:
- The makefile creator yMake uses `#define` directives. Unfortunately, there is a directive with name `X86_64`, which is also a part of important paths in our system. To override this, necessary directories were symlinked to `/compass/Shared/Common/IT/SW/SOLPS/modules/intel_oneapi/sw/ncl/system` and used for the compilation.
- Linking from both `-L/usr/lib` and `-L/usr/lib64` was the cause of `undefined reference to __libc_csu_fini` error. Only `lib64` is necessary.
- Logging problem. NCL library uses GKS and its error logging system. However, due to some incompatibilities between Fortran version, error logging routine `ncarg2d/src/libncarg_gks/awi/gerlog.f` fails. This then causes `b2plot` to fail, if an error is logged. Simple modification on the failing line 24 in the file can prevent this:
```fortran
WRITE(ERRFIL,*) ERRNR,GNAM(FCTID+1)
```
The error is then logged without formatting.

If you wish to make further changes in configuration, usually, modification of `config/LINUX` suffices. Follow these instructions upon editing it:
- Create new configuration using `./Configure -v`, select `n` when asked about overwriting existing configuration
- `make Everything >& make-output &`
- `tail -f make-output`

It is also important to correctly set the path to `NCARG_ROOT` (without any trailing `lib` etc.) -- then the fonts are not loaded properly and `b2plot` can fail again.

**NetCDF and HDF5**

We will use those provided by modules loaded above.

**MDSplus**

See the config file change in following text. Appropriate compass module should be loaded (at the time being `mdsplus/7-1-13`). Module path should be specified in the config file.

**System libraries**

- Cairo (libcairo.a) is provided by package `libcairo-dev`.
- Xmuu (libXmuu.a) is provided by package `libxmuu-dev`.

And several other commonly present libraries (`lz` etc).

**Environment**

SOLPS authors expect you to work in C shell. However, it is not common to use it here, thus you probably do not have your `.tcshrc` file set up. You have to create it in your home directory. It should contain at least this line of code:
```bash
source /usr/share/modules/init/tcsh
```
This enables the `module` command.

**Further modifications**

Due to incompatibility in the compiler, the Makefile from module amds had to be modified, replacing `cc` compiler with the repository-wide option `$(CC)`, see the `$(RES2FBR)` rule:
```
$(RES2FBR): $(OBJDIR)/res2fbr.o $(MAKES)
	*$(CC) $(CFLAGS)* -o $(RES2FBR) $(OBJDIR)/res2fbr.o
```

### Downloading SOLPS-ITER

*Copied from installation instructions from SOLPS-ITER folder at ITER org.*

You can generally browse the ITER Git repositories here: [https://git.iter.org](https://git.iter.org)<span class="material-symbols-outlined">open_in_new</span> and SOLPS-ITER specifically here: [https://git.iter.org/projects/BND/repos/solps-iter/browse](https://git.iter.org/projects/BND/repos/solps-iter/browse)<span class="material-symbols-outlined">open_in_new</span>, but since these repositories are restricted you will first need to authenticate with your ITER username and password – possibly twice, once for the intranet, and once for the Git web front end in the top right-hand corner.

If you upload a copy of your public ssh key here: [https://git.iter.org/plugins/servlet/ssh/account/keys](https://git.iter.org/plugins/servlet/ssh/account/keys)<span class="material-symbols-outlined">open_in_new</span> (by following links under “Manage Account”), then you should be able to simply clone a copy of SOLPS-ITER to your local machine by doing:
```bash
git clone ssh://git@git.iter.org/bnd/solps-iter.git
cd solps-iter
git submodule init
git submodule update
```
You will be prompted with your key passphrase several times.

**Configuration files**

Configuration files modified with necessary modifications are stored with directory structure matching the SOLPS installation in the directory `/compass/Shared/Common/IT/SW/SOLPS/solps-local`. The directory contains files for Soroban as well as for the IT4I infrastructure. Copying these files into the SOLPS-ITER repository directory will rewrite the script whereami. Following sections will describe the modifications that have been made. Version tracking is available at [https://repo.tok.ipp.cas.cz/solps/solps-local](https://repo.tok.ipp.cas.cz/solps/solps-local)<span class="material-symbols-outlined">open_in_new</span>.

To use these configuration files, just copy the entire directory contents into the repository directory (solps-iter). Do not overwrite the `.git` subdirectory\!

The script `whereami` (in the root of the repository) is modified to guess the server using hostname. Following lines added:
```
case "soroban*.tok.ipp.cas.cz":
echo SOROBAN
breaksw
```
Two files containing necessary configuration are created in SETUP directory (using files from ASDEX as a template):

- `config.SOROBAN.ifort64`
- `setup.csh.SOROBAN.ifort64`

**config.SOROBAN.ifort64**

`solps/solps-iter/SETUP/config.SOROBAN.ifort64`

**Libraries referencing**

We will modify the following paths:
```
       NCDIR ?= /usr/lib/x86_64-linux-gnu
   MSCL_ROOT ?= /compass/Shared/Common/IT/SW/SOLPS/local
       H5DIR ?= /usr/lib/x86_64-linux-gnu/hdf5/serial
     GR_ROOT ?= /compass/Shared/Common/IT/SW/SOLPS/local
    GLI_HOME ?= /compass/Shared/Common/IT/SW/SOLPS/sw/gli/install
  NCARG_ROOT ?= /compass/Shared/Common/IT/SW/SOLPS/ncl/ncl_stable
      NAGDIR ?= .
 MDSPLUS_DIR ?= /sw/mdsplus/7-1-13
```

Other changes follow.

Note that there is a NetCDF library directory (`NCDIR`), which has a purpose when NetCDF libraries are not on `LD_LIBRARY_PATH`. In our case, they are, thus we modify the linker path accordingly (by omitting `-L${NCDIR}` reference). If this library directory was specified explicitly, the linker would also link other libraries from `NCDIR`, ignoring the hierarchy provided by `LD_LIBRARY_PATH`, which can mess up things for MPI compilation:
```
LD_NETCDF  = -lnetcdff -lnetcdf
```

**NAG**

NAG license is expensive, thus we use random number generators from MKL.
```
LD_NAG = ${MKLROOT}/lib/intel64/libmkl_blas95_lp64.a ${MKLROOT}/lib/intel64/libmkl_lapack95_lp64.a -L${MKLROOT}/lib/intel64 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lpthread -lm -ldl
```
and
```
SOLPS_CPP = -DNCAR4 -DNO_F01AAF **-DNO_NAG**
```
**setup.csh.SOROBAN.ifort64**

`/net/soroban-node-04/solps/solps-iter/SETUP/setup.csh.SOROBAN.ifort64`

Proper modules should be loaded and environment variables set up.
```bash
module purge
module load solps/common

setenv NCDIR /usr/lib/x86_64-linux-gnu
setenv LATEX xelatex
setenv MSCL_ROOT $SOLPS_LOCAL
setenv GLI_HOME $SOLPS_SW/gli/install
setenv NCARG_ROOT $SOLPS_SW/ncl/ncl_stable
```

### Installing SOLPS-ITER

Prior to installation, check whether the tcsh shell instlalled on the computer recognizes the module command. If it does not, you should create (or add a line to an existing) `.tcshrc` file in your home directory:
```bash
source /usr/share/modules/init/tcsh
```
Run `tcsh` and load the configuration you have provided.

```
tcsh
# (tc shell starts)
source setup.csh
first_setup
```

First setup command copies the configuration file to necessary places.

**Additional modifications**

You then have to modify each individual config.SOROBAN.ifort64 file in all submodule configuration directories (`submodule_name/config`). If config file does not exist, it is not necessary to create one. Submodules also contain some subpackages with their own config files. These need to be modified as well.

All config files, as I have used them, can be copied from a local directory (see *Configuration files* above).

Following modifications are necessary:

Replace CPP:
```
CPP = cpp -traditional -ffreestanding
```
The flag -C produces a copyright notice, which is in C-style. This interrupts Fortran compilation.

Replace FC when needed (mpif90 is unfortunately a wrapper for gfortran here):
```
FC = mpiifort -I${MKLROOT}/include/intel64/lp64 -mkl=sequential
# or
FC = ifort -I${MKLROOT}/include/intel64/lp64 -mkl=sequential
```
Replace CC when needed:
```
CC = icc -I${MKLROOT}/include/intel64/lp64 -mkl=sequential
```
Do not replace CC in adas submodule.

**Building**

Then you can proceed with `make`.
```
make solps && make solps_mpi
```
Build both targets because single-threaded B2 is used by default by some scripts.

### Problems

**Bad object format**

Linker may complain that there is an unrecognized object format. This means that one of your libraries is compiled using a different compiler version (an incompatible one) than the others calling it. Good luck on finding which one (additional messages may be helpful). However, checking compiler versions when loading modules (also check underlying gcc version if possible).
