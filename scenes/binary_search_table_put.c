int put(BinarySearchTable* p_bst, KEY key, VALUE val) {
	int key_rank = 0, ix = 0;
	if (p_bst->size == 0 ||
		compare(key, p_bst->keys[p_bst->size - 1]) > 0) {
		p_bst->keys[p_bst->size] = key;
		p_bst->values[p_bst->size] = val;
		p_bst->size++;
		return 1;
	}
	key_rank = rank(p_bst, key);
	if (compare(p_bst->keys[key_rank], key) == 0) {
		p_bst->values[key_rank] = val;
		return p_bst->size;
	}
	else {
		if (p_bst->size == p_bst->capacity) {
			return -1;
		}
		for (ix = p_bst->size; ix > key_rank; ix--) {
			p_bst->keys[ix] = p_bst->keys[ix - 1];
			p_bst->values[ix] = p_bst->values[ix - 1];
		}
		p_bst->keys[key_rank] = key;
		p_bst->values[key_rank] = val;
		p_bst->size += 1;
		return p_bst->size;
	}
}