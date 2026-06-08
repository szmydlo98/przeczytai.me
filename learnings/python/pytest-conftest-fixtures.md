# Pytest fixtures and `conftest.py`

A **fixture** is reusable test setup that pytest can inject into tests by name.

```python
@pytest.fixture
def public_api_client(api_base_url):
    with httpx.Client(base_url=api_base_url) as client:
        yield client
```

A test asks for it by using the fixture name as a parameter:

```python
def test_health_endpoint(public_api_client):
    response = public_api_client.get("/api/v1/health")

    assert response.status_code == 200
```

Pytest sees `public_api_client`, finds the fixture, runs it, and passes its value
into the test.

## Why `conftest.py`?

`conftest.py` is a **special pytest filename**. Pytest automatically loads fixtures
from it and makes them available to tests in the same directory tree.

That is why `tests/api_gateway/conftest.py` can define shared things like:

- API base URL lookup
- bearer token lookup
- authenticated and public HTTP clients
- reusable completed reading test data

The test files do not need to import these fixtures manually.
