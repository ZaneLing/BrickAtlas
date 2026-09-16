## D2 运河巡检艇

### 模块识别（h3-canal-inspection-skiff-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：propeller
- B：hull
- C：cabin
- D：rudder

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "hull",
        "name": "Catamaran inspection hull"
      },
      {
        "id": "cabin",
        "name": "Inspection cabin"
      },
      {
        "id": "rudder",
        "name": "Steering rudder"
      },
      {
        "id": "propeller",
        "name": "Inspection propeller"
      },
      {
        "id": "sensor-mast",
        "name": "Survey mast"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 部件计数（h3-canal-inspection-skiff-count）

模块 propeller 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：7
- B：5
- C：9
- D：6

```json
{
  "input": {
    "parts": [
      {
        "id": "h0001",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0002",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0003",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0004",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0005",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0006",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0007",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0008",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0009",
        "moduleId": "hull",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0010",
        "moduleId": "hull",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0011",
        "moduleId": "hull",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0012",
        "moduleId": "hull",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0013",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0014",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0015",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0016",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0017",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0018",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0019",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0020",
        "moduleId": "hull",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "h0021",
        "moduleId": "hull",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0022",
        "moduleId": "hull",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0023",
        "moduleId": "hull",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0024",
        "moduleId": "hull",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0025",
        "moduleId": "cabin",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0026",
        "moduleId": "cabin",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0027",
        "moduleId": "cabin",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0028",
        "moduleId": "cabin",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0029",
        "moduleId": "cabin",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0030",
        "moduleId": "cabin",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0031",
        "moduleId": "cabin",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "h0032",
        "moduleId": "cabin",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "h0033",
        "moduleId": "cabin",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "h0034",
        "moduleId": "rudder",
        "shape": "panel",
        "color": "#e8792e"
      },
      {
        "id": "h0035",
        "moduleId": "propeller",
        "shape": "axle",
        "color": "#c6cdd2"
      },
      {
        "id": "h0036",
        "moduleId": "propeller",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0037",
        "moduleId": "propeller",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0038",
        "moduleId": "propeller",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0039",
        "moduleId": "propeller",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0040",
        "moduleId": "propeller",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0041",
        "moduleId": "sensor-mast",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "h0042",
        "moduleId": "sensor-mast",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "h0043",
        "moduleId": "sensor-mast",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "h0044",
        "moduleId": "sensor-mast",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "h0045",
        "moduleId": "sensor-mast",
        "shape": "sphere",
        "color": "#79c7d8"
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 颜色识别（h3-canal-inspection-skiff-color）

零件 h0035 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#d43a32
- B：#f2bf3c
- C：#c6cdd2
- D：#2878b8

```json
{
  "input": {
    "part": {
      "id": "h0035",
      "moduleId": "propeller",
      "shape": "axle",
      "size": [
        0.25,
        1.2,
        0.25
      ],
      "position": [
        -0.7089691907681028,
        0,
        0
      ],
      "rotation": [
        0,
        0,
        0.7071067811865475,
        0.7071067811865476
      ],
      "color": "#c6cdd2"
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 三维位置（h3-canal-inspection-skiff-position）

模块 propeller 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[5.5,0.19999999999999996,0]
- B：[4.008969190768103,0.5,0]
- C：[0,0.7124999999999999,0]
- D：[0,1.7875,0]

```json
{
  "input": {
    "centers": {
      "hull": [
        0,
        0.7124999999999999,
        0
      ],
      "cabin": [
        0,
        1.7875,
        0
      ],
      "rudder": [
        5.5,
        0.19999999999999996,
        0
      ],
      "propeller": [
        4.008969190768103,
        0.5,
        0
      ],
      "sensor-mast": [
        0,
        3.2625,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节类型（h3-canal-inspection-skiff-joint-type）

rudder-pivot 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：prismatic
- B：spring
- C：revolute
- D：fixed

```json
{
  "input": {
    "joint": {
      "id": "rudder-pivot",
      "name": "rudder pivot",
      "type": "revolute",
      "parent": "hull",
      "child": "rudder",
      "anchorParent": [
        5.5,
        -0.2124999999999999,
        0
      ],
      "anchorChild": [
        0,
        0.30000000000000004,
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
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 直接连接（h3-canal-inspection-skiff-parent）

propeller 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["hull","cabin","rudder","propeller","sensor-mast"]
- B：["hull"]
- C：["propeller"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "cabin-mount",
        "name": "cabin mount",
        "type": "fixed",
        "parent": "hull",
        "child": "cabin",
        "anchorParent": [
          0,
          0.48750000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.5875000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rudder-pivot",
        "name": "rudder pivot",
        "type": "revolute",
        "parent": "hull",
        "child": "rudder",
        "anchorParent": [
          5.5,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          0.30000000000000004,
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
        "id": "propeller-shaft",
        "name": "propeller shaft",
        "type": "revolute",
        "parent": "hull",
        "child": "propeller",
        "anchorParent": [
          3.3000000000000003,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          -0.7089691907681028,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "mast-turntable",
        "name": "mast turntable",
        "type": "revolute",
        "parent": "cabin",
        "child": "sensor-mast",
        "anchorParent": [
          0,
          0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 基座识别（h3-canal-inspection-skiff-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：[]
- B：["hull","cabin","rudder","propeller","sensor-mast"]
- C：["propeller"]
- D：["hull"]

```json
{
  "input": {
    "modules": [
      {
        "id": "hull",
        "name": "Catamaran inspection hull",
        "role": "foundation",
        "anchored": true,
        "mass": 16,
        "position": [
          0,
          0.7124999999999999,
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
        "id": "cabin",
        "name": "Inspection cabin",
        "role": "control",
        "anchored": false,
        "mass": 4,
        "position": [
          0,
          1.7875,
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
        "id": "rudder",
        "name": "Steering rudder",
        "role": "actuator",
        "anchored": false,
        "mass": 1,
        "position": [
          5.5,
          0.19999999999999996,
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
        "id": "propeller",
        "name": "Inspection propeller",
        "role": "service-module",
        "anchored": false,
        "mass": 1,
        "position": [
          4.008969190768103,
          0.5,
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
        "id": "sensor-mast",
        "name": "Survey mast",
        "role": "sensor",
        "anchored": false,
        "mass": 1,
        "position": [
          0,
          3.2625,
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

### 接口计数（h3-canal-inspection-skiff-degree）

propeller 连接几个声明关节？平行关节分别计数。

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
        "id": "cabin-mount",
        "name": "cabin mount",
        "type": "fixed",
        "parent": "hull",
        "child": "cabin",
        "anchorParent": [
          0,
          0.48750000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.5875000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rudder-pivot",
        "name": "rudder pivot",
        "type": "revolute",
        "parent": "hull",
        "child": "rudder",
        "anchorParent": [
          5.5,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          0.30000000000000004,
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
        "id": "propeller-shaft",
        "name": "propeller shaft",
        "type": "revolute",
        "parent": "hull",
        "child": "propeller",
        "anchorParent": [
          3.3000000000000003,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          -0.7089691907681028,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "mast-turntable",
        "name": "mast turntable",
        "type": "revolute",
        "parent": "cabin",
        "child": "sensor-mast",
        "anchorParent": [
          0,
          0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 局部改色（h3-canal-inspection-skiff-recolor）

仅将 h0035 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"h0035","color":"#2878b8"}
- B：{"id":"*","color":"#e8792e"}
- C：{"id":"h0035","color":"#e8792e"}
- D：{"id":"h0036","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "h0035",
      "moduleId": "propeller",
      "shape": "axle",
      "size": [
        0.25,
        1.2,
        0.25
      ],
      "position": [
        -0.7089691907681028,
        0,
        0
      ],
      "rotation": [
        0,
        0,
        0.7071067811865475,
        0.7071067811865476
      ],
      "color": "#c6cdd2"
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 补装部件（h3-canal-inspection-skiff-add）

模块 propeller 缺失零件 h0035。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"h0035","moduleId":"propeller","shape":"axle","size":[3,3,3],"position":[-0.7089691907681028,0,0],"rotation":[0,0,0.7071067811865475,0.7071067811865476],"color":"#c6cdd2"}
- B：{"id":"h0035","moduleId":"propeller","shape":"axle","size":[0.25,1.2,0.25],"position":[-0.7089691907681028,0,0],"rotation":[0,0,0.7071067811865475,0.7071067811865476],"color":"#000000"}
- C：{"id":"h0035","moduleId":"propeller","shape":"axle","size":[0.25,1.2,0.25],"position":[-0.7089691907681028,0,0],"rotation":[0,0,0.7071067811865475,0.7071067811865476],"color":"#c6cdd2"}
- D：{"id":"h0035","moduleId":"hull","shape":"axle","size":[0.25,1.2,0.25],"position":[-0.7089691907681028,0,0],"rotation":[0,0,0.7071067811865475,0.7071067811865476],"color":"#c6cdd2"}

```json
{
  "input": {
    "targetPart": {
      "id": "h0035",
      "moduleId": "propeller",
      "shape": "axle",
      "size": [
        0.25,
        1.2,
        0.25
      ],
      "position": [
        -0.7089691907681028,
        0,
        0
      ],
      "rotation": [
        0,
        0,
        0.7071067811865475,
        0.7071067811865476
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
      "h0027",
      "h0028",
      "h0029",
      "h0030",
      "h0031",
      "h0032",
      "h0033",
      "h0034",
      "h0036",
      "h0037",
      "h0038",
      "h0039",
      "h0040",
      "h0041",
      "h0042",
      "h0043",
      "h0044",
      "h0045"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 安全拆除（h3-canal-inspection-skiff-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["hull","cabin","rudder","propeller","sensor-mast"]
- B：["propeller","rudder","sensor-mast"]
- C：["hull"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "cabin-mount",
        "name": "cabin mount",
        "type": "fixed",
        "parent": "hull",
        "child": "cabin",
        "anchorParent": [
          0,
          0.48750000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.5875000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rudder-pivot",
        "name": "rudder pivot",
        "type": "revolute",
        "parent": "hull",
        "child": "rudder",
        "anchorParent": [
          5.5,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          0.30000000000000004,
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
        "id": "propeller-shaft",
        "name": "propeller shaft",
        "type": "revolute",
        "parent": "hull",
        "child": "propeller",
        "anchorParent": [
          3.3000000000000003,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          -0.7089691907681028,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "mast-turntable",
        "name": "mast turntable",
        "type": "revolute",
        "parent": "cabin",
        "child": "sensor-mast",
        "anchorParent": [
          0,
          0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      }
    ],
    "modules": [
      "hull",
      "cabin",
      "rudder",
      "propeller",
      "sensor-mast"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 替换选择（h3-canal-inspection-skiff-replace）

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
        "cost": 5,
        "stiffness": 9,
        "mass": 0.5
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 10,
        "mass": 0.5
      },
      {
        "id": "stock-2",
        "cost": 5,
        "stiffness": 7,
        "mass": 1
      },
      {
        "id": "stock-3",
        "cost": 5,
        "stiffness": 6,
        "mass": 1.8
      }
    ],
    "maxCost": 7
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-canal-inspection-skiff-translate）

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
    "target": "propeller"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-canal-inspection-skiff-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：90
- B：135
- C：-135
- D：0

```json
{
  "input": {
    "module": "propeller",
    "currentYaw": 180,
    "targetYaw": 315
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 下一步放置（h3-canal-inspection-skiff-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：[]
- B：["hull","cabin","rudder"]
- C：["hull"]
- D：["propeller","sensor-mast"]

```json
{
  "input": {
    "prefix": [
      "hull",
      "cabin",
      "rudder"
    ],
    "joints": [
      {
        "id": "cabin-mount",
        "name": "cabin mount",
        "type": "fixed",
        "parent": "hull",
        "child": "cabin",
        "anchorParent": [
          0,
          0.48750000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.5875000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rudder-pivot",
        "name": "rudder pivot",
        "type": "revolute",
        "parent": "hull",
        "child": "rudder",
        "anchorParent": [
          5.5,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          0.30000000000000004,
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
        "id": "propeller-shaft",
        "name": "propeller shaft",
        "type": "revolute",
        "parent": "hull",
        "child": "propeller",
        "anchorParent": [
          3.3000000000000003,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          -0.7089691907681028,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "mast-turntable",
        "name": "mast turntable",
        "type": "revolute",
        "parent": "cabin",
        "child": "sensor-mast",
        "anchorParent": [
          0,
          0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      }
    ],
    "modules": [
      "hull",
      "cabin",
      "rudder",
      "propeller",
      "sensor-mast"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 库存核算（h3-canal-inspection-skiff-inventory）

备件库有 13 件，替换模块需 6 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：8
- B：6
- C：10
- D：7

```json
{
  "input": {
    "available": 13,
    "required": 6
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 子装配边界（h3-canal-inspection-skiff-boundary）

隔离 propeller 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["cabin-mount","rudder-pivot","propeller-shaft","mast-turntable"]
- B：["rudder-pivot"]
- C：["propeller-shaft"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "cabin-mount",
        "name": "cabin mount",
        "type": "fixed",
        "parent": "hull",
        "child": "cabin",
        "anchorParent": [
          0,
          0.48750000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.5875000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rudder-pivot",
        "name": "rudder pivot",
        "type": "revolute",
        "parent": "hull",
        "child": "rudder",
        "anchorParent": [
          5.5,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          0.30000000000000004,
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
        "id": "propeller-shaft",
        "name": "propeller shaft",
        "type": "revolute",
        "parent": "hull",
        "child": "propeller",
        "anchorParent": [
          3.3000000000000003,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          -0.7089691907681028,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "mast-turntable",
        "name": "mast turntable",
        "type": "revolute",
        "parent": "cabin",
        "child": "sensor-mast",
        "anchorParent": [
          0,
          0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      }
    ],
    "target": "propeller"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 最小干预（h3-canal-inspection-skiff-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：6
- D：0

```json
{
  "input": {
    "module": "propeller"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 全过程依赖（h3-canal-inspection-skiff-prefix）

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
      "cabin",
      "hull",
      "rudder",
      "propeller",
      "sensor-mast"
    ],
    "joints": [
      {
        "id": "cabin-mount",
        "name": "cabin mount",
        "type": "fixed",
        "parent": "hull",
        "child": "cabin",
        "anchorParent": [
          0,
          0.48750000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.5875000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rudder-pivot",
        "name": "rudder pivot",
        "type": "revolute",
        "parent": "hull",
        "child": "rudder",
        "anchorParent": [
          5.5,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          0.30000000000000004,
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
        "id": "propeller-shaft",
        "name": "propeller shaft",
        "type": "revolute",
        "parent": "hull",
        "child": "propeller",
        "anchorParent": [
          3.3000000000000003,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          -0.7089691907681028,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "mast-turntable",
        "name": "mast turntable",
        "type": "revolute",
        "parent": "cabin",
        "child": "sensor-mast",
        "anchorParent": [
          0,
          0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 连续维修路径（h3-canal-inspection-skiff-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-1
- B：path-0
- C：path-2

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          9.625,
          0.5,
          0
        ],
        "end": [
          4.008969190768103,
          0.5,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.680195689201355
      },
      {
        "id": "path-1",
        "start": [
          4.008969190768103,
          8.8,
          0
        ],
        "end": [
          4.008969190768103,
          0.5,
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
          4.008969190768103,
          0.5,
          6.125
        ],
        "end": [
          4.008969190768103,
          0.5,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.6236735582351685
      }
    ],
    "simulator": "stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration"
  },
  "answer": {
    "choiceIds": [
      "A"
    ]
  }
}
```

### 支撑反事实（h3-canal-inspection-skiff-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["sensor-mast"]
- B：["cabin"]
- C：[]
- D：["hull","cabin","rudder","propeller","sensor-mast"]

```json
{
  "input": {
    "removed": "cabin",
    "roots": [
      "hull"
    ],
    "joints": [
      {
        "id": "cabin-mount",
        "name": "cabin mount",
        "type": "fixed",
        "parent": "hull",
        "child": "cabin",
        "anchorParent": [
          0,
          0.48750000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.5875000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rudder-pivot",
        "name": "rudder pivot",
        "type": "revolute",
        "parent": "hull",
        "child": "rudder",
        "anchorParent": [
          5.5,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          0.30000000000000004,
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
        "id": "propeller-shaft",
        "name": "propeller shaft",
        "type": "revolute",
        "parent": "hull",
        "child": "propeller",
        "anchorParent": [
          3.3000000000000003,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          -0.7089691907681028,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "mast-turntable",
        "name": "mast turntable",
        "type": "revolute",
        "parent": "cabin",
        "child": "sensor-mast",
        "anchorParent": [
          0,
          0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      }
    ],
    "modules": [
      "hull",
      "cabin",
      "rudder",
      "propeller",
      "sensor-mast"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 冲击响应读数（h3-canal-inspection-skiff-dynamic）

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
    "nominalDrift": 1.952494609368905e-7,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-canal-inspection-skiff-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：0
- B：-1.1
- C：1.1
- D：-0.6

```json
{
  "input": {
    "joint": "rudder-pivot",
    "limits": [
      -0.6,
      0.6
    ],
    "units": "radians"
  },
  "answer": {
    "choiceIds": [
      "A",
      "D"
    ]
  }
}
```

### 约束故障诊断（h3-canal-inspection-skiff-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：rudder-pivot
- B：mast-turntable
- C：propeller-shaft
- D：cabin-mount

```json
{
  "input": {
    "endpoints": [
      "hull",
      "propeller"
    ],
    "type": "revolute",
    "joints": [
      {
        "id": "cabin-mount",
        "name": "cabin mount",
        "type": "fixed",
        "parent": "hull",
        "child": "cabin",
        "anchorParent": [
          0,
          0.48750000000000004,
          0
        ],
        "anchorChild": [
          0,
          -0.5875000000000001,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rudder-pivot",
        "name": "rudder pivot",
        "type": "revolute",
        "parent": "hull",
        "child": "rudder",
        "anchorParent": [
          5.5,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          0.30000000000000004,
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
        "id": "propeller-shaft",
        "name": "propeller shaft",
        "type": "revolute",
        "parent": "hull",
        "child": "propeller",
        "anchorParent": [
          3.3000000000000003,
          -0.2124999999999999,
          0
        ],
        "anchorChild": [
          -0.7089691907681028,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "mast-turntable",
        "name": "mast turntable",
        "type": "revolute",
        "parent": "cabin",
        "child": "sensor-mast",
        "anchorParent": [
          0,
          0.2124999999999999,
          0
        ],
        "anchorChild": [
          0,
          -1.2625000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
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

### 主动检查收益（h3-canal-inspection-skiff-information-gain）

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
    "module": "propeller",
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

### 不确定性与弃答（h3-canal-inspection-skiff-abstention）

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

### 观测后信念更新（h3-canal-inspection-skiff-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.25
- B：0.5
- C：0.3333333333333333
- D：0

```json
{
  "input": {
    "module": "propeller",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "negative",
      "negative",
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

### 多目标工程权衡（h3-canal-inspection-skiff-pareto）

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
        "stiffness": 9,
        "mass": 0.5
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 10,
        "mass": 0.5
      },
      {
        "id": "stock-2",
        "cost": 5,
        "stiffness": 7,
        "mass": 1
      },
      {
        "id": "stock-3",
        "cost": 5,
        "stiffness": 6,
        "mass": 1.8
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "C",
      "D"
    ]
  }
}
```

### 依赖装配（h3-canal-inspection-skiff-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:rudder",
        "label": "安装 rudder",
        "requires": [
          "present:hull"
        ],
        "forbids": [
          "present:rudder"
        ],
        "adds": [
          "present:rudder"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rudder",
          "visible": true
        }
      },
      {
        "id": "place:propeller",
        "label": "安装 propeller",
        "requires": [
          "present:hull"
        ],
        "forbids": [
          "present:propeller"
        ],
        "adds": [
          "present:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller",
          "visible": true
        }
      },
      {
        "id": "place:sensor-mast",
        "label": "安装 sensor-mast",
        "requires": [
          "present:cabin"
        ],
        "forbids": [
          "present:sensor-mast"
        ],
        "adds": [
          "present:sensor-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast",
          "visible": true
        }
      },
      {
        "id": "place:cabin",
        "label": "安装 cabin",
        "requires": [
          "present:hull"
        ],
        "forbids": [
          "present:cabin"
        ],
        "adds": [
          "present:cabin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cabin",
          "visible": true
        }
      },
      {
        "id": "place:hull",
        "label": "安装 hull",
        "requires": [],
        "forbids": [
          "present:hull"
        ],
        "adds": [
          "present:hull"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hull",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:hull",
      "present:cabin",
      "present:rudder",
      "present:propeller",
      "present:sensor-mast"
    ],
    "budget": 5,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:hull",
      "place:rudder",
      "place:propeller",
      "place:cabin",
      "place:sensor-mast"
    ]
  }
}
```

### 依赖拆解（h3-canal-inspection-skiff-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:hull",
      "present:cabin",
      "present:rudder",
      "present:propeller",
      "present:sensor-mast"
    ],
    "initialModules": [
      "hull",
      "cabin",
      "rudder",
      "propeller",
      "sensor-mast"
    ],
    "actions": [
      {
        "id": "remove:rudder",
        "label": "拆除 rudder",
        "requires": [
          "present:rudder"
        ],
        "forbids": [],
        "adds": [
          "removed:rudder"
        ],
        "deletes": [
          "present:rudder"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rudder",
          "visible": false
        }
      },
      {
        "id": "remove:cabin",
        "label": "拆除 cabin",
        "requires": [
          "present:cabin"
        ],
        "forbids": [
          "present:sensor-mast"
        ],
        "adds": [
          "removed:cabin"
        ],
        "deletes": [
          "present:cabin"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cabin",
          "visible": false
        }
      },
      {
        "id": "remove:sensor-mast",
        "label": "拆除 sensor-mast",
        "requires": [
          "present:sensor-mast"
        ],
        "forbids": [],
        "adds": [
          "removed:sensor-mast"
        ],
        "deletes": [
          "present:sensor-mast"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast",
          "visible": false
        }
      },
      {
        "id": "remove:propeller",
        "label": "拆除 propeller",
        "requires": [
          "present:propeller"
        ],
        "forbids": [],
        "adds": [
          "removed:propeller"
        ],
        "deletes": [
          "present:propeller"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "propeller",
          "visible": false
        }
      },
      {
        "id": "remove:hull",
        "label": "拆除 hull",
        "requires": [
          "present:hull"
        ],
        "forbids": [
          "present:cabin",
          "present:rudder",
          "present:propeller"
        ],
        "adds": [
          "removed:hull"
        ],
        "deletes": [
          "present:hull"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "hull",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:sensor-mast",
      "removed:propeller",
      "removed:rudder",
      "removed:cabin",
      "removed:hull"
    ],
    "budget": 5,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:rudder",
      "remove:sensor-mast",
      "remove:cabin",
      "remove:propeller",
      "remove:hull"
    ]
  }
}
```

### 承载维修（h3-canal-inspection-skiff-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:propeller",
      "closed:propeller"
    ],
    "initialModules": [
      "hull",
      "cabin",
      "rudder",
      "propeller",
      "sensor-mast"
    ],
    "actions": [
      {
        "id": "replace:propeller",
        "label": "replace propeller",
        "requires": [
          "done:remove:propeller"
        ],
        "forbids": [
          "done:replace:propeller"
        ],
        "adds": [
          "done:replace:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller",
          "visible": true
        }
      },
      {
        "id": "support:propeller",
        "label": "support propeller",
        "requires": [
          "fault:propeller"
        ],
        "forbids": [
          "done:support:propeller"
        ],
        "adds": [
          "done:support:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "release:propeller",
        "label": "release propeller",
        "requires": [
          "done:close:propeller"
        ],
        "forbids": [
          "done:release:propeller"
        ],
        "adds": [
          "done:release:propeller",
          "repaired:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "remove:propeller",
        "label": "remove propeller",
        "requires": [
          "done:open:propeller"
        ],
        "forbids": [
          "done:remove:propeller"
        ],
        "adds": [
          "done:remove:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller",
          "visible": false
        }
      },
      {
        "id": "open:propeller",
        "label": "open propeller",
        "requires": [
          "done:support:propeller"
        ],
        "forbids": [
          "done:open:propeller"
        ],
        "adds": [
          "done:open:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "verify:propeller",
        "label": "verify propeller",
        "requires": [
          "done:replace:propeller"
        ],
        "forbids": [
          "done:verify:propeller"
        ],
        "adds": [
          "done:verify:propeller"
        ],
        "deletes": [
          "fault:propeller"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "close:propeller",
        "label": "close propeller",
        "requires": [
          "done:verify:propeller"
        ],
        "forbids": [
          "done:close:propeller"
        ],
        "adds": [
          "done:close:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      }
    ],
    "goalFacts": [
      "repaired:propeller"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:propeller",
      "open:propeller",
      "remove:propeller",
      "replace:propeller",
      "verify:propeller",
      "close:propeller",
      "release:propeller"
    ]
  }
}
```

### 复合编辑验证（h3-canal-inspection-skiff-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:propeller",
      "closed:propeller"
    ],
    "initialModules": [
      "hull",
      "cabin",
      "rudder",
      "propeller",
      "sensor-mast"
    ],
    "actions": [
      {
        "id": "support:propeller",
        "label": "support propeller",
        "requires": [
          "fault:propeller"
        ],
        "forbids": [
          "done:support:propeller"
        ],
        "adds": [
          "done:support:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "recolor:propeller",
        "label": "recolor propeller",
        "requires": [
          "done:open:propeller"
        ],
        "forbids": [
          "done:recolor:propeller"
        ],
        "adds": [
          "done:recolor:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller",
          "color": "#ea7635"
        }
      },
      {
        "id": "release:propeller",
        "label": "release propeller",
        "requires": [
          "done:close:propeller"
        ],
        "forbids": [
          "done:release:propeller"
        ],
        "adds": [
          "done:release:propeller",
          "repaired:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "open:propeller",
        "label": "open propeller",
        "requires": [
          "done:support:propeller"
        ],
        "forbids": [
          "done:open:propeller"
        ],
        "adds": [
          "done:open:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "verify:propeller",
        "label": "verify propeller",
        "requires": [
          "done:recolor:propeller"
        ],
        "forbids": [
          "done:verify:propeller"
        ],
        "adds": [
          "done:verify:propeller"
        ],
        "deletes": [
          "fault:propeller"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "close:propeller",
        "label": "close propeller",
        "requires": [
          "done:verify:propeller"
        ],
        "forbids": [
          "done:close:propeller"
        ],
        "adds": [
          "done:close:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      }
    ],
    "goalFacts": [
      "repaired:propeller"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:propeller",
      "open:propeller",
      "recolor:propeller",
      "verify:propeller",
      "close:propeller",
      "release:propeller"
    ]
  }
}
```

### 跨区域联合维修（h3-canal-inspection-skiff-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:propeller",
      "closed:propeller",
      "fault:sensor-mast",
      "closed:sensor-mast"
    ],
    "initialModules": [
      "hull",
      "cabin",
      "rudder",
      "propeller",
      "sensor-mast"
    ],
    "actions": [
      {
        "id": "replace:propeller",
        "label": "replace propeller",
        "requires": [
          "done:remove:propeller"
        ],
        "forbids": [
          "done:replace:propeller"
        ],
        "adds": [
          "done:replace:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller",
          "visible": true
        }
      },
      {
        "id": "verify:sensor-mast",
        "label": "verify sensor-mast",
        "requires": [
          "done:replace:sensor-mast"
        ],
        "forbids": [
          "done:verify:sensor-mast"
        ],
        "adds": [
          "done:verify:sensor-mast"
        ],
        "deletes": [
          "fault:sensor-mast"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast"
        }
      },
      {
        "id": "support:sensor-mast",
        "label": "support sensor-mast",
        "requires": [
          "fault:sensor-mast"
        ],
        "forbids": [
          "done:support:sensor-mast"
        ],
        "adds": [
          "done:support:sensor-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast"
        }
      },
      {
        "id": "release:sensor-mast",
        "label": "release sensor-mast",
        "requires": [
          "done:close:sensor-mast"
        ],
        "forbids": [
          "done:release:sensor-mast"
        ],
        "adds": [
          "done:release:sensor-mast",
          "repaired:sensor-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast"
        }
      },
      {
        "id": "support:propeller",
        "label": "support propeller",
        "requires": [
          "fault:propeller"
        ],
        "forbids": [
          "done:support:propeller"
        ],
        "adds": [
          "done:support:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "remove:sensor-mast",
        "label": "remove sensor-mast",
        "requires": [
          "done:open:sensor-mast"
        ],
        "forbids": [
          "done:remove:sensor-mast"
        ],
        "adds": [
          "done:remove:sensor-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast",
          "visible": false
        }
      },
      {
        "id": "release:propeller",
        "label": "release propeller",
        "requires": [
          "done:close:propeller"
        ],
        "forbids": [
          "done:release:propeller"
        ],
        "adds": [
          "done:release:propeller",
          "repaired:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "remove:propeller",
        "label": "remove propeller",
        "requires": [
          "done:open:propeller"
        ],
        "forbids": [
          "done:remove:propeller"
        ],
        "adds": [
          "done:remove:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller",
          "visible": false
        }
      },
      {
        "id": "open:propeller",
        "label": "open propeller",
        "requires": [
          "done:support:propeller"
        ],
        "forbids": [
          "done:open:propeller"
        ],
        "adds": [
          "done:open:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "verify:propeller",
        "label": "verify propeller",
        "requires": [
          "done:replace:propeller"
        ],
        "forbids": [
          "done:verify:propeller"
        ],
        "adds": [
          "done:verify:propeller"
        ],
        "deletes": [
          "fault:propeller"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "close:sensor-mast",
        "label": "close sensor-mast",
        "requires": [
          "done:verify:sensor-mast"
        ],
        "forbids": [
          "done:close:sensor-mast"
        ],
        "adds": [
          "done:close:sensor-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast"
        }
      },
      {
        "id": "replace:sensor-mast",
        "label": "replace sensor-mast",
        "requires": [
          "done:remove:sensor-mast"
        ],
        "forbids": [
          "done:replace:sensor-mast"
        ],
        "adds": [
          "done:replace:sensor-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast",
          "visible": true
        }
      },
      {
        "id": "close:propeller",
        "label": "close propeller",
        "requires": [
          "done:verify:propeller"
        ],
        "forbids": [
          "done:close:propeller"
        ],
        "adds": [
          "done:close:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "open:sensor-mast",
        "label": "open sensor-mast",
        "requires": [
          "done:support:sensor-mast"
        ],
        "forbids": [
          "done:open:sensor-mast"
        ],
        "adds": [
          "done:open:sensor-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast"
        }
      }
    ],
    "goalFacts": [
      "repaired:propeller",
      "repaired:sensor-mast"
    ],
    "budget": 14,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:sensor-mast",
      "support:propeller",
      "open:propeller",
      "remove:propeller",
      "replace:propeller",
      "verify:propeller",
      "close:propeller",
      "release:propeller",
      "open:sensor-mast",
      "remove:sensor-mast",
      "replace:sensor-mast",
      "verify:sensor-mast",
      "close:sensor-mast",
      "release:sensor-mast"
    ]
  }
}
```

### 多工位资源调度（h3-canal-inspection-skiff-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "hull",
        "duration": 3,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "cabin",
        "duration": 2,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "rudder",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "propeller",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "sensor-mast",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      }
    ],
    "deadline": 7
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 3,
      "job-3": 2,
      "job-4": 6
    }
  }
}
```

### 检查后条件策略（h3-canal-inspection-skiff-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "propeller",
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

### 局部坐标变换（h3-canal-inspection-skiff-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[5.3,1.5,1]
- B：[4.3,0.5,0]
- C：[0.29103,0,0]

```json
{
  "input": {
    "localPoint": [
      0.29103080923189717,
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
      4.008969190768103,
      0.5,
      0
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 正交视图投影（h3-canal-inspection-skiff-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[0,0]
- B：[-4,7]
- C：[7,3]
- D：[3,4]

```json
{
  "input": {
    "view": "side",
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

### 空间相对关系（h3-canal-inspection-skiff-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：less
- B：equal
- C：greater

```json
{
  "input": {
    "A": {
      "id": "hull",
      "position": [
        0,
        0.7124999999999999,
        0
      ]
    },
    "B": {
      "id": "sensor-mast",
      "position": [
        0,
        3.2625,
        0
      ]
    },
    "axis": "y"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 约束自由度（h3-canal-inspection-skiff-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：3
- B：6
- C：0
- D：1

```json
{
  "input": {
    "joint": {
      "id": "cabin-mount",
      "name": "cabin mount",
      "type": "fixed",
      "parent": "hull",
      "child": "cabin",
      "anchorParent": [
        0,
        0.48750000000000004,
        0
      ],
      "anchorChild": [
        0,
        -0.5875000000000001,
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
    "choiceId": "C"
  }
}
```

### 维修间隙预算（h3-canal-inspection-skiff-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "propeller",
    "aperture": 0.52,
    "toolWidth": 0.45,
    "eachSideMargin": 0.05
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-canal-inspection-skiff-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,-8]
- B：[0,0,8]
- C：[0,0,0]
- D：[0,-2,0]

```json
{
  "input": {
    "module": "propeller",
    "lever": [
      2,
      2,
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
    "choiceId": "A"
  }
}
```

### 非均匀先验更新（h3-canal-inspection-skiff-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0.3333333333333333
- C：0
- D：1

```json
{
  "input": {
    "module": "propeller",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      3,
      3,
      3
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

### 风险最小决策（h3-canal-inspection-skiff-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.5,
    "repairCost": 2,
    "failureLoss": 10,
    "module": "propeller"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-canal-inspection-skiff-trace-threshold）

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

### 安全联锁维修（h3-canal-inspection-skiff-guarded-repair）

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
        "id": "release:propeller",
        "label": "release propeller",
        "requires": [
          "done:relock:propeller"
        ],
        "forbids": [
          "done:release:propeller"
        ],
        "adds": [
          "done:release:propeller",
          "ready:propeller",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "relock:propeller",
        "label": "relock propeller",
        "requires": [
          "done:verify:propeller"
        ],
        "forbids": [
          "done:relock:propeller"
        ],
        "adds": [
          "done:relock:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "verify:propeller",
        "label": "verify propeller",
        "requires": [
          "done:replace:propeller"
        ],
        "forbids": [
          "done:verify:propeller"
        ],
        "adds": [
          "done:verify:propeller"
        ],
        "deletes": [
          "fault:propeller",
          "misaligned:propeller"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "replace:propeller",
        "label": "replace propeller",
        "requires": [
          "done:unlock:propeller"
        ],
        "forbids": [
          "done:replace:propeller"
        ],
        "adds": [
          "done:replace:propeller"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "unlock:propeller",
        "label": "unlock propeller",
        "requires": [
          "done:support:propeller"
        ],
        "forbids": [
          "done:unlock:propeller"
        ],
        "adds": [
          "done:unlock:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "support:propeller",
        "label": "support propeller",
        "requires": [
          "done:isolate:propeller"
        ],
        "forbids": [
          "done:support:propeller"
        ],
        "adds": [
          "done:support:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "isolate:propeller",
        "label": "isolate propeller",
        "requires": [
          "tool:free",
          "fault:propeller"
        ],
        "forbids": [
          "done:isolate:propeller"
        ],
        "adds": [
          "done:isolate:propeller"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:propeller"
    ],
    "initialModules": [
      "hull",
      "cabin",
      "rudder",
      "propeller",
      "sensor-mast"
    ],
    "goalFacts": [
      "ready:propeller"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:propeller",
      "support:propeller",
      "unlock:propeller",
      "replace:propeller",
      "verify:propeller",
      "relock:propeller",
      "release:propeller"
    ]
  }
}
```

### 失败状态回退（h3-canal-inspection-skiff-rollback）

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
        "id": "resume:propeller",
        "label": "resume propeller",
        "requires": [
          "done:verify:propeller"
        ],
        "forbids": [
          "done:resume:propeller"
        ],
        "adds": [
          "done:resume:propeller",
          "ready:propeller",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "verify:propeller",
        "label": "verify propeller",
        "requires": [
          "done:align:propeller"
        ],
        "forbids": [
          "done:verify:propeller"
        ],
        "adds": [
          "done:verify:propeller"
        ],
        "deletes": [
          "fault:propeller",
          "misaligned:propeller"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "align:propeller",
        "label": "align propeller",
        "requires": [
          "done:undo:propeller"
        ],
        "forbids": [
          "done:align:propeller"
        ],
        "adds": [
          "done:align:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller",
          "visible": true
        }
      },
      {
        "id": "undo:propeller",
        "label": "undo propeller",
        "requires": [
          "done:isolate:propeller"
        ],
        "forbids": [
          "done:undo:propeller"
        ],
        "adds": [
          "done:undo:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller",
          "visible": false
        }
      },
      {
        "id": "isolate:propeller",
        "label": "isolate propeller",
        "requires": [
          "tool:free",
          "fault:propeller"
        ],
        "forbids": [
          "done:isolate:propeller"
        ],
        "adds": [
          "done:isolate:propeller"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:propeller",
      "misaligned:propeller"
    ],
    "initialModules": [
      "hull",
      "cabin",
      "rudder",
      "propeller",
      "sensor-mast"
    ],
    "goalFacts": [
      "ready:propeller"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:propeller",
      "undo:propeller",
      "align:propeller",
      "verify:propeller",
      "resume:propeller"
    ]
  }
}
```

### 共享工具协同维修（h3-canal-inspection-skiff-resource-repair）

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
        "id": "release:sensor-mast",
        "label": "release sensor-mast",
        "requires": [
          "done:relock:sensor-mast"
        ],
        "forbids": [
          "done:release:sensor-mast"
        ],
        "adds": [
          "done:release:sensor-mast",
          "ready:sensor-mast",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast"
        }
      },
      {
        "id": "relock:sensor-mast",
        "label": "relock sensor-mast",
        "requires": [
          "done:verify:sensor-mast"
        ],
        "forbids": [
          "done:relock:sensor-mast"
        ],
        "adds": [
          "done:relock:sensor-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast"
        }
      },
      {
        "id": "verify:sensor-mast",
        "label": "verify sensor-mast",
        "requires": [
          "done:replace:sensor-mast"
        ],
        "forbids": [
          "done:verify:sensor-mast"
        ],
        "adds": [
          "done:verify:sensor-mast"
        ],
        "deletes": [
          "fault:sensor-mast",
          "misaligned:sensor-mast"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast"
        }
      },
      {
        "id": "replace:sensor-mast",
        "label": "replace sensor-mast",
        "requires": [
          "done:unlock:sensor-mast"
        ],
        "forbids": [
          "done:replace:sensor-mast"
        ],
        "adds": [
          "done:replace:sensor-mast"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "sensor-mast"
        }
      },
      {
        "id": "unlock:sensor-mast",
        "label": "unlock sensor-mast",
        "requires": [
          "done:support:sensor-mast"
        ],
        "forbids": [
          "done:unlock:sensor-mast"
        ],
        "adds": [
          "done:unlock:sensor-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast"
        }
      },
      {
        "id": "support:sensor-mast",
        "label": "support sensor-mast",
        "requires": [
          "done:isolate:sensor-mast"
        ],
        "forbids": [
          "done:support:sensor-mast"
        ],
        "adds": [
          "done:support:sensor-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast"
        }
      },
      {
        "id": "isolate:sensor-mast",
        "label": "isolate sensor-mast",
        "requires": [
          "tool:free",
          "fault:sensor-mast"
        ],
        "forbids": [
          "done:isolate:sensor-mast"
        ],
        "adds": [
          "done:isolate:sensor-mast"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sensor-mast"
        }
      },
      {
        "id": "release:propeller",
        "label": "release propeller",
        "requires": [
          "done:relock:propeller"
        ],
        "forbids": [
          "done:release:propeller"
        ],
        "adds": [
          "done:release:propeller",
          "ready:propeller",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "relock:propeller",
        "label": "relock propeller",
        "requires": [
          "done:verify:propeller"
        ],
        "forbids": [
          "done:relock:propeller"
        ],
        "adds": [
          "done:relock:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "verify:propeller",
        "label": "verify propeller",
        "requires": [
          "done:replace:propeller"
        ],
        "forbids": [
          "done:verify:propeller"
        ],
        "adds": [
          "done:verify:propeller"
        ],
        "deletes": [
          "fault:propeller",
          "misaligned:propeller"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "replace:propeller",
        "label": "replace propeller",
        "requires": [
          "done:unlock:propeller"
        ],
        "forbids": [
          "done:replace:propeller"
        ],
        "adds": [
          "done:replace:propeller"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "unlock:propeller",
        "label": "unlock propeller",
        "requires": [
          "done:support:propeller"
        ],
        "forbids": [
          "done:unlock:propeller"
        ],
        "adds": [
          "done:unlock:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "support:propeller",
        "label": "support propeller",
        "requires": [
          "done:isolate:propeller"
        ],
        "forbids": [
          "done:support:propeller"
        ],
        "adds": [
          "done:support:propeller"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "isolate:propeller",
        "label": "isolate propeller",
        "requires": [
          "tool:free",
          "fault:propeller"
        ],
        "forbids": [
          "done:isolate:propeller"
        ],
        "adds": [
          "done:isolate:propeller"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "propeller"
        }
      },
      {
        "id": "release:rudder",
        "label": "release rudder",
        "requires": [
          "done:relock:rudder"
        ],
        "forbids": [
          "done:release:rudder"
        ],
        "adds": [
          "done:release:rudder",
          "ready:rudder",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rudder"
        }
      },
      {
        "id": "relock:rudder",
        "label": "relock rudder",
        "requires": [
          "done:verify:rudder"
        ],
        "forbids": [
          "done:relock:rudder"
        ],
        "adds": [
          "done:relock:rudder"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rudder"
        }
      },
      {
        "id": "verify:rudder",
        "label": "verify rudder",
        "requires": [
          "done:replace:rudder"
        ],
        "forbids": [
          "done:verify:rudder"
        ],
        "adds": [
          "done:verify:rudder"
        ],
        "deletes": [
          "fault:rudder",
          "misaligned:rudder"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rudder"
        }
      },
      {
        "id": "replace:rudder",
        "label": "replace rudder",
        "requires": [
          "done:unlock:rudder"
        ],
        "forbids": [
          "done:replace:rudder"
        ],
        "adds": [
          "done:replace:rudder"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "rudder"
        }
      },
      {
        "id": "unlock:rudder",
        "label": "unlock rudder",
        "requires": [
          "done:support:rudder"
        ],
        "forbids": [
          "done:unlock:rudder"
        ],
        "adds": [
          "done:unlock:rudder"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rudder"
        }
      },
      {
        "id": "support:rudder",
        "label": "support rudder",
        "requires": [
          "done:isolate:rudder"
        ],
        "forbids": [
          "done:support:rudder"
        ],
        "adds": [
          "done:support:rudder"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rudder"
        }
      },
      {
        "id": "isolate:rudder",
        "label": "isolate rudder",
        "requires": [
          "tool:free",
          "fault:rudder"
        ],
        "forbids": [
          "done:isolate:rudder"
        ],
        "adds": [
          "done:isolate:rudder"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rudder"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:rudder",
      "fault:propeller",
      "fault:sensor-mast"
    ],
    "initialModules": [
      "hull",
      "cabin",
      "rudder",
      "propeller",
      "sensor-mast"
    ],
    "goalFacts": [
      "ready:rudder",
      "ready:propeller",
      "ready:sensor-mast"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 24
  },
  "answer": {
    "actionIds": [
      "isolate:sensor-mast",
      "support:sensor-mast",
      "unlock:sensor-mast",
      "replace:sensor-mast",
      "verify:sensor-mast",
      "relock:sensor-mast",
      "release:sensor-mast",
      "isolate:propeller",
      "support:propeller",
      "unlock:propeller",
      "replace:propeller",
      "verify:propeller",
      "relock:propeller",
      "release:propeller",
      "isolate:rudder",
      "support:rudder",
      "unlock:rudder",
      "replace:rudder",
      "verify:rudder",
      "relock:rudder",
      "release:rudder"
    ]
  }
}
```

### 预算约束检查策略（h3-canal-inspection-skiff-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "propeller",
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
        "cost": 2,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      },
      {
        "id": "thermal",
        "cost": 0,
        "returns": {
          "nominal": "pass",
          "fault": "pass"
        }
      }
    ],
    "budget": 2
  },
  "answer": {
    "queryId": "probe",
    "decisions": {
      "pass": "continue",
      "fail": "tighten"
    }
  }
}
```
