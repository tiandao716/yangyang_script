#!/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称:exchange_19_5.py
Author: yangyang
功能：
Date: 2022-3-21
cron: 30 59 6,9,14,17,20 * * *
new Env("极速版19减5(python)");
'''

from exchange_lib import *

body = r"body=%7B%22activityId%22%3A%22vN4YuYXS1mPse7yeVPRq4TNvCMR%22%2C%22scene%22%3A%221%22%2C%22args%22%3A%22key%3D13CE10DEFD75052795FFEBDA31379B65F2F22C26C5C5F0E3B8A128B978111DBB7A5BB54EBDB1373E0C35F5DEB9B67446_bingo%2CroleId%3DADAC87F1EC515A647C5357A175E3519B_bingo%2CstrengthenKey%3D19F512DCD8EE34ABE9C4FB4A92C2F42AAEFAF03A89700155D56A825B54D6675D_bingo%22%7D"
body = r"body=%7B%22activityId%22%3A%22vN4YuYXS1mPse7yeVPRq4TNvCMR%22%2C%22scene%22%3A%221%22%2C%22args%22%3A%22key%3DE72F2D6FD3B257AE6EAEEF81FEF44D9C3EFB9B5E0F0E11C4562D68BDA7BA69BF5C4E716FB9BBD7B1678E83551EA3A72E_bingo%2CroleId%3D3FE9EECAAA41B666E4FFAF79F20E21120520F1A5AFE5C9E8D77BD263F6726B9E3576C6C5571777201DA90CF204F2336AB211D7BA6D0E7255BAFF71BCC9ED7782F4BB5E97DDCA47183788BB228E79E0C3D6D9613C7FC7F959A45038CC7BDEF82DD7E61013399964509B5CDEF36C73EAE9EB6B63DA849EA90E7C87A96AB3C6FA44C65C483C9EECCB166A80C30000930072AC3B866785B1639C2C26FE898F623B48_bingo%2CstrengthenKey%3D19F512DCD8EE34ABE9C4FB4A92C2F42A42C9753D63098BF8E18509B9BE302B5B_bingo%22%7D"
exchangeCoupons(body=body)