# qed_py3 is debian linux with buildpack-deps
# updated with all needed qed python dependencies
# lite version contains no GDAL or anaconda installation
FROM dbsmith88/qed_py3:lite-3.8

# Overwrite the uWSGI config
COPY uwsgi.ini /etc/uwsgi/

# Copy the project code
RUN mkdir /src
COPY docker_start.sh /src/docker_start.sh

WORKDIR /src
EXPOSE 8080

# Ensure "docker_start" is executable
RUN chmod 755 /src/docker_start.sh

# Specific Docker-specific Django settings file (needed for collectstatic)
ENV DJANGO_SETTINGS_MODULE="settings_docker"

# Add project root to PYTHONPATH (needed to import custom Django settings)
ENV PYTHONPATH /src:$PYTHONPATH

# ENTRYPOINT ["sh /src/docker_start.sh"]
CMD [ "sh", "/src/docker_start.sh"]
