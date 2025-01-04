# Run the App

## With Podman or Docker compose
first copy `./app/.env.example` to `./app/.env` and then run Podman or Docker compose. 
```
cp ./app/.env.example ./app/.env 

podman compose -f docker-compose.dev.yaml
```

## Without Podman / Docker

```
# create virualenv directory
mkdir venv && virtualenv venv/

# activate it

# Linux
source venv/bin/activate

# Windows
venv/Scripts/activate
```

Install requirements:
```
# Install requirements
pip install -r requirements/dev.txt

# Install pre-commit hooks
pre-commit install

# Run the app
python app/manage.py runserver
```

### Run tests

You can run test and generate coverage with convenient script `test_coverage.sh` located in app's directory.
```
# make sure the script is executable
chmod +x ./app/test_coverage.sh

# run tests
./app/test_coverage.sh 
```


## How to run in Production

Adjust `./app/.env` file for production environment, then copy `docker-compose.production.yaml.example` to `docker-compose.production.yaml`. Edit it to your liking and then run:

```
podman compose -f docker-compose.production.yaml
```

