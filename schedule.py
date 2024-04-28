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


def get_movie_list():
    # 각 영화 데이터를 [영화아이디, 영화명, 러닝타임]으로 리스트를 만들어주는 함수
    movie_list = []
    for id, movie_name, runtime in data.get_movie_list():
        movie_list.append([id, movie_name, runtime])
    return movie_list


def get_theater_list():
    # 상영관아이디 데이터를 리스트로 저장
    theater_list = []
    for info in data.get_theater_list():
        theater_id = info[0]
        theater_list.append(theater_id)
    return theater_list


def get_schedule_list():
    # 상영스케줄 데이터를 [시간표아이디, 상영관아이디, 영화아이디, 날짜(20240000), 시작시간]으로 리스트를 만들어주는 함수
    schedule_list = []
    for schedule_id, theater_id, movie_id, date, start_time in data.get_schedule_list():
        schedule_list.append([schedule_id, theater_id, movie_id, date, start_time])
    return schedule_list


def calculate_end_time(start_time, runtime):
    # 영화의 끝나는 시간을 구하는 함수 / start_time : "00:00", runtime : "000" 형식으로 받음
    start_hour = int(start_time[:2])
    start_minute = int(start_time[4:])
    print(f"시간 : {start_hour} : 분 : {start_minute}")

    runtime_hour = int(runtime) // 60
    runtime_minute = int(runtime) % 60

    end_hour = start_hour + runtime_hour
    end_minute = start_minute + runtime_minute

    if end_minute >= 60:
        end_hour += 1
        end_minute -= 60

    end_hour %= 24

    end_time = '{:02d}:{:02d}'.format(end_hour, end_minute)
    print(end_time)
    return end_time  # 문자열 00:00 형식으로 반환


def schedule_add_menu():
    while True:
        movie_list = get_movie_list()
        theater_list = get_theater_list()

        print("[상영스케줄 추가] 추가할 영화아이디, 상영관, 상영날짜, 상영시작시작을 입력해주세요.\n[등록된 영화 내역]\n영화명     러닝타임     영화아이디")
        for i in range(0, len(movie_list)):
            print(movie_list[i][1]+"    "+movie_list[i][2]+"    "+movie_list[i][0])
        print("현재 상영관 목록 : " + ", ".join(theater_list))
        user_input = input("입력 : ")

        try:
            movie_id, theater_id, date, start_time = user_input.strip().split(" ")
        except ValueError:
            print("잘못된 형식입니다.")
            continue

        if not check_start_time(start_time):  # 시작시간 입력 검사 함수
            continue
        if not check_time_overlap(theater_id, start_time):  # 시간표가 중복되는지 검사하는 함수
            continue
        if not check_movie_id(movie_id, movie_list):  # 영화아이디 입력 검사 함수
            continue
        if not check_theater_id(theater_id, theater_list):  # 상영관 입력 검사 함수
            continue

        if len(theater_list)==0:
            timetable_id = 1
        else:
            timetable_id = theater_list[len(theater_list) - 1][0] + 1

        data.add_schedule(timetable_id, theater_id, movie_id, date, start_time)
        print("상영스케줄이 추가되었습니다.")

        return  #관리자 프롬프트로 이동


def check_start_time(new_start_time):
    # 추가하고자하는 스케줄의 시작시간이 유효한지 검사하는 함수
    if not sys.validate_time_syntax(new_start_time):
        print("상영시작시간의 문법적 형식이 올바르지 않습니다.")
        return False
    if not sys.validate_time_semantics(new_start_time):
        print("상영시작시간은 00:00 ~ 24:00 입니다. 다시 입력해주세요.")
        return False
    return True


def check_time_overlap(theater_id, new_start_time):
    schedule_list = get_schedule_list()
    overlap_theater_id_list = []

    for i in range(0, len(schedule_list)):
        # 상영관이 겹치는 스케줄만 가져옴
        if theater_id == schedule_list[i][1]:
            overlap_theater_id_list.append(schedule_list[i])

    for i in range(0, len(overlap_theater_id_list)):
        # 스케줄이 겹치는지 확인하는 부분

        for id, _, runtime in get_movie_list(): # 영화의 runtime 가져옴
            if id == schedule_list[i][2]:
                runtime = runtime
                break
        start_time = schedule_list[i][4]  # 각 영화의 시작시간 가져옴
        end_time = calculate_end_time(start_time, runtime)  # 각 영화의 종료 시간 구하기

        new_time_hour = int(new_start_time[:2])
        new_time_minute = int(new_start_time[4:])

        if new_time_hour >= int(start_time[:2]) & new_time_hour <= int(end_time[:2]):  # 이미 존재하는 상영스케줄 러닝 타임과 중복이고
            if new_time_minute >= int(end_time[4:]) + 10:  # 종료 시간+10분이라면 추가 가능
                return True
            else:
                print("같은 상영관 내에서 상영시작시간은 그 전 영화의 종료시간보다 + 10분 이상이여야 합니다.")
                return False

    return True


def check_movie_id(movie, movie_list):
    # 기존 영화아이디와 일치하는 지 검사하는 함수
    for i in range(0, len(movie_list)):
        if movie == movie_list[i][0]:
            return True
    print("일치하는 영화 아이디가 없습니다.")
    return False


def check_theater_id(theater_id, theater_list):
    # 기존 상영관아이디와 일치하는 지 검사하는 함수
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
            print('     ' + id + '         ' + movie + '     ' + theater + '상영관     ' + date + '     ' + time)
        user_input = input("입력 : ")

        if not user_input.isdigit():  #문법 규칙에 부합하지 않는 경우
            print("시간표아이디는 1이상의 정수입니다.")
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
        print("[상영스케줄 수정] 수정할 영화아이디, 상영관, 상영날짜, 상영시작시작을 입력해주세요.\n[등록된 영화 내역]\n영화명     러닝타임     영화아이디")
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
        if not check_time_overlap(theater_id, start_time):  # 시간표가 중복되는지 검사하는 함수
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
            print('     ' + id + '         ' + movie + '     ' + theater + '상영관     ' + date + '     ' + time)
        user_input = input("입력 : ")

        if not user_input.isdigit():  # 문법 규칙에 부합하지 않는 경우
            print("시간표아이디는 1이상의 정수입니다.")
            continue
        else:
            if not check_schedule_id(user_input, schedule_table):  # 의미규칙 1번에 부합하지 않는 경우
                continue
            if not check_schedule_reservation_empty(user_input):
                continue
        delete_schedule(user_input)  # 실제 스케줄 상영하는 부분
        break


def delete_schedule(delete_id):
    schedule_table = data.get_schedule_list()

    schedule_table = [schedule for schedule in schedule_table if schedule[0] != delete_id]

    with open("data/" + "schedule.txt", 'w', encoding='utf-8') as f:
        for id, movie, theater, date, time in schedule_table:
            f.write(f"{id}/{movie}/{theater}/{date}/{time}\n")

    print("상영스케줄이 삭제되었습니다.")


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


manage_schedule()