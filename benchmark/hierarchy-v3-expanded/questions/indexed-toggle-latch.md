## D1 双轴索引锁扣

### 模块识别（h3-indexed-toggle-latch-identify）

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
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 部件计数（h3-indexed-toggle-latch-count）

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
        "id": "rail-0-p17",
        "moduleId": "rail-0",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "carriage-0-p18",
        "moduleId": "carriage-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-0-p19",
        "moduleId": "carriage-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-0-p20",
        "moduleId": "carriage-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "carriage-0-p21",
        "moduleId": "carriage-0",
        "shape": "plate",
        "color": "#387bb3"
      },
      {
        "id": "turret-0-p22",
        "moduleId": "turret-0",
        "shape": "cylinder",
        "color": "#e9ad37"
      },
      {
        "id": "elbow-0-p23",
        "moduleId": "elbow-0",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "head-0-p24",
        "moduleId": "head-0",
        "shape": "arch",
        "color": "#45a080"
      },
      {
        "id": "head-0-p25",
        "moduleId": "head-0",
        "shape": "panel",
        "color": "#dfebed"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-indexed-toggle-latch-color）

零件 head-0-p24 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#d43a32
- B：#f2bf3c
- C：#45a080
- D：#2878b8

```json
{
  "input": {
    "part": {
      "id": "head-0-p24",
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
    "choiceId": "C"
  }
}
```

### 三维位置（h3-indexed-toggle-latch-position）

模块 head-0 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,0.35,0]
- B：[0,1,0]
- C：[0,1.5499999999999998,0]
- D：[0,4.7875,0]

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
        0,
        1,
        0
      ],
      "carriage-0": [
        0,
        1.5499999999999998,
        0
      ],
      "turret-0": [
        0,
        2.2,
        0
      ],
      "elbow-0": [
        0,
        3.45,
        0
      ],
      "head-0": [
        0,
        4.7875,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节类型（h3-indexed-toggle-latch-joint-type）

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

### 直接连接（h3-indexed-toggle-latch-parent）

head-0 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["head-0"]
- B：[]
- C：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0"]
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
          -0.8,
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
          1.2499999999999993,
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
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 基座识别（h3-indexed-toggle-latch-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["frame"]
- B：[]
- C：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0"]
- D：["head-0"]

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
        "id": "carriage-0",
        "name": "carriage 0",
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
        "id": "turret-0",
        "name": "turret 0",
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
        "id": "elbow-0",
        "name": "elbow 0",
        "role": "linkage",
        "position": [
          0,
          3.45,
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
          0,
          4.7875,
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
    "choiceId": "A"
  }
}
```

### 接口计数（h3-indexed-toggle-latch-degree）

head-0 连接几个声明关节？平行关节分别计数。

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
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
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
          -0.8,
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
          1.2499999999999993,
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
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 局部改色（h3-indexed-toggle-latch-recolor）

仅将 head-0-p24 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"head-0-p24","color":"#e8792e"}
- B：{"id":"head-0-p25","color":"#e8792e"}
- C：{"id":"head-0-p24","color":"#2878b8"}
- D：{"id":"*","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "head-0-p24",
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

### 补装部件（h3-indexed-toggle-latch-add）

模块 head-0 缺失零件 head-0-p24。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"head-0-p24","moduleId":"head-0","shape":"arch","position":[0,-0.08750000000000002,0],"size":[1.6,0.7,1],"color":"#45a080","rotation":[0,0,0,1]}
- B：{"id":"head-0-p24","moduleId":"frame","shape":"arch","position":[0,-0.08750000000000002,0],"size":[1.6,0.7,1],"color":"#45a080","rotation":[0,0,0,1]}
- C：{"id":"head-0-p24","moduleId":"head-0","shape":"arch","position":[0,-0.08750000000000002,0],"size":[3,3,3],"color":"#45a080","rotation":[0,0,0,1]}
- D：{"id":"head-0-p24","moduleId":"head-0","shape":"arch","position":[0,-0.08750000000000002,0],"size":[1.6,0.7,1],"color":"#000000","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "head-0-p24",
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
      "rail-0-p17",
      "carriage-0-p18",
      "carriage-0-p19",
      "carriage-0-p20",
      "carriage-0-p21",
      "turret-0-p22",
      "elbow-0-p23",
      "head-0-p25"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全拆除（h3-indexed-toggle-latch-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0"]
- B：["head-0"]
- C：["frame"]
- D：[]

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
          -0.8,
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
          1.2499999999999993,
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
      }
    ],
    "modules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 替换选择（h3-indexed-toggle-latch-replace）

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
        "cost": 4,
        "stiffness": 11,
        "mass": 1.8
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 8,
        "mass": 1.2
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 11,
        "mass": 0.5
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 8,
        "mass": 1
      }
    ],
    "maxCost": 7
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-indexed-toggle-latch-translate）

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
    "target": "head-0"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 姿态纠偏（h3-indexed-toggle-latch-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：135
- B：-135
- C：0
- D：90

```json
{
  "input": {
    "module": "head-0",
    "currentYaw": 315,
    "targetYaw": 90
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 下一步放置（h3-indexed-toggle-latch-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["frame","rail-0","carriage-0"]
- B：["turret-0","elbow-0","head-0"]
- C：["turret-0"]
- D：[]

```json
{
  "input": {
    "prefix": [
      "frame",
      "rail-0",
      "carriage-0"
    ],
    "joints": [
      {
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
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
          -0.8,
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
          1.2499999999999993,
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
      }
    ],
    "modules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 库存核算（h3-indexed-toggle-latch-inventory）

备件库有 3 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：0
- B：4
- C：1
- D：2

```json
{
  "input": {
    "available": 3,
    "required": 2
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 子装配边界（h3-indexed-toggle-latch-boundary）

隔离 head-0 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["head-0-joint"]
- B：[]
- C：["rail-0-joint","carriage-0-joint","turret-0-joint","elbow-0-joint","head-0-joint"]
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
          -0.8,
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
          1.2499999999999993,
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
      }
    ],
    "target": "head-0"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 最小干预（h3-indexed-toggle-latch-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：2
- B：0
- C：1

```json
{
  "input": {
    "module": "head-0"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 全过程依赖（h3-indexed-toggle-latch-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：0
- B：5
- C：-1

```json
{
  "input": {
    "order": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0"
    ],
    "joints": [
      {
        "id": "rail-0-joint",
        "name": "rail-0 interface",
        "parent": "frame",
        "child": "rail-0",
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
          -0.8,
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
          1.2499999999999993,
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
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 连续维修路径（h3-indexed-toggle-latch-access）

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
          5.99,
          4.7875,
          0
        ],
        "end": [
          0,
          4.7875,
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
          9.225,
          0
        ],
        "end": [
          0,
          4.7875,
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
          4.7875,
          6
        ],
        "end": [
          0,
          4.7875,
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

### 支撑反事实（h3-indexed-toggle-latch-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["carriage-0","elbow-0","head-0","turret-0"]
- B：["rail-0"]
- C：[]
- D：["frame","rail-0","carriage-0","turret-0","elbow-0","head-0"]

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
          -0.8,
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
          1.2499999999999993,
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
      }
    ],
    "modules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 冲击响应读数（h3-indexed-toggle-latch-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.0136
- B：0.2136
- C：0
- D：1.0136

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.013644105944877975
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0018448874713113104
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0007767834500269035
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.00001614783264634752
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.000055069442628290124
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.000005971426178550001
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.000003045380935857501
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0000015751849105437823
      },
      {
        "time": 0.8083333333333333,
        "displacement": 2.4663381733245223e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 2.4663381733245223e-7
      },
      {
        "time": 1,
        "displacement": 2.4663381733245223e-7
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.0000020980834962713857,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节限位推理（h3-indexed-toggle-latch-kinematic）

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

### 约束故障诊断（h3-indexed-toggle-latch-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：turret-0-joint
- B：head-0-joint
- C：rail-0-joint
- D：carriage-0-joint

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
          -0.8,
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
          1.2499999999999993,
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

### 主动检查收益（h3-indexed-toggle-latch-information-gain）

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
      "B"
    ]
  }
}
```

### 不确定性与弃答（h3-indexed-toggle-latch-abstention）

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

### 观测后信念更新（h3-indexed-toggle-latch-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0
- C：0.25
- D：0.3333333333333333

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
      "positive",
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

### 多目标工程权衡（h3-indexed-toggle-latch-pareto）

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
        "cost": 4,
        "stiffness": 11,
        "mass": 1.8
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 8,
        "mass": 1.2
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 11,
        "mass": 0.5
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 8,
        "mass": 1
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

### 依赖装配（h3-indexed-toggle-latch-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
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
      }
    ],
    "goalFacts": [
      "present:frame",
      "present:rail-0",
      "present:carriage-0",
      "present:turret-0",
      "present:elbow-0",
      "present:head-0"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:frame",
      "place:rail-0",
      "place:carriage-0",
      "place:turret-0",
      "place:elbow-0",
      "place:head-0"
    ]
  }
}
```

