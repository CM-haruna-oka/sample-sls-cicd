import src.handlers.list_items as handler
from moto import mock_dynamodb2
import boto3
import json
import pytest
import os
ITEMS_TABLE_NAME = 'Items'


@mock_dynamodb2()
def test_list_items():
    '''
    商品一覧の取得結果が一致する
    '''
    dynamodb = boto3.resource('dynamodb',
                              region_name='ap-northeast-1')
    dynamodb.create_table(
        TableName=ITEMS_TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'item_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'item_id',
                'AttributeType': 'S'
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    table = dynamodb.Table(ITEMS_TABLE_NAME)
    data = [
        {'item_id': 'item_0001',
         'item_name': 'サンプル品1', 'category': '食品'},
        {'item_id': 'item_0002',
         'item_name': 'サンプル品2', 'category': '食品'},
        {'item_id': 'item_0003',
         'item_name': 'サンプル品3', 'category': '食品'},
        {'item_id': 'item_0004',
         'item_name': 'サンプル品4', 'category': '雑貨'},
        {'item_id': 'item_0005',
         'item_name': 'サンプル品5', 'category': '雑貨'}
    ]
    for i in data:
        table.put_item(TableName=ITEMS_TABLE_NAME, Item=i)

    # 全件取得
    response = handler.list_items(20)
    assert response == data

    # 3件取得
    response2 = handler.list_items(3)
    assert len(response2) == 3
