# webserver for Cumera

Cumera 어플리케이션을 위한 api server입니다.
Api server는 apiserver/
프로젝트 설정 폴더는 cumera/
입니다.

deploy
======
- Install [Docker][docker-install] & [Docker-compose][docker-compose-install]

[docker-install]:https://www.docker.com/products/docker
[docker-compose-install]:https://docs.docker.com/compose/


- Build
Set local network ip or hostname into ALLOWED_HOST of cumera/settings.py
```bash
$ docker-compose build
```
- Run
```bash
$ docker-compose up -d
```

- Stop
```bash
$ cntrl + c
$ docker-compose stop
```

- Cleanup
```bash
$ docker-compose down
```

- Rebuild webapp
```bash
$ docker-compose build webapp
```
