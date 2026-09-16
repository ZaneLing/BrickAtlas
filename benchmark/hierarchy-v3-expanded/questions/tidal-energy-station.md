## D4 潮汐能维护站

### 模块识别（h3-tidal-energy-station-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：mast
- B：primary-boom
- C：service-cartridge
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
        "id": "mast",
        "name": "mast"
      },
      {
        "id": "primary-boom",
        "name": "primary boom"
      },
      {
        "id": "tool-head",
        "name": "tool head"
      },
      {
        "id": "control-cab",
        "name": "control cab"
      },
      {
        "id": "service-cartridge",
        "name": "service cartridge"
      },
      {
        "id": "secondary-boom",
        "name": "secondary boom"
      },
      {
        "id": "clamp",
        "name": "clamp"
      },
      {
        "id": "sliding-tray",
        "name": "sliding tray"
      },
      {
        "id": "station-0",
        "name": "station 0"
      },
      {
        "id": "station-0-machine",
        "name": "station 0 machine"
      },
      {
        "id": "station-0-transfer",
        "name": "station 0 transfer"
      },
      {
        "id": "station-1",
        "name": "station 1"
      },
      {
        "id": "station-1-machine",
        "name": "station 1 machine"
      },
      {
        "id": "station-1-transfer",
        "name": "station 1 transfer"
      },
      {
        "id": "station-2",
        "name": "station 2"
      },
      {
        "id": "station-2-machine",
        "name": "station 2 machine"
      },
      {
        "id": "station-2-transfer",
        "name": "station 2 transfer"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 部件计数（h3-tidal-energy-station-count）

模块 service-cartridge 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：3
- B：7
- C：4
- D：5

```json
{
  "input": {
    "parts": [
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
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p113",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p114",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p115",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p116",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p117",
        "moduleId": "foundation",
        "shape": "plate",
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
        "id": "mast-p121",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p122",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p123",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p124",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p125",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p126",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p127",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p128",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p129",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p130",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p131",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p132",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p133",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p134",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p135",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p136",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p137",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p138",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p139",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p140",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p141",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p142",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p143",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p144",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p145",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p146",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p147",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p148",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p149",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p150",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p151",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p152",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p153",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p154",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p155",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p156",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p157",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p158",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p159",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p160",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p161",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p162",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p163",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p164",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p165",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p166",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p167",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p168",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p169",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "mast-p170",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "mast-p171",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "mast-p172",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "primary-boom-p173",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p174",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p175",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p176",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p177",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p178",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p179",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p180",
        "moduleId": "primary-boom",
        "shape": "gear",
        "color": "#273e50"
      },
      {
        "id": "tool-head-p181",
        "moduleId": "tool-head",
        "shape": "gear",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p182",
        "moduleId": "tool-head",
        "shape": "axle",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p183",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p184",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p185",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p186",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p187",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p188",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p189",
        "moduleId": "control-cab",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "control-cab-p190",
        "moduleId": "control-cab",
        "shape": "slope",
        "color": "#387bb3"
      },
      {
        "id": "service-cartridge-p191",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p192",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p193",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p194",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "secondary-boom-p195",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p196",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p197",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p198",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p199",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p200",
        "moduleId": "secondary-boom",
        "shape": "gear",
        "color": "#273e50"
      },
      {
        "id": "clamp-p201",
        "moduleId": "clamp",
        "shape": "arch",
        "color": "#e9ad37"
      },
      {
        "id": "sliding-tray-p202",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p203",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p204",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p205",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p206",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p207",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p208",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p209",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-0-p210",
        "moduleId": "station-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "station-0-p211",
        "moduleId": "station-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "station-0-p212",
        "moduleId": "station-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "station-0-p213",
        "moduleId": "station-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "station-0-p214",
        "moduleId": "station-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "station-0-p215",
        "moduleId": "station-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "station-0-p216",
        "moduleId": "station-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "station-0-p217",
        "moduleId": "station-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "station-0-p218",
        "moduleId": "station-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "station-0-p219",
        "moduleId": "station-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "station-0-p220",
        "moduleId": "station-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "station-0-p221",
        "moduleId": "station-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "station-0-machine-p222",
        "moduleId": "station-0-machine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "station-0-machine-p223",
        "moduleId": "station-0-machine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "station-0-machine-p224",
        "moduleId": "station-0-machine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "station-0-machine-p225",
        "moduleId": "station-0-machine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "station-0-machine-p226",
        "moduleId": "station-0-machine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "station-0-machine-p227",
        "moduleId": "station-0-machine",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "station-0-transfer-p228",
        "moduleId": "station-0-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-0-transfer-p229",
        "moduleId": "station-0-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-0-transfer-p230",
        "moduleId": "station-0-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-0-transfer-p231",
        "moduleId": "station-0-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-0-transfer-p232",
        "moduleId": "station-0-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-0-transfer-p233",
        "moduleId": "station-0-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-0-transfer-p234",
        "moduleId": "station-0-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-0-transfer-p235",
        "moduleId": "station-0-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-1-p236",
        "moduleId": "station-1",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "station-1-p237",
        "moduleId": "station-1",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "station-1-p238",
        "moduleId": "station-1",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "station-1-p239",
        "moduleId": "station-1",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "station-1-p240",
        "moduleId": "station-1",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "station-1-p241",
        "moduleId": "station-1",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "station-1-p242",
        "moduleId": "station-1",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "station-1-p243",
        "moduleId": "station-1",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "station-1-p244",
        "moduleId": "station-1",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "station-1-p245",
        "moduleId": "station-1",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "station-1-p246",
        "moduleId": "station-1",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "station-1-p247",
        "moduleId": "station-1",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "station-1-machine-p248",
        "moduleId": "station-1-machine",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "station-1-machine-p249",
        "moduleId": "station-1-machine",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "station-1-machine-p250",
        "moduleId": "station-1-machine",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "station-1-machine-p251",
        "moduleId": "station-1-machine",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "station-1-machine-p252",
        "moduleId": "station-1-machine",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "station-1-machine-p253",
        "moduleId": "station-1-machine",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "station-1-transfer-p254",
        "moduleId": "station-1-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-1-transfer-p255",
        "moduleId": "station-1-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-1-transfer-p256",
        "moduleId": "station-1-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-1-transfer-p257",
        "moduleId": "station-1-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-1-transfer-p258",
        "moduleId": "station-1-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-1-transfer-p259",
        "moduleId": "station-1-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-1-transfer-p260",
        "moduleId": "station-1-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-1-transfer-p261",
        "moduleId": "station-1-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-2-p262",
        "moduleId": "station-2",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-2-p263",
        "moduleId": "station-2",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-2-p264",
        "moduleId": "station-2",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-2-p265",
        "moduleId": "station-2",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-2-p266",
        "moduleId": "station-2",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-2-p267",
        "moduleId": "station-2",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-2-p268",
        "moduleId": "station-2",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-2-p269",
        "moduleId": "station-2",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-2-p270",
        "moduleId": "station-2",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-2-p271",
        "moduleId": "station-2",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-2-p272",
        "moduleId": "station-2",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-2-p273",
        "moduleId": "station-2",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "station-2-machine-p274",
        "moduleId": "station-2-machine",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "station-2-machine-p275",
        "moduleId": "station-2-machine",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "station-2-machine-p276",
        "moduleId": "station-2-machine",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "station-2-machine-p277",
        "moduleId": "station-2-machine",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "station-2-machine-p278",
        "moduleId": "station-2-machine",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "station-2-machine-p279",
        "moduleId": "station-2-machine",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "station-2-transfer-p280",
        "moduleId": "station-2-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-2-transfer-p281",
        "moduleId": "station-2-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-2-transfer-p282",
        "moduleId": "station-2-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-2-transfer-p283",
        "moduleId": "station-2-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-2-transfer-p284",
        "moduleId": "station-2-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-2-transfer-p285",
        "moduleId": "station-2-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-2-transfer-p286",
        "moduleId": "station-2-transfer",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "station-2-transfer-p287",
        "moduleId": "station-2-transfer",
        "shape": "plate",
        "color": "#273e50"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 颜色识别（h3-tidal-energy-station-color）

零件 service-cartridge-p191 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#f2bf3c
- B：#dc6040
- C：#2878b8
- D：#d43a32

```json
{
  "input": {
    "part": {
      "id": "service-cartridge-p191",
      "moduleId": "service-cartridge",
      "shape": "plate",
      "position": [
        -0.5,
        -0.04999999999999999,
        -0.5
      ],
      "size": [
        0.98,
        0.28,
        0.98
      ],
      "color": "#dc6040",
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

### 三维位置（h3-tidal-energy-station-position）

模块 service-cartridge 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,0.35,0]
- B：[-1.6,4.25,-0.6000000000000001]
- C：[1.0444254541136477,10.018152420076138,-0.6]
- D：[2,0.8500000000000001,-2]

```json
{
  "input": {
    "centers": {
      "foundation": [
        0,
        0.35,
        0
      ],
      "mast": [
        -1.6,
        4.25,
        -0.6000000000000001
      ],
      "primary-boom": [
        1.0444254541136477,
        10.018152420076138,
        -0.6
      ],
      "tool-head": [
        3.972586589843391,
        11.336304840152277,
        0.6
      ],
      "control-cab": [
        2,
        2.1550000000000002,
        1.7999999999999998
      ],
      "service-cartridge": [
        2,
        0.8500000000000001,
        -2
      ],
      "secondary-boom": [
        1.8640575845044298,
        4.245907943882797,
        4
      ],
      "clamp": [
        0.7192658172642878,
        6.546487134128409,
        4.8
      ],
      "sliding-tray": [
        0,
        1.85,
        3.9000000000000004
      ],
      "station-0": [
        4.683914244512008,
        0.75,
        5.20201377834176
      ],
      "station-0-machine": [
        4.690919496891695,
        1.5,
        5.16727498485554
      ],
      "station-0-transfer": [
        8.029567276306299,
        1.05,
        8.917737905728732
      ],
      "station-1": [
        -6.84703320513664,
        0.75,
        1.4553818357243151
      ],
      "station-1-machine": [
        -6.840027952756952,
        1.5,
        1.4206430422380951
      ],
      "station-1-transfer": [
        -11.737771208805668,
        1.05,
        2.494940289813112
      ],
      "station-2": [
        2.1631189606246304,
        0.75,
        -6.6573956140660755
      ],
      "station-2-machine": [
        2.1701242130043186,
        1.5,
        -6.692134407552295
      ],
      "station-2-transfer": [
        3.7082039324993668,
        1.05,
        -11.412678195541844
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节类型（h3-tidal-energy-station-joint-type）

primary-boom-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：fixed
- B：prismatic
- C：spring
- D：revolute

```json
{
  "input": {
    "joint": {
      "id": "primary-boom-joint",
      "name": "primary-boom interface",
      "parent": "mast",
      "child": "primary-boom",
      "type": "revolute",
      "anchorParent": [
        0,
        3.65,
        0
      ],
      "anchorChild": [
        -2.644425454113648,
        -2.1181524200761386,
        0
      ],
      "axis": [
        0,
        0,
        1
      ],
      "limits": [
        -0.8,
        0.8
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 直接连接（h3-tidal-energy-station-parent）

service-cartridge 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray","station-0","station-0-machine","station-0-transfer","station-1","station-1-machine","station-1-transfer","station-2","station-2-machine","station-2-transfer"]
- B：["foundation"]
- C：["service-cartridge"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -3.35,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          3.65,
          0
        ],
        "anchorChild": [
          -2.644425454113648,
          -2.1181524200761386,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.9281611357297432,
          2.1181524200761386,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.9359424154955699,
          -2.2459079438827967,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -1.1447917672401422,
          2.300579190245612,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-joint",
        "name": "station-0 interface",
        "parent": "foundation",
        "child": "station-0",
        "type": "fixed",
        "anchorParent": [
          4.683914244512008,
          0.35,
          5.20201377834176
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-0-machine-joint",
        "name": "station-0-machine interface",
        "parent": "station-0",
        "child": "station-0-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-transfer-joint",
        "name": "station-0-transfer interface",
        "parent": "station-0",
        "child": "station-0-transfer",
        "type": "prismatic",
        "anchorParent": [
          3.345653031794291,
          0.25000000000000006,
          3.715724127386972
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.6691306063588582,
          0,
          0.7431448254773942
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-joint",
        "name": "station-1 interface",
        "parent": "foundation",
        "child": "station-1",
        "type": "fixed",
        "anchorParent": [
          -6.84703320513664,
          0.35,
          1.4553818357243151
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-1-machine-joint",
        "name": "station-1-machine interface",
        "parent": "station-1",
        "child": "station-1-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-transfer-joint",
        "name": "station-1-transfer interface",
        "parent": "station-1",
        "child": "station-1-transfer",
        "type": "prismatic",
        "anchorParent": [
          -4.8907380036690284,
          0.25000000000000006,
          1.0395584540887968
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          -0.9781476007338057,
          0,
          0.20791169081775931
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-joint",
        "name": "station-2 interface",
        "parent": "foundation",
        "child": "station-2",
        "type": "fixed",
        "anchorParent": [
          2.1631189606246304,
          0.35,
          -6.6573956140660755
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-2-machine-joint",
        "name": "station-2-machine interface",
        "parent": "station-2",
        "child": "station-2-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-transfer-joint",
        "name": "station-2-transfer interface",
        "parent": "station-2",
        "child": "station-2-transfer",
        "type": "prismatic",
        "anchorParent": [
          1.5450849718747364,
          0.25000000000000006,
          -4.755282581475768
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.30901699437494723,
          0,
          -0.9510565162951536
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 基座识别（h3-tidal-energy-station-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["service-cartridge"]
- B：["foundation"]
- C：[]
- D：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray","station-0","station-0-machine","station-0-transfer","station-1","station-1-machine","station-1-transfer","station-2","station-2-machine","station-2-transfer"]

```json
{
  "input": {
    "modules": [
      {
        "id": "foundation",
        "name": "foundation",
        "role": "frame",
        "position": [
          0,
          0.35,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": true,
        "mass": 10
      },
      {
        "id": "mast",
        "name": "mast",
        "role": "frame",
        "position": [
          -1.6,
          4.25,
          -0.6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 10
      },
      {
        "id": "primary-boom",
        "name": "primary boom",
        "role": "actuator",
        "position": [
          1.044425454113648,
          10.018152420076138,
          -0.6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "tool-head",
        "name": "tool head",
        "role": "tool",
        "position": [
          3.972586589843391,
          11.336304840152277,
          0.6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "control-cab",
        "name": "control cab",
        "role": "control",
        "position": [
          2,
          2.155,
          1.8
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "service-cartridge",
        "name": "service cartridge",
        "role": "service",
        "position": [
          2,
          0.8500000000000001,
          -2
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "secondary-boom",
        "name": "secondary boom",
        "role": "actuator",
        "position": [
          1.86405758450443,
          4.245907943882797,
          4
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "clamp",
        "name": "clamp",
        "role": "tool",
        "position": [
          0.7192658172642878,
          6.546487134128409,
          4.8
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "sliding-tray",
        "name": "sliding tray",
        "role": "payload",
        "position": [
          0,
          1.85,
          3.9
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "station-0",
        "name": "station 0",
        "role": "workcell",
        "position": [
          4.683914244512008,
          0.75,
          5.20201377834176
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "station-0-machine",
        "name": "station 0 machine",
        "role": "processor",
        "position": [
          4.690919496891696,
          1.5,
          5.16727498485554
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "station-0-transfer",
        "name": "station 0 transfer",
        "role": "transport",
        "position": [
          8.029567276306299,
          1.05,
          8.917737905728732
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "station-1",
        "name": "station 1",
        "role": "workcell",
        "position": [
          -6.84703320513664,
          0.75,
          1.4553818357243151
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "station-1-machine",
        "name": "station 1 machine",
        "role": "processor",
        "position": [
          -6.840027952756952,
          1.5,
          1.4206430422380953
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "station-1-transfer",
        "name": "station 1 transfer",
        "role": "transport",
        "position": [
          -11.737771208805668,
          1.05,
          2.494940289813112
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "station-2",
        "name": "station 2",
        "role": "workcell",
        "position": [
          2.1631189606246304,
          0.75,
          -6.6573956140660755
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "station-2-machine",
        "name": "station 2 machine",
        "role": "processor",
        "position": [
          2.1701242130043186,
          1.5,
          -6.692134407552295
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "station-2-transfer",
        "name": "station 2 transfer",
        "role": "transport",
        "position": [
          3.7082039324993668,
          1.05,
          -11.412678195541844
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 接口计数（h3-tidal-energy-station-degree）

service-cartridge 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：0
- B：3
- C：1
- D：2

```json
{
  "input": {
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -3.35,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          3.65,
          0
        ],
        "anchorChild": [
          -2.644425454113648,
          -2.1181524200761386,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.9281611357297432,
          2.1181524200761386,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.9359424154955699,
          -2.2459079438827967,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -1.1447917672401422,
          2.300579190245612,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-joint",
        "name": "station-0 interface",
        "parent": "foundation",
        "child": "station-0",
        "type": "fixed",
        "anchorParent": [
          4.683914244512008,
          0.35,
          5.20201377834176
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-0-machine-joint",
        "name": "station-0-machine interface",
        "parent": "station-0",
        "child": "station-0-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-transfer-joint",
        "name": "station-0-transfer interface",
        "parent": "station-0",
        "child": "station-0-transfer",
        "type": "prismatic",
        "anchorParent": [
          3.345653031794291,
          0.25000000000000006,
          3.715724127386972
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.6691306063588582,
          0,
          0.7431448254773942
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-joint",
        "name": "station-1 interface",
        "parent": "foundation",
        "child": "station-1",
        "type": "fixed",
        "anchorParent": [
          -6.84703320513664,
          0.35,
          1.4553818357243151
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-1-machine-joint",
        "name": "station-1-machine interface",
        "parent": "station-1",
        "child": "station-1-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-transfer-joint",
        "name": "station-1-transfer interface",
        "parent": "station-1",
        "child": "station-1-transfer",
        "type": "prismatic",
        "anchorParent": [
          -4.8907380036690284,
          0.25000000000000006,
          1.0395584540887968
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          -0.9781476007338057,
          0,
          0.20791169081775931
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-joint",
        "name": "station-2 interface",
        "parent": "foundation",
        "child": "station-2",
        "type": "fixed",
        "anchorParent": [
          2.1631189606246304,
          0.35,
          -6.6573956140660755
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-2-machine-joint",
        "name": "station-2-machine interface",
        "parent": "station-2",
        "child": "station-2-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-transfer-joint",
        "name": "station-2-transfer interface",
        "parent": "station-2",
        "child": "station-2-transfer",
        "type": "prismatic",
        "anchorParent": [
          1.5450849718747364,
          0.25000000000000006,
          -4.755282581475768
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.30901699437494723,
          0,
          -0.9510565162951536
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 局部改色（h3-tidal-energy-station-recolor）

仅将 service-cartridge-p191 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"service-cartridge-p191","color":"#2878b8"}
- B：{"id":"*","color":"#e8792e"}
- C：{"id":"service-cartridge-p191","color":"#e8792e"}
- D：{"id":"service-cartridge-p192","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "service-cartridge-p191",
      "moduleId": "service-cartridge",
      "shape": "plate",
      "position": [
        -0.5,
        -0.04999999999999999,
        -0.5
      ],
      "size": [
        0.98,
        0.28,
        0.98
      ],
      "color": "#dc6040",
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

### 补装部件（h3-tidal-energy-station-add）

模块 service-cartridge 缺失零件 service-cartridge-p191。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"service-cartridge-p191","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#dc6040","rotation":[0,0,0,1]}
- B：{"id":"service-cartridge-p191","moduleId":"foundation","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#dc6040","rotation":[0,0,0,1]}
- C：{"id":"service-cartridge-p191","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[3,3,3],"color":"#dc6040","rotation":[0,0,0,1]}
- D：{"id":"service-cartridge-p191","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#000000","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "service-cartridge-p191",
      "moduleId": "service-cartridge",
      "shape": "plate",
      "position": [
        -0.5,
        -0.04999999999999999,
        -0.5
      ],
      "size": [
        0.98,
        0.28,
        0.98
      ],
      "color": "#dc6040",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    },
    "existingIds": [
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
      "mast-p121",
      "mast-p122",
      "mast-p123",
      "mast-p124",
      "mast-p125",
      "mast-p126",
      "mast-p127",
      "mast-p128",
      "mast-p129",
      "mast-p130",
      "mast-p131",
      "mast-p132",
      "mast-p133",
      "mast-p134",
      "mast-p135",
      "mast-p136",
      "mast-p137",
      "mast-p138",
      "mast-p139",
      "mast-p140",
      "mast-p141",
      "mast-p142",
      "mast-p143",
      "mast-p144",
      "mast-p145",
      "mast-p146",
      "mast-p147",
      "mast-p148",
      "mast-p149",
      "mast-p150",
      "mast-p151",
      "mast-p152",
      "mast-p153",
      "mast-p154",
      "mast-p155",
      "mast-p156",
      "mast-p157",
      "mast-p158",
      "mast-p159",
      "mast-p160",
      "mast-p161",
      "mast-p162",
      "mast-p163",
      "mast-p164",
      "mast-p165",
      "mast-p166",
      "mast-p167",
      "mast-p168",
      "mast-p169",
      "mast-p170",
      "mast-p171",
      "mast-p172",
      "primary-boom-p173",
      "primary-boom-p174",
      "primary-boom-p175",
      "primary-boom-p176",
      "primary-boom-p177",
      "primary-boom-p178",
      "primary-boom-p179",
      "primary-boom-p180",
      "tool-head-p181",
      "tool-head-p182",
      "control-cab-p183",
      "control-cab-p184",
      "control-cab-p185",
      "control-cab-p186",
      "control-cab-p187",
      "control-cab-p188",
      "control-cab-p189",
      "control-cab-p190",
      "service-cartridge-p192",
      "service-cartridge-p193",
      "service-cartridge-p194",
      "secondary-boom-p195",
      "secondary-boom-p196",
      "secondary-boom-p197",
      "secondary-boom-p198",
      "secondary-boom-p199",
      "secondary-boom-p200",
      "clamp-p201",
      "sliding-tray-p202",
      "sliding-tray-p203",
      "sliding-tray-p204",
      "sliding-tray-p205",
      "sliding-tray-p206",
      "sliding-tray-p207",
      "sliding-tray-p208",
      "sliding-tray-p209",
      "station-0-p210",
      "station-0-p211",
      "station-0-p212",
      "station-0-p213",
      "station-0-p214",
      "station-0-p215",
      "station-0-p216",
      "station-0-p217",
      "station-0-p218",
      "station-0-p219",
      "station-0-p220",
      "station-0-p221",
      "station-0-machine-p222",
      "station-0-machine-p223",
      "station-0-machine-p224",
      "station-0-machine-p225",
      "station-0-machine-p226",
      "station-0-machine-p227",
      "station-0-transfer-p228",
      "station-0-transfer-p229",
      "station-0-transfer-p230",
      "station-0-transfer-p231",
      "station-0-transfer-p232",
      "station-0-transfer-p233",
      "station-0-transfer-p234",
      "station-0-transfer-p235",
      "station-1-p236",
      "station-1-p237",
      "station-1-p238",
      "station-1-p239",
      "station-1-p240",
      "station-1-p241",
      "station-1-p242",
      "station-1-p243",
      "station-1-p244",
      "station-1-p245",
      "station-1-p246",
      "station-1-p247",
      "station-1-machine-p248",
      "station-1-machine-p249",
      "station-1-machine-p250",
      "station-1-machine-p251",
      "station-1-machine-p252",
      "station-1-machine-p253",
      "station-1-transfer-p254",
      "station-1-transfer-p255",
      "station-1-transfer-p256",
      "station-1-transfer-p257",
      "station-1-transfer-p258",
      "station-1-transfer-p259",
      "station-1-transfer-p260",
      "station-1-transfer-p261",
      "station-2-p262",
      "station-2-p263",
      "station-2-p264",
      "station-2-p265",
      "station-2-p266",
      "station-2-p267",
      "station-2-p268",
      "station-2-p269",
      "station-2-p270",
      "station-2-p271",
      "station-2-p272",
      "station-2-p273",
      "station-2-machine-p274",
      "station-2-machine-p275",
      "station-2-machine-p276",
      "station-2-machine-p277",
      "station-2-machine-p278",
      "station-2-machine-p279",
      "station-2-transfer-p280",
      "station-2-transfer-p281",
      "station-2-transfer-p282",
      "station-2-transfer-p283",
      "station-2-transfer-p284",
      "station-2-transfer-p285",
      "station-2-transfer-p286",
      "station-2-transfer-p287"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全拆除（h3-tidal-energy-station-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["foundation"]
- B：[]
- C：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray","station-0","station-0-machine","station-0-transfer","station-1","station-1-machine","station-1-transfer","station-2","station-2-machine","station-2-transfer"]
- D：["clamp","service-cartridge","sliding-tray","station-0-machine","station-0-transfer","station-1-machine","station-1-transfer","station-2-machine","station-2-transfer","tool-head"]

```json
{
  "input": {
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -3.35,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          3.65,
          0
        ],
        "anchorChild": [
          -2.644425454113648,
          -2.1181524200761386,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.9281611357297432,
          2.1181524200761386,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.9359424154955699,
          -2.2459079438827967,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -1.1447917672401422,
          2.300579190245612,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-joint",
        "name": "station-0 interface",
        "parent": "foundation",
        "child": "station-0",
        "type": "fixed",
        "anchorParent": [
          4.683914244512008,
          0.35,
          5.20201377834176
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-0-machine-joint",
        "name": "station-0-machine interface",
        "parent": "station-0",
        "child": "station-0-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-transfer-joint",
        "name": "station-0-transfer interface",
        "parent": "station-0",
        "child": "station-0-transfer",
        "type": "prismatic",
        "anchorParent": [
          3.345653031794291,
          0.25000000000000006,
          3.715724127386972
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.6691306063588582,
          0,
          0.7431448254773942
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-joint",
        "name": "station-1 interface",
        "parent": "foundation",
        "child": "station-1",
        "type": "fixed",
        "anchorParent": [
          -6.84703320513664,
          0.35,
          1.4553818357243151
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-1-machine-joint",
        "name": "station-1-machine interface",
        "parent": "station-1",
        "child": "station-1-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-transfer-joint",
        "name": "station-1-transfer interface",
        "parent": "station-1",
        "child": "station-1-transfer",
        "type": "prismatic",
        "anchorParent": [
          -4.8907380036690284,
          0.25000000000000006,
          1.0395584540887968
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          -0.9781476007338057,
          0,
          0.20791169081775931
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-joint",
        "name": "station-2 interface",
        "parent": "foundation",
        "child": "station-2",
        "type": "fixed",
        "anchorParent": [
          2.1631189606246304,
          0.35,
          -6.6573956140660755
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-2-machine-joint",
        "name": "station-2-machine interface",
        "parent": "station-2",
        "child": "station-2-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-transfer-joint",
        "name": "station-2-transfer interface",
        "parent": "station-2",
        "child": "station-2-transfer",
        "type": "prismatic",
        "anchorParent": [
          1.5450849718747364,
          0.25000000000000006,
          -4.755282581475768
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.30901699437494723,
          0,
          -0.9510565162951536
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ],
    "modules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "station-0",
      "station-0-machine",
      "station-0-transfer",
      "station-1",
      "station-1-machine",
      "station-1-transfer",
      "station-2",
      "station-2-machine",
      "station-2-transfer"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 替换选择（h3-tidal-energy-station-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-1
- B：stock-2
- C：stock-3
- D：stock-0

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 3,
        "stiffness": 11,
        "mass": 1.2
      },
      {
        "id": "stock-1",
        "cost": 7,
        "stiffness": 11,
        "mass": 0.8
      },
      {
        "id": "stock-2",
        "cost": 6,
        "stiffness": 11,
        "mass": 0.5
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 9,
        "mass": 0.5
      }
    ],
    "maxCost": 6
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-tidal-energy-station-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[-4,0,2]
- B：[4,0,-2]
- C：[0,0,0]
- D：[0,2,0]

```json
{
  "input": {
    "delta": [
      4,
      0,
      -2
    ],
    "target": "service-cartridge"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 姿态纠偏（h3-tidal-energy-station-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：-90
- B：-180
- C：0
- D：90

```json
{
  "input": {
    "module": "service-cartridge",
    "currentYaw": 270,
    "targetYaw": 270
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 下一步放置（h3-tidal-energy-station-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray"]
- C：["station-0","station-0-machine","station-0-transfer","station-1","station-1-machine","station-1-transfer","station-2","station-2-machine","station-2-transfer"]
- D：["station-0","station-1","station-2"]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray"
    ],
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -3.35,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          3.65,
          0
        ],
        "anchorChild": [
          -2.644425454113648,
          -2.1181524200761386,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.9281611357297432,
          2.1181524200761386,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.9359424154955699,
          -2.2459079438827967,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -1.1447917672401422,
          2.300579190245612,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-joint",
        "name": "station-0 interface",
        "parent": "foundation",
        "child": "station-0",
        "type": "fixed",
        "anchorParent": [
          4.683914244512008,
          0.35,
          5.20201377834176
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-0-machine-joint",
        "name": "station-0-machine interface",
        "parent": "station-0",
        "child": "station-0-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-transfer-joint",
        "name": "station-0-transfer interface",
        "parent": "station-0",
        "child": "station-0-transfer",
        "type": "prismatic",
        "anchorParent": [
          3.345653031794291,
          0.25000000000000006,
          3.715724127386972
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.6691306063588582,
          0,
          0.7431448254773942
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-joint",
        "name": "station-1 interface",
        "parent": "foundation",
        "child": "station-1",
        "type": "fixed",
        "anchorParent": [
          -6.84703320513664,
          0.35,
          1.4553818357243151
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-1-machine-joint",
        "name": "station-1-machine interface",
        "parent": "station-1",
        "child": "station-1-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-transfer-joint",
        "name": "station-1-transfer interface",
        "parent": "station-1",
        "child": "station-1-transfer",
        "type": "prismatic",
        "anchorParent": [
          -4.8907380036690284,
          0.25000000000000006,
          1.0395584540887968
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          -0.9781476007338057,
          0,
          0.20791169081775931
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-joint",
        "name": "station-2 interface",
        "parent": "foundation",
        "child": "station-2",
        "type": "fixed",
        "anchorParent": [
          2.1631189606246304,
          0.35,
          -6.6573956140660755
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-2-machine-joint",
        "name": "station-2-machine interface",
        "parent": "station-2",
        "child": "station-2-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-transfer-joint",
        "name": "station-2-transfer interface",
        "parent": "station-2",
        "child": "station-2-transfer",
        "type": "prismatic",
        "anchorParent": [
          1.5450849718747364,
          0.25000000000000006,
          -4.755282581475768
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.30901699437494723,
          0,
          -0.9510565162951536
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ],
    "modules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "station-0",
      "station-0-machine",
      "station-0-transfer",
      "station-1",
      "station-1-machine",
      "station-1-transfer",
      "station-2",
      "station-2-machine",
      "station-2-transfer"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 库存核算（h3-tidal-energy-station-inventory）

备件库有 7 件，替换模块需 4 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：6
- B：3
- C：4
- D：2

```json
{
  "input": {
    "available": 7,
    "required": 4
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 子装配边界（h3-tidal-energy-station-boundary）

隔离 service-cartridge 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["primary-boom-joint"]
- B：["service-cartridge-joint"]
- C：[]
- D：["mast-joint","primary-boom-joint","tool-head-joint","control-cab-joint","service-cartridge-joint","secondary-boom-joint","clamp-joint","sliding-tray-joint","station-0-joint","station-0-machine-joint","station-0-transfer-joint","station-1-joint","station-1-machine-joint","station-1-transfer-joint","station-2-joint","station-2-machine-joint","station-2-transfer-joint"]

```json
{
  "input": {
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -3.35,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          3.65,
          0
        ],
        "anchorChild": [
          -2.644425454113648,
          -2.1181524200761386,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.9281611357297432,
          2.1181524200761386,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.9359424154955699,
          -2.2459079438827967,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -1.1447917672401422,
          2.300579190245612,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-joint",
        "name": "station-0 interface",
        "parent": "foundation",
        "child": "station-0",
        "type": "fixed",
        "anchorParent": [
          4.683914244512008,
          0.35,
          5.20201377834176
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-0-machine-joint",
        "name": "station-0-machine interface",
        "parent": "station-0",
        "child": "station-0-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-transfer-joint",
        "name": "station-0-transfer interface",
        "parent": "station-0",
        "child": "station-0-transfer",
        "type": "prismatic",
        "anchorParent": [
          3.345653031794291,
          0.25000000000000006,
          3.715724127386972
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.6691306063588582,
          0,
          0.7431448254773942
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-joint",
        "name": "station-1 interface",
        "parent": "foundation",
        "child": "station-1",
        "type": "fixed",
        "anchorParent": [
          -6.84703320513664,
          0.35,
          1.4553818357243151
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-1-machine-joint",
        "name": "station-1-machine interface",
        "parent": "station-1",
        "child": "station-1-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-transfer-joint",
        "name": "station-1-transfer interface",
        "parent": "station-1",
        "child": "station-1-transfer",
        "type": "prismatic",
        "anchorParent": [
          -4.8907380036690284,
          0.25000000000000006,
          1.0395584540887968
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          -0.9781476007338057,
          0,
          0.20791169081775931
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-joint",
        "name": "station-2 interface",
        "parent": "foundation",
        "child": "station-2",
        "type": "fixed",
        "anchorParent": [
          2.1631189606246304,
          0.35,
          -6.6573956140660755
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-2-machine-joint",
        "name": "station-2-machine interface",
        "parent": "station-2",
        "child": "station-2-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-transfer-joint",
        "name": "station-2-transfer interface",
        "parent": "station-2",
        "child": "station-2-transfer",
        "type": "prismatic",
        "anchorParent": [
          1.5450849718747364,
          0.25000000000000006,
          -4.755282581475768
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.30901699437494723,
          0,
          -0.9510565162951536
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ],
    "target": "service-cartridge"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 最小干预（h3-tidal-energy-station-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：2
- B：4
- C：0
- D：1

```json
{
  "input": {
    "module": "service-cartridge"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 全过程依赖（h3-tidal-energy-station-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：2
- B：17
- C：1
- D：-1

```json
{
  "input": {
    "order": [
      "foundation",
      "primary-boom",
      "mast",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "station-0",
      "station-0-machine",
      "station-0-transfer",
      "station-1",
      "station-1-machine",
      "station-1-transfer",
      "station-2",
      "station-2-machine",
      "station-2-transfer"
    ],
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -3.35,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          3.65,
          0
        ],
        "anchorChild": [
          -2.644425454113648,
          -2.1181524200761386,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.9281611357297432,
          2.1181524200761386,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.9359424154955699,
          -2.2459079438827967,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -1.1447917672401422,
          2.300579190245612,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-joint",
        "name": "station-0 interface",
        "parent": "foundation",
        "child": "station-0",
        "type": "fixed",
        "anchorParent": [
          4.683914244512008,
          0.35,
          5.20201377834176
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-0-machine-joint",
        "name": "station-0-machine interface",
        "parent": "station-0",
        "child": "station-0-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-transfer-joint",
        "name": "station-0-transfer interface",
        "parent": "station-0",
        "child": "station-0-transfer",
        "type": "prismatic",
        "anchorParent": [
          3.345653031794291,
          0.25000000000000006,
          3.715724127386972
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.6691306063588582,
          0,
          0.7431448254773942
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-joint",
        "name": "station-1 interface",
        "parent": "foundation",
        "child": "station-1",
        "type": "fixed",
        "anchorParent": [
          -6.84703320513664,
          0.35,
          1.4553818357243151
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-1-machine-joint",
        "name": "station-1-machine interface",
        "parent": "station-1",
        "child": "station-1-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-transfer-joint",
        "name": "station-1-transfer interface",
        "parent": "station-1",
        "child": "station-1-transfer",
        "type": "prismatic",
        "anchorParent": [
          -4.8907380036690284,
          0.25000000000000006,
          1.0395584540887968
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          -0.9781476007338057,
          0,
          0.20791169081775931
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-joint",
        "name": "station-2 interface",
        "parent": "foundation",
        "child": "station-2",
        "type": "fixed",
        "anchorParent": [
          2.1631189606246304,
          0.35,
          -6.6573956140660755
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-2-machine-joint",
        "name": "station-2-machine interface",
        "parent": "station-2",
        "child": "station-2-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-transfer-joint",
        "name": "station-2-transfer interface",
        "parent": "station-2",
        "child": "station-2-transfer",
        "type": "prismatic",
        "anchorParent": [
          1.5450849718747364,
          0.25000000000000006,
          -4.755282581475768
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.30901699437494723,
          0,
          -0.9510565162951536
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 连续维修路径（h3-tidal-energy-station-access）

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
          14.019567276306299,
          0.8500000000000001,
          -2
        ],
        "end": [
          2,
          0.8500000000000001,
          -2
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
          2,
          16.536304840152276,
          -2
        ],
        "end": [
          2,
          0.8500000000000001,
          -2
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
          2,
          0.8500000000000001,
          13.907737905728732
        ],
        "end": [
          2,
          0.8500000000000001,
          -2
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

### 支撑反事实（h3-tidal-energy-station-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray","station-0","station-0-machine","station-0-transfer","station-1","station-1-machine","station-1-transfer","station-2","station-2-machine","station-2-transfer"]
- C：["primary-boom","tool-head"]
- D：["mast"]

```json
{
  "input": {
    "removed": "mast",
    "roots": [
      "foundation"
    ],
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -3.35,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          3.65,
          0
        ],
        "anchorChild": [
          -2.644425454113648,
          -2.1181524200761386,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.9281611357297432,
          2.1181524200761386,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.9359424154955699,
          -2.2459079438827967,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -1.1447917672401422,
          2.300579190245612,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-joint",
        "name": "station-0 interface",
        "parent": "foundation",
        "child": "station-0",
        "type": "fixed",
        "anchorParent": [
          4.683914244512008,
          0.35,
          5.20201377834176
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-0-machine-joint",
        "name": "station-0-machine interface",
        "parent": "station-0",
        "child": "station-0-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-transfer-joint",
        "name": "station-0-transfer interface",
        "parent": "station-0",
        "child": "station-0-transfer",
        "type": "prismatic",
        "anchorParent": [
          3.345653031794291,
          0.25000000000000006,
          3.715724127386972
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.6691306063588582,
          0,
          0.7431448254773942
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-joint",
        "name": "station-1 interface",
        "parent": "foundation",
        "child": "station-1",
        "type": "fixed",
        "anchorParent": [
          -6.84703320513664,
          0.35,
          1.4553818357243151
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-1-machine-joint",
        "name": "station-1-machine interface",
        "parent": "station-1",
        "child": "station-1-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-transfer-joint",
        "name": "station-1-transfer interface",
        "parent": "station-1",
        "child": "station-1-transfer",
        "type": "prismatic",
        "anchorParent": [
          -4.8907380036690284,
          0.25000000000000006,
          1.0395584540887968
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          -0.9781476007338057,
          0,
          0.20791169081775931
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-joint",
        "name": "station-2 interface",
        "parent": "foundation",
        "child": "station-2",
        "type": "fixed",
        "anchorParent": [
          2.1631189606246304,
          0.35,
          -6.6573956140660755
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-2-machine-joint",
        "name": "station-2-machine interface",
        "parent": "station-2",
        "child": "station-2-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-transfer-joint",
        "name": "station-2-transfer interface",
        "parent": "station-2",
        "child": "station-2-transfer",
        "type": "prismatic",
        "anchorParent": [
          1.5450849718747364,
          0.25000000000000006,
          -4.755282581475768
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.30901699437494723,
          0,
          -0.9510565162951536
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ],
    "modules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "station-0",
      "station-0-machine",
      "station-0-transfer",
      "station-1",
      "station-1-machine",
      "station-1-transfer",
      "station-2",
      "station-2-machine",
      "station-2-transfer"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-tidal-energy-station-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.2126
- B：0
- C：1.0126
- D：0.0126

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.005873355322933528
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.012614477239857366
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.008770120670057472
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0013756763842113176
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0015260327529835285
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0013265273469910837
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00023070690564183543
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0001316624509502049
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0002331639236260605
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.000008427051306687483
      },
      {
        "time": 1,
        "displacement": 0.0000023337330759110322
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.0172973211504919,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节限位推理（h3-tidal-energy-station-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-1.3
- B：1.3
- C：-0.8
- D：0

```json
{
  "input": {
    "joint": "primary-boom-joint",
    "limits": [
      -0.8,
      0.8
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

### 约束故障诊断（h3-tidal-energy-station-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：tool-head-joint
- B：service-cartridge-joint
- C：mast-joint
- D：primary-boom-joint

```json
{
  "input": {
    "endpoints": [
      "foundation",
      "service-cartridge"
    ],
    "type": "fixed",
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -3.35,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          3.65,
          0
        ],
        "anchorChild": [
          -2.644425454113648,
          -2.1181524200761386,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.9281611357297432,
          2.1181524200761386,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.9359424154955699,
          -2.2459079438827967,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -1.1447917672401422,
          2.300579190245612,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-joint",
        "name": "station-0 interface",
        "parent": "foundation",
        "child": "station-0",
        "type": "fixed",
        "anchorParent": [
          4.683914244512008,
          0.35,
          5.20201377834176
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-0-machine-joint",
        "name": "station-0-machine interface",
        "parent": "station-0",
        "child": "station-0-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-0-transfer-joint",
        "name": "station-0-transfer interface",
        "parent": "station-0",
        "child": "station-0-transfer",
        "type": "prismatic",
        "anchorParent": [
          3.345653031794291,
          0.25000000000000006,
          3.715724127386972
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.6691306063588582,
          0,
          0.7431448254773942
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-joint",
        "name": "station-1 interface",
        "parent": "foundation",
        "child": "station-1",
        "type": "fixed",
        "anchorParent": [
          -6.84703320513664,
          0.35,
          1.4553818357243151
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-1-machine-joint",
        "name": "station-1-machine interface",
        "parent": "station-1",
        "child": "station-1-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-1-transfer-joint",
        "name": "station-1-transfer interface",
        "parent": "station-1",
        "child": "station-1-transfer",
        "type": "prismatic",
        "anchorParent": [
          -4.8907380036690284,
          0.25000000000000006,
          1.0395584540887968
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          -0.9781476007338057,
          0,
          0.20791169081775931
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-joint",
        "name": "station-2 interface",
        "parent": "foundation",
        "child": "station-2",
        "type": "fixed",
        "anchorParent": [
          2.1631189606246304,
          0.35,
          -6.6573956140660755
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "station-2-machine-joint",
        "name": "station-2-machine interface",
        "parent": "station-2",
        "child": "station-2-machine",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          -0.007005252379688187,
          0,
          0.03473879348621978
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "station-2-transfer-joint",
        "name": "station-2-transfer interface",
        "parent": "station-2",
        "child": "station-2-transfer",
        "type": "prismatic",
        "anchorParent": [
          1.5450849718747364,
          0.25000000000000006,
          -4.755282581475768
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0.30901699437494723,
          0,
          -0.9510565162951536
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "B"
    ]
  }
}
```

### 主动检查收益（h3-tidal-energy-station-information-gain）

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
    "module": "service-cartridge",
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

### 不确定性与弃答（h3-tidal-energy-station-abstention）

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

### 观测后信念更新（h3-tidal-energy-station-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0
- B：0.25
- C：0.5
- D：0.3333333333333333

```json
{
  "input": {
    "module": "service-cartridge",
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

### 多目标工程权衡（h3-tidal-energy-station-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-2
- B：stock-1
- C：stock-3
- D：stock-0

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 3,
        "stiffness": 11,
        "mass": 1.2
      },
      {
        "id": "stock-1",
        "cost": 7,
        "stiffness": 11,
        "mass": 0.8
      },
      {
        "id": "stock-2",
        "cost": 6,
        "stiffness": 11,
        "mass": 0.5
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 9,
        "mass": 0.5
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "D"
    ]
  }
}
```

### 依赖装配（h3-tidal-energy-station-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
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
        "id": "place:secondary-boom",
        "label": "安装 secondary-boom",
        "requires": [
          "present:control-cab"
        ],
        "forbids": [
          "present:secondary-boom"
        ],
        "adds": [
          "present:secondary-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "secondary-boom",
          "visible": true
        }
      },
      {
        "id": "place:station-2",
        "label": "安装 station-2",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:station-2"
        ],
        "adds": [
          "present:station-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2",
          "visible": true
        }
      },
      {
        "id": "place:station-1-machine",
        "label": "安装 station-1-machine",
        "requires": [
          "present:station-1"
        ],
        "forbids": [
          "present:station-1-machine"
        ],
        "adds": [
          "present:station-1-machine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-machine",
          "visible": true
        }
      },
      {
        "id": "place:control-cab",
        "label": "安装 control-cab",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:control-cab"
        ],
        "adds": [
          "present:control-cab"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "control-cab",
          "visible": true
        }
      },
      {
        "id": "place:station-0",
        "label": "安装 station-0",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:station-0"
        ],
        "adds": [
          "present:station-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-0",
          "visible": true
        }
      },
      {
        "id": "place:station-1",
        "label": "安装 station-1",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:station-1"
        ],
        "adds": [
          "present:station-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1",
          "visible": true
        }
      },
      {
        "id": "place:service-cartridge",
        "label": "安装 service-cartridge",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:service-cartridge"
        ],
        "adds": [
          "present:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "visible": true
        }
      },
      {
        "id": "place:station-0-machine",
        "label": "安装 station-0-machine",
        "requires": [
          "present:station-0"
        ],
        "forbids": [
          "present:station-0-machine"
        ],
        "adds": [
          "present:station-0-machine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-0-machine",
          "visible": true
        }
      },
      {
        "id": "place:station-0-transfer",
        "label": "安装 station-0-transfer",
        "requires": [
          "present:station-0"
        ],
        "forbids": [
          "present:station-0-transfer"
        ],
        "adds": [
          "present:station-0-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-0-transfer",
          "visible": true
        }
      },
      {
        "id": "place:tool-head",
        "label": "安装 tool-head",
        "requires": [
          "present:primary-boom"
        ],
        "forbids": [
          "present:tool-head"
        ],
        "adds": [
          "present:tool-head"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-head",
          "visible": true
        }
      },
      {
        "id": "place:mast",
        "label": "安装 mast",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:mast"
        ],
        "adds": [
          "present:mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "mast",
          "visible": true
        }
      },
      {
        "id": "place:primary-boom",
        "label": "安装 primary-boom",
        "requires": [
          "present:mast"
        ],
        "forbids": [
          "present:primary-boom"
        ],
        "adds": [
          "present:primary-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "primary-boom",
          "visible": true
        }
      },
      {
        "id": "place:station-1-transfer",
        "label": "安装 station-1-transfer",
        "requires": [
          "present:station-1"
        ],
        "forbids": [
          "present:station-1-transfer"
        ],
        "adds": [
          "present:station-1-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer",
          "visible": true
        }
      },
      {
        "id": "place:station-2-transfer",
        "label": "安装 station-2-transfer",
        "requires": [
          "present:station-2"
        ],
        "forbids": [
          "present:station-2-transfer"
        ],
        "adds": [
          "present:station-2-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer",
          "visible": true
        }
      },
      {
        "id": "place:station-2-machine",
        "label": "安装 station-2-machine",
        "requires": [
          "present:station-2"
        ],
        "forbids": [
          "present:station-2-machine"
        ],
        "adds": [
          "present:station-2-machine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine",
          "visible": true
        }
      },
      {
        "id": "place:clamp",
        "label": "安装 clamp",
        "requires": [
          "present:secondary-boom"
        ],
        "forbids": [
          "present:clamp"
        ],
        "adds": [
          "present:clamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "clamp",
          "visible": true
        }
      },
      {
        "id": "place:sliding-tray",
        "label": "安装 sliding-tray",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:sliding-tray"
        ],
        "adds": [
          "present:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:mast",
      "present:primary-boom",
      "present:tool-head",
      "present:control-cab",
      "present:service-cartridge",
      "present:secondary-boom",
      "present:clamp",
      "present:sliding-tray",
      "present:station-0",
      "present:station-0-machine",
      "present:station-0-transfer",
      "present:station-1",
      "present:station-1-machine",
      "present:station-1-transfer",
      "present:station-2",
      "present:station-2-machine",
      "present:station-2-transfer"
    ],
    "budget": 18,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:station-2",
      "place:control-cab",
      "place:secondary-boom",
      "place:station-0",
      "place:station-1",
      "place:station-1-machine",
      "place:service-cartridge",
      "place:station-0-machine",
      "place:station-0-transfer",
      "place:mast",
      "place:primary-boom",
      "place:tool-head",
      "place:station-1-transfer",
      "place:station-2-transfer",
      "place:station-2-machine",
      "place:clamp",
      "place:sliding-tray"
    ]
  }
}
```

### 依赖拆解（h3-tidal-energy-station-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:mast",
      "present:primary-boom",
      "present:tool-head",
      "present:control-cab",
      "present:service-cartridge",
      "present:secondary-boom",
      "present:clamp",
      "present:sliding-tray",
      "present:station-0",
      "present:station-0-machine",
      "present:station-0-transfer",
      "present:station-1",
      "present:station-1-machine",
      "present:station-1-transfer",
      "present:station-2",
      "present:station-2-machine",
      "present:station-2-transfer"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "station-0",
      "station-0-machine",
      "station-0-transfer",
      "station-1",
      "station-1-machine",
      "station-1-transfer",
      "station-2",
      "station-2-machine",
      "station-2-transfer"
    ],
    "actions": [
      {
        "id": "remove:foundation",
        "label": "拆除 foundation",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:mast",
          "present:control-cab",
          "present:service-cartridge",
          "present:sliding-tray",
          "present:station-0",
          "present:station-1",
          "present:station-2"
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
        "id": "remove:sliding-tray",
        "label": "拆除 sliding-tray",
        "requires": [
          "present:sliding-tray"
        ],
        "forbids": [],
        "adds": [
          "removed:sliding-tray"
        ],
        "deletes": [
          "present:sliding-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray",
          "visible": false
        }
      },
      {
        "id": "remove:tool-head",
        "label": "拆除 tool-head",
        "requires": [
          "present:tool-head"
        ],
        "forbids": [],
        "adds": [
          "removed:tool-head"
        ],
        "deletes": [
          "present:tool-head"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tool-head",
          "visible": false
        }
      },
      {
        "id": "remove:station-2-transfer",
        "label": "拆除 station-2-transfer",
        "requires": [
          "present:station-2-transfer"
        ],
        "forbids": [],
        "adds": [
          "removed:station-2-transfer"
        ],
        "deletes": [
          "present:station-2-transfer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer",
          "visible": false
        }
      },
      {
        "id": "remove:secondary-boom",
        "label": "拆除 secondary-boom",
        "requires": [
          "present:secondary-boom"
        ],
        "forbids": [
          "present:clamp"
        ],
        "adds": [
          "removed:secondary-boom"
        ],
        "deletes": [
          "present:secondary-boom"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "secondary-boom",
          "visible": false
        }
      },
      {
        "id": "remove:mast",
        "label": "拆除 mast",
        "requires": [
          "present:mast"
        ],
        "forbids": [
          "present:primary-boom"
        ],
        "adds": [
          "removed:mast"
        ],
        "deletes": [
          "present:mast"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "mast",
          "visible": false
        }
      },
      {
        "id": "remove:clamp",
        "label": "拆除 clamp",
        "requires": [
          "present:clamp"
        ],
        "forbids": [],
        "adds": [
          "removed:clamp"
        ],
        "deletes": [
          "present:clamp"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "clamp",
          "visible": false
        }
      },
      {
        "id": "remove:control-cab",
        "label": "拆除 control-cab",
        "requires": [
          "present:control-cab"
        ],
        "forbids": [
          "present:secondary-boom"
        ],
        "adds": [
          "removed:control-cab"
        ],
        "deletes": [
          "present:control-cab"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "control-cab",
          "visible": false
        }
      },
      {
        "id": "remove:station-2",
        "label": "拆除 station-2",
        "requires": [
          "present:station-2"
        ],
        "forbids": [
          "present:station-2-machine",
          "present:station-2-transfer"
        ],
        "adds": [
          "removed:station-2"
        ],
        "deletes": [
          "present:station-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-2",
          "visible": false
        }
      },
      {
        "id": "remove:station-1-transfer",
        "label": "拆除 station-1-transfer",
        "requires": [
          "present:station-1-transfer"
        ],
        "forbids": [],
        "adds": [
          "removed:station-1-transfer"
        ],
        "deletes": [
          "present:station-1-transfer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer",
          "visible": false
        }
      },
      {
        "id": "remove:station-0-transfer",
        "label": "拆除 station-0-transfer",
        "requires": [
          "present:station-0-transfer"
        ],
        "forbids": [],
        "adds": [
          "removed:station-0-transfer"
        ],
        "deletes": [
          "present:station-0-transfer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-0-transfer",
          "visible": false
        }
      },
      {
        "id": "remove:service-cartridge",
        "label": "拆除 service-cartridge",
        "requires": [
          "present:service-cartridge"
        ],
        "forbids": [],
        "adds": [
          "removed:service-cartridge"
        ],
        "deletes": [
          "present:service-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "visible": false
        }
      },
      {
        "id": "remove:station-0-machine",
        "label": "拆除 station-0-machine",
        "requires": [
          "present:station-0-machine"
        ],
        "forbids": [],
        "adds": [
          "removed:station-0-machine"
        ],
        "deletes": [
          "present:station-0-machine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-0-machine",
          "visible": false
        }
      },
      {
        "id": "remove:station-1",
        "label": "拆除 station-1",
        "requires": [
          "present:station-1"
        ],
        "forbids": [
          "present:station-1-machine",
          "present:station-1-transfer"
        ],
        "adds": [
          "removed:station-1"
        ],
        "deletes": [
          "present:station-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-1",
          "visible": false
        }
      },
      {
        "id": "remove:primary-boom",
        "label": "拆除 primary-boom",
        "requires": [
          "present:primary-boom"
        ],
        "forbids": [
          "present:tool-head"
        ],
        "adds": [
          "removed:primary-boom"
        ],
        "deletes": [
          "present:primary-boom"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "primary-boom",
          "visible": false
        }
      },
      {
        "id": "remove:station-0",
        "label": "拆除 station-0",
        "requires": [
          "present:station-0"
        ],
        "forbids": [
          "present:station-0-machine",
          "present:station-0-transfer"
        ],
        "adds": [
          "removed:station-0"
        ],
        "deletes": [
          "present:station-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-0",
          "visible": false
        }
      },
      {
        "id": "remove:station-2-machine",
        "label": "拆除 station-2-machine",
        "requires": [
          "present:station-2-machine"
        ],
        "forbids": [],
        "adds": [
          "removed:station-2-machine"
        ],
        "deletes": [
          "present:station-2-machine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine",
          "visible": false
        }
      },
      {
        "id": "remove:station-1-machine",
        "label": "拆除 station-1-machine",
        "requires": [
          "present:station-1-machine"
        ],
        "forbids": [],
        "adds": [
          "removed:station-1-machine"
        ],
        "deletes": [
          "present:station-1-machine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-machine",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:station-2-transfer",
      "removed:station-2-machine",
      "removed:station-2",
      "removed:station-1-transfer",
      "removed:station-1-machine",
      "removed:station-1",
      "removed:station-0-transfer",
      "removed:station-0-machine",
      "removed:station-0",
      "removed:sliding-tray",
      "removed:clamp",
      "removed:secondary-boom",
      "removed:service-cartridge",
      "removed:control-cab",
      "removed:tool-head",
      "removed:primary-boom",
      "removed:mast",
      "removed:foundation"
    ],
    "budget": 18,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:sliding-tray",
      "remove:tool-head",
      "remove:station-2-transfer",
      "remove:clamp",
      "remove:secondary-boom",
      "remove:control-cab",
      "remove:station-1-transfer",
      "remove:station-0-transfer",
      "remove:service-cartridge",
      "remove:station-0-machine",
      "remove:primary-boom",
      "remove:mast",
      "remove:station-0",
      "remove:station-2-machine",
      "remove:station-2",
      "remove:station-1-machine",
      "remove:station-1",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-tidal-energy-station-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:service-cartridge",
      "closed:service-cartridge"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "station-0",
      "station-0-machine",
      "station-0-transfer",
      "station-1",
      "station-1-machine",
      "station-1-transfer",
      "station-2",
      "station-2-machine",
      "station-2-transfer"
    ],
    "actions": [
      {
        "id": "release:service-cartridge",
        "label": "release service-cartridge",
        "requires": [
          "done:close:service-cartridge"
        ],
        "forbids": [
          "done:release:service-cartridge"
        ],
        "adds": [
          "done:release:service-cartridge",
          "repaired:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "close:service-cartridge",
        "label": "close service-cartridge",
        "requires": [
          "done:verify:service-cartridge"
        ],
        "forbids": [
          "done:close:service-cartridge"
        ],
        "adds": [
          "done:close:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "remove:service-cartridge",
        "label": "remove service-cartridge",
        "requires": [
          "done:open:service-cartridge"
        ],
        "forbids": [
          "done:remove:service-cartridge"
        ],
        "adds": [
          "done:remove:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "visible": false
        }
      },
      {
        "id": "verify:service-cartridge",
        "label": "verify service-cartridge",
        "requires": [
          "done:replace:service-cartridge"
        ],
        "forbids": [
          "done:verify:service-cartridge"
        ],
        "adds": [
          "done:verify:service-cartridge"
        ],
        "deletes": [
          "fault:service-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "support:service-cartridge",
        "label": "support service-cartridge",
        "requires": [
          "fault:service-cartridge"
        ],
        "forbids": [
          "done:support:service-cartridge"
        ],
        "adds": [
          "done:support:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "open:service-cartridge",
        "label": "open service-cartridge",
        "requires": [
          "done:support:service-cartridge"
        ],
        "forbids": [
          "done:open:service-cartridge"
        ],
        "adds": [
          "done:open:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "replace:service-cartridge",
        "label": "replace service-cartridge",
        "requires": [
          "done:remove:service-cartridge"
        ],
        "forbids": [
          "done:replace:service-cartridge"
        ],
        "adds": [
          "done:replace:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "repaired:service-cartridge"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:service-cartridge",
      "open:service-cartridge",
      "remove:service-cartridge",
      "replace:service-cartridge",
      "verify:service-cartridge",
      "close:service-cartridge",
      "release:service-cartridge"
    ]
  }
}
```

### 复合编辑验证（h3-tidal-energy-station-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:service-cartridge",
      "closed:service-cartridge"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "station-0",
      "station-0-machine",
      "station-0-transfer",
      "station-1",
      "station-1-machine",
      "station-1-transfer",
      "station-2",
      "station-2-machine",
      "station-2-transfer"
    ],
    "actions": [
      {
        "id": "release:service-cartridge",
        "label": "release service-cartridge",
        "requires": [
          "done:close:service-cartridge"
        ],
        "forbids": [
          "done:release:service-cartridge"
        ],
        "adds": [
          "done:release:service-cartridge",
          "repaired:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "close:service-cartridge",
        "label": "close service-cartridge",
        "requires": [
          "done:verify:service-cartridge"
        ],
        "forbids": [
          "done:close:service-cartridge"
        ],
        "adds": [
          "done:close:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "verify:service-cartridge",
        "label": "verify service-cartridge",
        "requires": [
          "done:recolor:service-cartridge"
        ],
        "forbids": [
          "done:verify:service-cartridge"
        ],
        "adds": [
          "done:verify:service-cartridge"
        ],
        "deletes": [
          "fault:service-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "support:service-cartridge",
        "label": "support service-cartridge",
        "requires": [
          "fault:service-cartridge"
        ],
        "forbids": [
          "done:support:service-cartridge"
        ],
        "adds": [
          "done:support:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "open:service-cartridge",
        "label": "open service-cartridge",
        "requires": [
          "done:support:service-cartridge"
        ],
        "forbids": [
          "done:open:service-cartridge"
        ],
        "adds": [
          "done:open:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "recolor:service-cartridge",
        "label": "recolor service-cartridge",
        "requires": [
          "done:open:service-cartridge"
        ],
        "forbids": [
          "done:recolor:service-cartridge"
        ],
        "adds": [
          "done:recolor:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "color": "#ea7635"
        }
      }
    ],
    "goalFacts": [
      "repaired:service-cartridge"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:service-cartridge",
      "open:service-cartridge",
      "recolor:service-cartridge",
      "verify:service-cartridge",
      "close:service-cartridge",
      "release:service-cartridge"
    ]
  }
}
```

### 跨区域联合维修（h3-tidal-energy-station-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:station-1-transfer",
      "closed:station-1-transfer",
      "fault:station-2",
      "closed:station-2",
      "fault:station-2-machine",
      "closed:station-2-machine",
      "fault:station-2-transfer",
      "closed:station-2-transfer"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "station-0",
      "station-0-machine",
      "station-0-transfer",
      "station-1",
      "station-1-machine",
      "station-1-transfer",
      "station-2",
      "station-2-machine",
      "station-2-transfer"
    ],
    "actions": [
      {
        "id": "support:station-2-machine",
        "label": "support station-2-machine",
        "requires": [
          "fault:station-2-machine"
        ],
        "forbids": [
          "done:support:station-2-machine"
        ],
        "adds": [
          "done:support:station-2-machine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine"
        }
      },
      {
        "id": "replace:station-2-transfer",
        "label": "replace station-2-transfer",
        "requires": [
          "done:remove:station-2-transfer"
        ],
        "forbids": [
          "done:replace:station-2-transfer"
        ],
        "adds": [
          "done:replace:station-2-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer",
          "visible": true
        }
      },
      {
        "id": "open:station-2-transfer",
        "label": "open station-2-transfer",
        "requires": [
          "done:support:station-2-transfer"
        ],
        "forbids": [
          "done:open:station-2-transfer"
        ],
        "adds": [
          "done:open:station-2-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer"
        }
      },
      {
        "id": "support:station-1-transfer",
        "label": "support station-1-transfer",
        "requires": [
          "fault:station-1-transfer"
        ],
        "forbids": [
          "done:support:station-1-transfer"
        ],
        "adds": [
          "done:support:station-1-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer"
        }
      },
      {
        "id": "release:station-2-machine",
        "label": "release station-2-machine",
        "requires": [
          "done:close:station-2-machine"
        ],
        "forbids": [
          "done:release:station-2-machine"
        ],
        "adds": [
          "done:release:station-2-machine",
          "repaired:station-2-machine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine"
        }
      },
      {
        "id": "open:station-1-transfer",
        "label": "open station-1-transfer",
        "requires": [
          "done:support:station-1-transfer"
        ],
        "forbids": [
          "done:open:station-1-transfer"
        ],
        "adds": [
          "done:open:station-1-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer"
        }
      },
      {
        "id": "verify:station-2-machine",
        "label": "verify station-2-machine",
        "requires": [
          "done:replace:station-2-machine"
        ],
        "forbids": [
          "done:verify:station-2-machine"
        ],
        "adds": [
          "done:verify:station-2-machine"
        ],
        "deletes": [
          "fault:station-2-machine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine"
        }
      },
      {
        "id": "remove:station-2-transfer",
        "label": "remove station-2-transfer",
        "requires": [
          "done:open:station-2-transfer"
        ],
        "forbids": [
          "done:remove:station-2-transfer"
        ],
        "adds": [
          "done:remove:station-2-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer",
          "visible": false
        }
      },
      {
        "id": "open:station-2",
        "label": "open station-2",
        "requires": [
          "done:support:station-2"
        ],
        "forbids": [
          "done:open:station-2"
        ],
        "adds": [
          "done:open:station-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2"
        }
      },
      {
        "id": "verify:station-2-transfer",
        "label": "verify station-2-transfer",
        "requires": [
          "done:replace:station-2-transfer"
        ],
        "forbids": [
          "done:verify:station-2-transfer"
        ],
        "adds": [
          "done:verify:station-2-transfer"
        ],
        "deletes": [
          "fault:station-2-transfer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer"
        }
      },
      {
        "id": "replace:station-2",
        "label": "replace station-2",
        "requires": [
          "done:remove:station-2"
        ],
        "forbids": [
          "done:replace:station-2"
        ],
        "adds": [
          "done:replace:station-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2",
          "visible": true
        }
      },
      {
        "id": "verify:station-1-transfer",
        "label": "verify station-1-transfer",
        "requires": [
          "done:replace:station-1-transfer"
        ],
        "forbids": [
          "done:verify:station-1-transfer"
        ],
        "adds": [
          "done:verify:station-1-transfer"
        ],
        "deletes": [
          "fault:station-1-transfer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer"
        }
      },
      {
        "id": "open:station-2-machine",
        "label": "open station-2-machine",
        "requires": [
          "done:support:station-2-machine"
        ],
        "forbids": [
          "done:open:station-2-machine"
        ],
        "adds": [
          "done:open:station-2-machine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine"
        }
      },
      {
        "id": "release:station-2",
        "label": "release station-2",
        "requires": [
          "done:close:station-2"
        ],
        "forbids": [
          "done:release:station-2"
        ],
        "adds": [
          "done:release:station-2",
          "repaired:station-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2"
        }
      },
      {
        "id": "support:station-2-transfer",
        "label": "support station-2-transfer",
        "requires": [
          "fault:station-2-transfer"
        ],
        "forbids": [
          "done:support:station-2-transfer"
        ],
        "adds": [
          "done:support:station-2-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer"
        }
      },
      {
        "id": "remove:station-2",
        "label": "remove station-2",
        "requires": [
          "done:open:station-2"
        ],
        "forbids": [
          "done:remove:station-2"
        ],
        "adds": [
          "done:remove:station-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2",
          "visible": false
        }
      },
      {
        "id": "remove:station-1-transfer",
        "label": "remove station-1-transfer",
        "requires": [
          "done:open:station-1-transfer"
        ],
        "forbids": [
          "done:remove:station-1-transfer"
        ],
        "adds": [
          "done:remove:station-1-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer",
          "visible": false
        }
      },
      {
        "id": "close:station-1-transfer",
        "label": "close station-1-transfer",
        "requires": [
          "done:verify:station-1-transfer"
        ],
        "forbids": [
          "done:close:station-1-transfer"
        ],
        "adds": [
          "done:close:station-1-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer"
        }
      },
      {
        "id": "replace:station-1-transfer",
        "label": "replace station-1-transfer",
        "requires": [
          "done:remove:station-1-transfer"
        ],
        "forbids": [
          "done:replace:station-1-transfer"
        ],
        "adds": [
          "done:replace:station-1-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer",
          "visible": true
        }
      },
      {
        "id": "close:station-2-machine",
        "label": "close station-2-machine",
        "requires": [
          "done:verify:station-2-machine"
        ],
        "forbids": [
          "done:close:station-2-machine"
        ],
        "adds": [
          "done:close:station-2-machine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine"
        }
      },
      {
        "id": "close:station-2",
        "label": "close station-2",
        "requires": [
          "done:verify:station-2"
        ],
        "forbids": [
          "done:close:station-2"
        ],
        "adds": [
          "done:close:station-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2"
        }
      },
      {
        "id": "release:station-2-transfer",
        "label": "release station-2-transfer",
        "requires": [
          "done:close:station-2-transfer"
        ],
        "forbids": [
          "done:release:station-2-transfer"
        ],
        "adds": [
          "done:release:station-2-transfer",
          "repaired:station-2-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer"
        }
      },
      {
        "id": "release:station-1-transfer",
        "label": "release station-1-transfer",
        "requires": [
          "done:close:station-1-transfer"
        ],
        "forbids": [
          "done:release:station-1-transfer"
        ],
        "adds": [
          "done:release:station-1-transfer",
          "repaired:station-1-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer"
        }
      },
      {
        "id": "replace:station-2-machine",
        "label": "replace station-2-machine",
        "requires": [
          "done:remove:station-2-machine"
        ],
        "forbids": [
          "done:replace:station-2-machine"
        ],
        "adds": [
          "done:replace:station-2-machine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine",
          "visible": true
        }
      },
      {
        "id": "verify:station-2",
        "label": "verify station-2",
        "requires": [
          "done:replace:station-2"
        ],
        "forbids": [
          "done:verify:station-2"
        ],
        "adds": [
          "done:verify:station-2"
        ],
        "deletes": [
          "fault:station-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-2"
        }
      },
      {
        "id": "close:station-2-transfer",
        "label": "close station-2-transfer",
        "requires": [
          "done:verify:station-2-transfer"
        ],
        "forbids": [
          "done:close:station-2-transfer"
        ],
        "adds": [
          "done:close:station-2-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer"
        }
      },
      {
        "id": "remove:station-2-machine",
        "label": "remove station-2-machine",
        "requires": [
          "done:open:station-2-machine"
        ],
        "forbids": [
          "done:remove:station-2-machine"
        ],
        "adds": [
          "done:remove:station-2-machine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine",
          "visible": false
        }
      },
      {
        "id": "support:station-2",
        "label": "support station-2",
        "requires": [
          "fault:station-2"
        ],
        "forbids": [
          "done:support:station-2"
        ],
        "adds": [
          "done:support:station-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2"
        }
      }
    ],
    "goalFacts": [
      "repaired:station-1-transfer",
      "repaired:station-2",
      "repaired:station-2-machine",
      "repaired:station-2-transfer"
    ],
    "budget": 28,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:station-2-machine",
      "support:station-1-transfer",
      "open:station-1-transfer",
      "open:station-2-machine",
      "support:station-2-transfer",
      "open:station-2-transfer",
      "remove:station-2-transfer",
      "replace:station-2-transfer",
      "verify:station-2-transfer",
      "remove:station-1-transfer",
      "replace:station-1-transfer",
      "verify:station-1-transfer",
      "close:station-1-transfer",
      "release:station-1-transfer",
      "close:station-2-transfer",
      "release:station-2-transfer",
      "remove:station-2-machine",
      "replace:station-2-machine",
      "verify:station-2-machine",
      "close:station-2-machine",
      "release:station-2-machine",
      "support:station-2",
      "open:station-2",
      "remove:station-2",
      "replace:station-2",
      "verify:station-2",
      "close:station-2",
      "release:station-2"
    ]
  }
}
```

### 多工位资源调度（h3-tidal-energy-station-scheduling）

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
        "module": "mast",
        "duration": 3,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "primary-boom",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "tool-head",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "control-cab",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "service-cartridge",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      },
      {
        "id": "job-6",
        "module": "secondary-boom",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-4"
        ]
      },
      {
        "id": "job-7",
        "module": "clamp",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-5"
        ]
      },
      {
        "id": "job-8",
        "module": "sliding-tray",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-6"
        ]
      },
      {
        "id": "job-9",
        "module": "station-0",
        "duration": 1,
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
      "job-3": 3,
      "job-4": 4,
      "job-5": 6,
      "job-6": 7,
      "job-7": 9,
      "job-8": 8,
      "job-9": 10
    }
  }
}
```

### 检查后条件策略（h3-tidal-energy-station-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "service-cartridge",
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

### 局部坐标变换（h3-tidal-energy-station-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[1.5,0.8,-1.5]
- B：[0.5,-0.05,-0.5]
- C：[2.5,0.8,-2.5]
- D：[2.5,1.8,-0.5]

```json
{
  "input": {
    "localPoint": [
      0.5,
      -0.04999999999999999,
      -0.5
    ],
    "rotationXYZW": [
      0,
      1,
      0,
      6.123233995736766e-17
    ],
    "translation": [
      2,
      0.8500000000000001,
      -2
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 正交视图投影（h3-tidal-energy-station-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[11,5]
- B：[5,6]
- C：[0,0]
- D：[5,11]

```json
{
  "input": {
    "view": "front",
    "point": [
      5,
      11,
      -6
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 空间相对关系（h3-tidal-energy-station-relative-order）

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
        0.35,
        0
      ]
    },
    "B": {
      "id": "station-2-transfer",
      "position": [
        3.7082039324993668,
        1.05,
        -11.412678195541844
      ]
    },
    "axis": "x"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 约束自由度（h3-tidal-energy-station-joint-axis）

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
      "id": "primary-boom-joint",
      "name": "primary-boom interface",
      "parent": "mast",
      "child": "primary-boom",
      "type": "revolute",
      "anchorParent": [
        0,
        3.65,
        0
      ],
      "anchorChild": [
        -2.644425454113648,
        -2.1181524200761386,
        0
      ],
      "axis": [
        0,
        0,
        1
      ],
      "limits": [
        -0.8,
        0.8
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 维修间隙预算（h3-tidal-energy-station-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "service-cartridge",
    "aperture": 0.6,
    "toolWidth": 0.65,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-tidal-energy-station-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,16]
- B：[0,0,0]
- C：[0,-4,0]
- D：[0,0,-16]

```json
{
  "input": {
    "module": "service-cartridge",
    "lever": [
      4,
      1,
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

### 非均匀先验更新（h3-tidal-energy-station-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0
- B：1
- C：0.625
- D：0.38461538461538464

```json
{
  "input": {
    "module": "service-cartridge",
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

### 风险最小决策（h3-tidal-energy-station-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.7,
    "repairCost": 6,
    "failureLoss": 16,
    "module": "service-cartridge"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-tidal-energy-station-trace-threshold）

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
        "displacement": 0.005873355322933528
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.012614477239857366
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.008770120670057472
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0013756763842113176
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0015260327529835285
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0013265273469910837
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00023070690564183543
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0001316624509502049
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0002331639236260605
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.000008427051306687483
      },
      {
        "time": 1,
        "displacement": 0.0000023337330759110322
      }
    ],
    "threshold": 0.010091581791885892
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-tidal-energy-station-guarded-repair）

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
        "id": "release:service-cartridge",
        "label": "release service-cartridge",
        "requires": [
          "done:relock:service-cartridge"
        ],
        "forbids": [
          "done:release:service-cartridge"
        ],
        "adds": [
          "done:release:service-cartridge",
          "ready:service-cartridge",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "relock:service-cartridge",
        "label": "relock service-cartridge",
        "requires": [
          "done:verify:service-cartridge"
        ],
        "forbids": [
          "done:relock:service-cartridge"
        ],
        "adds": [
          "done:relock:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "verify:service-cartridge",
        "label": "verify service-cartridge",
        "requires": [
          "done:replace:service-cartridge"
        ],
        "forbids": [
          "done:verify:service-cartridge"
        ],
        "adds": [
          "done:verify:service-cartridge"
        ],
        "deletes": [
          "fault:service-cartridge",
          "misaligned:service-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "replace:service-cartridge",
        "label": "replace service-cartridge",
        "requires": [
          "done:unlock:service-cartridge"
        ],
        "forbids": [
          "done:replace:service-cartridge"
        ],
        "adds": [
          "done:replace:service-cartridge"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "unlock:service-cartridge",
        "label": "unlock service-cartridge",
        "requires": [
          "done:support:service-cartridge"
        ],
        "forbids": [
          "done:unlock:service-cartridge"
        ],
        "adds": [
          "done:unlock:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "support:service-cartridge",
        "label": "support service-cartridge",
        "requires": [
          "done:isolate:service-cartridge"
        ],
        "forbids": [
          "done:support:service-cartridge"
        ],
        "adds": [
          "done:support:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "isolate:service-cartridge",
        "label": "isolate service-cartridge",
        "requires": [
          "tool:free",
          "fault:service-cartridge"
        ],
        "forbids": [
          "done:isolate:service-cartridge"
        ],
        "adds": [
          "done:isolate:service-cartridge"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:service-cartridge"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "station-0",
      "station-0-machine",
      "station-0-transfer",
      "station-1",
      "station-1-machine",
      "station-1-transfer",
      "station-2",
      "station-2-machine",
      "station-2-transfer"
    ],
    "goalFacts": [
      "ready:service-cartridge"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:service-cartridge",
      "support:service-cartridge",
      "unlock:service-cartridge",
      "replace:service-cartridge",
      "verify:service-cartridge",
      "relock:service-cartridge",
      "release:service-cartridge"
    ]
  }
}
```

### 失败状态回退（h3-tidal-energy-station-rollback）

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
        "id": "resume:service-cartridge",
        "label": "resume service-cartridge",
        "requires": [
          "done:verify:service-cartridge"
        ],
        "forbids": [
          "done:resume:service-cartridge"
        ],
        "adds": [
          "done:resume:service-cartridge",
          "ready:service-cartridge",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "verify:service-cartridge",
        "label": "verify service-cartridge",
        "requires": [
          "done:align:service-cartridge"
        ],
        "forbids": [
          "done:verify:service-cartridge"
        ],
        "adds": [
          "done:verify:service-cartridge"
        ],
        "deletes": [
          "fault:service-cartridge",
          "misaligned:service-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "align:service-cartridge",
        "label": "align service-cartridge",
        "requires": [
          "done:undo:service-cartridge"
        ],
        "forbids": [
          "done:align:service-cartridge"
        ],
        "adds": [
          "done:align:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "visible": true
        }
      },
      {
        "id": "undo:service-cartridge",
        "label": "undo service-cartridge",
        "requires": [
          "done:isolate:service-cartridge"
        ],
        "forbids": [
          "done:undo:service-cartridge"
        ],
        "adds": [
          "done:undo:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "visible": false
        }
      },
      {
        "id": "isolate:service-cartridge",
        "label": "isolate service-cartridge",
        "requires": [
          "tool:free",
          "fault:service-cartridge"
        ],
        "forbids": [
          "done:isolate:service-cartridge"
        ],
        "adds": [
          "done:isolate:service-cartridge"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:service-cartridge",
      "misaligned:service-cartridge"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "station-0",
      "station-0-machine",
      "station-0-transfer",
      "station-1",
      "station-1-machine",
      "station-1-transfer",
      "station-2",
      "station-2-machine",
      "station-2-transfer"
    ],
    "goalFacts": [
      "ready:service-cartridge"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:service-cartridge",
      "undo:service-cartridge",
      "align:service-cartridge",
      "verify:service-cartridge",
      "resume:service-cartridge"
    ]
  }
}
```

### 共享工具协同维修（h3-tidal-energy-station-resource-repair）

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
        "id": "release:station-2-transfer",
        "label": "release station-2-transfer",
        "requires": [
          "done:relock:station-2-transfer"
        ],
        "forbids": [
          "done:release:station-2-transfer"
        ],
        "adds": [
          "done:release:station-2-transfer",
          "ready:station-2-transfer",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer"
        }
      },
      {
        "id": "relock:station-2-transfer",
        "label": "relock station-2-transfer",
        "requires": [
          "done:verify:station-2-transfer"
        ],
        "forbids": [
          "done:relock:station-2-transfer"
        ],
        "adds": [
          "done:relock:station-2-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer"
        }
      },
      {
        "id": "verify:station-2-transfer",
        "label": "verify station-2-transfer",
        "requires": [
          "done:replace:station-2-transfer"
        ],
        "forbids": [
          "done:verify:station-2-transfer"
        ],
        "adds": [
          "done:verify:station-2-transfer"
        ],
        "deletes": [
          "fault:station-2-transfer",
          "misaligned:station-2-transfer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer"
        }
      },
      {
        "id": "replace:station-2-transfer",
        "label": "replace station-2-transfer",
        "requires": [
          "done:unlock:station-2-transfer"
        ],
        "forbids": [
          "done:replace:station-2-transfer"
        ],
        "adds": [
          "done:replace:station-2-transfer"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "station-2-transfer"
        }
      },
      {
        "id": "unlock:station-2-transfer",
        "label": "unlock station-2-transfer",
        "requires": [
          "done:support:station-2-transfer"
        ],
        "forbids": [
          "done:unlock:station-2-transfer"
        ],
        "adds": [
          "done:unlock:station-2-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer"
        }
      },
      {
        "id": "support:station-2-transfer",
        "label": "support station-2-transfer",
        "requires": [
          "done:isolate:station-2-transfer"
        ],
        "forbids": [
          "done:support:station-2-transfer"
        ],
        "adds": [
          "done:support:station-2-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer"
        }
      },
      {
        "id": "isolate:station-2-transfer",
        "label": "isolate station-2-transfer",
        "requires": [
          "tool:free",
          "fault:station-2-transfer"
        ],
        "forbids": [
          "done:isolate:station-2-transfer"
        ],
        "adds": [
          "done:isolate:station-2-transfer"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-transfer"
        }
      },
      {
        "id": "release:station-2-machine",
        "label": "release station-2-machine",
        "requires": [
          "done:relock:station-2-machine"
        ],
        "forbids": [
          "done:release:station-2-machine"
        ],
        "adds": [
          "done:release:station-2-machine",
          "ready:station-2-machine",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine"
        }
      },
      {
        "id": "relock:station-2-machine",
        "label": "relock station-2-machine",
        "requires": [
          "done:verify:station-2-machine"
        ],
        "forbids": [
          "done:relock:station-2-machine"
        ],
        "adds": [
          "done:relock:station-2-machine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine"
        }
      },
      {
        "id": "verify:station-2-machine",
        "label": "verify station-2-machine",
        "requires": [
          "done:replace:station-2-machine"
        ],
        "forbids": [
          "done:verify:station-2-machine"
        ],
        "adds": [
          "done:verify:station-2-machine"
        ],
        "deletes": [
          "fault:station-2-machine",
          "misaligned:station-2-machine"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine"
        }
      },
      {
        "id": "replace:station-2-machine",
        "label": "replace station-2-machine",
        "requires": [
          "done:unlock:station-2-machine"
        ],
        "forbids": [
          "done:replace:station-2-machine"
        ],
        "adds": [
          "done:replace:station-2-machine"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "station-2-machine"
        }
      },
      {
        "id": "unlock:station-2-machine",
        "label": "unlock station-2-machine",
        "requires": [
          "done:support:station-2-machine"
        ],
        "forbids": [
          "done:unlock:station-2-machine"
        ],
        "adds": [
          "done:unlock:station-2-machine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine"
        }
      },
      {
        "id": "support:station-2-machine",
        "label": "support station-2-machine",
        "requires": [
          "done:isolate:station-2-machine"
        ],
        "forbids": [
          "done:support:station-2-machine"
        ],
        "adds": [
          "done:support:station-2-machine"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine"
        }
      },
      {
        "id": "isolate:station-2-machine",
        "label": "isolate station-2-machine",
        "requires": [
          "tool:free",
          "fault:station-2-machine"
        ],
        "forbids": [
          "done:isolate:station-2-machine"
        ],
        "adds": [
          "done:isolate:station-2-machine"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-2-machine"
        }
      },
      {
        "id": "release:station-2",
        "label": "release station-2",
        "requires": [
          "done:relock:station-2"
        ],
        "forbids": [
          "done:release:station-2"
        ],
        "adds": [
          "done:release:station-2",
          "ready:station-2",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2"
        }
      },
      {
        "id": "relock:station-2",
        "label": "relock station-2",
        "requires": [
          "done:verify:station-2"
        ],
        "forbids": [
          "done:relock:station-2"
        ],
        "adds": [
          "done:relock:station-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2"
        }
      },
      {
        "id": "verify:station-2",
        "label": "verify station-2",
        "requires": [
          "done:replace:station-2"
        ],
        "forbids": [
          "done:verify:station-2"
        ],
        "adds": [
          "done:verify:station-2"
        ],
        "deletes": [
          "fault:station-2",
          "misaligned:station-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-2"
        }
      },
      {
        "id": "replace:station-2",
        "label": "replace station-2",
        "requires": [
          "done:unlock:station-2"
        ],
        "forbids": [
          "done:replace:station-2"
        ],
        "adds": [
          "done:replace:station-2"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "station-2"
        }
      },
      {
        "id": "unlock:station-2",
        "label": "unlock station-2",
        "requires": [
          "done:support:station-2"
        ],
        "forbids": [
          "done:unlock:station-2"
        ],
        "adds": [
          "done:unlock:station-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2"
        }
      },
      {
        "id": "support:station-2",
        "label": "support station-2",
        "requires": [
          "done:isolate:station-2"
        ],
        "forbids": [
          "done:support:station-2"
        ],
        "adds": [
          "done:support:station-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-2"
        }
      },
      {
        "id": "isolate:station-2",
        "label": "isolate station-2",
        "requires": [
          "tool:free",
          "fault:station-2"
        ],
        "forbids": [
          "done:isolate:station-2"
        ],
        "adds": [
          "done:isolate:station-2"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-2"
        }
      },
      {
        "id": "release:station-1-transfer",
        "label": "release station-1-transfer",
        "requires": [
          "done:relock:station-1-transfer"
        ],
        "forbids": [
          "done:release:station-1-transfer"
        ],
        "adds": [
          "done:release:station-1-transfer",
          "ready:station-1-transfer",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer"
        }
      },
      {
        "id": "relock:station-1-transfer",
        "label": "relock station-1-transfer",
        "requires": [
          "done:verify:station-1-transfer"
        ],
        "forbids": [
          "done:relock:station-1-transfer"
        ],
        "adds": [
          "done:relock:station-1-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer"
        }
      },
      {
        "id": "verify:station-1-transfer",
        "label": "verify station-1-transfer",
        "requires": [
          "done:replace:station-1-transfer"
        ],
        "forbids": [
          "done:verify:station-1-transfer"
        ],
        "adds": [
          "done:verify:station-1-transfer"
        ],
        "deletes": [
          "fault:station-1-transfer",
          "misaligned:station-1-transfer"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer"
        }
      },
      {
        "id": "replace:station-1-transfer",
        "label": "replace station-1-transfer",
        "requires": [
          "done:unlock:station-1-transfer"
        ],
        "forbids": [
          "done:replace:station-1-transfer"
        ],
        "adds": [
          "done:replace:station-1-transfer"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "station-1-transfer"
        }
      },
      {
        "id": "unlock:station-1-transfer",
        "label": "unlock station-1-transfer",
        "requires": [
          "done:support:station-1-transfer"
        ],
        "forbids": [
          "done:unlock:station-1-transfer"
        ],
        "adds": [
          "done:unlock:station-1-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer"
        }
      },
      {
        "id": "support:station-1-transfer",
        "label": "support station-1-transfer",
        "requires": [
          "done:isolate:station-1-transfer"
        ],
        "forbids": [
          "done:support:station-1-transfer"
        ],
        "adds": [
          "done:support:station-1-transfer"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer"
        }
      },
      {
        "id": "isolate:station-1-transfer",
        "label": "isolate station-1-transfer",
        "requires": [
          "tool:free",
          "fault:station-1-transfer"
        ],
        "forbids": [
          "done:isolate:station-1-transfer"
        ],
        "adds": [
          "done:isolate:station-1-transfer"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-1-transfer"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:station-1-transfer",
      "fault:station-2",
      "fault:station-2-machine",
      "fault:station-2-transfer"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "station-0",
      "station-0-machine",
      "station-0-transfer",
      "station-1",
      "station-1-machine",
      "station-1-transfer",
      "station-2",
      "station-2-machine",
      "station-2-transfer"
    ],
    "goalFacts": [
      "ready:station-1-transfer",
      "ready:station-2",
      "ready:station-2-machine",
      "ready:station-2-transfer"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:station-2-transfer",
      "support:station-2-transfer",
      "unlock:station-2-transfer",
      "replace:station-2-transfer",
      "verify:station-2-transfer",
      "relock:station-2-transfer",
      "release:station-2-transfer",
      "isolate:station-2-machine",
      "support:station-2-machine",
      "unlock:station-2-machine",
      "replace:station-2-machine",
      "verify:station-2-machine",
      "relock:station-2-machine",
      "release:station-2-machine",
      "isolate:station-2",
      "support:station-2",
      "unlock:station-2",
      "replace:station-2",
      "verify:station-2",
      "relock:station-2",
      "release:station-2",
      "isolate:station-1-transfer",
      "support:station-1-transfer",
      "unlock:station-1-transfer",
      "replace:station-1-transfer",
      "verify:station-1-transfer",
      "relock:station-1-transfer",
      "release:station-1-transfer"
    ]
  }
}
```

### 预算约束检查策略（h3-tidal-energy-station-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "service-cartridge",
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
        "cost": 0,
        "returns": {
          "nominal": "pass",
          "fault": "pass"
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
        "cost": 1,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      }
    ],
    "budget": 1
  },
  "answer": {
    "queryId": "thermal",
    "decisions": {
      "pass": "continue",
      "fail": "tighten"
    }
  }
}
```
