# client-python

[![Tests](https://github.com/nebhale/client-python/workflows/Tests/badge.svg?branch=main)](https://github.com/nebhale/client-python/actions/workflows/tests.yaml)
[![codecov](https://codecov.io/gh/nebhale/client-python/branch/main/graph/badge.svg)](https://codecov.io/gh/nebhale/client-python)

`client-python` is a library to access [Service Binding Specification for Kubernetes](https://k8s-service-bindings.github.io/spec/) conformant Service Binding [Workload Projections](https://k8s-service-bindings.github.io/spec/#workload-projection).

## Example

```python
import psycopg2 as psycopg2

from bindings import bindings

b = bindings.from_service_binding_root()
b = bindings.filter(b, "postgresql")

if len(b) != 1:
raise ValueError("Incorrect number of PostgreSQL bindings: %s" % len(b))

u = b[0].get("url")
if u is None:
    raise ValueError("No URL in binding")

conn = psycopg2.connect(u)

# ...

```

## License

Apache License v2.0: see [LICENSE](./LICENSE) for details.
