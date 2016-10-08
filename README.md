# sh8email-django

## Usage

### Starting/stoping servers in **development machine**
#### Starting
- web application: `python manage.py runserver`
- mail receiver: `python manage.py runrecv`
- mail delete batch: `python manage.py runbatch`

#### Stopping
- web application: Press `Ctrl+C`
- mail receiver: `python manage.py runrecv --stop`
- mail delete batch: `python manage.py runbatch --stop`

### Deploying new code in **production machine**
Enter python virtual environment and type `invoke deploy`.
 
### Running tests
- Unit tests: `invoke test.unit`
- Functional tests: `invoke test.func`

#### Note
For running tests in development environment, **port 25 should be forwarding to 2525**.
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
##### In Ubuntu
```shell
$ sudo apt install postgresql
```
##### In OSX (brew required)
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
##### In Ubuntu, edit
```
/etc/postgresql/9.5/main/pg_hba.conf
```
##### In OSX edit
```
/usr/local/var/postgres/pg_hba.conf
```
from
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

## Trouble Shooting
### django.db.utils.OperationalError: SSL error: decryption failed or bad record mac
See **item 8**(Edit pg_hba.conf to disable SSL connection in localhost connection) of 'Setting up development database'.
