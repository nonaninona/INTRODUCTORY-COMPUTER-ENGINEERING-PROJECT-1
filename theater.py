import moviesystem
import data

theater_list = []  # 상영관 정보


# theater_dict = {}  # 상영관 행렬 정보


def write_theater():
    with open("data/" + "theater.txt", "w", encoding="utf-8") as file:
        for item in theater_list:
            file.write(str(item) + "\n")


# 예매아이디
seat_id = 0


# 상영관 좌석 추가 함수
def add_seat(theater_id):
    # seat id 얻어오기
    seat_list = data.get_seat_list()
    str_theater_id = str(theater_id)
    data.add_theater(str_theater_id,'SSSSSSSSSSSSSSSSSSSSSSSSS')
    seat_id = -1
    if seat_list == []:
        seat_id = 1
    else:
        max = 0
        for seat in seat_list:
            (s_id, t_id, label) = seat
            if max < int(s_id):
                max = int(s_id)
        seat_id = max + 1

    row = ['A', 'B', 'C', 'D', 'E']
    column = ['0', '1', '2', '3', '4']

    for r in row:
        for c in column:
            data.add_seat(str(seat_id), str(theater_id), r + c)
            seat_id = seat_id + 1

# 2차요구사항 자리 요청받아 그대로 좌석 수정
def update_seat_layout(theater_id, seat_layout):
    # 상영관의 기존 좌석을 삭제
    delete_seat(theater_id)
    
    seat_list = data.get_seat_list()
    seat_id = -1
    if seat_list == []:
        seat_id = 1
    else:
        max = 0
        for seat in seat_list:
            (s_id, t_id, label) = seat
            if max < int(s_id):
                max = int(s_id)
        seat_id = max + 1
    
    row = ['A', 'B', 'C', 'D', 'E']
    column = ['0', '1', '2', '3', '4']

    # seat_layout에서 사용할 인덱스 초기화
    layout_index = 0

    for r in row:
        for c in column:
            # seat_layout 문자열에서 상태를 확인하고 'S'인 경우에만 좌석 추가
            if layout_index < len(seat_layout) and seat_layout[layout_index] == 'S':
                data.add_seat(str(seat_id), str(theater_id), r + c)
                seat_id = seat_id + 1
            # 인덱스를 1 증가시켜 다음 좌석 상태를 확인
            layout_index += 1

            
            
def delete_seat(theater_id):
    seat_list = data.get_seat_list()

    # 삭제할 행 빼고 넣기
    new_lines = []
    for seat in seat_list:
        (s_id, t_id, label) = seat
        if not str(t_id) == str(theater_id):
            new_lines.append(str(s_id) + '/' + str(t_id) + '/' + str(label) + '\n')

    try:
        with open("data/" + "seat.txt", "w", encoding="utf-8") as file:
            file.writelines(new_lines)
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

# 상영관 좌석배치 수정 시 : theater.txt 파일 수정함수
def get_change_theater_structure(cinema_id, new_seat_layout):
    # 변경할 내용을 저장할 임시 리스트 생성
    updated_lines = []
    found = False
    
    try:
        # 파일을 읽고 각 줄을 확인
        with open("data/" +"theater.txt", "r", encoding="utf-8") as file:
            for line in file:
                id, layout = line.strip().split('/')
                # 해당 cinema_id를 찾으면 새로운 좌석 배치로 업데이트
                if int(id) == cinema_id:
                    updated_lines.append(f"{cinema_id}/{new_seat_layout}\n")
                    found = True
                else:
                    updated_lines.append(line)
        
        # 해당 cinema_id가 파일 내에 존재하면 파일을 업데이트
        if found:
            with open("data/" + "theater.txt", "w", encoding="utf-8") as file:
                file.writelines(updated_lines)
        else:
            print("해당하는 상영관이 없습니다.")
    
    except FileNotFoundError:
        print("theater.txt 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")


