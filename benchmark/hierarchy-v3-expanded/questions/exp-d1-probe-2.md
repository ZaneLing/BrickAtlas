## D1 三向探针架

### 模块识别（h3-exp-d1-probe-2-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：cell-0-hub
- B：cell-0-probe-2
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
        "id": "cell-0-hub",
        "name": "cell 0 hub"
      },
      {
        "id": "cell-0-probe-0",
        "name": "cell 0 probe 0"
      },
      {
        "id": "cell-0-probe-1",
        "name": "cell 0 probe 1"
      },
      {
        "id": "cell-0-probe-2",
        "name": "cell 0 probe 2"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 部件计数（h3-exp-d1-probe-2-count）

模块 cell-0-probe-2 有多少个可视零件？

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
        "id": "cell-0-hub-p91",
        "moduleId": "cell-0-hub",
        "shape": "cylinder",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-probe-0-p92",
        "moduleId": "cell-0-probe-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-probe-0-p93",
        "moduleId": "cell-0-probe-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-probe-0-p94",
        "moduleId": "cell-0-probe-0",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-probe-0-p95",
        "moduleId": "cell-0-probe-0",
        "shape": "sphere",
        "color": "#45a080"
      },
      {
        "id": "cell-0-probe-1-p96",
        "moduleId": "cell-0-probe-1",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-probe-1-p97",
        "moduleId": "cell-0-probe-1",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-probe-1-p98",
        "moduleId": "cell-0-probe-1",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-probe-1-p99",
        "moduleId": "cell-0-probe-1",
        "shape": "sphere",
        "color": "#45a080"
      },
      {
        "id": "cell-0-probe-2-p100",
        "moduleId": "cell-0-probe-2",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-probe-2-p101",
        "moduleId": "cell-0-probe-2",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-probe-2-p102",
        "moduleId": "cell-0-probe-2",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-probe-2-p103",
        "moduleId": "cell-0-probe-2",
        "shape": "sphere",
        "color": "#45a080"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 颜色识别（h3-exp-d1-probe-2-color）

零件 cell-0-probe-2-p100 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#e9ad37
- B：#2878b8
- C：#d43a32
- D：#f2bf3c

```json
{
  "input": {
    "part": {
      "id": "cell-0-probe-2-p100",
      "moduleId": "cell-0-probe-2",
      "shape": "beam",
      "position": [
        0.33126565491822885,
        -0.8552064085095366,
        0.5260277826906352
      ],
      "size": [
        0.25,
        0.8137703743822469,
        0.25
      ],
      "color": "#e9ad37",
      "rotation": [
        -0.2603613446834222,
        0,
        0.15031969243954693,
        0.9537378886567945
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 三维位置（h3-exp-d1-probe-2-position）

模块 cell-0-probe-2 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[-0.9479323215848959,4.03853974184287,-1.5941257806914426]
- B：[0,0.2,0]
- C：[0,0.7,0]
- D：[0,1.65,0]

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
        0.7,
        0
      ],
      "cell-0-hub": [
        0,
        1.65,
        0
      ],
      "cell-0-probe-0": [
        1.83629800496756,
        4.051658603477293,
        0
      ],
      "cell-0-probe-1": [
        -0.9479323215848947,
        4.03853974184287,
        1.5941257806914428
      ],
      "cell-0-probe-2": [
        -0.9479323215848959,
        4.03853974184287,
        -1.5941257806914426
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节类型（h3-exp-d1-probe-2-joint-type）

cell-0-probe-2-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：fixed
- B：revolute
- C：spring
- D：prismatic

```json
{
  "input": {
    "joint": {
      "id": "cell-0-probe-2-joint",
      "name": "cell-0-probe-2 interface",
      "parent": "cell-0-hub",
      "child": "cell-0-probe-2",
      "type": "prismatic",
      "anchorParent": [
        -0.5000000000000004,
        1.2000000000000002,
        -0.8660254037844385
      ],
      "anchorChild": [
        0.4479323215848956,
        -1.1885397418428698,
        0.7281003769070041
      ],
      "axis": [
        -0.30000000000000027,
        0.8,
        -0.519615242270663
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

### 直接连接（h3-exp-d1-probe-2-parent）

cell-0-probe-2 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["cell-0-hub"]
- B：["cell-0-probe-2"]
- C：[]
- D：["foundation","cell-0-mount","cell-0-hub","cell-0-probe-0","cell-0-probe-1","cell-0-probe-2"]

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
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-hub-joint",
        "name": "cell-0-hub interface",
        "parent": "cell-0-mount",
        "child": "cell-0-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.95,
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
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772927,
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
        "id": "cell-0-probe-1-joint",
        "name": "cell-0-probe-1 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-1",
        "type": "prismatic",
        "anchorParent": [
          -0.4999999999999998,
          1.2000000000000002,
          0.8660254037844387
        ],
        "anchorChild": [
          0.44793232158489493,
          -1.1885397418428698,
          -0.7281003769070041
        ],
        "axis": [
          -0.2999999999999999,
          0.8,
          0.5196152422706632
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-2-joint",
        "name": "cell-0-probe-2 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-2",
        "type": "prismatic",
        "anchorParent": [
          -0.5000000000000004,
          1.2000000000000002,
          -0.8660254037844385
        ],
        "anchorChild": [
          0.4479323215848956,
          -1.1885397418428698,
          0.7281003769070041
        ],
        "axis": [
          -0.30000000000000027,
          0.8,
          -0.519615242270663
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

### 基座识别（h3-exp-d1-probe-2-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["cell-0-probe-2"]
- B：["foundation"]
- C：[]
- D：["foundation","cell-0-mount","cell-0-hub","cell-0-probe-0","cell-0-probe-1","cell-0-probe-2"]

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
          0.7,
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
        "id": "cell-0-hub",
        "name": "cell 0 hub",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          1.65,
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
        "id": "cell-0-probe-0",
        "name": "cell 0 probe 0",
        "role": "actuator",
        "anchored": false,
        "mass": 0.5,
        "position": [
          1.83629800496756,
          4.051658603477293,
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
        "id": "cell-0-probe-1",
        "name": "cell 0 probe 1",
        "role": "actuator",
        "anchored": false,
        "mass": 0.5,
        "position": [
          -0.9479323215848947,
          4.03853974184287,
          1.5941257806914428
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-probe-2",
        "name": "cell 0 probe 2",
        "role": "actuator",
        "anchored": false,
        "mass": 0.5,
        "position": [
          -0.947932321584896,
          4.03853974184287,
          -1.5941257806914426
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

### 接口计数（h3-exp-d1-probe-2-degree）

cell-0-probe-2 连接几个声明关节？平行关节分别计数。

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
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-hub-joint",
        "name": "cell-0-hub interface",
        "parent": "cell-0-mount",
        "child": "cell-0-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.95,
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
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772927,
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
        "id": "cell-0-probe-1-joint",
        "name": "cell-0-probe-1 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-1",
        "type": "prismatic",
        "anchorParent": [
          -0.4999999999999998,
          1.2000000000000002,
          0.8660254037844387
        ],
        "anchorChild": [
          0.44793232158489493,
          -1.1885397418428698,
          -0.7281003769070041
        ],
        "axis": [
          -0.2999999999999999,
          0.8,
          0.5196152422706632
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-2-joint",
        "name": "cell-0-probe-2 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-2",
        "type": "prismatic",
        "anchorParent": [
          -0.5000000000000004,
          1.2000000000000002,
          -0.8660254037844385
        ],
        "anchorChild": [
          0.4479323215848956,
          -1.1885397418428698,
          0.7281003769070041
        ],
        "axis": [
          -0.30000000000000027,
          0.8,
          -0.519615242270663
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

### 局部改色（h3-exp-d1-probe-2-recolor）

仅将 cell-0-probe-2-p100 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-probe-2-p101","color":"#e8792e"}
- B：{"id":"cell-0-probe-2-p100","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"cell-0-probe-2-p100","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "cell-0-probe-2-p100",
      "moduleId": "cell-0-probe-2",
      "shape": "beam",
      "position": [
        0.33126565491822885,
        -0.8552064085095366,
        0.5260277826906352
      ],
      "size": [
        0.25,
        0.8137703743822469,
        0.25
      ],
      "color": "#e9ad37",
      "rotation": [
        -0.2603613446834222,
        0,
        0.15031969243954693,
        0.9537378886567945
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 补装部件（h3-exp-d1-probe-2-add）

模块 cell-0-probe-2 缺失零件 cell-0-probe-2-p100。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-probe-2-p100","moduleId":"cell-0-probe-2","shape":"beam","position":[0.33126565491822885,-0.8552064085095366,0.5260277826906352],"size":[0.25,0.8137703743822469,0.25],"color":"#e9ad37","rotation":[-0.2603613446834222,0,0.15031969243954693,0.9537378886567945]}
- B：{"id":"cell-0-probe-2-p100","moduleId":"foundation","shape":"beam","position":[0.33126565491822885,-0.8552064085095366,0.5260277826906352],"size":[0.25,0.8137703743822469,0.25],"color":"#e9ad37","rotation":[-0.2603613446834222,0,0.15031969243954693,0.9537378886567945]}
- C：{"id":"cell-0-probe-2-p100","moduleId":"cell-0-probe-2","shape":"beam","position":[0.33126565491822885,-0.8552064085095366,0.5260277826906352],"size":[3,3,3],"color":"#e9ad37","rotation":[-0.2603613446834222,0,0.15031969243954693,0.9537378886567945]}
- D：{"id":"cell-0-probe-2-p100","moduleId":"cell-0-probe-2","shape":"beam","position":[0.33126565491822885,-0.8552064085095366,0.5260277826906352],"size":[0.25,0.8137703743822469,0.25],"color":"#000000","rotation":[-0.2603613446834222,0,0.15031969243954693,0.9537378886567945]}

```json
{
  "input": {
    "targetPart": {
      "id": "cell-0-probe-2-p100",
      "moduleId": "cell-0-probe-2",
      "shape": "beam",
      "position": [
        0.33126565491822885,
        -0.8552064085095366,
        0.5260277826906352
      ],
      "size": [
        0.25,
        0.8137703743822469,
        0.25
      ],
      "color": "#e9ad37",
      "rotation": [
        -0.2603613446834222,
        0,
        0.15031969243954693,
        0.9537378886567945
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
      "cell-0-hub-p91",
      "cell-0-probe-0-p92",
      "cell-0-probe-0-p93",
      "cell-0-probe-0-p94",
      "cell-0-probe-0-p95",
      "cell-0-probe-1-p96",
      "cell-0-probe-1-p97",
      "cell-0-probe-1-p98",
      "cell-0-probe-1-p99",
      "cell-0-probe-2-p101",
      "cell-0-probe-2-p102",
      "cell-0-probe-2-p103"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全拆除（h3-exp-d1-probe-2-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["cell-0-probe-0","cell-0-probe-1","cell-0-probe-2"]
- B：["foundation"]
- C：[]
- D：["foundation","cell-0-mount","cell-0-hub","cell-0-probe-0","cell-0-probe-1","cell-0-probe-2"]

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
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-hub-joint",
        "name": "cell-0-hub interface",
        "parent": "cell-0-mount",
        "child": "cell-0-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.95,
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
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772927,
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
        "id": "cell-0-probe-1-joint",
        "name": "cell-0-probe-1 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-1",
        "type": "prismatic",
        "anchorParent": [
          -0.4999999999999998,
          1.2000000000000002,
          0.8660254037844387
        ],
        "anchorChild": [
          0.44793232158489493,
          -1.1885397418428698,
          -0.7281003769070041
        ],
        "axis": [
          -0.2999999999999999,
          0.8,
          0.5196152422706632
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-2-joint",
        "name": "cell-0-probe-2 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-2",
        "type": "prismatic",
        "anchorParent": [
          -0.5000000000000004,
          1.2000000000000002,
          -0.8660254037844385
        ],
        "anchorChild": [
          0.4479323215848956,
          -1.1885397418428698,
          0.7281003769070041
        ],
        "axis": [
          -0.30000000000000027,
          0.8,
          -0.519615242270663
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
      "cell-0-hub",
      "cell-0-probe-0",
      "cell-0-probe-1",
      "cell-0-probe-2"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 替换选择（h3-exp-d1-probe-2-replace）

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
        "cost": 6,
        "stiffness": 8,
        "mass": 0.5
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 8,
        "mass": 1.7
      },
      {
        "id": "stock-2",
        "cost": 2,
        "stiffness": 3,
        "mass": 1.4
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 9,
        "mass": 1.2
      }
    ],
    "maxCost": 8
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 平移纠偏（h3-exp-d1-probe-2-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[1,0,-2]
- B：[0,0,0]
- C：[0,2,0]
- D：[-1,0,2]

```json
{
  "input": {
    "delta": [
      1,
      0,
      -2
    ],
    "target": "cell-0-probe-2"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 姿态纠偏（h3-exp-d1-probe-2-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：0
- B：-180
- C：-90
- D：90

```json
{
  "input": {
    "module": "cell-0-probe-2",
    "currentYaw": 270,
    "targetYaw": 180
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 下一步放置（h3-exp-d1-probe-2-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["foundation","cell-0-mount","cell-0-hub"]
- B：["foundation"]
- C：["cell-0-probe-0","cell-0-probe-1","cell-0-probe-2"]
- D：[]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "cell-0-mount",
      "cell-0-hub"
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
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-hub-joint",
        "name": "cell-0-hub interface",
        "parent": "cell-0-mount",
        "child": "cell-0-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.95,
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
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772927,
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
        "id": "cell-0-probe-1-joint",
        "name": "cell-0-probe-1 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-1",
        "type": "prismatic",
        "anchorParent": [
          -0.4999999999999998,
          1.2000000000000002,
          0.8660254037844387
        ],
        "anchorChild": [
          0.44793232158489493,
          -1.1885397418428698,
          -0.7281003769070041
        ],
        "axis": [
          -0.2999999999999999,
          0.8,
          0.5196152422706632
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-2-joint",
        "name": "cell-0-probe-2 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-2",
        "type": "prismatic",
        "anchorParent": [
          -0.5000000000000004,
          1.2000000000000002,
          -0.8660254037844385
        ],
        "anchorChild": [
          0.4479323215848956,
          -1.1885397418428698,
          0.7281003769070041
        ],
        "axis": [
          -0.30000000000000027,
          0.8,
          -0.519615242270663
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
      "cell-0-hub",
      "cell-0-probe-0",
      "cell-0-probe-1",
      "cell-0-probe-2"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 库存核算（h3-exp-d1-probe-2-inventory）

备件库有 6 件，替换模块需 4 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：1
- B：5
- C：2
- D：3

```json
{
  "input": {
    "available": 6,
    "required": 4
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 子装配边界（h3-exp-d1-probe-2-boundary）

隔离 cell-0-probe-2 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：[]
- B：["cell-0-mount-joint","cell-0-hub-joint","cell-0-probe-0-joint","cell-0-probe-1-joint","cell-0-probe-2-joint"]
- C：["cell-0-probe-2-joint"]

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
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-hub-joint",
        "name": "cell-0-hub interface",
        "parent": "cell-0-mount",
        "child": "cell-0-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.95,
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
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772927,
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
        "id": "cell-0-probe-1-joint",
        "name": "cell-0-probe-1 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-1",
        "type": "prismatic",
        "anchorParent": [
          -0.4999999999999998,
          1.2000000000000002,
          0.8660254037844387
        ],
        "anchorChild": [
          0.44793232158489493,
          -1.1885397418428698,
          -0.7281003769070041
        ],
        "axis": [
          -0.2999999999999999,
          0.8,
          0.5196152422706632
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-2-joint",
        "name": "cell-0-probe-2 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-2",
        "type": "prismatic",
        "anchorParent": [
          -0.5000000000000004,
          1.2000000000000002,
          -0.8660254037844385
        ],
        "anchorChild": [
          0.4479323215848956,
          -1.1885397418428698,
          0.7281003769070041
        ],
        "axis": [
          -0.30000000000000027,
          0.8,
          -0.519615242270663
        ],
        "limits": [
          -0.45,
          0.45
        ]
      }
    ],
    "target": "cell-0-probe-2"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 最小干预（h3-exp-d1-probe-2-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：4
- D：0

```json
{
  "input": {
    "module": "cell-0-probe-2"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 全过程依赖（h3-exp-d1-probe-2-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：2
- B：-1
- C：3
- D：5

```json
{
  "input": {
    "order": [
      "foundation",
      "cell-0-mount",
      "cell-0-probe-0",
      "cell-0-hub",
      "cell-0-probe-1",
      "cell-0-probe-2"
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
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-hub-joint",
        "name": "cell-0-hub interface",
        "parent": "cell-0-mount",
        "child": "cell-0-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.95,
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
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772927,
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
        "id": "cell-0-probe-1-joint",
        "name": "cell-0-probe-1 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-1",
        "type": "prismatic",
        "anchorParent": [
          -0.4999999999999998,
          1.2000000000000002,
          0.8660254037844387
        ],
        "anchorChild": [
          0.44793232158489493,
          -1.1885397418428698,
          -0.7281003769070041
        ],
        "axis": [
          -0.2999999999999999,
          0.8,
          0.5196152422706632
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-2-joint",
        "name": "cell-0-probe-2 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-2",
        "type": "prismatic",
        "anchorParent": [
          -0.5000000000000004,
          1.2000000000000002,
          -0.8660254037844385
        ],
        "anchorChild": [
          0.4479323215848956,
          -1.1885397418428698,
          0.7281003769070041
        ],
        "axis": [
          -0.30000000000000027,
          0.8,
          -0.519615242270663
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

### 连续维修路径（h3-exp-d1-probe-2-access）

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
          7.98,
          4.03853974184287,
          -1.5941257806914426
        ],
        "end": [
          -0.9479323215848959,
          4.03853974184287,
          -1.5941257806914426
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
          -0.9479323215848959,
          9.325000000000001,
          -1.5941257806914426
        ],
        "end": [
          -0.9479323215848959,
          4.03853974184287,
          -1.5941257806914426
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
          -0.9479323215848959,
          4.03853974184287,
          7.48
        ],
        "end": [
          -0.9479323215848959,
          4.03853974184287,
          -1.5941257806914426
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.6002463102340698
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

### 支撑反事实（h3-exp-d1-probe-2-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["foundation","cell-0-mount","cell-0-hub","cell-0-probe-0","cell-0-probe-1","cell-0-probe-2"]
- B：["cell-0-hub","cell-0-probe-0","cell-0-probe-1","cell-0-probe-2"]
- C：["cell-0-mount"]
- D：[]

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
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-hub-joint",
        "name": "cell-0-hub interface",
        "parent": "cell-0-mount",
        "child": "cell-0-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.95,
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
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772927,
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
        "id": "cell-0-probe-1-joint",
        "name": "cell-0-probe-1 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-1",
        "type": "prismatic",
        "anchorParent": [
          -0.4999999999999998,
          1.2000000000000002,
          0.8660254037844387
        ],
        "anchorChild": [
          0.44793232158489493,
          -1.1885397418428698,
          -0.7281003769070041
        ],
        "axis": [
          -0.2999999999999999,
          0.8,
          0.5196152422706632
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-2-joint",
        "name": "cell-0-probe-2 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-2",
        "type": "prismatic",
        "anchorParent": [
          -0.5000000000000004,
          1.2000000000000002,
          -0.8660254037844385
        ],
        "anchorChild": [
          0.4479323215848956,
          -1.1885397418428698,
          0.7281003769070041
        ],
        "axis": [
          -0.30000000000000027,
          0.8,
          -0.519615242270663
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
      "cell-0-hub",
      "cell-0-probe-0",
      "cell-0-probe-1",
      "cell-0-probe-2"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 冲击响应读数（h3-exp-d1-probe-2-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：1.0143
- C：0.0143
- D：0.2143

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.014331449138378423
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0001279337855700553
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.00005855846184483468
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.00005854341387080424
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.00005854341387080424
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00005856237489803094
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.000058581390433943545
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.000058581390433943545
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.000058581390433943545
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.000058581390433943545
      },
      {
        "time": 1,
        "displacement": 0.000058581390433943545
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.000035599018906522977,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-exp-d1-probe-2-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：0.95
- B：-0.45
- C：0
- D：-0.95

```json
{
  "input": {
    "joint": "cell-0-probe-2-joint",
    "limits": [
      -0.45,
      0.45
    ],
    "units": "scene units"
  },
  "answer": {
    "choiceIds": [
      "B",
      "C"
    ]
  }
}
```

### 约束故障诊断（h3-exp-d1-probe-2-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：cell-0-probe-0-joint
- B：cell-0-probe-2-joint
- C：cell-0-mount-joint
- D：cell-0-hub-joint

```json
{
  "input": {
    "endpoints": [
      "cell-0-hub",
      "cell-0-probe-2"
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
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-hub-joint",
        "name": "cell-0-hub interface",
        "parent": "cell-0-mount",
        "child": "cell-0-hub",
        "type": "revolute",
        "anchorParent": [
          0,
          0.95,
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
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          1,
          1.2000000000000002,
          0
        ],
        "anchorChild": [
          -0.8362980049675599,
          -1.2016586034772927,
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
        "id": "cell-0-probe-1-joint",
        "name": "cell-0-probe-1 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-1",
        "type": "prismatic",
        "anchorParent": [
          -0.4999999999999998,
          1.2000000000000002,
          0.8660254037844387
        ],
        "anchorChild": [
          0.44793232158489493,
          -1.1885397418428698,
          -0.7281003769070041
        ],
        "axis": [
          -0.2999999999999999,
          0.8,
          0.5196152422706632
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-2-joint",
        "name": "cell-0-probe-2 interface",
        "parent": "cell-0-hub",
        "child": "cell-0-probe-2",
        "type": "prismatic",
        "anchorParent": [
          -0.5000000000000004,
          1.2000000000000002,
          -0.8660254037844385
        ],
        "anchorChild": [
          0.4479323215848956,
          -1.1885397418428698,
          0.7281003769070041
        ],
        "axis": [
          -0.30000000000000027,
          0.8,
          -0.519615242270663
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
      "B"
    ]
  }
}
```

### 主动检查收益（h3-exp-d1-probe-2-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-1
- B：query-0
- C：query-2

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
    "module": "cell-0-probe-2",
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

### 不确定性与弃答（h3-exp-d1-probe-2-abstention）

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

### 观测后信念更新（h3-exp-d1-probe-2-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.3333333333333333
- B：0
- C：0.25
- D：0.5

```json
{
  "input": {
    "module": "cell-0-probe-2",
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
    "choiceId": "A"
  }
}
```

### 多目标工程权衡（h3-exp-d1-probe-2-pareto）

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
        "stiffness": 8,
        "mass": 0.5
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 8,
        "mass": 1.7
      },
      {
        "id": "stock-2",
        "cost": 2,
        "stiffness": 3,
        "mass": 1.4
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 9,
        "mass": 1.2
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "B",
      "C",
      "D"
    ]
  }
}
```

### 依赖装配（h3-exp-d1-probe-2-assembly）

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
        "id": "place:cell-0-hub",
        "label": "安装 cell-0-hub",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-hub"
        ],
        "adds": [
          "present:cell-0-hub"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-hub",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-probe-2",
        "label": "安装 cell-0-probe-2",
        "requires": [
          "present:cell-0-hub"
        ],
        "forbids": [
          "present:cell-0-probe-2"
        ],
        "adds": [
          "present:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-probe-1",
        "label": "安装 cell-0-probe-1",
        "requires": [
          "present:cell-0-hub"
        ],
        "forbids": [
          "present:cell-0-probe-1"
        ],
        "adds": [
          "present:cell-0-probe-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-1",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-probe-0",
        "label": "安装 cell-0-probe-0",
        "requires": [
          "present:cell-0-hub"
        ],
        "forbids": [
          "present:cell-0-probe-0"
        ],
        "adds": [
          "present:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:cell-0-mount",
      "present:cell-0-hub",
      "present:cell-0-probe-0",
      "present:cell-0-probe-1",
      "present:cell-0-probe-2"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:cell-0-mount",
      "place:cell-0-hub",
      "place:cell-0-probe-2",
      "place:cell-0-probe-1",
      "place:cell-0-probe-0"
    ]
  }
}
```

### 依赖拆解（h3-exp-d1-probe-2-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:cell-0-mount",
      "present:cell-0-hub",
      "present:cell-0-probe-0",
      "present:cell-0-probe-1",
      "present:cell-0-probe-2"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-hub",
      "cell-0-probe-0",
      "cell-0-probe-1",
      "cell-0-probe-2"
    ],
    "actions": [
      {
        "id": "remove:cell-0-mount",
        "label": "拆除 cell-0-mount",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-hub"
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
        "id": "remove:cell-0-probe-2",
        "label": "拆除 cell-0-probe-2",
        "requires": [
          "present:cell-0-probe-2"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-probe-2"
        ],
        "deletes": [
          "present:cell-0-probe-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-hub",
        "label": "拆除 cell-0-hub",
        "requires": [
          "present:cell-0-hub"
        ],
        "forbids": [
          "present:cell-0-probe-0",
          "present:cell-0-probe-1",
          "present:cell-0-probe-2"
        ],
        "adds": [
          "removed:cell-0-hub"
        ],
        "deletes": [
          "present:cell-0-hub"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-hub",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-probe-1",
        "label": "拆除 cell-0-probe-1",
        "requires": [
          "present:cell-0-probe-1"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-probe-1"
        ],
        "deletes": [
          "present:cell-0-probe-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-1",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-probe-0",
        "label": "拆除 cell-0-probe-0",
        "requires": [
          "present:cell-0-probe-0"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-probe-0"
        ],
        "deletes": [
          "present:cell-0-probe-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:cell-0-probe-2",
      "removed:cell-0-probe-1",
      "removed:cell-0-probe-0",
      "removed:cell-0-hub",
      "removed:cell-0-mount",
      "removed:foundation"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:cell-0-probe-2",
      "remove:cell-0-probe-1",
      "remove:cell-0-probe-0",
      "remove:cell-0-hub",
      "remove:cell-0-mount",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-exp-d1-probe-2-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-probe-2",
      "closed:cell-0-probe-2"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-hub",
      "cell-0-probe-0",
      "cell-0-probe-1",
      "cell-0-probe-2"
    ],
    "actions": [
      {
        "id": "support:cell-0-probe-2",
        "label": "support cell-0-probe-2",
        "requires": [
          "fault:cell-0-probe-2"
        ],
        "forbids": [
          "done:support:cell-0-probe-2"
        ],
        "adds": [
          "done:support:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "close:cell-0-probe-2",
        "label": "close cell-0-probe-2",
        "requires": [
          "done:verify:cell-0-probe-2"
        ],
        "forbids": [
          "done:close:cell-0-probe-2"
        ],
        "adds": [
          "done:close:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "verify:cell-0-probe-2",
        "label": "verify cell-0-probe-2",
        "requires": [
          "done:replace:cell-0-probe-2"
        ],
        "forbids": [
          "done:verify:cell-0-probe-2"
        ],
        "adds": [
          "done:verify:cell-0-probe-2"
        ],
        "deletes": [
          "fault:cell-0-probe-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "remove:cell-0-probe-2",
        "label": "remove cell-0-probe-2",
        "requires": [
          "done:open:cell-0-probe-2"
        ],
        "forbids": [
          "done:remove:cell-0-probe-2"
        ],
        "adds": [
          "done:remove:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2",
          "visible": false
        }
      },
      {
        "id": "replace:cell-0-probe-2",
        "label": "replace cell-0-probe-2",
        "requires": [
          "done:remove:cell-0-probe-2"
        ],
        "forbids": [
          "done:replace:cell-0-probe-2"
        ],
        "adds": [
          "done:replace:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2",
          "visible": true
        }
      },
      {
        "id": "release:cell-0-probe-2",
        "label": "release cell-0-probe-2",
        "requires": [
          "done:close:cell-0-probe-2"
        ],
        "forbids": [
          "done:release:cell-0-probe-2"
        ],
        "adds": [
          "done:release:cell-0-probe-2",
          "repaired:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "open:cell-0-probe-2",
        "label": "open cell-0-probe-2",
        "requires": [
          "done:support:cell-0-probe-2"
        ],
        "forbids": [
          "done:open:cell-0-probe-2"
        ],
        "adds": [
          "done:open:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-probe-2"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-probe-2",
      "open:cell-0-probe-2",
      "remove:cell-0-probe-2",
      "replace:cell-0-probe-2",
      "verify:cell-0-probe-2",
      "close:cell-0-probe-2",
      "release:cell-0-probe-2"
    ]
  }
}
```

### 复合编辑验证（h3-exp-d1-probe-2-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-probe-2",
      "closed:cell-0-probe-2"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-hub",
      "cell-0-probe-0",
      "cell-0-probe-1",
      "cell-0-probe-2"
    ],
    "actions": [
      {
        "id": "support:cell-0-probe-2",
        "label": "support cell-0-probe-2",
        "requires": [
          "fault:cell-0-probe-2"
        ],
        "forbids": [
          "done:support:cell-0-probe-2"
        ],
        "adds": [
          "done:support:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "close:cell-0-probe-2",
        "label": "close cell-0-probe-2",
        "requires": [
          "done:verify:cell-0-probe-2"
        ],
        "forbids": [
          "done:close:cell-0-probe-2"
        ],
        "adds": [
          "done:close:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "verify:cell-0-probe-2",
        "label": "verify cell-0-probe-2",
        "requires": [
          "done:recolor:cell-0-probe-2"
        ],
        "forbids": [
          "done:verify:cell-0-probe-2"
        ],
        "adds": [
          "done:verify:cell-0-probe-2"
        ],
        "deletes": [
          "fault:cell-0-probe-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "release:cell-0-probe-2",
        "label": "release cell-0-probe-2",
        "requires": [
          "done:close:cell-0-probe-2"
        ],
        "forbids": [
          "done:release:cell-0-probe-2"
        ],
        "adds": [
          "done:release:cell-0-probe-2",
          "repaired:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "recolor:cell-0-probe-2",
        "label": "recolor cell-0-probe-2",
        "requires": [
          "done:open:cell-0-probe-2"
        ],
        "forbids": [
          "done:recolor:cell-0-probe-2"
        ],
        "adds": [
          "done:recolor:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2",
          "color": "#ea7635"
        }
      },
      {
        "id": "open:cell-0-probe-2",
        "label": "open cell-0-probe-2",
        "requires": [
          "done:support:cell-0-probe-2"
        ],
        "forbids": [
          "done:open:cell-0-probe-2"
        ],
        "adds": [
          "done:open:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-probe-2"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-probe-2",
      "open:cell-0-probe-2",
      "recolor:cell-0-probe-2",
      "verify:cell-0-probe-2",
      "close:cell-0-probe-2",
      "release:cell-0-probe-2"
    ]
  }
}
```

### 跨区域联合维修（h3-exp-d1-probe-2-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-probe-2",
      "closed:cell-0-probe-2"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-hub",
      "cell-0-probe-0",
      "cell-0-probe-1",
      "cell-0-probe-2"
    ],
    "actions": [
      {
        "id": "support:cell-0-probe-2",
        "label": "support cell-0-probe-2",
        "requires": [
          "fault:cell-0-probe-2"
        ],
        "forbids": [
          "done:support:cell-0-probe-2"
        ],
        "adds": [
          "done:support:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "close:cell-0-probe-2",
        "label": "close cell-0-probe-2",
        "requires": [
          "done:verify:cell-0-probe-2"
        ],
        "forbids": [
          "done:close:cell-0-probe-2"
        ],
        "adds": [
          "done:close:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "verify:cell-0-probe-2",
        "label": "verify cell-0-probe-2",
        "requires": [
          "done:replace:cell-0-probe-2"
        ],
        "forbids": [
          "done:verify:cell-0-probe-2"
        ],
        "adds": [
          "done:verify:cell-0-probe-2"
        ],
        "deletes": [
          "fault:cell-0-probe-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "remove:cell-0-probe-2",
        "label": "remove cell-0-probe-2",
        "requires": [
          "done:open:cell-0-probe-2"
        ],
        "forbids": [
          "done:remove:cell-0-probe-2"
        ],
        "adds": [
          "done:remove:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2",
          "visible": false
        }
      },
      {
        "id": "replace:cell-0-probe-2",
        "label": "replace cell-0-probe-2",
        "requires": [
          "done:remove:cell-0-probe-2"
        ],
        "forbids": [
          "done:replace:cell-0-probe-2"
        ],
        "adds": [
          "done:replace:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2",
          "visible": true
        }
      },
      {
        "id": "release:cell-0-probe-2",
        "label": "release cell-0-probe-2",
        "requires": [
          "done:close:cell-0-probe-2"
        ],
        "forbids": [
          "done:release:cell-0-probe-2"
        ],
        "adds": [
          "done:release:cell-0-probe-2",
          "repaired:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "open:cell-0-probe-2",
        "label": "open cell-0-probe-2",
        "requires": [
          "done:support:cell-0-probe-2"
        ],
        "forbids": [
          "done:open:cell-0-probe-2"
        ],
        "adds": [
          "done:open:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-probe-2"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-probe-2",
      "open:cell-0-probe-2",
      "remove:cell-0-probe-2",
      "replace:cell-0-probe-2",
      "verify:cell-0-probe-2",
      "close:cell-0-probe-2",
      "release:cell-0-probe-2"
    ]
  }
}
```

### 多工位资源调度（h3-exp-d1-probe-2-scheduling）

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
        "module": "cell-0-hub",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "cell-0-probe-0",
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

### 检查后条件策略（h3-exp-d1-probe-2-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-probe-2",
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

### 局部坐标变换（h3-exp-d1-probe-2-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[0.38333,3.18333,-1.0681]
- B：[-1.2792,4.18333,-1.1201500000000002]
- C：[-2.2792,3.18333,-2.12015]
- D：[1.33127,-0.85521,0.52603]

```json
{
  "input": {
    "localPoint": [
      1.331265654918229,
      -0.8552064085095366,
      0.5260277826906352
    ],
    "rotationXYZW": [
      0,
      1,
      0,
      6.123233995736766e-17
    ],
    "translation": [
      -0.947932321584896,
      4.03853974184287,
      -1.5941257806914426
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-exp-d1-probe-2-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[5,2]
- B：[2,3]
- C：[0,0]
- D：[2,-3]

```json
{
  "input": {
    "view": "top",
    "point": [
      2,
      5,
      -3
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 空间相对关系（h3-exp-d1-probe-2-relative-order）

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
      "id": "cell-0-probe-2",
      "position": [
        -0.947932321584896,
        4.03853974184287,
        -1.5941257806914426
      ]
    },
    "axis": "z"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 约束自由度（h3-exp-d1-probe-2-joint-axis）

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
      "id": "cell-0-probe-0-joint",
      "name": "cell-0-probe-0 interface",
      "parent": "cell-0-hub",
      "child": "cell-0-probe-0",
      "type": "prismatic",
      "anchorParent": [
        1,
        1.2000000000000002,
        0
      ],
      "anchorChild": [
        -0.8362980049675599,
        -1.2016586034772927,
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
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 维修间隙预算（h3-exp-d1-probe-2-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "cell-0-probe-2",
    "aperture": 0.5,
    "toolWidth": 0.35,
    "eachSideMargin": 0.1
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-exp-d1-probe-2-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,4]
- B：[0,0,0]
- C：[0,-1,0]
- D：[0,0,-4]

```json
{
  "input": {
    "module": "cell-0-probe-2",
    "lever": [
      1,
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

### 非均匀先验更新（h3-exp-d1-probe-2-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.7
- B：0.5833333333333334
- C：0
- D：1

```json
{
  "input": {
    "module": "cell-0-probe-2",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      3,
      7,
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

### 风险最小决策（h3-exp-d1-probe-2-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.7,
    "repairCost": 7,
    "failureLoss": 7,
    "module": "cell-0-probe-2"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-exp-d1-probe-2-trace-threshold）

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
        "displacement": 0.014331449138378423
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0001279337855700553
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.00005855846184483468
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.00005854341387080424
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.00005854341387080424
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00005856237489803094
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.000058581390433943545
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.000058581390433943545
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.000058581390433943545
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.000058581390433943545
      },
      {
        "time": 1,
        "displacement": 0.000058581390433943545
      }
    ],
    "threshold": 0.011465159310702739
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-exp-d1-probe-2-guarded-repair）

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
        "id": "release:cell-0-probe-2",
        "label": "release cell-0-probe-2",
        "requires": [
          "done:relock:cell-0-probe-2"
        ],
        "forbids": [
          "done:release:cell-0-probe-2"
        ],
        "adds": [
          "done:release:cell-0-probe-2",
          "ready:cell-0-probe-2",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "relock:cell-0-probe-2",
        "label": "relock cell-0-probe-2",
        "requires": [
          "done:verify:cell-0-probe-2"
        ],
        "forbids": [
          "done:relock:cell-0-probe-2"
        ],
        "adds": [
          "done:relock:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "verify:cell-0-probe-2",
        "label": "verify cell-0-probe-2",
        "requires": [
          "done:replace:cell-0-probe-2"
        ],
        "forbids": [
          "done:verify:cell-0-probe-2"
        ],
        "adds": [
          "done:verify:cell-0-probe-2"
        ],
        "deletes": [
          "fault:cell-0-probe-2",
          "misaligned:cell-0-probe-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "replace:cell-0-probe-2",
        "label": "replace cell-0-probe-2",
        "requires": [
          "done:unlock:cell-0-probe-2"
        ],
        "forbids": [
          "done:replace:cell-0-probe-2"
        ],
        "adds": [
          "done:replace:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "unlock:cell-0-probe-2",
        "label": "unlock cell-0-probe-2",
        "requires": [
          "done:support:cell-0-probe-2"
        ],
        "forbids": [
          "done:unlock:cell-0-probe-2"
        ],
        "adds": [
          "done:unlock:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "support:cell-0-probe-2",
        "label": "support cell-0-probe-2",
        "requires": [
          "done:isolate:cell-0-probe-2"
        ],
        "forbids": [
          "done:support:cell-0-probe-2"
        ],
        "adds": [
          "done:support:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "isolate:cell-0-probe-2",
        "label": "isolate cell-0-probe-2",
        "requires": [
          "tool:free",
          "fault:cell-0-probe-2"
        ],
        "forbids": [
          "done:isolate:cell-0-probe-2"
        ],
        "adds": [
          "done:isolate:cell-0-probe-2"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-probe-2"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-hub",
      "cell-0-probe-0",
      "cell-0-probe-1",
      "cell-0-probe-2"
    ],
    "goalFacts": [
      "ready:cell-0-probe-2"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-probe-2",
      "support:cell-0-probe-2",
      "unlock:cell-0-probe-2",
      "replace:cell-0-probe-2",
      "verify:cell-0-probe-2",
      "relock:cell-0-probe-2",
      "release:cell-0-probe-2"
    ]
  }
}
```

### 失败状态回退（h3-exp-d1-probe-2-rollback）

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
        "id": "resume:cell-0-probe-2",
        "label": "resume cell-0-probe-2",
        "requires": [
          "done:verify:cell-0-probe-2"
        ],
        "forbids": [
          "done:resume:cell-0-probe-2"
        ],
        "adds": [
          "done:resume:cell-0-probe-2",
          "ready:cell-0-probe-2",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "verify:cell-0-probe-2",
        "label": "verify cell-0-probe-2",
        "requires": [
          "done:align:cell-0-probe-2"
        ],
        "forbids": [
          "done:verify:cell-0-probe-2"
        ],
        "adds": [
          "done:verify:cell-0-probe-2"
        ],
        "deletes": [
          "fault:cell-0-probe-2",
          "misaligned:cell-0-probe-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "align:cell-0-probe-2",
        "label": "align cell-0-probe-2",
        "requires": [
          "done:undo:cell-0-probe-2"
        ],
        "forbids": [
          "done:align:cell-0-probe-2"
        ],
        "adds": [
          "done:align:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2",
          "visible": true
        }
      },
      {
        "id": "undo:cell-0-probe-2",
        "label": "undo cell-0-probe-2",
        "requires": [
          "done:isolate:cell-0-probe-2"
        ],
        "forbids": [
          "done:undo:cell-0-probe-2"
        ],
        "adds": [
          "done:undo:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2",
          "visible": false
        }
      },
      {
        "id": "isolate:cell-0-probe-2",
        "label": "isolate cell-0-probe-2",
        "requires": [
          "tool:free",
          "fault:cell-0-probe-2"
        ],
        "forbids": [
          "done:isolate:cell-0-probe-2"
        ],
        "adds": [
          "done:isolate:cell-0-probe-2"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-probe-2",
      "misaligned:cell-0-probe-2"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-hub",
      "cell-0-probe-0",
      "cell-0-probe-1",
      "cell-0-probe-2"
    ],
    "goalFacts": [
      "ready:cell-0-probe-2"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-probe-2",
      "undo:cell-0-probe-2",
      "align:cell-0-probe-2",
      "verify:cell-0-probe-2",
      "resume:cell-0-probe-2"
    ]
  }
}
```

### 共享工具协同维修（h3-exp-d1-probe-2-resource-repair）

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
        "id": "release:cell-0-probe-2",
        "label": "release cell-0-probe-2",
        "requires": [
          "done:relock:cell-0-probe-2"
        ],
        "forbids": [
          "done:release:cell-0-probe-2"
        ],
        "adds": [
          "done:release:cell-0-probe-2",
          "ready:cell-0-probe-2",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "relock:cell-0-probe-2",
        "label": "relock cell-0-probe-2",
        "requires": [
          "done:verify:cell-0-probe-2"
        ],
        "forbids": [
          "done:relock:cell-0-probe-2"
        ],
        "adds": [
          "done:relock:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "verify:cell-0-probe-2",
        "label": "verify cell-0-probe-2",
        "requires": [
          "done:replace:cell-0-probe-2"
        ],
        "forbids": [
          "done:verify:cell-0-probe-2"
        ],
        "adds": [
          "done:verify:cell-0-probe-2"
        ],
        "deletes": [
          "fault:cell-0-probe-2",
          "misaligned:cell-0-probe-2"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "replace:cell-0-probe-2",
        "label": "replace cell-0-probe-2",
        "requires": [
          "done:unlock:cell-0-probe-2"
        ],
        "forbids": [
          "done:replace:cell-0-probe-2"
        ],
        "adds": [
          "done:replace:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "unlock:cell-0-probe-2",
        "label": "unlock cell-0-probe-2",
        "requires": [
          "done:support:cell-0-probe-2"
        ],
        "forbids": [
          "done:unlock:cell-0-probe-2"
        ],
        "adds": [
          "done:unlock:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "support:cell-0-probe-2",
        "label": "support cell-0-probe-2",
        "requires": [
          "done:isolate:cell-0-probe-2"
        ],
        "forbids": [
          "done:support:cell-0-probe-2"
        ],
        "adds": [
          "done:support:cell-0-probe-2"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "isolate:cell-0-probe-2",
        "label": "isolate cell-0-probe-2",
        "requires": [
          "tool:free",
          "fault:cell-0-probe-2"
        ],
        "forbids": [
          "done:isolate:cell-0-probe-2"
        ],
        "adds": [
          "done:isolate:cell-0-probe-2"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-2"
        }
      },
      {
        "id": "release:cell-0-probe-1",
        "label": "release cell-0-probe-1",
        "requires": [
          "done:relock:cell-0-probe-1"
        ],
        "forbids": [
          "done:release:cell-0-probe-1"
        ],
        "adds": [
          "done:release:cell-0-probe-1",
          "ready:cell-0-probe-1",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-1"
        }
      },
      {
        "id": "relock:cell-0-probe-1",
        "label": "relock cell-0-probe-1",
        "requires": [
          "done:verify:cell-0-probe-1"
        ],
        "forbids": [
          "done:relock:cell-0-probe-1"
        ],
        "adds": [
          "done:relock:cell-0-probe-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-1"
        }
      },
      {
        "id": "verify:cell-0-probe-1",
        "label": "verify cell-0-probe-1",
        "requires": [
          "done:replace:cell-0-probe-1"
        ],
        "forbids": [
          "done:verify:cell-0-probe-1"
        ],
        "adds": [
          "done:verify:cell-0-probe-1"
        ],
        "deletes": [
          "fault:cell-0-probe-1",
          "misaligned:cell-0-probe-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-1"
        }
      },
      {
        "id": "replace:cell-0-probe-1",
        "label": "replace cell-0-probe-1",
        "requires": [
          "done:unlock:cell-0-probe-1"
        ],
        "forbids": [
          "done:replace:cell-0-probe-1"
        ],
        "adds": [
          "done:replace:cell-0-probe-1"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-probe-1"
        }
      },
      {
        "id": "unlock:cell-0-probe-1",
        "label": "unlock cell-0-probe-1",
        "requires": [
          "done:support:cell-0-probe-1"
        ],
        "forbids": [
          "done:unlock:cell-0-probe-1"
        ],
        "adds": [
          "done:unlock:cell-0-probe-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-1"
        }
      },
      {
        "id": "support:cell-0-probe-1",
        "label": "support cell-0-probe-1",
        "requires": [
          "done:isolate:cell-0-probe-1"
        ],
        "forbids": [
          "done:support:cell-0-probe-1"
        ],
        "adds": [
          "done:support:cell-0-probe-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-1"
        }
      },
      {
        "id": "isolate:cell-0-probe-1",
        "label": "isolate cell-0-probe-1",
        "requires": [
          "tool:free",
          "fault:cell-0-probe-1"
        ],
        "forbids": [
          "done:isolate:cell-0-probe-1"
        ],
        "adds": [
          "done:isolate:cell-0-probe-1"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-1"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-probe-1",
      "fault:cell-0-probe-2"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-hub",
      "cell-0-probe-0",
      "cell-0-probe-1",
      "cell-0-probe-2"
    ],
    "goalFacts": [
      "ready:cell-0-probe-1",
      "ready:cell-0-probe-2"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 16
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-probe-2",
      "support:cell-0-probe-2",
      "unlock:cell-0-probe-2",
      "replace:cell-0-probe-2",
      "verify:cell-0-probe-2",
      "relock:cell-0-probe-2",
      "release:cell-0-probe-2",
      "isolate:cell-0-probe-1",
      "support:cell-0-probe-1",
      "unlock:cell-0-probe-1",
      "replace:cell-0-probe-1",
      "verify:cell-0-probe-1",
      "relock:cell-0-probe-1",
      "release:cell-0-probe-1"
    ]
  }
}
```

### 预算约束检查策略（h3-exp-d1-probe-2-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-probe-2",
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
        "cost": 0,
        "returns": {
          "nominal": "pass",
          "fault": "pass"
        }
      },
      {
        "id": "thermal",
        "cost": 4,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      }
    ],
    "budget": 3
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
