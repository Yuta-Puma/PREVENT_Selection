%%writefile date_converter.py
import pandas as pd
import re

# 和暦の変換用辞書
era_dict = {
    'R': 2018,  # 令和 (2019年5月1日から)
    'H': 1988,  # 平成 (1989年1月8日から)
    'S': 1925,  # 昭和 (1926年12月25日から)
    'T': 1911,  # 大正 (1912年7月30日から)
    'M': 1867   # 明治 (1868年1月25日から)
}

def convert_date(date_str):
    # 和暦の処理
    if '平成' in date_str:
        year = int(re.search(r'\d+', date_str).group())  # 平成の年を抽出
        year += era_dict['H']  # 西暦に変換
        date_str = re.sub(r'平成\d+年', f'{year}年', date_str)  # 正しい年を置換
    elif '令和' in date_str:
        year = int(re.search(r'\d+', date_str).group())  # 令和の年を抽出
        year += era_dict['R']  # 西暦に変換
        date_str = re.sub(r'令和\d+年', f'{year}年', date_str)
    elif '昭和' in date_str:
        year = int(re.search(r'\d+', date_str).group())  # 昭和の年を抽出
        year += era_dict['S']  # 西暦に変換
        date_str = re.sub(r'昭和\d+年', f'{year}年', date_str)
    elif '大正' in date_str:
        year = int(re.search(r'\d+', date_str).group())  # 大正の年を抽出
        year += era_dict['T']  # 西暦に変換
        date_str = re.sub(r'大正\d+年', f'{year}年', date_str)
    elif '明治' in date_str:
        year = int(re.search(r'\d+', date_str).group())  # 明治の年を抽出
        year += era_dict['M']  # 西暦に変換
        date_str = re.sub(r'明治\d+年', f'{year}年', date_str)

    # 和暦の日付フォーマットの処理 (例: H5/2/6 や H5年2月6日 -> 西暦に変換)
    # 年、月、日をスラッシュ形式に変更
    date_str = re.sub(r'(\d+)年(\d+)月(\d+)日', r'\1/\2/\3', date_str)

    # スラッシュ区切りの和暦フォーマットに対応
    if re.match(r'[RHS]\d+/\d+/\d+', date_str):
        era = date_str[0]  # 和暦の記号を抽出（例: H, R, S）
        year, month, day = map(int, date_str[1:].split('/'))
        year += era_dict[era]  # 西暦に変換
        return f'{year:04d}-{month:02d}-{day:02d}'
    
    # 西暦の日付フォーマットの処理 (例: 1995.2.4, 2008/12/23, 20180506)
    try:
        if '.' in date_str:
            return pd.to_datetime(date_str, format='%Y.%m.%d').strftime('%Y-%m-%d')
        elif '/' in date_str:
            return pd.to_datetime(date_str, format='%Y/%m/%d').strftime('%Y-%m-%d')
        elif len(date_str) == 8 and date_str.isdigit():
            return pd.to_datetime(date_str, format='%Y%m%d').strftime('%Y-%m-%d')
    except ValueError:
        pass

    # デフォルト処理
    converted_date = pd.to_datetime(date_str, errors='coerce')
    if pd.isna(converted_date):
        print(f"Error: Could not parse date format: {date_str}")  # 原因を出力
        return 'Invalid date format'  # 変換できない場合
    return converted_date.strftime('%Y-%m-%d')

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

!pip install pytest
!pytest test_date_converter.py