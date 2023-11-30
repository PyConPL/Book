#!/usr/bin/python
# -*- coding: UTF-8 -*-

def apply_patch(diffsrc, test_mode=0):
    src_file = diffsrc + ["/dev/null"]
    return "cat " + src_file[test_mode] + " | patch -d .tmp"


def run_pandoc(main_md):
    return (
        "pandoc -t context --template=src/template.pandoc " + main_md
        + "| sed -e s/subsubsection/section/ > "
        + ".tmp/${TARGET.file}"
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
