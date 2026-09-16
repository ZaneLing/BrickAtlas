## D1 样品转盘

### 模块识别（h3-sample-carousel-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：rotor
- B：service-cartridge
- C：foundation
- D：mount

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "foundation",
        "name": "foundation"
      },
      {
        "id": "mount",
        "name": "mount"
      },
      {
        "id": "rotor",
        "name": "rotor"
      },
      {
        "id": "service-cartridge",
        "name": "service cartridge"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 部件计数（h3-sample-carousel-count）

模块 service-cartridge 有多少个可视零件？

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
        "id": "mount-p7",
        "moduleId": "mount",
        "shape": "cylinder",
        "color": "#dfebed"
      },
      {
        "id": "rotor-p8",
        "moduleId": "rotor",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "rotor-p9",
        "moduleId": "rotor",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "rotor-p10",
        "moduleId": "rotor",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "rotor-p11",
        "moduleId": "rotor",
        "shape": "beam",
        "color": "#45a080"
      },
      {
        "id": "service-cartridge-p12",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p13",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p14",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p15",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-sample-carousel-color）

零件 service-cartridge-p12 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#2878b8
- B：#d43a32
- C：#f2bf3c
- D：#dc6040

```json
{
  "input": {
    "part": {
      "id": "service-cartridge-p12",
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
    "choiceId": "D"
  }
}
```

### 三维位置（h3-sample-carousel-position）

模块 service-cartridge 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,0.35,0]
- B：[0,1.2,0]
- C：[0.24757694770007121,2.1,-0.004183202882357184]
- D：[0,0.8,2.2]

