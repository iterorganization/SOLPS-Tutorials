"""
Generate web-page version of B2 input files documentation. Usage:

    module load python/3.9-anaconda-2021.11
    cd extras/b2_inputs
    python generate_html.py

    firefox public

Using data from
    - "solps-iter/modules/B2.5/src/documentation/b2input.xml"
    - "solps-iter/modules/B2.5/src/documentation/xhtml-symbol.ent"
"""

import argparse
import datetime
import json
import logging
import re
from pathlib import Path

import yaml
from bs4 import BeautifulSoup as BS
from jinja2 import Environment, FileSystemLoader, select_autoescape
from lxml import etree

logger = logging.getLogger()


def parse_b2input_xml(b2input_xml):
    """Parse "b2input.xml" file located at path b2input_xml and return Soup."""
    logger.info(f'Parsing XML file: "{b2input_xml}"')
    # NOTE: Parsing XML in a complicated way, because BS4 does not know
    #       how to resolve external entities reference in XML.
    tree = etree.parse(str(b2input_xml), parser=etree.XMLParser(load_dtd=True))
    soup = BS(etree.tostring(tree.getroot()), 'lxml-xml')
    logger.info('XML parsed successfully')
    return soup


def gen_from_module(module, env, out_path='.'):
    """Used by gen_html_all_modules()"""
    logger.info(f'Processing module: {module["name"]}')
    template = env.get_template('module_template.html')

    def format_description(text):
        text = re.sub(r'\n\s+(\d+\s*:)', r'</li><li><b>\1</b>', text)
        if '</li>' in text:
            text = text.replace(
                '</li>', '<ul class="ui list">', 1).strip() + '</ul>'
        return text

    for cat in module['categories']:
        for group in cat['groups']:
            if group.get('description'):
                group['description'] = format_description(group['description'])
            for switch in group['switches']:
                if switch['description']:
                    switch['description'] = format_description(
                        switch['description'])

    with (Path(out_path) / f'{module["name"]}.html').open('w') as f:
        f.write(template.render(module=module))
        logger.info(f'Writing to file: "{f.name}"')


def gen_toplevel_index(labels, env, out_path='.'):
    """Generate top-level index page when using multiple b2input.xml files"""
    logger.info('Processing index_toplevel template')
    template = env.get_template('index_toplevel_template.html')
    with (Path(out_path) / 'index.html').open('w') as f:
        f.write(template.render(labels=labels, current_date=datetime.datetime.now()))
        logger.info(f'Writing to file: "{f.name}"')


def gen_modules_index(b2json, env, out_path='.'):
    """Used by gen_html_all_modules()"""
    logger.info('Processing index_modules template')
    template = env.get_template('index_modules_template.html')
    with (Path(out_path) / 'index.html').open('w') as f:
        f.write(template.render(all_modules=b2json))
        logger.info(f'Writing to file: "{f.name}"')


def gen_all_modules(b2json, env, out_path='.'):
    """Generate html version of all modules"""
    for module in b2json.values():
        gen_from_module(module, env=env, out_path=out_path)
    gen_modules_index(b2json, env=env, out_path=out_path)


def module_to_json(module_soup):
    def extract_texts(soup, tags=[], attrs=[]):
        return {
            **{tag: getattr(soup.find(tag), 'text', None) for tag in tags},
            **{attr: soup.get(attr) for attr in attrs},
        }

    def parse_switch(soup):
        return extract_texts(soup, tags=[
            'name', 'description', 'type', 'default',
        ])

    def parse_switch_group(soup):
        return {
            **extract_texts(soup, tags=['name', 'description']),
            'switches': [
                parse_switch(s) for s in soup.find_all('switch')
            ],
        }

    module = {
        **extract_texts(module_soup, attrs=['name', 'type']),
        'categories': [],
    }

    for cat_soup in module_soup.find_all('category'):
        category = {
            **extract_texts(cat_soup, attrs=['name']),
            'groups': [],
        }
        for child_soup in cat_soup.children:
            if child_soup.name == 'introduction':
                category.update(extract_texts(
                    child_soup, tags=['namelist', 'description']
                ))
            if child_soup.name == 'switch':
                group = {'switches': [parse_switch(child_soup)]}
                category['groups'].append(group)
            elif child_soup.name == 'switchgroup':
                group = parse_switch_group(child_soup)
                category['groups'].append(group)
        module['categories'].append(category)
    return module


def b2input_to_json(soup):
    return {
        module_soup['name']: module_to_json(module_soup)
        for module_soup in soup.b2.find_all('module')
    }


