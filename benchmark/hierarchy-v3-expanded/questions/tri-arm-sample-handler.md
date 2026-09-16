## D3 三臂样品操作器

### 模块识别（h3-tri-arm-sample-handler-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：rail-0
- B：carriage-0
- C：head-0
- D：frame

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
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 部件计数（h3-tri-arm-sample-handler-count）

模块 head-0 有多少个可视零件？

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
        "id": "rail-0-p65",
        "moduleId": "rail-0",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "carriage-0-p66",
        "moduleId": "carriage-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-0-p67",
        "moduleId": "carriage-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-0-p68",
        "moduleId": "carriage-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-0-p69",
        "moduleId": "carriage-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "turret-0-p70",
        "moduleId": "turret-0",
        "shape": "cylinder",
        "color": "#e9ad37"
      },
      {
        "id": "elbow-0-p71",
        "moduleId": "elbow-0",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "head-0-p72",
        "moduleId": "head-0",
        "shape": "arch",
        "color": "#45a080"
      },
      {
        "id": "head-0-p73",
        "moduleId": "head-0",
        "shape": "panel",
        "color": "#dfebed"
      },
      {
        "id": "petal-0-p74",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p75",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p76",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p77",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p78",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p79",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p80",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p81",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p82",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p83",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p84",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-0-p85",
        "moduleId": "petal-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "sensor-0-p86",
        "moduleId": "sensor-0",
        "shape": "sphere",
        "color": "#79c7d8"
      },
      {
        "id": "rail-1-p87",
        "moduleId": "rail-1",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "carriage-1-p88",
        "moduleId": "carriage-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-1-p89",
        "moduleId": "carriage-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-1-p90",
        "moduleId": "carriage-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-1-p91",
        "moduleId": "carriage-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "turret-1-p92",
        "moduleId": "turret-1",
        "shape": "cylinder",
        "color": "#e9ad37"
      },
      {
        "id": "elbow-1-p93",
        "moduleId": "elbow-1",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "head-1-p94",
        "moduleId": "head-1",
        "shape": "arch",
        "color": "#45a080"
      },
      {
        "id": "head-1-p95",
        "moduleId": "head-1",
        "shape": "panel",
        "color": "#dfebed"
      },
      {
        "id": "petal-1-p96",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p97",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p98",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p99",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p100",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p101",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p102",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p103",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p104",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p105",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p106",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-1-p107",
        "moduleId": "petal-1",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "sensor-1-p108",
        "moduleId": "sensor-1",
        "shape": "sphere",
        "color": "#79c7d8"
      },
      {
        "id": "rail-2-p109",
        "moduleId": "rail-2",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "carriage-2-p110",
        "moduleId": "carriage-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-2-p111",
        "moduleId": "carriage-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-2-p112",
        "moduleId": "carriage-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-2-p113",
        "moduleId": "carriage-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "turret-2-p114",
        "moduleId": "turret-2",
        "shape": "cylinder",
        "color": "#e9ad37"
      },
      {
        "id": "elbow-2-p115",
        "moduleId": "elbow-2",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "head-2-p116",
        "moduleId": "head-2",
        "shape": "arch",
        "color": "#45a080"
      },
      {
        "id": "head-2-p117",
        "moduleId": "head-2",
        "shape": "panel",
        "color": "#dfebed"
      },
      {
        "id": "petal-2-p118",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p119",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p120",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p121",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p122",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p123",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p124",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p125",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p126",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p127",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p128",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "petal-2-p129",
        "moduleId": "petal-2",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "sensor-2-p130",
        "moduleId": "sensor-2",
        "shape": "sphere",
        "color": "#79c7d8"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-tri-arm-sample-handler-color）

零件 head-0-p72 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#45a080
- B：#2878b8
- C：#d43a32
- D：#f2bf3c

```json
{
  "input": {
    "part": {
      "id": "head-0-p72",
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
    "choiceId": "A"
  }
}
```

### 三维位置（h3-tri-arm-sample-handler-position）

模块 head-0 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[-4,1.5499999999999998,0]
- B：[-4,5.9875,0]
- C：[0,0.35,0]
- D：[-4,1,0]

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
        -4,
        1,
        0
      ],
      "carriage-0": [
        -4,
        1.5499999999999998,
        0
      ],
      "turret-0": [
        -4,
        2.2,
        0
      ],
      "elbow-0": [
        -4,
        4.05,
        0
      ],
      "head-0": [
        -4,
        5.9875,
        0
      ],
      "petal-0": [
        -4,
        7.25,
        0
      ],
      "sensor-0": [
        -4,
        7.75,
        0
      ],
      "rail-1": [
        0,
        1,
        0
      ],
      "carriage-1": [
        0,
        1.5499999999999998,
        0
      ],
      "turret-1": [
        0,
        2.2,
        0
      ],
      "elbow-1": [
        0,
        4.05,
        0
      ],
      "head-1": [
        0,
        5.9875,
        0
      ],
      "petal-1": [
        0,
        7.25,
        0
      ],
      "sensor-1": [
        0,
        7.75,
        0
      ],
      "rail-2": [
        4,
        1,
        0
      ],
      "carriage-2": [
        4,
        1.5499999999999998,
        0
      ],
      "turret-2": [
        4,
        2.2,
        0
      ],
      "elbow-2": [
        4,
        4.05,
        0
      ],
      "head-2": [
        4,
        5.9875,
        0
      ],
      "petal-2": [
        4,
        7.25,
        0
      ],
      "sensor-2": [
        4,
        7.75,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节类型（h3-tri-arm-sample-handler-joint-type）

carriage-0-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：revolute
- B：spring
- C：prismatic
- D：fixed

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
    "choiceId": "C"
  }
}
```

### 直接连接（h3-tri-arm-sample-handler-parent）

head-0 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["head-0"]
- B：[]
- C：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0","petal-0","sensor-0","rail-1","carriage-1","turret-1","elbow-1","head-1","petal-1","sensor-1","rail-2","carriage-2","turret-2","elbow-2","head-2","petal-2","sensor-2"]
- D：["elbow-0"]

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
          -4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 基座识别（h3-tri-arm-sample-handler-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：[]
- B：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0","petal-0","sensor-0","rail-1","carriage-1","turret-1","elbow-1","head-1","petal-1","sensor-1","rail-2","carriage-2","turret-2","elbow-2","head-2","petal-2","sensor-2"]
- C：["head-0"]
- D：["frame"]

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
          -4,
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
          -4,
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
          -4,
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
          -4,
          4.05,
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
          -4,
          5.9875,
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
          -4,
          7.25,
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
          -4,
          7.75,
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
        "id": "rail-1",
        "name": "rail 1",
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
        "id": "carriage-1",
        "name": "carriage 1",
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
        "id": "turret-1",
        "name": "turret 1",
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
        "id": "elbow-1",
        "name": "elbow 1",
        "role": "linkage",
        "position": [
          0,
          4.05,
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
          0,
          5.9875,
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
          0,
          7.25,
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
          0,
          7.75,
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
        "id": "rail-2",
        "name": "rail 2",
        "role": "guide",
        "position": [
          4,
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
          4,
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
          4,
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
          4,
          4.05,
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
          4,
          5.9875,
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
          4,
          7.25,
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
          4,
          7.75,
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
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 接口计数（h3-tri-arm-sample-handler-degree）

head-0 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：4
- B：2
- C：3
- D：1

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
          -4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 局部改色（h3-tri-arm-sample-handler-recolor）

仅将 head-0-p72 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"head-0-p72","color":"#e8792e"}
- B：{"id":"head-0-p73","color":"#e8792e"}
- C：{"id":"head-0-p72","color":"#2878b8"}
- D：{"id":"*","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "head-0-p72",
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
    "choiceId": "A"
  }
}
```

