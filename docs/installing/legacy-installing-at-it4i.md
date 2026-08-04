# Installing SOLPS-ITER at IT4I (Karolina, Barbora)

/// warning | This is a legacy tutorial
The instructions below are outdated and may not work, and/or may be unnecessarily complicated! Use at the risk of your own time wasted. See the [Installation overview](solps-iter-codebase.md#where-and-how-to-install-solps-iter) for better alternatives (e.g. Docker or Apptainer containers).
///

Assuming that you have access to the SOLPS-ITER codebase you can proceed with the installation at the IT4I cluster. Currently, the cluster features two computers, Karolina and Barbora. The author has verified this approach on Karolina (CentOS 7). Sadly, Barbora was recently upgraded and now features different linux distribution (RHEL 8), which broke some things again.

Outline:

1. Create directories, download code
1. Pre-installed libraries
    * load as modules, easy
1. External libraries
    * some libs are not available (downloaded and compile manually)
1. Configure SOLPS-ITER with paths to libs, etc.
1. Compile SOLPS-ITER
    * pray that no libs are missing, otherwise return to step 3.

## Preparation

Create a directory for installation. IT4I assigns you a project directory on fast storage, which is recommended place to run your simulations.
```bash
IT4I_PROJECT={your project id}
export SOLPS_SW=/scratch/work/project/$IT4I_PROJECT/solps/sw
export SOLPS_LOCAL=/scratch/work/project/$IT4I_PROJECT/solps/local
mkdir -p $SOLPS_SW $SOLPS_LOCAL $SOLPS_LOCAL/lib
```
We have exported `SOLPS_LOCAL` and `SOLPS_SW` env. variables as shortcuts to the subdirectories of the install directory (`/scratch/work/project/$IT4I_PROJECT/solps`), where the locally compiled libraries will be stored. They will serve us well on our journey.

## Required libraries

All required libraries are listed in config and setup files. We will go through them one by one and attempt to install them here. For starters, some fundamental libraries are already available on the system as modules. Use the latest Intel compilers, Cairo and netCDF.
```
module purge
module load intel/2020b
module load cairo/1.16.0-GCCcore-10.2.0
module load netCDF-Fortran/4.5.3-intel-2020b
```
Although there are specific version of the modules listed above, note that they may not be available in the future (=present) because the computers get upgraded from time to time. Just try to load some combination of versions that are compatible with each other (or use the default ones, i.e. `intel cairo netCDF-Fortran`).

### The system

SOLPS contains a myriad of scripts written in C shell, however, it requires `tcsh` shell instead of pure `csh`. Thus it expects that both
```
/usr/bin/csh
/bin/csh
```
to be, in fact, `tcsh`. HPC infrastructure usually (Marconi, IT4I) obeys this rule. Feel free to check anyways that both paths are links
```bash
$ ls -l /bin/csh /usr/bin/csh
lrwxrwxrwx 1 root root 13 Nov 20 00:02 /bin/csh -> /usr/bin/tcsh
lrwxrwxrwx 1 root root 13 Nov 20 00:02 /usr/bin/csh -> /usr/bin/tcsh
```

### Lib MSCL

Can be downloaded from ITER git repository.
```bash
cd $SOLPS_SW
git clone ssh://git@git.iter.org/lib/mscl.git
```

Adjustments:

- Current version of the library is not compatible with SOLPS sources. We need to use an older one (ITM uses a binary compiled 10 years ago).

        cd mscl
        git checkout a64eba15137

- There can be an issue with C preprocessor (cpp), which prints out a copyright notice, which causes Fortran compiler to fail. Replace `${CPP} -P -C` with `${CPP} -P` everywhere in the Makefile. Avoid hard work by using this bash trickery:

        cp Makefile Makefile.back
        sed 's/\(${CPP}.*\) -C/\1/g' Makefile.back > Makefile

Finally, compile.
```bash
export OBJECTCODE=linux.ifort64 SOLPS_LIB=$SOLPS_LOCAL/lib
make
make install
# Creates $SOLPS_LOCAL/lib/libmscl.a
```


### Lib GLI (GR dependency)

GR libs have a dependency of their own: **GLI**. We need to install that first. GLI can be downloaded from Jülich site. [https://pgi-jcns.fz-juelich.de/portal/pages/gli.html](https://pgi-jcns.fz-juelich.de/portal/pages/gli.html)<span class="material-symbols-outlined">open_in_new</span>
```bash
cd $SOLPS_SW
wget https://iffwww.iff.kfa-juelich.de/pub/gli/gli-4.5.30.tar.gz
tar -xzf gli-4.5.30.tar.gz
```

Adjustments:

- Flag `USE_INTERP_RESULT` is necessary for correct compilation. Also, we use `$SOLPS_SW/gli/install` instead of the local directory because GLI does not install nicely.

        cd gli/src
        export CFLAGS=-DUSE_INTERP_RESULT
        mkdir -p $SOLPS_SW/gli/install
        ./configure --prefix=$SOLPS_SW/gli/install

- Modify Makefile, replacing `-u MAIN__` with `-nofor-main` **only** in cases when `ifort` is used for linking and replacing. Also, Zlib tends to be incorrectly recognized so replace direct path `/usr/lib64/libz.so` with library flag `-lz`. Avoid hard work by using this bash trickery:

        cp Makefile Makefile.back
        sed -i ':a;N;$!ba;s/\\\n//g' Makefile
        sed -i 's/\(ifort.*\)-u MAIN__/\1-nofor-main/g' Makefile
        sed -i 's|/usr/lib64/libz.so|-lz|g' Makefile

Finally, compile.
```bash
make
make install
# Populates $SOLPS_SW/gli/install directory
```

### Lib GR

Now we can proceed with the GR installation itself. Can be downloaded from ITER git repository.
```bash
cd $SOLPS_SW
git clone ssh://git@git.iter.org/lib/gr-software.git
```

Adjustments:

- Path to GLI has to be specified inside the Makefile as `GLI_HOME=${SOLPS_SW}/gli/install`. Bash trickery for lazy people can do this for you:

        cd gr-software
        cp Makefile Makefile.back
        sed 's|\(GLI_HOME=\).*$|\1${SOLPS_SW}/gli/install|g' Makefile.back > Makefile

Finally, compile.
```bash
export SOLPS_LIB=$SOLPS_LOCAL/lib
make linux.ifort64
# Creates $SOLPS_LOCAL/lib/libgr.a
```

### Lib NAG

We do not have NAG, thus we will use MKL instead. See the config file update in further text.

### Lib NCARG &lt;precompiled&gt;

SOLPS also needs NCARG libraries (NCL and stuff). We are using precompiled binaries provided by NCL. This is the most tricky part. Download from [<span class="underline">https://www.earthsystemgrid.org/dataset/ncl.662.dap/file.html?df=true</span>](https://www.earthsystemgrid.org/dataset/ncl.662.dap/file.html?df=true)<span class="material-symbols-outlined">open_in_new</span> (choose one according to your OS, probably CentOS7 64bit for IT4I). Compiling NCARG from sources proved to be a nightmare.
```bash
cd $SOLPS_SW
wget https://www.earthsystemgrid.org/api/v1/dataset/ncl.662.dap/file/ncl_ncarg-6.6.2-CentOS7.6_64bit_gnu485.tar.gz
mkdir ncl_precompiled
tar -xzf ncl_ncarg-6.6.2-CentOS7.6_64bit_gnu485.tar.gz -C ncl_precompiled
```

### Libs NetCDF and HDF5

Already loaded as modules (see above).

### Lib MDSplus

Can be downloaded from github, use a stable release.
```bash
cd $SOLPS_SW
wget https://github.com/MDSplus/mdsplus/archive/refs/tags/stable_release-6-1-84.tar.gz
tar -xzf stable_release-6-1-84.tar.gz
mv mdsplus-stable_release-6-1-84 mdsplus
```

Adjustments:

- For some reason the Makefile in *mitdevices* overrides the variable `LD_LIBRARY_PATH` instead of appending to it, which causes errors. Fix it by replacing `LD_LIBRARY_PATH=<something>` with `LD_LIBRARY_PATH=$(LD_LIBRARY_PATH):<something>`. Of course, you can use bash trickery to do that:

        cd mdsplus
        cp mitdevices/Makefile mitdevices/Makefile.back
        sed 's/\(LD_LIBRARY_PATH\)=/\1:=$(\1):/g' mitdevices/Makefile.back > mitdevices/Makefile

Finally, configure and compile.
```bash
mkdir -p $SOLPS_SW/mdsplus/builds/it4i
./configure --disable-java --prefix=$SOLPS_SW/mdsplus/builds/it4i
make
make install
# Populates $SOLPS_SW/mdsplus/builds/it4i/lib directory
```

> If you encounter "No rule to make target `svrgn.o'" after repeated compilation attempts (after "make clean"), try deleting the source directory and redo all steps starting with extracting the tar archive.

### System libraries

- Cairo (libcairo.a) is provided by module cairo (already loaded).
- Xmuu (libXmuu.a) is provided by package libxmuu-dev (at IT4I provided by cairo module).

And several other commonly present libraries (`lz` etc). No issues there.

## SOLPS-ITER itself

*Copied from installation instructions from SOLPS-ITER folder at ITER org.*

You can generally browse the ITER Git repositories here: https://git.iter.org and SOLPS-ITER specifically here: [https://git.iter.org/projects/BND/repos/solps-iter/browse](https://git.iter.org/projects/BND/repos/solps-iter/browse)<span class="material-symbols-outlined">open_in_new</span>, but since these repositories are restricted you will first need to authenticate with your ITER username and password – possibly twice, once for the intranet, and once for the Git web front end in the top right-hand corner.

If you upload a copy of your public ssh key here: [https://git.iter.org/plugins/servlet/ssh/account/keys](https://git.iter.org/plugins/servlet/ssh/account/keys)<span class="material-symbols-outlined">open_in_new</span> (by following links under “Manage Account”), then you should be able to simply clone a copy of SOLPS-ITER to your local machine by doing:
```bash
git clone ssh://git@git.iter.org/bnd/solps-iter.git
cd solps-iter
git submodule init
git submodule update

#Switch to the respective master branches
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
You will be prompted with your key passphrase several times.

### Configuration files

Modify the script `whereami` (in the root of the repository) to guess the server using hostname. Add the following lines:
```bash
case "*.it4i.cz":
echo IT4ICZ
breaksw
```
Then create the two main configuration files in the SETUP directory (as listed below), use files from ??ASDEX as a template and modify accordingly. The first file specifies paths to the libraries and compiler options, while the other one essentially does tbe same thing (?).

1. Config ... *solps-iter/SETUP/config.IT4ICZ.ifort64*

    First, modify the following paths in this config so that they point to our installed libraries.

        NCDIR ?= /apps/all/netCDF/4.6.2-intel-2017c
        H5DIR ?= /usr/lib/x86_64-linux-gnu/hdf5/serial
        MSCL_ROOT ?= ${SOLPS_LOCAL}
        GR_ROOT ?= ${SOLPS_LOCAL}
        GLI_HOME ?= ${SOLPS_SW}/gli/install
        NCARG_ROOT ?= ${SOLPS_SW}/ncl_precompiled
        # NAGDIR ?= ${NAGFLIB_HOME}
        NAGDIR ?= .
        MDSPLUS_DIR ?= ${SOLPS_SW}/mdsplus/builds/it4i

     Then change path to NAG and related compiler options.

        LD_NAG = ${MKLROOT}/lib/intel64/libmkl_blas95_lp64.a ${MKLROOT}/lib/intel64/libmkl_lapack95_lp64.a -L${MKLROOT}/lib/intel64 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lpthread -lm -ldl

        # ... (a few lines below) ...

        SOLPS_CPP = -DNCAR4 -DNO_F01AAF -DNO_NAG

2. Config ... *solps-iter/SETUP/setup.csh.IT4ICZ.ifort64*

    This config loads all relevant modules and sets important environment variables (mainly the LD_LIBRARY_PATH, which specifies paths to shared libraries for the compiler).

        module purge
        # Use the same modules that were used to compile the libraries
        module load intel/2020b
        module load cairo/1.16.0-GCCcore-10.2.0
        module load netCDF-Fortran/4.5.3-intel-2020b
        module load latex/2020

        setenv NCDIR /apps/all/netCDF/4.6.2-intel-2017c
        setenv LATEX "/apps/all/latex/2020/bin/x86_64-linux/pdflatex -interaction=nonstopmode"
        setenv MSCL_ROOT ${SOLPS_LOCAL}
        setenv GLI_HOME ${SOLPS_SW}/gli/install
        setenv MDSPLUS_DIR ${SOLPS_SW}/mdsplus/builds/it4i
        setenv LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:${NCDIR}/lib64:${MSCL_ROOT}/lib:${GLI_HOME}:${MDSPLUS_DIR}/lib

    LaTeX in this example unfortunately outputs very bad output, because we ignore any errors. We have to do it like this at IT4I because there is no suitable TeX working with modules compatible with other libraries. This is ridiculous.

### First time setup (distribute the config files)

Prior to installation, check whether the `tcsh` shell instlalled on the computer recognizes the `module` command. If it does not, you should create (or add a line to an existing) `.tcshrc` file in your home directory:
```bash
# Contents of "~/.tcshrc"
source /usr/share/modules/init/tcsh
```
Run `tcsh` and load the configuration you have provided.
```bash
tcsh

source setup.csh
first_setup
```
The `first_setup` script parses and copies the configuration files to all of the appropriate locations. **Only use it if this is your first installation of SOLPS-ITER at IT4I.** Otherwise, skip it.

### Fix the distributed config files

Now you have to modify each individual `config.IT4ICZ.ifort64` file in all submodule configuration directories (`submodule_name/config`). If config file does not exist, it is not necessary to create one. Submodules also contain some subpackages with their own config files. These need to be modified as well. Proceed with following.

- Replace `CPP`:

        CPP = cpp -traditional -ffreestanding

    We are removing the flag `-C`, which produces a copyright notice, which is in C-style. This interrupts the Fortran compilation.

- Replace FC where present:

        FC = mpif90 -I${MKLROOT}/include/intel64/lp64 -mkl=sequential
        # or
        FC = ifort -I${MKLROOT}/include/intel64/lp64 -mkl=sequential

- Replace CC where present (do not replace CC in the **adas** submodule):

        CC = icc -I${MKLROOT}/include/intel64/lp64 -mkl=sequential


### Building

Finally, you can proceed with `make`.
```bash
make solps && make solps_mpi
```
Due to LaTeX problems, it will probably end with Error 2, but if the manual was the last thing to be done, the code is ready to be run. Otherwise, it can be fixed by adding special targets (which skip the TeX compilation) to the Makefile:
```Makefile
solps_it4i: carre divgeo b25eirene uinp triang amds sonnet-light
solps_mpi_it4i: carre divgeo b25eirene_mpi uinp_mpi triang_mpi amds_mpi sonnet-light
```
Then, make those targets.
```bash
make solps_it4i && make solps_mpi_it4i
```
And make the manual on its own with an appropriate latex module.
```bash
module purge && module load latex/2020
make manual
```

## Problems with (SOLPS-ITER) compilation

**Bad object format**

Linker may complain that there is unrecognized object format. This means that one of your libraries is compiled using different compiler version (an incompatible one) than the others calling it. Good luck on finding which one (additional messages may be helpful). However, checking compiler versions when loading modules (also check underlying gcc version if possible).

**ld: somelibrary.so not found**

You have probably omitted one of necessary paths in definition of `LD_LIBRARY_PATH`.
