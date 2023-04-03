# Blinkrate

On server:
docker-compose --env-file .env.prod build
docker-compose --env-file .env.prod up -d

On client:
pip install -r requirements.txt
python client.py
