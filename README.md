# kelvin
Data pipeline for Kelvin.education student pulse surveys

## Dependencies:

- Python3.X _(see Pipfile for latest version)_
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

# Mailgun & email notification variables
ENABLE_MAILER=1
MG_API_KEY=
MG_API_URL=
MG_DOMAIN=
SENDER_EMAIL=
RECIPIENT_EMAIL=

# Enable Debug Logging (Optional)
DEBUG=1
```

## Running the job

```
$ docker build -t kelvin .

# Running job based on most recent "responded_at" date in table
$ docker run --rm -it kelvin

# Running a full truncate and reload of the data
$ docker run --rm -it kelvin --truncate-reload

# Run in debug mode
$ docker run --rm -it kelvin --debug

# Useful for printing files to local directory
$ docker run --rm -it -v ${PWD}:/code/ kelvin
```

## Troubleshooting and maintenance

### Scheduling
The job should be scheduled to run once a week because Kelvin Pulse surveys do not close more frequently than weekly. If this frequency changes, then the time window filter in `Survey_factResponse.sql` should also be updated.

### Re-running
We are not comparing to existing records due to performance challenges. If the job needs to be rerun, you should delete any survey dim and fact data associated with the last week - do this directly in the database. If you don't do this, then there will be duplicates.

## Maintenance

* No annual maintenance is required
* This connector can be paused over the summer and restarted when the first Pulse survey opens
