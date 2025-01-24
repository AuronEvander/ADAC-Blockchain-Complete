import React, { useState, useEffect } from 'react';
import { Lock, Unlock, ArrowRight, Clock } from 'lucide-react';

interface StakingProps {
  address: string;
  balance: string;
}

interface StakingInfo {
  stakedAmount: string;
  rewards: string;
  apr: number;
  lockPeriod: number;
  unstakeDate?: Date;
}

const Staking: React.FC<StakingProps> = ({ address, balance }) => {
  const [stakingAmount, setStakingAmount] = useState<string>('');
  const [stakingInfo, setStakingInfo] = useState<StakingInfo>({
    stakedAmount: '0',
    rewards: '0',
    apr: 12.5,
    lockPeriod: 30
  });
  const [isStaking, setIsStaking] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStakingInfo();
  }, [address]);

  const fetchStakingInfo = async () => {
    try {
      setStakingInfo({
        stakedAmount: '1000',
        rewards: '125',
        apr: 12.5,
        lockPeriod: 30,
        unstakeDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
      });
    } catch (err) {
      console.error('Error fetching staking info:', err);
      setError('Failed to load staking information');
    }
  };

  const handleStake = async () => {
    try {
      setIsStaking(true);
      setError(null);

      if (!stakingAmount || parseFloat(stakingAmount) <= 0) {
        throw new Error('Please enter a valid amount to stake');
      }

      if (parseFloat(stakingAmount) > parseFloat(balance)) {
        throw new Error('Insufficient balance for staking');
      }

      await new Promise(resolve => setTimeout(resolve, 2000));
      await fetchStakingInfo();
      setStakingAmount('');

    } catch (err) {
      console.error('Staking error:', err);
      setError(err instanceof Error ? err.message : 'Failed to stake tokens');
    } finally {
      setIsStaking(false);
    }
  };

  const handleUnstake = async () => {
    try {
      setIsStaking(true);
      setError(null);

      if (stakingInfo.unstakeDate && stakingInfo.unstakeDate > new Date()) {
        throw new Error('Tokens are still in lock period');
      }

      await new Promise(resolve => setTimeout(resolve, 2000));
      await fetchStakingInfo();

    } catch (err) {
      console.error('Unstaking error:', err);
      setError(err instanceof Error ? err.message : 'Failed to unstake tokens');
    } finally {
      setIsStaking(false);
    }
  };

  const calculateRewards = (amount: string): string => {
    const principal = parseFloat(amount) || 0;
    const annualReward = (principal * stakingInfo.apr) / 100;
    const monthlyReward = annualReward / 12;
    return monthlyReward.toFixed(2);
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm text-gray-600">Total Staked</p>
              <p className="text-2xl font-bold mt-1">{stakingInfo.stakedAmount} ADAC</p>
            </div>
            <Lock className="h-6 w-6 text-blue-500" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm text-gray-600">Earned Rewards</p>
              <p className="text-2xl font-bold mt-1">{stakingInfo.rewards} ADAC</p>
            </div>
            <ArrowRight className="h-6 w-6 text-green-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm text-gray-600">Lock Period</p>
              <p className="text-2xl font-bold mt-1">{stakingInfo.lockPeriod} Days</p>
            </div>
            <Clock className="h-6 w-6 text-purple-500" />
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-semibold mb-4">Stake ADAC</h3>
        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Amount to Stake
            </label>
            <div className="relative">
              <input
                type="number"
                value={stakingAmount}
                onChange={(e) => setStakingAmount(e.target.value)}
                className="w-full p-2 pr-16 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0.0"
                min="0"
                step="0.000001"
              />
              <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                <span className="text-gray-500">ADAC</span>
              </div>
            </div>
            {stakingAmount && (
              <p className="mt-1 text-sm text-gray-600">
                Estimated monthly reward: {calculateRewards(stakingAmount)} ADAC
              </p>
            )}
          </div>

          <div className="flex space-x-4">
            <button
              onClick={handleStake}
              disabled={isStaking}
              className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-blue-300 transition-colors"
            >
              <Lock className="h-4 w-4" />
              <span>{isStaking ? 'Staking...' : 'Stake'}</span>
            </button>

            <button
              onClick={handleUnstake}
              disabled={isStaking || !parseFloat(stakingInfo.stakedAmount)}
              className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 disabled:bg-purple-300 transition-colors"
            >
              <Unlock className="h-4 w-4" />
              <span>{isStaking ? 'Unstaking...' : 'Unstake'}</span>
            </button>
          </div>
        </div>

        <div className="mt-6 p-4 bg-gray-50 rounded">
          <h4 className="font-medium mb-2">Staking Information</h4>
          <ul className="space-y-2 text-sm text-gray-600">
            <li className="flex justify-between">
              <span>Annual Percentage Rate (APR)</span>
              <span className="font-medium">{stakingInfo.apr}%</span>
            </li>
            <li className="flex justify-between">
              <span>Lock Period</span>
              <span className="font-medium">{stakingInfo.lockPeriod} Days</span>
            </li>
            {stakingInfo.unstakeDate && (
              <li className="flex justify-between">
                <span>Available to Unstake</span>
                <span className="font-medium">
                  {stakingInfo.unstakeDate > new Date() 
                    ? stakingInfo.unstakeDate.toLocaleDateString() 
                    : 'Now'}
                </span>
              </li>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Staking;
