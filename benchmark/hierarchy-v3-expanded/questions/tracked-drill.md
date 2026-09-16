## D2 履带取芯钻机

### 模块识别（h3-tracked-drill-identify）

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
        "id": "track--1",
        "name": "track  1"
      },
      {
        "id": "track-1",
        "name": "track 1"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 部件计数（h3-tracked-drill-count）

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
        "id": "mast-p31",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p32",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p33",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p34",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p35",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p36",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p37",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p38",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p39",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p40",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p41",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p42",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p43",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p44",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p45",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p46",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p47",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p48",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p49",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p50",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p51",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p52",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p53",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p54",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p55",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "mast-p56",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "primary-boom-p57",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p58",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p59",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p60",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p61",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p62",
        "moduleId": "primary-boom",
        "shape": "gear",
        "color": "#273e50"
      },
      {
        "id": "tool-head-p63",
        "moduleId": "tool-head",
        "shape": "gear",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p64",
        "moduleId": "tool-head",
        "shape": "axle",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p65",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p66",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p67",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p68",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p69",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p70",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p71",
        "moduleId": "control-cab",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "control-cab-p72",
        "moduleId": "control-cab",
        "shape": "slope",
        "color": "#387bb3"
      },
      {
        "id": "service-cartridge-p73",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p74",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p75",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p76",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "track--1-p77",
        "moduleId": "track--1",
        "shape": "wheel",
        "color": "#273e50"
      },
      {
        "id": "track--1-p78",
        "moduleId": "track--1",
        "shape": "wheel",
        "color": "#273e50"
      },
      {
        "id": "track--1-p79",
        "moduleId": "track--1",
        "shape": "wheel",
        "color": "#273e50"
      },
      {
        "id": "track--1-p80",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p81",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p82",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p83",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p84",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p85",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p86",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p87",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p88",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p89",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p90",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p91",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p92",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p93",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p94",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p95",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p96",
        "moduleId": "track-1",
        "shape": "wheel",
        "color": "#273e50"
      },
      {
        "id": "track-1-p97",
        "moduleId": "track-1",
        "shape": "wheel",
        "color": "#273e50"
      },
      {
        "id": "track-1-p98",
        "moduleId": "track-1",
        "shape": "wheel",
        "color": "#273e50"
      },
      {
        "id": "track-1-p99",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p100",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p101",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p102",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p103",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p104",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p105",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p106",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p107",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p108",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p109",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p110",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p111",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p112",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p113",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p114",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 颜色识别（h3-tracked-drill-color）

零件 service-cartridge-p73 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#dc6040
- B：#2878b8
- C：#d43a32
- D：#f2bf3c

```json
{
  "input": {
    "part": {
      "id": "service-cartridge-p73",
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
    "choiceId": "A"
  }
}
```

### 三维位置（h3-tracked-drill-position）

模块 service-cartridge 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0.6748883430420973,3.9264046688160024,-0.6]
- B：[2,0.8500000000000001,-2]
- C：[0,0.35,0]
- D：[-1.6,2.45,-0.6000000000000001]

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
        2.45,
        -0.6000000000000001
      ],
      "primary-boom": [
        0.6748883430420973,
        3.9264046688160024,
        -0.6
      ],
      "tool-head": [
        4.243855389680211,
        2.752809337632004,
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
      "track--1": [
        -0.050000000000000266,
        0.7,
        -4
      ],
      "track-1": [
        -0.050000000000000266,
        0.7,
        4
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节类型（h3-tracked-drill-joint-type）

primary-boom-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：revolute
- B：fixed
- C：prismatic
- D：spring

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
        1.8499999999999999,
        0
      ],
      "anchorChild": [
        -2.2748883430420976,
        0.373595331183998,
        0
      ],
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
    "choiceId": "A"
  }
}
```

### 直接连接（h3-tracked-drill-parent）

service-cartridge 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","track--1","track-1"]
- C：["foundation"]
- D：["service-cartridge"]

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
          -1.55,
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
          1.8499999999999999,
          0
        ],
        "anchorChild": [
          -2.2748883430420976,
          0.373595331183998,
          0
        ],
        "axis": [
          0,
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
        "type": "prismatic",
        "anchorParent": [
          3.5689670466381136,
          -0.3735953311839978,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
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
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
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
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 基座识别（h3-tracked-drill-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","track--1","track-1"]
- C：["service-cartridge"]
- D：["foundation"]

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
          2.45,
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
          0.6748883430420975,
          3.926404668816002,
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
          4.243855389680211,
          2.752809337632004,
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
        "id": "track--1",
        "name": "track  1",
        "role": "traction",
        "position": [
          -0.050000000000000266,
          0.7,
          -4
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
        "id": "track-1",
        "name": "track 1",
        "role": "traction",
        "position": [
          -0.050000000000000266,
          0.7,
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
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 接口计数（h3-tracked-drill-degree）

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
          -1.55,
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
          1.8499999999999999,
          0
        ],
        "anchorChild": [
          -2.2748883430420976,
          0.373595331183998,
          0
        ],
        "axis": [
          0,
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
        "type": "prismatic",
        "anchorParent": [
          3.5689670466381136,
          -0.3735953311839978,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
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
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
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
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 局部改色（h3-tracked-drill-recolor）

仅将 service-cartridge-p73 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"service-cartridge-p73","color":"#e8792e"}
- B：{"id":"service-cartridge-p74","color":"#e8792e"}
- C：{"id":"service-cartridge-p73","color":"#2878b8"}
- D：{"id":"*","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "service-cartridge-p73",
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
    "choiceId": "A"
  }
}
```

