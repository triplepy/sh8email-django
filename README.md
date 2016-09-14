# sh8email-django

## Setting up development environment

### Setting up development database
1. Install postgresql. In ubuntu,
```
$ sudo apt install postgresql
```
2. Login as postgres, and enter the psql which is command line tool for postgresql. In ubuntu,
```shell
$ sudo su postgres
$ psql
```
3. Add a user named *sh8email*.
```sql
postgres=# CREATE USER sh8email WITH PASSWORD 'password';
CREATE ROLE
```
4. Create a database named *sh8email*.
```sql
postgres=# CREATE DATABASE sh8email;
CREATE DATABASE
```
5. Grant access to user.
```sql
postgres=# GRANT ALL PRIVILEGES ON DATABASE sh8email to sh8email;
GRANT
```
6. Add a privilege to *create database* which used for creating test database.
```sql
postgres=# ALTER USER sh8email CREATEDB;
ALTER ROLE
```
8. Edit pg_hba.conf to disable SSL connection in localhost connection. In ubuntu, edit
```
/etc/postgresql/9.5/main/pg_hba.conf
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

## Trouble Shootings
### django.db.utils.OperationalError: SSL error: decryption failed or bad record mac
See **item 8**(Edit pg_hba.conf to disable SSL connection in localhost connection) of 'Setting up development database'.