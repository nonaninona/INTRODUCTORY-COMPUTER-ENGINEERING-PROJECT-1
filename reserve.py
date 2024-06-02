import data
import sys
import moviesystem


# 예매 기능
def reserve(user_id, date_time):
    # 상영 스케쥴 출력
    schedule_list = data.get_schedule_list()
    schedule_list = sort_schedule(schedule_list, date_time)
    [movie_list, theater_list, seat_list, ticket_list, reservation_list] = get_lists()

    table = get_schedule_table(schedule_list, movie_list, theater_list, seat_list, ticket_list, reservation_list)
    print_schedule_list(table)

    # 예매할 영화 번호 입력
    while True:
        print("예매할 시간표 아이디를 입력해주세요")
        choice = input("시간표아이디 입력 : ")
        if validate_input(choice):
            if is_id_exist(table, choice):  # 가능한 시간표 아이디 범위 내이면
                if if_seat_full(table, choice):  # 여석이 모자르면(매진이면)
                    print("여석이 없습니다")
                else:  # 정상 입력 + 여석 존재면
                    break
                # 좌석 출력
            else:  # 그 밖의 범위이면
                print("영화가 존재하지 않습니다")
        else:  # 문법적으로 올바르지 않을 때
            print("시간표아이디는 숫자로 이루어진 길이가 1 이상인 문자열입니다.")

    schedule = get_schedule(choice, schedule_list)
    tickets = get_tickets(schedule, seat_list, ticket_list)
    seats = get_ticket_reservation_map(tickets, reservation_list)
    print_seats(seats)

    while True:
        print("예약인원수를 입력해주세요")
        choice = input("예약인원수 입력: ")
        if validate_seat_choice(choice):  # 문법이 맞은 경우
            if check_maximum_inline(choice, seats):
                break
            else:  # 예약인원수를 만족하는 연속으로 배치된 좌석이 부족
                print("예약인원수를 만족하는 연속으로 배치된 좌석이 부족합니다.")
        else:
            print("예약인원수는 1~5 사이 숫자로 이루어진 길이가 1인 문자열입니다.")

    people = choice

    while True:
        print("예매할 좌석번호를 입력해주세요")
        print("(좌석번호를 기준으로 오른쪽 방향으로 예약인원수 만큼 예매를 진행합니다.)")
        choice = input("좌석번호 입력: ")
        if validate_seat_number(choice):  # 문법이 맞은 경우
            if check_seat_available(choice, seats, people):  # 오른쪽으로 예약인원수만큼 부족하거나 이미 예약된 좌석인 경우
                break
            else:
                print("예약이 불가능한 좌석입니다.")
        else:  # 문법 규칙에 부합하지 않는 경우
            print("올바른 좌석번호를 입력해 주시기 바랍니다.")

    reservation_id = make_reservation(reservation_list, user_id, people)
    add_ticket_reservation(ticket_list, seat_list, schedule, reservation_id, choice, people)
    print("예매가 완료되었습니다")


### reserve 짜잘이 함수들 ###

def sort_schedule(schedule_list, date_time):
    schedule_list = sorted(schedule_list, key=lambda x: x[3] + x[4])
    idx = -1
    length = len(schedule_list)
    date = date_time.split(' ')[0]
    time = date_time.split(' ')[1]

    for i in range(length):
        date1 = schedule_list[i][3]
        time1 = schedule_list[i][4]
        if date + time < date1 + time1:
            idx = i
            break

    if idx == -1:
        return []
    else:
        schedule_list = schedule_list[idx:length]
        schedule_list = sorted(schedule_list, key=lambda x: x[0])
        return schedule_list


# 테이블 긁어오기
def get_lists():
    movie_list = data.get_movie_list()
    theater_list = data.get_theater_list()
    seat_list = data.get_seat_list()
    ticket_list = data.get_ticket_list()
    reservation_list = data.get_reservation_list()

    return [movie_list, theater_list, seat_list, ticket_list, reservation_list]


# 스케쥴 테이블 구성(join 연산)
def get_schedule_table(schedule_list, movie_list, theater_list, seat_list, ticket_list, reservation_list):
    table = []
    for i in range(len(schedule_list)):
        (id, theater_id, movie_id, date, time) = schedule_list[i]
        movie = find_movie(movie_list, movie_id)
        movie_title = movie[1]
        # theater_name = find_theater(theater_list, theater_id)
        max = get_maximum(theater_id, seat_list)
        cur = get_current(id, ticket_list, reservation_list)
        start_time = time
        end_time = get_endtime(movie, start_time)
        table.append([id, movie_title, date, start_time, end_time, cur, max, theater_id])

    return table


