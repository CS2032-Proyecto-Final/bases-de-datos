#!/bin/bash

# Listado de scripts a ejecutar
scripts=(
  "books.py"
  "users.py"
  "environments.py"
  "favorites.py"
  "notifications.py"
  "reservations.py"
)

# Ejecutar cada script
for script in "${scripts[@]}"; do
  echo "Ejecutando $script..."
  python "$script"
  if [ $? -ne 0 ]; then
    echo "Error al ejecutar $script. Saliendo..."
    exit 1
  fi
done

echo "Todos los scripts se ejecutaron correctamente."
