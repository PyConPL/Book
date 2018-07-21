#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import os
import re
import shutil

diagnose_article_pages = 0

debug = 0
verbose = 0
tex_to_file = 0
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


def fl_dump(label, fl_name):
    if diagnose_article_pages:
        print label, fl_name
        if os.path.isfile(fl_name):
            print open(fl_name, 'rb').read()
        else:
            print 'no file (yet).'


def check_for_source(alias, fl_name):
    if os.path.exists(fl_name):
        result = 1
        if verbose:
            print '%s - found: %s' % (alias, fl_name)
    else:
        result = 0
        if verbose:
            print '%s - not found: %s' % (alias, fl_name)
    return result


def sanity_check():
    src_dir = 'src'
    if not os.path.isdir(src_dir):
        raise RuntimeError("No directory: '%s'" % src_dir)
    pndc_tmpl = 'src/template.pandoc'
    if not os.path.isfile(pndc_tmpl):
        raise RuntimeError("No file: '%s'" % pndc_tmpl)


def final_command():
    cmd = "texexec --pdfcopy --result=$TARGET $SOURCES"
    if tex_to_file:
        cmd = cmd + " >log_b1.txt 2>log_b2.txt"
    return cmd


class OneTalk(object):
    def __init__(self, tty_columns, alias, location, copy_images, create_pdfs):
        '''
        OneTalk:
        '''
        self.tty_columns = tty_columns
        self.alias = alias
        self.location = location
        self.copy_images = copy_images
        self.create_pdfs = create_pdfs

    def copy_needed_files(self):
        '''
        OneTalk:
        '''
        one_ls = files_to_copy.get(self.alias)
        if one_ls:
            src_dir = one_ls[0]
            for src_file in one_ls[1:]:
                full_src = src_dir + src_file
                full_dst = src_file
                if verbose:
                    print 'Copy %(full_src)s to %(full_dst)s' % dict(
                        full_src=full_src,
                        full_dst=full_dst,
                        )
                shutil.copyfile(full_src, full_dst)

    def run_tex_for_chapter(self):
        '''
        OneTalk:
        '''
        cmd = "texexec --pdf " + self.alias
        if tex_to_file:
            cmd = cmd + " >log_a1.txt 2>log_a2.txt"
        if verbose:
            print cmd
        fl_dump('ABOVE1', '../artpages.inc')
        fl_dump('HERE1', 'artpages.inc')
        os.system(cmd)
        fl_dump('ABOVE2', '../artpages.inc')
        fl_dump('HERE2', 'artpages.inc')

    def move_page_numbers_file(self):
        '''
        OneTalk:
        '''
        full_src = 'artpages.inc'
        full_dst = '../' + full_src
        fl_dump('ABOVE3', '../artpages.inc')
        fl_dump('HERE3', 'artpages.inc')
        if verbose:
            print 'Move %(full_src)s to %(full_dst)s' % dict(
                full_src=full_src,
                full_dst=full_dst,
                )
        if os.path.isfile(full_src):
            result = os.rename(full_src, full_dst)
            if verbose:
                print 'Move result:', result
        else:
            print 'No file to move:', full_src
        fl_dump('ABOVE4', '../artpages.inc')
        fl_dump('HERE4', 'artpages.inc')

    def small_fn(self, env, target, source):
        '''
        OneTalk:
        '''
        my_stars = '*' * 50 + ' '
        if verbose:
            print my_stars + 'START ' + self.alias
        if 0 and verbose:
            tmp_format = 'self.alias, self.copy_images, env, target, source'
            print('Eval: %s %s' % (tmp_format, eval(tmp_format)))
        print os.getcwd()
        txt_line = prepare_line(self.tty_columns, self.alias, self.location)
        print '# ' + txt_line
        link_do_src(self.alias)
        if self.copy_images:
            self.copy_needed_files()
        if self.create_pdfs:
            self.run_tex_for_chapter()
        self.move_page_numbers_file()
        if verbose:
            print my_stars + 'END ' + self.alias
