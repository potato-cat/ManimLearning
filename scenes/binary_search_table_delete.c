int delete(BinarySearchTable* p_bst, KEY key) {
	int key_rank = 0, ix = 0;
	if (p_bst->size == 0 ||
		compare(key, p_bst->keys[p_bst->size - 1]) > 0) {
		return 0;
	}
	key_rank = rank(p_bst, key);
	if (compare(p_bst->keys[key_rank], key) == 0) {
		for (ix = key_rank; ix < p_bst->size - 1; ix++) {
			p_bst->keys[ix] = p_bst->keys[ix + 1];
			p_bst->values[ix] = p_bst->values[ix + 1];
		}
		p_bst->size--;
		return p_bst->size;
	}
	else
		return -1;
}