## D1 铰接安全舱盖

### 模块识别（h3-hinged-safety-hatch-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：lid
- B：latch
- C：frame

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "frame",
        "name": "Safety hatch frame"
      },
      {
        "id": "lid",
        "name": "Hinged safety lid"
      },
      {
        "id": "latch",
        "name": "Sliding latch cartridge"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 部件计数（h3-hinged-safety-hatch-count）

模块 latch 有多少个可视零件？

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
        "id": "h0001",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0002",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0003",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0004",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0005",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0006",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0007",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0008",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0009",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0010",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0011",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0012",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0013",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0014",
        "moduleId": "frame",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0015",
        "moduleId": "lid",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0016",
        "moduleId": "lid",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0017",
        "moduleId": "lid",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0018",
        "moduleId": "lid",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0019",
        "moduleId": "lid",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0020",
        "moduleId": "lid",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0021",
        "moduleId": "lid",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0022",
        "moduleId": "lid",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0023",
        "moduleId": "lid",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0024",
        "moduleId": "lid",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0025",
        "moduleId": "lid",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0026",
        "moduleId": "lid",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0027",
        "moduleId": "latch",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "h0028",
        "moduleId": "latch",
        "shape": "gear",
        "color": "#101820"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-hinged-safety-hatch-color）

零件 h0027 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#f2bf3c
- B：#c6cdd2
- C：#2878b8
- D：#d43a32

```json
{
  "input": {
    "part": {
      "id": "h0027",
      "moduleId": "latch",
      "shape": "beam",
      "size": [
        2,
        0.35,
        0.45
      ],
      "position": [
        -0.3125,
        0,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#c6cdd2"
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 三维位置（h3-hinged-safety-hatch-position）

模块 latch 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0.3125,1.7000000000000002,1.45]
- B：[0,0.55,0]
- C：[0,1.0999999999999999,0]
- D：[999,999,999]

```json
{
  "input": {
    "centers": {
      "frame": [
        0,
        0.55,
        0
      ],
      "lid": [
        0,
        1.0999999999999999,
        0
      ],
      "latch": [
        0.3125,
        1.7000000000000002,
        1.45
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节类型（h3-hinged-safety-hatch-joint-type）

lid-hinge 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：prismatic
- B：spring
- C：revolute
- D：fixed

```json
{
  "input": {
    "joint": {
      "id": "lid-hinge",
      "name": "lid hinge",
      "type": "revolute",
      "parent": "frame",
      "child": "lid",
      "anchorParent": [
        -2,
        0.44999999999999996,
        0
      ],
      "anchorChild": [
        -2,
        -0.09999999999999987,
        0
      ],
      "axis": [
        0,
        0,
        1
      ],
      "limits": [
        0,
        1.35
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 直接连接（h3-hinged-safety-hatch-parent）

latch 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["latch"]
- B：[]
- C：["frame","lid","latch"]
- D：["lid"]

```json
{
  "input": {
    "joints": [
      {
        "id": "lid-hinge",
        "name": "lid hinge",
        "type": "revolute",
        "parent": "frame",
        "child": "lid",
        "anchorParent": [
          -2,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -2,
          -0.09999999999999987,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.35
        ]
      },
      {
        "id": "latch-slide",
        "name": "latch slide",
        "type": "prismatic",
        "parent": "lid",
        "child": "latch",
        "anchorParent": [
          0,
          0.6000000000000001,
          1.45
        ],
        "anchorChild": [
          -0.3125,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 基座识别（h3-hinged-safety-hatch-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["latch"]
- B：["frame"]
- C：[]
- D：["frame","lid","latch"]

```json
{
  "input": {
    "modules": [
      {
        "id": "frame",
        "name": "Safety hatch frame",
        "role": "foundation",
        "anchored": true,
        "mass": 6,
        "position": [
          0,
          0.55,
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
        "id": "lid",
        "name": "Hinged safety lid",
        "role": "actuator",
        "anchored": false,
        "mass": 2,
        "position": [
          0,
          1.0999999999999999,
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
        "id": "latch",
        "name": "Sliding latch cartridge",
        "role": "service-module",
        "anchored": false,
        "mass": 0.5,
        "position": [
          0.3125,
          1.7,
          1.45
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

### 接口计数（h3-hinged-safety-hatch-degree）

latch 连接几个声明关节？平行关节分别计数。

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
        "id": "lid-hinge",
        "name": "lid hinge",
        "type": "revolute",
        "parent": "frame",
        "child": "lid",
        "anchorParent": [
          -2,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -2,
          -0.09999999999999987,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.35
        ]
      },
      {
        "id": "latch-slide",
        "name": "latch slide",
        "type": "prismatic",
        "parent": "lid",
        "child": "latch",
        "anchorParent": [
          0,
          0.6000000000000001,
          1.45
        ],
        "anchorChild": [
          -0.3125,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 局部改色（h3-hinged-safety-hatch-recolor）

仅将 h0027 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"h0027","color":"#e8792e"}
- B：{"id":"h0028","color":"#e8792e"}
- C：{"id":"h0027","color":"#2878b8"}
- D：{"id":"*","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "h0027",
      "moduleId": "latch",
      "shape": "beam",
      "size": [
        2,
        0.35,
        0.45
      ],
      "position": [
        -0.3125,
        0,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#c6cdd2"
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 补装部件（h3-hinged-safety-hatch-add）

模块 latch 缺失零件 h0027。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"h0027","moduleId":"frame","shape":"beam","size":[2,0.35,0.45],"position":[-0.3125,0,0],"rotation":[0,0,0,1],"color":"#c6cdd2"}
- B：{"id":"h0027","moduleId":"latch","shape":"beam","size":[3,3,3],"position":[-0.3125,0,0],"rotation":[0,0,0,1],"color":"#c6cdd2"}
- C：{"id":"h0027","moduleId":"latch","shape":"beam","size":[2,0.35,0.45],"position":[-0.3125,0,0],"rotation":[0,0,0,1],"color":"#000000"}
- D：{"id":"h0027","moduleId":"latch","shape":"beam","size":[2,0.35,0.45],"position":[-0.3125,0,0],"rotation":[0,0,0,1],"color":"#c6cdd2"}

```json
{
  "input": {
    "targetPart": {
      "id": "h0027",
      "moduleId": "latch",
      "shape": "beam",
      "size": [
        2,
        0.35,
        0.45
      ],
      "position": [
        -0.3125,
        0,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#c6cdd2"
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
      "h0021",
      "h0022",
      "h0023",
      "h0024",
      "h0025",
      "h0026",
      "h0028"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 安全拆除（h3-hinged-safety-hatch-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["frame","lid","latch"]
- B：["latch"]
- C：["frame"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "lid-hinge",
        "name": "lid hinge",
        "type": "revolute",
        "parent": "frame",
        "child": "lid",
        "anchorParent": [
          -2,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -2,
          -0.09999999999999987,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.35
        ]
      },
      {
        "id": "latch-slide",
        "name": "latch slide",
        "type": "prismatic",
        "parent": "lid",
        "child": "latch",
        "anchorParent": [
          0,
          0.6000000000000001,
          1.45
        ],
        "anchorChild": [
          -0.3125,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ],
    "modules": [
      "frame",
      "lid",
      "latch"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 替换选择（h3-hinged-safety-hatch-replace）

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
        "cost": 2,
        "stiffness": 3,
        "mass": 1.7
      },
      {
        "id": "stock-1",
        "cost": 7,
        "stiffness": 5,
        "mass": 1.2
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 4,
        "mass": 0.8
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 4,
        "mass": 1
      }
    ],
    "maxCost": 8
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 平移纠偏（h3-hinged-safety-hatch-translate）

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
    "target": "latch"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-hinged-safety-hatch-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：0
- B：-180
- C：-90
- D：90

```json
{
  "input": {
    "module": "latch",
    "currentYaw": 315,
    "targetYaw": 225
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 下一步放置（h3-hinged-safety-hatch-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["frame"]
- B：["latch"]
- C：[]
- D：["frame","lid"]

```json
{
  "input": {
    "prefix": [
      "frame",
      "lid"
    ],
    "joints": [
      {
        "id": "lid-hinge",
        "name": "lid hinge",
        "type": "revolute",
        "parent": "frame",
        "child": "lid",
        "anchorParent": [
          -2,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -2,
          -0.09999999999999987,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.35
        ]
      },
      {
        "id": "latch-slide",
        "name": "latch slide",
        "type": "prismatic",
        "parent": "lid",
        "child": "latch",
        "anchorParent": [
          0,
          0.6000000000000001,
          1.45
        ],
        "anchorChild": [
          -0.3125,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ],
    "modules": [
      "frame",
      "lid",
      "latch"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 库存核算（h3-hinged-safety-hatch-inventory）

备件库有 4 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：5
- B：2
- C：3
- D：1

```json
{
  "input": {
    "available": 4,
    "required": 2
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 子装配边界（h3-hinged-safety-hatch-boundary）

隔离 latch 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：[]
- B：["lid-hinge","latch-slide"]
- C：["lid-hinge"]
- D：["latch-slide"]

```json
{
  "input": {
    "joints": [
      {
        "id": "lid-hinge",
        "name": "lid hinge",
        "type": "revolute",
        "parent": "frame",
        "child": "lid",
        "anchorParent": [
          -2,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -2,
          -0.09999999999999987,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.35
        ]
      },
      {
        "id": "latch-slide",
        "name": "latch slide",
        "type": "prismatic",
        "parent": "lid",
        "child": "latch",
        "anchorParent": [
          0,
          0.6000000000000001,
          1.45
        ],
        "anchorChild": [
          -0.3125,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ],
    "target": "latch"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 最小干预（h3-hinged-safety-hatch-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：0

```json
{
  "input": {
    "module": "latch"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 全过程依赖（h3-hinged-safety-hatch-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：1
- B：-1
- C：2

```json
{
  "input": {
    "order": [
      "frame",
      "latch",
      "lid"
    ],
    "joints": [
      {
        "id": "lid-hinge",
        "name": "lid hinge",
        "type": "revolute",
        "parent": "frame",
        "child": "lid",
        "anchorParent": [
          -2,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -2,
          -0.09999999999999987,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.35
        ]
      },
      {
        "id": "latch-slide",
        "name": "latch slide",
        "type": "prismatic",
        "parent": "lid",
        "child": "latch",
        "anchorParent": [
          0,
          0.6000000000000001,
          1.45
        ],
        "anchorChild": [
          -0.3125,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 连续维修路径（h3-hinged-safety-hatch-access）

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
          6.45,
          1.7000000000000002,
          1.45
        ],
        "end": [
          0.3125,
          1.7000000000000002,
          1.45
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
          0.3125,
          6.075,
          1.45
        ],
        "end": [
          0.3125,
          1.7000000000000002,
          1.45
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
          0.3125,
          1.7000000000000002,
          6.050000000000001
        ],
        "end": [
          0.3125,
          1.7000000000000002,
          1.45
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

### 支撑反事实（h3-hinged-safety-hatch-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["latch"]
- B：["lid"]
- C：[]
- D：["frame","lid","latch"]

```json
{
  "input": {
    "removed": "lid",
    "roots": [
      "frame"
    ],
    "joints": [
      {
        "id": "lid-hinge",
        "name": "lid hinge",
        "type": "revolute",
        "parent": "frame",
        "child": "lid",
        "anchorParent": [
          -2,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -2,
          -0.09999999999999987,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.35
        ]
      },
      {
        "id": "latch-slide",
        "name": "latch slide",
        "type": "prismatic",
        "parent": "lid",
        "child": "latch",
        "anchorParent": [
          0,
          0.6000000000000001,
          1.45
        ],
        "anchorChild": [
          -0.3125,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ],
    "modules": [
      "frame",
      "lid",
      "latch"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 冲击响应读数（h3-hinged-safety-hatch-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.2003
- B：0
- C：1.0003
- D：0.0003

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0003216716739469508
      },
      {
        "time": 0.10833333333333334,
        "displacement": 5.04559916816436e-10
      },
      {
        "time": 0.20833333333333334,
        "displacement": 5.040481583263154e-10
      },
      {
        "time": 0.30833333333333335,
        "displacement": 5.039668296291153e-10
      },
      {
        "time": 0.4083333333333333,
        "displacement": 5.03997258083171e-10
      },
      {
        "time": 0.5083333333333333,
        "displacement": 5.044000272571203e-10
      },
      {
        "time": 0.6083333333333333,
        "displacement": 5.044000272571203e-10
      },
      {
        "time": 0.7083333333333334,
        "displacement": 5.044000272571203e-10
      },
      {
        "time": 0.8083333333333333,
        "displacement": 5.044000272571203e-10
      },
      {
        "time": 0.9083333333333333,
        "displacement": 5.044000272571203e-10
      },
      {
        "time": 1,
        "displacement": 5.044000272571203e-10
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 4.604627588931818e-7,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节限位推理（h3-hinged-safety-hatch-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：1.85
- B：0
- C：0.675
- D：-0.5

```json
{
  "input": {
    "joint": "lid-hinge",
    "limits": [
      0,
      1.35
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

### 约束故障诊断（h3-hinged-safety-hatch-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：latch-slide
- B：lid-hinge

```json
{
  "input": {
    "endpoints": [
      "lid",
      "latch"
    ],
    "type": "prismatic",
    "joints": [
      {
        "id": "lid-hinge",
        "name": "lid hinge",
        "type": "revolute",
        "parent": "frame",
        "child": "lid",
        "anchorParent": [
          -2,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -2,
          -0.09999999999999987,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.35
        ]
      },
      {
        "id": "latch-slide",
        "name": "latch slide",
        "type": "prismatic",
        "parent": "lid",
        "child": "latch",
        "anchorParent": [
          0,
          0.6000000000000001,
          1.45
        ],
        "anchorChild": [
          -0.3125,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.6,
          0.6
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

### 主动检查收益（h3-hinged-safety-hatch-information-gain）

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
    "module": "latch",
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

### 不确定性与弃答（h3-hinged-safety-hatch-abstention）

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

### 观测后信念更新（h3-hinged-safety-hatch-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.3333333333333333
- B：0.5
- C：0
- D：0.25

```json
{
  "input": {
    "module": "latch",
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
    "choiceId": "C"
  }
}
```

### 多目标工程权衡（h3-hinged-safety-hatch-pareto）

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
        "cost": 2,
        "stiffness": 3,
        "mass": 1.7
      },
      {
        "id": "stock-1",
        "cost": 7,
        "stiffness": 5,
        "mass": 1.2
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 4,
        "mass": 0.8
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 4,
        "mass": 1
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

### 依赖装配（h3-hinged-safety-hatch-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:lid",
        "label": "安装 lid",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:lid"
        ],
        "adds": [
          "present:lid"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lid",
          "visible": true
        }
      },
      {
        "id": "place:latch",
        "label": "安装 latch",
        "requires": [
          "present:lid"
        ],
        "forbids": [
          "present:latch"
        ],
        "adds": [
          "present:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch",
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
      }
    ],
    "goalFacts": [
      "present:frame",
      "present:lid",
      "present:latch"
    ],
    "budget": 3,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:frame",
      "place:lid",
      "place:latch"
    ]
  }
}
```

### 依赖拆解（h3-hinged-safety-hatch-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:frame",
      "present:lid",
      "present:latch"
    ],
    "initialModules": [
      "frame",
      "lid",
      "latch"
    ],
    "actions": [
      {
        "id": "remove:frame",
        "label": "拆除 frame",
        "requires": [
          "present:frame"
        ],
        "forbids": [
          "present:lid"
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
        "id": "remove:latch",
        "label": "拆除 latch",
        "requires": [
          "present:latch"
        ],
        "forbids": [],
        "adds": [
          "removed:latch"
        ],
        "deletes": [
          "present:latch"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "latch",
          "visible": false
        }
      },
      {
        "id": "remove:lid",
        "label": "拆除 lid",
        "requires": [
          "present:lid"
        ],
        "forbids": [
          "present:latch"
        ],
        "adds": [
          "removed:lid"
        ],
        "deletes": [
          "present:lid"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lid",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:latch",
      "removed:lid",
      "removed:frame"
    ],
    "budget": 3,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:latch",
      "remove:lid",
      "remove:frame"
    ]
  }
}
```

### 承载维修（h3-hinged-safety-hatch-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:latch",
      "closed:latch"
    ],
    "initialModules": [
      "frame",
      "lid",
      "latch"
    ],
    "actions": [
      {
        "id": "replace:latch",
        "label": "replace latch",
        "requires": [
          "done:remove:latch"
        ],
        "forbids": [
          "done:replace:latch"
        ],
        "adds": [
          "done:replace:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch",
          "visible": true
        }
      },
      {
        "id": "open:latch",
        "label": "open latch",
        "requires": [
          "done:support:latch"
        ],
        "forbids": [
          "done:open:latch"
        ],
        "adds": [
          "done:open:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "remove:latch",
        "label": "remove latch",
        "requires": [
          "done:open:latch"
        ],
        "forbids": [
          "done:remove:latch"
        ],
        "adds": [
          "done:remove:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch",
          "visible": false
        }
      },
      {
        "id": "support:latch",
        "label": "support latch",
        "requires": [
          "fault:latch"
        ],
        "forbids": [
          "done:support:latch"
        ],
        "adds": [
          "done:support:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "close:latch",
        "label": "close latch",
        "requires": [
          "done:verify:latch"
        ],
        "forbids": [
          "done:close:latch"
        ],
        "adds": [
          "done:close:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "release:latch",
        "label": "release latch",
        "requires": [
          "done:close:latch"
        ],
        "forbids": [
          "done:release:latch"
        ],
        "adds": [
          "done:release:latch",
          "repaired:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "verify:latch",
        "label": "verify latch",
        "requires": [
          "done:replace:latch"
        ],
        "forbids": [
          "done:verify:latch"
        ],
        "adds": [
          "done:verify:latch"
        ],
        "deletes": [
          "fault:latch"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      }
    ],
    "goalFacts": [
      "repaired:latch"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:latch",
      "open:latch",
      "remove:latch",
      "replace:latch",
      "verify:latch",
      "close:latch",
      "release:latch"
    ]
  }
}
```

### 复合编辑验证（h3-hinged-safety-hatch-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:latch",
      "closed:latch"
    ],
    "initialModules": [
      "frame",
      "lid",
      "latch"
    ],
    "actions": [
      {
        "id": "open:latch",
        "label": "open latch",
        "requires": [
          "done:support:latch"
        ],
        "forbids": [
          "done:open:latch"
        ],
        "adds": [
          "done:open:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "recolor:latch",
        "label": "recolor latch",
        "requires": [
          "done:open:latch"
        ],
        "forbids": [
          "done:recolor:latch"
        ],
        "adds": [
          "done:recolor:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch",
          "color": "#ea7635"
        }
      },
      {
        "id": "support:latch",
        "label": "support latch",
        "requires": [
          "fault:latch"
        ],
        "forbids": [
          "done:support:latch"
        ],
        "adds": [
          "done:support:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "close:latch",
        "label": "close latch",
        "requires": [
          "done:verify:latch"
        ],
        "forbids": [
          "done:close:latch"
        ],
        "adds": [
          "done:close:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "release:latch",
        "label": "release latch",
        "requires": [
          "done:close:latch"
        ],
        "forbids": [
          "done:release:latch"
        ],
        "adds": [
          "done:release:latch",
          "repaired:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "verify:latch",
        "label": "verify latch",
        "requires": [
          "done:recolor:latch"
        ],
        "forbids": [
          "done:verify:latch"
        ],
        "adds": [
          "done:verify:latch"
        ],
        "deletes": [
          "fault:latch"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      }
    ],
    "goalFacts": [
      "repaired:latch"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:latch",
      "open:latch",
      "recolor:latch",
      "verify:latch",
      "close:latch",
      "release:latch"
    ]
  }
}
```

### 跨区域联合维修（h3-hinged-safety-hatch-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:latch",
      "closed:latch"
    ],
    "initialModules": [
      "frame",
      "lid",
      "latch"
    ],
    "actions": [
      {
        "id": "replace:latch",
        "label": "replace latch",
        "requires": [
          "done:remove:latch"
        ],
        "forbids": [
          "done:replace:latch"
        ],
        "adds": [
          "done:replace:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch",
          "visible": true
        }
      },
      {
        "id": "open:latch",
        "label": "open latch",
        "requires": [
          "done:support:latch"
        ],
        "forbids": [
          "done:open:latch"
        ],
        "adds": [
          "done:open:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "remove:latch",
        "label": "remove latch",
        "requires": [
          "done:open:latch"
        ],
        "forbids": [
          "done:remove:latch"
        ],
        "adds": [
          "done:remove:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch",
          "visible": false
        }
      },
      {
        "id": "support:latch",
        "label": "support latch",
        "requires": [
          "fault:latch"
        ],
        "forbids": [
          "done:support:latch"
        ],
        "adds": [
          "done:support:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "close:latch",
        "label": "close latch",
        "requires": [
          "done:verify:latch"
        ],
        "forbids": [
          "done:close:latch"
        ],
        "adds": [
          "done:close:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "release:latch",
        "label": "release latch",
        "requires": [
          "done:close:latch"
        ],
        "forbids": [
          "done:release:latch"
        ],
        "adds": [
          "done:release:latch",
          "repaired:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "verify:latch",
        "label": "verify latch",
        "requires": [
          "done:replace:latch"
        ],
        "forbids": [
          "done:verify:latch"
        ],
        "adds": [
          "done:verify:latch"
        ],
        "deletes": [
          "fault:latch"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      }
    ],
    "goalFacts": [
      "repaired:latch"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:latch",
      "open:latch",
      "remove:latch",
      "replace:latch",
      "verify:latch",
      "close:latch",
      "release:latch"
    ]
  }
}
```

### 多工位资源调度（h3-hinged-safety-hatch-scheduling）

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
        "module": "lid",
        "duration": 1,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "latch",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      }
    ],
    "deadline": 3
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 2
    }
  }
}
```

### 检查后条件策略（h3-hinged-safety-hatch-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "latch",
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

### 局部坐标变换（h3-hinged-safety-hatch-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[1,1.7,1.45]
- B：[1.3125,2.7,3.1375]
- C：[0.3125,1.7,2.1375]
- D：[0.6875,0,0]

```json
{
  "input": {
    "localPoint": [
      0.6875,
      0,
      0
    ],
    "rotationXYZW": [
      0,
      0.7071067811865476,
      0,
      -0.7071067811865475
    ],
    "translation": [
      0.3125,
      1.7,
      1.45
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-hinged-safety-hatch-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[0,0]
- B：[2,-3]
- C：[5,2]
- D：[2,3]

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
    "choiceId": "B"
  }
}
```

### 空间相对关系（h3-hinged-safety-hatch-relative-order）

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
        0.55,
        0
      ]
    },
    "B": {
      "id": "latch",
      "position": [
        0.3125,
        1.7,
        1.45
      ]
    },
    "axis": "z"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 约束自由度（h3-hinged-safety-hatch-joint-axis）

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
      "id": "latch-slide",
      "name": "latch slide",
      "type": "prismatic",
      "parent": "lid",
      "child": "latch",
      "anchorParent": [
        0,
        0.6000000000000001,
        1.45
      ],
      "anchorChild": [
        -0.3125,
        0,
        0
      ],
      "axis": [
        1,
        0,
        0
      ],
      "limits": [
        -0.6,
        0.6
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 维修间隙预算（h3-hinged-safety-hatch-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "latch",
    "aperture": 0.6100000000000001,
    "toolWidth": 0.35,
    "eachSideMargin": 0.1
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-hinged-safety-hatch-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,-1,0]
- B：[0,0,-6]
- C：[0,0,6]
- D：[0,0,0]

```json
{
  "input": {
    "module": "latch",
    "lever": [
      1,
      3,
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
    "choiceId": "B"
  }
}
```

### 非均匀先验更新（h3-hinged-safety-hatch-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0
- B：1
- C：0.2857142857142857
- D：0.2222222222222222

```json
{
  "input": {
    "module": "latch",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      5,
      2,
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

### 风险最小决策（h3-hinged-safety-hatch-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.8,
    "repairCost": 5,
    "failureLoss": 7,
    "module": "latch"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-hinged-safety-hatch-trace-threshold）

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
        "displacement": 0.0003216716739469508
      },
      {
        "time": 0.10833333333333334,
        "displacement": 5.04559916816436e-10
      },
      {
        "time": 0.20833333333333334,
        "displacement": 5.040481583263154e-10
      },
      {
        "time": 0.30833333333333335,
        "displacement": 5.039668296291153e-10
      },
      {
        "time": 0.4083333333333333,
        "displacement": 5.03997258083171e-10
      },
      {
        "time": 0.5083333333333333,
        "displacement": 5.044000272571203e-10
      },
      {
        "time": 0.6083333333333333,
        "displacement": 5.044000272571203e-10
      },
      {
        "time": 0.7083333333333334,
        "displacement": 5.044000272571203e-10
      },
      {
        "time": 0.8083333333333333,
        "displacement": 5.044000272571203e-10
      },
      {
        "time": 0.9083333333333333,
        "displacement": 5.044000272571203e-10
      },
      {
        "time": 1,
        "displacement": 5.044000272571203e-10
      }
    ],
    "threshold": 0.00038600600873634096
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-hinged-safety-hatch-guarded-repair）

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
        "id": "release:latch",
        "label": "release latch",
        "requires": [
          "done:relock:latch"
        ],
        "forbids": [
          "done:release:latch"
        ],
        "adds": [
          "done:release:latch",
          "ready:latch",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "relock:latch",
        "label": "relock latch",
        "requires": [
          "done:verify:latch"
        ],
        "forbids": [
          "done:relock:latch"
        ],
        "adds": [
          "done:relock:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "verify:latch",
        "label": "verify latch",
        "requires": [
          "done:replace:latch"
        ],
        "forbids": [
          "done:verify:latch"
        ],
        "adds": [
          "done:verify:latch"
        ],
        "deletes": [
          "fault:latch",
          "misaligned:latch"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "replace:latch",
        "label": "replace latch",
        "requires": [
          "done:unlock:latch"
        ],
        "forbids": [
          "done:replace:latch"
        ],
        "adds": [
          "done:replace:latch"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "unlock:latch",
        "label": "unlock latch",
        "requires": [
          "done:support:latch"
        ],
        "forbids": [
          "done:unlock:latch"
        ],
        "adds": [
          "done:unlock:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "support:latch",
        "label": "support latch",
        "requires": [
          "done:isolate:latch"
        ],
        "forbids": [
          "done:support:latch"
        ],
        "adds": [
          "done:support:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "isolate:latch",
        "label": "isolate latch",
        "requires": [
          "tool:free",
          "fault:latch"
        ],
        "forbids": [
          "done:isolate:latch"
        ],
        "adds": [
          "done:isolate:latch"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:latch"
    ],
    "initialModules": [
      "frame",
      "lid",
      "latch"
    ],
    "goalFacts": [
      "ready:latch"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:latch",
      "support:latch",
      "unlock:latch",
      "replace:latch",
      "verify:latch",
      "relock:latch",
      "release:latch"
    ]
  }
}
```

### 失败状态回退（h3-hinged-safety-hatch-rollback）

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
        "id": "resume:latch",
        "label": "resume latch",
        "requires": [
          "done:verify:latch"
        ],
        "forbids": [
          "done:resume:latch"
        ],
        "adds": [
          "done:resume:latch",
          "ready:latch",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "verify:latch",
        "label": "verify latch",
        "requires": [
          "done:align:latch"
        ],
        "forbids": [
          "done:verify:latch"
        ],
        "adds": [
          "done:verify:latch"
        ],
        "deletes": [
          "fault:latch",
          "misaligned:latch"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "align:latch",
        "label": "align latch",
        "requires": [
          "done:undo:latch"
        ],
        "forbids": [
          "done:align:latch"
        ],
        "adds": [
          "done:align:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch",
          "visible": true
        }
      },
      {
        "id": "undo:latch",
        "label": "undo latch",
        "requires": [
          "done:isolate:latch"
        ],
        "forbids": [
          "done:undo:latch"
        ],
        "adds": [
          "done:undo:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch",
          "visible": false
        }
      },
      {
        "id": "isolate:latch",
        "label": "isolate latch",
        "requires": [
          "tool:free",
          "fault:latch"
        ],
        "forbids": [
          "done:isolate:latch"
        ],
        "adds": [
          "done:isolate:latch"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:latch",
      "misaligned:latch"
    ],
    "initialModules": [
      "frame",
      "lid",
      "latch"
    ],
    "goalFacts": [
      "ready:latch"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:latch",
      "undo:latch",
      "align:latch",
      "verify:latch",
      "resume:latch"
    ]
  }
}
```

### 共享工具协同维修（h3-hinged-safety-hatch-resource-repair）

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
        "id": "release:latch",
        "label": "release latch",
        "requires": [
          "done:relock:latch"
        ],
        "forbids": [
          "done:release:latch"
        ],
        "adds": [
          "done:release:latch",
          "ready:latch",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "relock:latch",
        "label": "relock latch",
        "requires": [
          "done:verify:latch"
        ],
        "forbids": [
          "done:relock:latch"
        ],
        "adds": [
          "done:relock:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "verify:latch",
        "label": "verify latch",
        "requires": [
          "done:replace:latch"
        ],
        "forbids": [
          "done:verify:latch"
        ],
        "adds": [
          "done:verify:latch"
        ],
        "deletes": [
          "fault:latch",
          "misaligned:latch"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "replace:latch",
        "label": "replace latch",
        "requires": [
          "done:unlock:latch"
        ],
        "forbids": [
          "done:replace:latch"
        ],
        "adds": [
          "done:replace:latch"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "unlock:latch",
        "label": "unlock latch",
        "requires": [
          "done:support:latch"
        ],
        "forbids": [
          "done:unlock:latch"
        ],
        "adds": [
          "done:unlock:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "support:latch",
        "label": "support latch",
        "requires": [
          "done:isolate:latch"
        ],
        "forbids": [
          "done:support:latch"
        ],
        "adds": [
          "done:support:latch"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "isolate:latch",
        "label": "isolate latch",
        "requires": [
          "tool:free",
          "fault:latch"
        ],
        "forbids": [
          "done:isolate:latch"
        ],
        "adds": [
          "done:isolate:latch"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "latch"
        }
      },
      {
        "id": "release:lid",
        "label": "release lid",
        "requires": [
          "done:relock:lid"
        ],
        "forbids": [
          "done:release:lid"
        ],
        "adds": [
          "done:release:lid",
          "ready:lid",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lid"
        }
      },
      {
        "id": "relock:lid",
        "label": "relock lid",
        "requires": [
          "done:verify:lid"
        ],
        "forbids": [
          "done:relock:lid"
        ],
        "adds": [
          "done:relock:lid"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lid"
        }
      },
      {
        "id": "verify:lid",
        "label": "verify lid",
        "requires": [
          "done:replace:lid"
        ],
        "forbids": [
          "done:verify:lid"
        ],
        "adds": [
          "done:verify:lid"
        ],
        "deletes": [
          "fault:lid",
          "misaligned:lid"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lid"
        }
      },
      {
        "id": "replace:lid",
        "label": "replace lid",
        "requires": [
          "done:unlock:lid"
        ],
        "forbids": [
          "done:replace:lid"
        ],
        "adds": [
          "done:replace:lid"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "lid"
        }
      },
      {
        "id": "unlock:lid",
        "label": "unlock lid",
        "requires": [
          "done:support:lid"
        ],
        "forbids": [
          "done:unlock:lid"
        ],
        "adds": [
          "done:unlock:lid"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lid"
        }
      },
      {
        "id": "support:lid",
        "label": "support lid",
        "requires": [
          "done:isolate:lid"
        ],
        "forbids": [
          "done:support:lid"
        ],
        "adds": [
          "done:support:lid"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lid"
        }
      },
      {
        "id": "isolate:lid",
        "label": "isolate lid",
        "requires": [
          "tool:free",
          "fault:lid"
        ],
        "forbids": [
          "done:isolate:lid"
        ],
        "adds": [
          "done:isolate:lid"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lid"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:lid",
      "fault:latch"
    ],
    "initialModules": [
      "frame",
      "lid",
      "latch"
    ],
    "goalFacts": [
      "ready:lid",
      "ready:latch"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 16
  },
  "answer": {
    "actionIds": [
      "isolate:latch",
      "support:latch",
      "unlock:latch",
      "replace:latch",
      "verify:latch",
      "relock:latch",
      "release:latch",
      "isolate:lid",
      "support:lid",
      "unlock:lid",
      "replace:lid",
      "verify:lid",
      "relock:lid",
      "release:lid"
    ]
  }
}
```

### 预算约束检查策略（h3-hinged-safety-hatch-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "latch",
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
