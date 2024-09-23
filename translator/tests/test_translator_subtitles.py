from translator.services.translator_subtitles import TranslatorSubtitles


def test_separate_sentence():
    sentence = "This is a test sentence"
    number_words_in_segment = [4, 6]

    result = TranslatorSubtitles._separate_sentence(sentence, number_words_in_segment)

    expected_result = ["This is", "a test sentence"]

    assert result == expected_result


def test_collect_segments_from_translated_sentences():
    translated_sentences = ["Hello world!", "This is a test!"]
    sentences_from_segments = {0: [0], 1: [0, 1]}
    sentences_from_segments_number_words = {0: [2], 1: [1, 3]}
    number_segments = 2

    result = TranslatorSubtitles._collect_segments_from_translated_sentences(
        translated_sentences, sentences_from_segments, sentences_from_segments_number_words, number_segments
    )

    expected_result = ["Hello world! This", "is a test!"]

    assert result == expected_result


def test_separate_segments():
    segments = [
        {"text": "Привет! Как дела?", "start": 0.0, "end": 1.0},
        {"text": "Это тест.", "start": 1.0, "end": 2.0}
    ]

    sentences_from_segments, sentences_list, sentences_from_segments_number_words = (
        TranslatorSubtitles._separate_segments(segments))

    expected_sentences_from_segments = {0: [0], 1: [0], 2: [1]}
    expected_sentences_list = ["Привет!", "Как дела?", "Это тест."]
    expected_sentences_from_segments_number_words = {0: [1], 1: [2], 2: [2]}

    assert sentences_from_segments == expected_sentences_from_segments
    assert sentences_list == expected_sentences_list
    assert sentences_from_segments_number_words == expected_sentences_from_segments_number_words


def test_get_translated_segments():
    segments = [
        {"text": "Привет мир!", "start": 0.0, "end": 1.0},
        {"text": "Это тестовое предложение!", "start": 1.0, "end": 2.0},
    ]

    segments_list = ["Hello world!", "This is a test sentence!"]

    result = TranslatorSubtitles._get_translated_segments(segments, segments_list)

    expected_result = [
        {"text": "Hello world!", "start": 0.0, "end": 1.0},
        {"text": "This is a test sentence!", "start": 1.0, "end": 2.0},
    ]

    assert result == expected_result
