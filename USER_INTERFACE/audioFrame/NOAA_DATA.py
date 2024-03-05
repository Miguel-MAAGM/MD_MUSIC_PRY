import requests
BASE_URL ="https://www.ndbc.noaa.gov/data/realtime2/"
DATA_TYPE_Height  =".dart"


def get_dataNOAA(Name):
    url=BASE_URL+Name+DATA_TYPE_Height

    try:
        response = requests.get(url)
        response.raise_for_status()  # Comprueba si hubo errores en la solicitud HTTP
        text_data = response.text  # Obtiene el contenido de la página web en formato de texto
        lineas = text_data.split('\n')
        lineas= lineas[2:]
        datos = []
        # Recorrer las líneas e imprimir la fecha y la hora
        for linea in lineas:
            if (len(linea) > 15):  # Asegurarse de que la línea tiene suficientes caracteres
                    fecha = f"{linea[0:4]}-{linea[5:7]}-{linea[8:10]}"
                    hora =f"{linea[11:13]}:{linea[14:16]}"
                    altura = linea[21:21+9]
                    altura_m=float(altura)
                    datos.append((fecha,hora,altura_m))            
                

        # Imprime el texto obtenido
        return datos
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")
        return False
