import json
import logging
import os
import boto3

log_level = 'DEBUG' if os.getenv('ENV') == 'dev' else 'INFO'

logger = logging.getLogger()
logger.setLevel(log_level)


def list_items(limit, last_key=None):
    logging.debug(limit)
    dynamodb = boto3.resource('dynamodb')
    TABLE_NAME = 'Items'
    table = dynamodb.Table(TABLE_NAME)

    scan_kwargs = {
        'ConsistentRead': True,
        'Limit': limit
    }

    if last_key:
        scan_kwargs['ExclusiveStartKey'] = last_key

    response = table.scan(**scan_kwargs)
    logging.info(response)
    result = response.get('Items', [])

    return result


def validator_params(event):
    query = event.get('queryStringParameters')
    DEFAULT_DATA_LIMIT = int(
        os.getenv('DEFAULT_DATA_LIMIT'))  # ページングのデフォルトかつ最大値
    try:
        limit = query['limit'] if (query and query.get(
            'limit')) else os.environ['DEFAULT_DATA_LIMIT']
        limit = int(limit)
    except ValueError as valueError:
        logger.info(valueError)
        limit = DEFAULT_DATA_LIMIT

    # 20以上の数値の場合は20を再代入
    if limit >= DEFAULT_DATA_LIMIT or limit <= 0:
        limit = DEFAULT_DATA_LIMIT

    params = {'limit': limit}
    if query and query.get('lastKey'):
        params['last_key'] = query['lastKey']

    return params


def handler(event, context):
    try:
        logging.info(event)
        logging.info(context)

        params = validator_params(event)

        result = list_items(
            params['limit'], event.get('last_evaluated_key'))
        logging.debug(result)
        return {
            'statusCode': 200,
            # ensure_ascii: 日本語文字化け対応
            'body': json.dumps(result, ensure_ascii=False)
        }

    except Exception as e:
        logging.error(e)
