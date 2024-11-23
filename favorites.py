import json
import random

# Salidas y entradas
input_file_users = "users.json"
input_file_books = "books.json"
output_file_favorites = "favorites.json"

# Lista de tenants
tenants = ["utec", "upn", "bnp", "unmsm", "uni", "upch"]

# Cargar usuarios y libros
with open(input_file_users, "r", encoding="utf-8") as user_file:
    users = json.load(user_file)

with open(input_file_books, "r", encoding="utf-8") as book_file:
    books = json.load(book_file)

# Separar libros en una matriz por tenant
books_by_tenant = {tenant: [] for tenant in tenants}
for book in books:
    books_by_tenant[book["tenant_id"]].append(book)

# Crear favoritos asegurando que coincidan tenant_id
favorites = []
for _ in range(50000):
    user = random.choice(users)
    tenant_id = user["tenant_id"]
    email = user["email"]
    
    # Obtener libros del tenant correspondiente
    tenant_books = books_by_tenant.get(tenant_id, [])
    if not tenant_books:
        continue

    book = random.choice(tenant_books)
    isbn = book["isbn"]
    
    favorite = {
        "tenant_id": tenant_id,
        "email#isbn": f"{email}#{isbn}",
        "isFavorite": random.choice([True, False])
    }
    favorites.append(favorite)

# Guardar en favorites.json
with open(output_file_favorites, "w", encoding="utf-8") as outfile:
    json.dump(favorites, outfile, ensure_ascii=False, indent=4)

print(f"Archivo '{output_file_favorites}' generado con éxito.")
