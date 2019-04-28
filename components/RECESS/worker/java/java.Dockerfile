FROM python:3.7-alpine

#Instal openjdk
ENV LANG C.UTF-8

RUN { \
		echo '#!/bin/sh'; \
		echo 'set -e'; \
		echo; \
		echo 'dirname "$(dirname "$(readlink -f "$(which javac || which java)")")"'; \
	} > /usr/local/bin/docker-java-home \
	&& chmod +x /usr/local/bin/docker-java-home
ENV JAVA_HOME /usr/lib/jvm/java-1.8-openjdk
ENV PATH $PATH:/usr/lib/jvm/java-1.8-openjdk/jre/bin:/usr/lib/jvm/java-1.8-openjdk/bin

ENV JAVA_VERSION 8u201
ENV JAVA_ALPINE_VERSION 8.201.08-r1

RUN set -x \
	&& apk add --no-cache \
		openjdk8="$JAVA_ALPINE_VERSION" \
	&& [ "$JAVA_HOME" = "$(docker-java-home)" ]


#RECESS stuff
RUN mkdir -p /code

WORKDIR /code

ADD requirements.txt /code

RUN pip install -r requirements.txt

RUN rm -rf /code/requirements.txt

RUN adduser -D -u 1000 runner

ADD worker.py /code

RUN chown -R runner:runner /code

USER runner

# CMD [ "python", "worker.py", "-l", "INFO" ]

CMD [ "python", "worker.py"]

