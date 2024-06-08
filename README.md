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

Home Page: http://localhost:5000

You should see the admin page at after logging in at http://localhost:5000/admin

### Create user

```shell
flask user create
```
Output:
```shell
Username:
Email:
Password:
First Name:
Last Name:
```

### Docker

To Use dockerized web app with mysql database please run the following command.
```shell
docker-compose up -d
```

Verify at `http://localhost`


Note: Please make sure that Docker Desktop is installed and running
