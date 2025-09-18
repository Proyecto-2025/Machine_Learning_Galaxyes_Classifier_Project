from pyexpat import features

import numpy

features_map = {
    0: "SUAVE",
    1: "CON CARACTERISTICAS O DISCO",
    2: "ESTRELLA O ARTEFACTO",
    3: "VISTA DE PERFIL",
    4: "NO VISTA DE PERFIL",
    5: "BARRA ATRAVESANDO EL CENTRO DE LA GALAXIA",
    6: "SIN BARRA EN EL CENTRO",
    7: "CON PATRON DE BRAZOS ESPIRALES",
    8: "SIN PATRON DE BRAZOS ESPIRALES",
    9: "SIN BULTO CENTRAL",
    10: "BULTO CENTRAL APENAS PERCEPTIBLE",
    11: "BULTO CENTRAL OBVIO",
    12: "BULTO CENTRAL DOMINANTE",
    13: "HAY ALGO EXTRAÑO (ODD)",
    14 : "NO HAY NADA EXTRAÑO (ODD)",
    15: "COMPLETAMENTE REDONDA",
    16: "MEDIANAMENTE REDONDA",
    17: "FORMA DE CIGARRO",
    18: "ANILLO",
    19: "LENTE O ARCO",
    20: "PERTURBADA",
    21: "IRREGULAR",
    22: "OTRA",
    23: "FUSION",
    24: "BANDA DE POLVO",
    25: "BULTO REDONDEADO",
    26: "BULTO CUADRADO (BOXY)",
    27: "SIN BULBO",
    28: "BRAZOS ESPIRALES MUY APRETADOS",
    29: "BRAZOS ESPIRALES MEDIANAMENTE APRETADOS",
    30: "BRAZOS ESPIRALES SUELTOS",
    31: "1 BRAZO ESPIRAL",
    32: "2 BRAZOS ESPIRALES",
    33: "3 BRAZOS ESPIRALES",
    34: "4 BRAZOS ESPIRALES",
    35: "MAS DE 4 BRAZOS ESPIRALES",
    36: "NO SE PUEDEN CONTAR LOS BRAZOS ESPIRALES"
}

class Response:
    def __init__(self, prediction: numpy.ndarray):
        self.__prediction = prediction
        self.__features = []
        self.map_features()

    @property
    def prediction(self):
        return self.__prediction

    @prediction.setter
    def prediction(self, value):
        self.__prediction = value

    def __str__(self):
        rounded = numpy.round(self.__prediction, 3) #3 decimales
        return f"Response(prediction={rounded}, features = {self.__features})"

    def map_features(self):
        self.__features = [] #limpiar la lista por las dudas
        for key in features_map:
            if self.__prediction[key] > 0.5:
                self.__features.append(features_map[key])