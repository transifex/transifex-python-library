IMAGE_NAME := transifex/pyenv-tox

build:
	@ docker build -t ${IMAGE_NAME} .

push: build
	@ docker push ${IMAGE_NAME}

shell: build
	@ docker run -it ${IMAGE_NAME} /bin/bash

ci_test: 
	@ find . -name \*.pyc -delete
	@ circleci build

ci_setup: /usr/local/bin/circleci
	@ printf "downloading CircleCI builder from https://circle-downloads.s3.amazonaws.com..." && \
	  curl -s -o /usr/local/bin/circleci https://circle-downloads.s3.amazonaws.com/releases/build_agent_wrapper/circleci && \
	  chmod +x /usr/local/bin/circleci && \
	  printf " success!\n"
