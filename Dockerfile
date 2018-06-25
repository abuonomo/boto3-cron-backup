FROM python:3.6.5-alpine3.7

COPY entrypoint.sh /
COPY dobackup.py /
COPY requirements.txt /

RUN pip install -r requirements.txt

RUN \
	mkdir -p /aws && \
	apk -Uuv add groff less python py-pip && \
	pip install awscli && \
	apk --purge -v del py-pip && \
	rm /var/cache/apk/* && \
  chmod +x /entrypoint.sh


ENTRYPOINT /entrypoint.sh
