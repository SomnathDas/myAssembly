// gcc block.c -o block -lcrypto

#include <openssl/sha.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    unsigned char currentBlockHash[SHA256_DIGEST_LENGTH];
    unsigned char previousBlockHash[SHA256_DIGEST_LENGTH];
    char* message;
} Block;

typedef struct {
    int ixCurrentBlock;
    Block* blocks[];
} Blockchain;

void setHash(Block* block) {
    unsigned char md_buf[SHA256_DIGEST_LENGTH];
    size_t count = strlen(block->message);
    SHA256(block->message, count, md_buf);
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
        block->currentBlockHash[i] = md_buf[i];
    }
}

Block* createBlock(char* data, unsigned char previousBlockHash[SHA256_DIGEST_LENGTH]) {
    Block* newBlock = (Block*)malloc(sizeof(Block));
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
        newBlock->previousBlockHash[i] = previousBlockHash[i];
    }
    newBlock->message = data;
    setHash(newBlock);
    return newBlock;
}

Block* createGenesisBlock() {
    Block* genesisBlock = malloc(sizeof(Block));
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
        genesisBlock->previousBlockHash[i] = 0;
    }
    genesisBlock->message = "Root Block";
    setHash(genesisBlock);
    return genesisBlock;
}

Blockchain* newBlockchain() {
    Blockchain* newChain = malloc(sizeof(Blockchain) + sizeof(Block) * 100);
    newChain->ixCurrentBlock = 0;
    newChain->blocks[0] = createGenesisBlock();
    return newChain;
}

void addBlock(Blockchain* chain, char* data) {
    Block* previousBlock = chain->blocks[chain->ixCurrentBlock];
    Block* newBlock = createBlock(data, previousBlock->currentBlockHash);
    chain->blocks[chain->ixCurrentBlock + 1] = newBlock;
    chain->ixCurrentBlock += 1;
}

void freeBlockchain(Blockchain* chain) {
    for (int i = 0; i <= chain->ixCurrentBlock; ++i) {
        Block* currentBlock = chain->blocks[i];
        free(currentBlock);
    }
    free(chain);
}

int main(void) {
    Blockchain* chain = newBlockchain();
    addBlock(chain, "First transaction!");
    addBlock(chain, "Second transaction!");
    addBlock(chain, "Third transaction!");

    for (int i = 0; i <= chain->ixCurrentBlock; ++i) {
        Block* currentBlock = chain->blocks[i];
        printf("Previous Hash of Block %d :: \n", i);
        for (int j = 0; j < SHA256_DIGEST_LENGTH; ++j) {
            printf("%02x", currentBlock->previousBlockHash[j]);
        }
        printf("\n");

        printf("Current Hash of Block %d :: \n", i);
        for (int j = 0; j < SHA256_DIGEST_LENGTH; ++j) {
            printf("%02x", currentBlock->currentBlockHash[j]);
        }
        printf("\n");

        printf("Data stored in Block %d ::\n%s\n", i, currentBlock->message);
        printf("\n");
    }

    freeBlockchain(chain);
    return 0;
}
