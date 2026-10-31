"""
Adapter fuer AWS Lambda + API Gateway (siehe Exposé-Diskussion zu
Kapitel 6.1: FastAPI + Mangum auf Lambda, da bereits Lambda-Erfahrung
vorhanden ist). Diese Datei wird lokal (uvicorn) nicht verwendet -
sie ist ausschliesslich der Einstiegspunkt, den Lambda aufruft.

Lambda-Handler-Konfiguration: app.lambda_handler.handler
"""
from mangum import Mangum

from app.main import app

handler = Mangum(app)
