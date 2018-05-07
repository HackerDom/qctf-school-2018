#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TOKENS_FILENAME "/etc/tokens/tokens"

#define TOKEN_LENGTH 32
#define FLAG_LENGTH 36


void usage(char* name) {
    printf("That program will give you your flag.\n");
    printf("Usage: %s <token>\n", name);
    printf("Where <token> is your team token.\n");
}


char* extract_flag(char* token) { 
    FILE* fp;
    char* read_token;
    char* read_flag;

    read_token = malloc(TOKEN_LENGTH);
    read_flag = malloc(FLAG_LENGTH);

    fp = fopen(TOKENS_FILENAME, "r");
    if (!fp)
        return NULL;

    while (fscanf(fp, "%s %s\n", read_token, read_flag) != EOF) {
        if (!strncmp(token, read_token, TOKEN_LENGTH)) {
            free(read_token);

            fclose(fp);
            return read_flag;
        }
    }

    free(read_token);
    free(read_flag);

    fclose(fp);
    return NULL;
}


int main(int argc, char* argv[]) {
    char* flag;

    if (argc > 1) {
        flag = extract_flag(argv[1]);

        if (flag) {
            printf("Your flag: %s\n", flag);
            free(flag);
        }
        else {
            printf("Incorrect team token.\n");
        }

        return 0;
    }

    usage(argv[0]);
    return 0;
}
