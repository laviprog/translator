import os

import pytest

from translator.services.srt_service import SrtService
from translator.tests import PATH_RESOURCES

path_test_srt_file = os.path.join(PATH_RESOURCES, "test.srt")


@pytest.fixture
def srt_content():
    with open(path_test_srt_file) as f:
        return f.read()


@pytest.fixture
def segments():
    return [{'text': 'Страх и ярость,', 'start': 12.003, 'end': 14.305},
            {'text': 'Храбрость и трусость,', 'start': 14.346, 'end': 16.147},
            {'text': 'Сострадание и жестокость, искренность и притворство.', 'start': 19.141, 'end': 23.978},
            {'text': 'Нам кажется, что это чисто человеческие качества.', 'start': 27.475, 'end': 30.535}]


def test_get_segments_from_content(srt_content, segments):
    assert SrtService.get_segments_from_content(srt_content) == segments


def test_get_segments_from_srt_file(segments):
    assert SrtService.get_segments_from_srt_file(path_test_srt_file) == segments


def test_segments_to_srt(srt_content, segments):
    print(srt_content)
    print(SrtService.segments_to_srt(segments))
    assert SrtService.segments_to_srt(segments) == srt_content