### 补装部件（h3-tracked-drill-add）

模块 service-cartridge 缺失零件 service-cartridge-p73。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"service-cartridge-p73","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#000000","rotation":[0,0,0,1]}
- B：{"id":"service-cartridge-p73","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#dc6040","rotation":[0,0,0,1]}
- C：{"id":"service-cartridge-p73","moduleId":"foundation","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#dc6040","rotation":[0,0,0,1]}
- D：{"id":"service-cartridge-p73","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[3,3,3],"color":"#dc6040","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "service-cartridge-p73",
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
      "mast-p31",
      "mast-p32",
      "mast-p33",
      "mast-p34",
      "mast-p35",
      "mast-p36",
      "mast-p37",
      "mast-p38",
      "mast-p39",
      "mast-p40",
      "mast-p41",
      "mast-p42",
      "mast-p43",
      "mast-p44",
      "mast-p45",
      "mast-p46",
      "mast-p47",
      "mast-p48",
      "mast-p49",
      "mast-p50",
      "mast-p51",
      "mast-p52",
      "mast-p53",
      "mast-p54",
      "mast-p55",
      "mast-p56",
      "primary-boom-p57",
      "primary-boom-p58",
      "primary-boom-p59",
      "primary-boom-p60",
      "primary-boom-p61",
      "primary-boom-p62",
      "tool-head-p63",
      "tool-head-p64",
      "control-cab-p65",
      "control-cab-p66",
      "control-cab-p67",
      "control-cab-p68",
      "control-cab-p69",
      "control-cab-p70",
      "control-cab-p71",
      "control-cab-p72",
      "service-cartridge-p74",
      "service-cartridge-p75",
      "service-cartridge-p76",
      "track--1-p77",
      "track--1-p78",
      "track--1-p79",
      "track--1-p80",
      "track--1-p81",
      "track--1-p82",
      "track--1-p83",
      "track--1-p84",
      "track--1-p85",
      "track--1-p86",
      "track--1-p87",
      "track--1-p88",
      "track--1-p89",
      "track--1-p90",
      "track--1-p91",
      "track--1-p92",
      "track--1-p93",
      "track--1-p94",
      "track--1-p95",
      "track-1-p96",
      "track-1-p97",
      "track-1-p98",
      "track-1-p99",
      "track-1-p100",
      "track-1-p101",
      "track-1-p102",
      "track-1-p103",
      "track-1-p104",
      "track-1-p105",
      "track-1-p106",
      "track-1-p107",
      "track-1-p108",
      "track-1-p109",
      "track-1-p110",
      "track-1-p111",
      "track-1-p112",
      "track-1-p113",
      "track-1-p114"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全拆除（h3-tracked-drill-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["control-cab","service-cartridge","tool-head","track--1","track-1"]
- B：["foundation"]
- C：[]
- D：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","track--1","track-1"]

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
          -1.55,
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
          1.8499999999999999,
          0
        ],
        "anchorChild": [
          -2.2748883430420976,
          0.373595331183998,
          0
        ],
        "axis": [
          0,
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
        "type": "prismatic",
        "anchorParent": [
          3.5689670466381136,
          -0.3735953311839978,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
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
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
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
    ],
    "modules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "track--1",
      "track-1"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 替换选择（h3-tracked-drill-replace）

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
        "cost": 6,
        "stiffness": 6,
        "mass": 1.9
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 5,
        "mass": 1.8
      },
      {
        "id": "stock-2",
        "cost": 3,
        "stiffness": 7,
        "mass": 1.1
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 11,
        "mass": 1.5
      }
    ],
    "maxCost": 6
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 平移纠偏（h3-tracked-drill-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,2,0]
- C：[-2,0,2]
- D：[2,0,-2]

