# serverless
𝝀 𝝀 𝝀 𝝀
=======


Setup
-----
Assumptions:
  * you have the following installed: python3, pip, yarn, docker

0. `yarn global install serverless`
1. `virtualenv ~/.virtualenv/aws-util --python=python3`
2. `source ~/.virtualenv/aws-util/bin/activate`
3. `pip install -r requirements-dev.txt`
4. `yarn`
5. `docker-machine create main`

Running tests
-------------

0. `source ~/.virtualenv/aws-util/bin/activate`
1. `pip install -r requirements-dev.txt`
1. `python test_handler.py`


Running Locally
--------------

0. `source ~/.virtualenv/aws-util/bin/activate`
1. `python handler.py`

Building
--------
1. `pip-compile --output-file requirements.txt requirements.in`
1. `docker-machine start main`
2. `eval $(docker-machine env main)`
3. `pip-compile --output-file requirements.txt requirements.in`

Deploying
---------
* you'll need to build dependency packages first see `Building`
* this deploys to `personal` profile replace with `$YOUR_PROFILE_NAME` as defined in
  your ~/.aws/credentials file.

1. `AWS_PROFILE=personal serverless deploy`

Adding package dependencies
---------------------------
1. add package to requirements.in
2. `pip-compile requirements.in`
