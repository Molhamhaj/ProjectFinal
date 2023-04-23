# Flight system Project
Fullstack website using Django and Frontend 
(recommendation use the first option )

1)If u are using the docker image:

	1)Make sure you have Docker desktop and docker hub account
	2)use command "Docker login" in the powershell 
	3)Use the docker-compose-final.yml -----> command in pwershell "docker-compose -f docker-compose-final.yml up -d" .(after reaching file dictionary, do the command)
	4)Spouse to be the right credentials ,but anway make sure the credentials in the settings.py for Database are correct as in docker-compose.
	5)after pulling/composing the contianer on your docker desktop wait a bit untill its completly up, and then use url 127.0.0.1:8000 ,
	6)when its running create super user : in the contariner Terminal command: python manage.py createsuperuser , and follow instructions.
	6)you need to add data to db :
			*)login to 127.0.0.1:8000/admin
			*)insert the credentinals of the superuser .
			*)go to contries and add some countries 
			*)go to User roles and add the user roles (Manager, customer, airline) (if you dont do that u get query do not exist error)
	7)now you can swin the web application .  :)
			

  
2)If u are bulding a container from scratch:

	1)Make sure you have Docker and Docker-Compose install on your machine.
	2)Navigate to the project directory
	3)Open command line [ if you are in windows ] or Terminal [ if you are in Mac or Linux ] inside the project directory
	4)Run : `docker-compose -f docker-compose.yml up -d` (this is not the same file as previous method).
	5)That should automatically build all containers and run them in background
		## what docker-compose will do
			- Build MYSQL container
			- Build Django Backend
			- Build Frontend app
			- Run python migrations to MYSQL DB
			- Run python run server on port 8000
			- Run Django Backend
			- Run Frontend

  

	6)Access in browser:
	
		http://localhost:8000/ Or use domain/IP of the Cloud Server if hosted on cloud
		you can check the docker-compose.yml file to see the defined ports for the applications
		`ports:`
			`-"8000:8000"`
  
 		 Left port defined which is accessible to the host machine, Right port defines the running port inside the docker container
		
		Docker container ports:
			-Container name: mfp_django_1[ Backend & Frontend ]

			External port: 8000

			internal docker running port : 8000

			-Container name: mysql

			External port: 3306

			Internal docker running port : 3306

	7)Create SuperAdmin user:
	
		1)Enter the Docker Django container : `docker exec -it django bash` (in case ur are in powershell)
		2)Run python command to create superuser: `python manage.py createsuperuser` (if u are using Docker terminal you just command this 			command)
		3)And follow the instructions


3)Application Overview and usage without Docker:
		
		Hi this is a Flight system Project mande by Molham Haj
		tried my best to do it as good as i can , taking the circumstances 
		hope you will like it , and hit me with feedback , I am ready for it !!!


		now 
		this are the steps 

		1.open project file with coding environment
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