```json
{
  "input": {
    "delta": [
      2,
      0,
      -2
    ],
    "target": "service-cartridge"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-tracked-drill-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：0
- B：90
- C：-180
- D：180

```json
{
  "input": {
    "module": "service-cartridge",
    "currentYaw": 45,
    "targetYaw": 225
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 下一步放置（h3-tracked-drill-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["foundation","mast","primary-boom","tool-head"]
- B：["foundation"]
- C：["control-cab","service-cartridge","track--1","track-1"]
- D：[]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head"
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
          -1.55,
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
          1.8499999999999999,
          0
        ],
        "anchorChild": [
          -2.2748883430420976,
          0.373595331183998,
          0
        ],
        "axis": [
          0,
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
        "type": "prismatic",
        "anchorParent": [
          3.5689670466381136,
          -0.3735953311839978,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
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
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
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
    ],
    "modules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "track--1",
      "track-1"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 库存核算（h3-tracked-drill-inventory）

备件库有 7 件，替换模块需 4 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：2
- B：6
- C：3
- D：4

```json
{
  "input": {
    "available": 7,
    "required": 4
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 子装配边界（h3-tracked-drill-boundary）

隔离 service-cartridge 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：[]
- B：["mast-joint","primary-boom-joint","tool-head-joint","control-cab-joint","service-cartridge-joint","track--1-joint","track-1-joint"]
- C：["primary-boom-joint"]
- D：["service-cartridge-joint"]

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
          -1.55,
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
          1.8499999999999999,
          0
        ],
        "anchorChild": [
          -2.2748883430420976,
          0.373595331183998,
          0
        ],
        "axis": [
          0,
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
        "type": "prismatic",
        "anchorParent": [
          3.5689670466381136,
          -0.3735953311839978,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
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
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
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
    ],
    "target": "service-cartridge"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 最小干预（h3-tracked-drill-no-op）

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

### 全过程依赖（h3-tracked-drill-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：0
- B：-1
- C：1
- D：7

```json
{
  "input": {
    "order": [
      "track--1",
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "track-1"
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
          -1.55,
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
          1.8499999999999999,
          0
        ],
        "anchorChild": [
          -2.2748883430420976,
          0.373595331183998,
          0
        ],
        "axis": [
          0,
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
        "type": "prismatic",
        "anchorParent": [
          3.5689670466381136,
          -0.3735953311839978,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
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
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
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
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 连续维修路径（h3-tracked-drill-access）

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
          9.093855389680211,
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
          8.536557868042284,
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
          8.4
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
        "clear": false,
        "timeOfImpact": 0.37211543321609497
      }
    ],
    "simulator": "stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration"
  },
  "answer": {
    "choiceIds": [
      "A",
      "C"
    ]
  }
}
```

### 支撑反事实（h3-tracked-drill-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","track--1","track-1"]
- B：["primary-boom","tool-head"]
- C：["mast"]
- D：[]

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
          -1.55,
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
          1.8499999999999999,
          0
        ],
        "anchorChild": [
          -2.2748883430420976,
          0.373595331183998,
          0
        ],
        "axis": [
          0,
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
        "type": "prismatic",
        "anchorParent": [
          3.5689670466381136,
          -0.3735953311839978,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
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
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
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
    ],
    "modules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "track--1",
      "track-1"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 冲击响应读数（h3-tracked-drill-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.0005
- B：0.2005
- C：0
- D：1.0005

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0004604532108525891
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0003935256097966644
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0003294994199733185
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.00014111486193483185
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.000039372511214316635
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.000011837338391951567
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.000002913319923841938
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.000002913319923841938
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.000002913319923841938
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.000002913319923841938
      },
      {
        "time": 1,
        "displacement": 0.000002913319923841938
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.01594577935542277,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节限位推理（h3-tracked-drill-kinematic）

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

### 约束故障诊断（h3-tracked-drill-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：service-cartridge-joint
- B：mast-joint
- C：primary-boom-joint
- D：tool-head-joint

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
          -1.55,
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
          1.8499999999999999,
          0
        ],
        "anchorChild": [
          -2.2748883430420976,
          0.373595331183998,
          0
        ],
        "axis": [
          0,
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
        "type": "prismatic",
        "anchorParent": [
          3.5689670466381136,
          -0.3735953311839978,
          1.2
        ],
        "anchorChild": [
          0,
          0.8,
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
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
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
    ]
  },
  "answer": {
    "choiceIds": [
      "A"
    ]
  }
}
```

### 主动检查收益（h3-tracked-drill-information-gain）

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

### 不确定性与弃答（h3-tracked-drill-abstention）

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

### 观测后信念更新（h3-tracked-drill-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.25
- B：0.3333333333333333
- C：0.5
- D：0

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
      "positive",
      "negative",
      "negative",
      "positive"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 多目标工程权衡（h3-tracked-drill-pareto）

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
        "cost": 6,
        "stiffness": 6,
        "mass": 1.9
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 5,
        "mass": 1.8
      },
      {
        "id": "stock-2",
        "cost": 3,
        "stiffness": 7,
        "mass": 1.1
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 11,
        "mass": 1.5
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

### 依赖装配（h3-tracked-drill-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
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
        "id": "place:track--1",
        "label": "安装 track--1",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:track--1"
        ],
        "adds": [
          "present:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1",
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
        "id": "place:track-1",
        "label": "安装 track-1",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:track-1"
        ],
        "adds": [
          "present:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1",
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
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:mast",
      "present:primary-boom",
      "present:tool-head",
      "present:control-cab",
      "present:service-cartridge",
      "present:track--1",
      "present:track-1"
    ],
    "budget": 8,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:track--1",
      "place:control-cab",
      "place:track-1",
      "place:mast",
      "place:primary-boom",
      "place:tool-head",
      "place:service-cartridge"
    ]
  }
}
```

### 依赖拆解（h3-tracked-drill-disassembly）

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
      "present:track--1",
      "present:track-1"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "track--1",
      "track-1"
    ],
    "actions": [
      {
        "id": "remove:track--1",
        "label": "拆除 track--1",
        "requires": [
          "present:track--1"
        ],
        "forbids": [],
        "adds": [
          "removed:track--1"
        ],
        "deletes": [
          "present:track--1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track--1",
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
        "id": "remove:foundation",
        "label": "拆除 foundation",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:mast",
          "present:control-cab",
          "present:service-cartridge",
          "present:track--1",
          "present:track-1"
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
        "id": "remove:track-1",
        "label": "拆除 track-1",
        "requires": [
          "present:track-1"
        ],
        "forbids": [],
        "adds": [
          "removed:track-1"
        ],
        "deletes": [
          "present:track-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track-1",
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
        "id": "remove:control-cab",
        "label": "拆除 control-cab",
        "requires": [
          "present:control-cab"
        ],
        "forbids": [],
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
      }
    ],
    "goalFacts": [
      "removed:track-1",
      "removed:track--1",
      "removed:service-cartridge",
      "removed:control-cab",
      "removed:tool-head",
      "removed:primary-boom",
      "removed:mast",
      "removed:foundation"
    ],
    "budget": 8,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:track--1",
      "remove:track-1",
      "remove:service-cartridge",
      "remove:control-cab",
      "remove:tool-head",
      "remove:primary-boom",
      "remove:mast",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-tracked-drill-service-repair）

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
      "track--1",
      "track-1"
    ],
    "actions": [
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

### 复合编辑验证（h3-tracked-drill-compound-edit）

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
      "track--1",
      "track-1"
    ],
    "actions": [
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

### 跨区域联合维修（h3-tracked-drill-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:track--1",
      "closed:track--1",
      "fault:track-1",
      "closed:track-1"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "track--1",
      "track-1"
    ],
    "actions": [
      {
        "id": "open:track--1",
        "label": "open track--1",
        "requires": [
          "done:support:track--1"
        ],
        "forbids": [
          "done:open:track--1"
        ],
        "adds": [
          "done:open:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "support:track-1",
        "label": "support track-1",
        "requires": [
          "fault:track-1"
        ],
        "forbids": [
          "done:support:track-1"
        ],
        "adds": [
          "done:support:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "open:track-1",
        "label": "open track-1",
        "requires": [
          "done:support:track-1"
        ],
        "forbids": [
          "done:open:track-1"
        ],
        "adds": [
          "done:open:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "remove:track--1",
        "label": "remove track--1",
        "requires": [
          "done:open:track--1"
        ],
        "forbids": [
          "done:remove:track--1"
        ],
        "adds": [
          "done:remove:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1",
          "visible": false
        }
      },
      {
        "id": "replace:track--1",
        "label": "replace track--1",
        "requires": [
          "done:remove:track--1"
        ],
        "forbids": [
          "done:replace:track--1"
        ],
        "adds": [
          "done:replace:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1",
          "visible": true
        }
      },
      {
        "id": "close:track-1",
        "label": "close track-1",
        "requires": [
          "done:verify:track-1"
        ],
        "forbids": [
          "done:close:track-1"
        ],
        "adds": [
          "done:close:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "replace:track-1",
        "label": "replace track-1",
        "requires": [
          "done:remove:track-1"
        ],
        "forbids": [
          "done:replace:track-1"
        ],
        "adds": [
          "done:replace:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1",
          "visible": true
        }
      },
      {
        "id": "remove:track-1",
        "label": "remove track-1",
        "requires": [
          "done:open:track-1"
        ],
        "forbids": [
          "done:remove:track-1"
        ],
        "adds": [
          "done:remove:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1",
          "visible": false
        }
      },
      {
        "id": "release:track-1",
        "label": "release track-1",
        "requires": [
          "done:close:track-1"
        ],
        "forbids": [
          "done:release:track-1"
        ],
        "adds": [
          "done:release:track-1",
          "repaired:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "verify:track--1",
        "label": "verify track--1",
        "requires": [
          "done:replace:track--1"
        ],
        "forbids": [
          "done:verify:track--1"
        ],
        "adds": [
          "done:verify:track--1"
        ],
        "deletes": [
          "fault:track--1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "support:track--1",
        "label": "support track--1",
        "requires": [
          "fault:track--1"
        ],
        "forbids": [
          "done:support:track--1"
        ],
        "adds": [
          "done:support:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "release:track--1",
        "label": "release track--1",
        "requires": [
          "done:close:track--1"
        ],
        "forbids": [
          "done:release:track--1"
        ],
        "adds": [
          "done:release:track--1",
          "repaired:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "verify:track-1",
        "label": "verify track-1",
        "requires": [
          "done:replace:track-1"
        ],
        "forbids": [
          "done:verify:track-1"
        ],
        "adds": [
          "done:verify:track-1"
        ],
        "deletes": [
          "fault:track-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "close:track--1",
        "label": "close track--1",
        "requires": [
          "done:verify:track--1"
        ],
        "forbids": [
          "done:close:track--1"
        ],
        "adds": [
          "done:close:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      }
    ],
    "goalFacts": [
      "repaired:track--1",
      "repaired:track-1"
    ],
    "budget": 14,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:track-1",
      "open:track-1",
      "remove:track-1",
      "replace:track-1",
      "support:track--1",
      "open:track--1",
      "remove:track--1",
      "replace:track--1",
      "verify:track--1",
      "verify:track-1",
      "close:track-1",
      "release:track-1",
      "close:track--1",
      "release:track--1"
    ]
  }
}
```

