typedef uint8_t VALUE;
typedef char KEY;
typedef struct {
	uint32_t capacity;
	KEY* keys;
	VALUE* values;
	uint8_t size;
} BinarySearchTable;