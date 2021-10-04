FROM python:3.9

RUN apt-get update && \
    apt-get install -y \
      build-essential


COPY . /rev
WORKDIR /rev

# NOTE(mmicu): we should split test requirements vs app requirements
RUN pip install -r /rev/requirements.txt

RUN chmod +x /rev/entrypoint.sh

ENTRYPOINT ["/rev/entrypoint.sh"]
CMD ["run"]
