# Docker image for checking integration across the main repo (allennlp) and
# sub-repos with every master commit.  This provides early warning when the
# current masters of some combination of allennlp, allennlp-hub and the
# sub-repos are incompatible.
#
# We expect that the various repos are checked out under a directory matching
# their name, e.g. allennlp-semparse. A TeamCity build can be configured to do
# this by adding the checkout rule "+:.=>allennlp-semparse". These are found
# under "Version Control Settings" -> "VCS Roots" -> "Edit checkout rules".

FROM python:3.7.2

# Setup a spot for the code
WORKDIR /stage

# Copy requirements files first so we can install them and get better caching
# from Docker.
RUN mkdir allennlp
RUN mkdir allennlp-semparse
COPY allennlp/requirements.txt allennlp/requirements.txt
COPY allennlp-semparse/requirements.txt allennlp-semparse/requirements.txt

RUN pip install -r allennlp/requirements.txt
RUN pip install -r allennlp-semparse/requirements.txt

# Copy remaining files
COPY allennlp-hub allennlp-hub
COPY allennlp allennlp
COPY allennlp-semparse allennlp-semparse

# Install the allennlp we want to test.
RUN pip install --editable allennlp

# Ensure we don't blow away the allennlp under test.
# Note: Each new sub-repo needs to implement the EXCLUDE_ALLENNLP_IN_SETUP
# logic in its setup.py.
# TODO(brendanr): Could we avoid this by carefully ordering our installs here?
# Specifically, by placing allennlp last.
ENV EXCLUDE_ALLENNLP_IN_SETUP true
RUN pip install --editable allennlp-semparse
RUN pip install --editable allennlp-hub

CMD ["/bin/bash"]
