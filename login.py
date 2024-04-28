import moviesystem
import administrator
import reservation
import data
import sys
# import data
# import reservation


def input_date_time():
    # moviesystem.file_exist()
    # moviesystem.validate_theater()
    # moviesystem.validate_seat()
    # moviesystem.validate_reservation()
    # moviesystem.validate_ticket()
    # moviesystem.validate_user()
    # moviesystem.validate_schedule()
    # moviesystem.validate_movie()
    while True:
        print("[날짜 및 시간 입력]")
        print("날짜와 현재 시간을 입력해주세요.")
        print("형식: (<날짜><space><시간>)")
        user_input = input("입력: ")

        date_str = user_input[:8]
        time_str = user_input[9:]
        #print(date_str)
        #print(time_str)
        # 입력 형식 및 문법 검증
        if (len(user_input) != 14 or user_input[8] != ' '
                or not validate_date_syntax(date_str)) or not validate_time_syntax(time_str):
            print("올바르지 않은 입력 형식입니다. 다시 입력해주세요.")
            continue

        # 날짜와 시간 추출
        date_str, time_str = user_input.split()

        # 의미규칙 검증 (여기에 추가적인 검증을 수행할 수 있습니다)
        if not validate_date_semantics(date_str) or not validate_time_semantics(time_str):
            print("예매가능한 영화가 없습니다. 다시 입력해주세요.")
            continue

        # 모든 검증 통과시 True 반환
        return user_input
    

def movie_theater_menu():
    while True:
        print("[건국 영화관]")
        print("1. 로그인")
        print("2. 관리자모드")
        print("3. 종료")
        choice = int(input("메뉴 입력: "))
        if choice == 1:
            print("로그인을 시작합니다.")
            user_id = login()
            reservation.print_reserve_menu(user_id)
        elif choice == 2:
            print("관리자 모드를 시작합니다.")
            # todo : 관리자 모드 실행 함수
            administrator.manage_menu()
        elif choice == 3:
            print("프로그램을 종료합니다.")
            sys.exit(0)
        else:
            print("입력이 올바르지 않습니다. 다시 입력해 주세요.")


def login():

    while True:
        user_id = input("아이디(4자리 숫자)를 입력하세요 : ")

        if not validate_user_id(user_id):
            print("아이디는 4자리 숫자여야 합니다. 다시 입력해주세요.")
            continue
        else:
            break

    ret = check_reserver(user_id)
    # todo : 예약자 메뉴 출력

    return ret


def validate_date_syntax(date_str):
    # 문법적 형식 검증
    if len(date_str) != 8 or not date_str.isdigit():
        #print("validate_date_syntax error")
        return False

    return True


def validate_date_semantics(date_str):
    # 의미적 규칙 검증
    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:])

    if year != 2024:
        #print("validate_date_semantics error")
        return False
    if month < 1 or month > 12:
        #print("validate_date_semantics error")
        return False
    if day < 1 or day > 31:
        #print("validate_date_semantics error")
        return False

    return True


def validate_time_syntax(time_str):
    # 문법적 형식 검증
    if len(time_str) != 5 or not time_str[:2].isdigit() or not time_str[3:].isdigit() or time_str[2] != ':':
        #print("validate_time_syntax error")
        return False

    return True


def validate_time_semantics(time_str):
    # 의미적 규칙 검증
    hour = int(time_str[:2])
    minute = int(time_str[3:])

    if hour < 0 or hour > 23:
        #print("validate_time_semantics error")
        return False
    if minute < 0 or minute > 59:
        #print("validate_time_semantics error")
        return False

    return True

# todo : def check_schedule(date_str, time_str): # 입력한 날짜 뒤에 영화 스케쥴이 있는지 확인

def validate_user_id(user_id):
    # 문법 형식 검증
    if not user_id.isdigit() or len(user_id) != 4:
        return False

    return True


def check_reserver(user_id):
    if is_user_id_exist(user_id):
        return user_id
    else:
        add_user(user_id)
        return user_id


def is_user_id_exist(user_id):
    found = False
    # user.txt 무결성 검사 진행 to do
    user_list = data.get_user_list()
    for (user_id1, ) in user_list:
            if user_id1 == user_id:
                found = True
                break
    # with open('user.txt', 'r', encoding='utf-8') as file:
    #     for line in file:
    #         existing_id, _ = line.strip().split('/')
    #         if existing_id == user_id:
    #             found = True
    #             break

    return found


def add_user(user_id):
    data.add_user(user_id)
    # with open('user.txt', 'a', encoding='utf-8') as file:
    #     file.write(f"{user_id}/{password}\n")
