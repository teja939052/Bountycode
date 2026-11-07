import StreakFlameUrl from "./streak-flame.svg";
import BadgeBronzeUrl from "./badge-bronze.svg";
import BadgeSilverUrl from "./badge-silver.svg";
import BadgeGoldUrl from "./badge-gold.svg";
import BadgePlatinumUrl from "./badge-platinum.svg";
import ChestWoodUrl from "./chest-wood.svg";
import ChestSilverUrl from "./chest-silver.svg";
import ChestGoldUrl from "./chest-gold.svg";
import ChestDiamondUrl from "./chest-diamond.svg";
import JourneyHexDoneUrl from "./journey-hex-done.svg";
import JourneyHexActiveUrl from "./journey-hex-active.svg";
import JourneyHexLockedUrl from "./journey-hex-locked.svg";
import XPCoinUrl from "./xp-coin.svg";
import EnergyBoltUrl from "./energy-bolt.svg";
import BugsyBadgeUrl from "./bugsy-badge.svg";

const makeIcon = (src: string, alt: string) => (props: { className?: string }) => (
  <img src={src} alt={alt} className={props.className} />
);

const StreakFlame = makeIcon(StreakFlameUrl as unknown as string, "streak flame");
const BadgeBronze = makeIcon(BadgeBronzeUrl as unknown as string, "badge bronze");
const BadgeSilver = makeIcon(BadgeSilverUrl as unknown as string, "badge silver");
const BadgeGold = makeIcon(BadgeGoldUrl as unknown as string, "badge gold");
const BadgePlatinum = makeIcon(
  BadgePlatinumUrl as unknown as string,
  "badge platinum"
);
const ChestWood = makeIcon(ChestWoodUrl as unknown as string, "chest wood");
const ChestSilver = makeIcon(
  ChestSilverUrl as unknown as string,
  "chest silver"
);
const ChestGold = makeIcon(ChestGoldUrl as unknown as string, "chest gold");
const ChestDiamond = makeIcon(
  ChestDiamondUrl as unknown as string,
  "chest diamond"
);
const JourneyHexDone = makeIcon(
  JourneyHexDoneUrl as unknown as string,
  "journey done"
);
const JourneyHexActive = makeIcon(
  JourneyHexActiveUrl as unknown as string,
  "journey active"
);
const JourneyHexLocked = makeIcon(
  JourneyHexLockedUrl as unknown as string,
  "journey locked"
);
const XPCoin = makeIcon(XPCoinUrl as unknown as string, "xp coin");
const EnergyBolt = makeIcon(
  EnergyBoltUrl as unknown as string,
  "energy bolt"
);
const BugsyBadge = makeIcon(
  BugsyBadgeUrl as unknown as string,
  "bugsy badge"
);

export {
  StreakFlame,
  BadgeBronze,
  BadgeSilver,
  BadgeGold,
  BadgePlatinum,
  ChestWood,
  ChestSilver,
  ChestGold,
  ChestDiamond,
  JourneyHexDone,
  JourneyHexActive,
  JourneyHexLocked,
  XPCoin,
  EnergyBolt,
  BugsyBadge,
};

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
