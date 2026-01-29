import re
class StringUtils:
    @staticmethod
    def normalize(word: str):
        regex_pattern = r'[”“()_`\'"\n]'
        cleaned = re.sub(regex_pattern, "", word)

        # if cleaned.isupper() and len(cleaned) > 0:
        #     return cleaned[0].upper() + cleaned[1:].lower()

        return cleaned

    @staticmethod
    def substring(word: str, delimiter: str):
        regex_pattern = fr"[{delimiter}]"
        return re.split(regex_pattern, word)[0]