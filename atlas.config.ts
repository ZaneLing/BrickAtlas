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
];
