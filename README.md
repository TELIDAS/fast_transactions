## Running the Application

1. **Clone the Repository**

   First, clone the repository to your local machine:

   ```bash
   git clone https://github.com/TELIDAS/fast_transactions.git
   cd fast_transactions
   ```

2. **Start the Application**

**Use Docker Compose to build and start the application:**

```bash
   docker-compose -f docker-compose.yml up --build -d
   ```
**Once the application is running, here is cURL examples of using API:**
1. Save or Update Rates
```bash
   curl -X 'POST' \
  'http://127.0.0.1:8000/api/save-or-update-rates/' \
  -H 'accept: application/json'
   ```

2. Convert Currency

```bash
   curl -X 'GET' \
  'http://127.0.0.1:8000/api/convert/?from_currency=EUR&to_currency=USD&amount=100' \
  -H 'accept: application/json'
   ```

3. Get Latest Exchange Rate
```bash
  curl -X 'GET' \
  'http://127.0.0.1:8000/api/latest-exchange-rate/' \
  -H 'accept: application/json'
   ```

### Stopping the Application
```bash
   docker-compose down
   ```