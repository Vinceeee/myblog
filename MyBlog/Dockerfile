FROM python:3.5
ADD ./code /code
WORKDIR	/code
#ENV DATABASE_URL="mysql+pymysql://my:123456@db/mydb"
#ENV REDIS_HOST="redis"
RUN pip install -r requirements.txt -i  https://pypi.douban.com/simple