"""
Reward Calculator for Alpha and MASA Token Staking Program

This module implements a reward calculation system for participants staking both Alpha and MASA tokens.
The rewards are distributed from a fixed pool of MASA tokens based on:
- Amount of Alpha tokens staked with time-based multipliers (earlier participants get higher weights)
- Amount of MASA tokens staked with duration-based multipliers
- Relative share of total staking pool weight

Program Rules:
- Program runs for 120 days from launch date
- Participants can join at any point during the program
- Alpha staking weight decreases linearly from 1.0 (day 0) to 0.25 (day 120)
- MASA staking periods are fixed: 3, 6, 9, or 12 months from join date
- Minimum MASA stake duration is 90 days
- Each participant is identified by their unique Bittensor hotkey and EVM ECDSA public key

The total reward pool consists of 15M MASA tokens that are distributed proportionally to participants
based on their staking positions and respective multipliers.

Classes:
    ParticipantPosition: Data class representing a participant's staking position
    RewardCalculator: Main class handling reward calculations and participant management

Example:
    launch_date = date(2024, 1, 1)
    calculator = RewardCalculator(launch_date)
    position = ParticipantPosition(
        hotkey="5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
        evm_address="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        alpha_staked=Decimal('1000'),
        masa_staked=Decimal('10000'), 
        masa_stake_months=6,
        join_date=date(2024, 1, 1)
    )
    calculator.add_participant(position)
    results = calculator.calculate_all_rewards()
"""

from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from datetime import datetime, date, timedelta

@dataclass
class ParticipantPosition:
    hotkey: str          # Bittensor hotkey as unique identifier
    evm_address: str     # EVM ECDSA public key
    alpha_staked: Decimal  # Amount of alpha tokens staked
    masa_staked: Decimal   # Amount of MASA tokens staked
    masa_stake_months: int # Duration of MASA stake in months
    join_date: date       # Date the participant joined the program

class RewardCalculator:
    # Constants
    TOTAL_REWARD_POOL = Decimal('15000000')  # 15M MASA tokens
    MAX_ALPHA_STAKE_DAYS = 120
    MIN_MASA_STAKE_DAYS = 90
    VALID_MASA_STAKE_MONTHS = [3, 6, 9, 12]
    
    def __init__(self, launch_date: date):
        self.participants = {}  # Changed to dict with hotkey as key
        self.launch_date = launch_date
        self.program_end_date = self._calculate_end_date(launch_date)
    
    def _calculate_end_date(self, launch_date: date) -> date:
        """Calculate program end date (launch date + 120 days)"""
        return launch_date + timedelta(days=self.MAX_ALPHA_STAKE_DAYS)
    
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
        self.participants[position.hotkey] = position

    def calculate_individual_weights(self, position: ParticipantPosition) -> Optional[dict]:
        """Calculate raw weights for a single participant"""
        if position.join_date < self.launch_date or position.join_date > self.program_end_date:
            return None
            
        if position.masa_stake_months not in self.VALID_MASA_STAKE_MONTHS:
            return None

        # Calculate days since program launch
        days_since_launch = (position.join_date - self.launch_date).days
        
        # Calculate time-based multiplier for Alpha staking
        # Those joining on launch date get full weight (1.0), decreasing linearly to 0.25 for those joining on day 120
        alpha_time_multiplier = Decimal('1.0') - (Decimal(str(days_since_launch)) / self.MAX_ALPHA_STAKE_DAYS * Decimal('0.75'))
        
        alpha_weight = position.alpha_staked * alpha_time_multiplier
        masa_weight = position.masa_staked * self.get_masa_stake_multiplier(position.masa_stake_months)
        total_weight = alpha_weight + masa_weight

        return {
            'total_weight': total_weight,
            'alpha_weight': alpha_weight,
            'masa_weight': masa_weight,
            'alpha_time_multiplier': alpha_time_multiplier,
            'masa_multiplier': self.get_masa_stake_multiplier(position.masa_stake_months),
            'days_since_launch': days_since_launch
        }

    def calculate_all_rewards(self) -> list[dict]:
        """Calculate normalized rewards for all participants"""
        total_pool_weight = Decimal('0')
        participant_weights = []

        # First pass: calculate individual weights and total pool weight
        for hotkey, position in self.participants.items():
            weights = self.calculate_individual_weights(position)
            if weights:
                total_pool_weight += weights['total_weight']
                participant_weights.append((hotkey, position, weights))

        # Second pass: calculate normalized rewards
        results = []
        for hotkey, position, weights in participant_weights:
            if total_pool_weight > 0:
                share_of_pool = weights['total_weight'] / total_pool_weight
                masa_reward = self.TOTAL_REWARD_POOL * share_of_pool
            else:
                share_of_pool = Decimal('0')
                masa_reward = Decimal('0')

            results.append({
                'hotkey': hotkey,
                'position': position,
                'total_weight': weights['total_weight'],
                'alpha_weight': weights['alpha_weight'],
                'masa_weight': weights['masa_weight'],
                'alpha_time_multiplier': weights['alpha_time_multiplier'],
                'masa_multiplier': weights['masa_multiplier'],
                'days_since_launch': weights['days_since_launch'],
                'share_of_pool': share_of_pool,
                'estimated_masa_reward': masa_reward
            })

        return results

def main():
    # Example with actual dates
    launch_date = date(2024, 1, 1)  # Program launches January 1st, 2024
    calculator = RewardCalculator(launch_date)
    
    # Example usage with multiple participants joining at different dates
    participants = [
        ParticipantPosition(
            hotkey="5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
            evm_address="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            alpha_staked=Decimal('1000'),
            masa_staked=Decimal('10000'),
            masa_stake_months=6,
            join_date=date(2024, 1, 1)  # Joined on launch day
        ),
        ParticipantPosition(
            hotkey="5FLSigC9HGRKVhB9FiEo4Y3koPsNmBmLJbpXg2mp1hXcS59Y",
            evm_address="0x8894e0a0c962cb723c1976a4421c95949be2d4e3",
            alpha_staked=Decimal('2000'),
            masa_staked=Decimal('20000'),
            masa_stake_months=9,
            join_date=date(2024, 2, 15)  # Joined mid-February
        )
    ]
    
    for position in participants:
        calculator.add_participant(position)
    
    results = calculator.calculate_all_rewards()
    
    print("\nReward Calculation Results:")
    for result in results:
        print("\nParticipant Position:")
        print(f"Hotkey: {result['hotkey']}")
        print(f"EVM Address: {result['position'].evm_address}")
        print(f"Join Date: {result['position'].join_date}")
        print(f"Days Since Launch: {result['days_since_launch']}")
        print(f"Alpha Staked: {result['position'].alpha_staked}")
        print(f"MASA Staked: {result['position'].masa_staked}")
        print(f"Alpha Time Multiplier: {result['alpha_time_multiplier']:.3f}")
        print(f"Share of Pool: {result['share_of_pool']:.2%}")
        print(f"Estimated MASA Reward: {result['estimated_masa_reward']:.2f}")

if __name__ == "__main__":
    main()
