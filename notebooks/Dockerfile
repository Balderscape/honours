# This dockerfile is based of the dockerfiles at https://github.com/jupyter/docker-stacks
# specifically base-notebook, minimal-notebook and scipy-notebook
# Note: Creating a ubuntu user and installing as that user does not work well as I need to share in a host volume to pass in the notebooks, and they are owned by root

FROM krallin/ubuntu-tini:xenial

RUN apt-get update -y \
	&& apt-get upgrade -y \
	&& apt-get install -y --no-install-recommends \
		build-essential \
		git \
		wget \
		bzip2 \
		ca-certificates \
		sudo \
        locales \
        cmake \
        gcc \
        g++ \
        less \
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
RUN cd /tmp && \
    mkdir -p $CONDA_DIR && \
    wget https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh && \
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

EXPOSE 8888
WORKDIR /root

# Configure container startup
ENTRYPOINT ["tini", "--"]

# Install Gromacs
ENV GROMACS_DIR /opt/gromacs/2016.2

RUN cd /tmp && \
    mkdir -p $GROMACS_DIR && \
    wget http://ftp.gromacs.org/pub/gromacs/gromacs-2016.2.tar.gz && \
    tar xzf gromacs-2016.2.tar.gz && \
    rm gromacs-2016.2.tar.gz && \
    cd gromacs-2016.2 && \
    mkdir build && \
    cd build && \
    cmake .. -DGMX_BUILD_OWN_FFTW=ON -DGMX_OPENMP=ON -DCMAKE_INSTALL_PREFIX=$GROMACS_DIR && \
    make && \
    make install && \
    cd /tmp && \
    rm -fr gromacs-2016.2

# Setup the environment module system
RUN apt-get update -y \
	&& apt-get install -y --no-install-recommends \
        environment-modules \
	&& apt-get clean \
	&& rm -fr /var/lib/apt/lists

RUN echo ". /usr/share/modules/init/bash" >> /root/.bashrc \
    && mkdir -p /usr/share/modules/modulefiles/conda3 \
    && mkdir -p /usr/share/modules/modulefiles/gromacs

COPY modulefiles/conda3/* /usr/share/modules/modulefiles/conda3/
COPY modulefiles/gromacs/* /usr/share/modules/modulefiles/gromacs/



# Add some more OS dependencies for the notebook server
RUN apt-get update -y \
	&& apt-get upgrade -y \
	&& apt-get install -y --no-install-recommends \
#        git \
#        vim \
#        jed \
#        emacs \
        python-dev \
        unzip \
        libsm6 \
        pandoc \
        texlive-latex-base \
        texlive-latex-extra \
        texlive-fonts-extra \
        texlive-fonts-recommended \
        texlive-generic-recommended \
#        libxrender1 \
#        inkscape \
        libav-tools \
	&& apt-get clean \
	&& rm -fr /var/lib/apt/lists


# Set up conda environments for the notebooks

RUN $CONDA_DIR/bin/conda create --name md-gmx-2016.2 --yes python=2.7 ipykernel \ 
	&& $CONDA_DIR/bin/conda clean -tipsy

RUN $CONDA_DIR/bin/conda install --yes -c mw --name md-gmx-2016.2 pymol \
    && $CONDA_DIR/bin/conda clean -tipsy

RUN $CONDA_DIR/bin/conda install --yes -c salford_systems --name md-gmx-2016.2 matplotlib prettyplotlib \
    && $CONDA_DIR/bin/conda clean -tipsy

# Load gromacs module when in the md-gmx-2016.2 environment
RUN mkdir -p $CONDA_DIR/envs/md-gmx-2016.2/etc/conda/activate.d \
    && mkdir -p $CONDA_DIR/envs/md-gmx-2016.2/etc/conda/deactivate.d \
    && echo "module load gromacs/2016.2" > $CONDA_DIR/envs/md-gmx-2016.2/etc/conda/activate.d/gromacs.sh \
    && echo "module unload gromacs/2016.2" > $CONDA_DIR/envs/md-gmx-2016.2/etc/conda/deactivate.d/gromacs.sh    

# Setup Remote Kernal to allow for notebooks to run on Artemis
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        libssl-dev \
        libffi-dev \
        openssh-client \
        dos2unix \
    && apt-get clean \
    && rm -fr /var/lib/apt/lists

RUN $CONDA_DIR/bin/pip install rk
RUN ssh-keygen -t rsa -b 4096 -N "" -f /root/.ssh/id_rsa
RUN $CONDA_DIR/bin/rk install-template

#### NOTE: You will need to run: ssh-copy-id psol3692@hpc.sydney.edu.au once to copy the login keys to the hpc cluster ####

# Add local files as late as possible to avoid cache busting
COPY start-notebook.sh /usr/local/bin/
RUN chmod a+x /usr/local/bin/start-notebook.sh && dos2unix /usr/local/bin/start-notebook.sh
RUN echo "StrictHostKeyChecking no" > /root/.ssh/config

COPY jupyter_notebook_config.py /root/.jupyter/
COPY kernel.json /usr/local/share/jupyter/kernels/template/

CMD ["start-notebook.sh"]


