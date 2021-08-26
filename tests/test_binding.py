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

import unittest
from os import path
from typing import Optional

from bindings import binding, bindings


class TestBinding(unittest.TestCase):
    def test_get(self):
        b = binding.DictBinding("test-name", {"test-secret-key": b"test-secret-value\n"})

        self.assertEqual("test-secret-value", b.get("test-secret-key"))

    def test_get_provider_invalid_key(self):
        b = binding.DictBinding("test-name", {})

        self.assertIsNone(b.get_provider())

    def test_get_provider_valid_key(self):
        b = binding.DictBinding("test-name", {"provider": b"test-provider-1"})

        self.assertEqual("test-provider-1", b.get_provider())

    def test_get_type_invalid_binding(self):
        b = binding.DictBinding("test-name", {})

        self.assertRaises(ValueError, lambda: b.get_type())

    def test_get_type_valid_binding(self):
        b = binding.DictBinding("test-name", {"type": b"test-type-1"})

        self.assertEqual("test-type-1", b.get_type())

    def test_CacheBinding_uncached(self):
        s = StubBinding()
        b = bindings.CacheBinding(s)

        self.assertIsNotNone(b.get_as_bytes("test-key"))
        self.assertEqual(1, s.get_as_bytes_count)

    def test_CacheBinding_missing(self):
        s = StubBinding()
        b = bindings.CacheBinding(s)

        self.assertIsNone(b.get_as_bytes("test-unknown-key"))
        self.assertIsNone(b.get_as_bytes("test-unknown-key"))
        self.assertEqual(2, s.get_as_bytes_count)

    def test_CacheBinding_cached(self):
        s = StubBinding()
        b = bindings.CacheBinding(s)

        self.assertIsNotNone(b.get_as_bytes("test-key"))
        self.assertIsNotNone(b.get_as_bytes("test-key"))
        self.assertEqual(1, s.get_as_bytes_count)

    def test_CacheBinding_get_name(self):
        s = StubBinding()
        b = bindings.CacheBinding(s)

        self.assertEqual("test-name", b.get_name())
        self.assertEqual(1, s.get_name_count)

    def test_ConfigTreeBinding_get_as_bytes_missing_key(self):
        b = binding.ConfigTreeBinding(path.join("tests", "testdata", "test-k8s"))

        self.assertIsNone(b.get_as_bytes("test-missing-key"))

    def test_ConfigTreeBinding_get_as_bytes_directory(self):
        b = binding.ConfigTreeBinding(path.join("tests", "testdata", "test-k8s"))

        self.assertIsNone(b.get_as_bytes(".hidden-data"))

    def test_ConfigTreeBinding_get_as_bytes_invalid_key(self):
        b = binding.ConfigTreeBinding(path.join("tests", "testdata", "test-k8s"))

        self.assertIsNone(b.get_as_bytes("test^secret^key"))

    def test_ConfigTreeBinding_get_as_bytes_valid_key(self):
        b = binding.ConfigTreeBinding(path.join("tests", "testdata", "test-k8s"))

        self.assertEqual(b"test-secret-value\n", b.get_as_bytes("test-secret-key"))

    def test_ConfigTreeBinding_get_name(self):
        b = binding.ConfigTreeBinding(path.join("tests", "testdata", "test-k8s"))

        self.assertEqual("test-k8s", b.get_name())

    def test_DictBinding_get_as_bytes_missing_key(self):
        b = binding.DictBinding("test-name", {"test-secret-key": b"test-secret-value\n"})

        self.assertIsNone(b.get_as_bytes("test-missing-key"))

    def test_DictBinding_get_as_bytes_invalid_key(self):
        b = binding.DictBinding("test-name", {"test-secret-key": b"test-secret-value\n"})

        self.assertIsNone(b.get_as_bytes("test^secret^key"))

    def test_DictBinding_get_as_bytes_valid_key(self):
        b = binding.DictBinding("test-name", {"test-secret-key": b"test-secret-value\n"})

        self.assertEqual(b"test-secret-value\n", b.get_as_bytes("test-secret-key"))

    def test_DictBinding_get_name(self):
        b = binding.DictBinding("test-name", {})

        self.assertEqual("test-name", b.get_name())


class StubBinding(binding.Binding):
    get_as_bytes_count = 0
    get_name_count = 0

    def get_as_bytes(self, key: str) -> Optional[bytes]:
        self.get_as_bytes_count += 1

        if key == "test-key":
            return bytes()

        return None

    def get_name(self) -> str:
        self.get_name_count += 1
        return "test-name"


if __name__ == "__main__":
    unittest.main()
