# Contribute

SOLPS Tutorials is an open, collaborative project between SOLPS-ITER users. Contributions are warmly welcome, whether they be individual fixes, tutorial expansions or entirely new tutorials.

To clone the [`SOLPS-Tutorials` repository](https://github.com/iterorganization/SOLPS-Tutorials)<span class="material-symbols-outlined">open_in_new</span> to your local machine:

    cd /new/home/for/solps/documentation
    git clone git@github.com:iterorganization/SOLPS-Tutorials.git

/// hint | Basic Git knowledge is required
Learn more in [Introduction to Git](installing/solps-iter-codebase.md#introduction-to-git),
[Git workflow for dummies](https://docs.google.com/presentation/d/1wFOoQAADQA7c4HcRa3vST2iAq2a4faZs461T9hgz9Ek/edit?slide=id.p#slide=id.p)<span class="material-symbols-outlined">open_in_new</span>,
[CodeRefinery Git intro](https://coderefinery.github.io/git-intro/)<span class="material-symbols-outlined">open_in_new</span> or
[Contributing to Django](https://docs.djangoproject.com/en/dev/internals/contributing/)<span class="material-symbols-outlined">open_in_new</span>.
///


## Technical information

Our tutorials are written in [Markdown](https://www.markdownguide.org/cheat-sheet/)<span class="material-symbols-outlined">open_in_new</span> and rendered as web pages with [MkDocs](https://www.mkdocs.org/)<span class="material-symbols-outlined">open_in_new</span>. The [`SOLPS-Tutorials` repository](https://github.com/iterorganization/SOLPS-Tutorials)<span class="material-symbols-outlined">open_in_new</span> on GitHub is owned by the ITER Organisation. Their [website](https://solps-tutorials.readthedocs.io/)<span class="material-symbols-outlined">open_in_new</span> is hosted by [ReadtheDocs](https://about.readthedocs.com/)<span class="material-symbols-outlined">open_in_new</span>.

**Repository structure**:

- `docs`: Markdown tutorials and their figures and files
    - `feature_blog`: tutorials introducing advanced SOLPS features
    - `files`: non-image files, mostly PDFs
    - `img`: pictures used to illustrate the tutorials
    - `installing`: tutorials on installing SOLPS
    - `my_first_simulation`: tutorials taking a beginner through their first SOLPS simulation
    - `supplementary`: tutorials covering everything around SOLPS
    - `css`, `javascript` (technical stuff)
- `extras`: additional content generated without MkDocs, most importantly the B2.5 switch documentation
- `mkdocs.yml`: controls of the navigation bar on the left
- `README.md`: basic information about `SOLPS-Tutorials`
- `.gitignore`, `.gitlab-ci.yml`, `requirements.txt` (technical stuff)



## Contribution guidelines

- **Respect the existing documentation structure.** Before you write a tutorial, figure out if an equivalent is already present, and amend that if necessary.
    - *My first SOLPS-ITER simulation*: A beginner's first contact with SOLPS-ITER, step-by-step instructions toward creating one's first SOLPS-ITER simulation with the narrow grids version. Keep it simple. Document frequently encountered problems, but don't explain anything in depth. If needed, describe the issue at length elsewhere (e.g. in [Common pitfalls](supplementary/Common_pitfalls.md)) and link to it.
    - *Feature blog*: Largely independent ways to make a SOLPS simulation more complicated. Explain why one would want to adopt a particular feature, what are the benefits and costs, and how to do it. You can go into detail, but don't paraphrase or copy-paste existing documentation. Link to it instead.
    - *Supplementary material*: Everything that didn't fit in the first two categories. 

- **Do not duplicate.** If something is explained elsewhere (SOLPS manual, ITER SharePoint...) and you find yourself paraphrasing it or, God forbid, copy-pasting it, link to it instead.

- **Kateřina's three postulates for writing SOLPS Tutorials:**
    1. You will forget everything you don't write down.
    2. You can't keep any notes other than SOLPS Tutorials.
    3. Someone else will read SOLPS Tutorials.

- Use [admonitions](#markdown-extensions) (colour boxes) for information outside the main tutorial flow.

- Use [in-text icons](#icons) for external links, downloadable files, email addresses and "under construction" warnings.

- Keep lists short. (They turn up as long paragraphs in the search bar, clogging the output. This list is borderline.)

- All the `.md` files have to be accessible from the navigation sidebar. Put new files into `mkdocs.yml`.

- Use the [mother tongue](https://serendipstudio.org/sci_cult/leguin/)<span class="material-symbols-outlined">open_in_new</span>. Read the instructions aloud and see if they flow off the tongue or make you choke. Write as if you were explaining it to a confused student. Sounding too familiar is better than sounding too stiff.



## How to publish your contribution

First, clean your local copy of SOLPS Tutorials.

    cd SOLPS-Tutorials
    git fetch
    git status
    
If you see you're up-to-date with `master`, you're good to go. If you are on `master` but you're missing the last updates, download them to your local copy.

    git pull

Usually I find myself a different, long-forgotten branch, from the last time I was contributing commits and forgot to switch back to `master`. Usually there are modified files as well. In such a case, it's easiest to make a new local copy of the repository and merge your changes into it. Rename your old local copy (I go with `SOLPS-Tutorials_definitely_not`) and clone another, fresh copy:

    cd ..
    git clone git@github.com:iterorganization/SOLPS-Tutorials.git

Then proceed according to the instructions below. At the point where you're supposed to start writing your contributions, copy over the files from your old folder `SOLPS-Tutorials_definitely_not`. More on that below.
    
Once you are on the latest update of the `master` branch, your work table is clean. You can start on your latest contribution.
    
1. Visit the [list of `SOLPS-Tutorials` branches](https://github.com/iterorganization/SOLPS-Tutorials/branches)<span class="material-symbols-outlined">open_in_new</span> on its GitHub page. On the upper right, click `New branch`. Select `master` as the source. Name the branch using the [common conventions](https://medium.com/@abhay.pixolo/naming-conventions-for-git-branches-a-cheatsheet-8549feca2534)<span class="material-symbols-outlined">open_in_new</span>, using branch prefixes such as `feature/`, `fix/` or `refactor/`.

2. Switch to the new branch on your local machine.

        git fetch  # this downloads the information that there is a new remote branch
        git checkout -b feature/my_new_branch origin/feature/my_new_branch
    
    The `-b` will create your own local branch which tracks the remote branch. It prevents the detached HEAD state.

3. If you have any accumulated past changes, integrate them. Simply copy all the contents of `SOLPS-Tutorials_definitely_not` and paste them into your new shiny `SOLPS-Tutorials`. **Immediately** after that, resolve conflicts/deletions. The `Source Control` tab in our editor of choice, [Visual Studio Code](#recommended-editors), works well. Compare your old files with the newest `master`, get familiar with what has been done while you were sleeping and modify your past contributions accordingly. Use the `Revert` button/option to undo your "deletions". You don't want to overwrite any work others have done in the meantime. I know you're impatient to get started on the actual work, but if you postpone dealing with the conflicts, they will become a headache. You'll invest effort into rewriting documentation that's out-of-date. At the end of it, when you're making your commits and merging into `master`, you will have to deal with the conflicts anyway. And it will be harder, because you've *just* polished your contribution, you want to send it out there already, and now not only you are bogged down by Git conflicts, but you also have to rewrite your contribution to accommodate the work of others.

    - (Note: Kateřina is getting so deep into this because she's lazy. She hopes stern, detailed instructions will make Git conflicts more bearable in the long-term.)

4. Write your contribution. We recommend the [Visual Studio Code](#recommended-editors) as editor. Make generous use of Markdown [extensions](#markdown-extensions) and [icons](#icons) where appropriate.

5. When it's time to publish your contributions, go through the changes, stage them into logical units and commit them with informative commit messages. The `Source Control` tab in [Visual Studio Code](#recommended-editors) is more convenient than doing this in the command line.

    Basic commit guidelines:

    - It's preferable to make a large number of atomic commits ("Change recommended gas puff value", "Add section on lowering grid resolution") as opposed to one all-encompassing commit ("I'm done for today", "There were so many typos oh my God").
    - Commit messages should be so informative that you don't need to check the commit line by line to know what it did.
    - Individual commits should form logical wholes. If you aren't done yet (you're in the middle of rewriting an entire section), don't commit it yet.
    - For commit message wording, refer to [How to write better Git commit messages](https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/)<span class="material-symbols-outlined">open_in_new</span>.

6. Once you have a series of commits, ideally acknowledging all the changes you've made to the tutorials, upload them to the central GitLab repository.

        git push
    
    (You can also do this in Visual Studio Code `Source Control` tab.)

7. On the [`SOLPS-Tutorials` GitHub page](https://github.com/iterorganization/SOLPS-Tutorials/pulls)<span class="material-symbols-outlined">open_in_new</span>, create a new pull request which merges your new branch back into `master`. Add Katka as a reviewer so she can check the changes and give you a deserved pat on the back. Expect a response within 3 days.

8. Switch to the `master` branch on your local machine. (I always forget about this step.)

        git checkout master
        git pull
    
    Thank you for contributing to SOLPS Tutorials!



## Recommended editors

SOLPS Tutorials are written in [Markdown](https://www.markdownguide.org/)<span class="material-symbols-outlined">open_in_new</span>, which is little more than plain text with a few basic formatting marks. Any text editor suffices to edit the tutorials. However, to edit **and display the rendered results** (like seeing actual bullet points instead of `-`), we recommend [Visual Studio Code](https://code.visualstudio.com/)<span class="material-symbols-outlined">open_in_new</span>, which includes a Markdown preview out-of-the-box. To display the rendered results, click on the icon with the page and magnifying glass in the top right corner of the editor.

Note that some of the fancier extension features (such as "external link" icons) will not be displayed properly by VC Code. To preview how the rendered page will look on the SOLPS Tutorials web, [install MkDocs locally](#render-solps-tutorials-locally-with-mkdocs).


## Markdown extensions

To make the SOLPS Tutorials easier to read, we use extensions of the Markdown syntax, such as boxes with useful tips. Consider using them to break up the text flow and mark up notes and details. They are implemented using [Python Markdown Extensions](https://facelessuser.github.io/pymdown-extensions/)<span class="material-symbols-outlined">open_in_new</span>, which are are pre-installed in MkDocs as a Python package. Use

```bash
pip install --upgrade pymdown-extensions
```

to get the most recent version. Note that the extensions won't be displayed properly in a pure-Markdown preview in VS Code. You need to [build the MkDocs locally](#render-solps-tutorials-locally-with-mkdocs) or let it be built in a CI pipeline to see the final result.

The setup of Markdown extensions is easy. Just make sure the specific extension is enabled in the `mkdocs.yml` config:

```yaml
markdown_extensions:
  - pymdownx.arithmatex:
      generic: true   # Options can be specified like this
  - pymdownx.blocks.tab
  - ... # Add more extensions here
```

Currently enabled extensions:

- [`pymdownx.arithmatex`](https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex)<span class="material-symbols-outlined">open_in_new</span>: LaTeX math equations in `$...$` and `$$...$$` blocks
- [`pymdownx.superfences`](https://facelessuser.github.io/pymdown-extensions/extensions/superfences)<span class="material-symbols-outlined">open_in_new</span>: better fenced code blocks with syntax highlighting
    - Can add title, add line numbers, highlight lines
- [`pymdownx.inlinehilite`](https://facelessuser.github.io/pymdown-extensions/extensions/inlinehilite)<span class="material-symbols-outlined">open_in_new</span>: same as superfences, but for inline code snippets
    - Add shebang `#!python` at the start, followed by a space and the code line
- `pymdownx.blocks.*` several block-based features that share a common syntax using `///` fences
    - [`pymdownx.blocks.admonition`](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/admonition/)<span class="material-symbols-outlined">open_in_new</span>: highlighted box with note, warning, etc.
        - Predefined types: `note`, `danger`, `tip`, `warning` (also `attention`, `hint`, `caution`, `error`, but they all seem to be styled like `note`)
    - [`pymdownx.blocks.definition`](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/definition/)<span class="material-symbols-outlined">open_in_new</span>: indented list of terms and their definitions
    - [`pymdownx.blocks.details`](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/details/)<span class="material-symbols-outlined">open_in_new</span>: similar to admonition, but collapsible
    - [`pymdownx.blocks.tab`](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/tab/)<span class="material-symbols-outlined">open_in_new</span>: tabbed content blocks
        - Fence the content with lines `/// tab | Tab 1 name` and `///`, repeat for each tab

### LaTEX math

Math written in LaTeX syntax, both inline expressions with $P_{SOL}$ (`$P_{SOL}$`) and equations:

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

````markdown
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
````

### Admonitions

There are four admonition box styles available: `hint` (blue), `tip` (green), `warning` (yellow) and `danger` (red). The former three are self-explanatory; `danger` usually denotes a piece of information or an entire section focused on a particular machine or server.

Admonition box displaying a tip:

/// tip | Hot tip
SOLPS Tutorials will help you learn SOLPS-ITER.
///

````markdown
/// tip | Hot tip
SOLPS Tutorials will help you learn SOLPS-ITER.
///
````

Admonition box with a warning:

/// warning | Warning
SOLPS-ITER is not for the feeble of mind.
///

````markdown
/// warning | Warning
SOLPS-ITER is not for the feeble of mind.
///
````

Admonition box with a hint or a note:

/// hint | Helpful hint
Life will get better if you sleep a lot.
///

````markdown
/// hint | Helpful hint
Life will get better if you sleep a lot.
///
````

Admonition box with very specific information:

/// danger | IPP Prague
COMPASS was a sheath-limited tokamak.
///

````markdown
/// danger | IPP Prague
COMPASS was a sheath-limited tokamak.
///
````

### Code blocks

Code block with syntax highlighting and a title (e.g. a filename):

```{.fortran title="b2.neutrals.parameters"}
crcstra= 'W', 'E', 'S', 'S', 'N', 'C', 'V', 'T',
```

````markdown
```{.fortran title="b2.neutrals.parameters"}
crcstra= 'W', 'E', 'S', 'S', 'N', 'C', 'V', 'T',
```
````

Fancy two-tab code block with highlighted lines showing the same parameter for both alternatives of Eirene input files.

/// tab | Formatted (`input.dat`)
```{.python hl_lines="4"}
SURFMOD_4_CARBON_SPT_PUMP_580K
    1     2     0     0     1
1.20600E+03-5.00000E-02 0.00000E+00 0.00000E+00 0.00000E+00-1.00000E+00
1.00000E+00 9.00000E-01 1.00000E+00 1.00000E+00 5.00000E-01 1.00000E+00
1.00000E+00 1.00000E+00 0.00000E+00 0.00000E+00 1.00000E+00
```
///

/// tab | JSON (`eirene.input.json`)
```{.json hl_lines="10"}
{
  // ...
  "REFLECTION_MODELS": {
    "MANUAL": "http://www.eirene.de/eirene.pdf#subsection.2.6.1",
    // ...
    "SURFMODS": [
      {
        "NAME": "SURFMOD_4_CARBON_SPT_PUMP_580K",
        // ...
        "RECYCT": 9.0E-01,
        // ...
      }
    ]
  }
}
```
///

````markdown
/// tab | Formatted (`input.dat`)
```{.python hl_lines="4"}
SURFMOD_4_CARBON_SPT_PUMP_580K
    1     2     0     0     1
1.20600E+03-5.00000E-02 0.00000E+00 0.00000E+00 0.00000E+00-1.00000E+00
1.00000E+00 9.00000E-01 1.00000E+00 1.00000E+00 5.00000E-01 1.00000E+00
1.00000E+00 1.00000E+00 0.00000E+00 0.00000E+00 1.00000E+00
```
///

/// tab | JSON (`eirene.input.json`)
```{.json hl_lines="10"}
{
  // ...
  "REFLECTION_MODELS": {
    "MANUAL": "http://www.eirene.de/eirene.pdf#subsection.2.6.1",
    // ...
    "SURFMODS": [
      {
        "NAME": "SURFMOD_4_CARBON_SPT_PUMP_580K",
        // ...
        "RECYCT": 9.0E-01,
        // ...
      }
    ]
  }
}
```
///
````



## Icons

To make SOLPS Tutorials easier to read, we use icons from the *Material Symbols* set provided by Google. Everything is set up in the MkDocs config. To use the icons, simply search for them on [Google Fonts](https://fonts.google.com/icons)<span class="material-symbols-outlined">open_in_new</span>. Click on an icon to open a sidebar, scroll to the *Inserting the icon* section and copy the `<span>` tag into your Markdown text.

Note that, like the Markdown extensions, the icons will not show up in Markdown editors such as Visual Studio Code. They will only show on the final webpage or when you [generate a preview of the MkDocs yourself](#render-solps-tutorials-locally-with-mkdocs).

**External link** (pointing outside SOLPS Tutorials): ITER Sharepoint<span class="material-symbols-outlined">open_in_new</span>

```html
ITER Sharepoint
<span class="material-symbols-outlined">open_in_new</span>
```

**Link to a (downloadable) file**: Katka's PhD thesis<span class="material-symbols-outlined">download</span>

```html
Katka's PhD thesis
<span class="material-symbols-outlined">download</span>
```

**Under construction or to do**:

> **TODO** <span class="material-symbols-outlined">construction</span>:
> Update the tutorials.

```html
> **TODO** <span class="material-symbols-outlined">construction</span>:
> Update the tutorials.
```

**Email address**: <span class="material-symbols-outlined">mail</span> [hromasova@ipp.cas.cz](mailto:hromasova@ipp.cas.cz)

```html
<span class="material-symbols-outlined">mail</span>
[hromasova@ipp.cas.cz](mailto:hromasova@ipp.cas.cz)
```


## Render SOLPS Tutorials locally with MkDocs

Quick edits of SOLPS Tutorials are best done in a [Markdown editor](#recommended-editors), which will render the files in real time. However, most of the fancy [extensions](#markdown-extensions) will not be rendered in that way. There are two options to view the final result before it goes live with a Git pull request into the `master` branch:

> **TODO** <span class="material-symbols-outlined">construction</span>: Update the pipeline artifact information.

- A complete build of pages is generated after each push as a downloadable artifact in the automatic [Pipelines](https://repo.tok.ipp.cas.cz/solps/solps-doc/-/pipelines)<span class="material-symbols-outlined">open_in_new</span> (see download button on the right).

- Build the pages locally:

    ```bash
    # Go to the cloned repository
    cd SOLPS-Tutorials

    # Create a virtual environment and install the libraries
    # This may take a few minutes the first time
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    # Serve and automatically rebuild on any file modifications
    mkdocs serve
    ```

/// danger | IPP Prague
When on COMPASS servers, it's easiest to build the pages locally on Soroban:

```
# Log in to your IPP Prague work station
# If you log into the Soroban front instead, add a tunneling request
ssh -X jirakova@soroban.tok.ipp.cas.cz -L 8000:127.0.0.1:8000
# 8000 is the port being tunneled
# Adjust the port according to where MkDocs creates the documentation

# Load Python 3.8
module load python/3.8-anaconda-2021.05
```
///


`Ctrl + right click` on the link on the last line of the command line output, and a live preview of SOLPS Tutorials will open in your web browser. Every time you save a file, its preview will be updated on the page.

>**TODO** <span class="material-symbols-outlined">construction</span>: Update for GitHub configuration.
>
> Sub-pages located in `./extras` may be handled differently. Refer to corresponding readmes in the `./extras` folder for build instructions and/or check the definition of automated pipeline in `.gitlab-ci.yml` file.






