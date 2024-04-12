from abc import ABC
from nltk.corpus import stopwords

stops = stopwords.words('english')

class Medicine(ABC):
    def __init__(self, name, prescribed_for):
        self.name = name
        self.prescribed_for = prescribed_for
        self.__reduce_text()

    def __reduce_text(self):
        self.prescribed_for = [i for i in self.prescribed_for.split() if i not in stops]


    def __str__(self):
        return f'{self.name} :  {self.prescribed_for}'
    def __repr__(self):
        return self.__str__()


