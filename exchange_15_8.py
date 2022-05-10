#!/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称:exchange_15_8_test.py
Author: yangyang
功能：
Date: 2022-5-7
cron: 20 59 8,11,14,17,19 * * *
new Env("极速版15减8");
'''

from exchange_lib import *

body_dict = {
    'activityId': 'vN4YuYXS1mPse7yeVPRq4TNvCMR',
    'scene': '1',
    'args': 'key=DDF1B71D0AF91A8547973CE5362A890F18C8E73AAC10BA9179CE5D2D745E95AC9AC125029761397270C947AC9F5E11CE_bingo,roleId=3FE9EECAAA41B666E4FFAF79F20E2112EC5A32B22271AD04523B3C66AE5807591E0DB913F0F40F86F97AAA49D12C568D47FEEE50418AD25C6B23D81C476A40CB07BCCE74C4EDAD2E0D1BCF515F06DECE783A16EA99A0959CAC63BDF9BD9A9037450AB25EE84616EF9E65486A529F6690F93EA6903FF6754FD22FD39B43821B0041487D3996E0CF72C487DD107C4D0F13EA507700B35B495859747F1E700186EA385A46F6ED361FE40B11663D21263EB1_bingo,strengthenKey=4C8818C1732D1A7B9733D611F28BD8B57923ADE220C9B60370F65B533E02E0F823A5E9624E2105020B0FB67EE3BFC671_bingo'
}

# 优先前4个号，全部抢到后从后面每次执行2个号
exchangeCouponsMayMonthV2(header="https://api.m.jd.com/client.action?functionId=lite_newBabelAwardCollection&client=wh5&clientVersion=1.0.0", body_dict=body_dict, batch_size=4, other_batch_size=2, waiting_delta=0.26, process_number=4)
