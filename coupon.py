import data

""""
print_my_coupon(user_id) : 해당 유저의 쿠폰 출력

publish_new_coupon(user_id, date_time) : login 시 유저에게 해당하는 쿠폰 발급

"""

def print_my_coupon(user_id):
    print("-----------")
    # 유효성 검사
    result = get_user_coupon(user_id)
    if result != -1: # 쿠폰 있는 경우
        print("쿠폰 : "+result+"원 할인 쿠폰")
        print("사용 가능 유무 : O")
    else: # 쿠폰 없는 경우 (임의로 작성)
        print("사용 가능한 쿠폰이 없습니다.")


def publish_new_coupon(user_id, date_time):
    # 현재 날짜에서 월/일 저장
    current_month = date_time[4:6]
    current_date = date_time[6:8]
    # 현재 날짜가 16일 이상인 경우 쿠폰유효여부 변경
    if int(current_date) >= 16:
        change_coupon_unavailable(user_id)
        return
    
    else: # 현재 날짜가 15일 이하인 경우
        is_used = is_coupon_used(current_month, user_id)
        if is_used == True: # 이번달에 쿠폰 사용한 경우
            return
        # 이번달에 쿠폰 사용하지 않은 경우
        # 1. 쿠폰유효여부를 통해 쿠폰의 발급달 확인
        # 유효여부가 O라면 이미 쿠폰 발급되었다는 것 => 종료 // X라면 저번달 쿠폰 => 계속 진행
        coupon_available = get_coupon_available(user_id)
        if coupon_available == "O":
            return
        
        # 2. 지난달 실적 확인
        prev_month = ""
        if int(current_month) > 1: # 1월이 아닌 경우
            prev_month = str(int(current_month) - 1)
        else: #1월인 경우
            prev_month = str(12)
        last_reservation = data.get_month_reservation_list(prev_month, user_id)
        if last_reservation == []:
            # 0/X 쿠폰 발급
            change_coupon(user_id, "0", "X")
        else:
            last_price = 0
            for r in last_reservation:
                last_price += int(r[2]) * 10000
            if last_price >= 50000 and last_price < 60000:
                # 1000/O 쿠폰 발급
                change_coupon(user_id, "1000", "O")
            elif last_price >= 60000 and last_price < 80000:
                # 3000/O 쿠폰 발급
                change_coupon(user_id, "3000", "O")
            elif last_price >= 80000:
                # 5000/O 쿠폰 발급
                change_coupon(user_id, "5000", "O")
            else:
                # 0/X 쿠폰 발급
                change_coupon(user_id, "0", "X")

    
def is_coupon_used(current_month, user_id):
    # 이번달의 예매내역
    current_month_reservation = data.get_month_reservation_list(current_month, user_id)
    for r in current_month_reservation:
        if r[4] != "0": # 쿠폰 사용한 경우
            return True
    return False

def pay_prompt(user_id,people,exist):
    coupon = get_user_coupon(user_id)
    print("결제하실 금액은 다음과 같습니다")
    print("결제 금액 : %d원\n"%(10000*int(people))) # 10000 * 인원수
    print("[나의 쿠폰 목록]\n")

    if not exist:
        print("적용 가능한 쿠폰이 없습니다.")
        print("결제금액 : " + str(10000*int(people)) + "원")
        print("----------------")
        print("\n결제 금액 : " + str(10000*int(people)) + "원")
        print("성공적으로 예매가 완료되었습니다.\n")
        return 0
    
    print_coupon_menu(coupon, people, user_id)


