## D3 轨道检修车

### 模块识别（h3-orbital-service-rover-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：chassis
- B：wheel-lf
- C：wheel-lm
- D：battery

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "chassis",
        "name": "Pressurized rover chassis"
      },
      {
        "id": "battery",
        "name": "Rear battery cartridge"
      },
      {
        "id": "wheel-lf",
        "name": "wheel lf"
      },
      {
        "id": "wheel-lm",
        "name": "wheel lm"
      },
      {
        "id": "wheel-lr",
        "name": "wheel lr"
      },
      {
        "id": "wheel-rf",
        "name": "wheel rf"
      },
      {
        "id": "wheel-rm",
        "name": "wheel rm"
      },
      {
        "id": "wheel-rr",
        "name": "wheel rr"
      },
      {
        "id": "sample-arm",
        "name": "Articulated sample arm"
      },
      {
        "id": "sensor-mast",
        "name": "Panoramic sensor mast"
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 部件计数（h3-orbital-service-rover-count）

模块 battery 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：1
- B：5
- C：2
- D：3

```json
{
  "input": {
    "parts": [
      {
        "id": "v0001",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0002",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0003",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0004",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0005",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0006",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0007",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0008",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0009",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0010",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0011",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0012",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0013",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0014",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0015",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "v0016",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0017",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0018",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0019",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0020",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0021",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0022",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0023",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0024",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0025",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0026",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0027",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0028",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0029",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0030",
        "moduleId": "chassis",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0031",
        "moduleId": "chassis",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0032",
        "moduleId": "chassis",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0033",
        "moduleId": "chassis",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0034",
        "moduleId": "chassis",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0035",
        "moduleId": "chassis",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0036",
        "moduleId": "chassis",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0037",
        "moduleId": "chassis",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0038",
        "moduleId": "chassis",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0039",
        "moduleId": "chassis",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0040",
        "moduleId": "chassis",
        "shape": "panel",
        "color": "#edf1f2"
      },
      {
        "id": "v0041",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "v0042",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "v0043",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "v0044",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "v0045",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "v0046",
        "moduleId": "chassis",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "v0047",
        "moduleId": "battery",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "v0048",
        "moduleId": "battery",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "v0049",
        "moduleId": "wheel-lf",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "v0050",
        "moduleId": "wheel-lf",
        "shape": "axle",
        "color": "#c6cdd2"
      },
      {
        "id": "v0051",
        "moduleId": "wheel-lm",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "v0052",
        "moduleId": "wheel-lm",
        "shape": "axle",
        "color": "#c6cdd2"
      },
      {
        "id": "v0053",
        "moduleId": "wheel-lr",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "v0054",
        "moduleId": "wheel-lr",
        "shape": "axle",
        "color": "#c6cdd2"
      },
      {
        "id": "v0055",
        "moduleId": "wheel-rf",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "v0056",
        "moduleId": "wheel-rf",
        "shape": "axle",
        "color": "#c6cdd2"
      },
      {
        "id": "v0057",
        "moduleId": "wheel-rm",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "v0058",
        "moduleId": "wheel-rm",
        "shape": "axle",
        "color": "#c6cdd2"
      },
      {
        "id": "v0059",
        "moduleId": "wheel-rr",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "v0060",
        "moduleId": "wheel-rr",
        "shape": "axle",
        "color": "#c6cdd2"
      },
      {
        "id": "v0061",
        "moduleId": "sample-arm",
        "shape": "gear",
        "color": "#8c99a3"
      },
      {
        "id": "v0062",
        "moduleId": "sample-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "v0063",
        "moduleId": "sample-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "v0064",
        "moduleId": "sample-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "v0065",
        "moduleId": "sample-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "v0066",
        "moduleId": "sample-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "v0067",
        "moduleId": "sample-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "v0068",
        "moduleId": "sample-arm",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "v0069",
        "moduleId": "sensor-mast",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "v0070",
        "moduleId": "sensor-mast",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "v0071",
        "moduleId": "sensor-mast",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "v0072",
        "moduleId": "sensor-mast",
        "shape": "beam",
        "color": "#8c99a3"
      },
      {
        "id": "v0073",
        "moduleId": "sensor-mast",
        "shape": "sphere",
        "color": "#79c7d8"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 颜色识别（h3-orbital-service-rover-color）

零件 v0047 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#2878b8
- B：#d43a32
- C：#26323b
- D：#f2bf3c

```json
{
  "input": {
    "part": {
      "id": "v0047",
      "moduleId": "battery",
      "shape": "panel",
      "size": [
        3.4,
        1.1,
        1.2
      ],
      "position": [
        0,
        0,
        -0.1375
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

### 三维位置（h3-orbital-service-rover-position）

模块 battery 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[-3.75,1,-3]
- B：[-3.75,1,0]
- C：[0,1.4,5.4375]
- D：[0,2.6250000000000004,-0.344822903061214]

```json
{
  "input": {
    "centers": {
      "chassis": [
        0,
        2.6250000000000004,
        -0.344822903061214
      ],
      "battery": [
        0,
        1.4,
        5.4375
      ],
      "wheel-lf": [
        -3.75,
        1,
        -3
      ],
      "wheel-lm": [
        -3.75,
        1,
        0
      ],
      "wheel-lr": [
        -3.75,
        1,
        3
      ],
      "wheel-rf": [
        3.75,
        1,
        -3
      ],
      "wheel-rm": [
        3.75,
        1,
        0
      ],
      "wheel-rr": [
        3.75,
        1,
        3
      ],
      "sample-arm": [
        3.5125,
        5.057450054324738,
        -1.5
      ],
      "sensor-mast": [
        -1.3,
        4.9375,
        -0.8
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节类型（h3-orbital-service-rover-joint-type）

arm-shoulder 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：revolute
- B：fixed
- C：prismatic
- D：spring

```json
{
  "input": {
    "joint": {
      "id": "arm-shoulder",
      "name": "Arm shoulder hinge",
      "type": "revolute",
      "parent": "chassis",
      "child": "sample-arm",
      "anchorParent": [
        2.3,
        0.375,
        -1.155177096938786
      ],
      "anchorChild": [
        -1.2125000000000001,
        -2.057450054324738,
        0
      ],
      "axis": [
        0,
        0,
        1
      ],
      "limits": [
        -0.2,
        1.2
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 直接连接（h3-orbital-service-rover-parent）

battery 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["battery"]
- B：[]
- C：["chassis","battery","wheel-lf","wheel-lm","wheel-lr","wheel-rf","wheel-rm","wheel-rr","sample-arm","sensor-mast"]
- D：["chassis"]

```json
{
  "input": {
    "joints": [
      {
        "id": "battery-lock",
        "name": "Battery locking pins",
        "type": "fixed",
        "parent": "chassis",
        "child": "battery",
        "anchorParent": [
          0,
          -1.225,
          5.644822903061214
        ],
        "anchorChild": [
          0,
          0,
          -0.1375
        ]
      },
      {
        "id": "wheel-lf-axle",
        "name": "wheel-lf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lf",
        "anchorParent": [
          -3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-lm-axle",
        "name": "wheel-lm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lm",
        "anchorParent": [
          -3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-lr-axle",
        "name": "wheel-lr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lr",
        "anchorParent": [
          -3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "wheel-rf-axle",
        "name": "wheel-rf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rf",
        "anchorParent": [
          3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-rm-axle",
        "name": "wheel-rm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rm",
        "anchorParent": [
          3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-rr-axle",
        "name": "wheel-rr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rr",
        "anchorParent": [
          3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "Arm shoulder hinge",
        "type": "revolute",
        "parent": "chassis",
        "child": "sample-arm",
        "anchorParent": [
          2.3,
          0.375,
          -1.155177096938786
        ],
        "anchorChild": [
          -1.2125000000000001,
          -2.057450054324738,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.2
        ]
      },
      {
        "id": "mast-turntable",
        "name": "Mast turntable",
        "type": "revolute",
        "parent": "chassis",
        "child": "sensor-mast",
        "anchorParent": [
          -1.3,
          0.575,
          -0.45517709693878605
        ],
        "anchorChild": [
          0,
          -1.7374999999999998,
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
    "choiceId": "D"
  }
}
```

### 基座识别（h3-orbital-service-rover-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["battery"]
- B：["chassis"]
- C：[]
- D：["chassis","battery","wheel-lf","wheel-lm","wheel-lr","wheel-rf","wheel-rm","wheel-rr","sample-arm","sensor-mast"]

```json
{
  "input": {
    "modules": [
      {
        "id": "chassis",
        "name": "Pressurized rover chassis",
        "role": "primary-frame",
        "anchored": true,
        "mass": 18,
        "position": [
          0,
          2.625,
          -0.344822903061214
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
        "name": "Rear battery cartridge",
        "role": "service-module",
        "anchored": false,
        "mass": 2,
        "position": [
          0,
          1.4,
          5.4375
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "wheel-lf",
        "name": "wheel lf",
        "role": "wheel",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -3.75,
          1,
          -3
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "wheel-lm",
        "name": "wheel lm",
        "role": "wheel",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -3.75,
          1,
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
        "id": "wheel-lr",
        "name": "wheel lr",
        "role": "wheel",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -3.75,
          1,
          3
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "wheel-rf",
        "name": "wheel rf",
        "role": "wheel",
        "anchored": false,
        "mass": 1.2,
        "position": [
          3.75,
          1,
          -3
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "wheel-rm",
        "name": "wheel rm",
        "role": "wheel",
        "anchored": false,
        "mass": 1.2,
        "position": [
          3.75,
          1,
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
        "id": "wheel-rr",
        "name": "wheel rr",
        "role": "wheel",
        "anchored": false,
        "mass": 1.2,
        "position": [
          3.75,
          1,
          3
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "sample-arm",
        "name": "Articulated sample arm",
        "role": "actuator",
        "anchored": false,
        "mass": 2.5,
        "position": [
          3.5125,
          5.057450054324738,
          -1.5
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
        "name": "Panoramic sensor mast",
        "role": "sensor",
        "anchored": false,
        "mass": 1.4,
        "position": [
          -1.3,
          4.9375,
          -0.8
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

### 接口计数（h3-orbital-service-rover-degree）

battery 连接几个声明关节？平行关节分别计数。

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
        "id": "battery-lock",
        "name": "Battery locking pins",
        "type": "fixed",
        "parent": "chassis",
        "child": "battery",
        "anchorParent": [
          0,
          -1.225,
          5.644822903061214
        ],
        "anchorChild": [
          0,
          0,
          -0.1375
        ]
      },
      {
        "id": "wheel-lf-axle",
        "name": "wheel-lf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lf",
        "anchorParent": [
          -3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-lm-axle",
        "name": "wheel-lm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lm",
        "anchorParent": [
          -3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-lr-axle",
        "name": "wheel-lr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lr",
        "anchorParent": [
          -3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "wheel-rf-axle",
        "name": "wheel-rf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rf",
        "anchorParent": [
          3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-rm-axle",
        "name": "wheel-rm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rm",
        "anchorParent": [
          3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-rr-axle",
        "name": "wheel-rr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rr",
        "anchorParent": [
          3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "Arm shoulder hinge",
        "type": "revolute",
        "parent": "chassis",
        "child": "sample-arm",
        "anchorParent": [
          2.3,
          0.375,
          -1.155177096938786
        ],
        "anchorChild": [
          -1.2125000000000001,
          -2.057450054324738,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.2
        ]
      },
      {
        "id": "mast-turntable",
        "name": "Mast turntable",
        "type": "revolute",
        "parent": "chassis",
        "child": "sensor-mast",
        "anchorParent": [
          -1.3,
          0.575,
          -0.45517709693878605
        ],
        "anchorChild": [
          0,
          -1.7374999999999998,
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
    "choiceId": "D"
  }
}
```

### 局部改色（h3-orbital-service-rover-recolor）

仅将 v0047 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"v0048","color":"#e8792e"}
- B：{"id":"v0047","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"v0047","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "v0047",
      "moduleId": "battery",
      "shape": "panel",
      "size": [
        3.4,
        1.1,
        1.2
      ],
      "position": [
        0,
        0,
        -0.1375
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

### 补装部件（h3-orbital-service-rover-add）

模块 battery 缺失零件 v0047。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"v0047","moduleId":"battery","shape":"panel","size":[3.4,1.1,1.2],"position":[0,0,-0.1375],"rotation":[0,0,0,1],"color":"#000000"}
- B：{"id":"v0047","moduleId":"battery","shape":"panel","size":[3.4,1.1,1.2],"position":[0,0,-0.1375],"rotation":[0,0,0,1],"color":"#f2bf3c"}
- C：{"id":"v0047","moduleId":"chassis","shape":"panel","size":[3.4,1.1,1.2],"position":[0,0,-0.1375],"rotation":[0,0,0,1],"color":"#f2bf3c"}
- D：{"id":"v0047","moduleId":"battery","shape":"panel","size":[3,3,3],"position":[0,0,-0.1375],"rotation":[0,0,0,1],"color":"#f2bf3c"}

```json
{
  "input": {
    "targetPart": {
      "id": "v0047",
      "moduleId": "battery",
      "shape": "panel",
      "size": [
        3.4,
        1.1,
        1.2
      ],
      "position": [
        0,
        0,
        -0.1375
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
      "v0048",
      "v0049",
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
      "v0066",
      "v0067",
      "v0068",
      "v0069",
      "v0070",
      "v0071",
      "v0072",
      "v0073"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全拆除（h3-orbital-service-rover-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["chassis","battery","wheel-lf","wheel-lm","wheel-lr","wheel-rf","wheel-rm","wheel-rr","sample-arm","sensor-mast"]
- B：["battery","sample-arm","sensor-mast","wheel-lf","wheel-lm","wheel-lr","wheel-rf","wheel-rm","wheel-rr"]
- C：["chassis"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "battery-lock",
        "name": "Battery locking pins",
        "type": "fixed",
        "parent": "chassis",
        "child": "battery",
        "anchorParent": [
          0,
          -1.225,
          5.644822903061214
        ],
        "anchorChild": [
          0,
          0,
          -0.1375
        ]
      },
      {
        "id": "wheel-lf-axle",
        "name": "wheel-lf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lf",
        "anchorParent": [
          -3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-lm-axle",
        "name": "wheel-lm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lm",
        "anchorParent": [
          -3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-lr-axle",
        "name": "wheel-lr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lr",
        "anchorParent": [
          -3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "wheel-rf-axle",
        "name": "wheel-rf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rf",
        "anchorParent": [
          3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-rm-axle",
        "name": "wheel-rm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rm",
        "anchorParent": [
          3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-rr-axle",
        "name": "wheel-rr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rr",
        "anchorParent": [
          3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "Arm shoulder hinge",
        "type": "revolute",
        "parent": "chassis",
        "child": "sample-arm",
        "anchorParent": [
          2.3,
          0.375,
          -1.155177096938786
        ],
        "anchorChild": [
          -1.2125000000000001,
          -2.057450054324738,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.2
        ]
      },
      {
        "id": "mast-turntable",
        "name": "Mast turntable",
        "type": "revolute",
        "parent": "chassis",
        "child": "sensor-mast",
        "anchorParent": [
          -1.3,
          0.575,
          -0.45517709693878605
        ],
        "anchorChild": [
          0,
          -1.7374999999999998,
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
      "chassis",
      "battery",
      "wheel-lf",
      "wheel-lm",
      "wheel-lr",
      "wheel-rf",
      "wheel-rm",
      "wheel-rr",
      "sample-arm",
      "sensor-mast"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 替换选择（h3-orbital-service-rover-replace）

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
        "cost": 7,
        "stiffness": 6,
        "mass": 0.7
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 10,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 6,
        "stiffness": 7,
        "mass": 0.9
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 11,
        "mass": 1.6
      }
    ],
    "maxCost": 7
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 平移纠偏（h3-orbital-service-rover-translate）

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
    "target": "battery"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-orbital-service-rover-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：135
- B：0
- C：90
- D：-135

```json
{
  "input": {
    "module": "battery",
    "currentYaw": 90,
    "targetYaw": 315
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 下一步放置（h3-orbital-service-rover-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["chassis","battery","wheel-lf","wheel-lm","wheel-lr"]
- B：["chassis"]
- C：["sample-arm","sensor-mast","wheel-rf","wheel-rm","wheel-rr"]
- D：[]

```json
{
  "input": {
    "prefix": [
      "chassis",
      "battery",
      "wheel-lf",
      "wheel-lm",
      "wheel-lr"
    ],
    "joints": [
      {
        "id": "battery-lock",
        "name": "Battery locking pins",
        "type": "fixed",
        "parent": "chassis",
        "child": "battery",
        "anchorParent": [
          0,
          -1.225,
          5.644822903061214
        ],
        "anchorChild": [
          0,
          0,
          -0.1375
        ]
      },
      {
        "id": "wheel-lf-axle",
        "name": "wheel-lf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lf",
        "anchorParent": [
          -3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-lm-axle",
        "name": "wheel-lm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lm",
        "anchorParent": [
          -3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-lr-axle",
        "name": "wheel-lr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lr",
        "anchorParent": [
          -3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "wheel-rf-axle",
        "name": "wheel-rf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rf",
        "anchorParent": [
          3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-rm-axle",
        "name": "wheel-rm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rm",
        "anchorParent": [
          3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-rr-axle",
        "name": "wheel-rr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rr",
        "anchorParent": [
          3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "Arm shoulder hinge",
        "type": "revolute",
        "parent": "chassis",
        "child": "sample-arm",
        "anchorParent": [
          2.3,
          0.375,
          -1.155177096938786
        ],
        "anchorChild": [
          -1.2125000000000001,
          -2.057450054324738,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.2
        ]
      },
      {
        "id": "mast-turntable",
        "name": "Mast turntable",
        "type": "revolute",
        "parent": "chassis",
        "child": "sensor-mast",
        "anchorParent": [
          -1.3,
          0.575,
          -0.45517709693878605
        ],
        "anchorChild": [
          0,
          -1.7374999999999998,
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
      "chassis",
      "battery",
      "wheel-lf",
      "wheel-lm",
      "wheel-lr",
      "wheel-rf",
      "wheel-rm",
      "wheel-rr",
      "sample-arm",
      "sensor-mast"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 库存核算（h3-orbital-service-rover-inventory）

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

### 子装配边界（h3-orbital-service-rover-boundary）

隔离 battery 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["battery-lock"]
- B：[]
- C：["battery-lock","wheel-lf-axle","wheel-lm-axle","wheel-lr-axle","wheel-rf-axle","wheel-rm-axle","wheel-rr-axle","arm-shoulder","mast-turntable"]
- D：["arm-shoulder"]

```json
{
  "input": {
    "joints": [
      {
        "id": "battery-lock",
        "name": "Battery locking pins",
        "type": "fixed",
        "parent": "chassis",
        "child": "battery",
        "anchorParent": [
          0,
          -1.225,
          5.644822903061214
        ],
        "anchorChild": [
          0,
          0,
          -0.1375
        ]
      },
      {
        "id": "wheel-lf-axle",
        "name": "wheel-lf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lf",
        "anchorParent": [
          -3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-lm-axle",
        "name": "wheel-lm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lm",
        "anchorParent": [
          -3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-lr-axle",
        "name": "wheel-lr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lr",
        "anchorParent": [
          -3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "wheel-rf-axle",
        "name": "wheel-rf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rf",
        "anchorParent": [
          3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-rm-axle",
        "name": "wheel-rm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rm",
        "anchorParent": [
          3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-rr-axle",
        "name": "wheel-rr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rr",
        "anchorParent": [
          3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "Arm shoulder hinge",
        "type": "revolute",
        "parent": "chassis",
        "child": "sample-arm",
        "anchorParent": [
          2.3,
          0.375,
          -1.155177096938786
        ],
        "anchorChild": [
          -1.2125000000000001,
          -2.057450054324738,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.2
        ]
      },
      {
        "id": "mast-turntable",
        "name": "Mast turntable",
        "type": "revolute",
        "parent": "chassis",
        "child": "sensor-mast",
        "anchorParent": [
          -1.3,
          0.575,
          -0.45517709693878605
        ],
        "anchorChild": [
          0,
          -1.7374999999999998,
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
    "target": "battery"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 最小干预（h3-orbital-service-rover-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：0

```json
{
  "input": {
    "module": "battery"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 全过程依赖（h3-orbital-service-rover-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：9
- B：0
- C：-1
- D：1

```json
{
  "input": {
    "order": [
      "wheel-lf",
      "chassis",
      "battery",
      "wheel-lm",
      "wheel-lr",
      "wheel-rf",
      "wheel-rm",
      "wheel-rr",
      "sensor-mast",
      "sample-arm"
    ],
    "joints": [
      {
        "id": "battery-lock",
        "name": "Battery locking pins",
        "type": "fixed",
        "parent": "chassis",
        "child": "battery",
        "anchorParent": [
          0,
          -1.225,
          5.644822903061214
        ],
        "anchorChild": [
          0,
          0,
          -0.1375
        ]
      },
      {
        "id": "wheel-lf-axle",
        "name": "wheel-lf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lf",
        "anchorParent": [
          -3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-lm-axle",
        "name": "wheel-lm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lm",
        "anchorParent": [
          -3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-lr-axle",
        "name": "wheel-lr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lr",
        "anchorParent": [
          -3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "wheel-rf-axle",
        "name": "wheel-rf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rf",
        "anchorParent": [
          3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-rm-axle",
        "name": "wheel-rm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rm",
        "anchorParent": [
          3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-rr-axle",
        "name": "wheel-rr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rr",
        "anchorParent": [
          3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "Arm shoulder hinge",
        "type": "revolute",
        "parent": "chassis",
        "child": "sample-arm",
        "anchorParent": [
          2.3,
          0.375,
          -1.155177096938786
        ],
        "anchorChild": [
          -1.2125000000000001,
          -2.057450054324738,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.2
        ]
      },
      {
        "id": "mast-turntable",
        "name": "Mast turntable",
        "type": "revolute",
        "parent": "chassis",
        "child": "sensor-mast",
        "anchorParent": [
          -1.3,
          0.575,
          -0.45517709693878605
        ],
        "anchorChild": [
          0,
          -1.7374999999999998,
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

### 连续维修路径（h3-orbital-service-rover-access）

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
          9.125,
          1.4,
          5.4375
        ],
        "end": [
          0,
          1.4,
          5.4375
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
          11.514900108649476,
          5.4375
        ],
        "end": [
          0,
          1.4,
          5.4375
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
          1.4,
          10.175
        ],
        "end": [
          0,
          1.4,
          5.4375
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

### 支撑反事实（h3-orbital-service-rover-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["chassis","battery","wheel-lf","wheel-lm","wheel-lr","wheel-rf","wheel-rm","wheel-rr","sample-arm","sensor-mast"]
- B：[]
- C：["battery"]

```json
{
  "input": {
    "removed": "battery",
    "roots": [
      "chassis"
    ],
    "joints": [
      {
        "id": "battery-lock",
        "name": "Battery locking pins",
        "type": "fixed",
        "parent": "chassis",
        "child": "battery",
        "anchorParent": [
          0,
          -1.225,
          5.644822903061214
        ],
        "anchorChild": [
          0,
          0,
          -0.1375
        ]
      },
      {
        "id": "wheel-lf-axle",
        "name": "wheel-lf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lf",
        "anchorParent": [
          -3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-lm-axle",
        "name": "wheel-lm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lm",
        "anchorParent": [
          -3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-lr-axle",
        "name": "wheel-lr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lr",
        "anchorParent": [
          -3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "wheel-rf-axle",
        "name": "wheel-rf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rf",
        "anchorParent": [
          3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-rm-axle",
        "name": "wheel-rm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rm",
        "anchorParent": [
          3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-rr-axle",
        "name": "wheel-rr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rr",
        "anchorParent": [
          3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "Arm shoulder hinge",
        "type": "revolute",
        "parent": "chassis",
        "child": "sample-arm",
        "anchorParent": [
          2.3,
          0.375,
          -1.155177096938786
        ],
        "anchorChild": [
          -1.2125000000000001,
          -2.057450054324738,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.2
        ]
      },
      {
        "id": "mast-turntable",
        "name": "Mast turntable",
        "type": "revolute",
        "parent": "chassis",
        "child": "sensor-mast",
        "anchorParent": [
          -1.3,
          0.575,
          -0.45517709693878605
        ],
        "anchorChild": [
          0,
          -1.7374999999999998,
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
      "chassis",
      "battery",
      "wheel-lf",
      "wheel-lm",
      "wheel-lr",
      "wheel-rf",
      "wheel-rm",
      "wheel-rr",
      "sample-arm",
      "sensor-mast"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 冲击响应读数（h3-orbital-service-rover-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.2204
- B：0
- C：1.0204
- D：0.0204

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.020376059626404163
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.001253883655302942
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.00002735586974129204
      },
      {
        "time": 0.30833333333333335,
        "displacement": 4.76837158203125e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 4.76837158203125e-7
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
    "nominalDrift": 0.0004458205897280736,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节限位推理（h3-orbital-service-rover-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-0.7
- B：1.7
- C：-0.2
- D：0.5

```json
{
  "input": {
    "joint": "arm-shoulder",
    "limits": [
      -0.2,
      1.2
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

### 约束故障诊断（h3-orbital-service-rover-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：wheel-lm-axle
- B：arm-shoulder
- C：battery-lock
- D：wheel-lf-axle

```json
{
  "input": {
    "endpoints": [
      "chassis",
      "sample-arm"
    ],
    "type": "revolute",
    "joints": [
      {
        "id": "battery-lock",
        "name": "Battery locking pins",
        "type": "fixed",
        "parent": "chassis",
        "child": "battery",
        "anchorParent": [
          0,
          -1.225,
          5.644822903061214
        ],
        "anchorChild": [
          0,
          0,
          -0.1375
        ]
      },
      {
        "id": "wheel-lf-axle",
        "name": "wheel-lf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lf",
        "anchorParent": [
          -3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-lm-axle",
        "name": "wheel-lm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lm",
        "anchorParent": [
          -3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-lr-axle",
        "name": "wheel-lr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-lr",
        "anchorParent": [
          -3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "wheel-rf-axle",
        "name": "wheel-rf axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rf",
        "anchorParent": [
          3.75,
          -1.625,
          -2.655177096938786
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
        ]
      },
      {
        "id": "wheel-rm-axle",
        "name": "wheel-rm axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rm",
        "anchorParent": [
          3.75,
          -1.625,
          0.344822903061214
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
        ]
      },
      {
        "id": "wheel-rr-axle",
        "name": "wheel-rr axle",
        "type": "revolute",
        "parent": "chassis",
        "child": "wheel-rr",
        "anchorParent": [
          3.75,
          -1.625,
          3.344822903061214
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
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "Arm shoulder hinge",
        "type": "revolute",
        "parent": "chassis",
        "child": "sample-arm",
        "anchorParent": [
          2.3,
          0.375,
          -1.155177096938786
        ],
        "anchorChild": [
          -1.2125000000000001,
          -2.057450054324738,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.2
        ]
      },
      {
        "id": "mast-turntable",
        "name": "Mast turntable",
        "type": "revolute",
        "parent": "chassis",
        "child": "sensor-mast",
        "anchorParent": [
          -1.3,
          0.575,
          -0.45517709693878605
        ],
        "anchorChild": [
          0,
          -1.7374999999999998,
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
      "B"
    ]
  }
}
```

### 主动检查收益（h3-orbital-service-rover-information-gain）

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

### 不确定性与弃答（h3-orbital-service-rover-abstention）

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

### 观测后信念更新（h3-orbital-service-rover-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0
- C：0.25
- D：0.3333333333333333

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
    "choiceId": "B"
  }
}
```

### 多目标工程权衡（h3-orbital-service-rover-pareto）

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
        "cost": 7,
        "stiffness": 6,
        "mass": 0.7
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 10,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 6,
        "stiffness": 7,
        "mass": 0.9
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 11,
        "mass": 1.6
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

### 依赖装配（h3-orbital-service-rover-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:wheel-rr",
        "label": "安装 wheel-rr",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:wheel-rr"
        ],
        "adds": [
          "present:wheel-rr"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr",
          "visible": true
        }
      },
      {
        "id": "place:wheel-rm",
        "label": "安装 wheel-rm",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:wheel-rm"
        ],
        "adds": [
          "present:wheel-rm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rm",
          "visible": true
        }
      },
      {
        "id": "place:wheel-lm",
        "label": "安装 wheel-lm",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:wheel-lm"
        ],
        "adds": [
          "present:wheel-lm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-lm",
          "visible": true
        }
      },
      {
        "id": "place:battery",
        "label": "安装 battery",
        "requires": [
          "present:chassis"
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
        "id": "place:sample-arm",
        "label": "安装 sample-arm",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:sample-arm"
        ],
        "adds": [
          "present:sample-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm",
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
        "id": "place:wheel-lr",
        "label": "安装 wheel-lr",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:wheel-lr"
        ],
        "adds": [
          "present:wheel-lr"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-lr",
          "visible": true
        }
      },
      {
        "id": "place:wheel-rf",
        "label": "安装 wheel-rf",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:wheel-rf"
        ],
        "adds": [
          "present:wheel-rf"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rf",
          "visible": true
        }
      },
      {
        "id": "place:wheel-lf",
        "label": "安装 wheel-lf",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:wheel-lf"
        ],
        "adds": [
          "present:wheel-lf"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-lf",
          "visible": true
        }
      },
      {
        "id": "place:sensor-mast",
        "label": "安装 sensor-mast",
        "requires": [
          "present:chassis"
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
      }
    ],
    "goalFacts": [
      "present:chassis",
      "present:battery",
      "present:wheel-lf",
      "present:wheel-lm",
      "present:wheel-lr",
      "present:wheel-rf",
      "present:wheel-rm",
      "present:wheel-rr",
      "present:sensor-mast",
      "present:sample-arm"
    ],
    "budget": 10,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:chassis",
      "place:wheel-rr",
      "place:wheel-rm",
      "place:wheel-lm",
      "place:battery",
      "place:sample-arm",
      "place:wheel-lr",
      "place:wheel-rf",
      "place:wheel-lf",
      "place:sensor-mast"
    ]
  }
}
```

### 依赖拆解（h3-orbital-service-rover-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:chassis",
      "present:battery",
      "present:wheel-lf",
      "present:wheel-lm",
      "present:wheel-lr",
      "present:wheel-rf",
      "present:wheel-rm",
      "present:wheel-rr",
      "present:sample-arm",
      "present:sensor-mast"
    ],
    "initialModules": [
      "chassis",
      "battery",
      "wheel-lf",
      "wheel-lm",
      "wheel-lr",
      "wheel-rf",
      "wheel-rm",
      "wheel-rr",
      "sample-arm",
      "sensor-mast"
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
        "id": "remove:wheel-lr",
        "label": "拆除 wheel-lr",
        "requires": [
          "present:wheel-lr"
        ],
        "forbids": [],
        "adds": [
          "removed:wheel-lr"
        ],
        "deletes": [
          "present:wheel-lr"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-lr",
          "visible": false
        }
      },
      {
        "id": "remove:wheel-rf",
        "label": "拆除 wheel-rf",
        "requires": [
          "present:wheel-rf"
        ],
        "forbids": [],
        "adds": [
          "removed:wheel-rf"
        ],
        "deletes": [
          "present:wheel-rf"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rf",
          "visible": false
        }
      },
      {
        "id": "remove:wheel-lf",
        "label": "拆除 wheel-lf",
        "requires": [
          "present:wheel-lf"
        ],
        "forbids": [],
        "adds": [
          "removed:wheel-lf"
        ],
        "deletes": [
          "present:wheel-lf"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-lf",
          "visible": false
        }
      },
      {
        "id": "remove:wheel-rm",
        "label": "拆除 wheel-rm",
        "requires": [
          "present:wheel-rm"
        ],
        "forbids": [],
        "adds": [
          "removed:wheel-rm"
        ],
        "deletes": [
          "present:wheel-rm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rm",
          "visible": false
        }
      },
      {
        "id": "remove:wheel-rr",
        "label": "拆除 wheel-rr",
        "requires": [
          "present:wheel-rr"
        ],
        "forbids": [],
        "adds": [
          "removed:wheel-rr"
        ],
        "deletes": [
          "present:wheel-rr"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr",
          "visible": false
        }
      },
      {
        "id": "remove:sample-arm",
        "label": "拆除 sample-arm",
        "requires": [
          "present:sample-arm"
        ],
        "forbids": [],
        "adds": [
          "removed:sample-arm"
        ],
        "deletes": [
          "present:sample-arm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm",
          "visible": false
        }
      },
      {
        "id": "remove:wheel-lm",
        "label": "拆除 wheel-lm",
        "requires": [
          "present:wheel-lm"
        ],
        "forbids": [],
        "adds": [
          "removed:wheel-lm"
        ],
        "deletes": [
          "present:wheel-lm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-lm",
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
        "id": "remove:chassis",
        "label": "拆除 chassis",
        "requires": [
          "present:chassis"
        ],
        "forbids": [
          "present:battery",
          "present:wheel-lf",
          "present:wheel-lm",
          "present:wheel-lr",
          "present:wheel-rf",
          "present:wheel-rm",
          "present:wheel-rr",
          "present:sample-arm",
          "present:sensor-mast"
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
      }
    ],
    "goalFacts": [
      "removed:sample-arm",
      "removed:sensor-mast",
      "removed:wheel-rr",
      "removed:wheel-rm",
      "removed:wheel-rf",
      "removed:wheel-lr",
      "removed:wheel-lm",
      "removed:wheel-lf",
      "removed:battery",
      "removed:chassis"
    ],
    "budget": 10,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:battery",
      "remove:wheel-lr",
      "remove:wheel-rf",
      "remove:wheel-lf",
      "remove:wheel-rm",
      "remove:wheel-rr",
      "remove:sample-arm",
      "remove:wheel-lm",
      "remove:sensor-mast",
      "remove:chassis"
    ]
  }
}
```

### 承载维修（h3-orbital-service-rover-service-repair）

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
      "chassis",
      "battery",
      "wheel-lf",
      "wheel-lm",
      "wheel-lr",
      "wheel-rf",
      "wheel-rm",
      "wheel-rr",
      "sample-arm",
      "sensor-mast"
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

### 复合编辑验证（h3-orbital-service-rover-compound-edit）

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
      "chassis",
      "battery",
      "wheel-lf",
      "wheel-lm",
      "wheel-lr",
      "wheel-rf",
      "wheel-rm",
      "wheel-rr",
      "sample-arm",
      "sensor-mast"
    ],
    "actions": [
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

### 跨区域联合维修（h3-orbital-service-rover-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:wheel-rr",
      "closed:wheel-rr",
      "fault:sample-arm",
      "closed:sample-arm",
      "fault:sensor-mast",
      "closed:sensor-mast"
    ],
    "initialModules": [
      "chassis",
      "battery",
      "wheel-lf",
      "wheel-lm",
      "wheel-lr",
      "wheel-rf",
      "wheel-rm",
      "wheel-rr",
      "sample-arm",
      "sensor-mast"
    ],
    "actions": [
      {
        "id": "verify:wheel-rr",
        "label": "verify wheel-rr",
        "requires": [
          "done:replace:wheel-rr"
        ],
        "forbids": [
          "done:verify:wheel-rr"
        ],
        "adds": [
          "done:verify:wheel-rr"
        ],
        "deletes": [
          "fault:wheel-rr"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr"
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
        "id": "open:sample-arm",
        "label": "open sample-arm",
        "requires": [
          "done:support:sample-arm"
        ],
        "forbids": [
          "done:open:sample-arm"
        ],
        "adds": [
          "done:open:sample-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm"
        }
      },
      {
        "id": "replace:sample-arm",
        "label": "replace sample-arm",
        "requires": [
          "done:remove:sample-arm"
        ],
        "forbids": [
          "done:replace:sample-arm"
        ],
        "adds": [
          "done:replace:sample-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm",
          "visible": true
        }
      },
      {
        "id": "close:wheel-rr",
        "label": "close wheel-rr",
        "requires": [
          "done:verify:wheel-rr"
        ],
        "forbids": [
          "done:close:wheel-rr"
        ],
        "adds": [
          "done:close:wheel-rr"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr"
        }
      },
      {
        "id": "support:wheel-rr",
        "label": "support wheel-rr",
        "requires": [
          "fault:wheel-rr"
        ],
        "forbids": [
          "done:support:wheel-rr"
        ],
        "adds": [
          "done:support:wheel-rr"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr"
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
        "id": "open:wheel-rr",
        "label": "open wheel-rr",
        "requires": [
          "done:support:wheel-rr"
        ],
        "forbids": [
          "done:open:wheel-rr"
        ],
        "adds": [
          "done:open:wheel-rr"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr"
        }
      },
      {
        "id": "support:sample-arm",
        "label": "support sample-arm",
        "requires": [
          "fault:sample-arm"
        ],
        "forbids": [
          "done:support:sample-arm"
        ],
        "adds": [
          "done:support:sample-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm"
        }
      },
      {
        "id": "verify:sample-arm",
        "label": "verify sample-arm",
        "requires": [
          "done:replace:sample-arm"
        ],
        "forbids": [
          "done:verify:sample-arm"
        ],
        "adds": [
          "done:verify:sample-arm"
        ],
        "deletes": [
          "fault:sample-arm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm"
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
        "id": "replace:wheel-rr",
        "label": "replace wheel-rr",
        "requires": [
          "done:remove:wheel-rr"
        ],
        "forbids": [
          "done:replace:wheel-rr"
        ],
        "adds": [
          "done:replace:wheel-rr"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr",
          "visible": true
        }
      },
      {
        "id": "remove:wheel-rr",
        "label": "remove wheel-rr",
        "requires": [
          "done:open:wheel-rr"
        ],
        "forbids": [
          "done:remove:wheel-rr"
        ],
        "adds": [
          "done:remove:wheel-rr"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr",
          "visible": false
        }
      },
      {
        "id": "remove:sample-arm",
        "label": "remove sample-arm",
        "requires": [
          "done:open:sample-arm"
        ],
        "forbids": [
          "done:remove:sample-arm"
        ],
        "adds": [
          "done:remove:sample-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm",
          "visible": false
        }
      },
      {
        "id": "close:sample-arm",
        "label": "close sample-arm",
        "requires": [
          "done:verify:sample-arm"
        ],
        "forbids": [
          "done:close:sample-arm"
        ],
        "adds": [
          "done:close:sample-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm"
        }
      },
      {
        "id": "release:wheel-rr",
        "label": "release wheel-rr",
        "requires": [
          "done:close:wheel-rr"
        ],
        "forbids": [
          "done:release:wheel-rr"
        ],
        "adds": [
          "done:release:wheel-rr",
          "repaired:wheel-rr"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr"
        }
      },
      {
        "id": "release:sample-arm",
        "label": "release sample-arm",
        "requires": [
          "done:close:sample-arm"
        ],
        "forbids": [
          "done:release:sample-arm"
        ],
        "adds": [
          "done:release:sample-arm",
          "repaired:sample-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm"
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
      }
    ],
    "goalFacts": [
      "repaired:wheel-rr",
      "repaired:sample-arm",
      "repaired:sensor-mast"
    ],
    "budget": 21,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:wheel-rr",
      "open:wheel-rr",
      "support:sample-arm",
      "open:sample-arm",
      "support:sensor-mast",
      "remove:wheel-rr",
      "replace:wheel-rr",
      "verify:wheel-rr",
      "close:wheel-rr",
      "remove:sample-arm",
      "replace:sample-arm",
      "verify:sample-arm",
      "close:sample-arm",
      "release:wheel-rr",
      "release:sample-arm",
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

### 多工位资源调度（h3-orbital-service-rover-scheduling）

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
        "module": "battery",
        "duration": 1,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "wheel-lf",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "wheel-lm",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "wheel-lr",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "wheel-rf",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      },
      {
        "id": "job-6",
        "module": "wheel-rm",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-4"
        ]
      },
      {
        "id": "job-7",
        "module": "wheel-rr",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-5"
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
      "job-3": 1,
      "job-4": 2,
      "job-5": 2,
      "job-6": 4,
      "job-7": 3
    }
  }
}
```

### 检查后条件策略（h3-orbital-service-rover-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "battery",
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

### 局部坐标变换（h3-orbital-service-rover-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[1,0,-0.1375]
- B：[1,1.4,5.3]
- C：[0,2.4,6.575]
- D：[-1,1.4,5.575]

```json
{
  "input": {
    "localPoint": [
      1,
      0,
      -0.1375
    ],
    "rotationXYZW": [
      0,
      1,
      0,
      6.123233995736766e-17
    ],
    "translation": [
      0,
      1.4,
      5.4375
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 正交视图投影（h3-orbital-service-rover-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[-5,9]
- B：[9,4]
- C：[4,5]
- D：[0,0]

```json
{
  "input": {
    "view": "side",
    "point": [
      4,
      9,
      -5
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 空间相对关系（h3-orbital-service-rover-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：equal
- B：greater
- C：less

```json
{
  "input": {
    "A": {
      "id": "chassis",
      "position": [
        0,
        2.625,
        -0.344822903061214
      ]
    },
    "B": {
      "id": "sensor-mast",
      "position": [
        -1.3,
        4.9375,
        -0.8
      ]
    },
    "axis": "y"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 约束自由度（h3-orbital-service-rover-joint-axis）

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
      "id": "wheel-lf-axle",
      "name": "wheel-lf axle",
      "type": "revolute",
      "parent": "chassis",
      "child": "wheel-lf",
      "anchorParent": [
        -3.75,
        -1.625,
        -2.655177096938786
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
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 维修间隙预算（h3-orbital-service-rover-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "battery",
    "aperture": 0.6,
    "toolWidth": 0.55,
    "eachSideMargin": 0.05
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-orbital-service-rover-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,-9]
- B：[0,0,9]
- C：[0,0,0]
- D：[0,-3,0]

```json
{
  "input": {
    "module": "battery",
    "lever": [
      3,
      2,
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
    "choiceId": "A"
  }
}
```

### 非均匀先验更新（h3-orbital-service-rover-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.3333333333333333
- B：0
- C：1
- D：0.6

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
      4
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

### 风险最小决策（h3-orbital-service-rover-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.3,
    "repairCost": 5,
    "failureLoss": 13,
    "module": "battery"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-orbital-service-rover-trace-threshold）

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
        "displacement": 0.020376059626404163
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.001253883655302942
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.00002735586974129204
      },
      {
        "time": 0.30833333333333335,
        "displacement": 4.76837158203125e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 4.76837158203125e-7
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
    "threshold": 0.01630084770112333
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-orbital-service-rover-guarded-repair）

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
      "chassis",
      "battery",
      "wheel-lf",
      "wheel-lm",
      "wheel-lr",
      "wheel-rf",
      "wheel-rm",
      "wheel-rr",
      "sample-arm",
      "sensor-mast"
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

### 失败状态回退（h3-orbital-service-rover-rollback）

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
      "chassis",
      "battery",
      "wheel-lf",
      "wheel-lm",
      "wheel-lr",
      "wheel-rf",
      "wheel-rm",
      "wheel-rr",
      "sample-arm",
      "sensor-mast"
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

### 共享工具协同维修（h3-orbital-service-rover-resource-repair）

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
        "id": "release:sample-arm",
        "label": "release sample-arm",
        "requires": [
          "done:relock:sample-arm"
        ],
        "forbids": [
          "done:release:sample-arm"
        ],
        "adds": [
          "done:release:sample-arm",
          "ready:sample-arm",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm"
        }
      },
      {
        "id": "relock:sample-arm",
        "label": "relock sample-arm",
        "requires": [
          "done:verify:sample-arm"
        ],
        "forbids": [
          "done:relock:sample-arm"
        ],
        "adds": [
          "done:relock:sample-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm"
        }
      },
      {
        "id": "verify:sample-arm",
        "label": "verify sample-arm",
        "requires": [
          "done:replace:sample-arm"
        ],
        "forbids": [
          "done:verify:sample-arm"
        ],
        "adds": [
          "done:verify:sample-arm"
        ],
        "deletes": [
          "fault:sample-arm",
          "misaligned:sample-arm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm"
        }
      },
      {
        "id": "replace:sample-arm",
        "label": "replace sample-arm",
        "requires": [
          "done:unlock:sample-arm"
        ],
        "forbids": [
          "done:replace:sample-arm"
        ],
        "adds": [
          "done:replace:sample-arm"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "sample-arm"
        }
      },
      {
        "id": "unlock:sample-arm",
        "label": "unlock sample-arm",
        "requires": [
          "done:support:sample-arm"
        ],
        "forbids": [
          "done:unlock:sample-arm"
        ],
        "adds": [
          "done:unlock:sample-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm"
        }
      },
      {
        "id": "support:sample-arm",
        "label": "support sample-arm",
        "requires": [
          "done:isolate:sample-arm"
        ],
        "forbids": [
          "done:support:sample-arm"
        ],
        "adds": [
          "done:support:sample-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm"
        }
      },
      {
        "id": "isolate:sample-arm",
        "label": "isolate sample-arm",
        "requires": [
          "tool:free",
          "fault:sample-arm"
        ],
        "forbids": [
          "done:isolate:sample-arm"
        ],
        "adds": [
          "done:isolate:sample-arm"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sample-arm"
        }
      },
      {
        "id": "release:wheel-rr",
        "label": "release wheel-rr",
        "requires": [
          "done:relock:wheel-rr"
        ],
        "forbids": [
          "done:release:wheel-rr"
        ],
        "adds": [
          "done:release:wheel-rr",
          "ready:wheel-rr",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr"
        }
      },
      {
        "id": "relock:wheel-rr",
        "label": "relock wheel-rr",
        "requires": [
          "done:verify:wheel-rr"
        ],
        "forbids": [
          "done:relock:wheel-rr"
        ],
        "adds": [
          "done:relock:wheel-rr"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr"
        }
      },
      {
        "id": "verify:wheel-rr",
        "label": "verify wheel-rr",
        "requires": [
          "done:replace:wheel-rr"
        ],
        "forbids": [
          "done:verify:wheel-rr"
        ],
        "adds": [
          "done:verify:wheel-rr"
        ],
        "deletes": [
          "fault:wheel-rr",
          "misaligned:wheel-rr"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr"
        }
      },
      {
        "id": "replace:wheel-rr",
        "label": "replace wheel-rr",
        "requires": [
          "done:unlock:wheel-rr"
        ],
        "forbids": [
          "done:replace:wheel-rr"
        ],
        "adds": [
          "done:replace:wheel-rr"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "wheel-rr"
        }
      },
      {
        "id": "unlock:wheel-rr",
        "label": "unlock wheel-rr",
        "requires": [
          "done:support:wheel-rr"
        ],
        "forbids": [
          "done:unlock:wheel-rr"
        ],
        "adds": [
          "done:unlock:wheel-rr"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr"
        }
      },
      {
        "id": "support:wheel-rr",
        "label": "support wheel-rr",
        "requires": [
          "done:isolate:wheel-rr"
        ],
        "forbids": [
          "done:support:wheel-rr"
        ],
        "adds": [
          "done:support:wheel-rr"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr"
        }
      },
      {
        "id": "isolate:wheel-rr",
        "label": "isolate wheel-rr",
        "requires": [
          "tool:free",
          "fault:wheel-rr"
        ],
        "forbids": [
          "done:isolate:wheel-rr"
        ],
        "adds": [
          "done:isolate:wheel-rr"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rr"
        }
      },
      {
        "id": "release:wheel-rm",
        "label": "release wheel-rm",
        "requires": [
          "done:relock:wheel-rm"
        ],
        "forbids": [
          "done:release:wheel-rm"
        ],
        "adds": [
          "done:release:wheel-rm",
          "ready:wheel-rm",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rm"
        }
      },
      {
        "id": "relock:wheel-rm",
        "label": "relock wheel-rm",
        "requires": [
          "done:verify:wheel-rm"
        ],
        "forbids": [
          "done:relock:wheel-rm"
        ],
        "adds": [
          "done:relock:wheel-rm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rm"
        }
      },
      {
        "id": "verify:wheel-rm",
        "label": "verify wheel-rm",
        "requires": [
          "done:replace:wheel-rm"
        ],
        "forbids": [
          "done:verify:wheel-rm"
        ],
        "adds": [
          "done:verify:wheel-rm"
        ],
        "deletes": [
          "fault:wheel-rm",
          "misaligned:wheel-rm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rm"
        }
      },
      {
        "id": "replace:wheel-rm",
        "label": "replace wheel-rm",
        "requires": [
          "done:unlock:wheel-rm"
        ],
        "forbids": [
          "done:replace:wheel-rm"
        ],
        "adds": [
          "done:replace:wheel-rm"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "wheel-rm"
        }
      },
      {
        "id": "unlock:wheel-rm",
        "label": "unlock wheel-rm",
        "requires": [
          "done:support:wheel-rm"
        ],
        "forbids": [
          "done:unlock:wheel-rm"
        ],
        "adds": [
          "done:unlock:wheel-rm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rm"
        }
      },
      {
        "id": "support:wheel-rm",
        "label": "support wheel-rm",
        "requires": [
          "done:isolate:wheel-rm"
        ],
        "forbids": [
          "done:support:wheel-rm"
        ],
        "adds": [
          "done:support:wheel-rm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rm"
        }
      },
      {
        "id": "isolate:wheel-rm",
        "label": "isolate wheel-rm",
        "requires": [
          "tool:free",
          "fault:wheel-rm"
        ],
        "forbids": [
          "done:isolate:wheel-rm"
        ],
        "adds": [
          "done:isolate:wheel-rm"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "wheel-rm"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:wheel-rm",
      "fault:wheel-rr",
      "fault:sample-arm",
      "fault:sensor-mast"
    ],
    "initialModules": [
      "chassis",
      "battery",
      "wheel-lf",
      "wheel-lm",
      "wheel-lr",
      "wheel-rf",
      "wheel-rm",
      "wheel-rr",
      "sample-arm",
      "sensor-mast"
    ],
    "goalFacts": [
      "ready:wheel-rm",
      "ready:wheel-rr",
      "ready:sample-arm",
      "ready:sensor-mast"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
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
      "isolate:sample-arm",
      "support:sample-arm",
      "unlock:sample-arm",
      "replace:sample-arm",
      "verify:sample-arm",
      "relock:sample-arm",
      "release:sample-arm",
      "isolate:wheel-rr",
      "support:wheel-rr",
      "unlock:wheel-rr",
      "replace:wheel-rr",
      "verify:wheel-rr",
      "relock:wheel-rr",
      "release:wheel-rr",
      "isolate:wheel-rm",
      "support:wheel-rm",
      "unlock:wheel-rm",
      "replace:wheel-rm",
      "verify:wheel-rm",
      "relock:wheel-rm",
      "release:wheel-rm"
    ]
  }
}
```

### 预算约束检查策略（h3-orbital-service-rover-budget-policy）

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
