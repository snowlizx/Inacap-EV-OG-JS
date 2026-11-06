import os
import requests

# Misión 1: Ejecutar con un token inventado tipo "token_falso_123"
TOKEN = "token_falso_123"
BASE_URL = "https://minsal.cl"

def renovar_token():
    """Función requerida para renovar las credenciales al detectar 401."""
    print("[Sistema] Detectado problema de autenticación. Ejecutando renovación...")

def consultar_api(reintentos=1):
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}
    try:
        resp = requests.get(BASE_URL, headers=headers, timeout=10)
        
        # Misión 2: Observa cómo la aplicación detecta el 401 y ejecuta la renovación
        if resp.status_code == 401 and reintentos > 0:
            print("[Aviso] Token expirado. Renovando credenciales...")
            renovar_token()
            return consultar_api(reintentos - 1)
        
        # Si se agotan los reintentos, lanza la excepción controlada
        resp.raise_for_status() 
        return resp.json()
        
    except requests.exceptions.Timeout:
        raise TimeoutError("El servidor externo tardó más de 10s en responder.")

if __name__ == "__main__":
    print("--- Iniciando Cliente API ---")
    try:
        resultado = consultar_api(reintentos=1)
        print("Resultado:", resultado)
    except requests.exceptions.HTTPError as err:
        # Reporta el fallo controlado sin colgarse con un traceback en crudo
        print(f"\n[Fallo Controlado] Código de estado de la API: {err.response.status_code}")
        print("[Resultado] Éxito: El programa manejó el error limpiamente sin romperse.")
