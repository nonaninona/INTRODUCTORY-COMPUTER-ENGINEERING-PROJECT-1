import data
import moviesystem


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


def get_movie_data(flag, id):  # flag : name/runtime 중 하나
    # 영화아이디로 영화 정보 가져오는 함수
    movie_list = get_movie_list()

    for movie_id, movie_name, movie_runtime in movie_list:
        if movie_id == id:
            if flag == "name":
                return movie_name
            elif flag == "runtime":
                return movie_runtime
            else:
                print("flag 값이 잘못 입력됨")


def manage_schedule():
    while True:
        print("[관리자 모드] 실행할 메뉴를 선택하세요.")
        menu = input("1. 상영스케줄 추가\n2. 상영스케줄 수정\n3. 상영스케줄 삭제\n4. 종료\n입력 : ")
        if menu == "1":
            schedule_add_menu()
            break
        elif menu == "2":
            schedule_edit_menu()
            break
        elif menu == "3":
            schedule_delete_menu()
            break
        elif menu == "4":
            print("관리자모드 메뉴로 돌아갑니다.")
            break
        else:
            print("1~4 사이 숫자 내에서 입력해주세요.")


def schedule_add_menu():
    movie_list = get_movie_list()
    theater_list = get_theater_list()
    schedule_list = get_schedule_list()

    # 상영스케줄 추가함수
    while True:
        print("[상영스케줄 추가] 추가할 영화아이디, 상영관, 상영날짜, 상영시작시간을 입력해주세요.\n[등록된 영화 내역]\n영화명     러닝타임     영화아이디")
        for i in range(0, len(movie_list)):
            print(movie_list[i][1] + "    " + movie_list[i][2] + "    " + movie_list[i][0])
        print("현재 상영관 목록 : " + ", ".join(theater_list))
        user_input = input("입력 : ")

        try:
            movie_id, theater_id, date, time = user_input.strip().split()
            if not validate_input(movie_id, theater_id, date, time):
                print("[오류] 올바른 형식으로 입력해주세요.")
                continue
        except ValueError:
            print("[오류] 올바른 형식으로 입력해주세요.")
            continue

        if not check_movie_id(movie_id, movie_list):  # 영화아이디 입력 검사 함수
            continue
        if not check_theater_id(theater_id, theater_list):  # 상영관 입력 검사 함수
            continue
        if not check_time_overlap(0, movie_id, theater_id, date, time):  # 시간표가 중복되는지 검사하는 함수
            continue

        if len(schedule_list) == 0:
            timetable_id = 1
        else:
            timetable_id = int(schedule_list[len(schedule_list) - 1][0]) + 1

        data.add_schedule(str(timetable_id), theater_id, movie_id, date, time)
        print("상영스케줄이 추가되었습니다.")
        return  # 관리자 프롬프트로 이동


def schedule_edit_menu():
    schedule_table = data.get_schedule_list()

    while True:
        print("[상영스케줄 수정] 시간표아이디를 선택해주세요.\n시간표아이디     영화명     상영관     날짜     시간")
        for id, theater, movie, date, time in schedule_table:
            movie_name = get_movie_data("name", movie)
            runtime = get_movie_data("runtime", movie)
            print(
                '     ' + id + '        ' + movie_name + '     ' + theater + '상영관     ' + date + '     ' + time + ' - ' + calculate_end_time(
                    time, runtime))
        user_input = input("입력 : ")

        if not user_input.isdigit():  # 문법 규칙에 부합하지 않는 경우
            print("번호를 입력해주세요. 다시 입력해주세요.")
            continue
        else:
            if not check_schedule_id(user_input, schedule_table):  # 의미규칙 1번에 부합하지 않는 경우
                continue
            if not check_schedule_reservation_empty(user_input):
                continue
            schedule_edit_menu2(user_input)
            break


