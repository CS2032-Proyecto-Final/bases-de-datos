import json
import random
from datetime import datetime

# Tabla de colores por tenant_id (basado en la imagen proporcionada)
tenant_colors = {
    "uni": "#800020",
    "upch": "#800000",
    "bnp": "#800040",
    "upn": "#ffd966",
    "utec": "#00aaff",
    "unmsm": "#800040"
}

# Función para generar una hora aleatoria dentro del día
def random_time_for_date(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")  # Convertir la fecha a objeto datetime
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    return date.replace(hour=random_hour, minute=random_minute, second=random_second).isoformat()

# Función para generar el archivo JSON de notificaciones
def generate_notifications_file(users_file, output_file):
    # Cargar datos del archivo JSON de usuarios
    with open(users_file, 'r', encoding='utf-8') as file:
        users = json.load(file)
    
    notifications = []  # Lista para almacenar las notificaciones generadas
    
    for user in users:
        # Extraer datos del usuario
        tenant_id = user["tenant_id"]
        email = user["email"]
        firstname = user["firstname"]
        lastname = user["lastname"]
        creation_date = user["creation_date"]
        
        # Crear notificación para el usuario
        notification = {
            "tenant_id": tenant_id,
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
            "creationDate": creation_date,
            "full_name": f"{firstname} {lastname}",
            "color": tenant_colors.get(tenant_id, "#000000"),  # Default color si no existe tenant_id
            "sentAt": random_time_for_date(creation_date)  # Hora aleatoria del mismo día
        }
        
        # Agregar la notificación a la lista
        notifications.append(notification)
    
    # Guardar las notificaciones en el archivo de salida
    with open(output_file, 'w', encoding='utf-8') as output:
        json.dump(notifications, output, ensure_ascii=False, indent=4)
    
    print(f"Archivo generado: {output_file}")

# Llamada a la función con el archivo de entrada y salida
generate_notifications_file('users.json', 'notifications.json')
