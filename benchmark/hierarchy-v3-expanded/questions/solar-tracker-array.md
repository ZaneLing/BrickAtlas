## D2 双轴太阳能跟踪阵列

### 模块识别（h3-solar-tracker-array-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：yoke
- B：battery
- C：foundation
- D：mast

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "foundation",
        "name": "Tracker foundation"
      },
      {
        "id": "mast",
        "name": "Rotating support mast"
      },
      {
        "id": "yoke",
        "name": "Azimuth yoke"
      },
      {
        "id": "panel-left",
        "name": "Left solar wing"
      },
      {
        "id": "panel-right",
        "name": "Right solar wing"
      },
      {
        "id": "battery",
        "name": "Tracker battery pack"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 部件计数（h3-solar-tracker-array-count）

模块 battery 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：7
- B：4
- C：5
- D：3

```json
{
  "input": {
    "parts": [
      {
        "id": "h0001",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0002",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0003",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0004",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0005",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0006",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0007",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0008",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0009",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0010",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0011",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0012",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0013",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0014",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0015",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0016",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0017",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "h0018",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "h0019",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "h0020",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "h0021",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "h0022",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "h0023",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "h0024",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "h0025",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "h0026",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "h0027",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "h0028",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "h0029",
        "moduleId": "yoke",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0030",
        "moduleId": "yoke",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0031",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0032",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0033",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0034",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0035",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0036",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0037",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0038",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0039",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0040",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0041",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0042",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0043",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0044",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0045",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0046",
        "moduleId": "panel-left",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0047",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0048",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0049",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0050",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0051",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0052",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0053",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0054",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0055",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0056",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0057",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0058",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0059",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0060",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0061",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0062",
        "moduleId": "panel-right",
        "shape": "panel",
        "color": "#2878b8"
      },
      {
        "id": "h0063",
        "moduleId": "battery",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0064",
        "moduleId": "battery",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0065",
        "moduleId": "battery",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0066",
        "moduleId": "battery",
        "shape": "plate",
        "color": "#f2bf3c"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 颜色识别（h3-solar-tracker-array-color）

零件 h0063 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#2878b8
- B：#d43a32
- C：#26323b
- D：#f2bf3c

```json
{
  "input": {
    "part": {
      "id": "h0063",
      "moduleId": "battery",
      "shape": "plate",
      "size": [
        0.92,
        0.25,
        0.92
      ],
      "position": [
        -0.5,
        -0.04999999999999993,
        -0.5
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#f2bf3c"
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 三维位置（h3-solar-tracker-array-position）

模块 battery 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,5.325,0]
- B：[0,0.85,2.5]
- C：[0,0.2,0]
- D：[0,2.675,0]

```json
{
  "input": {
    "centers": {
      "foundation": [
        0,
        0.2,
        0
      ],
      "mast": [
        0,
        2.675,
        0
      ],
      "yoke": [
        0,
        5.325,
        0
      ],
      "panel-left": [
        -4.6000000000000005,
        5.5,
        0
      ],
      "panel-right": [
        4.6000000000000005,
        5.5,
        0
      ],
      "battery": [
        0,
        0.85,
        2.5
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节类型（h3-solar-tracker-array-joint-type）

yoke-tilt 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：fixed
- B：prismatic
- C：spring
- D：revolute

```json
{
  "input": {
    "joint": {
      "id": "yoke-tilt",
      "name": "yoke tilt",
      "type": "revolute",
      "parent": "mast",
      "child": "yoke",
      "anchorParent": [
        0,
        2.825,
        0
      ],
      "anchorChild": [
        0,
        0.17499999999999982,
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

### 直接连接（h3-solar-tracker-array-parent）

battery 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["battery"]
- B：[]
- C：["foundation","mast","yoke","panel-left","panel-right","battery"]
- D：["foundation"]

```json
{
  "input": {
    "joints": [
      {
        "id": "mast-base",
        "name": "mast base",
        "type": "revolute",
        "parent": "foundation",
        "child": "mast",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.175,
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
      },
      {
        "id": "yoke-tilt",
        "name": "yoke tilt",
        "type": "revolute",
        "parent": "mast",
        "child": "yoke",
        "anchorParent": [
          0,
          2.825,
          0
        ],
        "anchorChild": [
          0,
          0.17499999999999982,
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
        "id": "left-panel-hinge",
        "name": "left panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-left",
        "anchorParent": [
          -3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "right-panel-hinge",
        "name": "right panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-right",
        "anchorParent": [
          3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          -1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "battery-lock",
        "name": "battery lock",
        "type": "fixed",
        "parent": "foundation",
        "child": "battery",
        "anchorParent": [
          0,
          0.6000000000000001,
          2
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.5
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

### 基座识别（h3-solar-tracker-array-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","mast","yoke","panel-left","panel-right","battery"]
- C：["battery"]
- D：["foundation"]

```json
{
  "input": {
    "modules": [
      {
        "id": "foundation",
        "name": "Tracker foundation",
        "role": "foundation",
        "anchored": true,
        "mass": 18,
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
        "id": "mast",
        "name": "Rotating support mast",
        "role": "support",
        "anchored": false,
        "mass": 5,
        "position": [
          0,
          2.675,
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
        "id": "yoke",
        "name": "Azimuth yoke",
        "role": "actuator",
        "anchored": false,
        "mass": 3,
        "position": [
          0,
          5.325,
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
        "id": "panel-left",
        "name": "Left solar wing",
        "role": "energy-surface",
        "anchored": false,
        "mass": 3,
        "position": [
          -4.6000000000000005,
          5.5,
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
        "id": "panel-right",
        "name": "Right solar wing",
        "role": "energy-surface",
        "anchored": false,
        "mass": 3,
        "position": [
          4.6000000000000005,
          5.5,
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
        "id": "battery",
        "name": "Tracker battery pack",
        "role": "service-module",
        "anchored": false,
        "mass": 2,
        "position": [
          0,
          0.85,
          2.5
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

### 接口计数（h3-solar-tracker-array-degree）

battery 连接几个声明关节？平行关节分别计数。

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
        "id": "mast-base",
        "name": "mast base",
        "type": "revolute",
        "parent": "foundation",
        "child": "mast",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.175,
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
      },
      {
        "id": "yoke-tilt",
        "name": "yoke tilt",
        "type": "revolute",
        "parent": "mast",
        "child": "yoke",
        "anchorParent": [
          0,
          2.825,
          0
        ],
        "anchorChild": [
          0,
          0.17499999999999982,
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
        "id": "left-panel-hinge",
        "name": "left panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-left",
        "anchorParent": [
          -3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "right-panel-hinge",
        "name": "right panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-right",
        "anchorParent": [
          3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          -1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "battery-lock",
        "name": "battery lock",
        "type": "fixed",
        "parent": "foundation",
        "child": "battery",
        "anchorParent": [
          0,
          0.6000000000000001,
          2
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.5
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

### 局部改色（h3-solar-tracker-array-recolor）

仅将 h0063 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"h0064","color":"#e8792e"}
- B：{"id":"h0063","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"h0063","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "h0063",
      "moduleId": "battery",
      "shape": "plate",
      "size": [
        0.92,
        0.25,
        0.92
      ],
      "position": [
        -0.5,
        -0.04999999999999993,
        -0.5
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#f2bf3c"
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 补装部件（h3-solar-tracker-array-add）

模块 battery 缺失零件 h0063。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"h0063","moduleId":"battery","shape":"plate","size":[3,3,3],"position":[-0.5,-0.04999999999999993,-0.5],"rotation":[0,0,0,1],"color":"#f2bf3c"}
- B：{"id":"h0063","moduleId":"battery","shape":"plate","size":[0.92,0.25,0.92],"position":[-0.5,-0.04999999999999993,-0.5],"rotation":[0,0,0,1],"color":"#000000"}
- C：{"id":"h0063","moduleId":"battery","shape":"plate","size":[0.92,0.25,0.92],"position":[-0.5,-0.04999999999999993,-0.5],"rotation":[0,0,0,1],"color":"#f2bf3c"}
- D：{"id":"h0063","moduleId":"foundation","shape":"plate","size":[0.92,0.25,0.92],"position":[-0.5,-0.04999999999999993,-0.5],"rotation":[0,0,0,1],"color":"#f2bf3c"}

```json
{
  "input": {
    "targetPart": {
      "id": "h0063",
      "moduleId": "battery",
      "shape": "plate",
      "size": [
        0.92,
        0.25,
        0.92
      ],
      "position": [
        -0.5,
        -0.04999999999999993,
        -0.5
      ],
      "rotation": [
        0,
        0,
        0,
        1
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
      "h0035",
      "h0036",
      "h0037",
      "h0038",
      "h0039",
      "h0040",
      "h0041",
      "h0042",
      "h0043",
      "h0044",
      "h0045",
      "h0046",
      "h0047",
      "h0048",
      "h0049",
      "h0050",
      "h0051",
      "h0052",
      "h0053",
      "h0054",
      "h0055",
      "h0056",
      "h0057",
      "h0058",
      "h0059",
      "h0060",
      "h0061",
      "h0062",
      "h0064",
      "h0065",
      "h0066"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 安全拆除（h3-solar-tracker-array-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["foundation","mast","yoke","panel-left","panel-right","battery"]
- B：["battery","panel-left","panel-right"]
- C：["foundation"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "mast-base",
        "name": "mast base",
        "type": "revolute",
        "parent": "foundation",
        "child": "mast",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.175,
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
      },
      {
        "id": "yoke-tilt",
        "name": "yoke tilt",
        "type": "revolute",
        "parent": "mast",
        "child": "yoke",
        "anchorParent": [
          0,
          2.825,
          0
        ],
        "anchorChild": [
          0,
          0.17499999999999982,
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
        "id": "left-panel-hinge",
        "name": "left panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-left",
        "anchorParent": [
          -3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "right-panel-hinge",
        "name": "right panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-right",
        "anchorParent": [
          3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          -1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "battery-lock",
        "name": "battery lock",
        "type": "fixed",
        "parent": "foundation",
        "child": "battery",
        "anchorParent": [
          0,
          0.6000000000000001,
          2
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.5
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
      "mast",
      "yoke",
      "panel-left",
      "panel-right",
      "battery"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 替换选择（h3-solar-tracker-array-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-0
- B：stock-1
- C：stock-2
- D：stock-3

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 3,
        "stiffness": 11,
        "mass": 0.5
      },
      {
        "id": "stock-1",
        "cost": 5,
        "stiffness": 9,
        "mass": 0.6
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 8,
        "mass": 1.6
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 4,
        "mass": 1.6
      }
    ],
    "maxCost": 8
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 平移纠偏（h3-solar-tracker-array-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[2,0,-2]
- B：[0,0,0]
- C：[0,2,0]
- D：[-2,0,2]

```json
{
  "input": {
    "delta": [
      2,
      0,
      -2
    ],
    "target": "battery"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 姿态纠偏（h3-solar-tracker-array-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：-45
- B：45
- C：0
- D：90

```json
{
  "input": {
    "module": "battery",
    "currentYaw": 90,
    "targetYaw": 45
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 下一步放置（h3-solar-tracker-array-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["battery","panel-left","panel-right"]
- B：[]
- C：["foundation","mast","yoke"]
- D：["foundation"]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "mast",
      "yoke"
    ],
    "joints": [
      {
        "id": "mast-base",
        "name": "mast base",
        "type": "revolute",
        "parent": "foundation",
        "child": "mast",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.175,
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
      },
      {
        "id": "yoke-tilt",
        "name": "yoke tilt",
        "type": "revolute",
        "parent": "mast",
        "child": "yoke",
        "anchorParent": [
          0,
          2.825,
          0
        ],
        "anchorChild": [
          0,
          0.17499999999999982,
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
        "id": "left-panel-hinge",
        "name": "left panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-left",
        "anchorParent": [
          -3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "right-panel-hinge",
        "name": "right panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-right",
        "anchorParent": [
          3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          -1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "battery-lock",
        "name": "battery lock",
        "type": "fixed",
        "parent": "foundation",
        "child": "battery",
        "anchorParent": [
          0,
          0.6000000000000001,
          2
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.5
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
      "mast",
      "yoke",
      "panel-left",
      "panel-right",
      "battery"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 库存核算（h3-solar-tracker-array-inventory）

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

### 子装配边界（h3-solar-tracker-array-boundary）

隔离 battery 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["yoke-tilt"]
- B：["battery-lock"]
- C：[]
- D：["mast-base","yoke-tilt","left-panel-hinge","right-panel-hinge","battery-lock"]

```json
{
  "input": {
    "joints": [
      {
        "id": "mast-base",
        "name": "mast base",
        "type": "revolute",
        "parent": "foundation",
        "child": "mast",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.175,
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
      },
      {
        "id": "yoke-tilt",
        "name": "yoke tilt",
        "type": "revolute",
        "parent": "mast",
        "child": "yoke",
        "anchorParent": [
          0,
          2.825,
          0
        ],
        "anchorChild": [
          0,
          0.17499999999999982,
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
        "id": "left-panel-hinge",
        "name": "left panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-left",
        "anchorParent": [
          -3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "right-panel-hinge",
        "name": "right panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-right",
        "anchorParent": [
          3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          -1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "battery-lock",
        "name": "battery lock",
        "type": "fixed",
        "parent": "foundation",
        "child": "battery",
        "anchorParent": [
          0,
          0.6000000000000001,
          2
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "target": "battery"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 最小干预（h3-solar-tracker-array-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：4
- B：0
- C：1
- D：2

```json
{
  "input": {
    "module": "battery"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 全过程依赖（h3-solar-tracker-array-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：1
- B：-1
- C：2
- D：5

```json
{
  "input": {
    "order": [
      "foundation",
      "yoke",
      "mast",
      "panel-left",
      "panel-right",
      "battery"
    ],
    "joints": [
      {
        "id": "mast-base",
        "name": "mast base",
        "type": "revolute",
        "parent": "foundation",
        "child": "mast",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.175,
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
      },
      {
        "id": "yoke-tilt",
        "name": "yoke tilt",
        "type": "revolute",
        "parent": "mast",
        "child": "yoke",
        "anchorParent": [
          0,
          2.825,
          0
        ],
        "anchorChild": [
          0,
          0.17499999999999982,
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
        "id": "left-panel-hinge",
        "name": "left panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-left",
        "anchorParent": [
          -3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "right-panel-hinge",
        "name": "right panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-right",
        "anchorParent": [
          3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          -1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "battery-lock",
        "name": "battery lock",
        "type": "fixed",
        "parent": "foundation",
        "child": "battery",
        "anchorParent": [
          0,
          0.6000000000000001,
          2
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.5
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

### 连续维修路径（h3-solar-tracker-array-access）

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
          10.55,
          0.85,
          2.5
        ],
        "end": [
          0,
          0.85,
          2.5
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
          9.775,
          2.5
        ],
        "end": [
          0,
          0.85,
          2.5
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
          0.85,
          7.46
        ],
        "end": [
          0,
          0.85,
          2.5
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

### 支撑反事实（h3-solar-tracker-array-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["panel-left","panel-right","yoke"]
- B：["mast"]
- C：[]
- D：["foundation","mast","yoke","panel-left","panel-right","battery"]

```json
{
  "input": {
    "removed": "mast",
    "roots": [
      "foundation"
    ],
    "joints": [
      {
        "id": "mast-base",
        "name": "mast base",
        "type": "revolute",
        "parent": "foundation",
        "child": "mast",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.175,
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
      },
      {
        "id": "yoke-tilt",
        "name": "yoke tilt",
        "type": "revolute",
        "parent": "mast",
        "child": "yoke",
        "anchorParent": [
          0,
          2.825,
          0
        ],
        "anchorChild": [
          0,
          0.17499999999999982,
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
        "id": "left-panel-hinge",
        "name": "left panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-left",
        "anchorParent": [
          -3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "right-panel-hinge",
        "name": "right panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-right",
        "anchorParent": [
          3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          -1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "battery-lock",
        "name": "battery lock",
        "type": "fixed",
        "parent": "foundation",
        "child": "battery",
        "anchorParent": [
          0,
          0.6000000000000001,
          2
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.5
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
      "mast",
      "yoke",
      "panel-left",
      "panel-right",
      "battery"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 冲击响应读数（h3-solar-tracker-array-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：1.0126
- C：0.0126
- D：0.2126

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.005162231414707345
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.012595683282121146
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.006658168266459055
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0016026344060284662
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0029983298995557217
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0006982835976116159
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0007546684567202486
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0005605445073073392
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.00002896960980481627
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.00021870045730808778
      },
      {
        "time": 1,
        "displacement": 0.00021870045730808778
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.0000028863737160900154,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-solar-tracker-array-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：0
- B：-1.3
- C：1.3
- D：-0.8

```json
{
  "input": {
    "joint": "yoke-tilt",
    "limits": [
      -0.8,
      0.8
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

### 约束故障诊断（h3-solar-tracker-array-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：right-panel-hinge
- B：left-panel-hinge
- C：mast-base
- D：yoke-tilt

```json
{
  "input": {
    "endpoints": [
      "yoke",
      "panel-left"
    ],
    "type": "revolute",
    "joints": [
      {
        "id": "mast-base",
        "name": "mast base",
        "type": "revolute",
        "parent": "foundation",
        "child": "mast",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.175,
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
      },
      {
        "id": "yoke-tilt",
        "name": "yoke tilt",
        "type": "revolute",
        "parent": "mast",
        "child": "yoke",
        "anchorParent": [
          0,
          2.825,
          0
        ],
        "anchorChild": [
          0,
          0.17499999999999982,
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
        "id": "left-panel-hinge",
        "name": "left panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-left",
        "anchorParent": [
          -3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "right-panel-hinge",
        "name": "right panel hinge",
        "type": "revolute",
        "parent": "yoke",
        "child": "panel-right",
        "anchorParent": [
          3,
          0.17499999999999982,
          0
        ],
        "anchorChild": [
          -1.6,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.3,
          0.3
        ]
      },
      {
        "id": "battery-lock",
        "name": "battery lock",
        "type": "fixed",
        "parent": "foundation",
        "child": "battery",
        "anchorParent": [
          0,
          0.6000000000000001,
          2
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          -0.5
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
      "B"
    ]
  }
}
```

### 主动检查收益（h3-solar-tracker-array-information-gain）

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
    "module": "battery",
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

### 不确定性与弃答（h3-solar-tracker-array-abstention）

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

### 观测后信念更新（h3-solar-tracker-array-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.3333333333333333
- B：0.5
- C：0
- D：0.25

```json
{
  "input": {
    "module": "battery",
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

### 多目标工程权衡（h3-solar-tracker-array-pareto）

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
        "cost": 3,
        "stiffness": 11,
        "mass": 0.5
      },
      {
        "id": "stock-1",
        "cost": 5,
        "stiffness": 9,
        "mass": 0.6
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 8,
        "mass": 1.6
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 4,
        "mass": 1.6
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

### 依赖装配（h3-solar-tracker-array-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:panel-left",
        "label": "安装 panel-left",
        "requires": [
          "present:yoke"
        ],
        "forbids": [
          "present:panel-left"
        ],
        "adds": [
          "present:panel-left"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-left",
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
      },
      {
        "id": "place:yoke",
        "label": "安装 yoke",
        "requires": [
          "present:mast"
        ],
        "forbids": [
          "present:yoke"
        ],
        "adds": [
          "present:yoke"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "yoke",
          "visible": true
        }
      },
      {
        "id": "place:battery",
        "label": "安装 battery",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:battery"
        ],
        "adds": [
          "present:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery",
          "visible": true
        }
      },
      {
        "id": "place:panel-right",
        "label": "安装 panel-right",
        "requires": [
          "present:yoke"
        ],
        "forbids": [
          "present:panel-right"
        ],
        "adds": [
          "present:panel-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right",
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
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:mast",
      "present:yoke",
      "present:panel-left",
      "present:panel-right",
      "present:battery"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:battery",
      "place:mast",
      "place:yoke",
      "place:panel-left",
      "place:panel-right"
    ]
  }
}
```

### 依赖拆解（h3-solar-tracker-array-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:mast",
      "present:yoke",
      "present:panel-left",
      "present:panel-right",
      "present:battery"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "yoke",
      "panel-left",
      "panel-right",
      "battery"
    ],
    "actions": [
      {
        "id": "remove:battery",
        "label": "拆除 battery",
        "requires": [
          "present:battery"
        ],
        "forbids": [],
        "adds": [
          "removed:battery"
        ],
        "deletes": [
          "present:battery"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "battery",
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
          "present:battery"
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
        "id": "remove:yoke",
        "label": "拆除 yoke",
        "requires": [
          "present:yoke"
        ],
        "forbids": [
          "present:panel-left",
          "present:panel-right"
        ],
        "adds": [
          "removed:yoke"
        ],
        "deletes": [
          "present:yoke"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "yoke",
          "visible": false
        }
      },
      {
        "id": "remove:mast",
        "label": "拆除 mast",
        "requires": [
          "present:mast"
        ],
        "forbids": [
          "present:yoke"
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
        "id": "remove:panel-left",
        "label": "拆除 panel-left",
        "requires": [
          "present:panel-left"
        ],
        "forbids": [],
        "adds": [
          "removed:panel-left"
        ],
        "deletes": [
          "present:panel-left"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "panel-left",
          "visible": false
        }
      },
      {
        "id": "remove:panel-right",
        "label": "拆除 panel-right",
        "requires": [
          "present:panel-right"
        ],
        "forbids": [],
        "adds": [
          "removed:panel-right"
        ],
        "deletes": [
          "present:panel-right"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:battery",
      "removed:panel-right",
      "removed:panel-left",
      "removed:yoke",
      "removed:mast",
      "removed:foundation"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:battery",
      "remove:panel-left",
      "remove:panel-right",
      "remove:yoke",
      "remove:mast",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-solar-tracker-array-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:battery",
      "closed:battery"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "yoke",
      "panel-left",
      "panel-right",
      "battery"
    ],
    "actions": [
      {
        "id": "remove:battery",
        "label": "remove battery",
        "requires": [
          "done:open:battery"
        ],
        "forbids": [
          "done:remove:battery"
        ],
        "adds": [
          "done:remove:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery",
          "visible": false
        }
      },
      {
        "id": "support:battery",
        "label": "support battery",
        "requires": [
          "fault:battery"
        ],
        "forbids": [
          "done:support:battery"
        ],
        "adds": [
          "done:support:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "replace:battery",
        "label": "replace battery",
        "requires": [
          "done:remove:battery"
        ],
        "forbids": [
          "done:replace:battery"
        ],
        "adds": [
          "done:replace:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery",
          "visible": true
        }
      },
      {
        "id": "release:battery",
        "label": "release battery",
        "requires": [
          "done:close:battery"
        ],
        "forbids": [
          "done:release:battery"
        ],
        "adds": [
          "done:release:battery",
          "repaired:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "close:battery",
        "label": "close battery",
        "requires": [
          "done:verify:battery"
        ],
        "forbids": [
          "done:close:battery"
        ],
        "adds": [
          "done:close:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "open:battery",
        "label": "open battery",
        "requires": [
          "done:support:battery"
        ],
        "forbids": [
          "done:open:battery"
        ],
        "adds": [
          "done:open:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "verify:battery",
        "label": "verify battery",
        "requires": [
          "done:replace:battery"
        ],
        "forbids": [
          "done:verify:battery"
        ],
        "adds": [
          "done:verify:battery"
        ],
        "deletes": [
          "fault:battery"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      }
    ],
    "goalFacts": [
      "repaired:battery"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:battery",
      "open:battery",
      "remove:battery",
      "replace:battery",
      "verify:battery",
      "close:battery",
      "release:battery"
    ]
  }
}
```

### 复合编辑验证（h3-solar-tracker-array-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:battery",
      "closed:battery"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "yoke",
      "panel-left",
      "panel-right",
      "battery"
    ],
    "actions": [
      {
        "id": "support:battery",
        "label": "support battery",
        "requires": [
          "fault:battery"
        ],
        "forbids": [
          "done:support:battery"
        ],
        "adds": [
          "done:support:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "recolor:battery",
        "label": "recolor battery",
        "requires": [
          "done:open:battery"
        ],
        "forbids": [
          "done:recolor:battery"
        ],
        "adds": [
          "done:recolor:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery",
          "color": "#ea7635"
        }
      },
      {
        "id": "release:battery",
        "label": "release battery",
        "requires": [
          "done:close:battery"
        ],
        "forbids": [
          "done:release:battery"
        ],
        "adds": [
          "done:release:battery",
          "repaired:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "close:battery",
        "label": "close battery",
        "requires": [
          "done:verify:battery"
        ],
        "forbids": [
          "done:close:battery"
        ],
        "adds": [
          "done:close:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "open:battery",
        "label": "open battery",
        "requires": [
          "done:support:battery"
        ],
        "forbids": [
          "done:open:battery"
        ],
        "adds": [
          "done:open:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "verify:battery",
        "label": "verify battery",
        "requires": [
          "done:recolor:battery"
        ],
        "forbids": [
          "done:verify:battery"
        ],
        "adds": [
          "done:verify:battery"
        ],
        "deletes": [
          "fault:battery"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      }
    ],
    "goalFacts": [
      "repaired:battery"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:battery",
      "open:battery",
      "recolor:battery",
      "verify:battery",
      "close:battery",
      "release:battery"
    ]
  }
}
```

### 跨区域联合维修（h3-solar-tracker-array-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:panel-right",
      "closed:panel-right",
      "fault:battery",
      "closed:battery"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "yoke",
      "panel-left",
      "panel-right",
      "battery"
    ],
    "actions": [
      {
        "id": "remove:battery",
        "label": "remove battery",
        "requires": [
          "done:open:battery"
        ],
        "forbids": [
          "done:remove:battery"
        ],
        "adds": [
          "done:remove:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery",
          "visible": false
        }
      },
      {
        "id": "support:battery",
        "label": "support battery",
        "requires": [
          "fault:battery"
        ],
        "forbids": [
          "done:support:battery"
        ],
        "adds": [
          "done:support:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "release:panel-right",
        "label": "release panel-right",
        "requires": [
          "done:close:panel-right"
        ],
        "forbids": [
          "done:release:panel-right"
        ],
        "adds": [
          "done:release:panel-right",
          "repaired:panel-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right"
        }
      },
      {
        "id": "verify:panel-right",
        "label": "verify panel-right",
        "requires": [
          "done:replace:panel-right"
        ],
        "forbids": [
          "done:verify:panel-right"
        ],
        "adds": [
          "done:verify:panel-right"
        ],
        "deletes": [
          "fault:panel-right"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right"
        }
      },
      {
        "id": "replace:battery",
        "label": "replace battery",
        "requires": [
          "done:remove:battery"
        ],
        "forbids": [
          "done:replace:battery"
        ],
        "adds": [
          "done:replace:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery",
          "visible": true
        }
      },
      {
        "id": "close:panel-right",
        "label": "close panel-right",
        "requires": [
          "done:verify:panel-right"
        ],
        "forbids": [
          "done:close:panel-right"
        ],
        "adds": [
          "done:close:panel-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right"
        }
      },
      {
        "id": "support:panel-right",
        "label": "support panel-right",
        "requires": [
          "fault:panel-right"
        ],
        "forbids": [
          "done:support:panel-right"
        ],
        "adds": [
          "done:support:panel-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right"
        }
      },
      {
        "id": "open:panel-right",
        "label": "open panel-right",
        "requires": [
          "done:support:panel-right"
        ],
        "forbids": [
          "done:open:panel-right"
        ],
        "adds": [
          "done:open:panel-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right"
        }
      },
      {
        "id": "replace:panel-right",
        "label": "replace panel-right",
        "requires": [
          "done:remove:panel-right"
        ],
        "forbids": [
          "done:replace:panel-right"
        ],
        "adds": [
          "done:replace:panel-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right",
          "visible": true
        }
      },
      {
        "id": "remove:panel-right",
        "label": "remove panel-right",
        "requires": [
          "done:open:panel-right"
        ],
        "forbids": [
          "done:remove:panel-right"
        ],
        "adds": [
          "done:remove:panel-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right",
          "visible": false
        }
      },
      {
        "id": "release:battery",
        "label": "release battery",
        "requires": [
          "done:close:battery"
        ],
        "forbids": [
          "done:release:battery"
        ],
        "adds": [
          "done:release:battery",
          "repaired:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "close:battery",
        "label": "close battery",
        "requires": [
          "done:verify:battery"
        ],
        "forbids": [
          "done:close:battery"
        ],
        "adds": [
          "done:close:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "open:battery",
        "label": "open battery",
        "requires": [
          "done:support:battery"
        ],
        "forbids": [
          "done:open:battery"
        ],
        "adds": [
          "done:open:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "verify:battery",
        "label": "verify battery",
        "requires": [
          "done:replace:battery"
        ],
        "forbids": [
          "done:verify:battery"
        ],
        "adds": [
          "done:verify:battery"
        ],
        "deletes": [
          "fault:battery"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      }
    ],
    "goalFacts": [
      "repaired:panel-right",
      "repaired:battery"
    ],
    "budget": 14,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:battery",
      "support:panel-right",
      "open:panel-right",
      "remove:panel-right",
      "replace:panel-right",
      "verify:panel-right",
      "close:panel-right",
      "release:panel-right",
      "open:battery",
      "remove:battery",
      "replace:battery",
      "verify:battery",
      "close:battery",
      "release:battery"
    ]
  }
}
```

### 多工位资源调度（h3-solar-tracker-array-scheduling）

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
        "module": "yoke",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "panel-left",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "panel-right",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "battery",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      }
    ],
    "deadline": 7
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 3,
      "job-4": 4,
      "job-5": 4
    }
  }
}
```

### 检查后条件策略（h3-solar-tracker-array-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "battery",
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

### 局部坐标变换（h3-solar-tracker-array-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[0.5,1.8,4]
- B：[-0.5,0.8,3]
- C：[0.5,-0.05,-0.5]
- D：[0.5,0.8,2]

```json
{
  "input": {
    "localPoint": [
      0.5,
      -0.04999999999999993,
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
      0.85,
      2.5
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 正交视图投影（h3-solar-tracker-array-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[0,0]
- B：[3,-4]
- C：[7,3]
- D：[3,4]

```json
{
  "input": {
    "view": "top",
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

### 空间相对关系（h3-solar-tracker-array-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：greater
- B：less
- C：equal

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
      "id": "battery",
      "position": [
        0,
        0.85,
        2.5
      ]
    },
    "axis": "z"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 约束自由度（h3-solar-tracker-array-joint-axis）

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
      "id": "yoke-tilt",
      "name": "yoke tilt",
      "type": "revolute",
      "parent": "mast",
      "child": "yoke",
      "anchorParent": [
        0,
        2.825,
        0
      ],
      "anchorChild": [
        0,
        0.17499999999999982,
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

### 维修间隙预算（h3-solar-tracker-array-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "battery",
    "aperture": 0.6,
    "toolWidth": 0.45,
    "eachSideMargin": 0.1
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-solar-tracker-array-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,6]
- B：[0,0,0]
- C：[0,-2,0]
- D：[0,0,-6]

```json
{
  "input": {
    "module": "battery",
    "lever": [
      2,
      3,
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
    "choiceId": "D"
  }
}
```

### 非均匀先验更新（h3-solar-tracker-array-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：1
- B：0.6
- C：0.375
- D：0

```json
{
  "input": {
    "module": "battery",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      2,
      3,
      3
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

### 风险最小决策（h3-solar-tracker-array-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.3,
    "repairCost": 5,
    "failureLoss": 10,
    "module": "battery"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-solar-tracker-array-trace-threshold）

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
        "displacement": 0.005162231414707345
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.012595683282121146
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.006658168266459055
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0016026344060284662
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0029983298995557217
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0006982835976116159
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0007546684567202486
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0005605445073073392
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.00002896960980481627
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.00021870045730808778
      },
      {
        "time": 1,
        "displacement": 0.00021870045730808778
      }
    ],
    "threshold": 0.010076546625696917
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-solar-tracker-array-guarded-repair）

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
        "id": "release:battery",
        "label": "release battery",
        "requires": [
          "done:relock:battery"
        ],
        "forbids": [
          "done:release:battery"
        ],
        "adds": [
          "done:release:battery",
          "ready:battery",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "relock:battery",
        "label": "relock battery",
        "requires": [
          "done:verify:battery"
        ],
        "forbids": [
          "done:relock:battery"
        ],
        "adds": [
          "done:relock:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "verify:battery",
        "label": "verify battery",
        "requires": [
          "done:replace:battery"
        ],
        "forbids": [
          "done:verify:battery"
        ],
        "adds": [
          "done:verify:battery"
        ],
        "deletes": [
          "fault:battery",
          "misaligned:battery"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "replace:battery",
        "label": "replace battery",
        "requires": [
          "done:unlock:battery"
        ],
        "forbids": [
          "done:replace:battery"
        ],
        "adds": [
          "done:replace:battery"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "unlock:battery",
        "label": "unlock battery",
        "requires": [
          "done:support:battery"
        ],
        "forbids": [
          "done:unlock:battery"
        ],
        "adds": [
          "done:unlock:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "support:battery",
        "label": "support battery",
        "requires": [
          "done:isolate:battery"
        ],
        "forbids": [
          "done:support:battery"
        ],
        "adds": [
          "done:support:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "isolate:battery",
        "label": "isolate battery",
        "requires": [
          "tool:free",
          "fault:battery"
        ],
        "forbids": [
          "done:isolate:battery"
        ],
        "adds": [
          "done:isolate:battery"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:battery"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "yoke",
      "panel-left",
      "panel-right",
      "battery"
    ],
    "goalFacts": [
      "ready:battery"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:battery",
      "support:battery",
      "unlock:battery",
      "replace:battery",
      "verify:battery",
      "relock:battery",
      "release:battery"
    ]
  }
}
```

### 失败状态回退（h3-solar-tracker-array-rollback）

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
        "id": "resume:battery",
        "label": "resume battery",
        "requires": [
          "done:verify:battery"
        ],
        "forbids": [
          "done:resume:battery"
        ],
        "adds": [
          "done:resume:battery",
          "ready:battery",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "verify:battery",
        "label": "verify battery",
        "requires": [
          "done:align:battery"
        ],
        "forbids": [
          "done:verify:battery"
        ],
        "adds": [
          "done:verify:battery"
        ],
        "deletes": [
          "fault:battery",
          "misaligned:battery"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "align:battery",
        "label": "align battery",
        "requires": [
          "done:undo:battery"
        ],
        "forbids": [
          "done:align:battery"
        ],
        "adds": [
          "done:align:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery",
          "visible": true
        }
      },
      {
        "id": "undo:battery",
        "label": "undo battery",
        "requires": [
          "done:isolate:battery"
        ],
        "forbids": [
          "done:undo:battery"
        ],
        "adds": [
          "done:undo:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery",
          "visible": false
        }
      },
      {
        "id": "isolate:battery",
        "label": "isolate battery",
        "requires": [
          "tool:free",
          "fault:battery"
        ],
        "forbids": [
          "done:isolate:battery"
        ],
        "adds": [
          "done:isolate:battery"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:battery",
      "misaligned:battery"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "yoke",
      "panel-left",
      "panel-right",
      "battery"
    ],
    "goalFacts": [
      "ready:battery"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:battery",
      "undo:battery",
      "align:battery",
      "verify:battery",
      "resume:battery"
    ]
  }
}
```

### 共享工具协同维修（h3-solar-tracker-array-resource-repair）

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
        "id": "release:battery",
        "label": "release battery",
        "requires": [
          "done:relock:battery"
        ],
        "forbids": [
          "done:release:battery"
        ],
        "adds": [
          "done:release:battery",
          "ready:battery",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "relock:battery",
        "label": "relock battery",
        "requires": [
          "done:verify:battery"
        ],
        "forbids": [
          "done:relock:battery"
        ],
        "adds": [
          "done:relock:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "verify:battery",
        "label": "verify battery",
        "requires": [
          "done:replace:battery"
        ],
        "forbids": [
          "done:verify:battery"
        ],
        "adds": [
          "done:verify:battery"
        ],
        "deletes": [
          "fault:battery",
          "misaligned:battery"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "replace:battery",
        "label": "replace battery",
        "requires": [
          "done:unlock:battery"
        ],
        "forbids": [
          "done:replace:battery"
        ],
        "adds": [
          "done:replace:battery"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "unlock:battery",
        "label": "unlock battery",
        "requires": [
          "done:support:battery"
        ],
        "forbids": [
          "done:unlock:battery"
        ],
        "adds": [
          "done:unlock:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "support:battery",
        "label": "support battery",
        "requires": [
          "done:isolate:battery"
        ],
        "forbids": [
          "done:support:battery"
        ],
        "adds": [
          "done:support:battery"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "isolate:battery",
        "label": "isolate battery",
        "requires": [
          "tool:free",
          "fault:battery"
        ],
        "forbids": [
          "done:isolate:battery"
        ],
        "adds": [
          "done:isolate:battery"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "battery"
        }
      },
      {
        "id": "release:panel-right",
        "label": "release panel-right",
        "requires": [
          "done:relock:panel-right"
        ],
        "forbids": [
          "done:release:panel-right"
        ],
        "adds": [
          "done:release:panel-right",
          "ready:panel-right",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right"
        }
      },
      {
        "id": "relock:panel-right",
        "label": "relock panel-right",
        "requires": [
          "done:verify:panel-right"
        ],
        "forbids": [
          "done:relock:panel-right"
        ],
        "adds": [
          "done:relock:panel-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right"
        }
      },
      {
        "id": "verify:panel-right",
        "label": "verify panel-right",
        "requires": [
          "done:replace:panel-right"
        ],
        "forbids": [
          "done:verify:panel-right"
        ],
        "adds": [
          "done:verify:panel-right"
        ],
        "deletes": [
          "fault:panel-right",
          "misaligned:panel-right"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right"
        }
      },
      {
        "id": "replace:panel-right",
        "label": "replace panel-right",
        "requires": [
          "done:unlock:panel-right"
        ],
        "forbids": [
          "done:replace:panel-right"
        ],
        "adds": [
          "done:replace:panel-right"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "panel-right"
        }
      },
      {
        "id": "unlock:panel-right",
        "label": "unlock panel-right",
        "requires": [
          "done:support:panel-right"
        ],
        "forbids": [
          "done:unlock:panel-right"
        ],
        "adds": [
          "done:unlock:panel-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right"
        }
      },
      {
        "id": "support:panel-right",
        "label": "support panel-right",
        "requires": [
          "done:isolate:panel-right"
        ],
        "forbids": [
          "done:support:panel-right"
        ],
        "adds": [
          "done:support:panel-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right"
        }
      },
      {
        "id": "isolate:panel-right",
        "label": "isolate panel-right",
        "requires": [
          "tool:free",
          "fault:panel-right"
        ],
        "forbids": [
          "done:isolate:panel-right"
        ],
        "adds": [
          "done:isolate:panel-right"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "panel-right"
        }
      },
      {
        "id": "release:panel-left",
        "label": "release panel-left",
        "requires": [
          "done:relock:panel-left"
        ],
        "forbids": [
          "done:release:panel-left"
        ],
        "adds": [
          "done:release:panel-left",
          "ready:panel-left",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-left"
        }
      },
      {
        "id": "relock:panel-left",
        "label": "relock panel-left",
        "requires": [
          "done:verify:panel-left"
        ],
        "forbids": [
          "done:relock:panel-left"
        ],
        "adds": [
          "done:relock:panel-left"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-left"
        }
      },
      {
        "id": "verify:panel-left",
        "label": "verify panel-left",
        "requires": [
          "done:replace:panel-left"
        ],
        "forbids": [
          "done:verify:panel-left"
        ],
        "adds": [
          "done:verify:panel-left"
        ],
        "deletes": [
          "fault:panel-left",
          "misaligned:panel-left"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "panel-left"
        }
      },
      {
        "id": "replace:panel-left",
        "label": "replace panel-left",
        "requires": [
          "done:unlock:panel-left"
        ],
        "forbids": [
          "done:replace:panel-left"
        ],
        "adds": [
          "done:replace:panel-left"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "panel-left"
        }
      },
      {
        "id": "unlock:panel-left",
        "label": "unlock panel-left",
        "requires": [
          "done:support:panel-left"
        ],
        "forbids": [
          "done:unlock:panel-left"
        ],
        "adds": [
          "done:unlock:panel-left"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-left"
        }
      },
      {
        "id": "support:panel-left",
        "label": "support panel-left",
        "requires": [
          "done:isolate:panel-left"
        ],
        "forbids": [
          "done:support:panel-left"
        ],
        "adds": [
          "done:support:panel-left"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "panel-left"
        }
      },
      {
        "id": "isolate:panel-left",
        "label": "isolate panel-left",
        "requires": [
          "tool:free",
          "fault:panel-left"
        ],
        "forbids": [
          "done:isolate:panel-left"
        ],
        "adds": [
          "done:isolate:panel-left"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "panel-left"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:panel-left",
      "fault:panel-right",
      "fault:battery"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "yoke",
      "panel-left",
      "panel-right",
      "battery"
    ],
    "goalFacts": [
      "ready:panel-left",
      "ready:panel-right",
      "ready:battery"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 24
  },
  "answer": {
    "actionIds": [
      "isolate:battery",
      "support:battery",
      "unlock:battery",
      "replace:battery",
      "verify:battery",
      "relock:battery",
      "release:battery",
      "isolate:panel-right",
      "support:panel-right",
      "unlock:panel-right",
      "replace:panel-right",
      "verify:panel-right",
      "relock:panel-right",
      "release:panel-right",
      "isolate:panel-left",
      "support:panel-left",
      "unlock:panel-left",
      "replace:panel-left",
      "verify:panel-left",
      "relock:panel-left",
      "release:panel-left"
    ]
  }
}
```

### 预算约束检查策略（h3-solar-tracker-array-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "battery",
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
