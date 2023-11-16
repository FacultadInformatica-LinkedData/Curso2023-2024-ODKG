## Backend Vida Activa Madrid

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar el servidor Jena Fuseki
# Nota: Cargar los datos con los .ttl usando la UI de Jena
./fuseki-server

# Ejecutar
python3 api.py
```