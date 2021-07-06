<p align="center"><img src="https://media.discordapp.net/attachments/795652759302701126/796759324105113660/logo_large.png?width=288&height=100"></p>

<h4 align="center">Open source ready-to-use hospital infrastructure deployment tool</h4>
<p align="center">
  <img alt="Docker" src="https://img.shields.io/badge/docker%20-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white"/>
  <img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>
  <img alt="Flask" src="https://img.shields.io/badge/flask%20-%23000.svg?&style=for-the-badge&logo=flask&logoColor=white"/>
  <img alt="JavaScript" src="https://img.shields.io/badge/javascript%20-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/>
  <img alt="TailwindCSS" src="https://img.shields.io/badge/tailwindcss%20-%2338B2AC.svg?&style=for-the-badge&logo=tailwind-css&logoColor=white"/>
  <img alt="MongoDB" src ="https://img.shields.io/badge/MongoDB-%234ea94b.svg?&style=for-the-badge&logo=mongodb&logoColor=white"/>
</p>

# Archived
> This project is now discontinued and has been archived. We thoroughly think that we didn't hit the potential and limits of this project and it may be recreated in the future by using different languages.

## Introduction

Early in 2020, the Ministry of Armed Forces of France announced their [call for new projects to fight against the pandemic](https://www.defense.gouv.fr/english/aid/appels-a-projets/appel-a-projets-lutte-covid-19) and were looking for new and innovative solutions to help civil servants, mostly in hospitals and similar sensitive places by using some recent technologies.

While the applications are currently officially closed, our university requested to their students to make and create their own solutions and submissions. Local authorities will be contacted for the most interesting, serious and innovating projects selected by our university.

## Short description

To respond to this call, us, a group of 4 students decided to create a small service (likely a prototype) which will be easily manageable and deployable (with Docker) to quickly deploy an infrastructure (server) for health/medical services with an intranet (website), database and API, without needing any special knowledge on development.

### Key features

* **Ready-to-go.** Using Docker to deploy and configure all dependencies automatically
* **User friendly startup.** You can easily configure your infrastructure directly from the UI
* **Using real frameworks.** Frontend made with WindiCSS, powered by TailwindCSS's amazing features
* **Real time stats.**  Select and display important/key values to be live-fetched with an API
* **Patients management.** Add, create/edit/delete patients information with multiple privacy/permissions checks
* **Organization.** Permissions presets, configurable permissions, manage multiple departments with an administration panel

### Installation
1. Clone this repository. `git clone https://github.com/eri/shid.git`
2. Install Docker Compose.

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

> If this command fails, you would try alternative methods which are referenced [here](https://docs.docker.com/compose/install/#alternative-install-options).

3. Check if docker-compose is installed properly. `docker-compose --version`
4. Create new images and containers by using the config from the `/Dockerfiles` directory. `sudo docker-compose up -d`

> If your Flask container is stopped after the end of this step and/or have a `No such files or directory` error:
>
> - Consider renaming your `app` folder as `.app`
> - Delete your containers and images 
> - Run the `sudo docker-compose up -d` command again.

5. The website should be now accessible from `your_ip:5000` (ex: `55.12.455.52:5000`) and MongoDB must be available at the port `27277`. Consider updating the ports from the `docker-compose.yml` file to keep things secure.


### Planned
* **Work routine tool.** See and manage your recent activities, personal notes and daily/weekly/monthly planning
* **Real-time messaging.** Messaging between workers and other health departments, to stay connected without using third party platforms

### Dependencies & Tools
* [Flask](https://flask.palletsprojects.com/)
* [MongoDB](https://www.mongodb.com/)
* [Docker Compose](https://docker.com)
* [WindiCSS](https://windicss.org) by [@antfu](https://github.com/antfu)
* [Python-Flask-MongoDB](https://github.com/ivoreali/Python-Flask-MongoDB) by [@ivoreali](https://github.com/ivoreali)

### Collaborators
* [Baflee](https://github.com/Baflee)
* [Aleou27](https://github.com/aleou)
