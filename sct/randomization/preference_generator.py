"""
Preference generation strategies for simulating voter behavior.
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import random


class GenerationStrategy(ABC):
    """Abstract base class for preference generation strategies."""
    
    @abstractmethod
    def generate(self, num_agents: int, num_candidates: int, seed: Optional[int] = None) -> List[List[int]]:
        """
        Generate preferences for a number of agents.
        
        Args:
            num_agents: Number of agents to generate preferences for
            num_candidates: Number of candidates (rating for each)
            seed: Random seed for reproducibility
            
        Returns:
            List of preference lists, where each preference is a rating 0-4
            (0 = Strongly Disagree, 4 = Strongly Agree)
        """
        pass


class RandomStrategy(GenerationStrategy):
    """
    Completely random preference generation.
    Each agent gets random ratings for each candidate.
    """
    
    def generate(self, num_agents: int, num_candidates: int, seed: Optional[int] = None) -> List[List[int]]:
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        
        preferences = []
        for _ in range(num_agents):
            # Generate random ratings 0-4 for each candidate
            agent_prefs = [random.randint(0, 4) for _ in range(num_candidates)]
            preferences.append(agent_prefs)
        
        return preferences


class ClusteredStrategy(GenerationStrategy):
    """
    Clustered preference generation.
    Agents are grouped into clusters with similar preferences.
    Useful for simulating realistic voting populations.
    """
    
    def __init__(self, num_clusters: int = 3, noise_level: float = 0.3):
        """
        Args:
            num_clusters: Number of voter clusters/archetypes
            noise_level: How much individual preferences deviate from cluster center (0-1)
        """
        self.num_clusters = num_clusters
        self.noise_level = noise_level
    
    def generate(self, num_agents: int, num_candidates: int, seed: Optional[int] = None) -> List[List[int]]:
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        
        # Generate cluster centers (archetypes)
        cluster_centers = []
        for _ in range(self.num_clusters):
            center = [random.randint(0, 4) for _ in range(num_candidates)]
            cluster_centers.append(center)
        
        preferences = []
        for _ in range(num_agents):
            # Assign to a random cluster
            cluster_idx = random.randint(0, self.num_clusters - 1)
            center = cluster_centers[cluster_idx]
            
            # Add noise to cluster center
            agent_prefs = []
            for rating in center:
                noise = int(random.gauss(0, self.noise_level * 2))
                new_rating = max(0, min(4, rating + noise))
                agent_prefs.append(new_rating)
            
            preferences.append(agent_prefs)
        
        return preferences


class BiasedStrategy(GenerationStrategy):
    """
    Biased preference generation based on candidate archetypes.
    Simulates realistic city planning voter behavior.
    """
    
    # Predefined voter archetypes for city planning scenarios
    ARCHETYPES = {
        'conservative': [4, 2, 1, 0],      # Prefers business-as-usual
        'moderate': [2, 4, 3, 1],           # Prefers slow cars
        'progressive': [1, 2, 4, 3],        # Prefers few cars
        'radical': [0, 1, 3, 4],            # Prefers no cars
        'neutral': [2, 2, 2, 2],            # No strong preference
    }
    
    def __init__(self, archetype_weights: Optional[Dict[str, float]] = None, noise_level: float = 0.3):
        """
        Args:
            archetype_weights: Weight for each archetype (default: equal weights)
            noise_level: How much individual preferences deviate from archetype (0-1)
        """
        self.noise_level = noise_level
        if archetype_weights is None:
            self.archetype_weights = {k: 1.0 for k in self.ARCHETYPES}
        else:
            self.archetype_weights = archetype_weights
    
    def generate(self, num_agents: int, num_candidates: int, seed: Optional[int] = None) -> List[List[int]]:
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        
        # Normalize weights
        archetypes = list(self.ARCHETYPES.keys())
        weights = [self.archetype_weights.get(a, 1.0) for a in archetypes]
        total = sum(weights)
        weights = [w / total for w in weights]
        
        preferences = []
        for _ in range(num_agents):
            # Select archetype based on weights
            archetype = random.choices(archetypes, weights=weights)[0]
            base_prefs = self.ARCHETYPES[archetype][:num_candidates]
            
            # Add noise
            agent_prefs = []
            for rating in base_prefs:
                noise = int(random.gauss(0, self.noise_level * 2))
                new_rating = max(0, min(4, rating + noise))
                agent_prefs.append(new_rating)
            
            preferences.append(agent_prefs)
        
        return preferences


class PreferenceGenerator:
    """
    Main class for generating voter preferences.
    Supports multiple strategies and reproducibility via seeds.
    """
    
    STRATEGIES = {
        'random': RandomStrategy,
        'clustered': ClusteredStrategy,
        'biased': BiasedStrategy,
    }
    
    def __init__(self, strategy: str = 'random', **kwargs):
        """
        Args:
            strategy: Name of the generation strategy ('random', 'clustered', 'biased')
            **kwargs: Additional arguments passed to the strategy constructor
        """
        if strategy not in self.STRATEGIES:
            raise ValueError(f"Unknown strategy: {strategy}. Available: {list(self.STRATEGIES.keys())}")
        
        self.strategy = self.STRATEGIES[strategy](**kwargs)
    
    def generate(self, num_agents: int, num_candidates: int = 4, seed: Optional[int] = None) -> List[Dict]:
        """
        Generate preferences for a number of agents.
        
        Args:
            num_agents: Number of agents to generate
            num_candidates: Number of candidates
            seed: Random seed for reproducibility
            
        Returns:
            List of agent dictionaries with 'preferences' key
        """
        raw_prefs = self.strategy.generate(num_agents, num_candidates, seed)
        
        agents = []
        for i, prefs in enumerate(raw_prefs):
            agents.append({
                'id': f'agent_{i}',
                'preferences': prefs,
                'is_synthetic': True
            })
        
        return agents


# Utility function for API use
def generate_random_votes(num_agents: int, strategy: str = 'biased', seed: Optional[int] = None) -> List[Dict]:
    """
    Convenience function to generate random votes.
    
    Args:
        num_agents: Number of agents to generate
        strategy: Generation strategy ('random', 'clustered', 'biased')
        seed: Random seed for reproducibility
        
    Returns:
        List of agent preference dictionaries
    """
    generator = PreferenceGenerator(strategy=strategy)
    return generator.generate(num_agents, num_candidates=4, seed=seed)