```json
{
  "input": {
    "centers": {
      "foundation": [
        0,
        0.35,
        0
      ],
      "mount": [
        0,
        1.2,
        0
      ],
      "rotor": [
        0.24757694770007121,
        2.1,
        -0.004183202882357184
      ],
      "service-cartridge": [
        0,
        0.8,
        2.2
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节类型（h3-sample-carousel-joint-type）

rotor-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：fixed
- B：prismatic
- C：spring
- D：revolute

```json
{
  "input": {
    "joint": {
      "id": "rotor-joint",
      "name": "rotor interface",
      "parent": "mount",
      "child": "rotor",
      "type": "revolute",
      "anchorParent": [
        0,
        0.9000000000000001,
        0
      ],
      "anchorChild": [
        -0.24757694770007121,
        0,
        0.004183202882357184
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
    "choiceId": "D"
  }
}
```

### 直接连接（h3-sample-carousel-parent）

service-cartridge 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["foundation","mount","rotor","service-cartridge"]
- B：["foundation"]
- C：["service-cartridge"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "mount-joint",
        "name": "mount interface",
        "parent": "foundation",
        "child": "mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8499999999999999,
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
        "id": "rotor-joint",
        "name": "rotor interface",
        "parent": "mount",
        "child": "rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9000000000000001,
          0
        ],
        "anchorChild": [
          -0.24757694770007121,
          0,
          0.004183202882357184
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
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          0,
          0.4,
          2.2
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
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 基座识别（h3-sample-carousel-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["foundation","mount","rotor","service-cartridge"]
- B：["service-cartridge"]
- C：["foundation"]
- D：[]

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
        "id": "mount",
        "name": "mount",
        "role": "support",
        "position": [
          0,
          1.2,
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
        "id": "rotor",
        "name": "rotor",
        "role": "actuator",
        "position": [
          0.24757694770007121,
          2.1,
          -0.004183202882357184
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
          0,
          0.8,
          2.2
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

### 接口计数（h3-sample-carousel-degree）

service-cartridge 连接几个声明关节？平行关节分别计数。

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
        "id": "mount-joint",
        "name": "mount interface",
        "parent": "foundation",
        "child": "mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8499999999999999,
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
        "id": "rotor-joint",
        "name": "rotor interface",
        "parent": "mount",
        "child": "rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9000000000000001,
          0
        ],
        "anchorChild": [
          -0.24757694770007121,
          0,
          0.004183202882357184
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
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          0,
          0.4,
          2.2
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
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 局部改色（h3-sample-carousel-recolor）

仅将 service-cartridge-p12 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"service-cartridge-p12","color":"#2878b8"}
- B：{"id":"*","color":"#e8792e"}
- C：{"id":"service-cartridge-p12","color":"#e8792e"}
- D：{"id":"service-cartridge-p13","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "service-cartridge-p12",
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

### 补装部件（h3-sample-carousel-add）

模块 service-cartridge 缺失零件 service-cartridge-p12。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"service-cartridge-p12","moduleId":"foundation","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#dc6040","rotation":[0,0,0,1]}
- B：{"id":"service-cartridge-p12","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[3,3,3],"color":"#dc6040","rotation":[0,0,0,1]}
- C：{"id":"service-cartridge-p12","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#000000","rotation":[0,0,0,1]}
- D：{"id":"service-cartridge-p12","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#dc6040","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "service-cartridge-p12",
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
      "mount-p7",
      "rotor-p8",
      "rotor-p9",
      "rotor-p10",
      "rotor-p11",
      "service-cartridge-p13",
      "service-cartridge-p14",
      "service-cartridge-p15"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 安全拆除（h3-sample-carousel-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["foundation"]
- B：[]
- C：["foundation","mount","rotor","service-cartridge"]
- D：["rotor","service-cartridge"]

```json
{
  "input": {
    "joints": [
      {
        "id": "mount-joint",
        "name": "mount interface",
        "parent": "foundation",
        "child": "mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8499999999999999,
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
        "id": "rotor-joint",
        "name": "rotor interface",
        "parent": "mount",
        "child": "rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9000000000000001,
          0
        ],
        "anchorChild": [
          -0.24757694770007121,
          0,
          0.004183202882357184
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
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          0,
          0.4,
          2.2
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
      }
    ],
    "modules": [
      "foundation",
      "mount",
      "rotor",
      "service-cartridge"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 替换选择（h3-sample-carousel-replace）

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
        "mass": 0.9
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 11,
        "mass": 0.6
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 7,
        "mass": 1.6
      },
      {
        "id": "stock-3",
        "cost": 2,
        "stiffness": 6,
        "mass": 1.8
      }
    ],
    "maxCost": 6
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-sample-carousel-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,2,0]
- C：[-1,0,2]
- D：[1,0,-2]

```json
{
  "input": {
    "delta": [
      1,
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

### 姿态纠偏（h3-sample-carousel-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：0
- B：-180
- C：90
- D：-90

```json
{
  "input": {
    "module": "service-cartridge",
    "currentYaw": 225,
    "targetYaw": 315
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 下一步放置（h3-sample-carousel-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["foundation","mount"]
- B：["foundation"]
- C：["rotor","service-cartridge"]
- D：[]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "mount"
    ],
    "joints": [
      {
        "id": "mount-joint",
        "name": "mount interface",
        "parent": "foundation",
        "child": "mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8499999999999999,
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
        "id": "rotor-joint",
        "name": "rotor interface",
        "parent": "mount",
        "child": "rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9000000000000001,
          0
        ],
        "anchorChild": [
          -0.24757694770007121,
          0,
          0.004183202882357184
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
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          0,
          0.4,
          2.2
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
      }
    ],
    "modules": [
      "foundation",
      "mount",
      "rotor",
      "service-cartridge"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 库存核算（h3-sample-carousel-inventory）

备件库有 4 件，替换模块需 4 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：1
- B：3
- C：0

```json
{
  "input": {
    "available": 4,
    "required": 4
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 子装配边界（h3-sample-carousel-boundary）

隔离 service-cartridge 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：[]
- B：["mount-joint","rotor-joint","service-cartridge-joint"]
- C：["rotor-joint"]
- D：["service-cartridge-joint"]

```json
{
  "input": {
    "joints": [
      {
        "id": "mount-joint",
        "name": "mount interface",
        "parent": "foundation",
        "child": "mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8499999999999999,
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
        "id": "rotor-joint",
        "name": "rotor interface",
        "parent": "mount",
        "child": "rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9000000000000001,
          0
        ],
        "anchorChild": [
          -0.24757694770007121,
          0,
          0.004183202882357184
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
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          0,
          0.4,
          2.2
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
      }
    ],
    "target": "service-cartridge"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 最小干预（h3-sample-carousel-no-op）

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

### 全过程依赖（h3-sample-carousel-prefix）

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
      "mount",
      "foundation",
      "rotor",
      "service-cartridge"
    ],
    "joints": [
      {
        "id": "mount-joint",
        "name": "mount interface",
        "parent": "foundation",
        "child": "mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8499999999999999,
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
        "id": "rotor-joint",
        "name": "rotor interface",
        "parent": "mount",
        "child": "rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9000000000000001,
          0
        ],
        "anchorChild": [
          -0.24757694770007121,
          0,
          0.004183202882357184
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
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          0,
          0.4,
          2.2
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
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 连续维修路径（h3-sample-carousel-access）

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
          6.25,
          0.8,
          2.2
        ],
        "end": [
          0,
          0.8,
          2.2
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
          6.25,
          2.2
        ],
        "end": [
          0,
          0.8,
          2.2
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
          0.8,
          7.19
        ],
        "end": [
          0,
          0.8,
          2.2
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

### 支撑反事实（h3-sample-carousel-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["mount"]
- B：[]
- C：["foundation","mount","rotor","service-cartridge"]
- D：["rotor"]

```json
{
  "input": {
    "removed": "mount",
    "roots": [
      "foundation"
    ],
    "joints": [
      {
        "id": "mount-joint",
        "name": "mount interface",
        "parent": "foundation",
        "child": "mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8499999999999999,
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
        "id": "rotor-joint",
        "name": "rotor interface",
        "parent": "mount",
        "child": "rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9000000000000001,
          0
        ],
        "anchorChild": [
          -0.24757694770007121,
          0,
          0.004183202882357184
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
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          0,
          0.4,
          2.2
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
      }
    ],
    "modules": [
      "foundation",
      "mount",
      "rotor",
      "service-cartridge"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 冲击响应读数（h3-sample-carousel-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：1.0001
- C：0.0001
- D：0.2001

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0001475538707307192
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0000018410196227049627
      },
      {
        "time": 0.20833333333333334,
        "displacement": 2.5545415972204395e-7
      },
      {
        "time": 0.30833333333333335,
        "displacement": 2.457562461863554e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 2.4027400458748785e-7
      },
      {
        "time": 0.5083333333333333,
        "displacement": 2.4027400458748785e-7
      },
      {
        "time": 0.6083333333333333,
        "displacement": 2.4027400458748785e-7
      },
      {
        "time": 0.7083333333333334,
        "displacement": 2.4027400458748785e-7
      },
      {
        "time": 0.8083333333333333,
        "displacement": 2.4027400458748785e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 2.4027400458748785e-7
      },
      {
        "time": 1,
        "displacement": 2.4027400458748785e-7
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 3.6730734675109543e-7,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-sample-carousel-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-0.8
- B：0
- C：-1.3
- D：1.3

```json
{
  "input": {
    "joint": "rotor-joint",
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

### 约束故障诊断（h3-sample-carousel-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：service-cartridge-joint
- B：mount-joint
- C：rotor-joint

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
        "id": "mount-joint",
        "name": "mount interface",
        "parent": "foundation",
        "child": "mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.8499999999999999,
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
        "id": "rotor-joint",
        "name": "rotor interface",
        "parent": "mount",
        "child": "rotor",
        "type": "revolute",
        "anchorParent": [
          0,
          0.9000000000000001,
          0
        ],
        "anchorChild": [
          -0.24757694770007121,
          0,
          0.004183202882357184
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
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          0,
          0.4,
          2.2
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

### 主动检查收益（h3-sample-carousel-information-gain）

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

### 不确定性与弃答（h3-sample-carousel-abstention）

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

### 观测后信念更新（h3-sample-carousel-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.25
- B：0.3333333333333333
- C：1
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
      "positive",
      "positive"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 多目标工程权衡（h3-sample-carousel-pareto）

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
        "cost": 3,
        "stiffness": 11,
        "mass": 0.9
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 11,
        "mass": 0.6
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 7,
        "mass": 1.6
      },
      {
        "id": "stock-3",
        "cost": 2,
        "stiffness": 6,
        "mass": 1.8
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

### 依赖装配（h3-sample-carousel-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:rotor",
        "label": "安装 rotor",
        "requires": [
          "present:mount"
        ],
        "forbids": [
          "present:rotor"
        ],
        "adds": [
          "present:rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor",
          "visible": true
        }
      },
      {
        "id": "place:mount",
        "label": "安装 mount",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:mount"
        ],
        "adds": [
          "present:mount"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "mount",
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
      "present:mount",
      "present:rotor",
      "present:service-cartridge"
    ],
    "budget": 4,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:mount",
      "place:rotor",
      "place:service-cartridge"
    ]
  }
}
```

### 依赖拆解（h3-sample-carousel-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:mount",
      "present:rotor",
      "present:service-cartridge"
    ],
    "initialModules": [
      "foundation",
      "mount",
      "rotor",
      "service-cartridge"
    ],
    "actions": [
      {
        "id": "remove:mount",
        "label": "拆除 mount",
        "requires": [
          "present:mount"
        ],
        "forbids": [
          "present:rotor"
        ],
        "adds": [
          "removed:mount"
        ],
        "deletes": [
          "present:mount"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "mount",
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
        "id": "remove:rotor",
        "label": "拆除 rotor",
        "requires": [
          "present:rotor"
        ],
        "forbids": [],
        "adds": [
          "removed:rotor"
        ],
        "deletes": [
          "present:rotor"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rotor",
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
          "present:mount",
          "present:service-cartridge"
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
      }
    ],
    "goalFacts": [
      "removed:service-cartridge",
      "removed:rotor",
      "removed:mount",
      "removed:foundation"
    ],
    "budget": 4,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:service-cartridge",
      "remove:rotor",
      "remove:mount",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-sample-carousel-service-repair）

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
      "mount",
      "rotor",
      "service-cartridge"
    ],
    "actions": [
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

### 复合编辑验证（h3-sample-carousel-compound-edit）

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
      "mount",
      "rotor",
      "service-cartridge"
    ],
    "actions": [
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

### 跨区域联合维修（h3-sample-carousel-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:service-cartridge",
      "closed:service-cartridge"
    ],
    "initialModules": [
      "foundation",
      "mount",
      "rotor",
      "service-cartridge"
    ],
    "actions": [
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

### 多工位资源调度（h3-sample-carousel-scheduling）

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
        "module": "mount",
        "duration": 3,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "rotor",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "service-cartridge",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      }
    ],
    "deadline": 6
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

### 检查后条件策略（h3-sample-carousel-policy）

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

### 局部坐标变换（h3-sample-carousel-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[0.5,0.75,1.7]
- B：[0.5,1.75,2.7]
- C：[-0.5,0.75,1.7]
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
      0,
      0.8,
      2.2
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-sample-carousel-projection）

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

### 空间相对关系（h3-sample-carousel-relative-order）

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
        0.35,
        0
      ]
    },
    "B": {
      "id": "service-cartridge",
      "position": [
        0,
        0.8,
        2.2
      ]
    },
    "axis": "x"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 约束自由度（h3-sample-carousel-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：6
- B：0
- C：1
- D：3

```json
{
  "input": {
    "joint": {
      "id": "mount-joint",
      "name": "mount interface",
      "parent": "foundation",
      "child": "mount",
      "type": "fixed",
      "anchorParent": [
        0,
        0.8499999999999999,
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
    "choiceId": "B"
  }
}
```

### 维修间隙预算（h3-sample-carousel-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "service-cartridge",
    "aperture": 0.38999999999999996,
    "toolWidth": 0.35,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-sample-carousel-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,-1,0]
- B：[0,0,-3]
- C：[0,0,3]
- D：[0,0,0]

```json
{
  "input": {
    "module": "service-cartridge",
    "lever": [
      1,
      1,
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
    "choiceId": "B"
  }
}
```

### 非均匀先验更新（h3-sample-carousel-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0
- C：1
- D：0.6666666666666666

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
      2,
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

### 风险最小决策（h3-sample-carousel-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.6,
    "repairCost": 2,
    "failureLoss": 7,
    "module": "service-cartridge"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-sample-carousel-trace-threshold）

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
        "displacement": 0.0001475538707307192
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0000018410196227049627
      },
      {
        "time": 0.20833333333333334,
        "displacement": 2.5545415972204395e-7
      },
      {
        "time": 0.30833333333333335,
        "displacement": 2.457562461863554e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 2.4027400458748785e-7
      },
      {
        "time": 0.5083333333333333,
        "displacement": 2.4027400458748785e-7
      },
      {
        "time": 0.6083333333333333,
        "displacement": 2.4027400458748785e-7
      },
      {
        "time": 0.7083333333333334,
        "displacement": 2.4027400458748785e-7
      },
      {
        "time": 0.8083333333333333,
        "displacement": 2.4027400458748785e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 2.4027400458748785e-7
      },
      {
        "time": 1,
        "displacement": 2.4027400458748785e-7
      }
    ],
    "threshold": 0.00017706464487686303
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-sample-carousel-guarded-repair）

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
      "mount",
      "rotor",
      "service-cartridge"
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

### 失败状态回退（h3-sample-carousel-rollback）

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
      "mount",
      "rotor",
      "service-cartridge"
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

### 共享工具协同维修（h3-sample-carousel-resource-repair）

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
      },
      {
        "id": "release:rotor",
        "label": "release rotor",
        "requires": [
          "done:relock:rotor"
        ],
        "forbids": [
          "done:release:rotor"
        ],
        "adds": [
          "done:release:rotor",
          "ready:rotor",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor"
        }
      },
      {
        "id": "relock:rotor",
        "label": "relock rotor",
        "requires": [
          "done:verify:rotor"
        ],
        "forbids": [
          "done:relock:rotor"
        ],
        "adds": [
          "done:relock:rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor"
        }
      },
      {
        "id": "verify:rotor",
        "label": "verify rotor",
        "requires": [
          "done:replace:rotor"
        ],
        "forbids": [
          "done:verify:rotor"
        ],
        "adds": [
          "done:verify:rotor"
        ],
        "deletes": [
          "fault:rotor",
          "misaligned:rotor"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rotor"
        }
      },
      {
        "id": "replace:rotor",
        "label": "replace rotor",
        "requires": [
          "done:unlock:rotor"
        ],
        "forbids": [
          "done:replace:rotor"
        ],
        "adds": [
          "done:replace:rotor"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "rotor"
        }
      },
      {
        "id": "unlock:rotor",
        "label": "unlock rotor",
        "requires": [
          "done:support:rotor"
        ],
        "forbids": [
          "done:unlock:rotor"
        ],
        "adds": [
          "done:unlock:rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor"
        }
      },
      {
        "id": "support:rotor",
        "label": "support rotor",
        "requires": [
          "done:isolate:rotor"
        ],
        "forbids": [
          "done:support:rotor"
        ],
        "adds": [
          "done:support:rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rotor"
        }
      },
      {
        "id": "isolate:rotor",
        "label": "isolate rotor",
        "requires": [
          "tool:free",
          "fault:rotor"
        ],
        "forbids": [
          "done:isolate:rotor"
        ],
        "adds": [
          "done:isolate:rotor"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rotor"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:rotor",
      "fault:service-cartridge"
    ],
    "initialModules": [
      "foundation",
      "mount",
      "rotor",
      "service-cartridge"
    ],
    "goalFacts": [
      "ready:rotor",
      "ready:service-cartridge"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 16
  },
  "answer": {
    "actionIds": [
      "isolate:service-cartridge",
      "support:service-cartridge",
      "unlock:service-cartridge",
      "replace:service-cartridge",
      "verify:service-cartridge",
      "relock:service-cartridge",
      "release:service-cartridge",
      "isolate:rotor",
      "support:rotor",
      "unlock:rotor",
      "replace:rotor",
      "verify:rotor",
      "relock:rotor",
      "release:rotor"
    ]
  }
}
```

### 预算约束检查策略（h3-sample-carousel-budget-policy）

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
        "cost": 0,
        "returns": {
          "nominal": "clear",
          "fault": "clear"
        }
      },
      {
        "id": "probe",
        "cost": 2,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "thermal",
        "cost": 1,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      }
    ],
    "budget": 1
  },
  "answer": {
    "queryId": "thermal",
    "decisions": {
      "clear": "continue",
      "alert": "replace"
    }
  }
}
```