### 多工位资源调度（h3-tracked-drill-scheduling）

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
      }
    ],
    "deadline": 9
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 3,
      "job-4": 4,
      "job-5": 6
    }
  }
}
```

### 检查后条件策略（h3-tracked-drill-policy）

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

### 局部坐标变换（h3-tracked-drill-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[2.5,0.8,-2.5]
- B：[2.5,1.8,-1.5]
- C：[1.5,0.8,-2.5]
- D：[0.5,-0.05,-0.5]

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
      0.7071067811865475,
      0,
      0.7071067811865476
    ],
    "translation": [
      2,
      0.8500000000000001,
      -2
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-tracked-drill-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[0,0]
- B：[3,7]
- C：[7,3]
- D：[3,4]

```json
{
  "input": {
    "view": "front",
    "point": [
      3,
      7,
      -4
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 空间相对关系（h3-tracked-drill-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：less
- B：greater
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
      "id": "track-1",
      "position": [
        -0.050000000000000266,
        0.7,
        4
      ]
    },
    "axis": "x"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 约束自由度（h3-tracked-drill-joint-axis）

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
      "id": "track--1-joint",
      "name": "track--1 interface",
      "parent": "foundation",
      "child": "track--1",
      "type": "revolute",
      "anchorParent": [
        0,
        0.25,
        -4
      ],
      "anchorChild": [
        0.050000000000000266,
        -0.10000000000000003,
        0
      ],
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

### 维修间隙预算（h3-tracked-drill-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "service-cartridge",
    "aperture": 0.49,
    "toolWidth": 0.45,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-tracked-drill-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,10]
- B：[0,0,0]
- C：[0,-2,0]
- D：[0,0,-10]

```json
{
  "input": {
    "module": "service-cartridge",
    "lever": [
      2,
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
    "choiceId": "D"
  }
}
```

### 非均匀先验更新（h3-tracked-drill-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0
- B：1
- C：0.5555555555555556
- D：0.4166666666666667

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
      4,
      5,
      3
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

### 风险最小决策（h3-tracked-drill-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.2,
    "repairCost": 6,
    "failureLoss": 10,
    "module": "service-cartridge"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-tracked-drill-trace-threshold）

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
        "displacement": 0.0004604532108525891
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0003935256097966644
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0003294994199733185
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.00014111486193483185
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.000039372511214316635
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.000011837338391951567
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.000002913319923841938
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.000002913319923841938
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.000002913319923841938
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.000002913319923841938
      },
      {
        "time": 1,
        "displacement": 0.000002913319923841938
      }
    ],
    "threshold": 0.000552543853023107
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-tracked-drill-guarded-repair）

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
      "track--1",
      "track-1"
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

