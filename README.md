# mysql-sandbox

# Ref
https://github.com/budougumi0617/mysql-sakila


# Docker Commands
```
docker build -t mysql-sandbox .
```

```
docker run --rm -d -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -p 43306:3306 --name mysql-sandbox mysql-sandbox
```

```
docker run --rm -it -e MYSQL_ALLOW_EMPTY_PASSWORD=yes --name mysql-sandbox mysql-sandbox bash
```