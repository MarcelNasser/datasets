import unittest
from unittest.mock import Mock, patch

from pipelines.translate.run import to_list, to_roman, SEPARATOR, integers_enumerate, Translator


class APITranslate(unittest.TestCase):

    letter_b = Mock()
    letter_b.value = "b"
    letter_b.translations = [Mock()]
    letter_b.translations[0].translated_text = "b"
    letter_b.other = {"en": "b", "ar": "ب", "ru": "б"}
    maximum = 20

    def test_roman(self):
        for le in self.letter_b.other.values():
            assert to_roman(le) == self.letter_b.value

    def test_list(self):
        word = SEPARATOR.join(self.letter_b.other.values())
        for le, lt in zip(to_list(word), self.letter_b.other.values()):
            assert le == lt

    def test_enumerate(self):
        assert len(to_list(integers_enumerate(self.maximum))) == self.maximum

    @patch('pipelines.translate.run.Translator.request', return_value=letter_b)
    def test_translator(self, mocked):
        translator = Translator()
        for lg, tx in mocked().other:
            assert translator.translate(lang=lg, text=tx) == self.letter_b.value


if __name__ == '__main__':
    unittest.main()
