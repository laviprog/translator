import pytest

from translator.services.translator_text import TranslatorText, get_sentences_from_text


@pytest.fixture
def translator():
    return TranslatorText()


@pytest.fixture
def text():
    return ("Привет! Меня зовут Виктор. "
            "Я создатель этого небольшого проекта, "
            "который может оказаться весьма полезным тем, "
            "кто планирует работать с субтитрами и делать их перевод.")


@pytest.fixture
def sentences():
    return [
        "Привет!",
        "Меня зовут Виктор.",
        "Я создатель этого небольшого проекта, "
        "который может оказаться весьма полезным тем, "
        "кто планирует работать с субтитрами и делать их перевод."
    ]


def test_get_sentences_from_text(text, sentences):
    assert get_sentences_from_text(text) == sentences


def test_separate_text(translator, sentences):
    assert (translator._separate_text_from_limit(sentences, 30)
            == [["Привет!", "Меня зовут Виктор."], ["Я создатель этого небольшого проекта, "
                                                    "который может оказаться весьма полезным тем, "
                                                    "кто планирует работать с субтитрами и делать их перевод."]])

    assert (translator._separate_text_from_limit(["Hello, world!", "I am Runi!"], 30)
            == [["Hello, world!", "I am Runi!"]])