def find_movie(movie_list, id):
    for movie in movie_list:
        if movie[0] == id:
            return movie
    return None


def find_theater(theater_list, id):
    for theater in theater_list:
        if theater == id:
            return theater
    return None


# 해당하는 스케쥴의 최대 정원 구하기
# 해당하는 스케쥴의 상영관의 seat 수
def get_maximum(theater_id, seat_list):
    count = 0
    for seat in seat_list:
        if seat[1] == theater_id:
            count = count + 1
    if count == 1:
        return 25
    return count


# 해당하는 스케쥴의 에약된 seat의 수
# 해당하는 스케쥴의 티켓
def get_current(schedule_id, ticket_list, reservation_list):
    cur_tickets = []
    for ticket in ticket_list:
        if ticket[3] == schedule_id:
            cur_tickets.append(ticket)

    count = 0
    for reservation in reservation_list:
        if reservation[3] == True:
            continue
        for ticket in cur_tickets:
            if ticket[1] == reservation[0]:
                count = count + 1

    return count


# 종료 시간 얻기
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


# 스케쥴 표 출력
def print_schedule_list(table):
    print("영화목록")
    print("시간표아이디\t영화제목\t\t날짜/상영시간\t\t예약인원/최대예약인원\t상영관")
    for (id, movie_title, date, start_time, end_time, cur, max, theater_name) in table:
        date = date[4:6] + "." + date[6:8]
        print(str(id).strip() + "\t\t" + "{0:<10}".format(movie_title.strip()) + "\t\t" + date + " / " + start_time.strip() + " - " + end_time.strip() + "\t" + str(
            cur).strip() + " / " + str(max).strip() + "명\t\t" + theater_name.strip() + "관")
    # 영화목록
    # 시간표아이디 영화제목  날짜/상영시간     예약인원/최대예약인원   상영관
    #     1      파묘   04.04/08-10        25 / 25명       1관


def validate_input(choice):
    # 문법적 형식 검증
    if len(choice) < 1 or not choice.isdigit():
        # print("validate_date_syntax error")
        return False
    return True


def is_id_exist(table, id):
    for schedule in table:
        if schedule[0] == id:
            return True
    return False


def if_seat_full(table, id):
    for schedule in table:
        if schedule[0] == id:
            if int(schedule[5]) >= int(schedule[6]):
                return True
    return False


def get_schedule(schedule_id, schedule_list):
    for schedule in schedule_list:
        if schedule[0] == schedule_id:
            return schedule


# 해당 스케쥴의 좌석 목록과 좌석 예약 상태 불러오기
def get_tickets(schedule, seat_list, ticket_list):
    (id, theater_id, movie_id, date, time) = schedule

    tickets = []
    for ticket in ticket_list:
        temp = str(ticket[3].strip())
        if temp == str(id):
            tickets.append(ticket)

    tickets = sort_tickets(tickets, seat_list)
    return tickets


def sort_tickets(tickets, seat_list):
    map = []
    for ticket in tickets:
        for seat in seat_list:
            if ticket[2] == seat[0]:
                temp = ticket + [seat[2]]
                map.append(temp)
    sorted_map = sorted(map, key=lambda x: x[4])
    ret = []
    for t in sorted_map:
        ret.append(t)

    return ret


def get_ticket_reservation_map(tickets, reservation_list):
    ret = []
    for i in range(25):
        ret.append('O')

    for ticket in tickets:
        (id, reservation_id, seat_id, schedule_id, seat) = ticket
        row = seat[0]
        row = (ord(row) - ord('A')) * 5
        column = int(seat[1])
        idx = row + column

        for reservation in reservation_list:
            if ticket[1] == reservation[0]:
                if reservation[3] == 'X':
                    ret[idx] = 'X'

    return ret


def print_seats(seats):
    alphabet = ['A', 'B', 'C', 'D', 'E']

    print("좌석 입력")
    print("  | 0 1 2 3 4")
    print("  -----------")

    j = 0
    str = ""
    for i in range(len(seats)):
        if i % 5 == 0:
            str = ""
            str = str + alphabet[j] + " |"
            j = j + 1
        str = str + " " + seats[i]
        if i % 5 == 4:
            if i == 24:
                str = str + "\t\t※(X : 예매불가능 / O 예매가능)"
            str = str + "\n"
            print(str)
    # 좌석 입력
    # 좌석 출력
    #   | 0 1 2 3 4
    #   -----------
    # A | X O X O X
    # B | X O X O X 


