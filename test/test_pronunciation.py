from unittest import TestCase, main

from ko_pron import romanise


def mr_romanize(word):
    return romanise(word, "mr")


class TestKoPron(TestCase):
    def test_kosinga(self):
        self.assertEqual("kŏsin'ga", mr_romanize("것인가"))

    def test_kosida(self):
        self.assertEqual("kŏsida", mr_romanize("것이다"))


if __name__ == '__main__':
    main()
