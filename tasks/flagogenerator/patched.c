#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

int DEBUG_MODE = 1;

int silly_power(int base, int n)
{	
	int p = 1;
	for (int i = 1; i <= n; ++i)
		p = p * base;
	p = abs(p - 666);
	return p;
}

uint32_t useless_hash(char *key, size_t len)
{
    uint32_t hash, i;
    for(hash = i = 0; i < len; ++i)
    {
        hash += key[i];
        hash += (hash << 10);
        hash ^= (hash >> 6);
    }
    hash += (hash << 3);
    hash ^= (hash >> 11);
    hash += (hash >> 10);
    hash ^= (hash >> 7);
    hash ^= (hash >> 11);
    hash += (hash << 8);
    hash ^= (hash << 6);    
    hash += (hash << 15);

    return hash;
}

char *bad_concat(char *str1, char *str2)
{
	str2[1] = str1[7];
	str1[0] = str2[3];
	str1[2] = str2[4];
	str2[6] = str1[0];
	str2[0] = str2[2];
	str2[5] = str1[5];
	str1[7] = str2[7];
	str2[4] = str1[6];
	str1[1] = str2[5];
	str1[5] = str1[6];
	char *newstr; 
	char *tempstr;
	asprintf(&newstr, "%s%s", str1, str2);
	return newstr;
}

char *broken_caesar(char *text)
{
	int key = 19;
	char ch;
	for(int i = 0; text[i] != '\0'; ++i)
	{
        ch = text[i];        
        if(ch >= 'A' && ch <= 'Z')
        {
            ch = ch + key;            
            if(ch > 'Z')
            {
                ch = ch - 'Z' + 'A' - 1;                
            }
            text[i] = ch;
            if (i > 3)         
            	if(ch == 'O')
            		text[i] = text[i - 2];
        }
    }
    return text;
}

void break_everything(char* substr1, char* substr2, char* substr3)
{
	printf("\nYour flag is generated!\n");
	if (DEBUG_MODE == 1)
		printf("QCTF{%s%s%s}\n", substr1, substr2, substr3);
	else
		printf("...But you're not allowed to see it. Ahahaha :D\n");
}

int main(int argc, char* argv[])
{	
	if (argc != 2)
	{
		printf("usage: ./flagogenerator <TOKEN>\n");
		exit(1);
	}

	char salt1[] = "REVERSEME";
	char salt2[] = "OLOLOLOLOLOLOLO";
	char salt3[] = "EASYPEASY";
	char token[33];
	char substr1[11];
	char substr2[13];
	char substr3[11];
	char str[11];
	
	memcpy(token, argv[1], 32);
	printf("Hello! This program will generate a flag for you by your token :)\n");

	memcpy(substr1, token, 10);
	memcpy(substr2, token + 10, 12);
	memcpy(substr3, token + 22, 10);

	
	printf("\nApplying Caesar...\n");
	memcpy(substr2, broken_caesar(substr2), 12);	
	memcpy(substr3, broken_caesar(substr3), 10);
	printf("Applying hashing algorithms...\n");
	sprintf(str, "%u", useless_hash(substr3, sizeof(substr3)));
	sprintf(str, "%u", useless_hash(str, sizeof(str)));
	printf("Applying concatenation...\n");
	memcpy(substr2, bad_concat(broken_caesar(substr1), substr2), 12);
	memcpy(substr2, bad_concat(broken_caesar(substr3), substr2), 12);
	memcpy(substr2, bad_concat(broken_caesar(substr1), substr2), 12);
	memcpy(substr2, bad_concat(substr2, bad_concat(substr1, broken_caesar(substr3))), 12);
	memcpy(substr3, bad_concat(broken_caesar(bad_concat(substr1, substr2)), broken_caesar(substr3)), 10);
	memcpy(substr1, bad_concat(broken_caesar(substr3), bad_concat(str, substr1)), 10);

	break_everything(substr2, substr3, substr1);

	return 0;
}

