import logging
import os
import shlex
import subprocess
import sys

import srt
from srt import Subtitle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SrtService:
    @staticmethod
    def get_segments_from_srt_file(file_path) -> list[dict[str, str]]:
        fixed_file = os.path.join(os.path.dirname(file_path), "fixed_sub.srt")
        try:
            srt_content_list = SrtService._extract_from_srt(file_path)
        except Exception:
            SrtService._run_command(f'ffmpeg -i "{file_path}" "{fixed_file}" -y')
            srt_content_list = SrtService._extract_from_srt(fixed_file)

        return SrtService._make_segments_from_srt(srt_content_list)

    @staticmethod
    def _make_segments_from_srt(list_subtitles: list[Subtitle]) -> list[dict[str, str]]:
        segments = []

        for segment in list_subtitles:
            segments.append(
                {
                    "text": str(segment.content),
                    "start": float(segment.start.total_seconds()),
                    "end": float(segment.end.total_seconds()),
                }
            )

        if not segments:
            raise Exception("No data found in srt subtitle file")

        return segments

    @staticmethod
    def segments_to_srt(segments: list[dict[str, str]]) -> str:
        srt_output = ""
        for i, segment in enumerate(segments, start=1):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]

            if len(text) > 0 and text[0] == ' ':
                text = text[1:]

            def format_time(seconds):
                ms = round((seconds % 1) * 1000)  # Округляем миллисекунды до ближайшего целого
                total_seconds = int(seconds)
                hrs = total_seconds // 3600
                mins = (total_seconds % 3600) // 60
                secs = total_seconds % 60
                return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

            formatted_start = format_time(start)
            formatted_end = format_time(end)
            srt_output += f"{i}\n{formatted_start} --> {formatted_end}\n{text}\n\n"

        return srt_output.strip()

    @staticmethod
    def get_segments_from_content(srt_content):
        return SrtService._make_segments_from_srt(list(srt.parse(srt_content)))

    @staticmethod
    def _read_srt_file(srt_file_path: str) -> str:
        with open(srt_file_path, "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def _extract_from_srt(file_path: str) -> list[Subtitle]:
        return list(srt.parse(SrtService._read_srt_file(file_path)))

    @staticmethod
    def _run_command(command):
        if isinstance(command, str):
            command = shlex.split(command)

        sub_params = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "creationflags": subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        }
        process_command = subprocess.Popen(command, **sub_params)
        output, errors = process_command.communicate()
        if (
                process_command.returncode != 0
        ):
            raise Exception(errors)
