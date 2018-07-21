#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import os
import re

debug = 0
verbose = 0
build_dir = "build"

master_pattern = re.compile(
'''
^
pycon
\d{4}
$
''',
re.VERBOSE
)

files_to_copy = {
    'cyber': [
        '../../../presentations/with_python_security/',
        '000_notpetya.png',
        '001_attacks_per_day.png',
        '002_batman.png',
        ],
    'real': [
        '../../../presentations/django_in_the_real_world/',
        'diagram.png',
        ],
    'zodb': [
        '../../../presentations/zodb_ecosystem/',
        'ZODBTitleGraphics.png',
        ],
    'micro': [
        '../../../workshops/micropython/',
        'ryc1.png',
        'ryc2.png',
        'ryc3.png',
        'ryc4.png',
        ],
    'networkx': [
        '../../../workshops/Network_Analysis_using_Python/',
        'network.png',
        ],
}

def apply_patch(diffsrc, gm_dir, test_mode=0):
    src_file = diffsrc + ["/dev/null"]
    return "cat " + src_file[test_mode] + " | patch -d " + gm_dir

def run_pandoc(main_md, gm_dir, pyladies=0):
    if pyladies:
        tag_replace = r" -e 's/:snake:/$\\sim$/g' -e 's/:pushpin:/$\\swarrow$/g'"
    else:
        tag_replace = ''
    return ''.join([
        "pandoc -t context --template=src/template.pandoc ",
        main_md,
        "| sed -e s/subsubsection/section/",
        tag_replace,
        " > ",
        gm_dir,
        "/${TARGET.file}",
        ])

def art_src_dir(alias):
    return "../../src/" + alias

def link_src(alias):
    '''
    Current directory: build/a
    Link to src/a directory, assuming it exists.
    '''
    source = art_src_dir(alias)
    return "[ -L src -o ! -d %(source)s ] || ln -s %(source)s src" % dict(
        source=source,
        )

def link_do_src(alias):
    '''
    Current directory: build/a
    Link to src/a directory, assuming it exists.
    '''
    tmp_sr_dir = 'src'
    source = art_src_dir(alias)
    if verbose:
        print 'Preparing to create symlink %(source)s -> %(tmp_sr_dir)s' % dict(
            source=source,
            tmp_sr_dir=tmp_sr_dir,
            )
    if not os.path.islink(tmp_sr_dir) and os.path.isdir(source):
        os.symlink(source, tmp_sr_dir)

def pass_line(one_line):
    if one_line and not one_line.strip().startswith('%'):
        result = 1
    else:
        result = 0
    return result

def remove_comments(line):
    return line.split('%')[0]

def env_command(
        env,
        target,
        source,
        action,
        **kwargs
        ):
    if debug:
        print('')
        tmp_format = 'target'; print('Eval: %s %s' % (tmp_format, eval(tmp_format)))
        tmp_format = 'source'; print('Eval: %s %s' % (tmp_format, eval(tmp_format)))
        tmp_format = 'action'; print('Eval: %s %s' % (tmp_format, eval(tmp_format)))
        tmp_format = 'kwargs'; print('Eval: %s %s' % (tmp_format, eval(tmp_format)))
    env.Command(
        target,
        source,
        action,
        **kwargs
        )

def read_file(name):
    fd = open(name, 'rb')
    data = fd.read()
    fd.close()
    return data

def write_file(name, data):
    fd = open(name, 'wb')
    fd.write(data)
    fd.close()
    print("Written %d bytes to '%s'" % (
        len(data),
        name,
        ))

def write_if_needed(name, new_data):
    if os.path.isfile(name):
        prev_data = read_file(name)
    else:
        prev_data = ''
    if prev_data != new_data:
        write_file(name, new_data)

def prepare_file(al_loc_ls):
    line_ls = []
    for alias, location in al_loc_ls:
        elem = '%s %s\n' % (alias, location)
        line_ls.append(elem)
    return ''.join(line_ls)

def prepare_line(tty_columns, alias, location):
    if tty_columns:
        dash_count = tty_columns - 5 - len(alias) - len(location)
        txt_line = ''.join([
            '-' * dash_count,
            ' ',
            alias,
            ' ',
            location,
            ])
    else:
        txt_line = ''
    return txt_line

def art_home(alias):
    return "%s/%s" % (build_dir, alias)

def art_file_core(alias):
    return ''.join([
        art_home(alias),
        '/',
        alias,
        ])

def art_file_pdf(alias):
    return art_file_core(alias) + '.pdf'

def art_pages_file():
    return art_home('artpages.inc')


def is_master(one_alias):
    if master_pattern.search(one_alias):
        result = 1
    else:
        result = 0
    return result
