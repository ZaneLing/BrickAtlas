## D1 阀门控制台

### 模块识别（h3-valve-control-stand-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：valve-wheel
- B：indicator
- C：pipe-base

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "pipe-base",
        "name": "Pipe and pedestal"
      },
      {
        "id": "valve-wheel",
        "name": "Rotary valve wheel"
      },
      {
        "id": "indicator",
        "name": "Position indicator"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 部件计数（h3-valve-control-stand-count）

模块 indicator 有多少个可视零件？

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
        "moduleId": "pipe-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0002",
        "moduleId": "pipe-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0003",
        "moduleId": "pipe-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0004",
        "moduleId": "pipe-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0005",
        "moduleId": "pipe-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0006",
        "moduleId": "pipe-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0007",
        "moduleId": "pipe-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0008",
        "moduleId": "pipe-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0009",
        "moduleId": "pipe-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0010",
        "moduleId": "pipe-base",
        "shape": "cylinder",
        "color": "#2878b8"
      },
      {
        "id": "h0011",
        "moduleId": "pipe-base",
        "shape": "cylinder",
        "color": "#2878b8"
      },
      {
        "id": "h0012",
        "moduleId": "pipe-base",
        "shape": "cylinder",
        "color": "#2878b8"
      },
      {
        "id": "h0013",
        "moduleId": "pipe-base",
        "shape": "cylinder",
        "color": "#2878b8"
      },
      {
        "id": "h0014",
        "moduleId": "pipe-base",
        "shape": "cylinder",
        "color": "#2878b8"
      },
      {
        "id": "h0015",
        "moduleId": "valve-wheel",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0016",
        "moduleId": "valve-wheel",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0017",
        "moduleId": "valve-wheel",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0018",
        "moduleId": "valve-wheel",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0019",
        "moduleId": "valve-wheel",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0020",
        "moduleId": "valve-wheel",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0021",
        "moduleId": "valve-wheel",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0022",
        "moduleId": "valve-wheel",
        "shape": "beam",
        "color": "#d43a32"
      },
      {
        "id": "h0023",
        "moduleId": "valve-wheel",
        "shape": "axle",
        "color": "#c6cdd2"
      },
      {
        "id": "h0024",
        "moduleId": "indicator",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "h0025",
        "moduleId": "indicator",
        "shape": "beam",
        "color": "#e8792e"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-valve-control-stand-color）

零件 h0024 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#2878b8
- B：#d43a32
- C：#f2bf3c
- D：#edf1f2

```json
{
  "input": {
    "part": {
      "id": "h0024",
      "moduleId": "indicator",
      "shape": "panel",
      "size": [
        1.4,
        0.2,
        0.7
      ],
      "position": [
        0,
        0.5499999999999998,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#edf1f2"
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 三维位置（h3-valve-control-stand-position）

模块 indicator 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,4.3,0]
- B：[999,999,999]
- C：[0,5.25,0]
- D：[0,1.9674999999999998,0]

```json
{
  "input": {
    "centers": {
      "pipe-base": [
        0,
        1.9674999999999998,
        0
      ],
      "valve-wheel": [
        0,
        4.3,
        0
      ],
      "indicator": [
        0,
        5.25,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节类型（h3-valve-control-stand-joint-type）

wheel-shaft 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：revolute
- B：fixed
- C：prismatic
- D：spring

```json
{
  "input": {
    "joint": {
      "id": "wheel-shaft",
      "name": "wheel shaft",
      "type": "revolute",
      "parent": "pipe-base",
      "child": "valve-wheel",
      "anchorParent": [
        0,
        2.3325,
        0
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
        -3.141592653589793,
        3.141592653589793
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 直接连接（h3-valve-control-stand-parent）

indicator 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：[]
- B：["pipe-base","valve-wheel","indicator"]
- C：["valve-wheel"]
- D：["indicator"]

```json
{
  "input": {
    "joints": [
      {
        "id": "wheel-shaft",
        "name": "wheel shaft",
        "type": "revolute",
        "parent": "pipe-base",
        "child": "valve-wheel",
        "anchorParent": [
          0,
          2.3325,
          0
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
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "indicator-coupler",
        "name": "indicator coupler",
        "type": "fixed",
        "parent": "valve-wheel",
        "child": "indicator",
        "anchorParent": [
          0,
          0.7999999999999998,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000036,
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

### 基座识别（h3-valve-control-stand-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：[]
- B：["pipe-base","valve-wheel","indicator"]
- C：["indicator"]
- D：["pipe-base"]

```json
{
  "input": {
    "modules": [
      {
        "id": "pipe-base",
        "name": "Pipe and pedestal",
        "role": "foundation",
        "anchored": true,
        "mass": 8,
        "position": [
          0,
          1.9674999999999998,
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
        "id": "valve-wheel",
        "name": "Rotary valve wheel",
        "role": "actuator",
        "anchored": false,
        "mass": 1,
        "position": [
          0,
          4.3,
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
        "id": "indicator",
        "name": "Position indicator",
        "role": "service-module",
        "anchored": false,
        "mass": 0.4,
        "position": [
          0,
          5.25,
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
    "choiceId": "D"
  }
}
```

### 接口计数（h3-valve-control-stand-degree）

indicator 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：2
- B：0
- C：3
- D：1

```json
{
  "input": {
    "joints": [
      {
        "id": "wheel-shaft",
        "name": "wheel shaft",
        "type": "revolute",
        "parent": "pipe-base",
        "child": "valve-wheel",
        "anchorParent": [
          0,
          2.3325,
          0
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
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "indicator-coupler",
        "name": "indicator coupler",
        "type": "fixed",
        "parent": "valve-wheel",
        "child": "indicator",
        "anchorParent": [
          0,
          0.7999999999999998,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000036,
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

### 局部改色（h3-valve-control-stand-recolor）

仅将 h0024 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"*","color":"#e8792e"}
- B：{"id":"h0024","color":"#e8792e"}
- C：{"id":"h0025","color":"#e8792e"}
- D：{"id":"h0024","color":"#2878b8"}

```json
{
  "input": {
    "part": {
      "id": "h0024",
      "moduleId": "indicator",
      "shape": "panel",
      "size": [
        1.4,
        0.2,
        0.7
      ],
      "position": [
        0,
        0.5499999999999998,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#edf1f2"
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 补装部件（h3-valve-control-stand-add）

模块 indicator 缺失零件 h0024。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"h0024","moduleId":"indicator","shape":"panel","size":[1.4,0.2,0.7],"position":[0,0.5499999999999998,0],"rotation":[0,0,0,1],"color":"#edf1f2"}
- B：{"id":"h0024","moduleId":"pipe-base","shape":"panel","size":[1.4,0.2,0.7],"position":[0,0.5499999999999998,0],"rotation":[0,0,0,1],"color":"#edf1f2"}
- C：{"id":"h0024","moduleId":"indicator","shape":"panel","size":[3,3,3],"position":[0,0.5499999999999998,0],"rotation":[0,0,0,1],"color":"#edf1f2"}
- D：{"id":"h0024","moduleId":"indicator","shape":"panel","size":[1.4,0.2,0.7],"position":[0,0.5499999999999998,0],"rotation":[0,0,0,1],"color":"#000000"}

```json
{
  "input": {
    "targetPart": {
      "id": "h0024",
      "moduleId": "indicator",
      "shape": "panel",
      "size": [
        1.4,
        0.2,
        0.7
      ],
      "position": [
        0,
        0.5499999999999998,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#edf1f2"
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
      "h0025"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全拆除（h3-valve-control-stand-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["pipe-base","valve-wheel","indicator"]
- B：["indicator"]
- C：["pipe-base"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "wheel-shaft",
        "name": "wheel shaft",
        "type": "revolute",
        "parent": "pipe-base",
        "child": "valve-wheel",
        "anchorParent": [
          0,
          2.3325,
          0
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
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "indicator-coupler",
        "name": "indicator coupler",
        "type": "fixed",
        "parent": "valve-wheel",
        "child": "indicator",
        "anchorParent": [
          0,
          0.7999999999999998,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000036,
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
      "pipe-base",
      "valve-wheel",
      "indicator"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 替换选择（h3-valve-control-stand-replace）

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
        "mass": 1.7
      },
      {
        "id": "stock-1",
        "cost": 3,
        "stiffness": 4,
        "mass": 1.1
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 3,
        "mass": 1.1
      },
      {
        "id": "stock-3",
        "cost": 5,
        "stiffness": 10,
        "mass": 1.1
      }
    ],
    "maxCost": 6
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-valve-control-stand-translate）

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
    "target": "indicator"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-valve-control-stand-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：0
- B：90
- C：-180
- D：180

```json
{
  "input": {
    "module": "indicator",
    "currentYaw": 270,
    "targetYaw": 90
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 下一步放置（h3-valve-control-stand-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["indicator"]
- B：[]
- C：["pipe-base","valve-wheel"]
- D：["pipe-base"]

```json
{
  "input": {
    "prefix": [
      "pipe-base",
      "valve-wheel"
    ],
    "joints": [
      {
        "id": "wheel-shaft",
        "name": "wheel shaft",
        "type": "revolute",
        "parent": "pipe-base",
        "child": "valve-wheel",
        "anchorParent": [
          0,
          2.3325,
          0
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
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "indicator-coupler",
        "name": "indicator coupler",
        "type": "fixed",
        "parent": "valve-wheel",
        "child": "indicator",
        "anchorParent": [
          0,
          0.7999999999999998,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000036,
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
      "pipe-base",
      "valve-wheel",
      "indicator"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 库存核算（h3-valve-control-stand-inventory）

备件库有 8 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：7
- B：5
- C：9
- D：6

```json
{
  "input": {
    "available": 8,
    "required": 2
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 子装配边界（h3-valve-control-stand-boundary）

隔离 indicator 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["wheel-shaft"]
- B：["indicator-coupler"]
- C：[]
- D：["wheel-shaft","indicator-coupler"]

```json
{
  "input": {
    "joints": [
      {
        "id": "wheel-shaft",
        "name": "wheel shaft",
        "type": "revolute",
        "parent": "pipe-base",
        "child": "valve-wheel",
        "anchorParent": [
          0,
          2.3325,
          0
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
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "indicator-coupler",
        "name": "indicator coupler",
        "type": "fixed",
        "parent": "valve-wheel",
        "child": "indicator",
        "anchorParent": [
          0,
          0.7999999999999998,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000036,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "target": "indicator"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 最小干预（h3-valve-control-stand-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：2
- B：0
- C：1

```json
{
  "input": {
    "module": "indicator"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 全过程依赖（h3-valve-control-stand-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：2
- B：0
- C：-1
- D：1

```json
{
  "input": {
    "order": [
      "valve-wheel",
      "pipe-base",
      "indicator"
    ],
    "joints": [
      {
        "id": "wheel-shaft",
        "name": "wheel shaft",
        "type": "revolute",
        "parent": "pipe-base",
        "child": "valve-wheel",
        "anchorParent": [
          0,
          2.3325,
          0
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
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "indicator-coupler",
        "name": "indicator coupler",
        "type": "fixed",
        "parent": "valve-wheel",
        "child": "indicator",
        "anchorParent": [
          0,
          0.7999999999999998,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000036,
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

### 连续维修路径（h3-valve-control-stand-access）

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
          5.825,
          5.25,
          0
        ],
        "end": [
          0,
          5.25,
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
          9.899999999999999,
          0
        ],
        "end": [
          0,
          5.25,
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
          5.25,
          5.825
        ],
        "end": [
          0,
          5.25,
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

### 支撑反事实（h3-valve-control-stand-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["pipe-base","valve-wheel","indicator"]
- C：["indicator"]
- D：["valve-wheel"]

```json
{
  "input": {
    "removed": "valve-wheel",
    "roots": [
      "pipe-base"
    ],
    "joints": [
      {
        "id": "wheel-shaft",
        "name": "wheel shaft",
        "type": "revolute",
        "parent": "pipe-base",
        "child": "valve-wheel",
        "anchorParent": [
          0,
          2.3325,
          0
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
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "indicator-coupler",
        "name": "indicator coupler",
        "type": "fixed",
        "parent": "valve-wheel",
        "child": "indicator",
        "anchorParent": [
          0,
          0.7999999999999998,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000036,
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
      "pipe-base",
      "valve-wheel",
      "indicator"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-valve-control-stand-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：1
- B：0
- C：0.2

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 7.494457715654684e-14
      },
      {
        "time": 0.10833333333333334,
        "displacement": 1.7763568394002505e-15
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
    "nominalDrift": 1.9073486345888568e-7,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节限位推理（h3-valve-control-stand-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-3.641592653589793
- B：3.641592653589793
- C：-3.141592653589793
- D：0

```json
{
  "input": {
    "joint": "wheel-shaft",
    "limits": [
      -3.141592653589793,
      3.141592653589793
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

### 约束故障诊断（h3-valve-control-stand-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：indicator-coupler
- B：wheel-shaft

```json
{
  "input": {
    "endpoints": [
      "valve-wheel",
      "indicator"
    ],
    "type": "fixed",
    "joints": [
      {
        "id": "wheel-shaft",
        "name": "wheel shaft",
        "type": "revolute",
        "parent": "pipe-base",
        "child": "valve-wheel",
        "anchorParent": [
          0,
          2.3325,
          0
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
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "indicator-coupler",
        "name": "indicator coupler",
        "type": "fixed",
        "parent": "valve-wheel",
        "child": "indicator",
        "anchorParent": [
          0,
          0.7999999999999998,
          0
        ],
        "anchorChild": [
          0,
          -0.15000000000000036,
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

### 主动检查收益（h3-valve-control-stand-information-gain）

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
    "module": "indicator",
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

### 不确定性与弃答（h3-valve-control-stand-abstention）

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

### 观测后信念更新（h3-valve-control-stand-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0.3333333333333333
- C：0
- D：0.25

```json
{
  "input": {
    "module": "indicator",
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
    "choiceId": "B"
  }
}
```

### 多目标工程权衡（h3-valve-control-stand-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

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
        "cost": 3,
        "stiffness": 11,
        "mass": 1.7
      },
      {
        "id": "stock-1",
        "cost": 3,
        "stiffness": 4,
        "mass": 1.1
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 3,
        "mass": 1.1
      },
      {
        "id": "stock-3",
        "cost": 5,
        "stiffness": 10,
        "mass": 1.1
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

### 依赖装配（h3-valve-control-stand-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:indicator",
        "label": "安装 indicator",
        "requires": [
          "present:valve-wheel"
        ],
        "forbids": [
          "present:indicator"
        ],
        "adds": [
          "present:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator",
          "visible": true
        }
      },
      {
        "id": "place:pipe-base",
        "label": "安装 pipe-base",
        "requires": [],
        "forbids": [
          "present:pipe-base"
        ],
        "adds": [
          "present:pipe-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pipe-base",
          "visible": true
        }
      },
      {
        "id": "place:valve-wheel",
        "label": "安装 valve-wheel",
        "requires": [
          "present:pipe-base"
        ],
        "forbids": [
          "present:valve-wheel"
        ],
        "adds": [
          "present:valve-wheel"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "valve-wheel",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:pipe-base",
      "present:valve-wheel",
      "present:indicator"
    ],
    "budget": 3,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:pipe-base",
      "place:valve-wheel",
      "place:indicator"
    ]
  }
}
```

### 依赖拆解（h3-valve-control-stand-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:pipe-base",
      "present:valve-wheel",
      "present:indicator"
    ],
    "initialModules": [
      "pipe-base",
      "valve-wheel",
      "indicator"
    ],
    "actions": [
      {
        "id": "remove:indicator",
        "label": "拆除 indicator",
        "requires": [
          "present:indicator"
        ],
        "forbids": [],
        "adds": [
          "removed:indicator"
        ],
        "deletes": [
          "present:indicator"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "indicator",
          "visible": false
        }
      },
      {
        "id": "remove:pipe-base",
        "label": "拆除 pipe-base",
        "requires": [
          "present:pipe-base"
        ],
        "forbids": [
          "present:valve-wheel"
        ],
        "adds": [
          "removed:pipe-base"
        ],
        "deletes": [
          "present:pipe-base"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "pipe-base",
          "visible": false
        }
      },
      {
        "id": "remove:valve-wheel",
        "label": "拆除 valve-wheel",
        "requires": [
          "present:valve-wheel"
        ],
        "forbids": [
          "present:indicator"
        ],
        "adds": [
          "removed:valve-wheel"
        ],
        "deletes": [
          "present:valve-wheel"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "valve-wheel",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:indicator",
      "removed:valve-wheel",
      "removed:pipe-base"
    ],
    "budget": 3,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:indicator",
      "remove:valve-wheel",
      "remove:pipe-base"
    ]
  }
}
```

### 承载维修（h3-valve-control-stand-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:indicator",
      "closed:indicator"
    ],
    "initialModules": [
      "pipe-base",
      "valve-wheel",
      "indicator"
    ],
    "actions": [
      {
        "id": "remove:indicator",
        "label": "remove indicator",
        "requires": [
          "done:open:indicator"
        ],
        "forbids": [
          "done:remove:indicator"
        ],
        "adds": [
          "done:remove:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator",
          "visible": false
        }
      },
      {
        "id": "verify:indicator",
        "label": "verify indicator",
        "requires": [
          "done:replace:indicator"
        ],
        "forbids": [
          "done:verify:indicator"
        ],
        "adds": [
          "done:verify:indicator"
        ],
        "deletes": [
          "fault:indicator"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "support:indicator",
        "label": "support indicator",
        "requires": [
          "fault:indicator"
        ],
        "forbids": [
          "done:support:indicator"
        ],
        "adds": [
          "done:support:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "open:indicator",
        "label": "open indicator",
        "requires": [
          "done:support:indicator"
        ],
        "forbids": [
          "done:open:indicator"
        ],
        "adds": [
          "done:open:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "release:indicator",
        "label": "release indicator",
        "requires": [
          "done:close:indicator"
        ],
        "forbids": [
          "done:release:indicator"
        ],
        "adds": [
          "done:release:indicator",
          "repaired:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "replace:indicator",
        "label": "replace indicator",
        "requires": [
          "done:remove:indicator"
        ],
        "forbids": [
          "done:replace:indicator"
        ],
        "adds": [
          "done:replace:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator",
          "visible": true
        }
      },
      {
        "id": "close:indicator",
        "label": "close indicator",
        "requires": [
          "done:verify:indicator"
        ],
        "forbids": [
          "done:close:indicator"
        ],
        "adds": [
          "done:close:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      }
    ],
    "goalFacts": [
      "repaired:indicator"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:indicator",
      "open:indicator",
      "remove:indicator",
      "replace:indicator",
      "verify:indicator",
      "close:indicator",
      "release:indicator"
    ]
  }
}
```

### 复合编辑验证（h3-valve-control-stand-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:indicator",
      "closed:indicator"
    ],
    "initialModules": [
      "pipe-base",
      "valve-wheel",
      "indicator"
    ],
    "actions": [
      {
        "id": "verify:indicator",
        "label": "verify indicator",
        "requires": [
          "done:recolor:indicator"
        ],
        "forbids": [
          "done:verify:indicator"
        ],
        "adds": [
          "done:verify:indicator"
        ],
        "deletes": [
          "fault:indicator"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "support:indicator",
        "label": "support indicator",
        "requires": [
          "fault:indicator"
        ],
        "forbids": [
          "done:support:indicator"
        ],
        "adds": [
          "done:support:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "open:indicator",
        "label": "open indicator",
        "requires": [
          "done:support:indicator"
        ],
        "forbids": [
          "done:open:indicator"
        ],
        "adds": [
          "done:open:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "release:indicator",
        "label": "release indicator",
        "requires": [
          "done:close:indicator"
        ],
        "forbids": [
          "done:release:indicator"
        ],
        "adds": [
          "done:release:indicator",
          "repaired:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "close:indicator",
        "label": "close indicator",
        "requires": [
          "done:verify:indicator"
        ],
        "forbids": [
          "done:close:indicator"
        ],
        "adds": [
          "done:close:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "recolor:indicator",
        "label": "recolor indicator",
        "requires": [
          "done:open:indicator"
        ],
        "forbids": [
          "done:recolor:indicator"
        ],
        "adds": [
          "done:recolor:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator",
          "color": "#ea7635"
        }
      }
    ],
    "goalFacts": [
      "repaired:indicator"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:indicator",
      "open:indicator",
      "recolor:indicator",
      "verify:indicator",
      "close:indicator",
      "release:indicator"
    ]
  }
}
```

### 跨区域联合维修（h3-valve-control-stand-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:indicator",
      "closed:indicator"
    ],
    "initialModules": [
      "pipe-base",
      "valve-wheel",
      "indicator"
    ],
    "actions": [
      {
        "id": "remove:indicator",
        "label": "remove indicator",
        "requires": [
          "done:open:indicator"
        ],
        "forbids": [
          "done:remove:indicator"
        ],
        "adds": [
          "done:remove:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator",
          "visible": false
        }
      },
      {
        "id": "verify:indicator",
        "label": "verify indicator",
        "requires": [
          "done:replace:indicator"
        ],
        "forbids": [
          "done:verify:indicator"
        ],
        "adds": [
          "done:verify:indicator"
        ],
        "deletes": [
          "fault:indicator"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "support:indicator",
        "label": "support indicator",
        "requires": [
          "fault:indicator"
        ],
        "forbids": [
          "done:support:indicator"
        ],
        "adds": [
          "done:support:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "open:indicator",
        "label": "open indicator",
        "requires": [
          "done:support:indicator"
        ],
        "forbids": [
          "done:open:indicator"
        ],
        "adds": [
          "done:open:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "release:indicator",
        "label": "release indicator",
        "requires": [
          "done:close:indicator"
        ],
        "forbids": [
          "done:release:indicator"
        ],
        "adds": [
          "done:release:indicator",
          "repaired:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "replace:indicator",
        "label": "replace indicator",
        "requires": [
          "done:remove:indicator"
        ],
        "forbids": [
          "done:replace:indicator"
        ],
        "adds": [
          "done:replace:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator",
          "visible": true
        }
      },
      {
        "id": "close:indicator",
        "label": "close indicator",
        "requires": [
          "done:verify:indicator"
        ],
        "forbids": [
          "done:close:indicator"
        ],
        "adds": [
          "done:close:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      }
    ],
    "goalFacts": [
      "repaired:indicator"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:indicator",
      "open:indicator",
      "remove:indicator",
      "replace:indicator",
      "verify:indicator",
      "close:indicator",
      "release:indicator"
    ]
  }
}
```

### 多工位资源调度（h3-valve-control-stand-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "pipe-base",
        "duration": 2,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "valve-wheel",
        "duration": 1,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "indicator",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      }
    ],
    "deadline": 4
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

### 检查后条件策略（h3-valve-control-stand-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "indicator",
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

### 局部坐标变换（h3-valve-control-stand-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[1,0.55,0]
- B：[1,5.8,0]
- C：[0,6.8,1]
- D：[-1,5.8,0]

```json
{
  "input": {
    "localPoint": [
      1,
      0.5499999999999998,
      0
    ],
    "rotationXYZW": [
      0,
      1,
      0,
      6.123233995736766e-17
    ],
    "translation": [
      0,
      5.25,
      0
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 正交视图投影（h3-valve-control-stand-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[2,3]
- B：[0,0]
- C：[2,5]
- D：[5,2]

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
    "choiceId": "C"
  }
}
```

### 空间相对关系（h3-valve-control-stand-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：equal
- B：greater
- C：less

```json
{
  "input": {
    "A": {
      "id": "pipe-base",
      "position": [
        0,
        1.9674999999999998,
        0
      ]
    },
    "B": {
      "id": "indicator",
      "position": [
        0,
        5.25,
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

### 约束自由度（h3-valve-control-stand-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：3
- B：6
- C：1
- D：0

```json
{
  "input": {
    "joint": {
      "id": "wheel-shaft",
      "name": "wheel shaft",
      "type": "revolute",
      "parent": "pipe-base",
      "child": "valve-wheel",
      "anchorParent": [
        0,
        2.3325,
        0
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
        -3.141592653589793,
        3.141592653589793
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 维修间隙预算（h3-valve-control-stand-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "indicator",
    "aperture": 0.3,
    "toolWidth": 0.35,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-valve-control-stand-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,-1,0]
- B：[0,0,-3]
- C：[0,0,3]
- D：[0,0,0]

```json
{
  "input": {
    "module": "indicator",
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

### 非均匀先验更新（h3-valve-control-stand-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0
- B：1
- C：0.5
- D：0.3333333333333333

```json
{
  "input": {
    "module": "indicator",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      2,
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

### 风险最小决策（h3-valve-control-stand-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.7,
    "repairCost": 1,
    "failureLoss": 7,
    "module": "indicator"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-valve-control-stand-trace-threshold）

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
        "displacement": 7.494457715654684e-14
      },
      {
        "time": 0.10833333333333334,
        "displacement": 1.7763568394002505e-15
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
    "threshold": 5.995566172523748e-14
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-valve-control-stand-guarded-repair）

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
        "id": "release:indicator",
        "label": "release indicator",
        "requires": [
          "done:relock:indicator"
        ],
        "forbids": [
          "done:release:indicator"
        ],
        "adds": [
          "done:release:indicator",
          "ready:indicator",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "relock:indicator",
        "label": "relock indicator",
        "requires": [
          "done:verify:indicator"
        ],
        "forbids": [
          "done:relock:indicator"
        ],
        "adds": [
          "done:relock:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "verify:indicator",
        "label": "verify indicator",
        "requires": [
          "done:replace:indicator"
        ],
        "forbids": [
          "done:verify:indicator"
        ],
        "adds": [
          "done:verify:indicator"
        ],
        "deletes": [
          "fault:indicator",
          "misaligned:indicator"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "replace:indicator",
        "label": "replace indicator",
        "requires": [
          "done:unlock:indicator"
        ],
        "forbids": [
          "done:replace:indicator"
        ],
        "adds": [
          "done:replace:indicator"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "unlock:indicator",
        "label": "unlock indicator",
        "requires": [
          "done:support:indicator"
        ],
        "forbids": [
          "done:unlock:indicator"
        ],
        "adds": [
          "done:unlock:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "support:indicator",
        "label": "support indicator",
        "requires": [
          "done:isolate:indicator"
        ],
        "forbids": [
          "done:support:indicator"
        ],
        "adds": [
          "done:support:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "isolate:indicator",
        "label": "isolate indicator",
        "requires": [
          "tool:free",
          "fault:indicator"
        ],
        "forbids": [
          "done:isolate:indicator"
        ],
        "adds": [
          "done:isolate:indicator"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:indicator"
    ],
    "initialModules": [
      "pipe-base",
      "valve-wheel",
      "indicator"
    ],
    "goalFacts": [
      "ready:indicator"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:indicator",
      "support:indicator",
      "unlock:indicator",
      "replace:indicator",
      "verify:indicator",
      "relock:indicator",
      "release:indicator"
    ]
  }
}
```

### 失败状态回退（h3-valve-control-stand-rollback）

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
        "id": "resume:indicator",
        "label": "resume indicator",
        "requires": [
          "done:verify:indicator"
        ],
        "forbids": [
          "done:resume:indicator"
        ],
        "adds": [
          "done:resume:indicator",
          "ready:indicator",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "verify:indicator",
        "label": "verify indicator",
        "requires": [
          "done:align:indicator"
        ],
        "forbids": [
          "done:verify:indicator"
        ],
        "adds": [
          "done:verify:indicator"
        ],
        "deletes": [
          "fault:indicator",
          "misaligned:indicator"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "align:indicator",
        "label": "align indicator",
        "requires": [
          "done:undo:indicator"
        ],
        "forbids": [
          "done:align:indicator"
        ],
        "adds": [
          "done:align:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator",
          "visible": true
        }
      },
      {
        "id": "undo:indicator",
        "label": "undo indicator",
        "requires": [
          "done:isolate:indicator"
        ],
        "forbids": [
          "done:undo:indicator"
        ],
        "adds": [
          "done:undo:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator",
          "visible": false
        }
      },
      {
        "id": "isolate:indicator",
        "label": "isolate indicator",
        "requires": [
          "tool:free",
          "fault:indicator"
        ],
        "forbids": [
          "done:isolate:indicator"
        ],
        "adds": [
          "done:isolate:indicator"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:indicator",
      "misaligned:indicator"
    ],
    "initialModules": [
      "pipe-base",
      "valve-wheel",
      "indicator"
    ],
    "goalFacts": [
      "ready:indicator"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:indicator",
      "undo:indicator",
      "align:indicator",
      "verify:indicator",
      "resume:indicator"
    ]
  }
}
```

### 共享工具协同维修（h3-valve-control-stand-resource-repair）

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
        "id": "release:indicator",
        "label": "release indicator",
        "requires": [
          "done:relock:indicator"
        ],
        "forbids": [
          "done:release:indicator"
        ],
        "adds": [
          "done:release:indicator",
          "ready:indicator",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "relock:indicator",
        "label": "relock indicator",
        "requires": [
          "done:verify:indicator"
        ],
        "forbids": [
          "done:relock:indicator"
        ],
        "adds": [
          "done:relock:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "verify:indicator",
        "label": "verify indicator",
        "requires": [
          "done:replace:indicator"
        ],
        "forbids": [
          "done:verify:indicator"
        ],
        "adds": [
          "done:verify:indicator"
        ],
        "deletes": [
          "fault:indicator",
          "misaligned:indicator"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "replace:indicator",
        "label": "replace indicator",
        "requires": [
          "done:unlock:indicator"
        ],
        "forbids": [
          "done:replace:indicator"
        ],
        "adds": [
          "done:replace:indicator"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "unlock:indicator",
        "label": "unlock indicator",
        "requires": [
          "done:support:indicator"
        ],
        "forbids": [
          "done:unlock:indicator"
        ],
        "adds": [
          "done:unlock:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "support:indicator",
        "label": "support indicator",
        "requires": [
          "done:isolate:indicator"
        ],
        "forbids": [
          "done:support:indicator"
        ],
        "adds": [
          "done:support:indicator"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "isolate:indicator",
        "label": "isolate indicator",
        "requires": [
          "tool:free",
          "fault:indicator"
        ],
        "forbids": [
          "done:isolate:indicator"
        ],
        "adds": [
          "done:isolate:indicator"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "indicator"
        }
      },
      {
        "id": "release:valve-wheel",
        "label": "release valve-wheel",
        "requires": [
          "done:relock:valve-wheel"
        ],
        "forbids": [
          "done:release:valve-wheel"
        ],
        "adds": [
          "done:release:valve-wheel",
          "ready:valve-wheel",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "valve-wheel"
        }
      },
      {
        "id": "relock:valve-wheel",
        "label": "relock valve-wheel",
        "requires": [
          "done:verify:valve-wheel"
        ],
        "forbids": [
          "done:relock:valve-wheel"
        ],
        "adds": [
          "done:relock:valve-wheel"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "valve-wheel"
        }
      },
      {
        "id": "verify:valve-wheel",
        "label": "verify valve-wheel",
        "requires": [
          "done:replace:valve-wheel"
        ],
        "forbids": [
          "done:verify:valve-wheel"
        ],
        "adds": [
          "done:verify:valve-wheel"
        ],
        "deletes": [
          "fault:valve-wheel",
          "misaligned:valve-wheel"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "valve-wheel"
        }
      },
      {
        "id": "replace:valve-wheel",
        "label": "replace valve-wheel",
        "requires": [
          "done:unlock:valve-wheel"
        ],
        "forbids": [
          "done:replace:valve-wheel"
        ],
        "adds": [
          "done:replace:valve-wheel"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "valve-wheel"
        }
      },
      {
        "id": "unlock:valve-wheel",
        "label": "unlock valve-wheel",
        "requires": [
          "done:support:valve-wheel"
        ],
        "forbids": [
          "done:unlock:valve-wheel"
        ],
        "adds": [
          "done:unlock:valve-wheel"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "valve-wheel"
        }
      },
      {
        "id": "support:valve-wheel",
        "label": "support valve-wheel",
        "requires": [
          "done:isolate:valve-wheel"
        ],
        "forbids": [
          "done:support:valve-wheel"
        ],
        "adds": [
          "done:support:valve-wheel"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "valve-wheel"
        }
      },
      {
        "id": "isolate:valve-wheel",
        "label": "isolate valve-wheel",
        "requires": [
          "tool:free",
          "fault:valve-wheel"
        ],
        "forbids": [
          "done:isolate:valve-wheel"
        ],
        "adds": [
          "done:isolate:valve-wheel"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "valve-wheel"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:valve-wheel",
      "fault:indicator"
    ],
    "initialModules": [
      "pipe-base",
      "valve-wheel",
      "indicator"
    ],
    "goalFacts": [
      "ready:valve-wheel",
      "ready:indicator"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 16
  },
  "answer": {
    "actionIds": [
      "isolate:indicator",
      "support:indicator",
      "unlock:indicator",
      "replace:indicator",
      "verify:indicator",
      "relock:indicator",
      "release:indicator",
      "isolate:valve-wheel",
      "support:valve-wheel",
      "unlock:valve-wheel",
      "replace:valve-wheel",
      "verify:valve-wheel",
      "relock:valve-wheel",
      "release:valve-wheel"
    ]
  }
}
```

### 预算约束检查策略（h3-valve-control-stand-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "indicator",
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
