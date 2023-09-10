#include <stdio.h>

extern int doAdd(int,int);

int doAdd(int a, int b) {
	printf("Adding inputs...\n");
	return a + b;
}
