# ui.py
from git_config import pause

def banner():
    print('-' * 100)
    print('\n\n\n\n\n    SDT - 섯다 전문가 양성 과정    \n\n\n\n\n')
    print('-' * 100)

def draw_table(player_card, cpu_card, player_money, cpu_money, pandon):
    print('-' * 100)
    print(f'당신의 남은 돈 : {int(player_money)}')
    print(f'상대의 남은 돈 : {int(cpu_money)}')
    print()
    print(f'판 돈 : {int(pandon)}')
    print(f' 당신의 패  ==>  {player_card}')
    print(f' 상대의 패  ==>  {cpu_card}')
    print('-' * 100)

def ask_player_action() -> int:
    """플레이어 베팅 선택 입력"""
    while True:
        try:
            choice = int(input('[1. 50% 베팅]\n[2. 25% 베팅]\n[3. 받기]\n[4. 다이]\n\n입력 : '))
            if choice in (1, 2, 3, 4):
                return choice
        except ValueError:
            pass
        print('\n잘못된 입력입니다. 다시 입력하세요.\n')

def ask_continue() -> int:
    """라운드 종료 후 계속 여부"""
    while True:
        try:
            mg = int(input('\n\n[1. 계속] [2. 종료]\n\n입력 : '))
            if mg in (1, 2):
                return mg
        except ValueError:
            pass
        print('\n잘못된 입력입니다. 다시 입력하세요.\n')

def say(msg: str, wait: float = 1.0):
    print(msg)
    pause(wait)
