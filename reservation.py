import sys
import data
import reserve
import moviesystem
import coupon

"""

구조

print_reserve_menu : 메뉴 출력 기능, 최상위 반복문
- reserve.reserve : 예매하기 기능
- print_check_reservation_menu : 예매조회 기능
    - print_cancel_reservation_menu : 예매취소 기능


"""


# 메뉴 출력
def print_reserve_menu(user_id, date_time):
    while True:
        print("[메인 메뉴] 실행할 메뉴를 선택하세요.")
        print("1. 영화예매하기")
        print("2. 영화조회하기")
        print("3. 나의 쿠폰 확인하기")
        print("4. 로그아웃")
        print("5. 종료하기")
        choice = input("입력: ")

        if not validate_main_syntax(choice):  # 문법 규칙 위배
            print("화면에 출력된 숫자 내에서 입력해주세요")
        else:
            if int(choice) == 1:
                reserve.reserve(user_id, date_time)
            elif int(choice) == 2:
                print("영화 조회")
                print_check_reservation_menu(user_id)
            elif int(choice) == 3:
                print("나의 쿠폰 조회")
                coupon.print_my_coupon(user_id)
            elif int(choice) == 4:
                print("로그아웃이 완료되었습니다.")
                break
            elif int(choice) == 5:
                print("프로그램을 종료합니다.")
                sys.exit(0)
            else:  # 비정상 입력
                print("화면에 출력된 숫자 내에서 입력해주세요")


# 예매 조회 기능
def print_check_reservation_menu(user_id):
    reservation_list = data.get_reservation_list()
    ticket_list = data.get_ticket_list()
    movie_list = data.get_movie_list()
    theater_list = data.get_theater_list()
    seat_list = data.get_seat_list()
    schedule_list = data.get_schedule_list()
    reservation_table = get_user_reservation_table(user_id, reservation_list, ticket_list, movie_list, theater_list,
                                                   seat_list, schedule_list)

    if not reservation_table:  # 예매한 영화가 없는 경우
        print("예매한 영화가 없습니다")
        return

    print("영화 조회")
    print_reservation_table(reservation_table)

    while True:
        print("※(예매 취소를 원할 시 '1', 이전 화면으로 돌아가려면 '2'를 눌러주세요)")
        print("1. 영화 예매 취소")
        print("2. 영화 예매 변경")
        print("3. 돌아가기")
        choice = input("입력: ")

        if not validate_choice_syntax(choice):  # 문법 규칙 위배
            print("입력이 올바르지 않습니다. 다시 입력해주세요.")
        else:
            if int(choice) == 1:
                print("예매 취소")
                print_cancel_reservation_menu(user_id)
                
                break
            elif int(choice) == 2:
                print_change_reservation_menu(user_id)
                break
            elif int(choice) == 3:
                print("메인메뉴로 돌아갑니다.")
                break


# 예매 취소 기능
def print_cancel_reservation_menu(user_id):
    reservation_list = data.get_reservation_list()
    ticket_list = data.get_ticket_list()
    movie_list = data.get_movie_list()
    theater_list = data.get_theater_list()
    seat_list = data.get_seat_list()
    schedule_list = data.get_schedule_list()

    reservation_table = get_user_reservation_table(user_id, reservation_list, ticket_list, movie_list, theater_list,
                                                   seat_list, schedule_list)

    # 예매내역 출력
    print_reservation_table(reservation_table)

    # 예매 취소를 위한 예매 아이디 추출
    reservation_id_list = []
    reservation_id_list = [reservation[0] for reservation in reservation_table]

    while True:
        print("예매취소할 예매아이디를 입력해주세요")
        choice = input("예매아이디 입력: ")

        if not validate_cancel_syntax(choice):  # 문법 규칙 위배
            print("올바른 예매아이디를 입력해 주시기 바랍니다.")
        elif not validate_cancel_semantics(choice, reservation_id_list):  # 의미 규칙 위배 (없는 아이디)
            print("예매한 올바른 예매아이디를 입력해주시기 바랍니다.")
        else:
            break

    cancel_reservation(user_id,choice, ticket_list)
    print("영화 예매취소가 완료되었습니다. 메인메뉴로 돌아갑니다.")