# 상영관 기본 내역 수정함수
def update_theater(theater_id, new_theater_id):
    temp_lines = []  # 수정된 내용을 임시로 저장할 리스트

    idx = theater_list.index(theater_id)
    theater_list[idx] = new_theater_id

    # 파일을 읽어서 기존 내용을 temp_lines에 저장하고, 수정할 상영관 ID를 찾아 해당 내용만 업데이트
    try:
        with open("data/theater.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if not line.strip():
                    continue
                new_line = line.strip()
                # 줄에서 '/' 앞의 숫자를 찾아서 비교
                parts = new_line.split('/')
                if len(parts) == 2:
                    t_id = int(parts[0])
                    if theater_id == t_id:
                        parts[0] = str(new_theater_id)
                        new_line = '/'.join(parts)
                new_line = new_line + '\n'
                temp_lines.append(new_line)

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

    # 수정된 내용을 파일에 다시 쓰기
    try:
        with open("data/theater.txt", "w", encoding="utf-8") as file:
            file.writelines(temp_lines)
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")





# 상영관 삭제함수
def delete_theater(theater_id):
    # # seat.txt에서 해당 theater_id 줄 삭제
    # try:
    #     with open("data/" + "seat.txt", "r", encoding="utf-8") as file:
    #         lines = file.readlines()
    #     with open("data/" + "seat.txt", "w", encoding="utf-8") as file:
    #         for line in lines:
    #             if int(line.split('/')[1]) != theater_id:
    #                 file.write(line)
    # except FileNotFoundError:
    #     print("seat.txt 파일을 찾을 수 없습니다.")

    # theater.txt에서 해당 theater_id 줄 삭제
    try:
        with open("data/" + "theater.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        with open("data/" + "theater.txt", "w", encoding="utf-8") as file:
            for line in lines:
                line = line.strip()
                if int(line) != theater_id:
                    file.write(line)
    except FileNotFoundError:
        print("theater.txt 파일을 찾을 수 없습니다.")


# theater.txt 파일 읽어오기
def read_theater():
    
    TheaterTable = []
    with open("data/theater.txt", "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            id_str, theater_seat = line.strip().split("/")
            id = int(id_str)
            TheaterTable.append(id)
    return TheaterTable


# schedule.txt 파일 읽어오기
def read_theater_ids_from_schedule():
    theater_ids = set()  # 중복을 제거하기 위해 set 사용
    with open("data/" + "schedule.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("/")

            theater_id = parts[1]
            theater_ids.add(int(theater_id))
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
# theater_dict = read_seat()


def add_cinema():
    while True:
        # print("[상영관 추가] 추가할 상영관아이디와 좌석수(행,열)를 입력해주세요.")
        print("[상영관 추가] 추가할 상영관아이디를 입력해주세요.")
        user_input = input("입력 : ")

        # theater_list = get_Theater_list()

        try:
            # cinema_id, rows, cols = map(int, user_input.split())
            cinema_id = int(user_input)

            if cinema_id < 0:
                print("상영관아이디는 0 이상인 정수입니다.")
                continue

            # # 좌석수 검증
            # if not (1 <= rows <= 5) or not (1 <= cols <= 5):
            #     print("좌석 행과 열의 개수는 1~5 중 하나입니다.")
            #     continue

            # 이미 등록된 상영관 ID 검증
            if cinema_id in theater_list:
                print("이미 등록되어 있는 상영관아이디입니다.")
                continue

            # 상영관 등록
            # theater_dict[cinema_id] = {'rows': rows, 'cols': cols}
            theater_list.append(cinema_id)
            add_seat(cinema_id)
            # update_seat(cinema_id, rows, cols)
            print("정상적으로 추가되었습니다.")
            break

        except ValueError:
            print("[오류] 올바른 형식으로 입력해주세요.")
            continue
        
# 데이터요소 여쭤보기
def get_theater_layout(cinema_id):
    try:
        with open("data/" + "theater.txt", "r", encoding="utf-8") as file:
            for line in file:
                # 줄을 '/'를 기준으로 분리하여 id와 좌석 구조를 분리합니다.
                id, layout = line.strip().split('/')
                # 주어진 cinema_id와 일치하는지 확인합니다.
                if id == str(cinema_id):
                    return layout
        # 파일 내에서 해당 cinema_id를 찾지 못한 경우
        print(f"{cinema_id}에 해당하는 좌석 구조를 찾을 수 없습니다.")
    except FileNotFoundError:
        print("theater.txt 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
    return None


def update_cinema():
    while True:
        print("[상영관 수정] 실행할 메뉴를 선택하세요.")
        print("1. 상영관 기본 내역 수정")
        print("2. 상영관 좌석배치 수정")
        user_choice = input("입력: ")

        if user_choice == '1':
            while True:
                print("[상영관 수정] 수정 대상이 될 상영관아이디와 수정 결과가 될 상영관아이디를 입력해주세요.")
                print("현재 상영관 목록 :", ",".join(map(str, theater_list)))
                user_input = input("입력 : ")
                user_input = ' '.join(user_input.strip().split())
                
                try:
                    cinema_id, new_cinema_id = map(int, user_input.split())
                    if cinema_id < 0 or new_cinema_id < 0:
                        print("상영관아이디는 0 이상인 정수입니다.")
                        continue

                    if cinema_id in scheduled_cinemas:
                        print("상영스케줄이 잡힌 영화가 있어 수정이 불가능합니다.")
                        continue

                    if cinema_id not in theater_list:
                        print("해당하는 상영관이 없습니다.")
                        continue

                    if new_cinema_id in theater_list:
                        print("이미 존재하는 상영관입니다.")
                        continue
                    
                    # 해당 번호 좌석 가져오기
                    layout = get_theater_layout(cinema_id)
                    
                    # 상영관 정보 수정(theater.txt)
                    update_theater(cinema_id, new_cinema_id)
                    
                    
                    delete_seat(cinema_id)
                    
                    # seat.txt 정보 업데이트
                    update_seat_layout(new_cinema_id, layout)
                    print("정상적으로 수정되었습니다.")
                    return

                except ValueError:
                    print("[오류] 올바른 형식으로 입력해주세요.")
                    continue

        elif user_choice == '2':
            while True:
                print("[상영관 수정] 수정할 상영관아이디와 좌석배치를 입력해주세요. (좌석배치는 S(좌석 존재), E(좌석 미존재)로 이루어진 25자리 문자입니다.)")
                print("현재 상영관 목록 :", ",".join(map(str, theater_list)))
                user_input = input("입력 : ")

                try:
                    inputs = user_input.split()
                    if len(inputs) != 2:
                        raise ValueError("[오류] 올바른 형식으로 입력해주세요")

                    cinema_id = int(inputs[0])
                    seat_layout = inputs[1]

                    if cinema_id < 0:
                        print("상영관아이디는 0 이상인 정수입니다.")
                        continue

                    if cinema_id in scheduled_cinemas:
                        print("상영스케줄이 잡힌 영화가 있어 수정이 불가능합니다.")
                        continue

                    if cinema_id not in theater_list:
                        print("해당하는 상영관이 없습니다.")
                        continue

                    if len(seat_layout) != 25 or not all(c in 'SE' for c in seat_layout):
                        print("[오류] 올바른 형식으로 입력해주세요")
                        continue
                    
                    # 좌석정보 가져오기
                    get_change_theater_structure(cinema_id, seat_layout)
                    
                    # seat.txt 정보 업데이트
                    update_seat_layout(cinema_id, seat_layout)
                    print("정상적으로 수정되었습니다.")
                    break

                except ValueError:
                    print("[오류] 올바른 형식으로 입력해주세요.")
                    continue

        else:
            print("[오류] 올바른 메뉴를 선택해주세요.")
            continue

def delete_cinema():
    while True:
        print("[상영관 삭제] 삭제할 상영관아이디를 입력해주세요.")
        print("현재 상영관 목록 :", ",".join(map(str, theater_list)))
        user_input = input("입력 : ")

        try:
            cinema_id = int(user_input)

            if cinema_id < 0:
                print("상영관아이디는 0 이상인 정수입니다.")
                continue

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
            # del theater_dict[cinema_id]
            delete_theater(cinema_id)
            delete_seat(cinema_id)
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
            # write_theater()

            break
        elif choice == "2":
            update_cinema()  # 상영관 수정 함수

            break
        elif choice == "3":
            delete_cinema()  # 상영관 삭제 함수
            # write_theater()

            break
        elif choice == "4":
            print("관리자모드 메뉴로 돌아갑니다.")
            break  # 루프 종료
        else:
            print("1~4 사이 숫자 내에서 입력해주세요.")

#manage_cinema()
