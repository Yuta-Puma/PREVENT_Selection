%%writefile test_date_converter.py
import pytest
from date_converter import convert_date

def test_convert_date():
    assert convert_date('平成30年2月6日') == '2018-02-06'
    assert convert_date('令和4年2月6日') == '2022-02-06'
    assert convert_date('S50/12/31') == '1975-12-31'
    assert convert_date('明治45年5月5日') == '1912-05-05'
    assert convert_date('1995.2.4') == '1995-02-04'
    assert convert_date('2008/12/23') == '2008-12-23'
    assert convert_date('20180506') == '2018-05-06'
    assert convert_date('Invalid Date') == 'Invalid date format'