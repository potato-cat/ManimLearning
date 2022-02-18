def merge(start, mid, end):
    i = start
    j = mid + 1
    for k in range(start, end + 1):
        temp[k] = array[k]
    for k in range(start, end + 1):
        if i > mid:
            array[k] = temp[j]
            j += 1
        elif j > end:
            array[k] = temp[i]
            i += 1
        elif temp[i] > temp[j]:
            array[k] = temp[j]
            j += 1
        else:
            array[k] = temp[i]
            i += 1
