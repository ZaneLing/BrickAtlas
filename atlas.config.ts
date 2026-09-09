export const atlasConfig = {
  id: '5867',
  title: 'Super Speedster',
  subtitle: '超级跑车',
  theme: 'Creator 3-in-1',
  year: 2010,
  sourceFile: 'assets-source/set-original/5867-1.mpd',
  sourceUrl: 'https://library.ldraw.org/omr/sets/1431',
  license: 'CC BY 2.0',
  licenseUrl: 'https://creativecommons.org/licenses/by/2.0/',
  author: 'Takeshi Takahashi [RainbowDolphin]',
  classificationFile: 'assets-source/classification.json',
  notes: [
    '以 OMR 5867-1.mpd 为完整性基准，不包含备用零件及另外两种搭建形态。',
    '源模型没有 STEP 元命令，装配步骤未提供。',
    '结构分类是编辑规则，不是官方装配分组；保留所有原始子模型。',
    '无缺失依赖、无替代件、无减面；未进行实物套装逐件盘点。',
  ],
};

export interface ModelConfig {
  id: string;
  setNumber: string;
  title: string;
  subtitle: string;
  theme: string;
  category: string;
  year: number;
  sourceFile: string;
  sourceUrl: string;
  downloadUrl?: string;
  sourceHash: string;
  license: string;
  licenseUrl: string;
  author: string;
  notes: string[];
  classificationFile?: string;
}

