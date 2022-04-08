int rank(BinarySearchTable* p_bst, KEY key) {
	int low = 0, high = p_bst->size - 1, mid = 0;
	if (p_bst->size == 0)
		return 0;
	while (low <= high) {
		mid = (low + high) / 2;
		if (compare(p_bst->keys[mid], key) == 0) {
			return mid;
		}
		if (compare(p_bst->keys[mid], key) > 0) {
			high = mid - 1;
		}
		else {
			low = mid + 1;
		}
	}
	return low;
}