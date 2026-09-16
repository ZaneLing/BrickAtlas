## D1 双导轨升降台

### 模块识别（h3-exp-d1-slide-2-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：cell-0-carriage
- B：cell-0-cross-feed
- C：foundation
- D：cell-0-mount

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "foundation",
        "name": "foundation"
      },
      {
        "id": "cell-0-mount",
        "name": "cell 0 mount"
      },
      {
        "id": "cell-0-carriage",
        "name": "cell 0 carriage"
      },
      {
        "id": "cell-0-cross-feed",
        "name": "cell 0 cross feed"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 部件计数（h3-exp-d1-slide-2-count）

模块 cell-0-cross-feed 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：4
- B：5
- C：3
- D：7

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
        "id": "cell-0-mount-p56",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p57",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p58",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p59",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p60",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p61",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p62",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p63",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p64",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p65",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p66",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p67",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p68",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p69",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p70",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p71",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p72",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p73",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p74",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p75",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p76",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p77",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p78",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p79",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p80",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p81",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p82",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p83",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p84",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p85",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p86",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p87",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p88",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p89",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p90",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p91",
        "moduleId": "cell-0-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-mount-p92",
        "moduleId": "cell-0-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-mount-p93",
        "moduleId": "cell-0-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-mount-p94",
        "moduleId": "cell-0-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-mount-p95",
        "moduleId": "cell-0-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-mount-p96",
        "moduleId": "cell-0-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-mount-p97",
        "moduleId": "cell-0-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-mount-p98",
        "moduleId": "cell-0-mount",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-carriage-p99",
        "moduleId": "cell-0-carriage",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-carriage-p100",
        "moduleId": "cell-0-carriage",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-carriage-p101",
        "moduleId": "cell-0-carriage",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-carriage-p102",
        "moduleId": "cell-0-carriage",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-carriage-p103",
        "moduleId": "cell-0-carriage",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-carriage-p104",
        "moduleId": "cell-0-carriage",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-cross-feed-p105",
        "moduleId": "cell-0-cross-feed",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-cross-feed-p106",
        "moduleId": "cell-0-cross-feed",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-cross-feed-p107",
        "moduleId": "cell-0-cross-feed",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-cross-feed-p108",
        "moduleId": "cell-0-cross-feed",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-carriage-p109",
        "moduleId": "cell-0-carriage",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-carriage-p110",
        "moduleId": "cell-0-carriage",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-carriage-p111",
        "moduleId": "cell-0-carriage",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-carriage-p112",
        "moduleId": "cell-0-carriage",
        "shape": "beam",
        "color": "#e9ad37"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-exp-d1-slide-2-color）

零件 cell-0-cross-feed-p105 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#d43a32
- B：#f2bf3c
- C：#dc6040
- D：#2878b8

```json
{
  "input": {
    "part": {
      "id": "cell-0-cross-feed-p105",
      "moduleId": "cell-0-cross-feed",
      "shape": "plate",
      "position": [
        -0.5,
        -0.04999999999999982,
        -0.5
      ],
      "size": [
        0.96,
        0.24,
        0.96
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

### 三维位置（h3-exp-d1-slide-2-position）

模块 cell-0-cross-feed 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,2.84,-0.33499999999999996]
- B：[0,2.3,0]
- C：[0,0.2,0]
- D：[0,0.9025,0]

```json
{
  "input": {
    "centers": {
      "foundation": [
        0,
        0.2,
        0
      ],
      "cell-0-mount": [
        0,
        0.9025,
        0
      ],
      "cell-0-carriage": [
        0,
        2.84,
        -0.33499999999999996
      ],
      "cell-0-cross-feed": [
        0,
        2.3,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节类型（h3-exp-d1-slide-2-joint-type）

cell-0-cross-feed-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：fixed
- B：revolute
- C：spring
- D：prismatic

```json
{
  "input": {
    "joint": {
      "id": "cell-0-cross-feed-joint",
      "name": "cell-0-cross-feed interface",
      "parent": "cell-0-carriage",
      "child": "cell-0-cross-feed",
      "type": "prismatic",
      "anchorParent": [
        0,
        -0.5899999999999999,
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
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 直接连接（h3-exp-d1-slide-2-parent）

cell-0-cross-feed 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["cell-0-cross-feed"]
- B：[]
- C：["foundation","cell-0-mount","cell-0-carriage","cell-0-cross-feed"]
- D：["cell-0-carriage"]

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.25249999999999995,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-carriage-joint",
        "name": "cell-0-carriage interface",
        "parent": "cell-0-mount",
        "child": "cell-0-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.19,
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
        "id": "cell-0-cross-feed-joint",
        "name": "cell-0-cross-feed interface",
        "parent": "cell-0-carriage",
        "child": "cell-0-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.5899999999999999,
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
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 基座识别（h3-exp-d1-slide-2-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["cell-0-cross-feed"]
- B：["foundation"]
- C：[]
- D：["foundation","cell-0-mount","cell-0-carriage","cell-0-cross-feed"]

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
        "id": "cell-0-mount",
        "name": "cell 0 mount",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          0.9025,
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
        "id": "cell-0-carriage",
        "name": "cell 0 carriage",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          2.84,
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
        "id": "cell-0-cross-feed",
        "name": "cell 0 cross feed",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          2.3,
          0
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

### 接口计数（h3-exp-d1-slide-2-degree）

cell-0-cross-feed 连接几个声明关节？平行关节分别计数。

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
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.25249999999999995,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-carriage-joint",
        "name": "cell-0-carriage interface",
        "parent": "cell-0-mount",
        "child": "cell-0-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.19,
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
        "id": "cell-0-cross-feed-joint",
        "name": "cell-0-cross-feed interface",
        "parent": "cell-0-carriage",
        "child": "cell-0-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.5899999999999999,
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
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 局部改色（h3-exp-d1-slide-2-recolor）

仅将 cell-0-cross-feed-p105 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-cross-feed-p106","color":"#e8792e"}
- B：{"id":"cell-0-cross-feed-p105","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"cell-0-cross-feed-p105","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "cell-0-cross-feed-p105",
      "moduleId": "cell-0-cross-feed",
      "shape": "plate",
      "position": [
        -0.5,
        -0.04999999999999982,
        -0.5
      ],
      "size": [
        0.96,
        0.24,
        0.96
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
    "choiceId": "D"
  }
}
```

### 补装部件（h3-exp-d1-slide-2-add）

模块 cell-0-cross-feed 缺失零件 cell-0-cross-feed-p105。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-cross-feed-p105","moduleId":"foundation","shape":"plate","position":[-0.5,-0.04999999999999982,-0.5],"size":[0.96,0.24,0.96],"color":"#dc6040","rotation":[0,0,0,1]}
- B：{"id":"cell-0-cross-feed-p105","moduleId":"cell-0-cross-feed","shape":"plate","position":[-0.5,-0.04999999999999982,-0.5],"size":[3,3,3],"color":"#dc6040","rotation":[0,0,0,1]}
- C：{"id":"cell-0-cross-feed-p105","moduleId":"cell-0-cross-feed","shape":"plate","position":[-0.5,-0.04999999999999982,-0.5],"size":[0.96,0.24,0.96],"color":"#000000","rotation":[0,0,0,1]}
- D：{"id":"cell-0-cross-feed-p105","moduleId":"cell-0-cross-feed","shape":"plate","position":[-0.5,-0.04999999999999982,-0.5],"size":[0.96,0.24,0.96],"color":"#dc6040","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "cell-0-cross-feed-p105",
      "moduleId": "cell-0-cross-feed",
      "shape": "plate",
      "position": [
        -0.5,
        -0.04999999999999982,
        -0.5
      ],
      "size": [
        0.96,
        0.24,
        0.96
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
      "cell-0-mount-p56",
      "cell-0-mount-p57",
      "cell-0-mount-p58",
      "cell-0-mount-p59",
      "cell-0-mount-p60",
      "cell-0-mount-p61",
      "cell-0-mount-p62",
      "cell-0-mount-p63",
      "cell-0-mount-p64",
      "cell-0-mount-p65",
      "cell-0-mount-p66",
      "cell-0-mount-p67",
      "cell-0-mount-p68",
      "cell-0-mount-p69",
      "cell-0-mount-p70",
      "cell-0-mount-p71",
      "cell-0-mount-p72",
      "cell-0-mount-p73",
      "cell-0-mount-p74",
      "cell-0-mount-p75",
      "cell-0-mount-p76",
      "cell-0-mount-p77",
      "cell-0-mount-p78",
      "cell-0-mount-p79",
      "cell-0-mount-p80",
      "cell-0-mount-p81",
      "cell-0-mount-p82",
      "cell-0-mount-p83",
      "cell-0-mount-p84",
      "cell-0-mount-p85",
      "cell-0-mount-p86",
      "cell-0-mount-p87",
      "cell-0-mount-p88",
      "cell-0-mount-p89",
      "cell-0-mount-p90",
      "cell-0-mount-p91",
      "cell-0-mount-p92",
      "cell-0-mount-p93",
      "cell-0-mount-p94",
      "cell-0-mount-p95",
      "cell-0-mount-p96",
      "cell-0-mount-p97",
      "cell-0-mount-p98",
      "cell-0-carriage-p99",
      "cell-0-carriage-p100",
      "cell-0-carriage-p101",
      "cell-0-carriage-p102",
      "cell-0-carriage-p103",
      "cell-0-carriage-p104",
      "cell-0-cross-feed-p106",
      "cell-0-cross-feed-p107",
      "cell-0-cross-feed-p108",
      "cell-0-carriage-p109",
      "cell-0-carriage-p110",
      "cell-0-carriage-p111",
      "cell-0-carriage-p112"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 安全拆除（h3-exp-d1-slide-2-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["foundation","cell-0-mount","cell-0-carriage","cell-0-cross-feed"]
- B：["cell-0-cross-feed"]
- C：["foundation"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.25249999999999995,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-carriage-joint",
        "name": "cell-0-carriage interface",
        "parent": "cell-0-mount",
        "child": "cell-0-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.19,
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
        "id": "cell-0-cross-feed-joint",
        "name": "cell-0-cross-feed interface",
        "parent": "cell-0-carriage",
        "child": "cell-0-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.5899999999999999,
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
      }
    ],
    "modules": [
      "foundation",
      "cell-0-mount",
      "cell-0-carriage",
      "cell-0-cross-feed"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 替换选择（h3-exp-d1-slide-2-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

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
        "cost": 2,
        "stiffness": 11,
        "mass": 1.4
      },
      {
        "id": "stock-1",
        "cost": 7,
        "stiffness": 7,
        "mass": 1.9
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 3,
        "mass": 1.1
      },
      {
        "id": "stock-3",
        "cost": 2,
        "stiffness": 3,
        "mass": 1.3
      }
    ],
    "maxCost": 6
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 平移纠偏（h3-exp-d1-slide-2-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[-1,0,2]
- B：[1,0,-2]
- C：[0,0,0]
- D：[0,2,0]

```json
{
  "input": {
    "delta": [
      1,
      0,
      -2
    ],
    "target": "cell-0-cross-feed"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 姿态纠偏（h3-exp-d1-slide-2-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：135
- B：0
- C：90
- D：-135

```json
{
  "input": {
    "module": "cell-0-cross-feed",
    "currentYaw": 90,
    "targetYaw": 315
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 下一步放置（h3-exp-d1-slide-2-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["cell-0-carriage"]
- B：[]
- C：["foundation","cell-0-mount"]
- D：["cell-0-carriage","cell-0-cross-feed"]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "cell-0-mount"
    ],
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.25249999999999995,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-carriage-joint",
        "name": "cell-0-carriage interface",
        "parent": "cell-0-mount",
        "child": "cell-0-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.19,
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
        "id": "cell-0-cross-feed-joint",
        "name": "cell-0-cross-feed interface",
        "parent": "cell-0-carriage",
        "child": "cell-0-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.5899999999999999,
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
      }
    ],
    "modules": [
      "foundation",
      "cell-0-mount",
      "cell-0-carriage",
      "cell-0-cross-feed"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 库存核算（h3-exp-d1-slide-2-inventory）

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

### 子装配边界（h3-exp-d1-slide-2-boundary）

隔离 cell-0-cross-feed 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：[]
- B：["cell-0-mount-joint","cell-0-carriage-joint","cell-0-cross-feed-joint"]
- C：["cell-0-cross-feed-joint"]

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.25249999999999995,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-carriage-joint",
        "name": "cell-0-carriage interface",
        "parent": "cell-0-mount",
        "child": "cell-0-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.19,
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
        "id": "cell-0-cross-feed-joint",
        "name": "cell-0-cross-feed interface",
        "parent": "cell-0-carriage",
        "child": "cell-0-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.5899999999999999,
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
      }
    ],
    "target": "cell-0-cross-feed"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 最小干预（h3-exp-d1-slide-2-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：0
- B：1
- C：2
- D：4

```json
{
  "input": {
    "module": "cell-0-cross-feed"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 全过程依赖（h3-exp-d1-slide-2-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：3
- B：0
- C：-1
- D：1

```json
{
  "input": {
    "order": [
      "cell-0-mount",
      "foundation",
      "cell-0-carriage",
      "cell-0-cross-feed"
    ],
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.25249999999999995,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-carriage-joint",
        "name": "cell-0-carriage interface",
        "parent": "cell-0-mount",
        "child": "cell-0-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.19,
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
        "id": "cell-0-cross-feed-joint",
        "name": "cell-0-cross-feed interface",
        "parent": "cell-0-carriage",
        "child": "cell-0-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.5899999999999999,
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
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 连续维修路径（h3-exp-d1-slide-2-access）

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
          7.98,
          2.3,
          0
        ],
        "end": [
          0,
          2.3,
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
        "id": "path-1",
        "start": [
          0,
          8.149999999999999,
          0
        ],
        "end": [
          0,
          2.3,
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
          0,
          2.3,
          7.48
        ],
        "end": [
          0,
          2.3,
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
      "A",
      "B",
      "C"
    ]
  }
}
```

### 支撑反事实（h3-exp-d1-slide-2-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["foundation","cell-0-mount","cell-0-carriage","cell-0-cross-feed"]
- C：["cell-0-carriage","cell-0-cross-feed"]
- D：["cell-0-mount"]

```json
{
  "input": {
    "removed": "cell-0-mount",
    "roots": [
      "foundation"
    ],
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.25249999999999995,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-carriage-joint",
        "name": "cell-0-carriage interface",
        "parent": "cell-0-mount",
        "child": "cell-0-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.19,
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
        "id": "cell-0-cross-feed-joint",
        "name": "cell-0-cross-feed interface",
        "parent": "cell-0-carriage",
        "child": "cell-0-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.5899999999999999,
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
      }
    ],
    "modules": [
      "foundation",
      "cell-0-mount",
      "cell-0-carriage",
      "cell-0-cross-feed"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-exp-d1-slide-2-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.2023
- B：0
- C：1.0023
- D：0.0023

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0022844323089978988
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.000028458307737811343
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0000030218143638225386
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 1,
        "displacement": 0.0000030218143638226292
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.0001841068267829572,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节限位推理（h3-exp-d1-slide-2-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-0.45
- B：0
- C：-0.95
- D：0.95

```json
{
  "input": {
    "joint": "cell-0-cross-feed-joint",
    "limits": [
      -0.45,
      0.45
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

### 约束故障诊断（h3-exp-d1-slide-2-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：cell-0-cross-feed-joint
- B：cell-0-mount-joint
- C：cell-0-carriage-joint

```json
{
  "input": {
    "endpoints": [
      "cell-0-carriage",
      "cell-0-cross-feed"
    ],
    "type": "prismatic",
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.25249999999999995,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-carriage-joint",
        "name": "cell-0-carriage interface",
        "parent": "cell-0-mount",
        "child": "cell-0-carriage",
        "type": "prismatic",
        "anchorParent": [
          0,
          0.7474999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.19,
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
        "id": "cell-0-cross-feed-joint",
        "name": "cell-0-cross-feed interface",
        "parent": "cell-0-carriage",
        "child": "cell-0-cross-feed",
        "type": "prismatic",
        "anchorParent": [
          0,
          -0.5899999999999999,
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

### 主动检查收益（h3-exp-d1-slide-2-information-gain）

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
    "module": "cell-0-cross-feed",
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

### 不确定性与弃答（h3-exp-d1-slide-2-abstention）

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

### 观测后信念更新（h3-exp-d1-slide-2-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.3333333333333333
- B：0.5
- C：0
- D：0.25

```json
{
  "input": {
    "module": "cell-0-cross-feed",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "negative",
      "positive",
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

### 多目标工程权衡（h3-exp-d1-slide-2-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

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
        "cost": 2,
        "stiffness": 11,
        "mass": 1.4
      },
      {
        "id": "stock-1",
        "cost": 7,
        "stiffness": 7,
        "mass": 1.9
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 3,
        "mass": 1.1
      },
      {
        "id": "stock-3",
        "cost": 2,
        "stiffness": 3,
        "mass": 1.3
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

### 依赖装配（h3-exp-d1-slide-2-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:cell-0-carriage",
        "label": "安装 cell-0-carriage",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-carriage"
        ],
        "adds": [
          "present:cell-0-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-carriage",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-mount",
        "label": "安装 cell-0-mount",
        "requires": [
          "present:foundation"
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
        "id": "place:cell-0-cross-feed",
        "label": "安装 cell-0-cross-feed",
        "requires": [
          "present:cell-0-carriage"
        ],
        "forbids": [
          "present:cell-0-cross-feed"
        ],
        "adds": [
          "present:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed",
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
      "present:cell-0-mount",
      "present:cell-0-carriage",
      "present:cell-0-cross-feed"
    ],
    "budget": 4,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:cell-0-mount",
      "place:cell-0-carriage",
      "place:cell-0-cross-feed"
    ]
  }
}
```

### 依赖拆解（h3-exp-d1-slide-2-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:cell-0-mount",
      "present:cell-0-carriage",
      "present:cell-0-cross-feed"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-carriage",
      "cell-0-cross-feed"
    ],
    "actions": [
      {
        "id": "remove:cell-0-cross-feed",
        "label": "拆除 cell-0-cross-feed",
        "requires": [
          "present:cell-0-cross-feed"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-cross-feed"
        ],
        "deletes": [
          "present:cell-0-cross-feed"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-carriage",
        "label": "拆除 cell-0-carriage",
        "requires": [
          "present:cell-0-carriage"
        ],
        "forbids": [
          "present:cell-0-cross-feed"
        ],
        "adds": [
          "removed:cell-0-carriage"
        ],
        "deletes": [
          "present:cell-0-carriage"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-carriage",
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
          "present:cell-0-mount"
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
        "id": "remove:cell-0-mount",
        "label": "拆除 cell-0-mount",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-carriage"
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
      }
    ],
    "goalFacts": [
      "removed:cell-0-cross-feed",
      "removed:cell-0-carriage",
      "removed:cell-0-mount",
      "removed:foundation"
    ],
    "budget": 4,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:cell-0-cross-feed",
      "remove:cell-0-carriage",
      "remove:cell-0-mount",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-exp-d1-slide-2-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-cross-feed",
      "closed:cell-0-cross-feed"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-carriage",
      "cell-0-cross-feed"
    ],
    "actions": [
      {
        "id": "close:cell-0-cross-feed",
        "label": "close cell-0-cross-feed",
        "requires": [
          "done:verify:cell-0-cross-feed"
        ],
        "forbids": [
          "done:close:cell-0-cross-feed"
        ],
        "adds": [
          "done:close:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "release:cell-0-cross-feed",
        "label": "release cell-0-cross-feed",
        "requires": [
          "done:close:cell-0-cross-feed"
        ],
        "forbids": [
          "done:release:cell-0-cross-feed"
        ],
        "adds": [
          "done:release:cell-0-cross-feed",
          "repaired:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "remove:cell-0-cross-feed",
        "label": "remove cell-0-cross-feed",
        "requires": [
          "done:open:cell-0-cross-feed"
        ],
        "forbids": [
          "done:remove:cell-0-cross-feed"
        ],
        "adds": [
          "done:remove:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed",
          "visible": false
        }
      },
      {
        "id": "replace:cell-0-cross-feed",
        "label": "replace cell-0-cross-feed",
        "requires": [
          "done:remove:cell-0-cross-feed"
        ],
        "forbids": [
          "done:replace:cell-0-cross-feed"
        ],
        "adds": [
          "done:replace:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed",
          "visible": true
        }
      },
      {
        "id": "support:cell-0-cross-feed",
        "label": "support cell-0-cross-feed",
        "requires": [
          "fault:cell-0-cross-feed"
        ],
        "forbids": [
          "done:support:cell-0-cross-feed"
        ],
        "adds": [
          "done:support:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "verify:cell-0-cross-feed",
        "label": "verify cell-0-cross-feed",
        "requires": [
          "done:replace:cell-0-cross-feed"
        ],
        "forbids": [
          "done:verify:cell-0-cross-feed"
        ],
        "adds": [
          "done:verify:cell-0-cross-feed"
        ],
        "deletes": [
          "fault:cell-0-cross-feed"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "open:cell-0-cross-feed",
        "label": "open cell-0-cross-feed",
        "requires": [
          "done:support:cell-0-cross-feed"
        ],
        "forbids": [
          "done:open:cell-0-cross-feed"
        ],
        "adds": [
          "done:open:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-cross-feed"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-cross-feed",
      "open:cell-0-cross-feed",
      "remove:cell-0-cross-feed",
      "replace:cell-0-cross-feed",
      "verify:cell-0-cross-feed",
      "close:cell-0-cross-feed",
      "release:cell-0-cross-feed"
    ]
  }
}
```

### 复合编辑验证（h3-exp-d1-slide-2-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-cross-feed",
      "closed:cell-0-cross-feed"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-carriage",
      "cell-0-cross-feed"
    ],
    "actions": [
      {
        "id": "close:cell-0-cross-feed",
        "label": "close cell-0-cross-feed",
        "requires": [
          "done:verify:cell-0-cross-feed"
        ],
        "forbids": [
          "done:close:cell-0-cross-feed"
        ],
        "adds": [
          "done:close:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "release:cell-0-cross-feed",
        "label": "release cell-0-cross-feed",
        "requires": [
          "done:close:cell-0-cross-feed"
        ],
        "forbids": [
          "done:release:cell-0-cross-feed"
        ],
        "adds": [
          "done:release:cell-0-cross-feed",
          "repaired:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "recolor:cell-0-cross-feed",
        "label": "recolor cell-0-cross-feed",
        "requires": [
          "done:open:cell-0-cross-feed"
        ],
        "forbids": [
          "done:recolor:cell-0-cross-feed"
        ],
        "adds": [
          "done:recolor:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed",
          "color": "#ea7635"
        }
      },
      {
        "id": "support:cell-0-cross-feed",
        "label": "support cell-0-cross-feed",
        "requires": [
          "fault:cell-0-cross-feed"
        ],
        "forbids": [
          "done:support:cell-0-cross-feed"
        ],
        "adds": [
          "done:support:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "verify:cell-0-cross-feed",
        "label": "verify cell-0-cross-feed",
        "requires": [
          "done:recolor:cell-0-cross-feed"
        ],
        "forbids": [
          "done:verify:cell-0-cross-feed"
        ],
        "adds": [
          "done:verify:cell-0-cross-feed"
        ],
        "deletes": [
          "fault:cell-0-cross-feed"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "open:cell-0-cross-feed",
        "label": "open cell-0-cross-feed",
        "requires": [
          "done:support:cell-0-cross-feed"
        ],
        "forbids": [
          "done:open:cell-0-cross-feed"
        ],
        "adds": [
          "done:open:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-cross-feed"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-cross-feed",
      "open:cell-0-cross-feed",
      "recolor:cell-0-cross-feed",
      "verify:cell-0-cross-feed",
      "close:cell-0-cross-feed",
      "release:cell-0-cross-feed"
    ]
  }
}
```

### 跨区域联合维修（h3-exp-d1-slide-2-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-cross-feed",
      "closed:cell-0-cross-feed"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-carriage",
      "cell-0-cross-feed"
    ],
    "actions": [
      {
        "id": "close:cell-0-cross-feed",
        "label": "close cell-0-cross-feed",
        "requires": [
          "done:verify:cell-0-cross-feed"
        ],
        "forbids": [
          "done:close:cell-0-cross-feed"
        ],
        "adds": [
          "done:close:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "release:cell-0-cross-feed",
        "label": "release cell-0-cross-feed",
        "requires": [
          "done:close:cell-0-cross-feed"
        ],
        "forbids": [
          "done:release:cell-0-cross-feed"
        ],
        "adds": [
          "done:release:cell-0-cross-feed",
          "repaired:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "remove:cell-0-cross-feed",
        "label": "remove cell-0-cross-feed",
        "requires": [
          "done:open:cell-0-cross-feed"
        ],
        "forbids": [
          "done:remove:cell-0-cross-feed"
        ],
        "adds": [
          "done:remove:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed",
          "visible": false
        }
      },
      {
        "id": "replace:cell-0-cross-feed",
        "label": "replace cell-0-cross-feed",
        "requires": [
          "done:remove:cell-0-cross-feed"
        ],
        "forbids": [
          "done:replace:cell-0-cross-feed"
        ],
        "adds": [
          "done:replace:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed",
          "visible": true
        }
      },
      {
        "id": "support:cell-0-cross-feed",
        "label": "support cell-0-cross-feed",
        "requires": [
          "fault:cell-0-cross-feed"
        ],
        "forbids": [
          "done:support:cell-0-cross-feed"
        ],
        "adds": [
          "done:support:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "verify:cell-0-cross-feed",
        "label": "verify cell-0-cross-feed",
        "requires": [
          "done:replace:cell-0-cross-feed"
        ],
        "forbids": [
          "done:verify:cell-0-cross-feed"
        ],
        "adds": [
          "done:verify:cell-0-cross-feed"
        ],
        "deletes": [
          "fault:cell-0-cross-feed"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "open:cell-0-cross-feed",
        "label": "open cell-0-cross-feed",
        "requires": [
          "done:support:cell-0-cross-feed"
        ],
        "forbids": [
          "done:open:cell-0-cross-feed"
        ],
        "adds": [
          "done:open:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-cross-feed"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-cross-feed",
      "open:cell-0-cross-feed",
      "remove:cell-0-cross-feed",
      "replace:cell-0-cross-feed",
      "verify:cell-0-cross-feed",
      "close:cell-0-cross-feed",
      "release:cell-0-cross-feed"
    ]
  }
}
```

### 多工位资源调度（h3-exp-d1-slide-2-scheduling）

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
        "module": "cell-0-mount",
        "duration": 3,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "cell-0-carriage",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "cell-0-cross-feed",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      }
    ],
    "deadline": 4
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 3
    }
  }
}
```

### 检查后条件策略（h3-exp-d1-slide-2-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-cross-feed",
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

### 局部坐标变换（h3-exp-d1-slide-2-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[-0.5,2.25,0.5]
- B：[0.5,-0.05,-0.5]
- C：[0.5,2.25,-0.5]
- D：[0.5,3.25,1.5]

```json
{
  "input": {
    "localPoint": [
      0.5,
      -0.04999999999999982,
      -0.5
    ],
    "rotationXYZW": [
      0,
      1,
      0,
      6.123233995736766e-17
    ],
    "translation": [
      0,
      2.3,
      0
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 正交视图投影（h3-exp-d1-slide-2-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[0,0]
- B：[2,5]
- C：[5,2]
- D：[2,3]

```json
{
  "input": {
    "view": "front",
    "point": [
      2,
      5,
      -3
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 空间相对关系（h3-exp-d1-slide-2-relative-order）

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
      "id": "cell-0-cross-feed",
      "position": [
        0,
        2.3,
        0
      ]
    },
    "axis": "x"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 约束自由度（h3-exp-d1-slide-2-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：0
- B：1
- C：3
- D：6

```json
{
  "input": {
    "joint": {
      "id": "cell-0-mount-joint",
      "name": "cell-0-mount interface",
      "parent": "foundation",
      "child": "cell-0-mount",
      "type": "fixed",
      "anchorParent": [
        0,
        0.44999999999999996,
        0
      ],
      "anchorChild": [
        0,
        -0.25249999999999995,
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
    "choiceId": "A"
  }
}
```

### 维修间隙预算（h3-exp-d1-slide-2-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "cell-0-cross-feed",
    "aperture": 0.3,
    "toolWidth": 0.35,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-exp-d1-slide-2-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,-1,0]
- C：[0,0,-4]
- D：[0,0,4]

```json
{
  "input": {
    "module": "cell-0-cross-feed",
    "lever": [
      1,
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
    "choiceId": "C"
  }
}
```

### 非均匀先验更新（h3-exp-d1-slide-2-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.625
- B：0.5
- C：0
- D：1

```json
{
  "input": {
    "module": "cell-0-cross-feed",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      3,
      5,
      2
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

### 风险最小决策（h3-exp-d1-slide-2-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.3,
    "repairCost": 6,
    "failureLoss": 7,
    "module": "cell-0-cross-feed"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-exp-d1-slide-2-trace-threshold）

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
        "displacement": 0.0022844323089978988
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.000028458307737811343
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0000030218143638225386
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000030218143638226292
      },
      {
        "time": 1,
        "displacement": 0.0000030218143638226292
      }
    ],
    "threshold": 0.0018275458471983192
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-exp-d1-slide-2-guarded-repair）

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
        "id": "release:cell-0-cross-feed",
        "label": "release cell-0-cross-feed",
        "requires": [
          "done:relock:cell-0-cross-feed"
        ],
        "forbids": [
          "done:release:cell-0-cross-feed"
        ],
        "adds": [
          "done:release:cell-0-cross-feed",
          "ready:cell-0-cross-feed",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "relock:cell-0-cross-feed",
        "label": "relock cell-0-cross-feed",
        "requires": [
          "done:verify:cell-0-cross-feed"
        ],
        "forbids": [
          "done:relock:cell-0-cross-feed"
        ],
        "adds": [
          "done:relock:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "verify:cell-0-cross-feed",
        "label": "verify cell-0-cross-feed",
        "requires": [
          "done:replace:cell-0-cross-feed"
        ],
        "forbids": [
          "done:verify:cell-0-cross-feed"
        ],
        "adds": [
          "done:verify:cell-0-cross-feed"
        ],
        "deletes": [
          "fault:cell-0-cross-feed",
          "misaligned:cell-0-cross-feed"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "replace:cell-0-cross-feed",
        "label": "replace cell-0-cross-feed",
        "requires": [
          "done:unlock:cell-0-cross-feed"
        ],
        "forbids": [
          "done:replace:cell-0-cross-feed"
        ],
        "adds": [
          "done:replace:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "unlock:cell-0-cross-feed",
        "label": "unlock cell-0-cross-feed",
        "requires": [
          "done:support:cell-0-cross-feed"
        ],
        "forbids": [
          "done:unlock:cell-0-cross-feed"
        ],
        "adds": [
          "done:unlock:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "support:cell-0-cross-feed",
        "label": "support cell-0-cross-feed",
        "requires": [
          "done:isolate:cell-0-cross-feed"
        ],
        "forbids": [
          "done:support:cell-0-cross-feed"
        ],
        "adds": [
          "done:support:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "isolate:cell-0-cross-feed",
        "label": "isolate cell-0-cross-feed",
        "requires": [
          "tool:free",
          "fault:cell-0-cross-feed"
        ],
        "forbids": [
          "done:isolate:cell-0-cross-feed"
        ],
        "adds": [
          "done:isolate:cell-0-cross-feed"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-cross-feed"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-carriage",
      "cell-0-cross-feed"
    ],
    "goalFacts": [
      "ready:cell-0-cross-feed"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-cross-feed",
      "support:cell-0-cross-feed",
      "unlock:cell-0-cross-feed",
      "replace:cell-0-cross-feed",
      "verify:cell-0-cross-feed",
      "relock:cell-0-cross-feed",
      "release:cell-0-cross-feed"
    ]
  }
}
```

### 失败状态回退（h3-exp-d1-slide-2-rollback）

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
        "id": "resume:cell-0-cross-feed",
        "label": "resume cell-0-cross-feed",
        "requires": [
          "done:verify:cell-0-cross-feed"
        ],
        "forbids": [
          "done:resume:cell-0-cross-feed"
        ],
        "adds": [
          "done:resume:cell-0-cross-feed",
          "ready:cell-0-cross-feed",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "verify:cell-0-cross-feed",
        "label": "verify cell-0-cross-feed",
        "requires": [
          "done:align:cell-0-cross-feed"
        ],
        "forbids": [
          "done:verify:cell-0-cross-feed"
        ],
        "adds": [
          "done:verify:cell-0-cross-feed"
        ],
        "deletes": [
          "fault:cell-0-cross-feed",
          "misaligned:cell-0-cross-feed"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "align:cell-0-cross-feed",
        "label": "align cell-0-cross-feed",
        "requires": [
          "done:undo:cell-0-cross-feed"
        ],
        "forbids": [
          "done:align:cell-0-cross-feed"
        ],
        "adds": [
          "done:align:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed",
          "visible": true
        }
      },
      {
        "id": "undo:cell-0-cross-feed",
        "label": "undo cell-0-cross-feed",
        "requires": [
          "done:isolate:cell-0-cross-feed"
        ],
        "forbids": [
          "done:undo:cell-0-cross-feed"
        ],
        "adds": [
          "done:undo:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed",
          "visible": false
        }
      },
      {
        "id": "isolate:cell-0-cross-feed",
        "label": "isolate cell-0-cross-feed",
        "requires": [
          "tool:free",
          "fault:cell-0-cross-feed"
        ],
        "forbids": [
          "done:isolate:cell-0-cross-feed"
        ],
        "adds": [
          "done:isolate:cell-0-cross-feed"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-cross-feed",
      "misaligned:cell-0-cross-feed"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-carriage",
      "cell-0-cross-feed"
    ],
    "goalFacts": [
      "ready:cell-0-cross-feed"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-cross-feed",
      "undo:cell-0-cross-feed",
      "align:cell-0-cross-feed",
      "verify:cell-0-cross-feed",
      "resume:cell-0-cross-feed"
    ]
  }
}
```

### 共享工具协同维修（h3-exp-d1-slide-2-resource-repair）

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
        "id": "release:cell-0-cross-feed",
        "label": "release cell-0-cross-feed",
        "requires": [
          "done:relock:cell-0-cross-feed"
        ],
        "forbids": [
          "done:release:cell-0-cross-feed"
        ],
        "adds": [
          "done:release:cell-0-cross-feed",
          "ready:cell-0-cross-feed",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "relock:cell-0-cross-feed",
        "label": "relock cell-0-cross-feed",
        "requires": [
          "done:verify:cell-0-cross-feed"
        ],
        "forbids": [
          "done:relock:cell-0-cross-feed"
        ],
        "adds": [
          "done:relock:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "verify:cell-0-cross-feed",
        "label": "verify cell-0-cross-feed",
        "requires": [
          "done:replace:cell-0-cross-feed"
        ],
        "forbids": [
          "done:verify:cell-0-cross-feed"
        ],
        "adds": [
          "done:verify:cell-0-cross-feed"
        ],
        "deletes": [
          "fault:cell-0-cross-feed",
          "misaligned:cell-0-cross-feed"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "replace:cell-0-cross-feed",
        "label": "replace cell-0-cross-feed",
        "requires": [
          "done:unlock:cell-0-cross-feed"
        ],
        "forbids": [
          "done:replace:cell-0-cross-feed"
        ],
        "adds": [
          "done:replace:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "unlock:cell-0-cross-feed",
        "label": "unlock cell-0-cross-feed",
        "requires": [
          "done:support:cell-0-cross-feed"
        ],
        "forbids": [
          "done:unlock:cell-0-cross-feed"
        ],
        "adds": [
          "done:unlock:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "support:cell-0-cross-feed",
        "label": "support cell-0-cross-feed",
        "requires": [
          "done:isolate:cell-0-cross-feed"
        ],
        "forbids": [
          "done:support:cell-0-cross-feed"
        ],
        "adds": [
          "done:support:cell-0-cross-feed"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "isolate:cell-0-cross-feed",
        "label": "isolate cell-0-cross-feed",
        "requires": [
          "tool:free",
          "fault:cell-0-cross-feed"
        ],
        "forbids": [
          "done:isolate:cell-0-cross-feed"
        ],
        "adds": [
          "done:isolate:cell-0-cross-feed"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-cross-feed"
        }
      },
      {
        "id": "release:cell-0-carriage",
        "label": "release cell-0-carriage",
        "requires": [
          "done:relock:cell-0-carriage"
        ],
        "forbids": [
          "done:release:cell-0-carriage"
        ],
        "adds": [
          "done:release:cell-0-carriage",
          "ready:cell-0-carriage",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-carriage"
        }
      },
      {
        "id": "relock:cell-0-carriage",
        "label": "relock cell-0-carriage",
        "requires": [
          "done:verify:cell-0-carriage"
        ],
        "forbids": [
          "done:relock:cell-0-carriage"
        ],
        "adds": [
          "done:relock:cell-0-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-carriage"
        }
      },
      {
        "id": "verify:cell-0-carriage",
        "label": "verify cell-0-carriage",
        "requires": [
          "done:replace:cell-0-carriage"
        ],
        "forbids": [
          "done:verify:cell-0-carriage"
        ],
        "adds": [
          "done:verify:cell-0-carriage"
        ],
        "deletes": [
          "fault:cell-0-carriage",
          "misaligned:cell-0-carriage"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-carriage"
        }
      },
      {
        "id": "replace:cell-0-carriage",
        "label": "replace cell-0-carriage",
        "requires": [
          "done:unlock:cell-0-carriage"
        ],
        "forbids": [
          "done:replace:cell-0-carriage"
        ],
        "adds": [
          "done:replace:cell-0-carriage"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-carriage"
        }
      },
      {
        "id": "unlock:cell-0-carriage",
        "label": "unlock cell-0-carriage",
        "requires": [
          "done:support:cell-0-carriage"
        ],
        "forbids": [
          "done:unlock:cell-0-carriage"
        ],
        "adds": [
          "done:unlock:cell-0-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-carriage"
        }
      },
      {
        "id": "support:cell-0-carriage",
        "label": "support cell-0-carriage",
        "requires": [
          "done:isolate:cell-0-carriage"
        ],
        "forbids": [
          "done:support:cell-0-carriage"
        ],
        "adds": [
          "done:support:cell-0-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-carriage"
        }
      },
      {
        "id": "isolate:cell-0-carriage",
        "label": "isolate cell-0-carriage",
        "requires": [
          "tool:free",
          "fault:cell-0-carriage"
        ],
        "forbids": [
          "done:isolate:cell-0-carriage"
        ],
        "adds": [
          "done:isolate:cell-0-carriage"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-carriage"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-carriage",
      "fault:cell-0-cross-feed"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-carriage",
      "cell-0-cross-feed"
    ],
    "goalFacts": [
      "ready:cell-0-carriage",
      "ready:cell-0-cross-feed"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 16
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-cross-feed",
      "support:cell-0-cross-feed",
      "unlock:cell-0-cross-feed",
      "replace:cell-0-cross-feed",
      "verify:cell-0-cross-feed",
      "relock:cell-0-cross-feed",
      "release:cell-0-cross-feed",
      "isolate:cell-0-carriage",
      "support:cell-0-carriage",
      "unlock:cell-0-carriage",
      "replace:cell-0-carriage",
      "verify:cell-0-carriage",
      "relock:cell-0-carriage",
      "release:cell-0-carriage"
    ]
  }
}
```

### 预算约束检查策略（h3-exp-d1-slide-2-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-cross-feed",
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
