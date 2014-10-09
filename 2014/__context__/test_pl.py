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

def make_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPL))
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    make_tests()
