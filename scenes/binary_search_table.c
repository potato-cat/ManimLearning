#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<stdint.h>

typedef uint8_t VALUE;

typedef char KEY;

int compare(KEY k1, KEY k2) {
	return k1 - k2;
}

typedef struct {
	uint32_t capacity;
	KEY* keys;
	VALUE* values;
	uint8_t size;
} BinarySearchTable;

int initialize(BinarySearchTable* p_bst, uint32_t capacity) {
	p_bst->capacity = capacity;
	p_bst->keys = malloc(capacity * sizeof(KEY));
	p_bst->values = malloc(capacity * sizeof(VALUE));
	p_bst->size = 0;
	return 0;
}

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

int put(BinarySearchTable* p_bst, KEY key, VALUE val) {
	int key_rank = 0, ix = 0;
	if (p_bst->size == 0 || compare(key, p_bst->keys[p_bst->size - 1]) > 0) {
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

int delete(BinarySearchTable* p_bst, KEY key) {
	int key_rank = 0, ix = 0;
	if (p_bst->size == 0 || compare(key, p_bst->keys[p_bst->size - 1]) > 0) {
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

void print(BinarySearchTable* p_bst) {
	int ix = 0;
	for (ix = 0; ix < p_bst->size; ix++) {
		printf("%c: %d\n", p_bst->keys[ix], p_bst->values[ix]);
	}
}

int main() {
	int key_rank;
	BinarySearchTable bst = { 0, 0, 0, 0 };
	initialize(&bst, 10);
	put(&bst, 'c', 50);
	put(&bst, 'a', 48);
	put(&bst, 'b', 49);
	key_rank = rank(&bst, 'd');
	print(&bst);
	printf("find: %d\n", key_rank);
	delete(&bst, 'a');
	print(&bst);
}