import logging
import os
import shutil

from fastapi import APIRouter, UploadFile, Form, File
from starlette.responses import JSONResponse

from translator import PATH
from translator.models import *
from translator.services.srt_service import SrtService
from translator.services.translator_subtitles import TranslatorSubtitles
from translator.services.translator_text import TranslatorText, get_sentences_from_text

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/translate_text", response_model=TranslateTextResponse)
def translate_text(request: TranslateTextRequest):
    translator_text = TranslatorText(
        request.source_language,
        request.target_language,
        request.translator
    )

    try:
        translated_text = translator_text.translate_text(get_sentences_from_text(request.text))
        return TranslateTextResponse(translated_text=" ".join(translated_text))

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post("/translate_subtitles", response_model=TranslateSubtitlesResponse)
def translate_subtitles(request: TranslateSubtitlesRequest):
    translator_subtitles = TranslatorSubtitles(
        request.source_language,
        request.target_language,
        request.translator
    )

    try:
        segments = SrtService.get_segments_from_content(request.subtitles)
        translated_segments = translator_subtitles.translate(segments)
        translated_subtitles = SrtService.segments_to_srt(translated_segments)

        return TranslateSubtitlesResponse(translated_subtitles=translated_subtitles)

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post("/translate_subtitles_file", response_model=TranslateSubtitlesResponse)
def translate_subtitles_file(file: UploadFile = File(...),
                             source_language: SupportedLanguages = Form(...),
                             target_language: SupportedLanguages = Form(...),
                             translator: SupportedTranslators = Form("yandex")):
    resources_path = os.path.join(PATH, "services", "resources")

    if not os.path.exists(resources_path):
        os.makedirs(resources_path)

    file_path = os.path.join(resources_path, file.filename)
    translator_subtitles = TranslatorSubtitles(source_language, target_language, translator)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    try:
        segments = SrtService.get_segments_from_srt_file(file_path)
        translated_segments = translator_subtitles.translate(segments)
        translated_subtitles = SrtService.segments_to_srt(translated_segments)

        return TranslateSubtitlesResponse(translated_subtitles=translated_subtitles)

    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content={"message": str(e)})

    finally:
        if os.path.exists(resources_path):
            shutil.rmtree(resources_path)


@router.get("/supported_languages", response_model=SupportedLanguagesResponse)
def get_supported_languages():
    return SupportedLanguagesResponse(supported_languages=[lang for lang in SupportedLanguages])


@router.get("/supported_translators", response_model=SupportedTranslatorsResponse)
def get_supported_translators():
    return SupportedTranslatorsResponse(supported_translators=[translator for translator in SupportedTranslators])
