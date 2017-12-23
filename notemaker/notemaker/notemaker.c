#include <stdio.h>
#include <stdlib.h>

int main()
{
	FILE *f1 = fopen("C:\\Users\\mskan\\Desktop\\rhythmgmae\\note\\Aragami.txt", "r");
	FILE *f2 = fopen("Aragami.txt", "w");
	int i = 0, a, b, c;
	char str[20];
	int target1[1019];
	int target2[1019];
	if (f1 == NULL || f2 == NULL) {
		puts("FILE OPEN ERROR!");
		return 1;
	}

	while (!feof(f1)) {
		fscanf(f1, "%d, %d, %d, %d, %d, %s", &target1[i], &a, &target2[i], &b, &c, str);
		i += 1;
	}

	for (i = 0; i < 1019; i++) {
		if (target1[i] == 64)
			fprintf(f2, "%d ", 1);
		else if (target1[i] == 192)
			fprintf(f2, "%d ", 2);
		else if (target1[i] == 320)
			fprintf(f2, "%d ", 3);
		else if (target1[i] == 448)
			fprintf(f2, "%d ", 4);

		fprintf(f2, "%d\n", target2[i]);
	}

	fclose(f1);
	fclose(f2);

	return 0;
}