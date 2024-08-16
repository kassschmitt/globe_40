import unittest
from datetime import datetime, timedelta
import math
from globe40.utils import (
    extend_interval,
)  # Adjust the import path based on your project structure


class TestExtendInterval(unittest.TestCase):

    def test_increase_duration(self):
        """Test with a positive percentage change and padding days."""
        start_date = "2024-01-01"
        end_date = "2024-01-10"
        percentage_to_change = 50  # Increase duration by 50%
        days_either_end = 2  # Pad with 2 days on either end

        result = extend_interval(
            start_date, end_date, percentage_to_change, days_either_end
        )
        expected_start_date = "2021-12-30"
        expected_end_date = "2022-01-17"

        self.assertEqual(result, (expected_start_date, expected_end_date))

    def test_decrease_duration(self):
        """Test with a negative percentage change and padding days."""
        start_date = "2024-01-01"
        end_date = "2024-01-10"
        percentage_to_change = -50  # Decrease duration by 50%
        days_either_end = 2  # Pad with 2 days on either end

        result = extend_interval(
            start_date, end_date, percentage_to_change, days_either_end
        )
        expected_start_date = "2021-12-30"
        expected_end_date = "2022-01-07"

        self.assertEqual(result, (expected_start_date, expected_end_date))

    def test_no_change(self):
        """Test with zero percentage change and zero padding days."""
        start_date = "2024-01-01"
        end_date = "2024-01-10"
        percentage_to_change = 0
        days_either_end = 0

        result = extend_interval(
            start_date, end_date, percentage_to_change, days_either_end
        )
        self.assertEqual(result, ("2022-01-01", "2022-01-10"))

    def test_padding_only(self):
        """Test with zero percentage change but padding days."""
        start_date = "2024-01-01"
        end_date = "2024-01-10"
        percentage_to_change = 0
        days_either_end = 3  # Pad with 3 days on either end

        result = extend_interval(
            start_date, end_date, percentage_to_change, days_either_end
        )
        self.assertEqual(result, ("2021-12-29", "2022-01-13"))

    def test_invalid_dates(self):
        """Test with invalid date range where start_date is after end_date."""
        start_date = "2024-01-10"
        end_date = "2024-01-01"

        with self.assertRaises(ValueError):
            extend_interval(start_date, end_date)


if __name__ == "__main__":
    unittest.main()
