# Installing SOLPS-ITER in a container

In its essence, a container is a tiny virtual computer which contains nothing but the software you wish to run (here SOLPS-ITER) and the libraries you need to run it, exactly in the form and version you need. Like a parasite, it uses another machine's computational power to run its software, while being completely isolated from the mother organism save for CPU power. It is the perfect microcosm to nourish the beast which is SOLPS-ITER.

///error | Proper container definition
A container is a **virtual Operating System (OS)**. It is isolated from the host OS, but it **uses the host OS's kernel**, i.e. the guardian of the hardware components. It is a form of virtualization, but much leaner than an actual virtual machine. In case of Linux, the OS part (= the specific Linux distribution) is nothing more than bunch of system executables, libraries, and configurations in `/bin`, `/lib`, `/etc` and so on. Container is a process like any other, but it is started with a "different view" of the filesystem, where the root `/` directory points to the prepared container image, which can be based on an entirely different Linux distribution.
///

The IPP Prague in-house expert on SOLPS containers is Jan Hečko (<span class="material-symbols-outlined">mail</span> [hecko@ipp.cas.cz](mailto:hecko@ipp.cas.cz)), author of the package [SOLPS-container](https://repo.tok.ipp.cas.cz/solps/solps-container)<span class="material-symbols-outlined">open_in_new</span>.

///warning | Alternative sources
Our tutorials are just dumbed-down versions of the official [SOLPS-container](https://repo.tok.ipp.cas.cz/solps/solps-container)<span class="material-symbols-outlined">open_in_new</span> READMEs. **They are the primary, up-to-date reference material.**
///

There are two options of using Honza's SOLPS container:

- [Use a pre-compiled, read-only container](#use-a-pre-installed-read-only-container). This will free you of installing SOLPS-ITER, but it will also confine you to a list of specific versions. As of January 2026, this list includes 3.0.9 ("narrow grids" master), 3.1.1 (9-point-stencil) and 3.2.0-alpha (wide grids).
- [Compile your own container](#build-your-own-solps-container). This will give you more freedom of which SOLPS version to use and allow you to adjust your code, but it will open you up to possible compilation errors.


<a name="preinstalled-container"></a>

## Use a pre-installed, read-only container

/// danger | The following instructions are specific to IPP Prague ([Soroban](https://wiki.tok.ipp.cas.cz/index.php/Soroban_cluster)<span class="material-symbols-outlined">open_in_new</span> cluster)
For generic instructions, refer to [SOLPS-container](https://repo.tok.ipp.cas.cz/solps/solps-container)<span class="material-symbols-outlined">open_in_new</span> READMEs. Katka keeps these tutorials here because she isn't sure how to disentangle the generic and Soroban-specific details, and she has a hard time following the official documentation.
///

A read-only SOLPS installation is perfect if you want to get a quick start in using SOLPS and don't plan to tweak the source code. To check which SOLPS versions are available for usage on Soroban:

```bash
module load solps-container/  #now hit Tab!

solps-container/3.0.8                 solps-container/userdefined
solps-container/3.0.9                 solps-container/wg-3.2.0-alpha
solps-container/3.1.1
```

 As the read-only designation suggests, the entire `$SOLPSTOP` directory is immutable. This means your run data (mesh files and the `$SOLPSTOP/runs` folder) has to be stored elsewhere. By default, this is in your COMPASS home directory. More info [below](#features-of-a-solps-container).


### Get started with a read-only SOLPS container

1. Log into the Soroban front.

        ssh -X username@soroban.tok.ipp.cas.cz

2. In a Soroban node with available computational power (see [soroban:44444](http://soroban.tok.ipp.cas.cz:44444)<span class="material-symbols-outlined">open_in_new</span>), create an interactive QSUB job, so that you have your own computational space.

        qsub -IX -l select=1:host=soroban-node-03

    Launching the container from `soroban-front-01` will result in the `Illegal instruction` error, as detailed in the SOLPS-container [README](https://repo.tok.ipp.cas.cz/solps/solps-container)<span class="material-symbols-outlined">open_in_new</span>.

3. Choose a version of the write-only container.

        module load solps-container/3.0.9

4. Change the working directory to `/net`.

        cd /net

    This is so that this directory is mounted by the SOLPS container, providing you access to everything inside. For each node, the directory `/net/soroban-node-XX/scratch/$USER/live` is where your simulations, submitted with the QSUB script, will be actually run. Access to them will give you the option to run mid-simulation diagnostics (`2dt nesepm`) or to interrupt the simulation prematurely (`touch b2mn.exe.dir/.quit`).

5. Open a command line inside the container.

        solps_tcsh

    You are now inside a tiny Linux computer with SOLPS (and not much more) installed on it. You are in the `/opt/solps-iter` directory, where SOLPS-ITER is installed. The SOLPS-ITER work environment is activated (`tcsh` and `source setup.csh` have been run). You can use SOLPS commands and launch short simulations, but to launch longer simulations, switch to Soroban front and [use the job submission system](#submit-simulations-from-a-solps-container-with-qsub).


### Features of a SOLPS container

- Inside the container, your **COMPASS home directory is mounted** and ready to contain your runs. Go there and create a place for your SOLPS runs.

        cd /compass/home/$USER/
        mkdir solps_runs

    When you launch runs in the future, it will be from this directory. No worries, the container knows where its SOLPS is located, even if you aren't launching `b2run` from inside `$SOLPSTOP`.

    Storing your run data inside your home directory, as compared to the `/scratch` directory, has one advantage and one disadvantage. On the plus side, the run data is backed up regularly, so if you delete something by accident, it can be retrieved. On the minus side, access to the home directory while running SOLPS from the Docker container is *slow*, and it will slow your runs down. The `/scratch` directory is not backed up, but it is designed for fast access. A middle ground is trodden in Honza's [example QSUB script](https://repo.tok.ipp.cas.cz/solps/solps-container#bonus-step-4-example-of-qsub-script)<span class="material-symbols-outlined">open_in_new</span> for submitting simulations from the read-only SOLPS container, where at the start of the simulation the files are copied to `/scratch`, and at the end of it, they are copied back to your home directory.

- Inside the container, the **current working directory, where you launched the container from, is mounted** as well. You will find it under the same absolute path as in the Soroban node you launched the container from. This is handy when submitting simulations using Honza's [example QSUB script](https://repo.tok.ipp.cas.cz/solps/solps-container#bonus-step-4-example-of-qsub-script)<span class="material-symbols-outlined">open_in_new</span>, which copies the simulation into the Soroban node's `/scratch/$USER/live` directory. If you change the working directory prior to launching the container...

        qsub -IX -l select=1:host=a-random-free-soroban-node
        module load solps-container/3.0.9
        cd /net
        solps_tcsh

    ...then the directories `/net/soroban-node-XX/scratch/$USER/live`, where XX runs from 01 to 06, will also be accessible from inside the SOLPS work environment. (If you don't see them using the `ls` command, don't worry. Just `cd` into the node you want, and the symbolic link will be created on the fly.) This will enable you to use mid-simulation commands such as `2dt nesepm`, no matter which node the simulation is run on.

- When you create grids with **DivGeo, Carre and Triang**, by default the data is saved not inside the read-only SOLPS installation, but to your home directory. Check them out:

        cd /compass/home/$USER/.solps_container

- **LaTEX is not installed in the container**, because it's additional 5-10 GB. As a result, the manual is not compiled in the `$SOLPSTOP/docs/solps/` directory. Access the latest version of the manual at the [ITER Sharepoint](https://iterorganization.sharepoint.com/sites/SOLPS-ITER/Shared%20Documents/General/)<span class="material-symbols-outlined">open_in_new</span>.

- **If you work with a particular container a lot**, consider loading the module automatically by placing this line into the `.bashrc` file:

        module load solps-container/3.0.9  #or any other version you prefer

    If you're using a manually compiled SOLPS container, replace this with:

        module load solps-container/userdefined
        export SOLPS_CONTAINER=/path/to/your/container/


<a name="qsub"></a>

### Submit simulations from a SOLPS container with QSUB

This tutorial should work for both a read-only or a manually installed SOLPS container, but it has not been tested for the latter.

1. Log into the Soroban front.

        ssh -X username@soroban.tok.ipp.cas.cz

     This time, **stay at the Soroban front** and don't log into a particular node. Also, don't enter an interactive QSUB job, as you can't submit QSUB jobs from inside a QSUB job.

2. Load the appropriate container module.

        module load solps-container/3.0.9

3. Go to the `run` directory you would like to run.

        cd /compass/home/$USER/solps_runs/case/run

 4. Make sure the case is ready to run: choose the appropriate `b2fstati` and check the desired run length in `b2mn.dat` (using the elapsed real time `b2mndr_elapsed` is my personal favourite). The QSUB script will take can of `b2mn.prt`, setting up baserun EIRENE links and correcting time stamps (to make sure your [`b2fstati` isn't ignored](../supplementary/Common_pitfalls.md#the-danger-of-timestamps) in favour of flat profiles).

5. Launch a SOLPS simulation using a QSUB script.

        # Honza's example QSUB script
        qsub -N "short_job_name_without_spaces" -V $(which solps_qsub_soroban)

        # Your copy of this script, see below
        qsub -N "short_job_name_without_spaces" -V /path/to/script

    Honza's [example QSUB script](https://repo.tok.ipp.cas.cz/solps/solps-container#bonus-step-4-example-of-qsub-script)<span class="material-symbols-outlined">open_in_new</span> will launch the simulation on a free Soroban node, in the `long` queue, using 1 CPU (without MPI parallelisation). See [options of the QSUB script](#qsub_script_options). While the example script can be used out-of-the-box, I would still recommend that you [make your own copy](#make_your_own_qsub_script_copy).

6. Check that your job has been submitted with

        qstat -u $USER

    The number at the beginning of the line is the job ID number, used in manipulating the queue (e.g. while deleting a job, see [sorobansubmit](../my_first_simulation/Running_SOLPS-ITER.md#official-submission-scripts)). In a minute, you will also see the job at [soroban:44444](http://soroban.tok.ipp.cas.cz:44444)<span class="material-symbols-outlined">open_in_new</span>.



8. At the end of the simulation, the script will automatically perform `b2run b2uf` to generate an up-to-date `b2fplasmf` file.



<a name="simulation-progress"></a>

/// tip | Checking simulation progress
At the start of the simulation, Honza's script will copy the run folder to the appropriate Soroban node's `/scratch` directory. **Consequently, the run folder in your `home` is not updated as the simulation progresses.** To check on the simulation progress (`2dt nesepm` etc.), visit the directory:

    cd /net/soroban-node-XX/scratch/$USER/live/<jobid>/<scenario_name>/run_01

If such a directory does not exist within your SOLPS work environment, you did not follow the advice to launch `solps_tcsh` from `/net`. Exit the SOLPS work environment, switch the working directory here, and run `solps_tcsh` again.
///


<a name="qsub_script_options"></a>

**Options of the QSUB script** include:

- Launch the simulation with **MPI parallelisation** (here 8 cores):

        NPROC=8 qsub -V -l select=1:ncpus=8 -N "short_name" /path/to/script

- Launch the simulation on a **particular Soroban node**:

        qsub -V -l select=1:host=soroban-node-03 -N "short_name" /path/to/script

- Put the simulation into a different **queue** than `long`.

        qsub -V -q medium -N "short_name" /path/to/script

    This is useful if there are a lot of jobs queued and your simulation will be short (less than 24 hours for the `medium` queue). The available queues are `long`, `medium` and `batch`.

- These options can be combined. For example, `-l select=1:ncpus=8:host=soroban-node-03`.

<a name="make_your_own_qsub_script_copy"></a>

**Making your own copy of Honza's example QSUB script**:

1. Find the example script source code.

        which solps_qsub_soroban

2. Make a copy and save it somewhere you'll find it later.

3. Specify your email in the script header.

        #PBS -M hromasova@ipp.cas.cz

    This will make the PBS queue email you whenever a simulation concludes. When a simulation diverges and ends early, the email will notify you. It will also remind you which simulations you were running yesterday.

4. If you typically run simulation "until the next day", change the default queue to `medium`.

        #PBS -q medium


        


        


## Build your own SOLPS container

/// danger | The following instructions are specific to IPP Prague ([Soroban](https://wiki.tok.ipp.cas.cz/index.php/Soroban_cluster)<span class="material-symbols-outlined">open_in_new</span> cluster)
For generic instructions, refer to [SOLPS-container](https://repo.tok.ipp.cas.cz/solps/solps-container)<span class="material-symbols-outlined">open_in_new</span> READMEs. Katka keeps these tutorials here because she isn't sure how to disentangle the generic and Soroban-specific details, and she has a hard time following the official documentation.
///


This option is for those who need to adjust the SOLPS source code, or who need a particular version of SOLPS-ITER. It is more time-intensive than using a pre-compiled SOLPS container, but it allows the full flexibility of your own SOLPS installation while avoiding the library dependency problem. The only major difference from the read-only container is that you can keep your mesh and run files inside the SOLPS installation.

1. Log into the Soroban front.

        ssh -X username@soroban.tok.ipp.cas.cz if needed

2. In a somewhat free Soroban node (check [soroban:44444](http://soroban.tok.ipp.cas.cz:44444)<span class="material-symbols-outlined">open_in_new</span>), create an interactive QSUB job, so you have your own computational space. **Do not use `soroban-node-01`**.

        qsub -IX -l select=1:host=soroban-node-03

3. Load the general SOLPS-container module.

        module load solps-container/userdefined

4. Check which containers Honza has prepared.

        find $SOLPS_IMAGES
        # /ansys/fast/solps/solps_images/singularity/solps-iter@3.0.8.sif
        # /ansys/fast/solps/solps_images/singularity/solps-iter@3.1.0.sif
        # ...

5. Build a container in your directory of choice, for example `/scratch/$USER/solps-3.0.8-container`. Do not access another Soroban node through `/net`.

        singularity build --sandbox /scratch/jirakova/solps-3.0.8-container /ansys/fast/solps/solps_images/singularity/solps-iter@3.0.8-29-gf89a6a23.sif

    The process should take only a few minutes. If it's taking hours, you're probably writing to another Soroban node or the Soroban front.

6. Create a mount point for your home directory inside the container.

        mkdir -p /scratch/jirakova/solps-docker$HOME

    This will not only allow you to store your runs in your home directory (where they are backed up), but it will also link the SOLPS installation to `~/.ssh`, where your SSH keys are very probably located. This will allow you to use SOLPS Git without needing to punch in a username and password every time.

7. If you like, you can now move the entire container (here called `solps-3.0.8-container`) around. You can put it on another Soroban node. You can send it to the EUROfusion Gateway. The process will take a while, though; the entire pre-compiled SOLPS is pretty big. If you move the container outside Soroban, be aware that the module `solps-container/userdefined` and its handy commands such as `solps_tcsh` will become unavailable. In that case, refer to the original [SOLPS-container package](https://repo.tok.ipp.cas.cz/solps/solps-container)<span class="material-symbols-outlined">open_in_new</span> for instructions.

8. Tell the shell where to look for your SOLPS container.

        export SOLPS_CONTAINER=/scratch/jirakova/solps-3.0.8-container

9. Open the SOLPS-ITER work environment inside the container.

        solps_tcsh

    You are now inside a fully functional installation of SOLPS-ITER. Refer to the read-only container tutorials for instructions how to work with it.


### Switch to another SOLPS-ITER version

1. Log into the Soroban node where your SOLPS container is located and start an interactive QSUB job there.

        qsub -IX -l select=1:host=soroban-node-03

2. Load the SOLPS-container module and define the path to your container.

        module load solps-container/userdefined
        export SOLPS_CONTAINER=/path/to/container/

3. Open the SOLPS-ITER work environment.

        solps_tcsh

4. Tell Git to ignore the files `default_compiler` and `whereami`. Otherwise, they will cause conflicts in pulling a different SOLPS version.

        git checkout default_compiler whereami

5. Pull the desired SOLPS-ITER version using Git. To switch to the current **master** version:

        git checkout master
        git pull

    To switch to a **particular** version:

        git checkout release/3.1.1
        git pull
        git submodule update --init

6. Build up the correct files `default_compiler` and `whereami` again.

        /opt/fix_whereami.sh .

7. Exit the SOLPS-ITER work environment and enter it again. This will ensure the up-to-date `source.csh` is loaded.

        exit
        solps_tcsh

6. Compile SOLPS-ITER using the `make` command (`gmake`, which is everywhere in the manual, doesn't work here for some reason).

        make -j 8

    If you get LaTEX errors about special characters in German names, don't mind them. They will not prevent SOLPS or the manual from compiling. If the compilation fails at some point, exit the SOLPS-ITER work environment, enter it again, and continue the compilation.

