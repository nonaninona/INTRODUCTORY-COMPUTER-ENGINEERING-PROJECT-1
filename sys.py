import sys
import data
import os.path


# import reservation

def file_exist():
    theater = os.path.exists('theater.txt')
    seat = os.path.exists('seat.txt')
    movie = os.path.exists('movie.txt')
    schedule = os.path.exists('schedule.txt')
    ticket = os.path.exists('ticket.txt')
    reservation = os.path.exists('reservation.txt')
    user = os.path.exists('user.txt')
    if not (theater and seat and movie and schedule and ticket and reservation and user):
        print('파일이 존재하지않음')


def validate_theater():
    data_list = data.sort_data(data.file_r('theater.txt'), 0)
    prev_id = -1
    for arr in data_list:
        if len(arr) != 2:
            print('theater.txt 저장 형식 오류')
            exit()
        for id, name in arr:
            if int(id) < 0:
                print('theater_id 오류')
            if prev_id == int(id):
                print('theater.txt id 중복')
                exit()
            else:
                prev_id = int(id)
            name_to_arr = [char for char in name]
            if name_to_arr[-1] != '\n':
                print('theater.txt 형식 오류 발생')
                exit()


def validate_seat():
    data_list = data.sort_data(data.file_r('theater.txt'), 0)
    prev_id = -1
    for arr in data_list:
        if len(arr) != 3:
            print('theater.txt 저장 형식 오류')
            exit()
        for seat_ID, theater_ID, seat_num in arr:
            if int(theater_ID) < 0:
                print('theater_id 오류')
            if prev_id == int(seat_ID):
                print('seat.txt seat_ID 중복')
                exit()
            else:
                prev_id = int(id)
            seat_num_to_arr = [char for char in seat_num]
            if seat_num_to_arr[-1] != '\n':
                print('seat.txt 형식 오류 발생')
                exit()
            if not ((seat_num_to_arr[0] >= 'A' and seat_num_to_arr[0] <= 'E') and (
                    int(seat_num_to_arr[1]) >= 0 and int(seat_num_to_arr[1]) <= 4)):
                print('seat.txt 좌석번호 형식 오류')


def validate_movie():
    data_list = data.sort_data(data.file_r('theater.txt'), 0)
    prev_id = -1
    for arr in data_list:
        if len(arr) != 3:
            print('theater.txt 저장 형식 오류')
            exit()
        for ID, name, time in arr:
            if int(ID) > 999 or int(ID) < 100:
                print('movie.txt ID형식 오류')
            if prev_id == int(ID):
                print('movie.txt movie ID 중복')
                exit()
            else:
                prev_id = int(ID)
            time_to_arr = [char for char in time]
            if time_to_arr[-1] != '\n':
                print('movie.txt 형식 오류 발생')
                exit()
            if int(time) < 50 or int(time) > 240:
                print('movie.txt 러닝타임 오류')


def validate_schedule():
    data_list = data.sort_data(data.file_r('theater.txt'), 0)
    prev_id = -1
    for arr in data_list:
        if len(arr) != 5:
            print('theater.txt 저장 형식 오류')
            exit()
        for timetable_ID, movie_ID, theater_ID, date, time in arr:

            if int(movie_ID) > 999 or int(movie_ID) < 100:
                print('movie_id형식 오류')

            if int(theater_ID) < 0:
                print('theater_id 오류')

            if prev_id == int(timetable_ID):
                print('movie.txt movie ID 중복')
                exit()
            else:
                prev_id = int(timetable_ID)
            if validate_date_syntax(date) & validate_date_semantics(date):
                time_to_arr = [char for char in time]
                if time_to_arr[-1] != '\n':
                    print('movie.txt 형식 오류 발생')
                    exit()
                if not (validate_date_semantics(time_to_arr[0:4]) and validate_time_syntax(
                        time_to_arr[0:4]) and validate_date_semantics(time_to_arr[5:9]) and validate_time_syntax(
                        time_to_arr[5:9])):
                    print('movie.txt 시간 형식 오류 발생')
            else:
                print('movie.txt date 형식 오류 발생')
                exit()


def validate_ticket():
    data_list = data.sort_data(data.file_r('ticket.txt'), 0)
    prev_id = -1
    for arr in data_list:
        if len(arr) != 4:
            print('ticket.txt 저장 형식 오류')
            exit()
        for ticket_ID, reservation_ID, seat_ID, timetable_ID in arr:
            if int(reservation_ID) < 0:
                print('reservation_id 오류')
            if int(seat_ID) < 0:
                print('seat_id 오류')
            if int(timetable_ID) < 0:
                print('timetable_id 오류')
            if prev_id == int(ticket_ID):
                print('ticket.txt ticket ID 중복')
                exit()
            else:
                prev_id = int(ticket_ID)
            timetable_ID_to_arr = [char for char in timetable_ID]
            if timetable_ID_to_arr[-1] != '\n':
                print('ticket.txt 형식 오류 발생')
                exit()


