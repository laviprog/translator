import logging
import os
import re

import requests
from deep_translator import GoogleTranslator

from translator.models import SupportedLanguages, SupportedTranslators
from translator.services.exceptions import TranslationRequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_sentences_from_text(text: str) -> list[str]:
    return re.split(r'(?<=[.!?])\s+', text)


class TranslatorText:
    YANDEX_LIMIT = 10000
    GOOGLE_LIMIT = 3000
    _YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")

    def __init__(self,
                 source_language: SupportedLanguages = SupportedLanguages.RUSSIAN,
                 target_language: SupportedLanguages = SupportedLanguages.ENGLISH,
                 translator: SupportedTranslators = SupportedTranslators.YANDEX):
        self._source_language = source_language
        self._target_language = target_language
        self._translator = translator

    def translate_text(self, texts: list[str]) -> list[str]:
        limit = self.YANDEX_LIMIT if self._translator == SupportedTranslators.YANDEX else self.GOOGLE_LIMIT
        return self._join_text(
            [
                (
                    self._translate_yandex(texts)
                    if self._translator == SupportedTranslators.YANDEX
                    else self._translate_google(texts)
                )
                for texts in self._separate_text_from_limit(texts, limit)
            ]
        )

    @staticmethod
    def _separate_text_from_limit(texts: list[str], limit: int) -> list[list[str]]:
        all_sentences = texts
        separated_texts = []

        now_len = 0
        now_sentences = []
        for sentence in all_sentences:
            if len(sentence) + now_len > limit:
                separated_texts.append(now_sentences)
                now_sentences = [sentence]
                now_len = len(sentence)
            else:
                now_sentences.append(sentence)
                now_len += len(sentence)

        if len(now_sentences) > 0:
            separated_texts.append(now_sentences)

        return separated_texts

    @staticmethod
    def _join_text(texts: list[list[str]]) -> list[str]:
        result = []
        for text in texts:
            for sentence in text:
                result.append(sentence)
        return result

    def _translate_yandex(self, text: list[str]) -> list[str]:
        url = "https://translate.api.cloud.yandex.net/translate/v2/translate"

        headers = {
            "Authorization": f"Api-Key {self._YANDEX_API_KEY}"
        }

        data = {
            "sourceLanguageCode": self._source_language,
            "targetLanguageCode": self._target_language,
            "texts": text,
            "speller": True,
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 200:
            raise TranslationRequestException(response.status_code, response.text)

        return [text["text"] for text in response.json()["translations"]]

    def _translate_google(self, texts: list[str]) -> list[str]:

        translator = GoogleTranslator(
            source=self._source_language,
            target=self._target_language
        )

        try:
            return translator.translate_batch(texts)
        except Exception as e:
            raise TranslationRequestException(str(e))
