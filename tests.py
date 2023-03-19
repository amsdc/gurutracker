import unittest
import os

os.environ["GURUTRACKER_CONFIGURATION_TESTING"] = "yes"

import dotenv
dotenv.load_dotenv()

import gurutracker.tests.database
import gurutracker.tests.helpers
import gurutracker.tests.storage
        
if __name__ == "__main__":
    allsuites = unittest.TestSuite([
        gurutracker.tests.database.suite(),
        gurutracker.tests.helpers.suite(),
        gurutracker.tests.storage.suite()
        ])
    unittest.TextTestRunner(verbosity=2).run(allsuites)
    
    del os.environ["GURUTRACKER_CONFIGURATION_TESTING"]