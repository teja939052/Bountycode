import { ReactComponent as StreakFlame } from './streak-flame.svg';
import { ReactComponent as BadgeBronze } from './badge-bronze.svg';
import { ReactComponent as BadgeSilver } from './badge-silver.svg';
import { ReactComponent as BadgeGold } from './badge-gold.svg';
import { ReactComponent as BadgePlatinum } from './badge-platinum.svg';
import { ReactComponent as ChestWood } from './chest-wood.svg';
import { ReactComponent as ChestSilver } from './chest-silver.svg';
import { ReactComponent as ChestGold } from './chest-gold.svg';
import { ReactComponent as ChestDiamond } from './chest-diamond.svg';
import { ReactComponent as JourneyHexDone } from './journey-hex-done.svg';
import { ReactComponent as JourneyHexActive } from './journey-hex-active.svg';
import { ReactComponent as JourneyHexLocked } from './journey-hex-locked.svg';
import { ReactComponent as XPCoin } from './xp-coin.svg';
import { ReactComponent as EnergyBolt } from './energy-bolt.svg';
import { ReactComponent as BugsyBadge } from './bugsy-badge.svg';

export { StreakFlame, BadgeBronze, BadgeSilver, BadgeGold, BadgePlatinum, ChestWood, ChestSilver, ChestGold, ChestDiamond, JourneyHexDone, JourneyHexActive, JourneyHexLocked, XPCoin, EnergyBolt, BugsyBadge };

export const GAMIFICATION_ICONS = {
  streak: StreakFlame,
  badge_bronze: BadgeBronze,
  badge_silver: BadgeSilver,
  badge_gold: BadgeGold,
  badge_platinum: BadgePlatinum,
  chest_wood: ChestWood,
  chest_silver: ChestSilver,
  chest_gold: ChestGold,
  chest_diamond: ChestDiamond,
  journey_done: JourneyHexDone,
  journey_active: JourneyHexActive,
  journey_locked: JourneyHexLocked,
  xp: XPCoin,
  energy: EnergyBolt,
  bugsy: BugsyBadge,
} as const;
