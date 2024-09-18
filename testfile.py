%%writefile test_date_converter.py
import pytest
from date_converter import convert_date

def test_convert_date():
    assert convert_date('1995.2.4') == '1995-02-05'
    assert convert_date('2008/12/23') == '2008-12-23'
    assert convert_date('平成5年2月6日') == '1993-02-06'
    assert convert_date('R3/08/30') == '2021-08-30'
    assert convert_date('1995.2.4') == '1995-02-04'
    assert convert_date('20180506') == '2018-05-06'
