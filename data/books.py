import csv
import json
import random
import re

# Lista de tenants, se puede añadir mas
tenants = ["utec", "upn", "bnp", "unmsm", "uni", "upch"]

# Salida
output_file = "books.json"

# Funcion para extraer el primer nombre y apellido del autor
# por temas practicos solo toma el primer autor si es que hay mas de uno
def extract_author_names(author):
    first_author = author.split(",")[0].strip() 
    names = first_author.split()
    if len(names) > 1:
        author_name = names[0]
        author_lastname = " ".join(names[1:])
        
        author_lastname = re.split(r'\s*\(', author_lastname)[0].strip()
        
        return author_name, author_lastname
    else:
        return None, None

# Funcion para numero de paginas, si no hay se inventa un numero
def clean_pages(pages):
    if pages:
        match = re.search(r'\d+', pages)
        if match:
            return int(match.group())
    return random.randint(100, 450)

# Generar un código único de ubicación
def generate_location_code():
    letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Letra aleatoria
    number = random.randint(0, 999)  # Número de hasta 3 dígitos
    return f"{letter}{number}" if number else letter


# Funcion para crear un libro valido, si no hay ciertos campos se omite toda la fila
# Campos obligatorios: isbn, title, author, coverImg(url del cover)
def create_book(entry):
    
    if not entry["isbn"] or entry["isbn"] == "9999999999999" or not entry["title"] or not entry["author"] or not entry["coverImg"]:
        return None

    author_name, author_lastname = extract_author_names(entry["author"])
    if not author_name or not author_lastname:
        return None
    
    # Crea el diccionario del libro
    book = {
        "tenant_id": random.choice(tenants),
        "isbn": entry["isbn"],
        "title": entry["title"],
        "author_name": author_name,
        "author_lastname": author_lastname,
        "pages": clean_pages(entry["pages"]),
        "quantity": random.randint(3, 20),
        "stock": random.randint(1, 15),
        "cover_url": entry["coverImg"],
        "description": entry["description"] if entry["description"] else "Descripción no disponible.",
        "ubicacion": generate_location_code()  # Añadir el código de ubicación
    }
    return book

# Lee el csv y llama a la funcion para crear los libros
books = []
with open("data.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        book = create_book(row)
        if book:  # Solo añadimos el libro si todos los campos obligatorios están presentes
            books.append(book)

# Se escribe todo en un .txt
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(books, outfile, ensure_ascii=False, indent=4)


print(f"Archivo '{output_file}' generado con éxito.")