def validate_seat_choice(choice):
    if not choice.isdigit():
        return False
    if (int(choice) < 1 or int(choice) > 5) or len(choice) != 1:
        return False
    return True


def check_maximum_inline(choice, seats):
    max = 0
    cur = 0
    local_max = 0
    for i in range(len(seats)):
        if seats[i] == 'O':
            cur = cur + 1
        else:
            if local_max < cur:
                local_max = cur
            cur = 0

        if i % 5 == 4:
            if local_max < cur:
                local_max = cur
            cur = 0

            if max < local_max:
                max = local_max
            local_max = 0

    return int(choice) <= max


def validate_seat_number(choice):
    row = choice[0]
    column = choice[1]

    if not ('A' <= row and row <= 'E'):
        return False
    if not column.isdigit() or int(column) < 0 or 4 < int(column):
        return False
    return True


def check_seat_available(choice, seats, people):
    row = choice[0]
    row = (ord(row) - ord('A')) * 5
    column = int(choice[1])
    people = int(people)
    if 4 - column + 1 < people:
        return False

    for i in range(people):
        idx = row + column + i
        if seats[idx] == 'X':
            return False

    return True


def make_reservation(reservation_list, user_id, people):
    # reservation 추가
    if reservation_list == []:
        reservation_id = 1
    else:
        max = 0
        for reservation in reservation_list:
            (id, reserver_id, people, is_canceled) = reservation
            if max < int(id):
                max = int(id)
        reservation_id = max + 1

    data.add_reservation(str(reservation_id), str(user_id), str(people), 'X')

    return reservation_id


def add_ticket_reservation(ticket_list, seat_list, schedule, reservation_id, choice, people):
    # 좌석 번호 목록
    row = choice[0]
    column = int(choice[1])

    choices = []
    for i in range(int(people)):
        choices.append(row + str(column))
        column = column + 1

    # 좌석 번호에 해당하는 seat들의 id 목록
    (schedule_id, theater_id, movie_id, date, time) = schedule

    seat_ids = []
    for seat in seat_list:
        (id, t_id, label) = seat
        id = id.strip()
        t_id = t_id.strip()
        label = str(label).strip()

        if (label in choices) and (str(theater_id) == str(t_id)):
            seat_ids.append(id)


    # 시작 아이디 얻어오기
    if ticket_list == []:
        ticket_id = 1
    else:
        max = 0
        for ticket in ticket_list:
            (id, r_id, seat_id, s_id) = ticket
            if max < int(id):
                max = int(id)
        ticket_id = max + 1



    # ticket 생성
    for seat_id in seat_ids:
        data.add_ticket(str(ticket_id), str(reservation_id), str(seat_id), str(schedule_id))
        ticket_id = ticket_id + 1

def reserve_change(user_id, choosed_reservation_id, schedule_id, before_cost, coupon_price):

    # (추가)상영 스케쥴 출력
    schedule_list = data.get_schedule_list()
    # schedule_list = sort_schedule(schedule_list, date_time)
    [movie_list, theater_list, seat_list, ticket_list, reservation_list] = get_lists()

    table = get_schedule_table(schedule_list, movie_list, theater_list, seat_list, ticket_list, reservation_list)

    schedule = get_schedule(schedule_id, schedule_list)
    tickets = get_tickets(schedule, seat_list, ticket_list)
    seats = get_ticket_reservation_map(tickets, reservation_list)
    ###

    # 좌석을 가져온 후 좌석 출력 코드
    print_seats(seats)

    # 예약 인원 입력 부분
    while True:
        print("예약인원수를 입력해주세요")
        choice = input("예약인원수 입력: ")
        if validate_seat_choice(choice):  # 문법이 맞은 경우
            if check_maximum_inline(choice, seats):
                break
            else:  # 예약인원수를 만족하는 연속으로 배치된 좌석이 부족
                print("예약인원수를 만족하는 연속으로 배치된 좌석이 부족합니다.")
        else:
            print("예약인원수는 1~5 사이 숫자로 이루어진 길이가 1인 문자열입니다.")

    people = choice # 예약 인원
    after_cost = 0

    # 좌석 번호 선택 부분
    while True:
        print("예매할 좌석번호를 입력해주세요")
        print("(좌석번호를 기준으로 오른쪽 방향으로 예약인원수 만큼 예매를 진행합니다.)")
        choice = input("좌석번호 입력: ")
        if validate_seat_number(choice):  # 문법이 맞은 경우
            if check_seat_available(choice, seats, people):  # 오른쪽으로 예약인원수만큼 부족하거나 이미 예약된 좌석인 경우
                break
            else:
                print("예약이 불가능한 좌석입니다.")
        else:  # 문법 규칙에 부합하지 않는 경우
            print("올바른 좌석번호를 입력해 주시기 바랍니다.")


    # 결제 부분 : 매개변수 before_cost와 비교하여 결제가격을 계산
    after_cost = people * 10000
    cost_diff = after_cost - (before_cost - coupon_price)

    # 계산한 결제 가격으로 재결재 : 같거나 낮을 시 결제 skip
    check_resume()

    # 결제 후 예약하기 부분
    reservation_id = make_reservation(reservation_list, user_id, people)
    add_ticket_reservation(ticket_list, seat_list, schedule, reservation_id, choice, people)
    print("예매가 완료되었습니다")

