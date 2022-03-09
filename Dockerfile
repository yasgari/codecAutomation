FROM python:3

ADD addFinal.py /
ADD requirements.txt /
ADD codecIPs.xlsx /
ADD names.xlsx /
ADD logs.txt /

RUN pip3 install -r requirements.txt

CMD [ "python3", "./addFinal.py" ]