# sh8email-django
[sh8email](https://sh8.email) is an anonymous, silent and lockable email service.
This is a django-implementation of [sh8email](https://sh8.email).

# Usage

## Starting/stopping server in **development machine**

### Starting
- Web application: `python manage.py runserver`
- Mail receiver: `python manage.py runrecv`
- Mail delete batch: `python manage.py runbatch`

### Stopping
- Web application: Press `Ctrl+C`
- Mail receiver: `python manage.py runrecv --stop`
- Mail delete batch: `python manage.py runbatch --stop`

## Deploying new code in **production machine**
Enter python virtual environment and type `invoke deploy`.
 
## Running tests
- Unit tests: `invoke test.unit`
- Functional tests: `invoke test.func`

### Note
For running tests in development environment, **port 25 should be forwarded to 2525**.
It can be performed using [rinetd](https://boutell.com/rinetd/) in Linux system.
```
# /etc/rinetd.conf
#
# forwarding rules come here
#
# you may specify allow and deny rules after a specific forwarding rule
# to apply to only that forwarding rule
#
# bindadress    bindport  connectaddress  connectport
0.0.0.0 25 127.0.0.1 2525
```

## Setting up development environment

### Setting up development database

#### 1. Install postgresql.

In Ubuntu, 
```shell
$ sudo apt install postgresql
```

In OSX (brew required),
```shell
$ brew install postgresql
```

#### 2. Login as postgres, and enter the psql which is command line tool for postgresql.

##### In ubuntu
```shell
$ sudo su postgres
$ psql
```

##### In OSX
```shell
$ psql postgres
```

#### 3. Add a user named *sh8email*.
```sql
postgres=# CREATE USER sh8email WITH PASSWORD 'password';
CREATE ROLE
```

#### 4. Create a database named *sh8email*.
```sql
postgres=# CREATE DATABASE sh8email;
CREATE DATABASE
```

#### 5. Grant access to user.
```sql
postgres=# GRANT ALL PRIVILEGES ON DATABASE sh8email to sh8email;
GRANT
```

#### 6. Add a privilege to *create database* which used for creating test database.
```sql
postgres=# ALTER USER sh8email CREATEDB;
ALTER ROLE
```

#### 7. Edit pg_hba.conf to disable SSL connection in localhost connection.
In Ubuntu, edit `/etc/postgresql/9.5/main/pg_hba.conf`.
In OS X or macOS, edit `/usr/local/var/postgres/pg_hba.conf`.

From
```
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
```
to
```
# IPv4 local connections:
hostnossl    all             all             127.0.0.1/32            md5
# IPv6 local connections:
hostnossl    all             all             ::1/128                 md5
```

# Trouble Shooting

## django.db.utils.OperationalError: SSL error: decryption failed or bad record mac
See [Edit pg_hba.conf to disable SSL connection in localhost connection](https://github.com/triplepy/sh8email-django#7-edit-pg_hbaconf-to-disable-ssl-connection-in-localhost-connection).

# Contact us
Please mail to eightsh8@gmail.com.