import data
import theater
import schedule


# schedule.txt 파일 읽어오기
def read_schedule():
    movie_ids = set()  # 중복을 제거하기 위해 set 사용
    with open("data/" + "schedule.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("/")

            theater_id = parts[2]
            movie_ids.add(theater_id)
    return list(movie_ids)

def manage_menu():
    while True:
        print("[관리자 모드] 실행할 메뉴를 선택하세요.")
        # menu = input("1. 영화 관리\n2. 상영관 관리\n3. 상영스케줄 관리\n4. 종료\n입력 : ")
        menu = "2"
        if menu == "1":
            manage_movie()
        elif menu == "2":
            theater.manage_cinema()
        elif menu == "3":
            schedule.manage_schedule()
        elif menu == "4":
            print("관리자모드를 종료합니다.")
            break
        else:
            print("화면에 출력된 숫자 내에서 입력해주세요.")


def manage_movie():
    while True:
        print("[관리자 모드] 실행할 메뉴를 선택하세요.")
        menu = input("1. 영화 추가\n2. 영화 수정\n3. 영화 삭제\n4. 종료\n입력 : ")
        if menu == "1":
            movie_add_menu()
            break
        elif menu == "2":
            movie_change_menu()
            break
        elif menu == "3":
            movie_delete_menu()
            break
        elif menu == "4":
            print("관리자모드 메뉴로 돌아갑니다.")
            break
        else:
            print("1~4 사이 숫자 내에서 입력해주세요.")


def movie_add_menu():
    print("추가할 영화명, 러닝타임을 입력해주세요.\n형식: (<영화명><\"/\"><러닝타임>)")
    while True:
        menu = input("입력 : ")

        flag = True
        movieTable = read_movie()

        try:
            movie, time = menu.strip().split("/")
        except ValueError:
            print("잘못된 형식입니다. 영화명과 러닝타임을 '/'로 구분하여 입력해주세요.")
            continue

        for i, m, t in movieTable:
            if m == movie:
                print("이미 존재하는 영화입니다. 다시 입력해주세요.")
                flag = False
        if flag == True:
            if time.isdigit():
                time = int(time)
                if 50 <= time <= 240:
                    write_movie(len(movieTable), movie, time)
                    print("성공적으로 영화가 추가되었습니다.")
                    break
                else:
                    print("러닝타임은 50 이상 240 이하의 정수입니다. 다시 입력해주세요.")
            else:
                print("러닝타임은 50 이상 240 이하의 정수입니다. 다시 입력해주세요.")

def movie_change_menu():
    print("수정할 영화아이디를 입력해주세요.\n[등록된 영화 내역]\n영화명     러닝타임     영화아이디\n")
    movieTable = read_movie()
    movieIdTable = []
    for i, m, t in movieTable:
        movieIdTable.append(i)
        print(m, "     ", t, "     ", i)
    while True:
        id = input("입력 : ")
        # 입력 문법 검사
        if (len(id) == 3 and id[0].isdigit() and id[1].isdigit() and id[2].isdigit()):
            # 없는 영화아이디일 때
            f = True
            for m in movieIdTable:
                if m == id:
                    f = False
                    break
            if (f):
                print("해당하는 영화아이디가 없습니다. 다시 입력해주세요.")
            else:
                # 상영스케줄이 잡혀있을 때
                flag0 = False
                for i in read_schedule():
                    if id == i:
                        flag0 = True
                        break
                if (flag0):
                    print("해당 영화의 상영스케줄이 있습니다. 상영스케줄을 모두 제거 후 영화를 수정해주세요.")
                else:
                    print("※  (영화명 수정을 원할 시 ‘1’, 러닝타임 수정을 원할 시 ‘2’을 눌러주세요.)\n1. 영화명 수정하기\n2. 러닝타임 수정하기")
                    while True:
                        change = input("입력 : ")
                        if change == "1":
                            flag1 = True
                            print("변경하고 싶은 영화명을 입력해주세요.")
                            while True:
                                changeMovie = input("입력 : ")
                                if changeMovie == "":
                                    print("영화명을 입력해주세요.")
                                    continue
                                for _, m, _ in movieTable:
                                    if changeMovie == m:
                                        flag1 = False
                                        break
                                if flag1:
                                    edit_movie_title(id, changeMovie)
                                    print("영화명이 성공적으로 수정되었습니다.")
                                    # break
                                    return
                                else:
                                    print("이미 등록된 영화명입니다. 다시 입력해주세요.")
                                    flag1 = True
                        elif change == "2":
                            flag2 = True
                            while True:
                                print("변경하고 싶은 러닝타임을 입력해주세요. (최소 50 ~ 최대 240)")
                                changeTime = input("입력 : ")
                                for _, _, t in movieTable:
                                    if changeTime == t:
                                        flag2 = False
                                        break
                                if flag2:
                                    try:
                                        if (50 <= int(changeTime) and int(changeTime) <= 240 and changeTime.isdigit()):
                                            edit_movie_time(id, int(changeTime))
                                            print("러닝타임이 성공적으로 수정되었습니다.")
                                            # break
                                            return
                                        else:
                                            print("러닝타임은 최소 50 ~ 최대 240 사이 숫자입니다. 다시 입력해주세요.")
                                    except ValueError:
                                        print("러닝타임은 최소 50 ~ 최대 240 사이 숫자입니다. 다시 입력해주세요.")
                                        continue
                                else:
                                    print("해당 영화의 러닝타임과 일치합니다. 다시 입력해주세요.")
                                    flag2 = True
                        else:
                            print("1~2 사이 숫자 내에서 입력해주세요.")
        else:
            print("0과 정수로만 이루어진 길이가 3인 숫자입니다. 다시 입력해주세요.")

def movie_delete_menu():
    print("삭제할 영화아이디를 입력해주세요.\n[등록된 영화 내역]\n영화명     러닝타임     영화아이디\n")
    movieTable = read_movie()
    for i, m, t in movieTable:
        print(m, "     ", t, "     ", i)
    while True:
        id = input("입력 : ")
        if (len(id) == 3 and id[0].isdigit() and id[1].isdigit() and id[2].isdigit()):
            flag = False
            for i, _, _ in movieTable:
                if i == id:
                    flag = True
                    break
            # 상영스케줄이 잡혀있을 때
            flag0 = False
            for a in read_schedule():
                if a == i:
                    flag0 = True
                    break
            if (flag0):
                print("해당 영화의 상영스케줄이 있습니다. 상영스케줄을 모두 제거 후 영화를 수정해주세요.")
            else:
                if flag:
                    delete_movie(id)
                    print("영화가 삭제되었습니다.")
                    break
                else:
                    print("등록되어 있지 않은 영화아이디입니다. 다시 입력해주세요.")

        else:
            print("0과 정수로만 이루어진 길이가 3인 숫자입니다. 다시 입력해주세요.")


def read_movie():
    #print(data.get_movie_list())
    return data.get_movie_list()

     #movieTable = []
     #with open("data/" + "movie.txt", "r", encoding="utf-8") as f:
     #    for line in f:
     #        id, movie, time = line.strip().split("/")
     #        movieTable.append((id, movie, time))
     #return movieTable


def write_movie(id, movie, time):
    if (id < 10):
        newID = "0" + "0" + f"{id + 1}"
    elif (10 <= id < 100):
        newID = "0" + f"{id + 1}"
    elif (100 <= id):
        newID = f"{id + 1}"

    data.add_movie(newID, movie, time)
    #with open("data/" + "movie.txt", "a", encoding="utf-8") as f:
    #     f.write(f"{newID}/{movie}/{time}\n")

def edit_movie_title(id, movie):
    movieTable = read_movie()  # 기존 영화 목록을 읽어옴

    # 영화명을 수정할 대상의 인덱스를 찾음
    for a, (i, m, t) in enumerate(movieTable):
        if i == id:
            movieTable[a] = (i, movie, t)  # 새로운 영화명으로 수정

    # 수정된 내용을 파일에 기록
    with open("data/" + "movie.txt", 'w', encoding='utf-8') as f:
        for i, m, t in movieTable:
            f.write(f"{i}/{m}/{t}\n")

def edit_movie_time(id, time):
    movieTable = read_movie()  # 기존 영화 목록을 읽어옴

    # 러닝타임을 수정할 대상의 인덱스를 찾음
    for a, (i, m, t) in enumerate(movieTable):
        if i == id:
            movieTable[a] = (i, m, time)  # 새로운 러닝타임으로 수정

    # 수정된 내용을 파일에 기록
    with open("data/" + "movie.txt", 'w', encoding='utf-8') as f:
        for i, m, t in movieTable:
            f.write(f"{i}/{m}/{t}\n")


def delete_movie(id):
    movieTable = read_movie()  # 기존 영화 목록을 읽어옴
    newMovieTable = []

    # 삭제할 영화를 찾아서 제외함
    for a, (i, m, t) in enumerate(movieTable):
        if i != id:
            newMovieTable.append((i, m, t))

    # 수정된 내용을 파일에 기록
    with open("data/" + "movie.txt", 'w', encoding='utf-8') as f:
        for i, m, t in newMovieTable:
            f.write(f"{i}/{m}/{t}\n")