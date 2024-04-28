# theater
def add_theater(id, name):
    file_a("theater.txt", id + '/' + name + '\n')


def get_theater_list():
    theater_list = file_r("theater.txt")
    return theater_list


# seat
def add_seat(seat_id, theater_id, seat_num):
    file_a("seat.txt", seat_id + '/' + theater_id + '/' + seat_num + '\n')


def get_seat_list():
    seat_list = file_r("seat.txt")
    return seat_list


# movie
def add_movie(id, name, time):
    file_a("movie.txt", id + '/' + name + '/' + str(time) + '\n')


def get_movie_list():
    movie_list = file_r("movie.txt")
    return movie_list


# schedule
def add_schedule(timetable_id, movie_id, theater_id, date, time):
    file_a("schedule.txt", timetable_id + '/' + movie_id + '/' + theater_id + '/' + date + '/' + time + '\n')


def get_schedule_list():
    schedule_list = file_r("schedule.txt")
    return schedule_list


# ticket
def add_ticket(ticket_id, reservation_id, seat_id, timetable_id):
    file_a("ticket.txt", ticket_id + '/' + reservation_id + '/' + seat_id + '/' + timetable_id + '\n')


def get_ticket_list():
    ticket_list = file_r("ticket.txt")
    return ticket_list


# reservation
def add_reservation(reservation_id, user_id, num, cancel):
    file_a("reservation.txt", reservation_id + '/' + user_id + '/' + num + '/' + cancel + '\n')


def get_reservation_list():
    ticket_list = file_r("reservation.txt")
    return ticket_list


# user
def add_user(user_id):
    file_a("user.txt", user_id + '\n')


def get_user_list():
    user_list = file_r("user.txt")
    return user_list


def file_a(path, content):
    f = open("data/" + path, 'a', encoding='utf-8')
    f.write(content)
    f.close()


def file_i(path, content):
    f = open("data/" + path, 'w', encoding='utf-8')
    f.write(content)
    f.close()


def file_r(path):
    f = open("data/" + path, 'r', encoding='utf-8')
    data_list = f.readlines()
    f.close()
    return data_parsing(data_list)


# base function
def data_parsing(array):
    parsed_data = []
    for str in array:
        row = str.strip().split('/')
        parsed_data.append(row)
    return parsed_data


def sort_data(data_list, index):
    return sorted(data_list, key=lambda x: x[index])
