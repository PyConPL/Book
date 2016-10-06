#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
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

def make_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPL))
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    make_tests()
