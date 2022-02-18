def sort(arr):
    h = 1
    while h < len(arr) // 3:
        h = 3 * h + 1
    while h >= 1:
        for i in range(h, len(arr)):
            for j in range(i, h - 1, -h):
                if arr[j] < arr[j - h]:
                    arr[j], arr[j - h] = arr[j - h], arr[j]
        h = h // 3
    return arr
