## D3 缆索巡检机器人

### 模块识别（h3-cable-inspection-robot-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：service-cartridge
- B：foundation
- C：mast
- D：primary-boom

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
        "id": "cable-roller--2.5",
        "name": "cable roller  2.5"
      },
      {
        "id": "cable-roller-2.5",
        "name": "cable roller 2.5"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 部件计数（h3-cable-inspection-robot-count）

模块 service-cartridge 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：5
- B：3
- C：7
- D：4

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
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p56",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p57",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p58",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p59",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p60",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p61",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p62",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p63",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p64",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p65",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p66",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p67",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "mast-p68",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "mast-p69",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "primary-boom-p70",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p71",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p72",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p73",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p74",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p75",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p76",
        "moduleId": "primary-boom",
        "shape": "gear",
        "color": "#273e50"
      },
      {
        "id": "tool-head-p77",
        "moduleId": "tool-head",
        "shape": "gear",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p78",
        "moduleId": "tool-head",
        "shape": "axle",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p79",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p80",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p81",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p82",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p83",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p84",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p85",
        "moduleId": "control-cab",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "control-cab-p86",
        "moduleId": "control-cab",
        "shape": "slope",
        "color": "#387bb3"
      },
      {
        "id": "service-cartridge-p87",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p88",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p89",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p90",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "secondary-boom-p91",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p92",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p93",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p94",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p95",
        "moduleId": "secondary-boom",
        "shape": "gear",
        "color": "#273e50"
      },
      {
        "id": "clamp-p96",
        "moduleId": "clamp",
        "shape": "arch",
        "color": "#e9ad37"
      },
      {
        "id": "sliding-tray-p97",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p98",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p99",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p100",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p101",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p102",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p103",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p104",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cable-roller--2.5-p105",
        "moduleId": "cable-roller--2.5",
        "shape": "wheel",
        "color": "#dc6040"
      },
      {
        "id": "cable-roller--2.5-p106",
        "moduleId": "cable-roller--2.5",
        "shape": "axle",
        "color": "#273e50"
      },
      {
        "id": "cable-roller-2.5-p107",
        "moduleId": "cable-roller-2.5",
        "shape": "wheel",
        "color": "#dc6040"
      },
      {
        "id": "cable-roller-2.5-p108",
        "moduleId": "cable-roller-2.5",
        "shape": "axle",
        "color": "#273e50"
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 颜色识别（h3-cable-inspection-robot-color）

零件 service-cartridge-p87 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#d43a32
- B：#f2bf3c
- C：#dc6040
- D：#2878b8

```json
{
  "input": {
    "part": {
      "id": "service-cartridge-p87",
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

### 三维位置（h3-cable-inspection-robot-position）

模块 service-cartridge 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[-1.6,3.3499999999999996,-0.6000000000000001]
- B：[1.1820049954185017,6.399500249940485,-0.6]
- C：[2,0.8500000000000001,-2]
- D：[0,0.35,0]

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
        3.3499999999999996,
        -0.6000000000000001
      ],
      "primary-boom": [
        1.1820049954185017,
        6.399500249940485,
        -0.6
      ],
      "tool-head": [
        4.370024991668155,
        5.8990004998809695,
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
        2.072131002778001,
        3.7912592304699557,
        4
      ],
      "clamp": [
        1.1354126538114302,
        5.637189707302727,
        4.8
      ],
      "sliding-tray": [
        0,
        1.85,
        3.9000000000000004
      ],
      "cable-roller--2.5": [
        0,
        7,
        -2.5
      ],
      "cable-roller-2.5": [
        0,
        7,
        2.5
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节类型（h3-cable-inspection-robot-joint-type）

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
        2.75,
        0
      ],
      "anchorChild": [
        -2.7820049954185015,
        -0.29950024994048446,
        0
      ],
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

### 直接连接（h3-cable-inspection-robot-parent）

service-cartridge 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray","cable-roller--2.5","cable-roller-2.5"]
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
          -2.45,
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
          2.75,
          0
        ],
        "anchorChild": [
          -2.7820049954185015,
          -0.29950024994048446,
          0
        ],
        "axis": [
          0,
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
          3.1880199962496527,
          0.29950024994048435,
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
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
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
          -0.9367183489665709,
          1.8459304768327705,
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
        "id": "cable-roller--2.5-joint",
        "name": "cable-roller--2.5 interface",
        "parent": "mast",
        "child": "cable-roller--2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          -1.9
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
        "id": "cable-roller-2.5-joint",
        "name": "cable-roller-2.5 interface",
        "parent": "mast",
        "child": "cable-roller-2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          3.1
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
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 基座识别（h3-cable-inspection-robot-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["service-cartridge"]
- B：["foundation"]
- C：[]
- D：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray","cable-roller--2.5","cable-roller-2.5"]

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
          3.35,
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
          1.1820049954185015,
          6.399500249940485,
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
          4.370024991668155,
          5.8990004998809695,
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
          2.072131002778001,
          3.791259230469956,
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
          1.1354126538114302,
          5.637189707302727,
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
        "id": "cable-roller--2.5",
        "name": "cable roller  2.5",
        "role": "traction",
        "position": [
          0,
          7,
          -2.5
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
        "id": "cable-roller-2.5",
        "name": "cable roller 2.5",
        "role": "traction",
        "position": [
          0,
          7,
          2.5
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

### 接口计数（h3-cable-inspection-robot-degree）

service-cartridge 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：0
- D：3

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
          -2.45,
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
          2.75,
          0
        ],
        "anchorChild": [
          -2.7820049954185015,
          -0.29950024994048446,
          0
        ],
        "axis": [
          0,
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
          3.1880199962496527,
          0.29950024994048435,
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
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
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
          -0.9367183489665709,
          1.8459304768327705,
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
        "id": "cable-roller--2.5-joint",
        "name": "cable-roller--2.5 interface",
        "parent": "mast",
        "child": "cable-roller--2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          -1.9
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
        "id": "cable-roller-2.5-joint",
        "name": "cable-roller-2.5 interface",
        "parent": "mast",
        "child": "cable-roller-2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          3.1
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
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 局部改色（h3-cable-inspection-robot-recolor）

仅将 service-cartridge-p87 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"service-cartridge-p87","color":"#2878b8"}
- B：{"id":"*","color":"#e8792e"}
- C：{"id":"service-cartridge-p87","color":"#e8792e"}
- D：{"id":"service-cartridge-p88","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "service-cartridge-p87",
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

### 补装部件（h3-cable-inspection-robot-add）

模块 service-cartridge 缺失零件 service-cartridge-p87。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"service-cartridge-p87","moduleId":"foundation","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#dc6040","rotation":[0,0,0,1]}
- B：{"id":"service-cartridge-p87","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[3,3,3],"color":"#dc6040","rotation":[0,0,0,1]}
- C：{"id":"service-cartridge-p87","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#000000","rotation":[0,0,0,1]}
- D：{"id":"service-cartridge-p87","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#dc6040","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "service-cartridge-p87",
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
      "mast-p57",
      "mast-p58",
      "mast-p59",
      "mast-p60",
      "mast-p61",
      "mast-p62",
      "mast-p63",
      "mast-p64",
      "mast-p65",
      "mast-p66",
      "mast-p67",
      "mast-p68",
      "mast-p69",
      "primary-boom-p70",
      "primary-boom-p71",
      "primary-boom-p72",
      "primary-boom-p73",
      "primary-boom-p74",
      "primary-boom-p75",
      "primary-boom-p76",
      "tool-head-p77",
      "tool-head-p78",
      "control-cab-p79",
      "control-cab-p80",
      "control-cab-p81",
      "control-cab-p82",
      "control-cab-p83",
      "control-cab-p84",
      "control-cab-p85",
      "control-cab-p86",
      "service-cartridge-p88",
      "service-cartridge-p89",
      "service-cartridge-p90",
      "secondary-boom-p91",
      "secondary-boom-p92",
      "secondary-boom-p93",
      "secondary-boom-p94",
      "secondary-boom-p95",
      "clamp-p96",
      "sliding-tray-p97",
      "sliding-tray-p98",
      "sliding-tray-p99",
      "sliding-tray-p100",
      "sliding-tray-p101",
      "sliding-tray-p102",
      "sliding-tray-p103",
      "sliding-tray-p104",
      "cable-roller--2.5-p105",
      "cable-roller--2.5-p106",
      "cable-roller-2.5-p107",
      "cable-roller-2.5-p108"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 安全拆除（h3-cable-inspection-robot-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray","cable-roller--2.5","cable-roller-2.5"]
- C：["cable-roller--2.5","cable-roller-2.5","clamp","service-cartridge","sliding-tray","tool-head"]
- D：["foundation"]

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
          -2.45,
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
          2.75,
          0
        ],
        "anchorChild": [
          -2.7820049954185015,
          -0.29950024994048446,
          0
        ],
        "axis": [
          0,
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
          3.1880199962496527,
          0.29950024994048435,
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
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
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
          -0.9367183489665709,
          1.8459304768327705,
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
        "id": "cable-roller--2.5-joint",
        "name": "cable-roller--2.5 interface",
        "parent": "mast",
        "child": "cable-roller--2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          -1.9
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
        "id": "cable-roller-2.5-joint",
        "name": "cable-roller-2.5 interface",
        "parent": "mast",
        "child": "cable-roller-2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          3.1
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
      "cable-roller--2.5",
      "cable-roller-2.5"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 替换选择（h3-cable-inspection-robot-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

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
        "cost": 5,
        "stiffness": 5,
        "mass": 0.7
      },
      {
        "id": "stock-1",
        "cost": 4,
        "stiffness": 9,
        "mass": 1.8
      },
      {
        "id": "stock-2",
        "cost": 3,
        "stiffness": 9,
        "mass": 1.7
      },
      {
        "id": "stock-3",
        "cost": 2,
        "stiffness": 8,
        "mass": 0.8
      }
    ],
    "maxCost": 8
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 平移纠偏（h3-cable-inspection-robot-translate）

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
    "target": "service-cartridge"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 姿态纠偏（h3-cable-inspection-robot-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：0
- B：90
- C：-135
- D：135

```json
{
  "input": {
    "module": "service-cartridge",
    "currentYaw": 135,
    "targetYaw": 0
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 下一步放置（h3-cable-inspection-robot-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge"]
- C：["secondary-boom","clamp","sliding-tray","cable-roller--2.5","cable-roller-2.5"]
- D：["cable-roller--2.5","cable-roller-2.5","secondary-boom","sliding-tray"]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge"
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
          -2.45,
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
          2.75,
          0
        ],
        "anchorChild": [
          -2.7820049954185015,
          -0.29950024994048446,
          0
        ],
        "axis": [
          0,
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
          3.1880199962496527,
          0.29950024994048435,
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
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
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
          -0.9367183489665709,
          1.8459304768327705,
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
        "id": "cable-roller--2.5-joint",
        "name": "cable-roller--2.5 interface",
        "parent": "mast",
        "child": "cable-roller--2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          -1.9
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
        "id": "cable-roller-2.5-joint",
        "name": "cable-roller-2.5 interface",
        "parent": "mast",
        "child": "cable-roller-2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          3.1
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
      "cable-roller--2.5",
      "cable-roller-2.5"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 库存核算（h3-cable-inspection-robot-inventory）

备件库有 6 件，替换模块需 4 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：5
- B：2
- C：3
- D：1

```json
{
  "input": {
    "available": 6,
    "required": 4
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 子装配边界（h3-cable-inspection-robot-boundary）

隔离 service-cartridge 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：[]
- B：["mast-joint","primary-boom-joint","tool-head-joint","control-cab-joint","service-cartridge-joint","secondary-boom-joint","clamp-joint","sliding-tray-joint","cable-roller--2.5-joint","cable-roller-2.5-joint"]
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
          -2.45,
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
          2.75,
          0
        ],
        "anchorChild": [
          -2.7820049954185015,
          -0.29950024994048446,
          0
        ],
        "axis": [
          0,
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
          3.1880199962496527,
          0.29950024994048435,
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
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
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
          -0.9367183489665709,
          1.8459304768327705,
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
        "id": "cable-roller--2.5-joint",
        "name": "cable-roller--2.5 interface",
        "parent": "mast",
        "child": "cable-roller--2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          -1.9
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
        "id": "cable-roller-2.5-joint",
        "name": "cable-roller-2.5 interface",
        "parent": "mast",
        "child": "cable-roller-2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          3.1
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
      }
    ],
    "target": "service-cartridge"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 最小干预（h3-cable-inspection-robot-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：4
- D：0

```json
{
  "input": {
    "module": "service-cartridge"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 全过程依赖（h3-cable-inspection-robot-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：-1
- B：1
- C：10
- D：0

```json
{
  "input": {
    "order": [
      "sliding-tray",
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "cable-roller--2.5",
      "cable-roller-2.5"
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
          -2.45,
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
          2.75,
          0
        ],
        "anchorChild": [
          -2.7820049954185015,
          -0.29950024994048446,
          0
        ],
        "axis": [
          0,
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
          3.1880199962496527,
          0.29950024994048435,
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
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
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
          -0.9367183489665709,
          1.8459304768327705,
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
        "id": "cable-roller--2.5-joint",
        "name": "cable-roller--2.5 interface",
        "parent": "mast",
        "child": "cable-roller--2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          -1.9
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
        "id": "cable-roller-2.5-joint",
        "name": "cable-roller-2.5 interface",
        "parent": "mast",
        "child": "cable-roller-2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          3.1
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
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 连续维修路径（h3-cable-inspection-robot-access）

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
          9.220024991668154,
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
          12.5,
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
          9.3
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

### 支撑反事实（h3-cable-inspection-robot-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray","cable-roller--2.5","cable-roller-2.5"]
- B：["cable-roller--2.5","cable-roller-2.5","primary-boom","tool-head"]
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
          -2.45,
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
          2.75,
          0
        ],
        "anchorChild": [
          -2.7820049954185015,
          -0.29950024994048446,
          0
        ],
        "axis": [
          0,
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
          3.1880199962496527,
          0.29950024994048435,
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
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
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
          -0.9367183489665709,
          1.8459304768327705,
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
        "id": "cable-roller--2.5-joint",
        "name": "cable-roller--2.5 interface",
        "parent": "mast",
        "child": "cable-roller--2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          -1.9
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
        "id": "cable-roller-2.5-joint",
        "name": "cable-roller-2.5 interface",
        "parent": "mast",
        "child": "cable-roller-2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          3.1
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
      "cable-roller--2.5",
      "cable-roller-2.5"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 冲击响应读数（h3-cable-inspection-robot-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：1.0021
- C：0.0021
- D：0.2021

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0018228537298288002
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0020668262373495566
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0017097775042068026
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0006688458878030513
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0001366619605613628
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00007911961499191961
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00004461454445065515
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.000028777626194373853
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.000028777626194373853
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.000028777626194373853
      },
      {
        "time": 1,
        "displacement": 0.000028777626194373853
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.016720304155543507,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-cable-inspection-robot-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-0.8
- B：0
- C：-1.3
- D：1.3

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
      "A",
      "B"
    ]
  }
}
```

### 约束故障诊断（h3-cable-inspection-robot-diagnosis）

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
          -2.45,
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
          2.75,
          0
        ],
        "anchorChild": [
          -2.7820049954185015,
          -0.29950024994048446,
          0
        ],
        "axis": [
          0,
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
          3.1880199962496527,
          0.29950024994048435,
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
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
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
          -0.9367183489665709,
          1.8459304768327705,
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
        "id": "cable-roller--2.5-joint",
        "name": "cable-roller--2.5 interface",
        "parent": "mast",
        "child": "cable-roller--2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          -1.9
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
        "id": "cable-roller-2.5-joint",
        "name": "cable-roller-2.5 interface",
        "parent": "mast",
        "child": "cable-roller-2.5",
        "type": "revolute",
        "anchorParent": [
          1.6,
          3.6499999999999995,
          3.1
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

### 主动检查收益（h3-cable-inspection-robot-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-2
- B：query-1
- C：query-0

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
      "B"
    ]
  }
}
```

### 不确定性与弃答（h3-cable-inspection-robot-abstention）

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

### 观测后信念更新（h3-cable-inspection-robot-posterior）

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
      "positive",
      "positive",
      "negative",
      "positive"
    ],
    "observed": "positive"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 多目标工程权衡（h3-cable-inspection-robot-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-3
- B：stock-1
- C：stock-0
- D：stock-2

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 5,
        "stiffness": 5,
        "mass": 0.7
      },
      {
        "id": "stock-1",
        "cost": 4,
        "stiffness": 9,
        "mass": 1.8
      },
      {
        "id": "stock-2",
        "cost": 3,
        "stiffness": 9,
        "mass": 1.7
      },
      {
        "id": "stock-3",
        "cost": 2,
        "stiffness": 8,
        "mass": 0.8
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

### 依赖装配（h3-cable-inspection-robot-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
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
        "id": "place:cable-roller--2.5",
        "label": "安装 cable-roller--2.5",
        "requires": [
          "present:mast"
        ],
        "forbids": [
          "present:cable-roller--2.5"
        ],
        "adds": [
          "present:cable-roller--2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5",
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
        "id": "place:cable-roller-2.5",
        "label": "安装 cable-roller-2.5",
        "requires": [
          "present:mast"
        ],
        "forbids": [
          "present:cable-roller-2.5"
        ],
        "adds": [
          "present:cable-roller-2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5",
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
      "present:cable-roller--2.5",
      "present:cable-roller-2.5"
    ],
    "budget": 11,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:control-cab",
      "place:sliding-tray",
      "place:service-cartridge",
      "place:mast",
      "place:primary-boom",
      "place:tool-head",
      "place:secondary-boom",
      "place:cable-roller--2.5",
      "place:clamp",
      "place:cable-roller-2.5"
    ]
  }
}
```

### 依赖拆解（h3-cable-inspection-robot-disassembly）

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
      "present:cable-roller--2.5",
      "present:cable-roller-2.5"
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
      "cable-roller--2.5",
      "cable-roller-2.5"
    ],
    "actions": [
      {
        "id": "remove:mast",
        "label": "拆除 mast",
        "requires": [
          "present:mast"
        ],
        "forbids": [
          "present:primary-boom",
          "present:cable-roller--2.5",
          "present:cable-roller-2.5"
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
        "id": "remove:cable-roller--2.5",
        "label": "拆除 cable-roller--2.5",
        "requires": [
          "present:cable-roller--2.5"
        ],
        "forbids": [],
        "adds": [
          "removed:cable-roller--2.5"
        ],
        "deletes": [
          "present:cable-roller--2.5"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5",
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
        "id": "remove:cable-roller-2.5",
        "label": "拆除 cable-roller-2.5",
        "requires": [
          "present:cable-roller-2.5"
        ],
        "forbids": [],
        "adds": [
          "removed:cable-roller-2.5"
        ],
        "deletes": [
          "present:cable-roller-2.5"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5",
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
        "id": "remove:foundation",
        "label": "拆除 foundation",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:mast",
          "present:control-cab",
          "present:service-cartridge",
          "present:sliding-tray"
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
      }
    ],
    "goalFacts": [
      "removed:cable-roller-2.5",
      "removed:cable-roller--2.5",
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
    "budget": 11,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:cable-roller--2.5",
      "remove:cable-roller-2.5",
      "remove:service-cartridge",
      "remove:clamp",
      "remove:secondary-boom",
      "remove:control-cab",
      "remove:sliding-tray",
      "remove:tool-head",
      "remove:primary-boom",
      "remove:mast",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-cable-inspection-robot-service-repair）

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
      "cable-roller--2.5",
      "cable-roller-2.5"
    ],
    "actions": [
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

### 复合编辑验证（h3-cable-inspection-robot-compound-edit）

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
      "cable-roller--2.5",
      "cable-roller-2.5"
    ],
    "actions": [
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

### 跨区域联合维修（h3-cable-inspection-robot-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:sliding-tray",
      "closed:sliding-tray",
      "fault:cable-roller--2.5",
      "closed:cable-roller--2.5",
      "fault:cable-roller-2.5",
      "closed:cable-roller-2.5"
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
      "cable-roller--2.5",
      "cable-roller-2.5"
    ],
    "actions": [
      {
        "id": "close:cable-roller--2.5",
        "label": "close cable-roller--2.5",
        "requires": [
          "done:verify:cable-roller--2.5"
        ],
        "forbids": [
          "done:close:cable-roller--2.5"
        ],
        "adds": [
          "done:close:cable-roller--2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5"
        }
      },
      {
        "id": "release:cable-roller--2.5",
        "label": "release cable-roller--2.5",
        "requires": [
          "done:close:cable-roller--2.5"
        ],
        "forbids": [
          "done:release:cable-roller--2.5"
        ],
        "adds": [
          "done:release:cable-roller--2.5",
          "repaired:cable-roller--2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5"
        }
      },
      {
        "id": "remove:cable-roller--2.5",
        "label": "remove cable-roller--2.5",
        "requires": [
          "done:open:cable-roller--2.5"
        ],
        "forbids": [
          "done:remove:cable-roller--2.5"
        ],
        "adds": [
          "done:remove:cable-roller--2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5",
          "visible": false
        }
      },
      {
        "id": "replace:cable-roller-2.5",
        "label": "replace cable-roller-2.5",
        "requires": [
          "done:remove:cable-roller-2.5"
        ],
        "forbids": [
          "done:replace:cable-roller-2.5"
        ],
        "adds": [
          "done:replace:cable-roller-2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5",
          "visible": true
        }
      },
      {
        "id": "verify:cable-roller--2.5",
        "label": "verify cable-roller--2.5",
        "requires": [
          "done:replace:cable-roller--2.5"
        ],
        "forbids": [
          "done:verify:cable-roller--2.5"
        ],
        "adds": [
          "done:verify:cable-roller--2.5"
        ],
        "deletes": [
          "fault:cable-roller--2.5"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5"
        }
      },
      {
        "id": "remove:cable-roller-2.5",
        "label": "remove cable-roller-2.5",
        "requires": [
          "done:open:cable-roller-2.5"
        ],
        "forbids": [
          "done:remove:cable-roller-2.5"
        ],
        "adds": [
          "done:remove:cable-roller-2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5",
          "visible": false
        }
      },
      {
        "id": "verify:sliding-tray",
        "label": "verify sliding-tray",
        "requires": [
          "done:replace:sliding-tray"
        ],
        "forbids": [
          "done:verify:sliding-tray"
        ],
        "adds": [
          "done:verify:sliding-tray"
        ],
        "deletes": [
          "fault:sliding-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "replace:sliding-tray",
        "label": "replace sliding-tray",
        "requires": [
          "done:remove:sliding-tray"
        ],
        "forbids": [
          "done:replace:sliding-tray"
        ],
        "adds": [
          "done:replace:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray",
          "visible": true
        }
      },
      {
        "id": "close:cable-roller-2.5",
        "label": "close cable-roller-2.5",
        "requires": [
          "done:verify:cable-roller-2.5"
        ],
        "forbids": [
          "done:close:cable-roller-2.5"
        ],
        "adds": [
          "done:close:cable-roller-2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5"
        }
      },
      {
        "id": "support:sliding-tray",
        "label": "support sliding-tray",
        "requires": [
          "fault:sliding-tray"
        ],
        "forbids": [
          "done:support:sliding-tray"
        ],
        "adds": [
          "done:support:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "replace:cable-roller--2.5",
        "label": "replace cable-roller--2.5",
        "requires": [
          "done:remove:cable-roller--2.5"
        ],
        "forbids": [
          "done:replace:cable-roller--2.5"
        ],
        "adds": [
          "done:replace:cable-roller--2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5",
          "visible": true
        }
      },
      {
        "id": "open:sliding-tray",
        "label": "open sliding-tray",
        "requires": [
          "done:support:sliding-tray"
        ],
        "forbids": [
          "done:open:sliding-tray"
        ],
        "adds": [
          "done:open:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "close:sliding-tray",
        "label": "close sliding-tray",
        "requires": [
          "done:verify:sliding-tray"
        ],
        "forbids": [
          "done:close:sliding-tray"
        ],
        "adds": [
          "done:close:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "support:cable-roller--2.5",
        "label": "support cable-roller--2.5",
        "requires": [
          "fault:cable-roller--2.5"
        ],
        "forbids": [
          "done:support:cable-roller--2.5"
        ],
        "adds": [
          "done:support:cable-roller--2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5"
        }
      },
      {
        "id": "release:cable-roller-2.5",
        "label": "release cable-roller-2.5",
        "requires": [
          "done:close:cable-roller-2.5"
        ],
        "forbids": [
          "done:release:cable-roller-2.5"
        ],
        "adds": [
          "done:release:cable-roller-2.5",
          "repaired:cable-roller-2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5"
        }
      },
      {
        "id": "remove:sliding-tray",
        "label": "remove sliding-tray",
        "requires": [
          "done:open:sliding-tray"
        ],
        "forbids": [
          "done:remove:sliding-tray"
        ],
        "adds": [
          "done:remove:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray",
          "visible": false
        }
      },
      {
        "id": "open:cable-roller-2.5",
        "label": "open cable-roller-2.5",
        "requires": [
          "done:support:cable-roller-2.5"
        ],
        "forbids": [
          "done:open:cable-roller-2.5"
        ],
        "adds": [
          "done:open:cable-roller-2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5"
        }
      },
      {
        "id": "open:cable-roller--2.5",
        "label": "open cable-roller--2.5",
        "requires": [
          "done:support:cable-roller--2.5"
        ],
        "forbids": [
          "done:open:cable-roller--2.5"
        ],
        "adds": [
          "done:open:cable-roller--2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5"
        }
      },
      {
        "id": "release:sliding-tray",
        "label": "release sliding-tray",
        "requires": [
          "done:close:sliding-tray"
        ],
        "forbids": [
          "done:release:sliding-tray"
        ],
        "adds": [
          "done:release:sliding-tray",
          "repaired:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "verify:cable-roller-2.5",
        "label": "verify cable-roller-2.5",
        "requires": [
          "done:replace:cable-roller-2.5"
        ],
        "forbids": [
          "done:verify:cable-roller-2.5"
        ],
        "adds": [
          "done:verify:cable-roller-2.5"
        ],
        "deletes": [
          "fault:cable-roller-2.5"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5"
        }
      },
      {
        "id": "support:cable-roller-2.5",
        "label": "support cable-roller-2.5",
        "requires": [
          "fault:cable-roller-2.5"
        ],
        "forbids": [
          "done:support:cable-roller-2.5"
        ],
        "adds": [
          "done:support:cable-roller-2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5"
        }
      }
    ],
    "goalFacts": [
      "repaired:sliding-tray",
      "repaired:cable-roller--2.5",
      "repaired:cable-roller-2.5"
    ],
    "budget": 21,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:sliding-tray",
      "open:sliding-tray",
      "support:cable-roller--2.5",
      "remove:sliding-tray",
      "replace:sliding-tray",
      "verify:sliding-tray",
      "close:sliding-tray",
      "open:cable-roller--2.5",
      "remove:cable-roller--2.5",
      "replace:cable-roller--2.5",
      "verify:cable-roller--2.5",
      "close:cable-roller--2.5",
      "release:cable-roller--2.5",
      "release:sliding-tray",
      "support:cable-roller-2.5",
      "open:cable-roller-2.5",
      "remove:cable-roller-2.5",
      "replace:cable-roller-2.5",
      "verify:cable-roller-2.5",
      "close:cable-roller-2.5",
      "release:cable-roller-2.5"
    ]
  }
}
```

### 多工位资源调度（h3-cable-inspection-robot-scheduling）

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
      }
    ],
    "deadline": 10
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
      "job-7": 9
    }
  }
}
```

### 检查后条件策略（h3-cable-inspection-robot-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "service-cartridge",
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

### 局部坐标变换（h3-cable-inspection-robot-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[0.5,-0.05,-0.5]
- B：[2.5,0.8,-2.5]
- C：[3.5,1.8,-0.5]
- D：[2.5,0.8,-1.5]

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
      0.7071067811865476,
      0,
      -0.7071067811865475
    ],
    "translation": [
      2,
      0.8500000000000001,
      -2
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 正交视图投影（h3-cable-inspection-robot-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[9,4]
- B：[4,5]
- C：[0,0]
- D：[4,-5]

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
    "choiceId": "D"
  }
}
```

### 空间相对关系（h3-cable-inspection-robot-relative-order）

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
        0.35,
        0
      ]
    },
    "B": {
      "id": "cable-roller-2.5",
      "position": [
        0,
        7,
        2.5
      ]
    },
    "axis": "z"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 约束自由度（h3-cable-inspection-robot-joint-axis）

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
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 维修间隙预算（h3-cable-inspection-robot-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "service-cartridge",
    "aperture": 0.81,
    "toolWidth": 0.55,
    "eachSideMargin": 0.1
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-cable-inspection-robot-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,12]
- B：[0,0,0]
- C：[0,-3,0]
- D：[0,0,-12]

```json
{
  "input": {
    "module": "service-cartridge",
    "lever": [
      3,
      3,
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

### 非均匀先验更新（h3-cable-inspection-robot-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.5714285714285714
- B：0.36363636363636365
- C：0
- D：1

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
      4,
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

### 风险最小决策（h3-cable-inspection-robot-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.4,
    "repairCost": 2,
    "failureLoss": 13,
    "module": "service-cartridge"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-cable-inspection-robot-trace-threshold）

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
        "displacement": 0.0018228537298288002
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0020668262373495566
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0017097775042068026
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0006688458878030513
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0001366619605613628
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00007911961499191961
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00004461454445065515
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.000028777626194373853
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.000028777626194373853
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.000028777626194373853
      },
      {
        "time": 1,
        "displacement": 0.000028777626194373853
      }
    ],
    "threshold": 0.0024801914848194676
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-cable-inspection-robot-guarded-repair）

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
      "cable-roller--2.5",
      "cable-roller-2.5"
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

### 失败状态回退（h3-cable-inspection-robot-rollback）

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
      "cable-roller--2.5",
      "cable-roller-2.5"
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

### 共享工具协同维修（h3-cable-inspection-robot-resource-repair）

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
        "id": "release:cable-roller-2.5",
        "label": "release cable-roller-2.5",
        "requires": [
          "done:relock:cable-roller-2.5"
        ],
        "forbids": [
          "done:release:cable-roller-2.5"
        ],
        "adds": [
          "done:release:cable-roller-2.5",
          "ready:cable-roller-2.5",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5"
        }
      },
      {
        "id": "relock:cable-roller-2.5",
        "label": "relock cable-roller-2.5",
        "requires": [
          "done:verify:cable-roller-2.5"
        ],
        "forbids": [
          "done:relock:cable-roller-2.5"
        ],
        "adds": [
          "done:relock:cable-roller-2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5"
        }
      },
      {
        "id": "verify:cable-roller-2.5",
        "label": "verify cable-roller-2.5",
        "requires": [
          "done:replace:cable-roller-2.5"
        ],
        "forbids": [
          "done:verify:cable-roller-2.5"
        ],
        "adds": [
          "done:verify:cable-roller-2.5"
        ],
        "deletes": [
          "fault:cable-roller-2.5",
          "misaligned:cable-roller-2.5"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5"
        }
      },
      {
        "id": "replace:cable-roller-2.5",
        "label": "replace cable-roller-2.5",
        "requires": [
          "done:unlock:cable-roller-2.5"
        ],
        "forbids": [
          "done:replace:cable-roller-2.5"
        ],
        "adds": [
          "done:replace:cable-roller-2.5"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cable-roller-2.5"
        }
      },
      {
        "id": "unlock:cable-roller-2.5",
        "label": "unlock cable-roller-2.5",
        "requires": [
          "done:support:cable-roller-2.5"
        ],
        "forbids": [
          "done:unlock:cable-roller-2.5"
        ],
        "adds": [
          "done:unlock:cable-roller-2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5"
        }
      },
      {
        "id": "support:cable-roller-2.5",
        "label": "support cable-roller-2.5",
        "requires": [
          "done:isolate:cable-roller-2.5"
        ],
        "forbids": [
          "done:support:cable-roller-2.5"
        ],
        "adds": [
          "done:support:cable-roller-2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5"
        }
      },
      {
        "id": "isolate:cable-roller-2.5",
        "label": "isolate cable-roller-2.5",
        "requires": [
          "tool:free",
          "fault:cable-roller-2.5"
        ],
        "forbids": [
          "done:isolate:cable-roller-2.5"
        ],
        "adds": [
          "done:isolate:cable-roller-2.5"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller-2.5"
        }
      },
      {
        "id": "release:cable-roller--2.5",
        "label": "release cable-roller--2.5",
        "requires": [
          "done:relock:cable-roller--2.5"
        ],
        "forbids": [
          "done:release:cable-roller--2.5"
        ],
        "adds": [
          "done:release:cable-roller--2.5",
          "ready:cable-roller--2.5",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5"
        }
      },
      {
        "id": "relock:cable-roller--2.5",
        "label": "relock cable-roller--2.5",
        "requires": [
          "done:verify:cable-roller--2.5"
        ],
        "forbids": [
          "done:relock:cable-roller--2.5"
        ],
        "adds": [
          "done:relock:cable-roller--2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5"
        }
      },
      {
        "id": "verify:cable-roller--2.5",
        "label": "verify cable-roller--2.5",
        "requires": [
          "done:replace:cable-roller--2.5"
        ],
        "forbids": [
          "done:verify:cable-roller--2.5"
        ],
        "adds": [
          "done:verify:cable-roller--2.5"
        ],
        "deletes": [
          "fault:cable-roller--2.5",
          "misaligned:cable-roller--2.5"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5"
        }
      },
      {
        "id": "replace:cable-roller--2.5",
        "label": "replace cable-roller--2.5",
        "requires": [
          "done:unlock:cable-roller--2.5"
        ],
        "forbids": [
          "done:replace:cable-roller--2.5"
        ],
        "adds": [
          "done:replace:cable-roller--2.5"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cable-roller--2.5"
        }
      },
      {
        "id": "unlock:cable-roller--2.5",
        "label": "unlock cable-roller--2.5",
        "requires": [
          "done:support:cable-roller--2.5"
        ],
        "forbids": [
          "done:unlock:cable-roller--2.5"
        ],
        "adds": [
          "done:unlock:cable-roller--2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5"
        }
      },
      {
        "id": "support:cable-roller--2.5",
        "label": "support cable-roller--2.5",
        "requires": [
          "done:isolate:cable-roller--2.5"
        ],
        "forbids": [
          "done:support:cable-roller--2.5"
        ],
        "adds": [
          "done:support:cable-roller--2.5"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5"
        }
      },
      {
        "id": "isolate:cable-roller--2.5",
        "label": "isolate cable-roller--2.5",
        "requires": [
          "tool:free",
          "fault:cable-roller--2.5"
        ],
        "forbids": [
          "done:isolate:cable-roller--2.5"
        ],
        "adds": [
          "done:isolate:cable-roller--2.5"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cable-roller--2.5"
        }
      },
      {
        "id": "release:sliding-tray",
        "label": "release sliding-tray",
        "requires": [
          "done:relock:sliding-tray"
        ],
        "forbids": [
          "done:release:sliding-tray"
        ],
        "adds": [
          "done:release:sliding-tray",
          "ready:sliding-tray",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "relock:sliding-tray",
        "label": "relock sliding-tray",
        "requires": [
          "done:verify:sliding-tray"
        ],
        "forbids": [
          "done:relock:sliding-tray"
        ],
        "adds": [
          "done:relock:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "verify:sliding-tray",
        "label": "verify sliding-tray",
        "requires": [
          "done:replace:sliding-tray"
        ],
        "forbids": [
          "done:verify:sliding-tray"
        ],
        "adds": [
          "done:verify:sliding-tray"
        ],
        "deletes": [
          "fault:sliding-tray",
          "misaligned:sliding-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "replace:sliding-tray",
        "label": "replace sliding-tray",
        "requires": [
          "done:unlock:sliding-tray"
        ],
        "forbids": [
          "done:replace:sliding-tray"
        ],
        "adds": [
          "done:replace:sliding-tray"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "unlock:sliding-tray",
        "label": "unlock sliding-tray",
        "requires": [
          "done:support:sliding-tray"
        ],
        "forbids": [
          "done:unlock:sliding-tray"
        ],
        "adds": [
          "done:unlock:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "support:sliding-tray",
        "label": "support sliding-tray",
        "requires": [
          "done:isolate:sliding-tray"
        ],
        "forbids": [
          "done:support:sliding-tray"
        ],
        "adds": [
          "done:support:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "isolate:sliding-tray",
        "label": "isolate sliding-tray",
        "requires": [
          "tool:free",
          "fault:sliding-tray"
        ],
        "forbids": [
          "done:isolate:sliding-tray"
        ],
        "adds": [
          "done:isolate:sliding-tray"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "release:clamp",
        "label": "release clamp",
        "requires": [
          "done:relock:clamp"
        ],
        "forbids": [
          "done:release:clamp"
        ],
        "adds": [
          "done:release:clamp",
          "ready:clamp",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "clamp"
        }
      },
      {
        "id": "relock:clamp",
        "label": "relock clamp",
        "requires": [
          "done:verify:clamp"
        ],
        "forbids": [
          "done:relock:clamp"
        ],
        "adds": [
          "done:relock:clamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "clamp"
        }
      },
      {
        "id": "verify:clamp",
        "label": "verify clamp",
        "requires": [
          "done:replace:clamp"
        ],
        "forbids": [
          "done:verify:clamp"
        ],
        "adds": [
          "done:verify:clamp"
        ],
        "deletes": [
          "fault:clamp",
          "misaligned:clamp"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "clamp"
        }
      },
      {
        "id": "replace:clamp",
        "label": "replace clamp",
        "requires": [
          "done:unlock:clamp"
        ],
        "forbids": [
          "done:replace:clamp"
        ],
        "adds": [
          "done:replace:clamp"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "clamp"
        }
      },
      {
        "id": "unlock:clamp",
        "label": "unlock clamp",
        "requires": [
          "done:support:clamp"
        ],
        "forbids": [
          "done:unlock:clamp"
        ],
        "adds": [
          "done:unlock:clamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "clamp"
        }
      },
      {
        "id": "support:clamp",
        "label": "support clamp",
        "requires": [
          "done:isolate:clamp"
        ],
        "forbids": [
          "done:support:clamp"
        ],
        "adds": [
          "done:support:clamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "clamp"
        }
      },
      {
        "id": "isolate:clamp",
        "label": "isolate clamp",
        "requires": [
          "tool:free",
          "fault:clamp"
        ],
        "forbids": [
          "done:isolate:clamp"
        ],
        "adds": [
          "done:isolate:clamp"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "clamp"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:clamp",
      "fault:sliding-tray",
      "fault:cable-roller--2.5",
      "fault:cable-roller-2.5"
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
      "cable-roller--2.5",
      "cable-roller-2.5"
    ],
    "goalFacts": [
      "ready:clamp",
      "ready:sliding-tray",
      "ready:cable-roller--2.5",
      "ready:cable-roller-2.5"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:cable-roller-2.5",
      "support:cable-roller-2.5",
      "unlock:cable-roller-2.5",
      "replace:cable-roller-2.5",
      "verify:cable-roller-2.5",
      "relock:cable-roller-2.5",
      "release:cable-roller-2.5",
      "isolate:cable-roller--2.5",
      "support:cable-roller--2.5",
      "unlock:cable-roller--2.5",
      "replace:cable-roller--2.5",
      "verify:cable-roller--2.5",
      "relock:cable-roller--2.5",
      "release:cable-roller--2.5",
      "isolate:sliding-tray",
      "support:sliding-tray",
      "unlock:sliding-tray",
      "replace:sliding-tray",
      "verify:sliding-tray",
      "relock:sliding-tray",
      "release:sliding-tray",
      "isolate:clamp",
      "support:clamp",
      "unlock:clamp",
      "replace:clamp",
      "verify:clamp",
      "relock:clamp",
      "release:clamp"
    ]
  }
}
```

### 预算约束检查策略（h3-cable-inspection-robot-budget-policy）

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
        "cost": 3,
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
        "cost": 4,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      }
    ],
    "budget": 3
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
