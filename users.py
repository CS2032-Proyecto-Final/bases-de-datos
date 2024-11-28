import json
import random
from datetime import datetime, timedelta
from faker import Faker
import hashlib

# Inicializar Faker
fake = Faker()

# Lista de tenants y sus dominios
tenants_domains = {
    "utec": "utec.edu.pe",
    "upn": "upn.edu.pe",
    "bnp": "bnp.com",
    "unmsm": "unmsm.edu.pe",
    "uni": "uni.edu.pe",
    "upch": "upch.pe"
}

# Salida
output_file_users = "users.json"

# Generar fecha de creación aleatoria desde hace un mes hasta hoy
def random_date():
    start_date = datetime.now() - timedelta(days=30)
    random_days = random.randint(0, 30)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

# Generar contraseña hasheada
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Generar datos para 10,000 usuarios
users = []
for _ in range(10000):
    tenant_id = random.choice(list(tenants_domains.keys()))
    domain = tenants_domains[tenant_id]
    
    # Generar datos realistas con Faker
    firstname = fake.first_name()
    lastname = fake.last_name()
    email = f"{firstname.lower()}.{lastname.lower()}@{domain}"
    password = hash_password(fake.password(length=12))  # Contraseña hasheada
    
    user = {
        "tenant_id": tenant_id,
        "email": email,
        "password": password,
        "creation_date": random_date(),
        "firstname": firstname,
        "lastname": lastname,
    }
    users.append(user)

# Guardar en users.json
with open(output_file_users, "w", encoding="utf-8") as outfile:
    json.dump(users, outfile, ensure_ascii=False, indent=4)

print(f"Archivo '{output_file_users}' generado con éxito.")
