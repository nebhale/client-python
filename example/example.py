# Copyright 2021 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
