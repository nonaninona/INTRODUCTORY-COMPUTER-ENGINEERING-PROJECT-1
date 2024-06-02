import data


def get_user_coupon(user_id):
    # 사용자 리스트에서 해당 id에 대한 쿠폰을 조회 / 유효한 쿠폰이면 쿠폰값을 반환, 아니라면 오류 메시지 출력 후 -1 반환
    for user in data.get_user_list():
        if user[0] == user_id:
            if user[2] == "O":
                return user[1]
            else:
                print("[get_user_coupon] 쿠폰이 유효하지 않습니다.")
                return -1

    print("[get_user_coupon] 일치하는 사용자아이디가 없습니다.")
    return -1


def change_coupon_available(user_id):
    # 쿠폰유효여부변경 O => X or X => O를 수행
    new_available = ""
    for user in data.get_ticket_list():
        if user[0] == user_id:
            if user[2] == '0':
                new_available = 'X'
                break
            elif user[2] == 'X':
                new_available = 'O'
                break
            else:
                print("[change_coupon_available] 잘못된 쿠폰유효여부가 들어있습니다.")
                exit()
    delete_user(user_id)
    data.add_user(user_id, get_user_coupon(user_id), new_available)


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
    user_list = data.get_user_list()
    new_user_list = [user for user in user_list if user[0] != user_id]

    with open("data/" + "user.txt", 'w', encoding='utf-8') as f:
        for user_id, coupon_price, coupon_available in new_user_list:
            f.write(f"{user_id}/{coupon_price}/{coupon_available}\n")

