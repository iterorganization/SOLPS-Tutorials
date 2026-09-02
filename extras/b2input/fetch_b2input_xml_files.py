"""
Fetch b2input.xml files (and xhtml-symbol.ent) from different versions
of the B2.5 repository hosted on https://github.com/iterorganization/.

Usage:

    python fetch_b2input_xml_files.py ./versions.yaml -d ./fetched

"""
import argparse
import logging
import shutil
import urllib.request
from pathlib import Path

import yaml

logger = logging.getLogger()


def fetch_b25_repo_file(ref, src, dest):
    """Fetch B2.5 repository and copy a file from it."""
    if not shutil.which('git'):
        raise RuntimeError('Command `git` not found, please install git')
    if not any(ref.startswith(prefix) for prefix in ('refs/heads/', 'refs/tags/')):
        raise RuntimeError(f'Unsupported ref "{ref}", expected "refs/heads/..." or "refs/tags/..."')

    fileurl = f'https://github.com/iterorganization/B2.5/raw/{ref}/{src}'
    try:
        urllib.request.urlretrieve(fileurl, dest)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'Failed to fetch file from {fileurl}: {e}') from e


def fetch_all_versions(versions_yaml, dest_dir):
    if not Path(dest_dir).exists():
        Path(dest_dir).mkdir(exist_ok=True, parents=True)

    with Path(versions_yaml).open() as f:
        config = yaml.safe_load(f)
        logger.debug(f'Loaded config:\n{config}')

    git_ref = config['xhtml_symbol']['git_ref']
    path = Path(dest_dir, 'xhtml-symbol.ent')
    logger.info(f'Downloading xhtml-symbol.ent at ref "{git_ref}" to "{path}"')
    fetch_b25_repo_file(git_ref, 'src/documentation/xhtml-symbol.ent', path)

    for item in config['versions']:
        git_ref = item['git_ref']
        path = Path(dest_dir, f'b2input.xml.{item["label"]}')
        logger.info(f'Downloading b2input.xml at ref "{git_ref}" to "{path}"')
        if ' ' in item['label']:
            raise ValueError(f'Version label "{item["label"]}" contains a space')
        fetch_b25_repo_file(git_ref, 'src/documentation/b2input.xml', path)


parser = argparse.ArgumentParser()
parser.add_argument('versions_yaml', metavar='PATH_VERSIONS_YAML', help=(
    'path to a "versions.yaml" file containing the list of git refs in the B2.5'
    ' repository and corresponding labels for the webpage, see the "versions.yaml"'
    ' file in this repo for more information'
))
parser.add_argument('-d', '--dest-dir', default='.', help=(
    'destination directory for the fetched files, will be created if it'
    ' does not exist, default="."'
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

    fetch_all_versions(
        versions_yaml=args.versions_yaml,
        dest_dir=args.dest_dir,
    )
