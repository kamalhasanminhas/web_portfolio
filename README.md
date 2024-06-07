### Web Portfolio

A Simple Web Portfolio app which allow admin to update their portfolio and has a public view for interested viewers.

### Installation

Update the `app.env` file.

```shell
# Python 3.12.2
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Add -c to create tables.
python app.py -c
```

You should see the admin page at after logging in at http://localhost/admin


### Dockerized Database

TO Use Dockerized MySQL run the following command
```shell
docker-compose up -d
```

Note: Please make sure that Docker Desktop is installed and running
