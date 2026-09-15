#include <stdio.h>
#include "cqlib_c.h"

int main(void) {
    int exit_code = 1;
    CircuitWrapper *source = NULL;
    CircuitWrapper *bound = NULL;
    ParameterWrapper *theta = NULL;

    source = circuit_new(2);
    theta = param_parse("theta");
    if (source == NULL || theta == NULL) goto cleanup;
    if (circuit_h(source, 0) != 0) goto cleanup;
    if (circuit_rx_param(source, 1, theta) != 0) goto cleanup;
    if (circuit_cx(source, 0, 1) != 0) goto cleanup;

    /* Append clones the parameter; the circuit keeps its own value. */
    param_free(theta);
    theta = NULL;
    if (circuit_validate(source) != 0) goto cleanup;
    if (circuit_num_qubits(source) != 2) goto cleanup;
    if (circuit_num_operations(source) != 3) goto cleanup;
    if (circuit_x(source, 2) != -2) goto cleanup;
    if (circuit_num_operations(source) != 3) goto cleanup;

    bound = circuit_assign_params(source, "theta:0.5");
    if (bound == NULL || bound == source) goto cleanup;
    if (circuit_validate(bound) != 0) goto cleanup;
    if (circuit_num_operations(bound) != 3) goto cleanup;
    puts("Cqlib C construction, binding and ownership checks passed");
    exit_code = 0;

cleanup:
    circuit_free(bound);
    circuit_free(source);
    param_free(theta);
    return exit_code;
}
