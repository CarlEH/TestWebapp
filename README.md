# Test Webapp

## This small project works as a CMS or BackOffice tool that allows its users to take notes and manage sessions with their patients

### How to launch it
- clone this repo into your machine
- make sure that you have docker installed on your machine, you can download it from https://www.docker.com/
- once that is done open up a terminal and execute these 2 commands in the folder where you cloned this repo:
  - docker-compose build
  - docker-compose up
  - when accessing the webapp for the first time, go to you browser and connect to http://localhost:5050 and login via the account admin@cuure.co/password


- when your are done you can take down thhe service with the following command:
  - docker-compose down
