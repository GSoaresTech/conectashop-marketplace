"""Leitura das variáveis de ambiente do servidor REST."""

import os

SERVER_TEAM = os.getenv("SERVER_TEAM", "S00")
HOST = os.getenv("REST_HOST", "0.0.0.0")
PORT = int(os.getenv("REST_PORT", "8080"))
