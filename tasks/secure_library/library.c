#include <stdio.h>
#include <string.h>

#define FIELD_LENGTH 64


void welcome(void) {
    printf("Welcome to our library!\nHere are our books:\n\n");
    system("ls | grep .txt | cat");
    printf("\nEnter the name of a book you want to read:\n");
}


void readfile(char *filename) {
    char buffer[FIELD_LENGTH];
    FILE *fp;

    if (strstr(filename, "flag.txt")) {
        printf("\nPermission denied.\n");
        return;
    }

    fp = fopen(filename, "r");
    if (!fp) {
        printf("\nSorry, can't find a book like this...\n");  
        return;
    }

    printf("\nContent of book \"%s\":\n", filename);    
    while (fgets(buffer, FIELD_LENGTH, fp))
        printf("%s", buffer);

    fclose(fp);
}


void choose(void) {
    char command[FIELD_LENGTH];
    char garbage[FIELD_LENGTH * 4];
    char book_name[FIELD_LENGTH];
    
    memset(command, 0, sizeof(command));
    memset(garbage, 0, sizeof(garbage));
    memset(book_name, 0, sizeof(book_name));

    gets(book_name);
    readfile(book_name);
    
    if (garbage[0]) {
        garbage[FIELD_LENGTH - 1] = 0;
        printf("\nWhat did you mean by sending me %s??\n", garbage);
    }
    
    if (garbage[FIELD_LENGTH]) {
        garbage[FIELD_LENGTH * 2 - 1] = 0;
        printf("\nI can't understand your '%s'!\n", garbage + FIELD_LENGTH);
    }
    
    if (garbage[FIELD_LENGTH * 2]) {
        garbage[FIELD_LENGTH * 3 - 1] = 0;
        printf("\nWhat are you doing?! '%s' doesn't look friendly!\n", garbage + FIELD_LENGTH * 2);
    } 
    
    if (garbage[FIELD_LENGTH * 3]) {
        garbage[FIELD_LENGTH * 4 - 1] = 0;        
        printf("\nSTOP DOING THIS! You'll loose your library card!!!\n");
    }

    if (command[0]) {
        if (system(command))
            printf("invalid command\n");
    }
}


int main(int argc, char* argv) {
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    
    welcome();
    choose();

    return 0;
}
