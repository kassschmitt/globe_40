import unittest
from datetime import datetime
from globe40.utils import (
    get_days_in_interval,
)  # Adjust the import based on your file structure


class TestGetDaysInInterval(unittest.TestCase):

    def test_single_month(self):
        """Test interval within a single month."""
        result = get_days_in_interval("2024-01-01", "2024-01-31")
        expected = [
            (
                2024,
                1,
                [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                    "31",
                ],
            )
        ]
        self.assertEqual(result, expected)

    def test_multiple_months(self):
        """Test interval spanning multiple months."""
        result = get_days_in_interval("2024-01-15", "2024-03-05")
        expected = [
            (
                2024,
                1,
                [
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                    "31",
                ],
            ),
            (
                2024,
                2,
                [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                ],
            ),
            (2024, 3, ["1", "2", "3", "4", "5"]),
        ]
        self.assertEqual(result, expected)

    def test_end_of_year(self):
        """Test interval spanning the end of a year."""
        result = get_days_in_interval("2023-12-15", "2024-01-10")
        expected = [
            (
                2023,
                12,
                [
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                    "31",
                ],
            ),
            (2024, 1, ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]),
        ]
        self.assertEqual(result, expected)

    def test_same_day(self):
        """Test interval where start and end date are the same."""
        result = get_days_in_interval("2024-05-15", "2024-05-15")
        expected = [(2024, 5, ["15"])]
        self.assertEqual(result, expected)

    def test_invalid_date_range(self):
        """Test interval where the start date is after the end date."""
        with self.assertRaises(ValueError):
            get_days_in_interval("2024-03-05", "2024-01-15")

    def test_invalid_date_format(self):
        """Test interval with incorrectly formatted dates."""
        with self.assertRaises(ValueError):
            get_days_in_interval("2024-03-05", "March 15, 2024")

    def test_leap_year(self):
        """Test interval during a leap year."""
        result = get_days_in_interval("2024-02-01", "2024-02-29")
        expected = [
            (
                2024,
                2,
                [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                ],
            )
        ]
        self.assertEqual(result, expected)

    def test_non_leap_year(self):
        """Test interval in a non-leap year for February."""
        result = get_days_in_interval("2023-02-01", "2023-02-28")
        expected = [
            (
                2023,
                2,
                [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                ],
            )
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
