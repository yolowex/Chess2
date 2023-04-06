
def expand_fen_row( row ) :
    text = ""
    for i in row :
        if i.isnumeric() :
            for c in range(int(i)) :
                text += '0'
        else :
            text += i

    return text