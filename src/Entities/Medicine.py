import string
from abc import ABC
from nltk.corpus import stopwords

stops = stopwords.words('english')

class Medicine(ABC):
    def __init__(self, name, prescribed_for: str, side_effects:list[str]):
        self.name = name
        self.prescribed_for = prescribed_for
        self.side_effects = side_effects
        self.__reduce_text()

    def __reduce_text(self):
        self.prescribed_for = [i.lower() for i in self.prescribed_for.split() if i.lower() not in stops]
        self.prescribed_for = [i for i in self.prescribed_for if i not in string.punctuation]

    def treats(self, symptom):
        #return if any word in symptom matches any word in prescribed_for
        return any([sym in self.prescribed_for for sym in symptom.split()])

    def __str__(self):
        return f'{self.name} :  {self.prescribed_for}'
    def __repr__(self):
        return self.__str__()


