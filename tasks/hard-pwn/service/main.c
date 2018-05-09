#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>


int debug = 0;


void loading_bar(void) {
    srand(time(NULL));
    
    int max_size = 20;
    fprintf(stdout, "\e[1m[\e[0m");
    for (int i = 0; i < max_size; i++) {
        usleep(10000 * (rand() % 30));
        fprintf(stdout, "\x1b[33m#\x1b[0m");
        fflush(stdout);
    }
    fprintf(stdout, "\e[1m]\e[0m\n");
    fprintf(stdout, "\x1b[32m[+]\x1b[0m \e[1mCompleted!\e[0m\n\n");
}

void process(char *command) {
    long buf = 0;
    
    read(0, buf, 0);
    write(1, buf, 0);
    
    asm(".intel_syntax noprefix\n\t"
        "pop rdx; ret;"
        ".att_syntax prefix");
}

void welcome(void) {
    size_t len = 0;
    char buf[101];

    memset(buf, 0, 101);
    
    fprintf(stdout, "\x1b[35m[~]\x1b[0m System is \e[1msetting up\e[0m...\n");
    loading_bar();
    fprintf(stdout, "\x1b[36m[*]\x1b[0m Identify yourself: ");
    
    fgets(buf, 101, stdin);
    len = strlen(buf);
    if (buf[len-1] == '\n') buf[len] = 0;
}

void login_panel(void) {
    char *command;
    long key;
    
    asm(".intel_syntax noprefix\n\t"
        "mov rsi, [rsp-0x4];"
        "mov [rbp-8], rsi;   "
        ".att_syntax prefix");

    fprintf(stdout, "\x1b[36m[*]\x1b[0m Input \e[1msecret key\e[0m: ");

    getchar();
    read(0, key, 10);
    fflush(stdin);

    if (key != 0xdeadbeef) {
        printf("\x1b[31m[-]\x1b[0m Incorrect key\n");
        exit(1);
    }
    
    fprintf(stdout, "\x1b[32m[+]\x1b[0m Logged in\n");
    
    fprintf(stdout, "\x1b[36m[*]\x1b[0m Enter command: ");
    fgets(&command, 250, stdin);
    
    if (debug)
        process(command);
}

int main(int argc, char **argv) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    welcome();
    login_panel();
    
    fprintf(stdout, "Bye-bye.\n");
}
