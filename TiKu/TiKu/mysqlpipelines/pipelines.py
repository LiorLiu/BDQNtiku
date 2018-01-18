#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@TIME   :2018/1/16 16:08
from .sql import Sql
from TiKu.items import TikuItem

class TikuPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, TikuItem):
            id = item['id']
            sort_id=item['sort_id']
            answer = item['answer']
            ret = Sql.select_id(id,answer)
            if ret[0] == 1:
                print('已经存在了')
                return False
            else:
                print('开始保存试题')
                Sql.insert_shiti(id, sort_id, answer)