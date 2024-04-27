import sys

theater_list = []  # 상영관 정보
theater_dict = {}  # 상영관 행렬 정보


def write_theater():
    with open("data/" + "theater.txt", "w", encoding="utf-8") as file:
        for item in theater_list:
            file.write(str(item) + "/" + str(item) + "\n")


# 예매아이디
seat_id = 0


# 상영관 업데이트 함수
def update_seat(theater_id, new_rows, new_cols):
    global seat_id
    updated = False
    temp_lines = []  # 수정된 내용을 임시로 저장할 리스트
    last_seat_id = 0  # 파일에서 찾은 마지막 seat_id 값을 저장

    # 파일을 읽어서 기존 내용을 temp_lines에 저장하고, 수정할 상영관 ID를 찾아 해당 내용만 업데이트
    try:
        with open("data/" + "seat.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split('/')
                # seat_id 갱신
                current_seat_id = int(parts[0])
                if current_seat_id > last_seat_id:
                    last_seat_id = current_seat_id

                if int(parts[1]) == theater_id:
                    row_alpha = chr(new_rows + 64)  # 새로운 행 정보를 영어 알파벳으로 변환
                    temp_lines.append(f"{current_seat_id}/{theater_id}/{row_alpha}{new_cols}\n")  # 업데이트된 내용
                    updated = True
                else:
                    temp_lines.append(line)
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

    # 새로운 seat_id 할당을 위해 last_seat_id에 1을 더함
    seat_id = last_seat_id + 1

    # 상영관 ID에 해당하는 정보를 찾지 못했다면, 새로운 정보를 추가
    if not updated:
        row_alpha = chr(new_rows + 64)
        temp_lines.append(f"{seat_id}/{theater_id}/{row_alpha}{new_cols}\n")
        seat_id += 1  # 다음 seat_id 준비

    # 수정된 내용을 파일에 다시 쓰기
    try:
        with open("data/" + "seat.txt", "w", encoding="utf-8") as file:
            file.writelines(temp_lines)
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


# 상영관 삭제함수
def delete_theater(theater_id):
    # seat.txt에서 해당 theater_id 줄 삭제
    try:
        with open("data/" + "seat.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        with open("data/" + "seat.txt", "w", encoding="utf-8") as file:
            for line in lines:
                if int(line.split('/')[1]) != theater_id:
                    file.write(line)
    except FileNotFoundError:
        print("seat.txt 파일을 찾을 수 없습니다.")

    # theater.txt에서 해당 theater_id 줄 삭제
    try:
        with open("data/" + "theater.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        with open("data/" + "theater.txt", "w", encoding="utf-8") as file:
            for line in lines:
                if int(line.split('/')[0]) != theater_id:
                    file.write(line)
    except FileNotFoundError:
        print("theater.txt 파일을 찾을 수 없습니다.")


# theater.txt 파일 읽어오기
def read_theater():
    TheaterTable = []
    with open("data/" + "theater.txt", "r", encoding="utf-8") as f:
        for line in f:
            id_str, movie = line.strip().split("/")
            id = int(id_str)  # 첫 번째 요소를 정수형으로 변환
            TheaterTable.append(id)  # 변환된 정수형 id를 리스트에 추가
    return TheaterTable


# schedule.txt 파일 읽어오기
def read_theater_ids_from_schedule():
    theater_ids = set()  # 중복을 제거하기 위해 set 사용
    with open("data/" + "schedule.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("/")

            theater_id = parts[2]
            #theater_ids.add(int(theater_id))
    return list(theater_ids)


# 상영중인 아이디 불러와서 저장
scheduled_cinemas = read_theater_ids_from_schedule()


# 좌석정보 읽어오는 함수
def read_seat():
    theater_dict = {}
    with open("data/" + "seat.txt", "r", encoding="utf-8") as f:
        for line in f:
            id_str, theater, theater_seat = line.strip().split("/")
            theater_id = int(theater)  # 문자열을 정수형으로 변환
            rows, cols = parse_coordinates(theater_seat)
            theater_dict[theater_id] = {'rows': rows, 'cols': cols}  # 변환된 정수형 id를 사용
    return theater_dict


# 좌석번호 변환함수(4 4 -> D4)
def parse_coordinates(coord):
    column = coord[0].lower()  # Ensure the column letter is lowercase
    row = int(coord[1:])
    return row, ord(column) - ord('a') + 1


theater_list = read_theater()
theater_dict = read_seat()


def add_cinema():
    while True:
        print("[상영관 추가] 추가할 상영관아이디와 좌석수(행,열)를 입력해주세요.")
        user_input = input("입력 : ")

        # theater_list = get_Theater_list()

        try:
            cinema_id, rows, cols = map(int, user_input.split())

            if cinema_id < 0:
                print("상영관아이디는 0 이상인 정수입니다.")
                continue

            # 좌석수 검증
            if not (1 <= rows <= 5) or not (1 <= cols <= 5):
                print("좌석 행과 열의 개수는 1~5 중 하나입니다.")
                continue

            # 이미 등록된 상영관 ID 검증
            if cinema_id in theater_list:
                print("이미 등록되어 있는 상영관아이디입니다.")
                continue

            # 상영관 등록
            theater_dict[cinema_id] = {'rows': rows, 'cols': cols}
            theater_list.append(cinema_id)
            update_seat(cinema_id, rows, cols)
            print("정상적으로 추가되었습니다.")
            break

        except ValueError:
            print("[오류] 올바른 형식으로 입력해주세요.")
            continue


def update_cinema():
    while True:
        print("[상영관 수정] 수정할 상영관아이디와 좌석수(행,열)를 입력해주세요.")

        user_input = input("입력 : ")

        try:
            cinema_id, rows, cols = map(int, user_input.split())

            # 좌석수 검증
            if not (1 <= rows <= 5) or not (1 <= cols <= 5):
                print("좌석 행과 열의 개수는 1~5 중 하나입니다.")
                continue

            # 상영 스케줄이 잡힌 상영관 검증
            if cinema_id in scheduled_cinemas:
                print("상영스케줄이 잡힌 영화가 있어 수정이 불가능합니다.")
                continue

            # 존재하지 않는 상영관 검증
            if cinema_id not in theater_list:
                print("해당하는 상영관이 없습니다.")
                continue

            # 상영관 수정
            theater_dict[cinema_id]['rows'] = rows
            theater_dict[cinema_id]['cols'] = cols
            update_seat(cinema_id, rows, cols)
            print("정상적으로 수정되었습니다.")
            break

        except ValueError:
            print("[오류] 올바른 형식으로 입력해주세요.")
            continue


def delete_cinema():
    while True:
        print("[상영관 삭제] 삭제할 상영관아이디를 입력해주세요.")
        print("현재 상영관 목록 :", ",".join(map(str, theater_dict.keys())))
        user_input = input("입력 : ")

        try:
            cinema_id = int(user_input)

            # 존재하지 않는 상영관 검증
            if cinema_id not in theater_list:
                print("해당 상영관이 존재하지 않습니다. 다시 입력해주세요.")
                continue

            # 상영 스케줄이 있는 상영관 검증
            if cinema_id in scheduled_cinemas:
                print("해당 상영관에 상영스케줄이 있습니다. 상영스케줄을 모두 제거 후 상영관을 삭제해주세요.")
                continue

            # 상영관 삭제
            theater_list.remove(cinema_id)
            del theater_dict[cinema_id]
            delete_theater(cinema_id)
            print("정상적으로 삭제가 완료되었습니다.")
            break

        except ValueError:
            print("올바른 상영관아이디를 입력해주세요.")
            continue


def manage_cinema():
    while True:
        print("[관리자 모드] 실행할 메뉴를 선택하세요.")
        print("1. 상영관 추가\n2. 상영관 수정\n3. 상영관 삭제\n4. 종료")
        choice = input("입력: ").strip()

        if choice == "1":
            add_cinema()  # 상영관 추가 함수
            write_theater()

            break
        elif choice == "2":
            update_cinema()  # 상영관 수정 함수

            break
        elif choice == "3":
            delete_cinema()  # 상영관 삭제 함수
            write_theater()

            break
        elif choice == "4":
            print("관리자 모드를 종료합니다.")
            break  # 루프 종료
        else:
            print("잘못된 입력입니다. 다시 입력해주세요.")


# manage_cinema()
