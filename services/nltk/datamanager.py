import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from services.file.file_processor import FileProcessor
import asyncio


class DataManager:
    def __init__(self, processor: FileProcessor):
        self.data = processor.get_data()
        self.language_for_llm = self._normalize_language(self.data["language"])

        self.key_words = None
        self.summary = None
        self.language = self.data["language"]
        self.file_name = self.data["file_name"]
        self.file_size = self.data["file_size"]
        self.file_type = self.data["file_type"]

    def _normalize_language(self, lang: str) -> str:
        return {
            "ru": "russian",
            "en": "english"
        }.get(lang, "english")

    async def extract_keywords(self):
        stop_words = set(stopwords.words(self.language_for_llm))
        words = await asyncio.to_thread(word_tokenize, self.data["text"])
        self.key_words = [
            word.lower()
            for word in words
            if word.isalnum() and word.lower() not in stop_words
        ]

    async def summarize_text(self, sentences_count: int = 2):
        stop_words = set(stopwords.words(self.language_for_llm))
        sentences = await asyncio.to_thread(sent_tokenize, self.data["text"], language=self.language_for_llm)

        if len(sentences) <= sentences_count:
            self.summary = self.data["text"]
            return

        words = [w.lower() for w in await asyncio.to_thread(word_tokenize, self.data["text"]) if w.isalnum() and w.lower() not in stop_words]
        freq = Counter(words)

        sentence_scores = {}
        for sentence in sentences:
            for word in await asyncio.to_thread(word_tokenize, sentence.lower()):
                if word in freq:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + freq[word]

        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:sentences_count]
        top_set = set(top_sentences)
        self.summary = " ".join([s for s in sentences if s in top_set])

    async def run(self):
        await asyncio.gather(
            self.summarize_text(),
            self.extract_keywords()
        )
