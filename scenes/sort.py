def sort(start, end):
    mid = (start+end)//2
    sort(start, mid)
    sort(mid + 1, end)
    if array[mid] <= array[mid + 1]:
        return
    merge(start, mid, end)