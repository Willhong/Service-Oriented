def whatdo(do):
    if do == '서울특별시':
        add_code = 11
    if do == '부산광역시':
        add_code = 26
    if do == '대구광역시':
        add_code = 27
    if do == '인천광역시':
        add_code = 28
    if do == '광주광역시':
        add_code = 29
    if do == '대전광역시':
        add_code = 30
    if do == '울산광역시':
        add_code = 31
    if do == '세종특별자치시':
        add_code = 36
    if do == '경기도' or do =='경기':
        add_code = 41
    if do == '강원도' or do=='강원':
        add_code = 42
    if do == '충청북도' or do =='충북':
        add_code = 43
    if do == '충청남도' or do =='충남':
        add_code = 44
    if do == '전라북도' or do =='전북':
        add_code = 45
    if do == '전라남도' or do =='전남':
        add_code = 46
    if do == '경상북도' or do =='경북':
        add_code = 47
    if do == '경상남도' or do =='경남':
        add_code = 48
    if do == '제주특별자치도' or do =='제주':
        add_code = 50

    try:
        return add_code
    except UnboundLocalError:
        return 50
