import os
import unittest
from growth_engine import is_flagged, mom_growth, validate_feed


class TestGrowthEngine(unittest.TestCase):

  def setUp(self):
    self.base_dir = os.path.dirname(os.path.abspath(__file__))
    self.corrupted_fixture = os.path.join(
        self.base_dir, "fixtures", "corrupted_feed.csv"
    )
    self.valid_fixture = os.path.join(
        self.base_dir, "fixtures", "monthly_category_revenue.csv"
    )

  def test_spec_1_ethnic_wear_april_to_may(self):
    """GIVEN April->May Ethnic Wear moves from 104520.77 to 185107.61,

    WHEN mom_growth and is_flagged run,
    THEN mom_growth returns 77.1 and is_flagged returns 'flagged'.
    """
    growth = mom_growth(104520.77, 185107.61)
    status = is_flagged(growth)
    self.assertEqual(growth, 77.1)
    self.assertEqual(status, "flagged")

  def test_spec_2_beauty_may_to_june(self):
    """GIVEN May->June Beauty & Personal Care moves from 35542.11 to 37559.07,

    WHEN evaluated,
    THEN mom_growth returns 5.67 and is_flagged returns 'not_flagged'.
    """
    growth = mom_growth(35542.11, 37559.07)
    status = is_flagged(growth)
    self.assertEqual(growth, 5.67)
    self.assertEqual(status, "not_flagged")

  def test_spec_3_exact_boundary(self):
    """GIVEN synthetic pair previous=100000, current=108000,

    WHEN evaluated,
    THEN mom_growth returns 8.0 and is_flagged returns 'escalate_exact_boundary'.
    """
    growth = mom_growth(100000.0, 108000.0)
    status = is_flagged(growth)
    self.assertEqual(growth, 8.0)
    self.assertEqual(status, "escalate_exact_boundary")

  def test_spec_4_corrupted_feed(self):
    """GIVEN the corrupted feed fixture,

    WHEN validate_feed runs,
    THEN it returns (False, errors) with exactly 3 ordered errors.
    """
    is_valid, errors = validate_feed(self.corrupted_fixture)
    self.assertFalse(is_valid)
    expected_errors = [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]
    self.assertEqual(errors, expected_errors)

  def test_valid_feed_passes(self):
    """Confirm all 15 rows of monthly_category_revenue.csv pass with zero errors."""
    is_valid, errors = validate_feed(self.valid_fixture)
    self.assertTrue(is_valid)
    self.assertEqual(errors, [])

  def test_full_may_vs_april_mom_table(self):
    """Confirm full May-vs-April MoM table matches acceptance criteria."""
    data = [
        ("Ethnic Wear", 104520.77, 185107.61, 77.1, "flagged"),
        ("Western Wear", 113866.15, 86998.18, -23.6, "flagged"),
        ("Kids Wear", 59847.27, 45793.78, -23.48, "flagged"),
        ("Home & Kitchen", 100446.23, 91152.57, -9.25, "flagged"),
        ("Beauty & Personal Care", 40737.01, 35542.11, -12.75, "flagged"),
    ]
    for cat, prev_rev, curr_rev, exp_mom, exp_flag in data:
      g = mom_growth(prev_rev, curr_rev)
      f = is_flagged(g)
      self.assertEqual(g, exp_mom, f"Mismatch in MoM for {cat}")
      self.assertEqual(f, exp_flag, f"Mismatch in flag for {cat}")

  def test_full_june_vs_may_mom_table(self):
    """Confirm full June-vs-May MoM table matches acceptance criteria."""
    data = [
        ("Ethnic Wear", 185107.61, 76371.53, -58.74, "flagged"),
        ("Western Wear", 86998.18, 97415.64, 11.97, "flagged"),
        ("Kids Wear", 45793.78, 56737.78, 23.9, "flagged"),
        ("Home & Kitchen", 91152.57, 129971.22, 42.59, "flagged"),
        ("Beauty & Personal Care", 35542.11, 37559.07, 5.67, "not_flagged"),
    ]
    for cat, prev_rev, curr_rev, exp_mom, exp_flag in data:
      g = mom_growth(prev_rev, curr_rev)
      f = is_flagged(g)
      self.assertEqual(g, exp_mom, f"Mismatch in MoM for {cat}")
      self.assertEqual(f, exp_flag, f"Mismatch in flag for {cat}")


if __name__ == "__main__":
  unittest.main()