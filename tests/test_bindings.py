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

import os
import unittest
from os import path

from bindings import binding, bindings


class TestBindings(unittest.TestCase):
    def test_cached(self):
        b = bindings.cached([binding.DictBinding("test-name-1", {}), binding.DictBinding("test-name-2", {})])

        for b in b:
            self.assertIs(binding.CacheBinding, type(b))

    def test_from_invalid(self):
        v = bindings.from_path("missing")
        self.assertEqual(0, len(v))

    def test_from_non_directory(self):
        v = bindings.from_path(path.join("tests", "testdata", "additional-file"))
        self.assertEqual(0, len(v))

    def test_from_exists(self):
        v = bindings.from_path(path.join("tests", "testdata"))
        self.assertEqual(3, len(v))

    def test_from_service_binding_root_unset(self):
        v = bindings.from_service_binding_root()
        self.assertEqual(0, len(v))

    def test_from_service_binding_root_set(self):
        old = os.getenv("SERVICE_BINDING_ROOT")
        os.environ["SERVICE_BINDING_ROOT"] = path.join("tests", "testdata")

        try:
            v = bindings.from_service_binding_root()
            self.assertEqual(3, len(v))
        finally:
            if old is None:
                del os.environ["SERVICE_BINDING_ROOT"]
            else:
                os.environ["SERVICE_BINDING_ROOT"] = old

    def test_find_invalid(self):
        b = [binding.DictBinding("test-name-1", {})]

        self.assertIsNone(bindings.find(b, "test-name-2"))

    def test_find_valid(self):
        b = [binding.DictBinding("test-name-1", {})]

        self.assertIsNotNone(bindings.find(b, "test-name-1"))

    def test_filter_empty(self):
        b = [
            binding.DictBinding("test-name-1", {"type": b"test-type-1", "provider": b"test-provider-1"}),
            binding.DictBinding("test-name-1", {"type": b"test-type-2"}),
        ]

        self.assertEqual(0, len(bindings.filter(b, "test-type-3")))

    def test_filter_single(self):
        b = [
            binding.DictBinding("test-name-1", {"type": b"test-type-1", "provider": b"test-provider-1"}),
            binding.DictBinding("test-name-1", {"type": b"test-type-2"}),
        ]

        self.assertEqual(1, len(bindings.filter(b, "test-type-1")))

    def test_filter_multiple(self):
        b = [
            binding.DictBinding("test-name-1", {"type": b"test-type-1", "provider": b"test-provider-1"}),
            binding.DictBinding("test-name-1", {"type": b"test-type-1", "provider": b"test-provider-2"}),
        ]

        self.assertEqual(2, len(bindings.filter(b, "test-type-1")))

    def test_filter_type_and_provider(self):
        b = [
            binding.DictBinding("test-name-1", {"type": b"test-type-1", "provider": b"test-provider-1"}),
            binding.DictBinding("test-name-1", {"type": b"test-type-1", "provider": b"test-provider-2"}),
        ]

        self.assertEqual(1, len(bindings.filter(b, "test-type-1", "test-provider-1")))

    def test_filter_provider(self):
        b = [
            binding.DictBinding("test-name-1", {"type": b"test-type-1", "provider": b"test-provider-1"}),
            binding.DictBinding("test-name-1", {"type": b"test-type-1", "provider": b"test-provider-2"}),
        ]

        self.assertEqual(1, len(bindings.filter(b, None, "test-provider-1")))


if __name__ == "__main__":
    unittest.main()
