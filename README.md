# Information Retrival Project: Search Engine

A simple search engine for [wikipedia farsi](https://dumps.wikimedia.org/fawiki/) writen in Python.

Project done as part of Information Retrival course at Urmia University.

Extract resource files:

```bash
tar xvf resources.tar.xz
```

Run docker version:

```bash
sudo docker pull rqbx91/search-engine:latest
sudo docker run -d -p 80:80 rqbx91/search-engine:latest
```

Build docker image:

```bash
sudo docker build -t search-engine:latest .
sudo docker run -d -p 80:80 search-engine:latest
```

Server is now running on [localhost](http://localhost:80). (Building Index may take a few minutes)