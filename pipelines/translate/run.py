"""
Numbers translation calls to Google translate cloud service
"""
import os
import re
from os.path import join
from pathlib import Path
from anyascii import anyascii
import hashlib

import inflect
import argparse

from diskcache import FanoutCache
import sys
from logging import getLogger, basicConfig, ERROR

cache_dir = join(Path(__file__).resolve().parent, '.cache')
cache = FanoutCache(directory=str(cache_dir))
logger = getLogger("translate")
basicConfig(level=ERROR, format="%(levelname)s: %(message)s")
SEPARATOR = "|"


class Translator:
    """
    translation calls to cloud service
    """

    def __init__(self):
        self.client = None

    def hash(self, lang: str, text: str) -> str:
        """
        map translation information towards a unique string
        :param lang: translate english to 'language'
        :param text: text to translate
        :return: hash equivalent string
        """
        __hash = hashlib.md5(lang.encode())
        __hash.update(text.encode())
        __hash.update(self.__class__.__name__.encode())
        return __hash.hexdigest()

    def reload(self):
        """
        Lazy loading of client lib to optimize performance
        :return:
        """
        if not self.client:
            from google.cloud import translate
            self.client = translate.TranslationServiceClient()

    def request(self, lang: str, text: str):
        """
        Wrap client request for unittest without network
        :param lang:
        :param text:
        :return: iterable object
        """
        # tip: load client just in time to optim performance
        self.reload()
        # load billing "project" in google cloud
        google_project = os.environ.get("GOOGLE_PROJECT")
        if google_project is None:
            logger.error("env variable 'GOOGLE_PROJECT' is not set.")
            exit(1)
        return self.client.translate_text(parent=f"projects/{google_project}/locations/global",
                                          contents=[text],
                                          mime_type="text/plain",
                                          source_language_code="en-US",
                                          target_language_code=lang,
                                          )

    def translate(self, lang: str, text: str) -> str:
        """
        :param lang: translate english to 'language'
        :param text: text to translate
        :return: translated text
        """
        # tip: load translation from cache
        translation = cache.get(self.hash(lang, text))
        if translation:
            return translation

        response = self.request(lang=lang, text=text)
        translation = ""
        for tr in response.translations:
            translation += tr.translated_text
        cache.set(key=self.hash(lang, text), value=translation)
        return translation


def serialize(maximum: int) -> str:
    """
    Enumerate numbers in English
    :param maximum: maximum integer without cap
    :return: a serialized list of numbers:: 1 | 2 | 3 | 4 | ... | 99
    """
    engine = inflect.engine()
    text = ""
    for n in range(1, maximum + 1):
        text += engine.number_to_words(n, group=0) + SEPARATOR + ' '
    return text[:-(len(SEPARATOR) + 1)]


def to_roman(text: str) -> str:
    """
    Turn entry string to ascii 128-characters
    See library documentation for better understanding
    :return: converted string
    """
    return anyascii(text).replace("  ", "")


def deserialize(text: str) -> list:
    """
    Split into a list entry string
    :return: list of numbers
    """
    return re.sub(rf"('\s+[\\{SEPARATOR}]\s')", SEPARATOR, text, flags=re.UNICODE).split(SEPARATOR)


def __integers_list(opt):
    """
    :param opt:
    :return: print to standard output numbers serialized list
    """
    print(serialize(opt.maximum))


def __integers_translate(opt):
    """
    :param opt:
    :return: print to standard output translated numbers csv,txt or json format
    """
    text = serialize(opt.maximum)
    translations = {"en": deserialize(text)}
    translator = Translator()
    for language in opt.language:
        translations[language] = deserialize(to_roman(translator.translate(lang=language, text=text)))
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
    sub_1.add_argument("--maximum", "-m",
                       help="list integers up to this maximum", nargs="?",
                       type=int, default=99)
    sub_1.set_defaults(func=__integers_list)
    sub_2 = subparsers.add_parser("translate", help="translate integer list")
    sub_2.add_argument("--maximum", "-m",
                       help="list integers up to this maximum", nargs="?",
                       type=int, default=99)
    sub_2.add_argument("--language", "-l",
                       help="destination language", nargs="+", type=str, default=[])
    sub_2.add_argument("--output", "-o", help="output format", type=str,
                       choices=["text", "csv", "json"], default="text")

    sub_2.set_defaults(func=__integers_translate)
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    try:
        args.func(args)
    except Exception as e:
        raise e
