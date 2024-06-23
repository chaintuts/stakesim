# This file contains unit tests for StakeSim library functionality
#
# Author: Josh McIntyre
#
import hashlib
import unittest
from unittest.mock import patch, Mock

import stakesimlib

class TestStakeSim(unittest.TestCase):

    @patch("stakesimlib.StakeNode._generate_entropy", side_effect=[16, 64, 128])
    def test_generate_address_privkey_btc(self, mock_generate_entropy):

        ssn = stakesimlib.StakeSimNode(3)
        result = ssn.simulate()

        assert result.committed == [ 239, 191, 127 ]
        assert result.revealed == [ 16, 64, 128 ]
        assert result.validated == [ True, True, True ]
        
        assert result.staked == [ 32, 64, 96 ]
        
        assert result.combined_entropy == 208
        assert result.selected_node == 2
