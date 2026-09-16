## D3 复合机构·三点弹性托盘

### 模块识别（h3-exp-d3-suspension-1-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：cell-0-shuttle
- B：cell-0-mount
- C：cell-0-elastic-tray
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
        "id": "cell-0-support",
        "name": "cell 0 support"
      },
      {
        "id": "cell-0-elastic-tray",
        "name": "cell 0 elastic tray"
      },
      {
        "id": "cell-0-instrument",
        "name": "cell 0 instrument"
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
        "id": "cell-1-pedestal",
        "name": "cell 1 pedestal"
      },
      {
        "id": "cell-1-rotor",
        "name": "cell 1 rotor"
      },
      {
        "id": "cell-1-offset-load",
        "name": "cell 1 offset load"
      },
      {
        "id": "cell-1-upper-stage",
        "name": "cell 1 upper stage"
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
    "choiceId": "C"
  }
}
```

### 部件计数（h3-exp-d3-suspension-1-count）

模块 cell-0-elastic-tray 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：8
- B：12
- C：9
- D：10

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
        "id": "cell-0-support-p196",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p197",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p198",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p199",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p200",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-support-p201",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-support-p202",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-support-p203",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p204",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p205",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p206",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p207",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-support-p208",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-support-p209",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-elastic-tray-p210",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p211",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p212",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p213",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p214",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p215",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p216",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p217",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p218",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-instrument-p219",
        "moduleId": "cell-0-instrument",
        "shape": "cylinder",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-instrument-p220",
        "moduleId": "cell-0-instrument",
        "shape": "sphere",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p221",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p222",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p223",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p224",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p225",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p226",
        "moduleId": "cell-0-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-console-p227",
        "moduleId": "cell-0-console",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-0-console-p228",
        "moduleId": "cell-0-console",
        "shape": "slope",
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
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p250",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p251",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p252",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p253",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p254",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p255",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p256",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p257",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p258",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p259",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p260",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p261",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p262",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p263",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p264",
        "moduleId": "cell-0-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-magazine-p265",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p266",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p267",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p268",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p269",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p270",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p271",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-magazine-p272",
        "moduleId": "cell-0-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-drawer-p273",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p274",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p275",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p276",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p277",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-drawer-p278",
        "moduleId": "cell-0-drawer",
        "shape": "plate",
        "color": "#45a080"
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
        "id": "cell-1-shuttle-p311",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p312",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p313",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p314",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p315",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p316",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p317",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p318",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p319",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p320",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p321",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p322",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p323",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p324",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p325",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-shuttle-p326",
        "moduleId": "cell-1-shuttle",
        "shape": "plate",
        "color": "#dfebed"
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
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p347",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p348",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p349",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p350",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p351",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p352",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p353",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p354",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p355",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p356",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p357",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p358",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p359",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p360",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-mount-p361",
        "moduleId": "cell-1-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-1-pedestal-p362",
        "moduleId": "cell-1-pedestal",
        "shape": "cylinder",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-rotor-p363",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p364",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p365",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p366",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p367",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p368",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p369",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p370",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p371",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p372",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p373",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p374",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p375",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p376",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p377",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-rotor-p378",
        "moduleId": "cell-1-rotor",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-1-offset-load-p379",
        "moduleId": "cell-1-offset-load",
        "shape": "cylinder",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-offset-load-p380",
        "moduleId": "cell-1-offset-load",
        "shape": "gear",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-upper-stage-p381",
        "moduleId": "cell-1-upper-stage",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-upper-stage-p382",
        "moduleId": "cell-1-upper-stage",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-upper-stage-p383",
        "moduleId": "cell-1-upper-stage",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-upper-stage-p384",
        "moduleId": "cell-1-upper-stage",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-console-p385",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p386",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p387",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p388",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p389",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p390",
        "moduleId": "cell-1-console",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-1-console-p391",
        "moduleId": "cell-1-console",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "cell-1-console-p392",
        "moduleId": "cell-1-console",
        "shape": "slope",
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
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p413",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p414",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p415",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p416",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p417",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p418",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p419",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p420",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p421",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p422",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p423",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p424",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p425",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p426",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p427",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p428",
        "moduleId": "cell-1-magazine",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "cell-1-magazine-p429",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p430",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p431",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p432",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p433",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p434",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p435",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-magazine-p436",
        "moduleId": "cell-1-magazine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-1-drawer-p437",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p438",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p439",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p440",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p441",
        "moduleId": "cell-1-drawer",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-1-drawer-p442",
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

### 颜色识别（h3-exp-d3-suspension-1-color）

零件 cell-0-elastic-tray-p210 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#2878b8
- B：#d43a32
- C：#f2bf3c
- D：#45a080

```json
{
  "input": {
    "part": {
      "id": "cell-0-elastic-tray-p210",
      "moduleId": "cell-0-elastic-tray",
      "shape": "plate",
      "position": [
        -1,
        -0.04999999999999982,
        -1
      ],
      "size": [
        0.96,
        0.24,
        0.96
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

### 三维位置（h3-exp-d3-suspension-1-position）

模块 cell-0-elastic-tray 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[-6.5,0.75,0]
- B：[-6.5,1.35,0]
- C：[-6.5,3.6499999999999995,0]
- D：[0,0.2,0]

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
      "cell-0-support": [
        -6.5,
        3.7750000000000004,
        -0.07499999999999996
      ],
      "cell-0-elastic-tray": [
        -6.5,
        3.6499999999999995,
        0
      ],
      "cell-0-instrument": [
        -6.5,
        4.65,
        0
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
        1.35,
        0
      ],
      "cell-1-pedestal": [
        6.5,
        2.2,
        0
      ],
      "cell-1-rotor": [
        6.5,
        3.25,
        0
      ],
      "cell-1-offset-load": [
        7.5,
        4.1625,
        0.5999999999999999
      ],
      "cell-1-upper-stage": [
        5.5,
        4.35,
        -1
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
    "choiceId": "C"
  }
}
```

### 关节类型（h3-exp-d3-suspension-1-joint-type）

cell-0-instrument-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：fixed
- B：prismatic
- C：spring
- D：revolute

```json
{
  "input": {
    "joint": {
      "id": "cell-0-instrument-joint",
      "name": "cell-0-instrument interface",
      "parent": "cell-0-elastic-tray",
      "child": "cell-0-instrument",
      "type": "revolute",
      "anchorParent": [
        0,
        0.7500000000000009,
        0
      ],
      "anchorChild": [
        0,
        -0.25,
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
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 直接连接（h3-exp-d3-suspension-1-parent）

cell-0-elastic-tray 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["cell-0-support"]
- B：["cell-0-elastic-tray"]
- C：[]
- D：["foundation","cell-0-shuttle","cell-0-mount","cell-0-support","cell-0-elastic-tray","cell-0-instrument","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-pedestal","cell-1-rotor","cell-1-offset-load","cell-1-upper-stage","cell-1-console","cell-1-magazine","cell-1-drawer"]

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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.8250000000000002,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.1750000000000007,
          0.07499999999999996
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
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.7500000000000009,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
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
        "id": "cell-1-pedestal-joint",
        "name": "cell-1-pedestal interface",
        "parent": "cell-1-mount",
        "child": "cell-1-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
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
        "id": "cell-1-rotor-joint",
        "name": "cell-1-rotor interface",
        "parent": "cell-1-pedestal",
        "child": "cell-1-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
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
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-offset-load-joint",
        "name": "cell-1-offset-load interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-upper-stage-joint",
        "name": "cell-1-upper-stage interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
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
    "choiceId": "A"
  }
}
```

### 基座识别（h3-exp-d3-suspension-1-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["cell-0-elastic-tray"]
- B：["foundation"]
- C：[]
- D：["foundation","cell-0-shuttle","cell-0-mount","cell-0-support","cell-0-elastic-tray","cell-0-instrument","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-pedestal","cell-1-rotor","cell-1-offset-load","cell-1-upper-stage","cell-1-console","cell-1-magazine","cell-1-drawer"]

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
        "id": "cell-0-support",
        "name": "cell 0 support",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -6.5,
          3.7750000000000004,
          -0.07499999999999996
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-elastic-tray",
        "name": "cell 0 elastic tray",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -6.5,
          3.6499999999999995,
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
        "id": "cell-0-instrument",
        "name": "cell 0 instrument",
        "role": "actuator",
        "anchored": false,
        "mass": 0.25,
        "position": [
          -6.5,
          4.65,
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
        "id": "cell-1-pedestal",
        "name": "cell 1 pedestal",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          6.5,
          2.2,
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
        "id": "cell-1-rotor",
        "name": "cell 1 rotor",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          6.5,
          3.25,
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
        "id": "cell-1-offset-load",
        "name": "cell 1 offset load",
        "role": "structure",
        "anchored": false,
        "mass": 0.8,
        "position": [
          7.5,
          4.1625,
          0.5999999999999999
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-1-upper-stage",
        "name": "cell 1 upper stage",
        "role": "actuator",
        "anchored": false,
        "mass": 0.8,
        "position": [
          5.5,
          4.35,
          -1
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
    "choiceId": "B"
  }
}
```

### 接口计数（h3-exp-d3-suspension-1-degree）

cell-0-elastic-tray 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：3
- B：6
- C：4
- D：5

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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.8250000000000002,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.1750000000000007,
          0.07499999999999996
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
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.7500000000000009,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
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
        "id": "cell-1-pedestal-joint",
        "name": "cell-1-pedestal interface",
        "parent": "cell-1-mount",
        "child": "cell-1-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
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
        "id": "cell-1-rotor-joint",
        "name": "cell-1-rotor interface",
        "parent": "cell-1-pedestal",
        "child": "cell-1-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
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
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-offset-load-joint",
        "name": "cell-1-offset-load interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-upper-stage-joint",
        "name": "cell-1-upper-stage interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
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

### 局部改色（h3-exp-d3-suspension-1-recolor）

仅将 cell-0-elastic-tray-p210 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-elastic-tray-p211","color":"#e8792e"}
- B：{"id":"cell-0-elastic-tray-p210","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"cell-0-elastic-tray-p210","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "cell-0-elastic-tray-p210",
      "moduleId": "cell-0-elastic-tray",
      "shape": "plate",
      "position": [
        -1,
        -0.04999999999999982,
        -1
      ],
      "size": [
        0.96,
        0.24,
        0.96
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

### 补装部件（h3-exp-d3-suspension-1-add）

模块 cell-0-elastic-tray 缺失零件 cell-0-elastic-tray-p210。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-elastic-tray-p210","moduleId":"cell-0-elastic-tray","shape":"plate","position":[-1,-0.04999999999999982,-1],"size":[0.96,0.24,0.96],"color":"#45a080","rotation":[0,0,0,1]}
- B：{"id":"cell-0-elastic-tray-p210","moduleId":"foundation","shape":"plate","position":[-1,-0.04999999999999982,-1],"size":[0.96,0.24,0.96],"color":"#45a080","rotation":[0,0,0,1]}
- C：{"id":"cell-0-elastic-tray-p210","moduleId":"cell-0-elastic-tray","shape":"plate","position":[-1,-0.04999999999999982,-1],"size":[3,3,3],"color":"#45a080","rotation":[0,0,0,1]}
- D：{"id":"cell-0-elastic-tray-p210","moduleId":"cell-0-elastic-tray","shape":"plate","position":[-1,-0.04999999999999982,-1],"size":[0.96,0.24,0.96],"color":"#000000","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "cell-0-elastic-tray-p210",
      "moduleId": "cell-0-elastic-tray",
      "shape": "plate",
      "position": [
        -1,
        -0.04999999999999982,
        -1
      ],
      "size": [
        0.96,
        0.24,
        0.96
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
      "cell-0-support-p196",
      "cell-0-support-p197",
      "cell-0-support-p198",
      "cell-0-support-p199",
      "cell-0-support-p200",
      "cell-0-support-p201",
      "cell-0-support-p202",
      "cell-0-support-p203",
      "cell-0-support-p204",
      "cell-0-support-p205",
      "cell-0-support-p206",
      "cell-0-support-p207",
      "cell-0-support-p208",
      "cell-0-support-p209",
      "cell-0-elastic-tray-p211",
      "cell-0-elastic-tray-p212",
      "cell-0-elastic-tray-p213",
      "cell-0-elastic-tray-p214",
      "cell-0-elastic-tray-p215",
      "cell-0-elastic-tray-p216",
      "cell-0-elastic-tray-p217",
      "cell-0-elastic-tray-p218",
      "cell-0-instrument-p219",
      "cell-0-instrument-p220",
      "cell-0-console-p221",
      "cell-0-console-p222",
      "cell-0-console-p223",
      "cell-0-console-p224",
      "cell-0-console-p225",
      "cell-0-console-p226",
      "cell-0-console-p227",
      "cell-0-console-p228",
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
      "cell-0-magazine-p257",
      "cell-0-magazine-p258",
      "cell-0-magazine-p259",
      "cell-0-magazine-p260",
      "cell-0-magazine-p261",
      "cell-0-magazine-p262",
      "cell-0-magazine-p263",
      "cell-0-magazine-p264",
      "cell-0-magazine-p265",
      "cell-0-magazine-p266",
      "cell-0-magazine-p267",
      "cell-0-magazine-p268",
      "cell-0-magazine-p269",
      "cell-0-magazine-p270",
      "cell-0-magazine-p271",
      "cell-0-magazine-p272",
      "cell-0-drawer-p273",
      "cell-0-drawer-p274",
      "cell-0-drawer-p275",
      "cell-0-drawer-p276",
      "cell-0-drawer-p277",
      "cell-0-drawer-p278",
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
      "cell-1-shuttle-p311",
      "cell-1-shuttle-p312",
      "cell-1-shuttle-p313",
      "cell-1-shuttle-p314",
      "cell-1-shuttle-p315",
      "cell-1-shuttle-p316",
      "cell-1-shuttle-p317",
      "cell-1-shuttle-p318",
      "cell-1-shuttle-p319",
      "cell-1-shuttle-p320",
      "cell-1-shuttle-p321",
      "cell-1-shuttle-p322",
      "cell-1-shuttle-p323",
      "cell-1-shuttle-p324",
      "cell-1-shuttle-p325",
      "cell-1-shuttle-p326",
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
      "cell-1-mount-p354",
      "cell-1-mount-p355",
      "cell-1-mount-p356",
      "cell-1-mount-p357",
      "cell-1-mount-p358",
      "cell-1-mount-p359",
      "cell-1-mount-p360",
      "cell-1-mount-p361",
      "cell-1-pedestal-p362",
      "cell-1-rotor-p363",
      "cell-1-rotor-p364",
      "cell-1-rotor-p365",
      "cell-1-rotor-p366",
      "cell-1-rotor-p367",
      "cell-1-rotor-p368",
      "cell-1-rotor-p369",
      "cell-1-rotor-p370",
      "cell-1-rotor-p371",
      "cell-1-rotor-p372",
      "cell-1-rotor-p373",
      "cell-1-rotor-p374",
      "cell-1-rotor-p375",
      "cell-1-rotor-p376",
      "cell-1-rotor-p377",
      "cell-1-rotor-p378",
      "cell-1-offset-load-p379",
      "cell-1-offset-load-p380",
      "cell-1-upper-stage-p381",
      "cell-1-upper-stage-p382",
      "cell-1-upper-stage-p383",
      "cell-1-upper-stage-p384",
      "cell-1-console-p385",
      "cell-1-console-p386",
      "cell-1-console-p387",
      "cell-1-console-p388",
      "cell-1-console-p389",
      "cell-1-console-p390",
      "cell-1-console-p391",
      "cell-1-console-p392",
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
      "cell-1-magazine-p420",
      "cell-1-magazine-p421",
      "cell-1-magazine-p422",
      "cell-1-magazine-p423",
      "cell-1-magazine-p424",
      "cell-1-magazine-p425",
      "cell-1-magazine-p426",
      "cell-1-magazine-p427",
      "cell-1-magazine-p428",
      "cell-1-magazine-p429",
      "cell-1-magazine-p430",
      "cell-1-magazine-p431",
      "cell-1-magazine-p432",
      "cell-1-magazine-p433",
      "cell-1-magazine-p434",
      "cell-1-magazine-p435",
      "cell-1-magazine-p436",
      "cell-1-drawer-p437",
      "cell-1-drawer-p438",
      "cell-1-drawer-p439",
      "cell-1-drawer-p440",
      "cell-1-drawer-p441",
      "cell-1-drawer-p442"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全拆除（h3-exp-d3-suspension-1-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["foundation"]
- B：[]
- C：["foundation","cell-0-shuttle","cell-0-mount","cell-0-support","cell-0-elastic-tray","cell-0-instrument","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-pedestal","cell-1-rotor","cell-1-offset-load","cell-1-upper-stage","cell-1-console","cell-1-magazine","cell-1-drawer"]
- D：["cell-0-console","cell-0-drawer","cell-0-instrument","cell-1-console","cell-1-drawer","cell-1-offset-load","cell-1-upper-stage"]

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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.8250000000000002,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.1750000000000007,
          0.07499999999999996
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
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.7500000000000009,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
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
        "id": "cell-1-pedestal-joint",
        "name": "cell-1-pedestal interface",
        "parent": "cell-1-mount",
        "child": "cell-1-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
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
        "id": "cell-1-rotor-joint",
        "name": "cell-1-rotor interface",
        "parent": "cell-1-pedestal",
        "child": "cell-1-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
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
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-offset-load-joint",
        "name": "cell-1-offset-load interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-upper-stage-joint",
        "name": "cell-1-upper-stage interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
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
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-pedestal",
      "cell-1-rotor",
      "cell-1-offset-load",
      "cell-1-upper-stage",
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

### 替换选择（h3-exp-d3-suspension-1-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-0
- B：stock-2
- C：stock-3
- D：stock-1

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 8,
        "stiffness": 3,
        "mass": 1.9
      },
      {
        "id": "stock-1",
        "cost": 3,
        "stiffness": 3,
        "mass": 1.3
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 8,
        "mass": 1.6
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 3,
        "mass": 1.8
      }
    ],
    "maxCost": 6
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-exp-d3-suspension-1-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[-3,0,2]
- B：[3,0,-2]
- C：[0,0,0]
- D：[0,2,0]

```json
{
  "input": {
    "delta": [
      3,
      0,
      -2
    ],
    "target": "cell-0-elastic-tray"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 姿态纠偏（h3-exp-d3-suspension-1-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：90
- B：-90
- C：0
- D：-180

```json
{
  "input": {
    "module": "cell-0-elastic-tray",
    "currentYaw": 315,
    "targetYaw": 45
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 下一步放置（h3-exp-d3-suspension-1-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","cell-0-shuttle","cell-0-mount","cell-0-support","cell-0-elastic-tray","cell-0-instrument","cell-0-console","cell-0-magazine","cell-0-drawer"]
- C：["cell-1-shuttle","cell-1-mount","cell-1-pedestal","cell-1-rotor","cell-1-offset-load","cell-1-upper-stage","cell-1-console","cell-1-magazine","cell-1-drawer"]
- D：["cell-1-console","cell-1-magazine","cell-1-shuttle"]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer"
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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.8250000000000002,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.1750000000000007,
          0.07499999999999996
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
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.7500000000000009,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
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
        "id": "cell-1-pedestal-joint",
        "name": "cell-1-pedestal interface",
        "parent": "cell-1-mount",
        "child": "cell-1-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
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
        "id": "cell-1-rotor-joint",
        "name": "cell-1-rotor interface",
        "parent": "cell-1-pedestal",
        "child": "cell-1-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
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
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-offset-load-joint",
        "name": "cell-1-offset-load interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-upper-stage-joint",
        "name": "cell-1-upper-stage interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
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
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-pedestal",
      "cell-1-rotor",
      "cell-1-offset-load",
      "cell-1-upper-stage",
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

### 库存核算（h3-exp-d3-suspension-1-inventory）

备件库有 15 件，替换模块需 9 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：6
- B：7
- C：5
- D：9

```json
{
  "input": {
    "available": 15,
    "required": 9
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 子装配边界（h3-exp-d3-suspension-1-boundary）

隔离 cell-0-elastic-tray 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：[]
- B：["cell-0-shuttle-joint","cell-0-mount-joint","cell-0-support-joint","cell-0-elastic-tray-joint","cell-0-elastic-tray-elastic-1","cell-0-elastic-tray-elastic-2","cell-0-instrument-joint","cell-0-console-joint","cell-0-magazine-joint","cell-0-drawer-joint","cell-1-shuttle-joint","cell-1-mount-joint","cell-1-pedestal-joint","cell-1-rotor-joint","cell-1-offset-load-joint","cell-1-upper-stage-joint","cell-1-console-joint","cell-1-magazine-joint","cell-1-drawer-joint"]
- C：["cell-0-instrument-joint"]
- D：["cell-0-elastic-tray-elastic-1","cell-0-elastic-tray-elastic-2","cell-0-elastic-tray-joint","cell-0-instrument-joint"]

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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.8250000000000002,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.1750000000000007,
          0.07499999999999996
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
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.7500000000000009,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
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
        "id": "cell-1-pedestal-joint",
        "name": "cell-1-pedestal interface",
        "parent": "cell-1-mount",
        "child": "cell-1-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
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
        "id": "cell-1-rotor-joint",
        "name": "cell-1-rotor interface",
        "parent": "cell-1-pedestal",
        "child": "cell-1-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
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
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-offset-load-joint",
        "name": "cell-1-offset-load interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-upper-stage-joint",
        "name": "cell-1-upper-stage interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
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
    "target": "cell-0-elastic-tray"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 最小干预（h3-exp-d3-suspension-1-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：9
- B：0
- C：1
- D：2

```json
{
  "input": {
    "module": "cell-0-elastic-tray"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 全过程依赖（h3-exp-d3-suspension-1-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：17
- B：16
- C：-1

```json
{
  "input": {
    "order": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-pedestal",
      "cell-1-rotor",
      "cell-1-offset-load",
      "cell-1-upper-stage",
      "cell-1-console",
      "cell-1-drawer",
      "cell-1-magazine"
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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.8250000000000002,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.1750000000000007,
          0.07499999999999996
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
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.7500000000000009,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
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
        "id": "cell-1-pedestal-joint",
        "name": "cell-1-pedestal interface",
        "parent": "cell-1-mount",
        "child": "cell-1-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
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
        "id": "cell-1-rotor-joint",
        "name": "cell-1-rotor interface",
        "parent": "cell-1-pedestal",
        "child": "cell-1-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
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
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-offset-load-joint",
        "name": "cell-1-offset-load interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-upper-stage-joint",
        "name": "cell-1-upper-stage interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
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
    "choiceId": "B"
  }
}
```

### 连续维修路径（h3-exp-d3-suspension-1-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-2
- B：path-0
- C：path-1

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          14.48,
          3.6499999999999995,
          0
        ],
        "end": [
          -6.5,
          3.6499999999999995,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.2931362986564636
      },
      {
        "id": "path-1",
        "start": [
          -6.5,
          9.600000000000001,
          0
        ],
        "end": [
          -6.5,
          3.6499999999999995,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.6924371123313904
      },
      {
        "id": "path-2",
        "start": [
          -6.5,
          3.6499999999999995,
          10.98
        ],
        "end": [
          -6.5,
          3.6499999999999995,
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
      "A"
    ]
  }
}
```

### 支撑反事实（h3-exp-d3-suspension-1-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["foundation","cell-0-shuttle","cell-0-mount","cell-0-support","cell-0-elastic-tray","cell-0-instrument","cell-0-console","cell-0-magazine","cell-0-drawer","cell-1-shuttle","cell-1-mount","cell-1-pedestal","cell-1-rotor","cell-1-offset-load","cell-1-upper-stage","cell-1-console","cell-1-magazine","cell-1-drawer"]
- B：["cell-0-elastic-tray","cell-0-instrument","cell-0-mount","cell-0-support"]
- C：["cell-0-shuttle"]
- D：[]

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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.8250000000000002,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.1750000000000007,
          0.07499999999999996
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
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.7500000000000009,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
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
        "id": "cell-1-pedestal-joint",
        "name": "cell-1-pedestal interface",
        "parent": "cell-1-mount",
        "child": "cell-1-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
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
        "id": "cell-1-rotor-joint",
        "name": "cell-1-rotor interface",
        "parent": "cell-1-pedestal",
        "child": "cell-1-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
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
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-offset-load-joint",
        "name": "cell-1-offset-load interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-upper-stage-joint",
        "name": "cell-1-upper-stage interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
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
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-pedestal",
      "cell-1-rotor",
      "cell-1-offset-load",
      "cell-1-upper-stage",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 冲击响应读数（h3-exp-d3-suspension-1-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.225
- B：0
- C：1.025
- D：0.025

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.024995151978505815
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.016497226250901408
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.009740811859584688
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.005026268528015397
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.00258364457571099
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0015926704128136013
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.000878086498211033
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0005121817127218718
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.00027861862379473625
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.00010289875148899049
      },
      {
        "time": 1,
        "displacement": 0.00013120010775369729
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.005148423657378856,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节限位推理（h3-exp-d3-suspension-1-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：0
- B：-1.1
- C：1.1
- D：-0.6

```json
{
  "input": {
    "joint": "cell-0-instrument-joint",
    "limits": [
      -0.6,
      0.6
    ],
    "units": "radians"
  },
  "answer": {
    "choiceIds": [
      "A",
      "D"
    ]
  }
}
```

### 约束故障诊断（h3-exp-d3-suspension-1-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：cell-0-elastic-tray-elastic-1
- B：cell-0-elastic-tray-elastic-2
- C：cell-0-shuttle-joint
- D：cell-0-mount-joint
- O5：cell-0-support-joint
- O6：cell-0-elastic-tray-joint

```json
{
  "input": {
    "endpoints": [
      "cell-0-support",
      "cell-0-elastic-tray"
    ],
    "type": "spring",
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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.8250000000000002,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.1750000000000007,
          0.07499999999999996
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
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.1750000000000007,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.04999999999999982,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.7500000000000009,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
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
        "id": "cell-1-pedestal-joint",
        "name": "cell-1-pedestal interface",
        "parent": "cell-1-mount",
        "child": "cell-1-pedestal",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8500000000000001,
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
        "id": "cell-1-rotor-joint",
        "name": "cell-1-rotor interface",
        "parent": "cell-1-pedestal",
        "child": "cell-1-rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          1,
          0
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
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-1-offset-load-joint",
        "name": "cell-1-offset-load interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-offset-load",
        "type": "fixed",
        "anchorParent": [
          1,
          0.75,
          0.6
        ],
        "anchorChild": [
          0,
          -0.16249999999999964,
          1.1102230246251565e-16
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-1-upper-stage-joint",
        "name": "cell-1-upper-stage interface",
        "parent": "cell-1-rotor",
        "child": "cell-1-upper-stage",
        "type": "prismatic",
        "anchorParent": [
          -1,
          1.0499999999999998,
          -1
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
      "A",
      "B",
      "O6"
    ]
  }
}
```

### 主动检查收益（h3-exp-d3-suspension-1-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-1
- B：query-2
- C：query-0

```json
{
  "input": {
    "queries": [
      {
        "id": "query-0",
        "cost": 1,
        "returns": [
          0,
          0,
          1,
          1
        ]
      },
      {
        "id": "query-1",
        "cost": 2,
        "returns": [
          0,
          1,
          2,
          3
        ]
      },
      {
        "id": "query-2",
        "cost": 3,
        "returns": [
          0,
          0,
          0,
          1
        ]
      }
    ],
    "module": "cell-0-elastic-tray",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "C"
    ]
  }
}
```

### 不确定性与弃答（h3-exp-d3-suspension-1-abstention）

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

### 观测后信念更新（h3-exp-d3-suspension-1-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.3333333333333333
- B：0.5
- C：0.25
- D：0

```json
{
  "input": {
    "module": "cell-0-elastic-tray",
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
      "positive"
    ],
    "observed": "positive"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 多目标工程权衡（h3-exp-d3-suspension-1-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-3
- B：stock-1
- C：stock-2
- D：stock-0

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 8,
        "stiffness": 3,
        "mass": 1.9
      },
      {
        "id": "stock-1",
        "cost": 3,
        "stiffness": 3,
        "mass": 1.3
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 8,
        "mass": 1.6
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 3,
        "mass": 1.8
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "B",
      "C"
    ]
  }
}
```

### 依赖装配（h3-exp-d3-suspension-1-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
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
        "id": "place:cell-0-elastic-tray",
        "label": "安装 cell-0-elastic-tray",
        "requires": [
          "present:cell-0-support",
          "present:cell-0-support",
          "present:cell-0-support"
        ],
        "forbids": [
          "present:cell-0-elastic-tray"
        ],
        "adds": [
          "present:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
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
        "id": "place:cell-1-pedestal",
        "label": "安装 cell-1-pedestal",
        "requires": [
          "present:cell-1-mount"
        ],
        "forbids": [
          "present:cell-1-pedestal"
        ],
        "adds": [
          "present:cell-1-pedestal"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-pedestal",
          "visible": true
        }
      },
      {
        "id": "place:cell-1-rotor",
        "label": "安装 cell-1-rotor",
        "requires": [
          "present:cell-1-pedestal"
        ],
        "forbids": [
          "present:cell-1-rotor"
        ],
        "adds": [
          "present:cell-1-rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-rotor",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-instrument",
        "label": "安装 cell-0-instrument",
        "requires": [
          "present:cell-0-elastic-tray"
        ],
        "forbids": [
          "present:cell-0-instrument"
        ],
        "adds": [
          "present:cell-0-instrument"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument",
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
        "id": "place:cell-1-offset-load",
        "label": "安装 cell-1-offset-load",
        "requires": [
          "present:cell-1-rotor"
        ],
        "forbids": [
          "present:cell-1-offset-load"
        ],
        "adds": [
          "present:cell-1-offset-load"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-offset-load",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-support",
        "label": "安装 cell-0-support",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-support"
        ],
        "adds": [
          "present:cell-0-support"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-support",
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
        "id": "place:cell-1-upper-stage",
        "label": "安装 cell-1-upper-stage",
        "requires": [
          "present:cell-1-rotor"
        ],
        "forbids": [
          "present:cell-1-upper-stage"
        ],
        "adds": [
          "present:cell-1-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-upper-stage",
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
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:cell-0-shuttle",
      "present:cell-0-mount",
      "present:cell-0-support",
      "present:cell-0-elastic-tray",
      "present:cell-0-instrument",
      "present:cell-0-console",
      "present:cell-0-magazine",
      "present:cell-0-drawer",
      "present:cell-1-shuttle",
      "present:cell-1-mount",
      "present:cell-1-pedestal",
      "present:cell-1-rotor",
      "present:cell-1-offset-load",
      "present:cell-1-upper-stage",
      "present:cell-1-console",
      "present:cell-1-magazine",
      "present:cell-1-drawer"
    ],
    "budget": 18,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:cell-0-console",
      "place:cell-1-magazine",
      "place:cell-0-magazine",
      "place:cell-0-shuttle",
      "place:cell-0-mount",
      "place:cell-1-console",
      "place:cell-1-shuttle",
      "place:cell-1-mount",
      "place:cell-1-pedestal",
      "place:cell-1-rotor",
      "place:cell-1-offset-load",
      "place:cell-0-support",
      "place:cell-0-elastic-tray",
      "place:cell-0-instrument",
      "place:cell-1-drawer",
      "place:cell-1-upper-stage",
      "place:cell-0-drawer"
    ]
  }
}
```

### 依赖拆解（h3-exp-d3-suspension-1-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:cell-0-shuttle",
      "present:cell-0-mount",
      "present:cell-0-support",
      "present:cell-0-elastic-tray",
      "present:cell-0-instrument",
      "present:cell-0-console",
      "present:cell-0-magazine",
      "present:cell-0-drawer",
      "present:cell-1-shuttle",
      "present:cell-1-mount",
      "present:cell-1-pedestal",
      "present:cell-1-rotor",
      "present:cell-1-offset-load",
      "present:cell-1-upper-stage",
      "present:cell-1-console",
      "present:cell-1-magazine",
      "present:cell-1-drawer"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-pedestal",
      "cell-1-rotor",
      "cell-1-offset-load",
      "cell-1-upper-stage",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "actions": [
      {
        "id": "remove:cell-0-elastic-tray",
        "label": "拆除 cell-0-elastic-tray",
        "requires": [
          "present:cell-0-elastic-tray"
        ],
        "forbids": [
          "present:cell-0-instrument"
        ],
        "adds": [
          "removed:cell-0-elastic-tray"
        ],
        "deletes": [
          "present:cell-0-elastic-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
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
        "id": "remove:cell-1-mount",
        "label": "拆除 cell-1-mount",
        "requires": [
          "present:cell-1-mount"
        ],
        "forbids": [
          "present:cell-1-pedestal"
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
        "id": "remove:cell-1-upper-stage",
        "label": "拆除 cell-1-upper-stage",
        "requires": [
          "present:cell-1-upper-stage"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-1-upper-stage"
        ],
        "deletes": [
          "present:cell-1-upper-stage"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-upper-stage",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-offset-load",
        "label": "拆除 cell-1-offset-load",
        "requires": [
          "present:cell-1-offset-load"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-1-offset-load"
        ],
        "deletes": [
          "present:cell-1-offset-load"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-offset-load",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-rotor",
        "label": "拆除 cell-1-rotor",
        "requires": [
          "present:cell-1-rotor"
        ],
        "forbids": [
          "present:cell-1-offset-load",
          "present:cell-1-upper-stage"
        ],
        "adds": [
          "removed:cell-1-rotor"
        ],
        "deletes": [
          "present:cell-1-rotor"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-rotor",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-instrument",
        "label": "拆除 cell-0-instrument",
        "requires": [
          "present:cell-0-instrument"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-instrument"
        ],
        "deletes": [
          "present:cell-0-instrument"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-support",
        "label": "拆除 cell-0-support",
        "requires": [
          "present:cell-0-support"
        ],
        "forbids": [
          "present:cell-0-elastic-tray",
          "present:cell-0-elastic-tray",
          "present:cell-0-elastic-tray"
        ],
        "adds": [
          "removed:cell-0-support"
        ],
        "deletes": [
          "present:cell-0-support"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-support",
          "visible": false
        }
      },
      {
        "id": "remove:cell-1-pedestal",
        "label": "拆除 cell-1-pedestal",
        "requires": [
          "present:cell-1-pedestal"
        ],
        "forbids": [
          "present:cell-1-rotor"
        ],
        "adds": [
          "removed:cell-1-pedestal"
        ],
        "deletes": [
          "present:cell-1-pedestal"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-pedestal",
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
        "id": "remove:cell-0-mount",
        "label": "拆除 cell-0-mount",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-support"
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
      }
    ],
    "goalFacts": [
      "removed:cell-1-drawer",
      "removed:cell-1-magazine",
      "removed:cell-1-console",
      "removed:cell-1-upper-stage",
      "removed:cell-1-offset-load",
      "removed:cell-1-rotor",
      "removed:cell-1-pedestal",
      "removed:cell-1-mount",
      "removed:cell-1-shuttle",
      "removed:cell-0-drawer",
      "removed:cell-0-magazine",
      "removed:cell-0-console",
      "removed:cell-0-instrument",
      "removed:cell-0-elastic-tray",
      "removed:cell-0-support",
      "removed:cell-0-mount",
      "removed:cell-0-shuttle",
      "removed:foundation"
    ],
    "budget": 18,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:cell-1-upper-stage",
      "remove:cell-1-offset-load",
      "remove:cell-1-rotor",
      "remove:cell-0-instrument",
      "remove:cell-0-elastic-tray",
      "remove:cell-0-support",
      "remove:cell-1-pedestal",
      "remove:cell-1-mount",
      "remove:cell-1-drawer",
      "remove:cell-1-magazine",
      "remove:cell-0-drawer",
      "remove:cell-1-console",
      "remove:cell-0-magazine",
      "remove:cell-0-mount",
      "remove:cell-0-shuttle",
      "remove:cell-1-shuttle",
      "remove:cell-0-console",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-exp-d3-suspension-1-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-elastic-tray",
      "closed:cell-0-elastic-tray"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-pedestal",
      "cell-1-rotor",
      "cell-1-offset-load",
      "cell-1-upper-stage",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "actions": [
      {
        "id": "remove:cell-0-elastic-tray",
        "label": "remove cell-0-elastic-tray",
        "requires": [
          "done:open:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:remove:cell-0-elastic-tray"
        ],
        "adds": [
          "done:remove:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
          "visible": false
        }
      },
      {
        "id": "support:cell-0-elastic-tray",
        "label": "support cell-0-elastic-tray",
        "requires": [
          "fault:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:support:cell-0-elastic-tray"
        ],
        "adds": [
          "done:support:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "release:cell-0-elastic-tray",
        "label": "release cell-0-elastic-tray",
        "requires": [
          "done:close:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:release:cell-0-elastic-tray"
        ],
        "adds": [
          "done:release:cell-0-elastic-tray",
          "repaired:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "verify:cell-0-elastic-tray",
        "label": "verify cell-0-elastic-tray",
        "requires": [
          "done:replace:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:verify:cell-0-elastic-tray"
        ],
        "adds": [
          "done:verify:cell-0-elastic-tray"
        ],
        "deletes": [
          "fault:cell-0-elastic-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "close:cell-0-elastic-tray",
        "label": "close cell-0-elastic-tray",
        "requires": [
          "done:verify:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:close:cell-0-elastic-tray"
        ],
        "adds": [
          "done:close:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "open:cell-0-elastic-tray",
        "label": "open cell-0-elastic-tray",
        "requires": [
          "done:support:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:open:cell-0-elastic-tray"
        ],
        "adds": [
          "done:open:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "replace:cell-0-elastic-tray",
        "label": "replace cell-0-elastic-tray",
        "requires": [
          "done:remove:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:replace:cell-0-elastic-tray"
        ],
        "adds": [
          "done:replace:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-elastic-tray"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-elastic-tray",
      "open:cell-0-elastic-tray",
      "remove:cell-0-elastic-tray",
      "replace:cell-0-elastic-tray",
      "verify:cell-0-elastic-tray",
      "close:cell-0-elastic-tray",
      "release:cell-0-elastic-tray"
    ]
  }
}
```

### 复合编辑验证（h3-exp-d3-suspension-1-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-elastic-tray",
      "closed:cell-0-elastic-tray"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-pedestal",
      "cell-1-rotor",
      "cell-1-offset-load",
      "cell-1-upper-stage",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "actions": [
      {
        "id": "support:cell-0-elastic-tray",
        "label": "support cell-0-elastic-tray",
        "requires": [
          "fault:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:support:cell-0-elastic-tray"
        ],
        "adds": [
          "done:support:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "release:cell-0-elastic-tray",
        "label": "release cell-0-elastic-tray",
        "requires": [
          "done:close:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:release:cell-0-elastic-tray"
        ],
        "adds": [
          "done:release:cell-0-elastic-tray",
          "repaired:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "recolor:cell-0-elastic-tray",
        "label": "recolor cell-0-elastic-tray",
        "requires": [
          "done:open:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:recolor:cell-0-elastic-tray"
        ],
        "adds": [
          "done:recolor:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
          "color": "#ea7635"
        }
      },
      {
        "id": "verify:cell-0-elastic-tray",
        "label": "verify cell-0-elastic-tray",
        "requires": [
          "done:recolor:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:verify:cell-0-elastic-tray"
        ],
        "adds": [
          "done:verify:cell-0-elastic-tray"
        ],
        "deletes": [
          "fault:cell-0-elastic-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "close:cell-0-elastic-tray",
        "label": "close cell-0-elastic-tray",
        "requires": [
          "done:verify:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:close:cell-0-elastic-tray"
        ],
        "adds": [
          "done:close:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "open:cell-0-elastic-tray",
        "label": "open cell-0-elastic-tray",
        "requires": [
          "done:support:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:open:cell-0-elastic-tray"
        ],
        "adds": [
          "done:open:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-elastic-tray"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-elastic-tray",
      "open:cell-0-elastic-tray",
      "recolor:cell-0-elastic-tray",
      "verify:cell-0-elastic-tray",
      "close:cell-0-elastic-tray",
      "release:cell-0-elastic-tray"
    ]
  }
}
```

### 跨区域联合维修（h3-exp-d3-suspension-1-multi-fault）

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
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-pedestal",
      "cell-1-rotor",
      "cell-1-offset-load",
      "cell-1-upper-stage",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "actions": [
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
      "support:cell-1-magazine",
      "open:cell-1-magazine",
      "remove:cell-1-magazine",
      "support:cell-1-drawer",
      "open:cell-1-drawer",
      "remove:cell-1-drawer",
      "replace:cell-1-drawer",
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
      "release:cell-1-magazine",
      "verify:cell-1-drawer",
      "close:cell-1-drawer",
      "release:cell-1-drawer"
    ]
  }
}
```

### 多工位资源调度（h3-exp-d3-suspension-1-scheduling）

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
        "module": "cell-0-support",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "cell-0-elastic-tray",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "cell-0-instrument",
        "duration": 3,
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
      }
    ],
    "deadline": 8
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 1,
      "job-4": 4,
      "job-5": 4,
      "job-6": 5,
      "job-7": 7
    }
  }
}
```

### 检查后条件策略（h3-exp-d3-suspension-1-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-elastic-tray",
    "worlds": [
      {
        "id": "normal",
        "action": "continue"
      },
      {
        "id": "loose",
        "action": "tighten"
      },
      {
        "id": "jammed",
        "action": "replace"
      }
    ],
    "budget": 1,
    "queries": [
      {
        "id": "visual",
        "cost": 1,
        "returns": {
          "normal": "signal-0",
          "loose": "signal-1",
          "jammed": "signal-2"
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
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      }
    ]
  },
  "answer": {
    "queryId": "visual",
    "decisions": {
      "signal-0": "continue",
      "signal-1": "tighten",
      "signal-2": "replace"
    }
  }
}
```

### 局部坐标变换（h3-exp-d3-suspension-1-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[-6.5,3.6,-1]
- B：[-4.5,4.6,1]
- C：[-5.5,3.6,0]
- D：[0,-0.05,-1]

```json
{
  "input": {
    "localPoint": [
      0,
      -0.04999999999999982,
      -1
    ],
    "rotationXYZW": [
      0,
      0.7071067811865476,
      0,
      -0.7071067811865475
    ],
    "translation": [
      -6.5,
      3.6499999999999995,
      0
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-exp-d3-suspension-1-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[9,4]
- B：[4,5]
- C：[0,0]
- D：[4,9]

```json
{
  "input": {
    "view": "front",
    "point": [
      4,
      9,
      -5
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 空间相对关系（h3-exp-d3-suspension-1-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：less
- B：equal
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
    "axis": "x"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 约束自由度（h3-exp-d3-suspension-1-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：0
- B：3
- C：6
- D：1

```json
{
  "input": {
    "joint": {
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
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 维修间隙预算（h3-exp-d3-suspension-1-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "cell-0-elastic-tray",
    "aperture": 0.6100000000000001,
    "toolWidth": 0.55,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-exp-d3-suspension-1-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,-3,0]
- C：[0,0,-9]
- D：[0,0,9]

```json
{
  "input": {
    "module": "cell-0-elastic-tray",
    "lever": [
      3,
      1,
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
    "choiceId": "C"
  }
}
```

### 非均匀先验更新（h3-exp-d3-suspension-1-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.75
- B：0.5
- C：0
- D：1

```json
{
  "input": {
    "module": "cell-0-elastic-tray",
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
    "choiceId": "A"
  }
}
```

### 风险最小决策（h3-exp-d3-suspension-1-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.8,
    "repairCost": 3,
    "failureLoss": 13,
    "module": "cell-0-elastic-tray"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-exp-d3-suspension-1-trace-threshold）

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
        "displacement": 0.024995151978505815
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.016497226250901408
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.009740811859584688
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.005026268528015397
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.00258364457571099
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0015926704128136013
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.000878086498211033
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0005121817127218718
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.00027861862379473625
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.00010289875148899049
      },
      {
        "time": 1,
        "displacement": 0.00013120010775369729
      }
    ],
    "threshold": 0.029994182374206976
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-exp-d3-suspension-1-guarded-repair）

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
        "id": "release:cell-0-elastic-tray",
        "label": "release cell-0-elastic-tray",
        "requires": [
          "done:relock:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:release:cell-0-elastic-tray"
        ],
        "adds": [
          "done:release:cell-0-elastic-tray",
          "ready:cell-0-elastic-tray",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "relock:cell-0-elastic-tray",
        "label": "relock cell-0-elastic-tray",
        "requires": [
          "done:verify:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:relock:cell-0-elastic-tray"
        ],
        "adds": [
          "done:relock:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "verify:cell-0-elastic-tray",
        "label": "verify cell-0-elastic-tray",
        "requires": [
          "done:replace:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:verify:cell-0-elastic-tray"
        ],
        "adds": [
          "done:verify:cell-0-elastic-tray"
        ],
        "deletes": [
          "fault:cell-0-elastic-tray",
          "misaligned:cell-0-elastic-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "replace:cell-0-elastic-tray",
        "label": "replace cell-0-elastic-tray",
        "requires": [
          "done:unlock:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:replace:cell-0-elastic-tray"
        ],
        "adds": [
          "done:replace:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "unlock:cell-0-elastic-tray",
        "label": "unlock cell-0-elastic-tray",
        "requires": [
          "done:support:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:unlock:cell-0-elastic-tray"
        ],
        "adds": [
          "done:unlock:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "support:cell-0-elastic-tray",
        "label": "support cell-0-elastic-tray",
        "requires": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:support:cell-0-elastic-tray"
        ],
        "adds": [
          "done:support:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "isolate:cell-0-elastic-tray",
        "label": "isolate cell-0-elastic-tray",
        "requires": [
          "tool:free",
          "fault:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "adds": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-elastic-tray"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-pedestal",
      "cell-1-rotor",
      "cell-1-offset-load",
      "cell-1-upper-stage",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "goalFacts": [
      "ready:cell-0-elastic-tray"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-elastic-tray",
      "support:cell-0-elastic-tray",
      "unlock:cell-0-elastic-tray",
      "replace:cell-0-elastic-tray",
      "verify:cell-0-elastic-tray",
      "relock:cell-0-elastic-tray",
      "release:cell-0-elastic-tray"
    ]
  }
}
```

### 失败状态回退（h3-exp-d3-suspension-1-rollback）

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
        "id": "resume:cell-0-elastic-tray",
        "label": "resume cell-0-elastic-tray",
        "requires": [
          "done:verify:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:resume:cell-0-elastic-tray"
        ],
        "adds": [
          "done:resume:cell-0-elastic-tray",
          "ready:cell-0-elastic-tray",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "verify:cell-0-elastic-tray",
        "label": "verify cell-0-elastic-tray",
        "requires": [
          "done:align:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:verify:cell-0-elastic-tray"
        ],
        "adds": [
          "done:verify:cell-0-elastic-tray"
        ],
        "deletes": [
          "fault:cell-0-elastic-tray",
          "misaligned:cell-0-elastic-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "align:cell-0-elastic-tray",
        "label": "align cell-0-elastic-tray",
        "requires": [
          "done:undo:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:align:cell-0-elastic-tray"
        ],
        "adds": [
          "done:align:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
          "visible": true
        }
      },
      {
        "id": "undo:cell-0-elastic-tray",
        "label": "undo cell-0-elastic-tray",
        "requires": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:undo:cell-0-elastic-tray"
        ],
        "adds": [
          "done:undo:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
          "visible": false
        }
      },
      {
        "id": "isolate:cell-0-elastic-tray",
        "label": "isolate cell-0-elastic-tray",
        "requires": [
          "tool:free",
          "fault:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "adds": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-elastic-tray",
      "misaligned:cell-0-elastic-tray"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-pedestal",
      "cell-1-rotor",
      "cell-1-offset-load",
      "cell-1-upper-stage",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "goalFacts": [
      "ready:cell-0-elastic-tray"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-elastic-tray",
      "undo:cell-0-elastic-tray",
      "align:cell-0-elastic-tray",
      "verify:cell-0-elastic-tray",
      "resume:cell-0-elastic-tray"
    ]
  }
}
```

### 共享工具协同维修（h3-exp-d3-suspension-1-resource-repair）

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
        "id": "release:cell-1-upper-stage",
        "label": "release cell-1-upper-stage",
        "requires": [
          "done:relock:cell-1-upper-stage"
        ],
        "forbids": [
          "done:release:cell-1-upper-stage"
        ],
        "adds": [
          "done:release:cell-1-upper-stage",
          "ready:cell-1-upper-stage",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-upper-stage"
        }
      },
      {
        "id": "relock:cell-1-upper-stage",
        "label": "relock cell-1-upper-stage",
        "requires": [
          "done:verify:cell-1-upper-stage"
        ],
        "forbids": [
          "done:relock:cell-1-upper-stage"
        ],
        "adds": [
          "done:relock:cell-1-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-upper-stage"
        }
      },
      {
        "id": "verify:cell-1-upper-stage",
        "label": "verify cell-1-upper-stage",
        "requires": [
          "done:replace:cell-1-upper-stage"
        ],
        "forbids": [
          "done:verify:cell-1-upper-stage"
        ],
        "adds": [
          "done:verify:cell-1-upper-stage"
        ],
        "deletes": [
          "fault:cell-1-upper-stage",
          "misaligned:cell-1-upper-stage"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-upper-stage"
        }
      },
      {
        "id": "replace:cell-1-upper-stage",
        "label": "replace cell-1-upper-stage",
        "requires": [
          "done:unlock:cell-1-upper-stage"
        ],
        "forbids": [
          "done:replace:cell-1-upper-stage"
        ],
        "adds": [
          "done:replace:cell-1-upper-stage"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-1-upper-stage"
        }
      },
      {
        "id": "unlock:cell-1-upper-stage",
        "label": "unlock cell-1-upper-stage",
        "requires": [
          "done:support:cell-1-upper-stage"
        ],
        "forbids": [
          "done:unlock:cell-1-upper-stage"
        ],
        "adds": [
          "done:unlock:cell-1-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-upper-stage"
        }
      },
      {
        "id": "support:cell-1-upper-stage",
        "label": "support cell-1-upper-stage",
        "requires": [
          "done:isolate:cell-1-upper-stage"
        ],
        "forbids": [
          "done:support:cell-1-upper-stage"
        ],
        "adds": [
          "done:support:cell-1-upper-stage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-upper-stage"
        }
      },
      {
        "id": "isolate:cell-1-upper-stage",
        "label": "isolate cell-1-upper-stage",
        "requires": [
          "tool:free",
          "fault:cell-1-upper-stage"
        ],
        "forbids": [
          "done:isolate:cell-1-upper-stage"
        ],
        "adds": [
          "done:isolate:cell-1-upper-stage"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-1-upper-stage"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-1-upper-stage",
      "fault:cell-1-console",
      "fault:cell-1-magazine",
      "fault:cell-1-drawer"
    ],
    "initialModules": [
      "foundation",
      "cell-0-shuttle",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument",
      "cell-0-console",
      "cell-0-magazine",
      "cell-0-drawer",
      "cell-1-shuttle",
      "cell-1-mount",
      "cell-1-pedestal",
      "cell-1-rotor",
      "cell-1-offset-load",
      "cell-1-upper-stage",
      "cell-1-console",
      "cell-1-magazine",
      "cell-1-drawer"
    ],
    "goalFacts": [
      "ready:cell-1-upper-stage",
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
      "isolate:cell-1-upper-stage",
      "support:cell-1-upper-stage",
      "unlock:cell-1-upper-stage",
      "replace:cell-1-upper-stage",
      "verify:cell-1-upper-stage",
      "relock:cell-1-upper-stage",
      "release:cell-1-upper-stage"
    ]
  }
}
```

### 预算约束检查策略（h3-exp-d3-suspension-1-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-elastic-tray",
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
        "cost": 2,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "probe",
        "cost": 1,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "thermal",
        "cost": 0,
        "returns": {
          "nominal": "clear",
          "fault": "clear"
        }
      }
    ],
    "budget": 1
  },
  "answer": {
    "queryId": "probe",
    "decisions": {
      "clear": "continue",
      "alert": "replace"
    }
  }
}
```
