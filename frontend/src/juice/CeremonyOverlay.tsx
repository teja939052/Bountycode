import React from 'react';
import MysteryBoxCeremony from './MysteryBoxCeremony';
import LevelUpCeremony from './LevelUpCeremony';
import StreakCeremony from './StreakCeremony';
import BadgeCeremony from './BadgeCeremony';
import CardRevealCeremony from './CardRevealCeremony';

export default function CeremonyOverlay({ ceremonies, onDismiss, play }) {
  return ceremonies.map((ceremony) => {
    switch (ceremony.type) {
      case 'mysterybox':
        return (
          <MysteryBoxCeremony
            key={ceremony.id}
            reward={ceremony.data}
            onDismiss={() => onDismiss(ceremony.id)}
            play={play}
          />
        );

      case 'levelup':
        return (
          <LevelUpCeremony
            key={ceremony.id}
            level={ceremony.data.level}
            onDismiss={() => onDismiss(ceremony.id)}
          />
        );

      case 'streak':
        return (
          <StreakCeremony
            key={ceremony.id}
            days={ceremony.data.days}
            onDismiss={() => onDismiss(ceremony.id)}
          />
        );

      case 'badge':
        return (
          <BadgeCeremony
            key={ceremony.id}
            badge={ceremony.data}
            onDismiss={() => onDismiss(ceremony.id)}
          />
        );

      case 'card':
        return (
          <CardRevealCeremony
            key={ceremony.id}
            card={ceremony.data}
            onDismiss={() => onDismiss(ceremony.id)}
          />
        );

      default:
        return null;
    }
  });
}