const creator = { theme: 'Creator 3-in-1', license: 'CC BY 2.0', licenseUrl: atlasConfig.licenseUrl };
const editorialNotes = ['源文件没有 STEP，工作台提供结构演示顺序，未经实物拼搭验证，不等同于官方说明书。'];
export const modelCatalog: ModelConfig[] = [
  { ...atlasConfig, setNumber: '5867', category: '车辆', downloadUrl: 'https://library.ldraw.org/library/omr/5867-1.mpd', sourceHash: '48082e34b40a6ed5bbf2edabe9d0deb313fac7c20b1128970ba73f722b70216d' },
  { ...creator, id: '31027', setNumber: '31027', title: 'Blue Racer', subtitle: '蓝色赛车', category: '车辆', year: 2015,
    sourceFile: 'assets-source/set-original/31027-1.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/223', downloadUrl: 'https://library.ldraw.org/library/omr/31027-1.mpd',
    sourceHash: '1f1975602ce9a63f2954c8da97f4fc13a473f709afa4a25b1022add33b55cfd1', author: 'Merlijn Wissink [legolijntje]', notes: editorialNotes },
  { ...creator, id: '31027-kart', setNumber: '31027', title: 'Kart', subtitle: '卡丁车 · 替代拼搭', category: '车辆', year: 2015,
    sourceFile: 'assets-source/set-original/31027-1_Kart.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/223', downloadUrl: 'https://library.ldraw.org/library/omr/31027-1_Kart.mpd',
    sourceHash: '743a56a012096a40e6b0aeb862b1e9e964d57824f460f9e9935c1bc82ebc467a', author: 'Merlijn Wissink [legolijntje]', notes: editorialNotes },
  { ...creator, id: '31028', setNumber: '31028', title: 'Sea Plane', subtitle: '水上飞机', category: '飞行', year: 2015,
    sourceFile: 'assets-source/set-original/31028-1.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/259', downloadUrl: 'https://library.ldraw.org/library/omr/31028-1.mpd',
    sourceHash: 'd2619a85e973430a1b256d607fe8e44a865beb05ef63ac8028a5109c228ee97c', author: 'Merlijn Wissink [legolijntje]', notes: editorialNotes },
  { ...creator, id: '31028-sailboat', setNumber: '31028', title: 'Sailboat', subtitle: '帆船 · 替代拼搭', category: '船舶', year: 2015,
    sourceFile: 'assets-source/set-original/31028-1_Sailboat.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/259', downloadUrl: 'https://library.ldraw.org/library/omr/31028-1_Sailboat.mpd',
    sourceHash: '5e90522ed24a91776a1217c43bd7285c10123c870fae5634377a017cdd4d9e6b', author: 'Merlijn Wissink [legolijntje]', notes: editorialNotes },
  { ...creator, id: '31009', setNumber: '31009', title: 'Small Cottage', subtitle: '田园小屋', category: '建筑', year: 2013,
    sourceFile: 'assets-source/set-original/31009-1.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/1164', downloadUrl: 'https://library.ldraw.org/library/omr/31009-1.mpd',
    sourceHash: '97b83517b0e843f8071ea3e4e80fbe0c7897685a7f476d3ba83161bb1185333d', author: 'Stefan Frenz [smf]',
    notes: ['步骤来自 OMR 作者 STEP；子装配按源层级展开，不是 LEGO 官方纸质说明书页码。'] },
  { theme: 'Train 9V', license: 'CC BY 2.0', licenseUrl: atlasConfig.licenseUrl,
    id: '10014', setNumber: '10014', title: 'Caboose', subtitle: '守车', category: '铁路', year: 2001,
    sourceFile: 'assets-source/set-original/10014-1.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/1415', downloadUrl: 'https://library.ldraw.org/library/omr/10014-1.mpd',
    sourceHash: 'f3aead9fe55512171565803f187f3f7a952fb70515983c39970cffd89431644d', author: 'TotalyWicked [TotalyWicked], OMR by Robert Paciorek [bercik]',
    notes: ['复杂铁路车辆模型；源文件没有 STEP，工作台提供结构演示顺序，不等同于官方说明书。'] },
  { theme: 'Town', license: 'CC BY 2.0', licenseUrl: atlasConfig.licenseUrl,
    id: '10156', setNumber: '10156', title: 'LEGO Truck', subtitle: '品牌运输卡车', category: '车辆', year: 2004,
    sourceFile: 'assets-source/set-original/10156-1.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/659', downloadUrl: 'https://library.ldraw.org/library/omr/10156-1.mpd',
    sourceHash: 'a58a784e6f6ce9d39999db1a4505941b5db5ebd1798af979bae891bc520a1a45', author: 'Robert Paciorek [bercik]',
    notes: ['复杂车辆模型；步骤来自 OMR 作者 STEP，按源层级展开，不对应官方纸质说明书页码。'] },
  { theme: 'Train', license: 'CC BY 2.0', licenseUrl: atlasConfig.licenseUrl,
    id: '10001', setNumber: '10001', title: 'Metroliner', subtitle: '城际特快列车', category: '铁路', year: 2001,
    sourceFile: 'assets-source/set-original/10001-1.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/657', downloadUrl: 'https://library.ldraw.org/library/omr/10001-1.mpd',
    sourceHash: '684a8032488dc2c5cb72a9ef32befb1399914eb32423e5b0cd91b6acfd3ab0e3', author: 'Zoltan Keri [kzoltan82]',
    notes: ['复杂列车模型；步骤来自 OMR 作者 STEP，按源层级展开，不对应官方纸质说明书页码。'] },
  { theme: 'World City', license: 'CC BY 2.0', licenseUrl: atlasConfig.licenseUrl,
    id: '10128', setNumber: '10128', title: 'Train Level Crossing', subtitle: '铁路道口', category: '铁路', year: 2003,
    sourceFile: 'assets-source/set-original/10128-1.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/864', downloadUrl: 'https://library.ldraw.org/library/omr/10128-1.mpd',
    sourceHash: '7928f4e259455ec49cc02c62acb1653f7a002824c789f099845936d0a2e8a0b9', author: 'Robert Paciorek [bercik]',
    notes: ['场景模型；步骤来自 OMR 作者 STEP，按源层级展开，不对应官方纸质说明书页码。'] },
  { theme: 'Town', license: 'CC BY 2.0', licenseUrl: atlasConfig.licenseUrl,
    id: '10036', setNumber: '10036', title: 'Pizza To Go', subtitle: '披萨餐厅', category: '建筑', year: 2002,
    sourceFile: 'assets-source/set-original/10036-1.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/658', downloadUrl: 'https://library.ldraw.org/library/omr/10036-1.mpd',
    sourceHash: 'bb9eafb3fc283a4b3b28eef58d6f9208528ee3d9b3debe4a7db8bbadc85f63f8', author: 'Robert Paciorek [bercik]',
    notes: ['城市场景模型；步骤来自 OMR 作者 STEP，按源层级展开，不对应官方纸质说明书页码。'] },
  { theme: 'City Airport', license: 'CC BY 2.0', licenseUrl: atlasConfig.licenseUrl,
    id: '10159', setNumber: '10159', title: 'City Airport', subtitle: '城市机场', category: '建筑', year: 2004,
    sourceFile: 'assets-source/set-original/10159-1.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/660', downloadUrl: 'https://library.ldraw.org/library/omr/10159-1.mpd',
    sourceHash: 'ef0b08af1e69059813e8965d3aa8fdd6a4aadbb04a21d92723cc4f9ae26bc1ec', author: 'Zoltan Keri [kzoltan82]',
    notes: ['大型机场场景；源文件没有 STEP，工作台提供结构演示顺序，不等同于官方说明书。'] },
  { theme: 'Creator Expert', license: 'CC BY 2.0', licenseUrl: atlasConfig.licenseUrl,
    id: '10220', setNumber: '10220', title: 'Volkswagen T1 Camper Van', subtitle: '大众 T1 露营车', category: '车辆', year: 2011,
    sourceFile: 'assets-source/set-original/10220-1.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/1294', downloadUrl: 'https://library.ldraw.org/library/omr/10220-1.mpd',
    sourceHash: 'ded9a68fc1b569e2965aa67febd225ab9d4b496a5d944247488d64c5d1619373', author: 'Stan Isachenko [angmarec]',
    notes: ['大型 Creator 车辆；步骤来自 OMR 作者 STEP，按源层级展开，不对应官方纸质说明书页码。'] },
  { theme: 'Creator Expert', license: 'CC BY 2.0', licenseUrl: atlasConfig.licenseUrl,
    id: '10214', setNumber: '10214', title: 'Tower Bridge', subtitle: '伦敦塔桥', category: '建筑', year: 2010,
    sourceFile: 'assets-source/set-original/10214-1.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/24', downloadUrl: 'https://library.ldraw.org/library/omr/10214-1.mpd',
    sourceHash: 'aca263220cb835cb2e32447f3f4738243d77e168c753c218d1e58890db4965d6', author: 'Orion Pobursky [OrionP]',
    notes: ['大型地标建筑；步骤来自 OMR 作者 STEP，模型无缺失零件与贴图。'] },
  { theme: 'Creator Expert', license: 'CC BY 2.0', licenseUrl: atlasConfig.licenseUrl,
    id: '10213', setNumber: '10213', title: 'Shuttle Adventure', subtitle: '航天飞机探险', category: '航天', year: 2010,
    sourceFile: 'assets-source/set-original/10213-1.mpd', sourceUrl: 'https://library.ldraw.org/omr/sets/870', downloadUrl: 'https://library.ldraw.org/library/omr/10213-1.mpd',
    sourceHash: 'e295434c8fc8c067e6cd01c398dccd3059a38799f03a6cecddb9319ecf16d909', author: 'Edward Carman [EdmanZA]',
    notes: ['大型航天模型；步骤来自 OMR 作者 STEP，图案与贴纸未完整包含。'] },
];
