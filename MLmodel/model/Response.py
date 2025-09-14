import numpy

class Response:
    def __init__(self, prediction: numpy.ndarray):
        self.__prediction = prediction
        self.saludo = "hola"

    @property
    def prediction(self):
        return self.__prediction

    @prediction.setter
    def prediction(self, value):
        self._prediction = value

    def __str__(self):
        rounded = numpy.round(self.__prediction, 3) #3 decimales
        return f"Response(prediction={rounded}, saludo={self.saludo})"