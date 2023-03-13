import unittest

import gurutracker.tests.database
import gurutracker.tests.helpers
        
if __name__ == "__main__":
    allsuites = unittest.TestSuite([
        gurutracker.tests.helpers.suite()
        ])
    unittest.TextTestRunner(verbosity=2).run(allsuites)