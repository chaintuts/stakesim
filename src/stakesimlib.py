# This file contains code for a simple proof-of-stake simulation
#
# Author: Josh McIntyre
#
import os

class StakeNode:

    # Some simple constants
    HASH_MOD = 256
    HASH_XOR = 255
    MIN_STAKE = 32
    BYTE_ORDER = 'big'

    # Initialization
    def __init__(self, node_id, staked):

        self.node_id = node_id
        self.staked = staked
        
        self.entropy = self._generate_entropy()

    # Generate entropy for the node
    def _generate_entropy(self):
    
        return int.from_bytes(os.urandom(1), self.BYTE_ORDER)

    # Hashing method for the demo
    # Return a really simple 8 bit hash
    # This is for educational purposes, so we don't need a
    # cryptographically secure hash, we just need one that works
    # to "shuffle" the data appearance wise
    @staticmethod
    def hash_8bit(data):

        hash8 = (data ^ StakeNode.HASH_XOR) % StakeNode.HASH_MOD

        return hash8
    
    # Commit random bytes to the blockchain
    # Hashes the internal random number and returns the hash
    def commit(self):
    
        entropy_hash8 = self.hash_8bit(self.entropy)
        
        return entropy_hash8
    
    # Reveal the actual random bytes
    # Other nodes will verify that these bytes hash
    # to the initial committed value
    def reveal(self):
    
        return self.entropy

    # Validate a node's committed and revealed entropy
    # The hash must match for a valid commit -> reveal to return True, otherwise False
    def validate(self, committed, revealed):
    
        return (committed == self.hash_8bit(revealed))

    # Conduct the entropy collection and selection of winning nodes
    # Returns a tuple with the combined entropy
    def pick_node(self, peers):
    
        combined_entropy = self._combine_entropy(peers)
        selection = self._weighted_selection(combined_entropy, peers)
        
        return selection
        
    # Get the combined entropy from all peers
    def combine_entropy(self, peers):
    
        return self._combine_entropy(peers)

    # Get the combined entropy of all peers
    # Use a bitwise XOR to do the combination
    def _combine_entropy(self, peers):
    
        # Start with our own entropy
        # Combine with each peer by doing a bitwise XOR
        # Order of the peers does not matter
        combined_entropy = self.entropy
        for peer in peers:
            combined_entropy = combined_entropy ^ peer.entropy
            
        return combined_entropy

    # Implement a weighted selection for nodes using the combined entropy
    # from all the nodes and weights based on the amount staked
    def _weighted_selection(self, combined_entropy, peers):

        # Compile a list of all nodes, both the manager node and peers
        nodes = [self] + peers

        # First, calculate the total amount staked
        total_staked = self.staked
        for peer in peers:
            total_staked += peer.staked
        
        # Calculate percentage of total stake for each node
        percentages_staked = [ (node.staked / total_staked) for node in nodes ]

        # The final weighted selection will be done with an n bit number
        # The default for this simulation is 8 bit, which means the entropy will be
        # a number between 0-255 (256 total possible numbers)
        # Calculate the ratio of each node's stake based to the total for the weighted selection
        # Due to rounding, we may need to expand or trim the final list to fit N bits
        # This may slightly alter the exact weights but is sufficient for our mock POS simulation
        ratio_staked = [ round(self.HASH_MOD * pct_staked) for pct_staked in percentages_staked ]
        if len(ratio_staked) > self.HASH_MOD:
            ratio_staked = ratio_staked[:self.HASH_MOD]
        if len(ratio_staked) < self.HASH_MOD:
            # Favor the highest staked node, and add a few until we hit the desired N bit total
            last = ratio_staked[-1]
            total = sum(ratio_staked)
            diff = self.HASH_MOD - total
            ratio_staked[-1] += diff
        
        # Construct a list for probability distribution
        # This list will be the size of N bit numbers
        # So we can simply selected the chosen node index using our entropy
        distribution = []
        for i in range(0, len(ratio_staked)):
            distribution += [nodes[i].node_id] * ratio_staked[i]

        # Choose the node that will validate the block using the combined entropy
        return distribution[combined_entropy]

# Define a class for handling stake simulation
# Normally, this would be done peer-to-peer on a per-node basis
# (everyone validates everyone else's data)
# For this simple educational demo, have a Manager act as one node
class StakeSimNode(StakeNode):

    # Initialization    
    def __init__(self, num_nodes):
    
        # Give this manager node an index of 0, and the rest of
        # the nodes incremented indexes
        super().__init__(0, self._calc_stake(0))
        self.nodes = [ StakeNode(i, self._calc_stake(i)) for i in range(1, num_nodes) ]

    # Calculate the stake amount given a node index/id
    def _calc_stake(self, i):
        
        if i == 0:
            return self.MIN_STAKE
        return self.MIN_STAKE * (i+1)

    # Conduct the simulation
    def simulate(self):
    
        node_ids = [ self.node_id] + [ node.node_id for node in self.nodes ]
        staked = [ self.staked] + [ node.staked for node in self.nodes ]
        committed = [ self.commit()] + [ node.commit() for node in self.nodes ]
        revealed = [ self.reveal()] + [ node.reveal() for node in self.nodes ]
        validated = [ self.validate(committed, revealed) for committed, revealed in zip(committed, revealed) ]
        weights = [ self.staked / sum(staked) ] + [ node.staked / sum(staked) for node in self.nodes ]
        

        combined_entropy = self.combine_entropy(self.nodes)
        selected_node = self.pick_node(self.nodes)

        result = Result(selected_node,
                        combined_entropy,
                        node_ids,
                        staked,
                        committed, 
                        revealed,
                        validated,
                        weights)

        return result

class Result:

    def __init__(self, selected_node, combined_entropy, node_ids, staked, committed, revealed, validated, weights):

        # The selected node id and the combined entropy used for selection
        self.selected_node = selected_node
        self.combined_entropy = combined_entropy
        
        # Parallel lists for node ids, amount staked, committed hashes, revealed entropy
        self.node_ids = node_ids
        self.staked = staked
        self.committed = committed
        self.revealed = revealed
        self.validated = validated
        self.weights = weights