def gen_detail_boundary(soup, env, out_path='.'):
    """Generate a "detail" page focusing on b2.boundary.parameters,
    which lists and categorizes available boundary condition options.
    """
    b2_boundary = soup.b2.find(
        'category', attrs={'name': 'b2.boundary.parameters'})
    bc_labels = yaml.safe_load(env.get_template('bc_labels.yaml').render())

    # Parse description, extract the individual options
    def parse_bc_description(text):
        conditions = {}
        for line in text.splitlines():
            matched = re.match(r'\s*(\d+)\s*:\s*(.*)', line)
            if matched:
                n = int(matched[1])
                conditions[n] = matched[2]
            elif len(conditions) > 1:
                conditions[n] += '\n' + line
            else:
                conditions['introduction'] = conditions.get(
                    'introduction', '') + '\n' + line
        return conditions
    bc_descriptions = {
        s.find('name').text.lower(): parse_bc_description(str(s.find('description')))
        for s in b2_boundary.find_all('switch')
        if s.find('name').text.lower() in bc_labels['bc_to_label']
    }

    # Invert mapping bc->labels to label->bc, the first label decides where does bc go
    def filter_by_first_label(bc_to_label, label):
        return [
            n for n, l in bc_to_label.items()
            if l.startswith(label)
        ]
    bc_labels['label_to_bc'] = {
        name: {
            label: filter_by_first_label(mapping, label)
            for label in bc_labels['labels']
        }
        for name, mapping in bc_labels['bc_to_label'].items()
    }

    logger.info('Processing detail_bc template')
    template = env.get_template('detail_bc_template.html')
    with (Path(out_path) / 'detail_bc.html').open('w') as f:
        f.write(template.render(
            descriptions=bc_descriptions,
            bc_to_label=bc_labels['bc_to_label'],
            label_to_bc=bc_labels['label_to_bc'],
            labels=bc_labels['labels'],
        ))
        logger.info(f'Writing to file: "{f.name}"')


def build_from_one(b2input_xml, source_dir, dest_dir, label=''):
    """Build a complete page from a single b2input.xml file.

    See configuration of `ArgumentParser` below for more details.
    """
    # Load and parse b2input.xml
    soup_file = Path(b2input_xml)
    if not soup_file.exists():
        raise FileNotFoundError(f'Unable to find the "{soup_file.name}" file')
    soup = parse_b2input_xml(soup_file)
    b2json = b2input_to_json(soup)

    # Look for the templates and dest_dir
    src_html = Path(source_dir, 'src_html')
    if not src_html.exists():
        raise FileNotFoundError(
            f'Unable to find the "{src_html.name}" directory')
    Path(dest_dir).mkdir(exist_ok=True, parents=True)

    # Write output (b2input.json, render templates)
    logger.info('Producing JSON representation')
    with Path(dest_dir, 'b2input.json').open('w') as out_file:
        json.dump(b2json, out_file)
        logger.info(f'Writing to file: "{out_file.name}"')
    env = Environment(
        loader=FileSystemLoader(src_html),
        autoescape=select_autoescape([]),
    )
    env.globals['header_label'] = label
    gen_all_modules(b2json, env, dest_dir)
    gen_detail_boundary(soup, env, dest_dir)

    for static_file in Path(source_dir, 'src_static').iterdir():
        Path(dest_dir, static_file.name).write_text(
            static_file.read_text()
        )
        logger.info(f'Copying static file: "{static_file.name}"')

    logger.info(
        f'Docs from "{b2input_xml}" were successfully generated in "{dest_dir}"')


def build_from_multiple(b2input_dir, source_dir, dest_dir):
    """Build a complete page from multiple b2input.xml files in directory.

    Automatically scans the directory for "b2input.xml.*" files, where the
    suffix represents SOLPS-ITER version (e.g. "b2input.xml.3.0.8"). New page
    is generated for each version and a top-level index is created to access them.
    """
    files = sorted(Path(b2input_dir).glob('b2input.xml.*'))
    suffixes = [f.name[len("b2input.xml."):] for f in files]

    logger.info(f'Processing {len(files)} b2input.xml files found in directory "{b2input_dir}"')
    Path(dest_dir).mkdir(exist_ok=True, parents=True)
    for b2input_xml, label in zip(files, suffixes):
        Path(dest_dir, label).mkdir(exist_ok=True)
        build_from_one(
            b2input_xml=b2input_xml,
            source_dir=source_dir,
            dest_dir=Path(dest_dir, label),
            label=f'SOLPS-ITER {label}'
        )
    env = Environment(loader=FileSystemLoader(Path(source_dir, 'src_html')))
    gen_toplevel_index(suffixes, env, dest_dir)


parser = argparse.ArgumentParser()
parser.add_argument('path_b2input', metavar='PATH_B2INPUT_XML', help=(
    'path to the "b2input.xml" file, can be also directory containing multiple "b2input.xml.*" files,'
    'where the suffix is expected to be SOLPS-ITER version (e.g. "b2input.xml.3.0.8")'
))
parser.add_argument('-d', '--dest-dir', default='./public', help=(
    'name of the output directory where the html files are written,'
    ' will be created if it does not exist, default="./public"'
))
parser.add_argument('-s', '--source-dir', default='.', help=(
    'name of the directory containing "src_html" and "src_static", default="."'
))
parser.add_argument('-l', '--label', default='', help=(
    'optional label (e.g. version) that is shown in header, ignored when PATH_B2INPUT_XML is directory'
))
parser.add_argument('-v', '--verbose', action='store_true', help=(
    'print logging output'
))

if __name__ == '__main__':
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        pass

    if Path(args.path_b2input).is_dir():
        build_from_multiple(
            b2input_dir=args.path_b2input,
            source_dir=args.source_dir,
            dest_dir=args.dest_dir
        )
    else:
        build_from_one(
            b2input_xml=args.path_b2input,
            source_dir=args.source_dir,
            dest_dir=args.dest_dir,
            label=args.label,
        )
