from util import make_response, make_redirect, func_name, run_handler, logger
import jwt
import functools
import os
import json


def validate_jwt(token):
  JWT_SECRET = os.environ['JWT_SECRET']
  JWT_AUD = os.environ['JWT_AUD']
  JWT_ALGORITHM = 'HS256'

  try:
    return jwt.decode(token, JWT_SECRET, audience=JWT_AUD, algorithms=[JWT_ALGORITHM])
  except Exception as err:
    logger.info(err)


def post_sso(event, body, headers):
  logger.info(func_name())
  logger.info(json.dumps(body))

  # Authorization: Bearer <token> (headers are lowercase by now)
  auth = headers.get('authorization')
  if not auth:
    return make_response({'error': 'missing auth header'}, 401)

  auth = auth.split()
  if len(auth) != 2 or auth[0] != 'Bearer':
    return make_response({'error': 'failed to parse bearer token'}, 401)

  payload = validate_jwt(auth[1])
  if not payload:
    return make_response({'error': 'invalid token'}, 401)

  logger.info(payload)

  return make_redirect(os.environ['REDIRECT_URL'])


def handler_sso(event, context):
  '''
    Handler for redox sso endpoint.
    Used when destination is configured to use SSO
  '''
  return run_handler(post_sso, event)
