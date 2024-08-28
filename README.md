# Run App

first copy `.env.example` to `.env` 

dev env
```
podman compose -f docker-compose.dev.yaml
```

For production copy `docker-compose.production.yaml.example` to `docker-compose.production.yaml`. Edit it to your liking and then run:

```
podman compose -f docker-compose.production.yaml
```

dont forget to create .env file for production environment!


## Run tests

first, make sure, the script is executable. If not, run:
```
chmod +x ./app/test_coverage.sh 
```

then run:
```
./app/test_coverage.sh
```