##### 여기서부턴 짜잘이 함수들 #####


### print_check_reservation_menu 짜잘이 함수들 ###

def get_user_reservation_table(user_id, reservation_list, ticket_list, movie_list, theater_list, seat_list,
                               schedule_list):
    # join의 경우 reserve.get_schedule_table() 참고
    sorted_ticket = []
    result = []
    # reservation_list에서 user_id에 해당하는 reservation id list 만들기
    reservation_id_list = get_reservation_id_list(reservation_list, user_id)
    # reservation id list의 reservation id 각각에 대한 ticket_list 가져오기(join)
    for id in reservation_id_list:
        sorted_ticket.extend(find_ticket(ticket_list, id))
    

        # ticket_list에서 movie, theater, seat, schedule 정보 구해오기(join)
    for ticket in sorted_ticket:
        schedule = find_schedule(schedule_list, ticket[3])
        movie = find_movie(movie_list, schedule[2])
        theater = find_theater(theater_list, schedule[1])
        seat = find_seat(seat_list, ticket[2])
        start_time = schedule[4]
        end_time = get_endtime(movie, start_time)
        # 인원수 찾기 위함
        reserve_num = find_reserve_num(reservation_list, ticket[1])
        result.append(
            [ticket[1], movie[1], schedule[3], start_time, end_time, theater[0], reserve_num, seat[2], ticket[3]])

    # 정보 모두 종합해서 2차원 배열로 리턴
    return result


def get_reservation_id_list(reservation_list, id):
    reservation_id = []
    for reservation in reservation_list:
        if reservation[1] == id and reservation[3] == 'X':
            reservation_id.append(reservation[0])
    return reservation_id


def find_ticket(ticket_list, id):
    result_ticket = []
    for ticket in ticket_list:
        if ticket[1] == id:
            result_ticket.append(ticket)
            break
    return result_ticket


def find_schedule(schedule_list, id):
    for schedule in schedule_list:
        if schedule[0] == id:
            return schedule
    return None


def find_movie(movie_list, id):
    for movie in movie_list:
        if movie[0] == id:
            return movie
    return None


