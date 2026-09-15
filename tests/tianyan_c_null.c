/* Offline ABI smoke test: no client construction, credentials or network. */
#include <assert.h>
#include <stdio.h>
#include "cqlib_tianyan.h"

int main(void) {
    assert(tianyan_platform_login(NULL) == NULL);
    char *error = tianyan_last_error();
    assert(error != NULL && error[0] != '\0');
    tianyan_string_free(error);
    assert(tianyan_backend_run_raw(NULL, NULL, 0, 1) == NULL);
    assert(tianyan_task_wait_raw(NULL, 1.0, 1.0) == NULL);
    assert(tianyan_result_list_len(NULL) == 0);
    assert(tianyan_result_task_id(NULL, 0) == NULL);
    tianyan_result_list_free(NULL);
    tianyan_task_ids_free(NULL, 0);
    tianyan_task_free(NULL);
    tianyan_backend_free(NULL);
    tianyan_platform_free(NULL);
    tianyan_string_free(NULL);
    puts("Tianyan C NULL/error/cleanup checks passed (no network)");
    return 0;
}