### 补装部件（h3-tri-arm-sample-handler-add）

模块 head-0 缺失零件 head-0-p72。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"head-0-p72","moduleId":"head-0","shape":"arch","position":[0,-0.08750000000000002,0],"size":[1.6,0.7,1],"color":"#000000","rotation":[0,0,0,1]}
- B：{"id":"head-0-p72","moduleId":"head-0","shape":"arch","position":[0,-0.08750000000000002,0],"size":[1.6,0.7,1],"color":"#45a080","rotation":[0,0,0,1]}
- C：{"id":"head-0-p72","moduleId":"frame","shape":"arch","position":[0,-0.08750000000000002,0],"size":[1.6,0.7,1],"color":"#45a080","rotation":[0,0,0,1]}
- D：{"id":"head-0-p72","moduleId":"head-0","shape":"arch","position":[0,-0.08750000000000002,0],"size":[3,3,3],"color":"#45a080","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "head-0-p72",
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
      "rail-0-p65",
      "carriage-0-p66",
      "carriage-0-p67",
      "carriage-0-p68",
      "carriage-0-p69",
      "turret-0-p70",
      "elbow-0-p71",
      "head-0-p73",
      "petal-0-p74",
      "petal-0-p75",
      "petal-0-p76",
      "petal-0-p77",
      "petal-0-p78",
      "petal-0-p79",
      "petal-0-p80",
      "petal-0-p81",
      "petal-0-p82",
      "petal-0-p83",
      "petal-0-p84",
      "petal-0-p85",
      "sensor-0-p86",
      "rail-1-p87",
      "carriage-1-p88",
      "carriage-1-p89",
      "carriage-1-p90",
      "carriage-1-p91",
      "turret-1-p92",
      "elbow-1-p93",
      "head-1-p94",
      "head-1-p95",
      "petal-1-p96",
      "petal-1-p97",
      "petal-1-p98",
      "petal-1-p99",
      "petal-1-p100",
      "petal-1-p101",
      "petal-1-p102",
      "petal-1-p103",
      "petal-1-p104",
      "petal-1-p105",
      "petal-1-p106",
      "petal-1-p107",
      "sensor-1-p108",
      "rail-2-p109",
      "carriage-2-p110",
      "carriage-2-p111",
      "carriage-2-p112",
      "carriage-2-p113",
      "turret-2-p114",
      "elbow-2-p115",
      "head-2-p116",
      "head-2-p117",
      "petal-2-p118",
      "petal-2-p119",
      "petal-2-p120",
      "petal-2-p121",
      "petal-2-p122",
      "petal-2-p123",
      "petal-2-p124",
      "petal-2-p125",
      "petal-2-p126",
      "petal-2-p127",
      "petal-2-p128",
      "petal-2-p129",
      "sensor-2-p130"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全拆除（h3-tri-arm-sample-handler-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["frame"]
- B：[]
- C：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0","petal-0","sensor-0","rail-1","carriage-1","turret-1","elbow-1","head-1","petal-1","sensor-1","rail-2","carriage-2","turret-2","elbow-2","head-2","petal-2","sensor-2"]
- D：["sensor-0","sensor-1","sensor-2"]

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
          -4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 替换选择（h3-tri-arm-sample-handler-replace）

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
        "cost": 4,
        "stiffness": 9,
        "mass": 0.7
      },
      {
        "id": "stock-1",
        "cost": 6,
        "stiffness": 10,
        "mass": 0.6
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 8,
        "mass": 0.9
      },
      {
        "id": "stock-3",
        "cost": 3,
        "stiffness": 10,
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

### 平移纠偏（h3-tri-arm-sample-handler-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,2,0]
- B：[-3,0,2]
- C：[3,0,-2]
- D：[0,0,0]

```json
{
  "input": {
    "delta": [
      3,
      0,
      -2
    ],
    "target": "head-0"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 姿态纠偏（h3-tri-arm-sample-handler-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：90
- B：-180
- C：180
- D：0

```json
{
  "input": {
    "module": "head-0",
    "currentYaw": 225,
    "targetYaw": 45
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 下一步放置（h3-tri-arm-sample-handler-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["elbow-1","rail-2"]
- B：[]
- C：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0","petal-0","sensor-0","rail-1","carriage-1","turret-1"]
- D：["elbow-1","head-1","petal-1","sensor-1","rail-2","carriage-2","turret-2","elbow-2","head-2","petal-2","sensor-2"]

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
      "rail-1",
      "carriage-1",
      "turret-1"
    ],
    "joints": [
      {
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
        "type": "fixed",
        "anchorParent": [
          -4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 库存核算（h3-tri-arm-sample-handler-inventory）

备件库有 2 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：1
- B：3
- C：0

```json
{
  "input": {
    "available": 2,
    "required": 2
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 子装配边界（h3-tri-arm-sample-handler-boundary）

隔离 head-0 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["head-0-joint","petal-0-joint"]
- B：[]
- C：["rail-0-joint","carriage-0-joint","turret-0-joint","elbow-0-joint","head-0-joint","petal-0-joint","sensor-0-joint","rail-1-joint","carriage-1-joint","turret-1-joint","elbow-1-joint","head-1-joint","petal-1-joint","sensor-1-joint","rail-2-joint","carriage-2-joint","turret-2-joint","elbow-2-joint","head-2-joint","petal-2-joint","sensor-2-joint"]
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
          -4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
    ],
    "target": "head-0"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 最小干预（h3-tri-arm-sample-handler-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：0

```json
{
  "input": {
    "module": "head-0"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 全过程依赖（h3-tri-arm-sample-handler-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：21
- B：9
- C：-1
- D：10

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
      "rail-1",
      "turret-1",
      "carriage-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2"
    ],
    "joints": [
      {
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
        "type": "fixed",
        "anchorParent": [
          -4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 连续维修路径（h3-tri-arm-sample-handler-access）

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
          9.49,
          5.9875,
          0
        ],
        "end": [
          -4,
          5.9875,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.3343217074871063
      },
      {
        "id": "path-1",
        "start": [
          -4,
          12.05,
          0
        ],
        "end": [
          -4,
          5.9875,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.6301031708717346
      },
      {
        "id": "path-2",
        "start": [
          -4,
          5.9875,
          8
        ],
        "end": [
          -4,
          5.9875,
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
      "B"
    ]
  }
}
```

### 支撑反事实（h3-tri-arm-sample-handler-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0","petal-0","sensor-0","rail-1","carriage-1","turret-1","elbow-1","head-1","petal-1","sensor-1","rail-2","carriage-2","turret-2","elbow-2","head-2","petal-2","sensor-2"]
- C：["carriage-0","elbow-0","head-0","petal-0","sensor-0","turret-0"]
- D：["rail-0"]

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
          -4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-tri-arm-sample-handler-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：1.0118
- B：0.0118
- C：0.2118
- D：0

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.007674306809934908
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.011768103079785186
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.005265001805380935
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.002690732923182377
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0029329107684124096
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00002272584511140016
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0011279783055376713
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00037783589751404375
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0003013510420704657
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.00015384934930359628
      },
      {
        "time": 1,
        "displacement": 0.00015384934930359628
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.000003814697265630505,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节限位推理（h3-tri-arm-sample-handler-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-0.8
- B：0
- C：-1.3
- D：1.3

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
      "A",
      "B"
    ]
  }
}
```

### 约束故障诊断（h3-tri-arm-sample-handler-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：carriage-0-joint
- B：turret-0-joint
- C：head-0-joint
- D：rail-0-joint

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
          -4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-1-joint",
        "name": "rail-1 interface",
        "parent": "frame",
        "child": "rail-1",
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
        "id": "rail-2-joint",
        "name": "rail-2 interface",
        "parent": "frame",
        "child": "rail-2",
        "type": "fixed",
        "anchorParent": [
          4,
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
          -1.4,
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
          1.8499999999999996,
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
          0.49999999999999983,
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
    ]
  },
  "answer": {
    "choiceIds": [
      "C"
    ]
  }
}
```

### 主动检查收益（h3-tri-arm-sample-handler-information-gain）

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
      "B",
      "C"
    ]
  }
}
```

### 不确定性与弃答（h3-tri-arm-sample-handler-abstention）

所有相容世界是否允许同一个后续动作？选择继续执行或请求检查。

能力：不确定性与弃答；形式：single-choice；证据：finite-world。

- A：commit
- B：inspect

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
    "choiceId": "A"
  }
}
```

### 观测后信念更新（h3-tri-arm-sample-handler-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.3333333333333333
- B：0.5
- C：0
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
      "positive",
      "negative",
      "positive",
      "negative"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 多目标工程权衡（h3-tri-arm-sample-handler-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-3
- B：stock-0
- C：stock-1
- D：stock-2

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 4,
        "stiffness": 9,
        "mass": 0.7
      },
      {
        "id": "stock-1",
        "cost": 6,
        "stiffness": 10,
        "mass": 0.6
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 8,
        "mass": 0.9
      },
      {
        "id": "stock-3",
        "cost": 3,
        "stiffness": 10,
        "mass": 0.5
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

### 依赖装配（h3-tri-arm-sample-handler-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
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
      "present:rail-1",
      "present:carriage-1",
      "present:turret-1",
      "present:elbow-1",
      "present:head-1",
      "present:petal-1",
      "present:sensor-1",
      "present:rail-2",
      "present:carriage-2",
      "present:turret-2",
      "present:elbow-2",
      "present:head-2",
      "present:petal-2",
      "present:sensor-2"
    ],
    "budget": 22,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:frame",
      "place:rail-1",
      "place:carriage-1",
      "place:turret-1",
      "place:rail-0",
      "place:carriage-0",
      "place:turret-0",
      "place:rail-2",
      "place:carriage-2",
      "place:elbow-0",
      "place:head-0",
      "place:petal-0",
      "place:sensor-0",
      "place:elbow-1",
      "place:head-1",
      "place:petal-1",
      "place:sensor-1",
      "place:turret-2",
      "place:elbow-2",
      "place:head-2",
      "place:petal-2",
      "place:sensor-2"
    ]
  }
}
```

### 依赖拆解（h3-tri-arm-sample-handler-disassembly）

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
      "present:rail-1",
      "present:carriage-1",
      "present:turret-1",
      "present:elbow-1",
      "present:head-1",
      "present:petal-1",
      "present:sensor-1",
      "present:rail-2",
      "present:carriage-2",
      "present:turret-2",
      "present:elbow-2",
      "present:head-2",
      "present:petal-2",
      "present:sensor-2"
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
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2"
    ],
    "actions": [
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
        "id": "remove:frame",
        "label": "拆除 frame",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rail-0",
          "present:rail-1",
          "present:rail-2"
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
      }
    ],
    "goalFacts": [
      "removed:sensor-2",
      "removed:petal-2",
      "removed:head-2",
      "removed:elbow-2",
      "removed:turret-2",
      "removed:carriage-2",
      "removed:rail-2",
      "removed:sensor-1",
      "removed:petal-1",
      "removed:head-1",
      "removed:elbow-1",
      "removed:turret-1",
      "removed:carriage-1",
      "removed:rail-1",
      "removed:sensor-0",
      "removed:petal-0",
      "removed:head-0",
      "removed:elbow-0",
      "removed:turret-0",
      "removed:carriage-0",
      "removed:rail-0",
      "removed:frame"
    ],
    "budget": 22,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:sensor-1",
      "remove:sensor-2",
      "remove:petal-2",
      "remove:head-2",
      "remove:elbow-2",
      "remove:turret-2",
      "remove:carriage-2",
      "remove:rail-2",
      "remove:sensor-0",
      "remove:petal-0",
      "remove:head-0",
      "remove:elbow-0",
      "remove:turret-0",
      "remove:carriage-0",
      "remove:rail-0",
      "remove:petal-1",
      "remove:head-1",
      "remove:elbow-1",
      "remove:turret-1",
      "remove:carriage-1",
      "remove:rail-1",
      "remove:frame"
    ]
  }
}
```

### 承载维修（h3-tri-arm-sample-handler-service-repair）

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
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2"
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

### 复合编辑验证（h3-tri-arm-sample-handler-compound-edit）

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
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2"
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

### 跨区域联合维修（h3-tri-arm-sample-handler-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:head-2",
      "closed:head-2",
      "fault:petal-2",
      "closed:petal-2",
      "fault:sensor-2",
      "closed:sensor-2"
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
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2"
    ],
    "actions": [
      {
        "id": "verify:head-2",
        "label": "verify head-2",
        "requires": [
          "done:replace:head-2"
        ],
        "forbids": [
          "done:verify:head-2"
        ],
        "adds": [
          "done:verify:head-2"
        ],
        "deletes": [
          "fault:head-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-2"
        }
      },
      {
        "id": "replace:petal-2",
        "label": "replace petal-2",
        "requires": [
          "done:remove:petal-2"
        ],
        "forbids": [
          "done:replace:petal-2"
        ],
        "adds": [
          "done:replace:petal-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2",
          "visible": true
        }
      },
      {
        "id": "close:head-2",
        "label": "close head-2",
        "requires": [
          "done:verify:head-2"
        ],
        "forbids": [
          "done:close:head-2"
        ],
        "adds": [
          "done:close:head-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-2"
        }
      },
      {
        "id": "replace:head-2",
        "label": "replace head-2",
        "requires": [
          "done:remove:head-2"
        ],
        "forbids": [
          "done:replace:head-2"
        ],
        "adds": [
          "done:replace:head-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-2",
          "visible": true
        }
      },
      {
        "id": "open:sensor-2",
        "label": "open sensor-2",
        "requires": [
          "done:support:sensor-2"
        ],
        "forbids": [
          "done:open:sensor-2"
        ],
        "adds": [
          "done:open:sensor-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2"
        }
      },
      {
        "id": "open:petal-2",
        "label": "open petal-2",
        "requires": [
          "done:support:petal-2"
        ],
        "forbids": [
          "done:open:petal-2"
        ],
        "adds": [
          "done:open:petal-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2"
        }
      },
      {
        "id": "release:head-2",
        "label": "release head-2",
        "requires": [
          "done:close:head-2"
        ],
        "forbids": [
          "done:release:head-2"
        ],
        "adds": [
          "done:release:head-2",
          "repaired:head-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-2"
        }
      },
      {
        "id": "support:petal-2",
        "label": "support petal-2",
        "requires": [
          "fault:petal-2"
        ],
        "forbids": [
          "done:support:petal-2"
        ],
        "adds": [
          "done:support:petal-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2"
        }
      },
      {
        "id": "verify:sensor-2",
        "label": "verify sensor-2",
        "requires": [
          "done:replace:sensor-2"
        ],
        "forbids": [
          "done:verify:sensor-2"
        ],
        "adds": [
          "done:verify:sensor-2"
        ],
        "deletes": [
          "fault:sensor-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2"
        }
      },
      {
        "id": "remove:petal-2",
        "label": "remove petal-2",
        "requires": [
          "done:open:petal-2"
        ],
        "forbids": [
          "done:remove:petal-2"
        ],
        "adds": [
          "done:remove:petal-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2",
          "visible": false
        }
      },
      {
        "id": "remove:sensor-2",
        "label": "remove sensor-2",
        "requires": [
          "done:open:sensor-2"
        ],
        "forbids": [
          "done:remove:sensor-2"
        ],
        "adds": [
          "done:remove:sensor-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2",
          "visible": false
        }
      },
      {
        "id": "release:sensor-2",
        "label": "release sensor-2",
        "requires": [
          "done:close:sensor-2"
        ],
        "forbids": [
          "done:release:sensor-2"
        ],
        "adds": [
          "done:release:sensor-2",
          "repaired:sensor-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2"
        }
      },
      {
        "id": "replace:sensor-2",
        "label": "replace sensor-2",
        "requires": [
          "done:remove:sensor-2"
        ],
        "forbids": [
          "done:replace:sensor-2"
        ],
        "adds": [
          "done:replace:sensor-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2",
          "visible": true
        }
      },
      {
        "id": "support:head-2",
        "label": "support head-2",
        "requires": [
          "fault:head-2"
        ],
        "forbids": [
          "done:support:head-2"
        ],
        "adds": [
          "done:support:head-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-2"
        }
      },
      {
        "id": "verify:petal-2",
        "label": "verify petal-2",
        "requires": [
          "done:replace:petal-2"
        ],
        "forbids": [
          "done:verify:petal-2"
        ],
        "adds": [
          "done:verify:petal-2"
        ],
        "deletes": [
          "fault:petal-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2"
        }
      },
      {
        "id": "support:sensor-2",
        "label": "support sensor-2",
        "requires": [
          "fault:sensor-2"
        ],
        "forbids": [
          "done:support:sensor-2"
        ],
        "adds": [
          "done:support:sensor-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2"
        }
      },
      {
        "id": "release:petal-2",
        "label": "release petal-2",
        "requires": [
          "done:close:petal-2"
        ],
        "forbids": [
          "done:release:petal-2"
        ],
        "adds": [
          "done:release:petal-2",
          "repaired:petal-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2"
        }
      },
      {
        "id": "close:sensor-2",
        "label": "close sensor-2",
        "requires": [
          "done:verify:sensor-2"
        ],
        "forbids": [
          "done:close:sensor-2"
        ],
        "adds": [
          "done:close:sensor-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2"
        }
      },
      {
        "id": "open:head-2",
        "label": "open head-2",
        "requires": [
          "done:support:head-2"
        ],
        "forbids": [
          "done:open:head-2"
        ],
        "adds": [
          "done:open:head-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-2"
        }
      },
      {
        "id": "remove:head-2",
        "label": "remove head-2",
        "requires": [
          "done:open:head-2"
        ],
        "forbids": [
          "done:remove:head-2"
        ],
        "adds": [
          "done:remove:head-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-2",
          "visible": false
        }
      },
      {
        "id": "close:petal-2",
        "label": "close petal-2",
        "requires": [
          "done:verify:petal-2"
        ],
        "forbids": [
          "done:close:petal-2"
        ],
        "adds": [
          "done:close:petal-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2"
        }
      }
    ],
    "goalFacts": [
      "repaired:head-2",
      "repaired:petal-2",
      "repaired:sensor-2"
    ],
    "budget": 21,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:petal-2",
      "open:petal-2",
      "remove:petal-2",
      "replace:petal-2",
      "support:head-2",
      "verify:petal-2",
      "support:sensor-2",
      "open:sensor-2",
      "remove:sensor-2",
      "replace:sensor-2",
      "verify:sensor-2",
      "close:sensor-2",
      "release:sensor-2",
      "open:head-2",
      "remove:head-2",
      "replace:head-2",
      "verify:head-2",
      "close:head-2",
      "release:head-2",
      "close:petal-2",
      "release:petal-2"
    ]
  }
}
```

