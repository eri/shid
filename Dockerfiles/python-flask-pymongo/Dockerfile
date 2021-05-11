FROM       ubuntu:latest

COPY . .

# Update apt-get sources AND install Python-dve
RUN apt-get update && apt-get install -y build-essential python-dev 
RUN apt-get install -y python-setuptools
RUN apt-get install -y python3-pip
RUN apt-get install -y nano
RUN apt-get install -y telnet

## Flask Extensions
RUN pip3 install pymongo
RUN pip3 install Werkzeug
RUN pip3 install requests
RUN pip3 install Flask_Caching
RUN pip3 install flask
RUN pip3 install discord.py
RUN pip3 install discord

## Install a few other tools, nano, telnet and so on...
RUN apt-get install -y nano && apt-get install -y telnet

EXPOSE 5000

ENTRYPOINT ["/usr/bin/python3", "/app/app.py"]
