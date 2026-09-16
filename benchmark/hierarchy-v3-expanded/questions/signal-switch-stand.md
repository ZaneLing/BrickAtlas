## D1 检修信号转臂

### 模块识别（h3-signal-switch-stand-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：lamp
- B：base
- C：post
- D：signal-arm

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "base",
        "name": "Weighted signal base"
      },
      {
        "id": "post",
        "name": "Signal mast"
      },
      {
        "id": "signal-arm",
        "name": "Pivoting signal arm"
      },
      {
        "id": "lamp",
        "name": "Inspection lamp"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 部件计数（h3-signal-switch-stand-count）

模块 lamp 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：3
- B：1
- C：5
- D：2

```json
{
  "input": {
    "parts": [
      {
        "id": "h0001",
        "moduleId": "base",
        "shape": "plate",
        "color": "#26323b"
      },
      {
        "id": "h0002",
        "moduleId": "base",
        "shape": "plate",
        "color": "#26323b"
      },
      {
        "id": "h0003",
        "moduleId": "base",
        "shape": "plate",
        "color": "#26323b"
      },
      {
        "id": "h0004",
        "moduleId": "base",
        "shape": "plate",
        "color": "#26323b"
      },
      {
        "id": "h0005",
        "moduleId": "base",
        "shape": "plate",
        "color": "#26323b"
      },
      {
        "id": "h0006",
        "moduleId": "base",
        "shape": "plate",
        "color": "#26323b"
      },
      {
        "id": "h0007",
        "moduleId": "base",
        "shape": "plate",
        "color": "#26323b"
      },
      {
        "id": "h0008",
        "moduleId": "base",
        "shape": "plate",
        "color": "#26323b"
      },
      {
        "id": "h0009",
        "moduleId": "base",
        "shape": "plate",
        "color": "#26323b"
      },
      {
        "id": "h0010",
        "moduleId": "post",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "h0011",
        "moduleId": "post",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "h0012",
        "moduleId": "post",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "h0013",
        "moduleId": "post",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "h0014",
        "moduleId": "post",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "h0015",
        "moduleId": "post",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "h0016",
        "moduleId": "signal-arm",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0017",
        "moduleId": "signal-arm",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0018",
        "moduleId": "signal-arm",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0019",
        "moduleId": "signal-arm",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0020",
        "moduleId": "signal-arm",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0021",
        "moduleId": "lamp",
        "shape": "cylinder",
        "color": "#f2bf3c"
      },
      {
        "id": "h0022",
        "moduleId": "lamp",
        "shape": "panel",
        "color": "#101820"
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 颜色识别（h3-signal-switch-stand-color）

零件 h0021 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#f2bf3c
- B：#2878b8
- C：#d43a32
- D：#26323b

```json
{
  "input": {
    "part": {
      "id": "h0021",
      "moduleId": "lamp",
      "shape": "cylinder",
      "size": [
        0.9,
        0.45,
        0.9
      ],
      "position": [
        -0.027499999999999858,
        0,
        0
      ],
      "rotation": [
        0.7071067811865475,
        0,
        0,
        0.7071067811865476
      ],
      "color": "#f2bf3c"
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 三维位置（h3-signal-switch-stand-position）

模块 lamp 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[2.0500000000000003,4.1,0.55]
- B：[4.6275,4.1,0.55]
- C：[0,0.2,0]
- D：[0,2.3,0]

```json
{
  "input": {
    "centers": {
      "base": [
        0,
        0.2,
        0
      ],
      "post": [
        0,
        2.3,
        0
      ],
      "signal-arm": [
        2.0500000000000003,
        4.1,
        0.55
      ],
      "lamp": [
        4.6275,
        4.1,
        0.55
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节类型（h3-signal-switch-stand-joint-type）

arm-pivot 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：prismatic
- B：spring
- C：revolute
- D：fixed

```json
{
  "input": {
    "joint": {
      "id": "arm-pivot",
      "name": "arm pivot",
      "type": "revolute",
      "parent": "post",
      "child": "signal-arm",
      "anchorParent": [
        0,
        1.7999999999999998,
        0.55
      ],
      "anchorChild": [
        -2.0500000000000003,
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
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 直接连接（h3-signal-switch-stand-parent）

lamp 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["base","post","signal-arm","lamp"]
- B：["signal-arm"]
- C：["lamp"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "post-foot",
        "name": "post foot",
        "type": "fixed",
        "parent": "base",
        "child": "post",
        "anchorParent": [
          0,
          0.14999999999999997,
          0
        ],
        "anchorChild": [
          0,
          -1.9499999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-pivot",
        "name": "arm pivot",
        "type": "revolute",
        "parent": "post",
        "child": "signal-arm",
        "anchorParent": [
          0,
          1.7999999999999998,
          0.55
        ],
        "anchorChild": [
          -2.0500000000000003,
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
        "id": "lamp-lock",
        "name": "lamp lock",
        "type": "fixed",
        "parent": "signal-arm",
        "child": "lamp",
        "anchorParent": [
          2.5500000000000003,
          0,
          0
        ],
        "anchorChild": [
          -0.027499999999999858,
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

### 基座识别（h3-signal-switch-stand-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["base","post","signal-arm","lamp"]
- B：["lamp"]
- C：["base"]
- D：[]

```json
{
  "input": {
    "modules": [
      {
        "id": "base",
        "name": "Weighted signal base",
        "role": "foundation",
        "anchored": true,
        "mass": 8,
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
        "id": "post",
        "name": "Signal mast",
        "role": "support",
        "anchored": false,
        "mass": 2,
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
      },
      {
        "id": "signal-arm",
        "name": "Pivoting signal arm",
        "role": "actuator",
        "anchored": false,
        "mass": 1,
        "position": [
          2.0500000000000003,
          4.1,
          0.55
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "lamp",
        "name": "Inspection lamp",
        "role": "service-module",
        "anchored": false,
        "mass": 0.5,
        "position": [
          4.6275,
          4.1,
          0.55
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
    "choiceId": "C"
  }
}
```

### 接口计数（h3-signal-switch-stand-degree）

lamp 连接几个声明关节？平行关节分别计数。

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
        "id": "post-foot",
        "name": "post foot",
        "type": "fixed",
        "parent": "base",
        "child": "post",
        "anchorParent": [
          0,
          0.14999999999999997,
          0
        ],
        "anchorChild": [
          0,
          -1.9499999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-pivot",
        "name": "arm pivot",
        "type": "revolute",
        "parent": "post",
        "child": "signal-arm",
        "anchorParent": [
          0,
          1.7999999999999998,
          0.55
        ],
        "anchorChild": [
          -2.0500000000000003,
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
        "id": "lamp-lock",
        "name": "lamp lock",
        "type": "fixed",
        "parent": "signal-arm",
        "child": "lamp",
        "anchorParent": [
          2.5500000000000003,
          0,
          0
        ],
        "anchorChild": [
          -0.027499999999999858,
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
    "choiceId": "C"
  }
}
```

### 局部改色（h3-signal-switch-stand-recolor）

仅将 h0021 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"h0021","color":"#e8792e"}
- B：{"id":"h0022","color":"#e8792e"}
- C：{"id":"h0021","color":"#2878b8"}
- D：{"id":"*","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "h0021",
      "moduleId": "lamp",
      "shape": "cylinder",
      "size": [
        0.9,
        0.45,
        0.9
      ],
      "position": [
        -0.027499999999999858,
        0,
        0
      ],
      "rotation": [
        0.7071067811865475,
        0,
        0,
        0.7071067811865476
      ],
      "color": "#f2bf3c"
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 补装部件（h3-signal-switch-stand-add）

模块 lamp 缺失零件 h0021。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"h0021","moduleId":"lamp","shape":"cylinder","size":[3,3,3],"position":[-0.027499999999999858,0,0],"rotation":[0.7071067811865475,0,0,0.7071067811865476],"color":"#f2bf3c"}
- B：{"id":"h0021","moduleId":"lamp","shape":"cylinder","size":[0.9,0.45,0.9],"position":[-0.027499999999999858,0,0],"rotation":[0.7071067811865475,0,0,0.7071067811865476],"color":"#000000"}
- C：{"id":"h0021","moduleId":"lamp","shape":"cylinder","size":[0.9,0.45,0.9],"position":[-0.027499999999999858,0,0],"rotation":[0.7071067811865475,0,0,0.7071067811865476],"color":"#f2bf3c"}
- D：{"id":"h0021","moduleId":"base","shape":"cylinder","size":[0.9,0.45,0.9],"position":[-0.027499999999999858,0,0],"rotation":[0.7071067811865475,0,0,0.7071067811865476],"color":"#f2bf3c"}

```json
{
  "input": {
    "targetPart": {
      "id": "h0021",
      "moduleId": "lamp",
      "shape": "cylinder",
      "size": [
        0.9,
        0.45,
        0.9
      ],
      "position": [
        -0.027499999999999858,
        0,
        0
      ],
      "rotation": [
        0.7071067811865475,
        0,
        0,
        0.7071067811865476
      ],
      "color": "#f2bf3c"
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
      "h0016",
      "h0017",
      "h0018",
      "h0019",
      "h0020",
      "h0022"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 安全拆除（h3-signal-switch-stand-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["lamp"]
- B：["base"]
- C：[]
- D：["base","post","signal-arm","lamp"]

```json
{
  "input": {
    "joints": [
      {
        "id": "post-foot",
        "name": "post foot",
        "type": "fixed",
        "parent": "base",
        "child": "post",
        "anchorParent": [
          0,
          0.14999999999999997,
          0
        ],
        "anchorChild": [
          0,
          -1.9499999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-pivot",
        "name": "arm pivot",
        "type": "revolute",
        "parent": "post",
        "child": "signal-arm",
        "anchorParent": [
          0,
          1.7999999999999998,
          0.55
        ],
        "anchorChild": [
          -2.0500000000000003,
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
        "id": "lamp-lock",
        "name": "lamp lock",
        "type": "fixed",
        "parent": "signal-arm",
        "child": "lamp",
        "anchorParent": [
          2.5500000000000003,
          0,
          0
        ],
        "anchorChild": [
          -0.027499999999999858,
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
      "base",
      "post",
      "signal-arm",
      "lamp"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 替换选择（h3-signal-switch-stand-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

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
        "cost": 8,
        "stiffness": 11,
        "mass": 1.2
      },
      {
        "id": "stock-1",
        "cost": 6,
        "stiffness": 9,
        "mass": 0.8
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 10,
        "mass": 1.4
      },
      {
        "id": "stock-3",
        "cost": 3,
        "stiffness": 11,
        "mass": 1.5
      }
    ],
    "maxCost": 7
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 平移纠偏（h3-signal-switch-stand-translate）

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
    "target": "lamp"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 姿态纠偏（h3-signal-switch-stand-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：135
- B：0
- C：90
- D：-135

```json
{
  "input": {
    "module": "lamp",
    "currentYaw": 0,
    "targetYaw": 225
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 下一步放置（h3-signal-switch-stand-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["base","post"]
- B：["signal-arm","lamp"]
- C：["signal-arm"]
- D：[]

```json
{
  "input": {
    "prefix": [
      "base",
      "post"
    ],
    "joints": [
      {
        "id": "post-foot",
        "name": "post foot",
        "type": "fixed",
        "parent": "base",
        "child": "post",
        "anchorParent": [
          0,
          0.14999999999999997,
          0
        ],
        "anchorChild": [
          0,
          -1.9499999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-pivot",
        "name": "arm pivot",
        "type": "revolute",
        "parent": "post",
        "child": "signal-arm",
        "anchorParent": [
          0,
          1.7999999999999998,
          0.55
        ],
        "anchorChild": [
          -2.0500000000000003,
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
        "id": "lamp-lock",
        "name": "lamp lock",
        "type": "fixed",
        "parent": "signal-arm",
        "child": "lamp",
        "anchorParent": [
          2.5500000000000003,
          0,
          0
        ],
        "anchorChild": [
          -0.027499999999999858,
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
      "base",
      "post",
      "signal-arm",
      "lamp"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 库存核算（h3-signal-switch-stand-inventory）

备件库有 3 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：2
- B：0
- C：4
- D：1

```json
{
  "input": {
    "available": 3,
    "required": 2
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 子装配边界（h3-signal-switch-stand-boundary）

隔离 lamp 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["arm-pivot"]
- B：["lamp-lock"]
- C：[]
- D：["post-foot","arm-pivot","lamp-lock"]

```json
{
  "input": {
    "joints": [
      {
        "id": "post-foot",
        "name": "post foot",
        "type": "fixed",
        "parent": "base",
        "child": "post",
        "anchorParent": [
          0,
          0.14999999999999997,
          0
        ],
        "anchorChild": [
          0,
          -1.9499999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-pivot",
        "name": "arm pivot",
        "type": "revolute",
        "parent": "post",
        "child": "signal-arm",
        "anchorParent": [
          0,
          1.7999999999999998,
          0.55
        ],
        "anchorChild": [
          -2.0500000000000003,
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
        "id": "lamp-lock",
        "name": "lamp lock",
        "type": "fixed",
        "parent": "signal-arm",
        "child": "lamp",
        "anchorParent": [
          2.5500000000000003,
          0,
          0
        ],
        "anchorChild": [
          -0.027499999999999858,
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
    "target": "lamp"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 最小干预（h3-signal-switch-stand-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：0

```json
{
  "input": {
    "module": "lamp"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 全过程依赖（h3-signal-switch-stand-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：1
- B：-1
- C：2
- D：3

```json
{
  "input": {
    "order": [
      "base",
      "signal-arm",
      "post",
      "lamp"
    ],
    "joints": [
      {
        "id": "post-foot",
        "name": "post foot",
        "type": "fixed",
        "parent": "base",
        "child": "post",
        "anchorParent": [
          0,
          0.14999999999999997,
          0
        ],
        "anchorChild": [
          0,
          -1.9499999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-pivot",
        "name": "arm pivot",
        "type": "revolute",
        "parent": "post",
        "child": "signal-arm",
        "anchorParent": [
          0,
          1.7999999999999998,
          0.55
        ],
        "anchorChild": [
          -2.0500000000000003,
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
        "id": "lamp-lock",
        "name": "lamp lock",
        "type": "fixed",
        "parent": "signal-arm",
        "child": "lamp",
        "anchorParent": [
          2.5500000000000003,
          0,
          0
        ],
        "anchorChild": [
          -0.027499999999999858,
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
    "choiceId": "A"
  }
}
```

### 连续维修路径（h3-signal-switch-stand-access）

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
          9.105,
          4.1,
          0.55
        ],
        "end": [
          4.6275,
          4.1,
          0.55
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
          4.6275,
          8.649999999999999,
          0.55
        ],
        "end": [
          4.6275,
          4.1,
          0.55
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
          4.6275,
          4.1,
          5.46
        ],
        "end": [
          4.6275,
          4.1,
          0.55
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

### 支撑反事实（h3-signal-switch-stand-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["lamp","signal-arm"]
- B：["post"]
- C：[]
- D：["base","post","signal-arm","lamp"]

```json
{
  "input": {
    "removed": "post",
    "roots": [
      "base"
    ],
    "joints": [
      {
        "id": "post-foot",
        "name": "post foot",
        "type": "fixed",
        "parent": "base",
        "child": "post",
        "anchorParent": [
          0,
          0.14999999999999997,
          0
        ],
        "anchorChild": [
          0,
          -1.9499999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-pivot",
        "name": "arm pivot",
        "type": "revolute",
        "parent": "post",
        "child": "signal-arm",
        "anchorParent": [
          0,
          1.7999999999999998,
          0.55
        ],
        "anchorChild": [
          -2.0500000000000003,
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
        "id": "lamp-lock",
        "name": "lamp lock",
        "type": "fixed",
        "parent": "signal-arm",
        "child": "lamp",
        "anchorParent": [
          2.5500000000000003,
          0,
          0
        ],
        "anchorChild": [
          -0.027499999999999858,
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
      "base",
      "post",
      "signal-arm",
      "lamp"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 冲击响应读数（h3-signal-switch-stand-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：1.0042
- C：0.0042
- D：0.2042

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.004169702599773726
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.00016450891676153548
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.000003816559456248789
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.000003816559456248789
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0000023871641629339203
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0000023871641629339203
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0000023871641629339203
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0000023871641629339203
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0000023871641629339203
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000023871641629339203
      },
      {
        "time": 1,
        "displacement": 0.0000023871641629339203
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.00348577499683225,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-signal-switch-stand-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：1.3
- B：-0.8
- C：0
- D：-1.3

```json
{
  "input": {
    "joint": "arm-pivot",
    "limits": [
      -0.8,
      0.8
    ],
    "units": "radians"
  },
  "answer": {
    "choiceIds": [
      "B",
      "C"
    ]
  }
}
```

### 约束故障诊断（h3-signal-switch-stand-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：post-foot
- B：arm-pivot
- C：lamp-lock

```json
{
  "input": {
    "endpoints": [
      "signal-arm",
      "lamp"
    ],
    "type": "fixed",
    "joints": [
      {
        "id": "post-foot",
        "name": "post foot",
        "type": "fixed",
        "parent": "base",
        "child": "post",
        "anchorParent": [
          0,
          0.14999999999999997,
          0
        ],
        "anchorChild": [
          0,
          -1.9499999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-pivot",
        "name": "arm pivot",
        "type": "revolute",
        "parent": "post",
        "child": "signal-arm",
        "anchorParent": [
          0,
          1.7999999999999998,
          0.55
        ],
        "anchorChild": [
          -2.0500000000000003,
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
        "id": "lamp-lock",
        "name": "lamp lock",
        "type": "fixed",
        "parent": "signal-arm",
        "child": "lamp",
        "anchorParent": [
          2.5500000000000003,
          0,
          0
        ],
        "anchorChild": [
          -0.027499999999999858,
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

### 主动检查收益（h3-signal-switch-stand-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-0
- B：query-1
- C：query-2

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
    "module": "lamp",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "C"
    ]
  }
}
```

### 不确定性与弃答（h3-signal-switch-stand-abstention）

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

### 观测后信念更新（h3-signal-switch-stand-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0.3333333333333333
- C：0
- D：0.25

```json
{
  "input": {
    "module": "lamp",
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
    "choiceId": "B"
  }
}
```

### 多目标工程权衡（h3-signal-switch-stand-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-2
- B：stock-0
- C：stock-1
- D：stock-3

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 8,
        "stiffness": 11,
        "mass": 1.2
      },
      {
        "id": "stock-1",
        "cost": 6,
        "stiffness": 9,
        "mass": 0.8
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 10,
        "mass": 1.4
      },
      {
        "id": "stock-3",
        "cost": 3,
        "stiffness": 11,
        "mass": 1.5
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "B",
      "C",
      "D"
    ]
  }
}
```

### 依赖装配（h3-signal-switch-stand-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:lamp",
        "label": "安装 lamp",
        "requires": [
          "present:signal-arm"
        ],
        "forbids": [
          "present:lamp"
        ],
        "adds": [
          "present:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp",
          "visible": true
        }
      },
      {
        "id": "place:base",
        "label": "安装 base",
        "requires": [],
        "forbids": [
          "present:base"
        ],
        "adds": [
          "present:base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "base",
          "visible": true
        }
      },
      {
        "id": "place:signal-arm",
        "label": "安装 signal-arm",
        "requires": [
          "present:post"
        ],
        "forbids": [
          "present:signal-arm"
        ],
        "adds": [
          "present:signal-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "signal-arm",
          "visible": true
        }
      },
      {
        "id": "place:post",
        "label": "安装 post",
        "requires": [
          "present:base"
        ],
        "forbids": [
          "present:post"
        ],
        "adds": [
          "present:post"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "post",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:base",
      "present:post",
      "present:signal-arm",
      "present:lamp"
    ],
    "budget": 4,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:base",
      "place:post",
      "place:signal-arm",
      "place:lamp"
    ]
  }
}
```

### 依赖拆解（h3-signal-switch-stand-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:base",
      "present:post",
      "present:signal-arm",
      "present:lamp"
    ],
    "initialModules": [
      "base",
      "post",
      "signal-arm",
      "lamp"
    ],
    "actions": [
      {
        "id": "remove:base",
        "label": "拆除 base",
        "requires": [
          "present:base"
        ],
        "forbids": [
          "present:post"
        ],
        "adds": [
          "removed:base"
        ],
        "deletes": [
          "present:base"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "base",
          "visible": false
        }
      },
      {
        "id": "remove:post",
        "label": "拆除 post",
        "requires": [
          "present:post"
        ],
        "forbids": [
          "present:signal-arm"
        ],
        "adds": [
          "removed:post"
        ],
        "deletes": [
          "present:post"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "post",
          "visible": false
        }
      },
      {
        "id": "remove:signal-arm",
        "label": "拆除 signal-arm",
        "requires": [
          "present:signal-arm"
        ],
        "forbids": [
          "present:lamp"
        ],
        "adds": [
          "removed:signal-arm"
        ],
        "deletes": [
          "present:signal-arm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "signal-arm",
          "visible": false
        }
      },
      {
        "id": "remove:lamp",
        "label": "拆除 lamp",
        "requires": [
          "present:lamp"
        ],
        "forbids": [],
        "adds": [
          "removed:lamp"
        ],
        "deletes": [
          "present:lamp"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lamp",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:lamp",
      "removed:signal-arm",
      "removed:post",
      "removed:base"
    ],
    "budget": 4,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:lamp",
      "remove:signal-arm",
      "remove:post",
      "remove:base"
    ]
  }
}
```

### 承载维修（h3-signal-switch-stand-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:lamp",
      "closed:lamp"
    ],
    "initialModules": [
      "base",
      "post",
      "signal-arm",
      "lamp"
    ],
    "actions": [
      {
        "id": "support:lamp",
        "label": "support lamp",
        "requires": [
          "fault:lamp"
        ],
        "forbids": [
          "done:support:lamp"
        ],
        "adds": [
          "done:support:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "open:lamp",
        "label": "open lamp",
        "requires": [
          "done:support:lamp"
        ],
        "forbids": [
          "done:open:lamp"
        ],
        "adds": [
          "done:open:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "replace:lamp",
        "label": "replace lamp",
        "requires": [
          "done:remove:lamp"
        ],
        "forbids": [
          "done:replace:lamp"
        ],
        "adds": [
          "done:replace:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp",
          "visible": true
        }
      },
      {
        "id": "verify:lamp",
        "label": "verify lamp",
        "requires": [
          "done:replace:lamp"
        ],
        "forbids": [
          "done:verify:lamp"
        ],
        "adds": [
          "done:verify:lamp"
        ],
        "deletes": [
          "fault:lamp"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "close:lamp",
        "label": "close lamp",
        "requires": [
          "done:verify:lamp"
        ],
        "forbids": [
          "done:close:lamp"
        ],
        "adds": [
          "done:close:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "release:lamp",
        "label": "release lamp",
        "requires": [
          "done:close:lamp"
        ],
        "forbids": [
          "done:release:lamp"
        ],
        "adds": [
          "done:release:lamp",
          "repaired:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "remove:lamp",
        "label": "remove lamp",
        "requires": [
          "done:open:lamp"
        ],
        "forbids": [
          "done:remove:lamp"
        ],
        "adds": [
          "done:remove:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "repaired:lamp"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:lamp",
      "open:lamp",
      "remove:lamp",
      "replace:lamp",
      "verify:lamp",
      "close:lamp",
      "release:lamp"
    ]
  }
}
```

### 复合编辑验证（h3-signal-switch-stand-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:lamp",
      "closed:lamp"
    ],
    "initialModules": [
      "base",
      "post",
      "signal-arm",
      "lamp"
    ],
    "actions": [
      {
        "id": "support:lamp",
        "label": "support lamp",
        "requires": [
          "fault:lamp"
        ],
        "forbids": [
          "done:support:lamp"
        ],
        "adds": [
          "done:support:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "open:lamp",
        "label": "open lamp",
        "requires": [
          "done:support:lamp"
        ],
        "forbids": [
          "done:open:lamp"
        ],
        "adds": [
          "done:open:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "verify:lamp",
        "label": "verify lamp",
        "requires": [
          "done:recolor:lamp"
        ],
        "forbids": [
          "done:verify:lamp"
        ],
        "adds": [
          "done:verify:lamp"
        ],
        "deletes": [
          "fault:lamp"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "close:lamp",
        "label": "close lamp",
        "requires": [
          "done:verify:lamp"
        ],
        "forbids": [
          "done:close:lamp"
        ],
        "adds": [
          "done:close:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "recolor:lamp",
        "label": "recolor lamp",
        "requires": [
          "done:open:lamp"
        ],
        "forbids": [
          "done:recolor:lamp"
        ],
        "adds": [
          "done:recolor:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp",
          "color": "#ea7635"
        }
      },
      {
        "id": "release:lamp",
        "label": "release lamp",
        "requires": [
          "done:close:lamp"
        ],
        "forbids": [
          "done:release:lamp"
        ],
        "adds": [
          "done:release:lamp",
          "repaired:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      }
    ],
    "goalFacts": [
      "repaired:lamp"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:lamp",
      "open:lamp",
      "recolor:lamp",
      "verify:lamp",
      "close:lamp",
      "release:lamp"
    ]
  }
}
```

### 跨区域联合维修（h3-signal-switch-stand-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:lamp",
      "closed:lamp"
    ],
    "initialModules": [
      "base",
      "post",
      "signal-arm",
      "lamp"
    ],
    "actions": [
      {
        "id": "support:lamp",
        "label": "support lamp",
        "requires": [
          "fault:lamp"
        ],
        "forbids": [
          "done:support:lamp"
        ],
        "adds": [
          "done:support:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "open:lamp",
        "label": "open lamp",
        "requires": [
          "done:support:lamp"
        ],
        "forbids": [
          "done:open:lamp"
        ],
        "adds": [
          "done:open:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "replace:lamp",
        "label": "replace lamp",
        "requires": [
          "done:remove:lamp"
        ],
        "forbids": [
          "done:replace:lamp"
        ],
        "adds": [
          "done:replace:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp",
          "visible": true
        }
      },
      {
        "id": "verify:lamp",
        "label": "verify lamp",
        "requires": [
          "done:replace:lamp"
        ],
        "forbids": [
          "done:verify:lamp"
        ],
        "adds": [
          "done:verify:lamp"
        ],
        "deletes": [
          "fault:lamp"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "close:lamp",
        "label": "close lamp",
        "requires": [
          "done:verify:lamp"
        ],
        "forbids": [
          "done:close:lamp"
        ],
        "adds": [
          "done:close:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "release:lamp",
        "label": "release lamp",
        "requires": [
          "done:close:lamp"
        ],
        "forbids": [
          "done:release:lamp"
        ],
        "adds": [
          "done:release:lamp",
          "repaired:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "remove:lamp",
        "label": "remove lamp",
        "requires": [
          "done:open:lamp"
        ],
        "forbids": [
          "done:remove:lamp"
        ],
        "adds": [
          "done:remove:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "repaired:lamp"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:lamp",
      "open:lamp",
      "remove:lamp",
      "replace:lamp",
      "verify:lamp",
      "close:lamp",
      "release:lamp"
    ]
  }
}
```

### 多工位资源调度（h3-signal-switch-stand-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "base",
        "duration": 2,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "post",
        "duration": 2,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "signal-arm",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "lamp",
        "duration": 2,
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
      "job-3": 2
    }
  }
}
```

### 检查后条件策略（h3-signal-switch-stand-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "lamp",
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

### 局部坐标变换（h3-signal-switch-stand-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[6.6,5.1,1.55]
- B：[5.6,4.1,0.55]
- C：[0.9725,0,0]

```json
{
  "input": {
    "localPoint": [
      0.9725000000000001,
      0,
      0
    ],
    "rotationXYZW": [
      0,
      0,
      0,
      1
    ],
    "translation": [
      4.6275,
      4.1,
      0.55
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 正交视图投影（h3-signal-switch-stand-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[5,2]
- B：[2,3]
- C：[0,0]
- D：[-3,5]

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
    "choiceId": "D"
  }
}
```

### 空间相对关系（h3-signal-switch-stand-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：greater
- B：less
- C：equal

```json
{
  "input": {
    "A": {
      "id": "base",
      "position": [
        0,
        0.2,
        0
      ]
    },
    "B": {
      "id": "lamp",
      "position": [
        4.6275,
        4.1,
        0.55
      ]
    },
    "axis": "y"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 约束自由度（h3-signal-switch-stand-joint-axis）

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
      "id": "arm-pivot",
      "name": "arm pivot",
      "type": "revolute",
      "parent": "post",
      "child": "signal-arm",
      "anchorParent": [
        0,
        1.7999999999999998,
        0.55
      ],
      "anchorChild": [
        -2.0500000000000003,
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
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 维修间隙预算（h3-signal-switch-stand-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "lamp",
    "aperture": 0.41999999999999993,
    "toolWidth": 0.35,
    "eachSideMargin": 0.05
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-signal-switch-stand-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,-6]
- B：[0,0,6]
- C：[0,0,0]
- D：[0,-1,0]

```json
{
  "input": {
    "module": "lamp",
    "lever": [
      1,
      2,
      0
    ],
    "force": [
      0,
      -6,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 非均匀先验更新（h3-signal-switch-stand-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：1
- B：0.16666666666666666
- C：0.125
- D：0

```json
{
  "input": {
    "module": "lamp",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      5,
      1,
      2
    ],
    "compatible": [
      "normal",
      "jammed"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 风险最小决策（h3-signal-switch-stand-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.1,
    "repairCost": 4,
    "failureLoss": 7,
    "module": "lamp"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-signal-switch-stand-trace-threshold）

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
        "displacement": 0.004169702599773726
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.00016450891676153548
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.000003816559456248789
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.000003816559456248789
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0000023871641629339203
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0000023871641629339203
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0000023871641629339203
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0000023871641629339203
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0000023871641629339203
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000023871641629339203
      },
      {
        "time": 1,
        "displacement": 0.0000023871641629339203
      }
    ],
    "threshold": 0.003335762079818981
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-signal-switch-stand-guarded-repair）

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
        "id": "release:lamp",
        "label": "release lamp",
        "requires": [
          "done:relock:lamp"
        ],
        "forbids": [
          "done:release:lamp"
        ],
        "adds": [
          "done:release:lamp",
          "ready:lamp",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "relock:lamp",
        "label": "relock lamp",
        "requires": [
          "done:verify:lamp"
        ],
        "forbids": [
          "done:relock:lamp"
        ],
        "adds": [
          "done:relock:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "verify:lamp",
        "label": "verify lamp",
        "requires": [
          "done:replace:lamp"
        ],
        "forbids": [
          "done:verify:lamp"
        ],
        "adds": [
          "done:verify:lamp"
        ],
        "deletes": [
          "fault:lamp",
          "misaligned:lamp"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "replace:lamp",
        "label": "replace lamp",
        "requires": [
          "done:unlock:lamp"
        ],
        "forbids": [
          "done:replace:lamp"
        ],
        "adds": [
          "done:replace:lamp"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "unlock:lamp",
        "label": "unlock lamp",
        "requires": [
          "done:support:lamp"
        ],
        "forbids": [
          "done:unlock:lamp"
        ],
        "adds": [
          "done:unlock:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "support:lamp",
        "label": "support lamp",
        "requires": [
          "done:isolate:lamp"
        ],
        "forbids": [
          "done:support:lamp"
        ],
        "adds": [
          "done:support:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "isolate:lamp",
        "label": "isolate lamp",
        "requires": [
          "tool:free",
          "fault:lamp"
        ],
        "forbids": [
          "done:isolate:lamp"
        ],
        "adds": [
          "done:isolate:lamp"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:lamp"
    ],
    "initialModules": [
      "base",
      "post",
      "signal-arm",
      "lamp"
    ],
    "goalFacts": [
      "ready:lamp"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:lamp",
      "support:lamp",
      "unlock:lamp",
      "replace:lamp",
      "verify:lamp",
      "relock:lamp",
      "release:lamp"
    ]
  }
}
```

### 失败状态回退（h3-signal-switch-stand-rollback）

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
        "id": "resume:lamp",
        "label": "resume lamp",
        "requires": [
          "done:verify:lamp"
        ],
        "forbids": [
          "done:resume:lamp"
        ],
        "adds": [
          "done:resume:lamp",
          "ready:lamp",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "verify:lamp",
        "label": "verify lamp",
        "requires": [
          "done:align:lamp"
        ],
        "forbids": [
          "done:verify:lamp"
        ],
        "adds": [
          "done:verify:lamp"
        ],
        "deletes": [
          "fault:lamp",
          "misaligned:lamp"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "align:lamp",
        "label": "align lamp",
        "requires": [
          "done:undo:lamp"
        ],
        "forbids": [
          "done:align:lamp"
        ],
        "adds": [
          "done:align:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp",
          "visible": true
        }
      },
      {
        "id": "undo:lamp",
        "label": "undo lamp",
        "requires": [
          "done:isolate:lamp"
        ],
        "forbids": [
          "done:undo:lamp"
        ],
        "adds": [
          "done:undo:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp",
          "visible": false
        }
      },
      {
        "id": "isolate:lamp",
        "label": "isolate lamp",
        "requires": [
          "tool:free",
          "fault:lamp"
        ],
        "forbids": [
          "done:isolate:lamp"
        ],
        "adds": [
          "done:isolate:lamp"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:lamp",
      "misaligned:lamp"
    ],
    "initialModules": [
      "base",
      "post",
      "signal-arm",
      "lamp"
    ],
    "goalFacts": [
      "ready:lamp"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:lamp",
      "undo:lamp",
      "align:lamp",
      "verify:lamp",
      "resume:lamp"
    ]
  }
}
```

### 共享工具协同维修（h3-signal-switch-stand-resource-repair）

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
        "id": "release:lamp",
        "label": "release lamp",
        "requires": [
          "done:relock:lamp"
        ],
        "forbids": [
          "done:release:lamp"
        ],
        "adds": [
          "done:release:lamp",
          "ready:lamp",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "relock:lamp",
        "label": "relock lamp",
        "requires": [
          "done:verify:lamp"
        ],
        "forbids": [
          "done:relock:lamp"
        ],
        "adds": [
          "done:relock:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "verify:lamp",
        "label": "verify lamp",
        "requires": [
          "done:replace:lamp"
        ],
        "forbids": [
          "done:verify:lamp"
        ],
        "adds": [
          "done:verify:lamp"
        ],
        "deletes": [
          "fault:lamp",
          "misaligned:lamp"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "replace:lamp",
        "label": "replace lamp",
        "requires": [
          "done:unlock:lamp"
        ],
        "forbids": [
          "done:replace:lamp"
        ],
        "adds": [
          "done:replace:lamp"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "unlock:lamp",
        "label": "unlock lamp",
        "requires": [
          "done:support:lamp"
        ],
        "forbids": [
          "done:unlock:lamp"
        ],
        "adds": [
          "done:unlock:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "support:lamp",
        "label": "support lamp",
        "requires": [
          "done:isolate:lamp"
        ],
        "forbids": [
          "done:support:lamp"
        ],
        "adds": [
          "done:support:lamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "isolate:lamp",
        "label": "isolate lamp",
        "requires": [
          "tool:free",
          "fault:lamp"
        ],
        "forbids": [
          "done:isolate:lamp"
        ],
        "adds": [
          "done:isolate:lamp"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lamp"
        }
      },
      {
        "id": "release:signal-arm",
        "label": "release signal-arm",
        "requires": [
          "done:relock:signal-arm"
        ],
        "forbids": [
          "done:release:signal-arm"
        ],
        "adds": [
          "done:release:signal-arm",
          "ready:signal-arm",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "signal-arm"
        }
      },
      {
        "id": "relock:signal-arm",
        "label": "relock signal-arm",
        "requires": [
          "done:verify:signal-arm"
        ],
        "forbids": [
          "done:relock:signal-arm"
        ],
        "adds": [
          "done:relock:signal-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "signal-arm"
        }
      },
      {
        "id": "verify:signal-arm",
        "label": "verify signal-arm",
        "requires": [
          "done:replace:signal-arm"
        ],
        "forbids": [
          "done:verify:signal-arm"
        ],
        "adds": [
          "done:verify:signal-arm"
        ],
        "deletes": [
          "fault:signal-arm",
          "misaligned:signal-arm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "signal-arm"
        }
      },
      {
        "id": "replace:signal-arm",
        "label": "replace signal-arm",
        "requires": [
          "done:unlock:signal-arm"
        ],
        "forbids": [
          "done:replace:signal-arm"
        ],
        "adds": [
          "done:replace:signal-arm"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "signal-arm"
        }
      },
      {
        "id": "unlock:signal-arm",
        "label": "unlock signal-arm",
        "requires": [
          "done:support:signal-arm"
        ],
        "forbids": [
          "done:unlock:signal-arm"
        ],
        "adds": [
          "done:unlock:signal-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "signal-arm"
        }
      },
      {
        "id": "support:signal-arm",
        "label": "support signal-arm",
        "requires": [
          "done:isolate:signal-arm"
        ],
        "forbids": [
          "done:support:signal-arm"
        ],
        "adds": [
          "done:support:signal-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "signal-arm"
        }
      },
      {
        "id": "isolate:signal-arm",
        "label": "isolate signal-arm",
        "requires": [
          "tool:free",
          "fault:signal-arm"
        ],
        "forbids": [
          "done:isolate:signal-arm"
        ],
        "adds": [
          "done:isolate:signal-arm"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "signal-arm"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:signal-arm",
      "fault:lamp"
    ],
    "initialModules": [
      "base",
      "post",
      "signal-arm",
      "lamp"
    ],
    "goalFacts": [
      "ready:signal-arm",
      "ready:lamp"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 16
  },
  "answer": {
    "actionIds": [
      "isolate:lamp",
      "support:lamp",
      "unlock:lamp",
      "replace:lamp",
      "verify:lamp",
      "relock:lamp",
      "release:lamp",
      "isolate:signal-arm",
      "support:signal-arm",
      "unlock:signal-arm",
      "replace:signal-arm",
      "verify:signal-arm",
      "relock:signal-arm",
      "release:signal-arm"
    ]
  }
}
```

### 预算约束检查策略（h3-signal-switch-stand-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "lamp",
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
        "cost": 3,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      },
      {
        "id": "thermal",
        "cost": 2,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      }
    ],
    "budget": 2
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
