import logging
import re

from translator.models import SupportedLanguages, SupportedTranslators
from translator.services.translator_text import TranslatorText

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TranslatorSubtitles:

    def __init__(self,
                 source_language: SupportedLanguages = SupportedLanguages.RUSSIAN,
                 target_language: SupportedLanguages = SupportedLanguages.ENGLISH,
                 translator: SupportedTranslators = SupportedTranslators.YANDEX):
        self._translator_text = TranslatorText(source_language, target_language, translator)

    def translate(self, segments: list[dict[str, str]]) -> list[dict[str, str]]:
        sentences_from_segments, sentences_list, sentences_from_segments_number_words = self._separate_segments(
            segments)

        translated_text = self._translator_text.translate_text(sentences_list)

        return self._get_translated_segments(
            segments,
            self._collect_segments_from_translated_sentences(
                translated_text,
                sentences_from_segments,
                sentences_from_segments_number_words,
                len(segments)
            )
        )

    @staticmethod
    def _separate_sentence(sentence: str, number_words_in_segment: list[int]) -> list[str]:
        words = sentence.split()
        total_words = len(words)
        total_proportion = sum(number_words_in_segment)

        sizes = [round((p / total_proportion) * total_words) for p in number_words_in_segment]

        if sum(sizes) != total_words:
            sizes[-1] += total_words - sum(sizes)

        result = []
        start = 0

        for size in sizes:
            end = start + size
            result.append(" ".join(words[start:end]))
            start = end

        return result

    @staticmethod
    def _collect_segments_from_translated_sentences(
            translated_sentences: list[str],
            sentences_from_segments: dict[int, list[int]],
            sentences_from_segments_number_words: dict[int, list[int]],
            number_segments: int
    ) -> list[str]:

        segments = [""] * number_segments

        for i, sentence in enumerate(translated_sentences):
            separated_sentence = TranslatorSubtitles._separate_sentence(sentence, sentences_from_segments_number_words[i])
            for part, segment in zip(separated_sentence, sentences_from_segments[i]):
                segments[segment] += (" " if segments[segment] != "" else "") + part
        return segments

    @staticmethod
    def _get_translated_segments(segments: list[dict[str, str]], segments_list: list[str]) -> list[dict[str, str]]:
        for i, segment in enumerate(segments):
            segment["text"] = segments_list[i]
        return segments

    @staticmethod
    def _separate_segments(segments: list[dict[str, str]]):
        current_sentence = ""
        sentences_list = []
        current_segments_list = []
        current_segments_number_words_list = []
        segments_counter = 0
        sentences_counter = 0
        sentences_from_segments = {}
        sentences_from_segments_number_words = {}

        for segment in segments:
            current_text = segment['text'].replace("...", ".")
            words = [word for word in re.split(r"([.!?])", current_text) if word != ""]

            for word in words:
                word = word.strip()
                if segments_counter not in current_segments_list:
                    current_segments_list.append(segments_counter)
                if word in ".!?":
                    current_sentence += word
                    sentences_list.append(current_sentence)
                    sentences_from_segments[sentences_counter] = current_segments_list
                    sentences_from_segments_number_words[sentences_counter] = current_segments_number_words_list
                    current_segments_number_words_list = []
                    sentences_counter += 1
                    current_sentence = ""
                    current_segments_list = []

                else:
                    current_segments_number_words_list.append(len(word.split()))
                    if current_sentence != "":
                        current_sentence += " " + word
                    else:
                        current_sentence += word
            segments_counter += 1

        return sentences_from_segments, sentences_list, sentences_from_segments_number_words
