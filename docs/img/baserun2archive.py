#!/usr/bin/env python3

from pathlib import Path
import argparse
import tarfile
import logging


FILES_REQUIRED = [
    'fort.33',
    'fort.34',
    'fort.35',
]

FILES_EXTRA = [
    '*.v*.geo',
    'template.a*.tria.ogr',
    'template.g*.tria.ogr',
]


def baserun2archive(baserun_dir, archive_path, exclude_extra=False):
    """Store contents of a baserun directory into a compressed archive in a
    "portable" from, meaning that all unimportant links (that can be recrated)
    are ignored and the links to the grid files are resolved.

    Use the following snippet to extract and reconstruct the archived baserun:

        tar -xvf baserun.tar.gz
        cd baserun
        lns <your_project_name>
        setup_baserun_eirene_links

    :baserun_dir str: path to the baserun directory, usually named "baserun"
    :archive_path str: path to the new archive, e.g. "./baserun.tar.gz"
    :exclude_extra bool: exclude linked grid files that are not read by the code
                         namely "*.geo" and "template.*.ogr" (for viewing in
                         DivGeo), defaults to False
    """
    baserun_dir = Path(baserun_dir)
    baserun_name = Path(baserun_dir.name)
    with tarfile.open(archive_path, 'x:gz') as tar:
        logging.info(f'Adding all regular files')
        tar.add(
            baserun_dir,
            arcname=baserun_name,
            filter=lambda t: t if (t.isfile() or t.isdir()) else None,
        )

        linked_files = list(FILES_REQUIRED)
        if not exclude_extra:
            linked_files.extend(FILES_EXTRA)
        logging.info('Resolving linked files (%d in total)', len(linked_files))

        for file_glob in linked_files:
            logging.debug('Resolving: %s', file_glob)
            for name, path in {a.name: a.resolve() for a in baserun_dir.glob(file_glob)}.items():
                tar.add(path, arcname=baserun_name/name)

        logging.info('Created a new baserun archive at "%s"', archive_path)
        logging.debug('Listing all contents:\n%s', '  ' + '\n  '.join(tar.getnames()))

    return archive_path


parser = argparse.ArgumentParser(description=(
    'Generates a compressed archive (.tar.gz) containing the specified baserun'
    ' directory in a form that is "portable" between different computers.'
    ' The "portability" is achieved mainly by resolving some of the linked files.'
    ' A bash snippet showing how to extract and reconstruct the archived baserun'
    ' can be found in the comments in the source code of this script.'
))
parser.add_argument('baserun_dir', help=(
    'path to the baserun directory, usually named "baserun"'
))
parser.add_argument('archive_path', help=(
    'path to the new archive, e.g. "baserun.tar.gz"'
))
parser.add_argument('-x', '--exclude-extra', action='store_true', help=(
    'exclude linked grid files that are not read by the code,'
    ' namely "*.geo" and "template.*.ogr" (for viewing in DivGeo)'
))
parser.add_argument('-v', '--verbose', action='store_true', help=(
    'print more output, including the debug log'
))
parser.add_argument('-s', '--silent', action='store_true', help=(
    'do not print any logging output'
))

if __name__ == '__main__':
    args = parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    if args.silent:
        logging.disable()

    baserun2archive(
        baserun_dir=args.baserun_dir,
        archive_path=args.archive_path,
        exclude_extra=args.exclude_extra,
    )
