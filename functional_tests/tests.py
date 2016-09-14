# -*- coding: utf-8 -*-
import email
import smtplib
import unittest
from email.mime.text import MIMEText

from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# BDD 개발을 위한 클래스 주석으로 유저 스토리를 작성
# 이후 테스트 코드를 작성한다.

# 주의 아래 유저 스토리는 픽션입니다.
# 실존 인물 및 단체와는 무관함을 알려드립니다.
class FunctionalTest(unittest.TestCase):
    def send_cert_mail(self):
        msg = MIMEText('우리가 바로 그 원영주식회사 입니다.')
        msg['To'] = email.utils.formataddr(('Downy',
                                            'downy@sh8.email'))
        msg['From'] = email.utils.formataddr(('Wonyoung Ju',
                                              'Ju@wonyoung.com'))
        msg['Subject'] = '인증해주시면 감사감사'
        server = smtplib.SMTP('127.0.0.1', settings.MAIL_SERVER_PORT)
        try:
            server.sendmail('Ju@wonyoung.com',['downy@sh8.email'],
                            msg.as_string())
        finally:
            server.quit()


    def test_new_user_ordinary_scene(self):
        # 주식왕 다운이는 원영주식회사(이하 (주)원영)의
        # 회사 정보를 알아보기 위해 (주)원영 홈페이지에 들어갔는데,
        # 자세한 정보를 보려면 회원가입을 해야 한다고 한다.
        # 어차피 정보만 한번 볼껀데 가입하라는 부분에서 다운이는 화가났다.
        
        # 이때 가입을 하려하는데 설상가상으로 이메일 인증까지 요구한다.
        # 문득, 다운이는 그녀가 속한
        # 파이썬 공부모임(사실은 이민 준비모임이라 카더라)에서 만난 젤리에게
        # sh8email 이라는 곳에 대해 들은 게 떠올라 이메일 부분에
        # downy@sh8.email 로 메일정보를 등록한다.
        # 회원 가입을 완료 후 (주)원영에서는 downy@sh8.email 로 인증메일을 보냈다.
        self.send_cert_mail()
        
        # 다운이는 이메일을 확인하기 위해 sh8.email에 접속했다.
        self.browser = webdriver.Firefox()
        self.browser.get("http://localhost:8000")
        self.assertIn('sh8.email', self.browser.title)
        # 근래 본 사이트중에 가장 미려함에 반해 10초간 멍하니 바라보다가
        nick_form = self.browser.find_element_by_id('recipient')
        self.assertEqual(
            nick_form.get_attribute('placeholder'),
            '닉네임'
        )
        # 로그인 창에 downy를 입력한다.
        nick_form.send_keys('downy')
        nick_form.send_keys(Keys.ENTER)
        # 로그인 이후 (주)원영에서 온 메일이 나타난다.
        
        # (주)원영으로 부터 온 메일을 클릭하자 메일 내용이 보인다.

        
        # 메일을 인증 한 다운이는 주식왕 답게 혹시 메일이 남아있는지,
        # 다시 확인하기 위해 접속을 시도한다.
        ## 새로운 브라우저 세션을 이용해서 접속해보기 위한 코드
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # TODO implementation is required.
        # 하지만 역시 무한대로 조용한 sh8.email 답게
        # 자동으로 메일이 삭제되어 있는 것을 확인한뒤,
        # 안심하고 (주)원영사의 주식을 사러 간다
        self.browser.quit()
