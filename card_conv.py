def card_conv(x : int, r : int):
    d = []
    dchar = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if x == 0:
        return ['0']
    if x < 0:
        return "Please Insert the Positive Number"
    while x>0:
        d.append(dchar [x%r])
        x //=r
    return d[::-1]

if __name__ == '__main__':
    print('10진수를 n진수로 변환합니다.')
    while True:
        while True:
            no = int(input('변환할 값으로 음이 아닌 정수: '))
            if no>0:
                break
        while True:
            cd = int(input('어떤 진수로 변환할까요?: '))
            if 2 <= cd <= 36:
                break
        print(f"{cd}진수로는 {card_conv(no, cd)}입니다.")
        retry = input("한 번 더 변환하시나요? Y ... 예 / N ... 아니오")
        if retry in {'N', 'n', 'ㅜ'}:
            break
