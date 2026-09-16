## D1 维修工具小车

### 模块识别（h3-maintenance-trolley-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：tool-tray
- B：chassis
- C：front-axle
- D：rear-axle

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "chassis",
        "name": "Maintenance trolley chassis"
      },
      {
        "id": "front-axle",
        "name": "Front wheel axle"
      },
      {
        "id": "rear-axle",
        "name": "Rear wheel axle"
      },
      {
        "id": "tool-tray",
        "name": "Removable tool tray"
      },
      {
        "id": "handle",
        "name": "Foldable pull handle"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 部件计数（h3-maintenance-trolley-count）

模块 tool-tray 有多少个可视零件？

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
        "id": "h0001",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0002",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0003",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0004",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0005",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0006",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0007",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0008",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0009",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0010",
        "moduleId": "front-axle",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "h0011",
        "moduleId": "front-axle",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "h0012",
        "moduleId": "front-axle",
        "shape": "axle",
        "color": "#c6cdd2"
      },
      {
        "id": "h0013",
        "moduleId": "rear-axle",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "h0014",
        "moduleId": "rear-axle",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "h0015",
        "moduleId": "rear-axle",
        "shape": "axle",
        "color": "#c6cdd2"
      },
      {
        "id": "h0016",
        "moduleId": "tool-tray",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0017",
        "moduleId": "tool-tray",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0018",
        "moduleId": "tool-tray",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0019",
        "moduleId": "tool-tray",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0020",
        "moduleId": "handle",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "h0021",
        "moduleId": "handle",
        "shape": "beam",
        "color": "#8c99a3"
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 颜色识别（h3-maintenance-trolley-color）

零件 h0016 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#2878b8
- B：#d43a32
- C：#f2bf3c
- D：#e8792e

```json
{
  "input": {
    "part": {
      "id": "h0016",
      "moduleId": "tool-tray",
      "shape": "plate",
      "size": [
        0.92,
        0.25,
        0.92
      ],
      "position": [
        -0.5,
        -0.050000000000000044,
        -0.5
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#e8792e"
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 三维位置（h3-maintenance-trolley-position）

模块 tool-tray 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,-0.10000000000000006,-1]
- B：[0,-0.10000000000000006,1]
- C：[0,1.1500000000000001,0]
- D：[0,0.6499999999999999,0]

```json
{
  "input": {
    "centers": {
      "chassis": [
        0,
        0.6499999999999999,
        0
      ],
      "front-axle": [
        0,
        -0.10000000000000006,
        -1
      ],
      "rear-axle": [
        0,
        -0.10000000000000006,
        1
      ],
      "tool-tray": [
        0,
        1.1500000000000001,
        0
      ],
      "handle": [
        0,
        2.2625,
        1.9
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节类型（h3-maintenance-trolley-joint-type）

handle-pivot 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：fixed
- B：prismatic
- C：spring
- D：revolute

```json
{
  "input": {
    "joint": {
      "id": "handle-pivot",
      "name": "handle pivot",
      "type": "revolute",
      "parent": "chassis",
      "child": "handle",
      "anchorParent": [
        0,
        0.15000000000000013,
        1.9
      ],
      "anchorChild": [
        0,
        -1.4625000000000001,
        0
      ],
      "axis": [
        1,
        0,
        0
      ],
      "limits": [
        0,
        1.2
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 直接连接（h3-maintenance-trolley-parent）

tool-tray 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：[]
- B：["chassis","front-axle","rear-axle","tool-tray","handle"]
- C：["chassis"]
- D：["tool-tray"]

```json
{
  "input": {
    "joints": [
      {
        "id": "front-axle-pin",
        "name": "front axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "front-axle",
        "anchorParent": [
          0,
          -0.75,
          -1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "rear-axle-pin",
        "name": "rear axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "rear-axle",
        "anchorParent": [
          0,
          -0.75,
          1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "tray-clips",
        "name": "tray clips",
        "type": "fixed",
        "parent": "chassis",
        "child": "tool-tray",
        "anchorParent": [
          0,
          0.3500000000000001,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000013,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "handle-pivot",
        "name": "handle pivot",
        "type": "revolute",
        "parent": "chassis",
        "child": "handle",
        "anchorParent": [
          0,
          0.15000000000000013,
          1.9
        ],
        "anchorChild": [
          0,
          -1.4625000000000001,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 基座识别（h3-maintenance-trolley-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：[]
- B：["chassis","front-axle","rear-axle","tool-tray","handle"]
- C：["tool-tray"]
- D：["chassis"]

```json
{
  "input": {
    "modules": [
      {
        "id": "chassis",
        "name": "Maintenance trolley chassis",
        "role": "foundation",
        "anchored": true,
        "mass": 7,
        "position": [
          0,
          0.6499999999999999,
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
        "id": "front-axle",
        "name": "Front wheel axle",
        "role": "wheel-pair",
        "anchored": false,
        "mass": 1,
        "position": [
          0,
          -0.10000000000000009,
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
        "id": "rear-axle",
        "name": "Rear wheel axle",
        "role": "wheel-pair",
        "anchored": false,
        "mass": 1,
        "position": [
          0,
          -0.10000000000000009,
          1
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "tool-tray",
        "name": "Removable tool tray",
        "role": "service-module",
        "anchored": false,
        "mass": 1,
        "position": [
          0,
          1.1500000000000001,
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
        "id": "handle",
        "name": "Foldable pull handle",
        "role": "actuator",
        "anchored": false,
        "mass": 0.7,
        "position": [
          0,
          2.2625,
          1.9
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
    "choiceId": "D"
  }
}
```

### 接口计数（h3-maintenance-trolley-degree）

tool-tray 连接几个声明关节？平行关节分别计数。

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
        "id": "front-axle-pin",
        "name": "front axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "front-axle",
        "anchorParent": [
          0,
          -0.75,
          -1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "rear-axle-pin",
        "name": "rear axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "rear-axle",
        "anchorParent": [
          0,
          -0.75,
          1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "tray-clips",
        "name": "tray clips",
        "type": "fixed",
        "parent": "chassis",
        "child": "tool-tray",
        "anchorParent": [
          0,
          0.3500000000000001,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000013,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "handle-pivot",
        "name": "handle pivot",
        "type": "revolute",
        "parent": "chassis",
        "child": "handle",
        "anchorParent": [
          0,
          0.15000000000000013,
          1.9
        ],
        "anchorChild": [
          0,
          -1.4625000000000001,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 局部改色（h3-maintenance-trolley-recolor）

仅将 h0016 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"h0017","color":"#e8792e"}
- B：{"id":"h0016","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"h0016","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "h0016",
      "moduleId": "tool-tray",
      "shape": "plate",
      "size": [
        0.92,
        0.25,
        0.92
      ],
      "position": [
        -0.5,
        -0.050000000000000044,
        -0.5
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#e8792e"
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 补装部件（h3-maintenance-trolley-add）

模块 tool-tray 缺失零件 h0016。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"h0016","moduleId":"tool-tray","shape":"plate","size":[0.92,0.25,0.92],"position":[-0.5,-0.050000000000000044,-0.5],"rotation":[0,0,0,1],"color":"#000000"}
- B：{"id":"h0016","moduleId":"tool-tray","shape":"plate","size":[0.92,0.25,0.92],"position":[-0.5,-0.050000000000000044,-0.5],"rotation":[0,0,0,1],"color":"#e8792e"}
- C：{"id":"h0016","moduleId":"chassis","shape":"plate","size":[0.92,0.25,0.92],"position":[-0.5,-0.050000000000000044,-0.5],"rotation":[0,0,0,1],"color":"#e8792e"}
- D：{"id":"h0016","moduleId":"tool-tray","shape":"plate","size":[3,3,3],"position":[-0.5,-0.050000000000000044,-0.5],"rotation":[0,0,0,1],"color":"#e8792e"}

```json
{
  "input": {
    "targetPart": {
      "id": "h0016",
      "moduleId": "tool-tray",
      "shape": "plate",
      "size": [
        0.92,
        0.25,
        0.92
      ],
      "position": [
        -0.5,
        -0.050000000000000044,
        -0.5
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#e8792e"
    },
    "existingIds": [
      "h0001",
      "h0002",
      "h0003",
      "h0004",
      "h0005",
      "h0006",
      "h0007",
      "h0008",
      "h0009",
      "h0010",
      "h0011",
      "h0012",
      "h0013",
      "h0014",
      "h0015",
      "h0017",
      "h0018",
      "h0019",
      "h0020",
      "h0021"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全拆除（h3-maintenance-trolley-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：[]
- B：["chassis","front-axle","rear-axle","tool-tray","handle"]
- C：["front-axle","handle","rear-axle","tool-tray"]
- D：["chassis"]

```json
{
  "input": {
    "joints": [
      {
        "id": "front-axle-pin",
        "name": "front axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "front-axle",
        "anchorParent": [
          0,
          -0.75,
          -1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "rear-axle-pin",
        "name": "rear axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "rear-axle",
        "anchorParent": [
          0,
          -0.75,
          1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "tray-clips",
        "name": "tray clips",
        "type": "fixed",
        "parent": "chassis",
        "child": "tool-tray",
        "anchorParent": [
          0,
          0.3500000000000001,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000013,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "handle-pivot",
        "name": "handle pivot",
        "type": "revolute",
        "parent": "chassis",
        "child": "handle",
        "anchorParent": [
          0,
          0.15000000000000013,
          1.9
        ],
        "anchorChild": [
          0,
          -1.4625000000000001,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      }
    ],
    "modules": [
      "chassis",
      "front-axle",
      "rear-axle",
      "tool-tray",
      "handle"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 替换选择（h3-maintenance-trolley-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-1
- B：stock-0
- C：stock-2
- D：stock-3

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 5,
        "stiffness": 4,
        "mass": 0.8
      },
      {
        "id": "stock-1",
        "cost": 5,
        "stiffness": 7,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 8,
        "mass": 0.9
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 7,
        "mass": 1.1
      }
    ],
    "maxCost": 6
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 平移纠偏（h3-maintenance-trolley-translate）

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
    "target": "tool-tray"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 姿态纠偏（h3-maintenance-trolley-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：-180
- B：180
- C：0
- D：90

```json
{
  "input": {
    "module": "tool-tray",
    "currentYaw": 0,
    "targetYaw": 180
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 下一步放置（h3-maintenance-trolley-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["chassis"]
- B：["handle","tool-tray"]
- C：[]
- D：["chassis","front-axle","rear-axle"]

```json
{
  "input": {
    "prefix": [
      "chassis",
      "front-axle",
      "rear-axle"
    ],
    "joints": [
      {
        "id": "front-axle-pin",
        "name": "front axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "front-axle",
        "anchorParent": [
          0,
          -0.75,
          -1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "rear-axle-pin",
        "name": "rear axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "rear-axle",
        "anchorParent": [
          0,
          -0.75,
          1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "tray-clips",
        "name": "tray clips",
        "type": "fixed",
        "parent": "chassis",
        "child": "tool-tray",
        "anchorParent": [
          0,
          0.3500000000000001,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000013,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "handle-pivot",
        "name": "handle pivot",
        "type": "revolute",
        "parent": "chassis",
        "child": "handle",
        "anchorParent": [
          0,
          0.15000000000000013,
          1.9
        ],
        "anchorChild": [
          0,
          -1.4625000000000001,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      }
    ],
    "modules": [
      "chassis",
      "front-axle",
      "rear-axle",
      "tool-tray",
      "handle"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 库存核算（h3-maintenance-trolley-inventory）

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

### 子装配边界（h3-maintenance-trolley-boundary）

隔离 tool-tray 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["front-axle-pin","rear-axle-pin","tray-clips","handle-pivot"]
- B：["handle-pivot"]
- C：["tray-clips"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "front-axle-pin",
        "name": "front axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "front-axle",
        "anchorParent": [
          0,
          -0.75,
          -1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "rear-axle-pin",
        "name": "rear axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "rear-axle",
        "anchorParent": [
          0,
          -0.75,
          1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "tray-clips",
        "name": "tray clips",
        "type": "fixed",
        "parent": "chassis",
        "child": "tool-tray",
        "anchorParent": [
          0,
          0.3500000000000001,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000013,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "handle-pivot",
        "name": "handle pivot",
        "type": "revolute",
        "parent": "chassis",
        "child": "handle",
        "anchorParent": [
          0,
          0.15000000000000013,
          1.9
        ],
        "anchorChild": [
          0,
          -1.4625000000000001,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      }
    ],
    "target": "tool-tray"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 最小干预（h3-maintenance-trolley-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：4
- D：0

```json
{
  "input": {
    "module": "tool-tray"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 全过程依赖（h3-maintenance-trolley-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：1
- B：4
- C：0
- D：-1

```json
{
  "input": {
    "order": [
      "front-axle",
      "chassis",
      "rear-axle",
      "tool-tray",
      "handle"
    ],
    "joints": [
      {
        "id": "front-axle-pin",
        "name": "front axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "front-axle",
        "anchorParent": [
          0,
          -0.75,
          -1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "rear-axle-pin",
        "name": "rear axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "rear-axle",
        "anchorParent": [
          0,
          -0.75,
          1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "tray-clips",
        "name": "tray clips",
        "type": "fixed",
        "parent": "chassis",
        "child": "tool-tray",
        "anchorParent": [
          0,
          0.3500000000000001,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000013,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "handle-pivot",
        "name": "handle pivot",
        "type": "revolute",
        "parent": "chassis",
        "child": "handle",
        "anchorParent": [
          0,
          0.15000000000000013,
          1.9
        ],
        "anchorChild": [
          0,
          -1.4625000000000001,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 连续维修路径（h3-maintenance-trolley-access）

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
          6.3,
          1.1500000000000001,
          0
        ],
        "end": [
          0,
          1.1500000000000001,
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
          7.925,
          0
        ],
        "end": [
          0,
          1.1500000000000001,
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
          1.1500000000000001,
          6.1
        ],
        "end": [
          0,
          1.1500000000000001,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.6262293457984924
      }
    ],
    "simulator": "stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration"
  },
  "answer": {
    "choiceIds": [
      "B",
      "C"
    ]
  }
}
```

### 支撑反事实（h3-maintenance-trolley-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["chassis","front-axle","rear-axle","tool-tray","handle"]
- B：[]
- C：["tool-tray"]

```json
{
  "input": {
    "removed": "tool-tray",
    "roots": [
      "chassis"
    ],
    "joints": [
      {
        "id": "front-axle-pin",
        "name": "front axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "front-axle",
        "anchorParent": [
          0,
          -0.75,
          -1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "rear-axle-pin",
        "name": "rear axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "rear-axle",
        "anchorParent": [
          0,
          -0.75,
          1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "tray-clips",
        "name": "tray clips",
        "type": "fixed",
        "parent": "chassis",
        "child": "tool-tray",
        "anchorParent": [
          0,
          0.3500000000000001,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000013,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "handle-pivot",
        "name": "handle pivot",
        "type": "revolute",
        "parent": "chassis",
        "child": "handle",
        "anchorParent": [
          0,
          0.15000000000000013,
          1.9
        ],
        "anchorChild": [
          0,
          -1.4625000000000001,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          0,
          1.2
        ]
      }
    ],
    "modules": [
      "chassis",
      "front-axle",
      "rear-axle",
      "tool-tray",
      "handle"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 冲击响应读数（h3-maintenance-trolley-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.2
- B：1
- C：0

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0
      },
      {
        "time": 1,
        "displacement": 0
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 1.9221920383523778e-7,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-maintenance-trolley-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：0
- B：0.6
- C：-0.5
- D：1.7

```json
{
  "input": {
    "joint": "handle-pivot",
    "limits": [
      0,
      1.2
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

### 约束故障诊断（h3-maintenance-trolley-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：front-axle-pin
- B：rear-axle-pin
- C：handle-pivot
- D：tray-clips

```json
{
  "input": {
    "endpoints": [
      "chassis",
      "tool-tray"
    ],
    "type": "fixed",
    "joints": [
      {
        "id": "front-axle-pin",
        "name": "front axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "front-axle",
        "anchorParent": [
          0,
          -0.75,
          -1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "rear-axle-pin",
        "name": "rear axle pin",
        "type": "revolute",
        "parent": "chassis",
        "child": "rear-axle",
        "anchorParent": [
          0,
          -0.75,
          1
        ],
        "anchorChild": [
          0,
          5.551115123125783e-17,
          0
        ],
        "axis": [
          1,
          0,
          0
        ]
      },
      {
        "id": "tray-clips",
        "name": "tray clips",
        "type": "fixed",
        "parent": "chassis",
        "child": "tool-tray",
        "anchorParent": [
          0,
          0.3500000000000001,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000013,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "handle-pivot",
        "name": "handle pivot",
        "type": "revolute",
        "parent": "chassis",
        "child": "handle",
        "anchorParent": [
          0,
          0.15000000000000013,
          1.9
        ],
        "anchorChild": [
          0,
          -1.4625000000000001,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          0,
          1.2
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

### 主动检查收益（h3-maintenance-trolley-information-gain）

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
    "module": "tool-tray",
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

### 不确定性与弃答（h3-maintenance-trolley-abstention）

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
        "action": "repair"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 观测后信念更新（h3-maintenance-trolley-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.3333333333333333
- B：0
- C：0.25
- D：0.5

```json
{
  "input": {
    "module": "tool-tray",
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
      "positive"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 多目标工程权衡（h3-maintenance-trolley-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

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
        "cost": 5,
        "stiffness": 4,
        "mass": 0.8
      },
      {
        "id": "stock-1",
        "cost": 5,
        "stiffness": 7,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 8,
        "mass": 0.9
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 7,
        "mass": 1.1
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

### 依赖装配（h3-maintenance-trolley-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:tool-tray",
        "label": "安装 tool-tray",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:tool-tray"
        ],
        "adds": [
          "present:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray",
          "visible": true
        }
      },
      {
        "id": "place:rear-axle",
        "label": "安装 rear-axle",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:rear-axle"
        ],
        "adds": [
          "present:rear-axle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rear-axle",
          "visible": true
        }
      },
      {
        "id": "place:chassis",
        "label": "安装 chassis",
        "requires": [],
        "forbids": [
          "present:chassis"
        ],
        "adds": [
          "present:chassis"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "chassis",
          "visible": true
        }
      },
      {
        "id": "place:front-axle",
        "label": "安装 front-axle",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:front-axle"
        ],
        "adds": [
          "present:front-axle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "front-axle",
          "visible": true
        }
      },
      {
        "id": "place:handle",
        "label": "安装 handle",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:handle"
        ],
        "adds": [
          "present:handle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "handle",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:chassis",
      "present:front-axle",
      "present:rear-axle",
      "present:tool-tray",
      "present:handle"
    ],
    "budget": 5,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:chassis",
      "place:tool-tray",
      "place:rear-axle",
      "place:front-axle",
      "place:handle"
    ]
  }
}
```

### 依赖拆解（h3-maintenance-trolley-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:chassis",
      "present:front-axle",
      "present:rear-axle",
      "present:tool-tray",
      "present:handle"
    ],
    "initialModules": [
      "chassis",
      "front-axle",
      "rear-axle",
      "tool-tray",
      "handle"
    ],
    "actions": [
      {
        "id": "remove:front-axle",
        "label": "拆除 front-axle",
        "requires": [
          "present:front-axle"
        ],
        "forbids": [],
        "adds": [
          "removed:front-axle"
        ],
        "deletes": [
          "present:front-axle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "front-axle",
          "visible": false
        }
      },
      {
        "id": "remove:rear-axle",
        "label": "拆除 rear-axle",
        "requires": [
          "present:rear-axle"
        ],
        "forbids": [],
        "adds": [
          "removed:rear-axle"
        ],
        "deletes": [
          "present:rear-axle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rear-axle",
          "visible": false
        }
      },
      {
        "id": "remove:handle",
        "label": "拆除 handle",
        "requires": [
          "present:handle"
        ],
        "forbids": [],
        "adds": [
          "removed:handle"
        ],
        "deletes": [
          "present:handle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "handle",
          "visible": false
        }
      },
      {
        "id": "remove:chassis",
        "label": "拆除 chassis",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:front-axle",
          "present:rear-axle",
          "present:tool-tray",
          "present:handle"
        ],
        "adds": [
          "removed:chassis"
        ],
        "deletes": [
          "present:chassis"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "chassis",
          "visible": false
        }
      },
      {
        "id": "remove:tool-tray",
        "label": "拆除 tool-tray",
        "requires": [
          "present:tool-tray"
        ],
        "forbids": [],
        "adds": [
          "removed:tool-tray"
        ],
        "deletes": [
          "present:tool-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:handle",
      "removed:tool-tray",
      "removed:rear-axle",
      "removed:front-axle",
      "removed:chassis"
    ],
    "budget": 5,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:front-axle",
      "remove:rear-axle",
      "remove:handle",
      "remove:tool-tray",
      "remove:chassis"
    ]
  }
}
```

### 承载维修（h3-maintenance-trolley-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:tool-tray",
      "closed:tool-tray"
    ],
    "initialModules": [
      "chassis",
      "front-axle",
      "rear-axle",
      "tool-tray",
      "handle"
    ],
    "actions": [
      {
        "id": "release:tool-tray",
        "label": "release tool-tray",
        "requires": [
          "done:close:tool-tray"
        ],
        "forbids": [
          "done:release:tool-tray"
        ],
        "adds": [
          "done:release:tool-tray",
          "repaired:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "close:tool-tray",
        "label": "close tool-tray",
        "requires": [
          "done:verify:tool-tray"
        ],
        "forbids": [
          "done:close:tool-tray"
        ],
        "adds": [
          "done:close:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "replace:tool-tray",
        "label": "replace tool-tray",
        "requires": [
          "done:remove:tool-tray"
        ],
        "forbids": [
          "done:replace:tool-tray"
        ],
        "adds": [
          "done:replace:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray",
          "visible": true
        }
      },
      {
        "id": "support:tool-tray",
        "label": "support tool-tray",
        "requires": [
          "fault:tool-tray"
        ],
        "forbids": [
          "done:support:tool-tray"
        ],
        "adds": [
          "done:support:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "verify:tool-tray",
        "label": "verify tool-tray",
        "requires": [
          "done:replace:tool-tray"
        ],
        "forbids": [
          "done:verify:tool-tray"
        ],
        "adds": [
          "done:verify:tool-tray"
        ],
        "deletes": [
          "fault:tool-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "remove:tool-tray",
        "label": "remove tool-tray",
        "requires": [
          "done:open:tool-tray"
        ],
        "forbids": [
          "done:remove:tool-tray"
        ],
        "adds": [
          "done:remove:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray",
          "visible": false
        }
      },
      {
        "id": "open:tool-tray",
        "label": "open tool-tray",
        "requires": [
          "done:support:tool-tray"
        ],
        "forbids": [
          "done:open:tool-tray"
        ],
        "adds": [
          "done:open:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      }
    ],
    "goalFacts": [
      "repaired:tool-tray"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:tool-tray",
      "open:tool-tray",
      "remove:tool-tray",
      "replace:tool-tray",
      "verify:tool-tray",
      "close:tool-tray",
      "release:tool-tray"
    ]
  }
}
```

### 复合编辑验证（h3-maintenance-trolley-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:tool-tray",
      "closed:tool-tray"
    ],
    "initialModules": [
      "chassis",
      "front-axle",
      "rear-axle",
      "tool-tray",
      "handle"
    ],
    "actions": [
      {
        "id": "release:tool-tray",
        "label": "release tool-tray",
        "requires": [
          "done:close:tool-tray"
        ],
        "forbids": [
          "done:release:tool-tray"
        ],
        "adds": [
          "done:release:tool-tray",
          "repaired:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "close:tool-tray",
        "label": "close tool-tray",
        "requires": [
          "done:verify:tool-tray"
        ],
        "forbids": [
          "done:close:tool-tray"
        ],
        "adds": [
          "done:close:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "recolor:tool-tray",
        "label": "recolor tool-tray",
        "requires": [
          "done:open:tool-tray"
        ],
        "forbids": [
          "done:recolor:tool-tray"
        ],
        "adds": [
          "done:recolor:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray",
          "color": "#ea7635"
        }
      },
      {
        "id": "support:tool-tray",
        "label": "support tool-tray",
        "requires": [
          "fault:tool-tray"
        ],
        "forbids": [
          "done:support:tool-tray"
        ],
        "adds": [
          "done:support:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "verify:tool-tray",
        "label": "verify tool-tray",
        "requires": [
          "done:recolor:tool-tray"
        ],
        "forbids": [
          "done:verify:tool-tray"
        ],
        "adds": [
          "done:verify:tool-tray"
        ],
        "deletes": [
          "fault:tool-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "open:tool-tray",
        "label": "open tool-tray",
        "requires": [
          "done:support:tool-tray"
        ],
        "forbids": [
          "done:open:tool-tray"
        ],
        "adds": [
          "done:open:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      }
    ],
    "goalFacts": [
      "repaired:tool-tray"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:tool-tray",
      "open:tool-tray",
      "recolor:tool-tray",
      "verify:tool-tray",
      "close:tool-tray",
      "release:tool-tray"
    ]
  }
}
```

### 跨区域联合维修（h3-maintenance-trolley-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:handle",
      "closed:handle"
    ],
    "initialModules": [
      "chassis",
      "front-axle",
      "rear-axle",
      "tool-tray",
      "handle"
    ],
    "actions": [
      {
        "id": "release:handle",
        "label": "release handle",
        "requires": [
          "done:close:handle"
        ],
        "forbids": [
          "done:release:handle"
        ],
        "adds": [
          "done:release:handle",
          "repaired:handle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "handle"
        }
      },
      {
        "id": "open:handle",
        "label": "open handle",
        "requires": [
          "done:support:handle"
        ],
        "forbids": [
          "done:open:handle"
        ],
        "adds": [
          "done:open:handle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "handle"
        }
      },
      {
        "id": "support:handle",
        "label": "support handle",
        "requires": [
          "fault:handle"
        ],
        "forbids": [
          "done:support:handle"
        ],
        "adds": [
          "done:support:handle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "handle"
        }
      },
      {
        "id": "replace:handle",
        "label": "replace handle",
        "requires": [
          "done:remove:handle"
        ],
        "forbids": [
          "done:replace:handle"
        ],
        "adds": [
          "done:replace:handle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "handle",
          "visible": true
        }
      },
      {
        "id": "close:handle",
        "label": "close handle",
        "requires": [
          "done:verify:handle"
        ],
        "forbids": [
          "done:close:handle"
        ],
        "adds": [
          "done:close:handle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "handle"
        }
      },
      {
        "id": "verify:handle",
        "label": "verify handle",
        "requires": [
          "done:replace:handle"
        ],
        "forbids": [
          "done:verify:handle"
        ],
        "adds": [
          "done:verify:handle"
        ],
        "deletes": [
          "fault:handle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "handle"
        }
      },
      {
        "id": "remove:handle",
        "label": "remove handle",
        "requires": [
          "done:open:handle"
        ],
        "forbids": [
          "done:remove:handle"
        ],
        "adds": [
          "done:remove:handle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "handle",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "repaired:handle"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:handle",
      "open:handle",
      "remove:handle",
      "replace:handle",
      "verify:handle",
      "close:handle",
      "release:handle"
    ]
  }
}
```

### 多工位资源调度（h3-maintenance-trolley-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "chassis",
        "duration": 1,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "front-axle",
        "duration": 3,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "rear-axle",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "tool-tray",
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

### 检查后条件策略（h3-maintenance-trolley-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "tool-tray",
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

### 局部坐标变换（h3-maintenance-trolley-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[0.5,-0.05,-0.5]
- B：[1.5,2.1,0.5]
- C：[0.5,1.1,-0.5]

```json
{
  "input": {
    "localPoint": [
      0.5,
      -0.050000000000000044,
      -0.5
    ],
    "rotationXYZW": [
      0,
      0,
      0,
      1
    ],
    "translation": [
      0,
      1.1500000000000001,
      0
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-maintenance-trolley-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[2,5]
- B：[5,2]
- C：[2,3]
- D：[0,0]

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
    "choiceId": "A"
  }
}
```

### 空间相对关系（h3-maintenance-trolley-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：less
- B：equal
- C：greater

```json
{
  "input": {
    "A": {
      "id": "chassis",
      "position": [
        0,
        0.6499999999999999,
        0
      ]
    },
    "B": {
      "id": "handle",
      "position": [
        0,
        2.2625,
        1.9
      ]
    },
    "axis": "x"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 约束自由度（h3-maintenance-trolley-joint-axis）

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
      "id": "front-axle-pin",
      "name": "front axle pin",
      "type": "revolute",
      "parent": "chassis",
      "child": "front-axle",
      "anchorParent": [
        0,
        -0.75,
        -1
      ],
      "anchorChild": [
        0,
        5.551115123125783e-17,
        0
      ],
      "axis": [
        1,
        0,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 维修间隙预算（h3-maintenance-trolley-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "tool-tray",
    "aperture": 0.31999999999999995,
    "toolWidth": 0.35,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-maintenance-trolley-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,4]
- B：[0,0,0]
- C：[0,-1,0]
- D：[0,0,-4]

```json
{
  "input": {
    "module": "tool-tray",
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
    "choiceId": "D"
  }
}
```

### 非均匀先验更新（h3-maintenance-trolley-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.4444444444444444
- B：0
- C：1
- D：0.5714285714285714

```json
{
  "input": {
    "module": "tool-tray",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      3,
      4,
      2
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

### 风险最小决策（h3-maintenance-trolley-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.1,
    "repairCost": 2,
    "failureLoss": 7,
    "module": "tool-tray"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-maintenance-trolley-trace-threshold）

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
        "displacement": 0
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0
      },
      {
        "time": 1,
        "displacement": 0
      }
    ],
    "threshold": 0
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-maintenance-trolley-guarded-repair）

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
        "id": "release:tool-tray",
        "label": "release tool-tray",
        "requires": [
          "done:relock:tool-tray"
        ],
        "forbids": [
          "done:release:tool-tray"
        ],
        "adds": [
          "done:release:tool-tray",
          "ready:tool-tray",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "relock:tool-tray",
        "label": "relock tool-tray",
        "requires": [
          "done:verify:tool-tray"
        ],
        "forbids": [
          "done:relock:tool-tray"
        ],
        "adds": [
          "done:relock:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "verify:tool-tray",
        "label": "verify tool-tray",
        "requires": [
          "done:replace:tool-tray"
        ],
        "forbids": [
          "done:verify:tool-tray"
        ],
        "adds": [
          "done:verify:tool-tray"
        ],
        "deletes": [
          "fault:tool-tray",
          "misaligned:tool-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "replace:tool-tray",
        "label": "replace tool-tray",
        "requires": [
          "done:unlock:tool-tray"
        ],
        "forbids": [
          "done:replace:tool-tray"
        ],
        "adds": [
          "done:replace:tool-tray"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "unlock:tool-tray",
        "label": "unlock tool-tray",
        "requires": [
          "done:support:tool-tray"
        ],
        "forbids": [
          "done:unlock:tool-tray"
        ],
        "adds": [
          "done:unlock:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "support:tool-tray",
        "label": "support tool-tray",
        "requires": [
          "done:isolate:tool-tray"
        ],
        "forbids": [
          "done:support:tool-tray"
        ],
        "adds": [
          "done:support:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "isolate:tool-tray",
        "label": "isolate tool-tray",
        "requires": [
          "tool:free",
          "fault:tool-tray"
        ],
        "forbids": [
          "done:isolate:tool-tray"
        ],
        "adds": [
          "done:isolate:tool-tray"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:tool-tray"
    ],
    "initialModules": [
      "chassis",
      "front-axle",
      "rear-axle",
      "tool-tray",
      "handle"
    ],
    "goalFacts": [
      "ready:tool-tray"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:tool-tray",
      "support:tool-tray",
      "unlock:tool-tray",
      "replace:tool-tray",
      "verify:tool-tray",
      "relock:tool-tray",
      "release:tool-tray"
    ]
  }
}
```

### 失败状态回退（h3-maintenance-trolley-rollback）

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
        "id": "resume:tool-tray",
        "label": "resume tool-tray",
        "requires": [
          "done:verify:tool-tray"
        ],
        "forbids": [
          "done:resume:tool-tray"
        ],
        "adds": [
          "done:resume:tool-tray",
          "ready:tool-tray",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "verify:tool-tray",
        "label": "verify tool-tray",
        "requires": [
          "done:align:tool-tray"
        ],
        "forbids": [
          "done:verify:tool-tray"
        ],
        "adds": [
          "done:verify:tool-tray"
        ],
        "deletes": [
          "fault:tool-tray",
          "misaligned:tool-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "align:tool-tray",
        "label": "align tool-tray",
        "requires": [
          "done:undo:tool-tray"
        ],
        "forbids": [
          "done:align:tool-tray"
        ],
        "adds": [
          "done:align:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray",
          "visible": true
        }
      },
      {
        "id": "undo:tool-tray",
        "label": "undo tool-tray",
        "requires": [
          "done:isolate:tool-tray"
        ],
        "forbids": [
          "done:undo:tool-tray"
        ],
        "adds": [
          "done:undo:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray",
          "visible": false
        }
      },
      {
        "id": "isolate:tool-tray",
        "label": "isolate tool-tray",
        "requires": [
          "tool:free",
          "fault:tool-tray"
        ],
        "forbids": [
          "done:isolate:tool-tray"
        ],
        "adds": [
          "done:isolate:tool-tray"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:tool-tray",
      "misaligned:tool-tray"
    ],
    "initialModules": [
      "chassis",
      "front-axle",
      "rear-axle",
      "tool-tray",
      "handle"
    ],
    "goalFacts": [
      "ready:tool-tray"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:tool-tray",
      "undo:tool-tray",
      "align:tool-tray",
      "verify:tool-tray",
      "resume:tool-tray"
    ]
  }
}
```

### 共享工具协同维修（h3-maintenance-trolley-resource-repair）

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
        "id": "release:handle",
        "label": "release handle",
        "requires": [
          "done:relock:handle"
        ],
        "forbids": [
          "done:release:handle"
        ],
        "adds": [
          "done:release:handle",
          "ready:handle",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "handle"
        }
      },
      {
        "id": "relock:handle",
        "label": "relock handle",
        "requires": [
          "done:verify:handle"
        ],
        "forbids": [
          "done:relock:handle"
        ],
        "adds": [
          "done:relock:handle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "handle"
        }
      },
      {
        "id": "verify:handle",
        "label": "verify handle",
        "requires": [
          "done:replace:handle"
        ],
        "forbids": [
          "done:verify:handle"
        ],
        "adds": [
          "done:verify:handle"
        ],
        "deletes": [
          "fault:handle",
          "misaligned:handle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "handle"
        }
      },
      {
        "id": "replace:handle",
        "label": "replace handle",
        "requires": [
          "done:unlock:handle"
        ],
        "forbids": [
          "done:replace:handle"
        ],
        "adds": [
          "done:replace:handle"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "handle"
        }
      },
      {
        "id": "unlock:handle",
        "label": "unlock handle",
        "requires": [
          "done:support:handle"
        ],
        "forbids": [
          "done:unlock:handle"
        ],
        "adds": [
          "done:unlock:handle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "handle"
        }
      },
      {
        "id": "support:handle",
        "label": "support handle",
        "requires": [
          "done:isolate:handle"
        ],
        "forbids": [
          "done:support:handle"
        ],
        "adds": [
          "done:support:handle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "handle"
        }
      },
      {
        "id": "isolate:handle",
        "label": "isolate handle",
        "requires": [
          "tool:free",
          "fault:handle"
        ],
        "forbids": [
          "done:isolate:handle"
        ],
        "adds": [
          "done:isolate:handle"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "handle"
        }
      },
      {
        "id": "release:tool-tray",
        "label": "release tool-tray",
        "requires": [
          "done:relock:tool-tray"
        ],
        "forbids": [
          "done:release:tool-tray"
        ],
        "adds": [
          "done:release:tool-tray",
          "ready:tool-tray",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "relock:tool-tray",
        "label": "relock tool-tray",
        "requires": [
          "done:verify:tool-tray"
        ],
        "forbids": [
          "done:relock:tool-tray"
        ],
        "adds": [
          "done:relock:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "verify:tool-tray",
        "label": "verify tool-tray",
        "requires": [
          "done:replace:tool-tray"
        ],
        "forbids": [
          "done:verify:tool-tray"
        ],
        "adds": [
          "done:verify:tool-tray"
        ],
        "deletes": [
          "fault:tool-tray",
          "misaligned:tool-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "replace:tool-tray",
        "label": "replace tool-tray",
        "requires": [
          "done:unlock:tool-tray"
        ],
        "forbids": [
          "done:replace:tool-tray"
        ],
        "adds": [
          "done:replace:tool-tray"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "unlock:tool-tray",
        "label": "unlock tool-tray",
        "requires": [
          "done:support:tool-tray"
        ],
        "forbids": [
          "done:unlock:tool-tray"
        ],
        "adds": [
          "done:unlock:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "support:tool-tray",
        "label": "support tool-tray",
        "requires": [
          "done:isolate:tool-tray"
        ],
        "forbids": [
          "done:support:tool-tray"
        ],
        "adds": [
          "done:support:tool-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      },
      {
        "id": "isolate:tool-tray",
        "label": "isolate tool-tray",
        "requires": [
          "tool:free",
          "fault:tool-tray"
        ],
        "forbids": [
          "done:isolate:tool-tray"
        ],
        "adds": [
          "done:isolate:tool-tray"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tool-tray"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:tool-tray",
      "fault:handle"
    ],
    "initialModules": [
      "chassis",
      "front-axle",
      "rear-axle",
      "tool-tray",
      "handle"
    ],
    "goalFacts": [
      "ready:tool-tray",
      "ready:handle"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 16
  },
  "answer": {
    "actionIds": [
      "isolate:handle",
      "support:handle",
      "unlock:handle",
      "replace:handle",
      "verify:handle",
      "relock:handle",
      "release:handle",
      "isolate:tool-tray",
      "support:tool-tray",
      "unlock:tool-tray",
      "replace:tool-tray",
      "verify:tool-tray",
      "relock:tool-tray",
      "release:tool-tray"
    ]
  }
}
```

### 预算约束检查策略（h3-maintenance-trolley-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "tool-tray",
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
