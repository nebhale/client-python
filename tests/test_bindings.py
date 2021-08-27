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
    def test__cached(self):
        b = bindings.cached([
            binding.DictBinding("test-name-1", {}),
            binding.DictBinding("test-name-2", {}),
        ])

        for b in b:
            self.assertIs(binding.CacheBinding, type(b))

    def test__from__missing(self):
        self.assertEqual(0, len(bindings.from_path("missing")))

    def test__from__file(self):
        self.assertEqual(0, len(bindings.from_path("tests/testdata/additional-file")))

    def test__from__exists(self):
        self.assertEqual(3, len(bindings.from_path("tests/testdata")))

    def test__from_service_binding_root__unset(self):
        self.assertEqual(0, len(bindings.from_service_binding_root()))

    def test__from_service_binding_root__set(self):
        old = os.getenv("SERVICE_BINDING_ROOT")
        os.environ["SERVICE_BINDING_ROOT"] = path.join("tests", "testdata")

        try:
            self.assertEqual(3, len(bindings.from_service_binding_root()))
        finally:
            if old is None:
                del os.environ["SERVICE_BINDING_ROOT"]
            else:
                os.environ["SERVICE_BINDING_ROOT"] = old

    def test__find__missing(self):
        b = [
            binding.DictBinding("test-name-1", {}),
        ]

        self.assertIsNone(bindings.find(b, "test-name-2"))

    def test_find_valid(self):
        b = [
            binding.DictBinding("test-name-1", {}),
            binding.DictBinding("test-name-2", {}),
        ]

        self.assertEqual("test-name-1", bindings.find(b, "test-name-1").get_name())

    def test_filter_none(self):
        b = [
            binding.DictBinding("test-name-1", {
                "type": b"test-type-1",
                "provider": b"test-provider-1",
            }),
            binding.DictBinding("test-name-2", {
                "type": b"test-type-1",
                "provider": b"test-provider-2",
            }),
            binding.DictBinding("test-name-3", {
                "type": b"test-type-2",
                "provider": b"test-provider-2",
            }),
            binding.DictBinding("test-name-4", {
                "type": b"test-type-2",
            }),
        ]

        self.assertEqual(4, len(bindings.filter(b)))

    def test_filter_type(self):
        b = [
            binding.DictBinding("test-name-1", {
                "type": b"test-type-1",
                "provider": b"test-provider-1",
            }),
            binding.DictBinding("test-name-2", {
                "type": b"test-type-1",
                "provider": b"test-provider-2",
            }),
            binding.DictBinding("test-name-3", {
                "type": b"test-type-2",
                "provider": b"test-provider-2",
            }),
            binding.DictBinding("test-name-4", {
                "type": b"test-type-2",
            }),
        ]

        self.assertEqual(2, len(bindings.filter(b, "test-type-1")))

    def test_filter_provider(self):
        b = [
            binding.DictBinding("test-name-1", {
                "type": b"test-type-1",
                "provider": b"test-provider-1",
            }),
            binding.DictBinding("test-name-2", {
                "type": b"test-type-1",
                "provider": b"test-provider-2",
            }),
            binding.DictBinding("test-name-3", {
                "type": b"test-type-2",
                "provider": b"test-provider-2",
            }),
            binding.DictBinding("test-name-4", {
                "type": b"test-type-2",
            }),
        ]

        self.assertEqual(2, len(bindings.filter(b, None, "test-provider-2")))

    def test_filter_type_and_provider(self):
        b = [
            binding.DictBinding("test-name-1", {
                "type": b"test-type-1",
                "provider": b"test-provider-1",
            }),
            binding.DictBinding("test-name-2", {
                "type": b"test-type-1",
                "provider": b"test-provider-2",
            }),
            binding.DictBinding("test-name-3", {
                "type": b"test-type-2",
                "provider": b"test-provider-2",
            }),
            binding.DictBinding("test-name-4", {
                "type": b"test-type-2",
            }),
        ]

        self.assertEqual(1, len(bindings.filter(b, "test-type-1", "test-provider-1")))


if __name__ == "__main__":
    unittest.main()