def schedule_edit_menu2(timetable_id):
    movie_list = get_movie_list()  # 영화아이디 영화명 러닝타임
    theater_list = get_theater_list()

    while True:
        print("[상영스케줄 수정] 수정할 영화아이디, 상영관, 상영날짜, 상영시작시간을 입력해주세요.\n[등록된 영화 내역]\n영화명     러닝타임     영화아이디")
        for i in range(0, len(movie_list)):
            print(movie_list[i][1] + "    " + movie_list[i][2] + "    " + movie_list[i][0])
        print("현재 상영관 목록 : " + ", ".join(theater_list))
        user_input = input("입력 : ")

        try:
            movie_id, theater_id, date, time = user_input.strip().split()
            if not validate_input(movie_id, theater_id, date, time):
                print("[오류] 올바른 형식으로 입력해주세요.")
                continue
        except ValueError:
            print("[오류] 올바른 형식으로 입력해주세요.")
            continue

        if not check_movie_id(movie_id, movie_list):  # 영화아이디 입력 검사 함수
            continue
        if not check_theater_id(theater_id, theater_list):  # 상영관 입력 검사 함수
            continue
        if not check_time_overlap(timetable_id, movie_id, theater_id, date, time):  # 시간표가 중복되는지 검사하는 함수
            continue

        edit_schedule(timetable_id, movie_id, theater_id, date, time)  # 실제 스케줄 수정하는 부분
        print("상영스케줄이 수정되었습니다.")
        return  # 관리자 프롬프트로 이동


def edit_schedule(timetable_id, movie_id, theater_id, date, time):
    # 실제 스케줄을 수정하는 부분
    delete_schedule(timetable_id)
    data.add_schedule(timetable_id, theater_id, movie_id, date, time)


def schedule_delete_menu():
    # 상영스케줄 삭제 메뉴 함수
    schedule_table = data.get_schedule_list()

    while True:
        print("[상영스케줄 삭제] 삭제할 시간표아이디를 선택해주세요.\n시간표아이디     영화명     상영관     날짜     시간")
        for id, theater, movie, date, time in schedule_table:
            movie_name = get_movie_data("name", movie)
            runtime = get_movie_data("runtime", movie)
            print(
                '     ' + id + '        ' + movie_name + '     ' + theater + '상영관     ' + date + '     ' + time + ' - ' + calculate_end_time(
                    time, runtime))

        user_input = input("입력 : ")

        if not user_input.isdigit():  # 문법 규칙에 부합하지 않는 경우
            print("시간표아이디는 1이상의 정수입니다.")
            continue
        else:
            if not check_schedule_id(user_input, schedule_table):  # 의미규칙 1번에 부합하지 않는 경우
                continue
            if not check_schedule_reservation_empty(user_input):
                continue

        delete_schedule(user_input)  # 실제 스케줄 삭제하는 부분
        print("성공적으로 삭제되었습니다.")
        return


def delete_schedule(delete_id):
    # 실제 스케줄을 삭제하는 부분
    schedule_table = data.get_schedule_list()
    schedule_table = [schedule for schedule in schedule_table if schedule[0] != delete_id]

    with open("data/" + "schedule.txt", 'w', encoding='utf-8') as f:
        for id, movie, theater, date, time in schedule_table:
            f.write(f"{id}/{movie}/{theater}/{date}/{time}\n")


def validate_input(movie_id, theater_id, date, time):
    # 사용자 입력의 유효성을 검사하는 함수
    if not moviesystem.validate_movie_id(movie_id):
        return False
    if not moviesystem.validate_theater_id(theater_id):
        return False
    if not (moviesystem.validate_date_semantics(date) or moviesystem.validate_date_syntax(date)):
        return False
    if not (moviesystem.validate_time_semantics(time) or moviesystem.validate_time_syntax(time)):
        return False
    return True


def check_movie_id(movie, movie_list):
    # 기존 영화아이디와 일치하는 지 검사하는 함수
    for i in range(0, len(movie_list)):
        if movie == movie_list[i][0]:
            return True
    print("일치하는 영화아이디가 없습니다.")
    return False


def check_theater_id(theater_id, theater_list):
    # 기존 상영관아이디와 일치하는 지 검사하는 함수
    if theater_id not in theater_list:
        print("일치하는 상영관아이디가 없습니다.")
        return False
    else:
        return True


