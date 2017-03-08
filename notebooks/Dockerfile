# This dockerfile is based of the dockerfiles at https://github.com/jupyter/docker-stacks
# specifically base-notebook, minimal-notebook and scipy-notebook
# Note: Creating a ubuntu user and installing as that user does not work well as I need to share in a host volume to pass in the notebooks, and they are owned by root

FROM krallin/ubuntu-tini:xenial

RUN apt-get update -yqq \
	&& apt-get upgrade -yqq \
	&& apt-get install -yqq --no-install-recommends \
		build-essential \
		git \
		wget \
		bzip2 \
		ca-certificates \
		sudo \
		locales \
	&& apt-get clean \
	&& rm -fr /var/lib/apt/lists

# Generate locales
RUN    echo "en_US.UTF-8 UTF-8" >  /etc/locale.gen \
	&& echo "en_AU.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen

# Configure environment
ENV SHELL /bin/bash
ENV HOME /root
ENV LC_ALL en_AU.UTF-8
ENV LANG en_AU.UTF-8
ENV LANGUAGE en_AU:en

# Setup root home directory
RUN mkdir /root/.jupyter \
	&& echo "cacert=/etc/ssl/certs/ca-certificates.crt" > /root/.curlrc

# Install conda as root
ENV CONDA_DIR /opt/conda3/4.2.12
#ENV PATH $CONDA_DIR/bin:$PATH
RUN cd /tmp && \
    mkdir -p $CONDA_DIR && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh && \
    echo "c59b3dd3cad550ac7596e0d599b91e75d88826db132e4146030ef471bb434e9a *Miniconda3-4.2.12-Linux-x86_64.sh" | sha256sum -c - && \
    /bin/bash Miniconda3-4.2.12-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-4.2.12-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda config --system --add channels conda-forge && \
    $CONDA_DIR/bin/conda config --system --set auto_update_conda false && \
    $CONDA_DIR/bin/conda clean -tipsy

# Install Jupyter Notebook
RUN $CONDA_DIR/bin/conda install --quiet --yes \
    'notebook=4.3*' \
    nb_conda \
    && $CONDA_DIR/bin/conda clean -tipsy

#USER root

EXPOSE 8888
WORKDIR /root/notebooks

# Configure container startup
ENTRYPOINT ["tini", "--"]

# Add local files as late as possible to avoid cache busting
COPY start-notebook.sh /usr/local/bin/
COPY jupyter_notebook_config.py /root/.jupyter/

CMD ["start-notebook.sh"]
