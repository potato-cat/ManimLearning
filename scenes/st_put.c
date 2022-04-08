NODE* put(NODE* st, char* key, int val) {
	NODE* node;
	if (st == NULL) {
		node = create(key, val, NULL);
		return node;
	}
	else {
		for (node = st; node != NULL; node=node->prev) {
			if (!strcmp(node->key, key)) {
				node->val = val;
				return st;
			}
		}
		node = create(key, val, st);
		return node;
	}
}