# ESD-Project

## Project Directory
The project directory is as follows:

```
├── backend
│   ├── amqp_setup.py
│   ├── amqp.reqs.text
│   ├── docker-compose-kong.yml
│   ├── docker-compose.yml
│   ├── hawker_payment.Dockerfile
│   ├── hawker_payment.py
│   ├── hawker_place_order.Dockerfile
│   ├── hawker_place_order.py
│   ├── http.reqs.txt
│   ├── inventory.Dockerfile
│   ├── inventory.py
│   ├── invokes.py
│   ├── notification.Dockerfile
│   ├── notification.py
│   ├── order.Dockerfile
│   ├── order.py
│   ├── payment_log.Dockerfile
│   ├── payment_log.py
│   ├── payment.Dockerfile
│   ├── payment.py
│   ├── stripe_wrapper.Dockerfile
│   ├── stripe_wrapper.py
│   ├── transaction_log.Dockerfile
│   ├── transaction_log.py
│   ├── transaction.Dockerfile
│   ├── transaction.py
│   ├── washing_vendor_update.Dockerfile
│   ├── washing_vendor_update.py
├── frontend
├── Postman JSON Files
├── SQL Scripts
├── Kong_Configuration.json
└── README.md
```

## Running the services
1. In the root directory, `cd backend` to go inside the services folder.
1a. If you are on MAC - In the `docker-compose.yml`, you need to edit all the dbURL's port to `8889` instead of `3306`. In the `docker-compose-kong.yml`, you need to edit the `kong-database` container's platform to `linux/arm64`.
2. In the terminal - Run `docker-compose -f docker-compose-kong.yml up` to start the Kong services first. Then, in another terminal, run `docker-compose up` to start up all services.

You will now be able to access the microservices through the following routes:

### Simple (Micro)services
- Inventory - `localhost:5001`
- Stripe Wrapper - `localhost:5002`
- Orders - `localhost:5003`
- Payments - `localhost:5004`
- Washing Vendor Transactions - `localhost:5005`

### Complex Microservices
- Place Order - `localhost:5100`
- Make Payment - `localhost:5101`
- Washing Vendor Update - `localhost:5102`

### RabbitMQ Consumers
- Notification
- Transaction Log
- Payment Log

### RabbitQ Management UI
- RabbitMQ Management UI - `localhost:15672`

### Konga Management UI
- Konga Management UI - `localhost:1337`

## Configuring Kong API Gateway through Konga Management UI

1. Access the Konga Management UI at `localhost:1337`.
2. Create an admin user for Konga
    a. Username: admin
    b. Email: <your email address>
    c. Password: adminadmin
3. Sign in to continue
4. Create a new connection
    a. Name: default
    b. Kong Admin URL: `http://kong:8001`
5. Click on `SNAPSHOTS` on the left hand side.
6. Click on `IMPORT FROM FILE` and import the `Kong_Configuration.json` file
7. Once imported, click on `DETAILS` and then `RESTORE`
8. Select all the objects, and import. You are all set!

Alternatively, you can set up the services manually with the details below.

### Services

#### 1. ordersapi
URL: `http://backend-order-1:5003/orders`

Routes: `/api/v1/orders` (hit enter)

Methods: `GET` `POST` `PUT` `OPTIONS` (hit enter after each method)

#### 2. paymentapi
URL: `http://backend-payment-1:5004/payment`

Routes: `/api/v1/payment` (hit enter)

Methods: `GET` `POST` `OPTIONS` (hit enter after each method)

#### 3. transactionapi
Url: `http://backend-transaction-1:5005/transaction`

Routes: `/api/v1/transaction` (hit enter)

Methods: `GET` `POST` `OPTIONS` (hit enter after each method)

#### 4. inventoryapi
URL: `http://backend-inventory-1:5001/inventory`

Routes: `/api/v1/inventory` (hit enter)

Methods: `GET` `PUT` `OPTIONS` (hit enter after each method)

#### 5. hawkerplaceorderapi
URL: `http://backend-hawker_place_order-1:5100/order`

Routes: `/api/v1/hawkerplaceorder` (hit enter)

Methods: `POST` `OPTIONS` (hit enter after each method)

#### 6. hawkerpaymentapi
URL: `http://backend-hawker_payment-1:5101/hawker_payment`

Routes: `/api/v1/hawkerpayment` (hit enter)

Methods: `POST` `OPTIONS` (hit enter after each method)

#### 7. washingvendorupdateapi
URL: `http://backend-washing_vendor_update-1:5102/washing_vendor_update`

Routes: `/api/v1/washingvendorupdate` (hit enter)

Methods: `POST` `OPTIONS` (hit enter after each method)

## Running the Frontend UI
1. You will need to have npm installed. Check the following to do so: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm
2. In the root directory, `cd frontend` to go inside the frontend folder.
2. Run `npm install` to install all the required dependencies.
3. Run `npm start` to start the Frontend UI.

You will now be able to access the Frontend UI through your browser at `localhost:3000`

## Setting up the databases
1. start MAMP/WAMP server
2. import all the files in `SQL Scripts` in `http://localhost/phpMyAdmin5/` (for Windows Users) or `http://localhost:8888/phpMyAdmin5/` (for Mac Users)
