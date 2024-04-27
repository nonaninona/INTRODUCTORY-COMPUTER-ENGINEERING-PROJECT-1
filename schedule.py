import data
import sys


def manage_schedule():
    while True:
        print("[관리자 모드] 실행할 메뉴를 선택하세요.")
        menu = input("1. 상영스케줄 추가\n2. 상영스케줄 수정\n3. 상영스케줄 삭제\n4. 종료\n입력 : ")
        if menu == "1":
            schedule_add_menu()
        elif menu == "2":
            schedule_edit_menu()
        elif menu == "3":
            schedule_delete_menu()
        elif menu == "4":
            print("관리자모드를 종료합니다.")
            break
        else:
            print("1~4 사이 숫자 내에서 입력해주세요.")


def schedule_add_menu():
    theater_list = []
    movie_table = data.get_movie_list()

    for info in data.get_theater_list():
        theater_id = info[0]
        theater_list.append(theater_id)

    while True:
        print("[상영스케줄 추가] 추가할 영화아이디, 상영관, 상영날짜, 상영시작시작을 입력해주세요.\n[등록된 영화 내역]\n영화명     러닝타임     영화아이디\n")
        for i, m, t in movie_table:
            print(m, "     ", t, "     ", i)
        print("현재 상영관 목록 : " + ", ".join(theater_list))
        user_input = input("입력 : ")

        try:
            movie_id, theater_id, date, start_time = user_input.strip().split(" ")
        except ValueError:
            print("잘못된 형식입니다.")
            continue

        if not check_start_time(start_time):  #시작시간 입력 검사 함수
            continue
        if not check_movie_id(movie_id, movie_table):  #영화아이디 입력 검사 함수
            continue
        if not check_theater_id(theater_id, movie_table):  #상영관 입력 검사 함수
            continue

        print("상영스케줄이 추가되었습니다.")

        return  #관리자 프롬프트로 이동


def check_start_time(start_time):
    if not sys.validate_time_syntax(start_time):
        print("상영시작시간의 문법적 형식이 올바르지 않습니다.")
        return False
    if not sys.validate_time_semantics(start_time):
        print("상영시작시간은 00:00 ~ 24:00 입니다. 다시 입력해주세요.")
        return False
    # 등록되어있는 상영스케줄과 비교하는 부분 추가
    return True


def check_movie_id(movie, movie_table):
    for id, _, _ in movie_table:
        if movie == id:
            return True
    print("일치하는 영화 아이디가 없습니다.")
    return False


def check_theater_id(theater_id, theater_list):
    if theater_id not in theater_list:
        print("일치하는 상영관이 없습니다.")
        return False
    else:
        return True


def schedule_edit_menu():
    schedule_table = data.get_schedule_list()

    while True:
        print("[상영스케줄 수정] 시간표아이디를 선택해주세요.\n시간표아이디     영화명     상영관     날짜     시간")
        for id, movie, theater, date, time in schedule_table:
            print(id + '     ' + movie + '     ' + theater + '상영관     ' + date + '     ' + time)
        user_input = input("입력 : ")

        if not user_input.isdigit():  #문법 규칙에 부합하지 않는 경우
            print("시간표 아이디는 1이상의 정수입니다.")
            continue
        else:
            if not check_schedule_id(user_input, schedule_table):  #의미규칙 1번에 부합하지 않는 경우
                continue
            if not check_schedule_reservation_empty(user_input):
                continue

            schedule_edit()  #실제 스케줄 상영하는 부분


def schedule_edit():
    theater_list = []
    movie_table = data.get_movie_list()

    for info in data.get_theater_list():
        theater_id = info[0]
        theater_list.append(theater_id)

    while True:
        print("[상영스케줄 수정] 수정할 영화아이디, 상영관, 상영날짜, 상영시작시작을 입력해주세요.\n[등록된 영화 내역]\n영화명     러닝타임     영화아이디\n")
        for i, m, t in movie_table:
            print(m, "     ", t, "     ", i)
        print("현재 상영관 목록 : " + ", ".join(theater_list))
        user_input = input("입력 : ")

        try:
            movie_id, theater_id, date, start_time = user_input.strip().split(" ")
        except ValueError:
            print("잘못된 형식입니다.")
            continue

        if not check_start_time(start_time):  # 시작시간 입력 검사 함수
            continue
        if not check_movie_id(movie_id, movie_table):  # 영화아이디 입력 검사 함수
            continue
        if not check_theater_id(theater_id, movie_table):  # 상영관 입력 검사 함수
            continue

        print("상영스케줄이 수정되었습니다.")

        return  # 관리자 프롬프트로 이동


def schedule_delete_menu():
    schedule_table = data.get_schedule_list()

    while True:
        print("[상영스케줄 삭제] 삭제할 시간표아이디를 선택해주세요.\n시간표아이디     영화명     상영관     날짜     시간")
        for id, movie, theater, date, time in schedule_table:
            print(id + '     ' + movie + '     ' + theater + '상영관     ' + date + '     ' + time)
        user_input = input("입력 : ")

        if not user_input.isdigit():  # 문법 규칙에 부합하지 않는 경우
            print("시간표 아이디는 1이상의 정수입니다.")
            continue
        else:
            if not check_schedule_id(user_input, schedule_table):  # 의미규칙 1번에 부합하지 않는 경우
                continue
            if not check_schedule_reservation_empty(user_input):
                continue

            delete_schedule(user_input)  # 실제 스케줄 상영하는 부분


def delete_schedule(delete_id):
    schedule_table = data.get_schedule_list()

    schedule_table = [schedule for schedule in schedule_table if schedule[0] != delete_id]

    with open("data/" + "schedule.txt", 'w', encoding='utf-8') as f:
        for id, movie, theater, date, time in schedule_table:
            f.write(f"{id}/{movie}/{theater}/{date}/{time}\n")


def check_schedule_id(user_input, schedule_table):
    for id, _, _, _, _ in schedule_table:
        if id == user_input:
            return True
    print("해당하는 상영스케줄이 없습니다. 다시 입력해주세요.")
    return False


def check_schedule_reservation_empty(user_input):
    # 어떻게?
    # print("이미 예약한 인원이 있어 수정이 불가능합니다. 다시 입력해주세요.")
    # return False
    return True
