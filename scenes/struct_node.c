typedef struct __node{
	char key[100];
	int val;
	struct __node* prev;
} NODE;

NODE* create(char* key, int val, NODE* prev) {
	NODE* node = (NODE*)malloc(sizeof(NODE));
	if (node == NULL)
		return NULL;
	strcpy_s(node->key, 100, key);
	node->val = val;
	node->prev = prev;
	return node;
}