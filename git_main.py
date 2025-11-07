import time
from git_config import (
    PLAYER_START_MONEY, CPU_START_MONEY, START_PANDON, pause
)
from git_ui import banner, draw_table, ask_player_action, ask_continue, say
from git_logic import (
    deal_two_hands, match_card, hand_label, computer_batting_choose
)

def play():
    # 초기 화면
    print('-' * 100)
    banner()
    pause(2)

    player_money = PLAYER_START_MONEY
    cpu_money = CPU_START_MONEY
    start_pandon = START_PANDON

    lose_stack = 0  # 플레이어가 다이하면 다음 공개에서 패배 처리
    mmoregame = 0   # 게임 루프 플래그

    while True:
        # 라운드 초기화
        pandon = 0
        player_pay = 0
        cpu_pay = 0
        turn = 0
        howmany = 0

        draw_table(['?', '?'], ['?', '?'], player_money, cpu_money, pandon)
        print('\n\n****  잠시 후 기본 베팅과 카드 분배를 시작합니다! ****\n\n')
        pause(1.5)

        # 기본 판돈
        pandon += start_pandon * 2
        player_money -= start_pandon
        cpu_money -= start_pandon

        # 카드 분배
        player_card, cpu_card = deal_two_hands()
        draw_table(player_card, ['?', '?'], player_money, cpu_money, pandon)

        # 베팅 라운드(단일 턴 구조: 플레이어 -> CPU)
        while True:
            # 플레이어 액션
            if turn == 0:
                choose = ask_player_action()

                if choose == 1 and player_money > (pandon / 2):
                    bet = pandon / 2
                    player_money -= bet
                    player_pay += bet
                    pandon += bet
                    howmany += 1
                    turn = 1
                    draw_table(player_card, ['?', '?'], player_money, cpu_money, pandon)
                    say('\n\n   상대의 베팅은...   \n\n', 1.0)

                elif choose == 2 and player_money > (pandon / 4):
                    bet = pandon / 4
                    player_money -= bet
                    player_pay += bet
                    pandon += bet
                    howmany += 1
                    turn = 1
                    draw_table(player_card, ['?', '?'], player_money, cpu_money, pandon)
                    say('\n\n   상대의 베팅은...   \n\n', 1.0)

                elif choose == 3:
                    # 받기(콜)
                    if player_money < (cpu_pay - player_pay):
                        # 돈 부족 → 올인 후 공개
                        print('-' * 100)
                        draw_table(player_card, ['?', '?'], player_money, cpu_money, pandon)
                        say('\n\n   돈 부족으로 올인하고 결과를 공개합니다   \n\n', 1.0)
                        pandon += player_money
                        player_money = 0
                        # 즉시 공개 단계로 이동
                        turn = 0
                        cpu_pay = 0
                        player_pay = 0
                        howmany = 0
                    else:
                        # 콜 금액만큼 맞추기
                        call_amt = (cpu_pay - player_pay)
                        player_money -= call_amt
                        pandon += call_amt
                        howmany = 0
                        player_pay = 0
                        cpu_pay = 0
                        turn = 1
                        draw_table(player_card, ['?', '?'], player_money, cpu_money, pandon)
                        say('\n\n   상대의 베팅은...   \n\n', 1.0)
                    # 플레이어가 받기를 선택하면 베팅 라운드 종료
                    break

                elif choose == 4:
                    # 다이 → 즉시 라운드 종료(상대가 판돈 회수)
                    cpu_money += pandon
                    pandon = 0
                    howmany = 0
                    player_pay = 0
                    cpu_pay = 0
                    turn = 0
                    lose_stack = 1
                    break

                else:
                    # 잘못된 입력/돈 부족
                    draw_table(player_card, ['?', '?'], player_money, cpu_money, pandon)
                    say('\n\n잘못된 입력이거나 돈이 부족합니다\n\n', 1.0)
                    continue

                # CPU 액션
                if turn == 1:
                    cpu_choose = computer_batting_choose(cpu_money, cpu_card, howmany)

                    # 자금 부족 시 자동 받기 전환
                    if cpu_choose == 1 and cpu_money < (pandon / 2):
                        cpu_choose = 3
                    elif cpu_choose == 2 and cpu_money < (pandon / 4):
                        cpu_choose = 3

                    if cpu_choose == 1 and cpu_money > (pandon / 2):
                        bet = pandon / 2
                        cpu_money -= bet
                        cpu_pay += bet
                        pandon += bet
                        howmany += 1
                        turn = 0
                        draw_table(player_card, ['?', '?'], player_money, cpu_money, pandon)
                        say('\n\n   상대방이 50%를 배팅했습니다!\n\n', 1.0)

                    elif cpu_choose == 2 and cpu_money > (pandon / 4):
                        bet = pandon / 4
                        cpu_money -= bet
                        cpu_pay += bet
                        pandon += bet
                        howmany += 1
                        turn = 0
                        draw_table(player_card, ['?', '?'], player_money, cpu_money, pandon)
                        say('\n\n   상대방이 25%를 배팅했습니다!\n\n', 1.0)

                    elif cpu_choose == 3:
                        # 받기(콜)
                        call_amt = (player_pay - cpu_pay)
                        cpu_money -= call_amt
                        pandon += call_amt
                        howmany = 0
                        player_pay = 0
                        cpu_pay = 0
                        turn = 0
                        draw_table(player_card, ['?', '?'], player_money, cpu_money, pandon)
                        say('\n\n   상대방이 받았습니다!\n\n', 1.0)
                        break

                    elif cpu_choose == 4:
                        # 다이
                        player_money += pandon
                        pandon = 0
                        howmany = 0
                        player_pay = 0
                        cpu_pay = 0
                        turn = 0
                        draw_table(player_card, ['?', '?'], player_money, cpu_money, pandon)
                        print('*' * 100)
                        print('\n\n\n   상대방이 포기했습니다!\n\n')
                        print('*' * 100)
                        break

        # 결과 공개
        draw_table(player_card, ['?', '?'], player_money, cpu_money, pandon)
        say('\n\n   패를 공개합니다!\n\n', 1.0)

        x = match_card(player_card)
        y = match_card(cpu_card)
        xxx = hand_label(x)
        yyy = hand_label(y)

        pause(0.5)
        if (x > y) and (lose_stack == 0):
            print('*' * 100)
            print('\n\n\n   이겼습니다!!!!\n\n')
            print(f'당신의 족보 : {xxx}')
            print(f'상대의 족보 : {yyy}')
            print('*' * 100)
            player_money += pandon
            pandon = 0

        elif (y > x) or (lose_stack == 1):
            print('*' * 100)
            print('\n\n\n   졌습니다ㅠㅠㅠ\n\n')
            print(f'당신의 족보 : {xxx}')
            print(f'상대의 족보 : {yyy}')
            print('*' * 100)
            cpu_money += pandon
            pandon = 0
            lose_stack = 0

        else:
            print('*' * 100)
            print('\n\n\n   비겼습니다 ㅡㅡ\n\n')
            print(f'당신의 족보 : {xxx}')
            print(f'상대의 족보 : {yyy}')
            print('*' * 100)
            player_money += pandon / 2
            cpu_money += pandon / 2
            pandon = 0

        draw_table(['?', '?'], ['?', '?'], int(player_money), int(cpu_money), int(pandon))

        # 파산 체크
        if player_money <= 0:
            print('패배....')
            break
        if cpu_money <= 0:
            print('승~~ 리~~')
            break

        # 다음 라운드 여부
        mg = ask_continue()
        if mg == 1:
            continue
        else:
            print('-' * 100)
            print('게임을 종료합니다')
            print('-' * 100)
            break

if __name__ == '__main__':
    play()
