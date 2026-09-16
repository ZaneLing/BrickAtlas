## D4 分段天线协作装配场

### 模块识别（h3-segmented-antenna-yard-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：frame
- B：rail-0
- C：carriage-0
- D：head-0

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "frame",
        "name": "frame"
      },
      {
        "id": "rail-0",
        "name": "rail 0"
      },
      {
        "id": "carriage-0",
        "name": "carriage 0"
      },
      {
        "id": "turret-0",
        "name": "turret 0"
      },
      {
        "id": "elbow-0",
        "name": "elbow 0"
      },
      {
        "id": "head-0",
        "name": "head 0"
      },
      {
        "id": "petal-0",
        "name": "petal 0"
      },
      {
        "id": "sensor-0",
        "name": "sensor 0"
      },
      {
        "id": "rack-0",
        "name": "rack 0"
      },
      {
        "id": "exchange-pack-0",
        "name": "exchange pack 0"
      },
      {
        "id": "gate-0",
        "name": "gate 0"
      },
      {
        "id": "rail-1",
        "name": "rail 1"
      },
      {
        "id": "carriage-1",
        "name": "carriage 1"
      },
      {
        "id": "turret-1",
        "name": "turret 1"
      },
      {
        "id": "elbow-1",
        "name": "elbow 1"
      },
      {
        "id": "head-1",
        "name": "head 1"
      },
      {
        "id": "petal-1",
        "name": "petal 1"
      },
      {
        "id": "sensor-1",
        "name": "sensor 1"
      },
      {
        "id": "rack-1",
        "name": "rack 1"
      },
      {
        "id": "exchange-pack-1",
        "name": "exchange pack 1"
      },
      {
        "id": "gate-1",
        "name": "gate 1"
      },
      {
        "id": "rail-2",
        "name": "rail 2"
      },
      {
        "id": "carriage-2",
        "name": "carriage 2"
      },
      {
        "id": "turret-2",
        "name": "turret 2"
      },
      {
        "id": "elbow-2",
        "name": "elbow 2"
      },
      {
        "id": "head-2",
        "name": "head 2"
      },
      {
        "id": "petal-2",
        "name": "petal 2"
      },
      {
        "id": "sensor-2",
        "name": "sensor 2"
      },
      {
        "id": "rack-2",
        "name": "rack 2"
      },
      {
        "id": "exchange-pack-2",
        "name": "exchange pack 2"
      },
      {
        "id": "gate-2",
        "name": "gate 2"
      },
      {
        "id": "rail-3",
        "name": "rail 3"
      },
      {
        "id": "carriage-3",
        "name": "carriage 3"
      },
      {
        "id": "turret-3",
        "name": "turret 3"
      },
      {
        "id": "elbow-3",
        "name": "elbow 3"
      },
      {
        "id": "head-3",
        "name": "head 3"
      },
      {
        "id": "petal-3",
        "name": "petal 3"
      },
      {
        "id": "sensor-3",
        "name": "sensor 3"
      },
      {
        "id": "rack-3",
        "name": "rack 3"
      },
      {
        "id": "exchange-pack-3",
        "name": "exchange pack 3"
      },
      {
        "id": "gate-3",
        "name": "gate 3"
      },
      {
        "id": "rail-4",
        "name": "rail 4"
      },
      {
        "id": "carriage-4",
        "name": "carriage 4"
      },
      {
        "id": "turret-4",
        "name": "turret 4"
      },
      {
        "id": "elbow-4",
        "name": "elbow 4"
      },
      {
        "id": "head-4",
        "name": "head 4"
      },
      {
        "id": "petal-4",
        "name": "petal 4"
      },
      {
        "id": "sensor-4",
        "name": "sensor 4"
      },
      {
        "id": "rack-4",
        "name": "rack 4"
      },
      {
        "id": "exchange-pack-4",
        "name": "exchange pack 4"
      },
      {
        "id": "gate-4",
        "name": "gate 4"
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 部件计数（h3-segmented-antenna-yard-count）

模块 head-0 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：5
- B：2
- C：3
- D：1

```json
{
  "input": {
    "parts": [
      {
        "id": "frame-p1",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p2",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p3",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p4",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p5",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p6",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p7",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p8",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p9",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p10",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p11",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p12",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p13",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p14",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p15",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p16",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p17",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p18",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p19",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p20",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p21",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p22",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p23",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p24",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p25",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p26",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p27",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p28",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p29",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p30",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p31",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p32",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p33",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p34",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p35",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p36",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p37",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p38",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p39",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p40",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p41",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p42",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p43",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p44",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p45",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p46",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p47",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p48",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p49",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p50",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p51",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p52",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p53",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p54",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p55",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p56",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p57",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p58",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p59",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p60",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p61",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p62",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p63",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p64",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p65",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p66",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p67",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p68",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p69",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p70",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p71",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p72",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p73",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p74",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p75",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p76",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p77",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p78",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p79",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p80",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p81",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p82",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p83",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p84",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p85",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p86",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p87",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p88",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p89",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p90",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p91",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p92",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p93",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p94",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p95",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p96",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p97",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p98",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p99",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "frame-p100",
        "moduleId": "frame",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "rail-0-p101",
        "moduleId": "rail-0",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "carriage-0-p102",
        "moduleId": "carriage-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-0-p103",
        "moduleId": "carriage-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-0-p104",
        "moduleId": "carriage-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-0-p105",
        "moduleId": "carriage-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "turret-0-p106",
        "moduleId": "turret-0",
        "shape": "cylinder",
        "color": "#e9ad37"
      },
      {
        "id": "elbow-0-p107",
        "moduleId": "elbow-0",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "head-0-p108",
        "moduleId": "head-0",
        "shape": "arch",
        "color": "#45a080"
      },
      {
        "id": "head-0-p109",
        "moduleId": "head-0",
        "shape": "panel",
        "color": "#dfebed"
      },
      {
        "id": "petal-0-p110",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p111",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p112",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p113",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p114",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p115",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p116",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p117",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p118",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p119",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p120",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p121",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p122",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p123",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p124",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "sensor-0-p125",
        "moduleId": "sensor-0",
        "shape": "sphere",
        "color": "#79c7d8"
      },
      {
        "id": "rack-0-p126",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p127",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p128",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p129",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p130",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p131",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p132",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p133",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p134",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p135",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p136",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p137",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p138",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p139",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p140",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p141",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p142",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p143",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p144",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p145",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p146",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p147",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p148",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p149",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p150",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p151",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p152",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p153",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p154",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p155",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p156",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p157",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p158",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p159",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p160",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p161",
        "moduleId": "rack-0",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-0-p162",
        "moduleId": "rack-0",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "rack-0-p163",
        "moduleId": "rack-0",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "exchange-pack-0-p164",
        "moduleId": "exchange-pack-0",
        "shape": "panel",
        "color": "#e9ad37"
      },
      {
        "id": "gate-0-p165",
        "moduleId": "gate-0",
        "shape": "panel",
        "color": "#e9ad37"
      },
      {
        "id": "rail-1-p166",
        "moduleId": "rail-1",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "carriage-1-p167",
        "moduleId": "carriage-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-1-p168",
        "moduleId": "carriage-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-1-p169",
        "moduleId": "carriage-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-1-p170",
        "moduleId": "carriage-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "turret-1-p171",
        "moduleId": "turret-1",
        "shape": "cylinder",
        "color": "#e9ad37"
      },
      {
        "id": "elbow-1-p172",
        "moduleId": "elbow-1",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "head-1-p173",
        "moduleId": "head-1",
        "shape": "arch",
        "color": "#45a080"
      },
      {
        "id": "head-1-p174",
        "moduleId": "head-1",
        "shape": "panel",
        "color": "#dfebed"
      },
      {
        "id": "petal-1-p175",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p176",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p177",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p178",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p179",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p180",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p181",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p182",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p183",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p184",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p185",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p186",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p187",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p188",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p189",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "sensor-1-p190",
        "moduleId": "sensor-1",
        "shape": "sphere",
        "color": "#79c7d8"
      },
      {
        "id": "rack-1-p191",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p192",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p193",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p194",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p195",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p196",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p197",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p198",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p199",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p200",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p201",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p202",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p203",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p204",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p205",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p206",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p207",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p208",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p209",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p210",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p211",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p212",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p213",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p214",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p215",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p216",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p217",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p218",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p219",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p220",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p221",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p222",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p223",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p224",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p225",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p226",
        "moduleId": "rack-1",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-1-p227",
        "moduleId": "rack-1",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "rack-1-p228",
        "moduleId": "rack-1",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "exchange-pack-1-p229",
        "moduleId": "exchange-pack-1",
        "shape": "panel",
        "color": "#387bb3"
      },
      {
        "id": "gate-1-p230",
        "moduleId": "gate-1",
        "shape": "panel",
        "color": "#e9ad37"
      },
      {
        "id": "rail-2-p231",
        "moduleId": "rail-2",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "carriage-2-p232",
        "moduleId": "carriage-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-2-p233",
        "moduleId": "carriage-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-2-p234",
        "moduleId": "carriage-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-2-p235",
        "moduleId": "carriage-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "turret-2-p236",
        "moduleId": "turret-2",
        "shape": "cylinder",
        "color": "#e9ad37"
      },
      {
        "id": "elbow-2-p237",
        "moduleId": "elbow-2",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "head-2-p238",
        "moduleId": "head-2",
        "shape": "arch",
        "color": "#45a080"
      },
      {
        "id": "head-2-p239",
        "moduleId": "head-2",
        "shape": "panel",
        "color": "#dfebed"
      },
      {
        "id": "petal-2-p240",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p241",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p242",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p243",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p244",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p245",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p246",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p247",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p248",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p249",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p250",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p251",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p252",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p253",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p254",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "sensor-2-p255",
        "moduleId": "sensor-2",
        "shape": "sphere",
        "color": "#79c7d8"
      },
      {
        "id": "rack-2-p256",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p257",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p258",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p259",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p260",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p261",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p262",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p263",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p264",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p265",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p266",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p267",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p268",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p269",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p270",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p271",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p272",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p273",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p274",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p275",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p276",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p277",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p278",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p279",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p280",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p281",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p282",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p283",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p284",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p285",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p286",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p287",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p288",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p289",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p290",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p291",
        "moduleId": "rack-2",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-2-p292",
        "moduleId": "rack-2",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "rack-2-p293",
        "moduleId": "rack-2",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "exchange-pack-2-p294",
        "moduleId": "exchange-pack-2",
        "shape": "panel",
        "color": "#dc6040"
      },
      {
        "id": "gate-2-p295",
        "moduleId": "gate-2",
        "shape": "panel",
        "color": "#e9ad37"
      },
      {
        "id": "rail-3-p296",
        "moduleId": "rail-3",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "carriage-3-p297",
        "moduleId": "carriage-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-3-p298",
        "moduleId": "carriage-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-3-p299",
        "moduleId": "carriage-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-3-p300",
        "moduleId": "carriage-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "turret-3-p301",
        "moduleId": "turret-3",
        "shape": "cylinder",
        "color": "#e9ad37"
      },
      {
        "id": "elbow-3-p302",
        "moduleId": "elbow-3",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "head-3-p303",
        "moduleId": "head-3",
        "shape": "arch",
        "color": "#45a080"
      },
      {
        "id": "head-3-p304",
        "moduleId": "head-3",
        "shape": "panel",
        "color": "#dfebed"
      },
      {
        "id": "petal-3-p305",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p306",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p307",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p308",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p309",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p310",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p311",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p312",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p313",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p314",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p315",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p316",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p317",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p318",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-3-p319",
        "moduleId": "petal-3",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "sensor-3-p320",
        "moduleId": "sensor-3",
        "shape": "sphere",
        "color": "#79c7d8"
      },
      {
        "id": "rack-3-p321",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p322",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p323",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p324",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p325",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p326",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p327",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p328",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p329",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p330",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p331",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p332",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p333",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p334",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p335",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p336",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p337",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p338",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p339",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p340",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p341",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p342",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p343",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p344",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p345",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p346",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p347",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p348",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p349",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p350",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p351",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p352",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p353",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p354",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p355",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p356",
        "moduleId": "rack-3",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-3-p357",
        "moduleId": "rack-3",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "rack-3-p358",
        "moduleId": "rack-3",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "exchange-pack-3-p359",
        "moduleId": "exchange-pack-3",
        "shape": "panel",
        "color": "#e9ad37"
      },
      {
        "id": "gate-3-p360",
        "moduleId": "gate-3",
        "shape": "panel",
        "color": "#e9ad37"
      },
      {
        "id": "rail-4-p361",
        "moduleId": "rail-4",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "carriage-4-p362",
        "moduleId": "carriage-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-4-p363",
        "moduleId": "carriage-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-4-p364",
        "moduleId": "carriage-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-4-p365",
        "moduleId": "carriage-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "turret-4-p366",
        "moduleId": "turret-4",
        "shape": "cylinder",
        "color": "#e9ad37"
      },
      {
        "id": "elbow-4-p367",
        "moduleId": "elbow-4",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "head-4-p368",
        "moduleId": "head-4",
        "shape": "arch",
        "color": "#45a080"
      },
      {
        "id": "head-4-p369",
        "moduleId": "head-4",
        "shape": "panel",
        "color": "#dfebed"
      },
      {
        "id": "petal-4-p370",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p371",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p372",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p373",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p374",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p375",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p376",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p377",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p378",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p379",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p380",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p381",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p382",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p383",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-4-p384",
        "moduleId": "petal-4",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "sensor-4-p385",
        "moduleId": "sensor-4",
        "shape": "sphere",
        "color": "#79c7d8"
      },
      {
        "id": "rack-4-p386",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p387",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p388",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p389",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p390",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p391",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p392",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p393",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p394",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p395",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p396",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p397",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p398",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p399",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p400",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p401",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p402",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p403",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p404",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p405",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p406",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p407",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p408",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p409",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p410",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p411",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p412",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p413",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p414",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p415",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p416",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p417",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p418",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p419",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p420",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p421",
        "moduleId": "rack-4",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "rack-4-p422",
        "moduleId": "rack-4",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "rack-4-p423",
        "moduleId": "rack-4",
        "shape": "beam",
        "color": "#273e50"
      },
      {
        "id": "exchange-pack-4-p424",
        "moduleId": "exchange-pack-4",
        "shape": "panel",
        "color": "#387bb3"
      },
      {
        "id": "gate-4-p425",
        "moduleId": "gate-4",
        "shape": "panel",
        "color": "#e9ad37"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 颜色识别（h3-segmented-antenna-yard-color）

零件 head-0-p108 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#2878b8
- B：#d43a32
- C：#f2bf3c
- D：#45a080

```json
{
  "input": {
    "part": {
      "id": "head-0-p108",
      "moduleId": "head-0",
      "shape": "arch",
      "position": [
        0,
        -0.08750000000000002,
        0
      ],
      "size": [
        1.6,
        0.7,
        1
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

### 三维位置（h3-segmented-antenna-yard-position）

模块 head-0 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[-14,1,0]
- B：[-14,1.5499999999999998,0]
- C：[-14,6.5875,0]
- D：[0,0.35,0]

```json
{
  "input": {
    "centers": {
      "frame": [
        0,
        0.35,
        0
      ],
      "rail-0": [
        -14,
        1,
        0
      ],
      "carriage-0": [
        -14,
        1.5499999999999998,
        0
      ],
      "turret-0": [
        -14,
        2.2,
        0
      ],
      "elbow-0": [
        -14,
        4.35,
        0
      ],
      "head-0": [
        -14,
        6.5875,
        0
      ],
      "petal-0": [
        -14,
        7.850000000000001,
        0
      ],
      "sensor-0": [
        -14,
        8.35,
        0
      ],
      "rack-0": [
        -14,
        2.4,
        -7
      ],
      "exchange-pack-0": [
        -14,
        3,
        -7
      ],
      "gate-0": [
        -14,
        2,
        6
      ],
      "rail-1": [
        -7,
        1,
        0
      ],
      "carriage-1": [
        -7,
        1.5499999999999998,
        0
      ],
      "turret-1": [
        -7,
        2.2,
        0
      ],
      "elbow-1": [
        -7,
        4.35,
        0
      ],
      "head-1": [
        -7,
        6.5875,
        0
      ],
      "petal-1": [
        -7,
        7.850000000000001,
        0
      ],
      "sensor-1": [
        -7,
        8.35,
        0
      ],
      "rack-1": [
        -7,
        2.4,
        -7
      ],
      "exchange-pack-1": [
        -7,
        3,
        -7
      ],
      "gate-1": [
        -7,
        2,
        6
      ],
      "rail-2": [
        0,
        1,
        0
      ],
      "carriage-2": [
        0,
        1.5499999999999998,
        0
      ],
      "turret-2": [
        0,
        2.2,
        0
      ],
      "elbow-2": [
        0,
        4.35,
        0
      ],
      "head-2": [
        0,
        6.5875,
        0
      ],
      "petal-2": [
        0,
        7.850000000000001,
        0
      ],
      "sensor-2": [
        0,
        8.35,
        0
      ],
      "rack-2": [
        0,
        2.4,
        -7
      ],
      "exchange-pack-2": [
        0,
        3,
        -7
      ],
      "gate-2": [
        0,
        2,
        6
      ],
      "rail-3": [
        7,
        1,
        0
      ],
      "carriage-3": [
        7,
        1.5499999999999998,
        0
      ],
      "turret-3": [
        7,
        2.2,
        0
      ],
      "elbow-3": [
        7,
        4.35,
        0
      ],
      "head-3": [
        7,
        6.5875,
        0
      ],
      "petal-3": [
        7,
        7.850000000000001,
        0
      ],
      "sensor-3": [
        7,
        8.35,
        0
      ],
      "rack-3": [
        7,
        2.4,
        -7
      ],
      "exchange-pack-3": [
        7,
        3,
        -7
      ],
      "gate-3": [
        7,
        2,
        6
      ],
      "rail-4": [
        14,
        1,
        0
      ],
      "carriage-4": [
        14,
        1.5499999999999998,
        0
      ],
      "turret-4": [
        14,
        2.2,
        0
      ],
      "elbow-4": [
        14,
        4.35,
        0
      ],
      "head-4": [
        14,
        6.5875,
        0
      ],
      "petal-4": [
        14,
        7.850000000000001,
        0
      ],
      "sensor-4": [
        14,
        8.35,
        0
      ],
      "rack-4": [
        14,
        2.4,
        -7
      ],
      "exchange-pack-4": [
        14,
        3,
        -7
      ],
      "gate-4": [
        14,
        2,
        6
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节类型（h3-segmented-antenna-yard-joint-type）

carriage-0-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：spring
- B：prismatic
- C：fixed
- D：revolute

```json
{
  "input": {
    "joint": {
      "id": "carriage-0-joint",
      "name": "carriage-0 interface",
      "parent": "rail-0",
      "child": "carriage-0",
      "type": "prismatic",
      "anchorParent": [
        0,
        0.5,
        0
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
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 直接连接（h3-segmented-antenna-yard-parent）

head-0 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["elbow-0"]
- B：["head-0"]
- C：[]
- D：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0","petal-0","sensor-0","rack-0","exchange-pack-0","gate-0","rail-1","carriage-1","turret-1","elbow-1","head-1","petal-1","sensor-1","rack-1","exchange-pack-1","gate-1","rail-2","carriage-2","turret-2","elbow-2","head-2","petal-2","sensor-2","rack-2","exchange-pack-2","gate-2","rail-3","carriage-3","turret-3","elbow-3","head-3","petal-3","sensor-3","rack-3","exchange-pack-3","gate-3","rail-4","carriage-4","turret-4","elbow-4","head-4","petal-4","sensor-4","rack-4","exchange-pack-4","gate-4"]

```json
{
  "input": {
    "joints": [
      {
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
        "type": "fixed",
        "anchorParent": [
          -14,
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
        ]
      },
      {
        "id": "carriage-0-joint",
        "name": "carriage-0 interface",
        "parent": "rail-0",
        "child": "carriage-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-0-joint",
        "name": "turret-0 interface",
        "parent": "carriage-0",
        "child": "turret-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-0-joint",
        "name": "elbow-0 interface",
        "parent": "turret-0",
        "child": "elbow-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-0-joint",
        "name": "head-0 interface",
        "parent": "elbow-0",
        "child": "head-0",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-0-joint",
        "name": "petal-0 interface",
        "parent": "head-0",
        "child": "petal-0",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-0-joint",
        "name": "sensor-0 interface",
        "parent": "petal-0",
        "child": "sensor-0",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-0-joint",
        "name": "rack-0 interface",
        "parent": "frame",
        "child": "rack-0",
        "type": "fixed",
        "anchorParent": [
          -14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-0-joint",
        "name": "exchange-pack-0 interface",
        "parent": "rack-0",
        "child": "exchange-pack-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-0-joint",
        "name": "gate-0 interface",
        "parent": "frame",
        "child": "gate-0",
        "type": "revolute",
        "anchorParent": [
          -14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
        "type": "fixed",
        "anchorParent": [
          -7,
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
        ]
      },
      {
        "id": "carriage-1-joint",
        "name": "carriage-1 interface",
        "parent": "rail-1",
        "child": "carriage-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-1-joint",
        "name": "turret-1 interface",
        "parent": "carriage-1",
        "child": "turret-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-1-joint",
        "name": "elbow-1 interface",
        "parent": "turret-1",
        "child": "elbow-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-1-joint",
        "name": "head-1 interface",
        "parent": "elbow-1",
        "child": "head-1",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-1-joint",
        "name": "petal-1 interface",
        "parent": "head-1",
        "child": "petal-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-1-joint",
        "name": "sensor-1 interface",
        "parent": "petal-1",
        "child": "sensor-1",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-1-joint",
        "name": "rack-1 interface",
        "parent": "frame",
        "child": "rack-1",
        "type": "fixed",
        "anchorParent": [
          -7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-1-joint",
        "name": "exchange-pack-1 interface",
        "parent": "rack-1",
        "child": "exchange-pack-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-1-joint",
        "name": "gate-1 interface",
        "parent": "frame",
        "child": "gate-1",
        "type": "revolute",
        "anchorParent": [
          -7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          0,
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
        ]
      },
      {
        "id": "carriage-2-joint",
        "name": "carriage-2 interface",
        "parent": "rail-2",
        "child": "carriage-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-2-joint",
        "name": "turret-2 interface",
        "parent": "carriage-2",
        "child": "turret-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-2-joint",
        "name": "elbow-2 interface",
        "parent": "turret-2",
        "child": "elbow-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-2-joint",
        "name": "head-2 interface",
        "parent": "elbow-2",
        "child": "head-2",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-2-joint",
        "name": "petal-2 interface",
        "parent": "head-2",
        "child": "petal-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-2-joint",
        "name": "sensor-2 interface",
        "parent": "petal-2",
        "child": "sensor-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-2-joint",
        "name": "rack-2 interface",
        "parent": "frame",
        "child": "rack-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-2-joint",
        "name": "exchange-pack-2 interface",
        "parent": "rack-2",
        "child": "exchange-pack-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-2-joint",
        "name": "gate-2 interface",
        "parent": "frame",
        "child": "gate-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-3-joint",
        "name": "rail-3 interface",
        "parent": "frame",
        "child": "rail-3",
        "type": "fixed",
        "anchorParent": [
          7,
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
        ]
      },
      {
        "id": "carriage-3-joint",
        "name": "carriage-3 interface",
        "parent": "rail-3",
        "child": "carriage-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-3-joint",
        "name": "turret-3 interface",
        "parent": "carriage-3",
        "child": "turret-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-3-joint",
        "name": "elbow-3 interface",
        "parent": "turret-3",
        "child": "elbow-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-3-joint",
        "name": "head-3 interface",
        "parent": "elbow-3",
        "child": "head-3",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-3-joint",
        "name": "petal-3 interface",
        "parent": "head-3",
        "child": "petal-3",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-3-joint",
        "name": "sensor-3 interface",
        "parent": "petal-3",
        "child": "sensor-3",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-3-joint",
        "name": "rack-3 interface",
        "parent": "frame",
        "child": "rack-3",
        "type": "fixed",
        "anchorParent": [
          7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-3-joint",
        "name": "exchange-pack-3 interface",
        "parent": "rack-3",
        "child": "exchange-pack-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-3-joint",
        "name": "gate-3 interface",
        "parent": "frame",
        "child": "gate-3",
        "type": "revolute",
        "anchorParent": [
          7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-4-joint",
        "name": "rail-4 interface",
        "parent": "frame",
        "child": "rail-4",
        "type": "fixed",
        "anchorParent": [
          14,
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
        ]
      },
      {
        "id": "carriage-4-joint",
        "name": "carriage-4 interface",
        "parent": "rail-4",
        "child": "carriage-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-4-joint",
        "name": "turret-4 interface",
        "parent": "carriage-4",
        "child": "turret-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-4-joint",
        "name": "elbow-4 interface",
        "parent": "turret-4",
        "child": "elbow-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-4-joint",
        "name": "head-4 interface",
        "parent": "elbow-4",
        "child": "head-4",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-4-joint",
        "name": "petal-4 interface",
        "parent": "head-4",
        "child": "petal-4",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-4-joint",
        "name": "sensor-4 interface",
        "parent": "petal-4",
        "child": "sensor-4",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-4-joint",
        "name": "rack-4 interface",
        "parent": "frame",
        "child": "rack-4",
        "type": "fixed",
        "anchorParent": [
          14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-4-joint",
        "name": "exchange-pack-4 interface",
        "parent": "rack-4",
        "child": "exchange-pack-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-4-joint",
        "name": "gate-4 interface",
        "parent": "frame",
        "child": "gate-4",
        "type": "revolute",
        "anchorParent": [
          14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 基座识别（h3-segmented-antenna-yard-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0","petal-0","sensor-0","rack-0","exchange-pack-0","gate-0","rail-1","carriage-1","turret-1","elbow-1","head-1","petal-1","sensor-1","rack-1","exchange-pack-1","gate-1","rail-2","carriage-2","turret-2","elbow-2","head-2","petal-2","sensor-2","rack-2","exchange-pack-2","gate-2","rail-3","carriage-3","turret-3","elbow-3","head-3","petal-3","sensor-3","rack-3","exchange-pack-3","gate-3","rail-4","carriage-4","turret-4","elbow-4","head-4","petal-4","sensor-4","rack-4","exchange-pack-4","gate-4"]
- B：["head-0"]
- C：["frame"]
- D：[]

```json
{
  "input": {
    "modules": [
      {
        "id": "frame",
        "name": "frame",
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
        "id": "rail-0",
        "name": "rail 0",
        "role": "guide",
        "position": [
          -14,
          1,
          0
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
        "id": "carriage-0",
        "name": "carriage 0",
        "role": "linear-stage",
        "position": [
          -14,
          1.55,
          0
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
        "id": "turret-0",
        "name": "turret 0",
        "role": "rotary-stage",
        "position": [
          -14,
          2.2,
          0
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
        "id": "elbow-0",
        "name": "elbow 0",
        "role": "linkage",
        "position": [
          -14,
          4.35,
          0
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
        "id": "head-0",
        "name": "head 0",
        "role": "service-tool",
        "position": [
          -14,
          6.5875,
          0
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
        "id": "petal-0",
        "name": "petal 0",
        "role": "deployable-surface",
        "position": [
          -14,
          7.8500000000000005,
          0
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
        "id": "sensor-0",
        "name": "sensor 0",
        "role": "instrument",
        "position": [
          -14,
          8.35,
          0
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
        "id": "rack-0",
        "name": "rack 0",
        "role": "storage",
        "position": [
          -14,
          2.4,
          -7
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
        "id": "exchange-pack-0",
        "name": "exchange pack 0",
        "role": "payload",
        "position": [
          -14,
          3,
          -7
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
        "id": "gate-0",
        "name": "gate 0",
        "role": "interlock",
        "position": [
          -14,
          2,
          6
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
        "id": "rail-1",
        "name": "rail 1",
        "role": "guide",
        "position": [
          -7,
          1,
          0
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
        "id": "carriage-1",
        "name": "carriage 1",
        "role": "linear-stage",
        "position": [
          -7,
          1.55,
          0
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
        "id": "turret-1",
        "name": "turret 1",
        "role": "rotary-stage",
        "position": [
          -7,
          2.2,
          0
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
        "id": "elbow-1",
        "name": "elbow 1",
        "role": "linkage",
        "position": [
          -7,
          4.35,
          0
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
        "id": "head-1",
        "name": "head 1",
        "role": "service-tool",
        "position": [
          -7,
          6.5875,
          0
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
        "id": "petal-1",
        "name": "petal 1",
        "role": "deployable-surface",
        "position": [
          -7,
          7.8500000000000005,
          0
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
        "id": "sensor-1",
        "name": "sensor 1",
        "role": "instrument",
        "position": [
          -7,
          8.35,
          0
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
        "id": "rack-1",
        "name": "rack 1",
        "role": "storage",
        "position": [
          -7,
          2.4,
          -7
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
        "id": "exchange-pack-1",
        "name": "exchange pack 1",
        "role": "payload",
        "position": [
          -7,
          3,
          -7
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
        "id": "gate-1",
        "name": "gate 1",
        "role": "interlock",
        "position": [
          -7,
          2,
          6
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
        "id": "rail-2",
        "name": "rail 2",
        "role": "guide",
        "position": [
          0,
          1,
          0
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
        "id": "carriage-2",
        "name": "carriage 2",
        "role": "linear-stage",
        "position": [
          0,
          1.55,
          0
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
        "id": "turret-2",
        "name": "turret 2",
        "role": "rotary-stage",
        "position": [
          0,
          2.2,
          0
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
        "id": "elbow-2",
        "name": "elbow 2",
        "role": "linkage",
        "position": [
          0,
          4.35,
          0
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
        "id": "head-2",
        "name": "head 2",
        "role": "service-tool",
        "position": [
          0,
          6.5875,
          0
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
        "id": "petal-2",
        "name": "petal 2",
        "role": "deployable-surface",
        "position": [
          0,
          7.8500000000000005,
          0
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
        "id": "sensor-2",
        "name": "sensor 2",
        "role": "instrument",
        "position": [
          0,
          8.35,
          0
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
        "id": "rack-2",
        "name": "rack 2",
        "role": "storage",
        "position": [
          0,
          2.4,
          -7
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
        "id": "exchange-pack-2",
        "name": "exchange pack 2",
        "role": "payload",
        "position": [
          0,
          3,
          -7
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
        "id": "gate-2",
        "name": "gate 2",
        "role": "interlock",
        "position": [
          0,
          2,
          6
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
        "id": "rail-3",
        "name": "rail 3",
        "role": "guide",
        "position": [
          7,
          1,
          0
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
        "id": "carriage-3",
        "name": "carriage 3",
        "role": "linear-stage",
        "position": [
          7,
          1.55,
          0
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
        "id": "turret-3",
        "name": "turret 3",
        "role": "rotary-stage",
        "position": [
          7,
          2.2,
          0
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
        "id": "elbow-3",
        "name": "elbow 3",
        "role": "linkage",
        "position": [
          7,
          4.35,
          0
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
        "id": "head-3",
        "name": "head 3",
        "role": "service-tool",
        "position": [
          7,
          6.5875,
          0
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
        "id": "petal-3",
        "name": "petal 3",
        "role": "deployable-surface",
        "position": [
          7,
          7.8500000000000005,
          0
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
        "id": "sensor-3",
        "name": "sensor 3",
        "role": "instrument",
        "position": [
          7,
          8.35,
          0
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
        "id": "rack-3",
        "name": "rack 3",
        "role": "storage",
        "position": [
          7,
          2.4,
          -7
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
        "id": "exchange-pack-3",
        "name": "exchange pack 3",
        "role": "payload",
        "position": [
          7,
          3,
          -7
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
        "id": "gate-3",
        "name": "gate 3",
        "role": "interlock",
        "position": [
          7,
          2,
          6
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
        "id": "rail-4",
        "name": "rail 4",
        "role": "guide",
        "position": [
          14,
          1,
          0
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
        "id": "carriage-4",
        "name": "carriage 4",
        "role": "linear-stage",
        "position": [
          14,
          1.55,
          0
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
        "id": "turret-4",
        "name": "turret 4",
        "role": "rotary-stage",
        "position": [
          14,
          2.2,
          0
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
        "id": "elbow-4",
        "name": "elbow 4",
        "role": "linkage",
        "position": [
          14,
          4.35,
          0
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
        "id": "head-4",
        "name": "head 4",
        "role": "service-tool",
        "position": [
          14,
          6.5875,
          0
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
        "id": "petal-4",
        "name": "petal 4",
        "role": "deployable-surface",
        "position": [
          14,
          7.8500000000000005,
          0
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
        "id": "sensor-4",
        "name": "sensor 4",
        "role": "instrument",
        "position": [
          14,
          8.35,
          0
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
        "id": "rack-4",
        "name": "rack 4",
        "role": "storage",
        "position": [
          14,
          2.4,
          -7
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
        "id": "exchange-pack-4",
        "name": "exchange pack 4",
        "role": "payload",
        "position": [
          14,
          3,
          -7
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
        "id": "gate-4",
        "name": "gate 4",
        "role": "interlock",
        "position": [
          14,
          2,
          6
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
    "choiceId": "C"
  }
}
```

### 接口计数（h3-segmented-antenna-yard-degree）

head-0 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：2
- B：3
- C：1
- D：4

```json
{
  "input": {
    "joints": [
      {
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
        "type": "fixed",
        "anchorParent": [
          -14,
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
        ]
      },
      {
        "id": "carriage-0-joint",
        "name": "carriage-0 interface",
        "parent": "rail-0",
        "child": "carriage-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-0-joint",
        "name": "turret-0 interface",
        "parent": "carriage-0",
        "child": "turret-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-0-joint",
        "name": "elbow-0 interface",
        "parent": "turret-0",
        "child": "elbow-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-0-joint",
        "name": "head-0 interface",
        "parent": "elbow-0",
        "child": "head-0",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-0-joint",
        "name": "petal-0 interface",
        "parent": "head-0",
        "child": "petal-0",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-0-joint",
        "name": "sensor-0 interface",
        "parent": "petal-0",
        "child": "sensor-0",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-0-joint",
        "name": "rack-0 interface",
        "parent": "frame",
        "child": "rack-0",
        "type": "fixed",
        "anchorParent": [
          -14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-0-joint",
        "name": "exchange-pack-0 interface",
        "parent": "rack-0",
        "child": "exchange-pack-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-0-joint",
        "name": "gate-0 interface",
        "parent": "frame",
        "child": "gate-0",
        "type": "revolute",
        "anchorParent": [
          -14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
        "type": "fixed",
        "anchorParent": [
          -7,
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
        ]
      },
      {
        "id": "carriage-1-joint",
        "name": "carriage-1 interface",
        "parent": "rail-1",
        "child": "carriage-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-1-joint",
        "name": "turret-1 interface",
        "parent": "carriage-1",
        "child": "turret-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-1-joint",
        "name": "elbow-1 interface",
        "parent": "turret-1",
        "child": "elbow-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-1-joint",
        "name": "head-1 interface",
        "parent": "elbow-1",
        "child": "head-1",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-1-joint",
        "name": "petal-1 interface",
        "parent": "head-1",
        "child": "petal-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-1-joint",
        "name": "sensor-1 interface",
        "parent": "petal-1",
        "child": "sensor-1",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-1-joint",
        "name": "rack-1 interface",
        "parent": "frame",
        "child": "rack-1",
        "type": "fixed",
        "anchorParent": [
          -7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-1-joint",
        "name": "exchange-pack-1 interface",
        "parent": "rack-1",
        "child": "exchange-pack-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-1-joint",
        "name": "gate-1 interface",
        "parent": "frame",
        "child": "gate-1",
        "type": "revolute",
        "anchorParent": [
          -7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          0,
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
        ]
      },
      {
        "id": "carriage-2-joint",
        "name": "carriage-2 interface",
        "parent": "rail-2",
        "child": "carriage-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-2-joint",
        "name": "turret-2 interface",
        "parent": "carriage-2",
        "child": "turret-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-2-joint",
        "name": "elbow-2 interface",
        "parent": "turret-2",
        "child": "elbow-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-2-joint",
        "name": "head-2 interface",
        "parent": "elbow-2",
        "child": "head-2",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-2-joint",
        "name": "petal-2 interface",
        "parent": "head-2",
        "child": "petal-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-2-joint",
        "name": "sensor-2 interface",
        "parent": "petal-2",
        "child": "sensor-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-2-joint",
        "name": "rack-2 interface",
        "parent": "frame",
        "child": "rack-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-2-joint",
        "name": "exchange-pack-2 interface",
        "parent": "rack-2",
        "child": "exchange-pack-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-2-joint",
        "name": "gate-2 interface",
        "parent": "frame",
        "child": "gate-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-3-joint",
        "name": "rail-3 interface",
        "parent": "frame",
        "child": "rail-3",
        "type": "fixed",
        "anchorParent": [
          7,
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
        ]
      },
      {
        "id": "carriage-3-joint",
        "name": "carriage-3 interface",
        "parent": "rail-3",
        "child": "carriage-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-3-joint",
        "name": "turret-3 interface",
        "parent": "carriage-3",
        "child": "turret-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-3-joint",
        "name": "elbow-3 interface",
        "parent": "turret-3",
        "child": "elbow-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-3-joint",
        "name": "head-3 interface",
        "parent": "elbow-3",
        "child": "head-3",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-3-joint",
        "name": "petal-3 interface",
        "parent": "head-3",
        "child": "petal-3",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-3-joint",
        "name": "sensor-3 interface",
        "parent": "petal-3",
        "child": "sensor-3",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-3-joint",
        "name": "rack-3 interface",
        "parent": "frame",
        "child": "rack-3",
        "type": "fixed",
        "anchorParent": [
          7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-3-joint",
        "name": "exchange-pack-3 interface",
        "parent": "rack-3",
        "child": "exchange-pack-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-3-joint",
        "name": "gate-3 interface",
        "parent": "frame",
        "child": "gate-3",
        "type": "revolute",
        "anchorParent": [
          7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-4-joint",
        "name": "rail-4 interface",
        "parent": "frame",
        "child": "rail-4",
        "type": "fixed",
        "anchorParent": [
          14,
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
        ]
      },
      {
        "id": "carriage-4-joint",
        "name": "carriage-4 interface",
        "parent": "rail-4",
        "child": "carriage-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-4-joint",
        "name": "turret-4 interface",
        "parent": "carriage-4",
        "child": "turret-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-4-joint",
        "name": "elbow-4 interface",
        "parent": "turret-4",
        "child": "elbow-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-4-joint",
        "name": "head-4 interface",
        "parent": "elbow-4",
        "child": "head-4",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-4-joint",
        "name": "petal-4 interface",
        "parent": "head-4",
        "child": "petal-4",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-4-joint",
        "name": "sensor-4 interface",
        "parent": "petal-4",
        "child": "sensor-4",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-4-joint",
        "name": "rack-4 interface",
        "parent": "frame",
        "child": "rack-4",
        "type": "fixed",
        "anchorParent": [
          14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-4-joint",
        "name": "exchange-pack-4 interface",
        "parent": "rack-4",
        "child": "exchange-pack-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-4-joint",
        "name": "gate-4 interface",
        "parent": "frame",
        "child": "gate-4",
        "type": "revolute",
        "anchorParent": [
          14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 局部改色（h3-segmented-antenna-yard-recolor）

仅将 head-0-p108 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"*","color":"#e8792e"}
- B：{"id":"head-0-p108","color":"#e8792e"}
- C：{"id":"head-0-p109","color":"#e8792e"}
- D：{"id":"head-0-p108","color":"#2878b8"}

```json
{
  "input": {
    "part": {
      "id": "head-0-p108",
      "moduleId": "head-0",
      "shape": "arch",
      "position": [
        0,
        -0.08750000000000002,
        0
      ],
      "size": [
        1.6,
        0.7,
        1
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

### 补装部件（h3-segmented-antenna-yard-add）

模块 head-0 缺失零件 head-0-p108。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"head-0-p108","moduleId":"head-0","shape":"arch","position":[0,-0.08750000000000002,0],"size":[1.6,0.7,1],"color":"#45a080","rotation":[0,0,0,1]}
- B：{"id":"head-0-p108","moduleId":"frame","shape":"arch","position":[0,-0.08750000000000002,0],"size":[1.6,0.7,1],"color":"#45a080","rotation":[0,0,0,1]}
- C：{"id":"head-0-p108","moduleId":"head-0","shape":"arch","position":[0,-0.08750000000000002,0],"size":[3,3,3],"color":"#45a080","rotation":[0,0,0,1]}
- D：{"id":"head-0-p108","moduleId":"head-0","shape":"arch","position":[0,-0.08750000000000002,0],"size":[1.6,0.7,1],"color":"#000000","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "head-0-p108",
      "moduleId": "head-0",
      "shape": "arch",
      "position": [
        0,
        -0.08750000000000002,
        0
      ],
      "size": [
        1.6,
        0.7,
        1
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
      "frame-p1",
      "frame-p2",
      "frame-p3",
      "frame-p4",
      "frame-p5",
      "frame-p6",
      "frame-p7",
      "frame-p8",
      "frame-p9",
      "frame-p10",
      "frame-p11",
      "frame-p12",
      "frame-p13",
      "frame-p14",
      "frame-p15",
      "frame-p16",
      "frame-p17",
      "frame-p18",
      "frame-p19",
      "frame-p20",
      "frame-p21",
      "frame-p22",
      "frame-p23",
      "frame-p24",
      "frame-p25",
      "frame-p26",
      "frame-p27",
      "frame-p28",
      "frame-p29",
      "frame-p30",
      "frame-p31",
      "frame-p32",
      "frame-p33",
      "frame-p34",
      "frame-p35",
      "frame-p36",
      "frame-p37",
      "frame-p38",
      "frame-p39",
      "frame-p40",
      "frame-p41",
      "frame-p42",
      "frame-p43",
      "frame-p44",
      "frame-p45",
      "frame-p46",
      "frame-p47",
      "frame-p48",
      "frame-p49",
      "frame-p50",
      "frame-p51",
      "frame-p52",
      "frame-p53",
      "frame-p54",
      "frame-p55",
      "frame-p56",
      "frame-p57",
      "frame-p58",
      "frame-p59",
      "frame-p60",
      "frame-p61",
      "frame-p62",
      "frame-p63",
      "frame-p64",
      "frame-p65",
      "frame-p66",
      "frame-p67",
      "frame-p68",
      "frame-p69",
      "frame-p70",
      "frame-p71",
      "frame-p72",
      "frame-p73",
      "frame-p74",
      "frame-p75",
      "frame-p76",
      "frame-p77",
      "frame-p78",
      "frame-p79",
      "frame-p80",
      "frame-p81",
      "frame-p82",
      "frame-p83",
      "frame-p84",
      "frame-p85",
      "frame-p86",
      "frame-p87",
      "frame-p88",
      "frame-p89",
      "frame-p90",
      "frame-p91",
      "frame-p92",
      "frame-p93",
      "frame-p94",
      "frame-p95",
      "frame-p96",
      "frame-p97",
      "frame-p98",
      "frame-p99",
      "frame-p100",
      "rail-0-p101",
      "carriage-0-p102",
      "carriage-0-p103",
      "carriage-0-p104",
      "carriage-0-p105",
      "turret-0-p106",
      "elbow-0-p107",
      "head-0-p109",
      "petal-0-p110",
      "petal-0-p111",
      "petal-0-p112",
      "petal-0-p113",
      "petal-0-p114",
      "petal-0-p115",
      "petal-0-p116",
      "petal-0-p117",
      "petal-0-p118",
      "petal-0-p119",
      "petal-0-p120",
      "petal-0-p121",
      "petal-0-p122",
      "petal-0-p123",
      "petal-0-p124",
      "sensor-0-p125",
      "rack-0-p126",
      "rack-0-p127",
      "rack-0-p128",
      "rack-0-p129",
      "rack-0-p130",
      "rack-0-p131",
      "rack-0-p132",
      "rack-0-p133",
      "rack-0-p134",
      "rack-0-p135",
      "rack-0-p136",
      "rack-0-p137",
      "rack-0-p138",
      "rack-0-p139",
      "rack-0-p140",
      "rack-0-p141",
      "rack-0-p142",
      "rack-0-p143",
      "rack-0-p144",
      "rack-0-p145",
      "rack-0-p146",
      "rack-0-p147",
      "rack-0-p148",
      "rack-0-p149",
      "rack-0-p150",
      "rack-0-p151",
      "rack-0-p152",
      "rack-0-p153",
      "rack-0-p154",
      "rack-0-p155",
      "rack-0-p156",
      "rack-0-p157",
      "rack-0-p158",
      "rack-0-p159",
      "rack-0-p160",
      "rack-0-p161",
      "rack-0-p162",
      "rack-0-p163",
      "exchange-pack-0-p164",
      "gate-0-p165",
      "rail-1-p166",
      "carriage-1-p167",
      "carriage-1-p168",
      "carriage-1-p169",
      "carriage-1-p170",
      "turret-1-p171",
      "elbow-1-p172",
      "head-1-p173",
      "head-1-p174",
      "petal-1-p175",
      "petal-1-p176",
      "petal-1-p177",
      "petal-1-p178",
      "petal-1-p179",
      "petal-1-p180",
      "petal-1-p181",
      "petal-1-p182",
      "petal-1-p183",
      "petal-1-p184",
      "petal-1-p185",
      "petal-1-p186",
      "petal-1-p187",
      "petal-1-p188",
      "petal-1-p189",
      "sensor-1-p190",
      "rack-1-p191",
      "rack-1-p192",
      "rack-1-p193",
      "rack-1-p194",
      "rack-1-p195",
      "rack-1-p196",
      "rack-1-p197",
      "rack-1-p198",
      "rack-1-p199",
      "rack-1-p200",
      "rack-1-p201",
      "rack-1-p202",
      "rack-1-p203",
      "rack-1-p204",
      "rack-1-p205",
      "rack-1-p206",
      "rack-1-p207",
      "rack-1-p208",
      "rack-1-p209",
      "rack-1-p210",
      "rack-1-p211",
      "rack-1-p212",
      "rack-1-p213",
      "rack-1-p214",
      "rack-1-p215",
      "rack-1-p216",
      "rack-1-p217",
      "rack-1-p218",
      "rack-1-p219",
      "rack-1-p220",
      "rack-1-p221",
      "rack-1-p222",
      "rack-1-p223",
      "rack-1-p224",
      "rack-1-p225",
      "rack-1-p226",
      "rack-1-p227",
      "rack-1-p228",
      "exchange-pack-1-p229",
      "gate-1-p230",
      "rail-2-p231",
      "carriage-2-p232",
      "carriage-2-p233",
      "carriage-2-p234",
      "carriage-2-p235",
      "turret-2-p236",
      "elbow-2-p237",
      "head-2-p238",
      "head-2-p239",
      "petal-2-p240",
      "petal-2-p241",
      "petal-2-p242",
      "petal-2-p243",
      "petal-2-p244",
      "petal-2-p245",
      "petal-2-p246",
      "petal-2-p247",
      "petal-2-p248",
      "petal-2-p249",
      "petal-2-p250",
      "petal-2-p251",
      "petal-2-p252",
      "petal-2-p253",
      "petal-2-p254",
      "sensor-2-p255",
      "rack-2-p256",
      "rack-2-p257",
      "rack-2-p258",
      "rack-2-p259",
      "rack-2-p260",
      "rack-2-p261",
      "rack-2-p262",
      "rack-2-p263",
      "rack-2-p264",
      "rack-2-p265",
      "rack-2-p266",
      "rack-2-p267",
      "rack-2-p268",
      "rack-2-p269",
      "rack-2-p270",
      "rack-2-p271",
      "rack-2-p272",
      "rack-2-p273",
      "rack-2-p274",
      "rack-2-p275",
      "rack-2-p276",
      "rack-2-p277",
      "rack-2-p278",
      "rack-2-p279",
      "rack-2-p280",
      "rack-2-p281",
      "rack-2-p282",
      "rack-2-p283",
      "rack-2-p284",
      "rack-2-p285",
      "rack-2-p286",
      "rack-2-p287",
      "rack-2-p288",
      "rack-2-p289",
      "rack-2-p290",
      "rack-2-p291",
      "rack-2-p292",
      "rack-2-p293",
      "exchange-pack-2-p294",
      "gate-2-p295",
      "rail-3-p296",
      "carriage-3-p297",
      "carriage-3-p298",
      "carriage-3-p299",
      "carriage-3-p300",
      "turret-3-p301",
      "elbow-3-p302",
      "head-3-p303",
      "head-3-p304",
      "petal-3-p305",
      "petal-3-p306",
      "petal-3-p307",
      "petal-3-p308",
      "petal-3-p309",
      "petal-3-p310",
      "petal-3-p311",
      "petal-3-p312",
      "petal-3-p313",
      "petal-3-p314",
      "petal-3-p315",
      "petal-3-p316",
      "petal-3-p317",
      "petal-3-p318",
      "petal-3-p319",
      "sensor-3-p320",
      "rack-3-p321",
      "rack-3-p322",
      "rack-3-p323",
      "rack-3-p324",
      "rack-3-p325",
      "rack-3-p326",
      "rack-3-p327",
      "rack-3-p328",
      "rack-3-p329",
      "rack-3-p330",
      "rack-3-p331",
      "rack-3-p332",
      "rack-3-p333",
      "rack-3-p334",
      "rack-3-p335",
      "rack-3-p336",
      "rack-3-p337",
      "rack-3-p338",
      "rack-3-p339",
      "rack-3-p340",
      "rack-3-p341",
      "rack-3-p342",
      "rack-3-p343",
      "rack-3-p344",
      "rack-3-p345",
      "rack-3-p346",
      "rack-3-p347",
      "rack-3-p348",
      "rack-3-p349",
      "rack-3-p350",
      "rack-3-p351",
      "rack-3-p352",
      "rack-3-p353",
      "rack-3-p354",
      "rack-3-p355",
      "rack-3-p356",
      "rack-3-p357",
      "rack-3-p358",
      "exchange-pack-3-p359",
      "gate-3-p360",
      "rail-4-p361",
      "carriage-4-p362",
      "carriage-4-p363",
      "carriage-4-p364",
      "carriage-4-p365",
      "turret-4-p366",
      "elbow-4-p367",
      "head-4-p368",
      "head-4-p369",
      "petal-4-p370",
      "petal-4-p371",
      "petal-4-p372",
      "petal-4-p373",
      "petal-4-p374",
      "petal-4-p375",
      "petal-4-p376",
      "petal-4-p377",
      "petal-4-p378",
      "petal-4-p379",
      "petal-4-p380",
      "petal-4-p381",
      "petal-4-p382",
      "petal-4-p383",
      "petal-4-p384",
      "sensor-4-p385",
      "rack-4-p386",
      "rack-4-p387",
      "rack-4-p388",
      "rack-4-p389",
      "rack-4-p390",
      "rack-4-p391",
      "rack-4-p392",
      "rack-4-p393",
      "rack-4-p394",
      "rack-4-p395",
      "rack-4-p396",
      "rack-4-p397",
      "rack-4-p398",
      "rack-4-p399",
      "rack-4-p400",
      "rack-4-p401",
      "rack-4-p402",
      "rack-4-p403",
      "rack-4-p404",
      "rack-4-p405",
      "rack-4-p406",
      "rack-4-p407",
      "rack-4-p408",
      "rack-4-p409",
      "rack-4-p410",
      "rack-4-p411",
      "rack-4-p412",
      "rack-4-p413",
      "rack-4-p414",
      "rack-4-p415",
      "rack-4-p416",
      "rack-4-p417",
      "rack-4-p418",
      "rack-4-p419",
      "rack-4-p420",
      "rack-4-p421",
      "rack-4-p422",
      "rack-4-p423",
      "exchange-pack-4-p424",
      "gate-4-p425"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全拆除（h3-segmented-antenna-yard-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：[]
- B：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0","petal-0","sensor-0","rack-0","exchange-pack-0","gate-0","rail-1","carriage-1","turret-1","elbow-1","head-1","petal-1","sensor-1","rack-1","exchange-pack-1","gate-1","rail-2","carriage-2","turret-2","elbow-2","head-2","petal-2","sensor-2","rack-2","exchange-pack-2","gate-2","rail-3","carriage-3","turret-3","elbow-3","head-3","petal-3","sensor-3","rack-3","exchange-pack-3","gate-3","rail-4","carriage-4","turret-4","elbow-4","head-4","petal-4","sensor-4","rack-4","exchange-pack-4","gate-4"]
- C：["exchange-pack-0","exchange-pack-1","exchange-pack-2","exchange-pack-3","exchange-pack-4","gate-0","gate-1","gate-2","gate-3","gate-4","sensor-0","sensor-1","sensor-2","sensor-3","sensor-4"]
- D：["frame"]

```json
{
  "input": {
    "joints": [
      {
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
        "type": "fixed",
        "anchorParent": [
          -14,
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
        ]
      },
      {
        "id": "carriage-0-joint",
        "name": "carriage-0 interface",
        "parent": "rail-0",
        "child": "carriage-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-0-joint",
        "name": "turret-0 interface",
        "parent": "carriage-0",
        "child": "turret-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-0-joint",
        "name": "elbow-0 interface",
        "parent": "turret-0",
        "child": "elbow-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-0-joint",
        "name": "head-0 interface",
        "parent": "elbow-0",
        "child": "head-0",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-0-joint",
        "name": "petal-0 interface",
        "parent": "head-0",
        "child": "petal-0",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-0-joint",
        "name": "sensor-0 interface",
        "parent": "petal-0",
        "child": "sensor-0",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-0-joint",
        "name": "rack-0 interface",
        "parent": "frame",
        "child": "rack-0",
        "type": "fixed",
        "anchorParent": [
          -14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-0-joint",
        "name": "exchange-pack-0 interface",
        "parent": "rack-0",
        "child": "exchange-pack-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-0-joint",
        "name": "gate-0 interface",
        "parent": "frame",
        "child": "gate-0",
        "type": "revolute",
        "anchorParent": [
          -14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
        "type": "fixed",
        "anchorParent": [
          -7,
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
        ]
      },
      {
        "id": "carriage-1-joint",
        "name": "carriage-1 interface",
        "parent": "rail-1",
        "child": "carriage-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-1-joint",
        "name": "turret-1 interface",
        "parent": "carriage-1",
        "child": "turret-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-1-joint",
        "name": "elbow-1 interface",
        "parent": "turret-1",
        "child": "elbow-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-1-joint",
        "name": "head-1 interface",
        "parent": "elbow-1",
        "child": "head-1",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-1-joint",
        "name": "petal-1 interface",
        "parent": "head-1",
        "child": "petal-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-1-joint",
        "name": "sensor-1 interface",
        "parent": "petal-1",
        "child": "sensor-1",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-1-joint",
        "name": "rack-1 interface",
        "parent": "frame",
        "child": "rack-1",
        "type": "fixed",
        "anchorParent": [
          -7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-1-joint",
        "name": "exchange-pack-1 interface",
        "parent": "rack-1",
        "child": "exchange-pack-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-1-joint",
        "name": "gate-1 interface",
        "parent": "frame",
        "child": "gate-1",
        "type": "revolute",
        "anchorParent": [
          -7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          0,
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
        ]
      },
      {
        "id": "carriage-2-joint",
        "name": "carriage-2 interface",
        "parent": "rail-2",
        "child": "carriage-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-2-joint",
        "name": "turret-2 interface",
        "parent": "carriage-2",
        "child": "turret-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-2-joint",
        "name": "elbow-2 interface",
        "parent": "turret-2",
        "child": "elbow-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-2-joint",
        "name": "head-2 interface",
        "parent": "elbow-2",
        "child": "head-2",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-2-joint",
        "name": "petal-2 interface",
        "parent": "head-2",
        "child": "petal-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-2-joint",
        "name": "sensor-2 interface",
        "parent": "petal-2",
        "child": "sensor-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-2-joint",
        "name": "rack-2 interface",
        "parent": "frame",
        "child": "rack-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-2-joint",
        "name": "exchange-pack-2 interface",
        "parent": "rack-2",
        "child": "exchange-pack-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-2-joint",
        "name": "gate-2 interface",
        "parent": "frame",
        "child": "gate-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-3-joint",
        "name": "rail-3 interface",
        "parent": "frame",
        "child": "rail-3",
        "type": "fixed",
        "anchorParent": [
          7,
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
        ]
      },
      {
        "id": "carriage-3-joint",
        "name": "carriage-3 interface",
        "parent": "rail-3",
        "child": "carriage-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-3-joint",
        "name": "turret-3 interface",
        "parent": "carriage-3",
        "child": "turret-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-3-joint",
        "name": "elbow-3 interface",
        "parent": "turret-3",
        "child": "elbow-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-3-joint",
        "name": "head-3 interface",
        "parent": "elbow-3",
        "child": "head-3",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-3-joint",
        "name": "petal-3 interface",
        "parent": "head-3",
        "child": "petal-3",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-3-joint",
        "name": "sensor-3 interface",
        "parent": "petal-3",
        "child": "sensor-3",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-3-joint",
        "name": "rack-3 interface",
        "parent": "frame",
        "child": "rack-3",
        "type": "fixed",
        "anchorParent": [
          7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-3-joint",
        "name": "exchange-pack-3 interface",
        "parent": "rack-3",
        "child": "exchange-pack-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-3-joint",
        "name": "gate-3 interface",
        "parent": "frame",
        "child": "gate-3",
        "type": "revolute",
        "anchorParent": [
          7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-4-joint",
        "name": "rail-4 interface",
        "parent": "frame",
        "child": "rail-4",
        "type": "fixed",
        "anchorParent": [
          14,
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
        ]
      },
      {
        "id": "carriage-4-joint",
        "name": "carriage-4 interface",
        "parent": "rail-4",
        "child": "carriage-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-4-joint",
        "name": "turret-4 interface",
        "parent": "carriage-4",
        "child": "turret-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-4-joint",
        "name": "elbow-4 interface",
        "parent": "turret-4",
        "child": "elbow-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-4-joint",
        "name": "head-4 interface",
        "parent": "elbow-4",
        "child": "head-4",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-4-joint",
        "name": "petal-4 interface",
        "parent": "head-4",
        "child": "petal-4",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-4-joint",
        "name": "sensor-4 interface",
        "parent": "petal-4",
        "child": "sensor-4",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-4-joint",
        "name": "rack-4 interface",
        "parent": "frame",
        "child": "rack-4",
        "type": "fixed",
        "anchorParent": [
          14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-4-joint",
        "name": "exchange-pack-4 interface",
        "parent": "rack-4",
        "child": "exchange-pack-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-4-joint",
        "name": "gate-4 interface",
        "parent": "frame",
        "child": "gate-4",
        "type": "revolute",
        "anchorParent": [
          14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
      }
    ],
    "modules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0",
      "petal-0",
      "sensor-0",
      "rack-0",
      "exchange-pack-0",
      "gate-0",
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rack-1",
      "exchange-pack-1",
      "gate-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2",
      "rack-2",
      "exchange-pack-2",
      "gate-2",
      "rail-3",
      "carriage-3",
      "turret-3",
      "elbow-3",
      "head-3",
      "petal-3",
      "sensor-3",
      "rack-3",
      "exchange-pack-3",
      "gate-3",
      "rail-4",
      "carriage-4",
      "turret-4",
      "elbow-4",
      "head-4",
      "petal-4",
      "sensor-4",
      "rack-4",
      "exchange-pack-4",
      "gate-4"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 替换选择（h3-segmented-antenna-yard-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-1
- B：stock-3
- C：stock-2
- D：stock-0

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 3,
        "stiffness": 9,
        "mass": 0.8
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 3,
        "mass": 1
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 11,
        "mass": 1
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 4,
        "mass": 1.8
      }
    ],
    "maxCost": 7
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 平移纠偏（h3-segmented-antenna-yard-translate）

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
    "target": "head-0"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-segmented-antenna-yard-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：45
- B：-45
- C：0
- D：90

```json
{
  "input": {
    "module": "head-0",
    "currentYaw": 0,
    "targetYaw": 45
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 下一步放置（h3-segmented-antenna-yard-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0","petal-0","sensor-0","rack-0","exchange-pack-0","gate-0","rail-1","carriage-1","turret-1","elbow-1","head-1","petal-1","sensor-1","rack-1","exchange-pack-1","gate-1","rail-2","carriage-2","turret-2","elbow-2","head-2"]
- B：["petal-2","sensor-2","rack-2","exchange-pack-2","gate-2","rail-3","carriage-3","turret-3","elbow-3","head-3","petal-3","sensor-3","rack-3","exchange-pack-3","gate-3","rail-4","carriage-4","turret-4","elbow-4","head-4","petal-4","sensor-4","rack-4","exchange-pack-4","gate-4"]
- C：["gate-2","gate-3","gate-4","petal-2","rack-2","rack-3","rack-4","rail-3","rail-4"]
- D：[]

```json
{
  "input": {
    "prefix": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0",
      "petal-0",
      "sensor-0",
      "rack-0",
      "exchange-pack-0",
      "gate-0",
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rack-1",
      "exchange-pack-1",
      "gate-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2"
    ],
    "joints": [
      {
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
        "type": "fixed",
        "anchorParent": [
          -14,
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
        ]
      },
      {
        "id": "carriage-0-joint",
        "name": "carriage-0 interface",
        "parent": "rail-0",
        "child": "carriage-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-0-joint",
        "name": "turret-0 interface",
        "parent": "carriage-0",
        "child": "turret-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-0-joint",
        "name": "elbow-0 interface",
        "parent": "turret-0",
        "child": "elbow-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-0-joint",
        "name": "head-0 interface",
        "parent": "elbow-0",
        "child": "head-0",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-0-joint",
        "name": "petal-0 interface",
        "parent": "head-0",
        "child": "petal-0",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-0-joint",
        "name": "sensor-0 interface",
        "parent": "petal-0",
        "child": "sensor-0",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-0-joint",
        "name": "rack-0 interface",
        "parent": "frame",
        "child": "rack-0",
        "type": "fixed",
        "anchorParent": [
          -14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-0-joint",
        "name": "exchange-pack-0 interface",
        "parent": "rack-0",
        "child": "exchange-pack-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-0-joint",
        "name": "gate-0 interface",
        "parent": "frame",
        "child": "gate-0",
        "type": "revolute",
        "anchorParent": [
          -14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
        "type": "fixed",
        "anchorParent": [
          -7,
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
        ]
      },
      {
        "id": "carriage-1-joint",
        "name": "carriage-1 interface",
        "parent": "rail-1",
        "child": "carriage-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-1-joint",
        "name": "turret-1 interface",
        "parent": "carriage-1",
        "child": "turret-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-1-joint",
        "name": "elbow-1 interface",
        "parent": "turret-1",
        "child": "elbow-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-1-joint",
        "name": "head-1 interface",
        "parent": "elbow-1",
        "child": "head-1",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-1-joint",
        "name": "petal-1 interface",
        "parent": "head-1",
        "child": "petal-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-1-joint",
        "name": "sensor-1 interface",
        "parent": "petal-1",
        "child": "sensor-1",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-1-joint",
        "name": "rack-1 interface",
        "parent": "frame",
        "child": "rack-1",
        "type": "fixed",
        "anchorParent": [
          -7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-1-joint",
        "name": "exchange-pack-1 interface",
        "parent": "rack-1",
        "child": "exchange-pack-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-1-joint",
        "name": "gate-1 interface",
        "parent": "frame",
        "child": "gate-1",
        "type": "revolute",
        "anchorParent": [
          -7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          0,
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
        ]
      },
      {
        "id": "carriage-2-joint",
        "name": "carriage-2 interface",
        "parent": "rail-2",
        "child": "carriage-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-2-joint",
        "name": "turret-2 interface",
        "parent": "carriage-2",
        "child": "turret-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-2-joint",
        "name": "elbow-2 interface",
        "parent": "turret-2",
        "child": "elbow-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-2-joint",
        "name": "head-2 interface",
        "parent": "elbow-2",
        "child": "head-2",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-2-joint",
        "name": "petal-2 interface",
        "parent": "head-2",
        "child": "petal-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-2-joint",
        "name": "sensor-2 interface",
        "parent": "petal-2",
        "child": "sensor-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-2-joint",
        "name": "rack-2 interface",
        "parent": "frame",
        "child": "rack-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-2-joint",
        "name": "exchange-pack-2 interface",
        "parent": "rack-2",
        "child": "exchange-pack-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-2-joint",
        "name": "gate-2 interface",
        "parent": "frame",
        "child": "gate-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-3-joint",
        "name": "rail-3 interface",
        "parent": "frame",
        "child": "rail-3",
        "type": "fixed",
        "anchorParent": [
          7,
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
        ]
      },
      {
        "id": "carriage-3-joint",
        "name": "carriage-3 interface",
        "parent": "rail-3",
        "child": "carriage-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-3-joint",
        "name": "turret-3 interface",
        "parent": "carriage-3",
        "child": "turret-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-3-joint",
        "name": "elbow-3 interface",
        "parent": "turret-3",
        "child": "elbow-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-3-joint",
        "name": "head-3 interface",
        "parent": "elbow-3",
        "child": "head-3",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-3-joint",
        "name": "petal-3 interface",
        "parent": "head-3",
        "child": "petal-3",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-3-joint",
        "name": "sensor-3 interface",
        "parent": "petal-3",
        "child": "sensor-3",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-3-joint",
        "name": "rack-3 interface",
        "parent": "frame",
        "child": "rack-3",
        "type": "fixed",
        "anchorParent": [
          7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-3-joint",
        "name": "exchange-pack-3 interface",
        "parent": "rack-3",
        "child": "exchange-pack-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-3-joint",
        "name": "gate-3 interface",
        "parent": "frame",
        "child": "gate-3",
        "type": "revolute",
        "anchorParent": [
          7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-4-joint",
        "name": "rail-4 interface",
        "parent": "frame",
        "child": "rail-4",
        "type": "fixed",
        "anchorParent": [
          14,
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
        ]
      },
      {
        "id": "carriage-4-joint",
        "name": "carriage-4 interface",
        "parent": "rail-4",
        "child": "carriage-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-4-joint",
        "name": "turret-4 interface",
        "parent": "carriage-4",
        "child": "turret-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-4-joint",
        "name": "elbow-4 interface",
        "parent": "turret-4",
        "child": "elbow-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-4-joint",
        "name": "head-4 interface",
        "parent": "elbow-4",
        "child": "head-4",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-4-joint",
        "name": "petal-4 interface",
        "parent": "head-4",
        "child": "petal-4",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-4-joint",
        "name": "sensor-4 interface",
        "parent": "petal-4",
        "child": "sensor-4",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-4-joint",
        "name": "rack-4 interface",
        "parent": "frame",
        "child": "rack-4",
        "type": "fixed",
        "anchorParent": [
          14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-4-joint",
        "name": "exchange-pack-4 interface",
        "parent": "rack-4",
        "child": "exchange-pack-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-4-joint",
        "name": "gate-4 interface",
        "parent": "frame",
        "child": "gate-4",
        "type": "revolute",
        "anchorParent": [
          14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
      }
    ],
    "modules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0",
      "petal-0",
      "sensor-0",
      "rack-0",
      "exchange-pack-0",
      "gate-0",
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rack-1",
      "exchange-pack-1",
      "gate-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2",
      "rack-2",
      "exchange-pack-2",
      "gate-2",
      "rail-3",
      "carriage-3",
      "turret-3",
      "elbow-3",
      "head-3",
      "petal-3",
      "sensor-3",
      "rack-3",
      "exchange-pack-3",
      "gate-3",
      "rail-4",
      "carriage-4",
      "turret-4",
      "elbow-4",
      "head-4",
      "petal-4",
      "sensor-4",
      "rack-4",
      "exchange-pack-4",
      "gate-4"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 库存核算（h3-segmented-antenna-yard-inventory）

备件库有 6 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：7
- B：4
- C：5
- D：3

```json
{
  "input": {
    "available": 6,
    "required": 2
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 子装配边界（h3-segmented-antenna-yard-boundary）

隔离 head-0 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["head-0-joint","petal-0-joint"]
- B：[]
- C：["rail-0-joint","carriage-0-joint","turret-0-joint","elbow-0-joint","head-0-joint","petal-0-joint","sensor-0-joint","rack-0-joint","exchange-pack-0-joint","gate-0-joint","rail-1-joint","carriage-1-joint","turret-1-joint","elbow-1-joint","head-1-joint","petal-1-joint","sensor-1-joint","rack-1-joint","exchange-pack-1-joint","gate-1-joint","rail-2-joint","carriage-2-joint","turret-2-joint","elbow-2-joint","head-2-joint","petal-2-joint","sensor-2-joint","rack-2-joint","exchange-pack-2-joint","gate-2-joint","rail-3-joint","carriage-3-joint","turret-3-joint","elbow-3-joint","head-3-joint","petal-3-joint","sensor-3-joint","rack-3-joint","exchange-pack-3-joint","gate-3-joint","rail-4-joint","carriage-4-joint","turret-4-joint","elbow-4-joint","head-4-joint","petal-4-joint","sensor-4-joint","rack-4-joint","exchange-pack-4-joint","gate-4-joint"]
- D：["carriage-0-joint"]

```json
{
  "input": {
    "joints": [
      {
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
        "type": "fixed",
        "anchorParent": [
          -14,
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
        ]
      },
      {
        "id": "carriage-0-joint",
        "name": "carriage-0 interface",
        "parent": "rail-0",
        "child": "carriage-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-0-joint",
        "name": "turret-0 interface",
        "parent": "carriage-0",
        "child": "turret-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-0-joint",
        "name": "elbow-0 interface",
        "parent": "turret-0",
        "child": "elbow-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-0-joint",
        "name": "head-0 interface",
        "parent": "elbow-0",
        "child": "head-0",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-0-joint",
        "name": "petal-0 interface",
        "parent": "head-0",
        "child": "petal-0",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-0-joint",
        "name": "sensor-0 interface",
        "parent": "petal-0",
        "child": "sensor-0",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-0-joint",
        "name": "rack-0 interface",
        "parent": "frame",
        "child": "rack-0",
        "type": "fixed",
        "anchorParent": [
          -14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-0-joint",
        "name": "exchange-pack-0 interface",
        "parent": "rack-0",
        "child": "exchange-pack-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-0-joint",
        "name": "gate-0 interface",
        "parent": "frame",
        "child": "gate-0",
        "type": "revolute",
        "anchorParent": [
          -14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
        "type": "fixed",
        "anchorParent": [
          -7,
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
        ]
      },
      {
        "id": "carriage-1-joint",
        "name": "carriage-1 interface",
        "parent": "rail-1",
        "child": "carriage-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-1-joint",
        "name": "turret-1 interface",
        "parent": "carriage-1",
        "child": "turret-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-1-joint",
        "name": "elbow-1 interface",
        "parent": "turret-1",
        "child": "elbow-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-1-joint",
        "name": "head-1 interface",
        "parent": "elbow-1",
        "child": "head-1",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-1-joint",
        "name": "petal-1 interface",
        "parent": "head-1",
        "child": "petal-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-1-joint",
        "name": "sensor-1 interface",
        "parent": "petal-1",
        "child": "sensor-1",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-1-joint",
        "name": "rack-1 interface",
        "parent": "frame",
        "child": "rack-1",
        "type": "fixed",
        "anchorParent": [
          -7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-1-joint",
        "name": "exchange-pack-1 interface",
        "parent": "rack-1",
        "child": "exchange-pack-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-1-joint",
        "name": "gate-1 interface",
        "parent": "frame",
        "child": "gate-1",
        "type": "revolute",
        "anchorParent": [
          -7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          0,
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
        ]
      },
      {
        "id": "carriage-2-joint",
        "name": "carriage-2 interface",
        "parent": "rail-2",
        "child": "carriage-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-2-joint",
        "name": "turret-2 interface",
        "parent": "carriage-2",
        "child": "turret-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-2-joint",
        "name": "elbow-2 interface",
        "parent": "turret-2",
        "child": "elbow-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-2-joint",
        "name": "head-2 interface",
        "parent": "elbow-2",
        "child": "head-2",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-2-joint",
        "name": "petal-2 interface",
        "parent": "head-2",
        "child": "petal-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-2-joint",
        "name": "sensor-2 interface",
        "parent": "petal-2",
        "child": "sensor-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-2-joint",
        "name": "rack-2 interface",
        "parent": "frame",
        "child": "rack-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-2-joint",
        "name": "exchange-pack-2 interface",
        "parent": "rack-2",
        "child": "exchange-pack-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-2-joint",
        "name": "gate-2 interface",
        "parent": "frame",
        "child": "gate-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-3-joint",
        "name": "rail-3 interface",
        "parent": "frame",
        "child": "rail-3",
        "type": "fixed",
        "anchorParent": [
          7,
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
        ]
      },
      {
        "id": "carriage-3-joint",
        "name": "carriage-3 interface",
        "parent": "rail-3",
        "child": "carriage-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-3-joint",
        "name": "turret-3 interface",
        "parent": "carriage-3",
        "child": "turret-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-3-joint",
        "name": "elbow-3 interface",
        "parent": "turret-3",
        "child": "elbow-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-3-joint",
        "name": "head-3 interface",
        "parent": "elbow-3",
        "child": "head-3",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-3-joint",
        "name": "petal-3 interface",
        "parent": "head-3",
        "child": "petal-3",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-3-joint",
        "name": "sensor-3 interface",
        "parent": "petal-3",
        "child": "sensor-3",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-3-joint",
        "name": "rack-3 interface",
        "parent": "frame",
        "child": "rack-3",
        "type": "fixed",
        "anchorParent": [
          7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-3-joint",
        "name": "exchange-pack-3 interface",
        "parent": "rack-3",
        "child": "exchange-pack-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-3-joint",
        "name": "gate-3 interface",
        "parent": "frame",
        "child": "gate-3",
        "type": "revolute",
        "anchorParent": [
          7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-4-joint",
        "name": "rail-4 interface",
        "parent": "frame",
        "child": "rail-4",
        "type": "fixed",
        "anchorParent": [
          14,
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
        ]
      },
      {
        "id": "carriage-4-joint",
        "name": "carriage-4 interface",
        "parent": "rail-4",
        "child": "carriage-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-4-joint",
        "name": "turret-4 interface",
        "parent": "carriage-4",
        "child": "turret-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-4-joint",
        "name": "elbow-4 interface",
        "parent": "turret-4",
        "child": "elbow-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-4-joint",
        "name": "head-4 interface",
        "parent": "elbow-4",
        "child": "head-4",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-4-joint",
        "name": "petal-4 interface",
        "parent": "head-4",
        "child": "petal-4",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-4-joint",
        "name": "sensor-4 interface",
        "parent": "petal-4",
        "child": "sensor-4",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-4-joint",
        "name": "rack-4 interface",
        "parent": "frame",
        "child": "rack-4",
        "type": "fixed",
        "anchorParent": [
          14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-4-joint",
        "name": "exchange-pack-4 interface",
        "parent": "rack-4",
        "child": "exchange-pack-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-4-joint",
        "name": "gate-4 interface",
        "parent": "frame",
        "child": "gate-4",
        "type": "revolute",
        "anchorParent": [
          14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
      }
    ],
    "target": "head-0"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 最小干预（h3-segmented-antenna-yard-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：0
- B：1
- C：2

```json
{
  "input": {
    "module": "head-0"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 全过程依赖（h3-segmented-antenna-yard-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：-1
- B：37
- C：50
- D：36

```json
{
  "input": {
    "order": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0",
      "petal-0",
      "sensor-0",
      "rack-0",
      "exchange-pack-0",
      "gate-0",
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rack-1",
      "exchange-pack-1",
      "gate-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2",
      "rack-2",
      "exchange-pack-2",
      "gate-2",
      "rail-3",
      "carriage-3",
      "turret-3",
      "elbow-3",
      "head-3",
      "sensor-3",
      "petal-3",
      "rack-3",
      "exchange-pack-3",
      "gate-3",
      "rail-4",
      "carriage-4",
      "turret-4",
      "elbow-4",
      "head-4",
      "petal-4",
      "sensor-4",
      "rack-4",
      "exchange-pack-4",
      "gate-4"
    ],
    "joints": [
      {
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
        "type": "fixed",
        "anchorParent": [
          -14,
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
        ]
      },
      {
        "id": "carriage-0-joint",
        "name": "carriage-0 interface",
        "parent": "rail-0",
        "child": "carriage-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-0-joint",
        "name": "turret-0 interface",
        "parent": "carriage-0",
        "child": "turret-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-0-joint",
        "name": "elbow-0 interface",
        "parent": "turret-0",
        "child": "elbow-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-0-joint",
        "name": "head-0 interface",
        "parent": "elbow-0",
        "child": "head-0",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-0-joint",
        "name": "petal-0 interface",
        "parent": "head-0",
        "child": "petal-0",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-0-joint",
        "name": "sensor-0 interface",
        "parent": "petal-0",
        "child": "sensor-0",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-0-joint",
        "name": "rack-0 interface",
        "parent": "frame",
        "child": "rack-0",
        "type": "fixed",
        "anchorParent": [
          -14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-0-joint",
        "name": "exchange-pack-0 interface",
        "parent": "rack-0",
        "child": "exchange-pack-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-0-joint",
        "name": "gate-0 interface",
        "parent": "frame",
        "child": "gate-0",
        "type": "revolute",
        "anchorParent": [
          -14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
        "type": "fixed",
        "anchorParent": [
          -7,
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
        ]
      },
      {
        "id": "carriage-1-joint",
        "name": "carriage-1 interface",
        "parent": "rail-1",
        "child": "carriage-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-1-joint",
        "name": "turret-1 interface",
        "parent": "carriage-1",
        "child": "turret-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-1-joint",
        "name": "elbow-1 interface",
        "parent": "turret-1",
        "child": "elbow-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-1-joint",
        "name": "head-1 interface",
        "parent": "elbow-1",
        "child": "head-1",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-1-joint",
        "name": "petal-1 interface",
        "parent": "head-1",
        "child": "petal-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-1-joint",
        "name": "sensor-1 interface",
        "parent": "petal-1",
        "child": "sensor-1",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-1-joint",
        "name": "rack-1 interface",
        "parent": "frame",
        "child": "rack-1",
        "type": "fixed",
        "anchorParent": [
          -7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-1-joint",
        "name": "exchange-pack-1 interface",
        "parent": "rack-1",
        "child": "exchange-pack-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-1-joint",
        "name": "gate-1 interface",
        "parent": "frame",
        "child": "gate-1",
        "type": "revolute",
        "anchorParent": [
          -7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          0,
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
        ]
      },
      {
        "id": "carriage-2-joint",
        "name": "carriage-2 interface",
        "parent": "rail-2",
        "child": "carriage-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-2-joint",
        "name": "turret-2 interface",
        "parent": "carriage-2",
        "child": "turret-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-2-joint",
        "name": "elbow-2 interface",
        "parent": "turret-2",
        "child": "elbow-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-2-joint",
        "name": "head-2 interface",
        "parent": "elbow-2",
        "child": "head-2",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-2-joint",
        "name": "petal-2 interface",
        "parent": "head-2",
        "child": "petal-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-2-joint",
        "name": "sensor-2 interface",
        "parent": "petal-2",
        "child": "sensor-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-2-joint",
        "name": "rack-2 interface",
        "parent": "frame",
        "child": "rack-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-2-joint",
        "name": "exchange-pack-2 interface",
        "parent": "rack-2",
        "child": "exchange-pack-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-2-joint",
        "name": "gate-2 interface",
        "parent": "frame",
        "child": "gate-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-3-joint",
        "name": "rail-3 interface",
        "parent": "frame",
        "child": "rail-3",
        "type": "fixed",
        "anchorParent": [
          7,
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
        ]
      },
      {
        "id": "carriage-3-joint",
        "name": "carriage-3 interface",
        "parent": "rail-3",
        "child": "carriage-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-3-joint",
        "name": "turret-3 interface",
        "parent": "carriage-3",
        "child": "turret-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-3-joint",
        "name": "elbow-3 interface",
        "parent": "turret-3",
        "child": "elbow-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-3-joint",
        "name": "head-3 interface",
        "parent": "elbow-3",
        "child": "head-3",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-3-joint",
        "name": "petal-3 interface",
        "parent": "head-3",
        "child": "petal-3",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-3-joint",
        "name": "sensor-3 interface",
        "parent": "petal-3",
        "child": "sensor-3",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-3-joint",
        "name": "rack-3 interface",
        "parent": "frame",
        "child": "rack-3",
        "type": "fixed",
        "anchorParent": [
          7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-3-joint",
        "name": "exchange-pack-3 interface",
        "parent": "rack-3",
        "child": "exchange-pack-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-3-joint",
        "name": "gate-3 interface",
        "parent": "frame",
        "child": "gate-3",
        "type": "revolute",
        "anchorParent": [
          7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-4-joint",
        "name": "rail-4 interface",
        "parent": "frame",
        "child": "rail-4",
        "type": "fixed",
        "anchorParent": [
          14,
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
        ]
      },
      {
        "id": "carriage-4-joint",
        "name": "carriage-4 interface",
        "parent": "rail-4",
        "child": "carriage-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-4-joint",
        "name": "turret-4 interface",
        "parent": "carriage-4",
        "child": "turret-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-4-joint",
        "name": "elbow-4 interface",
        "parent": "turret-4",
        "child": "elbow-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-4-joint",
        "name": "head-4 interface",
        "parent": "elbow-4",
        "child": "head-4",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-4-joint",
        "name": "petal-4 interface",
        "parent": "head-4",
        "child": "petal-4",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-4-joint",
        "name": "sensor-4 interface",
        "parent": "petal-4",
        "child": "sensor-4",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-4-joint",
        "name": "rack-4 interface",
        "parent": "frame",
        "child": "rack-4",
        "type": "fixed",
        "anchorParent": [
          14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-4-joint",
        "name": "exchange-pack-4 interface",
        "parent": "rack-4",
        "child": "exchange-pack-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-4-joint",
        "name": "gate-4 interface",
        "parent": "frame",
        "child": "gate-4",
        "type": "revolute",
        "anchorParent": [
          14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 连续维修路径（h3-segmented-antenna-yard-access）

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
          19.990000000000002,
          6.5875,
          0
        ],
        "end": [
          -14,
          6.5875,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.1473962813615799
      },
      {
        "id": "path-1",
        "start": [
          -14,
          12.65,
          0
        ],
        "end": [
          -14,
          6.5875,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.6301029920578003
      },
      {
        "id": "path-2",
        "start": [
          -14,
          6.5875,
          10.125
        ],
        "end": [
          -14,
          6.5875,
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
      "C"
    ]
  }
}
```

### 支撑反事实（h3-segmented-antenna-yard-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["rail-0"]
- B：[]
- C：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0","petal-0","sensor-0","rack-0","exchange-pack-0","gate-0","rail-1","carriage-1","turret-1","elbow-1","head-1","petal-1","sensor-1","rack-1","exchange-pack-1","gate-1","rail-2","carriage-2","turret-2","elbow-2","head-2","petal-2","sensor-2","rack-2","exchange-pack-2","gate-2","rail-3","carriage-3","turret-3","elbow-3","head-3","petal-3","sensor-3","rack-3","exchange-pack-3","gate-3","rail-4","carriage-4","turret-4","elbow-4","head-4","petal-4","sensor-4","rack-4","exchange-pack-4","gate-4"]
- D：["carriage-0","elbow-0","head-0","petal-0","sensor-0","turret-0"]

```json
{
  "input": {
    "removed": "rail-0",
    "roots": [
      "frame"
    ],
    "joints": [
      {
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
        "type": "fixed",
        "anchorParent": [
          -14,
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
        ]
      },
      {
        "id": "carriage-0-joint",
        "name": "carriage-0 interface",
        "parent": "rail-0",
        "child": "carriage-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-0-joint",
        "name": "turret-0 interface",
        "parent": "carriage-0",
        "child": "turret-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-0-joint",
        "name": "elbow-0 interface",
        "parent": "turret-0",
        "child": "elbow-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-0-joint",
        "name": "head-0 interface",
        "parent": "elbow-0",
        "child": "head-0",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-0-joint",
        "name": "petal-0 interface",
        "parent": "head-0",
        "child": "petal-0",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-0-joint",
        "name": "sensor-0 interface",
        "parent": "petal-0",
        "child": "sensor-0",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-0-joint",
        "name": "rack-0 interface",
        "parent": "frame",
        "child": "rack-0",
        "type": "fixed",
        "anchorParent": [
          -14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-0-joint",
        "name": "exchange-pack-0 interface",
        "parent": "rack-0",
        "child": "exchange-pack-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-0-joint",
        "name": "gate-0 interface",
        "parent": "frame",
        "child": "gate-0",
        "type": "revolute",
        "anchorParent": [
          -14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
        "type": "fixed",
        "anchorParent": [
          -7,
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
        ]
      },
      {
        "id": "carriage-1-joint",
        "name": "carriage-1 interface",
        "parent": "rail-1",
        "child": "carriage-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-1-joint",
        "name": "turret-1 interface",
        "parent": "carriage-1",
        "child": "turret-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-1-joint",
        "name": "elbow-1 interface",
        "parent": "turret-1",
        "child": "elbow-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-1-joint",
        "name": "head-1 interface",
        "parent": "elbow-1",
        "child": "head-1",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-1-joint",
        "name": "petal-1 interface",
        "parent": "head-1",
        "child": "petal-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-1-joint",
        "name": "sensor-1 interface",
        "parent": "petal-1",
        "child": "sensor-1",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-1-joint",
        "name": "rack-1 interface",
        "parent": "frame",
        "child": "rack-1",
        "type": "fixed",
        "anchorParent": [
          -7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-1-joint",
        "name": "exchange-pack-1 interface",
        "parent": "rack-1",
        "child": "exchange-pack-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-1-joint",
        "name": "gate-1 interface",
        "parent": "frame",
        "child": "gate-1",
        "type": "revolute",
        "anchorParent": [
          -7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          0,
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
        ]
      },
      {
        "id": "carriage-2-joint",
        "name": "carriage-2 interface",
        "parent": "rail-2",
        "child": "carriage-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-2-joint",
        "name": "turret-2 interface",
        "parent": "carriage-2",
        "child": "turret-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-2-joint",
        "name": "elbow-2 interface",
        "parent": "turret-2",
        "child": "elbow-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-2-joint",
        "name": "head-2 interface",
        "parent": "elbow-2",
        "child": "head-2",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-2-joint",
        "name": "petal-2 interface",
        "parent": "head-2",
        "child": "petal-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-2-joint",
        "name": "sensor-2 interface",
        "parent": "petal-2",
        "child": "sensor-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-2-joint",
        "name": "rack-2 interface",
        "parent": "frame",
        "child": "rack-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-2-joint",
        "name": "exchange-pack-2 interface",
        "parent": "rack-2",
        "child": "exchange-pack-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-2-joint",
        "name": "gate-2 interface",
        "parent": "frame",
        "child": "gate-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-3-joint",
        "name": "rail-3 interface",
        "parent": "frame",
        "child": "rail-3",
        "type": "fixed",
        "anchorParent": [
          7,
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
        ]
      },
      {
        "id": "carriage-3-joint",
        "name": "carriage-3 interface",
        "parent": "rail-3",
        "child": "carriage-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-3-joint",
        "name": "turret-3 interface",
        "parent": "carriage-3",
        "child": "turret-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-3-joint",
        "name": "elbow-3 interface",
        "parent": "turret-3",
        "child": "elbow-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-3-joint",
        "name": "head-3 interface",
        "parent": "elbow-3",
        "child": "head-3",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-3-joint",
        "name": "petal-3 interface",
        "parent": "head-3",
        "child": "petal-3",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-3-joint",
        "name": "sensor-3 interface",
        "parent": "petal-3",
        "child": "sensor-3",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-3-joint",
        "name": "rack-3 interface",
        "parent": "frame",
        "child": "rack-3",
        "type": "fixed",
        "anchorParent": [
          7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-3-joint",
        "name": "exchange-pack-3 interface",
        "parent": "rack-3",
        "child": "exchange-pack-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-3-joint",
        "name": "gate-3 interface",
        "parent": "frame",
        "child": "gate-3",
        "type": "revolute",
        "anchorParent": [
          7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-4-joint",
        "name": "rail-4 interface",
        "parent": "frame",
        "child": "rail-4",
        "type": "fixed",
        "anchorParent": [
          14,
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
        ]
      },
      {
        "id": "carriage-4-joint",
        "name": "carriage-4 interface",
        "parent": "rail-4",
        "child": "carriage-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-4-joint",
        "name": "turret-4 interface",
        "parent": "carriage-4",
        "child": "turret-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-4-joint",
        "name": "elbow-4 interface",
        "parent": "turret-4",
        "child": "elbow-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-4-joint",
        "name": "head-4 interface",
        "parent": "elbow-4",
        "child": "head-4",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-4-joint",
        "name": "petal-4 interface",
        "parent": "head-4",
        "child": "petal-4",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-4-joint",
        "name": "sensor-4 interface",
        "parent": "petal-4",
        "child": "sensor-4",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-4-joint",
        "name": "rack-4 interface",
        "parent": "frame",
        "child": "rack-4",
        "type": "fixed",
        "anchorParent": [
          14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-4-joint",
        "name": "exchange-pack-4 interface",
        "parent": "rack-4",
        "child": "exchange-pack-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-4-joint",
        "name": "gate-4 interface",
        "parent": "frame",
        "child": "gate-4",
        "type": "revolute",
        "anchorParent": [
          14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
      }
    ],
    "modules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0",
      "petal-0",
      "sensor-0",
      "rack-0",
      "exchange-pack-0",
      "gate-0",
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rack-1",
      "exchange-pack-1",
      "gate-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2",
      "rack-2",
      "exchange-pack-2",
      "gate-2",
      "rail-3",
      "carriage-3",
      "turret-3",
      "elbow-3",
      "head-3",
      "petal-3",
      "sensor-3",
      "rack-3",
      "exchange-pack-3",
      "gate-3",
      "rail-4",
      "carriage-4",
      "turret-4",
      "elbow-4",
      "head-4",
      "petal-4",
      "sensor-4",
      "rack-4",
      "exchange-pack-4",
      "gate-4"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 冲击响应读数（h3-segmented-antenna-yard-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：1.0162
- B：0.0162
- C：0.2162
- D：0

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.008405341941991691
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.016167092228816963
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.003453992548491531
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.007075711114377948
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.002430426168391159
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0029887018628584183
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0014761990676887189
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0012095218745599556
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0008253851800617707
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0004626818653122467
      },
      {
        "time": 1,
        "displacement": 0.000406791140565561
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.0000034332275398279244,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节限位推理（h3-segmented-antenna-yard-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-1.3
- B：1.3
- C：-0.8
- D：0

```json
{
  "input": {
    "joint": "carriage-0-joint",
    "limits": [
      -0.8,
      0.8
    ],
    "units": "scene units"
  },
  "answer": {
    "choiceIds": [
      "C",
      "D"
    ]
  }
}
```

### 约束故障诊断（h3-segmented-antenna-yard-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：rail-0-joint
- B：carriage-0-joint
- C：turret-0-joint
- D：head-0-joint

```json
{
  "input": {
    "endpoints": [
      "elbow-0",
      "head-0"
    ],
    "type": "revolute",
    "joints": [
      {
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
        "type": "fixed",
        "anchorParent": [
          -14,
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
        ]
      },
      {
        "id": "carriage-0-joint",
        "name": "carriage-0 interface",
        "parent": "rail-0",
        "child": "carriage-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-0-joint",
        "name": "turret-0 interface",
        "parent": "carriage-0",
        "child": "turret-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-0-joint",
        "name": "elbow-0 interface",
        "parent": "turret-0",
        "child": "elbow-0",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-0-joint",
        "name": "head-0 interface",
        "parent": "elbow-0",
        "child": "head-0",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-0-joint",
        "name": "petal-0 interface",
        "parent": "head-0",
        "child": "petal-0",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-0-joint",
        "name": "sensor-0 interface",
        "parent": "petal-0",
        "child": "sensor-0",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-0-joint",
        "name": "rack-0 interface",
        "parent": "frame",
        "child": "rack-0",
        "type": "fixed",
        "anchorParent": [
          -14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-0-joint",
        "name": "exchange-pack-0 interface",
        "parent": "rack-0",
        "child": "exchange-pack-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-0-joint",
        "name": "gate-0 interface",
        "parent": "frame",
        "child": "gate-0",
        "type": "revolute",
        "anchorParent": [
          -14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
        "type": "fixed",
        "anchorParent": [
          -7,
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
        ]
      },
      {
        "id": "carriage-1-joint",
        "name": "carriage-1 interface",
        "parent": "rail-1",
        "child": "carriage-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-1-joint",
        "name": "turret-1 interface",
        "parent": "carriage-1",
        "child": "turret-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-1-joint",
        "name": "elbow-1 interface",
        "parent": "turret-1",
        "child": "elbow-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-1-joint",
        "name": "head-1 interface",
        "parent": "elbow-1",
        "child": "head-1",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-1-joint",
        "name": "petal-1 interface",
        "parent": "head-1",
        "child": "petal-1",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-1-joint",
        "name": "sensor-1 interface",
        "parent": "petal-1",
        "child": "sensor-1",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-1-joint",
        "name": "rack-1 interface",
        "parent": "frame",
        "child": "rack-1",
        "type": "fixed",
        "anchorParent": [
          -7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-1-joint",
        "name": "exchange-pack-1 interface",
        "parent": "rack-1",
        "child": "exchange-pack-1",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-1-joint",
        "name": "gate-1 interface",
        "parent": "frame",
        "child": "gate-1",
        "type": "revolute",
        "anchorParent": [
          -7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          0,
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
        ]
      },
      {
        "id": "carriage-2-joint",
        "name": "carriage-2 interface",
        "parent": "rail-2",
        "child": "carriage-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-2-joint",
        "name": "turret-2 interface",
        "parent": "carriage-2",
        "child": "turret-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-2-joint",
        "name": "elbow-2 interface",
        "parent": "turret-2",
        "child": "elbow-2",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-2-joint",
        "name": "head-2 interface",
        "parent": "elbow-2",
        "child": "head-2",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-2-joint",
        "name": "petal-2 interface",
        "parent": "head-2",
        "child": "petal-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-2-joint",
        "name": "sensor-2 interface",
        "parent": "petal-2",
        "child": "sensor-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-2-joint",
        "name": "rack-2 interface",
        "parent": "frame",
        "child": "rack-2",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-2-joint",
        "name": "exchange-pack-2 interface",
        "parent": "rack-2",
        "child": "exchange-pack-2",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-2-joint",
        "name": "gate-2 interface",
        "parent": "frame",
        "child": "gate-2",
        "type": "revolute",
        "anchorParent": [
          0,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-3-joint",
        "name": "rail-3 interface",
        "parent": "frame",
        "child": "rail-3",
        "type": "fixed",
        "anchorParent": [
          7,
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
        ]
      },
      {
        "id": "carriage-3-joint",
        "name": "carriage-3 interface",
        "parent": "rail-3",
        "child": "carriage-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-3-joint",
        "name": "turret-3 interface",
        "parent": "carriage-3",
        "child": "turret-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-3-joint",
        "name": "elbow-3 interface",
        "parent": "turret-3",
        "child": "elbow-3",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-3-joint",
        "name": "head-3 interface",
        "parent": "elbow-3",
        "child": "head-3",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-3-joint",
        "name": "petal-3 interface",
        "parent": "head-3",
        "child": "petal-3",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-3-joint",
        "name": "sensor-3 interface",
        "parent": "petal-3",
        "child": "sensor-3",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-3-joint",
        "name": "rack-3 interface",
        "parent": "frame",
        "child": "rack-3",
        "type": "fixed",
        "anchorParent": [
          7,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-3-joint",
        "name": "exchange-pack-3 interface",
        "parent": "rack-3",
        "child": "exchange-pack-3",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-3-joint",
        "name": "gate-3 interface",
        "parent": "frame",
        "child": "gate-3",
        "type": "revolute",
        "anchorParent": [
          7,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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
        "id": "rail-4-joint",
        "name": "rail-4 interface",
        "parent": "frame",
        "child": "rail-4",
        "type": "fixed",
        "anchorParent": [
          14,
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
        ]
      },
      {
        "id": "carriage-4-joint",
        "name": "carriage-4 interface",
        "parent": "rail-4",
        "child": "carriage-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.5,
          0
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
        "id": "turret-4-joint",
        "name": "turret-4 interface",
        "parent": "carriage-4",
        "child": "turret-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6500000000000001,
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
          -0.8,
          0.8
        ]
      },
      {
        "id": "elbow-4-joint",
        "name": "elbow-4 interface",
        "parent": "turret-4",
        "child": "elbow-4",
        "type": "revolute",
        "anchorParent": [
          0,
          0.44999999999999973,
          0
        ],
        "anchorChild": [
          0,
          -1.7,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "head-4-joint",
        "name": "head-4 interface",
        "parent": "elbow-4",
        "child": "head-4",
        "type": "revolute",
        "anchorParent": [
          0,
          2.1500000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.08750000000000002,
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
        "id": "petal-4-joint",
        "name": "petal-4 interface",
        "parent": "head-4",
        "child": "petal-4",
        "type": "revolute",
        "anchorParent": [
          0,
          1.2125000000000008,
          0
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
        "id": "sensor-4-joint",
        "name": "sensor-4 interface",
        "parent": "petal-4",
        "child": "sensor-4",
        "type": "fixed",
        "anchorParent": [
          0,
          0.49999999999999895,
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
        "id": "rack-4-joint",
        "name": "rack-4 interface",
        "parent": "frame",
        "child": "rack-4",
        "type": "fixed",
        "anchorParent": [
          14,
          0.6499999999999999,
          -7
        ],
        "anchorChild": [
          0,
          -1.4,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "exchange-pack-4-joint",
        "name": "exchange-pack-4 interface",
        "parent": "rack-4",
        "child": "exchange-pack-4",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
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
        "id": "gate-4-joint",
        "name": "gate-4 interface",
        "parent": "frame",
        "child": "gate-4",
        "type": "revolute",
        "anchorParent": [
          14,
          1.15,
          6
        ],
        "anchorChild": [
          0,
          -0.49999999999999994,
          0
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

### 主动检查收益（h3-segmented-antenna-yard-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-2
- B：query-0
- C：query-1

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
    "module": "head-0",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "A"
    ]
  }
}
```

### 不确定性与弃答（h3-segmented-antenna-yard-abstention）

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

### 观测后信念更新（h3-segmented-antenna-yard-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0
- B：0.3333333333333333
- C：0.5
- D：0.25

```json
{
  "input": {
    "module": "head-0",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "negative",
      "negative",
      "negative",
      "negative"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 多目标工程权衡（h3-segmented-antenna-yard-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

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
        "stiffness": 9,
        "mass": 0.8
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 3,
        "mass": 1
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 11,
        "mass": 1
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 4,
        "mass": 1.8
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

### 依赖装配（h3-segmented-antenna-yard-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:turret-1",
        "label": "安装 turret-1",
        "requires": [
          "present:carriage-1"
        ],
        "forbids": [
          "present:turret-1"
        ],
        "adds": [
          "present:turret-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "turret-1",
          "visible": true
        }
      },
      {
        "id": "place:turret-4",
        "label": "安装 turret-4",
        "requires": [
          "present:carriage-4"
        ],
        "forbids": [
          "present:turret-4"
        ],
        "adds": [
          "present:turret-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "turret-4",
          "visible": true
        }
      },
      {
        "id": "place:elbow-1",
        "label": "安装 elbow-1",
        "requires": [
          "present:turret-1"
        ],
        "forbids": [
          "present:elbow-1"
        ],
        "adds": [
          "present:elbow-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-1",
          "visible": true
        }
      },
      {
        "id": "place:exchange-pack-1",
        "label": "安装 exchange-pack-1",
        "requires": [
          "present:rack-1"
        ],
        "forbids": [
          "present:exchange-pack-1"
        ],
        "adds": [
          "present:exchange-pack-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-1",
          "visible": true
        }
      },
      {
        "id": "place:rail-2",
        "label": "安装 rail-2",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rail-2"
        ],
        "adds": [
          "present:rail-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rail-2",
          "visible": true
        }
      },
      {
        "id": "place:head-3",
        "label": "安装 head-3",
        "requires": [
          "present:elbow-3"
        ],
        "forbids": [
          "present:head-3"
        ],
        "adds": [
          "present:head-3"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-3",
          "visible": true
        }
      },
      {
        "id": "place:petal-3",
        "label": "安装 petal-3",
        "requires": [
          "present:head-3"
        ],
        "forbids": [
          "present:petal-3"
        ],
        "adds": [
          "present:petal-3"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-3",
          "visible": true
        }
      },
      {
        "id": "place:rail-0",
        "label": "安装 rail-0",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rail-0"
        ],
        "adds": [
          "present:rail-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rail-0",
          "visible": true
        }
      },
      {
        "id": "place:head-2",
        "label": "安装 head-2",
        "requires": [
          "present:elbow-2"
        ],
        "forbids": [
          "present:head-2"
        ],
        "adds": [
          "present:head-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-2",
          "visible": true
        }
      },
      {
        "id": "place:turret-0",
        "label": "安装 turret-0",
        "requires": [
          "present:carriage-0"
        ],
        "forbids": [
          "present:turret-0"
        ],
        "adds": [
          "present:turret-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "turret-0",
          "visible": true
        }
      },
      {
        "id": "place:gate-2",
        "label": "安装 gate-2",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:gate-2"
        ],
        "adds": [
          "present:gate-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-2",
          "visible": true
        }
      },
      {
        "id": "place:frame",
        "label": "安装 frame",
        "requires": [],
        "forbids": [
          "present:frame"
        ],
        "adds": [
          "present:frame"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "frame",
          "visible": true
        }
      },
      {
        "id": "place:petal-0",
        "label": "安装 petal-0",
        "requires": [
          "present:head-0"
        ],
        "forbids": [
          "present:petal-0"
        ],
        "adds": [
          "present:petal-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-0",
          "visible": true
        }
      },
      {
        "id": "place:gate-0",
        "label": "安装 gate-0",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:gate-0"
        ],
        "adds": [
          "present:gate-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-0",
          "visible": true
        }
      },
      {
        "id": "place:sensor-3",
        "label": "安装 sensor-3",
        "requires": [
          "present:petal-3"
        ],
        "forbids": [
          "present:sensor-3"
        ],
        "adds": [
          "present:sensor-3"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-3",
          "visible": true
        }
      },
      {
        "id": "place:petal-4",
        "label": "安装 petal-4",
        "requires": [
          "present:head-4"
        ],
        "forbids": [
          "present:petal-4"
        ],
        "adds": [
          "present:petal-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-4",
          "visible": true
        }
      },
      {
        "id": "place:carriage-4",
        "label": "安装 carriage-4",
        "requires": [
          "present:rail-4"
        ],
        "forbids": [
          "present:carriage-4"
        ],
        "adds": [
          "present:carriage-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "carriage-4",
          "visible": true
        }
      },
      {
        "id": "place:head-0",
        "label": "安装 head-0",
        "requires": [
          "present:elbow-0"
        ],
        "forbids": [
          "present:head-0"
        ],
        "adds": [
          "present:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0",
          "visible": true
        }
      },
      {
        "id": "place:sensor-0",
        "label": "安装 sensor-0",
        "requires": [
          "present:petal-0"
        ],
        "forbids": [
          "present:sensor-0"
        ],
        "adds": [
          "present:sensor-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-0",
          "visible": true
        }
      },
      {
        "id": "place:gate-3",
        "label": "安装 gate-3",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:gate-3"
        ],
        "adds": [
          "present:gate-3"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-3",
          "visible": true
        }
      },
      {
        "id": "place:carriage-2",
        "label": "安装 carriage-2",
        "requires": [
          "present:rail-2"
        ],
        "forbids": [
          "present:carriage-2"
        ],
        "adds": [
          "present:carriage-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "carriage-2",
          "visible": true
        }
      },
      {
        "id": "place:exchange-pack-4",
        "label": "安装 exchange-pack-4",
        "requires": [
          "present:rack-4"
        ],
        "forbids": [
          "present:exchange-pack-4"
        ],
        "adds": [
          "present:exchange-pack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4",
          "visible": true
        }
      },
      {
        "id": "place:carriage-1",
        "label": "安装 carriage-1",
        "requires": [
          "present:rail-1"
        ],
        "forbids": [
          "present:carriage-1"
        ],
        "adds": [
          "present:carriage-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "carriage-1",
          "visible": true
        }
      },
      {
        "id": "place:gate-4",
        "label": "安装 gate-4",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:gate-4"
        ],
        "adds": [
          "present:gate-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4",
          "visible": true
        }
      },
      {
        "id": "place:rack-3",
        "label": "安装 rack-3",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rack-3"
        ],
        "adds": [
          "present:rack-3"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-3",
          "visible": true
        }
      },
      {
        "id": "place:head-4",
        "label": "安装 head-4",
        "requires": [
          "present:elbow-4"
        ],
        "forbids": [
          "present:head-4"
        ],
        "adds": [
          "present:head-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-4",
          "visible": true
        }
      },
      {
        "id": "place:turret-2",
        "label": "安装 turret-2",
        "requires": [
          "present:carriage-2"
        ],
        "forbids": [
          "present:turret-2"
        ],
        "adds": [
          "present:turret-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "turret-2",
          "visible": true
        }
      },
      {
        "id": "place:carriage-0",
        "label": "安装 carriage-0",
        "requires": [
          "present:rail-0"
        ],
        "forbids": [
          "present:carriage-0"
        ],
        "adds": [
          "present:carriage-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "carriage-0",
          "visible": true
        }
      },
      {
        "id": "place:carriage-3",
        "label": "安装 carriage-3",
        "requires": [
          "present:rail-3"
        ],
        "forbids": [
          "present:carriage-3"
        ],
        "adds": [
          "present:carriage-3"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "carriage-3",
          "visible": true
        }
      },
      {
        "id": "place:petal-2",
        "label": "安装 petal-2",
        "requires": [
          "present:head-2"
        ],
        "forbids": [
          "present:petal-2"
        ],
        "adds": [
          "present:petal-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2",
          "visible": true
        }
      },
      {
        "id": "place:rail-1",
        "label": "安装 rail-1",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rail-1"
        ],
        "adds": [
          "present:rail-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rail-1",
          "visible": true
        }
      },
      {
        "id": "place:sensor-4",
        "label": "安装 sensor-4",
        "requires": [
          "present:petal-4"
        ],
        "forbids": [
          "present:sensor-4"
        ],
        "adds": [
          "present:sensor-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4",
          "visible": true
        }
      },
      {
        "id": "place:elbow-3",
        "label": "安装 elbow-3",
        "requires": [
          "present:turret-3"
        ],
        "forbids": [
          "present:elbow-3"
        ],
        "adds": [
          "present:elbow-3"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-3",
          "visible": true
        }
      },
      {
        "id": "place:rail-4",
        "label": "安装 rail-4",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rail-4"
        ],
        "adds": [
          "present:rail-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rail-4",
          "visible": true
        }
      },
      {
        "id": "place:petal-1",
        "label": "安装 petal-1",
        "requires": [
          "present:head-1"
        ],
        "forbids": [
          "present:petal-1"
        ],
        "adds": [
          "present:petal-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-1",
          "visible": true
        }
      },
      {
        "id": "place:elbow-0",
        "label": "安装 elbow-0",
        "requires": [
          "present:turret-0"
        ],
        "forbids": [
          "present:elbow-0"
        ],
        "adds": [
          "present:elbow-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-0",
          "visible": true
        }
      },
      {
        "id": "place:sensor-2",
        "label": "安装 sensor-2",
        "requires": [
          "present:petal-2"
        ],
        "forbids": [
          "present:sensor-2"
        ],
        "adds": [
          "present:sensor-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2",
          "visible": true
        }
      },
      {
        "id": "place:turret-3",
        "label": "安装 turret-3",
        "requires": [
          "present:carriage-3"
        ],
        "forbids": [
          "present:turret-3"
        ],
        "adds": [
          "present:turret-3"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "turret-3",
          "visible": true
        }
      },
      {
        "id": "place:elbow-2",
        "label": "安装 elbow-2",
        "requires": [
          "present:turret-2"
        ],
        "forbids": [
          "present:elbow-2"
        ],
        "adds": [
          "present:elbow-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-2",
          "visible": true
        }
      },
      {
        "id": "place:exchange-pack-0",
        "label": "安装 exchange-pack-0",
        "requires": [
          "present:rack-0"
        ],
        "forbids": [
          "present:exchange-pack-0"
        ],
        "adds": [
          "present:exchange-pack-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-0",
          "visible": true
        }
      },
      {
        "id": "place:exchange-pack-2",
        "label": "安装 exchange-pack-2",
        "requires": [
          "present:rack-2"
        ],
        "forbids": [
          "present:exchange-pack-2"
        ],
        "adds": [
          "present:exchange-pack-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-2",
          "visible": true
        }
      },
      {
        "id": "place:sensor-1",
        "label": "安装 sensor-1",
        "requires": [
          "present:petal-1"
        ],
        "forbids": [
          "present:sensor-1"
        ],
        "adds": [
          "present:sensor-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-1",
          "visible": true
        }
      },
      {
        "id": "place:rack-1",
        "label": "安装 rack-1",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rack-1"
        ],
        "adds": [
          "present:rack-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-1",
          "visible": true
        }
      },
      {
        "id": "place:rack-0",
        "label": "安装 rack-0",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rack-0"
        ],
        "adds": [
          "present:rack-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-0",
          "visible": true
        }
      },
      {
        "id": "place:elbow-4",
        "label": "安装 elbow-4",
        "requires": [
          "present:turret-4"
        ],
        "forbids": [
          "present:elbow-4"
        ],
        "adds": [
          "present:elbow-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-4",
          "visible": true
        }
      },
      {
        "id": "place:rack-4",
        "label": "安装 rack-4",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rack-4"
        ],
        "adds": [
          "present:rack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4",
          "visible": true
        }
      },
      {
        "id": "place:gate-1",
        "label": "安装 gate-1",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:gate-1"
        ],
        "adds": [
          "present:gate-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-1",
          "visible": true
        }
      },
      {
        "id": "place:rack-2",
        "label": "安装 rack-2",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rack-2"
        ],
        "adds": [
          "present:rack-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-2",
          "visible": true
        }
      },
      {
        "id": "place:head-1",
        "label": "安装 head-1",
        "requires": [
          "present:elbow-1"
        ],
        "forbids": [
          "present:head-1"
        ],
        "adds": [
          "present:head-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-1",
          "visible": true
        }
      },
      {
        "id": "place:rail-3",
        "label": "安装 rail-3",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rail-3"
        ],
        "adds": [
          "present:rail-3"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rail-3",
          "visible": true
        }
      },
      {
        "id": "place:exchange-pack-3",
        "label": "安装 exchange-pack-3",
        "requires": [
          "present:rack-3"
        ],
        "forbids": [
          "present:exchange-pack-3"
        ],
        "adds": [
          "present:exchange-pack-3"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-3",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:frame",
      "present:rail-0",
      "present:carriage-0",
      "present:turret-0",
      "present:elbow-0",
      "present:head-0",
      "present:petal-0",
      "present:sensor-0",
      "present:rack-0",
      "present:exchange-pack-0",
      "present:gate-0",
      "present:rail-1",
      "present:carriage-1",
      "present:turret-1",
      "present:elbow-1",
      "present:head-1",
      "present:petal-1",
      "present:sensor-1",
      "present:rack-1",
      "present:exchange-pack-1",
      "present:gate-1",
      "present:rail-2",
      "present:carriage-2",
      "present:turret-2",
      "present:elbow-2",
      "present:head-2",
      "present:petal-2",
      "present:sensor-2",
      "present:rack-2",
      "present:exchange-pack-2",
      "present:gate-2",
      "present:rail-3",
      "present:carriage-3",
      "present:turret-3",
      "present:elbow-3",
      "present:head-3",
      "present:petal-3",
      "present:sensor-3",
      "present:rack-3",
      "present:exchange-pack-3",
      "present:gate-3",
      "present:rail-4",
      "present:carriage-4",
      "present:turret-4",
      "present:elbow-4",
      "present:head-4",
      "present:petal-4",
      "present:sensor-4",
      "present:rack-4",
      "present:exchange-pack-4",
      "present:gate-4"
    ],
    "budget": 51,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:frame",
      "place:rail-2",
      "place:rail-0",
      "place:gate-2",
      "place:gate-0",
      "place:gate-3",
      "place:carriage-2",
      "place:gate-4",
      "place:rack-3",
      "place:turret-2",
      "place:carriage-0",
      "place:turret-0",
      "place:rail-1",
      "place:carriage-1",
      "place:turret-1",
      "place:elbow-1",
      "place:rail-4",
      "place:carriage-4",
      "place:turret-4",
      "place:elbow-0",
      "place:head-0",
      "place:petal-0",
      "place:sensor-0",
      "place:elbow-2",
      "place:head-2",
      "place:petal-2",
      "place:sensor-2",
      "place:rack-1",
      "place:exchange-pack-1",
      "place:rack-0",
      "place:exchange-pack-0",
      "place:elbow-4",
      "place:head-4",
      "place:petal-4",
      "place:sensor-4",
      "place:rack-4",
      "place:exchange-pack-4",
      "place:gate-1",
      "place:rack-2",
      "place:exchange-pack-2",
      "place:head-1",
      "place:petal-1",
      "place:sensor-1",
      "place:rail-3",
      "place:carriage-3",
      "place:turret-3",
      "place:elbow-3",
      "place:head-3",
      "place:petal-3",
      "place:sensor-3",
      "place:exchange-pack-3"
    ]
  }
}
```

### 依赖拆解（h3-segmented-antenna-yard-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:frame",
      "present:rail-0",
      "present:carriage-0",
      "present:turret-0",
      "present:elbow-0",
      "present:head-0",
      "present:petal-0",
      "present:sensor-0",
      "present:rack-0",
      "present:exchange-pack-0",
      "present:gate-0",
      "present:rail-1",
      "present:carriage-1",
      "present:turret-1",
      "present:elbow-1",
      "present:head-1",
      "present:petal-1",
      "present:sensor-1",
      "present:rack-1",
      "present:exchange-pack-1",
      "present:gate-1",
      "present:rail-2",
      "present:carriage-2",
      "present:turret-2",
      "present:elbow-2",
      "present:head-2",
      "present:petal-2",
      "present:sensor-2",
      "present:rack-2",
      "present:exchange-pack-2",
      "present:gate-2",
      "present:rail-3",
      "present:carriage-3",
      "present:turret-3",
      "present:elbow-3",
      "present:head-3",
      "present:petal-3",
      "present:sensor-3",
      "present:rack-3",
      "present:exchange-pack-3",
      "present:gate-3",
      "present:rail-4",
      "present:carriage-4",
      "present:turret-4",
      "present:elbow-4",
      "present:head-4",
      "present:petal-4",
      "present:sensor-4",
      "present:rack-4",
      "present:exchange-pack-4",
      "present:gate-4"
    ],
    "initialModules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0",
      "petal-0",
      "sensor-0",
      "rack-0",
      "exchange-pack-0",
      "gate-0",
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rack-1",
      "exchange-pack-1",
      "gate-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2",
      "rack-2",
      "exchange-pack-2",
      "gate-2",
      "rail-3",
      "carriage-3",
      "turret-3",
      "elbow-3",
      "head-3",
      "petal-3",
      "sensor-3",
      "rack-3",
      "exchange-pack-3",
      "gate-3",
      "rail-4",
      "carriage-4",
      "turret-4",
      "elbow-4",
      "head-4",
      "petal-4",
      "sensor-4",
      "rack-4",
      "exchange-pack-4",
      "gate-4"
    ],
    "actions": [
      {
        "id": "remove:rail-1",
        "label": "拆除 rail-1",
        "requires": [
          "present:rail-1"
        ],
        "forbids": [
          "present:carriage-1"
        ],
        "adds": [
          "removed:rail-1"
        ],
        "deletes": [
          "present:rail-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rail-1",
          "visible": false
        }
      },
      {
        "id": "remove:elbow-0",
        "label": "拆除 elbow-0",
        "requires": [
          "present:elbow-0"
        ],
        "forbids": [
          "present:head-0"
        ],
        "adds": [
          "removed:elbow-0"
        ],
        "deletes": [
          "present:elbow-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-0",
          "visible": false
        }
      },
      {
        "id": "remove:sensor-4",
        "label": "拆除 sensor-4",
        "requires": [
          "present:sensor-4"
        ],
        "forbids": [],
        "adds": [
          "removed:sensor-4"
        ],
        "deletes": [
          "present:sensor-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4",
          "visible": false
        }
      },
      {
        "id": "remove:rack-2",
        "label": "拆除 rack-2",
        "requires": [
          "present:rack-2"
        ],
        "forbids": [
          "present:exchange-pack-2"
        ],
        "adds": [
          "removed:rack-2"
        ],
        "deletes": [
          "present:rack-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rack-2",
          "visible": false
        }
      },
      {
        "id": "remove:gate-3",
        "label": "拆除 gate-3",
        "requires": [
          "present:gate-3"
        ],
        "forbids": [],
        "adds": [
          "removed:gate-3"
        ],
        "deletes": [
          "present:gate-3"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gate-3",
          "visible": false
        }
      },
      {
        "id": "remove:elbow-4",
        "label": "拆除 elbow-4",
        "requires": [
          "present:elbow-4"
        ],
        "forbids": [
          "present:head-4"
        ],
        "adds": [
          "removed:elbow-4"
        ],
        "deletes": [
          "present:elbow-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-4",
          "visible": false
        }
      },
      {
        "id": "remove:gate-2",
        "label": "拆除 gate-2",
        "requires": [
          "present:gate-2"
        ],
        "forbids": [],
        "adds": [
          "removed:gate-2"
        ],
        "deletes": [
          "present:gate-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gate-2",
          "visible": false
        }
      },
      {
        "id": "remove:rack-0",
        "label": "拆除 rack-0",
        "requires": [
          "present:rack-0"
        ],
        "forbids": [
          "present:exchange-pack-0"
        ],
        "adds": [
          "removed:rack-0"
        ],
        "deletes": [
          "present:rack-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rack-0",
          "visible": false
        }
      },
      {
        "id": "remove:rail-0",
        "label": "拆除 rail-0",
        "requires": [
          "present:rail-0"
        ],
        "forbids": [
          "present:carriage-0"
        ],
        "adds": [
          "removed:rail-0"
        ],
        "deletes": [
          "present:rail-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rail-0",
          "visible": false
        }
      },
      {
        "id": "remove:rack-1",
        "label": "拆除 rack-1",
        "requires": [
          "present:rack-1"
        ],
        "forbids": [
          "present:exchange-pack-1"
        ],
        "adds": [
          "removed:rack-1"
        ],
        "deletes": [
          "present:rack-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rack-1",
          "visible": false
        }
      },
      {
        "id": "remove:turret-1",
        "label": "拆除 turret-1",
        "requires": [
          "present:turret-1"
        ],
        "forbids": [
          "present:elbow-1"
        ],
        "adds": [
          "removed:turret-1"
        ],
        "deletes": [
          "present:turret-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "turret-1",
          "visible": false
        }
      },
      {
        "id": "remove:exchange-pack-3",
        "label": "拆除 exchange-pack-3",
        "requires": [
          "present:exchange-pack-3"
        ],
        "forbids": [],
        "adds": [
          "removed:exchange-pack-3"
        ],
        "deletes": [
          "present:exchange-pack-3"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-3",
          "visible": false
        }
      },
      {
        "id": "remove:exchange-pack-4",
        "label": "拆除 exchange-pack-4",
        "requires": [
          "present:exchange-pack-4"
        ],
        "forbids": [],
        "adds": [
          "removed:exchange-pack-4"
        ],
        "deletes": [
          "present:exchange-pack-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4",
          "visible": false
        }
      },
      {
        "id": "remove:turret-4",
        "label": "拆除 turret-4",
        "requires": [
          "present:turret-4"
        ],
        "forbids": [
          "present:elbow-4"
        ],
        "adds": [
          "removed:turret-4"
        ],
        "deletes": [
          "present:turret-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "turret-4",
          "visible": false
        }
      },
      {
        "id": "remove:petal-3",
        "label": "拆除 petal-3",
        "requires": [
          "present:petal-3"
        ],
        "forbids": [
          "present:sensor-3"
        ],
        "adds": [
          "removed:petal-3"
        ],
        "deletes": [
          "present:petal-3"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "petal-3",
          "visible": false
        }
      },
      {
        "id": "remove:carriage-1",
        "label": "拆除 carriage-1",
        "requires": [
          "present:carriage-1"
        ],
        "forbids": [
          "present:turret-1"
        ],
        "adds": [
          "removed:carriage-1"
        ],
        "deletes": [
          "present:carriage-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "carriage-1",
          "visible": false
        }
      },
      {
        "id": "remove:frame",
        "label": "拆除 frame",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rail-0",
          "present:rack-0",
          "present:gate-0",
          "present:rail-1",
          "present:rack-1",
          "present:gate-1",
          "present:rail-2",
          "present:rack-2",
          "present:gate-2",
          "present:rail-3",
          "present:rack-3",
          "present:gate-3",
          "present:rail-4",
          "present:rack-4",
          "present:gate-4"
        ],
        "adds": [
          "removed:frame"
        ],
        "deletes": [
          "present:frame"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "frame",
          "visible": false
        }
      },
      {
        "id": "remove:carriage-0",
        "label": "拆除 carriage-0",
        "requires": [
          "present:carriage-0"
        ],
        "forbids": [
          "present:turret-0"
        ],
        "adds": [
          "removed:carriage-0"
        ],
        "deletes": [
          "present:carriage-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "carriage-0",
          "visible": false
        }
      },
      {
        "id": "remove:turret-0",
        "label": "拆除 turret-0",
        "requires": [
          "present:turret-0"
        ],
        "forbids": [
          "present:elbow-0"
        ],
        "adds": [
          "removed:turret-0"
        ],
        "deletes": [
          "present:turret-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "turret-0",
          "visible": false
        }
      },
      {
        "id": "remove:turret-3",
        "label": "拆除 turret-3",
        "requires": [
          "present:turret-3"
        ],
        "forbids": [
          "present:elbow-3"
        ],
        "adds": [
          "removed:turret-3"
        ],
        "deletes": [
          "present:turret-3"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "turret-3",
          "visible": false
        }
      },
      {
        "id": "remove:sensor-0",
        "label": "拆除 sensor-0",
        "requires": [
          "present:sensor-0"
        ],
        "forbids": [],
        "adds": [
          "removed:sensor-0"
        ],
        "deletes": [
          "present:sensor-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-0",
          "visible": false
        }
      },
      {
        "id": "remove:head-2",
        "label": "拆除 head-2",
        "requires": [
          "present:head-2"
        ],
        "forbids": [
          "present:petal-2"
        ],
        "adds": [
          "removed:head-2"
        ],
        "deletes": [
          "present:head-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-2",
          "visible": false
        }
      },
      {
        "id": "remove:petal-0",
        "label": "拆除 petal-0",
        "requires": [
          "present:petal-0"
        ],
        "forbids": [
          "present:sensor-0"
        ],
        "adds": [
          "removed:petal-0"
        ],
        "deletes": [
          "present:petal-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "petal-0",
          "visible": false
        }
      },
      {
        "id": "remove:head-3",
        "label": "拆除 head-3",
        "requires": [
          "present:head-3"
        ],
        "forbids": [
          "present:petal-3"
        ],
        "adds": [
          "removed:head-3"
        ],
        "deletes": [
          "present:head-3"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-3",
          "visible": false
        }
      },
      {
        "id": "remove:rack-4",
        "label": "拆除 rack-4",
        "requires": [
          "present:rack-4"
        ],
        "forbids": [
          "present:exchange-pack-4"
        ],
        "adds": [
          "removed:rack-4"
        ],
        "deletes": [
          "present:rack-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4",
          "visible": false
        }
      },
      {
        "id": "remove:sensor-1",
        "label": "拆除 sensor-1",
        "requires": [
          "present:sensor-1"
        ],
        "forbids": [],
        "adds": [
          "removed:sensor-1"
        ],
        "deletes": [
          "present:sensor-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-1",
          "visible": false
        }
      },
      {
        "id": "remove:petal-4",
        "label": "拆除 petal-4",
        "requires": [
          "present:petal-4"
        ],
        "forbids": [
          "present:sensor-4"
        ],
        "adds": [
          "removed:petal-4"
        ],
        "deletes": [
          "present:petal-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "petal-4",
          "visible": false
        }
      },
      {
        "id": "remove:rail-4",
        "label": "拆除 rail-4",
        "requires": [
          "present:rail-4"
        ],
        "forbids": [
          "present:carriage-4"
        ],
        "adds": [
          "removed:rail-4"
        ],
        "deletes": [
          "present:rail-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rail-4",
          "visible": false
        }
      },
      {
        "id": "remove:elbow-2",
        "label": "拆除 elbow-2",
        "requires": [
          "present:elbow-2"
        ],
        "forbids": [
          "present:head-2"
        ],
        "adds": [
          "removed:elbow-2"
        ],
        "deletes": [
          "present:elbow-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-2",
          "visible": false
        }
      },
      {
        "id": "remove:carriage-3",
        "label": "拆除 carriage-3",
        "requires": [
          "present:carriage-3"
        ],
        "forbids": [
          "present:turret-3"
        ],
        "adds": [
          "removed:carriage-3"
        ],
        "deletes": [
          "present:carriage-3"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "carriage-3",
          "visible": false
        }
      },
      {
        "id": "remove:petal-1",
        "label": "拆除 petal-1",
        "requires": [
          "present:petal-1"
        ],
        "forbids": [
          "present:sensor-1"
        ],
        "adds": [
          "removed:petal-1"
        ],
        "deletes": [
          "present:petal-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "petal-1",
          "visible": false
        }
      },
      {
        "id": "remove:rail-3",
        "label": "拆除 rail-3",
        "requires": [
          "present:rail-3"
        ],
        "forbids": [
          "present:carriage-3"
        ],
        "adds": [
          "removed:rail-3"
        ],
        "deletes": [
          "present:rail-3"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rail-3",
          "visible": false
        }
      },
      {
        "id": "remove:sensor-3",
        "label": "拆除 sensor-3",
        "requires": [
          "present:sensor-3"
        ],
        "forbids": [],
        "adds": [
          "removed:sensor-3"
        ],
        "deletes": [
          "present:sensor-3"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-3",
          "visible": false
        }
      },
      {
        "id": "remove:elbow-1",
        "label": "拆除 elbow-1",
        "requires": [
          "present:elbow-1"
        ],
        "forbids": [
          "present:head-1"
        ],
        "adds": [
          "removed:elbow-1"
        ],
        "deletes": [
          "present:elbow-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-1",
          "visible": false
        }
      },
      {
        "id": "remove:head-1",
        "label": "拆除 head-1",
        "requires": [
          "present:head-1"
        ],
        "forbids": [
          "present:petal-1"
        ],
        "adds": [
          "removed:head-1"
        ],
        "deletes": [
          "present:head-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-1",
          "visible": false
        }
      },
      {
        "id": "remove:head-0",
        "label": "拆除 head-0",
        "requires": [
          "present:head-0"
        ],
        "forbids": [
          "present:petal-0"
        ],
        "adds": [
          "removed:head-0"
        ],
        "deletes": [
          "present:head-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-0",
          "visible": false
        }
      },
      {
        "id": "remove:turret-2",
        "label": "拆除 turret-2",
        "requires": [
          "present:turret-2"
        ],
        "forbids": [
          "present:elbow-2"
        ],
        "adds": [
          "removed:turret-2"
        ],
        "deletes": [
          "present:turret-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "turret-2",
          "visible": false
        }
      },
      {
        "id": "remove:gate-4",
        "label": "拆除 gate-4",
        "requires": [
          "present:gate-4"
        ],
        "forbids": [],
        "adds": [
          "removed:gate-4"
        ],
        "deletes": [
          "present:gate-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4",
          "visible": false
        }
      },
      {
        "id": "remove:gate-0",
        "label": "拆除 gate-0",
        "requires": [
          "present:gate-0"
        ],
        "forbids": [],
        "adds": [
          "removed:gate-0"
        ],
        "deletes": [
          "present:gate-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gate-0",
          "visible": false
        }
      },
      {
        "id": "remove:elbow-3",
        "label": "拆除 elbow-3",
        "requires": [
          "present:elbow-3"
        ],
        "forbids": [
          "present:head-3"
        ],
        "adds": [
          "removed:elbow-3"
        ],
        "deletes": [
          "present:elbow-3"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-3",
          "visible": false
        }
      },
      {
        "id": "remove:carriage-2",
        "label": "拆除 carriage-2",
        "requires": [
          "present:carriage-2"
        ],
        "forbids": [
          "present:turret-2"
        ],
        "adds": [
          "removed:carriage-2"
        ],
        "deletes": [
          "present:carriage-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "carriage-2",
          "visible": false
        }
      },
      {
        "id": "remove:head-4",
        "label": "拆除 head-4",
        "requires": [
          "present:head-4"
        ],
        "forbids": [
          "present:petal-4"
        ],
        "adds": [
          "removed:head-4"
        ],
        "deletes": [
          "present:head-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-4",
          "visible": false
        }
      },
      {
        "id": "remove:exchange-pack-1",
        "label": "拆除 exchange-pack-1",
        "requires": [
          "present:exchange-pack-1"
        ],
        "forbids": [],
        "adds": [
          "removed:exchange-pack-1"
        ],
        "deletes": [
          "present:exchange-pack-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-1",
          "visible": false
        }
      },
      {
        "id": "remove:rail-2",
        "label": "拆除 rail-2",
        "requires": [
          "present:rail-2"
        ],
        "forbids": [
          "present:carriage-2"
        ],
        "adds": [
          "removed:rail-2"
        ],
        "deletes": [
          "present:rail-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rail-2",
          "visible": false
        }
      },
      {
        "id": "remove:exchange-pack-0",
        "label": "拆除 exchange-pack-0",
        "requires": [
          "present:exchange-pack-0"
        ],
        "forbids": [],
        "adds": [
          "removed:exchange-pack-0"
        ],
        "deletes": [
          "present:exchange-pack-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-0",
          "visible": false
        }
      },
      {
        "id": "remove:petal-2",
        "label": "拆除 petal-2",
        "requires": [
          "present:petal-2"
        ],
        "forbids": [
          "present:sensor-2"
        ],
        "adds": [
          "removed:petal-2"
        ],
        "deletes": [
          "present:petal-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2",
          "visible": false
        }
      },
      {
        "id": "remove:exchange-pack-2",
        "label": "拆除 exchange-pack-2",
        "requires": [
          "present:exchange-pack-2"
        ],
        "forbids": [],
        "adds": [
          "removed:exchange-pack-2"
        ],
        "deletes": [
          "present:exchange-pack-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-2",
          "visible": false
        }
      },
      {
        "id": "remove:sensor-2",
        "label": "拆除 sensor-2",
        "requires": [
          "present:sensor-2"
        ],
        "forbids": [],
        "adds": [
          "removed:sensor-2"
        ],
        "deletes": [
          "present:sensor-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2",
          "visible": false
        }
      },
      {
        "id": "remove:carriage-4",
        "label": "拆除 carriage-4",
        "requires": [
          "present:carriage-4"
        ],
        "forbids": [
          "present:turret-4"
        ],
        "adds": [
          "removed:carriage-4"
        ],
        "deletes": [
          "present:carriage-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "carriage-4",
          "visible": false
        }
      },
      {
        "id": "remove:rack-3",
        "label": "拆除 rack-3",
        "requires": [
          "present:rack-3"
        ],
        "forbids": [
          "present:exchange-pack-3"
        ],
        "adds": [
          "removed:rack-3"
        ],
        "deletes": [
          "present:rack-3"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rack-3",
          "visible": false
        }
      },
      {
        "id": "remove:gate-1",
        "label": "拆除 gate-1",
        "requires": [
          "present:gate-1"
        ],
        "forbids": [],
        "adds": [
          "removed:gate-1"
        ],
        "deletes": [
          "present:gate-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gate-1",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:gate-4",
      "removed:exchange-pack-4",
      "removed:rack-4",
      "removed:sensor-4",
      "removed:petal-4",
      "removed:head-4",
      "removed:elbow-4",
      "removed:turret-4",
      "removed:carriage-4",
      "removed:rail-4",
      "removed:gate-3",
      "removed:exchange-pack-3",
      "removed:rack-3",
      "removed:sensor-3",
      "removed:petal-3",
      "removed:head-3",
      "removed:elbow-3",
      "removed:turret-3",
      "removed:carriage-3",
      "removed:rail-3",
      "removed:gate-2",
      "removed:exchange-pack-2",
      "removed:rack-2",
      "removed:sensor-2",
      "removed:petal-2",
      "removed:head-2",
      "removed:elbow-2",
      "removed:turret-2",
      "removed:carriage-2",
      "removed:rail-2",
      "removed:gate-1",
      "removed:exchange-pack-1",
      "removed:rack-1",
      "removed:sensor-1",
      "removed:petal-1",
      "removed:head-1",
      "removed:elbow-1",
      "removed:turret-1",
      "removed:carriage-1",
      "removed:rail-1",
      "removed:gate-0",
      "removed:exchange-pack-0",
      "removed:rack-0",
      "removed:sensor-0",
      "removed:petal-0",
      "removed:head-0",
      "removed:elbow-0",
      "removed:turret-0",
      "removed:carriage-0",
      "removed:rail-0",
      "removed:frame"
    ],
    "budget": 51,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:sensor-4",
      "remove:gate-3",
      "remove:gate-2",
      "remove:exchange-pack-3",
      "remove:exchange-pack-4",
      "remove:sensor-0",
      "remove:petal-0",
      "remove:rack-4",
      "remove:sensor-1",
      "remove:petal-4",
      "remove:petal-1",
      "remove:sensor-3",
      "remove:petal-3",
      "remove:head-3",
      "remove:head-1",
      "remove:elbow-1",
      "remove:turret-1",
      "remove:carriage-1",
      "remove:rail-1",
      "remove:head-0",
      "remove:elbow-0",
      "remove:turret-0",
      "remove:carriage-0",
      "remove:rail-0",
      "remove:gate-4",
      "remove:gate-0",
      "remove:elbow-3",
      "remove:turret-3",
      "remove:carriage-3",
      "remove:rail-3",
      "remove:head-4",
      "remove:elbow-4",
      "remove:turret-4",
      "remove:exchange-pack-1",
      "remove:rack-1",
      "remove:exchange-pack-0",
      "remove:rack-0",
      "remove:exchange-pack-2",
      "remove:rack-2",
      "remove:sensor-2",
      "remove:petal-2",
      "remove:head-2",
      "remove:elbow-2",
      "remove:turret-2",
      "remove:carriage-2",
      "remove:rail-2",
      "remove:carriage-4",
      "remove:rail-4",
      "remove:rack-3",
      "remove:gate-1",
      "remove:frame"
    ]
  }
}
```

### 承载维修（h3-segmented-antenna-yard-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:head-0",
      "closed:head-0"
    ],
    "initialModules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0",
      "petal-0",
      "sensor-0",
      "rack-0",
      "exchange-pack-0",
      "gate-0",
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rack-1",
      "exchange-pack-1",
      "gate-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2",
      "rack-2",
      "exchange-pack-2",
      "gate-2",
      "rail-3",
      "carriage-3",
      "turret-3",
      "elbow-3",
      "head-3",
      "petal-3",
      "sensor-3",
      "rack-3",
      "exchange-pack-3",
      "gate-3",
      "rail-4",
      "carriage-4",
      "turret-4",
      "elbow-4",
      "head-4",
      "petal-4",
      "sensor-4",
      "rack-4",
      "exchange-pack-4",
      "gate-4"
    ],
    "actions": [
      {
        "id": "verify:head-0",
        "label": "verify head-0",
        "requires": [
          "done:replace:head-0"
        ],
        "forbids": [
          "done:verify:head-0"
        ],
        "adds": [
          "done:verify:head-0"
        ],
        "deletes": [
          "fault:head-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "support:head-0",
        "label": "support head-0",
        "requires": [
          "fault:head-0"
        ],
        "forbids": [
          "done:support:head-0"
        ],
        "adds": [
          "done:support:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "replace:head-0",
        "label": "replace head-0",
        "requires": [
          "done:remove:head-0"
        ],
        "forbids": [
          "done:replace:head-0"
        ],
        "adds": [
          "done:replace:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0",
          "visible": true
        }
      },
      {
        "id": "close:head-0",
        "label": "close head-0",
        "requires": [
          "done:verify:head-0"
        ],
        "forbids": [
          "done:close:head-0"
        ],
        "adds": [
          "done:close:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "open:head-0",
        "label": "open head-0",
        "requires": [
          "done:support:head-0"
        ],
        "forbids": [
          "done:open:head-0"
        ],
        "adds": [
          "done:open:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "remove:head-0",
        "label": "remove head-0",
        "requires": [
          "done:open:head-0"
        ],
        "forbids": [
          "done:remove:head-0"
        ],
        "adds": [
          "done:remove:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0",
          "visible": false
        }
      },
      {
        "id": "release:head-0",
        "label": "release head-0",
        "requires": [
          "done:close:head-0"
        ],
        "forbids": [
          "done:release:head-0"
        ],
        "adds": [
          "done:release:head-0",
          "repaired:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      }
    ],
    "goalFacts": [
      "repaired:head-0"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:head-0",
      "open:head-0",
      "remove:head-0",
      "replace:head-0",
      "verify:head-0",
      "close:head-0",
      "release:head-0"
    ]
  }
}
```

### 复合编辑验证（h3-segmented-antenna-yard-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:head-0",
      "closed:head-0"
    ],
    "initialModules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0",
      "petal-0",
      "sensor-0",
      "rack-0",
      "exchange-pack-0",
      "gate-0",
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rack-1",
      "exchange-pack-1",
      "gate-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2",
      "rack-2",
      "exchange-pack-2",
      "gate-2",
      "rail-3",
      "carriage-3",
      "turret-3",
      "elbow-3",
      "head-3",
      "petal-3",
      "sensor-3",
      "rack-3",
      "exchange-pack-3",
      "gate-3",
      "rail-4",
      "carriage-4",
      "turret-4",
      "elbow-4",
      "head-4",
      "petal-4",
      "sensor-4",
      "rack-4",
      "exchange-pack-4",
      "gate-4"
    ],
    "actions": [
      {
        "id": "verify:head-0",
        "label": "verify head-0",
        "requires": [
          "done:recolor:head-0"
        ],
        "forbids": [
          "done:verify:head-0"
        ],
        "adds": [
          "done:verify:head-0"
        ],
        "deletes": [
          "fault:head-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "support:head-0",
        "label": "support head-0",
        "requires": [
          "fault:head-0"
        ],
        "forbids": [
          "done:support:head-0"
        ],
        "adds": [
          "done:support:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "close:head-0",
        "label": "close head-0",
        "requires": [
          "done:verify:head-0"
        ],
        "forbids": [
          "done:close:head-0"
        ],
        "adds": [
          "done:close:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "open:head-0",
        "label": "open head-0",
        "requires": [
          "done:support:head-0"
        ],
        "forbids": [
          "done:open:head-0"
        ],
        "adds": [
          "done:open:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "recolor:head-0",
        "label": "recolor head-0",
        "requires": [
          "done:open:head-0"
        ],
        "forbids": [
          "done:recolor:head-0"
        ],
        "adds": [
          "done:recolor:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0",
          "color": "#ea7635"
        }
      },
      {
        "id": "release:head-0",
        "label": "release head-0",
        "requires": [
          "done:close:head-0"
        ],
        "forbids": [
          "done:release:head-0"
        ],
        "adds": [
          "done:release:head-0",
          "repaired:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      }
    ],
    "goalFacts": [
      "repaired:head-0"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:head-0",
      "open:head-0",
      "recolor:head-0",
      "verify:head-0",
      "close:head-0",
      "release:head-0"
    ]
  }
}
```

### 跨区域联合维修（h3-segmented-antenna-yard-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:sensor-4",
      "closed:sensor-4",
      "fault:rack-4",
      "closed:rack-4",
      "fault:exchange-pack-4",
      "closed:exchange-pack-4",
      "fault:gate-4",
      "closed:gate-4"
    ],
    "initialModules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0",
      "petal-0",
      "sensor-0",
      "rack-0",
      "exchange-pack-0",
      "gate-0",
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rack-1",
      "exchange-pack-1",
      "gate-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2",
      "rack-2",
      "exchange-pack-2",
      "gate-2",
      "rail-3",
      "carriage-3",
      "turret-3",
      "elbow-3",
      "head-3",
      "petal-3",
      "sensor-3",
      "rack-3",
      "exchange-pack-3",
      "gate-3",
      "rail-4",
      "carriage-4",
      "turret-4",
      "elbow-4",
      "head-4",
      "petal-4",
      "sensor-4",
      "rack-4",
      "exchange-pack-4",
      "gate-4"
    ],
    "actions": [
      {
        "id": "support:gate-4",
        "label": "support gate-4",
        "requires": [
          "fault:gate-4"
        ],
        "forbids": [
          "done:support:gate-4"
        ],
        "adds": [
          "done:support:gate-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4"
        }
      },
      {
        "id": "remove:sensor-4",
        "label": "remove sensor-4",
        "requires": [
          "done:open:sensor-4"
        ],
        "forbids": [
          "done:remove:sensor-4"
        ],
        "adds": [
          "done:remove:sensor-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4",
          "visible": false
        }
      },
      {
        "id": "support:exchange-pack-4",
        "label": "support exchange-pack-4",
        "requires": [
          "fault:exchange-pack-4"
        ],
        "forbids": [
          "done:support:exchange-pack-4"
        ],
        "adds": [
          "done:support:exchange-pack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4"
        }
      },
      {
        "id": "verify:exchange-pack-4",
        "label": "verify exchange-pack-4",
        "requires": [
          "done:replace:exchange-pack-4"
        ],
        "forbids": [
          "done:verify:exchange-pack-4"
        ],
        "adds": [
          "done:verify:exchange-pack-4"
        ],
        "deletes": [
          "fault:exchange-pack-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4"
        }
      },
      {
        "id": "open:gate-4",
        "label": "open gate-4",
        "requires": [
          "done:support:gate-4"
        ],
        "forbids": [
          "done:open:gate-4"
        ],
        "adds": [
          "done:open:gate-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4"
        }
      },
      {
        "id": "open:exchange-pack-4",
        "label": "open exchange-pack-4",
        "requires": [
          "done:support:exchange-pack-4"
        ],
        "forbids": [
          "done:open:exchange-pack-4"
        ],
        "adds": [
          "done:open:exchange-pack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4"
        }
      },
      {
        "id": "support:rack-4",
        "label": "support rack-4",
        "requires": [
          "fault:rack-4"
        ],
        "forbids": [
          "done:support:rack-4"
        ],
        "adds": [
          "done:support:rack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4"
        }
      },
      {
        "id": "release:rack-4",
        "label": "release rack-4",
        "requires": [
          "done:close:rack-4"
        ],
        "forbids": [
          "done:release:rack-4"
        ],
        "adds": [
          "done:release:rack-4",
          "repaired:rack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4"
        }
      },
      {
        "id": "verify:gate-4",
        "label": "verify gate-4",
        "requires": [
          "done:replace:gate-4"
        ],
        "forbids": [
          "done:verify:gate-4"
        ],
        "adds": [
          "done:verify:gate-4"
        ],
        "deletes": [
          "fault:gate-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4"
        }
      },
      {
        "id": "close:gate-4",
        "label": "close gate-4",
        "requires": [
          "done:verify:gate-4"
        ],
        "forbids": [
          "done:close:gate-4"
        ],
        "adds": [
          "done:close:gate-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4"
        }
      },
      {
        "id": "remove:exchange-pack-4",
        "label": "remove exchange-pack-4",
        "requires": [
          "done:open:exchange-pack-4"
        ],
        "forbids": [
          "done:remove:exchange-pack-4"
        ],
        "adds": [
          "done:remove:exchange-pack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4",
          "visible": false
        }
      },
      {
        "id": "release:gate-4",
        "label": "release gate-4",
        "requires": [
          "done:close:gate-4"
        ],
        "forbids": [
          "done:release:gate-4"
        ],
        "adds": [
          "done:release:gate-4",
          "repaired:gate-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4"
        }
      },
      {
        "id": "replace:rack-4",
        "label": "replace rack-4",
        "requires": [
          "done:remove:rack-4"
        ],
        "forbids": [
          "done:replace:rack-4"
        ],
        "adds": [
          "done:replace:rack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4",
          "visible": true
        }
      },
      {
        "id": "replace:exchange-pack-4",
        "label": "replace exchange-pack-4",
        "requires": [
          "done:remove:exchange-pack-4"
        ],
        "forbids": [
          "done:replace:exchange-pack-4"
        ],
        "adds": [
          "done:replace:exchange-pack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4",
          "visible": true
        }
      },
      {
        "id": "open:sensor-4",
        "label": "open sensor-4",
        "requires": [
          "done:support:sensor-4"
        ],
        "forbids": [
          "done:open:sensor-4"
        ],
        "adds": [
          "done:open:sensor-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4"
        }
      },
      {
        "id": "replace:gate-4",
        "label": "replace gate-4",
        "requires": [
          "done:remove:gate-4"
        ],
        "forbids": [
          "done:replace:gate-4"
        ],
        "adds": [
          "done:replace:gate-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4",
          "visible": true
        }
      },
      {
        "id": "close:exchange-pack-4",
        "label": "close exchange-pack-4",
        "requires": [
          "done:verify:exchange-pack-4"
        ],
        "forbids": [
          "done:close:exchange-pack-4"
        ],
        "adds": [
          "done:close:exchange-pack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4"
        }
      },
      {
        "id": "release:sensor-4",
        "label": "release sensor-4",
        "requires": [
          "done:close:sensor-4"
        ],
        "forbids": [
          "done:release:sensor-4"
        ],
        "adds": [
          "done:release:sensor-4",
          "repaired:sensor-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4"
        }
      },
      {
        "id": "remove:rack-4",
        "label": "remove rack-4",
        "requires": [
          "done:open:rack-4"
        ],
        "forbids": [
          "done:remove:rack-4"
        ],
        "adds": [
          "done:remove:rack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4",
          "visible": false
        }
      },
      {
        "id": "verify:sensor-4",
        "label": "verify sensor-4",
        "requires": [
          "done:replace:sensor-4"
        ],
        "forbids": [
          "done:verify:sensor-4"
        ],
        "adds": [
          "done:verify:sensor-4"
        ],
        "deletes": [
          "fault:sensor-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4"
        }
      },
      {
        "id": "close:sensor-4",
        "label": "close sensor-4",
        "requires": [
          "done:verify:sensor-4"
        ],
        "forbids": [
          "done:close:sensor-4"
        ],
        "adds": [
          "done:close:sensor-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4"
        }
      },
      {
        "id": "remove:gate-4",
        "label": "remove gate-4",
        "requires": [
          "done:open:gate-4"
        ],
        "forbids": [
          "done:remove:gate-4"
        ],
        "adds": [
          "done:remove:gate-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4",
          "visible": false
        }
      },
      {
        "id": "replace:sensor-4",
        "label": "replace sensor-4",
        "requires": [
          "done:remove:sensor-4"
        ],
        "forbids": [
          "done:replace:sensor-4"
        ],
        "adds": [
          "done:replace:sensor-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4",
          "visible": true
        }
      },
      {
        "id": "support:sensor-4",
        "label": "support sensor-4",
        "requires": [
          "fault:sensor-4"
        ],
        "forbids": [
          "done:support:sensor-4"
        ],
        "adds": [
          "done:support:sensor-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4"
        }
      },
      {
        "id": "open:rack-4",
        "label": "open rack-4",
        "requires": [
          "done:support:rack-4"
        ],
        "forbids": [
          "done:open:rack-4"
        ],
        "adds": [
          "done:open:rack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4"
        }
      },
      {
        "id": "close:rack-4",
        "label": "close rack-4",
        "requires": [
          "done:verify:rack-4"
        ],
        "forbids": [
          "done:close:rack-4"
        ],
        "adds": [
          "done:close:rack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4"
        }
      },
      {
        "id": "verify:rack-4",
        "label": "verify rack-4",
        "requires": [
          "done:replace:rack-4"
        ],
        "forbids": [
          "done:verify:rack-4"
        ],
        "adds": [
          "done:verify:rack-4"
        ],
        "deletes": [
          "fault:rack-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4"
        }
      },
      {
        "id": "release:exchange-pack-4",
        "label": "release exchange-pack-4",
        "requires": [
          "done:close:exchange-pack-4"
        ],
        "forbids": [
          "done:release:exchange-pack-4"
        ],
        "adds": [
          "done:release:exchange-pack-4",
          "repaired:exchange-pack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4"
        }
      }
    ],
    "goalFacts": [
      "repaired:sensor-4",
      "repaired:rack-4",
      "repaired:exchange-pack-4",
      "repaired:gate-4"
    ],
    "budget": 28,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:gate-4",
      "support:exchange-pack-4",
      "open:gate-4",
      "open:exchange-pack-4",
      "support:rack-4",
      "remove:exchange-pack-4",
      "replace:exchange-pack-4",
      "verify:exchange-pack-4",
      "close:exchange-pack-4",
      "remove:gate-4",
      "replace:gate-4",
      "verify:gate-4",
      "close:gate-4",
      "release:gate-4",
      "support:sensor-4",
      "open:sensor-4",
      "remove:sensor-4",
      "replace:sensor-4",
      "verify:sensor-4",
      "close:sensor-4",
      "release:sensor-4",
      "open:rack-4",
      "remove:rack-4",
      "replace:rack-4",
      "verify:rack-4",
      "close:rack-4",
      "release:rack-4",
      "release:exchange-pack-4"
    ]
  }
}
```

### 多工位资源调度（h3-segmented-antenna-yard-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "frame",
        "duration": 2,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "rail-0",
        "duration": 1,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "carriage-0",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "turret-0",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "elbow-0",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "head-0",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      },
      {
        "id": "job-6",
        "module": "petal-0",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-4"
        ]
      },
      {
        "id": "job-7",
        "module": "sensor-0",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-5"
        ]
      },
      {
        "id": "job-8",
        "module": "rack-0",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-6"
        ]
      },
      {
        "id": "job-9",
        "module": "exchange-pack-0",
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
      "job-2": 2,
      "job-3": 1,
      "job-4": 5,
      "job-5": 2,
      "job-6": 6,
      "job-7": 3,
      "job-8": 9,
      "job-9": 6
    }
  }
}
```

### 检查后条件策略（h3-segmented-antenna-yard-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "head-0",
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

### 局部坐标变换（h3-segmented-antenna-yard-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[1,-0.0875,0]
- B：[-12,7.5,1]
- C：[-13,6.5,0]

```json
{
  "input": {
    "localPoint": [
      1,
      -0.08750000000000002,
      0
    ],
    "rotationXYZW": [
      0,
      0,
      0,
      1
    ],
    "translation": [
      -14,
      6.5875,
      0
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-segmented-antenna-yard-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[11,5]
- B：[5,6]
- C：[0,0]
- D：[-6,11]

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
    "choiceId": "D"
  }
}
```

### 空间相对关系（h3-segmented-antenna-yard-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：greater
- B：less
- C：equal

```json
{
  "input": {
    "A": {
      "id": "frame",
      "position": [
        0,
        0.35,
        0
      ]
    },
    "B": {
      "id": "gate-4",
      "position": [
        14,
        2,
        6
      ]
    },
    "axis": "y"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 约束自由度（h3-segmented-antenna-yard-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：1
- B：3
- C：6
- D：0

```json
{
  "input": {
    "joint": {
      "id": "sensor-3-joint",
      "name": "sensor-3 interface",
      "parent": "petal-3",
      "child": "sensor-3",
      "type": "fixed",
      "anchorParent": [
        0,
        0.49999999999999895,
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
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 维修间隙预算（h3-segmented-antenna-yard-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "head-0",
    "aperture": 0.72,
    "toolWidth": 0.65,
    "eachSideMargin": 0.05
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-segmented-antenna-yard-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,-4,0]
- C：[0,0,-12]
- D：[0,0,12]

```json
{
  "input": {
    "module": "head-0",
    "lever": [
      4,
      2,
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

### 非均匀先验更新（h3-segmented-antenna-yard-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.7777777777777778
- B：0.5
- C：0
- D：1

```json
{
  "input": {
    "module": "head-0",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      2,
      7,
      5
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

### 风险最小决策（h3-segmented-antenna-yard-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.1,
    "repairCost": 4,
    "failureLoss": 16,
    "module": "head-0"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-segmented-antenna-yard-trace-threshold）

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
        "displacement": 0.008405341941991691
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.016167092228816963
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.003453992548491531
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.007075711114377948
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.002430426168391159
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0029887018628584183
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0014761990676887189
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0012095218745599556
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0008253851800617707
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0004626818653122467
      },
      {
        "time": 1,
        "displacement": 0.000406791140565561
      }
    ],
    "threshold": 0.012933673783053571
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-segmented-antenna-yard-guarded-repair）

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
        "id": "release:head-0",
        "label": "release head-0",
        "requires": [
          "done:relock:head-0"
        ],
        "forbids": [
          "done:release:head-0"
        ],
        "adds": [
          "done:release:head-0",
          "ready:head-0",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "relock:head-0",
        "label": "relock head-0",
        "requires": [
          "done:verify:head-0"
        ],
        "forbids": [
          "done:relock:head-0"
        ],
        "adds": [
          "done:relock:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "verify:head-0",
        "label": "verify head-0",
        "requires": [
          "done:replace:head-0"
        ],
        "forbids": [
          "done:verify:head-0"
        ],
        "adds": [
          "done:verify:head-0"
        ],
        "deletes": [
          "fault:head-0",
          "misaligned:head-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "replace:head-0",
        "label": "replace head-0",
        "requires": [
          "done:unlock:head-0"
        ],
        "forbids": [
          "done:replace:head-0"
        ],
        "adds": [
          "done:replace:head-0"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "unlock:head-0",
        "label": "unlock head-0",
        "requires": [
          "done:support:head-0"
        ],
        "forbids": [
          "done:unlock:head-0"
        ],
        "adds": [
          "done:unlock:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "support:head-0",
        "label": "support head-0",
        "requires": [
          "done:isolate:head-0"
        ],
        "forbids": [
          "done:support:head-0"
        ],
        "adds": [
          "done:support:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "isolate:head-0",
        "label": "isolate head-0",
        "requires": [
          "tool:free",
          "fault:head-0"
        ],
        "forbids": [
          "done:isolate:head-0"
        ],
        "adds": [
          "done:isolate:head-0"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:head-0"
    ],
    "initialModules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0",
      "petal-0",
      "sensor-0",
      "rack-0",
      "exchange-pack-0",
      "gate-0",
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rack-1",
      "exchange-pack-1",
      "gate-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2",
      "rack-2",
      "exchange-pack-2",
      "gate-2",
      "rail-3",
      "carriage-3",
      "turret-3",
      "elbow-3",
      "head-3",
      "petal-3",
      "sensor-3",
      "rack-3",
      "exchange-pack-3",
      "gate-3",
      "rail-4",
      "carriage-4",
      "turret-4",
      "elbow-4",
      "head-4",
      "petal-4",
      "sensor-4",
      "rack-4",
      "exchange-pack-4",
      "gate-4"
    ],
    "goalFacts": [
      "ready:head-0"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:head-0",
      "support:head-0",
      "unlock:head-0",
      "replace:head-0",
      "verify:head-0",
      "relock:head-0",
      "release:head-0"
    ]
  }
}
```

### 失败状态回退（h3-segmented-antenna-yard-rollback）

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
        "id": "resume:head-0",
        "label": "resume head-0",
        "requires": [
          "done:verify:head-0"
        ],
        "forbids": [
          "done:resume:head-0"
        ],
        "adds": [
          "done:resume:head-0",
          "ready:head-0",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "verify:head-0",
        "label": "verify head-0",
        "requires": [
          "done:align:head-0"
        ],
        "forbids": [
          "done:verify:head-0"
        ],
        "adds": [
          "done:verify:head-0"
        ],
        "deletes": [
          "fault:head-0",
          "misaligned:head-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      },
      {
        "id": "align:head-0",
        "label": "align head-0",
        "requires": [
          "done:undo:head-0"
        ],
        "forbids": [
          "done:align:head-0"
        ],
        "adds": [
          "done:align:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0",
          "visible": true
        }
      },
      {
        "id": "undo:head-0",
        "label": "undo head-0",
        "requires": [
          "done:isolate:head-0"
        ],
        "forbids": [
          "done:undo:head-0"
        ],
        "adds": [
          "done:undo:head-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-0",
          "visible": false
        }
      },
      {
        "id": "isolate:head-0",
        "label": "isolate head-0",
        "requires": [
          "tool:free",
          "fault:head-0"
        ],
        "forbids": [
          "done:isolate:head-0"
        ],
        "adds": [
          "done:isolate:head-0"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-0"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:head-0",
      "misaligned:head-0"
    ],
    "initialModules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0",
      "petal-0",
      "sensor-0",
      "rack-0",
      "exchange-pack-0",
      "gate-0",
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rack-1",
      "exchange-pack-1",
      "gate-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2",
      "rack-2",
      "exchange-pack-2",
      "gate-2",
      "rail-3",
      "carriage-3",
      "turret-3",
      "elbow-3",
      "head-3",
      "petal-3",
      "sensor-3",
      "rack-3",
      "exchange-pack-3",
      "gate-3",
      "rail-4",
      "carriage-4",
      "turret-4",
      "elbow-4",
      "head-4",
      "petal-4",
      "sensor-4",
      "rack-4",
      "exchange-pack-4",
      "gate-4"
    ],
    "goalFacts": [
      "ready:head-0"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:head-0",
      "undo:head-0",
      "align:head-0",
      "verify:head-0",
      "resume:head-0"
    ]
  }
}
```

### 共享工具协同维修（h3-segmented-antenna-yard-resource-repair）

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
        "id": "release:gate-4",
        "label": "release gate-4",
        "requires": [
          "done:relock:gate-4"
        ],
        "forbids": [
          "done:release:gate-4"
        ],
        "adds": [
          "done:release:gate-4",
          "ready:gate-4",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4"
        }
      },
      {
        "id": "relock:gate-4",
        "label": "relock gate-4",
        "requires": [
          "done:verify:gate-4"
        ],
        "forbids": [
          "done:relock:gate-4"
        ],
        "adds": [
          "done:relock:gate-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4"
        }
      },
      {
        "id": "verify:gate-4",
        "label": "verify gate-4",
        "requires": [
          "done:replace:gate-4"
        ],
        "forbids": [
          "done:verify:gate-4"
        ],
        "adds": [
          "done:verify:gate-4"
        ],
        "deletes": [
          "fault:gate-4",
          "misaligned:gate-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4"
        }
      },
      {
        "id": "replace:gate-4",
        "label": "replace gate-4",
        "requires": [
          "done:unlock:gate-4"
        ],
        "forbids": [
          "done:replace:gate-4"
        ],
        "adds": [
          "done:replace:gate-4"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "gate-4"
        }
      },
      {
        "id": "unlock:gate-4",
        "label": "unlock gate-4",
        "requires": [
          "done:support:gate-4"
        ],
        "forbids": [
          "done:unlock:gate-4"
        ],
        "adds": [
          "done:unlock:gate-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4"
        }
      },
      {
        "id": "support:gate-4",
        "label": "support gate-4",
        "requires": [
          "done:isolate:gate-4"
        ],
        "forbids": [
          "done:support:gate-4"
        ],
        "adds": [
          "done:support:gate-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4"
        }
      },
      {
        "id": "isolate:gate-4",
        "label": "isolate gate-4",
        "requires": [
          "tool:free",
          "fault:gate-4"
        ],
        "forbids": [
          "done:isolate:gate-4"
        ],
        "adds": [
          "done:isolate:gate-4"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gate-4"
        }
      },
      {
        "id": "release:exchange-pack-4",
        "label": "release exchange-pack-4",
        "requires": [
          "done:relock:exchange-pack-4"
        ],
        "forbids": [
          "done:release:exchange-pack-4"
        ],
        "adds": [
          "done:release:exchange-pack-4",
          "ready:exchange-pack-4",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4"
        }
      },
      {
        "id": "relock:exchange-pack-4",
        "label": "relock exchange-pack-4",
        "requires": [
          "done:verify:exchange-pack-4"
        ],
        "forbids": [
          "done:relock:exchange-pack-4"
        ],
        "adds": [
          "done:relock:exchange-pack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4"
        }
      },
      {
        "id": "verify:exchange-pack-4",
        "label": "verify exchange-pack-4",
        "requires": [
          "done:replace:exchange-pack-4"
        ],
        "forbids": [
          "done:verify:exchange-pack-4"
        ],
        "adds": [
          "done:verify:exchange-pack-4"
        ],
        "deletes": [
          "fault:exchange-pack-4",
          "misaligned:exchange-pack-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4"
        }
      },
      {
        "id": "replace:exchange-pack-4",
        "label": "replace exchange-pack-4",
        "requires": [
          "done:unlock:exchange-pack-4"
        ],
        "forbids": [
          "done:replace:exchange-pack-4"
        ],
        "adds": [
          "done:replace:exchange-pack-4"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "exchange-pack-4"
        }
      },
      {
        "id": "unlock:exchange-pack-4",
        "label": "unlock exchange-pack-4",
        "requires": [
          "done:support:exchange-pack-4"
        ],
        "forbids": [
          "done:unlock:exchange-pack-4"
        ],
        "adds": [
          "done:unlock:exchange-pack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4"
        }
      },
      {
        "id": "support:exchange-pack-4",
        "label": "support exchange-pack-4",
        "requires": [
          "done:isolate:exchange-pack-4"
        ],
        "forbids": [
          "done:support:exchange-pack-4"
        ],
        "adds": [
          "done:support:exchange-pack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4"
        }
      },
      {
        "id": "isolate:exchange-pack-4",
        "label": "isolate exchange-pack-4",
        "requires": [
          "tool:free",
          "fault:exchange-pack-4"
        ],
        "forbids": [
          "done:isolate:exchange-pack-4"
        ],
        "adds": [
          "done:isolate:exchange-pack-4"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "exchange-pack-4"
        }
      },
      {
        "id": "release:rack-4",
        "label": "release rack-4",
        "requires": [
          "done:relock:rack-4"
        ],
        "forbids": [
          "done:release:rack-4"
        ],
        "adds": [
          "done:release:rack-4",
          "ready:rack-4",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4"
        }
      },
      {
        "id": "relock:rack-4",
        "label": "relock rack-4",
        "requires": [
          "done:verify:rack-4"
        ],
        "forbids": [
          "done:relock:rack-4"
        ],
        "adds": [
          "done:relock:rack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4"
        }
      },
      {
        "id": "verify:rack-4",
        "label": "verify rack-4",
        "requires": [
          "done:replace:rack-4"
        ],
        "forbids": [
          "done:verify:rack-4"
        ],
        "adds": [
          "done:verify:rack-4"
        ],
        "deletes": [
          "fault:rack-4",
          "misaligned:rack-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4"
        }
      },
      {
        "id": "replace:rack-4",
        "label": "replace rack-4",
        "requires": [
          "done:unlock:rack-4"
        ],
        "forbids": [
          "done:replace:rack-4"
        ],
        "adds": [
          "done:replace:rack-4"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "rack-4"
        }
      },
      {
        "id": "unlock:rack-4",
        "label": "unlock rack-4",
        "requires": [
          "done:support:rack-4"
        ],
        "forbids": [
          "done:unlock:rack-4"
        ],
        "adds": [
          "done:unlock:rack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4"
        }
      },
      {
        "id": "support:rack-4",
        "label": "support rack-4",
        "requires": [
          "done:isolate:rack-4"
        ],
        "forbids": [
          "done:support:rack-4"
        ],
        "adds": [
          "done:support:rack-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4"
        }
      },
      {
        "id": "isolate:rack-4",
        "label": "isolate rack-4",
        "requires": [
          "tool:free",
          "fault:rack-4"
        ],
        "forbids": [
          "done:isolate:rack-4"
        ],
        "adds": [
          "done:isolate:rack-4"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rack-4"
        }
      },
      {
        "id": "release:sensor-4",
        "label": "release sensor-4",
        "requires": [
          "done:relock:sensor-4"
        ],
        "forbids": [
          "done:release:sensor-4"
        ],
        "adds": [
          "done:release:sensor-4",
          "ready:sensor-4",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4"
        }
      },
      {
        "id": "relock:sensor-4",
        "label": "relock sensor-4",
        "requires": [
          "done:verify:sensor-4"
        ],
        "forbids": [
          "done:relock:sensor-4"
        ],
        "adds": [
          "done:relock:sensor-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4"
        }
      },
      {
        "id": "verify:sensor-4",
        "label": "verify sensor-4",
        "requires": [
          "done:replace:sensor-4"
        ],
        "forbids": [
          "done:verify:sensor-4"
        ],
        "adds": [
          "done:verify:sensor-4"
        ],
        "deletes": [
          "fault:sensor-4",
          "misaligned:sensor-4"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4"
        }
      },
      {
        "id": "replace:sensor-4",
        "label": "replace sensor-4",
        "requires": [
          "done:unlock:sensor-4"
        ],
        "forbids": [
          "done:replace:sensor-4"
        ],
        "adds": [
          "done:replace:sensor-4"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "sensor-4"
        }
      },
      {
        "id": "unlock:sensor-4",
        "label": "unlock sensor-4",
        "requires": [
          "done:support:sensor-4"
        ],
        "forbids": [
          "done:unlock:sensor-4"
        ],
        "adds": [
          "done:unlock:sensor-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4"
        }
      },
      {
        "id": "support:sensor-4",
        "label": "support sensor-4",
        "requires": [
          "done:isolate:sensor-4"
        ],
        "forbids": [
          "done:support:sensor-4"
        ],
        "adds": [
          "done:support:sensor-4"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4"
        }
      },
      {
        "id": "isolate:sensor-4",
        "label": "isolate sensor-4",
        "requires": [
          "tool:free",
          "fault:sensor-4"
        ],
        "forbids": [
          "done:isolate:sensor-4"
        ],
        "adds": [
          "done:isolate:sensor-4"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-4"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:sensor-4",
      "fault:rack-4",
      "fault:exchange-pack-4",
      "fault:gate-4"
    ],
    "initialModules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0",
      "petal-0",
      "sensor-0",
      "rack-0",
      "exchange-pack-0",
      "gate-0",
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rack-1",
      "exchange-pack-1",
      "gate-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2",
      "rack-2",
      "exchange-pack-2",
      "gate-2",
      "rail-3",
      "carriage-3",
      "turret-3",
      "elbow-3",
      "head-3",
      "petal-3",
      "sensor-3",
      "rack-3",
      "exchange-pack-3",
      "gate-3",
      "rail-4",
      "carriage-4",
      "turret-4",
      "elbow-4",
      "head-4",
      "petal-4",
      "sensor-4",
      "rack-4",
      "exchange-pack-4",
      "gate-4"
    ],
    "goalFacts": [
      "ready:sensor-4",
      "ready:rack-4",
      "ready:exchange-pack-4",
      "ready:gate-4"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:gate-4",
      "support:gate-4",
      "unlock:gate-4",
      "replace:gate-4",
      "verify:gate-4",
      "relock:gate-4",
      "release:gate-4",
      "isolate:exchange-pack-4",
      "support:exchange-pack-4",
      "unlock:exchange-pack-4",
      "replace:exchange-pack-4",
      "verify:exchange-pack-4",
      "relock:exchange-pack-4",
      "release:exchange-pack-4",
      "isolate:rack-4",
      "support:rack-4",
      "unlock:rack-4",
      "replace:rack-4",
      "verify:rack-4",
      "relock:rack-4",
      "release:rack-4",
      "isolate:sensor-4",
      "support:sensor-4",
      "unlock:sensor-4",
      "replace:sensor-4",
      "verify:sensor-4",
      "relock:sensor-4",
      "release:sensor-4"
    ]
  }
}
```

### 预算约束检查策略（h3-segmented-antenna-yard-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "head-0",
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
        "cost": 2,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      },
      {
        "id": "probe",
        "cost": 0,
        "returns": {
          "nominal": "pass",
          "fault": "pass"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      }
    ],
    "budget": 2
  },
  "answer": {
    "queryId": "visual",
    "decisions": {
      "pass": "continue",
      "fail": "tighten"
    }
  }
}
```
