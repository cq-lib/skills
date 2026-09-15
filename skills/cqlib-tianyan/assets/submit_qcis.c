#include <errno.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cqlib_tianyan.h"

int main(int argc, char **argv) {
    int exit_code = 1;
    TianyanPlatformC *platform = NULL;
    TianyanBackendC *backend = NULL;
    TianyanTaskC *task = NULL;
    TianyanResultList *results = NULL;
    char **ids = NULL;
    uintptr_t n_ids = 0;
    char *counts = NULL;
    const char *key = getenv("TIANYAN_API_KEY");
    if (argc != 4 || key == NULL || !*key || !*argv[1] || !*argv[2]) {
        fprintf(stderr, "Set TIANYAN_API_KEY; usage: submit_qcis BACKEND QCIS_TEXT SHOTS\n");
        return 1;
    }
    char *end = NULL;
    errno = 0;
    uintmax_t shots = strtoumax(argv[3], &end, 10);
    if (strspn(argv[3], "0123456789") != strlen(argv[3]) ||
        end == argv[3] || *end || errno ||
        shots == 0 || shots > UINTPTR_MAX) return 1;
    TianyanConfigC config = {NULL, NULL, false, true};
    platform = tianyan_platform_login_with_config(key, &config);
    if (!platform) goto failure;
    backend = tianyan_platform_get_backend(platform, argv[1]);
    if (!backend) goto failure;
    const char *circuits[] = {argv[2]};
    task = tianyan_backend_run_raw(backend, circuits, 1, (uintptr_t)shots);
    if (!task) goto failure;
    ids = tianyan_task_ids(task, &n_ids);
    if (!ids) goto failure;
    for (uintptr_t i = 0; i < n_ids; ++i) printf("Submitted: %s\n", ids[i]);
    fflush(stdout);
    results = tianyan_task_wait_raw(task, 120.0, 5.0);
    if (!results) goto failure;
    if (tianyan_result_list_len(results) != n_ids) {
        fprintf(stderr, "Returned result count differs from submission\n");
        goto cleanup;
    }
    for (uintptr_t i = 0; i < n_ids; ++i) {
        const char *id = tianyan_result_task_id(results, i);
        if (!id || strcmp(id, ids[i]) != 0) {
            fprintf(stderr, "Returned task ID/order differs from submission\n");
            goto cleanup;
        }
        counts = tianyan_result_counts_json(results, i);
        if (!counts) goto failure;
        printf("%s %s\n", id, counts);
        tianyan_string_free(counts);
        counts = NULL;
    }
    exit_code = 0;
    goto cleanup;
failure: {
    char *error = tianyan_last_error();
    fprintf(stderr, "Tianyan call failed: %s\n", error ? error : "unknown error");
    tianyan_string_free(error);
}
cleanup:
    tianyan_string_free(counts);
    tianyan_result_list_free(results);
    tianyan_task_ids_free(ids, n_ids);
    tianyan_task_free(task);
    tianyan_backend_free(backend);
    tianyan_platform_free(platform);
    return exit_code;
}
