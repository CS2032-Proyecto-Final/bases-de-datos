import json
import random

# Definir tenants y tipos de entornos por tenant
tenants = {
    "uni": [{"S": "salas_de_estudio", "count": 10}],
    "upch": [
        {"S": "computadoras", "count": 30},
        {"S": "salas_de_estudio", "count": 30},
        {"S": "salas_de_talleres", "count": 30},
    ],
    "bnp": [
        {"S": "computadoras", "count": 20},
        {"S": "salas_de_estudio", "count": 30},
        {"S": "salas_de_talleres", "count": 40},
    ]
}

# Prefijos por tipo y tenant
prefixes = {
    "computadoras": lambda tenant, index: f"PC{index:03}",
    "salas_de_estudio": lambda tenant, index: f"{tenant[0].upper()}{index:02}",
    "salas_de_talleres": lambda tenant, index: f"{tenant[:2].upper()}{index:03}",
}

# Generar entornos
environments = []
for tenant_id, types in tenants.items():
    for env_type in types:
        env_name = env_type["S"]
        count = env_type["count"]

        for i in range(1, count + 1):
            name = prefixes[env_name](tenant_id, i)

            # Generar registros por cada hora
            for hour in range(7, 21):  # Horas de 7 a 20
                environment = {
                    "tenant_id": tenant_id,
                    "type#name#hour": f"{env_name}#{name}#{hour:02}",
                    "type": env_name,
                    "name": name,
                    "hour": hour,
                    "status": "available",
                    "capacity": (
                        1
                        if env_name == "computadoras"
                        else random.randint(4, 8)  # Capacidad aleatoria para otros tipos
                    ),
                }
                environments.append(environment)

# Guardar en un archivo JSON
output_file = "environments.json"
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(environments, outfile, ensure_ascii=False, indent=4)

print(f"Archivo '{output_file}' generado con éxito.")
