import sys
import data
import reserve

"""

구조

print_reserve_menu : 메뉴 출력 기능, 최상위 반복문
- reserve : 예매하기 기능
- print_check_reserveation_menu : 예매조회 기능
    - print_cancel_reservation_menu : 예매취소 기능


"""

# 메뉴 출력
def print_reserve_menu(user_id):
    while True:
        print("[메인 메뉴] 실행할 메뉴를 선택하세요.")
        print("1. 영화예매하기")
        print("2. 영화조회하기")
        print("3. 로그아웃")
        print("4. 종료하기")
        choice = int(input("입력: "))
        #validation 필요##################
        if choice == 1:
            print("영화 예매")
            reserve.reserve(user_id)
        elif choice == 2:
            print("영화 조회")
            print_check_reservation_menu(user_id)
        elif choice == 3:
            print("로그아웃이 완료되었습니다.")
            break
        elif choice == 4:
            print("프로그램을 종료합니다.")
            sys.exit(0)
        else: # 비정상 입력
            print("화면에 출력된 숫자 내에서 입력해주세요")


# 예매 조회 기능
def print_check_reservation_menu(user_id):    
    reservation_list = data.get_reservation_list()
    ticket_list = data.get_ticket_list()
    reservation_table = get_user_reseration_list(user_id, reservation_list, ticket_list)

    if not reservation_table: # 예매한 영화가 없는 경우
        print("예매한 영화가 없습니다")
        return
    
    print_reservation_table(reservation_table)

    while True:
        print("※(예매 취소를 원할 시 '1', 이전 화면으로 돌아가려면 '2'를 눌러주세요)")
        print("1. 영화 예매 취소")
        print("2. 돌아가기")
        choice = int(input("입력: "))

        if choice == 1:
            print("예매 취소")
            print_cancel_reservation_menu(user_id)
        elif choice == 2:
            print("메인메뉴로 돌아갑니다.")
            break
        # 왜 비정상 입력에 대한 게 없지


# 예매 취소 기능
def print_cancel_reservation_menu(user_id):
    reservation_list = data.get_reservation_list()
    ticket_list = data.get_ticket_list()
    reservation_table = get_user_reseration_list(user_id, reservation_list, ticket_list)

    # 예매내역
    print_reservation_table(reservation_table)

    while True:
        print("예매취소할 예매아이디를 입력해주세요")
        choice = int(input("예매아이디 입력: "))

        if validate_cancel_input(choice): # 문법 규칙 위배
            print("올바른 예매아이디를 입력해 주시기 바랍니다.")
        else: # 의미 규칙 위배(없는 아이디)
            print("예매한 올바른 예매아이디를 입력해주시기 바랍니다.")
            break
        
    cancel_reservation(user_id, choice)
    print("영화 예매취소가 완료되었습니다. 메인메뉴로 돌아갑니다.")












##### 여기서부턴 짜잘이 함수들 #####


























### reserve 짜잘이 함수들 ###

def validate_cancel_input(choice):
    return True


def cancel_reservation(user_id, choice):
    return True











### reserve 짜잘이 함수들 ###

def get_user_reseration_list(user_id, reservation_list, ticket_list):
    return []

def print_reservation_table():
    # 예매내역
    # 예매아이디  영화제목   날짜/상영시간     상영관  예약인원수 시작좌석 시간표아이디
    #    1       파묘   04.04/08-10      1관     2       A3      1
    print()