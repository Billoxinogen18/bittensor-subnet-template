# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from dataclasses import dataclass
import typing
import bittensor as bt


@dataclass
class HashWork(bt.Synapse):
    """Synapse used by Zeus-hash subnet.

    Validator sends a mining *challenge* consisting of an 80-byte block header
    (pre-hash, little-endian hex) plus the target (32-byte little-endian hex).
    Miner tries to find a nonce that makes scrypt(header_with_nonce) ≤ target.

    Attributes
    ----------
    header_hex : str
        Full 80-byte block header in hexadecimal **without** the nonce updated.
    target_hex : str
        32-byte target threshold in hexadecimal (little-endian).
    nonce : typing.Optional[int]
        32-bit nonce that solves the work (filled by miner).
    success : typing.Optional[bool]
        True if miner claims header+nonce meets the target, else False.
    latency_ms : typing.Optional[float]
        Round-trip latency measured by miner (optional, for telemetry).
    """

    header_hex: str
    target_hex: str

    # Miner-side outputs
    nonce: typing.Optional[int] = None
    success: typing.Optional[bool] = None
    latency_ms: typing.Optional[float] = None

    def deserialize(self):
        """When the dendrite receives a response, return simple bool of success."""
        return bool(self.success)

# Backwards-compat alias so other template code doesn’t break
Work = HashWork