### 依赖拆解（h3-indexed-toggle-latch-disassembly）

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
      "present:head-0"
    ],
    "initialModules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0"
    ],
    "actions": [
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
        "id": "remove:frame",
        "label": "拆除 frame",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:rail-0"
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
        "id": "remove:head-0",
        "label": "拆除 head-0",
        "requires": [
          "present:head-0"
        ],
        "forbids": [],
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
      }
    ],
    "goalFacts": [
      "removed:head-0",
      "removed:elbow-0",
      "removed:turret-0",
      "removed:carriage-0",
      "removed:rail-0",
      "removed:frame"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:head-0",
      "remove:elbow-0",
      "remove:turret-0",
      "remove:carriage-0",
      "remove:rail-0",
      "remove:frame"
    ]
  }
}
```

### 承载维修（h3-indexed-toggle-latch-service-repair）

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
      "head-0"
    ],
    "actions": [
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

### 复合编辑验证（h3-indexed-toggle-latch-compound-edit）

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
      "head-0"
    ],
    "actions": [
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

### 跨区域联合维修（h3-indexed-toggle-latch-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


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
      "head-0"
    ],
    "actions": [
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

### 多工位资源调度（h3-indexed-toggle-latch-scheduling）

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
      }
    ],
    "deadline": 5
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 2,
      "job-3": 1
    }
  }
}
```

