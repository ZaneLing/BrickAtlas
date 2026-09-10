export type AssemblyDifficulty = 1 | 2 | 3 | 4 | 5;

const difficulties: Record<string, AssemblyDifficulty> = {
  '31028-sailboat': 1,
  '31027-kart': 1,
  '31028': 1,
  '31027': 2,
  '10156': 2,
  '10014': 2,
  '10036': 2,
  '5867': 3,
  '31009': 3,
  '10128': 3,
  '10159': 4,
  '10001': 4,
  '10213': 5,
  '10220': 5,
  '10214': 5,
};

export function assemblyDifficulty(modelId: string): AssemblyDifficulty {
  return difficulties[modelId] ?? 3;
}

export function difficultyLabel(
  difficulty: AssemblyDifficulty,
  locale: 'zh' | 'en',
) {
  const zh = ['入门', '简单', '进阶', '困难', '大师'];
  const en = ['Starter', 'Easy', 'Intermediate', 'Hard', 'Master'];
  return (locale === 'zh' ? zh : en)[difficulty - 1];
}
