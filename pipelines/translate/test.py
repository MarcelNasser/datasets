import unittest
from unittest.mock import MagicMock, Mock, patch

from pipelines.translate.run import to_list, to_roman, separator, integers_enumerate, Translator


class APITranslate(unittest.TestCase):

    letter_b = Mock()
    letter_b.translations = [Mock()]
    letter_b.translations[0].translated_text = "b"
    letter_b.other = {"en": "b", "ar": "ب", "ru": "б"}
    maximum = 20

    def test_roman(self):
        for le in self.letter_b.other.values():
            assert to_roman(le) == "b"

    def test_list(self):
        word = separator.join(self.letter_b.other.values())
        for le, lt in zip(to_list(word), self.letter_b.other.values()):
            assert le == lt

    def test_enumerate(self):
        assert len(to_list(integers_enumerate(self.maximum))) == self.maximum

    @patch('pipelines.translate.run.Translator.request', return_value=letter_b)
    @patch('pipelines.translate.run.Translator.reload')
    def test_translator(self, *mocked):
        translator = Translator()
        for lg, tx in self.letter_b.other:
            assert translator.translate(lang=lg, text=tx) == "b"


if __name__ == '__main__':
    unittest.main()
