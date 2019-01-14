import unittest
import sys


def factorize(x):
    """ Factorize positive integer and return its factors.
        :type x: int,>=0
        :rtype: tuple[N],N>0
    """
    pass

class TestFactorize(unittest.TestCase):

    def test_wrong_types_raise_exception(self):
        """
        Типы float и str (значения 'string', 1.5) вызывают исключение TypeError.
        """
        cases = ('string', 1.5)

        for x in cases:
            with self.subTest(case=x):
                self.assertRaises(TypeError, algorithm, x)

    def test_negative(self):
        """
        Для отрицательных чисел -1, -10 и -100 вызывается исключение ValueError.
        """
        cases = ( -1, -10, -100)

        for x in cases:
            with self.subTest(case=x):
                self.assertRaises(ValueError, algorithm, x)

    def test_zero_and_one_cases(self):
        """
        Для числа 0 возвращается кортеж (0,), а для числа 1 кортеж (1,)
        """
        cases = (0, 1)

        for x in cases:    
            with self.subTest(case=x):
                self.assertEqual(algorithm(x), (x,))
 

    def test_simple_numbers(self):
        """
        Для простых чисел 3, 13, 29 возвращается кортеж, содержащий одно данное число.
        """
        cases = (3, 13, 29)

        for x in cases:    
            with self.subTest(case=x):
                self.assertEqual(algorithm(x), (x,))

    def test_two_simple_multipliers(self):
        """
        Для чисел 6, 26, 121 возвращаются соответственно кортежи (2, 3), (2, 13) и (11, 11).
        """
        cases = (
                    (6, (2, 3)),
                    (26, (2, 13)),
                    (121, (11, 11))
                )

        for case in cases: 
            x, result = case
            with self.subTest(case=x):
                self.assertEqual(algorithm(x), result)

    def test_many_multipliers(self):
        """
        Для чисел 1001 и 9699690 возвращаются соответственно кортежи (7, 11, 13) и (2, 3, 5, 7, 11, 13, 17, 19).
        """
        cases = (
                    (1001, (7, 11, 13)),
                    (9699690, (2, 3, 5, 7, 11, 13, 17, 19))
                )

        for case in cases: 
            x, result = case
            with self.subTest(case=x):
                self.assertEqual(algorithm(x), result)


def factorize_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestFactorize('test_wrong_types_raise_exception'))
    suite.addTest(TestFactorize('test_negative'))
    suite.addTest(TestFactorize('test_zero_and_one_cases'))
    suite.addTest(TestFactorize('test_simple_numbers'))
    suite.addTest(TestFactorize('test_two_simple_multipliers'))
    suite.addTest(TestFactorize('test_many_multipliers'))
    return suite

if True: #__name__ == "__main__":
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)

    algo = factorize

    print('Testing function ', algo.__doc__.strip())
    test_suite = factorize_test_suite()
    algorithm = algo
    runner.run(test_suite)