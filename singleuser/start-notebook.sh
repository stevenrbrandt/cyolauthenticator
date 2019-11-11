#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

echo "start-notebook.sh: $@"
echo "I am: $(whoami)"

echo "pwd: $(pwd)"
cd
echo "after cd: pwd: $(pwd)"

echo "restartable: $RESTARTABLE"
echo "api token: $JUPYTERHUB_API_TOKEN"
echo "lab: $JUPYTER_ENABLE_LAB"

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
  $wrapper jupyter notebook --allow-root "$@"
fi
