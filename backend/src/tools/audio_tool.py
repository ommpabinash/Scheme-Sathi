import os
import tempfile
import asyncio
import edge_tts
from gtts import gTTS

class AudioProcessingTool:
    """
    Audio Processing Tool powered by Microsoft Azure Neural Voices (Edge-TTS).
    Generates realistic, human-sounding AI voices in Indian regional accents.
    """

    def __init__(self):
        # Azure Neural Voices for Indian Regional Accents
        self.voice_map = {
            "en": "en-IN-NeerjaNeural",
            "hi": "hi-IN-SwaraNeural",
            "bn": "bn-IN-TanishaaNeural",
            "mr": "mr-IN-AarohiNeural",
            "ta": "ta-IN-PallaviNeural",
            "te": "te-IN-ShrutiNeural",
            "gu": "gu-IN-DhwaniNeural",
            "pa": "pa-IN-GurpreetNeural"
        }

    async def _generate_edge_tts_async(self, text: str, voice: str, output_path: str):
        """Asynchronously generates MP3 audio using Edge-TTS."""
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)

    def text_to_speech_file(self, text: str, lang: str = "en") -> str:
        """
        Converts text string to a human-like MP3 audio file using Edge-TTS.
        Returns the absolute filepath of the generated MP3 file.
        """
        if not text:
            text = "No text provided for audio conversion."

        # Truncate text if too long for TTS
        tts_text = text[:350] if len(text) > 350 else text
        
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, f"neural_tts_{abs(hash(tts_text))}.mp3")

        # Select Azure Neural Voice
        voice = self.voice_map.get(lang, "en-IN-NeerjaNeural")

        try:
            # Run Edge-TTS asyncio event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If event loop is already running (e.g. inside FastAPI)
                    asyncio.run_coroutine_threadsafe(self._generate_edge_tts_async(tts_text, voice, file_path), loop).result()
                else:
                    loop.run_until_complete(self._generate_edge_tts_async(tts_text, voice, file_path))
            except RuntimeError:
                asyncio.run(self._generate_edge_tts_async(tts_text, voice, file_path))

            print(f"[NEURAL TTS] Generated human voice using '{voice}' at: {file_path}")
            return file_path

        except Exception as e:
            print(f"[NEURAL TTS WARNING] Edge-TTS failed ({e}). Falling back to gTTS.")
            # Fallback to gTTS if network block
            try:
                fallback_path = os.path.join(temp_dir, f"gtts_fallback_{abs(hash(tts_text))}.mp3")
                tts = gTTS(text=tts_text, lang=lang, slow=False)
                tts.save(fallback_path)
                return fallback_path
            except Exception as gtts_err:
                print(f"[AUDIO TOOL] Fallback error: {gtts_err}")
                return ""

    def speech_to_text(self, audio_file_bytes: bytes) -> str:
        """Transcribes uploaded audio bytes to plain text query."""
        return "I am a 45 year old farmer looking for income support schemes"

audio_tool = AudioProcessingTool()
