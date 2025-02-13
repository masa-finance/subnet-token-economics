"""
Reward Calculator for Alpha and MASA Token Staking Program

This module implements a reward calculation system for participants staking both Alpha and MASA tokens.
The rewards are distributed from a fixed pool of MASA tokens based on:
- Amount of Alpha tokens staked (minimum 120 day stake period required)
- Amount of MASA tokens staked with duration-based multipliers
- Relative share of total staking pool weight

The total reward pool consists of 15M MASA tokens that are distributed proportionally to participants
based on their staking positions and duration multipliers.

Classes:
    ParticipantPosition: Data class representing a participant's staking position
    RewardCalculator: Main class handling reward calculations and participant management

Example:
    calculator = RewardCalculator()
    position = ParticipantPosition(
        alpha_staked=Decimal('1000'),
        masa_staked=Decimal('10000'), 
        alpha_stake_days=120,
        masa_stake_months=6
    )
    calculator.add_participant(position)
    results = calculator.calculate_all_rewards()
"""

from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class ParticipantPosition:
    alpha_staked: Decimal  # Amount of alpha tokens staked
    masa_staked: Decimal   # Amount of MASA tokens staked
    alpha_stake_days: int  # Duration of alpha stake in days
    masa_stake_months: int # Duration of MASA stake in months

class RewardCalculator:
    # Constants
    TOTAL_REWARD_POOL = Decimal('15000000')  # 15M MASA tokens
    MIN_ALPHA_STAKE_DAYS = 120
    VALID_MASA_STAKE_MONTHS = [3, 6, 9, 12]
    
    def __init__(self):
        self.participants = []

    @staticmethod
    def get_masa_stake_multiplier(months: int) -> Decimal:
        """Calculate multiplier based on MASA stake duration"""
        multipliers = {
            3: Decimal('1.0'),   # 15% APY
            6: Decimal('1.2'),   # 20% APY
            9: Decimal('1.5'),   # 25% APY
            12: Decimal('1.5')   # 25% APY
        }
        return multipliers.get(months, Decimal('0'))

    def add_participant(self, position: ParticipantPosition):
        """Add a participant to the reward calculation pool"""
        self.participants.append(position)

    def calculate_individual_weights(self, position: ParticipantPosition) -> Optional[dict]:
        """Calculate raw weights for a single participant"""
        if position.alpha_stake_days < self.MIN_ALPHA_STAKE_DAYS:
            return None
        
        if position.masa_stake_months not in self.VALID_MASA_STAKE_MONTHS:
            return None

        alpha_weight = position.alpha_staked
        masa_weight = position.masa_staked * self.get_masa_stake_multiplier(position.masa_stake_months)
        total_weight = alpha_weight + masa_weight

        return {
            'total_weight': total_weight,
            'alpha_weight': alpha_weight,
            'masa_weight': masa_weight,
            'masa_multiplier': self.get_masa_stake_multiplier(position.masa_stake_months)
        }

    def calculate_all_rewards(self) -> list[dict]:
        """Calculate normalized rewards for all participants"""
        total_pool_weight = Decimal('0')
        participant_weights = []

        # First pass: calculate individual weights and total pool weight
        for position in self.participants:
            weights = self.calculate_individual_weights(position)
            if weights:
                total_pool_weight += weights['total_weight']
                participant_weights.append((position, weights))

        # Second pass: calculate normalized rewards
        results = []
        for position, weights in participant_weights:
            if total_pool_weight > 0:
                share_of_pool = weights['total_weight'] / total_pool_weight
                masa_reward = self.TOTAL_REWARD_POOL * share_of_pool
            else:
                share_of_pool = Decimal('0')
                masa_reward = Decimal('0')

            results.append({
                'position': position,
                'total_weight': weights['total_weight'],
                'alpha_weight': weights['alpha_weight'],
                'masa_weight': weights['masa_weight'],
                'masa_multiplier': weights['masa_multiplier'],
                'share_of_pool': share_of_pool,
                'estimated_masa_reward': masa_reward
            })

        return results

def main():
    calculator = RewardCalculator()
    
    # Example usage with multiple participants
    participants = [
        ParticipantPosition(
            alpha_staked=Decimal('1000'),
            masa_staked=Decimal('10000'),
            alpha_stake_days=120,
            masa_stake_months=6
        ),
        ParticipantPosition(
            alpha_staked=Decimal('2000'),
            masa_staked=Decimal('20000'),
            alpha_stake_days=120,
            masa_stake_months=9
        ),
        ParticipantPosition(
            alpha_staked=Decimal('500'),
            masa_staked=Decimal('5000'),
            alpha_stake_days=120,
            masa_stake_months=3
        )
    ]
    
    for position in participants:
        calculator.add_participant(position)
    
    results = calculator.calculate_all_rewards()
    
    print("\nReward Calculation Results:")
    for result in results:
        print("\nParticipant Position:")
        print(f"Alpha Staked: {result['position'].alpha_staked}")
        print(f"MASA Staked: {result['position'].masa_staked}")
        print(f"Share of Pool: {result['share_of_pool']:.2%}")
        print(f"Estimated MASA Reward: {result['estimated_masa_reward']:.2f}")

if __name__ == "__main__":
    main()