def get_endtime(movie, start_time):
    (id, title, running_time) = movie

    run_h = int(running_time) // 60
    run_m = int(running_time) % 60

    start_h = start_time.split(':')[0]
    start_m = start_time.split(':')[1]
    start_h = int(start_h)
    start_m = int(start_m)

    end_m = (start_m + run_m) % 60
    end_h = (start_h + run_h + (start_m + run_m) // 60) // 24

    # 다음날로 넘어가는 건?

    return str(end_h) + ":" + str(end_m)


def find_theater(theater_list, id):
    for theater in theater_list:
        if theater[0] == id:
            return theater
    return None


def find_seat(seat_list, id):
    for seat in seat_list:
        if seat[0] == id:
            return seat
    return None


def find_reserve_num(reservation_list, id):
    for reservation in reservation_list:
        if reservation[0] == id:
            return reservation[2]
    return None


def print_reservation_table(table):
    # 예매내역
    # 예매아이디  영화제목   날짜/상영시간     상영관  예약인원수 시작좌석 시간표아이디
    #    1       파묘   04.04/08-10      1관     2       A3      1

    print("예매내역")
    print("예매아이디\t영화제목\t날짜/상영시간\t\t상영관\t예약인원수\t시작좌석\t시간표아이디")
    for (id, movie_title, date, start_time, end_time, theater_name, reserve_number, start_seat, schedule_id) in table:
        print(
            str(id) + "\t\t" + movie_title + "\t\t" + date + "/" + start_time + "-" + end_time + "\t" + theater_name + "관" + "\t" + reserve_number + "\t\t" + start_seat + "\t\t" + schedule_id)


### print_cancel_reservation_menu 짜잘이 함수들 ###

def validate_cancel_syntax(choice):
    # 문법 규칙 검증
    if len(choice) < 1 or not choice.isdigit():
        return False
    return True


def validate_cancel_semantics(choice, reservation_id_list):
    # 의미 규칙 검증
    for id in reservation_id_list:
        if choice == id:
            return True
    return False


def validate_main_syntax(choice):
    # 문법 규칙 검증
    if not choice.isdigit():
        return False
    if (int(choice) < 1 or int(choice) > 5) or len(choice) != 1:
        return False
    return True


def validate_choice_syntax(choice):
    # 문법 규칙 검증
    if not choice.isdigit():
        return False
    if (int(choice) < 1 or int(choice) > 3) or len(choice) != 1:
        return False
    return True


def cancel_reservation(user_id,choosed_reservation_id, ticket_list):
    reservation_list = data.get_reservation_list()  # 기존 예약 리스트 읽어옴

    for reservation in reservation_list:
        if reservation[0] == choosed_reservation_id:  # 해당 reservation 찾음
            reservation[3] = 'O'  # 예약 취소 여부를 '0'으로 변경
            break

    # 수정된 내용을 파일에 기록
    with open("data/" + "reservation.txt", 'w', encoding='utf-8') as f:
        for reservation in reservation_list:
            f.write(f"{reservation[0]}/{reservation[1]}/{reservation[2]}/{reservation[3]}/{reservation[4]}\n")

    # 해당 reservation에 해당하는 ticket을 ticket_list에서 찾아 ticket에서 삭제
    modified_ticket_list = []
    for ticket in ticket_list:
        if ticket[1] != choosed_reservation_id:
            modified_ticket_list.append(ticket)
    coupon.change_coupon_available(user_id)
    # 수정된 내용을 파일에 기록
    with open("data/" + "ticket.txt", 'w', encoding='utf-8') as f:
        for ticket in modified_ticket_list:
            f.write(f"{ticket[0]}/{ticket[1]}/{ticket[2]}/{ticket[3]}/{ticket[4]}\n")

    return True


# 영화 예매 변경 함수
def print_change_reservation_menu(user_id) :

    # 예매내역 출력을 위한 데이터 불러오기
    reservation_list = data.get_reservation_list()
    ticket_list = data.get_ticket_list()
    movie_list = data.get_movie_list()
    theater_list = data.get_theater_list()
    seat_list = data.get_seat_list()
    schedule_list = data.get_schedule_list()
    reservation_table = get_user_reservation_table(user_id, reservation_list, ticket_list, movie_list, theater_list,
                                                   seat_list, schedule_list)

    # 예매내역 출력
    print_reservation_table(reservation_table)

    # 예매 변경을 위한 예매 아이디 추출
    reservation_id_list = [reservation[0] for reservation in reservation_table]

    choice = ""
    while True:
        print("예매변경할 예매아이디를 입력해주세요")
        choice = input("예매아이디 입력: ")

        if not validate_cancel_syntax(choice):  # 문법 규칙 위배
            print("올바른 예매아이디를 입력해 주시기 바랍니다.")
        elif not validate_cancel_semantics(choice, reservation_id_list):  # 의미 규칙 위배 (없는 아이디)
            print("예매한 올바른 예매아이디를 입력해주시기 바랍니다.")
        else:
            break

    before_cost = 0 # 변경 전 총 가격
    coupon_price = 0 # 취소하는 예매의 쿠폰 가격

    # (추가)예매 번호로 티켓에서 예매한 영화의 좌석을 가져오는 코드 : 현재 코드는 임시 : 추가 함수로 대체

    target_ticket_list = []
    for ticket in ticket_list:
        if ticket[1] == choice:
            target_ticket_list.append(ticket)
            before_cost = before_cost + int(ticket[4])

    for reservation in reservation_list:
        if reservation[0] == choice:  # 해당 reservation 찾음
            coupon_price = int(reservation[4])
            break

    schedule_id = target_ticket_list[0][3]

    # 결제 부분 추가 후 예매한 가격을 가져오는 코드
    # TODO: 인자에 예약아이디 추가해야 함
    cancel_reservation(choice, choice, ticket_list)  # 변경을 위한 예매 취소 
    reserve.reserve_change(user_id, schedule_id, before_cost, coupon_price) # 취소 후 좌석을 기준으로 예매 변경하기
