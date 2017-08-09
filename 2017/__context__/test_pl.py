#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import unittest
import sys

import pl_txt

class TestPL(unittest.TestCase):
    def test_patching(self):
        '''
        TestPL:
        '''
        self.assertEqual(
            pl_txt.apply_patch(diffsrc=['a']),
            'cat a | patch -d .tmp',
            )
        self.assertEqual(
            pl_txt.apply_patch(diffsrc=['a'], test_mode=1),
            'cat /dev/null | patch -d .tmp',
            )

    def test_md_to_tex_conversion(self):
        '''
        TestPL:
        '''
        self.assertEqual(
            pl_txt.run_pandoc(main_md='a'),
            'pandoc -t context --template=src/template.pandoc a| sed -e s/subsubsection/section/ > .tmp/${TARGET.file}',
            )

    def test_linking_source_directory(self):
        '''
        TestPL:
        '''
        self.assertEqual(
            pl_txt.art_src_dir(alias='a'),
            '../../src/a',
            )
        self.assertEqual(
            pl_txt.link_src(alias='a'),
            '[ -L src -o ! -d ../../src/a ] || ln -s ../../src/a src',
            )

    def test_article_selection(self):
        '''
        TestPL:
        '''
        self.assertEqual(pl_txt.pass_line(''), 0)
        self.assertEqual(pl_txt.pass_line('a'), 1)
        self.assertEqual(pl_txt.pass_line('%'), 0)
        self.assertEqual(pl_txt.pass_line(' %'), 0)

    def test_comment_removing(self):
        '''
        TestPL:
        '''
        self.assertEqual(pl_txt.remove_comments(''), '')
        self.assertEqual(pl_txt.remove_comments('a'), 'a')
        self.assertEqual(pl_txt.remove_comments('%a'), '')
        self.assertEqual(pl_txt.remove_comments('b%'), 'b')

    def test_article_home(self):
        '''
        TestPL:
        '''
        self.assertEqual(pl_txt.art_home('a'), 'build/a')

    def test_article_core(self):
        '''
        TestPL:
        '''
        self.assertEqual(pl_txt.art_file_core('b'), 'build/b/b')

    def test_article_pdf(self):
        '''
        TestPL:
        '''
        self.assertEqual(pl_txt.art_file_pdf('cd'), 'build/cd/cd.pdf')

    def test_pages_of_articles(self):
        '''
        TestPL:
        '''
        self.assertEqual(pl_txt.art_pages_file(), 'build/artpages.inc')

def make_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPL))
    text_test_result = unittest.TextTestRunner().run(suite)
    result = not not (text_test_result.failures or text_test_result.errors)
    return result

if __name__ == '__main__':
    result = make_tests()
    sys.exit(result)