def check_resume(before_cost, after_cost, coupon_price, cost_diff):
    if cost_diff > 0:
        # 추가 결제
        while True:
            print_additional_charge_menu(before_cost, after_cost, coupon_price, cost_diff)
            choice = input("입력 : ")
            if validate_change_choice(choice):
                break
            else:
                print("1~2 사이 숫자 내에서 입력해주세요.")

        if int(choice) == 1:
            print("예매 변경 및 추가 결제가 완료되었습니다.")
        elif int(choice) == 2:
            print("좌석 선택 프롬프트로 돌아갑니다.")

    elif cost_diff < 0:
        # 환불
        while True:
            print_refund_menu(before_cost, after_cost, coupon_price, cost_diff)
            choice = input("입력 : ")
            if validate_change_choice(choice):
                break
            else:
                print("1~2 사이 숫자 내에서 입력해주세요.")

        if int(choice) == 1:
            print("예매 변경 및 환불이 완료되었습니다.")
        elif int(choice) == 2:
            print("좌석 선택 프롬프트로 돌아갑니다.")

    else:
        # 변동 없음
        while True:
            print_keep_menu()
            choice = input("입력 : ")
            if validate_change_choice(choice):
                break
            else:
                print("1~2 사이 숫자 내에서 입력해주세요.")
        
        if int(choice) == 1:
            print("예매 변경이 완료되었습니다.")
        elif int(choice) == 2:
            print("좌석 선택 프롬프트로 돌아갑니다.")

def validate_change_choice(choice):
    # 문법적 형식 검증
    if len(choice) != 1 or not choice.isdigit():
        # print("validate_date_syntax error")
        return False
    if int(choice) < 1 or int(choice) > 2:
        return False
    return True

def print_additional_charge_menu(before_cost, after_cost, coupon_price, cost_diff):
    print("변경한 좌석에 대한 결제를 진행합니다.")
    print("**예매 변경**")
    print("------------")
    print("기존 결제 금액 : ", before_cost, "원")
    print("변경된 결제 금액 : ", after_cost, "원")
    if coupon_price > 0:
        print("적용 쿠폰 목록 : ", coupon_price, "원 할인 쿠폰")
    print("")
    print("추가 결제 금액 : ", cost_diff, "원")
    print("※ (예매 변경을 원하면 '1', 이전 단계로 돌아가려면 '2'을 입력해주세요.)")
    print("1. 예매 변경하기")
    print("2. 돌아가기")

def print_refund_menu(before_cost, after_cost, coupon_price, cost_diff):
    print("변경한 좌석에 대한 환불을 진행합니다.")
    print("**예매 변경**")
    print("------------")
    print("기존 결제 금액 : ", before_cost, "원")
    print("변경된 결제 금액 : ", after_cost, "원")
    if coupon_price > 0:
        print("적용 쿠폰 목록 : ", coupon_price, "원 할인 쿠폰")
    print("")
    print("환불 금액 : ", -1 * cost_diff, "원")
    print("※ (예매 변경을 원하면 '1', 이전 단계로 돌아가려면 '2'을 입력해주세요.)")
    print("1. 예매 변경하기")
    print("2. 돌아가기")

def print_keep_menu():
    print("금액이 변경되지 않았습니다. 예매 변경을 완료하시겠습니까?")
    print("※ (예매 변경을 원하면 '1', 이전 단계로 돌아가려면 '2'을 입력해주세요.)")
    print("1. 예매 변경하기")
    print("2. 돌아가기")