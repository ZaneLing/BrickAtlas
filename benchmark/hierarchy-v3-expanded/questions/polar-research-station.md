## D3 极地科研站

### 模块识别（h3-polar-research-station-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：wind-mast
- B：wind-rotor
- C：airlock-door
- D：station-base

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "station-base",
        "name": "Elevated polar station base"
      },
      {
        "id": "airlock-door",
        "name": "Pressure airlock door"
      },
      {
        "id": "wind-mast",
        "name": "Wind turbine mast"
      },
      {
        "id": "wind-rotor",
        "name": "Three-blade wind rotor"
      },
      {
        "id": "solar-carriage",
        "name": "Sliding solar service carriage"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 部件计数（h3-polar-research-station-count）

模块 airlock-door 有多少个可视零件？

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
        "id": "v0001",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0002",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0003",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0004",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0005",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0006",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0007",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0008",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0009",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0010",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0011",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0012",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0013",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0014",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0015",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0016",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0017",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0018",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0019",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0020",
        "moduleId": "station-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0021",
        "moduleId": "station-base",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0022",
        "moduleId": "station-base",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0023",
        "moduleId": "station-base",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0024",
        "moduleId": "station-base",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0025",
        "moduleId": "station-base",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0026",
        "moduleId": "station-base",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0027",
        "moduleId": "station-base",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0028",
        "moduleId": "station-base",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0029",
        "moduleId": "station-base",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0030",
        "moduleId": "station-base",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0031",
        "moduleId": "station-base",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0032",
        "moduleId": "station-base",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0033",
        "moduleId": "station-base",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0034",
        "moduleId": "station-base",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0035",
        "moduleId": "station-base",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0036",
        "moduleId": "station-base",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0037",
        "moduleId": "station-base",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0038",
        "moduleId": "station-base",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0039",
        "moduleId": "station-base",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0040",
        "moduleId": "station-base",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0041",
        "moduleId": "station-base",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0042",
        "moduleId": "station-base",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0043",
        "moduleId": "station-base",
        "shape": "slope",
        "color": "#e8792e"
      },
      {
        "id": "v0044",
        "moduleId": "station-base",
        "shape": "slope",
        "color": "#e8792e"
      },
      {
        "id": "v0045",
        "moduleId": "station-base",
        "shape": "slope",
        "color": "#e8792e"
      },
      {
        "id": "v0046",
        "moduleId": "station-base",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0047",
        "moduleId": "station-base",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0048",
        "moduleId": "station-base",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0049",
        "moduleId": "airlock-door",
        "shape": "panel",
        "color": "#e8792e"
      },
      {
        "id": "v0050",
        "moduleId": "airlock-door",
        "shape": "wheel",
        "color": "#26323b"
      },
      {
        "id": "v0051",
        "moduleId": "wind-mast",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "v0052",
        "moduleId": "wind-mast",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "v0053",
        "moduleId": "wind-mast",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "v0054",
        "moduleId": "wind-mast",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "v0055",
        "moduleId": "wind-mast",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "v0056",
        "moduleId": "wind-mast",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "v0057",
        "moduleId": "wind-mast",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "v0058",
        "moduleId": "wind-mast",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0059",
        "moduleId": "wind-rotor",
        "shape": "gear",
        "color": "#f2bf3c"
      },
      {
        "id": "v0060",
        "moduleId": "wind-rotor",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "v0061",
        "moduleId": "wind-rotor",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "v0062",
        "moduleId": "wind-rotor",
        "shape": "beam",
        "color": "#edf1f2"
      },
      {
        "id": "v0063",
        "moduleId": "solar-carriage",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "v0064",
        "moduleId": "solar-carriage",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "v0065",
        "moduleId": "solar-carriage",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "v0066",
        "moduleId": "solar-carriage",
        "shape": "panel",
        "color": "#173b63"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-polar-research-station-color）

零件 v0049 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#d43a32
- B：#f2bf3c
- C：#e8792e
- D：#2878b8

```json
{
  "input": {
    "part": {
      "id": "v0049",
      "moduleId": "airlock-door",
      "shape": "panel",
      "size": [
        0.35,
        2.1,
        2.1
      ],
      "position": [
        0.10000000000000006,
        0,
        0
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
    "choiceId": "C"
  }
}
```

### 三维位置（h3-polar-research-station-position）

模块 airlock-door 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[5.3,8.53007214207425,1.8000000000000003]
- B：[-5.299999999999999,2.2,0.30000000000000004]
- C：[0,1.6468114941533938,0]
- D：[5.3,4.3950000000000005,1.8]

```json
{
  "input": {
    "centers": {
      "station-base": [
        0,
        1.6468114941533938,
        0
      ],
      "airlock-door": [
        -5.299999999999999,
        2.2,
        0.30000000000000004
      ],
      "wind-mast": [
        5.3,
        4.3950000000000005,
        1.8
      ],
      "wind-rotor": [
        5.3,
        8.53007214207425,
        1.8000000000000003
      ],
      "solar-carriage": [
        0,
        4.1,
        4.8
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节类型（h3-polar-research-station-joint-type）

solar-rail 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：revolute
- B：spring
- C：prismatic
- D：fixed

```json
{
  "input": {
    "joint": {
      "id": "solar-rail",
      "name": "Solar carriage rail",
      "type": "prismatic",
      "parent": "station-base",
      "child": "solar-carriage",
      "anchorParent": [
        0,
        2.4531885058466063,
        4.8
      ],
      "anchorChild": [
        0,
        0,
        0
      ],
      "axis": [
        1,
        0,
        0
      ],
      "limits": [
        -2,
        2
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 直接连接（h3-polar-research-station-parent）

airlock-door 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["station-base","airlock-door","wind-mast","wind-rotor","solar-carriage"]
- B：["station-base"]
- C：["airlock-door"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "airlock-hinge",
        "name": "Airlock hinge",
        "type": "revolute",
        "parent": "station-base",
        "child": "airlock-door",
        "anchorParent": [
          -5.199999999999999,
          0.5531885058466064,
          -0.7
        ],
        "anchorChild": [
          0.10000000000000006,
          0,
          -1
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.7
        ]
      },
      {
        "id": "mast-foot",
        "name": "Turbine mast foot",
        "type": "fixed",
        "parent": "station-base",
        "child": "wind-mast",
        "anchorParent": [
          5.3,
          -0.3468114941533936,
          1.8
        ],
        "anchorChild": [
          0,
          -3.095,
          0
        ]
      },
      {
        "id": "rotor-shaft",
        "name": "Wind rotor shaft",
        "type": "revolute",
        "parent": "wind-mast",
        "child": "wind-rotor",
        "anchorParent": [
          0,
          3.7050000000000005,
          0
        ],
        "anchorChild": [
          -2.220446049250313e-16,
          -0.43007214207425015,
          0
        ],
        "axis": [
          0,
          0,
          1
        ]
      },
      {
        "id": "solar-rail",
        "name": "Solar carriage rail",
        "type": "prismatic",
        "parent": "station-base",
        "child": "solar-carriage",
        "anchorParent": [
          0,
          2.4531885058466063,
          4.8
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -2,
          2
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 基座识别（h3-polar-research-station-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["station-base","airlock-door","wind-mast","wind-rotor","solar-carriage"]
- B：["airlock-door"]
- C：["station-base"]
- D：[]

```json
{
  "input": {
    "modules": [
      {
        "id": "station-base",
        "name": "Elevated polar station base",
        "role": "foundation",
        "anchored": true,
        "mass": 20,
        "position": [
          0,
          1.6468114941533936,
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
        "id": "airlock-door",
        "name": "Pressure airlock door",
        "role": "service-module",
        "anchored": false,
        "mass": 2,
        "position": [
          -5.299999999999999,
          2.2,
          0.3
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "wind-mast",
        "name": "Wind turbine mast",
        "role": "energy-system",
        "anchored": false,
        "mass": 4,
        "position": [
          5.3,
          4.3950000000000005,
          1.8
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "wind-rotor",
        "name": "Three-blade wind rotor",
        "role": "rotor",
        "anchored": false,
        "mass": 1.8,
        "position": [
          5.3,
          8.53007214207425,
          1.8
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "solar-carriage",
        "name": "Sliding solar service carriage",
        "role": "actuator",
        "anchored": false,
        "mass": 3,
        "position": [
          0,
          4.1,
          4.8
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

### 接口计数（h3-polar-research-station-degree）

airlock-door 连接几个声明关节？平行关节分别计数。

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
        "id": "airlock-hinge",
        "name": "Airlock hinge",
        "type": "revolute",
        "parent": "station-base",
        "child": "airlock-door",
        "anchorParent": [
          -5.199999999999999,
          0.5531885058466064,
          -0.7
        ],
        "anchorChild": [
          0.10000000000000006,
          0,
          -1
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.7
        ]
      },
      {
        "id": "mast-foot",
        "name": "Turbine mast foot",
        "type": "fixed",
        "parent": "station-base",
        "child": "wind-mast",
        "anchorParent": [
          5.3,
          -0.3468114941533936,
          1.8
        ],
        "anchorChild": [
          0,
          -3.095,
          0
        ]
      },
      {
        "id": "rotor-shaft",
        "name": "Wind rotor shaft",
        "type": "revolute",
        "parent": "wind-mast",
        "child": "wind-rotor",
        "anchorParent": [
          0,
          3.7050000000000005,
          0
        ],
        "anchorChild": [
          -2.220446049250313e-16,
          -0.43007214207425015,
          0
        ],
        "axis": [
          0,
          0,
          1
        ]
      },
      {
        "id": "solar-rail",
        "name": "Solar carriage rail",
        "type": "prismatic",
        "parent": "station-base",
        "child": "solar-carriage",
        "anchorParent": [
          0,
          2.4531885058466063,
          4.8
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -2,
          2
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 局部改色（h3-polar-research-station-recolor）

仅将 v0049 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"*","color":"#e8792e"}
- B：{"id":"v0049","color":"#e8792e"}
- C：{"id":"v0050","color":"#e8792e"}
- D：{"id":"v0049","color":"#2878b8"}

```json
{
  "input": {
    "part": {
      "id": "v0049",
      "moduleId": "airlock-door",
      "shape": "panel",
      "size": [
        0.35,
        2.1,
        2.1
      ],
      "position": [
        0.10000000000000006,
        0,
        0
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
    "choiceId": "B"
  }
}
```

### 补装部件（h3-polar-research-station-add）

模块 airlock-door 缺失零件 v0049。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"v0049","moduleId":"airlock-door","shape":"panel","size":[0.35,2.1,2.1],"position":[0.10000000000000006,0,0],"rotation":[0,0,0,1],"color":"#000000"}
- B：{"id":"v0049","moduleId":"airlock-door","shape":"panel","size":[0.35,2.1,2.1],"position":[0.10000000000000006,0,0],"rotation":[0,0,0,1],"color":"#e8792e"}
- C：{"id":"v0049","moduleId":"station-base","shape":"panel","size":[0.35,2.1,2.1],"position":[0.10000000000000006,0,0],"rotation":[0,0,0,1],"color":"#e8792e"}
- D：{"id":"v0049","moduleId":"airlock-door","shape":"panel","size":[3,3,3],"position":[0.10000000000000006,0,0],"rotation":[0,0,0,1],"color":"#e8792e"}

```json
{
  "input": {
    "targetPart": {
      "id": "v0049",
      "moduleId": "airlock-door",
      "shape": "panel",
      "size": [
        0.35,
        2.1,
        2.1
      ],
      "position": [
        0.10000000000000006,
        0,
        0
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
      "v0001",
      "v0002",
      "v0003",
      "v0004",
      "v0005",
      "v0006",
      "v0007",
      "v0008",
      "v0009",
      "v0010",
      "v0011",
      "v0012",
      "v0013",
      "v0014",
      "v0015",
      "v0016",
      "v0017",
      "v0018",
      "v0019",
      "v0020",
      "v0021",
      "v0022",
      "v0023",
      "v0024",
      "v0025",
      "v0026",
      "v0027",
      "v0028",
      "v0029",
      "v0030",
      "v0031",
      "v0032",
      "v0033",
      "v0034",
      "v0035",
      "v0036",
      "v0037",
      "v0038",
      "v0039",
      "v0040",
      "v0041",
      "v0042",
      "v0043",
      "v0044",
      "v0045",
      "v0046",
      "v0047",
      "v0048",
      "v0050",
      "v0051",
      "v0052",
      "v0053",
      "v0054",
      "v0055",
      "v0056",
      "v0057",
      "v0058",
      "v0059",
      "v0060",
      "v0061",
      "v0062",
      "v0063",
      "v0064",
      "v0065",
      "v0066"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全拆除（h3-polar-research-station-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["station-base"]
- B：[]
- C：["station-base","airlock-door","wind-mast","wind-rotor","solar-carriage"]
- D：["airlock-door","solar-carriage","wind-rotor"]

```json
{
  "input": {
    "joints": [
      {
        "id": "airlock-hinge",
        "name": "Airlock hinge",
        "type": "revolute",
        "parent": "station-base",
        "child": "airlock-door",
        "anchorParent": [
          -5.199999999999999,
          0.5531885058466064,
          -0.7
        ],
        "anchorChild": [
          0.10000000000000006,
          0,
          -1
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.7
        ]
      },
      {
        "id": "mast-foot",
        "name": "Turbine mast foot",
        "type": "fixed",
        "parent": "station-base",
        "child": "wind-mast",
        "anchorParent": [
          5.3,
          -0.3468114941533936,
          1.8
        ],
        "anchorChild": [
          0,
          -3.095,
          0
        ]
      },
      {
        "id": "rotor-shaft",
        "name": "Wind rotor shaft",
        "type": "revolute",
        "parent": "wind-mast",
        "child": "wind-rotor",
        "anchorParent": [
          0,
          3.7050000000000005,
          0
        ],
        "anchorChild": [
          -2.220446049250313e-16,
          -0.43007214207425015,
          0
        ],
        "axis": [
          0,
          0,
          1
        ]
      },
      {
        "id": "solar-rail",
        "name": "Solar carriage rail",
        "type": "prismatic",
        "parent": "station-base",
        "child": "solar-carriage",
        "anchorParent": [
          0,
          2.4531885058466063,
          4.8
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -2,
          2
        ]
      }
    ],
    "modules": [
      "station-base",
      "airlock-door",
      "wind-mast",
      "wind-rotor",
      "solar-carriage"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 替换选择（h3-polar-research-station-replace）

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
        "cost": 7,
        "stiffness": 4,
        "mass": 0.5
      },
      {
        "id": "stock-1",
        "cost": 3,
        "stiffness": 4,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 5,
        "stiffness": 3,
        "mass": 1.2
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 11,
        "mass": 1.4
      }
    ],
    "maxCost": 8
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 平移纠偏（h3-polar-research-station-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,2,0]
- C：[-3,0,2]
- D：[3,0,-2]

```json
{
  "input": {
    "delta": [
      3,
      0,
      -2
    ],
    "target": "airlock-door"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-polar-research-station-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：-45
- B：45
- C：0
- D：90

```json
{
  "input": {
    "module": "airlock-door",
    "currentYaw": 315,
    "targetYaw": 270
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 下一步放置（h3-polar-research-station-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：[]
- B：["station-base","wind-mast","solar-carriage"]
- C：["station-base"]
- D：["airlock-door","wind-rotor"]

```json
{
  "input": {
    "prefix": [
      "station-base",
      "wind-mast",
      "solar-carriage"
    ],
    "joints": [
      {
        "id": "airlock-hinge",
        "name": "Airlock hinge",
        "type": "revolute",
        "parent": "station-base",
        "child": "airlock-door",
        "anchorParent": [
          -5.199999999999999,
          0.5531885058466064,
          -0.7
        ],
        "anchorChild": [
          0.10000000000000006,
          0,
          -1
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.7
        ]
      },
      {
        "id": "mast-foot",
        "name": "Turbine mast foot",
        "type": "fixed",
        "parent": "station-base",
        "child": "wind-mast",
        "anchorParent": [
          5.3,
          -0.3468114941533936,
          1.8
        ],
        "anchorChild": [
          0,
          -3.095,
          0
        ]
      },
      {
        "id": "rotor-shaft",
        "name": "Wind rotor shaft",
        "type": "revolute",
        "parent": "wind-mast",
        "child": "wind-rotor",
        "anchorParent": [
          0,
          3.7050000000000005,
          0
        ],
        "anchorChild": [
          -2.220446049250313e-16,
          -0.43007214207425015,
          0
        ],
        "axis": [
          0,
          0,
          1
        ]
      },
      {
        "id": "solar-rail",
        "name": "Solar carriage rail",
        "type": "prismatic",
        "parent": "station-base",
        "child": "solar-carriage",
        "anchorParent": [
          0,
          2.4531885058466063,
          4.8
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -2,
          2
        ]
      }
    ],
    "modules": [
      "station-base",
      "airlock-door",
      "wind-mast",
      "wind-rotor",
      "solar-carriage"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 库存核算（h3-polar-research-station-inventory）

备件库有 7 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：5
- B：6
- C：4
- D：8

```json
{
  "input": {
    "available": 7,
    "required": 2
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 子装配边界（h3-polar-research-station-boundary）

隔离 airlock-door 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["airlock-hinge","mast-foot","rotor-shaft","solar-rail"]
- B：["solar-rail"]
- C：["airlock-hinge"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "airlock-hinge",
        "name": "Airlock hinge",
        "type": "revolute",
        "parent": "station-base",
        "child": "airlock-door",
        "anchorParent": [
          -5.199999999999999,
          0.5531885058466064,
          -0.7
        ],
        "anchorChild": [
          0.10000000000000006,
          0,
          -1
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.7
        ]
      },
      {
        "id": "mast-foot",
        "name": "Turbine mast foot",
        "type": "fixed",
        "parent": "station-base",
        "child": "wind-mast",
        "anchorParent": [
          5.3,
          -0.3468114941533936,
          1.8
        ],
        "anchorChild": [
          0,
          -3.095,
          0
        ]
      },
      {
        "id": "rotor-shaft",
        "name": "Wind rotor shaft",
        "type": "revolute",
        "parent": "wind-mast",
        "child": "wind-rotor",
        "anchorParent": [
          0,
          3.7050000000000005,
          0
        ],
        "anchorChild": [
          -2.220446049250313e-16,
          -0.43007214207425015,
          0
        ],
        "axis": [
          0,
          0,
          1
        ]
      },
      {
        "id": "solar-rail",
        "name": "Solar carriage rail",
        "type": "prismatic",
        "parent": "station-base",
        "child": "solar-carriage",
        "anchorParent": [
          0,
          2.4531885058466063,
          4.8
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -2,
          2
        ]
      }
    ],
    "target": "airlock-door"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 最小干预（h3-polar-research-station-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：0

```json
{
  "input": {
    "module": "airlock-door"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 全过程依赖（h3-polar-research-station-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：-1
- B：1
- C：4
- D：0

```json
{
  "input": {
    "order": [
      "airlock-door",
      "station-base",
      "wind-mast",
      "solar-carriage",
      "wind-rotor"
    ],
    "joints": [
      {
        "id": "airlock-hinge",
        "name": "Airlock hinge",
        "type": "revolute",
        "parent": "station-base",
        "child": "airlock-door",
        "anchorParent": [
          -5.199999999999999,
          0.5531885058466064,
          -0.7
        ],
        "anchorChild": [
          0.10000000000000006,
          0,
          -1
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.7
        ]
      },
      {
        "id": "mast-foot",
        "name": "Turbine mast foot",
        "type": "fixed",
        "parent": "station-base",
        "child": "wind-mast",
        "anchorParent": [
          5.3,
          -0.3468114941533936,
          1.8
        ],
        "anchorChild": [
          0,
          -3.095,
          0
        ]
      },
      {
        "id": "rotor-shaft",
        "name": "Wind rotor shaft",
        "type": "revolute",
        "parent": "wind-mast",
        "child": "wind-rotor",
        "anchorParent": [
          0,
          3.7050000000000005,
          0
        ],
        "anchorChild": [
          -2.220446049250313e-16,
          -0.43007214207425015,
          0
        ],
        "axis": [
          0,
          0,
          1
        ]
      },
      {
        "id": "solar-rail",
        "name": "Solar carriage rail",
        "type": "prismatic",
        "parent": "station-base",
        "child": "solar-carriage",
        "anchorParent": [
          0,
          2.4531885058466063,
          4.8
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -2,
          2
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 连续维修路径（h3-polar-research-station-access）

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
          11.239813601985166,
          2.2,
          0.30000000000000004
        ],
        "end": [
          -5.299999999999999,
          2.2,
          0.30000000000000004
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.44648706912994385
      },
      {
        "id": "path-1",
        "start": [
          -5.299999999999999,
          14.209999999999999,
          0.30000000000000004
        ],
        "end": [
          -5.299999999999999,
          2.2,
          0.30000000000000004
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
          -5.299999999999999,
          2.2,
          10.393988775295556
        ],
        "end": [
          -5.299999999999999,
          2.2,
          0.30000000000000004
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
      "B",
      "C"
    ]
  }
}
```

### 支撑反事实（h3-polar-research-station-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["station-base","airlock-door","wind-mast","wind-rotor","solar-carriage"]
- C：["wind-rotor"]
- D：["wind-mast"]

```json
{
  "input": {
    "removed": "wind-mast",
    "roots": [
      "station-base"
    ],
    "joints": [
      {
        "id": "airlock-hinge",
        "name": "Airlock hinge",
        "type": "revolute",
        "parent": "station-base",
        "child": "airlock-door",
        "anchorParent": [
          -5.199999999999999,
          0.5531885058466064,
          -0.7
        ],
        "anchorChild": [
          0.10000000000000006,
          0,
          -1
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.7
        ]
      },
      {
        "id": "mast-foot",
        "name": "Turbine mast foot",
        "type": "fixed",
        "parent": "station-base",
        "child": "wind-mast",
        "anchorParent": [
          5.3,
          -0.3468114941533936,
          1.8
        ],
        "anchorChild": [
          0,
          -3.095,
          0
        ]
      },
      {
        "id": "rotor-shaft",
        "name": "Wind rotor shaft",
        "type": "revolute",
        "parent": "wind-mast",
        "child": "wind-rotor",
        "anchorParent": [
          0,
          3.7050000000000005,
          0
        ],
        "anchorChild": [
          -2.220446049250313e-16,
          -0.43007214207425015,
          0
        ],
        "axis": [
          0,
          0,
          1
        ]
      },
      {
        "id": "solar-rail",
        "name": "Solar carriage rail",
        "type": "prismatic",
        "parent": "station-base",
        "child": "solar-carriage",
        "anchorParent": [
          0,
          2.4531885058466063,
          4.8
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -2,
          2
        ]
      }
    ],
    "modules": [
      "station-base",
      "airlock-door",
      "wind-mast",
      "wind-rotor",
      "solar-carriage"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-polar-research-station-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：1.0032
- C：0.0032
- D：0.2032

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.003245850710514025
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.00003337860107421875
      },
      {
        "time": 0.20833333333333334,
        "displacement": 4.76837158203125e-7
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
    "nominalDrift": 2.9029358903463267e-7,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-polar-research-station-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：0
- B：-2.5
- C：2.5
- D：-2

```json
{
  "input": {
    "joint": "solar-rail",
    "limits": [
      -2,
      2
    ],
    "units": "scene units"
  },
  "answer": {
    "choiceIds": [
      "A",
      "D"
    ]
  }
}
```

### 约束故障诊断（h3-polar-research-station-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：airlock-hinge
- B：rotor-shaft
- C：solar-rail
- D：mast-foot

```json
{
  "input": {
    "endpoints": [
      "station-base",
      "wind-mast"
    ],
    "type": "fixed",
    "joints": [
      {
        "id": "airlock-hinge",
        "name": "Airlock hinge",
        "type": "revolute",
        "parent": "station-base",
        "child": "airlock-door",
        "anchorParent": [
          -5.199999999999999,
          0.5531885058466064,
          -0.7
        ],
        "anchorChild": [
          0.10000000000000006,
          0,
          -1
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          0,
          1.7
        ]
      },
      {
        "id": "mast-foot",
        "name": "Turbine mast foot",
        "type": "fixed",
        "parent": "station-base",
        "child": "wind-mast",
        "anchorParent": [
          5.3,
          -0.3468114941533936,
          1.8
        ],
        "anchorChild": [
          0,
          -3.095,
          0
        ]
      },
      {
        "id": "rotor-shaft",
        "name": "Wind rotor shaft",
        "type": "revolute",
        "parent": "wind-mast",
        "child": "wind-rotor",
        "anchorParent": [
          0,
          3.7050000000000005,
          0
        ],
        "anchorChild": [
          -2.220446049250313e-16,
          -0.43007214207425015,
          0
        ],
        "axis": [
          0,
          0,
          1
        ]
      },
      {
        "id": "solar-rail",
        "name": "Solar carriage rail",
        "type": "prismatic",
        "parent": "station-base",
        "child": "solar-carriage",
        "anchorParent": [
          0,
          2.4531885058466063,
          4.8
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -2,
          2
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

### 主动检查收益（h3-polar-research-station-information-gain）

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
    "module": "airlock-door",
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

### 不确定性与弃答（h3-polar-research-station-abstention）

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

### 观测后信念更新（h3-polar-research-station-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0
- B：0.3333333333333333
- C：0.5
- D：0.25

```json
{
  "input": {
    "module": "airlock-door",
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
      "positive"
    ],
    "observed": "positive"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 多目标工程权衡（h3-polar-research-station-pareto）

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
        "cost": 7,
        "stiffness": 4,
        "mass": 0.5
      },
      {
        "id": "stock-1",
        "cost": 3,
        "stiffness": 4,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 5,
        "stiffness": 3,
        "mass": 1.2
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 11,
        "mass": 1.4
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

### 依赖装配（h3-polar-research-station-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:airlock-door",
        "label": "安装 airlock-door",
        "requires": [
          "present:station-base"
        ],
        "forbids": [
          "present:airlock-door"
        ],
        "adds": [
          "present:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door",
          "visible": true
        }
      },
      {
        "id": "place:solar-carriage",
        "label": "安装 solar-carriage",
        "requires": [
          "present:station-base"
        ],
        "forbids": [
          "present:solar-carriage"
        ],
        "adds": [
          "present:solar-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage",
          "visible": true
        }
      },
      {
        "id": "place:wind-mast",
        "label": "安装 wind-mast",
        "requires": [
          "present:station-base"
        ],
        "forbids": [
          "present:wind-mast"
        ],
        "adds": [
          "present:wind-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast",
          "visible": true
        }
      },
      {
        "id": "place:wind-rotor",
        "label": "安装 wind-rotor",
        "requires": [
          "present:wind-mast"
        ],
        "forbids": [
          "present:wind-rotor"
        ],
        "adds": [
          "present:wind-rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor",
          "visible": true
        }
      },
      {
        "id": "place:station-base",
        "label": "安装 station-base",
        "requires": [],
        "forbids": [
          "present:station-base"
        ],
        "adds": [
          "present:station-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "station-base",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:station-base",
      "present:wind-mast",
      "present:solar-carriage",
      "present:wind-rotor",
      "present:airlock-door"
    ],
    "budget": 5,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:station-base",
      "place:airlock-door",
      "place:solar-carriage",
      "place:wind-mast",
      "place:wind-rotor"
    ]
  }
}
```

### 依赖拆解（h3-polar-research-station-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:station-base",
      "present:airlock-door",
      "present:wind-mast",
      "present:wind-rotor",
      "present:solar-carriage"
    ],
    "initialModules": [
      "station-base",
      "airlock-door",
      "wind-mast",
      "wind-rotor",
      "solar-carriage"
    ],
    "actions": [
      {
        "id": "remove:airlock-door",
        "label": "拆除 airlock-door",
        "requires": [
          "present:airlock-door"
        ],
        "forbids": [],
        "adds": [
          "removed:airlock-door"
        ],
        "deletes": [
          "present:airlock-door"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door",
          "visible": false
        }
      },
      {
        "id": "remove:wind-rotor",
        "label": "拆除 wind-rotor",
        "requires": [
          "present:wind-rotor"
        ],
        "forbids": [],
        "adds": [
          "removed:wind-rotor"
        ],
        "deletes": [
          "present:wind-rotor"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor",
          "visible": false
        }
      },
      {
        "id": "remove:station-base",
        "label": "拆除 station-base",
        "requires": [
          "present:station-base"
        ],
        "forbids": [
          "present:airlock-door",
          "present:wind-mast",
          "present:solar-carriage"
        ],
        "adds": [
          "removed:station-base"
        ],
        "deletes": [
          "present:station-base"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "station-base",
          "visible": false
        }
      },
      {
        "id": "remove:wind-mast",
        "label": "拆除 wind-mast",
        "requires": [
          "present:wind-mast"
        ],
        "forbids": [
          "present:wind-rotor"
        ],
        "adds": [
          "removed:wind-mast"
        ],
        "deletes": [
          "present:wind-mast"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast",
          "visible": false
        }
      },
      {
        "id": "remove:solar-carriage",
        "label": "拆除 solar-carriage",
        "requires": [
          "present:solar-carriage"
        ],
        "forbids": [],
        "adds": [
          "removed:solar-carriage"
        ],
        "deletes": [
          "present:solar-carriage"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:airlock-door",
      "removed:wind-rotor",
      "removed:solar-carriage",
      "removed:wind-mast",
      "removed:station-base"
    ],
    "budget": 5,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:airlock-door",
      "remove:wind-rotor",
      "remove:wind-mast",
      "remove:solar-carriage",
      "remove:station-base"
    ]
  }
}
```

### 承载维修（h3-polar-research-station-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:airlock-door",
      "closed:airlock-door"
    ],
    "initialModules": [
      "station-base",
      "airlock-door",
      "wind-mast",
      "wind-rotor",
      "solar-carriage"
    ],
    "actions": [
      {
        "id": "replace:airlock-door",
        "label": "replace airlock-door",
        "requires": [
          "done:remove:airlock-door"
        ],
        "forbids": [
          "done:replace:airlock-door"
        ],
        "adds": [
          "done:replace:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door",
          "visible": true
        }
      },
      {
        "id": "remove:airlock-door",
        "label": "remove airlock-door",
        "requires": [
          "done:open:airlock-door"
        ],
        "forbids": [
          "done:remove:airlock-door"
        ],
        "adds": [
          "done:remove:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door",
          "visible": false
        }
      },
      {
        "id": "release:airlock-door",
        "label": "release airlock-door",
        "requires": [
          "done:close:airlock-door"
        ],
        "forbids": [
          "done:release:airlock-door"
        ],
        "adds": [
          "done:release:airlock-door",
          "repaired:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "close:airlock-door",
        "label": "close airlock-door",
        "requires": [
          "done:verify:airlock-door"
        ],
        "forbids": [
          "done:close:airlock-door"
        ],
        "adds": [
          "done:close:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "open:airlock-door",
        "label": "open airlock-door",
        "requires": [
          "done:support:airlock-door"
        ],
        "forbids": [
          "done:open:airlock-door"
        ],
        "adds": [
          "done:open:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "verify:airlock-door",
        "label": "verify airlock-door",
        "requires": [
          "done:replace:airlock-door"
        ],
        "forbids": [
          "done:verify:airlock-door"
        ],
        "adds": [
          "done:verify:airlock-door"
        ],
        "deletes": [
          "fault:airlock-door"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "support:airlock-door",
        "label": "support airlock-door",
        "requires": [
          "fault:airlock-door"
        ],
        "forbids": [
          "done:support:airlock-door"
        ],
        "adds": [
          "done:support:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      }
    ],
    "goalFacts": [
      "repaired:airlock-door"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:airlock-door",
      "open:airlock-door",
      "remove:airlock-door",
      "replace:airlock-door",
      "verify:airlock-door",
      "close:airlock-door",
      "release:airlock-door"
    ]
  }
}
```

### 复合编辑验证（h3-polar-research-station-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:airlock-door",
      "closed:airlock-door"
    ],
    "initialModules": [
      "station-base",
      "airlock-door",
      "wind-mast",
      "wind-rotor",
      "solar-carriage"
    ],
    "actions": [
      {
        "id": "release:airlock-door",
        "label": "release airlock-door",
        "requires": [
          "done:close:airlock-door"
        ],
        "forbids": [
          "done:release:airlock-door"
        ],
        "adds": [
          "done:release:airlock-door",
          "repaired:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "close:airlock-door",
        "label": "close airlock-door",
        "requires": [
          "done:verify:airlock-door"
        ],
        "forbids": [
          "done:close:airlock-door"
        ],
        "adds": [
          "done:close:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "recolor:airlock-door",
        "label": "recolor airlock-door",
        "requires": [
          "done:open:airlock-door"
        ],
        "forbids": [
          "done:recolor:airlock-door"
        ],
        "adds": [
          "done:recolor:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door",
          "color": "#ea7635"
        }
      },
      {
        "id": "open:airlock-door",
        "label": "open airlock-door",
        "requires": [
          "done:support:airlock-door"
        ],
        "forbids": [
          "done:open:airlock-door"
        ],
        "adds": [
          "done:open:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "verify:airlock-door",
        "label": "verify airlock-door",
        "requires": [
          "done:recolor:airlock-door"
        ],
        "forbids": [
          "done:verify:airlock-door"
        ],
        "adds": [
          "done:verify:airlock-door"
        ],
        "deletes": [
          "fault:airlock-door"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "support:airlock-door",
        "label": "support airlock-door",
        "requires": [
          "fault:airlock-door"
        ],
        "forbids": [
          "done:support:airlock-door"
        ],
        "adds": [
          "done:support:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      }
    ],
    "goalFacts": [
      "repaired:airlock-door"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:airlock-door",
      "open:airlock-door",
      "recolor:airlock-door",
      "verify:airlock-door",
      "close:airlock-door",
      "release:airlock-door"
    ]
  }
}
```

### 跨区域联合维修（h3-polar-research-station-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:wind-mast",
      "closed:wind-mast",
      "fault:wind-rotor",
      "closed:wind-rotor",
      "fault:solar-carriage",
      "closed:solar-carriage"
    ],
    "initialModules": [
      "station-base",
      "airlock-door",
      "wind-mast",
      "wind-rotor",
      "solar-carriage"
    ],
    "actions": [
      {
        "id": "verify:solar-carriage",
        "label": "verify solar-carriage",
        "requires": [
          "done:replace:solar-carriage"
        ],
        "forbids": [
          "done:verify:solar-carriage"
        ],
        "adds": [
          "done:verify:solar-carriage"
        ],
        "deletes": [
          "fault:solar-carriage"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage"
        }
      },
      {
        "id": "support:wind-rotor",
        "label": "support wind-rotor",
        "requires": [
          "fault:wind-rotor"
        ],
        "forbids": [
          "done:support:wind-rotor"
        ],
        "adds": [
          "done:support:wind-rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor"
        }
      },
      {
        "id": "close:wind-rotor",
        "label": "close wind-rotor",
        "requires": [
          "done:verify:wind-rotor"
        ],
        "forbids": [
          "done:close:wind-rotor"
        ],
        "adds": [
          "done:close:wind-rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor"
        }
      },
      {
        "id": "remove:wind-rotor",
        "label": "remove wind-rotor",
        "requires": [
          "done:open:wind-rotor"
        ],
        "forbids": [
          "done:remove:wind-rotor"
        ],
        "adds": [
          "done:remove:wind-rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor",
          "visible": false
        }
      },
      {
        "id": "release:solar-carriage",
        "label": "release solar-carriage",
        "requires": [
          "done:close:solar-carriage"
        ],
        "forbids": [
          "done:release:solar-carriage"
        ],
        "adds": [
          "done:release:solar-carriage",
          "repaired:solar-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage"
        }
      },
      {
        "id": "verify:wind-mast",
        "label": "verify wind-mast",
        "requires": [
          "done:replace:wind-mast"
        ],
        "forbids": [
          "done:verify:wind-mast"
        ],
        "adds": [
          "done:verify:wind-mast"
        ],
        "deletes": [
          "fault:wind-mast"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast"
        }
      },
      {
        "id": "support:wind-mast",
        "label": "support wind-mast",
        "requires": [
          "fault:wind-mast"
        ],
        "forbids": [
          "done:support:wind-mast"
        ],
        "adds": [
          "done:support:wind-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast"
        }
      },
      {
        "id": "replace:wind-rotor",
        "label": "replace wind-rotor",
        "requires": [
          "done:remove:wind-rotor"
        ],
        "forbids": [
          "done:replace:wind-rotor"
        ],
        "adds": [
          "done:replace:wind-rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor",
          "visible": true
        }
      },
      {
        "id": "remove:wind-mast",
        "label": "remove wind-mast",
        "requires": [
          "done:open:wind-mast"
        ],
        "forbids": [
          "done:remove:wind-mast"
        ],
        "adds": [
          "done:remove:wind-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast",
          "visible": false
        }
      },
      {
        "id": "open:wind-mast",
        "label": "open wind-mast",
        "requires": [
          "done:support:wind-mast"
        ],
        "forbids": [
          "done:open:wind-mast"
        ],
        "adds": [
          "done:open:wind-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast"
        }
      },
      {
        "id": "replace:wind-mast",
        "label": "replace wind-mast",
        "requires": [
          "done:remove:wind-mast"
        ],
        "forbids": [
          "done:replace:wind-mast"
        ],
        "adds": [
          "done:replace:wind-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast",
          "visible": true
        }
      },
      {
        "id": "close:solar-carriage",
        "label": "close solar-carriage",
        "requires": [
          "done:verify:solar-carriage"
        ],
        "forbids": [
          "done:close:solar-carriage"
        ],
        "adds": [
          "done:close:solar-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage"
        }
      },
      {
        "id": "release:wind-rotor",
        "label": "release wind-rotor",
        "requires": [
          "done:close:wind-rotor"
        ],
        "forbids": [
          "done:release:wind-rotor"
        ],
        "adds": [
          "done:release:wind-rotor",
          "repaired:wind-rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor"
        }
      },
      {
        "id": "close:wind-mast",
        "label": "close wind-mast",
        "requires": [
          "done:verify:wind-mast"
        ],
        "forbids": [
          "done:close:wind-mast"
        ],
        "adds": [
          "done:close:wind-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast"
        }
      },
      {
        "id": "open:solar-carriage",
        "label": "open solar-carriage",
        "requires": [
          "done:support:solar-carriage"
        ],
        "forbids": [
          "done:open:solar-carriage"
        ],
        "adds": [
          "done:open:solar-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage"
        }
      },
      {
        "id": "release:wind-mast",
        "label": "release wind-mast",
        "requires": [
          "done:close:wind-mast"
        ],
        "forbids": [
          "done:release:wind-mast"
        ],
        "adds": [
          "done:release:wind-mast",
          "repaired:wind-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast"
        }
      },
      {
        "id": "open:wind-rotor",
        "label": "open wind-rotor",
        "requires": [
          "done:support:wind-rotor"
        ],
        "forbids": [
          "done:open:wind-rotor"
        ],
        "adds": [
          "done:open:wind-rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor"
        }
      },
      {
        "id": "verify:wind-rotor",
        "label": "verify wind-rotor",
        "requires": [
          "done:replace:wind-rotor"
        ],
        "forbids": [
          "done:verify:wind-rotor"
        ],
        "adds": [
          "done:verify:wind-rotor"
        ],
        "deletes": [
          "fault:wind-rotor"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor"
        }
      },
      {
        "id": "remove:solar-carriage",
        "label": "remove solar-carriage",
        "requires": [
          "done:open:solar-carriage"
        ],
        "forbids": [
          "done:remove:solar-carriage"
        ],
        "adds": [
          "done:remove:solar-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage",
          "visible": false
        }
      },
      {
        "id": "replace:solar-carriage",
        "label": "replace solar-carriage",
        "requires": [
          "done:remove:solar-carriage"
        ],
        "forbids": [
          "done:replace:solar-carriage"
        ],
        "adds": [
          "done:replace:solar-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage",
          "visible": true
        }
      },
      {
        "id": "support:solar-carriage",
        "label": "support solar-carriage",
        "requires": [
          "fault:solar-carriage"
        ],
        "forbids": [
          "done:support:solar-carriage"
        ],
        "adds": [
          "done:support:solar-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage"
        }
      }
    ],
    "goalFacts": [
      "repaired:wind-mast",
      "repaired:wind-rotor",
      "repaired:solar-carriage"
    ],
    "budget": 21,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:wind-rotor",
      "support:wind-mast",
      "open:wind-mast",
      "remove:wind-mast",
      "replace:wind-mast",
      "verify:wind-mast",
      "close:wind-mast",
      "release:wind-mast",
      "open:wind-rotor",
      "remove:wind-rotor",
      "replace:wind-rotor",
      "verify:wind-rotor",
      "close:wind-rotor",
      "release:wind-rotor",
      "support:solar-carriage",
      "open:solar-carriage",
      "remove:solar-carriage",
      "replace:solar-carriage",
      "verify:solar-carriage",
      "close:solar-carriage",
      "release:solar-carriage"
    ]
  }
}
```

### 多工位资源调度（h3-polar-research-station-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "station-base",
        "duration": 2,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "airlock-door",
        "duration": 3,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "wind-mast",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "wind-rotor",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "solar-carriage",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      }
    ],
    "deadline": 6
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 2,
      "job-3": 3,
      "job-4": 4
    }
  }
}
```

### 检查后条件策略（h3-polar-research-station-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "airlock-door",
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

### 局部坐标变换（h3-polar-research-station-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[-4.2,2.2,0.3]
- B：[-4.3,3.2,2.4]
- C：[-5.3,2.2,1.4]
- D：[1.1,0,0]

```json
{
  "input": {
    "localPoint": [
      1.1,
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
      -5.299999999999999,
      2.2,
      0.3
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-polar-research-station-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[4,5]
- B：[0,0]
- C：[4,-5]
- D：[9,4]

```json
{
  "input": {
    "view": "top",
    "point": [
      4,
      9,
      -5
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 空间相对关系（h3-polar-research-station-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：less
- B：equal
- C：greater

```json
{
  "input": {
    "A": {
      "id": "station-base",
      "position": [
        0,
        1.6468114941533936,
        0
      ]
    },
    "B": {
      "id": "solar-carriage",
      "position": [
        0,
        4.1,
        4.8
      ]
    },
    "axis": "z"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 约束自由度（h3-polar-research-station-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：6
- B：1
- C：0
- D：3

```json
{
  "input": {
    "joint": {
      "id": "solar-rail",
      "name": "Solar carriage rail",
      "type": "prismatic",
      "parent": "station-base",
      "child": "solar-carriage",
      "anchorParent": [
        0,
        2.4531885058466063,
        4.8
      ],
      "anchorChild": [
        0,
        0,
        0
      ],
      "axis": [
        1,
        0,
        0
      ],
      "limits": [
        -2,
        2
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 维修间隙预算（h3-polar-research-station-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "airlock-door",
    "aperture": 0.81,
    "toolWidth": 0.55,
    "eachSideMargin": 0.1
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-polar-research-station-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,-18]
- B：[0,0,18]
- C：[0,0,0]
- D：[0,-3,0]

```json
{
  "input": {
    "module": "airlock-door",
    "lever": [
      3,
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
    "choiceId": "A"
  }
}
```

### 非均匀先验更新（h3-polar-research-station-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：1
- B：0.5454545454545454
- C：0.4
- D：0

```json
{
  "input": {
    "module": "airlock-door",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      5,
      6,
      4
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

### 风险最小决策（h3-polar-research-station-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.8,
    "repairCost": 3,
    "failureLoss": 13,
    "module": "airlock-door"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-polar-research-station-trace-threshold）

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
        "displacement": 0.003245850710514025
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.00003337860107421875
      },
      {
        "time": 0.20833333333333334,
        "displacement": 4.76837158203125e-7
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
    "threshold": 0.00389502085261683
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-polar-research-station-guarded-repair）

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
        "id": "release:airlock-door",
        "label": "release airlock-door",
        "requires": [
          "done:relock:airlock-door"
        ],
        "forbids": [
          "done:release:airlock-door"
        ],
        "adds": [
          "done:release:airlock-door",
          "ready:airlock-door",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "relock:airlock-door",
        "label": "relock airlock-door",
        "requires": [
          "done:verify:airlock-door"
        ],
        "forbids": [
          "done:relock:airlock-door"
        ],
        "adds": [
          "done:relock:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "verify:airlock-door",
        "label": "verify airlock-door",
        "requires": [
          "done:replace:airlock-door"
        ],
        "forbids": [
          "done:verify:airlock-door"
        ],
        "adds": [
          "done:verify:airlock-door"
        ],
        "deletes": [
          "fault:airlock-door",
          "misaligned:airlock-door"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "replace:airlock-door",
        "label": "replace airlock-door",
        "requires": [
          "done:unlock:airlock-door"
        ],
        "forbids": [
          "done:replace:airlock-door"
        ],
        "adds": [
          "done:replace:airlock-door"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "unlock:airlock-door",
        "label": "unlock airlock-door",
        "requires": [
          "done:support:airlock-door"
        ],
        "forbids": [
          "done:unlock:airlock-door"
        ],
        "adds": [
          "done:unlock:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "support:airlock-door",
        "label": "support airlock-door",
        "requires": [
          "done:isolate:airlock-door"
        ],
        "forbids": [
          "done:support:airlock-door"
        ],
        "adds": [
          "done:support:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "isolate:airlock-door",
        "label": "isolate airlock-door",
        "requires": [
          "tool:free",
          "fault:airlock-door"
        ],
        "forbids": [
          "done:isolate:airlock-door"
        ],
        "adds": [
          "done:isolate:airlock-door"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:airlock-door"
    ],
    "initialModules": [
      "station-base",
      "airlock-door",
      "wind-mast",
      "wind-rotor",
      "solar-carriage"
    ],
    "goalFacts": [
      "ready:airlock-door"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:airlock-door",
      "support:airlock-door",
      "unlock:airlock-door",
      "replace:airlock-door",
      "verify:airlock-door",
      "relock:airlock-door",
      "release:airlock-door"
    ]
  }
}
```

### 失败状态回退（h3-polar-research-station-rollback）

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
        "id": "resume:airlock-door",
        "label": "resume airlock-door",
        "requires": [
          "done:verify:airlock-door"
        ],
        "forbids": [
          "done:resume:airlock-door"
        ],
        "adds": [
          "done:resume:airlock-door",
          "ready:airlock-door",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "verify:airlock-door",
        "label": "verify airlock-door",
        "requires": [
          "done:align:airlock-door"
        ],
        "forbids": [
          "done:verify:airlock-door"
        ],
        "adds": [
          "done:verify:airlock-door"
        ],
        "deletes": [
          "fault:airlock-door",
          "misaligned:airlock-door"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "align:airlock-door",
        "label": "align airlock-door",
        "requires": [
          "done:undo:airlock-door"
        ],
        "forbids": [
          "done:align:airlock-door"
        ],
        "adds": [
          "done:align:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door",
          "visible": true
        }
      },
      {
        "id": "undo:airlock-door",
        "label": "undo airlock-door",
        "requires": [
          "done:isolate:airlock-door"
        ],
        "forbids": [
          "done:undo:airlock-door"
        ],
        "adds": [
          "done:undo:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door",
          "visible": false
        }
      },
      {
        "id": "isolate:airlock-door",
        "label": "isolate airlock-door",
        "requires": [
          "tool:free",
          "fault:airlock-door"
        ],
        "forbids": [
          "done:isolate:airlock-door"
        ],
        "adds": [
          "done:isolate:airlock-door"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:airlock-door",
      "misaligned:airlock-door"
    ],
    "initialModules": [
      "station-base",
      "airlock-door",
      "wind-mast",
      "wind-rotor",
      "solar-carriage"
    ],
    "goalFacts": [
      "ready:airlock-door"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:airlock-door",
      "undo:airlock-door",
      "align:airlock-door",
      "verify:airlock-door",
      "resume:airlock-door"
    ]
  }
}
```

### 共享工具协同维修（h3-polar-research-station-resource-repair）

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
        "id": "release:solar-carriage",
        "label": "release solar-carriage",
        "requires": [
          "done:relock:solar-carriage"
        ],
        "forbids": [
          "done:release:solar-carriage"
        ],
        "adds": [
          "done:release:solar-carriage",
          "ready:solar-carriage",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage"
        }
      },
      {
        "id": "relock:solar-carriage",
        "label": "relock solar-carriage",
        "requires": [
          "done:verify:solar-carriage"
        ],
        "forbids": [
          "done:relock:solar-carriage"
        ],
        "adds": [
          "done:relock:solar-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage"
        }
      },
      {
        "id": "verify:solar-carriage",
        "label": "verify solar-carriage",
        "requires": [
          "done:replace:solar-carriage"
        ],
        "forbids": [
          "done:verify:solar-carriage"
        ],
        "adds": [
          "done:verify:solar-carriage"
        ],
        "deletes": [
          "fault:solar-carriage",
          "misaligned:solar-carriage"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage"
        }
      },
      {
        "id": "replace:solar-carriage",
        "label": "replace solar-carriage",
        "requires": [
          "done:unlock:solar-carriage"
        ],
        "forbids": [
          "done:replace:solar-carriage"
        ],
        "adds": [
          "done:replace:solar-carriage"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "solar-carriage"
        }
      },
      {
        "id": "unlock:solar-carriage",
        "label": "unlock solar-carriage",
        "requires": [
          "done:support:solar-carriage"
        ],
        "forbids": [
          "done:unlock:solar-carriage"
        ],
        "adds": [
          "done:unlock:solar-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage"
        }
      },
      {
        "id": "support:solar-carriage",
        "label": "support solar-carriage",
        "requires": [
          "done:isolate:solar-carriage"
        ],
        "forbids": [
          "done:support:solar-carriage"
        ],
        "adds": [
          "done:support:solar-carriage"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage"
        }
      },
      {
        "id": "isolate:solar-carriage",
        "label": "isolate solar-carriage",
        "requires": [
          "tool:free",
          "fault:solar-carriage"
        ],
        "forbids": [
          "done:isolate:solar-carriage"
        ],
        "adds": [
          "done:isolate:solar-carriage"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "solar-carriage"
        }
      },
      {
        "id": "release:wind-rotor",
        "label": "release wind-rotor",
        "requires": [
          "done:relock:wind-rotor"
        ],
        "forbids": [
          "done:release:wind-rotor"
        ],
        "adds": [
          "done:release:wind-rotor",
          "ready:wind-rotor",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor"
        }
      },
      {
        "id": "relock:wind-rotor",
        "label": "relock wind-rotor",
        "requires": [
          "done:verify:wind-rotor"
        ],
        "forbids": [
          "done:relock:wind-rotor"
        ],
        "adds": [
          "done:relock:wind-rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor"
        }
      },
      {
        "id": "verify:wind-rotor",
        "label": "verify wind-rotor",
        "requires": [
          "done:replace:wind-rotor"
        ],
        "forbids": [
          "done:verify:wind-rotor"
        ],
        "adds": [
          "done:verify:wind-rotor"
        ],
        "deletes": [
          "fault:wind-rotor",
          "misaligned:wind-rotor"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor"
        }
      },
      {
        "id": "replace:wind-rotor",
        "label": "replace wind-rotor",
        "requires": [
          "done:unlock:wind-rotor"
        ],
        "forbids": [
          "done:replace:wind-rotor"
        ],
        "adds": [
          "done:replace:wind-rotor"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "wind-rotor"
        }
      },
      {
        "id": "unlock:wind-rotor",
        "label": "unlock wind-rotor",
        "requires": [
          "done:support:wind-rotor"
        ],
        "forbids": [
          "done:unlock:wind-rotor"
        ],
        "adds": [
          "done:unlock:wind-rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor"
        }
      },
      {
        "id": "support:wind-rotor",
        "label": "support wind-rotor",
        "requires": [
          "done:isolate:wind-rotor"
        ],
        "forbids": [
          "done:support:wind-rotor"
        ],
        "adds": [
          "done:support:wind-rotor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor"
        }
      },
      {
        "id": "isolate:wind-rotor",
        "label": "isolate wind-rotor",
        "requires": [
          "tool:free",
          "fault:wind-rotor"
        ],
        "forbids": [
          "done:isolate:wind-rotor"
        ],
        "adds": [
          "done:isolate:wind-rotor"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wind-rotor"
        }
      },
      {
        "id": "release:wind-mast",
        "label": "release wind-mast",
        "requires": [
          "done:relock:wind-mast"
        ],
        "forbids": [
          "done:release:wind-mast"
        ],
        "adds": [
          "done:release:wind-mast",
          "ready:wind-mast",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast"
        }
      },
      {
        "id": "relock:wind-mast",
        "label": "relock wind-mast",
        "requires": [
          "done:verify:wind-mast"
        ],
        "forbids": [
          "done:relock:wind-mast"
        ],
        "adds": [
          "done:relock:wind-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast"
        }
      },
      {
        "id": "verify:wind-mast",
        "label": "verify wind-mast",
        "requires": [
          "done:replace:wind-mast"
        ],
        "forbids": [
          "done:verify:wind-mast"
        ],
        "adds": [
          "done:verify:wind-mast"
        ],
        "deletes": [
          "fault:wind-mast",
          "misaligned:wind-mast"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast"
        }
      },
      {
        "id": "replace:wind-mast",
        "label": "replace wind-mast",
        "requires": [
          "done:unlock:wind-mast"
        ],
        "forbids": [
          "done:replace:wind-mast"
        ],
        "adds": [
          "done:replace:wind-mast"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "wind-mast"
        }
      },
      {
        "id": "unlock:wind-mast",
        "label": "unlock wind-mast",
        "requires": [
          "done:support:wind-mast"
        ],
        "forbids": [
          "done:unlock:wind-mast"
        ],
        "adds": [
          "done:unlock:wind-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast"
        }
      },
      {
        "id": "support:wind-mast",
        "label": "support wind-mast",
        "requires": [
          "done:isolate:wind-mast"
        ],
        "forbids": [
          "done:support:wind-mast"
        ],
        "adds": [
          "done:support:wind-mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast"
        }
      },
      {
        "id": "isolate:wind-mast",
        "label": "isolate wind-mast",
        "requires": [
          "tool:free",
          "fault:wind-mast"
        ],
        "forbids": [
          "done:isolate:wind-mast"
        ],
        "adds": [
          "done:isolate:wind-mast"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wind-mast"
        }
      },
      {
        "id": "release:airlock-door",
        "label": "release airlock-door",
        "requires": [
          "done:relock:airlock-door"
        ],
        "forbids": [
          "done:release:airlock-door"
        ],
        "adds": [
          "done:release:airlock-door",
          "ready:airlock-door",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "relock:airlock-door",
        "label": "relock airlock-door",
        "requires": [
          "done:verify:airlock-door"
        ],
        "forbids": [
          "done:relock:airlock-door"
        ],
        "adds": [
          "done:relock:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "verify:airlock-door",
        "label": "verify airlock-door",
        "requires": [
          "done:replace:airlock-door"
        ],
        "forbids": [
          "done:verify:airlock-door"
        ],
        "adds": [
          "done:verify:airlock-door"
        ],
        "deletes": [
          "fault:airlock-door",
          "misaligned:airlock-door"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "replace:airlock-door",
        "label": "replace airlock-door",
        "requires": [
          "done:unlock:airlock-door"
        ],
        "forbids": [
          "done:replace:airlock-door"
        ],
        "adds": [
          "done:replace:airlock-door"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "unlock:airlock-door",
        "label": "unlock airlock-door",
        "requires": [
          "done:support:airlock-door"
        ],
        "forbids": [
          "done:unlock:airlock-door"
        ],
        "adds": [
          "done:unlock:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "support:airlock-door",
        "label": "support airlock-door",
        "requires": [
          "done:isolate:airlock-door"
        ],
        "forbids": [
          "done:support:airlock-door"
        ],
        "adds": [
          "done:support:airlock-door"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      },
      {
        "id": "isolate:airlock-door",
        "label": "isolate airlock-door",
        "requires": [
          "tool:free",
          "fault:airlock-door"
        ],
        "forbids": [
          "done:isolate:airlock-door"
        ],
        "adds": [
          "done:isolate:airlock-door"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock-door"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:airlock-door",
      "fault:wind-mast",
      "fault:wind-rotor",
      "fault:solar-carriage"
    ],
    "initialModules": [
      "station-base",
      "airlock-door",
      "wind-mast",
      "wind-rotor",
      "solar-carriage"
    ],
    "goalFacts": [
      "ready:airlock-door",
      "ready:wind-mast",
      "ready:wind-rotor",
      "ready:solar-carriage"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:solar-carriage",
      "support:solar-carriage",
      "unlock:solar-carriage",
      "replace:solar-carriage",
      "verify:solar-carriage",
      "relock:solar-carriage",
      "release:solar-carriage",
      "isolate:wind-rotor",
      "support:wind-rotor",
      "unlock:wind-rotor",
      "replace:wind-rotor",
      "verify:wind-rotor",
      "relock:wind-rotor",
      "release:wind-rotor",
      "isolate:wind-mast",
      "support:wind-mast",
      "unlock:wind-mast",
      "replace:wind-mast",
      "verify:wind-mast",
      "relock:wind-mast",
      "release:wind-mast",
      "isolate:airlock-door",
      "support:airlock-door",
      "unlock:airlock-door",
      "replace:airlock-door",
      "verify:airlock-door",
      "relock:airlock-door",
      "release:airlock-door"
    ]
  }
}
```

### 预算约束检查策略（h3-polar-research-station-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "airlock-door",
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
        "cost": 4,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "probe",
        "cost": 3,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "thermal",
        "cost": 0,
        "returns": {
          "nominal": "clear",
          "fault": "clear"
        }
      }
    ],
    "budget": 3
  },
  "answer": {
    "queryId": "probe",
    "decisions": {
      "clear": "continue",
      "alert": "replace"
    }
  }
}
```
