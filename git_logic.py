import random
from git_config import CARD_LIST

def match_card(x):
    """
    원본 규칙 그대로 유지:
    - 두 장의 '월' 숫자만 사용해 점수를 계산
    - 같은 월이면 '땡': 10 + 월
    - 다르면 '끗': (합 % 10)
    """
    winrate = 0
    # 'n월카드 m' -> 앞자리 숫자 추출
    a = int(x[0].split('월')[0])
    b = int(x[1].split('월')[0])
    if a == b:
        winrate += 10 + a
    else:
        winrate += (a + b)
        if winrate >= 10:
            winrate -= 10
    return winrate

def hand_label(score: int) -> str:
    """출력용 라벨(땡/끗)"""
    if score > 10:
        return f'{score-10} 땡'
    else:
        return f'{score} 끗'

def deal_two_hands():
    """
    플레이어 2장, CPU 2장 배분
    (원본은 0~18에서 샘플링했지만 카드가 20장이라 인덱스 19가 빠졌음.
     여기서는 버그를 고쳐 0~19 전체에서 4장을 뽑음.)
    """
    idx = random.sample(range(0, 20), 4)
    player = [CARD_LIST[idx[0]], CARD_LIST[idx[1]]]
    cpu    = [CARD_LIST[idx[2]], CARD_LIST[idx[3]]]
    return player, cpu

def computer_batting_choose(cpu_money, card, howmany):
    """
    원본 CPU 베팅 로직 + 블러핑 유지
    """
    # match_card는 카드 내용을 받아 점수 계산
    card_count = match_card(card) / 19
    count = cpu_money / 1_000_000
    per = (0.2 * count) + (0.8 * card_count)

    # 라운드가 길어질수록 보수적으로
    if howmany > 3: per *= 0.9
    if howmany > 5: per *= 0.9
    if howmany > 7: per *= 0.9

    if per >= 0.7:
        choose = 1
    elif 0.4 <= per < 0.7:
        choose = 2
    elif 0.2 <= per < 0.4:
        choose = 3
    else:
        choose = 4

    # 블러핑
    x = random.randint(1, 10)
    if x > 8:
        choose = 1

    return choose
