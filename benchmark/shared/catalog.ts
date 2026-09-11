export const CATALOG = {
  '3005': { name: 'Brick 1 x 1', width: 1, depth: 1, height: 3 },
  '3004': { name: 'Brick 1 x 2', width: 2, depth: 1, height: 3 },
  '3010': { name: 'Brick 1 x 4', width: 4, depth: 1, height: 3 },
  '3009': { name: 'Brick 1 x 6', width: 6, depth: 1, height: 3 },
  '3020': { name: 'Plate 2 x 4', width: 4, depth: 2, height: 1 },
  '3958': { name: 'Plate 6 x 6', width: 6, depth: 6, height: 1 },
} as const;

export const COLORS: Record<string, string> = {
  gray: '#9ca5aa',
  yellow: '#f2cd37',
  red: '#c91a09',
  blue: '#0055bf',
  green: '#237841',
  white: '#f4f4f4',
};

export const RULES = `CARE-mini v1. Grid X/Z are studs (8 mm), Y is plate layers (3.2 mm).
Positions describe the minimum X/Z corner and bottom Y of each part's rectangular body.
turn=0 or 2: catalog width runs along X. turn=1 or 3: width runs along Z.
All parts have top studs. A placement must be on the ground or overlap at least one stud
of a part directly below. Bodies cannot overlap. Detach lifts vertically (+Y); an overhead
part blocks removal, and remaining parts must stay supported. These are discrete rules,
NOT a force, clutch-strength, robot-reachability or stability simulation.
There is no target snapping, no official-step restriction and no correctness feedback.
The base is also a part. Coordinates may range from -8 to 16; Y ranges from 0 to 16.`;
