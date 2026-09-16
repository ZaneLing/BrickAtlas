## D4 协同系统·双段取样臂

### 模块识别（h3-exp-d4-arm-2-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：cell-0-mount
- B：cell-0-tool
- C：foundation
- D：cell-0-shuttle

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
        "id": "cell-0-shoulder",
        "name": "cell 0 shoulder"
      },
      {
        "id": "cell-0-elbow",
        "name": "cell 0 elbow"
      },
      {
        "id": "cell-0-wrist",
        "name": "cell 0 wrist"
      },
      {
        "id": "cell-0-tool",
        "name": "cell 0 tool"
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
        "id": "cell-1-yoke",
        "name": "cell 1 yoke"
      },
      {
        "id": "cell-1-cradle",
        "name": "cell 1 cradle"
      },
      {
        "id": "cell-1-optic",
        "name": "cell 1 optic"
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
        "id": "cell-2-wing-0",
        "name": "cell 2 wing 0"
      },
      {
        "id": "cell-2-wing-1",
        "name": "cell 2 wing 1"
      },
      {
        "id": "cell-2-wing-2",
        "name": "cell 2 wing 2"
      },
      {
        "id": "cell-2-wing-3",
        "name": "cell 2 wing 3"
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
        "id": "cell-3-shuttle",
        "name": "cell 3 shuttle"
      },
      {
        "id": "cell-3-mount",
        "name": "cell 3 mount"
      },
      {
        "id": "cell-3-hub",
        "name": "cell 3 hub"
      },
      {
        "id": "cell-3-probe-0",
        "name": "cell 3 probe 0"
      },
      {
        "id": "cell-3-console",
        "name": "cell 3 console"
      },
      {
        "id": "cell-3-magazine",
        "name": "cell 3 magazine"
      },
      {
        "id": "cell-3-drawer",
        "name": "cell 3 drawer"
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
    "choiceId": "B"
  }
}
```

### 部件计数（h3-exp-d4-arm-2-count）

模块 cell-0-tool 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：2
- B：3
- C：1
- D：5

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
        "id": "foundation-p180",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p181",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p182",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p183",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p184",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p185",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p186",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p187",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p188",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p189",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p190",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p191",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p192",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p193",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p194",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p195",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p196",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p197",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p198",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p199",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p200",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p201",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p202",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p203",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p204",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p205",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p206",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p207",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p208",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p209",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p210",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p211",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p212",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p213",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p214",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p215",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p216",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p217",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p218",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p219",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p220",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p221",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p222",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p223",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p224",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p225",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p226",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p227",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p228",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p229",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p230",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p231",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p232",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p233",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p234",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p235",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p236",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p237",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p238",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p239",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p240",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "foundation-p241",
        "moduleId": "foundation",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "cell-0-shuttle-p242",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p243",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p244",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p245",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p246",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p247",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p248",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p249",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p250",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p251",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p252",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p253",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p254",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p255",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p256",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p257",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p258",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p259",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p260",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p261",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p262",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p263",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p264",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p265",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p266",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p267",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p268",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p269",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p270",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p271",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p272",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p273",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p274",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p275",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p276",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p277",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p278",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p279",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p280",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p281",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p282",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p283",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p284",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p285",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p286",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p287",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p288",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p289",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-mount-p290",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p291",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p292",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p293",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p294",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p295",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p296",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p297",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p298",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p299",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p300",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p301",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p302",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p303",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p304",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p305",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p306",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p307",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p308",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p309",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p310",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p311",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p312",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p313",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p314",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p315",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p316",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p317",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p318",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p319",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p320",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p321",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p322",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p323",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p324",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-shoulder-p325",
        "moduleId": "cell-0-shoulder",
        "shape": "cylinder",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-elbow-p326",
        "moduleId": "cell-0-elbow",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-elbow-p327",
        "moduleId": "cell-0-elbow",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-elbow-p328",
        "moduleId": "cell-0-elbow",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-elbow-p329",
        "moduleId": "cell-0-elbow",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-wrist-p330",
        "moduleId": "cell-0-wrist",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-wrist-p331",
        "moduleId": "cell-0-wrist",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-wrist-p332",
        "moduleId": "cell-0-wrist",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-tool-p333",
        "moduleId": "cell-0-tool",
        "shape": "arch",
        "color": "#45a080"
      },
      {
        "id": "cell-0-tool-p334",
        "moduleId": "cell-0-tool",
        "shape": "axle",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-console-p335",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p336",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p337",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p338",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p339",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p340",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p341",
        "moduleId": "cell-0-console",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-0-console-p342",
        "moduleId": "cell-0-console",
        "shape": "slope",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p343",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p344",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p345",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p346",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p347",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p348",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p349",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p350",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p351",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p352",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p353",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p354",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p355",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p356",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p357",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p358",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p359",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p360",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p361",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p362",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p363",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p364",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p365",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p366",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p367",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p368",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p369",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p370",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p371",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p372",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p373",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p374",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p375",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p376",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p377",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p378",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p379",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p380",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p381",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p382",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p383",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p384",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p385",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p386",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p387",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p388",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p389",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p390",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p391",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p392",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p393",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p394",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p395",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p396",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p397",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p398",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p399",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p400",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-drawer-p401",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p402",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p403",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p404",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p405",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p406",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-shuttle-p407",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p408",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p409",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p410",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p411",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p412",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p413",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p414",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p415",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p416",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p417",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p418",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p419",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p420",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p421",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p422",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p423",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p424",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p425",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p426",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p427",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p428",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p429",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p430",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p431",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p432",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p433",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p434",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p435",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p436",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p437",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p438",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p439",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p440",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p441",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p442",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p443",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p444",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p445",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p446",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p447",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p448",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p449",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p450",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p451",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p452",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p453",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p454",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-mount-p455",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p456",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p457",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p458",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p459",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p460",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p461",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p462",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p463",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p464",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p465",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p466",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p467",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p468",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p469",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p470",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p471",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p472",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p473",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p474",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p475",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p476",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p477",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p478",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p479",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p480",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p481",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p482",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p483",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p484",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-yoke-p485",
        "moduleId": "cell-1-yoke",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-yoke-p486",
        "moduleId": "cell-1-yoke",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-yoke-p487",
        "moduleId": "cell-1-yoke",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-yoke-p488",
        "moduleId": "cell-1-yoke",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-yoke-p489",
        "moduleId": "cell-1-yoke",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-yoke-p490",
        "moduleId": "cell-1-yoke",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-yoke-p491",
        "moduleId": "cell-1-yoke",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-yoke-p492",
        "moduleId": "cell-1-yoke",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-yoke-p493",
        "moduleId": "cell-1-yoke",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-yoke-p494",
        "moduleId": "cell-1-yoke",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-yoke-p495",
        "moduleId": "cell-1-yoke",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-cradle-p496",
        "moduleId": "cell-1-cradle",
        "shape": "cylinder",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-optic-p497",
        "moduleId": "cell-1-optic",
        "shape": "cylinder",
        "color": "#45a080"
      },
      {
        "id": "cell-1-optic-p498",
        "moduleId": "cell-1-optic",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-1-console-p499",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p500",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p501",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p502",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p503",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p504",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p505",
        "moduleId": "cell-1-console",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-1-console-p506",
        "moduleId": "cell-1-console",
        "shape": "slope",
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
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p517",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p518",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p519",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p520",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p521",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p522",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p523",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p524",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p525",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p526",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p527",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p528",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p529",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p530",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p531",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p532",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p533",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p534",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p535",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p536",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p537",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p538",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p539",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p540",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p541",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p542",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p543",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p544",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p545",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p546",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p547",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p548",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p549",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p550",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p551",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p552",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p553",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p554",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p555",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p556",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p557",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p558",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p559",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p560",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p561",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p562",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p563",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p564",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-drawer-p565",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p566",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p567",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p568",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p569",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p570",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
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
        "id": "cell-2-shuttle-p580",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p581",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p582",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p583",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p584",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p585",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p586",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p587",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p588",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p589",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p590",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p591",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p592",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p593",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p594",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p595",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p596",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p597",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p598",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p599",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p600",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p601",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p602",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p603",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p604",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p605",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p606",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p607",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p608",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p609",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p610",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p611",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p612",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p613",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p614",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p615",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p616",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p617",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-shuttle-p618",
        "moduleId": "cell-2-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-mount-p619",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p620",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p621",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p622",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p623",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p624",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p625",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p626",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p627",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p628",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p629",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p630",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p631",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p632",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p633",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p634",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p635",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p636",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p637",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p638",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p639",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p640",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p641",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p642",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p643",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p644",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p645",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p646",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p647",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p648",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p649",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p650",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p651",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p652",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-mount-p653",
        "moduleId": "cell-2-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-2-hub-p654",
        "moduleId": "cell-2-hub",
        "shape": "cylinder",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-wing-0-p655",
        "moduleId": "cell-2-wing-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-0-p656",
        "moduleId": "cell-2-wing-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-0-p657",
        "moduleId": "cell-2-wing-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-0-p658",
        "moduleId": "cell-2-wing-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-0-p659",
        "moduleId": "cell-2-wing-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-0-p660",
        "moduleId": "cell-2-wing-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-0-p661",
        "moduleId": "cell-2-wing-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-wing-0-p662",
        "moduleId": "cell-2-wing-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-wing-1-p663",
        "moduleId": "cell-2-wing-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-1-p664",
        "moduleId": "cell-2-wing-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-1-p665",
        "moduleId": "cell-2-wing-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-1-p666",
        "moduleId": "cell-2-wing-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-1-p667",
        "moduleId": "cell-2-wing-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-1-p668",
        "moduleId": "cell-2-wing-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-1-p669",
        "moduleId": "cell-2-wing-1",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-wing-1-p670",
        "moduleId": "cell-2-wing-1",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-wing-2-p671",
        "moduleId": "cell-2-wing-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-2-p672",
        "moduleId": "cell-2-wing-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-2-p673",
        "moduleId": "cell-2-wing-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-2-p674",
        "moduleId": "cell-2-wing-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-2-p675",
        "moduleId": "cell-2-wing-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-2-p676",
        "moduleId": "cell-2-wing-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-2-p677",
        "moduleId": "cell-2-wing-2",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-wing-2-p678",
        "moduleId": "cell-2-wing-2",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-wing-3-p679",
        "moduleId": "cell-2-wing-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-3-p680",
        "moduleId": "cell-2-wing-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-3-p681",
        "moduleId": "cell-2-wing-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-3-p682",
        "moduleId": "cell-2-wing-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-3-p683",
        "moduleId": "cell-2-wing-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-3-p684",
        "moduleId": "cell-2-wing-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-2-wing-3-p685",
        "moduleId": "cell-2-wing-3",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-wing-3-p686",
        "moduleId": "cell-2-wing-3",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-console-p687",
        "moduleId": "cell-2-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-2-console-p688",
        "moduleId": "cell-2-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-2-console-p689",
        "moduleId": "cell-2-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-2-console-p690",
        "moduleId": "cell-2-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-2-console-p691",
        "moduleId": "cell-2-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-2-console-p692",
        "moduleId": "cell-2-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-2-console-p693",
        "moduleId": "cell-2-console",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-2-console-p694",
        "moduleId": "cell-2-console",
        "shape": "slope",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p695",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p696",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p697",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p698",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p699",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p700",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p701",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p702",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p703",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p704",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p705",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p706",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p707",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p708",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p709",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p710",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p711",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p712",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p713",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p714",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p715",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p716",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p717",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p718",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p719",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p720",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p721",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p722",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p723",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p724",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p725",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p726",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p727",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p728",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p729",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p730",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p731",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p732",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p733",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p734",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p735",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p736",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p737",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p738",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p739",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p740",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p741",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p742",
        "moduleId": "cell-2-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-2-magazine-p743",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p744",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p745",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p746",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p747",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p748",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p749",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p750",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p751",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-magazine-p752",
        "moduleId": "cell-2-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-2-drawer-p753",
        "moduleId": "cell-2-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-2-drawer-p754",
        "moduleId": "cell-2-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-2-drawer-p755",
        "moduleId": "cell-2-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-2-drawer-p756",
        "moduleId": "cell-2-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-2-drawer-p757",
        "moduleId": "cell-2-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-2-drawer-p758",
        "moduleId": "cell-2-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-3-shuttle-p759",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p760",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p761",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p762",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p763",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p764",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p765",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p766",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p767",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p768",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p769",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p770",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p771",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p772",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p773",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p774",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p775",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p776",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p777",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p778",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p779",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p780",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p781",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p782",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p783",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p784",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p785",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p786",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p787",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p788",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p789",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p790",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p791",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p792",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p793",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p794",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p795",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p796",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p797",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p798",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p799",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p800",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p801",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p802",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p803",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p804",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p805",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-shuttle-p806",
        "moduleId": "cell-3-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-mount-p807",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p808",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p809",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p810",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p811",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p812",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p813",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p814",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p815",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p816",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p817",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p818",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p819",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p820",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p821",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p822",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p823",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p824",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p825",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p826",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p827",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p828",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p829",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p830",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p831",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p832",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p833",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p834",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p835",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-mount-p836",
        "moduleId": "cell-3-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-3-hub-p837",
        "moduleId": "cell-3-hub",
        "shape": "cylinder",
        "color": "#387bb3"
      },
      {
        "id": "cell-3-probe-0-p838",
        "moduleId": "cell-3-probe-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-probe-0-p839",
        "moduleId": "cell-3-probe-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-probe-0-p840",
        "moduleId": "cell-3-probe-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-probe-0-p841",
        "moduleId": "cell-3-probe-0",
        "shape": "sphere",
        "color": "#45a080"
      },
      {
        "id": "cell-3-console-p842",
        "moduleId": "cell-3-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-3-console-p843",
        "moduleId": "cell-3-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-3-console-p844",
        "moduleId": "cell-3-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-3-console-p845",
        "moduleId": "cell-3-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-3-console-p846",
        "moduleId": "cell-3-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-3-console-p847",
        "moduleId": "cell-3-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-3-console-p848",
        "moduleId": "cell-3-console",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-3-console-p849",
        "moduleId": "cell-3-console",
        "shape": "slope",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p850",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p851",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p852",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p853",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p854",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p855",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p856",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p857",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p858",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p859",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p860",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p861",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p862",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p863",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p864",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p865",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p866",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p867",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p868",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p869",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p870",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p871",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p872",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p873",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p874",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p875",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p876",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p877",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p878",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p879",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p880",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p881",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p882",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p883",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p884",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p885",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p886",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p887",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p888",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p889",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p890",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p891",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p892",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p893",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p894",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p895",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p896",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p897",
        "moduleId": "cell-3-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-3-magazine-p898",
        "moduleId": "cell-3-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-magazine-p899",
        "moduleId": "cell-3-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-magazine-p900",
        "moduleId": "cell-3-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-magazine-p901",
        "moduleId": "cell-3-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-magazine-p902",
        "moduleId": "cell-3-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-magazine-p903",
        "moduleId": "cell-3-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-magazine-p904",
        "moduleId": "cell-3-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-magazine-p905",
        "moduleId": "cell-3-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-magazine-p906",
        "moduleId": "cell-3-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-magazine-p907",
        "moduleId": "cell-3-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-3-drawer-p908",
        "moduleId": "cell-3-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-3-drawer-p909",
        "moduleId": "cell-3-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-3-drawer-p910",
        "moduleId": "cell-3-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-3-drawer-p911",
        "moduleId": "cell-3-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-3-drawer-p912",
        "moduleId": "cell-3-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-3-drawer-p913",
        "moduleId": "cell-3-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "shared-inspection-mast-p914",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p915",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p916",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p917",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p918",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p919",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p920",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p921",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p922",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p923",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "shared-inspection-mast-p924",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "shared-inspection-mast-p925",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "shared-inspection-mast-p926",
        "moduleId": "shared-inspection-mast",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "shared-scanner-p927",
        "moduleId": "shared-scanner",
        "shape": "cylinder",
        "color": "#dc6040"
      },
      {
        "id": "shared-scanner-p928",
        "moduleId": "shared-scanner",
        "shape": "window",
        "color": "#79c7d8"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-exp-d4-arm-2-color）

零件 cell-0-tool-p333 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#f2bf3c
- B：#45a080
- C：#2878b8
- D：#d43a32

```json
{
  "input": {
    "part": {
      "id": "cell-0-tool-p333",
      "moduleId": "cell-0-tool",
      "shape": "arch",
      "position": [
        0,
        0.2625000000000002,
        0
      ],
      "size": [
        0.65,
        0.65,
        0.65
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
    "choiceId": "B"
  }
}
```

### 三维位置（h3-exp-d4-arm-2-position）

模块 cell-0-tool 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[-16.9,4.5375,1.3]
- B：[0,0.2,0]
- C：[-19.5,0.75,0]
- D：[-19.5,1.35,0]

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
        -19.5,
        0.75,
        0
      ],
      "cell-0-mount": [
        -19.5,
        1.35,
        0
      ],
      "cell-0-shoulder": [
        -21.2,
        2,
        0
      ],
      "cell-0-elbow": [
        -20.45,
        4.1,
        0
      ],
      "cell-0-wrist": [
        -18.35,
        5.2,
        0.7
      ],
      "cell-0-tool": [
        -16.9,
        4.5375,
        1.3
      ],
      "cell-0-console": [
        -19.5,
        1.8775000000000002,
        6
      ],
      "cell-0-magazine": [
        -19.5,
        3.1399999999999997,
        -6
      ],
      "cell-0-drawer": [
        -19.5,
        1.55,
        -6
      ],
      "cell-1-shuttle": [
        -6.5,
        0.75,
        0
      ],
      "cell-1-mount": [
        -6.5,
        1.35,
        0
      ],
      "cell-1-yoke": [
        -6.499999999999999,
        3.325,
        0
      ],
      "cell-1-cradle": [
        -6.5,
        4.6,
        0
      ],
      "cell-1-optic": [
        -6.5,
        5.949999999999999,
        0
      ],
      "cell-1-console": [
        -6.5,
        1.8775000000000002,
        6
      ],
      "cell-1-magazine": [
        -6.5,
        3.1399999999999997,
        -6
      ],
      "cell-1-drawer": [
        -6.5,
        1.55,
        -6
      ],
      "cell-2-shuttle": [
        6.5,
        0.75,
        0
      ],
      "cell-2-mount": [
        6.5,
        1.35,
        0
      ],
      "cell-2-hub": [
        6.5,
        2.8,
        0
      ],
      "cell-2-wing-0": [
        9,
        4.3225,
        0
      ],
      "cell-2-wing-1": [
        6.5,
        4.442500000000001,
        2.5
      ],
      "cell-2-wing-2": [
        4,
        4.5625,
        4.440892098500626e-16
      ],
      "cell-2-wing-3": [
        6.499999999999999,
        4.682499999999999,
        -2.5
      ],
      "cell-2-console": [
        6.5,
        1.8775000000000002,
        6
      ],
      "cell-2-magazine": [
        6.5,
        3.1399999999999997,
        -6
      ],
      "cell-2-drawer": [
        6.5,
        1.55,
        -6
      ],
      "cell-3-shuttle": [
        19.5,
        0.75,
        0
      ],
      "cell-3-mount": [
        19.5,
        1.35,
        0
      ],
      "cell-3-hub": [
        19.5,
        2.3,
        0
      ],
      "cell-3-probe-0": [
        21.33629800496756,
        4.701658603477292,
        0
      ],
      "cell-3-console": [
        19.5,
        1.8775000000000002,
        6
      ],
      "cell-3-magazine": [
        19.5,
        3.1399999999999997,
        -6
      ],
      "cell-3-drawer": [
        19.5,
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
    "choiceId": "A"
  }
}
```

### 关节类型（h3-exp-d4-arm-2-joint-type）

cell-0-elbow-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：spring
- B：revolute
- C：fixed
- D：prismatic

```json
{
  "input": {
    "joint": {
      "id": "cell-0-elbow-joint",
      "name": "cell-0-elbow interface",
      "parent": "cell-0-shoulder",
      "child": "cell-0-elbow",
      "type": "revolute",
      "anchorParent": [
        0,
        0.6500000000000004,
        0
      ],
      "anchorChild": [
        -0.75,
        -1.4499999999999993,
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
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 直接连接（h3-exp-d4-arm-2-parent）

cell-0-tool 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["cell-0-tool"]
- B：[]
- C：["foundation","cell-0-shuttle","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-yoke","cell-1-cradle","cell-1-optic","cell-1-console","cell-1-magazine","cell-1-drawer","cell-2-shuttle","cell-2-mount","cell-2-hub","cell-2-wing-0","cell-2-wing-1","cell-2-wing-2","cell-2-wing-3","cell-2-console","cell-2-magazine","cell-2-drawer","cell-3-shuttle","cell-3-mount","cell-3-hub","cell-3-probe-0","cell-3-console","cell-3-magazine","cell-3-drawer","shared-inspection-mast","shared-scanner"]
- D：["cell-0-wrist"]

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
          -19.5,
          0.4999999999999999,
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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.6999999999999993,
          0.6499999999999999,
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
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000004,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.4499999999999993,
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
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.4500000000000002,
          0.7
        ],
        "anchorChild": [
          -1.3499999999999979,
          0.34999999999999964,
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
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.4500000000000028,
          -0.40000000000000036,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -19.5,
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
          -19.5,
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
          -6.5,
          0.4999999999999999,
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
        "id": "cell-1-yoke-joint",
        "name": "cell-1-yoke interface",
        "parent": "cell-1-mount",
        "child": "cell-1-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          -8.881784197001252e-16,
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
        "id": "cell-1-cradle-joint",
        "name": "cell-1-cradle interface",
        "parent": "cell-1-yoke",
        "child": "cell-1-cradle",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
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
        "id": "cell-1-optic-joint",
        "name": "cell-1-optic interface",
        "parent": "cell-1-cradle",
        "child": "cell-1-optic",
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          -6.5,
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
          -6.5,
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
          6.5,
          0.4999999999999999,
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
        "id": "cell-2-wing-0-joint",
        "name": "cell-2-wing-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-0",
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
        "id": "cell-2-wing-1-joint",
        "name": "cell-2-wing-1 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-wing-2-joint",
        "name": "cell-2-wing-2 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-2",
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
        "id": "cell-2-wing-3-joint",
        "name": "cell-2-wing-3 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-3",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          6.5,
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
          6.5,
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
        "id": "cell-3-shuttle-joint",
        "name": "cell-3-shuttle interface",
        "parent": "foundation",
        "child": "cell-3-shuttle",
        "type": "prismatic",
        "anchorParent": [
          19.5,
          0.4999999999999999,
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
        "id": "cell-3-mount-joint",
        "name": "cell-3-mount interface",
        "parent": "cell-3-shuttle",
        "child": "cell-3-mount",
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
        "id": "cell-3-hub-joint",
        "name": "cell-3-hub interface",
        "parent": "cell-3-mount",
        "child": "cell-3-hub",
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
        "id": "cell-3-probe-0-joint",
        "name": "cell-3-probe-0 interface",
        "parent": "cell-3-hub",
        "child": "cell-3-probe-0",
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
        "id": "cell-3-console-joint",
        "name": "cell-3-console interface",
        "parent": "foundation",
        "child": "cell-3-console",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-magazine-joint",
        "name": "cell-3-magazine interface",
        "parent": "foundation",
        "child": "cell-3-magazine",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-drawer-joint",
        "name": "cell-3-drawer interface",
        "parent": "cell-3-magazine",
        "child": "cell-3-drawer",
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

### 基座识别（h3-exp-d4-arm-2-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["foundation"]
- B：[]
- C：["foundation","cell-0-shuttle","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-yoke","cell-1-cradle","cell-1-optic","cell-1-console","cell-1-magazine","cell-1-drawer","cell-2-shuttle","cell-2-mount","cell-2-hub","cell-2-wing-0","cell-2-wing-1","cell-2-wing-2","cell-2-wing-3","cell-2-console","cell-2-magazine","cell-2-drawer","cell-3-shuttle","cell-3-mount","cell-3-hub","cell-3-probe-0","cell-3-console","cell-3-magazine","cell-3-drawer","shared-inspection-mast","shared-scanner"]
- D：["cell-0-tool"]

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
          -19.5,
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
          -19.5,
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
        "id": "cell-0-shoulder",
        "name": "cell 0 shoulder",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -21.2,
          2,
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
        "id": "cell-0-elbow",
        "name": "cell 0 elbow",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -20.45,
          4.1,
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
        "id": "cell-0-wrist",
        "name": "cell 0 wrist",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -18.35,
          5.2,
          0.7
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-tool",
        "name": "cell 0 tool",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -16.9,
          4.5375,
          1.3
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
          -19.5,
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
          -19.5,
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
          -19.5,
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
          -6.5,
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
          -6.5,
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
        "id": "cell-1-yoke",
        "name": "cell 1 yoke",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -6.499999999999999,
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
        "id": "cell-1-cradle",
        "name": "cell 1 cradle",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -6.5,
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
        "id": "cell-1-optic",
        "name": "cell 1 optic",
        "role": "structure",
        "anchored": false,
        "mass": 0.5,
        "position": [
          -6.5,
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
        "id": "cell-1-console",
        "name": "cell 1 console",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -6.5,
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
          -6.5,
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
          -6.5,
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
          6.5,
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
          6.5,
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
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          6.5,
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
        "id": "cell-2-wing-0",
        "name": "cell 2 wing 0",
        "role": "actuator",
        "anchored": false,
        "mass": 0.65,
        "position": [
          9,
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
        "id": "cell-2-wing-1",
        "name": "cell 2 wing 1",
        "role": "actuator",
        "anchored": false,
        "mass": 0.65,
        "position": [
          6.5,
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
        "id": "cell-2-wing-2",
        "name": "cell 2 wing 2",
        "role": "actuator",
        "anchored": false,
        "mass": 0.65,
        "position": [
          4,
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
        "id": "cell-2-wing-3",
        "name": "cell 2 wing 3",
        "role": "actuator",
        "anchored": false,
        "mass": 0.65,
        "position": [
          6.499999999999999,
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
        "id": "cell-2-console",
        "name": "cell 2 console",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          6.5,
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
          6.5,
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
          6.5,
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
        "id": "cell-3-shuttle",
        "name": "cell 3 shuttle",
        "role": "actuator",
        "anchored": false,
        "mass": 3,
        "position": [
          19.5,
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
        "id": "cell-3-mount",
        "name": "cell 3 mount",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          19.5,
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
        "id": "cell-3-hub",
        "name": "cell 3 hub",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          19.5,
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
        "id": "cell-3-probe-0",
        "name": "cell 3 probe 0",
        "role": "actuator",
        "anchored": false,
        "mass": 0.5,
        "position": [
          21.33629800496756,
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
        "id": "cell-3-console",
        "name": "cell 3 console",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          19.5,
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
        "id": "cell-3-magazine",
        "name": "cell 3 magazine",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          19.5,
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
        "id": "cell-3-drawer",
        "name": "cell 3 drawer",
        "role": "actuator",
        "anchored": false,
        "mass": 0.7,
        "position": [
          19.5,
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
    "choiceId": "A"
  }
}
```

### 接口计数（h3-exp-d4-arm-2-degree）

cell-0-tool 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：3
- B：1
- C：2
- D：0

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
          -19.5,
          0.4999999999999999,
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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.6999999999999993,
          0.6499999999999999,
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
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000004,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.4499999999999993,
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
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.4500000000000002,
          0.7
        ],
        "anchorChild": [
          -1.3499999999999979,
          0.34999999999999964,
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
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.4500000000000028,
          -0.40000000000000036,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -19.5,
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
          -19.5,
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
          -6.5,
          0.4999999999999999,
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
        "id": "cell-1-yoke-joint",
        "name": "cell-1-yoke interface",
        "parent": "cell-1-mount",
        "child": "cell-1-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          -8.881784197001252e-16,
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
        "id": "cell-1-cradle-joint",
        "name": "cell-1-cradle interface",
        "parent": "cell-1-yoke",
        "child": "cell-1-cradle",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
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
        "id": "cell-1-optic-joint",
        "name": "cell-1-optic interface",
        "parent": "cell-1-cradle",
        "child": "cell-1-optic",
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          -6.5,
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
          -6.5,
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
          6.5,
          0.4999999999999999,
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
        "id": "cell-2-wing-0-joint",
        "name": "cell-2-wing-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-0",
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
        "id": "cell-2-wing-1-joint",
        "name": "cell-2-wing-1 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-wing-2-joint",
        "name": "cell-2-wing-2 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-2",
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
        "id": "cell-2-wing-3-joint",
        "name": "cell-2-wing-3 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-3",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          6.5,
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
          6.5,
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
        "id": "cell-3-shuttle-joint",
        "name": "cell-3-shuttle interface",
        "parent": "foundation",
        "child": "cell-3-shuttle",
        "type": "prismatic",
        "anchorParent": [
          19.5,
          0.4999999999999999,
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
        "id": "cell-3-mount-joint",
        "name": "cell-3-mount interface",
        "parent": "cell-3-shuttle",
        "child": "cell-3-mount",
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
        "id": "cell-3-hub-joint",
        "name": "cell-3-hub interface",
        "parent": "cell-3-mount",
        "child": "cell-3-hub",
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
        "id": "cell-3-probe-0-joint",
        "name": "cell-3-probe-0 interface",
        "parent": "cell-3-hub",
        "child": "cell-3-probe-0",
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
        "id": "cell-3-console-joint",
        "name": "cell-3-console interface",
        "parent": "foundation",
        "child": "cell-3-console",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-magazine-joint",
        "name": "cell-3-magazine interface",
        "parent": "foundation",
        "child": "cell-3-magazine",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-drawer-joint",
        "name": "cell-3-drawer interface",
        "parent": "cell-3-magazine",
        "child": "cell-3-drawer",
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
    "choiceId": "B"
  }
}
```

### 局部改色（h3-exp-d4-arm-2-recolor）

仅将 cell-0-tool-p333 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-tool-p334","color":"#e8792e"}
- B：{"id":"cell-0-tool-p333","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"cell-0-tool-p333","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "cell-0-tool-p333",
      "moduleId": "cell-0-tool",
      "shape": "arch",
      "position": [
        0,
        0.2625000000000002,
        0
      ],
      "size": [
        0.65,
        0.65,
        0.65
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

### 补装部件（h3-exp-d4-arm-2-add）

模块 cell-0-tool 缺失零件 cell-0-tool-p333。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-tool-p333","moduleId":"cell-0-tool","shape":"arch","position":[0,0.2625000000000002,0],"size":[0.65,0.65,0.65],"color":"#45a080","rotation":[0,0,0,1]}
- B：{"id":"cell-0-tool-p333","moduleId":"foundation","shape":"arch","position":[0,0.2625000000000002,0],"size":[0.65,0.65,0.65],"color":"#45a080","rotation":[0,0,0,1]}
- C：{"id":"cell-0-tool-p333","moduleId":"cell-0-tool","shape":"arch","position":[0,0.2625000000000002,0],"size":[3,3,3],"color":"#45a080","rotation":[0,0,0,1]}
- D：{"id":"cell-0-tool-p333","moduleId":"cell-0-tool","shape":"arch","position":[0,0.2625000000000002,0],"size":[0.65,0.65,0.65],"color":"#000000","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "cell-0-tool-p333",
      "moduleId": "cell-0-tool",
      "shape": "arch",
      "position": [
        0,
        0.2625000000000002,
        0
      ],
      "size": [
        0.65,
        0.65,
        0.65
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
      "foundation-p180",
      "foundation-p181",
      "foundation-p182",
      "foundation-p183",
      "foundation-p184",
      "foundation-p185",
      "foundation-p186",
      "foundation-p187",
      "foundation-p188",
      "foundation-p189",
      "foundation-p190",
      "foundation-p191",
      "foundation-p192",
      "foundation-p193",
      "foundation-p194",
      "foundation-p195",
      "foundation-p196",
      "foundation-p197",
      "foundation-p198",
      "foundation-p199",
      "foundation-p200",
      "foundation-p201",
      "foundation-p202",
      "foundation-p203",
      "foundation-p204",
      "foundation-p205",
      "foundation-p206",
      "foundation-p207",
      "foundation-p208",
      "foundation-p209",
      "foundation-p210",
      "foundation-p211",
      "foundation-p212",
      "foundation-p213",
      "foundation-p214",
      "foundation-p215",
      "foundation-p216",
      "foundation-p217",
      "foundation-p218",
      "foundation-p219",
      "foundation-p220",
      "foundation-p221",
      "foundation-p222",
      "foundation-p223",
      "foundation-p224",
      "foundation-p225",
      "foundation-p226",
      "foundation-p227",
      "foundation-p228",
      "foundation-p229",
      "foundation-p230",
      "foundation-p231",
      "foundation-p232",
      "foundation-p233",
      "foundation-p234",
      "foundation-p235",
      "foundation-p236",
      "foundation-p237",
      "foundation-p238",
      "foundation-p239",
      "foundation-p240",
      "foundation-p241",
      "cell-0-shuttle-p242",
      "cell-0-shuttle-p243",
      "cell-0-shuttle-p244",
      "cell-0-shuttle-p245",
      "cell-0-shuttle-p246",
      "cell-0-shuttle-p247",
      "cell-0-shuttle-p248",
      "cell-0-shuttle-p249",
      "cell-0-shuttle-p250",
      "cell-0-shuttle-p251",
      "cell-0-shuttle-p252",
      "cell-0-shuttle-p253",
      "cell-0-shuttle-p254",
      "cell-0-shuttle-p255",
      "cell-0-shuttle-p256",
      "cell-0-shuttle-p257",
      "cell-0-shuttle-p258",
      "cell-0-shuttle-p259",
      "cell-0-shuttle-p260",
      "cell-0-shuttle-p261",
      "cell-0-shuttle-p262",
      "cell-0-shuttle-p263",
      "cell-0-shuttle-p264",
      "cell-0-shuttle-p265",
      "cell-0-shuttle-p266",
      "cell-0-shuttle-p267",
      "cell-0-shuttle-p268",
      "cell-0-shuttle-p269",
      "cell-0-shuttle-p270",
      "cell-0-shuttle-p271",
      "cell-0-shuttle-p272",
      "cell-0-shuttle-p273",
      "cell-0-shuttle-p274",
      "cell-0-shuttle-p275",
      "cell-0-shuttle-p276",
      "cell-0-shuttle-p277",
      "cell-0-shuttle-p278",
      "cell-0-shuttle-p279",
      "cell-0-shuttle-p280",
      "cell-0-shuttle-p281",
      "cell-0-shuttle-p282",
      "cell-0-shuttle-p283",
      "cell-0-shuttle-p284",
      "cell-0-shuttle-p285",
      "cell-0-shuttle-p286",
      "cell-0-shuttle-p287",
      "cell-0-shuttle-p288",
      "cell-0-shuttle-p289",
      "cell-0-mount-p290",
      "cell-0-mount-p291",
      "cell-0-mount-p292",
      "cell-0-mount-p293",
      "cell-0-mount-p294",
      "cell-0-mount-p295",
      "cell-0-mount-p296",
      "cell-0-mount-p297",
      "cell-0-mount-p298",
      "cell-0-mount-p299",
      "cell-0-mount-p300",
      "cell-0-mount-p301",
      "cell-0-mount-p302",
      "cell-0-mount-p303",
      "cell-0-mount-p304",
      "cell-0-mount-p305",
      "cell-0-mount-p306",
      "cell-0-mount-p307",
      "cell-0-mount-p308",
      "cell-0-mount-p309",
      "cell-0-mount-p310",
      "cell-0-mount-p311",
      "cell-0-mount-p312",
      "cell-0-mount-p313",
      "cell-0-mount-p314",
      "cell-0-mount-p315",
      "cell-0-mount-p316",
      "cell-0-mount-p317",
      "cell-0-mount-p318",
      "cell-0-mount-p319",
      "cell-0-mount-p320",
      "cell-0-mount-p321",
      "cell-0-mount-p322",
      "cell-0-mount-p323",
      "cell-0-mount-p324",
      "cell-0-shoulder-p325",
      "cell-0-elbow-p326",
      "cell-0-elbow-p327",
      "cell-0-elbow-p328",
      "cell-0-elbow-p329",
      "cell-0-wrist-p330",
      "cell-0-wrist-p331",
      "cell-0-wrist-p332",
      "cell-0-tool-p334",
      "cell-0-console-p335",
      "cell-0-console-p336",
      "cell-0-console-p337",
      "cell-0-console-p338",
      "cell-0-console-p339",
      "cell-0-console-p340",
      "cell-0-console-p341",
      "cell-0-console-p342",
      "cell-0-magazine-p343",
      "cell-0-magazine-p344",
      "cell-0-magazine-p345",
      "cell-0-magazine-p346",
      "cell-0-magazine-p347",
      "cell-0-magazine-p348",
      "cell-0-magazine-p349",
      "cell-0-magazine-p350",
      "cell-0-magazine-p351",
      "cell-0-magazine-p352",
      "cell-0-magazine-p353",
      "cell-0-magazine-p354",
      "cell-0-magazine-p355",
      "cell-0-magazine-p356",
      "cell-0-magazine-p357",
      "cell-0-magazine-p358",
      "cell-0-magazine-p359",
      "cell-0-magazine-p360",
      "cell-0-magazine-p361",
      "cell-0-magazine-p362",
      "cell-0-magazine-p363",
      "cell-0-magazine-p364",
      "cell-0-magazine-p365",
      "cell-0-magazine-p366",
      "cell-0-magazine-p367",
      "cell-0-magazine-p368",
      "cell-0-magazine-p369",
      "cell-0-magazine-p370",
      "cell-0-magazine-p371",
      "cell-0-magazine-p372",
      "cell-0-magazine-p373",
      "cell-0-magazine-p374",
      "cell-0-magazine-p375",
      "cell-0-magazine-p376",
      "cell-0-magazine-p377",
      "cell-0-magazine-p378",
      "cell-0-magazine-p379",
      "cell-0-magazine-p380",
      "cell-0-magazine-p381",
      "cell-0-magazine-p382",
      "cell-0-magazine-p383",
      "cell-0-magazine-p384",
      "cell-0-magazine-p385",
      "cell-0-magazine-p386",
      "cell-0-magazine-p387",
      "cell-0-magazine-p388",
      "cell-0-magazine-p389",
      "cell-0-magazine-p390",
      "cell-0-magazine-p391",
      "cell-0-magazine-p392",
      "cell-0-magazine-p393",
      "cell-0-magazine-p394",
      "cell-0-magazine-p395",
      "cell-0-magazine-p396",
      "cell-0-magazine-p397",
      "cell-0-magazine-p398",
      "cell-0-magazine-p399",
      "cell-0-magazine-p400",
      "cell-0-drawer-p401",
      "cell-0-drawer-p402",
      "cell-0-drawer-p403",
      "cell-0-drawer-p404",
      "cell-0-drawer-p405",
      "cell-0-drawer-p406",
      "cell-1-shuttle-p407",
      "cell-1-shuttle-p408",
      "cell-1-shuttle-p409",
      "cell-1-shuttle-p410",
      "cell-1-shuttle-p411",
      "cell-1-shuttle-p412",
      "cell-1-shuttle-p413",
      "cell-1-shuttle-p414",
      "cell-1-shuttle-p415",
      "cell-1-shuttle-p416",
      "cell-1-shuttle-p417",
      "cell-1-shuttle-p418",
      "cell-1-shuttle-p419",
      "cell-1-shuttle-p420",
      "cell-1-shuttle-p421",
      "cell-1-shuttle-p422",
      "cell-1-shuttle-p423",
      "cell-1-shuttle-p424",
      "cell-1-shuttle-p425",
      "cell-1-shuttle-p426",
      "cell-1-shuttle-p427",
      "cell-1-shuttle-p428",
      "cell-1-shuttle-p429",
      "cell-1-shuttle-p430",
      "cell-1-shuttle-p431",
      "cell-1-shuttle-p432",
      "cell-1-shuttle-p433",
      "cell-1-shuttle-p434",
      "cell-1-shuttle-p435",
      "cell-1-shuttle-p436",
      "cell-1-shuttle-p437",
      "cell-1-shuttle-p438",
      "cell-1-shuttle-p439",
      "cell-1-shuttle-p440",
      "cell-1-shuttle-p441",
      "cell-1-shuttle-p442",
      "cell-1-shuttle-p443",
      "cell-1-shuttle-p444",
      "cell-1-shuttle-p445",
      "cell-1-shuttle-p446",
      "cell-1-shuttle-p447",
      "cell-1-shuttle-p448",
      "cell-1-shuttle-p449",
      "cell-1-shuttle-p450",
      "cell-1-shuttle-p451",
      "cell-1-shuttle-p452",
      "cell-1-shuttle-p453",
      "cell-1-shuttle-p454",
      "cell-1-mount-p455",
      "cell-1-mount-p456",
      "cell-1-mount-p457",
      "cell-1-mount-p458",
      "cell-1-mount-p459",
      "cell-1-mount-p460",
      "cell-1-mount-p461",
      "cell-1-mount-p462",
      "cell-1-mount-p463",
      "cell-1-mount-p464",
      "cell-1-mount-p465",
      "cell-1-mount-p466",
      "cell-1-mount-p467",
      "cell-1-mount-p468",
      "cell-1-mount-p469",
      "cell-1-mount-p470",
      "cell-1-mount-p471",
      "cell-1-mount-p472",
      "cell-1-mount-p473",
      "cell-1-mount-p474",
      "cell-1-mount-p475",
      "cell-1-mount-p476",
      "cell-1-mount-p477",
      "cell-1-mount-p478",
      "cell-1-mount-p479",
      "cell-1-mount-p480",
      "cell-1-mount-p481",
      "cell-1-mount-p482",
      "cell-1-mount-p483",
      "cell-1-mount-p484",
      "cell-1-yoke-p485",
      "cell-1-yoke-p486",
      "cell-1-yoke-p487",
      "cell-1-yoke-p488",
      "cell-1-yoke-p489",
      "cell-1-yoke-p490",
      "cell-1-yoke-p491",
      "cell-1-yoke-p492",
      "cell-1-yoke-p493",
      "cell-1-yoke-p494",
      "cell-1-yoke-p495",
      "cell-1-cradle-p496",
      "cell-1-optic-p497",
      "cell-1-optic-p498",
      "cell-1-console-p499",
      "cell-1-console-p500",
      "cell-1-console-p501",
      "cell-1-console-p502",
      "cell-1-console-p503",
      "cell-1-console-p504",
      "cell-1-console-p505",
      "cell-1-console-p506",
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
      "cell-1-magazine-p526",
      "cell-1-magazine-p527",
      "cell-1-magazine-p528",
      "cell-1-magazine-p529",
      "cell-1-magazine-p530",
      "cell-1-magazine-p531",
      "cell-1-magazine-p532",
      "cell-1-magazine-p533",
      "cell-1-magazine-p534",
      "cell-1-magazine-p535",
      "cell-1-magazine-p536",
      "cell-1-magazine-p537",
      "cell-1-magazine-p538",
      "cell-1-magazine-p539",
      "cell-1-magazine-p540",
      "cell-1-magazine-p541",
      "cell-1-magazine-p542",
      "cell-1-magazine-p543",
      "cell-1-magazine-p544",
      "cell-1-magazine-p545",
      "cell-1-magazine-p546",
      "cell-1-magazine-p547",
      "cell-1-magazine-p548",
      "cell-1-magazine-p549",
      "cell-1-magazine-p550",
      "cell-1-magazine-p551",
      "cell-1-magazine-p552",
      "cell-1-magazine-p553",
      "cell-1-magazine-p554",
      "cell-1-magazine-p555",
      "cell-1-magazine-p556",
      "cell-1-magazine-p557",
      "cell-1-magazine-p558",
      "cell-1-magazine-p559",
      "cell-1-magazine-p560",
      "cell-1-magazine-p561",
      "cell-1-magazine-p562",
      "cell-1-magazine-p563",
      "cell-1-magazine-p564",
      "cell-1-drawer-p565",
      "cell-1-drawer-p566",
      "cell-1-drawer-p567",
      "cell-1-drawer-p568",
      "cell-1-drawer-p569",
      "cell-1-drawer-p570",
      "cell-2-shuttle-p571",
      "cell-2-shuttle-p572",
      "cell-2-shuttle-p573",
      "cell-2-shuttle-p574",
      "cell-2-shuttle-p575",
      "cell-2-shuttle-p576",
      "cell-2-shuttle-p577",
      "cell-2-shuttle-p578",
      "cell-2-shuttle-p579",
      "cell-2-shuttle-p580",
      "cell-2-shuttle-p581",
      "cell-2-shuttle-p582",
      "cell-2-shuttle-p583",
      "cell-2-shuttle-p584",
      "cell-2-shuttle-p585",
      "cell-2-shuttle-p586",
      "cell-2-shuttle-p587",
      "cell-2-shuttle-p588",
      "cell-2-shuttle-p589",
      "cell-2-shuttle-p590",
      "cell-2-shuttle-p591",
      "cell-2-shuttle-p592",
      "cell-2-shuttle-p593",
      "cell-2-shuttle-p594",
      "cell-2-shuttle-p595",
      "cell-2-shuttle-p596",
      "cell-2-shuttle-p597",
      "cell-2-shuttle-p598",
      "cell-2-shuttle-p599",
      "cell-2-shuttle-p600",
      "cell-2-shuttle-p601",
      "cell-2-shuttle-p602",
      "cell-2-shuttle-p603",
      "cell-2-shuttle-p604",
      "cell-2-shuttle-p605",
      "cell-2-shuttle-p606",
      "cell-2-shuttle-p607",
      "cell-2-shuttle-p608",
      "cell-2-shuttle-p609",
      "cell-2-shuttle-p610",
      "cell-2-shuttle-p611",
      "cell-2-shuttle-p612",
      "cell-2-shuttle-p613",
      "cell-2-shuttle-p614",
      "cell-2-shuttle-p615",
      "cell-2-shuttle-p616",
      "cell-2-shuttle-p617",
      "cell-2-shuttle-p618",
      "cell-2-mount-p619",
      "cell-2-mount-p620",
      "cell-2-mount-p621",
      "cell-2-mount-p622",
      "cell-2-mount-p623",
      "cell-2-mount-p624",
      "cell-2-mount-p625",
      "cell-2-mount-p626",
      "cell-2-mount-p627",
      "cell-2-mount-p628",
      "cell-2-mount-p629",
      "cell-2-mount-p630",
      "cell-2-mount-p631",
      "cell-2-mount-p632",
      "cell-2-mount-p633",
      "cell-2-mount-p634",
      "cell-2-mount-p635",
      "cell-2-mount-p636",
      "cell-2-mount-p637",
      "cell-2-mount-p638",
      "cell-2-mount-p639",
      "cell-2-mount-p640",
      "cell-2-mount-p641",
      "cell-2-mount-p642",
      "cell-2-mount-p643",
      "cell-2-mount-p644",
      "cell-2-mount-p645",
      "cell-2-mount-p646",
      "cell-2-mount-p647",
      "cell-2-mount-p648",
      "cell-2-mount-p649",
      "cell-2-mount-p650",
      "cell-2-mount-p651",
      "cell-2-mount-p652",
      "cell-2-mount-p653",
      "cell-2-hub-p654",
      "cell-2-wing-0-p655",
      "cell-2-wing-0-p656",
      "cell-2-wing-0-p657",
      "cell-2-wing-0-p658",
      "cell-2-wing-0-p659",
      "cell-2-wing-0-p660",
      "cell-2-wing-0-p661",
      "cell-2-wing-0-p662",
      "cell-2-wing-1-p663",
      "cell-2-wing-1-p664",
      "cell-2-wing-1-p665",
      "cell-2-wing-1-p666",
      "cell-2-wing-1-p667",
      "cell-2-wing-1-p668",
      "cell-2-wing-1-p669",
      "cell-2-wing-1-p670",
      "cell-2-wing-2-p671",
      "cell-2-wing-2-p672",
      "cell-2-wing-2-p673",
      "cell-2-wing-2-p674",
      "cell-2-wing-2-p675",
      "cell-2-wing-2-p676",
      "cell-2-wing-2-p677",
      "cell-2-wing-2-p678",
      "cell-2-wing-3-p679",
      "cell-2-wing-3-p680",
      "cell-2-wing-3-p681",
      "cell-2-wing-3-p682",
      "cell-2-wing-3-p683",
      "cell-2-wing-3-p684",
      "cell-2-wing-3-p685",
      "cell-2-wing-3-p686",
      "cell-2-console-p687",
      "cell-2-console-p688",
      "cell-2-console-p689",
      "cell-2-console-p690",
      "cell-2-console-p691",
      "cell-2-console-p692",
      "cell-2-console-p693",
      "cell-2-console-p694",
      "cell-2-magazine-p695",
      "cell-2-magazine-p696",
      "cell-2-magazine-p697",
      "cell-2-magazine-p698",
      "cell-2-magazine-p699",
      "cell-2-magazine-p700",
      "cell-2-magazine-p701",
      "cell-2-magazine-p702",
      "cell-2-magazine-p703",
      "cell-2-magazine-p704",
      "cell-2-magazine-p705",
      "cell-2-magazine-p706",
      "cell-2-magazine-p707",
      "cell-2-magazine-p708",
      "cell-2-magazine-p709",
      "cell-2-magazine-p710",
      "cell-2-magazine-p711",
      "cell-2-magazine-p712",
      "cell-2-magazine-p713",
      "cell-2-magazine-p714",
      "cell-2-magazine-p715",
      "cell-2-magazine-p716",
      "cell-2-magazine-p717",
      "cell-2-magazine-p718",
      "cell-2-magazine-p719",
      "cell-2-magazine-p720",
      "cell-2-magazine-p721",
      "cell-2-magazine-p722",
      "cell-2-magazine-p723",
      "cell-2-magazine-p724",
      "cell-2-magazine-p725",
      "cell-2-magazine-p726",
      "cell-2-magazine-p727",
      "cell-2-magazine-p728",
      "cell-2-magazine-p729",
      "cell-2-magazine-p730",
      "cell-2-magazine-p731",
      "cell-2-magazine-p732",
      "cell-2-magazine-p733",
      "cell-2-magazine-p734",
      "cell-2-magazine-p735",
      "cell-2-magazine-p736",
      "cell-2-magazine-p737",
      "cell-2-magazine-p738",
      "cell-2-magazine-p739",
      "cell-2-magazine-p740",
      "cell-2-magazine-p741",
      "cell-2-magazine-p742",
      "cell-2-magazine-p743",
      "cell-2-magazine-p744",
      "cell-2-magazine-p745",
      "cell-2-magazine-p746",
      "cell-2-magazine-p747",
      "cell-2-magazine-p748",
      "cell-2-magazine-p749",
      "cell-2-magazine-p750",
      "cell-2-magazine-p751",
      "cell-2-magazine-p752",
      "cell-2-drawer-p753",
      "cell-2-drawer-p754",
      "cell-2-drawer-p755",
      "cell-2-drawer-p756",
      "cell-2-drawer-p757",
      "cell-2-drawer-p758",
      "cell-3-shuttle-p759",
      "cell-3-shuttle-p760",
      "cell-3-shuttle-p761",
      "cell-3-shuttle-p762",
      "cell-3-shuttle-p763",
      "cell-3-shuttle-p764",
      "cell-3-shuttle-p765",
      "cell-3-shuttle-p766",
      "cell-3-shuttle-p767",
      "cell-3-shuttle-p768",
      "cell-3-shuttle-p769",
      "cell-3-shuttle-p770",
      "cell-3-shuttle-p771",
      "cell-3-shuttle-p772",
      "cell-3-shuttle-p773",
      "cell-3-shuttle-p774",
      "cell-3-shuttle-p775",
      "cell-3-shuttle-p776",
      "cell-3-shuttle-p777",
      "cell-3-shuttle-p778",
      "cell-3-shuttle-p779",
      "cell-3-shuttle-p780",
      "cell-3-shuttle-p781",
      "cell-3-shuttle-p782",
      "cell-3-shuttle-p783",
      "cell-3-shuttle-p784",
      "cell-3-shuttle-p785",
      "cell-3-shuttle-p786",
      "cell-3-shuttle-p787",
      "cell-3-shuttle-p788",
      "cell-3-shuttle-p789",
      "cell-3-shuttle-p790",
      "cell-3-shuttle-p791",
      "cell-3-shuttle-p792",
      "cell-3-shuttle-p793",
      "cell-3-shuttle-p794",
      "cell-3-shuttle-p795",
      "cell-3-shuttle-p796",
      "cell-3-shuttle-p797",
      "cell-3-shuttle-p798",
      "cell-3-shuttle-p799",
      "cell-3-shuttle-p800",
      "cell-3-shuttle-p801",
      "cell-3-shuttle-p802",
      "cell-3-shuttle-p803",
      "cell-3-shuttle-p804",
      "cell-3-shuttle-p805",
      "cell-3-shuttle-p806",
      "cell-3-mount-p807",
      "cell-3-mount-p808",
      "cell-3-mount-p809",
      "cell-3-mount-p810",
      "cell-3-mount-p811",
      "cell-3-mount-p812",
      "cell-3-mount-p813",
      "cell-3-mount-p814",
      "cell-3-mount-p815",
      "cell-3-mount-p816",
      "cell-3-mount-p817",
      "cell-3-mount-p818",
      "cell-3-mount-p819",
      "cell-3-mount-p820",
      "cell-3-mount-p821",
      "cell-3-mount-p822",
      "cell-3-mount-p823",
      "cell-3-mount-p824",
      "cell-3-mount-p825",
      "cell-3-mount-p826",
      "cell-3-mount-p827",
      "cell-3-mount-p828",
      "cell-3-mount-p829",
      "cell-3-mount-p830",
      "cell-3-mount-p831",
      "cell-3-mount-p832",
      "cell-3-mount-p833",
      "cell-3-mount-p834",
      "cell-3-mount-p835",
      "cell-3-mount-p836",
      "cell-3-hub-p837",
      "cell-3-probe-0-p838",
      "cell-3-probe-0-p839",
      "cell-3-probe-0-p840",
      "cell-3-probe-0-p841",
      "cell-3-console-p842",
      "cell-3-console-p843",
      "cell-3-console-p844",
      "cell-3-console-p845",
      "cell-3-console-p846",
      "cell-3-console-p847",
      "cell-3-console-p848",
      "cell-3-console-p849",
      "cell-3-magazine-p850",
      "cell-3-magazine-p851",
      "cell-3-magazine-p852",
      "cell-3-magazine-p853",
      "cell-3-magazine-p854",
      "cell-3-magazine-p855",
      "cell-3-magazine-p856",
      "cell-3-magazine-p857",
      "cell-3-magazine-p858",
      "cell-3-magazine-p859",
      "cell-3-magazine-p860",
      "cell-3-magazine-p861",
      "cell-3-magazine-p862",
      "cell-3-magazine-p863",
      "cell-3-magazine-p864",
      "cell-3-magazine-p865",
      "cell-3-magazine-p866",
      "cell-3-magazine-p867",
      "cell-3-magazine-p868",
      "cell-3-magazine-p869",
      "cell-3-magazine-p870",
      "cell-3-magazine-p871",
      "cell-3-magazine-p872",
      "cell-3-magazine-p873",
      "cell-3-magazine-p874",
      "cell-3-magazine-p875",
      "cell-3-magazine-p876",
      "cell-3-magazine-p877",
      "cell-3-magazine-p878",
      "cell-3-magazine-p879",
      "cell-3-magazine-p880",
      "cell-3-magazine-p881",
      "cell-3-magazine-p882",
      "cell-3-magazine-p883",
      "cell-3-magazine-p884",
      "cell-3-magazine-p885",
      "cell-3-magazine-p886",
      "cell-3-magazine-p887",
      "cell-3-magazine-p888",
      "cell-3-magazine-p889",
      "cell-3-magazine-p890",
      "cell-3-magazine-p891",
      "cell-3-magazine-p892",
      "cell-3-magazine-p893",
      "cell-3-magazine-p894",
      "cell-3-magazine-p895",
      "cell-3-magazine-p896",
      "cell-3-magazine-p897",
      "cell-3-magazine-p898",
      "cell-3-magazine-p899",
      "cell-3-magazine-p900",
      "cell-3-magazine-p901",
      "cell-3-magazine-p902",
      "cell-3-magazine-p903",
      "cell-3-magazine-p904",
      "cell-3-magazine-p905",
      "cell-3-magazine-p906",
      "cell-3-magazine-p907",
      "cell-3-drawer-p908",
      "cell-3-drawer-p909",
      "cell-3-drawer-p910",
      "cell-3-drawer-p911",
      "cell-3-drawer-p912",
      "cell-3-drawer-p913",
      "shared-inspection-mast-p914",
      "shared-inspection-mast-p915",
      "shared-inspection-mast-p916",
      "shared-inspection-mast-p917",
      "shared-inspection-mast-p918",
      "shared-inspection-mast-p919",
      "shared-inspection-mast-p920",
      "shared-inspection-mast-p921",
      "shared-inspection-mast-p922",
      "shared-inspection-mast-p923",
      "shared-inspection-mast-p924",
      "shared-inspection-mast-p925",
      "shared-inspection-mast-p926",
      "shared-scanner-p927",
      "shared-scanner-p928"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全拆除（h3-exp-d4-arm-2-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["foundation"]
- B：[]
- C：["foundation","cell-0-shuttle","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-yoke","cell-1-cradle","cell-1-optic","cell-1-console","cell-1-magazine","cell-1-drawer","cell-2-shuttle","cell-2-mount","cell-2-hub","cell-2-wing-0","cell-2-wing-1","cell-2-wing-2","cell-2-wing-3","cell-2-console","cell-2-magazine","cell-2-drawer","cell-3-shuttle","cell-3-mount","cell-3-hub","cell-3-probe-0","cell-3-console","cell-3-magazine","cell-3-drawer","shared-inspection-mast","shared-scanner"]
- D：["cell-0-console","cell-0-drawer","cell-0-tool","cell-1-console","cell-1-drawer","cell-1-optic","cell-2-console","cell-2-drawer","cell-2-wing-0","cell-2-wing-1","cell-2-wing-2","cell-2-wing-3","cell-3-console","cell-3-drawer","cell-3-probe-0","shared-scanner"]

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
          -19.5,
          0.4999999999999999,
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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.6999999999999993,
          0.6499999999999999,
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
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000004,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.4499999999999993,
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
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.4500000000000002,
          0.7
        ],
        "anchorChild": [
          -1.3499999999999979,
          0.34999999999999964,
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
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.4500000000000028,
          -0.40000000000000036,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -19.5,
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
          -19.5,
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
          -6.5,
          0.4999999999999999,
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
        "id": "cell-1-yoke-joint",
        "name": "cell-1-yoke interface",
        "parent": "cell-1-mount",
        "child": "cell-1-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          -8.881784197001252e-16,
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
        "id": "cell-1-cradle-joint",
        "name": "cell-1-cradle interface",
        "parent": "cell-1-yoke",
        "child": "cell-1-cradle",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
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
        "id": "cell-1-optic-joint",
        "name": "cell-1-optic interface",
        "parent": "cell-1-cradle",
        "child": "cell-1-optic",
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          -6.5,
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
          -6.5,
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
          6.5,
          0.4999999999999999,
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
        "id": "cell-2-wing-0-joint",
        "name": "cell-2-wing-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-0",
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
        "id": "cell-2-wing-1-joint",
        "name": "cell-2-wing-1 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-wing-2-joint",
        "name": "cell-2-wing-2 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-2",
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
        "id": "cell-2-wing-3-joint",
        "name": "cell-2-wing-3 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-3",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          6.5,
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
          6.5,
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
        "id": "cell-3-shuttle-joint",
        "name": "cell-3-shuttle interface",
        "parent": "foundation",
        "child": "cell-3-shuttle",
        "type": "prismatic",
        "anchorParent": [
          19.5,
          0.4999999999999999,
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
        "id": "cell-3-mount-joint",
        "name": "cell-3-mount interface",
        "parent": "cell-3-shuttle",
        "child": "cell-3-mount",
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
        "id": "cell-3-hub-joint",
        "name": "cell-3-hub interface",
        "parent": "cell-3-mount",
        "child": "cell-3-hub",
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
        "id": "cell-3-probe-0-joint",
        "name": "cell-3-probe-0 interface",
        "parent": "cell-3-hub",
        "child": "cell-3-probe-0",
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
        "id": "cell-3-console-joint",
        "name": "cell-3-console interface",
        "parent": "foundation",
        "child": "cell-3-console",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-magazine-joint",
        "name": "cell-3-magazine interface",
        "parent": "foundation",
        "child": "cell-3-magazine",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-drawer-joint",
        "name": "cell-3-drawer interface",
        "parent": "cell-3-magazine",
        "child": "cell-3-drawer",
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
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-yoke",
      "cell-1-cradle",
      "cell-1-optic",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-wing-0",
      "cell-2-wing-1",
      "cell-2-wing-2",
      "cell-2-wing-3",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "cell-3-shuttle",
      "cell-3-mount",
      "cell-3-hub",
      "cell-3-probe-0",
      "cell-3-console",
      "cell-3-magazine",
      "cell-3-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 替换选择（h3-exp-d4-arm-2-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-0
- B：stock-1
- C：stock-2
- D：stock-3

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 9,
        "mass": 0.6
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 11,
        "mass": 0.7
      },
      {
        "id": "stock-2",
        "cost": 6,
        "stiffness": 8,
        "mass": 1.3
      },
      {
        "id": "stock-3",
        "cost": 3,
        "stiffness": 11,
        "mass": 1.3
      }
    ],
    "maxCost": 8
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-exp-d4-arm-2-translate）

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
    "target": "cell-0-tool"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-exp-d4-arm-2-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：-90
- B：0
- C：-180
- D：90

```json
{
  "input": {
    "module": "cell-0-tool",
    "currentYaw": 180,
    "targetYaw": 270
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 下一步放置（h3-exp-d4-arm-2-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","cell-0-shuttle","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-yoke","cell-1-cradle","cell-1-optic","cell-1-console","cell-1-magazine","cell-1-drawer","cell-2-shuttle"]
- C：["cell-2-mount","cell-2-hub","cell-2-wing-0","cell-2-wing-1","cell-2-wing-2","cell-2-wing-3","cell-2-console","cell-2-magazine","cell-2-drawer","cell-3-shuttle","cell-3-mount","cell-3-hub","cell-3-probe-0","cell-3-console","cell-3-magazine","cell-3-drawer","shared-inspection-mast","shared-scanner"]
- D：["cell-2-console","cell-2-magazine","cell-2-mount","cell-3-console","cell-3-magazine","cell-3-shuttle","shared-inspection-mast"]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-yoke",
      "cell-1-cradle",
      "cell-1-optic",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle"
    ],
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          -19.5,
          0.4999999999999999,
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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.6999999999999993,
          0.6499999999999999,
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
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000004,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.4499999999999993,
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
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.4500000000000002,
          0.7
        ],
        "anchorChild": [
          -1.3499999999999979,
          0.34999999999999964,
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
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.4500000000000028,
          -0.40000000000000036,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -19.5,
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
          -19.5,
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
          -6.5,
          0.4999999999999999,
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
        "id": "cell-1-yoke-joint",
        "name": "cell-1-yoke interface",
        "parent": "cell-1-mount",
        "child": "cell-1-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          -8.881784197001252e-16,
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
        "id": "cell-1-cradle-joint",
        "name": "cell-1-cradle interface",
        "parent": "cell-1-yoke",
        "child": "cell-1-cradle",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
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
        "id": "cell-1-optic-joint",
        "name": "cell-1-optic interface",
        "parent": "cell-1-cradle",
        "child": "cell-1-optic",
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          -6.5,
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
          -6.5,
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
          6.5,
          0.4999999999999999,
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
        "id": "cell-2-wing-0-joint",
        "name": "cell-2-wing-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-0",
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
        "id": "cell-2-wing-1-joint",
        "name": "cell-2-wing-1 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-wing-2-joint",
        "name": "cell-2-wing-2 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-2",
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
        "id": "cell-2-wing-3-joint",
        "name": "cell-2-wing-3 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-3",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          6.5,
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
          6.5,
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
        "id": "cell-3-shuttle-joint",
        "name": "cell-3-shuttle interface",
        "parent": "foundation",
        "child": "cell-3-shuttle",
        "type": "prismatic",
        "anchorParent": [
          19.5,
          0.4999999999999999,
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
        "id": "cell-3-mount-joint",
        "name": "cell-3-mount interface",
        "parent": "cell-3-shuttle",
        "child": "cell-3-mount",
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
        "id": "cell-3-hub-joint",
        "name": "cell-3-hub interface",
        "parent": "cell-3-mount",
        "child": "cell-3-hub",
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
        "id": "cell-3-probe-0-joint",
        "name": "cell-3-probe-0 interface",
        "parent": "cell-3-hub",
        "child": "cell-3-probe-0",
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
        "id": "cell-3-console-joint",
        "name": "cell-3-console interface",
        "parent": "foundation",
        "child": "cell-3-console",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-magazine-joint",
        "name": "cell-3-magazine interface",
        "parent": "foundation",
        "child": "cell-3-magazine",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-drawer-joint",
        "name": "cell-3-drawer interface",
        "parent": "cell-3-magazine",
        "child": "cell-3-drawer",
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
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-yoke",
      "cell-1-cradle",
      "cell-1-optic",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-wing-0",
      "cell-2-wing-1",
      "cell-2-wing-2",
      "cell-2-wing-3",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "cell-3-shuttle",
      "cell-3-mount",
      "cell-3-hub",
      "cell-3-probe-0",
      "cell-3-console",
      "cell-3-magazine",
      "cell-3-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 库存核算（h3-exp-d4-arm-2-inventory）

备件库有 10 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：8
- B：9
- C：7
- D：11

```json
{
  "input": {
    "available": 10,
    "required": 2
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 子装配边界（h3-exp-d4-arm-2-boundary）

隔离 cell-0-tool 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["cell-0-elbow-joint"]
- B：["cell-0-tool-joint"]
- C：[]
- D：["cell-0-shuttle-joint","cell-0-mount-joint","cell-0-shoulder-joint","cell-0-elbow-joint","cell-0-wrist-joint","cell-0-tool-joint","cell-0-console-joint","cell-0-magazine-joint","cell-0-drawer-joint","cell-1-shuttle-joint","cell-1-mount-joint","cell-1-yoke-joint","cell-1-cradle-joint","cell-1-optic-joint","cell-1-console-joint","cell-1-magazine-joint","cell-1-drawer-joint","cell-2-shuttle-joint","cell-2-mount-joint","cell-2-hub-joint","cell-2-wing-0-joint","cell-2-wing-1-joint","cell-2-wing-2-joint","cell-2-wing-3-joint","cell-2-console-joint","cell-2-magazine-joint","cell-2-drawer-joint","cell-3-shuttle-joint","cell-3-mount-joint","cell-3-hub-joint","cell-3-probe-0-joint","cell-3-console-joint","cell-3-magazine-joint","cell-3-drawer-joint","shared-inspection-mast-joint","shared-scanner-joint"]

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
          -19.5,
          0.4999999999999999,
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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.6999999999999993,
          0.6499999999999999,
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
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000004,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.4499999999999993,
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
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.4500000000000002,
          0.7
        ],
        "anchorChild": [
          -1.3499999999999979,
          0.34999999999999964,
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
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.4500000000000028,
          -0.40000000000000036,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -19.5,
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
          -19.5,
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
          -6.5,
          0.4999999999999999,
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
        "id": "cell-1-yoke-joint",
        "name": "cell-1-yoke interface",
        "parent": "cell-1-mount",
        "child": "cell-1-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          -8.881784197001252e-16,
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
        "id": "cell-1-cradle-joint",
        "name": "cell-1-cradle interface",
        "parent": "cell-1-yoke",
        "child": "cell-1-cradle",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
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
        "id": "cell-1-optic-joint",
        "name": "cell-1-optic interface",
        "parent": "cell-1-cradle",
        "child": "cell-1-optic",
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          -6.5,
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
          -6.5,
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
          6.5,
          0.4999999999999999,
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
        "id": "cell-2-wing-0-joint",
        "name": "cell-2-wing-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-0",
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
        "id": "cell-2-wing-1-joint",
        "name": "cell-2-wing-1 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-wing-2-joint",
        "name": "cell-2-wing-2 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-2",
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
        "id": "cell-2-wing-3-joint",
        "name": "cell-2-wing-3 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-3",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          6.5,
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
          6.5,
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
        "id": "cell-3-shuttle-joint",
        "name": "cell-3-shuttle interface",
        "parent": "foundation",
        "child": "cell-3-shuttle",
        "type": "prismatic",
        "anchorParent": [
          19.5,
          0.4999999999999999,
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
        "id": "cell-3-mount-joint",
        "name": "cell-3-mount interface",
        "parent": "cell-3-shuttle",
        "child": "cell-3-mount",
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
        "id": "cell-3-hub-joint",
        "name": "cell-3-hub interface",
        "parent": "cell-3-mount",
        "child": "cell-3-hub",
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
        "id": "cell-3-probe-0-joint",
        "name": "cell-3-probe-0 interface",
        "parent": "cell-3-hub",
        "child": "cell-3-probe-0",
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
        "id": "cell-3-console-joint",
        "name": "cell-3-console interface",
        "parent": "foundation",
        "child": "cell-3-console",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-magazine-joint",
        "name": "cell-3-magazine interface",
        "parent": "foundation",
        "child": "cell-3-magazine",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-drawer-joint",
        "name": "cell-3-drawer interface",
        "parent": "cell-3-magazine",
        "child": "cell-3-drawer",
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
    "target": "cell-0-tool"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 最小干预（h3-exp-d4-arm-2-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：0

```json
{
  "input": {
    "module": "cell-0-tool"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 全过程依赖（h3-exp-d4-arm-2-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：9
- B：36
- C：8
- D：-1

```json
{
  "input": {
    "order": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-drawer",
      "cell-0-magazine",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-yoke",
      "cell-1-cradle",
      "cell-1-optic",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-wing-0",
      "cell-2-wing-1",
      "cell-2-wing-2",
      "cell-2-wing-3",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "cell-3-shuttle",
      "cell-3-mount",
      "cell-3-hub",
      "cell-3-probe-0",
      "cell-3-console",
      "cell-3-magazine",
      "cell-3-drawer",
      "shared-inspection-mast",
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
          -19.5,
          0.4999999999999999,
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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.6999999999999993,
          0.6499999999999999,
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
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000004,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.4499999999999993,
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
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.4500000000000002,
          0.7
        ],
        "anchorChild": [
          -1.3499999999999979,
          0.34999999999999964,
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
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.4500000000000028,
          -0.40000000000000036,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -19.5,
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
          -19.5,
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
          -6.5,
          0.4999999999999999,
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
        "id": "cell-1-yoke-joint",
        "name": "cell-1-yoke interface",
        "parent": "cell-1-mount",
        "child": "cell-1-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          -8.881784197001252e-16,
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
        "id": "cell-1-cradle-joint",
        "name": "cell-1-cradle interface",
        "parent": "cell-1-yoke",
        "child": "cell-1-cradle",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
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
        "id": "cell-1-optic-joint",
        "name": "cell-1-optic interface",
        "parent": "cell-1-cradle",
        "child": "cell-1-optic",
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          -6.5,
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
          -6.5,
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
          6.5,
          0.4999999999999999,
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
        "id": "cell-2-wing-0-joint",
        "name": "cell-2-wing-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-0",
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
        "id": "cell-2-wing-1-joint",
        "name": "cell-2-wing-1 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-wing-2-joint",
        "name": "cell-2-wing-2 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-2",
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
        "id": "cell-2-wing-3-joint",
        "name": "cell-2-wing-3 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-3",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          6.5,
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
          6.5,
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
        "id": "cell-3-shuttle-joint",
        "name": "cell-3-shuttle interface",
        "parent": "foundation",
        "child": "cell-3-shuttle",
        "type": "prismatic",
        "anchorParent": [
          19.5,
          0.4999999999999999,
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
        "id": "cell-3-mount-joint",
        "name": "cell-3-mount interface",
        "parent": "cell-3-shuttle",
        "child": "cell-3-mount",
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
        "id": "cell-3-hub-joint",
        "name": "cell-3-hub interface",
        "parent": "cell-3-mount",
        "child": "cell-3-hub",
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
        "id": "cell-3-probe-0-joint",
        "name": "cell-3-probe-0 interface",
        "parent": "cell-3-hub",
        "child": "cell-3-probe-0",
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
        "id": "cell-3-console-joint",
        "name": "cell-3-console interface",
        "parent": "foundation",
        "child": "cell-3-console",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-magazine-joint",
        "name": "cell-3-magazine interface",
        "parent": "foundation",
        "child": "cell-3-magazine",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-drawer-joint",
        "name": "cell-3-drawer interface",
        "parent": "cell-3-magazine",
        "child": "cell-3-drawer",
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
    "choiceId": "C"
  }
}
```

### 连续维修路径（h3-exp-d4-arm-2-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-1
- B：path-2
- C：path-0

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          27.48,
          4.5375,
          1.3
        ],
        "end": [
          -16.9,
          4.5375,
          1.3
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.3902658224105835
      },
      {
        "id": "path-1",
        "start": [
          -16.9,
          11.524999999999999,
          1.3
        ],
        "end": [
          -16.9,
          4.5375,
          1.3
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
          -16.9,
          4.5375,
          15.65
        ],
        "end": [
          -16.9,
          4.5375,
          1.3
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
      "A",
      "B"
    ]
  }
}
```

### 支撑反事实（h3-exp-d4-arm-2-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["foundation","cell-0-shuttle","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-yoke","cell-1-cradle","cell-1-optic","cell-1-console","cell-1-magazine","cell-1-drawer","cell-2-shuttle","cell-2-mount","cell-2-hub","cell-2-wing-0","cell-2-wing-1","cell-2-wing-2","cell-2-wing-3","cell-2-console","cell-2-magazine","cell-2-drawer","cell-3-shuttle","cell-3-mount","cell-3-hub","cell-3-probe-0","cell-3-console","cell-3-magazine","cell-3-drawer","shared-inspection-mast","shared-scanner"]
- C：["cell-0-elbow","cell-0-mount","cell-0-shoulder","cell-0-tool","cell-0-wrist"]
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
          -19.5,
          0.4999999999999999,
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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.6999999999999993,
          0.6499999999999999,
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
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000004,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.4499999999999993,
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
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.4500000000000002,
          0.7
        ],
        "anchorChild": [
          -1.3499999999999979,
          0.34999999999999964,
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
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.4500000000000028,
          -0.40000000000000036,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -19.5,
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
          -19.5,
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
          -6.5,
          0.4999999999999999,
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
        "id": "cell-1-yoke-joint",
        "name": "cell-1-yoke interface",
        "parent": "cell-1-mount",
        "child": "cell-1-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          -8.881784197001252e-16,
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
        "id": "cell-1-cradle-joint",
        "name": "cell-1-cradle interface",
        "parent": "cell-1-yoke",
        "child": "cell-1-cradle",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
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
        "id": "cell-1-optic-joint",
        "name": "cell-1-optic interface",
        "parent": "cell-1-cradle",
        "child": "cell-1-optic",
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          -6.5,
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
          -6.5,
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
          6.5,
          0.4999999999999999,
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
        "id": "cell-2-wing-0-joint",
        "name": "cell-2-wing-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-0",
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
        "id": "cell-2-wing-1-joint",
        "name": "cell-2-wing-1 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-wing-2-joint",
        "name": "cell-2-wing-2 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-2",
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
        "id": "cell-2-wing-3-joint",
        "name": "cell-2-wing-3 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-3",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          6.5,
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
          6.5,
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
        "id": "cell-3-shuttle-joint",
        "name": "cell-3-shuttle interface",
        "parent": "foundation",
        "child": "cell-3-shuttle",
        "type": "prismatic",
        "anchorParent": [
          19.5,
          0.4999999999999999,
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
        "id": "cell-3-mount-joint",
        "name": "cell-3-mount interface",
        "parent": "cell-3-shuttle",
        "child": "cell-3-mount",
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
        "id": "cell-3-hub-joint",
        "name": "cell-3-hub interface",
        "parent": "cell-3-mount",
        "child": "cell-3-hub",
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
        "id": "cell-3-probe-0-joint",
        "name": "cell-3-probe-0 interface",
        "parent": "cell-3-hub",
        "child": "cell-3-probe-0",
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
        "id": "cell-3-console-joint",
        "name": "cell-3-console interface",
        "parent": "foundation",
        "child": "cell-3-console",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-magazine-joint",
        "name": "cell-3-magazine interface",
        "parent": "foundation",
        "child": "cell-3-magazine",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-drawer-joint",
        "name": "cell-3-drawer interface",
        "parent": "cell-3-magazine",
        "child": "cell-3-drawer",
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
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-yoke",
      "cell-1-cradle",
      "cell-1-optic",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-wing-0",
      "cell-2-wing-1",
      "cell-2-wing-2",
      "cell-2-wing-3",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "cell-3-shuttle",
      "cell-3-mount",
      "cell-3-hub",
      "cell-3-probe-0",
      "cell-3-console",
      "cell-3-magazine",
      "cell-3-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-exp-d4-arm-2-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.0163
- B：0.2163
- C：0
- D：1.0163

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.016323870037975755
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.01538021355252516
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.012283465603825048
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.005088173205986325
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0007392597020711207
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00033787069412119253
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0005408243661113503
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00007812456984420164
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.000014720295944626933
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.000014720295944626933
      },
      {
        "time": 1,
        "displacement": 0.000014720295944626933
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.014892708059218248,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节限位推理（h3-exp-d4-arm-2-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-1.1
- B：1.1
- C：-0.6
- D：0

```json
{
  "input": {
    "joint": "cell-0-elbow-joint",
    "limits": [
      -0.6,
      0.6
    ],
    "units": "radians"
  },
  "answer": {
    "choiceIds": [
      "C",
      "D"
    ]
  }
}
```

### 约束故障诊断（h3-exp-d4-arm-2-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：cell-0-mount-joint
- B：cell-0-shoulder-joint
- C：cell-0-tool-joint
- D：cell-0-shuttle-joint

```json
{
  "input": {
    "endpoints": [
      "cell-0-wrist",
      "cell-0-tool"
    ],
    "type": "prismatic",
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
        "type": "prismatic",
        "anchorParent": [
          -19.5,
          0.4999999999999999,
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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.6999999999999993,
          0.6499999999999999,
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
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000004,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.4499999999999993,
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
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.4500000000000002,
          0.7
        ],
        "anchorChild": [
          -1.3499999999999979,
          0.34999999999999964,
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
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.4500000000000028,
          -0.40000000000000036,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-console-joint",
        "name": "cell-0-console interface",
        "parent": "foundation",
        "child": "cell-0-console",
        "type": "fixed",
        "anchorParent": [
          -19.5,
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
          -19.5,
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
          -6.5,
          0.4999999999999999,
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
        "id": "cell-1-yoke-joint",
        "name": "cell-1-yoke interface",
        "parent": "cell-1-mount",
        "child": "cell-1-yoke",
        "type": "fixed",
        "anchorParent": [
          0,
          0.5499999999999998,
          0
        ],
        "anchorChild": [
          -8.881784197001252e-16,
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
        "id": "cell-1-cradle-joint",
        "name": "cell-1-cradle interface",
        "parent": "cell-1-yoke",
        "child": "cell-1-cradle",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
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
        "id": "cell-1-optic-joint",
        "name": "cell-1-optic interface",
        "parent": "cell-1-cradle",
        "child": "cell-1-optic",
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
        "type": "fixed",
        "anchorParent": [
          -6.5,
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
          -6.5,
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
          6.5,
          0.4999999999999999,
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
        "id": "cell-2-wing-0-joint",
        "name": "cell-2-wing-0 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-0",
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
        "id": "cell-2-wing-1-joint",
        "name": "cell-2-wing-1 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.7200000000000006,
          2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-wing-2-joint",
        "name": "cell-2-wing-2 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-2",
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
        "id": "cell-2-wing-3-joint",
        "name": "cell-2-wing-3 interface",
        "parent": "cell-2-hub",
        "child": "cell-2-wing-3",
        "type": "revolute",
        "anchorParent": [
          -8.881784197001252e-16,
          1.96,
          -2.5
        ],
        "anchorChild": [
          0,
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
        "id": "cell-2-console-joint",
        "name": "cell-2-console interface",
        "parent": "foundation",
        "child": "cell-2-console",
        "type": "fixed",
        "anchorParent": [
          6.5,
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
          6.5,
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
        "id": "cell-3-shuttle-joint",
        "name": "cell-3-shuttle interface",
        "parent": "foundation",
        "child": "cell-3-shuttle",
        "type": "prismatic",
        "anchorParent": [
          19.5,
          0.4999999999999999,
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
        "id": "cell-3-mount-joint",
        "name": "cell-3-mount interface",
        "parent": "cell-3-shuttle",
        "child": "cell-3-mount",
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
        "id": "cell-3-hub-joint",
        "name": "cell-3-hub interface",
        "parent": "cell-3-mount",
        "child": "cell-3-hub",
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
        "id": "cell-3-probe-0-joint",
        "name": "cell-3-probe-0 interface",
        "parent": "cell-3-hub",
        "child": "cell-3-probe-0",
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
        "id": "cell-3-console-joint",
        "name": "cell-3-console interface",
        "parent": "foundation",
        "child": "cell-3-console",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-magazine-joint",
        "name": "cell-3-magazine interface",
        "parent": "foundation",
        "child": "cell-3-magazine",
        "type": "fixed",
        "anchorParent": [
          19.5,
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
        "id": "cell-3-drawer-joint",
        "name": "cell-3-drawer interface",
        "parent": "cell-3-magazine",
        "child": "cell-3-drawer",
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
      "C"
    ]
  }
}
```

### 主动检查收益（h3-exp-d4-arm-2-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-0
- B：query-2
- C：query-1

```json
{
  "input": {
    "queries": [
      {
        "id": "query-0",
        "cost": 3,
        "returns": [
          0,
          0,
          1,
          1
        ]
      },
      {
        "id": "query-1",
        "cost": 1,
        "returns": [
          0,
          1,
          2,
          3
        ]
      },
      {
        "id": "query-2",
        "cost": 2,
        "returns": [
          0,
          0,
          0,
          1
        ]
      }
    ],
    "module": "cell-0-tool",
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

### 不确定性与弃答（h3-exp-d4-arm-2-abstention）

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

### 观测后信念更新（h3-exp-d4-arm-2-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.3333333333333333
- B：0.5
- C：0
- D：0.25

```json
{
  "input": {
    "module": "cell-0-tool",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "negative",
      "negative",
      "positive",
      "positive"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 多目标工程权衡（h3-exp-d4-arm-2-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-3
- B：stock-2
- C：stock-0
- D：stock-1

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 9,
        "mass": 0.6
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 11,
        "mass": 0.7
      },
      {
        "id": "stock-2",
        "cost": 6,
        "stiffness": 8,
        "mass": 1.3
      },
      {
        "id": "stock-3",
        "cost": 3,
        "stiffness": 11,
        "mass": 1.3
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "C",
      "D"
    ]
  }
}
```

### 依赖装配（h3-exp-d4-arm-2-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:cell-3-hub",
        "label": "安装 cell-3-hub",
        "requires": [
          "present:cell-3-mount"
        ],
        "forbids": [
          "present:cell-3-hub"
        ],
        "adds": [
          "present:cell-3-hub"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-hub",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-wrist",
        "label": "安装 cell-0-wrist",
        "requires": [
          "present:cell-0-elbow"
        ],
        "forbids": [
          "present:cell-0-wrist"
        ],
        "adds": [
          "present:cell-0-wrist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-wrist",
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
        "id": "place:cell-0-tool",
        "label": "安装 cell-0-tool",
        "requires": [
          "present:cell-0-wrist"
        ],
        "forbids": [
          "present:cell-0-tool"
        ],
        "adds": [
          "present:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
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
        "id": "place:cell-2-wing-2",
        "label": "安装 cell-2-wing-2",
        "requires": [
          "present:cell-2-hub"
        ],
        "forbids": [
          "present:cell-2-wing-2"
        ],
        "adds": [
          "present:cell-2-wing-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-wing-2",
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
        "id": "place:cell-1-yoke",
        "label": "安装 cell-1-yoke",
        "requires": [
          "present:cell-1-mount"
        ],
        "forbids": [
          "present:cell-1-yoke"
        ],
        "adds": [
          "present:cell-1-yoke"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-yoke",
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
        "id": "place:cell-2-wing-0",
        "label": "安装 cell-2-wing-0",
        "requires": [
          "present:cell-2-hub"
        ],
        "forbids": [
          "present:cell-2-wing-0"
        ],
        "adds": [
          "present:cell-2-wing-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-wing-0",
          "visible": true
        }
      },
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
        "id": "place:cell-3-mount",
        "label": "安装 cell-3-mount",
        "requires": [
          "present:cell-3-shuttle"
        ],
        "forbids": [
          "present:cell-3-mount"
        ],
        "adds": [
          "present:cell-3-mount"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-mount",
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
        "id": "place:cell-0-shoulder",
        "label": "安装 cell-0-shoulder",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-shoulder"
        ],
        "adds": [
          "present:cell-0-shoulder"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-shoulder",
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
        "id": "place:cell-1-cradle",
        "label": "安装 cell-1-cradle",
        "requires": [
          "present:cell-1-yoke"
        ],
        "forbids": [
          "present:cell-1-cradle"
        ],
        "adds": [
          "present:cell-1-cradle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-cradle",
          "visible": true
        }
      },
      {
        "id": "place:cell-3-magazine",
        "label": "安装 cell-3-magazine",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-3-magazine"
        ],
        "adds": [
          "present:cell-3-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine",
          "visible": true
        }
      },
      {
        "id": "place:cell-3-probe-0",
        "label": "安装 cell-3-probe-0",
        "requires": [
          "present:cell-3-hub"
        ],
        "forbids": [
          "present:cell-3-probe-0"
        ],
        "adds": [
          "present:cell-3-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-probe-0",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-elbow",
        "label": "安装 cell-0-elbow",
        "requires": [
          "present:cell-0-shoulder"
        ],
        "forbids": [
          "present:cell-0-elbow"
        ],
        "adds": [
          "present:cell-0-elbow"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elbow",
          "visible": true
        }
      },
      {
        "id": "place:cell-3-drawer",
        "label": "安装 cell-3-drawer",
        "requires": [
          "present:cell-3-magazine"
        ],
        "forbids": [
          "present:cell-3-drawer"
        ],
        "adds": [
          "present:cell-3-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer",
          "visible": true
        }
      },
      {
        "id": "place:cell-1-optic",
        "label": "安装 cell-1-optic",
        "requires": [
          "present:cell-1-cradle"
        ],
        "forbids": [
          "present:cell-1-optic"
        ],
        "adds": [
          "present:cell-1-optic"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-optic",
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
        "id": "place:cell-2-wing-1",
        "label": "安装 cell-2-wing-1",
        "requires": [
          "present:cell-2-hub"
        ],
        "forbids": [
          "present:cell-2-wing-1"
        ],
        "adds": [
          "present:cell-2-wing-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-wing-1",
          "visible": true
        }
      },
      {
        "id": "place:cell-3-shuttle",
        "label": "安装 cell-3-shuttle",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-3-shuttle"
        ],
        "adds": [
          "present:cell-3-shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-shuttle",
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
        "id": "place:cell-2-wing-3",
        "label": "安装 cell-2-wing-3",
        "requires": [
          "present:cell-2-hub"
        ],
        "forbids": [
          "present:cell-2-wing-3"
        ],
        "adds": [
          "present:cell-2-wing-3"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-wing-3",
          "visible": true
        }
      },
      {
        "id": "place:cell-3-console",
        "label": "安装 cell-3-console",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-3-console"
        ],
        "adds": [
          "present:cell-3-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-console",
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
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:cell-0-shuttle",
      "present:cell-0-mount",
      "present:cell-0-shoulder",
      "present:cell-0-elbow",
      "present:cell-0-wrist",
      "present:cell-0-tool",
      "present:cell-0-console",
      "present:cell-0-magazine",
      "present:cell-0-drawer",
      "present:cell-1-shuttle",
      "present:cell-1-mount",
      "present:cell-1-yoke",
      "present:cell-1-cradle",
      "present:cell-1-optic",
      "present:cell-1-console",
      "present:cell-1-magazine",
      "present:cell-1-drawer",
      "present:cell-2-shuttle",
      "present:cell-2-mount",
      "present:cell-2-hub",
      "present:cell-2-wing-0",
      "present:cell-2-wing-1",
      "present:cell-2-wing-2",
      "present:cell-2-wing-3",
      "present:cell-2-console",
      "present:cell-2-magazine",
      "present:cell-2-drawer",
      "present:cell-3-shuttle",
      "present:cell-3-mount",
      "present:cell-3-hub",
      "present:cell-3-probe-0",
      "present:cell-3-console",
      "present:cell-3-magazine",
      "present:cell-3-drawer",
      "present:shared-inspection-mast",
      "present:shared-scanner"
    ],
    "budget": 37,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:cell-2-magazine",
      "place:cell-2-drawer",
      "place:cell-2-console",
      "place:cell-1-console",
      "place:cell-2-shuttle",
      "place:cell-2-mount",
      "place:cell-2-hub",
      "place:cell-2-wing-2",
      "place:cell-0-magazine",
      "place:cell-0-drawer",
      "place:cell-2-wing-0",
      "place:cell-0-console",
      "place:cell-1-shuttle",
      "place:cell-1-magazine",
      "place:cell-3-magazine",
      "place:cell-3-drawer",
      "place:cell-0-shuttle",
      "place:cell-2-wing-1",
      "place:cell-3-shuttle",
      "place:cell-3-mount",
      "place:cell-3-hub",
      "place:cell-3-probe-0",
      "place:shared-inspection-mast",
      "place:shared-scanner",
      "place:cell-0-mount",
      "place:cell-0-shoulder",
      "place:cell-0-elbow",
      "place:cell-0-wrist",
      "place:cell-0-tool",
      "place:cell-1-mount",
      "place:cell-1-yoke",
      "place:cell-1-cradle",
      "place:cell-1-optic",
      "place:cell-2-wing-3",
      "place:cell-3-console",
      "place:cell-1-drawer"
    ]
  }
}
```

### 依赖拆解（h3-exp-d4-arm-2-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:cell-0-shuttle",
      "present:cell-0-mount",
      "present:cell-0-shoulder",
      "present:cell-0-elbow",
      "present:cell-0-wrist",
      "present:cell-0-tool",
      "present:cell-0-console",
      "present:cell-0-magazine",
      "present:cell-0-drawer",
      "present:cell-1-shuttle",
      "present:cell-1-mount",
      "present:cell-1-yoke",
      "present:cell-1-cradle",
      "present:cell-1-optic",
      "present:cell-1-console",
      "present:cell-1-magazine",
      "present:cell-1-drawer",
      "present:cell-2-shuttle",
      "present:cell-2-mount",
      "present:cell-2-hub",
      "present:cell-2-wing-0",
      "present:cell-2-wing-1",
      "present:cell-2-wing-2",
      "present:cell-2-wing-3",
      "present:cell-2-console",
      "present:cell-2-magazine",
      "present:cell-2-drawer",
      "present:cell-3-shuttle",
      "present:cell-3-mount",
      "present:cell-3-hub",
      "present:cell-3-probe-0",
      "present:cell-3-console",
      "present:cell-3-magazine",
      "present:cell-3-drawer",
      "present:shared-inspection-mast",
      "present:shared-scanner"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-yoke",
      "cell-1-cradle",
      "cell-1-optic",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-wing-0",
      "cell-2-wing-1",
      "cell-2-wing-2",
      "cell-2-wing-3",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "cell-3-shuttle",
      "cell-3-mount",
      "cell-3-hub",
      "cell-3-probe-0",
      "cell-3-console",
      "cell-3-magazine",
      "cell-3-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "actions": [
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
      },
      {
        "id": "remove:cell-3-drawer",
        "label": "拆除 cell-3-drawer",
        "requires": [
          "present:cell-3-drawer"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-3-drawer"
        ],
        "deletes": [
          "present:cell-3-drawer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer",
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
        "id": "remove:cell-1-optic",
        "label": "拆除 cell-1-optic",
        "requires": [
          "present:cell-1-optic"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-1-optic"
        ],
        "deletes": [
          "present:cell-1-optic"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-optic",
          "visible": false
        }
      },
      {
        "id": "remove:cell-2-wing-1",
        "label": "拆除 cell-2-wing-1",
        "requires": [
          "present:cell-2-wing-1"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-2-wing-1"
        ],
        "deletes": [
          "present:cell-2-wing-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-wing-1",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-cradle",
        "label": "拆除 cell-1-cradle",
        "requires": [
          "present:cell-1-cradle"
        ],
        "forbids": [
          "present:cell-1-optic"
        ],
        "adds": [
          "removed:cell-1-cradle"
        ],
        "deletes": [
          "present:cell-1-cradle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-cradle",
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
          "present:cell-2-wing-0",
          "present:cell-2-wing-1",
          "present:cell-2-wing-2",
          "present:cell-2-wing-3"
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
        "id": "remove:cell-3-shuttle",
        "label": "拆除 cell-3-shuttle",
        "requires": [
          "present:cell-3-shuttle"
        ],
        "forbids": [
          "present:cell-3-mount"
        ],
        "adds": [
          "removed:cell-3-shuttle"
        ],
        "deletes": [
          "present:cell-3-shuttle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-shuttle",
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
        "id": "remove:cell-2-wing-0",
        "label": "拆除 cell-2-wing-0",
        "requires": [
          "present:cell-2-wing-0"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-2-wing-0"
        ],
        "deletes": [
          "present:cell-2-wing-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-wing-0",
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
        "id": "remove:cell-3-probe-0",
        "label": "拆除 cell-3-probe-0",
        "requires": [
          "present:cell-3-probe-0"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-3-probe-0"
        ],
        "deletes": [
          "present:cell-3-probe-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-probe-0",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-elbow",
        "label": "拆除 cell-0-elbow",
        "requires": [
          "present:cell-0-elbow"
        ],
        "forbids": [
          "present:cell-0-wrist"
        ],
        "adds": [
          "removed:cell-0-elbow"
        ],
        "deletes": [
          "present:cell-0-elbow"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elbow",
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
        "id": "remove:cell-0-mount",
        "label": "拆除 cell-0-mount",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-shoulder"
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
        "id": "remove:cell-1-yoke",
        "label": "拆除 cell-1-yoke",
        "requires": [
          "present:cell-1-yoke"
        ],
        "forbids": [
          "present:cell-1-cradle"
        ],
        "adds": [
          "removed:cell-1-yoke"
        ],
        "deletes": [
          "present:cell-1-yoke"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-yoke",
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
        "id": "remove:cell-2-wing-2",
        "label": "拆除 cell-2-wing-2",
        "requires": [
          "present:cell-2-wing-2"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-2-wing-2"
        ],
        "deletes": [
          "present:cell-2-wing-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-wing-2",
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
          "present:cell-3-shuttle",
          "present:cell-3-console",
          "present:cell-3-magazine",
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
        "id": "remove:cell-0-shoulder",
        "label": "拆除 cell-0-shoulder",
        "requires": [
          "present:cell-0-shoulder"
        ],
        "forbids": [
          "present:cell-0-elbow"
        ],
        "adds": [
          "removed:cell-0-shoulder"
        ],
        "deletes": [
          "present:cell-0-shoulder"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-shoulder",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-tool",
        "label": "拆除 cell-0-tool",
        "requires": [
          "present:cell-0-tool"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-tool"
        ],
        "deletes": [
          "present:cell-0-tool"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
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
        "id": "remove:cell-1-mount",
        "label": "拆除 cell-1-mount",
        "requires": [
          "present:cell-1-mount"
        ],
        "forbids": [
          "present:cell-1-yoke"
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
        "id": "remove:cell-3-mount",
        "label": "拆除 cell-3-mount",
        "requires": [
          "present:cell-3-mount"
        ],
        "forbids": [
          "present:cell-3-hub"
        ],
        "adds": [
          "removed:cell-3-mount"
        ],
        "deletes": [
          "present:cell-3-mount"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-mount",
          "visible": false
        }
      },
      {
        "id": "remove:cell-2-wing-3",
        "label": "拆除 cell-2-wing-3",
        "requires": [
          "present:cell-2-wing-3"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-2-wing-3"
        ],
        "deletes": [
          "present:cell-2-wing-3"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-2-wing-3",
          "visible": false
        }
      },
      {
        "id": "remove:cell-3-magazine",
        "label": "拆除 cell-3-magazine",
        "requires": [
          "present:cell-3-magazine"
        ],
        "forbids": [
          "present:cell-3-drawer"
        ],
        "adds": [
          "removed:cell-3-magazine"
        ],
        "deletes": [
          "present:cell-3-magazine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine",
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
        "id": "remove:cell-3-hub",
        "label": "拆除 cell-3-hub",
        "requires": [
          "present:cell-3-hub"
        ],
        "forbids": [
          "present:cell-3-probe-0"
        ],
        "adds": [
          "removed:cell-3-hub"
        ],
        "deletes": [
          "present:cell-3-hub"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-hub",
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
        "id": "remove:cell-0-wrist",
        "label": "拆除 cell-0-wrist",
        "requires": [
          "present:cell-0-wrist"
        ],
        "forbids": [
          "present:cell-0-tool"
        ],
        "adds": [
          "removed:cell-0-wrist"
        ],
        "deletes": [
          "present:cell-0-wrist"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-wrist",
          "visible": false
        }
      },
      {
        "id": "remove:cell-3-console",
        "label": "拆除 cell-3-console",
        "requires": [
          "present:cell-3-console"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-3-console"
        ],
        "deletes": [
          "present:cell-3-console"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-console",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:shared-scanner",
      "removed:shared-inspection-mast",
      "removed:cell-3-drawer",
      "removed:cell-3-magazine",
      "removed:cell-3-console",
      "removed:cell-3-probe-0",
      "removed:cell-3-hub",
      "removed:cell-3-mount",
      "removed:cell-3-shuttle",
      "removed:cell-2-drawer",
      "removed:cell-2-magazine",
      "removed:cell-2-console",
      "removed:cell-2-wing-3",
      "removed:cell-2-wing-2",
      "removed:cell-2-wing-1",
      "removed:cell-2-wing-0",
      "removed:cell-2-hub",
      "removed:cell-2-mount",
      "removed:cell-2-shuttle",
      "removed:cell-1-drawer",
      "removed:cell-1-magazine",
      "removed:cell-1-console",
      "removed:cell-1-optic",
      "removed:cell-1-cradle",
      "removed:cell-1-yoke",
      "removed:cell-1-mount",
      "removed:cell-1-shuttle",
      "removed:cell-0-drawer",
      "removed:cell-0-magazine",
      "removed:cell-0-console",
      "removed:cell-0-tool",
      "removed:cell-0-wrist",
      "removed:cell-0-elbow",
      "removed:cell-0-shoulder",
      "removed:cell-0-mount",
      "removed:cell-0-shuttle",
      "removed:foundation"
    ],
    "budget": 37,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:cell-3-drawer",
      "remove:cell-2-drawer",
      "remove:cell-1-optic",
      "remove:cell-2-wing-1",
      "remove:cell-1-cradle",
      "remove:cell-2-wing-0",
      "remove:cell-3-probe-0",
      "remove:cell-2-magazine",
      "remove:cell-1-yoke",
      "remove:cell-0-console",
      "remove:cell-0-drawer",
      "remove:cell-2-wing-2",
      "remove:cell-2-console",
      "remove:cell-0-tool",
      "remove:cell-1-console",
      "remove:cell-1-drawer",
      "remove:cell-1-magazine",
      "remove:cell-1-mount",
      "remove:cell-1-shuttle",
      "remove:shared-scanner",
      "remove:cell-2-wing-3",
      "remove:cell-2-hub",
      "remove:cell-2-mount",
      "remove:cell-2-shuttle",
      "remove:cell-3-magazine",
      "remove:cell-0-magazine",
      "remove:cell-3-hub",
      "remove:cell-3-mount",
      "remove:cell-3-shuttle",
      "remove:shared-inspection-mast",
      "remove:cell-0-wrist",
      "remove:cell-0-elbow",
      "remove:cell-0-shoulder",
      "remove:cell-0-mount",
      "remove:cell-0-shuttle",
      "remove:cell-3-console",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-exp-d4-arm-2-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-tool",
      "closed:cell-0-tool"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-yoke",
      "cell-1-cradle",
      "cell-1-optic",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-wing-0",
      "cell-2-wing-1",
      "cell-2-wing-2",
      "cell-2-wing-3",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "cell-3-shuttle",
      "cell-3-mount",
      "cell-3-hub",
      "cell-3-probe-0",
      "cell-3-console",
      "cell-3-magazine",
      "cell-3-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "actions": [
      {
        "id": "open:cell-0-tool",
        "label": "open cell-0-tool",
        "requires": [
          "done:support:cell-0-tool"
        ],
        "forbids": [
          "done:open:cell-0-tool"
        ],
        "adds": [
          "done:open:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "close:cell-0-tool",
        "label": "close cell-0-tool",
        "requires": [
          "done:verify:cell-0-tool"
        ],
        "forbids": [
          "done:close:cell-0-tool"
        ],
        "adds": [
          "done:close:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "release:cell-0-tool",
        "label": "release cell-0-tool",
        "requires": [
          "done:close:cell-0-tool"
        ],
        "forbids": [
          "done:release:cell-0-tool"
        ],
        "adds": [
          "done:release:cell-0-tool",
          "repaired:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "verify:cell-0-tool",
        "label": "verify cell-0-tool",
        "requires": [
          "done:replace:cell-0-tool"
        ],
        "forbids": [
          "done:verify:cell-0-tool"
        ],
        "adds": [
          "done:verify:cell-0-tool"
        ],
        "deletes": [
          "fault:cell-0-tool"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "remove:cell-0-tool",
        "label": "remove cell-0-tool",
        "requires": [
          "done:open:cell-0-tool"
        ],
        "forbids": [
          "done:remove:cell-0-tool"
        ],
        "adds": [
          "done:remove:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
          "visible": false
        }
      },
      {
        "id": "support:cell-0-tool",
        "label": "support cell-0-tool",
        "requires": [
          "fault:cell-0-tool"
        ],
        "forbids": [
          "done:support:cell-0-tool"
        ],
        "adds": [
          "done:support:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "replace:cell-0-tool",
        "label": "replace cell-0-tool",
        "requires": [
          "done:remove:cell-0-tool"
        ],
        "forbids": [
          "done:replace:cell-0-tool"
        ],
        "adds": [
          "done:replace:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-tool"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-tool",
      "open:cell-0-tool",
      "remove:cell-0-tool",
      "replace:cell-0-tool",
      "verify:cell-0-tool",
      "close:cell-0-tool",
      "release:cell-0-tool"
    ]
  }
}
```

### 复合编辑验证（h3-exp-d4-arm-2-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-tool",
      "closed:cell-0-tool"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-yoke",
      "cell-1-cradle",
      "cell-1-optic",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-wing-0",
      "cell-2-wing-1",
      "cell-2-wing-2",
      "cell-2-wing-3",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "cell-3-shuttle",
      "cell-3-mount",
      "cell-3-hub",
      "cell-3-probe-0",
      "cell-3-console",
      "cell-3-magazine",
      "cell-3-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "actions": [
      {
        "id": "open:cell-0-tool",
        "label": "open cell-0-tool",
        "requires": [
          "done:support:cell-0-tool"
        ],
        "forbids": [
          "done:open:cell-0-tool"
        ],
        "adds": [
          "done:open:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "close:cell-0-tool",
        "label": "close cell-0-tool",
        "requires": [
          "done:verify:cell-0-tool"
        ],
        "forbids": [
          "done:close:cell-0-tool"
        ],
        "adds": [
          "done:close:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "release:cell-0-tool",
        "label": "release cell-0-tool",
        "requires": [
          "done:close:cell-0-tool"
        ],
        "forbids": [
          "done:release:cell-0-tool"
        ],
        "adds": [
          "done:release:cell-0-tool",
          "repaired:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "recolor:cell-0-tool",
        "label": "recolor cell-0-tool",
        "requires": [
          "done:open:cell-0-tool"
        ],
        "forbids": [
          "done:recolor:cell-0-tool"
        ],
        "adds": [
          "done:recolor:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
          "color": "#ea7635"
        }
      },
      {
        "id": "verify:cell-0-tool",
        "label": "verify cell-0-tool",
        "requires": [
          "done:recolor:cell-0-tool"
        ],
        "forbids": [
          "done:verify:cell-0-tool"
        ],
        "adds": [
          "done:verify:cell-0-tool"
        ],
        "deletes": [
          "fault:cell-0-tool"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "support:cell-0-tool",
        "label": "support cell-0-tool",
        "requires": [
          "fault:cell-0-tool"
        ],
        "forbids": [
          "done:support:cell-0-tool"
        ],
        "adds": [
          "done:support:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-tool"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-tool",
      "open:cell-0-tool",
      "recolor:cell-0-tool",
      "verify:cell-0-tool",
      "close:cell-0-tool",
      "release:cell-0-tool"
    ]
  }
}
```

### 跨区域联合维修（h3-exp-d4-arm-2-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-3-magazine",
      "closed:cell-3-magazine",
      "fault:cell-3-drawer",
      "closed:cell-3-drawer",
      "fault:shared-inspection-mast",
      "closed:shared-inspection-mast",
      "fault:shared-scanner",
      "closed:shared-scanner"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-yoke",
      "cell-1-cradle",
      "cell-1-optic",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-wing-0",
      "cell-2-wing-1",
      "cell-2-wing-2",
      "cell-2-wing-3",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "cell-3-shuttle",
      "cell-3-mount",
      "cell-3-hub",
      "cell-3-probe-0",
      "cell-3-console",
      "cell-3-magazine",
      "cell-3-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "actions": [
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
        "id": "remove:cell-3-drawer",
        "label": "remove cell-3-drawer",
        "requires": [
          "done:open:cell-3-drawer"
        ],
        "forbids": [
          "done:remove:cell-3-drawer"
        ],
        "adds": [
          "done:remove:cell-3-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer",
          "visible": false
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
        "id": "support:cell-3-drawer",
        "label": "support cell-3-drawer",
        "requires": [
          "fault:cell-3-drawer"
        ],
        "forbids": [
          "done:support:cell-3-drawer"
        ],
        "adds": [
          "done:support:cell-3-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer"
        }
      },
      {
        "id": "open:cell-3-drawer",
        "label": "open cell-3-drawer",
        "requires": [
          "done:support:cell-3-drawer"
        ],
        "forbids": [
          "done:open:cell-3-drawer"
        ],
        "adds": [
          "done:open:cell-3-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer"
        }
      },
      {
        "id": "close:cell-3-magazine",
        "label": "close cell-3-magazine",
        "requires": [
          "done:verify:cell-3-magazine"
        ],
        "forbids": [
          "done:close:cell-3-magazine"
        ],
        "adds": [
          "done:close:cell-3-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine"
        }
      },
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
        "id": "replace:cell-3-drawer",
        "label": "replace cell-3-drawer",
        "requires": [
          "done:remove:cell-3-drawer"
        ],
        "forbids": [
          "done:replace:cell-3-drawer"
        ],
        "adds": [
          "done:replace:cell-3-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer",
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
        "id": "verify:cell-3-magazine",
        "label": "verify cell-3-magazine",
        "requires": [
          "done:replace:cell-3-magazine"
        ],
        "forbids": [
          "done:verify:cell-3-magazine"
        ],
        "adds": [
          "done:verify:cell-3-magazine"
        ],
        "deletes": [
          "fault:cell-3-magazine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine"
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
        "id": "release:cell-3-drawer",
        "label": "release cell-3-drawer",
        "requires": [
          "done:close:cell-3-drawer"
        ],
        "forbids": [
          "done:release:cell-3-drawer"
        ],
        "adds": [
          "done:release:cell-3-drawer",
          "repaired:cell-3-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer"
        }
      },
      {
        "id": "close:cell-3-drawer",
        "label": "close cell-3-drawer",
        "requires": [
          "done:verify:cell-3-drawer"
        ],
        "forbids": [
          "done:close:cell-3-drawer"
        ],
        "adds": [
          "done:close:cell-3-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer"
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
        "id": "verify:cell-3-drawer",
        "label": "verify cell-3-drawer",
        "requires": [
          "done:replace:cell-3-drawer"
        ],
        "forbids": [
          "done:verify:cell-3-drawer"
        ],
        "adds": [
          "done:verify:cell-3-drawer"
        ],
        "deletes": [
          "fault:cell-3-drawer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer"
        }
      },
      {
        "id": "open:cell-3-magazine",
        "label": "open cell-3-magazine",
        "requires": [
          "done:support:cell-3-magazine"
        ],
        "forbids": [
          "done:open:cell-3-magazine"
        ],
        "adds": [
          "done:open:cell-3-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine"
        }
      },
      {
        "id": "replace:cell-3-magazine",
        "label": "replace cell-3-magazine",
        "requires": [
          "done:remove:cell-3-magazine"
        ],
        "forbids": [
          "done:replace:cell-3-magazine"
        ],
        "adds": [
          "done:replace:cell-3-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine",
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
        "id": "release:cell-3-magazine",
        "label": "release cell-3-magazine",
        "requires": [
          "done:close:cell-3-magazine"
        ],
        "forbids": [
          "done:release:cell-3-magazine"
        ],
        "adds": [
          "done:release:cell-3-magazine",
          "repaired:cell-3-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine"
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
        "id": "remove:cell-3-magazine",
        "label": "remove cell-3-magazine",
        "requires": [
          "done:open:cell-3-magazine"
        ],
        "forbids": [
          "done:remove:cell-3-magazine"
        ],
        "adds": [
          "done:remove:cell-3-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine",
          "visible": false
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
        "id": "support:cell-3-magazine",
        "label": "support cell-3-magazine",
        "requires": [
          "fault:cell-3-magazine"
        ],
        "forbids": [
          "done:support:cell-3-magazine"
        ],
        "adds": [
          "done:support:cell-3-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-3-magazine",
      "repaired:cell-3-drawer",
      "repaired:shared-inspection-mast",
      "repaired:shared-scanner"
    ],
    "budget": 28,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-3-drawer",
      "open:cell-3-drawer",
      "remove:cell-3-drawer",
      "replace:cell-3-drawer",
      "support:shared-inspection-mast",
      "open:shared-inspection-mast",
      "support:shared-scanner",
      "open:shared-scanner",
      "verify:cell-3-drawer",
      "close:cell-3-drawer",
      "release:cell-3-drawer",
      "remove:shared-scanner",
      "replace:shared-scanner",
      "verify:shared-scanner",
      "close:shared-scanner",
      "release:shared-scanner",
      "remove:shared-inspection-mast",
      "replace:shared-inspection-mast",
      "verify:shared-inspection-mast",
      "close:shared-inspection-mast",
      "release:shared-inspection-mast",
      "support:cell-3-magazine",
      "open:cell-3-magazine",
      "remove:cell-3-magazine",
      "replace:cell-3-magazine",
      "verify:cell-3-magazine",
      "close:cell-3-magazine",
      "release:cell-3-magazine"
    ]
  }
}
```

### 多工位资源调度（h3-exp-d4-arm-2-scheduling）

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
        "module": "cell-0-shoulder",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "cell-0-elbow",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "cell-0-wrist",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      },
      {
        "id": "job-6",
        "module": "cell-0-tool",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-4"
        ]
      },
      {
        "id": "job-7",
        "module": "cell-0-console",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-5"
        ]
      },
      {
        "id": "job-8",
        "module": "cell-0-magazine",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-6"
        ]
      },
      {
        "id": "job-9",
        "module": "cell-0-drawer",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-7"
        ]
      }
    ],
    "deadline": 10
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 1,
      "job-4": 4,
      "job-5": 2,
      "job-6": 7,
      "job-7": 3,
      "job-8": 9,
      "job-9": 5
    }
  }
}
```

### 检查后条件策略（h3-exp-d4-arm-2-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-tool",
    "worlds": [
      {
        "id": "normal",
        "action": "replace"
      },
      {
        "id": "loose",
        "action": "continue"
      },
      {
        "id": "jammed",
        "action": "tighten"
      }
    ],
    "budget": 3,
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
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "normal": "signal-0",
          "loose": "signal-1",
          "jammed": "signal-2"
        }
      }
    ]
  },
  "answer": {
    "queryId": "thermal",
    "decisions": {
      "signal-0": "replace",
      "signal-1": "continue",
      "signal-2": "tighten"
    }
  }
}
```

### 局部坐标变换（h3-exp-d4-arm-2-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[1,0.2625,0]
- B：[-14.9,5.8,2.3]
- C：[-15.9,4.8,1.3]

```json
{
  "input": {
    "localPoint": [
      1,
      0.2625000000000002,
      0
    ],
    "rotationXYZW": [
      0,
      0,
      0,
      1
    ],
    "translation": [
      -16.9,
      4.5375,
      1.3
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-exp-d4-arm-2-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[5,-6]
- B：[11,5]
- C：[5,6]
- D：[0,0]

```json
{
  "input": {
    "view": "top",
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

### 空间相对关系（h3-exp-d4-arm-2-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：equal
- B：greater
- C：less

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
    "axis": "z"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 约束自由度（h3-exp-d4-arm-2-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：1
- B：0
- C：3
- D：6

```json
{
  "input": {
    "joint": {
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
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 维修间隙预算（h3-exp-d4-arm-2-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "cell-0-tool",
    "aperture": 0.8200000000000001,
    "toolWidth": 0.65,
    "eachSideMargin": 0.1
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-exp-d4-arm-2-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,-4,0]
- C：[0,0,-20]
- D：[0,0,20]

```json
{
  "input": {
    "module": "cell-0-tool",
    "lever": [
      4,
      3,
      0
    ],
    "force": [
      0,
      -5,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 非均匀先验更新（h3-exp-d4-arm-2-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.18181818181818182
- B：0
- C：1
- D：0.3333333333333333

```json
{
  "input": {
    "module": "cell-0-tool",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      4,
      2,
      5
    ],
    "compatible": [
      "normal",
      "jammed"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 风险最小决策（h3-exp-d4-arm-2-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.5,
    "repairCost": 1,
    "failureLoss": 16,
    "module": "cell-0-tool"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-exp-d4-arm-2-trace-threshold）

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
        "displacement": 0.016323870037975755
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.01538021355252516
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.012283465603825048
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.005088173205986325
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0007392597020711207
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00033787069412119253
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0005408243661113503
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00007812456984420164
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.000014720295944626933
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.000014720295944626933
      },
      {
        "time": 1,
        "displacement": 0.000014720295944626933
      }
    ],
    "threshold": 0.013059096030380605
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-exp-d4-arm-2-guarded-repair）

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
        "id": "release:cell-0-tool",
        "label": "release cell-0-tool",
        "requires": [
          "done:relock:cell-0-tool"
        ],
        "forbids": [
          "done:release:cell-0-tool"
        ],
        "adds": [
          "done:release:cell-0-tool",
          "ready:cell-0-tool",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "relock:cell-0-tool",
        "label": "relock cell-0-tool",
        "requires": [
          "done:verify:cell-0-tool"
        ],
        "forbids": [
          "done:relock:cell-0-tool"
        ],
        "adds": [
          "done:relock:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "verify:cell-0-tool",
        "label": "verify cell-0-tool",
        "requires": [
          "done:replace:cell-0-tool"
        ],
        "forbids": [
          "done:verify:cell-0-tool"
        ],
        "adds": [
          "done:verify:cell-0-tool"
        ],
        "deletes": [
          "fault:cell-0-tool",
          "misaligned:cell-0-tool"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "replace:cell-0-tool",
        "label": "replace cell-0-tool",
        "requires": [
          "done:unlock:cell-0-tool"
        ],
        "forbids": [
          "done:replace:cell-0-tool"
        ],
        "adds": [
          "done:replace:cell-0-tool"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "unlock:cell-0-tool",
        "label": "unlock cell-0-tool",
        "requires": [
          "done:support:cell-0-tool"
        ],
        "forbids": [
          "done:unlock:cell-0-tool"
        ],
        "adds": [
          "done:unlock:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "support:cell-0-tool",
        "label": "support cell-0-tool",
        "requires": [
          "done:isolate:cell-0-tool"
        ],
        "forbids": [
          "done:support:cell-0-tool"
        ],
        "adds": [
          "done:support:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "isolate:cell-0-tool",
        "label": "isolate cell-0-tool",
        "requires": [
          "tool:free",
          "fault:cell-0-tool"
        ],
        "forbids": [
          "done:isolate:cell-0-tool"
        ],
        "adds": [
          "done:isolate:cell-0-tool"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-tool"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-yoke",
      "cell-1-cradle",
      "cell-1-optic",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-wing-0",
      "cell-2-wing-1",
      "cell-2-wing-2",
      "cell-2-wing-3",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "cell-3-shuttle",
      "cell-3-mount",
      "cell-3-hub",
      "cell-3-probe-0",
      "cell-3-console",
      "cell-3-magazine",
      "cell-3-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "goalFacts": [
      "ready:cell-0-tool"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-tool",
      "support:cell-0-tool",
      "unlock:cell-0-tool",
      "replace:cell-0-tool",
      "verify:cell-0-tool",
      "relock:cell-0-tool",
      "release:cell-0-tool"
    ]
  }
}
```

### 失败状态回退（h3-exp-d4-arm-2-rollback）

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
        "id": "resume:cell-0-tool",
        "label": "resume cell-0-tool",
        "requires": [
          "done:verify:cell-0-tool"
        ],
        "forbids": [
          "done:resume:cell-0-tool"
        ],
        "adds": [
          "done:resume:cell-0-tool",
          "ready:cell-0-tool",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "verify:cell-0-tool",
        "label": "verify cell-0-tool",
        "requires": [
          "done:align:cell-0-tool"
        ],
        "forbids": [
          "done:verify:cell-0-tool"
        ],
        "adds": [
          "done:verify:cell-0-tool"
        ],
        "deletes": [
          "fault:cell-0-tool",
          "misaligned:cell-0-tool"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "align:cell-0-tool",
        "label": "align cell-0-tool",
        "requires": [
          "done:undo:cell-0-tool"
        ],
        "forbids": [
          "done:align:cell-0-tool"
        ],
        "adds": [
          "done:align:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
          "visible": true
        }
      },
      {
        "id": "undo:cell-0-tool",
        "label": "undo cell-0-tool",
        "requires": [
          "done:isolate:cell-0-tool"
        ],
        "forbids": [
          "done:undo:cell-0-tool"
        ],
        "adds": [
          "done:undo:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
          "visible": false
        }
      },
      {
        "id": "isolate:cell-0-tool",
        "label": "isolate cell-0-tool",
        "requires": [
          "tool:free",
          "fault:cell-0-tool"
        ],
        "forbids": [
          "done:isolate:cell-0-tool"
        ],
        "adds": [
          "done:isolate:cell-0-tool"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-tool",
      "misaligned:cell-0-tool"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-yoke",
      "cell-1-cradle",
      "cell-1-optic",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-wing-0",
      "cell-2-wing-1",
      "cell-2-wing-2",
      "cell-2-wing-3",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "cell-3-shuttle",
      "cell-3-mount",
      "cell-3-hub",
      "cell-3-probe-0",
      "cell-3-console",
      "cell-3-magazine",
      "cell-3-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "goalFacts": [
      "ready:cell-0-tool"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-tool",
      "undo:cell-0-tool",
      "align:cell-0-tool",
      "verify:cell-0-tool",
      "resume:cell-0-tool"
    ]
  }
}
```

### 共享工具协同维修（h3-exp-d4-arm-2-resource-repair）

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
        "id": "release:cell-3-drawer",
        "label": "release cell-3-drawer",
        "requires": [
          "done:relock:cell-3-drawer"
        ],
        "forbids": [
          "done:release:cell-3-drawer"
        ],
        "adds": [
          "done:release:cell-3-drawer",
          "ready:cell-3-drawer",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer"
        }
      },
      {
        "id": "relock:cell-3-drawer",
        "label": "relock cell-3-drawer",
        "requires": [
          "done:verify:cell-3-drawer"
        ],
        "forbids": [
          "done:relock:cell-3-drawer"
        ],
        "adds": [
          "done:relock:cell-3-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer"
        }
      },
      {
        "id": "verify:cell-3-drawer",
        "label": "verify cell-3-drawer",
        "requires": [
          "done:replace:cell-3-drawer"
        ],
        "forbids": [
          "done:verify:cell-3-drawer"
        ],
        "adds": [
          "done:verify:cell-3-drawer"
        ],
        "deletes": [
          "fault:cell-3-drawer",
          "misaligned:cell-3-drawer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer"
        }
      },
      {
        "id": "replace:cell-3-drawer",
        "label": "replace cell-3-drawer",
        "requires": [
          "done:unlock:cell-3-drawer"
        ],
        "forbids": [
          "done:replace:cell-3-drawer"
        ],
        "adds": [
          "done:replace:cell-3-drawer"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-3-drawer"
        }
      },
      {
        "id": "unlock:cell-3-drawer",
        "label": "unlock cell-3-drawer",
        "requires": [
          "done:support:cell-3-drawer"
        ],
        "forbids": [
          "done:unlock:cell-3-drawer"
        ],
        "adds": [
          "done:unlock:cell-3-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer"
        }
      },
      {
        "id": "support:cell-3-drawer",
        "label": "support cell-3-drawer",
        "requires": [
          "done:isolate:cell-3-drawer"
        ],
        "forbids": [
          "done:support:cell-3-drawer"
        ],
        "adds": [
          "done:support:cell-3-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer"
        }
      },
      {
        "id": "isolate:cell-3-drawer",
        "label": "isolate cell-3-drawer",
        "requires": [
          "tool:free",
          "fault:cell-3-drawer"
        ],
        "forbids": [
          "done:isolate:cell-3-drawer"
        ],
        "adds": [
          "done:isolate:cell-3-drawer"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-drawer"
        }
      },
      {
        "id": "release:cell-3-magazine",
        "label": "release cell-3-magazine",
        "requires": [
          "done:relock:cell-3-magazine"
        ],
        "forbids": [
          "done:release:cell-3-magazine"
        ],
        "adds": [
          "done:release:cell-3-magazine",
          "ready:cell-3-magazine",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine"
        }
      },
      {
        "id": "relock:cell-3-magazine",
        "label": "relock cell-3-magazine",
        "requires": [
          "done:verify:cell-3-magazine"
        ],
        "forbids": [
          "done:relock:cell-3-magazine"
        ],
        "adds": [
          "done:relock:cell-3-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine"
        }
      },
      {
        "id": "verify:cell-3-magazine",
        "label": "verify cell-3-magazine",
        "requires": [
          "done:replace:cell-3-magazine"
        ],
        "forbids": [
          "done:verify:cell-3-magazine"
        ],
        "adds": [
          "done:verify:cell-3-magazine"
        ],
        "deletes": [
          "fault:cell-3-magazine",
          "misaligned:cell-3-magazine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine"
        }
      },
      {
        "id": "replace:cell-3-magazine",
        "label": "replace cell-3-magazine",
        "requires": [
          "done:unlock:cell-3-magazine"
        ],
        "forbids": [
          "done:replace:cell-3-magazine"
        ],
        "adds": [
          "done:replace:cell-3-magazine"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-3-magazine"
        }
      },
      {
        "id": "unlock:cell-3-magazine",
        "label": "unlock cell-3-magazine",
        "requires": [
          "done:support:cell-3-magazine"
        ],
        "forbids": [
          "done:unlock:cell-3-magazine"
        ],
        "adds": [
          "done:unlock:cell-3-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine"
        }
      },
      {
        "id": "support:cell-3-magazine",
        "label": "support cell-3-magazine",
        "requires": [
          "done:isolate:cell-3-magazine"
        ],
        "forbids": [
          "done:support:cell-3-magazine"
        ],
        "adds": [
          "done:support:cell-3-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine"
        }
      },
      {
        "id": "isolate:cell-3-magazine",
        "label": "isolate cell-3-magazine",
        "requires": [
          "tool:free",
          "fault:cell-3-magazine"
        ],
        "forbids": [
          "done:isolate:cell-3-magazine"
        ],
        "adds": [
          "done:isolate:cell-3-magazine"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-3-magazine"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-3-magazine",
      "fault:cell-3-drawer",
      "fault:shared-inspection-mast",
      "fault:shared-scanner"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-yoke",
      "cell-1-cradle",
      "cell-1-optic",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer",
      "cell-2-shuttle",
      "cell-2-mount",
      "cell-2-hub",
      "cell-2-wing-0",
      "cell-2-wing-1",
      "cell-2-wing-2",
      "cell-2-wing-3",
      "cell-2-console",
      "cell-2-magazine",
      "cell-2-drawer",
      "cell-3-shuttle",
      "cell-3-mount",
      "cell-3-hub",
      "cell-3-probe-0",
      "cell-3-console",
      "cell-3-magazine",
      "cell-3-drawer",
      "shared-inspection-mast",
      "shared-scanner"
    ],
    "goalFacts": [
      "ready:cell-3-magazine",
      "ready:cell-3-drawer",
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
      "isolate:cell-3-drawer",
      "support:cell-3-drawer",
      "unlock:cell-3-drawer",
      "replace:cell-3-drawer",
      "verify:cell-3-drawer",
      "relock:cell-3-drawer",
      "release:cell-3-drawer",
      "isolate:cell-3-magazine",
      "support:cell-3-magazine",
      "unlock:cell-3-magazine",
      "replace:cell-3-magazine",
      "verify:cell-3-magazine",
      "relock:cell-3-magazine",
      "release:cell-3-magazine"
    ]
  }
}
```

### 预算约束检查策略（h3-exp-d4-arm-2-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-tool",
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
        "cost": 4,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      },
      {
        "id": "probe",
        "cost": 3,
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
    "budget": 3
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
