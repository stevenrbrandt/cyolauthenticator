#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

#mount -t nfs hub:/home /home

ls /home

wrapper=""
if [[ "${RESTARTABLE}" == "yes" ]]; then
  wrapper="run-one-constantly"
fi

if [[ ! -z "${JUPYTERHUB_API_TOKEN}" ]]; then
  # launched by JupyterHub, use single-user entrypoint
  exec /usr/local/bin/start-singleuser.sh "$@"
elif [[ ! -z "${JUPYTER_ENABLE_LAB}" ]]; then
  #. /usr/local/bin/start.sh $wrapper jupyter lab "$@"
  $wrapper jupyter lab "$@"
else
  #. /usr/local/bin/start.sh $wrapper jupyter notebook "$@"
  $wrapper jupyter notebook "$@"
fi
