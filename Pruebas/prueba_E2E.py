import subprocess

# Comando de terminal a ejecutar
comando_terminal = "docker-compose -f docker-compose.yml up --build"

# Ejecutar el comando usando subprocess
subprocess.run(comando_terminal, shell=True)
