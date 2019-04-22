# Webapp for Python
In a Hackathon, it is very and very effective presentation method to deploy the web applications. In preparation for that, I summarized the consistent flow of making machine learning models into web app. If you follow this, you can easily deploy ML/DL model at a Hackathon:)
## [日本語版解説記事]()

## Architecture
<img src="https://camo.qiitausercontent.com/f27cff7fde0354a96c1eb617ac7271754d7ee5c9/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3330383730302f32393539623236622d613039322d373538642d363639662d3565306461303665313731342e706e67">

Reference: [A Guide to Scaling Machine Learning Models in Production]("https://hackernoon.com/a-guide-to-scaling-machine-learning-models-in-production-aa8831163846")


| Name                                        | Role                                                                        |
| ------------------------------------------- | --------------------------------------------------------------------------- |
| [Nginx](https://nginx.org/en/)              | Web server. It provides load-balancing, SSL configuration, and so on.       |
| [Flask](http://flask.pocoo.org)             | Minimalistic python framework for building RESTful APIs.                    |
| [uWSGI](https://uwsgi-docs.readthedocs.io/) | Web Server Gateway Interface. It can handle with multiple requests at once. |


## Structure

```
├── etc
│   ├── nginx
│   │   ├── conf.d
│   │   │   ├── default.conf
│   │   │   └── uwsgi.conf
│   │   ├── nginx.conf
│   │   └── uwsgi_params
│   └── systemd
│       └── system
│           └── uwsgi.service
└── usr
    └── local
        └── app
            ├── main.py
            ├── templates
            │   └── index.html
            ├── tmp
            └── uwsgi.ini
```
