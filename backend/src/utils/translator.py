import sys
from typing import List
from deep_translator import GoogleTranslator

# deep-translator (GoogleTranslator) has a hard limit of 5000 chars per request.
GOOGLE_TRANSLATE_LIMIT = 4500  # conservative limit


def safe_print(msg: str):
    """Windows CP1252-safe print that strips non-ASCII characters for logging."""
    try:
        print(msg)
    except UnicodeEncodeError:
        safe_msg = msg.encode("ascii", errors="replace").decode("ascii")
        print(safe_msg)


class MultilingualTranslator:
    """
    Multilingual Translator using deep-translator (GoogleTranslator).
    Supports: hi, bn, mr, pa, ta, te, gu, en.
    Handles batch translations to prevent Google Translate rate-limiting (Error 500).
    """

    def __init__(self):
        self.supported_langs = {
            "en": "English",  # Allowed as target (for regional → English translation)
            "hi": "Hindi",
            "bn": "Bengali",
            "mr": "Marathi",
            "pa": "Punjabi",
            "ta": "Tamil",
            "te": "Telugu",
            "gu": "Gujarati"
        }

    def _translate_chunk(self, text: str, target_lang: str) -> str:
        """Translate a single chunk (must be under char limit)."""
        return GoogleTranslator(source="auto", target=target_lang).translate(text)

    def translate_text(self, text: str, target_lang: str = "hi") -> str:
        """
        Translates English text into the target regional language.
        Automatically splits long text into chunks to handle the 5000-char limit.
        Returns original text if translation fails or gets rate-limited.
        """
        if not text:
            return text
        if target_lang not in self.supported_langs:
            return text

        text = text.strip()

        try:
            # Short text — single call
            if len(text) <= GOOGLE_TRANSLATE_LIMIT:
                result = self._translate_chunk(text, target_lang)
                if result:
                    # Check for rate-limiting HTML page returned as string
                    low_res = result.lower()
                    if "error 500" in low_res or "that’s an error" in low_res or "there was an error" in low_res:
                        safe_print("[TRANSLATOR] Caught Google Translate rate-limit page. Falling back to input.")
                        return text
                    
                    safe_print(f"[TRANSLATOR] OK -> lang={target_lang}, len={len(result)}")
                    return result
                return text

            # Chunked translation for long summaries
            safe_print(f"[TRANSLATOR] Long text ({len(text)} chars), splitting into chunks...")
            chunks = []
            sentences = text.replace(". ", ".|").split("|")
            current_chunk = ""

            for sentence in sentences:
                if len(current_chunk) + len(sentence) < GOOGLE_TRANSLATE_LIMIT:
                    current_chunk += sentence + " "
                else:
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + " "
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            translated_chunks = []
            for i, chunk in enumerate(chunks):
                translated_chunk = self._translate_chunk(chunk, target_lang)
                
                # Check rate-limit
                low_chunk = (translated_chunk or "").lower()
                if "error 500" in low_chunk or "that’s an error" in low_chunk:
                    translated_chunks.append(chunk)
                else:
                    translated_chunks.append(translated_chunk if translated_chunk else chunk)
                
                safe_print(f"[TRANSLATOR] Chunk {i+1}/{len(chunks)} done.")

            return " ".join(translated_chunks)

        except Exception as e:
            safe_print(f"[TRANSLATOR] ERROR for lang='{target_lang}': {e}")
            return text  # graceful fallback to original English

    def translate_batch(self, strings: List[str], target_lang: str = "hi") -> List[str]:
        """
        Translates a list of strings in a SINGLE HTTP request using a delimiter.
        This prevents Google Translate from rate-limiting the backend (Error 500).
        """
        if not strings:
            return []
        if target_lang == "en" or target_lang not in self.supported_langs:
            return strings

        # Clean strings and handle empty items
        cleaned_strings = [s.strip() if s else "" for s in strings]
        
        # We use a unique line delimiter that Google Translate preserves
        delimiter = "\n###\n"
        combined_text = delimiter.join(cleaned_strings)
        
        try:
            translated_combined = self.translate_text(combined_text, target_lang=target_lang)
            
            # If the translation returned the error message, return original list
            low_comb = translated_combined.lower()
            if "error 500" in low_comb or "that’s an error" in low_comb or "there was an error" in low_comb:
                safe_print("[TRANSLATOR] Batch translation hit Google rate-limit page. Bypassing translation.")
                return strings
                
            # Split the translated text back into list items
            parts = translated_combined.split("###")
            parts = [p.strip() for p in parts]
            
            if len(parts) == len(strings):
                return parts
                
            safe_print(f"[TRANSLATOR] Batch parts mismatch: expected {len(strings)}, got {len(parts)}. Falling back to individual translation.")
        except Exception as e:
            safe_print(f"[TRANSLATOR] Batch translation failed: {e}. Falling back.")
            
        # Fallback to translating individual strings
        return [self.translate_text(s, target_lang=target_lang) for s in strings]


translator = MultilingualTranslator()
