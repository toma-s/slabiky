class Word:

    def __init__(self):
        pass


class TextPunctuation(Word):
    """Read -> Clean"""

    def __init__(self, text, punctuation):
        super(Word).__init__()
        self._text = text
        self._punctuation = punctuation

    def __repr__(self):
        # return 'TextPunctuation(\'{}\', {})'.format(self.get_text(), self.get_punctuation())
        representation = ['[']
        for i in range(len(self.get_text())):
            representation.append('(\'{}\': {})'.format(self.get_text()[i], self.get_punctuation()[i]))
            representation.append(', ')
        representation.pop()
        representation.append(']')
        return ''.join(representation)

    def __eq__(self, other):
        if not isinstance(other, TextPunctuation):
            return False
        return self.get_text() == other.get_text() and self.get_punctuation() == other.get_punctuation()

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text

    def get_punctuation(self):
        return self._punctuation

    def set_punctuation(self, punctuation):
        self._punctuation = punctuation


class Text(Word):
    """Clean -> Phonotype"""

    def __init__(self, text):
        super(Word).__init__()
        self._text = text

    def __repr__(self):
        # return 'Text(\'{}\')'.format(self.get_text())
        return '\'{}\''.format(self.get_text())

    def __eq__(self, other):
        if not isinstance(other, Text):
            return False
        return self.get_text() == other.get_text()

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text


class TextPhonotypes(Word):
    """Phonotype -> Syllabify"""

    def __init__(self, text, phonotypes):
        super(Word).__init__()
        self._text = text
        self._phonotypes = phonotypes

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text

    def get_phonotypes(self):
        return self._phonotypes

    def set_phonotypes(self, phonotypes):
        self._phonotypes = phonotypes


class SyllablesPhonotypes(Word):
    """Syllabify -> Count"""

    def __init__(self, syllables, phonotypes):
        super(Word).__init__()
        self._syllables = syllables
        self._phonotypes = phonotypes

    def get_syllables(self):
        return self._syllables

    def set_syllables(self, syllables):
        self._syllables = syllables

    def get_phonotypes(self):
        return self._phonotypes

    def set_phonotypes(self, phonotypes):
        self._phonotypes = phonotypes


class SyllablesLengths(Word):
    """Count -> Result"""

    def __init__(self, syllables, lengths):
        super(Word).__init__()
        self._syllables = syllables
        self._lengths = lengths

    def get_syllables(self):
        return self._syllables

    def set_syllabled(self, syllables):
        self._syllables = syllables

    def get_lengths(self):
        return self._lengths

    def set_lengths(self, lengths):
        self._lengths = lengths
