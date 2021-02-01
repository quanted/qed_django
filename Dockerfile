# qed_py3 is debian linux with buildpack-deps
# updated with all needed qed python dependencies
# lite version contains no GDAL or anaconda installation
FROM quanted/qed_py3:lite

# Overwrite the uWSGI config
COPY uwsgi.ini /etc/uwsgi/

# Copy the project code
RUN mkdir /src
COPY docker_start.sh /src/docker_start.sh

WORKDIR /src
EXPOSE 8080

# Ensure "docker_start" is executable
RUN chmod 755 /src/docker_start.sh
RUN pip freeze | grep Django

RUN conda install -c conda-forge scipy
RUN conda install -c conda-forge numpy

# Specific Docker-specific Django settings file (needed for collectstatic)
ENV DJANGO_SETTINGS_MODULE="settings_docker"

# Add project root to PYTHONPATH (needed to import custom Django settings)
ENV PYTHONPATH="/src"

# ENTRYPOINT ["sh /src/docker_start.sh"]
CMD ["sh", "/src/docker_start.sh"]
