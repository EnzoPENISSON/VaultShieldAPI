Creer un venv

python3 -m venv venv/

activer le venv

source venv/bin/activate

run :

pip install -r requirements.txt

Dev mode
flask --app __init__ run --debug -p 8080

Production mode with https:
flask --app init run -p 8080 --cert=domain.crt --key=domain.key
