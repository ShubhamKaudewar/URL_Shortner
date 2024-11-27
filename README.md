
# URL Shortner

It is core functionality replica of bit.ly/tinyurl.com. It take long url as input and provide short version of url on which searching in browser will get redirect to original url.




## API Reference

#### Post long url

```http
  POST /shorten
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `url` | `string` | **Required**. Your Valid Long URL Link |

#### Redirect from short-url

```http
  GET /${short-link}
```

#### Open FastAPI Swagger Doc 

```http
  GET /docs
```

Takes two numbers and returns the sum.


## Run Locally

Clone the project

```bash
  git clone https://github.com/ShubhamKaudewar/URL_Shortner
```

Go to the project directory

```bash
  cd URL_Shortner
```

Install [uv](https://docs.astral.sh/uv)

```bash
  #If python is already installed
  pip install uv 
  
  #For MacOS and Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh 
  
  #For Window using powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Check python version

```bash
  python --version
```

Create virtualenv and Install python 3.10 using uv if not installed

```bash
  uv venv --python 3.10.0
```

Create virtualenv

```bash
  uv venv
```

Activate virtualenv

```bash
  .\.venv\Scripts\activate #Windows CMD
  source venv/Scripts/activate #Bash
```

Install dependencies from pyproject.toml file

```bash
  uv pip install -r pyproject.toml
```

Run FastAPI project

```bash
  fastapi dev main.py
```

Run ruff check [ruff is Python linter and code formatter]

```bash
  uv run ruff check 
```

Run Test cases

```bash
  pytest tests/unit_tests/api_test.py
```

You can run specific tests (Run command to populate dummy data)

```bash
  pytest -k tests/unit_tests/test_data_populate
```

## Features

- **Shorten URLs:** A user can submit a long URL and get a shortened version.
- **Redirection:** The shortened URL redirect the user to the original URL when accessed.
- **Unique URLs:** Each long URL generates a unique short URL. If the same URL is submitted again, the same short URL can be reused.
- **Validation:** The service validate input to ensure the URL is valid
- **Access Statistics:** Track the number of times a shortened URL has been accessed
- **Time-to-Live (TTL):** URLs expire's after a specified duration


## Approach, design, decisions, and challenges faced.

- **Approach:** Simple function associated with each file, class and methods. Applied SOLID principles. Not implemented any Abstract Methods since it not required here.

- **Design:** Used FastAPI for it's quick build, deploy usecase. Used NoSQL urldb.json which is handled by python TinyDB package which run locally. Added rate limiter to API to carefully handle DDoS Attack. 

- **Decisions:** Decided to use seperate Classes for single responsibility purpose. DB Queries, Services, Models etc. Used FastAPI routers for seperate routing purpose. Not handled multithreading this can be implemented in future use case. 

- **Challenges Faced:** Hard time to decide the logic for shorten url. Had to choose between base62 encoding which can server large unique short verion that MD5 or SHA256 encoding. Had to trim MD5 for it 128 bit hash value output and used 48 bits = 11 hexdecimal characters and later base64 encoded 7 letters.


## Example

```python
def generate_short_link(self, long_url):
  hashed = md5(long_url.encode('utf-8')). hexdigest()
  b64_value = urlsafe_b64encode(hashed[:11].encode('utf-8')).decode()
  shorten_value = b64_value[:7]
  print(f'shorten_value: {shorten_value}')
```

