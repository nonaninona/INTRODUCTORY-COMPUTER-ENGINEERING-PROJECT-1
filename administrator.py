import data
import theater


def manage_menu():
    while True:
        print("[관리자 모드] 실행할 메뉴를 선택하세요.")
        menu = input("1. 영화 관리\n2. 상영관 관리\n3. 상영스케줄 관리\n4. 종료\n입력 : ")
        if menu == "1":
            manage_menu()
        elif menu == "2":
            theater.manage_cinema()
        elif menu == "3":
            print("")
            # scheduleManageMenu()
        elif menu == "4":
            print("관리자모드를 종료합니다.")
            break
        else:
            print("화면에 출력된 숫자 내에서 입력해주세요.")


def manage_menu():
    while True:
        print("[관리자 모드] 실행할 메뉴를 선택하세요.")
        menu = input("1. 영화 추가\n2. 영화 수정\n3. 영화 삭제\n4. 종료\n입력 : ")
        if menu == "1":
            movie_add_menu()
        elif menu == "2":
            movie_change_menu()
        elif menu == "3":
            movie_delete_menu()
        elif menu == "4":
            print("관리자모드를 종료합니다.")
            break
        else:
            print("1~4 사이 숫자 내에서 입력해주세요.")


def movie_add_menu():
    print("추가할 영화명, 러닝타임을 입력해주세요.\n형식: <영화명><\"/\"><러닝타임>\n뒤로 가시려면 q를 입력해주세요.")
    while True:
        menu = input("입력 : ")
        if menu == "q":
            print("")
        # 뒤로가기
        else:
            flag = True
            movieTable = read_movie()
            # 예외처리 - 프롬프트 부분에 존재하지 않아요!
            try:
                movie, time = menu.strip().split("/")
            except ValueError:
                print("잘못된 형식입니다. 영화명과 러닝타임을 '/'로 구분하여 입력해주세요.")
                continue
            # 이미 있는 영화일 때 - 프롬프트 부분에 존재하지 않아요!
            for i, m, t in movieTable:
                if m == movie:
                    print("이미 존재하는 영화입니다. 다시 입력해주세요.")
                    flag = False
            # 러닝타임 의미규칙 어겼을 때 - 프롬프트에 숫자 잘못되어 있어요!, 프롬프트에 "~ 사이 숫자입니다" 를 아래의 워딩으로 수정해야 해요!
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

# 반복문 수정 필요
def movie_change_menu():
    print("수정할 영화아이디를 입력해주세요.\n[등록된 영화 내역]\n영화명     러닝타임     영화아이디\n")
    movieTable = read_movie()
    for i, m, t in movieTable:
        print(m, "     ", t, "     ", i)
    while True:
        id = input("입력1 : ")
        if id == "q":
            break
        else:
            # 입력 문법 검사
            if (len(id) == 3 and id[0].isdigit() and id[1].isdigit() and id[2].isdigit()):
                movieId = int(id)
                compareId = int(i)
                # 없는 영화아이디일 때
                if (movieId < 1 or movieId > compareId):
                    print("해당하는 영화아이디가 없습니다. 다시 입력해주세요.")
                else:
                    # !!! 상영스케줄이 잡혀있을 때 예외처리 !!!

                    # 프롬프트에서 문구 변경해야 해요!
                    print("1. 영화명 수정하기\n2. 러닝타임 수정하기")
                    while True:
                        change = input("입력2 : ")
                        if change == "1":
                            flag1 = True
                            print("변경하고 싶은 영화명을 입력해주세요.")
                            while True:
                                changeMovie = input("입력3 : ")
                                for _, m, _ in movieTable:
                                    if changeMovie == m:
                                        flag1 = False
                                        break
                                if flag1:
                                    edit_movie_title(id, changeMovie)
                                    print("영화명이 성공적으로 수정되었습니다.")
                                    #break
                                    return
                                else:
                                    # 프롬프트에서 문구 변경해야 해요!
                                    print("이미 등록된 영화명입니다. 다시 입력해주세요.")
                                    flag1 = True
                        elif change == "2":
                            flag2 = True
                            while True:
                                print("변경하고 싶은 러닝타임을 입력해주세요. (최소 50 ~ 최대 240)")
                                # 프롬프트에서 문구 변경해야 해요!
                                changeTime = input("입력4 : ")
                                for _, _, t in movieTable:
                                    if changeTime == t:
                                        flag2 = False
                                        break
                                if flag2:
                                    if (50 <= int(changeTime) and int(changeTime) <= 240 and changeTime.isdigit()):
                                        # 프롬프트에서 문구 변경해야 해요!
                                        edit_movie_time(id, changeTime)
                                        print("러닝타임이 성공적으로 수정되었습니다.")
                                        #break
                                        return
                                    else:
                                        print("러닝타임은 최소 50 ~ 최대 240 사이 숫자입니다. 다시 입력해주세요.")
                                else:
                                    # 프롬프트에서 문구 변경해야 해요!
                                    print("해당 영화의 러닝타임과 일치합니다. 다시 입력해주세요.")
                                    flag2 = True
                        else:
                            # 프롬프트에 추가 필요해요!
                            print("1~2 사이 숫자 내에서 입력해주세요.")
            else:
                # 프롬프트에서 문구 변경 필요해요!
                print("0과 정수로만 이루어진 길이가 3인 숫자입니다. 다시 입력해주세요.")

def movie_delete_menu():
    print("삭제할 영화아이디를 입력해주세요.\n[등록된 영화 내역]\n영화명     러닝타임     영화아이디\n")
    movieTable = read_movie()
    for i, m, t in movieTable:
        print(m, "     ", t, "     ", i)
    while True:
        id = input("입력 : ")
        # !!! 상영스케줄이 잡혀있을 때 예외처리 !!!
        if (len(id) == 3 and id[0].isdigit() and id[1].isdigit() and id[2].isdigit()):
            flag = False
            for i, _, _ in movieTable:
                if i == id:
                    flag = True
                    break

            if flag:
                # 프롬프트에서 문구 변경 필요해요!
                delete_movie(id)
                print("영화가 삭제되었습니다.")
                break
            else:
                # 프롬프트에서 문구 변경 필요해요!
                print("등록되어 있지 않은 영화 아이디 입니다. 다시 입력해주세요.")

        else:
            # 프롬프트에서 문구 변경 필요해요!
            print("0과 정수로만 이루어진 길이가 3인 숫자입니다. 다시 입력해주세요.")

def read_movie():
    return data.get_movie_list()

    # movieTable = []
    # with open("movie.txt", "r", encoding="utf-8") as f:
    #     for line in f:
    #         id, movie, time = line.strip().split("/")
    #         movieTable.append((id, movie, time))
    # return movieTable


def write_movie(id, movie, time):
    if (id < 10):
        newID = "0" + "0" + f"{id + 1}"
    elif (10 <= id < 100):
        newID = "0" + f"{id + 1}"
    elif (100 <= id):
        newID = f"{id + 1}"

    data.add_movie(newID, movie, time)
    # with open("movie.txt", "a", encoding="utf-8") as f:
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

    # 삭제할 영화를 찾아서 제외함
    movieTable = [movie for movie in movieTable if movie[0] != id]

    # 수정된 내용을 파일에 기록
    with open("data/" + "movie.txt", 'w', encoding='utf-8') as f:
        for i, m, t in movieTable:
            f.write(f"{i}/{m}/{t}\n")
