# Run the App

## With Podman /Docker
first copy `.env.example` to `.env` 

```
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
pip install -r requirements/dev.txt
# Run the app
python app/manage.py runserver
```

For production copy `docker-compose.production.yaml.example` to `docker-compose.production.yaml`. Edit it to your liking and then run:

```
podman compose -f docker-compose.production.yaml
```

Don't forget to create `.env` file for production environment!


# Run tests

```
# make sure the script is executable
chmod +x ./app/test_coverage.sh

# run tests
./app/test_coverage.sh 
```
