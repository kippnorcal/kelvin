# kelvin
Data pipeline for Kelvin.education student pulse surveys

## Dependencies:

- Python3.8
- [Pipenv](https://pipenv.readthedocs.io/en/latest/)
- [Docker](https://www.docker.com/)

## Getting Started

### Setup Environment

1. Clone this repo

```
git clone https://github.com/kippnorcal/kelvin.git
```

2. Create .env file with project secrets

The environment file should fit the following template:

```
# Database variables
DB_SERVER=
DB=
DB_USER=
DB_PWD=
DB_SCHEMA=


# Email Credentials (Optional)
ENABLE_MAILER=1
SENDER_EMAIL=
SENDER_PWD=
RECIPIENT_EMAIL=

# Enable Debug Logging (Optional)
DEBUG=1
```

## Running the job

```
$ docker build -t kelvin .
$ docker run --rm -it kelvin

# Useful for printing files to local directory
$ docker run --rm -it -v ${PWD}:/code/ kelvin
```