def check_time_overlap(flag, movie_id, theater_id, date, time):  # flag add인 경우 0 / edit인 경우 1이상 정수 중 하나
    # 추가하고자 하는 스케줄이 현재 스케줄에 들어갈 수 있는지 검사하는 함수
    schedule_list = get_schedule_list()
    overlap_theater_id_list = []

    for i in range(0, len(schedule_list)):
        # 상영관이 겹치는 스케줄만 가져옴
        if theater_id == schedule_list[i][1] and str(int(flag) + 1) != schedule_list[i][0]:
            overlap_theater_id_list.append(schedule_list[i])
    if len(overlap_theater_id_list) == 0:  # 상영관이 겹치지 않는다면 바로 추가
        return True

    # 새로 넣을 스케줄 정보
    new_hour = int(time[:2])
    new_minute = int(time[3:])
    new_runtime = get_movie_data("runtime", movie_id)
    new_end = calculate_end_time(time, new_runtime)

    for i in range(0, len(overlap_theater_id_list)):
        if date == overlap_theater_id_list[i][3]:  # 날짜가 일치하다면
            runtime = get_movie_data("runtime", overlap_theater_id_list[i][2])  # 영화의 runtime 가져옴
            start = overlap_theater_id_list[i][4]  # 각 영화의 시작시간 가져옴
            end = calculate_end_time(start, runtime)  # 각 영화의 종료 시간 구하기

            if new_hour >= int(start[:2]) & new_hour <= int(end[:2]):
                if new_hour == int(end[:2]):
                    if new_minute >= int(end[3:]) + 10:
                        return True
                    else:
                        print("해당 상영관의 상영스케줄과 겹칩니다.\n상영시작시간은 그 전 영화의 종료시간보다 + 10분 이상이여야 합니다.")
                        return False
                else:
                    print("해당 상영관의 상영스케줄과 겹칩니다.\n상영시작시간은 그 전 영화의 종료시간보다 + 10분 이상이여야 합니다.")
                    return False

            if int(new_end[:2]) >= int(start[:2]) & int(new_end[:2]) <= int(end[:2]):
                if int(new_end[:2]) == int(start[:2]):
                    if new_minute >= int(end[3:]) - 10:
                        return True
                    else:
                        print("해당 상영관의 상영스케줄과 겹칩니다.\n상영시작시간은 그 전 영화의 종료시간보다 + 10분 이상이여야 합니다.")
                        return False
                else:
                    print("해당 상영관의 상영스케줄과 겹칩니다.\n상영시작시간은 그 전 영화의 종료시간보다 + 10분 이상이여야 합니다.")
                    return False
    return True


def calculate_end_time(start_time, runtime):
    # 영화의 끝나는 시간을 구하는 함수 / start_time : "00:00", runtime : "000" 형식으로 받음
    start_hour = int(start_time[:2])
    start_minute = int(start_time[4:])

    runtime_hour = int(runtime) // 60
    runtime_minute = int(runtime) % 60

    end_hour = start_hour + runtime_hour
    end_minute = start_minute + runtime_minute

    if end_minute >= 60:
        end_hour += 1
        end_minute -= 60

    end_hour %= 24

    end_time = '{:02d}:{:02d}'.format(end_hour, end_minute)
    return end_time  # 문자열 00:00 형식으로 반환


def check_schedule_id(user_input, schedule_table):
    # 선택한 상영스케줄이 실제 상영스케줄 리스트에 있는지 검사하는 함수
    for id, _, _, _, _ in schedule_table:
        if id == user_input:
            return True
    print("해당하는 상영스케줄이 없습니다. 다시 입력해주세요.")
    return False


def check_schedule_reservation_empty(timetable_id):
    # 해당 스케줄에 예약자가 있는지 검사하는 함수
    ticket_list = data.get_ticket_list()  # 티켓아이디 예매아이디 좌석아이디 시간표아이디 티켓가격
    reservation_list = data.get_reservation_list()  # 예매아이디 예약자아이디 예약인원수 예약취소여부

    for _, reserv_id, _, time_id, _ in ticket_list:
        if timetable_id == time_id:
            for id, _, _, cancel in reservation_list:
                if reserv_id == id and cancel == "X":
                    print("이미 예약한 인원이 있어 수정, 삭제가 불가능합니다. 다시 입력해주세요.")
                    return False
    return True