def validate_reservation():
    data_list = data.sort_data(data.file_r('reservation.txt'), 0)
    prev_id = -1
    for arr in data_list:
        if len(arr) != 4:
            print('reservation.txt 저장 형식 오류')
            exit()
        for reservation_ID, reservation_person_ID, num, cancel in arr:
            if int(reservation_ID) < 0:
                print('reservation_id 오류')
            if int(reservation_person_ID) > 9999 or int(reservation_person_ID) < 1000:
                print('user ID 형식 오류')
            if prev_id == int(reservation_ID):
                print('reservation.txt reservation ID 중복')
                exit()
            else:
                prev_id = int(reservation_ID)
            cancel_to_arr = [char for char in cancel]
            if cancel_to_arr[-1] != '\n':
                print('reservation.txt 형식 오류 발생')
                exit()
            if int(num) < 1 or int(num) > 5:
                print('reservation.txt 인원수 오류')
            if not (cancel_to_arr[0] == 'O' or cancel_to_arr[0] == 'X'):
                print('reservation.txt 예약최소여부 형식 오류')


def validate_user():
    data_list = data.sort_data(data.file_r('user.txt'), 0)
    prev_id = -1
    for arr in data_list:
        if len(arr) != 4:
            print('user.txt 저장 형식 오류')
            exit()
        for reservation_person_ID in arr:
            if int(reservation_person_ID) > 9999 or int(reservation_person_ID) < 1000:
                print('user.txt user ID 형식 오류')
            if prev_id == int(reservation_person_ID):
                print('user.txt user ID 중복')
                exit()
            else:
                prev_id = int(reservation_person_ID)
            id_to_arr = [char for char in reservation_person_ID]
            if id_to_arr[-1] != '\n':
                print('user.txt 형식 오류 발생')
                exit()


def validate_date_syntax(date_str):
    # 문법적 형식 검증
    if len(date_str) != 8 or not date_str.isdigit():
        # print("validate_date_syntax error")
        return False

    return True


def validate_date_semantics(date_str):
    # 의미적 규칙 검증
    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:])

    if year != 2024:
        # print("validate_date_semantics error")
        return False
    if month < 1 or month > 12:
        # print("validate_date_semantics error")
        return False
    if day < 1 or day > 31:
        # print("validate_date_semantics error")
        return False

    return True


def validate_time_syntax(time_str):
    # 문법적 형식 검증
    if len(time_str) != 5 or not time_str[:2].isdigit() or not time_str[3:].isdigit() or time_str[2] != ':':
        # print("validate_time_syntax error")
        return False

    return True


def validate_time_semantics(time_str):
    # 의미적 규칙 검증
    hour = int(time_str[:2])
    minute = int(time_str[3:])

    if hour < 0 or hour > 23:
        # print("validate_time_semantics error")
        return False
    if minute < 0 or minute > 59:
        # print("validate_time_semantics error")
        return False

    return True


# todo : def check_schedule(date_str, time_str): # 입력한 날짜 뒤에 영화 스케쥴이 있는지 확인


def input_date_time():
    while True:
        print("[날짜 및 시간 입력]")
        print("날짜와 현재 시간을 입력해주세요.")
        print("형식: (<날짜><space><시간>)")
        user_input = input("입력: ")

        date_str = user_input[:8]
        time_str = user_input[9:]
        # print(date_str)
        # print(time_str)
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
    print("[건국 영화관]")
    print("1. 로그인")
    print("2. 관리자모드")
    print("3. 종료")
    while True:
        choice = int(input("메뉴 입력: "))

        if choice == 1:
            print("로그인을 시작합니다.")
            login()
        elif choice == 2:
            print("관리자 모드를 시작합니다.")
            # todo : 관리자 모드 실행 함수
        elif choice == 3:
            print("프로그램을 종료합니다.")
            sys.exit(0)
        else:
            print("입력이 올바르지 않습니다. 다시 입력해 주세요.")


def validate_reserver_id(reserver_id):
    # 문법 형식 검증
    if not reserver_id.isdigit() or len(reserver_id) != 4:
        return False

    return True


def login():
    while True:
        reserver_id = input("아이디(4자리 숫자)를 입력하세요 : ")

        if not validate_reserver_id(reserver_id):
            print("아이디는 4자리 숫자여야 합니다. 다시 입력해주세요.")
            continue
        else:
            break

    check_reserver(reserver_id)
    # todo : 예약자 메뉴 출력

    return reserver_id


def find_reserver_id(reserver_id):
    found = False
    # user.txt 무결성 검사 진행 to do
    with open('user.txt', 'r', encoding='utf-8') as file:
        for line in file:
            existing_id, _ = line.strip().split('/')
            if existing_id == reserver_id:
                found = True
                break

    return found


def add_reserver(reserver_id, password=''):
    with open('user.txt', 'a', encoding='utf-8') as file:
        file.write(f"{reserver_id}/{password}\n")


def check_reserver(reserver_id, password=''):
    if find_reserver_id(reserver_id):
        return reserver_id
    else:
        add_reserver(reserver_id, password)
        return reserver_id
