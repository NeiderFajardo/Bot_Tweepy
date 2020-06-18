FROM python:3.7-alpine


COPY ./Bots/geckodriver.log /Bots/
COPY ./Bots/main_geckodriver.py /Bots/
COPY ./Bots/tweepy_bot.py /Bots/
COPY ./Bots/.env /Bots/
COPY requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt

WORKDIR /Bots
CMD ["python3", "tweepy_bot.py"]