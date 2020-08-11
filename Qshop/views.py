import hashlib
from django.shortcuts import HttpResponseRedirect
#密码加密
def setPassword(p):
    md5=hashlib.md5()
    md5.update(p.encode())
    result=md5.hexdigest()
    return result

# Store的cookie验证
def Valid_Store(fun):
    def inner(request,*args,**kwargs):
        cookie=request.COOKIES.get('username')
        if cookie:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/Store/login/')
    return inner

# Buyer的cookie验证
def Valid_Buyer(fun):
    def inner(request,*args,**kwargs):
        cookie=request.COOKIES.get('username')
        if cookie:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/Buyer/login/')
    return inner


from django.core.mail import send_mail
from Qshop.settings import EMAIL_HOST_USER as sender

import random
import smtplib  # 登录smtp服务器发送
from email.mime.text import MIMEText  # 构建邮件
from Qshop.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD,EMAIL_HOST,EMAIL_PORT
from Buyer.models import ValidCode
import time

# 使用邮件发送验证码
def sendMessage(recver):
    random_str=str(random.randint(0,999999)).zfill(6)
    content = "您好，您的验证码是[%s]，打死也不要告诉别人哟" % random_str
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮箱内容
    # 内容类型 plain文本
    # 编码
    message['Subject'] = '欢迎你的光临'  # 邮箱标题
    message['To'] = recver  # 邮件的接收人
    message['From'] = EMAIL_HOST_USER  # 邮箱发送人

    smtp = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)  # 登录腾讯的SMTP服务器
    smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)  # 登录自己的SMTP服务器账号
    smtp.sendmail(EMAIL_HOST_USER, [recver], message.as_string())  # 发送邮件
    # # 发送人
    # # 接收人。是个列表
    # # 邮件封装
    smtp.close()  # 退出服务器
    code=ValidCode.objects.filter(loginName=recver).first()
    if not code:
        code=ValidCode()
    code.code=random_str
    code.loginName=recver
    code.flag=0
    code.time=time.time()
    code.save()
    return 'ok'


def validCode(recver,recv_code):
    """
    1、超时间的
    2、有了第二条的
    3、使用过的
    验证码有效期5分钟 300秒
    """
    result={'status':'error','data':''}
    code=ValidCode.objects.filter(loginName=recver).first()
    if code:
        live=time.time() - code.time
        if live<300 and code.flag=='0':
            code.flag=1
            code.save()
            if recv_code==code.code:
                result['status']='true'
                result['data']='验证成功'
            else:
                result['data']='验证码错误'
        else:
            result['data']='违法验证码，请从新获取'
    else:
        result['data']='当前用户还没有发送验证码'
    return result

