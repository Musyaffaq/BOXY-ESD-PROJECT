FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt -r amqp.reqs.txt
COPY ./washing_vendor_update.py ./invokes.py ./transaction.py ./amqp_setup.py ./inventory.py  ./
CMD [ "python", "./washing_vendor_update.py" ]