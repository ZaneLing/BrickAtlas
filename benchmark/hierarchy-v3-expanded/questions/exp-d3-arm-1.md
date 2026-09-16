## D3 复合机构·折肘检修臂

### 模块识别（h3-exp-d3-arm-1-identify）

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
        "id": "cell-1-carriage",
        "name": "cell 1 carriage"
      },
      {
        "id": "cell-1-cross-feed",
        "name": "cell 1 cross feed"
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
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 部件计数（h3-exp-d3-arm-1-count）

模块 cell-0-tool 有多少个可视零件？

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
        "id": "cell-0-shuttle-p118",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p119",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p120",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p121",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p122",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p123",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p124",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p125",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p126",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p127",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p128",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p129",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p130",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p131",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p132",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p133",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p134",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p135",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p136",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p137",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p138",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p139",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p140",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p141",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p142",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p143",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p144",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p145",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p146",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p147",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p148",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p149",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p150",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p151",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p152",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p153",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p154",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p155",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p156",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p157",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p158",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p159",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p160",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p161",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p162",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p163",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p164",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-shuttle-p165",
        "moduleId": "cell-0-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-mount-p166",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p167",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p168",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p169",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p170",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p171",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p172",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p173",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p174",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p175",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p176",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p177",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p178",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p179",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p180",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p181",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p182",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p183",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p184",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p185",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p186",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p187",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p188",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p189",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p190",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p191",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p192",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p193",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p194",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p195",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-shoulder-p196",
        "moduleId": "cell-0-shoulder",
        "shape": "cylinder",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-elbow-p197",
        "moduleId": "cell-0-elbow",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-elbow-p198",
        "moduleId": "cell-0-elbow",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-elbow-p199",
        "moduleId": "cell-0-elbow",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-wrist-p200",
        "moduleId": "cell-0-wrist",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-wrist-p201",
        "moduleId": "cell-0-wrist",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-wrist-p202",
        "moduleId": "cell-0-wrist",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-tool-p203",
        "moduleId": "cell-0-tool",
        "shape": "arch",
        "color": "#45a080"
      },
      {
        "id": "cell-0-tool-p204",
        "moduleId": "cell-0-tool",
        "shape": "axle",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-console-p205",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p206",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p207",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p208",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p209",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p210",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p211",
        "moduleId": "cell-0-console",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-0-console-p212",
        "moduleId": "cell-0-console",
        "shape": "slope",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p213",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p214",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p215",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p216",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p217",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p218",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p219",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p220",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p221",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p222",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p223",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p224",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p225",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p226",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p227",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p228",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p229",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p230",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p231",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p232",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p233",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p234",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p235",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p236",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p237",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p238",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p239",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p240",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p241",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p242",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p243",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p244",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p245",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p246",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p247",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p248",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p249",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p250",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p251",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p252",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p253",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p254",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p255",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p256",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-drawer-p257",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p258",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p259",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p260",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p261",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p262",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-shuttle-p263",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p264",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p265",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p266",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p267",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p268",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p269",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p270",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p271",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p272",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p273",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p274",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p275",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p276",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p277",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p278",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p279",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p280",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p281",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p282",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p283",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p284",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p285",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p286",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p287",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p288",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p289",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p290",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p291",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p292",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p293",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p294",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p295",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p296",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p297",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p298",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p299",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p300",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p301",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p302",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p303",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p304",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p305",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p306",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p307",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p308",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p309",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p310",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-mount-p311",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p312",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p313",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p314",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p315",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p316",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p317",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p318",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p319",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p320",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p321",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p322",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p323",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p324",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p325",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p326",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p327",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p328",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p329",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p330",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p331",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p332",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p333",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p334",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p335",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p336",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p337",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p338",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p339",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p340",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p341",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p342",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p343",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p344",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p345",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p346",
        "moduleId": "cell-1-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-mount-p347",
        "moduleId": "cell-1-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-mount-p348",
        "moduleId": "cell-1-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-mount-p349",
        "moduleId": "cell-1-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-mount-p350",
        "moduleId": "cell-1-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-mount-p351",
        "moduleId": "cell-1-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-mount-p352",
        "moduleId": "cell-1-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-mount-p353",
        "moduleId": "cell-1-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-carriage-p354",
        "moduleId": "cell-1-carriage",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-carriage-p355",
        "moduleId": "cell-1-carriage",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-carriage-p356",
        "moduleId": "cell-1-carriage",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-carriage-p357",
        "moduleId": "cell-1-carriage",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-carriage-p358",
        "moduleId": "cell-1-carriage",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-carriage-p359",
        "moduleId": "cell-1-carriage",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-cross-feed-p360",
        "moduleId": "cell-1-cross-feed",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-cross-feed-p361",
        "moduleId": "cell-1-cross-feed",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-cross-feed-p362",
        "moduleId": "cell-1-cross-feed",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-cross-feed-p363",
        "moduleId": "cell-1-cross-feed",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-carriage-p364",
        "moduleId": "cell-1-carriage",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-carriage-p365",
        "moduleId": "cell-1-carriage",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-carriage-p366",
        "moduleId": "cell-1-carriage",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-carriage-p367",
        "moduleId": "cell-1-carriage",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-console-p368",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p369",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p370",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p371",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p372",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p373",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p374",
        "moduleId": "cell-1-console",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-1-console-p375",
        "moduleId": "cell-1-console",
        "shape": "slope",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p376",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p377",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p378",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p379",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p380",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p381",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p382",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p383",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p384",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p385",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p386",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p387",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p388",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p389",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p390",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p391",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p392",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p393",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p394",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p395",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p396",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p397",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p398",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p399",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p400",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p401",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p402",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p403",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p404",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p405",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p406",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p407",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p408",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p409",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p410",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p411",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p412",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p413",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p414",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p415",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p416",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p417",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p418",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p419",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-drawer-p420",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p421",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p422",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p423",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p424",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p425",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 颜色识别（h3-exp-d3-arm-1-color）

零件 cell-0-tool-p203 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#d43a32
- B：#f2bf3c
- C：#45a080
- D：#2878b8

```json
{
  "input": {
    "part": {
      "id": "cell-0-tool-p203",
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
    "choiceId": "C"
  }
}
```

### 三维位置（h3-exp-d3-arm-1-position）

模块 cell-0-tool 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,0.2,0]
- B：[-6.5,0.75,0]
- C：[-6.5,1.35,0]
- D：[-4.6,4.0375,1.3]

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
        -6.5,
        0.75,
        0
      ],
      "cell-0-mount": [
        -6.5,
        1.35,
        0
      ],
      "cell-0-shoulder": [
        -8.2,
        2,
        0
      ],
      "cell-0-elbow": [
        -7.449999999999999,
        3.8500000000000005,
        0
      ],
      "cell-0-wrist": [
        -5.7,
        4.7,
        0.7
      ],
      "cell-0-tool": [
        -4.6,
        4.0375,
        1.3
      ],
      "cell-0-console": [
        -6.5,
        1.8775000000000002,
        6
      ],
      "cell-0-magazine": [
        -6.5,
        2.5399999999999996,
        -6
      ],
      "cell-0-drawer": [
        -6.5,
        1.55,
        -6
      ],
      "cell-1-shuttle": [
        6.5,
        0.75,
        0
      ],
      "cell-1-mount": [
        6.5,
        1.5525000000000002,
        0
      ],
      "cell-1-carriage": [
        6.5,
        3.4899999999999993,
        -0.33499999999999996
      ],
      "cell-1-cross-feed": [
        6.5,
        2.95,
        0
      ],
      "cell-1-console": [
        6.5,
        1.8775000000000002,
        6
      ],
      "cell-1-magazine": [
        6.5,
        2.5399999999999996,
        -6
      ],
      "cell-1-drawer": [
        6.5,
        1.55,
        -6
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节类型（h3-exp-d3-arm-1-joint-type）

cell-0-elbow-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：fixed
- B：prismatic
- C：spring
- D：revolute

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
        -1.2000000000000002,
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
    "choiceId": "D"
  }
}
```

### 直接连接（h3-exp-d3-arm-1-parent）

cell-0-tool 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","cell-0-shuttle","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-carriage","cell-1-cross-feed","cell-1-console","cell-1-magazine","cell-1-drawer"]
- C：["cell-0-wrist"]
- D：["cell-0-tool"]

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
          -1.2000000000000002,
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
          0.7499999999999991,
          1.1999999999999993,
          0.7
        ],
        "anchorChild": [
          -1,
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
          1.1000000000000005,
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
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
          -0.25250000000000017,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-carriage-joint",
        "name": "cell-1-carriage interface",
        "parent": "cell-1-mount",
        "child": "cell-1-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999996,
          0
        ],
        "anchorChild": [
          0,
          -1.1899999999999995,
          0.33499999999999996
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
        "id": "cell-1-cross-feed-joint",
        "name": "cell-1-cross-feed interface",
        "parent": "cell-1-carriage",
        "child": "cell-1-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.589999999999999,
          0.33499999999999996
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
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
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 基座识别（h3-exp-d3-arm-1-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["foundation","cell-0-shuttle","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-carriage","cell-1-cross-feed","cell-1-console","cell-1-magazine","cell-1-drawer"]
- B：["cell-0-tool"]
- C：["foundation"]
- D：[]

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
        "id": "cell-0-mount",
        "name": "cell 0 mount",
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
        "id": "cell-0-shoulder",
        "name": "cell 0 shoulder",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -8.2,
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
          -7.449999999999999,
          3.8500000000000005,
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
          -5.7,
          4.7,
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
          -4.6,
          4.0375,
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
        "id": "cell-0-magazine",
        "name": "cell 0 magazine",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -6.5,
          2.5399999999999996,
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
        "id": "cell-1-shuttle",
        "name": "cell 1 shuttle",
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
        "id": "cell-1-mount",
        "name": "cell 1 mount",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          6.5,
          1.5525000000000002,
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
        "id": "cell-1-carriage",
        "name": "cell 1 carriage",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          6.5,
          3.4899999999999993,
          -0.33499999999999996
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-1-cross-feed",
        "name": "cell 1 cross feed",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          6.5,
          2.95,
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
        "id": "cell-1-magazine",
        "name": "cell 1 magazine",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          6.5,
          2.5399999999999996,
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
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 接口计数（h3-exp-d3-arm-1-degree）

cell-0-tool 连接几个声明关节？平行关节分别计数。

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
          -1.2000000000000002,
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
          0.7499999999999991,
          1.1999999999999993,
          0.7
        ],
        "anchorChild": [
          -1,
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
          1.1000000000000005,
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
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
          -0.25250000000000017,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-carriage-joint",
        "name": "cell-1-carriage interface",
        "parent": "cell-1-mount",
        "child": "cell-1-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999996,
          0
        ],
        "anchorChild": [
          0,
          -1.1899999999999995,
          0.33499999999999996
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
        "id": "cell-1-cross-feed-joint",
        "name": "cell-1-cross-feed interface",
        "parent": "cell-1-carriage",
        "child": "cell-1-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.589999999999999,
          0.33499999999999996
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
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
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 局部改色（h3-exp-d3-arm-1-recolor）

仅将 cell-0-tool-p203 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-tool-p204","color":"#e8792e"}
- B：{"id":"cell-0-tool-p203","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"cell-0-tool-p203","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "cell-0-tool-p203",
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

### 补装部件（h3-exp-d3-arm-1-add）

模块 cell-0-tool 缺失零件 cell-0-tool-p203。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-tool-p203","moduleId":"foundation","shape":"arch","position":[0,0.2625000000000002,0],"size":[0.65,0.65,0.65],"color":"#45a080","rotation":[0,0,0,1]}
- B：{"id":"cell-0-tool-p203","moduleId":"cell-0-tool","shape":"arch","position":[0,0.2625000000000002,0],"size":[3,3,3],"color":"#45a080","rotation":[0,0,0,1]}
- C：{"id":"cell-0-tool-p203","moduleId":"cell-0-tool","shape":"arch","position":[0,0.2625000000000002,0],"size":[0.65,0.65,0.65],"color":"#000000","rotation":[0,0,0,1]}
- D：{"id":"cell-0-tool-p203","moduleId":"cell-0-tool","shape":"arch","position":[0,0.2625000000000002,0],"size":[0.65,0.65,0.65],"color":"#45a080","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "cell-0-tool-p203",
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
      "cell-0-shuttle-p118",
      "cell-0-shuttle-p119",
      "cell-0-shuttle-p120",
      "cell-0-shuttle-p121",
      "cell-0-shuttle-p122",
      "cell-0-shuttle-p123",
      "cell-0-shuttle-p124",
      "cell-0-shuttle-p125",
      "cell-0-shuttle-p126",
      "cell-0-shuttle-p127",
      "cell-0-shuttle-p128",
      "cell-0-shuttle-p129",
      "cell-0-shuttle-p130",
      "cell-0-shuttle-p131",
      "cell-0-shuttle-p132",
      "cell-0-shuttle-p133",
      "cell-0-shuttle-p134",
      "cell-0-shuttle-p135",
      "cell-0-shuttle-p136",
      "cell-0-shuttle-p137",
      "cell-0-shuttle-p138",
      "cell-0-shuttle-p139",
      "cell-0-shuttle-p140",
      "cell-0-shuttle-p141",
      "cell-0-shuttle-p142",
      "cell-0-shuttle-p143",
      "cell-0-shuttle-p144",
      "cell-0-shuttle-p145",
      "cell-0-shuttle-p146",
      "cell-0-shuttle-p147",
      "cell-0-shuttle-p148",
      "cell-0-shuttle-p149",
      "cell-0-shuttle-p150",
      "cell-0-shuttle-p151",
      "cell-0-shuttle-p152",
      "cell-0-shuttle-p153",
      "cell-0-shuttle-p154",
      "cell-0-shuttle-p155",
      "cell-0-shuttle-p156",
      "cell-0-shuttle-p157",
      "cell-0-shuttle-p158",
      "cell-0-shuttle-p159",
      "cell-0-shuttle-p160",
      "cell-0-shuttle-p161",
      "cell-0-shuttle-p162",
      "cell-0-shuttle-p163",
      "cell-0-shuttle-p164",
      "cell-0-shuttle-p165",
      "cell-0-mount-p166",
      "cell-0-mount-p167",
      "cell-0-mount-p168",
      "cell-0-mount-p169",
      "cell-0-mount-p170",
      "cell-0-mount-p171",
      "cell-0-mount-p172",
      "cell-0-mount-p173",
      "cell-0-mount-p174",
      "cell-0-mount-p175",
      "cell-0-mount-p176",
      "cell-0-mount-p177",
      "cell-0-mount-p178",
      "cell-0-mount-p179",
      "cell-0-mount-p180",
      "cell-0-mount-p181",
      "cell-0-mount-p182",
      "cell-0-mount-p183",
      "cell-0-mount-p184",
      "cell-0-mount-p185",
      "cell-0-mount-p186",
      "cell-0-mount-p187",
      "cell-0-mount-p188",
      "cell-0-mount-p189",
      "cell-0-mount-p190",
      "cell-0-mount-p191",
      "cell-0-mount-p192",
      "cell-0-mount-p193",
      "cell-0-mount-p194",
      "cell-0-mount-p195",
      "cell-0-shoulder-p196",
      "cell-0-elbow-p197",
      "cell-0-elbow-p198",
      "cell-0-elbow-p199",
      "cell-0-wrist-p200",
      "cell-0-wrist-p201",
      "cell-0-wrist-p202",
      "cell-0-tool-p204",
      "cell-0-console-p205",
      "cell-0-console-p206",
      "cell-0-console-p207",
      "cell-0-console-p208",
      "cell-0-console-p209",
      "cell-0-console-p210",
      "cell-0-console-p211",
      "cell-0-console-p212",
      "cell-0-magazine-p213",
      "cell-0-magazine-p214",
      "cell-0-magazine-p215",
      "cell-0-magazine-p216",
      "cell-0-magazine-p217",
      "cell-0-magazine-p218",
      "cell-0-magazine-p219",
      "cell-0-magazine-p220",
      "cell-0-magazine-p221",
      "cell-0-magazine-p222",
      "cell-0-magazine-p223",
      "cell-0-magazine-p224",
      "cell-0-magazine-p225",
      "cell-0-magazine-p226",
      "cell-0-magazine-p227",
      "cell-0-magazine-p228",
      "cell-0-magazine-p229",
      "cell-0-magazine-p230",
      "cell-0-magazine-p231",
      "cell-0-magazine-p232",
      "cell-0-magazine-p233",
      "cell-0-magazine-p234",
      "cell-0-magazine-p235",
      "cell-0-magazine-p236",
      "cell-0-magazine-p237",
      "cell-0-magazine-p238",
      "cell-0-magazine-p239",
      "cell-0-magazine-p240",
      "cell-0-magazine-p241",
      "cell-0-magazine-p242",
      "cell-0-magazine-p243",
      "cell-0-magazine-p244",
      "cell-0-magazine-p245",
      "cell-0-magazine-p246",
      "cell-0-magazine-p247",
      "cell-0-magazine-p248",
      "cell-0-magazine-p249",
      "cell-0-magazine-p250",
      "cell-0-magazine-p251",
      "cell-0-magazine-p252",
      "cell-0-magazine-p253",
      "cell-0-magazine-p254",
      "cell-0-magazine-p255",
      "cell-0-magazine-p256",
      "cell-0-drawer-p257",
      "cell-0-drawer-p258",
      "cell-0-drawer-p259",
      "cell-0-drawer-p260",
      "cell-0-drawer-p261",
      "cell-0-drawer-p262",
      "cell-1-shuttle-p263",
      "cell-1-shuttle-p264",
      "cell-1-shuttle-p265",
      "cell-1-shuttle-p266",
      "cell-1-shuttle-p267",
      "cell-1-shuttle-p268",
      "cell-1-shuttle-p269",
      "cell-1-shuttle-p270",
      "cell-1-shuttle-p271",
      "cell-1-shuttle-p272",
      "cell-1-shuttle-p273",
      "cell-1-shuttle-p274",
      "cell-1-shuttle-p275",
      "cell-1-shuttle-p276",
      "cell-1-shuttle-p277",
      "cell-1-shuttle-p278",
      "cell-1-shuttle-p279",
      "cell-1-shuttle-p280",
      "cell-1-shuttle-p281",
      "cell-1-shuttle-p282",
      "cell-1-shuttle-p283",
      "cell-1-shuttle-p284",
      "cell-1-shuttle-p285",
      "cell-1-shuttle-p286",
      "cell-1-shuttle-p287",
      "cell-1-shuttle-p288",
      "cell-1-shuttle-p289",
      "cell-1-shuttle-p290",
      "cell-1-shuttle-p291",
      "cell-1-shuttle-p292",
      "cell-1-shuttle-p293",
      "cell-1-shuttle-p294",
      "cell-1-shuttle-p295",
      "cell-1-shuttle-p296",
      "cell-1-shuttle-p297",
      "cell-1-shuttle-p298",
      "cell-1-shuttle-p299",
      "cell-1-shuttle-p300",
      "cell-1-shuttle-p301",
      "cell-1-shuttle-p302",
      "cell-1-shuttle-p303",
      "cell-1-shuttle-p304",
      "cell-1-shuttle-p305",
      "cell-1-shuttle-p306",
      "cell-1-shuttle-p307",
      "cell-1-shuttle-p308",
      "cell-1-shuttle-p309",
      "cell-1-shuttle-p310",
      "cell-1-mount-p311",
      "cell-1-mount-p312",
      "cell-1-mount-p313",
      "cell-1-mount-p314",
      "cell-1-mount-p315",
      "cell-1-mount-p316",
      "cell-1-mount-p317",
      "cell-1-mount-p318",
      "cell-1-mount-p319",
      "cell-1-mount-p320",
      "cell-1-mount-p321",
      "cell-1-mount-p322",
      "cell-1-mount-p323",
      "cell-1-mount-p324",
      "cell-1-mount-p325",
      "cell-1-mount-p326",
      "cell-1-mount-p327",
      "cell-1-mount-p328",
      "cell-1-mount-p329",
      "cell-1-mount-p330",
      "cell-1-mount-p331",
      "cell-1-mount-p332",
      "cell-1-mount-p333",
      "cell-1-mount-p334",
      "cell-1-mount-p335",
      "cell-1-mount-p336",
      "cell-1-mount-p337",
      "cell-1-mount-p338",
      "cell-1-mount-p339",
      "cell-1-mount-p340",
      "cell-1-mount-p341",
      "cell-1-mount-p342",
      "cell-1-mount-p343",
      "cell-1-mount-p344",
      "cell-1-mount-p345",
      "cell-1-mount-p346",
      "cell-1-mount-p347",
      "cell-1-mount-p348",
      "cell-1-mount-p349",
      "cell-1-mount-p350",
      "cell-1-mount-p351",
      "cell-1-mount-p352",
      "cell-1-mount-p353",
      "cell-1-carriage-p354",
      "cell-1-carriage-p355",
      "cell-1-carriage-p356",
      "cell-1-carriage-p357",
      "cell-1-carriage-p358",
      "cell-1-carriage-p359",
      "cell-1-cross-feed-p360",
      "cell-1-cross-feed-p361",
      "cell-1-cross-feed-p362",
      "cell-1-cross-feed-p363",
      "cell-1-carriage-p364",
      "cell-1-carriage-p365",
      "cell-1-carriage-p366",
      "cell-1-carriage-p367",
      "cell-1-console-p368",
      "cell-1-console-p369",
      "cell-1-console-p370",
      "cell-1-console-p371",
      "cell-1-console-p372",
      "cell-1-console-p373",
      "cell-1-console-p374",
      "cell-1-console-p375",
      "cell-1-magazine-p376",
      "cell-1-magazine-p377",
      "cell-1-magazine-p378",
      "cell-1-magazine-p379",
      "cell-1-magazine-p380",
      "cell-1-magazine-p381",
      "cell-1-magazine-p382",
      "cell-1-magazine-p383",
      "cell-1-magazine-p384",
      "cell-1-magazine-p385",
      "cell-1-magazine-p386",
      "cell-1-magazine-p387",
      "cell-1-magazine-p388",
      "cell-1-magazine-p389",
      "cell-1-magazine-p390",
      "cell-1-magazine-p391",
      "cell-1-magazine-p392",
      "cell-1-magazine-p393",
      "cell-1-magazine-p394",
      "cell-1-magazine-p395",
      "cell-1-magazine-p396",
      "cell-1-magazine-p397",
      "cell-1-magazine-p398",
      "cell-1-magazine-p399",
      "cell-1-magazine-p400",
      "cell-1-magazine-p401",
      "cell-1-magazine-p402",
      "cell-1-magazine-p403",
      "cell-1-magazine-p404",
      "cell-1-magazine-p405",
      "cell-1-magazine-p406",
      "cell-1-magazine-p407",
      "cell-1-magazine-p408",
      "cell-1-magazine-p409",
      "cell-1-magazine-p410",
      "cell-1-magazine-p411",
      "cell-1-magazine-p412",
      "cell-1-magazine-p413",
      "cell-1-magazine-p414",
      "cell-1-magazine-p415",
      "cell-1-magazine-p416",
      "cell-1-magazine-p417",
      "cell-1-magazine-p418",
      "cell-1-magazine-p419",
      "cell-1-drawer-p420",
      "cell-1-drawer-p421",
      "cell-1-drawer-p422",
      "cell-1-drawer-p423",
      "cell-1-drawer-p424",
      "cell-1-drawer-p425"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 安全拆除（h3-exp-d3-arm-1-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["cell-0-console","cell-0-drawer","cell-0-tool","cell-1-console","cell-1-cross-feed","cell-1-drawer"]
- B：["foundation"]
- C：[]
- D：["foundation","cell-0-shuttle","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-carriage","cell-1-cross-feed","cell-1-console","cell-1-magazine","cell-1-drawer"]

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
          -1.2000000000000002,
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
          0.7499999999999991,
          1.1999999999999993,
          0.7
        ],
        "anchorChild": [
          -1,
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
          1.1000000000000005,
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
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
          -0.25250000000000017,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-carriage-joint",
        "name": "cell-1-carriage interface",
        "parent": "cell-1-mount",
        "child": "cell-1-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999996,
          0
        ],
        "anchorChild": [
          0,
          -1.1899999999999995,
          0.33499999999999996
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
        "id": "cell-1-cross-feed-joint",
        "name": "cell-1-cross-feed interface",
        "parent": "cell-1-carriage",
        "child": "cell-1-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.589999999999999,
          0.33499999999999996
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
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
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
      "cell-1-carriage",
      "cell-1-cross-feed",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 替换选择（h3-exp-d3-arm-1-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-0
- B：stock-1
- C：stock-3
- D：stock-2

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 6,
        "stiffness": 9,
        "mass": 1.9
      },
      {
        "id": "stock-1",
        "cost": 3,
        "stiffness": 6,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 11,
        "mass": 0.8
      },
      {
        "id": "stock-3",
        "cost": 4,
        "stiffness": 5,
        "mass": 1.8
      }
    ],
    "maxCost": 8
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-exp-d3-arm-1-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[3,0,-2]
- B：[0,0,0]
- C：[0,2,0]
- D：[-3,0,2]

```json
{
  "input": {
    "delta": [
      3,
      0,
      -2
    ],
    "target": "cell-0-tool"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 姿态纠偏（h3-exp-d3-arm-1-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：-135
- B：0
- C：90
- D：135

```json
{
  "input": {
    "module": "cell-0-tool",
    "currentYaw": 315,
    "targetYaw": 90
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 下一步放置（h3-exp-d3-arm-1-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","cell-0-shuttle","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool","cell-0-console","cell-0-magazine"]
- C：["cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-carriage","cell-1-cross-feed","cell-1-console","cell-1-magazine","cell-1-drawer"]
- D：["cell-0-drawer","cell-1-console","cell-1-magazine","cell-1-shuttle"]

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
      "cell-0-magazine"
    ],
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
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
          -1.2000000000000002,
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
          0.7499999999999991,
          1.1999999999999993,
          0.7
        ],
        "anchorChild": [
          -1,
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
          1.1000000000000005,
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
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
          -0.25250000000000017,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-carriage-joint",
        "name": "cell-1-carriage interface",
        "parent": "cell-1-mount",
        "child": "cell-1-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999996,
          0
        ],
        "anchorChild": [
          0,
          -1.1899999999999995,
          0.33499999999999996
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
        "id": "cell-1-cross-feed-joint",
        "name": "cell-1-cross-feed interface",
        "parent": "cell-1-carriage",
        "child": "cell-1-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.589999999999999,
          0.33499999999999996
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
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
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
      "cell-1-carriage",
      "cell-1-cross-feed",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 库存核算（h3-exp-d3-arm-1-inventory）

备件库有 4 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：3
- B：1
- C：5
- D：2

```json
{
  "input": {
    "available": 4,
    "required": 2
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 子装配边界（h3-exp-d3-arm-1-boundary）

隔离 cell-0-tool 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["cell-0-tool-joint"]
- B：[]
- C：["cell-0-shuttle-joint","cell-0-mount-joint","cell-0-shoulder-joint","cell-0-elbow-joint","cell-0-wrist-joint","cell-0-tool-joint","cell-0-console-joint","cell-0-magazine-joint","cell-0-drawer-joint","cell-1-shuttle-joint","cell-1-mount-joint","cell-1-carriage-joint","cell-1-cross-feed-joint","cell-1-console-joint","cell-1-magazine-joint","cell-1-drawer-joint"]
- D：["cell-0-elbow-joint"]

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
          -1.2000000000000002,
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
          0.7499999999999991,
          1.1999999999999993,
          0.7
        ],
        "anchorChild": [
          -1,
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
          1.1000000000000005,
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
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
          -0.25250000000000017,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-carriage-joint",
        "name": "cell-1-carriage interface",
        "parent": "cell-1-mount",
        "child": "cell-1-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999996,
          0
        ],
        "anchorChild": [
          0,
          -1.1899999999999995,
          0.33499999999999996
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
        "id": "cell-1-cross-feed-joint",
        "name": "cell-1-cross-feed interface",
        "parent": "cell-1-carriage",
        "child": "cell-1-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.589999999999999,
          0.33499999999999996
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
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
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
    ],
    "target": "cell-0-tool"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 最小干预（h3-exp-d3-arm-1-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：2
- B：0
- C：1

```json
{
  "input": {
    "module": "cell-0-tool"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 全过程依赖（h3-exp-d3-arm-1-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：1
- B：16
- C：0
- D：-1

```json
{
  "input": {
    "order": [
      "cell-0-magazine",
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool",
      "cell-0-console",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-carriage",
      "cell-1-cross-feed",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "joints": [
      {
        "id": "cell-0-shuttle-joint",
        "name": "cell-0-shuttle interface",
        "parent": "foundation",
        "child": "cell-0-shuttle",
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
          -1.2000000000000002,
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
          0.7499999999999991,
          1.1999999999999993,
          0.7
        ],
        "anchorChild": [
          -1,
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
          1.1000000000000005,
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
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
          -0.25250000000000017,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-carriage-joint",
        "name": "cell-1-carriage interface",
        "parent": "cell-1-mount",
        "child": "cell-1-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999996,
          0
        ],
        "anchorChild": [
          0,
          -1.1899999999999995,
          0.33499999999999996
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
        "id": "cell-1-cross-feed-joint",
        "name": "cell-1-cross-feed interface",
        "parent": "cell-1-carriage",
        "child": "cell-1-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.589999999999999,
          0.33499999999999996
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
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
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 连续维修路径（h3-exp-d3-arm-1-access）

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
          14.48,
          4.0375,
          1.3
        ],
        "end": [
          -4.6,
          4.0375,
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
        "id": "path-1",
        "start": [
          -4.6,
          9.191578753454902,
          1.3
        ],
        "end": [
          -4.6,
          4.0375,
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
          -4.6,
          4.0375,
          10.98
        ],
        "end": [
          -4.6,
          4.0375,
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
      "B",
      "C"
    ]
  }
}
```

### 支撑反事实（h3-exp-d3-arm-1-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["foundation","cell-0-shuttle","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-carriage","cell-1-cross-feed","cell-1-console","cell-1-magazine","cell-1-drawer"]
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
          -1.2000000000000002,
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
          0.7499999999999991,
          1.1999999999999993,
          0.7
        ],
        "anchorChild": [
          -1,
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
          1.1000000000000005,
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
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
          -0.25250000000000017,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-carriage-joint",
        "name": "cell-1-carriage interface",
        "parent": "cell-1-mount",
        "child": "cell-1-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999996,
          0
        ],
        "anchorChild": [
          0,
          -1.1899999999999995,
          0.33499999999999996
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
        "id": "cell-1-cross-feed-joint",
        "name": "cell-1-cross-feed interface",
        "parent": "cell-1-carriage",
        "child": "cell-1-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.589999999999999,
          0.33499999999999996
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
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
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
      "cell-1-carriage",
      "cell-1-cross-feed",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-exp-d3-arm-1-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：1.0145
- C：0.0145
- D：0.2145

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.014517778137826379
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0025059783073411324
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.002866858025582689
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0014175403137376551
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0005556553042047405
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00017557598073956863
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00006056969922437509
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00004578878313803549
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0000014745374771181322
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000014745374771181322
      },
      {
        "time": 1,
        "displacement": 0.0000014745374771181322
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.010744740374128698,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-exp-d3-arm-1-kinematic）

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

### 约束故障诊断（h3-exp-d3-arm-1-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：cell-0-tool-joint
- B：cell-0-shuttle-joint
- C：cell-0-mount-joint
- D：cell-0-shoulder-joint

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
          -1.2000000000000002,
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
          0.7499999999999991,
          1.1999999999999993,
          0.7
        ],
        "anchorChild": [
          -1,
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
          1.1000000000000005,
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
        "id": "cell-0-magazine-joint",
        "name": "cell-0-magazine interface",
        "parent": "foundation",
        "child": "cell-0-magazine",
        "type": "fixed",
        "anchorParent": [
          -6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
          -0.25250000000000017,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-carriage-joint",
        "name": "cell-1-carriage interface",
        "parent": "cell-1-mount",
        "child": "cell-1-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999996,
          0
        ],
        "anchorChild": [
          0,
          -1.1899999999999995,
          0.33499999999999996
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
        "id": "cell-1-cross-feed-joint",
        "name": "cell-1-cross-feed interface",
        "parent": "cell-1-carriage",
        "child": "cell-1-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.589999999999999,
          0.33499999999999996
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
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
        "id": "cell-1-console-joint",
        "name": "cell-1-console interface",
        "parent": "foundation",
        "child": "cell-1-console",
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
        "id": "cell-1-magazine-joint",
        "name": "cell-1-magazine interface",
        "parent": "foundation",
        "child": "cell-1-magazine",
        "type": "fixed",
        "anchorParent": [
          6.5,
          0.6,
          -6
        ],
        "anchorChild": [
          0,
          -1.7399999999999995,
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
          -1.0399999999999996,
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
    ]
  },
  "answer": {
    "choiceIds": [
      "A"
    ]
  }
}
```

### 主动检查收益（h3-exp-d3-arm-1-information-gain）

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

### 不确定性与弃答（h3-exp-d3-arm-1-abstention）

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
        "action": "continue"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 观测后信念更新（h3-exp-d3-arm-1-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.25
- B：0.3333333333333333
- C：0.5
- D：0

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
      "positive",
      "positive",
      "positive",
      "negative"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 多目标工程权衡（h3-exp-d3-arm-1-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

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
        "cost": 6,
        "stiffness": 9,
        "mass": 1.9
      },
      {
        "id": "stock-1",
        "cost": 3,
        "stiffness": 6,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 11,
        "mass": 0.8
      },
      {
        "id": "stock-3",
        "cost": 4,
        "stiffness": 5,
        "mass": 1.8
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "B",
      "C"
    ]
  }
}
```

### 依赖装配（h3-exp-d3-arm-1-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
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
        "id": "place:cell-1-carriage",
        "label": "安装 cell-1-carriage",
        "requires": [
          "present:cell-1-mount"
        ],
        "forbids": [
          "present:cell-1-carriage"
        ],
        "adds": [
          "present:cell-1-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-carriage",
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
        "id": "place:cell-1-cross-feed",
        "label": "安装 cell-1-cross-feed",
        "requires": [
          "present:cell-1-carriage"
        ],
        "forbids": [
          "present:cell-1-cross-feed"
        ],
        "adds": [
          "present:cell-1-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-cross-feed",
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
      "present:cell-1-carriage",
      "present:cell-1-cross-feed",
      "present:cell-1-console",
      "present:cell-1-magazine",
      "present:cell-1-drawer"
    ],
    "budget": 17,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:cell-1-magazine",
      "place:cell-1-drawer",
      "place:cell-1-console",
      "place:cell-0-shuttle",
      "place:cell-0-mount",
      "place:cell-0-shoulder",
      "place:cell-0-elbow",
      "place:cell-0-wrist",
      "place:cell-0-tool",
      "place:cell-1-shuttle",
      "place:cell-0-magazine",
      "place:cell-0-drawer",
      "place:cell-1-mount",
      "place:cell-1-carriage",
      "place:cell-1-cross-feed",
      "place:cell-0-console"
    ]
  }
}
```

### 依赖拆解（h3-exp-d3-arm-1-disassembly）

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
      "present:cell-1-carriage",
      "present:cell-1-cross-feed",
      "present:cell-1-console",
      "present:cell-1-magazine",
      "present:cell-1-drawer"
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
      "cell-1-carriage",
      "cell-1-cross-feed",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "actions": [
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
        "id": "remove:cell-1-carriage",
        "label": "拆除 cell-1-carriage",
        "requires": [
          "present:cell-1-carriage"
        ],
        "forbids": [
          "present:cell-1-cross-feed"
        ],
        "adds": [
          "removed:cell-1-carriage"
        ],
        "deletes": [
          "present:cell-1-carriage"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-carriage",
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
          "present:cell-1-magazine"
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
        "id": "remove:cell-1-mount",
        "label": "拆除 cell-1-mount",
        "requires": [
          "present:cell-1-mount"
        ],
        "forbids": [
          "present:cell-1-carriage"
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
        "id": "remove:cell-1-cross-feed",
        "label": "拆除 cell-1-cross-feed",
        "requires": [
          "present:cell-1-cross-feed"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-1-cross-feed"
        ],
        "deletes": [
          "present:cell-1-cross-feed"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-cross-feed",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:cell-1-drawer",
      "removed:cell-1-magazine",
      "removed:cell-1-console",
      "removed:cell-1-cross-feed",
      "removed:cell-1-carriage",
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
    "budget": 17,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:cell-1-console",
      "remove:cell-0-console",
      "remove:cell-0-tool",
      "remove:cell-0-wrist",
      "remove:cell-0-elbow",
      "remove:cell-0-drawer",
      "remove:cell-0-magazine",
      "remove:cell-1-drawer",
      "remove:cell-1-magazine",
      "remove:cell-0-shoulder",
      "remove:cell-0-mount",
      "remove:cell-0-shuttle",
      "remove:cell-1-cross-feed",
      "remove:cell-1-carriage",
      "remove:cell-1-mount",
      "remove:cell-1-shuttle",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-exp-d3-arm-1-service-repair）

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
      "cell-1-carriage",
      "cell-1-cross-feed",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "actions": [
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

### 复合编辑验证（h3-exp-d3-arm-1-compound-edit）

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
      "cell-1-carriage",
      "cell-1-cross-feed",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "actions": [
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

### 跨区域联合维修（h3-exp-d3-arm-1-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-1-console",
      "closed:cell-1-console",
      "fault:cell-1-magazine",
      "closed:cell-1-magazine",
      "fault:cell-1-drawer",
      "closed:cell-1-drawer"
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
      "cell-1-carriage",
      "cell-1-cross-feed",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "actions": [
      {
        "id": "remove:cell-1-console",
        "label": "remove cell-1-console",
        "requires": [
          "done:open:cell-1-console"
        ],
        "forbids": [
          "done:remove:cell-1-console"
        ],
        "adds": [
          "done:remove:cell-1-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console",
          "visible": false
        }
      },
      {
        "id": "replace:cell-1-console",
        "label": "replace cell-1-console",
        "requires": [
          "done:remove:cell-1-console"
        ],
        "forbids": [
          "done:replace:cell-1-console"
        ],
        "adds": [
          "done:replace:cell-1-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console",
          "visible": true
        }
      },
      {
        "id": "support:cell-1-drawer",
        "label": "support cell-1-drawer",
        "requires": [
          "fault:cell-1-drawer"
        ],
        "forbids": [
          "done:support:cell-1-drawer"
        ],
        "adds": [
          "done:support:cell-1-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer"
        }
      },
      {
        "id": "release:cell-1-console",
        "label": "release cell-1-console",
        "requires": [
          "done:close:cell-1-console"
        ],
        "forbids": [
          "done:release:cell-1-console"
        ],
        "adds": [
          "done:release:cell-1-console",
          "repaired:cell-1-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console"
        }
      },
      {
        "id": "release:cell-1-drawer",
        "label": "release cell-1-drawer",
        "requires": [
          "done:close:cell-1-drawer"
        ],
        "forbids": [
          "done:release:cell-1-drawer"
        ],
        "adds": [
          "done:release:cell-1-drawer",
          "repaired:cell-1-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer"
        }
      },
      {
        "id": "verify:cell-1-console",
        "label": "verify cell-1-console",
        "requires": [
          "done:replace:cell-1-console"
        ],
        "forbids": [
          "done:verify:cell-1-console"
        ],
        "adds": [
          "done:verify:cell-1-console"
        ],
        "deletes": [
          "fault:cell-1-console"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console"
        }
      },
      {
        "id": "release:cell-1-magazine",
        "label": "release cell-1-magazine",
        "requires": [
          "done:close:cell-1-magazine"
        ],
        "forbids": [
          "done:release:cell-1-magazine"
        ],
        "adds": [
          "done:release:cell-1-magazine",
          "repaired:cell-1-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine"
        }
      },
      {
        "id": "remove:cell-1-magazine",
        "label": "remove cell-1-magazine",
        "requires": [
          "done:open:cell-1-magazine"
        ],
        "forbids": [
          "done:remove:cell-1-magazine"
        ],
        "adds": [
          "done:remove:cell-1-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine",
          "visible": false
        }
      },
      {
        "id": "close:cell-1-magazine",
        "label": "close cell-1-magazine",
        "requires": [
          "done:verify:cell-1-magazine"
        ],
        "forbids": [
          "done:close:cell-1-magazine"
        ],
        "adds": [
          "done:close:cell-1-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine"
        }
      },
      {
        "id": "support:cell-1-magazine",
        "label": "support cell-1-magazine",
        "requires": [
          "fault:cell-1-magazine"
        ],
        "forbids": [
          "done:support:cell-1-magazine"
        ],
        "adds": [
          "done:support:cell-1-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine"
        }
      },
      {
        "id": "open:cell-1-drawer",
        "label": "open cell-1-drawer",
        "requires": [
          "done:support:cell-1-drawer"
        ],
        "forbids": [
          "done:open:cell-1-drawer"
        ],
        "adds": [
          "done:open:cell-1-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer"
        }
      },
      {
        "id": "verify:cell-1-magazine",
        "label": "verify cell-1-magazine",
        "requires": [
          "done:replace:cell-1-magazine"
        ],
        "forbids": [
          "done:verify:cell-1-magazine"
        ],
        "adds": [
          "done:verify:cell-1-magazine"
        ],
        "deletes": [
          "fault:cell-1-magazine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine"
        }
      },
      {
        "id": "open:cell-1-magazine",
        "label": "open cell-1-magazine",
        "requires": [
          "done:support:cell-1-magazine"
        ],
        "forbids": [
          "done:open:cell-1-magazine"
        ],
        "adds": [
          "done:open:cell-1-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine"
        }
      },
      {
        "id": "close:cell-1-drawer",
        "label": "close cell-1-drawer",
        "requires": [
          "done:verify:cell-1-drawer"
        ],
        "forbids": [
          "done:close:cell-1-drawer"
        ],
        "adds": [
          "done:close:cell-1-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer"
        }
      },
      {
        "id": "replace:cell-1-drawer",
        "label": "replace cell-1-drawer",
        "requires": [
          "done:remove:cell-1-drawer"
        ],
        "forbids": [
          "done:replace:cell-1-drawer"
        ],
        "adds": [
          "done:replace:cell-1-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer",
          "visible": true
        }
      },
      {
        "id": "verify:cell-1-drawer",
        "label": "verify cell-1-drawer",
        "requires": [
          "done:replace:cell-1-drawer"
        ],
        "forbids": [
          "done:verify:cell-1-drawer"
        ],
        "adds": [
          "done:verify:cell-1-drawer"
        ],
        "deletes": [
          "fault:cell-1-drawer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer"
        }
      },
      {
        "id": "remove:cell-1-drawer",
        "label": "remove cell-1-drawer",
        "requires": [
          "done:open:cell-1-drawer"
        ],
        "forbids": [
          "done:remove:cell-1-drawer"
        ],
        "adds": [
          "done:remove:cell-1-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer",
          "visible": false
        }
      },
      {
        "id": "close:cell-1-console",
        "label": "close cell-1-console",
        "requires": [
          "done:verify:cell-1-console"
        ],
        "forbids": [
          "done:close:cell-1-console"
        ],
        "adds": [
          "done:close:cell-1-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console"
        }
      },
      {
        "id": "open:cell-1-console",
        "label": "open cell-1-console",
        "requires": [
          "done:support:cell-1-console"
        ],
        "forbids": [
          "done:open:cell-1-console"
        ],
        "adds": [
          "done:open:cell-1-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console"
        }
      },
      {
        "id": "support:cell-1-console",
        "label": "support cell-1-console",
        "requires": [
          "fault:cell-1-console"
        ],
        "forbids": [
          "done:support:cell-1-console"
        ],
        "adds": [
          "done:support:cell-1-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console"
        }
      },
      {
        "id": "replace:cell-1-magazine",
        "label": "replace cell-1-magazine",
        "requires": [
          "done:remove:cell-1-magazine"
        ],
        "forbids": [
          "done:replace:cell-1-magazine"
        ],
        "adds": [
          "done:replace:cell-1-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-1-console",
      "repaired:cell-1-magazine",
      "repaired:cell-1-drawer"
    ],
    "budget": 21,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-1-drawer",
      "support:cell-1-magazine",
      "open:cell-1-drawer",
      "open:cell-1-magazine",
      "remove:cell-1-magazine",
      "remove:cell-1-drawer",
      "replace:cell-1-drawer",
      "verify:cell-1-drawer",
      "close:cell-1-drawer",
      "release:cell-1-drawer",
      "support:cell-1-console",
      "open:cell-1-console",
      "remove:cell-1-console",
      "replace:cell-1-console",
      "verify:cell-1-console",
      "close:cell-1-console",
      "release:cell-1-console",
      "replace:cell-1-magazine",
      "verify:cell-1-magazine",
      "close:cell-1-magazine",
      "release:cell-1-magazine"
    ]
  }
}
```

### 多工位资源调度（h3-exp-d3-arm-1-scheduling）

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
      }
    ],
    "deadline": 9
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
      "job-7": 3
    }
  }
}
```

### 检查后条件策略（h3-exp-d3-arm-1-policy）

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

### 局部坐标变换（h3-exp-d3-arm-1-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[-3.6,4.3,1.3]
- B：[-3.5999999999999996,5.3,3.3]
- C：[-4.6,4.3,2.3]
- D：[1,0.2625,0]

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
      0.7071067811865476,
      0,
      -0.7071067811865475
    ],
    "translation": [
      -4.6,
      4.0375,
      1.3
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-exp-d3-arm-1-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[4,-5]
- B：[9,4]
- C：[4,5]
- D：[0,0]

```json
{
  "input": {
    "view": "top",
    "point": [
      4,
      9,
      -5
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 空间相对关系（h3-exp-d3-arm-1-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：equal
- B：less
- C：greater

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
      "id": "cell-1-drawer",
      "position": [
        6.5,
        1.55,
        -6
      ]
    },
    "axis": "z"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 约束自由度（h3-exp-d3-arm-1-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：6
- B：0
- C：1
- D：3

```json
{
  "input": {
    "joint": {
      "id": "cell-0-magazine-joint",
      "name": "cell-0-magazine interface",
      "parent": "foundation",
      "child": "cell-0-magazine",
      "type": "fixed",
      "anchorParent": [
        -6.5,
        0.6,
        -6
      ],
      "anchorChild": [
        0,
        -1.7399999999999995,
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
    "choiceId": "B"
  }
}
```

### 维修间隙预算（h3-exp-d3-arm-1-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "cell-0-tool",
    "aperture": 0.81,
    "toolWidth": 0.55,
    "eachSideMargin": 0.1
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-exp-d3-arm-1-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,9]
- B：[0,0,0]
- C：[0,-3,0]
- D：[0,0,-9]

```json
{
  "input": {
    "module": "cell-0-tool",
    "lever": [
      3,
      3,
      0
    ],
    "force": [
      0,
      -3,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 非均匀先验更新（h3-exp-d3-arm-1-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0
- C：1
- D：0.75

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
      2,
      6,
      4
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

### 风险最小决策（h3-exp-d3-arm-1-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.8,
    "repairCost": 7,
    "failureLoss": 13,
    "module": "cell-0-tool"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-exp-d3-arm-1-trace-threshold）

实际采样轨迹中是否有位移严格超过给定阈值？只评价采样点。

能力：轨迹阈值判定；形式：single-choice；证据：Rapier。

- A：within
- B：exceeded

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.014517778137826379
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0025059783073411324
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.002866858025582689
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0014175403137376551
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0005556553042047405
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00017557598073956863
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00006056969922437509
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00004578878313803549
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0000014745374771181322
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000014745374771181322
      },
      {
        "time": 1,
        "displacement": 0.0000014745374771181322
      }
    ],
    "threshold": 0.017421333765391653
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-exp-d3-arm-1-guarded-repair）

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
      "cell-1-carriage",
      "cell-1-cross-feed",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
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

### 失败状态回退（h3-exp-d3-arm-1-rollback）

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
      "cell-1-carriage",
      "cell-1-cross-feed",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
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

### 共享工具协同维修（h3-exp-d3-arm-1-resource-repair）

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
        "id": "release:cell-1-drawer",
        "label": "release cell-1-drawer",
        "requires": [
          "done:relock:cell-1-drawer"
        ],
        "forbids": [
          "done:release:cell-1-drawer"
        ],
        "adds": [
          "done:release:cell-1-drawer",
          "ready:cell-1-drawer",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer"
        }
      },
      {
        "id": "relock:cell-1-drawer",
        "label": "relock cell-1-drawer",
        "requires": [
          "done:verify:cell-1-drawer"
        ],
        "forbids": [
          "done:relock:cell-1-drawer"
        ],
        "adds": [
          "done:relock:cell-1-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer"
        }
      },
      {
        "id": "verify:cell-1-drawer",
        "label": "verify cell-1-drawer",
        "requires": [
          "done:replace:cell-1-drawer"
        ],
        "forbids": [
          "done:verify:cell-1-drawer"
        ],
        "adds": [
          "done:verify:cell-1-drawer"
        ],
        "deletes": [
          "fault:cell-1-drawer",
          "misaligned:cell-1-drawer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer"
        }
      },
      {
        "id": "replace:cell-1-drawer",
        "label": "replace cell-1-drawer",
        "requires": [
          "done:unlock:cell-1-drawer"
        ],
        "forbids": [
          "done:replace:cell-1-drawer"
        ],
        "adds": [
          "done:replace:cell-1-drawer"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-1-drawer"
        }
      },
      {
        "id": "unlock:cell-1-drawer",
        "label": "unlock cell-1-drawer",
        "requires": [
          "done:support:cell-1-drawer"
        ],
        "forbids": [
          "done:unlock:cell-1-drawer"
        ],
        "adds": [
          "done:unlock:cell-1-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer"
        }
      },
      {
        "id": "support:cell-1-drawer",
        "label": "support cell-1-drawer",
        "requires": [
          "done:isolate:cell-1-drawer"
        ],
        "forbids": [
          "done:support:cell-1-drawer"
        ],
        "adds": [
          "done:support:cell-1-drawer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer"
        }
      },
      {
        "id": "isolate:cell-1-drawer",
        "label": "isolate cell-1-drawer",
        "requires": [
          "tool:free",
          "fault:cell-1-drawer"
        ],
        "forbids": [
          "done:isolate:cell-1-drawer"
        ],
        "adds": [
          "done:isolate:cell-1-drawer"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-drawer"
        }
      },
      {
        "id": "release:cell-1-magazine",
        "label": "release cell-1-magazine",
        "requires": [
          "done:relock:cell-1-magazine"
        ],
        "forbids": [
          "done:release:cell-1-magazine"
        ],
        "adds": [
          "done:release:cell-1-magazine",
          "ready:cell-1-magazine",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine"
        }
      },
      {
        "id": "relock:cell-1-magazine",
        "label": "relock cell-1-magazine",
        "requires": [
          "done:verify:cell-1-magazine"
        ],
        "forbids": [
          "done:relock:cell-1-magazine"
        ],
        "adds": [
          "done:relock:cell-1-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine"
        }
      },
      {
        "id": "verify:cell-1-magazine",
        "label": "verify cell-1-magazine",
        "requires": [
          "done:replace:cell-1-magazine"
        ],
        "forbids": [
          "done:verify:cell-1-magazine"
        ],
        "adds": [
          "done:verify:cell-1-magazine"
        ],
        "deletes": [
          "fault:cell-1-magazine",
          "misaligned:cell-1-magazine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine"
        }
      },
      {
        "id": "replace:cell-1-magazine",
        "label": "replace cell-1-magazine",
        "requires": [
          "done:unlock:cell-1-magazine"
        ],
        "forbids": [
          "done:replace:cell-1-magazine"
        ],
        "adds": [
          "done:replace:cell-1-magazine"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-1-magazine"
        }
      },
      {
        "id": "unlock:cell-1-magazine",
        "label": "unlock cell-1-magazine",
        "requires": [
          "done:support:cell-1-magazine"
        ],
        "forbids": [
          "done:unlock:cell-1-magazine"
        ],
        "adds": [
          "done:unlock:cell-1-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine"
        }
      },
      {
        "id": "support:cell-1-magazine",
        "label": "support cell-1-magazine",
        "requires": [
          "done:isolate:cell-1-magazine"
        ],
        "forbids": [
          "done:support:cell-1-magazine"
        ],
        "adds": [
          "done:support:cell-1-magazine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine"
        }
      },
      {
        "id": "isolate:cell-1-magazine",
        "label": "isolate cell-1-magazine",
        "requires": [
          "tool:free",
          "fault:cell-1-magazine"
        ],
        "forbids": [
          "done:isolate:cell-1-magazine"
        ],
        "adds": [
          "done:isolate:cell-1-magazine"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-magazine"
        }
      },
      {
        "id": "release:cell-1-console",
        "label": "release cell-1-console",
        "requires": [
          "done:relock:cell-1-console"
        ],
        "forbids": [
          "done:release:cell-1-console"
        ],
        "adds": [
          "done:release:cell-1-console",
          "ready:cell-1-console",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console"
        }
      },
      {
        "id": "relock:cell-1-console",
        "label": "relock cell-1-console",
        "requires": [
          "done:verify:cell-1-console"
        ],
        "forbids": [
          "done:relock:cell-1-console"
        ],
        "adds": [
          "done:relock:cell-1-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console"
        }
      },
      {
        "id": "verify:cell-1-console",
        "label": "verify cell-1-console",
        "requires": [
          "done:replace:cell-1-console"
        ],
        "forbids": [
          "done:verify:cell-1-console"
        ],
        "adds": [
          "done:verify:cell-1-console"
        ],
        "deletes": [
          "fault:cell-1-console",
          "misaligned:cell-1-console"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console"
        }
      },
      {
        "id": "replace:cell-1-console",
        "label": "replace cell-1-console",
        "requires": [
          "done:unlock:cell-1-console"
        ],
        "forbids": [
          "done:replace:cell-1-console"
        ],
        "adds": [
          "done:replace:cell-1-console"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-1-console"
        }
      },
      {
        "id": "unlock:cell-1-console",
        "label": "unlock cell-1-console",
        "requires": [
          "done:support:cell-1-console"
        ],
        "forbids": [
          "done:unlock:cell-1-console"
        ],
        "adds": [
          "done:unlock:cell-1-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console"
        }
      },
      {
        "id": "support:cell-1-console",
        "label": "support cell-1-console",
        "requires": [
          "done:isolate:cell-1-console"
        ],
        "forbids": [
          "done:support:cell-1-console"
        ],
        "adds": [
          "done:support:cell-1-console"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console"
        }
      },
      {
        "id": "isolate:cell-1-console",
        "label": "isolate cell-1-console",
        "requires": [
          "tool:free",
          "fault:cell-1-console"
        ],
        "forbids": [
          "done:isolate:cell-1-console"
        ],
        "adds": [
          "done:isolate:cell-1-console"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-console"
        }
      },
      {
        "id": "release:cell-1-cross-feed",
        "label": "release cell-1-cross-feed",
        "requires": [
          "done:relock:cell-1-cross-feed"
        ],
        "forbids": [
          "done:release:cell-1-cross-feed"
        ],
        "adds": [
          "done:release:cell-1-cross-feed",
          "ready:cell-1-cross-feed",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-cross-feed"
        }
      },
      {
        "id": "relock:cell-1-cross-feed",
        "label": "relock cell-1-cross-feed",
        "requires": [
          "done:verify:cell-1-cross-feed"
        ],
        "forbids": [
          "done:relock:cell-1-cross-feed"
        ],
        "adds": [
          "done:relock:cell-1-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-cross-feed"
        }
      },
      {
        "id": "verify:cell-1-cross-feed",
        "label": "verify cell-1-cross-feed",
        "requires": [
          "done:replace:cell-1-cross-feed"
        ],
        "forbids": [
          "done:verify:cell-1-cross-feed"
        ],
        "adds": [
          "done:verify:cell-1-cross-feed"
        ],
        "deletes": [
          "fault:cell-1-cross-feed",
          "misaligned:cell-1-cross-feed"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-cross-feed"
        }
      },
      {
        "id": "replace:cell-1-cross-feed",
        "label": "replace cell-1-cross-feed",
        "requires": [
          "done:unlock:cell-1-cross-feed"
        ],
        "forbids": [
          "done:replace:cell-1-cross-feed"
        ],
        "adds": [
          "done:replace:cell-1-cross-feed"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-1-cross-feed"
        }
      },
      {
        "id": "unlock:cell-1-cross-feed",
        "label": "unlock cell-1-cross-feed",
        "requires": [
          "done:support:cell-1-cross-feed"
        ],
        "forbids": [
          "done:unlock:cell-1-cross-feed"
        ],
        "adds": [
          "done:unlock:cell-1-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-cross-feed"
        }
      },
      {
        "id": "support:cell-1-cross-feed",
        "label": "support cell-1-cross-feed",
        "requires": [
          "done:isolate:cell-1-cross-feed"
        ],
        "forbids": [
          "done:support:cell-1-cross-feed"
        ],
        "adds": [
          "done:support:cell-1-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-cross-feed"
        }
      },
      {
        "id": "isolate:cell-1-cross-feed",
        "label": "isolate cell-1-cross-feed",
        "requires": [
          "tool:free",
          "fault:cell-1-cross-feed"
        ],
        "forbids": [
          "done:isolate:cell-1-cross-feed"
        ],
        "adds": [
          "done:isolate:cell-1-cross-feed"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-cross-feed"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-1-cross-feed",
      "fault:cell-1-console",
      "fault:cell-1-magazine",
      "fault:cell-1-drawer"
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
      "cell-1-carriage",
      "cell-1-cross-feed",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "goalFacts": [
      "ready:cell-1-cross-feed",
      "ready:cell-1-console",
      "ready:cell-1-magazine",
      "ready:cell-1-drawer"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:cell-1-drawer",
      "support:cell-1-drawer",
      "unlock:cell-1-drawer",
      "replace:cell-1-drawer",
      "verify:cell-1-drawer",
      "relock:cell-1-drawer",
      "release:cell-1-drawer",
      "isolate:cell-1-magazine",
      "support:cell-1-magazine",
      "unlock:cell-1-magazine",
      "replace:cell-1-magazine",
      "verify:cell-1-magazine",
      "relock:cell-1-magazine",
      "release:cell-1-magazine",
      "isolate:cell-1-console",
      "support:cell-1-console",
      "unlock:cell-1-console",
      "replace:cell-1-console",
      "verify:cell-1-console",
      "relock:cell-1-console",
      "release:cell-1-console",
      "isolate:cell-1-cross-feed",
      "support:cell-1-cross-feed",
      "unlock:cell-1-cross-feed",
      "replace:cell-1-cross-feed",
      "verify:cell-1-cross-feed",
      "relock:cell-1-cross-feed",
      "release:cell-1-cross-feed"
    ]
  }
}
```

### 预算约束检查策略（h3-exp-d3-arm-1-budget-policy）

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
        "action": "replace"
      }
    ],
    "queries": [
      {
        "id": "visual",
        "cost": 0,
        "returns": {
          "nominal": "clear",
          "fault": "clear"
        }
      },
      {
        "id": "probe",
        "cost": 4,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      }
    ],
    "budget": 3
  },
  "answer": {
    "queryId": "thermal",
    "decisions": {
      "clear": "continue",
      "alert": "replace"
    }
  }
}
```
