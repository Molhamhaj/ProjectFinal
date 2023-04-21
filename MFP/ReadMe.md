# Flight system Project

  

Fullstack website using Django and Frontend 


## Docker
#### Pre Requisites

Make sure you have Docker and Docker-Compose install on your machine


## how to run as docker

Navigate to the project directory

  

Open command line [ if you are in windows ] or Terminal [ if you are in Mac or Linux ] inside the project directory

  

Run : `docker-compose up -d`

  That should automatically build all containers and run them in background

## what docker-compose will do

  

 - Build MYSQL container
 - Build Django Backend
 - Build Frontend app
 - Run python migrations to MYSQL DB
 - Run python run server on port 8000
 - Run Django Backend
 - Run Frontend

  

## How to access in browser

http://localhost:8000/ Or use domain/IP of the Cloud Server if hosted on cloud

  

you can check the docker-compose.yml file to see the defined ports for the applications
`ports:`
	`-"8000:8000"`
  
  Left port defined which is accessible to the host machine, Right port defines the running port inside the docker container

## Docker container ports

  

#### Container name: mfp_django_1[ Backend & Frontend ]

External port: 8000

internal docker running port : 8000

#### Container name: mysql

External port: 3306

Internal docker running port : 3306

  

## How to differentiate external and internal port [ just for information ]

Example postgres container, you would find this code in docker-compose file where left port is outside exposed port to public and right one is the docker container running port which is not public

ports:

- "3306:3306"


## Create SuperAdmin user
Enter the Docker Django container : `docker exec -it django bash`

Run python command to create superuser: `python manage.py createsuperuser`

And follow the instructions

## Basic docker commands

### docker ps
Show running docker containers

To show all running/stop/failing containers, Run: `docker ps -a`

  ![enter image description here](https://tecadmin.net/tutorial/wp-content/uploads/2017/09/docker-ps-command.png)

### docker images 
Show all docker images build on the host machine

![enter image description here](https://www.how2shout.com/linux/wp-content/uploads/2021/05/Docker-Images-check-on-Debian.jpg)
  
### Docker logs
To show the logs for specific containers [ includes all kinds of logs, error , access etc ]

Run : `docker logs -f container-ID/name`

example: `docker logs -f django`

### Docker Stop

To stop all running containers `docker-compose down`

### Docker restart

To restart all containers `docker-compose restart`

## Docker update changes
In case, you have new features completed and wanted to reflect on docker, follow this process

#### Step 1- Stop and remove the Application which is going to be updated
Run :  `docker-compose down`

#### Step 2- Re build image and run container
Simple as running : `docker-compose up -d ` will scan which container is missing and start building images and run the container.
Run:
 `docker-compose build --no-cache django`
`docker-compose up -d`


#### Bonus [ clear.sh ]
I have added a script in root directory, that works on Linux which cleans all running containers, images, volume. Wipes out all things

So you can Build and run from scratch.

how to run : 
`bash clear.sh`

### Application Overview and usage without Docker
Hi this is a Flight system Project mande by Molham Haj
tried my best to do it as good as i can , taking the circumstances 
hope you will like it , and hit me with feedback , I am ready for it !!!


now 
this are the steps 

1. open project file with coding environment
2.create a Data base called "flights_test"
3.install requirements.txt using pip install requirements.txt
3.don't forget to change the password of the new DB file in the sitting.py file !!!
4.Just do these steps:
            1. py manage.py Makemigration
            2. py manage.py Migrate
            3. python manage.py createsuperuser (for admin prevelliges)
            4. py manage.py Runserver 
            5. Open link and boom it's the react frontend


5.React config:
            1. cd client
            2. npm i
            3. npm run dev
            4. npm run build


there are some information in the data base ,added iformation to Database for more usabililty.

THank you

