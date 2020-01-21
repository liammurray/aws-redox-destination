import json
import boto3
import functools
import cgi
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_ssm_param(path, is_json=True, is_encrypted=True):
  client = boto3.client('ssm')
  value = client.get_parameter(Name=path, WithDecryption=is_encrypted)
  val = value['Parameter']['Value']
  if is_json:
    val = json.loads(val)
  return val


def func_name():
  import sys
  return sys._getframe(1).f_code.co_name


def parse_path_params(event, *names):
  '''
    Returns list of values extracted from given path parameter names
  '''
  params = event.get('pathParameters') or {}
  return [params.get(name) for name in names]


def make_redirect(location):
  return {
      'statusCode': 302,
      'headers': {
          'Location': location
      }
  }


def make_response(body, status=200, is_json=True):
  if body != None:
    if is_json:
      body = json.dumps(body)

  return {
      'statusCode': status,
      'body': body,
      'headers': {
          'Content-Type':
              'application/json',
          'Access-Control-Allow-Origin':
              '*',
          "Access-Control-Allow-Headers":
              "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
          "Access-Control-Allow-Methods":
              "GET, OPTIONS, POST",
          "Cache-Control":
              "no-store, no-cache, must-revalidate, max-age = 0",
      }
  }


def parse_body_json(body):
  body = json.loads(body)
  # We expect JSON to decode to an object (not JSON array, string, etc.)
  if isinstance(body, dict):
    return body
  else:
    raise Exception("Expected JSON object body")


BODY_PARSERS = {
    'application/json': parse_body_json
}


def get_content_type(headers):
  if not headers:
    return
  ct = headers.get('content-type')
  if not ct:
    return
  return cgi.parse_header(ct)[0]


def parse_body(event, headers):
  raw = event.get('body')
  if not raw:
    return raw
  ct = get_content_type(headers)
  if not ct:
    raise Exception('Unable to parse body without content-type')
  parser = BODY_PARSERS.get(ct)
  if not parser:
    raise Exception('No parser for content type {}'.format(ct))
  return parser(raw)


def run_handler(handler, event):
  logger.info(event)
  headers = event.get('headers')
  headers = {k.lower(): v for k, v in headers.items()}
  try:
    body = parse_body(event, headers)
  except Exception as e:
    logger.error(e)
    return make_response({'error': 'failed to parse body'}, 400)

  try:
    return handler(event, body, headers)
  except Exception as e:
    logger.error(e)
    return make_response({'error': 'internal error'}, 500)