### 多工位资源调度（h3-tri-arm-sample-handler-scheduling）

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
      }
    ],
    "deadline": 9
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
      "job-7": 3
    }
  }
}
```

### 检查后条件策略（h3-tri-arm-sample-handler-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "head-0",
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

### 局部坐标变换（h3-tri-arm-sample-handler-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[-3,5.9,0]
- B：[-3,6.9,0]
- C：[-4,5.9,-1]
- D：[1,-0.0875,0]

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
      0.7071067811865475,
      0,
      0.7071067811865476
    ],
    "translation": [
      -4,
      5.9875,
      0
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-tri-arm-sample-handler-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[0,0]
- B：[4,9]
- C：[9,4]
- D：[4,5]

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
    "choiceId": "B"
  }
}
```

### 空间相对关系（h3-tri-arm-sample-handler-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：equal
- B：greater
- C：less

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
      "id": "sensor-2",
      "position": [
        4,
        7.75,
        0
      ]
    },
    "axis": "x"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 约束自由度（h3-tri-arm-sample-handler-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：6
- B：1
- C：0
- D：3

```json
{
  "input": {
    "joint": {
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
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 维修间隙预算（h3-tri-arm-sample-handler-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "head-0",
    "aperture": 0.5900000000000001,
    "toolWidth": 0.55,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-tri-arm-sample-handler-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,-3,0]
- B：[0,0,-15]
- C：[0,0,15]
- D：[0,0,0]

```json
{
  "input": {
    "module": "head-0",
    "lever": [
      3,
      1,
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
    "choiceId": "B"
  }
}
```

### 非均匀先验更新（h3-tri-arm-sample-handler-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.5555555555555556
- B：0.38461538461538464
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
      4,
      5,
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

### 风险最小决策（h3-tri-arm-sample-handler-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.6,
    "repairCost": 3,
    "failureLoss": 13,
    "module": "head-0"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-tri-arm-sample-handler-trace-threshold）

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
        "displacement": 0.007674306809934908
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.011768103079785186
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.005265001805380935
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.002690732923182377
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0029329107684124096
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00002272584511140016
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0011279783055376713
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00037783589751404375
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0003013510420704657
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.00015384934930359628
      },
      {
        "time": 1,
        "displacement": 0.00015384934930359628
      }
    ],
    "threshold": 0.014121723695742222
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-tri-arm-sample-handler-guarded-repair）

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
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2"
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

### 失败状态回退（h3-tri-arm-sample-handler-rollback）

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
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2"
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

### 共享工具协同维修（h3-tri-arm-sample-handler-resource-repair）

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
        "id": "release:sensor-2",
        "label": "release sensor-2",
        "requires": [
          "done:relock:sensor-2"
        ],
        "forbids": [
          "done:release:sensor-2"
        ],
        "adds": [
          "done:release:sensor-2",
          "ready:sensor-2",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2"
        }
      },
      {
        "id": "relock:sensor-2",
        "label": "relock sensor-2",
        "requires": [
          "done:verify:sensor-2"
        ],
        "forbids": [
          "done:relock:sensor-2"
        ],
        "adds": [
          "done:relock:sensor-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2"
        }
      },
      {
        "id": "verify:sensor-2",
        "label": "verify sensor-2",
        "requires": [
          "done:replace:sensor-2"
        ],
        "forbids": [
          "done:verify:sensor-2"
        ],
        "adds": [
          "done:verify:sensor-2"
        ],
        "deletes": [
          "fault:sensor-2",
          "misaligned:sensor-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2"
        }
      },
      {
        "id": "replace:sensor-2",
        "label": "replace sensor-2",
        "requires": [
          "done:unlock:sensor-2"
        ],
        "forbids": [
          "done:replace:sensor-2"
        ],
        "adds": [
          "done:replace:sensor-2"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "sensor-2"
        }
      },
      {
        "id": "unlock:sensor-2",
        "label": "unlock sensor-2",
        "requires": [
          "done:support:sensor-2"
        ],
        "forbids": [
          "done:unlock:sensor-2"
        ],
        "adds": [
          "done:unlock:sensor-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2"
        }
      },
      {
        "id": "support:sensor-2",
        "label": "support sensor-2",
        "requires": [
          "done:isolate:sensor-2"
        ],
        "forbids": [
          "done:support:sensor-2"
        ],
        "adds": [
          "done:support:sensor-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2"
        }
      },
      {
        "id": "isolate:sensor-2",
        "label": "isolate sensor-2",
        "requires": [
          "tool:free",
          "fault:sensor-2"
        ],
        "forbids": [
          "done:isolate:sensor-2"
        ],
        "adds": [
          "done:isolate:sensor-2"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-2"
        }
      },
      {
        "id": "release:petal-2",
        "label": "release petal-2",
        "requires": [
          "done:relock:petal-2"
        ],
        "forbids": [
          "done:release:petal-2"
        ],
        "adds": [
          "done:release:petal-2",
          "ready:petal-2",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2"
        }
      },
      {
        "id": "relock:petal-2",
        "label": "relock petal-2",
        "requires": [
          "done:verify:petal-2"
        ],
        "forbids": [
          "done:relock:petal-2"
        ],
        "adds": [
          "done:relock:petal-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2"
        }
      },
      {
        "id": "verify:petal-2",
        "label": "verify petal-2",
        "requires": [
          "done:replace:petal-2"
        ],
        "forbids": [
          "done:verify:petal-2"
        ],
        "adds": [
          "done:verify:petal-2"
        ],
        "deletes": [
          "fault:petal-2",
          "misaligned:petal-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2"
        }
      },
      {
        "id": "replace:petal-2",
        "label": "replace petal-2",
        "requires": [
          "done:unlock:petal-2"
        ],
        "forbids": [
          "done:replace:petal-2"
        ],
        "adds": [
          "done:replace:petal-2"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "petal-2"
        }
      },
      {
        "id": "unlock:petal-2",
        "label": "unlock petal-2",
        "requires": [
          "done:support:petal-2"
        ],
        "forbids": [
          "done:unlock:petal-2"
        ],
        "adds": [
          "done:unlock:petal-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2"
        }
      },
      {
        "id": "support:petal-2",
        "label": "support petal-2",
        "requires": [
          "done:isolate:petal-2"
        ],
        "forbids": [
          "done:support:petal-2"
        ],
        "adds": [
          "done:support:petal-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2"
        }
      },
      {
        "id": "isolate:petal-2",
        "label": "isolate petal-2",
        "requires": [
          "tool:free",
          "fault:petal-2"
        ],
        "forbids": [
          "done:isolate:petal-2"
        ],
        "adds": [
          "done:isolate:petal-2"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "petal-2"
        }
      },
      {
        "id": "release:head-2",
        "label": "release head-2",
        "requires": [
          "done:relock:head-2"
        ],
        "forbids": [
          "done:release:head-2"
        ],
        "adds": [
          "done:release:head-2",
          "ready:head-2",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-2"
        }
      },
      {
        "id": "relock:head-2",
        "label": "relock head-2",
        "requires": [
          "done:verify:head-2"
        ],
        "forbids": [
          "done:relock:head-2"
        ],
        "adds": [
          "done:relock:head-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-2"
        }
      },
      {
        "id": "verify:head-2",
        "label": "verify head-2",
        "requires": [
          "done:replace:head-2"
        ],
        "forbids": [
          "done:verify:head-2"
        ],
        "adds": [
          "done:verify:head-2"
        ],
        "deletes": [
          "fault:head-2",
          "misaligned:head-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-2"
        }
      },
      {
        "id": "replace:head-2",
        "label": "replace head-2",
        "requires": [
          "done:unlock:head-2"
        ],
        "forbids": [
          "done:replace:head-2"
        ],
        "adds": [
          "done:replace:head-2"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "head-2"
        }
      },
      {
        "id": "unlock:head-2",
        "label": "unlock head-2",
        "requires": [
          "done:support:head-2"
        ],
        "forbids": [
          "done:unlock:head-2"
        ],
        "adds": [
          "done:unlock:head-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-2"
        }
      },
      {
        "id": "support:head-2",
        "label": "support head-2",
        "requires": [
          "done:isolate:head-2"
        ],
        "forbids": [
          "done:support:head-2"
        ],
        "adds": [
          "done:support:head-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "head-2"
        }
      },
      {
        "id": "isolate:head-2",
        "label": "isolate head-2",
        "requires": [
          "tool:free",
          "fault:head-2"
        ],
        "forbids": [
          "done:isolate:head-2"
        ],
        "adds": [
          "done:isolate:head-2"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "head-2"
        }
      },
      {
        "id": "release:elbow-2",
        "label": "release elbow-2",
        "requires": [
          "done:relock:elbow-2"
        ],
        "forbids": [
          "done:release:elbow-2"
        ],
        "adds": [
          "done:release:elbow-2",
          "ready:elbow-2",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-2"
        }
      },
      {
        "id": "relock:elbow-2",
        "label": "relock elbow-2",
        "requires": [
          "done:verify:elbow-2"
        ],
        "forbids": [
          "done:relock:elbow-2"
        ],
        "adds": [
          "done:relock:elbow-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-2"
        }
      },
      {
        "id": "verify:elbow-2",
        "label": "verify elbow-2",
        "requires": [
          "done:replace:elbow-2"
        ],
        "forbids": [
          "done:verify:elbow-2"
        ],
        "adds": [
          "done:verify:elbow-2"
        ],
        "deletes": [
          "fault:elbow-2",
          "misaligned:elbow-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-2"
        }
      },
      {
        "id": "replace:elbow-2",
        "label": "replace elbow-2",
        "requires": [
          "done:unlock:elbow-2"
        ],
        "forbids": [
          "done:replace:elbow-2"
        ],
        "adds": [
          "done:replace:elbow-2"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "elbow-2"
        }
      },
      {
        "id": "unlock:elbow-2",
        "label": "unlock elbow-2",
        "requires": [
          "done:support:elbow-2"
        ],
        "forbids": [
          "done:unlock:elbow-2"
        ],
        "adds": [
          "done:unlock:elbow-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-2"
        }
      },
      {
        "id": "support:elbow-2",
        "label": "support elbow-2",
        "requires": [
          "done:isolate:elbow-2"
        ],
        "forbids": [
          "done:support:elbow-2"
        ],
        "adds": [
          "done:support:elbow-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-2"
        }
      },
      {
        "id": "isolate:elbow-2",
        "label": "isolate elbow-2",
        "requires": [
          "tool:free",
          "fault:elbow-2"
        ],
        "forbids": [
          "done:isolate:elbow-2"
        ],
        "adds": [
          "done:isolate:elbow-2"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-2"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:elbow-2",
      "fault:head-2",
      "fault:petal-2",
      "fault:sensor-2"
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
      "rail-1",
      "carriage-1",
      "turret-1",
      "elbow-1",
      "head-1",
      "petal-1",
      "sensor-1",
      "rail-2",
      "carriage-2",
      "turret-2",
      "elbow-2",
      "head-2",
      "petal-2",
      "sensor-2"
    ],
    "goalFacts": [
      "ready:elbow-2",
      "ready:head-2",
      "ready:petal-2",
      "ready:sensor-2"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:sensor-2",
      "support:sensor-2",
      "unlock:sensor-2",
      "replace:sensor-2",
      "verify:sensor-2",
      "relock:sensor-2",
      "release:sensor-2",
      "isolate:petal-2",
      "support:petal-2",
      "unlock:petal-2",
      "replace:petal-2",
      "verify:petal-2",
      "relock:petal-2",
      "release:petal-2",
      "isolate:head-2",
      "support:head-2",
      "unlock:head-2",
      "replace:head-2",
      "verify:head-2",
      "relock:head-2",
      "release:head-2",
      "isolate:elbow-2",
      "support:elbow-2",
      "unlock:elbow-2",
      "replace:elbow-2",
      "verify:elbow-2",
      "relock:elbow-2",
      "release:elbow-2"
    ]
  }
}
```

### 预算约束检查策略（h3-tri-arm-sample-handler-budget-policy）

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
        "action": "replace"
      }
    ],
    "queries": [
      {
        "id": "visual",
        "cost": 1,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "probe",
        "cost": 0,
        "returns": {
          "nominal": "clear",
          "fault": "clear"
        }
      },
      {
        "id": "thermal",
        "cost": 2,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      }
    ],
    "budget": 1
  },
  "answer": {
    "queryId": "visual",
    "decisions": {
      "clear": "continue",
      "alert": "replace"
    }
  }
}
```
