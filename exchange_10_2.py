#!/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称:exchange_10_2.py
Author: yangyang
功能：
Date: 2022-5-7
cron: 30 59 6 * * *
new Env("极速版10减2");
'''

from exchange_lib import *

body_dict = {
    'activityId': 'vN4YuYXS1mPse7yeVPRq4TNvCMR',
    'scene': '1',
    'args': 'key=99E9BFB397BB9E081C3D211644F4D63B80C6629BF10290DBE13C6C11E1DF025FE3774FB37875ED1B720ABB1A6023D3B4_bingo,roleId=3FE9EECAAA41B666E4FFAF79F20E21129412DAD4469A00C14E234FFC59430A3B03E9CF1047D2889AA3D9F3A3AC9845F06DD6177A62EF3A4A570EC8E5C227CE0E4892C7A1A2B984AB9B022706661B4828BA6ED364141E21A7499FE93EB659B4824F445AC4EAB78AF162CA2B7289EDF2DB3F8144DBC4D261FB9826BF7F88790CF94A2ADC829BEE300EB9E27DAD459EA19FE22F265CEE7EE1E0E926357D049A9C9A01413BFC73541208CCC10919AE1DD223_bingo,strengthenKey=4C8818C1732D1A7B9733D611F28BD8B57923ADE220C9B60370F65B533E02E0F8F7A8DB4211A7817EF606DDAD4FA3E67F_bingo'
}

# 优先前5个号，全部抢到后从后面每次执行4个号
exchangeCouponsMayMonthV2(header="https://api.m.jd.com/client.action?functionId=lite_newBabelAwardCollection&client=wh5&clientVersion=1.0.0", body_dict=body_dict, batch_size=5, waiting_delta=0.2, process_number=4)
