import os
import sys
import unittest

# Ensure the module can be imported cleanly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from masking import alias_for, assert_no_raw_names_leak


class TestMasking(unittest.TestCase):

  def test_alias_for_rs019(self):
    """Acceptance criterion: alias_for('RS019') == 'ALIAS-19'."""
    self.assertEqual(alias_for("RS019"), "ALIAS-19")
    self.assertEqual(alias_for("RS006"), "ALIAS-06")
    self.assertEqual(alias_for("RS022"), "ALIAS-22")

  def test_raw_name_leak_detection(self):
    """Acceptance criteria:

    assert_no_raw_names_leak returns True on final clean narrative,
    and False on a version that contains raw names like 'Mumbai Reseller 1'.
    """
    raw_resellers = [
        "Mumbai Reseller 1",
        "Mumbai Reseller 4",
        "Hyderabad Reseller 6",
        "Lucknow Reseller 6",
        "Jaipur Reseller 5",
    ]

    clean_narrative = (
        "In the West region, top volume was driven by ALIAS-19 (INR 75295.09) "
        "and ALIAS-22 (INR 73882.33), with zero raw identity exposure."
    )

    leaked_narrative = (
        "In the West region, top volume was driven by Mumbai Reseller 1 (INR"
        " 75295.09) and ALIAS-22 (INR 73882.33)."
    )

    self.assertTrue(assert_no_raw_names_leak(clean_narrative, raw_resellers))
    self.assertFalse(assert_no_raw_names_leak(leaked_narrative, raw_resellers))


if __name__ == "__main__":
  unittest.main()