from alipay import AliPay
def Pay(order_id,money):
    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqTcQg3Fuwv41BCjA3Ujhk8zdU5/rHxbKY3VM8myJr/Zt35+fqZVuQ+iuSG25ZPi0iqtalvic5JsgEYhdPB6I+MqnAJDLl7rFtWRngFRa0xfDbiFNgjd+vmZMlXz9NylkD3pwO3/E5/yDtnXv5iGFpcCXmi2T8gmCKzFuLM31MkeVfVU/AajoTft9UiFJNRNyGlvbnDhvuF/cgqYoEZFiI9JFzhRk8zixqZTFo7n/AMlWn5s/nc//TvjKfb4FR49MVs2lSHV7vi5DOSR0tOcCaysKcTgKXLL42coPHcv1jg9aB4qV/AgsxbonGdIMzc4FnQ9dY8F6ER/uj4THUOxzbwIDAQAB
    -----END PUBLIC KEY-----'''

    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEpAIBAAKCAQEAqTcQg3Fuwv41BCjA3Ujhk8zdU5/rHxbKY3VM8myJr/Zt35+fqZVuQ+iuSG25ZPi0iqtalvic5JsgEYhdPB6I+MqnAJDLl7rFtWRngFRa0xfDbiFNgjd+vmZMlXz9NylkD3pwO3/E5/yDtnXv5iGFpcCXmi2T8gmCKzFuLM31MkeVfVU/AajoTft9UiFJNRNyGlvbnDhvuF/cgqYoEZFiI9JFzhRk8zixqZTFo7n/AMlWn5s/nc//TvjKfb4FR49MVs2lSHV7vi5DOSR0tOcCaysKcTgKXLL42coPHcv1jg9aB4qV/AgsxbonGdIMzc4FnQ9dY8F6ER/uj4THUOxzbwIDAQABAoIBAEoqLD6wFM+6AxqTkhRqwRO6krb4PGEf6Ay3eMY39BD/fSCqIZx+NhnlfZ2ZGcy7hMXSXJ4W0Q0RQHjuv45+A6Knj5Kb49/YqJbcLtD8J+KlY659Qi90i0SAKcjLQ2BN7+Eo1M//LBpRfpkWD9NZle4T/14/47wNltO/kn5otrMWHfHSd3aaMQe9es2OzU/aLvZj3muUZ8yLe5bFh2RWwqjQJloyBVgs4ryv7lHNwdv7hz+ucYCOfWiVVbHgLVGN3gR+ZiF8Q9sL+3D4JZBnLrHgImAqXjN7e+oIuFC9OI2KObD9comDskfihXTvfoBro2iVsV62Occ4W6Jhu0dm+6ECgYEA34ijDJDkO9SGJ4GQpStdfWyBJBHg0hoBUrin6DH0Qis46DbdnMoFP+nKTROOMfbnDuqdY9wiHLncxEobGRnTwdAJ6tEdOc3lTuvEKNzi2UHxd9DnOROhn2K/Si4GHv0JuuXokeBecAZmEuNtbuBO9Wws2ndMZ/OcPNxTVRjeuWMCgYEAwcrEuS/DpKZj4T+97QZUG6y5V3g1AWS68N4gD80XqV5ajvHL32uq6nr/vYedT/bVqr+r464ALr0DOji3tqcyuL4yLuYfWUuVyvCw14OgfhGrwZwaN4MXIU2lrn//XXnKDtQjZIywJ/MVpP2PHcSfb0Q7lRnzKL1rbUywM5KMQYUCgYAPlX4QjTVsOmfT70N/UGOnL95c/mYXH7sB4l/KX1kxF8RS5ChVGvx8tTbmYruiHh2Du7WXVayHJioPAT+cY2GQ/IkEdum7svAOrX8yfhvOm7tS6ByGrSiybPb7G/RPSsLX5dlt+h97XebV4Ecr2LWIhK8n1/Nat/AnihDBOQemEwKBgQC1eSdNb5AbEIG5vlIhsupyXAXYBkZEvspcovWNNnaw8R2GfKF44D9WgsYX+vXymugtlH3noNqk6fUqwVAwaFQUMm+WAYNbwG9OcqR3vNg/Flcr3/2g/E5drnO3fD9rjpAL4NYf46tWTcl4DsXFj4npzRCqqHlPLkp6OPVL5jEXbQKBgQCcO+laRLg+XshzpstbeYkmoABZ0Nwfjbcvr3qt/+aIH8ng30eZeLSNBZZRTdOsJg+hu8pTV2iPQHUwP1u2LopQZgwo5Eh4D7Qbovahxb0NXVJgFN2sj+DvT2boX3DfrJueKvrDIIgXYRMZ0vwvbvDjItt67NvePEBGHZ1o2Ayx6w==
    -----END RSA PRIVATE KEY-----'''

    # 实例化应用
    alipay = AliPay(
        appid="122121212121212",  # 支付宝app的id
        app_notify_url=None,  # 回调视图
        app_private_key_string=app_private_key_string,  # 私钥字符
        alipay_public_key_string=alipay_public_key_string,  # 公钥字符
        sign_type="RSA2",  # 加密方法
    )
    # 发起支付
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),  # 将Decimal类型转换为字符串交给支付宝
        subject="商城",
        return_url=None,
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    # 让用户进行支付的支付宝页面网址
    # return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)
    return "https://openapi.alipaydev.com/gateway.do?" + order_string
