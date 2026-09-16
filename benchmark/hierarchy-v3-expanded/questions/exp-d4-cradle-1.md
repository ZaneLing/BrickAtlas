## D4 协同系统·弧架倾转托座

### 模块识别（h3-exp-d4-cradle-1-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：cell-0-shuttle
- B：cell-0-mount
- C：cell-0-optic
- D：foundation

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "foundation",
        "name": "foundation"
      },
      {
        "id": "cell-0-shuttle",
        "name": "cell 0 shuttle"
      },
      {
        "id": "cell-0-mount",
        "name": "cell 0 mount"
      },
      {
        "id": "cell-0-yoke",
        "name": "cell 0 yoke"
      },
      {
        "id": "cell-0-cradle",
        "name": "cell 0 cradle"
      },
      {
        "id": "cell-0-optic",
        "name": "cell 0 optic"
      },
      {
        "id": "cell-0-console",
        "name": "cell 0 console"
      },
      {
        "id": "cell-0-magazine",
        "name": "cell 0 magazine"
      },
      {
        "id": "cell-0-drawer",
        "name": "cell 0 drawer"
      },
      {
        "id": "cell-1-shuttle",
        "name": "cell 1 shuttle"
      },
      {
        "id": "cell-1-mount",
        "name": "cell 1 mount"
      },
      {
        "id": "cell-1-hub",
        "name": "cell 1 hub"
      },
      {
        "id": "cell-1-wing-0",
        "name": "cell 1 wing 0"
      },
      {
        "id": "cell-1-wing-1",
        "name": "cell 1 wing 1"
      },
      {
        "id": "cell-1-wing-2",
        "name": "cell 1 wing 2"
      },
      {
        "id": "cell-1-wing-3",
        "name": "cell 1 wing 3"
      },
      {
        "id": "cell-1-console",
        "name": "cell 1 console"
      },
      {
        "id": "cell-1-magazine",
        "name": "cell 1 magazine"
      },
      {
        "id": "cell-1-drawer",
        "name": "cell 1 drawer"
      },
      {
        "id": "cell-2-shuttle",
        "name": "cell 2 shuttle"
      },
      {
        "id": "cell-2-mount",
        "name": "cell 2 mount"
      },
      {
        "id": "cell-2-hub",
        "name": "cell 2 hub"
      },
      {
        "id": "cell-2-probe-0",
        "name": "cell 2 probe 0"
      },
      {
        "id": "cell-2-console",
        "name": "cell 2 console"
      },
      {
        "id": "cell-2-magazine",
        "name": "cell 2 magazine"
      },
      {
        "id": "cell-2-drawer",
        "name": "cell 2 drawer"
      },
      {
        "id": "shared-inspection-mast",
        "name": "shared inspection mast"
      },
      {
        "id": "shared-scanner",
        "name": "shared scanner"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 部件计数（h3-exp-d4-cradle-1-count）

模块 cell-0-optic 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：1
- B：5
- C：2
- D：3

```json
{
  "input": {
    "parts": [
      {
        "id": "foundation-p0",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p1",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p2",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p3",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p4",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p5",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p6",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p7",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p8",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p9",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p10",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p11",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p12",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p13",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p14",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p15",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p16",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p17",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p18",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p19",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p20",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p21",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p22",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p23",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p24",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p25",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p26",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p27",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p28",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p29",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p30",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p31",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p32",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p33",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p34",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p35",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p36",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p37",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p38",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p39",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p40",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p41",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p42",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p43",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p44",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p45",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p46",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p47",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p48",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p49",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p50",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p51",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p52",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p53",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p54",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p55",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p56",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p57",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p58",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p59",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p60",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p61",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p62",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p63",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p64",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p65",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p66",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p67",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p68",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p69",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p70",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p71",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p72",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p73",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p74",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p75",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p76",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p77",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p78",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p79",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p80",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p81",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p82",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p83",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p84",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p85",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p86",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p87",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p88",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p89",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p90",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p91",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p92",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p93",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p94",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p95",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p96",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p97",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p98",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p99",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p100",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p101",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p102",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p103",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p104",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p105",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p106",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p107",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p108",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p109",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p110",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p111",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p112",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p113",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p114",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p115",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p116",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p117",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p118",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p119",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p120",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p121",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p122",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p123",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p124",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p125",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p126",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p127",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p128",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p129",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p130",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p131",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p132",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p133",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p134",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p135",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p136",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p137",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p138",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p139",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p140",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p141",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p142",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p143",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p144",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p145",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p146",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p147",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p148",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p149",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p150",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p151",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p152",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p153",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p154",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p155",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p156",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p157",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p158",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p159",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p160",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p161",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p162",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p163",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p164",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p165",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p166",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p167",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p168",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p169",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p170",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p171",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p172",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p173",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p174",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p175",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p176",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p177",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p178",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p179",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "cell-0-shuttle-p180",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p181",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p182",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p183",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p184",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p185",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p186",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p187",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p188",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p189",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p190",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p191",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p192",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p193",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p194",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p195",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p196",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p197",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p198",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p199",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p200",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p201",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p202",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p203",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p204",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p205",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p206",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p207",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p208",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p209",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p210",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p211",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p212",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p213",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p214",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p215",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p216",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p217",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p218",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p219",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p220",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p221",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p222",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p223",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p224",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p225",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p226",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p227",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-mount-p228",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p229",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p230",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p231",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p232",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p233",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p234",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p235",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p236",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p237",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p238",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p239",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p240",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p241",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p242",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p243",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p244",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p245",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p246",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p247",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p248",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p249",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p250",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p251",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p252",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p253",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p254",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p255",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p256",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p257",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-yoke-p258",
        "moduleId": "cell-0-yoke",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-yoke-p259",
        "moduleId": "cell-0-yoke",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-yoke-p260",
        "moduleId": "cell-0-yoke",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-yoke-p261",
        "moduleId": "cell-0-yoke",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-yoke-p262",
        "moduleId": "cell-0-yoke",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-yoke-p263",
        "moduleId": "cell-0-yoke",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-yoke-p264",
        "moduleId": "cell-0-yoke",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-yoke-p265",
        "moduleId": "cell-0-yoke",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-yoke-p266",
        "moduleId": "cell-0-yoke",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-yoke-p267",
        "moduleId": "cell-0-yoke",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-yoke-p268",
        "moduleId": "cell-0-yoke",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-cradle-p269",
        "moduleId": "cell-0-cradle",
        "shape": "cylinder",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-optic-p270",
        "moduleId": "cell-0-optic",
        "shape": "cylinder",
        "color": "#45a080"
      },
      {
        "id": "cell-0-optic-p271",
        "moduleId": "cell-0-optic",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-0-console-p272",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p273",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p274",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p275",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p276",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p277",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p278",
        "moduleId": "cell-0-console",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-0-console-p279",
        "moduleId": "cell-0-console",
        "shape": "slope",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p280",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p281",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p282",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p283",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p284",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p285",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p286",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p287",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p288",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p289",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p290",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p291",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p292",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p293",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p294",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p295",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p296",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p297",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p298",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p299",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p300",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p301",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p302",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p303",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p304",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p305",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p306",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p307",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p308",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p309",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p310",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p311",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p312",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p313",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p314",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p315",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p316",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p317",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p318",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p319",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p320",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p321",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p322",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p323",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p324",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p325",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p326",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p327",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p328",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p329",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p330",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p331",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p332",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p333",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p334",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p335",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p336",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p337",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-drawer-p338",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p339",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p340",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p341",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p342",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p343",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-shuttle-p344",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p345",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p346",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p347",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p348",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p349",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p350",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p351",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p352",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p353",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p354",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p355",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p356",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p357",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p358",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p359",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p360",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p361",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p362",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p363",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p364",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p365",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p366",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p367",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p368",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p369",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p370",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p371",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p372",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p373",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p374",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p375",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p376",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p377",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p378",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p379",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p380",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p381",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p382",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p383",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p384",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p385",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p386",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p387",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p388",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p389",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p390",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p391",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-mount-p392",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p393",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p394",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p395",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p396",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p397",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p398",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p399",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p400",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p401",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p402",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p403",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p404",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p405",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p406",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p407",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p408",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p409",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p410",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p411",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p412",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p413",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p414",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p415",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p416",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p417",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p418",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p419",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p420",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p421",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p422",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p423",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p424",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p425",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p426",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-hub-p427",
        "moduleId": "cell-1-hub",
        "shape": "cylinder",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-wing-0-p428",
        "moduleId": "cell-1-wing-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-0-p429",
        "moduleId": "cell-1-wing-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-0-p430",
        "moduleId": "cell-1-wing-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-0-p431",
        "moduleId": "cell-1-wing-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-0-p432",
        "moduleId": "cell-1-wing-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-0-p433",
        "moduleId": "cell-1-wing-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-0-p434",
        "moduleId": "cell-1-wing-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-wing-0-p435",
        "moduleId": "cell-1-wing-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-wing-1-p436",
        "moduleId": "cell-1-wing-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-1-p437",
        "moduleId": "cell-1-wing-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-1-p438",
        "moduleId": "cell-1-wing-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-1-p439",
        "moduleId": "cell-1-wing-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-1-p440",
        "moduleId": "cell-1-wing-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-1-p441",
        "moduleId": "cell-1-wing-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-1-p442",
        "moduleId": "cell-1-wing-1",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-wing-1-p443",
        "moduleId": "cell-1-wing-1",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-wing-2-p444",
        "moduleId": "cell-1-wing-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-2-p445",
        "moduleId": "cell-1-wing-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-2-p446",
        "moduleId": "cell-1-wing-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-2-p447",
        "moduleId": "cell-1-wing-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-2-p448",
        "moduleId": "cell-1-wing-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-2-p449",
        "moduleId": "cell-1-wing-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-2-p450",
        "moduleId": "cell-1-wing-2",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-wing-2-p451",
        "moduleId": "cell-1-wing-2",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-wing-3-p452",
        "moduleId": "cell-1-wing-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-3-p453",
        "moduleId": "cell-1-wing-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-3-p454",
        "moduleId": "cell-1-wing-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-3-p455",
        "moduleId": "cell-1-wing-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-3-p456",
        "moduleId": "cell-1-wing-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-3-p457",
        "moduleId": "cell-1-wing-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-wing-3-p458",
        "moduleId": "cell-1-wing-3",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-wing-3-p459",
        "moduleId": "cell-1-wing-3",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-console-p460",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p461",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p462",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p463",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p464",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p465",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p466",
        "moduleId": "cell-1-console",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-1-console-p467",
        "moduleId": "cell-1-console",
        "shape": "slope",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p468",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p469",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p470",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p471",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p472",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p473",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p474",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p475",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p476",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p477",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p478",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p479",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p480",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p481",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p482",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p483",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p484",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p485",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p486",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p487",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p488",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p489",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p490",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p491",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p492",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p493",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p494",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p495",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p496",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p497",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p498",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p499",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p500",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p501",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p502",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p503",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p504",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p505",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p506",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p507",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p508",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p509",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p510",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p511",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p512",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p513",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p514",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p515",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p516",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p517",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p518",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p519",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p520",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p521",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p522",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p523",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p524",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p525",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-drawer-p526",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p527",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p528",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p529",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p530",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p531",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-2-shuttle-p532",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p533",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p534",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p535",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p536",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p537",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p538",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p539",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p540",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p541",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p542",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p543",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p544",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p545",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p546",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p547",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p548",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p549",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p550",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p551",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p552",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p553",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p554",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p555",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p556",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p557",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p558",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p559",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p560",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p561",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p562",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p563",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p564",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p565",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p566",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p567",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p568",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p569",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p570",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p571",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p572",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p573",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p574",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p575",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p576",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p577",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p578",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p579",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-mount-p580",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p581",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p582",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p583",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p584",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p585",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p586",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p587",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p588",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p589",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p590",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p591",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p592",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p593",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p594",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p595",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p596",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p597",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p598",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p599",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p600",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p601",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p602",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p603",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p604",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p605",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p606",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p607",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p608",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p609",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-hub-p610",
        "moduleId": "cell-2-hub",
        "shape": "cylinder",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-probe-0-p611",
        "moduleId": "cell-2-probe-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-probe-0-p612",
        "moduleId": "cell-2-probe-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-probe-0-p613",
        "moduleId": "cell-2-probe-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-probe-0-p614",
        "moduleId": "cell-2-probe-0",
        "shape": "sphere",
        "color": "#45a080"
      },
      {
        "id": "cell-2-console-p615",
        "moduleId": "cell-2-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-2-console-p616",
        "moduleId": "cell-2-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-2-console-p617",
        "moduleId": "cell-2-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-2-console-p618",
        "moduleId": "cell-2-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-2-console-p619",
        "moduleId": "cell-2-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-2-console-p620",
        "moduleId": "cell-2-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-2-console-p621",
        "moduleId": "cell-2-console",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-2-console-p622",
        "moduleId": "cell-2-console",
        "shape": "slope",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p623",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p624",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p625",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p626",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p627",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p628",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p629",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p630",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p631",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p632",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p633",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p634",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p635",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p636",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p637",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p638",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p639",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p640",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p641",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p642",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p643",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p644",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p645",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p646",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p647",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p648",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p649",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p650",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p651",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p652",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p653",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p654",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p655",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p656",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p657",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p658",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p659",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p660",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p661",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p662",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p663",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p664",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p665",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p666",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p667",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p668",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p669",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p670",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p671",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p672",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p673",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p674",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p675",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p676",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p677",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p678",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p679",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p680",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-drawer-p681",
        "moduleId": "cell-2-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-2-drawer-p682",
        "moduleId": "cell-2-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-2-drawer-p683",
        "moduleId": "cell-2-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-2-drawer-p684",
        "moduleId": "cell-2-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-2-drawer-p685",
        "moduleId": "cell-2-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-2-drawer-p686",
        "moduleId": "cell-2-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "shared-inspection-mast-p687",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p688",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p689",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p690",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p691",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p692",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p693",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p694",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p695",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p696",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p697",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "shared-inspection-mast-p698",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "shared-inspection-mast-p699",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "shared-scanner-p700",
        "moduleId": "shared-scanner",
        "shape": "cylinder",
        "color": "#dc6040"
      },
      {
        "id": "shared-scanner-p701",
        "moduleId": "shared-scanner",
        "shape": "window",
        "color": "#79c7d8"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 颜色识别（h3-exp-d4-cradle-1-color）

零件 cell-0-optic-p270 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#d43a32
- B：#f2bf3c
- C：#45a080
- D：#2878b8

```json
{
  "input": {
    "part": {
      "id": "cell-0-optic-p270",
      "moduleId": "cell-0-optic",
      "shape": "cylinder",
      "position": [
        0,
        -0.09999999999999964,
        0
      ],
      "size": [
        1.2,
        0.5,
        1.2
      ],
      "color": "#45a080",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 三维位置（h3-exp-d4-cradle-1-position）

模块 cell-0-optic 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,0.2,0]
- B：[-13,0.75,0]
- C：[-13,1.35,0]
- D：[-13,5.949999999999999,0]

```json
{
  "input": {
    "centers": {
      "foundation": [
        0,
        0.2,
        0
      ],
      "cell-0-shuttle": [
        -13,
        0.75,
        0
      ],
      "cell-0-mount": [
        -13,
        1.35,
        0
      ],
      "cell-0-yoke": [
        -13,
        3.325,
        0
      ],
      "cell-0-cradle": [
        -13,
        4.6,
        0
      ],
      "cell-0-optic": [
        -13,
        5.949999999999999,
        0
      ],
      "cell-0-console": [
        -13,
        1.8775000000000002,
        6
      ],
      "cell-0-magazine": [
        -13,
        3.1399999999999997,
        -6
      ],
      "cell-0-drawer": [
        -13,
        1.55,
        -6
      ],
      "cell-1-shuttle": [
        0,
        0.75,
        0
      ],
      "cell-1-mount": [
        0,
        1.35,
        0
      ],
      "cell-1-hub": [
        0,
        2.8,
        0
      ],
      "cell-1-wing-0": [
        2.5,
        4.3225,
        0
      ],
      "cell-1-wing-1": [
        2.220446049250313e-16,
        4.442500000000001,
        2.5
      ],
      "cell-1-wing-2": [
        -2.5,
        4.5625,
        4.440892098500626e-16
      ],
      "cell-1-wing-3": [
        -4.440892098500626e-16,
        4.682499999999999,
        -2.5
      ],
      "cell-1-console": [
        0,
        1.8775000000000002,
        6
      ],
      "cell-1-magazine": [
        0,
        3.1399999999999997,
        -6
      ],
      "cell-1-drawer": [
        0,
        1.55,
        -6
      ],
      "cell-2-shuttle": [
        13,
        0.75,
        0
      ],
      "cell-2-mount": [
        13,
        1.35,
        0
      ],
      "cell-2-hub": [
        13,
        2.3,
        0
      ],
      "cell-2-probe-0": [
        14.83629800496756,
        4.701658603477292,
        0
      ],
      "cell-2-console": [
        13,
        1.8775000000000002,
        6
      ],
      "cell-2-magazine": [
        13,
        3.1399999999999997,
        -6
      ],
      "cell-2-drawer": [
        13,
        1.55,
        -6
      ],
      "shared-inspection-mast": [
        0,
        3.5875,
        11
      ],
      "shared-scanner": [
        0,
        7.012499999999999,
        11
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节类型（h3-exp-d4-cradle-1-joint-type）

cell-0-cradle-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：fixed
- B：prismatic
- C：spring
- D：revolute

```json
{
  "input": {
    "joint": {
      "id": "cell-0-cradle-joint",
      "name": "cell-0-cradle interface",
      "parent": "cell-0-yoke",
      "child": "cell-0-cradle",
      "type": "revolute",
      "anchorParent": [
        0,
        1.2749999999999995,
        0
      ],
      "anchorChild": [
        0,
        0,
        0
      ],
      "axis": [
        1,
        0,
        0
      ],
      "limits": [
        -0.6,
        0.6
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 直接连接（h3-exp-d4-cradle-1-parent）

cell-0-optic 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["cell-0-cradle"]
- B：["cell-0-optic"]
- C：[]
- D：["foundation","cell-0-shuttle","cell-0-mount","cell-0-yoke","cell-0-cradle","cell-0-optic","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-hub","cell-1-wing-0","cell-1-wing-1","cell-1-wing-2","cell-1-wing-3","cell-1-console","cell-1-magazine","cell-1-drawer","cell-2-shuttle","cell-2-mount","cell-2-hub","cell-2-probe-0","cell-2-console","cell-2-magazine","cell-2-drawer","shared-inspection-mast","shared-scanner"]

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          -13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-yoke-joint",
        "name": "cell-0-yoke interface",
        "parent": "cell-0-mount",
        "child": "cell-0-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          0,
          -1.4250000000000003,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-cradle-joint",
        "name": "cell-0-cradle interface",
        "parent": "cell-0-yoke",
        "child": "cell-0-cradle",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2749999999999995,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-optic-joint",
        "name": "cell-0-optic interface",
        "parent": "cell-0-cradle",
        "child": "cell-0-optic",
        "type": "fixed",
        "anchorParent": [
          0,
          1.25,
          0
        ],
        "anchorChild": [
          0,
          -0.09999999999999964,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-drawer-joint",
        "name": "cell-0-drawer interface",
        "parent": "cell-0-magazine",
        "child": "cell-0-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-shuttle-joint",
        "name": "cell-1-shuttle interface",
        "parent": "foundation",
        "child": "cell-1-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-mount-joint",
        "name": "cell-1-mount interface",
        "parent": "cell-1-shuttle",
        "child": "cell-1-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-hub-joint",
        "name": "cell-1-hub interface",
        "parent": "cell-1-mount",
        "child": "cell-1-hub",
        "type": "fixed",
        "anchorParent": [
          0,
          1.4499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-wing-0-joint",
        "name": "cell-1-wing-0 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-0",
        "type": "revolute",
        "anchorParent": [
          2.5,
          1.6000000000000005,
          0
        ],
        "anchorChild": [
          0,
          0.07750000000000057,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-1-joint",
        "name": "cell-1-wing-1 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-1",
        "type": "revolute",
        "anchorParent": [
          1.5308084989341916e-16,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          -1.3452603800354324e-17,
          0.07749999999999968,
          0
        ],
        "axis": [
          -1,
          0,
          6.123233995736766e-17
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-2-joint",
        "name": "cell-1-wing-2 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-2",
        "type": "revolute",
        "anchorParent": [
          -2.5,
          1.8399999999999999,
          3.061616997868383e-16
        ],
        "anchorChild": [
          0,
          0.07749999999999968,
          -2.6905207600708648e-17
        ],
        "axis": [
          -1.2246467991473532e-16,
          0,
          -1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-3-joint",
        "name": "cell-1-wing-3 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-3",
        "type": "revolute",
        "anchorParent": [
          -4.592425496802574e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          -1.515333983019478e-17,
          0.07750000000000057,
          0
        ],
        "axis": [
          1,
          0,
          -1.8369701987210297e-16
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-drawer-joint",
        "name": "cell-1-drawer interface",
        "parent": "cell-1-magazine",
        "child": "cell-1-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-shuttle-joint",
        "name": "cell-2-shuttle interface",
        "parent": "foundation",
        "child": "cell-2-shuttle",
        "type": "prismatic",
        "anchorParent": [
          13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-mount-joint",
        "name": "cell-2-mount interface",
        "parent": "cell-2-shuttle",
        "child": "cell-2-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-hub-joint",
        "name": "cell-2-hub interface",
        "parent": "cell-2-mount",
        "child": "cell-2-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-2-probe-0-joint",
        "name": "cell-2-probe-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772923,
          0
        ],
        "axis": [
          0.6,
          0.8,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-magazine-joint",
        "name": "cell-2-magazine interface",
        "parent": "foundation",
        "child": "cell-2-magazine",
        "type": "fixed",
        "anchorParent": [
          13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-drawer-joint",
        "name": "cell-2-drawer interface",
        "parent": "cell-2-magazine",
        "child": "cell-2-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "shared-inspection-mast-joint",
        "name": "shared-inspection-mast interface",
        "parent": "foundation",
        "child": "shared-inspection-mast",
        "type": "fixed",
        "anchorParent": [
          0,
          0.7999999999999999,
          11
        ],
        "anchorChild": [
          0,
          -2.5875,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shared-scanner-joint",
        "name": "shared-scanner interface",
        "parent": "shared-inspection-mast",
        "child": "shared-scanner",
        "type": "revolute",
        "anchorParent": [
          0,
          3.2125,
          0
        ],
        "anchorChild": [
          0,
          -0.21249999999999947,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 基座识别（h3-exp-d4-cradle-1-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","cell-0-shuttle","cell-0-mount","cell-0-yoke","cell-0-cradle","cell-0-optic","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-hub","cell-1-wing-0","cell-1-wing-1","cell-1-wing-2","cell-1-wing-3","cell-1-console","cell-1-magazine","cell-1-drawer","cell-2-shuttle","cell-2-mount","cell-2-hub","cell-2-probe-0","cell-2-console","cell-2-magazine","cell-2-drawer","shared-inspection-mast","shared-scanner"]
- C：["cell-0-optic"]
- D：["foundation"]

```json
{
  "input": {
    "modules": [
      {
        "id": "foundation",
        "name": "foundation",
        "role": "foundation",
        "anchored": true,
        "mass": 30,
        "position": [
          0,
          0.2,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-shuttle",
        "name": "cell 0 shuttle",
        "role": "actuator",
        "anchored": false,
        "mass": 3,
        "position": [
          -13,
          0.75,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-mount",
        "name": "cell 0 mount",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -13,
          1.35,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-yoke",
        "name": "cell 0 yoke",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -13,
          3.325,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-cradle",
        "name": "cell 0 cradle",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -13,
          4.6,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-optic",
        "name": "cell 0 optic",
        "role": "structure",
        "anchored": false,
        "mass": 0.5,
        "position": [
          -13,
          5.949999999999999,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-console",
        "name": "cell 0 console",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -13,
          1.8775000000000002,
          6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-magazine",
        "name": "cell 0 magazine",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -13,
          3.1399999999999997,
          -6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-drawer",
        "name": "cell 0 drawer",
        "role": "actuator",
        "anchored": false,
        "mass": 0.7,
        "position": [
          -13,
          1.55,
          -6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-1-shuttle",
        "name": "cell 1 shuttle",
        "role": "actuator",
        "anchored": false,
        "mass": 3,
        "position": [
          0,
          0.75,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-1-mount",
        "name": "cell 1 mount",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          1.35,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-1-hub",
        "name": "cell 1 hub",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          2.8,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-1-wing-0",
        "name": "cell 1 wing 0",
        "role": "actuator",
        "anchored": false,
        "mass": 0.65,
        "position": [
          2.5,
          4.3225,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-1-wing-1",
        "name": "cell 1 wing 1",
        "role": "actuator",
        "anchored": false,
        "mass": 0.65,
        "position": [
          1.6653345369377348e-16,
          4.442500000000001,
          2.5
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-1-wing-2",
        "name": "cell 1 wing 2",
        "role": "actuator",
        "anchored": false,
        "mass": 0.65,
        "position": [
          -2.5,
          4.5625,
          3.3306690738754696e-16
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-1-wing-3",
        "name": "cell 1 wing 3",
        "role": "actuator",
        "anchored": false,
        "mass": 0.65,
        "position": [
          -4.440892098500626e-16,
          4.682499999999999,
          -2.5
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-1-console",
        "name": "cell 1 console",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          1.8775000000000002,
          6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-1-magazine",
        "name": "cell 1 magazine",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          3.1399999999999997,
          -6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-1-drawer",
        "name": "cell 1 drawer",
        "role": "actuator",
        "anchored": false,
        "mass": 0.7,
        "position": [
          0,
          1.55,
          -6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-2-shuttle",
        "name": "cell 2 shuttle",
        "role": "actuator",
        "anchored": false,
        "mass": 3,
        "position": [
          13,
          0.75,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-2-mount",
        "name": "cell 2 mount",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          13,
          1.35,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-2-hub",
        "name": "cell 2 hub",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          13,
          2.3,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-2-probe-0",
        "name": "cell 2 probe 0",
        "role": "actuator",
        "anchored": false,
        "mass": 0.5,
        "position": [
          14.83629800496756,
          4.701658603477292,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-2-console",
        "name": "cell 2 console",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          13,
          1.8775000000000002,
          6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-2-magazine",
        "name": "cell 2 magazine",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          13,
          3.1399999999999997,
          -6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-2-drawer",
        "name": "cell 2 drawer",
        "role": "actuator",
        "anchored": false,
        "mass": 0.7,
        "position": [
          13,
          1.55,
          -6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "shared-inspection-mast",
        "name": "shared inspection mast",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          3.5875,
          11
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "shared-scanner",
        "name": "shared scanner",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          7.012499999999999,
          11
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 接口计数（h3-exp-d4-cradle-1-degree）

cell-0-optic 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：2
- B：0
- C：3
- D：1

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          -13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-yoke-joint",
        "name": "cell-0-yoke interface",
        "parent": "cell-0-mount",
        "child": "cell-0-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          0,
          -1.4250000000000003,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-cradle-joint",
        "name": "cell-0-cradle interface",
        "parent": "cell-0-yoke",
        "child": "cell-0-cradle",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2749999999999995,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-optic-joint",
        "name": "cell-0-optic interface",
        "parent": "cell-0-cradle",
        "child": "cell-0-optic",
        "type": "fixed",
        "anchorParent": [
          0,
          1.25,
          0
        ],
        "anchorChild": [
          0,
          -0.09999999999999964,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-drawer-joint",
        "name": "cell-0-drawer interface",
        "parent": "cell-0-magazine",
        "child": "cell-0-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-shuttle-joint",
        "name": "cell-1-shuttle interface",
        "parent": "foundation",
        "child": "cell-1-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-mount-joint",
        "name": "cell-1-mount interface",
        "parent": "cell-1-shuttle",
        "child": "cell-1-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-hub-joint",
        "name": "cell-1-hub interface",
        "parent": "cell-1-mount",
        "child": "cell-1-hub",
        "type": "fixed",
        "anchorParent": [
          0,
          1.4499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-wing-0-joint",
        "name": "cell-1-wing-0 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-0",
        "type": "revolute",
        "anchorParent": [
          2.5,
          1.6000000000000005,
          0
        ],
        "anchorChild": [
          0,
          0.07750000000000057,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-1-joint",
        "name": "cell-1-wing-1 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-1",
        "type": "revolute",
        "anchorParent": [
          1.5308084989341916e-16,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          -1.3452603800354324e-17,
          0.07749999999999968,
          0
        ],
        "axis": [
          -1,
          0,
          6.123233995736766e-17
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-2-joint",
        "name": "cell-1-wing-2 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-2",
        "type": "revolute",
        "anchorParent": [
          -2.5,
          1.8399999999999999,
          3.061616997868383e-16
        ],
        "anchorChild": [
          0,
          0.07749999999999968,
          -2.6905207600708648e-17
        ],
        "axis": [
          -1.2246467991473532e-16,
          0,
          -1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-3-joint",
        "name": "cell-1-wing-3 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-3",
        "type": "revolute",
        "anchorParent": [
          -4.592425496802574e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          -1.515333983019478e-17,
          0.07750000000000057,
          0
        ],
        "axis": [
          1,
          0,
          -1.8369701987210297e-16
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-drawer-joint",
        "name": "cell-1-drawer interface",
        "parent": "cell-1-magazine",
        "child": "cell-1-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-shuttle-joint",
        "name": "cell-2-shuttle interface",
        "parent": "foundation",
        "child": "cell-2-shuttle",
        "type": "prismatic",
        "anchorParent": [
          13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-mount-joint",
        "name": "cell-2-mount interface",
        "parent": "cell-2-shuttle",
        "child": "cell-2-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-hub-joint",
        "name": "cell-2-hub interface",
        "parent": "cell-2-mount",
        "child": "cell-2-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-2-probe-0-joint",
        "name": "cell-2-probe-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772923,
          0
        ],
        "axis": [
          0.6,
          0.8,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-magazine-joint",
        "name": "cell-2-magazine interface",
        "parent": "foundation",
        "child": "cell-2-magazine",
        "type": "fixed",
        "anchorParent": [
          13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-drawer-joint",
        "name": "cell-2-drawer interface",
        "parent": "cell-2-magazine",
        "child": "cell-2-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "shared-inspection-mast-joint",
        "name": "shared-inspection-mast interface",
        "parent": "foundation",
        "child": "shared-inspection-mast",
        "type": "fixed",
        "anchorParent": [
          0,
          0.7999999999999999,
          11
        ],
        "anchorChild": [
          0,
          -2.5875,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shared-scanner-joint",
        "name": "shared-scanner interface",
        "parent": "shared-inspection-mast",
        "child": "shared-scanner",
        "type": "revolute",
        "anchorParent": [
          0,
          3.2125,
          0
        ],
        "anchorChild": [
          0,
          -0.21249999999999947,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 局部改色（h3-exp-d4-cradle-1-recolor）

仅将 cell-0-optic-p270 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-optic-p271","color":"#e8792e"}
- B：{"id":"cell-0-optic-p270","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"cell-0-optic-p270","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "cell-0-optic-p270",
      "moduleId": "cell-0-optic",
      "shape": "cylinder",
      "position": [
        0,
        -0.09999999999999964,
        0
      ],
      "size": [
        1.2,
        0.5,
        1.2
      ],
      "color": "#45a080",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 补装部件（h3-exp-d4-cradle-1-add）

模块 cell-0-optic 缺失零件 cell-0-optic-p270。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-optic-p270","moduleId":"foundation","shape":"cylinder","position":[0,-0.09999999999999964,0],"size":[1.2,0.5,1.2],"color":"#45a080","rotation":[0,0,0,1]}
- B：{"id":"cell-0-optic-p270","moduleId":"cell-0-optic","shape":"cylinder","position":[0,-0.09999999999999964,0],"size":[3,3,3],"color":"#45a080","rotation":[0,0,0,1]}
- C：{"id":"cell-0-optic-p270","moduleId":"cell-0-optic","shape":"cylinder","position":[0,-0.09999999999999964,0],"size":[1.2,0.5,1.2],"color":"#000000","rotation":[0,0,0,1]}
- D：{"id":"cell-0-optic-p270","moduleId":"cell-0-optic","shape":"cylinder","position":[0,-0.09999999999999964,0],"size":[1.2,0.5,1.2],"color":"#45a080","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "cell-0-optic-p270",
      "moduleId": "cell-0-optic",
      "shape": "cylinder",
      "position": [
        0,
        -0.09999999999999964,
        0
      ],
      "size": [
        1.2,
        0.5,
        1.2
      ],
      "color": "#45a080",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    },
    "existingIds": [
      "foundation-p0",
      "foundation-p1",
      "foundation-p2",
      "foundation-p3",
      "foundation-p4",
      "foundation-p5",
      "foundation-p6",
      "foundation-p7",
      "foundation-p8",
      "foundation-p9",
      "foundation-p10",
      "foundation-p11",
      "foundation-p12",
      "foundation-p13",
      "foundation-p14",
      "foundation-p15",
      "foundation-p16",
      "foundation-p17",
      "foundation-p18",
      "foundation-p19",
      "foundation-p20",
      "foundation-p21",
      "foundation-p22",
      "foundation-p23",
      "foundation-p24",
      "foundation-p25",
      "foundation-p26",
      "foundation-p27",
      "foundation-p28",
      "foundation-p29",
      "foundation-p30",
      "foundation-p31",
      "foundation-p32",
      "foundation-p33",
      "foundation-p34",
      "foundation-p35",
      "foundation-p36",
      "foundation-p37",
      "foundation-p38",
      "foundation-p39",
      "foundation-p40",
      "foundation-p41",
      "foundation-p42",
      "foundation-p43",
      "foundation-p44",
      "foundation-p45",
      "foundation-p46",
      "foundation-p47",
      "foundation-p48",
      "foundation-p49",
      "foundation-p50",
      "foundation-p51",
      "foundation-p52",
      "foundation-p53",
      "foundation-p54",
      "foundation-p55",
      "foundation-p56",
      "foundation-p57",
      "foundation-p58",
      "foundation-p59",
      "foundation-p60",
      "foundation-p61",
      "foundation-p62",
      "foundation-p63",
      "foundation-p64",
      "foundation-p65",
      "foundation-p66",
      "foundation-p67",
      "foundation-p68",
      "foundation-p69",
      "foundation-p70",
      "foundation-p71",
      "foundation-p72",
      "foundation-p73",
      "foundation-p74",
      "foundation-p75",
      "foundation-p76",
      "foundation-p77",
      "foundation-p78",
      "foundation-p79",
      "foundation-p80",
      "foundation-p81",
      "foundation-p82",
      "foundation-p83",
      "foundation-p84",
      "foundation-p85",
      "foundation-p86",
      "foundation-p87",
      "foundation-p88",
      "foundation-p89",
      "foundation-p90",
      "foundation-p91",
      "foundation-p92",
      "foundation-p93",
      "foundation-p94",
      "foundation-p95",
      "foundation-p96",
      "foundation-p97",
      "foundation-p98",
      "foundation-p99",
      "foundation-p100",
      "foundation-p101",
      "foundation-p102",
      "foundation-p103",
      "foundation-p104",
      "foundation-p105",
      "foundation-p106",
      "foundation-p107",
      "foundation-p108",
      "foundation-p109",
      "foundation-p110",
      "foundation-p111",
      "foundation-p112",
      "foundation-p113",
      "foundation-p114",
      "foundation-p115",
      "foundation-p116",
      "foundation-p117",
      "foundation-p118",
      "foundation-p119",
      "foundation-p120",
      "foundation-p121",
      "foundation-p122",
      "foundation-p123",
      "foundation-p124",
      "foundation-p125",
      "foundation-p126",
      "foundation-p127",
      "foundation-p128",
      "foundation-p129",
      "foundation-p130",
      "foundation-p131",
      "foundation-p132",
      "foundation-p133",
      "foundation-p134",
      "foundation-p135",
      "foundation-p136",
      "foundation-p137",
      "foundation-p138",
      "foundation-p139",
      "foundation-p140",
      "foundation-p141",
      "foundation-p142",
      "foundation-p143",
      "foundation-p144",
      "foundation-p145",
      "foundation-p146",
      "foundation-p147",
      "foundation-p148",
      "foundation-p149",
      "foundation-p150",
      "foundation-p151",
      "foundation-p152",
      "foundation-p153",
      "foundation-p154",
      "foundation-p155",
      "foundation-p156",
      "foundation-p157",
      "foundation-p158",
      "foundation-p159",
      "foundation-p160",
      "foundation-p161",
      "foundation-p162",
      "foundation-p163",
      "foundation-p164",
      "foundation-p165",
      "foundation-p166",
      "foundation-p167",
      "foundation-p168",
      "foundation-p169",
      "foundation-p170",
      "foundation-p171",
      "foundation-p172",
      "foundation-p173",
      "foundation-p174",
      "foundation-p175",
      "foundation-p176",
      "foundation-p177",
      "foundation-p178",
      "foundation-p179",
      "cell-0-shuttle-p180",
      "cell-0-shuttle-p181",
      "cell-0-shuttle-p182",
      "cell-0-shuttle-p183",
      "cell-0-shuttle-p184",
      "cell-0-shuttle-p185",
      "cell-0-shuttle-p186",
      "cell-0-shuttle-p187",
      "cell-0-shuttle-p188",
      "cell-0-shuttle-p189",
      "cell-0-shuttle-p190",
      "cell-0-shuttle-p191",
      "cell-0-shuttle-p192",
      "cell-0-shuttle-p193",
      "cell-0-shuttle-p194",
      "cell-0-shuttle-p195",
      "cell-0-shuttle-p196",
      "cell-0-shuttle-p197",
      "cell-0-shuttle-p198",
      "cell-0-shuttle-p199",
      "cell-0-shuttle-p200",
      "cell-0-shuttle-p201",
      "cell-0-shuttle-p202",
      "cell-0-shuttle-p203",
      "cell-0-shuttle-p204",
      "cell-0-shuttle-p205",
      "cell-0-shuttle-p206",
      "cell-0-shuttle-p207",
      "cell-0-shuttle-p208",
      "cell-0-shuttle-p209",
      "cell-0-shuttle-p210",
      "cell-0-shuttle-p211",
      "cell-0-shuttle-p212",
      "cell-0-shuttle-p213",
      "cell-0-shuttle-p214",
      "cell-0-shuttle-p215",
      "cell-0-shuttle-p216",
      "cell-0-shuttle-p217",
      "cell-0-shuttle-p218",
      "cell-0-shuttle-p219",
      "cell-0-shuttle-p220",
      "cell-0-shuttle-p221",
      "cell-0-shuttle-p222",
      "cell-0-shuttle-p223",
      "cell-0-shuttle-p224",
      "cell-0-shuttle-p225",
      "cell-0-shuttle-p226",
      "cell-0-shuttle-p227",
      "cell-0-mount-p228",
      "cell-0-mount-p229",
      "cell-0-mount-p230",
      "cell-0-mount-p231",
      "cell-0-mount-p232",
      "cell-0-mount-p233",
      "cell-0-mount-p234",
      "cell-0-mount-p235",
      "cell-0-mount-p236",
      "cell-0-mount-p237",
      "cell-0-mount-p238",
      "cell-0-mount-p239",
      "cell-0-mount-p240",
      "cell-0-mount-p241",
      "cell-0-mount-p242",
      "cell-0-mount-p243",
      "cell-0-mount-p244",
      "cell-0-mount-p245",
      "cell-0-mount-p246",
      "cell-0-mount-p247",
      "cell-0-mount-p248",
      "cell-0-mount-p249",
      "cell-0-mount-p250",
      "cell-0-mount-p251",
      "cell-0-mount-p252",
      "cell-0-mount-p253",
      "cell-0-mount-p254",
      "cell-0-mount-p255",
      "cell-0-mount-p256",
      "cell-0-mount-p257",
      "cell-0-yoke-p258",
      "cell-0-yoke-p259",
      "cell-0-yoke-p260",
      "cell-0-yoke-p261",
      "cell-0-yoke-p262",
      "cell-0-yoke-p263",
      "cell-0-yoke-p264",
      "cell-0-yoke-p265",
      "cell-0-yoke-p266",
      "cell-0-yoke-p267",
      "cell-0-yoke-p268",
      "cell-0-cradle-p269",
      "cell-0-optic-p271",
      "cell-0-console-p272",
      "cell-0-console-p273",
      "cell-0-console-p274",
      "cell-0-console-p275",
      "cell-0-console-p276",
      "cell-0-console-p277",
      "cell-0-console-p278",
      "cell-0-console-p279",
      "cell-0-magazine-p280",
      "cell-0-magazine-p281",
      "cell-0-magazine-p282",
      "cell-0-magazine-p283",
      "cell-0-magazine-p284",
      "cell-0-magazine-p285",
      "cell-0-magazine-p286",
      "cell-0-magazine-p287",
      "cell-0-magazine-p288",
      "cell-0-magazine-p289",
      "cell-0-magazine-p290",
      "cell-0-magazine-p291",
      "cell-0-magazine-p292",
      "cell-0-magazine-p293",
      "cell-0-magazine-p294",
      "cell-0-magazine-p295",
      "cell-0-magazine-p296",
      "cell-0-magazine-p297",
      "cell-0-magazine-p298",
      "cell-0-magazine-p299",
      "cell-0-magazine-p300",
      "cell-0-magazine-p301",
      "cell-0-magazine-p302",
      "cell-0-magazine-p303",
      "cell-0-magazine-p304",
      "cell-0-magazine-p305",
      "cell-0-magazine-p306",
      "cell-0-magazine-p307",
      "cell-0-magazine-p308",
      "cell-0-magazine-p309",
      "cell-0-magazine-p310",
      "cell-0-magazine-p311",
      "cell-0-magazine-p312",
      "cell-0-magazine-p313",
      "cell-0-magazine-p314",
      "cell-0-magazine-p315",
      "cell-0-magazine-p316",
      "cell-0-magazine-p317",
      "cell-0-magazine-p318",
      "cell-0-magazine-p319",
      "cell-0-magazine-p320",
      "cell-0-magazine-p321",
      "cell-0-magazine-p322",
      "cell-0-magazine-p323",
      "cell-0-magazine-p324",
      "cell-0-magazine-p325",
      "cell-0-magazine-p326",
      "cell-0-magazine-p327",
      "cell-0-magazine-p328",
      "cell-0-magazine-p329",
      "cell-0-magazine-p330",
      "cell-0-magazine-p331",
      "cell-0-magazine-p332",
      "cell-0-magazine-p333",
      "cell-0-magazine-p334",
      "cell-0-magazine-p335",
      "cell-0-magazine-p336",
      "cell-0-magazine-p337",
      "cell-0-drawer-p338",
      "cell-0-drawer-p339",
      "cell-0-drawer-p340",
      "cell-0-drawer-p341",
      "cell-0-drawer-p342",
      "cell-0-drawer-p343",
      "cell-1-shuttle-p344",
      "cell-1-shuttle-p345",
      "cell-1-shuttle-p346",
      "cell-1-shuttle-p347",
      "cell-1-shuttle-p348",
      "cell-1-shuttle-p349",
      "cell-1-shuttle-p350",
      "cell-1-shuttle-p351",
      "cell-1-shuttle-p352",
      "cell-1-shuttle-p353",
      "cell-1-shuttle-p354",
      "cell-1-shuttle-p355",
      "cell-1-shuttle-p356",
      "cell-1-shuttle-p357",
      "cell-1-shuttle-p358",
      "cell-1-shuttle-p359",
      "cell-1-shuttle-p360",
      "cell-1-shuttle-p361",
      "cell-1-shuttle-p362",
      "cell-1-shuttle-p363",
      "cell-1-shuttle-p364",
      "cell-1-shuttle-p365",
      "cell-1-shuttle-p366",
      "cell-1-shuttle-p367",
      "cell-1-shuttle-p368",
      "cell-1-shuttle-p369",
      "cell-1-shuttle-p370",
      "cell-1-shuttle-p371",
      "cell-1-shuttle-p372",
      "cell-1-shuttle-p373",
      "cell-1-shuttle-p374",
      "cell-1-shuttle-p375",
      "cell-1-shuttle-p376",
      "cell-1-shuttle-p377",
      "cell-1-shuttle-p378",
      "cell-1-shuttle-p379",
      "cell-1-shuttle-p380",
      "cell-1-shuttle-p381",
      "cell-1-shuttle-p382",
      "cell-1-shuttle-p383",
      "cell-1-shuttle-p384",
      "cell-1-shuttle-p385",
      "cell-1-shuttle-p386",
      "cell-1-shuttle-p387",
      "cell-1-shuttle-p388",
      "cell-1-shuttle-p389",
      "cell-1-shuttle-p390",
      "cell-1-shuttle-p391",
      "cell-1-mount-p392",
      "cell-1-mount-p393",
      "cell-1-mount-p394",
      "cell-1-mount-p395",
      "cell-1-mount-p396",
      "cell-1-mount-p397",
      "cell-1-mount-p398",
      "cell-1-mount-p399",
      "cell-1-mount-p400",
      "cell-1-mount-p401",
      "cell-1-mount-p402",
      "cell-1-mount-p403",
      "cell-1-mount-p404",
      "cell-1-mount-p405",
      "cell-1-mount-p406",
      "cell-1-mount-p407",
      "cell-1-mount-p408",
      "cell-1-mount-p409",
      "cell-1-mount-p410",
      "cell-1-mount-p411",
      "cell-1-mount-p412",
      "cell-1-mount-p413",
      "cell-1-mount-p414",
      "cell-1-mount-p415",
      "cell-1-mount-p416",
      "cell-1-mount-p417",
      "cell-1-mount-p418",
      "cell-1-mount-p419",
      "cell-1-mount-p420",
      "cell-1-mount-p421",
      "cell-1-mount-p422",
      "cell-1-mount-p423",
      "cell-1-mount-p424",
      "cell-1-mount-p425",
      "cell-1-mount-p426",
      "cell-1-hub-p427",
      "cell-1-wing-0-p428",
      "cell-1-wing-0-p429",
      "cell-1-wing-0-p430",
      "cell-1-wing-0-p431",
      "cell-1-wing-0-p432",
      "cell-1-wing-0-p433",
      "cell-1-wing-0-p434",
      "cell-1-wing-0-p435",
      "cell-1-wing-1-p436",
      "cell-1-wing-1-p437",
      "cell-1-wing-1-p438",
      "cell-1-wing-1-p439",
      "cell-1-wing-1-p440",
      "cell-1-wing-1-p441",
      "cell-1-wing-1-p442",
      "cell-1-wing-1-p443",
      "cell-1-wing-2-p444",
      "cell-1-wing-2-p445",
      "cell-1-wing-2-p446",
      "cell-1-wing-2-p447",
      "cell-1-wing-2-p448",
      "cell-1-wing-2-p449",
      "cell-1-wing-2-p450",
      "cell-1-wing-2-p451",
      "cell-1-wing-3-p452",
      "cell-1-wing-3-p453",
      "cell-1-wing-3-p454",
      "cell-1-wing-3-p455",
      "cell-1-wing-3-p456",
      "cell-1-wing-3-p457",
      "cell-1-wing-3-p458",
      "cell-1-wing-3-p459",
      "cell-1-console-p460",
      "cell-1-console-p461",
      "cell-1-console-p462",
      "cell-1-console-p463",
      "cell-1-console-p464",
      "cell-1-console-p465",
      "cell-1-console-p466",
      "cell-1-console-p467",
      "cell-1-magazine-p468",
      "cell-1-magazine-p469",
      "cell-1-magazine-p470",
      "cell-1-magazine-p471",
      "cell-1-magazine-p472",
      "cell-1-magazine-p473",
      "cell-1-magazine-p474",
      "cell-1-magazine-p475",
      "cell-1-magazine-p476",
      "cell-1-magazine-p477",
      "cell-1-magazine-p478",
      "cell-1-magazine-p479",
      "cell-1-magazine-p480",
      "cell-1-magazine-p481",
      "cell-1-magazine-p482",
      "cell-1-magazine-p483",
      "cell-1-magazine-p484",
      "cell-1-magazine-p485",
      "cell-1-magazine-p486",
      "cell-1-magazine-p487",
      "cell-1-magazine-p488",
      "cell-1-magazine-p489",
      "cell-1-magazine-p490",
      "cell-1-magazine-p491",
      "cell-1-magazine-p492",
      "cell-1-magazine-p493",
      "cell-1-magazine-p494",
      "cell-1-magazine-p495",
      "cell-1-magazine-p496",
      "cell-1-magazine-p497",
      "cell-1-magazine-p498",
      "cell-1-magazine-p499",
      "cell-1-magazine-p500",
      "cell-1-magazine-p501",
      "cell-1-magazine-p502",
      "cell-1-magazine-p503",
      "cell-1-magazine-p504",
      "cell-1-magazine-p505",
      "cell-1-magazine-p506",
      "cell-1-magazine-p507",
      "cell-1-magazine-p508",
      "cell-1-magazine-p509",
      "cell-1-magazine-p510",
      "cell-1-magazine-p511",
      "cell-1-magazine-p512",
      "cell-1-magazine-p513",
      "cell-1-magazine-p514",
      "cell-1-magazine-p515",
      "cell-1-magazine-p516",
      "cell-1-magazine-p517",
      "cell-1-magazine-p518",
      "cell-1-magazine-p519",
      "cell-1-magazine-p520",
      "cell-1-magazine-p521",
      "cell-1-magazine-p522",
      "cell-1-magazine-p523",
      "cell-1-magazine-p524",
      "cell-1-magazine-p525",
      "cell-1-drawer-p526",
      "cell-1-drawer-p527",
      "cell-1-drawer-p528",
      "cell-1-drawer-p529",
      "cell-1-drawer-p530",
      "cell-1-drawer-p531",
      "cell-2-shuttle-p532",
      "cell-2-shuttle-p533",
      "cell-2-shuttle-p534",
      "cell-2-shuttle-p535",
      "cell-2-shuttle-p536",
      "cell-2-shuttle-p537",
      "cell-2-shuttle-p538",
      "cell-2-shuttle-p539",
      "cell-2-shuttle-p540",
      "cell-2-shuttle-p541",
      "cell-2-shuttle-p542",
      "cell-2-shuttle-p543",
      "cell-2-shuttle-p544",
      "cell-2-shuttle-p545",
      "cell-2-shuttle-p546",
      "cell-2-shuttle-p547",
      "cell-2-shuttle-p548",
      "cell-2-shuttle-p549",
      "cell-2-shuttle-p550",
      "cell-2-shuttle-p551",
      "cell-2-shuttle-p552",
      "cell-2-shuttle-p553",
      "cell-2-shuttle-p554",
      "cell-2-shuttle-p555",
      "cell-2-shuttle-p556",
      "cell-2-shuttle-p557",
      "cell-2-shuttle-p558",
      "cell-2-shuttle-p559",
      "cell-2-shuttle-p560",
      "cell-2-shuttle-p561",
      "cell-2-shuttle-p562",
      "cell-2-shuttle-p563",
      "cell-2-shuttle-p564",
      "cell-2-shuttle-p565",
      "cell-2-shuttle-p566",
      "cell-2-shuttle-p567",
      "cell-2-shuttle-p568",
      "cell-2-shuttle-p569",
      "cell-2-shuttle-p570",
      "cell-2-shuttle-p571",
      "cell-2-shuttle-p572",
      "cell-2-shuttle-p573",
      "cell-2-shuttle-p574",
      "cell-2-shuttle-p575",
      "cell-2-shuttle-p576",
      "cell-2-shuttle-p577",
      "cell-2-shuttle-p578",
      "cell-2-shuttle-p579",
      "cell-2-mount-p580",
      "cell-2-mount-p581",
      "cell-2-mount-p582",
      "cell-2-mount-p583",
      "cell-2-mount-p584",
      "cell-2-mount-p585",
      "cell-2-mount-p586",
      "cell-2-mount-p587",
      "cell-2-mount-p588",
      "cell-2-mount-p589",
      "cell-2-mount-p590",
      "cell-2-mount-p591",
      "cell-2-mount-p592",
      "cell-2-mount-p593",
      "cell-2-mount-p594",
      "cell-2-mount-p595",
      "cell-2-mount-p596",
      "cell-2-mount-p597",
      "cell-2-mount-p598",
      "cell-2-mount-p599",
      "cell-2-mount-p600",
      "cell-2-mount-p601",
      "cell-2-mount-p602",
      "cell-2-mount-p603",
      "cell-2-mount-p604",
      "cell-2-mount-p605",
      "cell-2-mount-p606",
      "cell-2-mount-p607",
      "cell-2-mount-p608",
      "cell-2-mount-p609",
      "cell-2-hub-p610",
      "cell-2-probe-0-p611",
      "cell-2-probe-0-p612",
      "cell-2-probe-0-p613",
      "cell-2-probe-0-p614",
      "cell-2-console-p615",
      "cell-2-console-p616",
      "cell-2-console-p617",
      "cell-2-console-p618",
      "cell-2-console-p619",
      "cell-2-console-p620",
      "cell-2-console-p621",
      "cell-2-console-p622",
      "cell-2-magazine-p623",
      "cell-2-magazine-p624",
      "cell-2-magazine-p625",
      "cell-2-magazine-p626",
      "cell-2-magazine-p627",
      "cell-2-magazine-p628",
      "cell-2-magazine-p629",
      "cell-2-magazine-p630",
      "cell-2-magazine-p631",
      "cell-2-magazine-p632",
      "cell-2-magazine-p633",
      "cell-2-magazine-p634",
      "cell-2-magazine-p635",
      "cell-2-magazine-p636",
      "cell-2-magazine-p637",
      "cell-2-magazine-p638",
      "cell-2-magazine-p639",
      "cell-2-magazine-p640",
      "cell-2-magazine-p641",
      "cell-2-magazine-p642",
      "cell-2-magazine-p643",
      "cell-2-magazine-p644",
      "cell-2-magazine-p645",
      "cell-2-magazine-p646",
      "cell-2-magazine-p647",
      "cell-2-magazine-p648",
      "cell-2-magazine-p649",
      "cell-2-magazine-p650",
      "cell-2-magazine-p651",
      "cell-2-magazine-p652",
      "cell-2-magazine-p653",
      "cell-2-magazine-p654",
      "cell-2-magazine-p655",
      "cell-2-magazine-p656",
      "cell-2-magazine-p657",
      "cell-2-magazine-p658",
      "cell-2-magazine-p659",
      "cell-2-magazine-p660",
      "cell-2-magazine-p661",
      "cell-2-magazine-p662",
      "cell-2-magazine-p663",
      "cell-2-magazine-p664",
      "cell-2-magazine-p665",
      "cell-2-magazine-p666",
      "cell-2-magazine-p667",
      "cell-2-magazine-p668",
      "cell-2-magazine-p669",
      "cell-2-magazine-p670",
      "cell-2-magazine-p671",
      "cell-2-magazine-p672",
      "cell-2-magazine-p673",
      "cell-2-magazine-p674",
      "cell-2-magazine-p675",
      "cell-2-magazine-p676",
      "cell-2-magazine-p677",
      "cell-2-magazine-p678",
      "cell-2-magazine-p679",
      "cell-2-magazine-p680",
      "cell-2-drawer-p681",
      "cell-2-drawer-p682",
      "cell-2-drawer-p683",
      "cell-2-drawer-p684",
      "cell-2-drawer-p685",
      "cell-2-drawer-p686",
      "shared-inspection-mast-p687",
      "shared-inspection-mast-p688",
      "shared-inspection-mast-p689",
      "shared-inspection-mast-p690",
      "shared-inspection-mast-p691",
      "shared-inspection-mast-p692",
      "shared-inspection-mast-p693",
      "shared-inspection-mast-p694",
      "shared-inspection-mast-p695",
      "shared-inspection-mast-p696",
      "shared-inspection-mast-p697",
      "shared-inspection-mast-p698",
      "shared-inspection-mast-p699",
      "shared-scanner-p700",
      "shared-scanner-p701"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 安全拆除（h3-exp-d4-cradle-1-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","cell-0-shuttle","cell-0-mount","cell-0-yoke","cell-0-cradle","cell-0-optic","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-hub","cell-1-wing-0","cell-1-wing-1","cell-1-wing-2","cell-1-wing-3","cell-1-console","cell-1-magazine","cell-1-drawer","cell-2-shuttle","cell-2-mount","cell-2-hub","cell-2-probe-0","cell-2-console","cell-2-magazine","cell-2-drawer","shared-inspection-mast","shared-scanner"]
- C：["cell-0-console","cell-0-drawer","cell-0-optic","cell-1-console","cell-1-drawer","cell-1-wing-0","cell-1-wing-1","cell-1-wing-2","cell-1-wing-3","cell-2-console","cell-2-drawer","cell-2-probe-0","shared-scanner"]
- D：["foundation"]

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          -13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-yoke-joint",
        "name": "cell-0-yoke interface",
        "parent": "cell-0-mount",
        "child": "cell-0-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          0,
          -1.4250000000000003,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-cradle-joint",
        "name": "cell-0-cradle interface",
        "parent": "cell-0-yoke",
        "child": "cell-0-cradle",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2749999999999995,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-optic-joint",
        "name": "cell-0-optic interface",
        "parent": "cell-0-cradle",
        "child": "cell-0-optic",
        "type": "fixed",
        "anchorParent": [
          0,
          1.25,
          0
        ],
        "anchorChild": [
          0,
          -0.09999999999999964,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-drawer-joint",
        "name": "cell-0-drawer interface",
        "parent": "cell-0-magazine",
        "child": "cell-0-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-shuttle-joint",
        "name": "cell-1-shuttle interface",
        "parent": "foundation",
        "child": "cell-1-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-mount-joint",
        "name": "cell-1-mount interface",
        "parent": "cell-1-shuttle",
        "child": "cell-1-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-hub-joint",
        "name": "cell-1-hub interface",
        "parent": "cell-1-mount",
        "child": "cell-1-hub",
        "type": "fixed",
        "anchorParent": [
          0,
          1.4499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-wing-0-joint",
        "name": "cell-1-wing-0 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-0",
        "type": "revolute",
        "anchorParent": [
          2.5,
          1.6000000000000005,
          0
        ],
        "anchorChild": [
          0,
          0.07750000000000057,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-1-joint",
        "name": "cell-1-wing-1 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-1",
        "type": "revolute",
        "anchorParent": [
          1.5308084989341916e-16,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          -1.3452603800354324e-17,
          0.07749999999999968,
          0
        ],
        "axis": [
          -1,
          0,
          6.123233995736766e-17
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-2-joint",
        "name": "cell-1-wing-2 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-2",
        "type": "revolute",
        "anchorParent": [
          -2.5,
          1.8399999999999999,
          3.061616997868383e-16
        ],
        "anchorChild": [
          0,
          0.07749999999999968,
          -2.6905207600708648e-17
        ],
        "axis": [
          -1.2246467991473532e-16,
          0,
          -1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-3-joint",
        "name": "cell-1-wing-3 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-3",
        "type": "revolute",
        "anchorParent": [
          -4.592425496802574e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          -1.515333983019478e-17,
          0.07750000000000057,
          0
        ],
        "axis": [
          1,
          0,
          -1.8369701987210297e-16
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-drawer-joint",
        "name": "cell-1-drawer interface",
        "parent": "cell-1-magazine",
        "child": "cell-1-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-shuttle-joint",
        "name": "cell-2-shuttle interface",
        "parent": "foundation",
        "child": "cell-2-shuttle",
        "type": "prismatic",
        "anchorParent": [
          13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-mount-joint",
        "name": "cell-2-mount interface",
        "parent": "cell-2-shuttle",
        "child": "cell-2-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-hub-joint",
        "name": "cell-2-hub interface",
        "parent": "cell-2-mount",
        "child": "cell-2-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-2-probe-0-joint",
        "name": "cell-2-probe-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772923,
          0
        ],
        "axis": [
          0.6,
          0.8,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-magazine-joint",
        "name": "cell-2-magazine interface",
        "parent": "foundation",
        "child": "cell-2-magazine",
        "type": "fixed",
        "anchorParent": [
          13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-drawer-joint",
        "name": "cell-2-drawer interface",
        "parent": "cell-2-magazine",
        "child": "cell-2-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "shared-inspection-mast-joint",
        "name": "shared-inspection-mast interface",
        "parent": "foundation",
        "child": "shared-inspection-mast",
        "type": "fixed",
        "anchorParent": [
          0,
          0.7999999999999999,
          11
        ],
        "anchorChild": [
          0,
          -2.5875,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shared-scanner-joint",
        "name": "shared-scanner interface",
        "parent": "shared-inspection-mast",
        "child": "shared-scanner",
        "type": "revolute",
        "anchorParent": [
          0,
          3.2125,
          0
        ],
        "anchorChild": [
          0,
          -0.21249999999999947,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ],
    "modules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-yoke",
      "cell-0-cradle",
      "cell-0-optic",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-hub",
      "cell-1-wing-0",
      "cell-1-wing-1",
      "cell-1-wing-2",
      "cell-1-wing-3",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-probe-0",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 替换选择（h3-exp-d4-cradle-1-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-2
- B：stock-0
- C：stock-1
- D：stock-3

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 8,
        "mass": 1.9
      },
      {
        "id": "stock-1",
        "cost": 6,
        "stiffness": 10,
        "mass": 1
      },
      {
        "id": "stock-2",
        "cost": 2,
        "stiffness": 11,
        "mass": 1.9
      },
      {
        "id": "stock-3",
        "cost": 4,
        "stiffness": 11,
        "mass": 1.5
      }
    ],
    "maxCost": 7
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 平移纠偏（h3-exp-d4-cradle-1-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,2,0]
- C：[-4,0,2]
- D：[4,0,-2]

```json
{
  "input": {
    "delta": [
      4,
      0,
      -2
    ],
    "target": "cell-0-optic"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-exp-d4-cradle-1-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：-180
- B：-90
- C：90
- D：0

```json
{
  "input": {
    "module": "cell-0-optic",
    "currentYaw": 270,
    "targetYaw": 180
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 下一步放置（h3-exp-d4-cradle-1-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["cell-1-wing-2","cell-1-wing-3","cell-1-console","cell-1-magazine","cell-1-drawer","cell-2-shuttle","cell-2-mount","cell-2-hub","cell-2-probe-0","cell-2-console","cell-2-magazine","cell-2-drawer","shared-inspection-mast","shared-scanner"]
- B：["cell-1-console","cell-1-magazine","cell-1-wing-2","cell-1-wing-3","cell-2-console","cell-2-magazine","cell-2-shuttle","shared-inspection-mast"]
- C：[]
- D：["foundation","cell-0-shuttle","cell-0-mount","cell-0-yoke","cell-0-cradle","cell-0-optic","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-hub","cell-1-wing-0","cell-1-wing-1"]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-yoke",
      "cell-0-cradle",
      "cell-0-optic",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-hub",
      "cell-1-wing-0",
      "cell-1-wing-1"
    ],
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          -13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-yoke-joint",
        "name": "cell-0-yoke interface",
        "parent": "cell-0-mount",
        "child": "cell-0-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          0,
          -1.4250000000000003,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-cradle-joint",
        "name": "cell-0-cradle interface",
        "parent": "cell-0-yoke",
        "child": "cell-0-cradle",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2749999999999995,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-optic-joint",
        "name": "cell-0-optic interface",
        "parent": "cell-0-cradle",
        "child": "cell-0-optic",
        "type": "fixed",
        "anchorParent": [
          0,
          1.25,
          0
        ],
        "anchorChild": [
          0,
          -0.09999999999999964,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-drawer-joint",
        "name": "cell-0-drawer interface",
        "parent": "cell-0-magazine",
        "child": "cell-0-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-shuttle-joint",
        "name": "cell-1-shuttle interface",
        "parent": "foundation",
        "child": "cell-1-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-mount-joint",
        "name": "cell-1-mount interface",
        "parent": "cell-1-shuttle",
        "child": "cell-1-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-hub-joint",
        "name": "cell-1-hub interface",
        "parent": "cell-1-mount",
        "child": "cell-1-hub",
        "type": "fixed",
        "anchorParent": [
          0,
          1.4499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-wing-0-joint",
        "name": "cell-1-wing-0 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-0",
        "type": "revolute",
        "anchorParent": [
          2.5,
          1.6000000000000005,
          0
        ],
        "anchorChild": [
          0,
          0.07750000000000057,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-1-joint",
        "name": "cell-1-wing-1 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-1",
        "type": "revolute",
        "anchorParent": [
          1.5308084989341916e-16,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          -1.3452603800354324e-17,
          0.07749999999999968,
          0
        ],
        "axis": [
          -1,
          0,
          6.123233995736766e-17
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-2-joint",
        "name": "cell-1-wing-2 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-2",
        "type": "revolute",
        "anchorParent": [
          -2.5,
          1.8399999999999999,
          3.061616997868383e-16
        ],
        "anchorChild": [
          0,
          0.07749999999999968,
          -2.6905207600708648e-17
        ],
        "axis": [
          -1.2246467991473532e-16,
          0,
          -1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-3-joint",
        "name": "cell-1-wing-3 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-3",
        "type": "revolute",
        "anchorParent": [
          -4.592425496802574e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          -1.515333983019478e-17,
          0.07750000000000057,
          0
        ],
        "axis": [
          1,
          0,
          -1.8369701987210297e-16
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-drawer-joint",
        "name": "cell-1-drawer interface",
        "parent": "cell-1-magazine",
        "child": "cell-1-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-shuttle-joint",
        "name": "cell-2-shuttle interface",
        "parent": "foundation",
        "child": "cell-2-shuttle",
        "type": "prismatic",
        "anchorParent": [
          13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-mount-joint",
        "name": "cell-2-mount interface",
        "parent": "cell-2-shuttle",
        "child": "cell-2-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-hub-joint",
        "name": "cell-2-hub interface",
        "parent": "cell-2-mount",
        "child": "cell-2-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-2-probe-0-joint",
        "name": "cell-2-probe-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772923,
          0
        ],
        "axis": [
          0.6,
          0.8,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-magazine-joint",
        "name": "cell-2-magazine interface",
        "parent": "foundation",
        "child": "cell-2-magazine",
        "type": "fixed",
        "anchorParent": [
          13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-drawer-joint",
        "name": "cell-2-drawer interface",
        "parent": "cell-2-magazine",
        "child": "cell-2-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "shared-inspection-mast-joint",
        "name": "shared-inspection-mast interface",
        "parent": "foundation",
        "child": "shared-inspection-mast",
        "type": "fixed",
        "anchorParent": [
          0,
          0.7999999999999999,
          11
        ],
        "anchorChild": [
          0,
          -2.5875,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shared-scanner-joint",
        "name": "shared-scanner interface",
        "parent": "shared-inspection-mast",
        "child": "shared-scanner",
        "type": "revolute",
        "anchorParent": [
          0,
          3.2125,
          0
        ],
        "anchorChild": [
          0,
          -0.21249999999999947,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ],
    "modules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-yoke",
      "cell-0-cradle",
      "cell-0-optic",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-hub",
      "cell-1-wing-0",
      "cell-1-wing-1",
      "cell-1-wing-2",
      "cell-1-wing-3",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-probe-0",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 库存核算（h3-exp-d4-cradle-1-inventory）

备件库有 9 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：8
- B：6
- C：10
- D：7

```json
{
  "input": {
    "available": 9,
    "required": 2
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 子装配边界（h3-exp-d4-cradle-1-boundary）

隔离 cell-0-optic 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["cell-0-cradle-joint"]
- B：["cell-0-optic-joint"]
- C：[]
- D：["cell-0-shuttle-joint","cell-0-mount-joint","cell-0-yoke-joint","cell-0-cradle-joint","cell-0-optic-joint","cell-0-console-joint","cell-0-magazine-joint","cell-0-drawer-joint","cell-1-shuttle-joint","cell-1-mount-joint","cell-1-hub-joint","cell-1-wing-0-joint","cell-1-wing-1-joint","cell-1-wing-2-joint","cell-1-wing-3-joint","cell-1-console-joint","cell-1-magazine-joint","cell-1-drawer-joint","cell-2-shuttle-joint","cell-2-mount-joint","cell-2-hub-joint","cell-2-probe-0-joint","cell-2-console-joint","cell-2-magazine-joint","cell-2-drawer-joint","shared-inspection-mast-joint","shared-scanner-joint"]

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          -13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-yoke-joint",
        "name": "cell-0-yoke interface",
        "parent": "cell-0-mount",
        "child": "cell-0-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          0,
          -1.4250000000000003,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-cradle-joint",
        "name": "cell-0-cradle interface",
        "parent": "cell-0-yoke",
        "child": "cell-0-cradle",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2749999999999995,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-optic-joint",
        "name": "cell-0-optic interface",
        "parent": "cell-0-cradle",
        "child": "cell-0-optic",
        "type": "fixed",
        "anchorParent": [
          0,
          1.25,
          0
        ],
        "anchorChild": [
          0,
          -0.09999999999999964,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-drawer-joint",
        "name": "cell-0-drawer interface",
        "parent": "cell-0-magazine",
        "child": "cell-0-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-shuttle-joint",
        "name": "cell-1-shuttle interface",
        "parent": "foundation",
        "child": "cell-1-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-mount-joint",
        "name": "cell-1-mount interface",
        "parent": "cell-1-shuttle",
        "child": "cell-1-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-hub-joint",
        "name": "cell-1-hub interface",
        "parent": "cell-1-mount",
        "child": "cell-1-hub",
        "type": "fixed",
        "anchorParent": [
          0,
          1.4499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-wing-0-joint",
        "name": "cell-1-wing-0 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-0",
        "type": "revolute",
        "anchorParent": [
          2.5,
          1.6000000000000005,
          0
        ],
        "anchorChild": [
          0,
          0.07750000000000057,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-1-joint",
        "name": "cell-1-wing-1 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-1",
        "type": "revolute",
        "anchorParent": [
          1.5308084989341916e-16,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          -1.3452603800354324e-17,
          0.07749999999999968,
          0
        ],
        "axis": [
          -1,
          0,
          6.123233995736766e-17
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-2-joint",
        "name": "cell-1-wing-2 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-2",
        "type": "revolute",
        "anchorParent": [
          -2.5,
          1.8399999999999999,
          3.061616997868383e-16
        ],
        "anchorChild": [
          0,
          0.07749999999999968,
          -2.6905207600708648e-17
        ],
        "axis": [
          -1.2246467991473532e-16,
          0,
          -1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-3-joint",
        "name": "cell-1-wing-3 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-3",
        "type": "revolute",
        "anchorParent": [
          -4.592425496802574e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          -1.515333983019478e-17,
          0.07750000000000057,
          0
        ],
        "axis": [
          1,
          0,
          -1.8369701987210297e-16
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-drawer-joint",
        "name": "cell-1-drawer interface",
        "parent": "cell-1-magazine",
        "child": "cell-1-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-shuttle-joint",
        "name": "cell-2-shuttle interface",
        "parent": "foundation",
        "child": "cell-2-shuttle",
        "type": "prismatic",
        "anchorParent": [
          13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-mount-joint",
        "name": "cell-2-mount interface",
        "parent": "cell-2-shuttle",
        "child": "cell-2-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-hub-joint",
        "name": "cell-2-hub interface",
        "parent": "cell-2-mount",
        "child": "cell-2-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-2-probe-0-joint",
        "name": "cell-2-probe-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772923,
          0
        ],
        "axis": [
          0.6,
          0.8,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-magazine-joint",
        "name": "cell-2-magazine interface",
        "parent": "foundation",
        "child": "cell-2-magazine",
        "type": "fixed",
        "anchorParent": [
          13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-drawer-joint",
        "name": "cell-2-drawer interface",
        "parent": "cell-2-magazine",
        "child": "cell-2-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "shared-inspection-mast-joint",
        "name": "shared-inspection-mast interface",
        "parent": "foundation",
        "child": "shared-inspection-mast",
        "type": "fixed",
        "anchorParent": [
          0,
          0.7999999999999999,
          11
        ],
        "anchorChild": [
          0,
          -2.5875,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shared-scanner-joint",
        "name": "shared-scanner interface",
        "parent": "shared-inspection-mast",
        "child": "shared-scanner",
        "type": "revolute",
        "anchorParent": [
          0,
          3.2125,
          0
        ],
        "anchorChild": [
          0,
          -0.21249999999999947,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ],
    "target": "cell-0-optic"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 最小干预（h3-exp-d4-cradle-1-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：0

```json
{
  "input": {
    "module": "cell-0-optic"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 全过程依赖（h3-exp-d4-cradle-1-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：0
- B：-1
- C：1
- D：27

```json
{
  "input": {
    "order": [
      "shared-inspection-mast",
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-yoke",
      "cell-0-cradle",
      "cell-0-optic",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-hub",
      "cell-1-wing-0",
      "cell-1-wing-1",
      "cell-1-wing-2",
      "cell-1-wing-3",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-probe-0",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "shared-scanner"
    ],
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          -13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-yoke-joint",
        "name": "cell-0-yoke interface",
        "parent": "cell-0-mount",
        "child": "cell-0-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          0,
          -1.4250000000000003,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-cradle-joint",
        "name": "cell-0-cradle interface",
        "parent": "cell-0-yoke",
        "child": "cell-0-cradle",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2749999999999995,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-optic-joint",
        "name": "cell-0-optic interface",
        "parent": "cell-0-cradle",
        "child": "cell-0-optic",
        "type": "fixed",
        "anchorParent": [
          0,
          1.25,
          0
        ],
        "anchorChild": [
          0,
          -0.09999999999999964,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-drawer-joint",
        "name": "cell-0-drawer interface",
        "parent": "cell-0-magazine",
        "child": "cell-0-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-shuttle-joint",
        "name": "cell-1-shuttle interface",
        "parent": "foundation",
        "child": "cell-1-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-mount-joint",
        "name": "cell-1-mount interface",
        "parent": "cell-1-shuttle",
        "child": "cell-1-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-hub-joint",
        "name": "cell-1-hub interface",
        "parent": "cell-1-mount",
        "child": "cell-1-hub",
        "type": "fixed",
        "anchorParent": [
          0,
          1.4499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-wing-0-joint",
        "name": "cell-1-wing-0 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-0",
        "type": "revolute",
        "anchorParent": [
          2.5,
          1.6000000000000005,
          0
        ],
        "anchorChild": [
          0,
          0.07750000000000057,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-1-joint",
        "name": "cell-1-wing-1 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-1",
        "type": "revolute",
        "anchorParent": [
          1.5308084989341916e-16,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          -1.3452603800354324e-17,
          0.07749999999999968,
          0
        ],
        "axis": [
          -1,
          0,
          6.123233995736766e-17
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-2-joint",
        "name": "cell-1-wing-2 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-2",
        "type": "revolute",
        "anchorParent": [
          -2.5,
          1.8399999999999999,
          3.061616997868383e-16
        ],
        "anchorChild": [
          0,
          0.07749999999999968,
          -2.6905207600708648e-17
        ],
        "axis": [
          -1.2246467991473532e-16,
          0,
          -1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-3-joint",
        "name": "cell-1-wing-3 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-3",
        "type": "revolute",
        "anchorParent": [
          -4.592425496802574e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          -1.515333983019478e-17,
          0.07750000000000057,
          0
        ],
        "axis": [
          1,
          0,
          -1.8369701987210297e-16
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-drawer-joint",
        "name": "cell-1-drawer interface",
        "parent": "cell-1-magazine",
        "child": "cell-1-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-shuttle-joint",
        "name": "cell-2-shuttle interface",
        "parent": "foundation",
        "child": "cell-2-shuttle",
        "type": "prismatic",
        "anchorParent": [
          13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-mount-joint",
        "name": "cell-2-mount interface",
        "parent": "cell-2-shuttle",
        "child": "cell-2-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-hub-joint",
        "name": "cell-2-hub interface",
        "parent": "cell-2-mount",
        "child": "cell-2-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-2-probe-0-joint",
        "name": "cell-2-probe-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772923,
          0
        ],
        "axis": [
          0.6,
          0.8,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-magazine-joint",
        "name": "cell-2-magazine interface",
        "parent": "foundation",
        "child": "cell-2-magazine",
        "type": "fixed",
        "anchorParent": [
          13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-drawer-joint",
        "name": "cell-2-drawer interface",
        "parent": "cell-2-magazine",
        "child": "cell-2-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "shared-inspection-mast-joint",
        "name": "shared-inspection-mast interface",
        "parent": "foundation",
        "child": "shared-inspection-mast",
        "type": "fixed",
        "anchorParent": [
          0,
          0.7999999999999999,
          11
        ],
        "anchorChild": [
          0,
          -2.5875,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shared-scanner-joint",
        "name": "shared-scanner interface",
        "parent": "shared-inspection-mast",
        "child": "shared-scanner",
        "type": "revolute",
        "anchorParent": [
          0,
          3.2125,
          0
        ],
        "anchorChild": [
          0,
          -0.21249999999999947,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 连续维修路径（h3-exp-d4-cradle-1-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-0
- B：path-1
- C：path-2

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          20.98,
          5.949999999999999,
          0
        ],
        "end": [
          -13,
          5.949999999999999,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.14788109064102173
      },
      {
        "id": "path-1",
        "start": [
          -13,
          11.524999999999999,
          0
        ],
        "end": [
          -13,
          5.949999999999999,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": true,
        "timeOfImpact": null
      },
      {
        "id": "path-2",
        "start": [
          -13,
          5.949999999999999,
          15.65
        ],
        "end": [
          -13,
          5.949999999999999,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": true,
        "timeOfImpact": null
      }
    ],
    "simulator": "stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration"
  },
  "answer": {
    "choiceIds": [
      "B",
      "C"
    ]
  }
}
```

### 支撑反事实（h3-exp-d4-cradle-1-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["foundation","cell-0-shuttle","cell-0-mount","cell-0-yoke","cell-0-cradle","cell-0-optic","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-hub","cell-1-wing-0","cell-1-wing-1","cell-1-wing-2","cell-1-wing-3","cell-1-console","cell-1-magazine","cell-1-drawer","cell-2-shuttle","cell-2-mount","cell-2-hub","cell-2-probe-0","cell-2-console","cell-2-magazine","cell-2-drawer","shared-inspection-mast","shared-scanner"]
- C：["cell-0-cradle","cell-0-mount","cell-0-optic","cell-0-yoke"]
- D：["cell-0-shuttle"]

```json
{
  "input": {
    "removed": "cell-0-shuttle",
    "roots": [
      "foundation"
    ],
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          -13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-yoke-joint",
        "name": "cell-0-yoke interface",
        "parent": "cell-0-mount",
        "child": "cell-0-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          0,
          -1.4250000000000003,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-cradle-joint",
        "name": "cell-0-cradle interface",
        "parent": "cell-0-yoke",
        "child": "cell-0-cradle",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2749999999999995,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-optic-joint",
        "name": "cell-0-optic interface",
        "parent": "cell-0-cradle",
        "child": "cell-0-optic",
        "type": "fixed",
        "anchorParent": [
          0,
          1.25,
          0
        ],
        "anchorChild": [
          0,
          -0.09999999999999964,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-drawer-joint",
        "name": "cell-0-drawer interface",
        "parent": "cell-0-magazine",
        "child": "cell-0-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-shuttle-joint",
        "name": "cell-1-shuttle interface",
        "parent": "foundation",
        "child": "cell-1-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-mount-joint",
        "name": "cell-1-mount interface",
        "parent": "cell-1-shuttle",
        "child": "cell-1-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-hub-joint",
        "name": "cell-1-hub interface",
        "parent": "cell-1-mount",
        "child": "cell-1-hub",
        "type": "fixed",
        "anchorParent": [
          0,
          1.4499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-wing-0-joint",
        "name": "cell-1-wing-0 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-0",
        "type": "revolute",
        "anchorParent": [
          2.5,
          1.6000000000000005,
          0
        ],
        "anchorChild": [
          0,
          0.07750000000000057,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-1-joint",
        "name": "cell-1-wing-1 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-1",
        "type": "revolute",
        "anchorParent": [
          1.5308084989341916e-16,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          -1.3452603800354324e-17,
          0.07749999999999968,
          0
        ],
        "axis": [
          -1,
          0,
          6.123233995736766e-17
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-2-joint",
        "name": "cell-1-wing-2 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-2",
        "type": "revolute",
        "anchorParent": [
          -2.5,
          1.8399999999999999,
          3.061616997868383e-16
        ],
        "anchorChild": [
          0,
          0.07749999999999968,
          -2.6905207600708648e-17
        ],
        "axis": [
          -1.2246467991473532e-16,
          0,
          -1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-3-joint",
        "name": "cell-1-wing-3 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-3",
        "type": "revolute",
        "anchorParent": [
          -4.592425496802574e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          -1.515333983019478e-17,
          0.07750000000000057,
          0
        ],
        "axis": [
          1,
          0,
          -1.8369701987210297e-16
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-drawer-joint",
        "name": "cell-1-drawer interface",
        "parent": "cell-1-magazine",
        "child": "cell-1-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-shuttle-joint",
        "name": "cell-2-shuttle interface",
        "parent": "foundation",
        "child": "cell-2-shuttle",
        "type": "prismatic",
        "anchorParent": [
          13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-mount-joint",
        "name": "cell-2-mount interface",
        "parent": "cell-2-shuttle",
        "child": "cell-2-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-hub-joint",
        "name": "cell-2-hub interface",
        "parent": "cell-2-mount",
        "child": "cell-2-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-2-probe-0-joint",
        "name": "cell-2-probe-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772923,
          0
        ],
        "axis": [
          0.6,
          0.8,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-magazine-joint",
        "name": "cell-2-magazine interface",
        "parent": "foundation",
        "child": "cell-2-magazine",
        "type": "fixed",
        "anchorParent": [
          13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-drawer-joint",
        "name": "cell-2-drawer interface",
        "parent": "cell-2-magazine",
        "child": "cell-2-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "shared-inspection-mast-joint",
        "name": "shared-inspection-mast interface",
        "parent": "foundation",
        "child": "shared-inspection-mast",
        "type": "fixed",
        "anchorParent": [
          0,
          0.7999999999999999,
          11
        ],
        "anchorChild": [
          0,
          -2.5875,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shared-scanner-joint",
        "name": "shared-scanner interface",
        "parent": "shared-inspection-mast",
        "child": "shared-scanner",
        "type": "revolute",
        "anchorParent": [
          0,
          3.2125,
          0
        ],
        "anchorChild": [
          0,
          -0.21249999999999947,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ],
    "modules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-yoke",
      "cell-0-cradle",
      "cell-0-optic",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-hub",
      "cell-1-wing-0",
      "cell-1-wing-1",
      "cell-1-wing-2",
      "cell-1-wing-3",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-probe-0",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-exp-d4-cradle-1-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.0082
- B：0.2082
- C：0
- D：1.0082

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.00815147412073568
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0001045917746092399
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.00004865554786635296
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.00004863739387877562
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.000048637390137489794
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0000486373901367189
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00004863739013671875
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00004863739013671875
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.00004863739013671875
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.00004863739013671875
      },
      {
        "time": 1,
        "displacement": 0.00004863739013671875
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.000012291248332882664,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节限位推理（h3-exp-d4-cradle-1-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-0.6
- B：0
- C：-1.1
- D：1.1

```json
{
  "input": {
    "joint": "cell-0-cradle-joint",
    "limits": [
      -0.6,
      0.6
    ],
    "units": "radians"
  },
  "answer": {
    "choiceIds": [
      "A",
      "B"
    ]
  }
}
```

### 约束故障诊断（h3-exp-d4-cradle-1-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：cell-0-shuttle-joint
- B：cell-0-mount-joint
- C：cell-0-yoke-joint
- D：cell-0-optic-joint

```json
{
  "input": {
    "endpoints": [
      "cell-0-cradle",
      "cell-0-optic"
    ],
    "type": "fixed",
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          -13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "cell-0-shuttle",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-yoke-joint",
        "name": "cell-0-yoke interface",
        "parent": "cell-0-mount",
        "child": "cell-0-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          0,
          -1.4250000000000003,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-cradle-joint",
        "name": "cell-0-cradle interface",
        "parent": "cell-0-yoke",
        "child": "cell-0-cradle",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2749999999999995,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-optic-joint",
        "name": "cell-0-optic interface",
        "parent": "cell-0-cradle",
        "child": "cell-0-optic",
        "type": "fixed",
        "anchorParent": [
          0,
          1.25,
          0
        ],
        "anchorChild": [
          0,
          -0.09999999999999964,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-drawer-joint",
        "name": "cell-0-drawer interface",
        "parent": "cell-0-magazine",
        "child": "cell-0-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-shuttle-joint",
        "name": "cell-1-shuttle interface",
        "parent": "foundation",
        "child": "cell-1-shuttle",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-1-mount-joint",
        "name": "cell-1-mount interface",
        "parent": "cell-1-shuttle",
        "child": "cell-1-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-hub-joint",
        "name": "cell-1-hub interface",
        "parent": "cell-1-mount",
        "child": "cell-1-hub",
        "type": "fixed",
        "anchorParent": [
          0,
          1.4499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-wing-0-joint",
        "name": "cell-1-wing-0 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-0",
        "type": "revolute",
        "anchorParent": [
          2.5,
          1.6000000000000005,
          0
        ],
        "anchorChild": [
          0,
          0.07750000000000057,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-1-joint",
        "name": "cell-1-wing-1 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-1",
        "type": "revolute",
        "anchorParent": [
          1.5308084989341916e-16,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          -1.3452603800354324e-17,
          0.07749999999999968,
          0
        ],
        "axis": [
          -1,
          0,
          6.123233995736766e-17
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-2-joint",
        "name": "cell-1-wing-2 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-2",
        "type": "revolute",
        "anchorParent": [
          -2.5,
          1.8399999999999999,
          3.061616997868383e-16
        ],
        "anchorChild": [
          0,
          0.07749999999999968,
          -2.6905207600708648e-17
        ],
        "axis": [
          -1.2246467991473532e-16,
          0,
          -1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-wing-3-joint",
        "name": "cell-1-wing-3 interface",
        "parent": "cell-1-hub",
        "child": "cell-1-wing-3",
        "type": "revolute",
        "anchorParent": [
          -4.592425496802574e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          -1.515333983019478e-17,
          0.07750000000000057,
          0
        ],
        "axis": [
          1,
          0,
          -1.8369701987210297e-16
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          0,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-drawer-joint",
        "name": "cell-1-drawer interface",
        "parent": "cell-1-magazine",
        "child": "cell-1-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-shuttle-joint",
        "name": "cell-2-shuttle interface",
        "parent": "foundation",
        "child": "cell-2-shuttle",
        "type": "prismatic",
        "anchorParent": [
          13,
          0.4999999999999999,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-mount-joint",
        "name": "cell-2-mount interface",
        "parent": "cell-2-shuttle",
        "child": "cell-2-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.55,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-hub-joint",
        "name": "cell-2-hub interface",
        "parent": "cell-2-mount",
        "child": "cell-2-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9499999999999997,
          0
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-2-probe-0-joint",
        "name": "cell-2-probe-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772923,
          0
        ],
        "axis": [
          0.6,
          0.8,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          13,
          1.1,
          6
        ],
        "anchorChild": [
          0,
          -0.5775000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-magazine-joint",
        "name": "cell-2-magazine interface",
        "parent": "foundation",
        "child": "cell-2-magazine",
        "type": "fixed",
        "anchorParent": [
          13,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -2.34,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-2-drawer-joint",
        "name": "cell-2-drawer interface",
        "parent": "cell-2-magazine",
        "child": "cell-2-drawer",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.64,
          0
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "shared-inspection-mast-joint",
        "name": "shared-inspection-mast interface",
        "parent": "foundation",
        "child": "shared-inspection-mast",
        "type": "fixed",
        "anchorParent": [
          0,
          0.7999999999999999,
          11
        ],
        "anchorChild": [
          0,
          -2.5875,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shared-scanner-joint",
        "name": "shared-scanner interface",
        "parent": "shared-inspection-mast",
        "child": "shared-scanner",
        "type": "revolute",
        "anchorParent": [
          0,
          3.2125,
          0
        ],
        "anchorChild": [
          0,
          -0.21249999999999947,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "D"
    ]
  }
}
```

### 主动检查收益（h3-exp-d4-cradle-1-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-0
- B：query-1
- C：query-2

```json
{
  "input": {
    "queries": [
      {
        "id": "query-0",
        "cost": 2,
        "returns": [
          0,
          0,
          1,
          1
        ]
      },
      {
        "id": "query-1",
        "cost": 3,
        "returns": [
          0,
          1,
          2,
          3
        ]
      },
      {
        "id": "query-2",
        "cost": 1,
        "returns": [
          0,
          0,
          0,
          1
        ]
      }
    ],
    "module": "cell-0-optic",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "C"
    ]
  }
}
```

### 不确定性与弃答（h3-exp-d4-cradle-1-abstention）

所有相容世界是否允许同一个后续动作？选择继续执行或请求检查。

能力：不确定性与弃答；形式：single-choice；证据：finite-world。

- A：inspect
- B：commit

```json
{
  "input": {
    "worlds": [
      {
        "id": "w0",
        "action": "continue"
      },
      {
        "id": "w1",
        "action": "repair"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 观测后信念更新（h3-exp-d4-cradle-1-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0
- B：0.25
- C：0.5
- D：0.3333333333333333

```json
{
  "input": {
    "module": "cell-0-optic",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "negative",
      "positive",
      "positive",
      "positive"
    ],
    "observed": "positive"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 多目标工程权衡（h3-exp-d4-cradle-1-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-2
- B：stock-3
- C：stock-0
- D：stock-1

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 8,
        "mass": 1.9
      },
      {
        "id": "stock-1",
        "cost": 6,
        "stiffness": 10,
        "mass": 1
      },
      {
        "id": "stock-2",
        "cost": 2,
        "stiffness": 11,
        "mass": 1.9
      },
      {
        "id": "stock-3",
        "cost": 4,
        "stiffness": 11,
        "mass": 1.5
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "B",
      "D"
    ]
  }
}
```

### 依赖装配（h3-exp-d4-cradle-1-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:cell-0-console",
        "label": "安装 cell-0-console",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-0-console"
        ],
        "adds": [
          "present:cell-0-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console",
          "visible": true
        }
      },
      {
        "id": "place:cell-1-shuttle",
        "label": "安装 cell-1-shuttle",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-1-shuttle"
        ],
        "adds": [
          "present:cell-1-shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-shuttle",
          "visible": true
        }
      },
      {
        "id": "place:shared-inspection-mast",
        "label": "安装 shared-inspection-mast",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:shared-inspection-mast"
        ],
        "adds": [
          "present:shared-inspection-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast",
          "visible": true
        }
      },
      {
        "id": "place:cell-1-mount",
        "label": "安装 cell-1-mount",
        "requires": [
          "present:cell-1-shuttle"
        ],
        "forbids": [
          "present:cell-1-mount"
        ],
        "adds": [
          "present:cell-1-mount"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-mount",
          "visible": true
        }
      },
      {
        "id": "place:foundation",
        "label": "安装 foundation",
        "requires": [],
        "forbids": [
          "present:foundation"
        ],
        "adds": [
          "present:foundation"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "foundation",
          "visible": true
        }
      },
      {
        "id": "place:cell-1-magazine",
        "label": "安装 cell-1-magazine",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-1-magazine"
        ],
        "adds": [
          "present:cell-1-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine",
          "visible": true
        }
      },
      {
        "id": "place:cell-1-wing-2",
        "label": "安装 cell-1-wing-2",
        "requires": [
          "present:cell-1-hub"
        ],
        "forbids": [
          "present:cell-1-wing-2"
        ],
        "adds": [
          "present:cell-1-wing-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-wing-2",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-optic",
        "label": "安装 cell-0-optic",
        "requires": [
          "present:cell-0-cradle"
        ],
        "forbids": [
          "present:cell-0-optic"
        ],
        "adds": [
          "present:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-drawer",
        "label": "安装 cell-0-drawer",
        "requires": [
          "present:cell-0-magazine"
        ],
        "forbids": [
          "present:cell-0-drawer"
        ],
        "adds": [
          "present:cell-0-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-drawer",
          "visible": true
        }
      },
      {
        "id": "place:shared-scanner",
        "label": "安装 shared-scanner",
        "requires": [
          "present:shared-inspection-mast"
        ],
        "forbids": [
          "present:shared-scanner"
        ],
        "adds": [
          "present:shared-scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner",
          "visible": true
        }
      },
      {
        "id": "place:cell-2-hub",
        "label": "安装 cell-2-hub",
        "requires": [
          "present:cell-2-mount"
        ],
        "forbids": [
          "present:cell-2-hub"
        ],
        "adds": [
          "present:cell-2-hub"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-hub",
          "visible": true
        }
      },
      {
        "id": "place:cell-1-wing-1",
        "label": "安装 cell-1-wing-1",
        "requires": [
          "present:cell-1-hub"
        ],
        "forbids": [
          "present:cell-1-wing-1"
        ],
        "adds": [
          "present:cell-1-wing-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-wing-1",
          "visible": true
        }
      },
      {
        "id": "place:cell-2-magazine",
        "label": "安装 cell-2-magazine",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-2-magazine"
        ],
        "adds": [
          "present:cell-2-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine",
          "visible": true
        }
      },
      {
        "id": "place:cell-1-hub",
        "label": "安装 cell-1-hub",
        "requires": [
          "present:cell-1-mount"
        ],
        "forbids": [
          "present:cell-1-hub"
        ],
        "adds": [
          "present:cell-1-hub"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-hub",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-cradle",
        "label": "安装 cell-0-cradle",
        "requires": [
          "present:cell-0-yoke"
        ],
        "forbids": [
          "present:cell-0-cradle"
        ],
        "adds": [
          "present:cell-0-cradle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cradle",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-shuttle",
        "label": "安装 cell-0-shuttle",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-0-shuttle"
        ],
        "adds": [
          "present:cell-0-shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-shuttle",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-magazine",
        "label": "安装 cell-0-magazine",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-0-magazine"
        ],
        "adds": [
          "present:cell-0-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-magazine",
          "visible": true
        }
      },
      {
        "id": "place:cell-2-shuttle",
        "label": "安装 cell-2-shuttle",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-2-shuttle"
        ],
        "adds": [
          "present:cell-2-shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-shuttle",
          "visible": true
        }
      },
      {
        "id": "place:cell-2-console",
        "label": "安装 cell-2-console",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-2-console"
        ],
        "adds": [
          "present:cell-2-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-console",
          "visible": true
        }
      },
      {
        "id": "place:cell-1-drawer",
        "label": "安装 cell-1-drawer",
        "requires": [
          "present:cell-1-magazine"
        ],
        "forbids": [
          "present:cell-1-drawer"
        ],
        "adds": [
          "present:cell-1-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer",
          "visible": true
        }
      },
      {
        "id": "place:cell-2-drawer",
        "label": "安装 cell-2-drawer",
        "requires": [
          "present:cell-2-magazine"
        ],
        "forbids": [
          "present:cell-2-drawer"
        ],
        "adds": [
          "present:cell-2-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer",
          "visible": true
        }
      },
      {
        "id": "place:cell-1-wing-3",
        "label": "安装 cell-1-wing-3",
        "requires": [
          "present:cell-1-hub"
        ],
        "forbids": [
          "present:cell-1-wing-3"
        ],
        "adds": [
          "present:cell-1-wing-3"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-wing-3",
          "visible": true
        }
      },
      {
        "id": "place:cell-1-wing-0",
        "label": "安装 cell-1-wing-0",
        "requires": [
          "present:cell-1-hub"
        ],
        "forbids": [
          "present:cell-1-wing-0"
        ],
        "adds": [
          "present:cell-1-wing-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-wing-0",
          "visible": true
        }
      },
      {
        "id": "place:cell-1-console",
        "label": "安装 cell-1-console",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-1-console"
        ],
        "adds": [
          "present:cell-1-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-mount",
        "label": "安装 cell-0-mount",
        "requires": [
          "present:cell-0-shuttle"
        ],
        "forbids": [
          "present:cell-0-mount"
        ],
        "adds": [
          "present:cell-0-mount"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-mount",
          "visible": true
        }
      },
      {
        "id": "place:cell-2-mount",
        "label": "安装 cell-2-mount",
        "requires": [
          "present:cell-2-shuttle"
        ],
        "forbids": [
          "present:cell-2-mount"
        ],
        "adds": [
          "present:cell-2-mount"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-mount",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-yoke",
        "label": "安装 cell-0-yoke",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-yoke"
        ],
        "adds": [
          "present:cell-0-yoke"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-yoke",
          "visible": true
        }
      },
      {
        "id": "place:cell-2-probe-0",
        "label": "安装 cell-2-probe-0",
        "requires": [
          "present:cell-2-hub"
        ],
        "forbids": [
          "present:cell-2-probe-0"
        ],
        "adds": [
          "present:cell-2-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-probe-0",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:cell-0-shuttle",
      "present:cell-0-mount",
      "present:cell-0-yoke",
      "present:cell-0-cradle",
      "present:cell-0-optic",
      "present:cell-0-console",
      "present:cell-0-magazine",
      "present:cell-0-drawer",
      "present:cell-1-shuttle",
      "present:cell-1-mount",
      "present:cell-1-hub",
      "present:cell-1-wing-0",
      "present:cell-1-wing-1",
      "present:cell-1-wing-2",
      "present:cell-1-wing-3",
      "present:cell-1-console",
      "present:cell-1-magazine",
      "present:cell-1-drawer",
      "present:cell-2-shuttle",
      "present:cell-2-mount",
      "present:cell-2-hub",
      "present:cell-2-probe-0",
      "present:cell-2-console",
      "present:cell-2-magazine",
      "present:cell-2-drawer",
      "present:shared-inspection-mast",
      "present:shared-scanner"
    ],
    "budget": 28,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:cell-0-console",
      "place:cell-1-shuttle",
      "place:shared-inspection-mast",
      "place:cell-1-mount",
      "place:cell-1-magazine",
      "place:shared-scanner",
      "place:cell-2-magazine",
      "place:cell-1-hub",
      "place:cell-1-wing-2",
      "place:cell-1-wing-1",
      "place:cell-0-shuttle",
      "place:cell-0-magazine",
      "place:cell-0-drawer",
      "place:cell-2-shuttle",
      "place:cell-2-console",
      "place:cell-1-drawer",
      "place:cell-2-drawer",
      "place:cell-1-wing-3",
      "place:cell-1-wing-0",
      "place:cell-1-console",
      "place:cell-0-mount",
      "place:cell-2-mount",
      "place:cell-2-hub",
      "place:cell-0-yoke",
      "place:cell-0-cradle",
      "place:cell-0-optic",
      "place:cell-2-probe-0"
    ]
  }
}
```

### 依赖拆解（h3-exp-d4-cradle-1-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:cell-0-shuttle",
      "present:cell-0-mount",
      "present:cell-0-yoke",
      "present:cell-0-cradle",
      "present:cell-0-optic",
      "present:cell-0-console",
      "present:cell-0-magazine",
      "present:cell-0-drawer",
      "present:cell-1-shuttle",
      "present:cell-1-mount",
      "present:cell-1-hub",
      "present:cell-1-wing-0",
      "present:cell-1-wing-1",
      "present:cell-1-wing-2",
      "present:cell-1-wing-3",
      "present:cell-1-console",
      "present:cell-1-magazine",
      "present:cell-1-drawer",
      "present:cell-2-shuttle",
      "present:cell-2-mount",
      "present:cell-2-hub",
      "present:cell-2-probe-0",
      "present:cell-2-console",
      "present:cell-2-magazine",
      "present:cell-2-drawer",
      "present:shared-inspection-mast",
      "present:shared-scanner"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-yoke",
      "cell-0-cradle",
      "cell-0-optic",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-hub",
      "cell-1-wing-0",
      "cell-1-wing-1",
      "cell-1-wing-2",
      "cell-1-wing-3",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-probe-0",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "actions": [
      {
        "id": "remove:cell-2-mount",
        "label": "拆除 cell-2-mount",
        "requires": [
          "present:cell-2-mount"
        ],
        "forbids": [
          "present:cell-2-hub"
        ],
        "adds": [
          "removed:cell-2-mount"
        ],
        "deletes": [
          "present:cell-2-mount"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-mount",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-mount",
        "label": "拆除 cell-1-mount",
        "requires": [
          "present:cell-1-mount"
        ],
        "forbids": [
          "present:cell-1-hub"
        ],
        "adds": [
          "removed:cell-1-mount"
        ],
        "deletes": [
          "present:cell-1-mount"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-mount",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-hub",
        "label": "拆除 cell-1-hub",
        "requires": [
          "present:cell-1-hub"
        ],
        "forbids": [
          "present:cell-1-wing-0",
          "present:cell-1-wing-1",
          "present:cell-1-wing-2",
          "present:cell-1-wing-3"
        ],
        "adds": [
          "removed:cell-1-hub"
        ],
        "deletes": [
          "present:cell-1-hub"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-hub",
          "visible": false
        }
      },
      {
        "id": "remove:cell-2-magazine",
        "label": "拆除 cell-2-magazine",
        "requires": [
          "present:cell-2-magazine"
        ],
        "forbids": [
          "present:cell-2-drawer"
        ],
        "adds": [
          "removed:cell-2-magazine"
        ],
        "deletes": [
          "present:cell-2-magazine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-wing-0",
        "label": "拆除 cell-1-wing-0",
        "requires": [
          "present:cell-1-wing-0"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-1-wing-0"
        ],
        "deletes": [
          "present:cell-1-wing-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-wing-0",
          "visible": false
        }
      },
      {
        "id": "remove:foundation",
        "label": "拆除 foundation",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-0-shuttle",
          "present:cell-0-console",
          "present:cell-0-magazine",
          "present:cell-1-shuttle",
          "present:cell-1-console",
          "present:cell-1-magazine",
          "present:cell-2-shuttle",
          "present:cell-2-console",
          "present:cell-2-magazine",
          "present:shared-inspection-mast"
        ],
        "adds": [
          "removed:foundation"
        ],
        "deletes": [
          "present:foundation"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "foundation",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-magazine",
        "label": "拆除 cell-1-magazine",
        "requires": [
          "present:cell-1-magazine"
        ],
        "forbids": [
          "present:cell-1-drawer"
        ],
        "adds": [
          "removed:cell-1-magazine"
        ],
        "deletes": [
          "present:cell-1-magazine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-optic",
        "label": "拆除 cell-0-optic",
        "requires": [
          "present:cell-0-optic"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-optic"
        ],
        "deletes": [
          "present:cell-0-optic"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic",
          "visible": false
        }
      },
      {
        "id": "remove:cell-2-probe-0",
        "label": "拆除 cell-2-probe-0",
        "requires": [
          "present:cell-2-probe-0"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-2-probe-0"
        ],
        "deletes": [
          "present:cell-2-probe-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-probe-0",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-console",
        "label": "拆除 cell-0-console",
        "requires": [
          "present:cell-0-console"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-console"
        ],
        "deletes": [
          "present:cell-0-console"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-console",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-mount",
        "label": "拆除 cell-0-mount",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-yoke"
        ],
        "adds": [
          "removed:cell-0-mount"
        ],
        "deletes": [
          "present:cell-0-mount"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-mount",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-drawer",
        "label": "拆除 cell-1-drawer",
        "requires": [
          "present:cell-1-drawer"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-1-drawer"
        ],
        "deletes": [
          "present:cell-1-drawer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-wing-2",
        "label": "拆除 cell-1-wing-2",
        "requires": [
          "present:cell-1-wing-2"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-1-wing-2"
        ],
        "deletes": [
          "present:cell-1-wing-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-wing-2",
          "visible": false
        }
      },
      {
        "id": "remove:shared-inspection-mast",
        "label": "拆除 shared-inspection-mast",
        "requires": [
          "present:shared-inspection-mast"
        ],
        "forbids": [
          "present:shared-scanner"
        ],
        "adds": [
          "removed:shared-inspection-mast"
        ],
        "deletes": [
          "present:shared-inspection-mast"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast",
          "visible": false
        }
      },
      {
        "id": "remove:cell-2-console",
        "label": "拆除 cell-2-console",
        "requires": [
          "present:cell-2-console"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-2-console"
        ],
        "deletes": [
          "present:cell-2-console"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-console",
          "visible": false
        }
      },
      {
        "id": "remove:cell-2-drawer",
        "label": "拆除 cell-2-drawer",
        "requires": [
          "present:cell-2-drawer"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-2-drawer"
        ],
        "deletes": [
          "present:cell-2-drawer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-yoke",
        "label": "拆除 cell-0-yoke",
        "requires": [
          "present:cell-0-yoke"
        ],
        "forbids": [
          "present:cell-0-cradle"
        ],
        "adds": [
          "removed:cell-0-yoke"
        ],
        "deletes": [
          "present:cell-0-yoke"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-yoke",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-drawer",
        "label": "拆除 cell-0-drawer",
        "requires": [
          "present:cell-0-drawer"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-drawer"
        ],
        "deletes": [
          "present:cell-0-drawer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-drawer",
          "visible": false
        }
      },
      {
        "id": "remove:shared-scanner",
        "label": "拆除 shared-scanner",
        "requires": [
          "present:shared-scanner"
        ],
        "forbids": [],
        "adds": [
          "removed:shared-scanner"
        ],
        "deletes": [
          "present:shared-scanner"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-wing-3",
        "label": "拆除 cell-1-wing-3",
        "requires": [
          "present:cell-1-wing-3"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-1-wing-3"
        ],
        "deletes": [
          "present:cell-1-wing-3"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-wing-3",
          "visible": false
        }
      },
      {
        "id": "remove:cell-2-shuttle",
        "label": "拆除 cell-2-shuttle",
        "requires": [
          "present:cell-2-shuttle"
        ],
        "forbids": [
          "present:cell-2-mount"
        ],
        "adds": [
          "removed:cell-2-shuttle"
        ],
        "deletes": [
          "present:cell-2-shuttle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-shuttle",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-magazine",
        "label": "拆除 cell-0-magazine",
        "requires": [
          "present:cell-0-magazine"
        ],
        "forbids": [
          "present:cell-0-drawer"
        ],
        "adds": [
          "removed:cell-0-magazine"
        ],
        "deletes": [
          "present:cell-0-magazine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-magazine",
          "visible": false
        }
      },
      {
        "id": "remove:cell-2-hub",
        "label": "拆除 cell-2-hub",
        "requires": [
          "present:cell-2-hub"
        ],
        "forbids": [
          "present:cell-2-probe-0"
        ],
        "adds": [
          "removed:cell-2-hub"
        ],
        "deletes": [
          "present:cell-2-hub"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-hub",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-console",
        "label": "拆除 cell-1-console",
        "requires": [
          "present:cell-1-console"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-1-console"
        ],
        "deletes": [
          "present:cell-1-console"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-wing-1",
        "label": "拆除 cell-1-wing-1",
        "requires": [
          "present:cell-1-wing-1"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-1-wing-1"
        ],
        "deletes": [
          "present:cell-1-wing-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-wing-1",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-cradle",
        "label": "拆除 cell-0-cradle",
        "requires": [
          "present:cell-0-cradle"
        ],
        "forbids": [
          "present:cell-0-optic"
        ],
        "adds": [
          "removed:cell-0-cradle"
        ],
        "deletes": [
          "present:cell-0-cradle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cradle",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-shuttle",
        "label": "拆除 cell-1-shuttle",
        "requires": [
          "present:cell-1-shuttle"
        ],
        "forbids": [
          "present:cell-1-mount"
        ],
        "adds": [
          "removed:cell-1-shuttle"
        ],
        "deletes": [
          "present:cell-1-shuttle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-shuttle",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-shuttle",
        "label": "拆除 cell-0-shuttle",
        "requires": [
          "present:cell-0-shuttle"
        ],
        "forbids": [
          "present:cell-0-mount"
        ],
        "adds": [
          "removed:cell-0-shuttle"
        ],
        "deletes": [
          "present:cell-0-shuttle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-shuttle",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:shared-scanner",
      "removed:shared-inspection-mast",
      "removed:cell-2-drawer",
      "removed:cell-2-magazine",
      "removed:cell-2-console",
      "removed:cell-2-probe-0",
      "removed:cell-2-hub",
      "removed:cell-2-mount",
      "removed:cell-2-shuttle",
      "removed:cell-1-drawer",
      "removed:cell-1-magazine",
      "removed:cell-1-console",
      "removed:cell-1-wing-3",
      "removed:cell-1-wing-2",
      "removed:cell-1-wing-1",
      "removed:cell-1-wing-0",
      "removed:cell-1-hub",
      "removed:cell-1-mount",
      "removed:cell-1-shuttle",
      "removed:cell-0-drawer",
      "removed:cell-0-magazine",
      "removed:cell-0-console",
      "removed:cell-0-optic",
      "removed:cell-0-cradle",
      "removed:cell-0-yoke",
      "removed:cell-0-mount",
      "removed:cell-0-shuttle",
      "removed:foundation"
    ],
    "budget": 28,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:cell-1-wing-0",
      "remove:cell-0-optic",
      "remove:cell-2-probe-0",
      "remove:cell-0-console",
      "remove:cell-1-drawer",
      "remove:cell-1-magazine",
      "remove:cell-1-wing-2",
      "remove:cell-2-console",
      "remove:cell-2-drawer",
      "remove:cell-2-magazine",
      "remove:cell-0-drawer",
      "remove:shared-scanner",
      "remove:shared-inspection-mast",
      "remove:cell-1-wing-3",
      "remove:cell-0-magazine",
      "remove:cell-2-hub",
      "remove:cell-2-mount",
      "remove:cell-2-shuttle",
      "remove:cell-1-console",
      "remove:cell-1-wing-1",
      "remove:cell-1-hub",
      "remove:cell-1-mount",
      "remove:cell-0-cradle",
      "remove:cell-0-yoke",
      "remove:cell-0-mount",
      "remove:cell-1-shuttle",
      "remove:cell-0-shuttle",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-exp-d4-cradle-1-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-optic",
      "closed:cell-0-optic"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-yoke",
      "cell-0-cradle",
      "cell-0-optic",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-hub",
      "cell-1-wing-0",
      "cell-1-wing-1",
      "cell-1-wing-2",
      "cell-1-wing-3",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-probe-0",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "actions": [
      {
        "id": "remove:cell-0-optic",
        "label": "remove cell-0-optic",
        "requires": [
          "done:open:cell-0-optic"
        ],
        "forbids": [
          "done:remove:cell-0-optic"
        ],
        "adds": [
          "done:remove:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic",
          "visible": false
        }
      },
      {
        "id": "replace:cell-0-optic",
        "label": "replace cell-0-optic",
        "requires": [
          "done:remove:cell-0-optic"
        ],
        "forbids": [
          "done:replace:cell-0-optic"
        ],
        "adds": [
          "done:replace:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic",
          "visible": true
        }
      },
      {
        "id": "open:cell-0-optic",
        "label": "open cell-0-optic",
        "requires": [
          "done:support:cell-0-optic"
        ],
        "forbids": [
          "done:open:cell-0-optic"
        ],
        "adds": [
          "done:open:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "release:cell-0-optic",
        "label": "release cell-0-optic",
        "requires": [
          "done:close:cell-0-optic"
        ],
        "forbids": [
          "done:release:cell-0-optic"
        ],
        "adds": [
          "done:release:cell-0-optic",
          "repaired:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "support:cell-0-optic",
        "label": "support cell-0-optic",
        "requires": [
          "fault:cell-0-optic"
        ],
        "forbids": [
          "done:support:cell-0-optic"
        ],
        "adds": [
          "done:support:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "close:cell-0-optic",
        "label": "close cell-0-optic",
        "requires": [
          "done:verify:cell-0-optic"
        ],
        "forbids": [
          "done:close:cell-0-optic"
        ],
        "adds": [
          "done:close:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "verify:cell-0-optic",
        "label": "verify cell-0-optic",
        "requires": [
          "done:replace:cell-0-optic"
        ],
        "forbids": [
          "done:verify:cell-0-optic"
        ],
        "adds": [
          "done:verify:cell-0-optic"
        ],
        "deletes": [
          "fault:cell-0-optic"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-optic"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-optic",
      "open:cell-0-optic",
      "remove:cell-0-optic",
      "replace:cell-0-optic",
      "verify:cell-0-optic",
      "close:cell-0-optic",
      "release:cell-0-optic"
    ]
  }
}
```

### 复合编辑验证（h3-exp-d4-cradle-1-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-optic",
      "closed:cell-0-optic"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-yoke",
      "cell-0-cradle",
      "cell-0-optic",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-hub",
      "cell-1-wing-0",
      "cell-1-wing-1",
      "cell-1-wing-2",
      "cell-1-wing-3",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-probe-0",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "actions": [
      {
        "id": "recolor:cell-0-optic",
        "label": "recolor cell-0-optic",
        "requires": [
          "done:open:cell-0-optic"
        ],
        "forbids": [
          "done:recolor:cell-0-optic"
        ],
        "adds": [
          "done:recolor:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic",
          "color": "#ea7635"
        }
      },
      {
        "id": "open:cell-0-optic",
        "label": "open cell-0-optic",
        "requires": [
          "done:support:cell-0-optic"
        ],
        "forbids": [
          "done:open:cell-0-optic"
        ],
        "adds": [
          "done:open:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "release:cell-0-optic",
        "label": "release cell-0-optic",
        "requires": [
          "done:close:cell-0-optic"
        ],
        "forbids": [
          "done:release:cell-0-optic"
        ],
        "adds": [
          "done:release:cell-0-optic",
          "repaired:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "support:cell-0-optic",
        "label": "support cell-0-optic",
        "requires": [
          "fault:cell-0-optic"
        ],
        "forbids": [
          "done:support:cell-0-optic"
        ],
        "adds": [
          "done:support:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "close:cell-0-optic",
        "label": "close cell-0-optic",
        "requires": [
          "done:verify:cell-0-optic"
        ],
        "forbids": [
          "done:close:cell-0-optic"
        ],
        "adds": [
          "done:close:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "verify:cell-0-optic",
        "label": "verify cell-0-optic",
        "requires": [
          "done:recolor:cell-0-optic"
        ],
        "forbids": [
          "done:verify:cell-0-optic"
        ],
        "adds": [
          "done:verify:cell-0-optic"
        ],
        "deletes": [
          "fault:cell-0-optic"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-optic"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-optic",
      "open:cell-0-optic",
      "recolor:cell-0-optic",
      "verify:cell-0-optic",
      "close:cell-0-optic",
      "release:cell-0-optic"
    ]
  }
}
```

### 跨区域联合维修（h3-exp-d4-cradle-1-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-2-magazine",
      "closed:cell-2-magazine",
      "fault:cell-2-drawer",
      "closed:cell-2-drawer",
      "fault:shared-inspection-mast",
      "closed:shared-inspection-mast",
      "fault:shared-scanner",
      "closed:shared-scanner"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-yoke",
      "cell-0-cradle",
      "cell-0-optic",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-hub",
      "cell-1-wing-0",
      "cell-1-wing-1",
      "cell-1-wing-2",
      "cell-1-wing-3",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-probe-0",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "actions": [
      {
        "id": "close:shared-inspection-mast",
        "label": "close shared-inspection-mast",
        "requires": [
          "done:verify:shared-inspection-mast"
        ],
        "forbids": [
          "done:close:shared-inspection-mast"
        ],
        "adds": [
          "done:close:shared-inspection-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast"
        }
      },
      {
        "id": "verify:cell-2-magazine",
        "label": "verify cell-2-magazine",
        "requires": [
          "done:replace:cell-2-magazine"
        ],
        "forbids": [
          "done:verify:cell-2-magazine"
        ],
        "adds": [
          "done:verify:cell-2-magazine"
        ],
        "deletes": [
          "fault:cell-2-magazine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine"
        }
      },
      {
        "id": "release:cell-2-drawer",
        "label": "release cell-2-drawer",
        "requires": [
          "done:close:cell-2-drawer"
        ],
        "forbids": [
          "done:release:cell-2-drawer"
        ],
        "adds": [
          "done:release:cell-2-drawer",
          "repaired:cell-2-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer"
        }
      },
      {
        "id": "remove:cell-2-magazine",
        "label": "remove cell-2-magazine",
        "requires": [
          "done:open:cell-2-magazine"
        ],
        "forbids": [
          "done:remove:cell-2-magazine"
        ],
        "adds": [
          "done:remove:cell-2-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine",
          "visible": false
        }
      },
      {
        "id": "open:cell-2-magazine",
        "label": "open cell-2-magazine",
        "requires": [
          "done:support:cell-2-magazine"
        ],
        "forbids": [
          "done:open:cell-2-magazine"
        ],
        "adds": [
          "done:open:cell-2-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine"
        }
      },
      {
        "id": "support:cell-2-magazine",
        "label": "support cell-2-magazine",
        "requires": [
          "fault:cell-2-magazine"
        ],
        "forbids": [
          "done:support:cell-2-magazine"
        ],
        "adds": [
          "done:support:cell-2-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine"
        }
      },
      {
        "id": "support:shared-inspection-mast",
        "label": "support shared-inspection-mast",
        "requires": [
          "fault:shared-inspection-mast"
        ],
        "forbids": [
          "done:support:shared-inspection-mast"
        ],
        "adds": [
          "done:support:shared-inspection-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast"
        }
      },
      {
        "id": "close:cell-2-drawer",
        "label": "close cell-2-drawer",
        "requires": [
          "done:verify:cell-2-drawer"
        ],
        "forbids": [
          "done:close:cell-2-drawer"
        ],
        "adds": [
          "done:close:cell-2-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer"
        }
      },
      {
        "id": "support:cell-2-drawer",
        "label": "support cell-2-drawer",
        "requires": [
          "fault:cell-2-drawer"
        ],
        "forbids": [
          "done:support:cell-2-drawer"
        ],
        "adds": [
          "done:support:cell-2-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer"
        }
      },
      {
        "id": "open:shared-inspection-mast",
        "label": "open shared-inspection-mast",
        "requires": [
          "done:support:shared-inspection-mast"
        ],
        "forbids": [
          "done:open:shared-inspection-mast"
        ],
        "adds": [
          "done:open:shared-inspection-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast"
        }
      },
      {
        "id": "close:cell-2-magazine",
        "label": "close cell-2-magazine",
        "requires": [
          "done:verify:cell-2-magazine"
        ],
        "forbids": [
          "done:close:cell-2-magazine"
        ],
        "adds": [
          "done:close:cell-2-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine"
        }
      },
      {
        "id": "verify:shared-scanner",
        "label": "verify shared-scanner",
        "requires": [
          "done:replace:shared-scanner"
        ],
        "forbids": [
          "done:verify:shared-scanner"
        ],
        "adds": [
          "done:verify:shared-scanner"
        ],
        "deletes": [
          "fault:shared-scanner"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner"
        }
      },
      {
        "id": "remove:shared-inspection-mast",
        "label": "remove shared-inspection-mast",
        "requires": [
          "done:open:shared-inspection-mast"
        ],
        "forbids": [
          "done:remove:shared-inspection-mast"
        ],
        "adds": [
          "done:remove:shared-inspection-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast",
          "visible": false
        }
      },
      {
        "id": "verify:cell-2-drawer",
        "label": "verify cell-2-drawer",
        "requires": [
          "done:replace:cell-2-drawer"
        ],
        "forbids": [
          "done:verify:cell-2-drawer"
        ],
        "adds": [
          "done:verify:cell-2-drawer"
        ],
        "deletes": [
          "fault:cell-2-drawer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer"
        }
      },
      {
        "id": "replace:shared-inspection-mast",
        "label": "replace shared-inspection-mast",
        "requires": [
          "done:remove:shared-inspection-mast"
        ],
        "forbids": [
          "done:replace:shared-inspection-mast"
        ],
        "adds": [
          "done:replace:shared-inspection-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast",
          "visible": true
        }
      },
      {
        "id": "replace:cell-2-drawer",
        "label": "replace cell-2-drawer",
        "requires": [
          "done:remove:cell-2-drawer"
        ],
        "forbids": [
          "done:replace:cell-2-drawer"
        ],
        "adds": [
          "done:replace:cell-2-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer",
          "visible": true
        }
      },
      {
        "id": "remove:cell-2-drawer",
        "label": "remove cell-2-drawer",
        "requires": [
          "done:open:cell-2-drawer"
        ],
        "forbids": [
          "done:remove:cell-2-drawer"
        ],
        "adds": [
          "done:remove:cell-2-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer",
          "visible": false
        }
      },
      {
        "id": "verify:shared-inspection-mast",
        "label": "verify shared-inspection-mast",
        "requires": [
          "done:replace:shared-inspection-mast"
        ],
        "forbids": [
          "done:verify:shared-inspection-mast"
        ],
        "adds": [
          "done:verify:shared-inspection-mast"
        ],
        "deletes": [
          "fault:shared-inspection-mast"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast"
        }
      },
      {
        "id": "replace:shared-scanner",
        "label": "replace shared-scanner",
        "requires": [
          "done:remove:shared-scanner"
        ],
        "forbids": [
          "done:replace:shared-scanner"
        ],
        "adds": [
          "done:replace:shared-scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner",
          "visible": true
        }
      },
      {
        "id": "remove:shared-scanner",
        "label": "remove shared-scanner",
        "requires": [
          "done:open:shared-scanner"
        ],
        "forbids": [
          "done:remove:shared-scanner"
        ],
        "adds": [
          "done:remove:shared-scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner",
          "visible": false
        }
      },
      {
        "id": "close:shared-scanner",
        "label": "close shared-scanner",
        "requires": [
          "done:verify:shared-scanner"
        ],
        "forbids": [
          "done:close:shared-scanner"
        ],
        "adds": [
          "done:close:shared-scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner"
        }
      },
      {
        "id": "open:shared-scanner",
        "label": "open shared-scanner",
        "requires": [
          "done:support:shared-scanner"
        ],
        "forbids": [
          "done:open:shared-scanner"
        ],
        "adds": [
          "done:open:shared-scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner"
        }
      },
      {
        "id": "open:cell-2-drawer",
        "label": "open cell-2-drawer",
        "requires": [
          "done:support:cell-2-drawer"
        ],
        "forbids": [
          "done:open:cell-2-drawer"
        ],
        "adds": [
          "done:open:cell-2-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer"
        }
      },
      {
        "id": "release:shared-inspection-mast",
        "label": "release shared-inspection-mast",
        "requires": [
          "done:close:shared-inspection-mast"
        ],
        "forbids": [
          "done:release:shared-inspection-mast"
        ],
        "adds": [
          "done:release:shared-inspection-mast",
          "repaired:shared-inspection-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast"
        }
      },
      {
        "id": "support:shared-scanner",
        "label": "support shared-scanner",
        "requires": [
          "fault:shared-scanner"
        ],
        "forbids": [
          "done:support:shared-scanner"
        ],
        "adds": [
          "done:support:shared-scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner"
        }
      },
      {
        "id": "release:cell-2-magazine",
        "label": "release cell-2-magazine",
        "requires": [
          "done:close:cell-2-magazine"
        ],
        "forbids": [
          "done:release:cell-2-magazine"
        ],
        "adds": [
          "done:release:cell-2-magazine",
          "repaired:cell-2-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine"
        }
      },
      {
        "id": "replace:cell-2-magazine",
        "label": "replace cell-2-magazine",
        "requires": [
          "done:remove:cell-2-magazine"
        ],
        "forbids": [
          "done:replace:cell-2-magazine"
        ],
        "adds": [
          "done:replace:cell-2-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine",
          "visible": true
        }
      },
      {
        "id": "release:shared-scanner",
        "label": "release shared-scanner",
        "requires": [
          "done:close:shared-scanner"
        ],
        "forbids": [
          "done:release:shared-scanner"
        ],
        "adds": [
          "done:release:shared-scanner",
          "repaired:shared-scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-2-magazine",
      "repaired:cell-2-drawer",
      "repaired:shared-inspection-mast",
      "repaired:shared-scanner"
    ],
    "budget": 28,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-2-magazine",
      "open:cell-2-magazine",
      "remove:cell-2-magazine",
      "support:shared-inspection-mast",
      "support:cell-2-drawer",
      "open:shared-inspection-mast",
      "remove:shared-inspection-mast",
      "replace:shared-inspection-mast",
      "verify:shared-inspection-mast",
      "close:shared-inspection-mast",
      "open:cell-2-drawer",
      "remove:cell-2-drawer",
      "replace:cell-2-drawer",
      "verify:cell-2-drawer",
      "close:cell-2-drawer",
      "release:cell-2-drawer",
      "release:shared-inspection-mast",
      "support:shared-scanner",
      "open:shared-scanner",
      "remove:shared-scanner",
      "replace:shared-scanner",
      "verify:shared-scanner",
      "close:shared-scanner",
      "replace:cell-2-magazine",
      "verify:cell-2-magazine",
      "close:cell-2-magazine",
      "release:cell-2-magazine",
      "release:shared-scanner"
    ]
  }
}
```

### 多工位资源调度（h3-exp-d4-cradle-1-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "foundation",
        "duration": 1,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "cell-0-shuttle",
        "duration": 1,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "cell-0-mount",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "cell-0-yoke",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "cell-0-cradle",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "cell-0-optic",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      },
      {
        "id": "job-6",
        "module": "cell-0-console",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-4"
        ]
      },
      {
        "id": "job-7",
        "module": "cell-0-magazine",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-5"
        ]
      },
      {
        "id": "job-8",
        "module": "cell-0-drawer",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-6"
        ]
      },
      {
        "id": "job-9",
        "module": "cell-1-shuttle",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-7"
        ]
      }
    ],
    "deadline": 11
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 1,
      "job-4": 4,
      "job-5": 3,
      "job-6": 7,
      "job-7": 4,
      "job-8": 9,
      "job-9": 5
    }
  }
}
```

### 检查后条件策略（h3-exp-d4-cradle-1-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-optic",
    "worlds": [
      {
        "id": "normal",
        "action": "tighten"
      },
      {
        "id": "loose",
        "action": "replace"
      },
      {
        "id": "jammed",
        "action": "continue"
      }
    ],
    "budget": 2,
    "queries": [
      {
        "id": "visual",
        "cost": 1,
        "returns": {
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      },
      {
        "id": "probe",
        "cost": 2,
        "returns": {
          "normal": "signal-0",
          "loose": "signal-1",
          "jammed": "signal-2"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      }
    ]
  },
  "answer": {
    "queryId": "probe",
    "decisions": {
      "signal-0": "tighten",
      "signal-1": "replace",
      "signal-2": "continue"
    }
  }
}
```

### 局部坐标变换（h3-exp-d4-cradle-1-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[-14,5.85,0]
- B：[1,-0.1,0]
- C：[-12,5.85,0]
- D：[-13,6.85,1]

```json
{
  "input": {
    "localPoint": [
      1,
      -0.09999999999999964,
      0
    ],
    "rotationXYZW": [
      0,
      1,
      0,
      6.123233995736766e-17
    ],
    "translation": [
      -13,
      5.949999999999999,
      0
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 正交视图投影（h3-exp-d4-cradle-1-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[-6,11]
- B：[11,5]
- C：[5,6]
- D：[0,0]

```json
{
  "input": {
    "view": "side",
    "point": [
      5,
      11,
      -6
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 空间相对关系（h3-exp-d4-cradle-1-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：greater
- B：less
- C：equal

```json
{
  "input": {
    "A": {
      "id": "foundation",
      "position": [
        0,
        0.2,
        0
      ]
    },
    "B": {
      "id": "shared-scanner",
      "position": [
        0,
        7.012499999999999,
        11
      ]
    },
    "axis": "y"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 约束自由度（h3-exp-d4-cradle-1-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：3
- B：6
- C：0
- D：1

```json
{
  "input": {
    "joint": {
      "id": "shared-inspection-mast-joint",
      "name": "shared-inspection-mast interface",
      "parent": "foundation",
      "child": "shared-inspection-mast",
      "type": "fixed",
      "anchorParent": [
        0,
        0.7999999999999999,
        11
      ],
      "anchorChild": [
        0,
        -2.5875,
        0
      ],
      "axis": [
        0,
        1,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 维修间隙预算（h3-exp-d4-cradle-1-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "cell-0-optic",
    "aperture": 0.7,
    "toolWidth": 0.65,
    "eachSideMargin": 0.05
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-exp-d4-cradle-1-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,16]
- B：[0,0,0]
- C：[0,-4,0]
- D：[0,0,-16]

```json
{
  "input": {
    "module": "cell-0-optic",
    "lever": [
      4,
      2,
      0
    ],
    "force": [
      0,
      -4,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 非均匀先验更新（h3-exp-d4-cradle-1-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0
- B：1
- C：0.625
- D：0.38461538461538464

```json
{
  "input": {
    "module": "cell-0-optic",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      3,
      5,
      5
    ],
    "compatible": [
      "normal",
      "jammed"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 风险最小决策（h3-exp-d4-cradle-1-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.7,
    "repairCost": 6,
    "failureLoss": 16,
    "module": "cell-0-optic"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-exp-d4-cradle-1-trace-threshold）

实际采样轨迹中是否有位移严格超过给定阈值？只评价采样点。

能力：轨迹阈值判定；形式：single-choice；证据：Rapier。

- A：exceeded
- B：within

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.00815147412073568
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0001045917746092399
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.00004865554786635296
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.00004863739387877562
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.000048637390137489794
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0000486373901367189
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00004863739013671875
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00004863739013671875
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.00004863739013671875
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.00004863739013671875
      },
      {
        "time": 1,
        "displacement": 0.00004863739013671875
      }
    ],
    "threshold": 0.006521179296588545
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-exp-d4-cradle-1-guarded-repair）

从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。

能力：安全联锁维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "actions": [
      {
        "id": "skip-inspection",
        "label": "跳过检查",
        "requires": [
          "tool:free"
        ],
        "forbids": [],
        "adds": [
          "unverified"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 0
      },
      {
        "id": "release:cell-0-optic",
        "label": "release cell-0-optic",
        "requires": [
          "done:relock:cell-0-optic"
        ],
        "forbids": [
          "done:release:cell-0-optic"
        ],
        "adds": [
          "done:release:cell-0-optic",
          "ready:cell-0-optic",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "relock:cell-0-optic",
        "label": "relock cell-0-optic",
        "requires": [
          "done:verify:cell-0-optic"
        ],
        "forbids": [
          "done:relock:cell-0-optic"
        ],
        "adds": [
          "done:relock:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "verify:cell-0-optic",
        "label": "verify cell-0-optic",
        "requires": [
          "done:replace:cell-0-optic"
        ],
        "forbids": [
          "done:verify:cell-0-optic"
        ],
        "adds": [
          "done:verify:cell-0-optic"
        ],
        "deletes": [
          "fault:cell-0-optic",
          "misaligned:cell-0-optic"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "replace:cell-0-optic",
        "label": "replace cell-0-optic",
        "requires": [
          "done:unlock:cell-0-optic"
        ],
        "forbids": [
          "done:replace:cell-0-optic"
        ],
        "adds": [
          "done:replace:cell-0-optic"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "unlock:cell-0-optic",
        "label": "unlock cell-0-optic",
        "requires": [
          "done:support:cell-0-optic"
        ],
        "forbids": [
          "done:unlock:cell-0-optic"
        ],
        "adds": [
          "done:unlock:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "support:cell-0-optic",
        "label": "support cell-0-optic",
        "requires": [
          "done:isolate:cell-0-optic"
        ],
        "forbids": [
          "done:support:cell-0-optic"
        ],
        "adds": [
          "done:support:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "isolate:cell-0-optic",
        "label": "isolate cell-0-optic",
        "requires": [
          "tool:free",
          "fault:cell-0-optic"
        ],
        "forbids": [
          "done:isolate:cell-0-optic"
        ],
        "adds": [
          "done:isolate:cell-0-optic"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-optic"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-yoke",
      "cell-0-cradle",
      "cell-0-optic",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-hub",
      "cell-1-wing-0",
      "cell-1-wing-1",
      "cell-1-wing-2",
      "cell-1-wing-3",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-probe-0",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "goalFacts": [
      "ready:cell-0-optic"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-optic",
      "support:cell-0-optic",
      "unlock:cell-0-optic",
      "replace:cell-0-optic",
      "verify:cell-0-optic",
      "relock:cell-0-optic",
      "release:cell-0-optic"
    ]
  }
}
```

### 失败状态回退（h3-exp-d4-cradle-1-rollback）

从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。

能力：失败状态回退；形式：actions；证据：state-machine。


```json
{
  "input": {
    "actions": [
      {
        "id": "skip-inspection",
        "label": "跳过检查",
        "requires": [
          "tool:free"
        ],
        "forbids": [],
        "adds": [
          "unverified"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 0
      },
      {
        "id": "resume:cell-0-optic",
        "label": "resume cell-0-optic",
        "requires": [
          "done:verify:cell-0-optic"
        ],
        "forbids": [
          "done:resume:cell-0-optic"
        ],
        "adds": [
          "done:resume:cell-0-optic",
          "ready:cell-0-optic",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "verify:cell-0-optic",
        "label": "verify cell-0-optic",
        "requires": [
          "done:align:cell-0-optic"
        ],
        "forbids": [
          "done:verify:cell-0-optic"
        ],
        "adds": [
          "done:verify:cell-0-optic"
        ],
        "deletes": [
          "fault:cell-0-optic",
          "misaligned:cell-0-optic"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      },
      {
        "id": "align:cell-0-optic",
        "label": "align cell-0-optic",
        "requires": [
          "done:undo:cell-0-optic"
        ],
        "forbids": [
          "done:align:cell-0-optic"
        ],
        "adds": [
          "done:align:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic",
          "visible": true
        }
      },
      {
        "id": "undo:cell-0-optic",
        "label": "undo cell-0-optic",
        "requires": [
          "done:isolate:cell-0-optic"
        ],
        "forbids": [
          "done:undo:cell-0-optic"
        ],
        "adds": [
          "done:undo:cell-0-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic",
          "visible": false
        }
      },
      {
        "id": "isolate:cell-0-optic",
        "label": "isolate cell-0-optic",
        "requires": [
          "tool:free",
          "fault:cell-0-optic"
        ],
        "forbids": [
          "done:isolate:cell-0-optic"
        ],
        "adds": [
          "done:isolate:cell-0-optic"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-optic"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-optic",
      "misaligned:cell-0-optic"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-yoke",
      "cell-0-cradle",
      "cell-0-optic",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-hub",
      "cell-1-wing-0",
      "cell-1-wing-1",
      "cell-1-wing-2",
      "cell-1-wing-3",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-probe-0",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "goalFacts": [
      "ready:cell-0-optic"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-optic",
      "undo:cell-0-optic",
      "align:cell-0-optic",
      "verify:cell-0-optic",
      "resume:cell-0-optic"
    ]
  }
}
```

### 共享工具协同维修（h3-exp-d4-cradle-1-resource-repair）

从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。

能力：共享工具协同维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "actions": [
      {
        "id": "skip-inspection",
        "label": "跳过检查",
        "requires": [
          "tool:free"
        ],
        "forbids": [],
        "adds": [
          "unverified"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 0
      },
      {
        "id": "release:shared-scanner",
        "label": "release shared-scanner",
        "requires": [
          "done:relock:shared-scanner"
        ],
        "forbids": [
          "done:release:shared-scanner"
        ],
        "adds": [
          "done:release:shared-scanner",
          "ready:shared-scanner",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner"
        }
      },
      {
        "id": "relock:shared-scanner",
        "label": "relock shared-scanner",
        "requires": [
          "done:verify:shared-scanner"
        ],
        "forbids": [
          "done:relock:shared-scanner"
        ],
        "adds": [
          "done:relock:shared-scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner"
        }
      },
      {
        "id": "verify:shared-scanner",
        "label": "verify shared-scanner",
        "requires": [
          "done:replace:shared-scanner"
        ],
        "forbids": [
          "done:verify:shared-scanner"
        ],
        "adds": [
          "done:verify:shared-scanner"
        ],
        "deletes": [
          "fault:shared-scanner",
          "misaligned:shared-scanner"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner"
        }
      },
      {
        "id": "replace:shared-scanner",
        "label": "replace shared-scanner",
        "requires": [
          "done:unlock:shared-scanner"
        ],
        "forbids": [
          "done:replace:shared-scanner"
        ],
        "adds": [
          "done:replace:shared-scanner"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "shared-scanner"
        }
      },
      {
        "id": "unlock:shared-scanner",
        "label": "unlock shared-scanner",
        "requires": [
          "done:support:shared-scanner"
        ],
        "forbids": [
          "done:unlock:shared-scanner"
        ],
        "adds": [
          "done:unlock:shared-scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner"
        }
      },
      {
        "id": "support:shared-scanner",
        "label": "support shared-scanner",
        "requires": [
          "done:isolate:shared-scanner"
        ],
        "forbids": [
          "done:support:shared-scanner"
        ],
        "adds": [
          "done:support:shared-scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner"
        }
      },
      {
        "id": "isolate:shared-scanner",
        "label": "isolate shared-scanner",
        "requires": [
          "tool:free",
          "fault:shared-scanner"
        ],
        "forbids": [
          "done:isolate:shared-scanner"
        ],
        "adds": [
          "done:isolate:shared-scanner"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shared-scanner"
        }
      },
      {
        "id": "release:shared-inspection-mast",
        "label": "release shared-inspection-mast",
        "requires": [
          "done:relock:shared-inspection-mast"
        ],
        "forbids": [
          "done:release:shared-inspection-mast"
        ],
        "adds": [
          "done:release:shared-inspection-mast",
          "ready:shared-inspection-mast",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast"
        }
      },
      {
        "id": "relock:shared-inspection-mast",
        "label": "relock shared-inspection-mast",
        "requires": [
          "done:verify:shared-inspection-mast"
        ],
        "forbids": [
          "done:relock:shared-inspection-mast"
        ],
        "adds": [
          "done:relock:shared-inspection-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast"
        }
      },
      {
        "id": "verify:shared-inspection-mast",
        "label": "verify shared-inspection-mast",
        "requires": [
          "done:replace:shared-inspection-mast"
        ],
        "forbids": [
          "done:verify:shared-inspection-mast"
        ],
        "adds": [
          "done:verify:shared-inspection-mast"
        ],
        "deletes": [
          "fault:shared-inspection-mast",
          "misaligned:shared-inspection-mast"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast"
        }
      },
      {
        "id": "replace:shared-inspection-mast",
        "label": "replace shared-inspection-mast",
        "requires": [
          "done:unlock:shared-inspection-mast"
        ],
        "forbids": [
          "done:replace:shared-inspection-mast"
        ],
        "adds": [
          "done:replace:shared-inspection-mast"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "shared-inspection-mast"
        }
      },
      {
        "id": "unlock:shared-inspection-mast",
        "label": "unlock shared-inspection-mast",
        "requires": [
          "done:support:shared-inspection-mast"
        ],
        "forbids": [
          "done:unlock:shared-inspection-mast"
        ],
        "adds": [
          "done:unlock:shared-inspection-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast"
        }
      },
      {
        "id": "support:shared-inspection-mast",
        "label": "support shared-inspection-mast",
        "requires": [
          "done:isolate:shared-inspection-mast"
        ],
        "forbids": [
          "done:support:shared-inspection-mast"
        ],
        "adds": [
          "done:support:shared-inspection-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast"
        }
      },
      {
        "id": "isolate:shared-inspection-mast",
        "label": "isolate shared-inspection-mast",
        "requires": [
          "tool:free",
          "fault:shared-inspection-mast"
        ],
        "forbids": [
          "done:isolate:shared-inspection-mast"
        ],
        "adds": [
          "done:isolate:shared-inspection-mast"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shared-inspection-mast"
        }
      },
      {
        "id": "release:cell-2-drawer",
        "label": "release cell-2-drawer",
        "requires": [
          "done:relock:cell-2-drawer"
        ],
        "forbids": [
          "done:release:cell-2-drawer"
        ],
        "adds": [
          "done:release:cell-2-drawer",
          "ready:cell-2-drawer",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer"
        }
      },
      {
        "id": "relock:cell-2-drawer",
        "label": "relock cell-2-drawer",
        "requires": [
          "done:verify:cell-2-drawer"
        ],
        "forbids": [
          "done:relock:cell-2-drawer"
        ],
        "adds": [
          "done:relock:cell-2-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer"
        }
      },
      {
        "id": "verify:cell-2-drawer",
        "label": "verify cell-2-drawer",
        "requires": [
          "done:replace:cell-2-drawer"
        ],
        "forbids": [
          "done:verify:cell-2-drawer"
        ],
        "adds": [
          "done:verify:cell-2-drawer"
        ],
        "deletes": [
          "fault:cell-2-drawer",
          "misaligned:cell-2-drawer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer"
        }
      },
      {
        "id": "replace:cell-2-drawer",
        "label": "replace cell-2-drawer",
        "requires": [
          "done:unlock:cell-2-drawer"
        ],
        "forbids": [
          "done:replace:cell-2-drawer"
        ],
        "adds": [
          "done:replace:cell-2-drawer"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-2-drawer"
        }
      },
      {
        "id": "unlock:cell-2-drawer",
        "label": "unlock cell-2-drawer",
        "requires": [
          "done:support:cell-2-drawer"
        ],
        "forbids": [
          "done:unlock:cell-2-drawer"
        ],
        "adds": [
          "done:unlock:cell-2-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer"
        }
      },
      {
        "id": "support:cell-2-drawer",
        "label": "support cell-2-drawer",
        "requires": [
          "done:isolate:cell-2-drawer"
        ],
        "forbids": [
          "done:support:cell-2-drawer"
        ],
        "adds": [
          "done:support:cell-2-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer"
        }
      },
      {
        "id": "isolate:cell-2-drawer",
        "label": "isolate cell-2-drawer",
        "requires": [
          "tool:free",
          "fault:cell-2-drawer"
        ],
        "forbids": [
          "done:isolate:cell-2-drawer"
        ],
        "adds": [
          "done:isolate:cell-2-drawer"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-drawer"
        }
      },
      {
        "id": "release:cell-2-magazine",
        "label": "release cell-2-magazine",
        "requires": [
          "done:relock:cell-2-magazine"
        ],
        "forbids": [
          "done:release:cell-2-magazine"
        ],
        "adds": [
          "done:release:cell-2-magazine",
          "ready:cell-2-magazine",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine"
        }
      },
      {
        "id": "relock:cell-2-magazine",
        "label": "relock cell-2-magazine",
        "requires": [
          "done:verify:cell-2-magazine"
        ],
        "forbids": [
          "done:relock:cell-2-magazine"
        ],
        "adds": [
          "done:relock:cell-2-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine"
        }
      },
      {
        "id": "verify:cell-2-magazine",
        "label": "verify cell-2-magazine",
        "requires": [
          "done:replace:cell-2-magazine"
        ],
        "forbids": [
          "done:verify:cell-2-magazine"
        ],
        "adds": [
          "done:verify:cell-2-magazine"
        ],
        "deletes": [
          "fault:cell-2-magazine",
          "misaligned:cell-2-magazine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine"
        }
      },
      {
        "id": "replace:cell-2-magazine",
        "label": "replace cell-2-magazine",
        "requires": [
          "done:unlock:cell-2-magazine"
        ],
        "forbids": [
          "done:replace:cell-2-magazine"
        ],
        "adds": [
          "done:replace:cell-2-magazine"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-2-magazine"
        }
      },
      {
        "id": "unlock:cell-2-magazine",
        "label": "unlock cell-2-magazine",
        "requires": [
          "done:support:cell-2-magazine"
        ],
        "forbids": [
          "done:unlock:cell-2-magazine"
        ],
        "adds": [
          "done:unlock:cell-2-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine"
        }
      },
      {
        "id": "support:cell-2-magazine",
        "label": "support cell-2-magazine",
        "requires": [
          "done:isolate:cell-2-magazine"
        ],
        "forbids": [
          "done:support:cell-2-magazine"
        ],
        "adds": [
          "done:support:cell-2-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine"
        }
      },
      {
        "id": "isolate:cell-2-magazine",
        "label": "isolate cell-2-magazine",
        "requires": [
          "tool:free",
          "fault:cell-2-magazine"
        ],
        "forbids": [
          "done:isolate:cell-2-magazine"
        ],
        "adds": [
          "done:isolate:cell-2-magazine"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-magazine"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-2-magazine",
      "fault:cell-2-drawer",
      "fault:shared-inspection-mast",
      "fault:shared-scanner"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-yoke",
      "cell-0-cradle",
      "cell-0-optic",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-hub",
      "cell-1-wing-0",
      "cell-1-wing-1",
      "cell-1-wing-2",
      "cell-1-wing-3",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-probe-0",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "goalFacts": [
      "ready:cell-2-magazine",
      "ready:cell-2-drawer",
      "ready:shared-inspection-mast",
      "ready:shared-scanner"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:shared-scanner",
      "support:shared-scanner",
      "unlock:shared-scanner",
      "replace:shared-scanner",
      "verify:shared-scanner",
      "relock:shared-scanner",
      "release:shared-scanner",
      "isolate:shared-inspection-mast",
      "support:shared-inspection-mast",
      "unlock:shared-inspection-mast",
      "replace:shared-inspection-mast",
      "verify:shared-inspection-mast",
      "relock:shared-inspection-mast",
      "release:shared-inspection-mast",
      "isolate:cell-2-drawer",
      "support:cell-2-drawer",
      "unlock:cell-2-drawer",
      "replace:cell-2-drawer",
      "verify:cell-2-drawer",
      "relock:cell-2-drawer",
      "release:cell-2-drawer",
      "isolate:cell-2-magazine",
      "support:cell-2-magazine",
      "unlock:cell-2-magazine",
      "replace:cell-2-magazine",
      "verify:cell-2-magazine",
      "relock:cell-2-magazine",
      "release:cell-2-magazine"
    ]
  }
}
```

### 预算约束检查策略（h3-exp-d4-cradle-1-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-optic",
    "worlds": [
      {
        "id": "nominal",
        "action": "continue"
      },
      {
        "id": "fault",
        "action": "tighten"
      }
    ],
    "queries": [
      {
        "id": "visual",
        "cost": 3,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      },
      {
        "id": "probe",
        "cost": 2,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      },
      {
        "id": "thermal",
        "cost": 0,
        "returns": {
          "nominal": "pass",
          "fault": "pass"
        }
      }
    ],
    "budget": 2
  },
  "answer": {
    "queryId": "probe",
    "decisions": {
      "pass": "continue",
      "fail": "tighten"
    }
  }
}
```
