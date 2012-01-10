import unittest
import doctest

OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

from csscheck import utils, main

def suite():
    return unittest.TestSuite([
        doctest.DocTestSuite(
            utils,
            optionflags=OPTIONFLAGS),
        doctest.DocTestSuite(
            main,
            optionflags=OPTIONFLAGS),
        ])

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
