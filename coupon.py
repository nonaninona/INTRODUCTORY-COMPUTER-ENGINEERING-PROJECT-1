import data

""""
print_my_coupon(user_id) : 해당 유저의 쿠폰 출력
"""

def print_my_coupon(user_id):
    print("-----------")
    # 유효성 검사
    result = get_user_coupon(user_id)
    if result != -1: # 쿠폰 있는 경우
        print("쿠폰 : %d원 할인 쿠폰" %result)
        print("사용 가능 유무 : O")
    else: # 쿠폰 없는 경우 (임의로 작성)
        print("사용 가능한 쿠폰이 없습니다.")
    

""""

data

"""
def get_user_coupon(user_id):
    # 사용자 리스트에서 해당 id에 대한 쿠폰을 조회 / 유효한 쿠폰이면 쿠폰값을 반환, 아니라면 오류 메시지 출력 후 -1 반환
    user_list = data.get_user_list2()

    for user in user_list:
        if user[0] == user_id:
            if user[2] == "O":
                return user[1]
            else:
                print("[오류] 쿠폰이 유효하지 않습니다.")
                return -1

    print("[오류] 일치하는 사용자아이디가 없습니다.")
    return -2
def coupon_exist(user_id):
    if get_user_coupon(user_id) < 0:
        return False
    else: return True



def change_coupon_available(user_id):
    # 쿠폰유효여부변경 O => X or X => O를 수행
    coupon_price = get_user_coupon(user_id)

    user_list = data.get_ticket_list2()
    new_available = ""
    for user in user_list:
        if user[0] == user_id:
            if user[2] == '0':
                new_available = 'X'
                break
            elif user[2] == 'X':
                new_available = 'O'
                break
            else:
                print("[오류] 잘못된 쿠폰유효여부가 들어있습니다.")

    delete_user(user_id)
    data.add_user(user_id, coupon_price, new_available)


def get_used_coupon(type, id):
    # 적용쿠폰가격 가져오기
    # type은 reservation_id 또는 user_id 중 하나로, 두 개 중 하나로 조회 가능
    reservation_list = data.get_reservation_list2()

    for reservation_id, user_id, _, cancel, coupon_price in reservation_list:
        if type == "reservation_id":
            if reservation_id == id:
                return coupon_price
        elif type == "user_id":
            if user_id == id:
                return coupon_price
    print("[오류] type이 잘못 입력되었거나 해당 id에 대한 예매정보가 없습니다. type : " + type + ", id : " + id)
    return -1


def delete_user(user_id):
    #user 삭제 부분 // coupon update에서 사용
    user_list = data.get_user_list2()
    new_user_list = [user for user in user_list if user[0] != user_id]

    with open("data/" + "user.txt", 'w', encoding='utf-8') as f:
        for user_id, coupon_price, coupon_available in new_user_list:
            f.write(f"{user_id}/{coupon_price}/{coupon_available}\n")

def apply_coupon(user_id,people):
    coupon=get_user_coupon(user_id)
    if coupon_exist() < 0:
        print("적용 가능한 쿠폰이 없습니다.")      
    else:
        while True:
            choice = input()
            if choice.isdigit():      
                while True:
                    print("결제금액 : "+str(10000*people)+"원")
                    print("적용쿠폰 : "+str(coupon)+"원 할인 쿠폰")
                    print("----------------")
                    print("총 결제금액 : "+str(10000*people-coupon)+"원\n")
                    print("※ (최종 결제를 원하면 '1', 이전 단계로 돌아가려면 '2'을 입력해주세요.)")
                    print("1.결제진행하기")
                    print("2.돌아가기\n")
                    print("입력 : ")
                    choice=input()
                    if choice.isdigit():
                        if int(choice)==1:
                            print("\n결제 금액 : "+str(10000*people-coupon)+"원")
                            print("성공적으로 예매가 완료되었습니다.\n")
                            change_coupon_available(user_id)
                            break
                        elif int(choice) == 2:
                            print("\n쿠폰 적용 메뉴로 돌아갑니다.\n")
                            break
                    else:
                        print("다시 입력해주세요.\n")   
                break
            else:
                print("다시 입력해주세요\n")          
    