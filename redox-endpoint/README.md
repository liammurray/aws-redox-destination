# redox-endpoint

## Setup Python

Start with pristine python env:

```bash
# Naming of virtualenv to your preference
mkvirtualenv mydevopsapi
```

Install requirements:

```bash
# At root
pip install -r requirements.txt
```

Run unit tests

```bash
# Point to latest (not layer)
pytest
# See print statements and verbose output
pytest -vs
```

If you install new dependencies save them.

```bash
pip freeze --exclude-editable --local > requirements.txt
```

There is a `requirements.txt` file in `./src`. This is for dependencies that are packaged with the lambdas. Basically add anything that is not in a layer or provided with the system.

## Test using local API GW

To test locally run a local API gateway instance in another shell.

```bash
make build
sam local start-api
# Invoke '/info/env' endpoint (spits out lambda environment for debug)
curl -s http://127.0.0.1:3000/env | jq
```

> API GW Authentication with Cognito is skipped with local api gateway
> The first time you hit the api gw it will download layers and create a docker image

### Verification

  See `curl.txt` for examples.

  ```bash
    curl -X GET -H "Verification-Token: 926b1333-a62b-444b-9546-af7b3af063d3" \
      -s http://127.0.0.1:3000/destinationchallenge=cc2f1bdf-af51-4974-af5c-f3af19d6526c
  ```

### Sending POST

  First enter the following.

  ```bash
  curl -X POST -H "Content-Type:application/json" -d @- -s http://127.0.0.1:3000/destination <<EOF
  ```

  Next paste the JSON body to send

  ```json
  {
    "foo": "bar"
  }
  ```

  Next complete the command by typeing `EOF`

  You can also pass `-d @filename`).