def print_coupon_menu(coupon, people, user_id):
    #쿠폰 있을 때
    print(coupon + "원 할인쿠폰\n")
    print("※ (쿠폰을 적용하시려면 '1', 적용하지 않으시려면 '2'를 입력해주세요)")
    print("1. 쿠폰 적용하기\n2. 쿠폰 적용없이 결제하기")
    while True:
        choice = input("입력 : ")
        if not (choice.isdigit() and (int(choice) ==1 or 2)):
            print("다시 입력해주세요\n")          
        else:
            break

    if int(choice)==1:
        while True:
            print("결제금액 : " + str(10000*int(people)) + "원")
            print("적용쿠폰 : " + coupon + "원 할인 쿠폰")
            print("----------------")
            print("총 결제금액 : " + str(10000*int(people)-int(coupon)) + "원\n")
            print("※ (최종 결제를 원하면 '1', 이전 단계로 돌아가려면 '2'을 입력해주세요.)")
            print("1.결제진행하기")
            print("2.돌아가기\n")
            choice=input("입력 : ")
            if not choice.isdigit():
                print("다시 입력해주세요.\n")   
            else:
                break

        if int(choice)==1:
            print("\n결제 금액 : " + str(10000*int(people)-int(coupon)) + "원")
            print("성공적으로 예매가 완료되었습니다.\n")
            change_coupon_available(user_id)
            return int(coupon)
        elif int(choice) == 2:
            print("\n쿠폰 적용 메뉴로 돌아갑니다.\n")
            return print_coupon_menu(coupon, people, user_id)
            
    elif int(choice)==2:
        while True:
            print("결제금액 : " + str(10000*int(people)) + "원")
            print("————————")
            print("총 결제금액 : " + str(10000*int(people)) + "원\n")
            print("※ (최종 결제를 원하면 '1', 이전 단계로 돌아가려면 '2'을 입력해주세요.)")
            print("1.결제진행하기")
            print("2.돌아가기\n")
            choice = input("입력 : ")
            if not choice.isdigit():
                print("다시 입력해주세요.\n") 
            else:
                break

        if int(choice)==1:
            print("\n결제 금액 : " + str(10000*int(people)) + "원")
            print("성공적으로 예매가 완료되었습니다.\n")
            return 0
        elif int(choice) == 2:
            print("\n쿠폰 적용 메뉴로 돌아갑니다.\n")
            return print_coupon_menu(coupon, people, user_id)


""""

data

"""

def get_coupon_available(user_id):
    # 해당 사용자의 쿠폰유효여부를 조회
    for user in data.get_user_list():
        if user[0] == user_id:
            return user[2]
    print("[get_coupon_available] 일치하는 예약자아이디가 없습니다")
    return -1


def get_user_coupon(user_id):
    # 사용자 리스트에서 해당 id에 대한 쿠폰을 조회 / 유효한 쿠폰이면 쿠폰값을 반환, 아니라면 오류 메시지 출력 후 -1 반환
    for user in data.get_user_list():
        if user[0] == user_id:
            print(user[2])
            if user[2] == "O":
                return user[1]
            else:
                print("[get_user_coupon] 쿠폰이 유효하지 않습니다.")
                return -1
    print("[get_user_coupon] 일치하는 예약자아이디가 없습니다.")
    return -1


def coupon_exist(user_id):
    if int(get_user_coupon(user_id)) < 0:
        return False
    else: return True


def change_coupon(user_id, price, available):
    # 해당 사용자의 쿠폰가격, 쿠폰유효여부 변경
    delete_user(user_id)
    data.add_user(user_id, price, available)


def change_coupon_available(user_id):
    # 쿠폰유효여부변경 O => X or X => O를 수행
    new_available = ""
    user_coupon = ""
    for user in data.get_user_list():
        if user[0] == user_id:
            if user[2].strip() == 'O':
                new_available = 'X'
                user_coupon = user[1]
                break
            elif user[2].strip() == 'X':
                new_available = 'O'
                user_coupon = user[1]
                break
            else:
                print("[change_coupon_available] 잘못된 쿠폰유효여부가 들어있습니다.")
                exit()
    print(user_coupon)
    delete_user(user_id)
    data.add_user(user_id, user_coupon, new_available)


def change_coupon_unavailable(user_id):
    # 쿠폰유효여부를 X로 변경
    user_coupon = get_user_coupon(user_id)
    delete_user(user_id)
    data.add_user(user_id, user_coupon, "X")


def get_used_coupon(type, id):
    # 적용쿠폰가격 가져오기
    # type은 reservation_id 또는 user_id 중 하나로, 두 개 중 하나로 조회 가능
    # reservation 0 예매아이디 / 1 예약자아이디 / 2 예약인원수 / 3 예약취소여부 / 4 적용쿠폰가격(개행)
    for reservation in data.get_reservation_list():
        if type == "reservation_id":
            if reservation[0] == id:
                return reservation[4].strip()
        elif type == "user_id":
            if reservation[1] == id:
                return reservation[4].strip()
    print("[get_used_coupon] type이 잘못 입력되었거나 해당 id에 대한 예매정보가 없습니다. type : " + type + ", id : " + id)
    return -1


def delete_user(user_id):
    # user 삭제 부분 // coupon update에서 사용
    new_user_list = [user for user in data.get_user_list() if user[0] != user_id]

    with open("data/" + "user.txt", 'w', encoding='utf-8') as f:
        for new_user in new_user_list:
            f.write(f"{new_user[0]}/{new_user[1]}/{new_user[2]}\n")     
    