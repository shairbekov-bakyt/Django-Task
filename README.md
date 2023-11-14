# Django-Task

## Install

1. Install Docker and docker-compose.

For Debian, Ubuntu:

```
su
apt update; apt upgrade -y; apt install -y curl; curl -sSL https://get.docker.com/ | sh; curl -L https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
```

Don't forget press CTRL+D to exit from super user account.

2. Apply environment variables:

```
cp example.env .env
```

3. Change a random string for `SECRET_KEY` and `POSTGRES_PASSWORD` in `.env`.

4. Install dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Up docker-compose, migrate database and create super user:

```
docker-compose -f docker-compose-production.yml up --build
docker-compose -f docker-compose-production.yml exec backend bash
python manage.py createsuperuser
```

6. open project swagger

http://0.0.0.0:8000/api/docs/
