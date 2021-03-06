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
from unittest import TestCase

from bindings.secret import is_valid_secret_key


class TestSecret(TestCase):
    def test__is_valid_secret_key__valid(self):
        valid = [
            "alpha",
            "BRAVO",
            "Charlie",
            "delta01",
            "echo-foxtrot",
            "golf_hotel",
            "india.juliet",
            ".kilo",
        ]

        for v in valid:
            self.assertTrue(is_valid_secret_key(v))

    def test__is_valid_secret_key__invalid(self):
        valid = [
            "lima^mike",
        ]

        for v in valid:
            self.assertFalse(is_valid_secret_key(v))


if __name__ == "__main__":
    unittest.main()
