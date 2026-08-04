"""
Fetch b2input.xml files (and xhtml-symbol.ent) from different versions
of the B2.5 repository hosted on https://git.iter.org.

Usage:

    export GIT_ITER_USER="username"
    export GIT_ITER_TOKEN="some_secret_token"
    python fetch_b2input_xml_files.py ./versions.yaml -d ./fetched

"""
import argparse
import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import yaml

logger = logging.getLogger()


def fetch_b25_repo_file(git_user, git_token, ref, src, dest):
    """Fetch B2.5 repository and copy a file from it."""
    if not shutil.which('git'):
        raise RuntimeError('Command `git` not found, please install git')
    repourl = f'https://{git_user}:{git_token}@git.iter.org/scm/bnd/b2.5.git'

    # Remove the prefix if ref is specified using the full git ref name
    if ref.startswith('refs/'):
        for prefix in ('refs/heads/', 'refs/tags/'):
            if ref.startswith(prefix):
                ref = ref.removeprefix(prefix)
                break
        else:
            raise RuntimeError(f'Unsupported ref "{ref}", expected "refs/heads/..." or "refs/tags/..."')

    with tempfile.TemporaryDirectory(prefix='b2.5_') as tmpdir:
        repodir = Path(tmpdir, ref.replace('/', '_'))
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', '--branch', ref, repourl, str(repodir)],
            # stdout=subprocess.DEVNULL,
            # stderr=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f'Failed to clone the B2.5 repository at ref "{ref}", return code={result.returncode},'
                + ' possibly a token authentication issue or invalid branch/tag name'
            )
        if not (repodir / src).exists():
            raise RuntimeError(f'File "{src}" not found in the B2.5 repository at ref "{ref}"')
        with open(dest, 'wb') as f:
            f.write((repodir / src).read_bytes())


def fetch_all_versions(git_user, git_token, versions_yaml, dest_dir):
    if not Path(dest_dir).exists():
        Path(dest_dir).mkdir(exist_ok=True, parents=True)

    with Path(versions_yaml).open() as f:
        config = yaml.safe_load(f)
        logger.debug(f'Loaded config:\n{config}')

    git_ref = config['xhtml_symbol']['git_ref']
    path = Path(dest_dir, 'xhtml-symbol.ent')
    logger.info(f'Downloading xhtml-symbol.ent at ref "{git_ref}" to "{path}"')
    fetch_b25_repo_file(git_user, git_token, git_ref, 'src/documentation/xhtml-symbol.ent', path)

    for item in config['versions']:
        git_ref = item['git_ref']
        path = Path(dest_dir, f'b2input.xml.{item["label"]}')
        logger.info(f'Downloading b2input.xml at ref "{git_ref}" to "{path}"')
        if ' ' in item['label']:
            raise ValueError(f'Version label "{item["label"]}" contains a space')
        fetch_b25_repo_file(git_user, git_token, git_ref, 'src/documentation/b2input.xml', path)


parser = argparse.ArgumentParser()
parser.add_argument('versions_yaml', metavar='PATH_VERSIONS_YAML', help=(
    'path to a "versions.yaml" file containing the list of git refs in the B2.5',
    ' repository and corresponding labels for the webpage, see the "versions.yaml"',
    ' file in this repo for more information'
))
parser.add_argument('-d', '--dest-dir', default='.', help=(
    'destination directory for the fetched files, will be created if it'
    ' does not exist, default="."'
))
parser.add_argument('-a', '--auth', default=None, help=(
    'username and access token in format "user:token" with read-only access to git.iter.org,'
    ' will attempt to read it from the GIT_ITER_USER and GIT_ITER_TOKEN env vars if this parameter is not specified'
))
parser.add_argument('-v', '--verbose', action='store_true', help=(
    'print logging output'
))

if __name__ == '__main__':
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        pass

    if args.auth is not None:
        try:
            git_user, git_token = args.auth.split(':')
        except ValueError:
            raise RuntimeError('Invalid auth format, expected "user:token"')
    elif 'GIT_ITER_USER' in os.environ and 'GIT_ITER_TOKEN' in os.environ:
        git_user = os.environ['GIT_ITER_USER']
        git_token = os.environ['GIT_ITER_TOKEN']
    else:
        raise RuntimeError(
            'If auth credentials are not provided (--token), GIT_ITER_USER and GIT_ITER_TOKEN env vars must be set')

    fetch_all_versions(
        git_user=git_user,
        git_token=git_token,
        versions_yaml=args.versions_yaml,
        dest_dir=args.dest_dir,
    )
