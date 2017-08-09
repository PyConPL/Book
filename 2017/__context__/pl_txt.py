#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

debug = 0

def apply_patch(diffsrc, test_mode=0):
    src_file = diffsrc + ["/dev/null"]
    return "cat " + src_file[test_mode] + " | patch -d .tmp"

def run_pandoc(main_md):
    return (
        "pandoc -t context --template=src/template.pandoc " + main_md +
        "| sed -e s/subsubsection/section/ > " +
        ".tmp/${TARGET.file}"
        )

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
    prev_data = read_file(name)
    if prev_data != new_data:
        write_file(name, new_data)
