# Remote access

This document is concerned with connecting to and running SOLPS-ITER on remote servers. When one needs a lot of runtime (small time step, lots of impurities, parameter scans...) which cannot be provided by the home institute, one runs SOLPS on high-performance clusters instead. The question then arises how to shuffle SOLPS data around.

Topics covered here:

- [Basic techniques](#basic-techniques)
- [IPP Prague](#ipp-prague-compass-tokamak)
- [EUROfusion Gateway](#eurofusion-gateway)
- [IPP Garching](#ipp-garching-asdex-upgrade-tokamak)
- [Transferring SOLPS-ITER runs](#transferring-solps-iter-runs)


/// warning | Linux-centric
Linux is the default operating system of most plasma research institutes. If you are brave enough to use Windows or Mac OS to run SOLPS-ITER, you are also smart enough to translate the instructions to the language of your own environment.
///

/// tip | Funny story
In the year of our Lord 2020, Kateřina was convinced that the [SOLPSpy package](https://gitlab.aug.ipp.mpg.de/ipar/solpspy)<span class="material-symbols-outlined">open_in_new</span> (predecessor of today's [Quixote](https://ipar.gitlab.io/quixote/)<span class="material-symbols-outlined">open_in_new</span>) could not be run outside IPP Garching. Since SOLPS-ITER could not be installed on her native IPP Prague servers either, she ran SOLPS-ITER on the Marconi Gateway, copied the files to IPP Garching, loaded them into Python using SOLPSpy, exported them to a Python-readable file using her own code, copied that to IPP Prague, and finally checked if the code results agree with the COMPASS experimental data using different code.

This is how the *Remote access* document came to be.
///


## Basic techniques

After you set up a [VPN](#vpn-virtual-private-network), there are two main ways to connect to remote servers:

- [SSH](#ssh-secure-shell): fast, baggage-free, only command line
- [Remote desktop](#remote-desktop): possibly laggy, but full graphical desktop (e.g. for the [SOLPS GUI](https://static.iter.org/imas/assets/solps-iter/html/index.html)<span class="material-symbols-outlined">open_in_new</span>)

Which method you'll grow to prefer depends on how you interact with SOLPS-ITER. To start with, set them both up and see which one you like better. You may find yourself alternating between them depending on what you need to do.


### VPN (Virtual Private Network)

> "A virtual private network (VPN) is an overlay network that uses network virtualization to extend a private network across a public network, such as the Internet, via the use of encryption and tunneling protocols." [[Wikipedia]](https://en.wikipedia.org/wiki/Virtual_private_network)<span class="material-symbols-outlined">open_in_new</span>

A VPN is a way to pretend you are somewhere else. The fun way is to pretend you are in the USA to [watch American shows on Netflix](https://cyberinsider.com/vpn/best/netflix/us-american/)<span class="material-symbols-outlined">open_in_new</span>. The boring way is to pretend you are sitting at your workstation so you can access internal services of your institute, such as the intranet, wiki or the tokamak discharge database. **It is advisable to hide inside a VPN before you connect via [SSH](#ssh-secure-shell) or any other method.** In some cases (like on IPP Prague), SSH will not work before a VPN connection is established, which makes VPN the make-or-break point of remote access.

There are many softwares providing VPN services and each institute has its own favourite one. Instructions how to set up a VPN are given individually below.



### SSH (Secure SHell)

> "The Secure Shell Protocol (SSH Protocol) is a cryptographic network protocol for operating network services securely over an unsecured network." [[Wikipedia]](https://en.wikipedia.org/wiki/Secure_Shell)<span class="material-symbols-outlined">open_in_new</span>

You know how you can open a [terminal/command line](https://en.wikipedia.org/wiki/Command-line_interface)<span class="material-symbols-outlined">open_in_new</span> on your computer and command it to do all sorts of wild stuff? SSH lets you open a command line on a remote server. And then you can do all sorts of wild stuff *there*! Like run SOLPS-ITER!

To open a remote command line using SSH, open a command line at your home computer and run:

```bash
ssh -X username@remote.server.eu
```

To break down that command:

- `ssh` is a command to use the SSH protocol.
- `-X` is graphics forwarding. If the remote command line attempts to open a graphics window (e.g. draw a picture with `b2plot`), the same window will open on your local machine as well. It's useful to have `-X` on pretty much all the time.
- `username` is your username on the remote server, which was set up when you got your account there (together with a password).
- `remote.server.eu` is the remote server address. It usually begins with the server name (like `soroban-node-06`) and ends with some sort of internet address (like `tok.ipp.cas.cz`).

SSH is secure because you must prove it's you before it lets you put in any commands. Two methods of authentication are common:

- Username + password. After typing the `ssh` command above, you will be prompted to punch in the password. (You gave the username in the SSH command.)
- [SSH certificates](https://jadaptive.com/understanding-ssh-certificates-a-beginners-guide/)<span class="material-symbols-outlined">open_in_new</span>. You typically set those up when you get tired of typing your password again and again. SSH certificates come in pairs: a public key and a private key, both long sequences of letters and numbers. The public key you upload to the remote server, the private key you keep to yourself. When you initiate the SSH connection, the remote server takes a look if any of its public keys match your private keys. If a match is found, the remote server concludes it must be you and doesn't ask you for a password. Use Google and common sense to set up SSH certificate authentication.


### SSHFS (SSH FileSystem)

> "SSHFS (SSH Filesystem) is a filesystem client to mount and interact with directories and files located on a remote server or workstation over a normal ssh connection". [[Wikipedia]](https://en.wikipedia.org/wiki/SSHFS)<span class="material-symbols-outlined">open_in_new</span>

SSHFS lets you browse folders and files on a remote server like you would at your own computer. It's useful if you come from a Windows background and you can't get used to interacting with files through the [SSH](#ssh-secure-shell) command line.

To *mount* a remote filesystem to your computer:
```bash
sshfs username@remote.server.eu:/ /path/to/mount/point
```
If you want to avoid mounting a large amount of data (which may take a long time and cause lag), add a specific folder path after the `:`.

/// warning | Don't mount links
Before you mount a folder, check that it isn't a link. For example, `/solps-iter` may point to a long, obscure address where the system admins hid the actual SOLPS-ITER installation. To avoid problems, mount real directories and not links.
///

After your work is done, don't forget to *dismount*:
```bash
fusermount -u /path/to/mount/point
```
Details may vary, but when Kateřina forgets to dismount a remote folder and closes her laptop (causing it to go to sleep), it messes up her entire filesystem. The only solution then is to reboot the laptop.


### SCP (Secure Copy Protocol)

> "Secure copy protocol (SCP) is a means of securely transferring computer files between a local host and a remote host or between two remote hosts." [[Wikipedia]](https://en.wikipedia.org/wiki/Secure_copy_protocol)<span class="material-symbols-outlined">open_in_new</span>

SCP is like the copy command (Ctrl+C Ctrl+V), except between remote servers. It uses a one-time SSH connection, so authentication is the same as for [SSH](#ssh-secure-shell). For large files, it's much faster than mounting the remote folder using [SSHFS](#sshfs-ssh-filesystem) and copying "normally".

To copy a file from a local source to a remote destination:

```bash
scp /path/to/source_file.zip username@remote.server.eu:/path/to/target_file.zip
```

It works the same for remote source and local destination:

```bash
scp username@remote.server.eu:/path/to/source_file.zip /path/to/target_file.zip 
```


### Remote desktop

> "Remote desktop software is software for remote administration of computers, allowing a desktop environment to be displayed on a computer, known as the client, other than the one on which it is running − the server." [[Wikipedia]](https://en.wikipedia.org/wiki/Remote_desktop_software)<span class="material-symbols-outlined">open_in_new</span>

A remote desktop is a window straight to the desktop of a remote computer. If you maximize the window, you can pretend you're sitting in front of your work station (with some lagging and bad graphics).

There are many softwares for running remote desktops, and each server has a favourite one. Instructions how to set up remote desktops are given for each server individually, see below.





## IPP Prague (COMPASS tokamak)

/// danger | IPP Prague
This section is specific to IPP Prague, though it may contain elements applicable elsewhere.
///

/// hint | Which IPP?
There are two institutes of plasma physics in Central Europe:

1. The [Institute of Plasma Physics](https://www.ipp.cas.cz/)<span class="material-symbols-outlined">open_in_new</span> of the [Czech Academy of Sciences](https://www.avcr.cz/en/)<span class="material-symbols-outlined">open_in_new</span>, located in Prague, Czech Republic
2. The [Max Planck Institute for Plasma Physics](https://www.ipp.mpg.de/en)<span class="material-symbols-outlined">open_in_new</span> of the [Max Planck Society for the Advancement of Science](https://www.mpg.de/en)<span class="material-symbols-outlined">open_in_new</span>, located in Garching, Germany

Being neighbours, the Czechs and the Germans have cleverly decided to use the same abbreviation, IPP. Sadly (for the Czechs), the German IPP is bigger and has been running SOLPS longer. So if you hear someone asking "IPP? Which IPP?", rest assured, it's a Czech getting testy about being forgotten. Use "IPP Prague" and "IPP Garching" when in doubt that a jealous Czech may be present.
///

IPP Prague runs three major servers: [ltserv](https://wiki.tok.ipp.cas.cz/index.php/Category:Workstations)<span class="material-symbols-outlined">open_in_new</span>, [Soroban](https://wiki.tok.ipp.cas.cz/index.php/Soroban_cluster)<span class="material-symbols-outlined">open_in_new</span> and [Abacus](https://wiki.tok.ipp.cas.cz/index.php/Abacus_tutorial)<span class="material-symbols-outlined">open_in_new</span>. Ltserv (Linux Terminal SERVer) is suited for everyday use, such as viewing files or writing theses. Soroban and Abacus are powerful computing clusters suited for demanding scientific calculations, such as SOLPS-ITER simulations. At the time of writing (July 2026), Abacus is old and being phased out. Install and run SOLPS-ITER on Soroban only.

/// tip | Installing SOLPS-ITER on Soroban
Users are encouraged to use the pre-made [container installation](../installing/installing-in-container.md#preinstalled-container) of SOLPS-ITER on Soroban. From the legacy era, there is also a central installation (available to all users) of SOLPS 3.0.6 in `/net/soroban-front-01/scratch/solps/solps-iter` and a [Soroban installation tutorial](../installing/legacy-installing-at-compass-soroban.md). 
///

The Soroban cluster is divided into individual nodes `soroban-node-01`-`08` (visit [soroban:44444](http://soroban:44444/)<span class="material-symbols-outlined">open_in_new</span> in the [internal network](#vpn-connection-to-ipp-prague) to see them), which are covered by the Soroban front and overseen by the [QSUB](https://linuxcommandlibrary.com/man/qsub)<span class="material-symbols-outlined">open_in_new</span> queue manager. The Soroban front is an entry point, an entrance hall if you will, from which you enter individual nodes and carry out your simulations there. To navigate between the front and the nodes while using SOLPS-ITER, refer to [Running SOLPS-ITER using submission scripts](../my_first_simulation/Running_SOLPS-ITER.md#submission-scripts), [Submit simulations from a SOLPS container with QSUB](../installing/installing-in-container.md#qsub) and the instructions [below](#ssh-connection-to-ipp-prague).




### SSH connection to IPP Prague

To open a command line on the **Soroban front** using [SSH](#ssh-secure-shell):
```bash
ssh -X username@soroban.tok.ipp.cas.cz
```
The `soroban` part may be replaced by `ltserv`, `abacus`, `soroban-node-01` etc. If you are in the [internal IPP network](#vpn-connection-to-ipp-prague), you may leave out the `tok.ipp.cas.cz` part.

To run SOLPS-ITER at IPP Prague via SSH:

1. Log into the Soroban front and ask for some computational power from the resource management system.

        ssh -X username@soroban
        qsub -IX

    The `-I` means you are starting an interactive session. The `-X` means, as usual, that Matplotlib plots and similar graphics are going to be tunneled to your screen. In an interactive session, it is assumed you are mostly going to mess around, make cheap simulations with `b2run` and look at the results. If you want to submit longer or more numerous simulations, use [`sorobansubmit`](../my_first_simulation/Running_SOLPS-ITER.md#official-submission-scripts) instead and don't bother initiating `qsub -I`.

2. Go to the SOLPS-ITER installation directory you wish to use:

        cd /net/soroban-node-06/scratch/jirakova/solps/solps-iter

3. Activate the [SOLPS-ITER work environment](../installing/solps-iter-codebase.md#how-to-initiate-the-solps-iter-work-environment).

To mount the COMPASS servers on your computer using [SSHFS](#sshfs-ssh-filesystem):
```bash
sshfs username@soroban.tok.ipp.cas.cz:/ /path/to/mount/point
```
The contents of individual Soroban nodes can be access through the `/net` directory. If you don't see a link to your node, simply access it as if it existed
```bash
cd /net/soroban-node-06
```
and a persistent link will be created automatically.



### VPN connection to IPP Prague

/// warning | The first step of this tutorial must be done from inside IPP Prague
If you don't have a working VPN, you can't use [SSH](#ssh-secure-shell) nor [SSHFS](#sshfs-ssh-filesystem), so you can't get to the VPN certificates on the IPP Prague servers. If you're at home on the weekend looking into setting up a VPN connection for the first time, you are screwed. Kick back and [read](https://onlinelibrary.wiley.com/doi/abs/10.1002/ctpp.200610001)<span class="material-symbols-outlined">open_in_new</span> [some](https://www.sciencedirect.com/science/article/pii/S0022311514006965)<span class="material-symbols-outlined">open_in_new</span> [articles](https://www.sciencedirect.com/science/article/pii/S2352179121000788)<span class="material-symbols-outlined">open_in_new</span>.
///

To set up a VPN connection, you need the certificates located in the folder `/compass/home/username/Public`. There should be a file called `username.tar.gz`. Copy it to your local device and extract the files to some location where you will find them easily (and will not delete them by accident). Then either decrypt the [VPN setup tutorial](https://wiki.tok.ipp.cas.cz/index.php/Openvpn)<span class="material-symbols-outlined">open_in_new</span> on the COMPASS wiki or, on Linux, do the following:

1. Check your version of OpenVPN.

           openvpn --version

    If the version is above 2.4.4 and the OpenSSL version is above 1.0.2m, you're good to go.

2.  Create a text file and copy-paste the preferred VPN configuration from the [tutorial](https://wiki.tok.ipp.cas.cz/index.php/Openvpn)<span class="material-symbols-outlined">open_in_new</span>. It's headed `This is the preferred configuration, using UDP protocol and OpenVPN registered port 1194/udp`.
3. Replace **both** occurences of `{{your_name}}` in the VPN configuration file with your username.
3. To increase the maximum connection time to 10 hours, add this line to the VPN configuration file:

        reneg-sec 36000

3.  Open the Network Manager (**right**-click the Connections icon on the right of your control panel, choose `Edit connections`) and add a VPN connection. Choose to import the settings from a file. Choose the text file you've just created.
4.  Call the VPN whatever you like.
5.  As the username and password, write your LDAP username and password. Next to the password you've typed, there is a little icon of a person. Click it and choose saving the password for all users.

To connect to the VPN, **left**-click the Connections icon on the right of your control panel and find VPN connections. You will know that your VPN is working when:

1. You can access the [IPP Prague intranet](http://intranet.ipp.cas.cz/)<span class="material-symbols-outlined">open_in_new</span>.
2. You can use SSH and SSHFS.
3. Your internet works like usual.

The VPN won't allow you to access subscription-based journal articles, such as those on IoP Science, but you can still log in via Shibboleth with your VERSO credentials. If that doesn't work, there's always [SciHub](https://sci-hub.st/)<span class="material-symbols-outlined">open_in_new</span>.

/// hint | VPN problems come as surely as the tide
Katka reconfigures her VPN connection every six months, because it stops working when she looks away for too long. The latest problem was connected with the [maximum packet size](https://www.thegeekpub.com/271035/openvpn-mtu-finding-the-correct-settings/)<span class="material-symbols-outlined">open_in_new</span>. Switching from the UDP protocol to the TCP protocol made the VPN work, using this line in the VPN configuration file:
```
proto tcp    # previously: proto udp
```
The TCP protocol was, however, slow as hell (as the COMPASS wiki [VPN tutorial](https://wiki.tok.ipp.cas.cz/index.php/Openvpn)<span class="material-symbols-outlined">open_in_new</span> warns). What fixed it was decreasing the maximum packet size to 1400 bytes using this line in the VPN configuration file:
```
tun-mtu 1400
```
///


### Remote desktop on IPP Prague

The [X2Go](https://wiki.x2go.org/doku.php)<span class="material-symbols-outlined">open_in_new</span> software allows you to open a remote desktop of your IPP Prague workspace, emulating work on a workstation in slightly worse graphics quality. To set up X2Go, follow the [COMPASS wiki tutorial](https://wiki.tok.ipp.cas.cz/index.php/X2Go)<span class="material-symbols-outlined">open_in_new</span>.




## EUROfusion Gateway

/// danger | EUROfusion Gateway
This section is specific to the EUROfusion Gateway, though it may contain elements applicable elsewhere.
///

[EUROfusion Gateway](https://docs.hpc.cineca.it/specific_users/gateway.html)<span class="material-symbols-outlined">open_in_new</span> (EFGW) is a high-performance computing cluster hosted by HPC-CINECA in Italy. Before 2025, it was known among SOLPS users as the Marconi Gateway, Gateway, Marconi or ITM. It is an accessible platform to run SOLPS, although it has chronic problems with its installation and support.

/// tip | Tip
Use [Docker containers](../installing/installing-in-container.md) to bypass installing SOLPS-ITER at the EUROfusion Gateway.
///

### Initial setup

To access EFGW, you need two independent accounts, registered under the same e-mail address.

1. Account at the [CINECA UserDB portal](https://docs.hpc.cineca.it/general/users_account.html#userdb)<span class="material-symbols-outlined">open_in_new</span>. This serves for CINECA to verify your identity and affiliation, down to a scan of your personal ID and the brand of jeans you're currently wearing.

2. [HPC-CINECA project account](https://docs.hpc.cineca.it/general/users_account.html#project-accounts)<span class="material-symbols-outlined">open_in_new</span>. This serves to track your allocated computing resources and the projects (like "SOLPS modelling") you're working on.

If you had access to the Marconi Gateway before its rebranding, you already have an HPC-CINECA project account. If you want to keep using EFGW, you must register a UserDB account as well.

**Instructions and links**:

- [HPC-CINECA documentation](https://docs.hpc.cineca.it/general/getting_started.html)<span class="material-symbols-outlined">open_in_new</span> is a general, detailed guide to accessing CINECA clusters (Leonardo, G100, Piragora...). Don't be discouraged that you don't see EFGW anywhere; it's listed in the section *Specific users - EUROfusion*.
- [EFGW-specific documentation](https://docs.hpc.cineca.it/specific_users/gateway.html)<span class="material-symbols-outlined">open_in_new</span> amends the general tutorials with EFGW-specific information. Mostly it's "replace `leonardo` with `efgw` in the command".
- [UserDB portal](https://userdb.hpc.cineca.it/)<span class="material-symbols-outlined">open_in_new</span> is where you log in using your UserDB credentials.
- [CINECA keycloak](https://sso.hpc.cineca.it/realms/EFGW/account/#/)<span class="material-symbols-outlined">open_in_new</span> is where you log in using your HPC-CINECA project account credentials.
- [FAQ](https://docs.hpc.cineca.it/faq.html)<span class="material-symbols-outlined">open_in_new</span> contain, among others, a solution to the `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` error message. It doesn't work for me, sadly.


### Connection to EFGW

HPC-CINECA has strict security, so you can't simply log in with a username and password. You must use SSH certificates, which are valid only for 12 hours, so you have to re-generate one every day using 2-factor authentication with your smartphone. Additionally, there is a fingerprint issue described below which I wasn't able to fix despite attentive tech support. It isn't a showstopper, but it's annoying.

Prior to the day's first connection to EFGW, **re-generate an SSH certificate** with the Smallstep client:

```bash
step ssh login 'username' --provisioner efgw
```

**SSH in the command line**: Official directions are:
```bash
ssh -X username@login.eufus.eu
```
`login.eufus.eu` is a front-end, from which you will be redirected to one of the login nodes (`vizXX-ext.efgw.cineca.it` where `XX` runs from `05` to `08`) depending on which is the least busy. However, this command only works the first time. After you add the `login.eufus.eu` fingerprint among your known hosts, next time you log in, you'll get the error `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`. Despite being specifically treated in the FAQ, I haven't been able to fix this. I propose two workarounds:

1. Connect to a specific node each time.
    ```bash
    ssh -X username@viz05-ext.efgw.cineca.it
    ```
2. Remove `login.eufus.eu` from the list of known hosts prior to every login.
    ```bash
    ssh-keygen -f '~/.ssh/known_hosts' -R 'login.eufus.eu'
    ```

**[NoMachine](https://www.nomachine.com/)<span class="material-symbols-outlined">open_in_new</span> virtual desktop**: Follow [CINECA's setup instructions](https://docs.hpc.cineca.it/specific_users/gateway.html#how-to-access-efgw-with-nx)<span class="material-symbols-outlined">open_in_new</span>. You may have to upgrade to the latest version of NoMachine. When it works, accessing EFGW through virtual desktops is super fast and convenient.


## IPP Garching (ASDEX Upgrade tokamak)

/// danger | IPP Garching
This section is specific to the IPP Garching, though it may contain elements applicable elsewhere.

<span class="material-symbols-outlined">construction</span>**TODO**: Update this section (it was last used in 2021).
///

IPP Garching has a [number of clusters](https://wiki.mpcdf.mpg.de/ipphpc/index.php/Available_computing_systems)<span class="material-symbols-outlined">open_in_new</span>, and not all were born equal. According to their [cluster guidelines](https://wiki.mpcdf.mpg.de/ipphpc/index.php/Cluster-Guidelines)<span class="material-symbols-outlined">open_in_new</span>, to process the SOLPS-ITER output the [TOK-I](https://wiki.mpcdf.mpg.de/ipphpc/index.php/TOK-I_cluster_in_Garching)<span class="material-symbols-outlined">open_in_new</span> cluster is the go-to option.

Note that your home folder has limited disk space (50 GB), which means you can't copy SOLPS-ITER runs there. As described [here](https://tok.ipp.mpg.de/wiki/TOK/index.php/Computing-TOKS)<span class="material-symbols-outlined">open_in_new</span>, an ideal place for SOLPS-ITER runs is the `/toks/scratch/username`.

First of all, you need access to the **IPP Garching intranet**. If you have visited AUG, you may already have an account there. If not, write to Marion Berger (<span class="material-symbols-outlined">mail</span> [sekmst@ipp.mpg.de](mailto:sekmst@ipp.mpg.de)), the MST secretary at AUG and ask her to confirm your request for a "real" user ID at the AUG computer system. You can submit the request [here](https://www.mpcdf.mpg.de/secure/registrieren/antrag.php?deisa=0&inst=IPP&projekt=MST-AUG&lang=en)<span class="material-symbols-outlined">open_in_new</span>. Fill in "Marion Berger" as your supervisor/project manager. (I'm assuming that if you're working with SOLPS, you are part of MST1.)

Login rights to the [**TOK clusters**](https://tok.ipp.mpg.de/wiki/TOK/index.php/Computing-LinuxClusters)<span class="material-symbols-outlined">open_in_new</span> (TOK-I, TOK-S, TOK-P... ) usually don't come automatically with intranet access. To get access, write to David Coster (<span class="material-symbols-outlined">mail</span> [David.Coster@ipp.mpg.de](mailto:David.Coster@ipp.mpg.de)).

### SSH connection to IPP Garching

All you need in this case is a command line. To log into the Solaris environment:
```bash
ssh -X username@sxbl16.aug.ipp.mpg.de
```
This is the environment you access when you log into a work station at AUG. According to Lisa Sytova, the only thing the Solaris environment is good for is `cview`, a programmed for viewing experimental data. However, to run Python, it's much better to switch into the Linux shell in one of the TOK clusters:
```bash
rlogin tok01
```
Alternatively, if you don't need the Solaris roundabout, you can log in directly to the TOK-I cluster:
```bash
ssh -X username@tok01.bc.rzg.mpg.de
```
If you want to access the files directly from your machine, you can also mount the file system:
```bash
sshfs -o transform_symlinks username@toki01.bc.rzg.mpg.de:/ '/path/to/mount/point'
```

### VPN connection to IPP Garching

1. Go to the [AUG computer network webpage](https://www.mpcdf.mpg.de/services/campus/vpn)<span class="material-symbols-outlined">open_in_new</span> and follow the instructions. To install the downloaded `.sh` file on Linux:

        cd /path/to/the/sh/file
        chmod +x anyconnect-linux64-4.7.03052-core-vpn-webdeploy-k9.sh
        sudo ./anyconnect-linux64-4.7.03052-core-vpn-webdeploy-k9.sh

2.  Run Cisco AnyConnect on your machine. Enter `vpn.mpcdf.mpg.de` as the server and your AUG intranet login. Click Connect. (It will ask for your password on every startup. I haven't yet found a way to make it remember me.)


### Remote desktop on IPP Garching

You have two options: one that is great (or "adequate" depending on your standards) and one that sucks (by all standards). The first one the [ThinLinc Client](https://www.aug.ipp.mpg.de/foswiki/bin/view/AUG/ThinLincClients)<span class="material-symbols-outlined">open_in_new</span>, the other is the [Oracle Virtual Desktop](https://www.aug.ipp.mpg.de/wwwaug/documentation/computerIT/Downloads.html)<span class="material-symbols-outlined">open_in_new</span>. Both of these links are exhaustive installation tutorials. In the case of the ThinLinc Client though, just be careful to download the ThinLinc *client* and not the *server*. In my case the client didn't show up among installed applications right away, so I ran it from the command line:
```bash
tlclient
```
There are many reasons why the Oracle Virtual Desktop sucks. It doggedly thinks that your keyboard has the weird layout used in AUG work stations. It doesn't support copy-paste between the remote desktop and your own desktop. It has Solaris, which is ugly. All in all, the only reason I write about it here is that it is an option.

Note, again, that to connect to the remote desktop, you need to have an active [VPN connection](#vpn-connection-to-ipp-garching) first.




## Transferring SOLPS-ITER runs

This section details how to transfer SOLPS data on several levels: inside a case, inside a SOLPS installation, between SOLPS installations, and between remote servers.

/// hint | Built-in `transfer_solps-iter_runs`
There is a built-in SOLPS-ITER command `transfer_solps-iter_runs`, but it requires the `sshpass` command, which isn't pre-installed on Gateway nor on Soroban. Installing it requires either superuser rights (which you might not have), or bugging the IT department (which you might want to avoid). As a result, Kateřina has never used it.
///

To clear up the terminology:

- A **server** refers to a computer cluster with a common file system. Examples of servers are Soroban at IPP Prague, Karolína at IT4I, or Gateway at Marconi Fusion.

- A **SOLPS installation** is a directory where the SOLPS-ITER source code has been cloned and compiled. Several independent SOLPS installations may coexist on a single server (e.g. different versions of SOLPS), each with a separate work environment. Within this work environment, the top directory is called `$SOLPSTOP`.

- A **case** is a directory located in `$SOLPSTOP/runs/`, containing a `baserun` directory and probably a few directories called `run`, `run2`, `diverged_run_wtf` or `cflme_0.3_cflmi_0.2`. The individual runs share computational grid specified in the baserun.

- A **run** is a specific SOLPS-ITER simulation, with its own boundary conditions, plasma solution, `run.log` etc.


### Copy a run inside the same case

Make a copy with the `cp` command.

```bash
cp -r run new_run
```

### Transfer the plasma solution from one case to another

If both the cases have the **same B2.5 cell count**, copy the converged `b2fstate` as the new `b2fstati`.

```bash
cp case1/run/b2fstate case2/run/b2fstati
```

This does not transfer the entire solution, but it does capture its essential part. Use this, for instance, to supply a new case with some starting realistic plasma profiles instead of the default flat profiles solution. Even if the simulation is completely different, this will reduce the time to convergence.

This can also be done when `case2` contains additional ion species, such as sputtered carbon. SOLPS will take the existing solution (background deuterium plasma) and start up the remaining species from the flat profiles solution.

The plasma solution can also be transferred among different SOLPS-ITER installations, given that the version is not too dissimilar. Use the [`scp`](#scp-secure-copy-protocol) command to transfer the `b2fstate` file among different servers. In both cases, it is required that the target case already built up (e.g. ready for running save for an initial plasma state) and has the same B2.5 cell count. (This is a compelling reason why, in the absence of grid issues, you should build all your simulations with the same number of cells.)

If the two cases have **different B2.5 cell count** (for instance when running the same simulation on a finer grid), use the `b2yt` command. Refer to section 3.14 of the manual for instructions; I've never used it.


### Transfer an entire case from one SOLPS installation to another

This is more complicated, as SOLPS-ITER doesn't store all the case-relevant files within the case directory. Files needed by B2.5 may be located in `$SOLPSTOP/modules/Carre/`, files needed by EIRENE may be located in `$SOLPSTOP/modules/Triang/` and so on. Jan Hečko has developed the following tutorial.

**Transfer the SOLPS-ITER files**:

1. Download the script [baserun2archive.py](../img/baserun2archive.py)<span class="material-symbols-outlined">download</span> to the server where your original simulation was performed.

2. Open a terminal on the origin server and run the script:

        cd /download/path
        python3 ./baserun2archive.py /solps/installation/path/runs/case/baserun baserun.tar.gz

3. Copy the archived `baserun` to the target server.

        scp baserun.tar.gz user@target-server.com:/solps/installation/path/runs/

4. At the origin server, go to the case directory and archive the `run` directory of your choice.

        cd  /solps/installation/path/runs/case/
        tar -czvf run.tar.gz run

5. Copy the archived `run` to the target server.

        scp run.tar.gz user@target-server.com:/solps/installation/path/runs/


**Set up a new SOLPS-ITER case**:

6. Switch to the target server command line.

        ssh -X user@target-server.com

7. Initiate the SOLPS work environment.

        cd /solps/installation/path
        tcsh
        source setup.csh
        setenv DEVICE compass #or your machine of choice

8. Create a new case directory and move both the archives there.

        cd runs
        mkdir transferred_case
        mv baserun.tar.gz transferred_case/baserun.tar.gz
        mv run.tar.gz transferred_case/run.tar.gz

9. Extract both the archives.

        cd transferred_case
        tar -xvf baserun.tar.gz
        tar -xvf run.tar.gz


**Prepare the simulation for running:**

10. Link up the DivGeo file (the file in baserun ending with `.dg`) and EIRENE links in `baserun`.

        cd baserun
        lns <DivGeo_file_name_without_the_.dg_extension>
        setup_baserun_eirene_links

11. Correct the `baserun` time stamps.

        cd ..
        correct_baserun_timestamps

12. Set up EIRENE links to `baserun` from `run`.

        cd run
        setup_baserun_eirene_links

**Run the simulation:**

13. Correct the `run` time stamps.

        correct_b2yt_timestamps

13. Perform a dry run and check which routines would be called.

        # Restart the simulation
        rm b2mn.prt
        cp b2fstate b2fstati

        # Perform a dry run
        b2run -n b2mn | grep -oE 'b2[a-z]+.exe' | uniq

    If `b2ai` (initial plasma solution) is among the lines, watch out, the simulation is about to ignore your `b2fstati` and start from the flat profiles solution. Check if all the necessary files are present and run `correct_b2yt_timestamps` in the `run` directory again.

14. Set the simulation time (`'b2mndr_elapsed'`) in `b2mn.dat` to 60 seconds and restart the simulation.

        b2run b2mn > & run.log &

15. Wait and check the results.

        # Plot residuals of the continuity equation for all ion species
        resco

        # Plot time evolution of the outer midplane electron density
        2dt nesepm

    If everything works, you have successfully transferred your simulation.



### Copying runs with `rsync`


If you don't intend to *run* the simulation on the target server, you can use the `rsync` command to simply transfer the files:
```
rsync -hivaz username1@source.com:/path/to/case username2@destination.com:/path/to_case
```
This will synchronise all of the runs going from the last modification date, so it won't copy old untouched runs over and over again. This will, however, not allow you to relaunch the simulation if you ever need it.


### Transferring a SOLPS-ITER run using `b2yt`

`b2yt` is useful in the following situations:

- You have a converged run and want to increase the grid resolution.
- You want to build a new case whose geometry is similar but not the same as a previously converged run, and you don't want to wait until the "flat profiles" solution converges.
- You want to check if the converged result is the same between two SOLPS version (4.3, 5, another release of SOLPS-ITER...).

The following materials concern `b2yt`:

- [SOLPS manual](../supplementary/SOLPS-ITER_user_wisdom.md#rtfm), section 3.14 *b2yt, changing from one grid size and species set to another*. Pretty informative in the large picture, but doesn't provide step-by-step instructions.
- ITER Organisation: [Converting or resizing a case: b2yt](https://user.iter.org/?uid=R7T2P2)<span class="material-symbols-outlined">open_in_new</span>. Describes a few steps in greater detail, but doesn't give the whole process either.
- [Conversion tutorial](https://iterorganization.sharepoint.com/:w:/r/sites/SOLPS-ITER/Shared%20Documents/General/SOLPS-ITER/US_GA_Workshop/SOLPS_Conversion_tutorial.docx?d=w9af0422060384998ab872bc47a3e9226&csf=1&web=1&e=S1ATX3)<span class="material-symbols-outlined">open_in_new</span>
