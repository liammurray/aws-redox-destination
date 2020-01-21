from util import make_response, func_name, run_handler, logger
import functools
import os
import json

def check_token(tokenInRequest):
  token = os.environ['VERIFICATION_TOKEN']
  logger.info('Our token (from env): {}'.format(token))
  if tokenInRequest != token:
    logger.error('Invalid verification token: {}'.format(tokenInRequest))
    return make_response(None, 401)

def get_verification(event, body, headers):
  '''
    GET /destination
    Deprecated approach to verification
    They send challenge and verification token in header and query string params
  '''
  logger.info(func_name())
  tokenInRequest = headers.get('verification-token')
  err = check_token(tokenInRequest)
  if err:
    return err

  query = event.get('queryStringParameters') or {}
  return make_response(query.get('challenge'), is_json=False)


def post_transmission(event, body, headers):
  logger.info(func_name())
  logger.info(json.dumps(body))

  # Will be in body for initial verification using POST
  tokenInRequest = body.get('verification-token')
  if tokenInRequest:
    err = check_token(tokenInRequest)
    if err:
      return err
    return make_response(body.get('challenge'), is_json=False)

  # Normal request...
  tokenInRequest = headers.get('verification-token')
  err = check_token(tokenInRequest)
  if err:
    return err

  return make_response(None, 200)


DEST_HANDLER_MAP = {
  'GET': get_verification,
  'POST': post_transmission
}
def handler_destination(event, context):
  '''
    Handler for redox destination
      GET - verification
      POST - transmission
  '''
  # logger.info(event)
  handler = DEST_HANDLER_MAP.get(event.get('httpMethod'))
  if handler:
    return run_handler(handler, event)
  return make_response(None, 401)


# Header
# 'application-name': 'RedoxEngine'
# 'Content-type': 'application/json'
# 'host': '<IP>'
# 'content-length': '93'
# 'Connection':'close'

# Body
# 'verification-token': 'verificationtoken'
# 'challenge':'cc2f1bdf-af51-4974-af5c-f3af19d6526c'
