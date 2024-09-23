from enum import Enum
from typing import List

from pydantic import BaseModel


class SupportedLanguages(str, Enum):
    AFRIKAANS = "af"
    AMHARIC = "am"
    ARABIC = "ar"
    AZERBAIJANI = "az"
    BELARUSIAN = "be"
    BULGARIAN = "bg"
    BENGALI = "bn"
    BOSNIAN = "bs"
    CATALAN = "ca"
    CEBUANO = "ceb"
    CZECH = "cs"
    WELSH = "cy"
    DANISH = "da"
    GERMAN = "de"
    GREEK = "el"
    ENGLISH = "en"
    ESPERANTO = "eo"
    SPANISH = "es"
    ESTONIAN = "et"
    BASQUE = "eu"
    PERSIAN = "fa"
    FINNISH = "fi"
    FRENCH = "fr"
    IRISH = "ga"
    SCOTS = "gd"
    GALICIAN = "gl"
    GUJARATI = "gu"
    HINDI = "hi"
    CROATIAN = "hr"
    HAITIAN = "ht"
    HUNGARIAN = "hu"
    ARMENIAN = "hy"
    INDONESIAN = "id"
    ICELANDIC = "is"
    ITALIAN = "it"
    JAPANESE = "ja"
    GEORGIAN = "ka"
    KAZAKH = "kk"
    KHMER = "km"
    KANNADA = "kn"
    KOREAN = "ko"
    KYRGYZ = "ky"
    LATIN = "la"
    LUXEMBOURGISH = "lb"
    LAO = "lo"
    LITHUANIAN = "lt"
    LATVIAN = "lv"
    MALAGASY = "mg"
    MAORI = "mi"
    MACEDONIAN = "mk"
    MALAYALAM = "ml"
    MONGOLIAN = "mn"
    MARATHI = "mr"
    MALAY = "ms"
    MALTESE = "mt"
    MYANMAR = "my"
    NEPALI = "ne"
    DUTCH = "nl"
    NORWEGIAN = "no"
    PUNJABI = "pa"
    POLISH = "pl"
    PORTUGUESE = "pt"
    ROMANIAN = "ro"
    RUSSIAN = "ru"
    SINHALA = "si"
    SLOVAK = "sk"
    SLOVENIAN = "sl"
    ALBANIAN = "sq"
    SERBIAN = "sr"
    SUNDANESE = "su"
    SWEDISH = "sv"
    SWAHILI = "sw"
    TAMIL = "ta"
    TELUGU = "te"
    TAJIK = "tg"
    THAI = "th"
    TAGALOG = "tl"
    TURKISH = "tr"
    TATAR = "tt"
    UKRAINIAN = "uk"
    URDU = "ur"
    UZBEK = "uz"
    VIETNAMESE = "vi"
    XHOSA = "xh"
    YIDDISH = "yi"
    ZULU = "zu"


class SupportedTranslators(str, Enum):
    YANDEX = "yandex"
    GOOGLE = "google"
    # LLM = "llm-1"
    # GPT = "GPT-4o"


class TranslateTextRequest(BaseModel):
    text: str
    source_language: SupportedLanguages
    target_language: SupportedLanguages
    translator: SupportedTranslators = "yandex"


class TranslateSubtitlesRequest(BaseModel):
    subtitles: str
    source_language: SupportedLanguages
    target_language: SupportedLanguages
    translator: SupportedTranslators = "yandex"


class TranslateTextResponse(BaseModel):
    translated_text: str


class TranslateSubtitlesResponse(BaseModel):
    translated_subtitles: str


class SupportedLanguagesResponse(BaseModel):
    supported_languages: List[SupportedLanguages]


class SupportedTranslatorsResponse(BaseModel):
    supported_translators: List[SupportedTranslators]