### 检查后条件策略（h3-indexed-toggle-latch-policy）

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

### 局部坐标变换（h3-indexed-toggle-latch-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[0,4.7,1]
- B：[1,-0.0875,0]
- C：[1,4.7,0]
- D：[1,5.7,2]

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
      0.7071067811865476,
      0,
      -0.7071067811865475
    ],
    "translation": [
      0,
      4.7875,
      0
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 正交视图投影（h3-indexed-toggle-latch-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[0,0]
- B：[-3,5]
- C：[5,2]
- D：[2,3]

```json
{
  "input": {
    "view": "side",
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

### 空间相对关系（h3-indexed-toggle-latch-relative-order）

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
      "id": "head-0",
      "position": [
        0,
        4.7875,
        0
      ]
    },
    "axis": "y"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 约束自由度（h3-indexed-toggle-latch-joint-axis）

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
      "id": "rail-0-joint",
      "name": "rail-0 interface",
      "parent": "frame",
      "child": "rail-0",
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
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 维修间隙预算（h3-indexed-toggle-latch-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "head-0",
    "aperture": 0.51,
    "toolWidth": 0.35,
    "eachSideMargin": 0.05
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-indexed-toggle-latch-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,2]
- B：[0,0,0]
- C：[0,-1,0]
- D：[0,0,-2]

```json
{
  "input": {
    "module": "head-0",
    "lever": [
      1,
      2,
      0
    ],
    "force": [
      0,
      -2,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 非均匀先验更新（h3-indexed-toggle-latch-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0
- B：1
- C：0.75
- D：0.5

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
      1,
      3,
      2
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

### 风险最小决策（h3-indexed-toggle-latch-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.8,
    "repairCost": 2,
    "failureLoss": 7,
    "module": "head-0"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-indexed-toggle-latch-trace-threshold）

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
        "displacement": 0.013644105944877975
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0018448874713113104
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0007767834500269035
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.00001614783264634752
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.000055069442628290124
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.000005971426178550001
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.000003045380935857501
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0000015751849105437823
      },
      {
        "time": 0.8083333333333333,
        "displacement": 2.4663381733245223e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 2.4663381733245223e-7
      },
      {
        "time": 1,
        "displacement": 2.4663381733245223e-7
      }
    ],
    "threshold": 0.01637292713385357
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-indexed-toggle-latch-guarded-repair）

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
      "head-0"
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

### 失败状态回退（h3-indexed-toggle-latch-rollback）

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
      "head-0"
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

### 共享工具协同维修（h3-indexed-toggle-latch-resource-repair）

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
      },
      {
        "id": "release:elbow-0",
        "label": "release elbow-0",
        "requires": [
          "done:relock:elbow-0"
        ],
        "forbids": [
          "done:release:elbow-0"
        ],
        "adds": [
          "done:release:elbow-0",
          "ready:elbow-0",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-0"
        }
      },
      {
        "id": "relock:elbow-0",
        "label": "relock elbow-0",
        "requires": [
          "done:verify:elbow-0"
        ],
        "forbids": [
          "done:relock:elbow-0"
        ],
        "adds": [
          "done:relock:elbow-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-0"
        }
      },
      {
        "id": "verify:elbow-0",
        "label": "verify elbow-0",
        "requires": [
          "done:replace:elbow-0"
        ],
        "forbids": [
          "done:verify:elbow-0"
        ],
        "adds": [
          "done:verify:elbow-0"
        ],
        "deletes": [
          "fault:elbow-0",
          "misaligned:elbow-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-0"
        }
      },
      {
        "id": "replace:elbow-0",
        "label": "replace elbow-0",
        "requires": [
          "done:unlock:elbow-0"
        ],
        "forbids": [
          "done:replace:elbow-0"
        ],
        "adds": [
          "done:replace:elbow-0"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "elbow-0"
        }
      },
      {
        "id": "unlock:elbow-0",
        "label": "unlock elbow-0",
        "requires": [
          "done:support:elbow-0"
        ],
        "forbids": [
          "done:unlock:elbow-0"
        ],
        "adds": [
          "done:unlock:elbow-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-0"
        }
      },
      {
        "id": "support:elbow-0",
        "label": "support elbow-0",
        "requires": [
          "done:isolate:elbow-0"
        ],
        "forbids": [
          "done:support:elbow-0"
        ],
        "adds": [
          "done:support:elbow-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-0"
        }
      },
      {
        "id": "isolate:elbow-0",
        "label": "isolate elbow-0",
        "requires": [
          "tool:free",
          "fault:elbow-0"
        ],
        "forbids": [
          "done:isolate:elbow-0"
        ],
        "adds": [
          "done:isolate:elbow-0"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "elbow-0"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:elbow-0",
      "fault:head-0"
    ],
    "initialModules": [
      "frame",
      "rail-0",
      "carriage-0",
      "turret-0",
      "elbow-0",
      "head-0"
    ],
    "goalFacts": [
      "ready:elbow-0",
      "ready:head-0"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 16
  },
  "answer": {
    "actionIds": [
      "isolate:head-0",
      "support:head-0",
      "unlock:head-0",
      "replace:head-0",
      "verify:head-0",
      "relock:head-0",
      "release:head-0",
      "isolate:elbow-0",
      "support:elbow-0",
      "unlock:elbow-0",
      "replace:elbow-0",
      "verify:elbow-0",
      "relock:elbow-0",
      "release:elbow-0"
    ]
  }
}
```

### 预算约束检查策略（h3-indexed-toggle-latch-budget-policy）

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
        "cost": 2,
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
        "cost": 3,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      }
    ],
    "budget": 2
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
