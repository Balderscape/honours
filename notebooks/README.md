This folder contains jupyter notebooks which are used to record the computational experiments performed.

A jupyter with gromacs environment can be quickly set up using Docker and the included Dockerfile.

To build the docker image type `docker build -t jupyter-gromacs .`

To run jupyter using the docker image type `docker run --rm -it -p 8888:8888 -v "%cd%:/root/notebooks" jupyter-gromacs` this will start up the jupyter notebook service and you can then connect via a browser to `localhost:8888` using the password `machino`. The jupyter server will serve up the notebooks in the local directory that you ran docker from.







