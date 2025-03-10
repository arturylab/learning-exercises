import unittest

def calculate_total(price, tax_rate):
    return price + (price * tax_rate)

class TestCalculateTotal(unittest.TestCase):
    def test_calculate_total(self):
        self.assertEqual(calculate_total(100, .05), 105)
        self.assertEqual(calculate_total(200, .10), 220)

if __name__ == '__main__':
    unittest.main()