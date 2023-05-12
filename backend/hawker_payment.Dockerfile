FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt -r amqp.reqs.txt
COPY ./hawker_payment.py invokes.py payment.py order.py amqp_setup.py ./
CMD [ "python", "./hawker_payment.py" ]