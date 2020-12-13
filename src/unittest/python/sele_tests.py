from mockito import mock, verify
import unittest

from sele import Rs

class ResTest(unittest.TestCase):
    def test_should_issue_res_message(self):
        out = mock()

        x = Rs(out)
        if x >=2:
            verify(out).write("Best Results")
        else:
            verify(out).write("Worst Results")