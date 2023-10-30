"""
Numbers translation calls to Google translate cloud service
"""
import re
from os.path import join
from pathlib import Path
from anyascii import anyascii

import inflect
import argparse

from diskcache import FanoutCache
import sys
from logging import getLogger, basicConfig, ERROR

cache_dir = join(Path(__file__).resolve().parent, '.cache')
cache = FanoutCache(directory=str(cache_dir))
logger = getLogger("translate")
basicConfig(level=ERROR, format="%(levelname)s: %(message)s")
google_project = "tesselite"
separator = "|"


class Translator:
    """
    translation calls to cloud service
    """

    def __init__(self):
        self.client = None

    def hash(self, lang, text):
        """
        custom hash key
        :param lang:
        :param text:
        :return:
        """
        return f"{self.__class__.__name__}{separator}{lang}{separator}{len(text)}"

    def reload(self):
        if not self.client:
            from google.cloud import translate
            self.client = translate.TranslationServiceClient()

    def request(self, lang, text):
        return self.client.translate_text(parent=f"projects/{google_project}/locations/global",
                                          contents=[text],
                                          mime_type="text/plain",
                                          source_language_code="en-US",
                                          target_language_code=lang,
                                          )

    def translate(self, lang, text) -> str:
        """
        :param lang: translate english to 'language'
        :param text: text to translate
        :return: translated text
        """
        # tip: load translation from cache
        translation = cache.get(self.hash(lang, text))
        if translation:
            return translation
        # tip: load client just in time to optim performance
        self.reload()
        response = self.request(lang=lang, text=text)
        translation = ""
        for tr in response.translations:
            translation += tr.translated_text
        cache.set(key=self.hash(lang, text), value=translation)
        return translation


def integers_enumerate(maximum: int) -> str:
    """
    Enumerate numbers in English
    :param maximum: maximum integer without cap
    :return: a serialized list of numbers:: 1 | 2 | 3 | 4 | ... | 99
    """
    engine = inflect.engine()
    text = ""
    for n in range(1, maximum + 1):
        text += engine.number_to_words(n, group=0) + separator + ' '
    return text[:-(len(separator) + 1)]


def to_roman(text: str) -> str:
    """
    Turn entry string to ascii 128-characters
    See library documentation for better understanding
    :return: converted string
    """
    return anyascii(text).replace("  ", "")


def to_list(text: str) -> list:
    """
    Split into a list entry string
    :return: list of numbers
    """
    return re.sub(rf"('\s+[\\{separator}]\s')", separator, text, flags=re.UNICODE).split(separator)


def __integers_list(opt):
    """
    :param opt:
    :return: print to standard output numbers serialized list
    """
    print(integers_enumerate(opt.maximum))


def __integers_translate(opt):
    """
    :param opt:
    :return: print to standard output translated numbers csv,txt or json format
    """
    text = integers_enumerate(opt.maximum)
    translations = {"en": to_list(text)}
    translator = Translator()
    for language in opt.language:
        translations[language] = to_list(to_roman(translator.translate(lang=language, text=text)))
    if opt.output == "json":
        import json
        print(json.dumps(translations))
    elif opt.output == "csv":
        import pandas
        df = pandas.DataFrame(data=translations)
        df.to_csv(sys.stdout, sep=',', index=False, lineterminator='\n')
    else:
        from tabulate import tabulate
        print(tabulate(translations, headers="keys"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="scripts")
    subparsers = parser.add_subparsers(help="select the action's command")
    sub_1 = subparsers.add_parser("list", help="list integer in english")
    sub_1.add_argument("--maximum", "-m", help=f"list integers up to this maximum", nargs="?", type=int, default=99)
    sub_1.set_defaults(func=__integers_list)
    sub_2 = subparsers.add_parser("translate", help="translate integer list")
    sub_2.add_argument("--maximum", "-m", help=f"list integers up to this maximum", nargs="?", type=int, default=99)
    sub_2.add_argument("--language", "-l", help=f"destination language", nargs="+", type=str, default=[])
    sub_2.add_argument("--output", "-o", help=f"output format", type=str,
                       choices=["text", "csv", "json"], default="text")

    sub_2.set_defaults(func=__integers_translate)
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    try:
        args.func(args)
    except Exception as e:
        raise e
