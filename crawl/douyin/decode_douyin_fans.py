import json
from .handle_db import save_task
def response(flow):
    if 'aweme/v1/user/flower/list' in flow.request.url:
        for user in json.loads(flow.response.test)['followers']:
            douyin_info = {}
            douyin_info['share_id'] = user['uid']
            douyin_info['douyin_id'] = user['short_id']
            douyin_info['nickname'] = user['nickname']
            save_task(douyin_info)
