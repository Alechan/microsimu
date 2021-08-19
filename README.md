# MicroSimu

![Main branch](https://github.com/Alechan/microsimu/workflows/Main%20branch/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/Alechan/microsimu/badge.svg?branch=microsimu-11-nmi-table-plot)](https://coveralls.io/github/Alechan/microsimu?branch=microsimu-11-nmi-table-plot)

MicroSimu is an open-source microservice that runs simulations of predefined models with user specified parameters.
Its main purpose is to offer a way of easily running simulations remotely and locally. It makes a clear distinction between the
"simulation run", its purpose, and the "simulation results visualization", not its purpose. Nevertheless,
basic lines plots and tables can be automatically generated for each simulation result but the user is
encouraged to create their own if these do not satisfy their needs (there are plans to expand the visualization
capabilities in the future).

## Demo
Currently offline.


## Locally

### Python on Linux
Unfortunately, without some type of virtualization (see Docker below), the only supported platform to run simulations
locally is Linux, as the version included of the Latin-American World is a pre-compiled linux binary. Starting
the server can be as simple as:

    # Clone the repo
    git clone https://github.com/Alechan/microsimu
    cd microsimu
    # Create a python virutal environment (in this example we use conda but others are also valid)
    conda create -c conda-forge python=3.9 -n microsimu
    conda activate microsimu
    # Install dependencies
    pip install -r requirements.txt
    # Start the server on localhost:8000
    cd src
    python manage.py runserver

### Using docker anywhere
Using docker, we can start a MicroSimu instance anywhere. We can use the Dockerfile to start a lone container, or
we can use the docker compose file to also start instances of nginx and postgres.

    # Clone the repo
    git clone https://github.com/Alechan/microsimu
    cd microsimu
    # Copy the .env files from the functional tests
    cp functional_tests/dotenv_db_func_test .env.db.prod
    cp functional_tests/dotenv_func_test .env.prod
    # Start the containers
    docker-compose up -d --build
    # Microsimu can now be accesed at localhost:1337

One of MicroSimu's secondary objectives is to contribute to the Open Source community with "real world"
examples of subjects normally hidden in other projects. In this case, you may see that we set the `.env.prod`
and `.env.db.prod` files, which have very curious names. This is because this is the exact same way that MicroSimu
is deployed at the live demo (currently offline), the only addition being that the host has another nginx instance
linked to this containerized nginx (and the fact that the environtment variables have been set with more "real world values" for the site). This is planned to be changed in the future as seen on issue [#108](https://github.com/Alechan/microsimu/issues/108).

## Models
### Latin-American World Model
In this first version of MicroSimu, the only model available to study and run simulations is the
The Latin-American World Model (LAWM), a global model developed in Fortran in 1972 by a multidisciplinary research group
in Bariloche, Argentina that fell into abandonment 4 years later due to the Military Coup suffered by the country. The
original plan was to release the first version of MicroSimu with a python translation of the model but due to time
constraints it was suspended at a completion of about 40%. Therefore, a pre-compiled fortran version of the model is included instead.

The book published in 1976 (see bibliography below), describes in great detail the inspiration, assumptions and
justifications of the model.

## FAQ
### I don't really care about simulations. What good is MicroSimu for me?
It provides real world examples of:
- Developing and testing microservices using Django Rest Framework
- Running Github Actions to provide Continuous Integration and Continuous Deployment (see ./github/workflows)
- Managing secrets in said Github Actions

Even if the items listed above end up being inconsequential and it falls into oblivion, it was and will still be an
excuse to learn and get out of my comfort zone so it is a win-win for me.

### Is this production ready?
Yes and not yet. It's the exact same code as the one that was running on the live demo (currently offline)
but it still needs
some extra configuration on the host and it may need a more robust database depending on your needs (see one of
the questions below).

### Is this the code for your website? You're gonna get hacked :O
Let's hope not. In any case, if you find any vulnerabilities please don't create a new issue as they're public.
Instead, hit me up on [LinkedIn][LinkedIn].

### You're using a containerized Postgres instance in production? That's so wrong. 
Kind of but not really. For low traffic sites it's cheaper and easier to maintain than DBaaS alternatives. Nevertheless,
[as people more intelligent than me have already explained the situation in detail](https://vsupalov.com/database-in-docker/),
you have to be careful.

### What are the plans for the future?
For a specific answer, you can check the active issues. In broad detail, finish translating LAWM to python and start
adding other models such as World3. It would also be great to "officially" support visualizations but I'm not very
proficient in javascript.

## Credits
- The "Latin American World Model 2.0 Web Interface" (see bibliography below) was a direct inspiration of this project
- Related books and online articles will be added here when I find the time. It may prove useful for readers with
similar projects.

## Bibliography

- Catastrophe or New Society? A LatinAmerican World Model -  Amı́lcar Herrera, Hugo Scolnik, Graciela Chichilnisky,
 Gilberto Gallopı́n, Jorge E. Hardoy, International Development Research Centre, Ottawa , Ontario Canada, and Buenos Aires (Argentina)
 Fundacion Bariloche. International Development Research Centre, January 1976.
-  Danós, Alejandro, Castro, Rodrigo, and Scolnik, Hugo (2017), "Latin American World Model 2.0 Web Interface" Discrete
 Events Simulation Lab, University of Buenos Aires, Retrieved November 12, 2020 from https://lawm.exp.dc.uba.ar/ 


[LinkedIn]: https://www.linkedin.com/in/alejandro-dan%C3%B3s-058a57104/