### 失败状态回退（h3-tracked-drill-rollback）

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
      "track--1",
      "track-1"
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

### 共享工具协同维修（h3-tracked-drill-resource-repair）

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
        "id": "release:track-1",
        "label": "release track-1",
        "requires": [
          "done:relock:track-1"
        ],
        "forbids": [
          "done:release:track-1"
        ],
        "adds": [
          "done:release:track-1",
          "ready:track-1",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "relock:track-1",
        "label": "relock track-1",
        "requires": [
          "done:verify:track-1"
        ],
        "forbids": [
          "done:relock:track-1"
        ],
        "adds": [
          "done:relock:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "verify:track-1",
        "label": "verify track-1",
        "requires": [
          "done:replace:track-1"
        ],
        "forbids": [
          "done:verify:track-1"
        ],
        "adds": [
          "done:verify:track-1"
        ],
        "deletes": [
          "fault:track-1",
          "misaligned:track-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "replace:track-1",
        "label": "replace track-1",
        "requires": [
          "done:unlock:track-1"
        ],
        "forbids": [
          "done:replace:track-1"
        ],
        "adds": [
          "done:replace:track-1"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "unlock:track-1",
        "label": "unlock track-1",
        "requires": [
          "done:support:track-1"
        ],
        "forbids": [
          "done:unlock:track-1"
        ],
        "adds": [
          "done:unlock:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "support:track-1",
        "label": "support track-1",
        "requires": [
          "done:isolate:track-1"
        ],
        "forbids": [
          "done:support:track-1"
        ],
        "adds": [
          "done:support:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "isolate:track-1",
        "label": "isolate track-1",
        "requires": [
          "tool:free",
          "fault:track-1"
        ],
        "forbids": [
          "done:isolate:track-1"
        ],
        "adds": [
          "done:isolate:track-1"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "release:track--1",
        "label": "release track--1",
        "requires": [
          "done:relock:track--1"
        ],
        "forbids": [
          "done:release:track--1"
        ],
        "adds": [
          "done:release:track--1",
          "ready:track--1",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "relock:track--1",
        "label": "relock track--1",
        "requires": [
          "done:verify:track--1"
        ],
        "forbids": [
          "done:relock:track--1"
        ],
        "adds": [
          "done:relock:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "verify:track--1",
        "label": "verify track--1",
        "requires": [
          "done:replace:track--1"
        ],
        "forbids": [
          "done:verify:track--1"
        ],
        "adds": [
          "done:verify:track--1"
        ],
        "deletes": [
          "fault:track--1",
          "misaligned:track--1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "replace:track--1",
        "label": "replace track--1",
        "requires": [
          "done:unlock:track--1"
        ],
        "forbids": [
          "done:replace:track--1"
        ],
        "adds": [
          "done:replace:track--1"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "unlock:track--1",
        "label": "unlock track--1",
        "requires": [
          "done:support:track--1"
        ],
        "forbids": [
          "done:unlock:track--1"
        ],
        "adds": [
          "done:unlock:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "support:track--1",
        "label": "support track--1",
        "requires": [
          "done:isolate:track--1"
        ],
        "forbids": [
          "done:support:track--1"
        ],
        "adds": [
          "done:support:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "isolate:track--1",
        "label": "isolate track--1",
        "requires": [
          "tool:free",
          "fault:track--1"
        ],
        "forbids": [
          "done:isolate:track--1"
        ],
        "adds": [
          "done:isolate:track--1"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
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
      "fault:service-cartridge",
      "fault:track--1",
      "fault:track-1"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "track--1",
      "track-1"
    ],
    "goalFacts": [
      "ready:service-cartridge",
      "ready:track--1",
      "ready:track-1"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 24
  },
  "answer": {
    "actionIds": [
      "isolate:track-1",
      "support:track-1",
      "unlock:track-1",
      "replace:track-1",
      "verify:track-1",
      "relock:track-1",
      "release:track-1",
      "isolate:track--1",
      "support:track--1",
      "unlock:track--1",
      "replace:track--1",
      "verify:track--1",
      "relock:track--1",
      "release:track--1",
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

### 预算约束检查策略（h3-tracked-drill-budget-policy）

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
