import json
import random
from datetime import datetime, timedelta
import uuid

# Salidas y entradas
input_file_users = "users.json"
input_file_books = "books.json"
input_file_environments = "environments.json"
output_file_reservations = "reservations.json"

# Lista de tenants
tenants = ["utec", "upn", "bnp", "unmsm", "uni", "upch"]

# Tiempos de reserva de libros
reserve_times = {
    "utec": 4,
    "upn": 3,
    "bnp": 3,
    "unmsm": 2,
    "uni": 2,
    "upch": 3
}

# Cargar usuarios, libros y ambientes
with open(input_file_users, "r", encoding="utf-8") as user_file:
    users = json.load(user_file)

with open(input_file_books, "r", encoding="utf-8") as book_file:
    books = json.load(book_file)

with open(input_file_environments, "r", encoding="utf-8") as book_file:
    environments = json.load(book_file)

# Generar fecha aleatoria desde hace 1 año
def generate_dates(num):
    dates = []
    start_date = datetime.now() - timedelta(days=num)
    for i in range(num):
        dates.append((start_date + timedelta(days=i)).strftime("%Y-%m-%d"))
    return dates
    
# Generar diccionario que separe usuarios por tenant
users_por_tenant = {tenant: [] for tenant in tenants}
for user in users:
    users_por_tenant[user["tenant_id"]].append(user)

# Generar diccionario que separe libros por tenant
books_por_tenant = {tenant: [] for tenant in tenants}
for book in books:
    books_por_tenant[book["tenant_id"]].append(book)

reservations = []
# Reservas de ambientes
for environment in environments:
    tenant = environment['tenant_id']
    # type = environment['type']
    name = environment['name']
    hour = environment['hour']
    capacity = environment['capacity']

    # Reservar esa hora de ese ambiente en 10 dias diferentes del último mes
    dates = random.sample(generate_dates(30), 10)
    for date in dates:
        # Seleccionar un usuario del mismo tenant que el environment
        user = random.choice(users_por_tenant[tenant])
        email = user["email"]

        reservation = {
            "tenant_id#email": f"{tenant}#{email}",
            "res_id": str(uuid.uuid4()),
            "type": "env",
            "status": "pending",
            "tenant_id#type": f"{tenant}#env",
            "email#status": f"{email}#pending",
            "max_return_date#status": "",
            "isbn": "",
            "author_name": "",
            "author_lastname": "",
            "title": "",
            "pickup_date": "",
            "max_return_date": "",
            "env_name": name,
            "date": date,
            "hour": hour,
            "capacity": capacity
        }

        reservations.append(reservation)

# Reservas de libros
for _ in range(50000):
    user = random.choice(users)
    tenant = user["tenant_id"]
    email = user["email"]
    res_id = str(uuid.uuid4())
    start_date = datetime.now() - timedelta(days=random.randint(0, 30))
    pickup_date = start_date.strftime('%d-%m-%Y')
    max_return_date = (start_date + timedelta(days=reserve_times[tenant])).strftime('%d-%m-%Y')
    
    if(start_date + timedelta(days=reserve_times[tenant]) > datetime.now()):
        status = random.choice(["returned", "expired"])
    else:
        status = random.choice(["pending", "returned"])

    book = random.choice(books_por_tenant[tenant])
    isbn = book["isbn"]
    author_name = book["author_name"]
    author_lastname = book["author_lastname"]
    title = book["title"]

    reservation = {
        "tenant_id#email": f"{tenant}#f{email}",
        "res_id": res_id,
        "type": "book",
        "status": status,
        "tenant_id#type": f"{tenant}#book",
        "email#status": f"{email}#{status}",
        "max_return_date#status": f"{max_return_date}#{status}",
        "isbn": isbn,
        "author_name": author_name,
        "author_lastname": author_lastname,
        "title": title,
        "pickup_date": pickup_date,
        "max_return_date": max_return_date,
        "env_name": "",
        "date": "",
        "hour": "",
        "capacity": ""
    }

    reservations.append(reservation)

print(f"Se generaron {len(reservations)} entradas")

# Guardar en reservations.json
with open(output_file_reservations, "w", encoding="utf-8") as outfile:
    json.dump(reservations, outfile, ensure_ascii=False, indent=4)

print(f"Archivo '{output_file_reservations}' generado con éxito.")
