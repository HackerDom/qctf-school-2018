#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*  

=== HOW 2 COMPILE ===
    
gcc -fno-stack-protector -mpreferred-stack-boundary=2 -z execstack -m32 oil.c -o oil
    
=== OK NOW USE IT === 

*/

void print_menu(void) {
    printf("\n");
    printf("Select your action:\n");
    printf("1. Show current oil reserve on the platform.\n");
    printf("2. Update information about platform.\n");
    printf("3. Export all information.\n");
    printf("4. Exit.\n");
    printf("\n");
    printf("Your choice: ");
}


void manage(void) {
    char platforms[1024];
    int choice;
    int number;
    
    memset(platforms, 0, 1024);

    while (1) {
        print_menu();
        scanf("%d", &choice);

        if (choice == 4)
            break;
        
        if (choice == 3) {
            printf("Save it! %s\n", platforms);
            continue;
        }
        
        if (choice != 1 && choice != 2) {
            printf("Incorrect action!\n");
            continue;
        }
        
        printf("Enter platform number: ");
        scanf("%d", &number);
        if (number < 0 || number > 1024) {
            printf("Incorrect number of the platform!\n");
            continue;
        }

        if (choice == 1)
            printf("Selected platform contains %d oil.\n", (unsigned char)(platforms[number]));

        if (choice == 2) {
            printf("Enter new oil reserve on the platform: ");
            scanf("%lld", &platforms[number]);
            printf("Platform updated.\n");
        }
    }
}


int main(int argc, char **argv) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    printf("Welcome to Oil Platform Manager!\n");
    
    manage();
    
    printf("Bye.\n");
    return 0;
}

// one day, one fine day... I'll build my own Oil Tower!!!
