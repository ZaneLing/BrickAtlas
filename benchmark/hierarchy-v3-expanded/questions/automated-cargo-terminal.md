## D4 自动化货运终端

### 模块识别（h3-automated-cargo-terminal-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：rack-b
- B：lift
- C：floor
- D：rack-a

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "floor",
        "name": "Automated terminal floor"
      },
      {
        "id": "rack-a",
        "name": "West storage rack"
      },
      {
        "id": "rack-b",
        "name": "East storage rack"
      },
      {
        "id": "conveyor-a",
        "name": "Inbound conveyor"
      },
      {
        "id": "conveyor-b",
        "name": "Outbound conveyor"
      },
      {
        "id": "gantry",
        "name": "Overhead transfer gantry"
      },
      {
        "id": "shuttle",
        "name": "Gantry shuttle"
      },
      {
        "id": "lift",
        "name": "Vertical transfer lift"
      },
      {
        "id": "robot-a",
        "name": "West sorting robot"
      },
      {
        "id": "robot-b",
        "name": "East sorting robot"
      },
      {
        "id": "container-red",
        "name": "container red"
      },
      {
        "id": "container-blue",
        "name": "container blue"
      },
      {
        "id": "container-yellow",
        "name": "container yellow"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 部件计数（h3-automated-cargo-terminal-count）

模块 lift 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：12
- B：16
- C：13
- D：14

```json
{
  "input": {
    "parts": [
      {
        "id": "h0001",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0002",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0003",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0004",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0005",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0006",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0007",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0008",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0009",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0010",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0011",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0012",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0013",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0014",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0015",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0016",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0017",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0018",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0019",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0020",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0021",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0022",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0023",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0024",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0025",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0026",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0027",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0028",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0029",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0030",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0031",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0032",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0033",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0034",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0035",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0036",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0037",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0038",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0039",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0040",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0041",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0042",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0043",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0044",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0045",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0046",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0047",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0048",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0049",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0050",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0051",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0052",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0053",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0054",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0055",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0056",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0057",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0058",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0059",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0060",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0061",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0062",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0063",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0064",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0065",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0066",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0067",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0068",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0069",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0070",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0071",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0072",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0073",
        "moduleId": "rack-a",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0074",
        "moduleId": "rack-a",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "h0075",
        "moduleId": "rack-a",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0076",
        "moduleId": "rack-a",
        "shape": "panel",
        "color": "#e8792e"
      },
      {
        "id": "h0077",
        "moduleId": "rack-a",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0078",
        "moduleId": "rack-a",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "h0079",
        "moduleId": "rack-a",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0080",
        "moduleId": "rack-a",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "h0081",
        "moduleId": "rack-a",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0082",
        "moduleId": "rack-a",
        "shape": "panel",
        "color": "#e8792e"
      },
      {
        "id": "h0083",
        "moduleId": "rack-a",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0084",
        "moduleId": "rack-a",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "h0085",
        "moduleId": "rack-a",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0086",
        "moduleId": "rack-a",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "h0087",
        "moduleId": "rack-a",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0088",
        "moduleId": "rack-a",
        "shape": "panel",
        "color": "#e8792e"
      },
      {
        "id": "h0089",
        "moduleId": "rack-a",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0090",
        "moduleId": "rack-a",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "h0091",
        "moduleId": "rack-b",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0092",
        "moduleId": "rack-b",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "h0093",
        "moduleId": "rack-b",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0094",
        "moduleId": "rack-b",
        "shape": "panel",
        "color": "#e8792e"
      },
      {
        "id": "h0095",
        "moduleId": "rack-b",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0096",
        "moduleId": "rack-b",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "h0097",
        "moduleId": "rack-b",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0098",
        "moduleId": "rack-b",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "h0099",
        "moduleId": "rack-b",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0100",
        "moduleId": "rack-b",
        "shape": "panel",
        "color": "#e8792e"
      },
      {
        "id": "h0101",
        "moduleId": "rack-b",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0102",
        "moduleId": "rack-b",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "h0103",
        "moduleId": "rack-b",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0104",
        "moduleId": "rack-b",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "h0105",
        "moduleId": "rack-b",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0106",
        "moduleId": "rack-b",
        "shape": "panel",
        "color": "#e8792e"
      },
      {
        "id": "h0107",
        "moduleId": "rack-b",
        "shape": "beam",
        "color": "#173b63"
      },
      {
        "id": "h0108",
        "moduleId": "rack-b",
        "shape": "panel",
        "color": "#f2bf3c"
      },
      {
        "id": "h0109",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0110",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0111",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0112",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0113",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0114",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0115",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0116",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0117",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0118",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0119",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0120",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0121",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0122",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0123",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0124",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0125",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0126",
        "moduleId": "conveyor-a",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0127",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0128",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0129",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0130",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0131",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0132",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0133",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0134",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0135",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0136",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0137",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0138",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0139",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0140",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0141",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0142",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0143",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0144",
        "moduleId": "conveyor-b",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0145",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0146",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0147",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0148",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0149",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0150",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0151",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0152",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0153",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0154",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0155",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0156",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0157",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0158",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0159",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0160",
        "moduleId": "gantry",
        "shape": "brick",
        "color": "#f2bf3c"
      },
      {
        "id": "h0161",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0162",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0163",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0164",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0165",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0166",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0167",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0168",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0169",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0170",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0171",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0172",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0173",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0174",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0175",
        "moduleId": "shuttle",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0176",
        "moduleId": "shuttle",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0177",
        "moduleId": "shuttle",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0178",
        "moduleId": "shuttle",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0179",
        "moduleId": "shuttle",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0180",
        "moduleId": "shuttle",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0181",
        "moduleId": "lift",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0182",
        "moduleId": "lift",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0183",
        "moduleId": "lift",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0184",
        "moduleId": "lift",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0185",
        "moduleId": "lift",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0186",
        "moduleId": "lift",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0187",
        "moduleId": "lift",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0188",
        "moduleId": "lift",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0189",
        "moduleId": "lift",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0190",
        "moduleId": "lift",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0191",
        "moduleId": "lift",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0192",
        "moduleId": "lift",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0193",
        "moduleId": "lift",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0194",
        "moduleId": "robot-a",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0195",
        "moduleId": "robot-a",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0196",
        "moduleId": "robot-a",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0197",
        "moduleId": "robot-a",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0198",
        "moduleId": "robot-a",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0199",
        "moduleId": "robot-a",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0200",
        "moduleId": "robot-a",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0201",
        "moduleId": "robot-b",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0202",
        "moduleId": "robot-b",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0203",
        "moduleId": "robot-b",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0204",
        "moduleId": "robot-b",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0205",
        "moduleId": "robot-b",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0206",
        "moduleId": "robot-b",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0207",
        "moduleId": "robot-b",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0208",
        "moduleId": "container-red",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0209",
        "moduleId": "container-red",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0210",
        "moduleId": "container-red",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0211",
        "moduleId": "container-red",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0212",
        "moduleId": "container-red",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0213",
        "moduleId": "container-red",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0214",
        "moduleId": "container-red",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0215",
        "moduleId": "container-red",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0216",
        "moduleId": "container-blue",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0217",
        "moduleId": "container-blue",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0218",
        "moduleId": "container-blue",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0219",
        "moduleId": "container-blue",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0220",
        "moduleId": "container-blue",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0221",
        "moduleId": "container-blue",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0222",
        "moduleId": "container-blue",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0223",
        "moduleId": "container-blue",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0224",
        "moduleId": "container-yellow",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0225",
        "moduleId": "container-yellow",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0226",
        "moduleId": "container-yellow",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0227",
        "moduleId": "container-yellow",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0228",
        "moduleId": "container-yellow",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0229",
        "moduleId": "container-yellow",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0230",
        "moduleId": "container-yellow",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0231",
        "moduleId": "container-yellow",
        "shape": "plate",
        "color": "#f2bf3c"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 颜色识别（h3-automated-cargo-terminal-color）

零件 h0181 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#d43a32
- B：#f2bf3c
- C：#edf1f2
- D：#2878b8

```json
{
  "input": {
    "part": {
      "id": "h0181",
      "moduleId": "lift",
      "shape": "plate",
      "size": [
        0.92,
        0.25,
        0.92
      ],
      "position": [
        -0.855,
        -1.6,
        -0.855
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
    "choiceId": "C"
  }
}
```

### 三维位置（h3-automated-cargo-terminal-position）

模块 lift 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[-6.7,2.8375,0]
- B：[6.7,2.8375,0]
- C：[-0.14500000000000002,2.8000000000000003,-0.14500000000000002]
- D：[0,0.2,0]

```json
{
  "input": {
    "centers": {
      "floor": [
        0,
        0.2,
        0
      ],
      "rack-a": [
        -6.7,
        2.8375,
        0
      ],
      "rack-b": [
        6.7,
        2.8375,
        0
      ],
      "conveyor-a": [
        0,
        0.75,
        -1.2
      ],
      "conveyor-b": [
        0,
        0.75,
        1.2
      ],
      "gantry": [
        0,
        3.55,
        0
      ],
      "shuttle": [
        0,
        6.749999999999999,
        0
      ],
      "lift": [
        -0.14500000000000002,
        2.8000000000000003,
        -0.14500000000000002
      ],
      "robot-a": [
        -1.9,
        2.75,
        0
      ],
      "robot-b": [
        1.9,
        2.75,
        0
      ],
      "container-red": [
        0,
        1.05,
        4
      ],
      "container-blue": [
        4,
        1.05,
        4
      ],
      "container-yellow": [
        8,
        1.05,
        4
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节类型（h3-automated-cargo-terminal-joint-type）

shuttle-slide 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：fixed
- B：revolute
- C：spring
- D：prismatic

```json
{
  "input": {
    "joint": {
      "id": "shuttle-slide",
      "name": "shuttle slide",
      "type": "prismatic",
      "parent": "gantry",
      "child": "shuttle",
      "anchorParent": [
        0,
        2.95,
        0
      ],
      "anchorChild": [
        0,
        -0.2499999999999991,
        0
      ],
      "axis": [
        1,
        0,
        0
      ],
      "limits": [
        -4.5,
        4.5
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 直接连接（h3-automated-cargo-terminal-parent）

lift 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["lift"]
- B：[]
- C：["floor","rack-a","rack-b","conveyor-a","conveyor-b","gantry","shuttle","lift","robot-a","robot-b","container-red","container-blue","container-yellow"]
- D：["shuttle"]

```json
{
  "input": {
    "joints": [
      {
        "id": "rack-a-feet",
        "name": "rack a feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-a",
        "anchorParent": [
          -6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rack-b-feet",
        "name": "rack b feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-b",
        "anchorParent": [
          6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "inbound-drive",
        "name": "inbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-a",
        "anchorParent": [
          0,
          0.49999999999999994,
          -1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "outbound-drive",
        "name": "outbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-b",
        "anchorParent": [
          0,
          0.49999999999999994,
          1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "floor",
        "child": "gantry",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -3.05,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shuttle-slide",
        "name": "shuttle slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "shuttle",
        "anchorParent": [
          0,
          2.95,
          0
        ],
        "anchorChild": [
          0,
          -0.2499999999999991,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4.5,
          4.5
        ]
      },
      {
        "id": "lift-slide",
        "name": "lift slide",
        "type": "prismatic",
        "parent": "shuttle",
        "child": "lift",
        "anchorParent": [
          0,
          -2.05,
          0
        ],
        "anchorChild": [
          0.14500000000000002,
          1.9,
          0.14500000000000002
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4,
          0
        ]
      },
      {
        "id": "robot-a-base",
        "name": "robot a base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-a",
        "anchorParent": [
          -2.5,
          0.8,
          0
        ],
        "anchorChild": [
          -0.6000000000000001,
          -1.75,
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
        "id": "robot-b-base",
        "name": "robot b base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-b",
        "anchorParent": [
          2.5,
          0.8,
          0
        ],
        "anchorChild": [
          0.6000000000000001,
          -1.75,
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
        "id": "container-0-lock",
        "name": "container 0 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-red",
        "anchorParent": [
          -1.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-1-lock",
        "name": "container 1 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-blue",
        "anchorParent": [
          2.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-2-lock",
        "name": "container 2 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-yellow",
        "anchorParent": [
          6.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
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

### 基座识别（h3-automated-cargo-terminal-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["floor"]
- B：[]
- C：["floor","rack-a","rack-b","conveyor-a","conveyor-b","gantry","shuttle","lift","robot-a","robot-b","container-red","container-blue","container-yellow"]
- D：["lift"]

```json
{
  "input": {
    "modules": [
      {
        "id": "floor",
        "name": "Automated terminal floor",
        "role": "foundation",
        "anchored": true,
        "mass": 70,
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
        "id": "rack-a",
        "name": "West storage rack",
        "role": "storage",
        "anchored": false,
        "mass": 14,
        "position": [
          -6.7,
          2.8375,
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
        "id": "rack-b",
        "name": "East storage rack",
        "role": "storage",
        "anchored": false,
        "mass": 14,
        "position": [
          6.7,
          2.8375,
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
        "id": "conveyor-a",
        "name": "Inbound conveyor",
        "role": "transport",
        "anchored": false,
        "mass": 6,
        "position": [
          0,
          0.75,
          -1.2
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "conveyor-b",
        "name": "Outbound conveyor",
        "role": "transport",
        "anchored": false,
        "mass": 6,
        "position": [
          0,
          0.75,
          1.2
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "gantry",
        "name": "Overhead transfer gantry",
        "role": "support",
        "anchored": false,
        "mass": 14,
        "position": [
          0,
          3.55,
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
        "id": "shuttle",
        "name": "Gantry shuttle",
        "role": "actuator",
        "anchored": false,
        "mass": 3,
        "position": [
          0,
          6.749999999999999,
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
        "id": "lift",
        "name": "Vertical transfer lift",
        "role": "service-module",
        "anchored": false,
        "mass": 4,
        "position": [
          -0.14500000000000002,
          2.8000000000000003,
          -0.14500000000000002
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "robot-a",
        "name": "West sorting robot",
        "role": "actuator",
        "anchored": false,
        "mass": 2,
        "position": [
          -1.9,
          2.75,
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
        "id": "robot-b",
        "name": "East sorting robot",
        "role": "actuator",
        "anchored": false,
        "mass": 2,
        "position": [
          1.9,
          2.75,
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
        "id": "container-red",
        "name": "container red",
        "role": "payload",
        "anchored": false,
        "mass": 3,
        "position": [
          0,
          1.05,
          4
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "container-blue",
        "name": "container blue",
        "role": "payload",
        "anchored": false,
        "mass": 3,
        "position": [
          4,
          1.05,
          4
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "container-yellow",
        "name": "container yellow",
        "role": "payload",
        "anchored": false,
        "mass": 3,
        "position": [
          8,
          1.05,
          4
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
    "choiceId": "A"
  }
}
```

### 接口计数（h3-automated-cargo-terminal-degree）

lift 连接几个声明关节？平行关节分别计数。

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
        "id": "rack-a-feet",
        "name": "rack a feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-a",
        "anchorParent": [
          -6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rack-b-feet",
        "name": "rack b feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-b",
        "anchorParent": [
          6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "inbound-drive",
        "name": "inbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-a",
        "anchorParent": [
          0,
          0.49999999999999994,
          -1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "outbound-drive",
        "name": "outbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-b",
        "anchorParent": [
          0,
          0.49999999999999994,
          1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "floor",
        "child": "gantry",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -3.05,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shuttle-slide",
        "name": "shuttle slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "shuttle",
        "anchorParent": [
          0,
          2.95,
          0
        ],
        "anchorChild": [
          0,
          -0.2499999999999991,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4.5,
          4.5
        ]
      },
      {
        "id": "lift-slide",
        "name": "lift slide",
        "type": "prismatic",
        "parent": "shuttle",
        "child": "lift",
        "anchorParent": [
          0,
          -2.05,
          0
        ],
        "anchorChild": [
          0.14500000000000002,
          1.9,
          0.14500000000000002
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4,
          0
        ]
      },
      {
        "id": "robot-a-base",
        "name": "robot a base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-a",
        "anchorParent": [
          -2.5,
          0.8,
          0
        ],
        "anchorChild": [
          -0.6000000000000001,
          -1.75,
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
        "id": "robot-b-base",
        "name": "robot b base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-b",
        "anchorParent": [
          2.5,
          0.8,
          0
        ],
        "anchorChild": [
          0.6000000000000001,
          -1.75,
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
        "id": "container-0-lock",
        "name": "container 0 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-red",
        "anchorParent": [
          -1.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-1-lock",
        "name": "container 1 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-blue",
        "anchorParent": [
          2.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-2-lock",
        "name": "container 2 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-yellow",
        "anchorParent": [
          6.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
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
    "choiceId": "C"
  }
}
```

### 局部改色（h3-automated-cargo-terminal-recolor）

仅将 h0181 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"h0182","color":"#e8792e"}
- B：{"id":"h0181","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"h0181","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "h0181",
      "moduleId": "lift",
      "shape": "plate",
      "size": [
        0.92,
        0.25,
        0.92
      ],
      "position": [
        -0.855,
        -1.6,
        -0.855
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

### 补装部件（h3-automated-cargo-terminal-add）

模块 lift 缺失零件 h0181。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"h0181","moduleId":"lift","shape":"plate","size":[3,3,3],"position":[-0.855,-1.6,-0.855],"rotation":[0,0,0,1],"color":"#edf1f2"}
- B：{"id":"h0181","moduleId":"lift","shape":"plate","size":[0.92,0.25,0.92],"position":[-0.855,-1.6,-0.855],"rotation":[0,0,0,1],"color":"#000000"}
- C：{"id":"h0181","moduleId":"lift","shape":"plate","size":[0.92,0.25,0.92],"position":[-0.855,-1.6,-0.855],"rotation":[0,0,0,1],"color":"#edf1f2"}
- D：{"id":"h0181","moduleId":"floor","shape":"plate","size":[0.92,0.25,0.92],"position":[-0.855,-1.6,-0.855],"rotation":[0,0,0,1],"color":"#edf1f2"}

```json
{
  "input": {
    "targetPart": {
      "id": "h0181",
      "moduleId": "lift",
      "shape": "plate",
      "size": [
        0.92,
        0.25,
        0.92
      ],
      "position": [
        -0.855,
        -1.6,
        -0.855
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
      "h0063",
      "h0064",
      "h0065",
      "h0066",
      "h0067",
      "h0068",
      "h0069",
      "h0070",
      "h0071",
      "h0072",
      "h0073",
      "h0074",
      "h0075",
      "h0076",
      "h0077",
      "h0078",
      "h0079",
      "h0080",
      "h0081",
      "h0082",
      "h0083",
      "h0084",
      "h0085",
      "h0086",
      "h0087",
      "h0088",
      "h0089",
      "h0090",
      "h0091",
      "h0092",
      "h0093",
      "h0094",
      "h0095",
      "h0096",
      "h0097",
      "h0098",
      "h0099",
      "h0100",
      "h0101",
      "h0102",
      "h0103",
      "h0104",
      "h0105",
      "h0106",
      "h0107",
      "h0108",
      "h0109",
      "h0110",
      "h0111",
      "h0112",
      "h0113",
      "h0114",
      "h0115",
      "h0116",
      "h0117",
      "h0118",
      "h0119",
      "h0120",
      "h0121",
      "h0122",
      "h0123",
      "h0124",
      "h0125",
      "h0126",
      "h0127",
      "h0128",
      "h0129",
      "h0130",
      "h0131",
      "h0132",
      "h0133",
      "h0134",
      "h0135",
      "h0136",
      "h0137",
      "h0138",
      "h0139",
      "h0140",
      "h0141",
      "h0142",
      "h0143",
      "h0144",
      "h0145",
      "h0146",
      "h0147",
      "h0148",
      "h0149",
      "h0150",
      "h0151",
      "h0152",
      "h0153",
      "h0154",
      "h0155",
      "h0156",
      "h0157",
      "h0158",
      "h0159",
      "h0160",
      "h0161",
      "h0162",
      "h0163",
      "h0164",
      "h0165",
      "h0166",
      "h0167",
      "h0168",
      "h0169",
      "h0170",
      "h0171",
      "h0172",
      "h0173",
      "h0174",
      "h0175",
      "h0176",
      "h0177",
      "h0178",
      "h0179",
      "h0180",
      "h0182",
      "h0183",
      "h0184",
      "h0185",
      "h0186",
      "h0187",
      "h0188",
      "h0189",
      "h0190",
      "h0191",
      "h0192",
      "h0193",
      "h0194",
      "h0195",
      "h0196",
      "h0197",
      "h0198",
      "h0199",
      "h0200",
      "h0201",
      "h0202",
      "h0203",
      "h0204",
      "h0205",
      "h0206",
      "h0207",
      "h0208",
      "h0209",
      "h0210",
      "h0211",
      "h0212",
      "h0213",
      "h0214",
      "h0215",
      "h0216",
      "h0217",
      "h0218",
      "h0219",
      "h0220",
      "h0221",
      "h0222",
      "h0223",
      "h0224",
      "h0225",
      "h0226",
      "h0227",
      "h0228",
      "h0229",
      "h0230",
      "h0231"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 安全拆除（h3-automated-cargo-terminal-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["container-blue","container-red","container-yellow","conveyor-a","conveyor-b","lift","rack-a","rack-b","robot-a","robot-b"]
- B：["floor"]
- C：[]
- D：["floor","rack-a","rack-b","conveyor-a","conveyor-b","gantry","shuttle","lift","robot-a","robot-b","container-red","container-blue","container-yellow"]

```json
{
  "input": {
    "joints": [
      {
        "id": "rack-a-feet",
        "name": "rack a feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-a",
        "anchorParent": [
          -6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rack-b-feet",
        "name": "rack b feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-b",
        "anchorParent": [
          6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "inbound-drive",
        "name": "inbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-a",
        "anchorParent": [
          0,
          0.49999999999999994,
          -1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "outbound-drive",
        "name": "outbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-b",
        "anchorParent": [
          0,
          0.49999999999999994,
          1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "floor",
        "child": "gantry",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -3.05,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shuttle-slide",
        "name": "shuttle slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "shuttle",
        "anchorParent": [
          0,
          2.95,
          0
        ],
        "anchorChild": [
          0,
          -0.2499999999999991,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4.5,
          4.5
        ]
      },
      {
        "id": "lift-slide",
        "name": "lift slide",
        "type": "prismatic",
        "parent": "shuttle",
        "child": "lift",
        "anchorParent": [
          0,
          -2.05,
          0
        ],
        "anchorChild": [
          0.14500000000000002,
          1.9,
          0.14500000000000002
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4,
          0
        ]
      },
      {
        "id": "robot-a-base",
        "name": "robot a base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-a",
        "anchorParent": [
          -2.5,
          0.8,
          0
        ],
        "anchorChild": [
          -0.6000000000000001,
          -1.75,
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
        "id": "robot-b-base",
        "name": "robot b base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-b",
        "anchorParent": [
          2.5,
          0.8,
          0
        ],
        "anchorChild": [
          0.6000000000000001,
          -1.75,
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
        "id": "container-0-lock",
        "name": "container 0 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-red",
        "anchorParent": [
          -1.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-1-lock",
        "name": "container 1 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-blue",
        "anchorParent": [
          2.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-2-lock",
        "name": "container 2 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-yellow",
        "anchorParent": [
          6.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
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
      "floor",
      "rack-a",
      "rack-b",
      "conveyor-a",
      "conveyor-b",
      "gantry",
      "shuttle",
      "lift",
      "robot-a",
      "robot-b",
      "container-red",
      "container-blue",
      "container-yellow"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 替换选择（h3-automated-cargo-terminal-replace）

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
        "stiffness": 7,
        "mass": 0.5
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 6,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 6,
        "stiffness": 3,
        "mass": 1.6
      },
      {
        "id": "stock-3",
        "cost": 6,
        "stiffness": 5,
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

### 平移纠偏（h3-automated-cargo-terminal-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[-4,0,2]
- B：[4,0,-2]
- C：[0,0,0]
- D：[0,2,0]

```json
{
  "input": {
    "delta": [
      4,
      0,
      -2
    ],
    "target": "lift"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 姿态纠偏（h3-automated-cargo-terminal-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：0
- B：90
- C：135
- D：-135

```json
{
  "input": {
    "module": "lift",
    "currentYaw": 270,
    "targetYaw": 45
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 下一步放置（h3-automated-cargo-terminal-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["floor"]
- B：["container-blue","container-red","container-yellow","lift","robot-a","robot-b"]
- C：[]
- D：["floor","rack-a","rack-b","conveyor-a","conveyor-b","gantry","shuttle"]

```json
{
  "input": {
    "prefix": [
      "floor",
      "rack-a",
      "rack-b",
      "conveyor-a",
      "conveyor-b",
      "gantry",
      "shuttle"
    ],
    "joints": [
      {
        "id": "rack-a-feet",
        "name": "rack a feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-a",
        "anchorParent": [
          -6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rack-b-feet",
        "name": "rack b feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-b",
        "anchorParent": [
          6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "inbound-drive",
        "name": "inbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-a",
        "anchorParent": [
          0,
          0.49999999999999994,
          -1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "outbound-drive",
        "name": "outbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-b",
        "anchorParent": [
          0,
          0.49999999999999994,
          1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "floor",
        "child": "gantry",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -3.05,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shuttle-slide",
        "name": "shuttle slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "shuttle",
        "anchorParent": [
          0,
          2.95,
          0
        ],
        "anchorChild": [
          0,
          -0.2499999999999991,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4.5,
          4.5
        ]
      },
      {
        "id": "lift-slide",
        "name": "lift slide",
        "type": "prismatic",
        "parent": "shuttle",
        "child": "lift",
        "anchorParent": [
          0,
          -2.05,
          0
        ],
        "anchorChild": [
          0.14500000000000002,
          1.9,
          0.14500000000000002
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4,
          0
        ]
      },
      {
        "id": "robot-a-base",
        "name": "robot a base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-a",
        "anchorParent": [
          -2.5,
          0.8,
          0
        ],
        "anchorChild": [
          -0.6000000000000001,
          -1.75,
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
        "id": "robot-b-base",
        "name": "robot b base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-b",
        "anchorParent": [
          2.5,
          0.8,
          0
        ],
        "anchorChild": [
          0.6000000000000001,
          -1.75,
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
        "id": "container-0-lock",
        "name": "container 0 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-red",
        "anchorParent": [
          -1.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-1-lock",
        "name": "container 1 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-blue",
        "anchorParent": [
          2.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-2-lock",
        "name": "container 2 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-yellow",
        "anchorParent": [
          6.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
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
      "floor",
      "rack-a",
      "rack-b",
      "conveyor-a",
      "conveyor-b",
      "gantry",
      "shuttle",
      "lift",
      "robot-a",
      "robot-b",
      "container-red",
      "container-blue",
      "container-yellow"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 库存核算（h3-automated-cargo-terminal-inventory）

备件库有 14 件，替换模块需 13 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：4
- B：1
- C：2
- D：0

```json
{
  "input": {
    "available": 14,
    "required": 13
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 子装配边界（h3-automated-cargo-terminal-boundary）

隔离 lift 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["shuttle-slide"]
- B：["lift-slide"]
- C：[]
- D：["rack-a-feet","rack-b-feet","inbound-drive","outbound-drive","gantry-feet","shuttle-slide","lift-slide","robot-a-base","robot-b-base","container-0-lock","container-1-lock","container-2-lock"]

```json
{
  "input": {
    "joints": [
      {
        "id": "rack-a-feet",
        "name": "rack a feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-a",
        "anchorParent": [
          -6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rack-b-feet",
        "name": "rack b feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-b",
        "anchorParent": [
          6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "inbound-drive",
        "name": "inbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-a",
        "anchorParent": [
          0,
          0.49999999999999994,
          -1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "outbound-drive",
        "name": "outbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-b",
        "anchorParent": [
          0,
          0.49999999999999994,
          1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "floor",
        "child": "gantry",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -3.05,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shuttle-slide",
        "name": "shuttle slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "shuttle",
        "anchorParent": [
          0,
          2.95,
          0
        ],
        "anchorChild": [
          0,
          -0.2499999999999991,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4.5,
          4.5
        ]
      },
      {
        "id": "lift-slide",
        "name": "lift slide",
        "type": "prismatic",
        "parent": "shuttle",
        "child": "lift",
        "anchorParent": [
          0,
          -2.05,
          0
        ],
        "anchorChild": [
          0.14500000000000002,
          1.9,
          0.14500000000000002
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4,
          0
        ]
      },
      {
        "id": "robot-a-base",
        "name": "robot a base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-a",
        "anchorParent": [
          -2.5,
          0.8,
          0
        ],
        "anchorChild": [
          -0.6000000000000001,
          -1.75,
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
        "id": "robot-b-base",
        "name": "robot b base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-b",
        "anchorParent": [
          2.5,
          0.8,
          0
        ],
        "anchorChild": [
          0.6000000000000001,
          -1.75,
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
        "id": "container-0-lock",
        "name": "container 0 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-red",
        "anchorParent": [
          -1.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-1-lock",
        "name": "container 1 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-blue",
        "anchorParent": [
          2.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-2-lock",
        "name": "container 2 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-yellow",
        "anchorParent": [
          6.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "target": "lift"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 最小干预（h3-automated-cargo-terminal-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：2
- B：13
- C：0
- D：1

```json
{
  "input": {
    "module": "lift"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 全过程依赖（h3-automated-cargo-terminal-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：-1
- B：1
- C：12
- D：0

```json
{
  "input": {
    "order": [
      "container-blue",
      "floor",
      "rack-a",
      "rack-b",
      "conveyor-a",
      "conveyor-b",
      "gantry",
      "shuttle",
      "lift",
      "robot-a",
      "robot-b",
      "container-red",
      "container-yellow"
    ],
    "joints": [
      {
        "id": "rack-a-feet",
        "name": "rack a feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-a",
        "anchorParent": [
          -6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rack-b-feet",
        "name": "rack b feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-b",
        "anchorParent": [
          6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "inbound-drive",
        "name": "inbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-a",
        "anchorParent": [
          0,
          0.49999999999999994,
          -1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "outbound-drive",
        "name": "outbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-b",
        "anchorParent": [
          0,
          0.49999999999999994,
          1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "floor",
        "child": "gantry",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -3.05,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shuttle-slide",
        "name": "shuttle slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "shuttle",
        "anchorParent": [
          0,
          2.95,
          0
        ],
        "anchorChild": [
          0,
          -0.2499999999999991,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4.5,
          4.5
        ]
      },
      {
        "id": "lift-slide",
        "name": "lift slide",
        "type": "prismatic",
        "parent": "shuttle",
        "child": "lift",
        "anchorParent": [
          0,
          -2.05,
          0
        ],
        "anchorChild": [
          0.14500000000000002,
          1.9,
          0.14500000000000002
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4,
          0
        ]
      },
      {
        "id": "robot-a-base",
        "name": "robot a base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-a",
        "anchorParent": [
          -2.5,
          0.8,
          0
        ],
        "anchorChild": [
          -0.6000000000000001,
          -1.75,
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
        "id": "robot-b-base",
        "name": "robot b base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-b",
        "anchorParent": [
          2.5,
          0.8,
          0
        ],
        "anchorChild": [
          0.6000000000000001,
          -1.75,
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
        "id": "container-0-lock",
        "name": "container 0 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-red",
        "anchorParent": [
          -1.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-1-lock",
        "name": "container 1 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-blue",
        "anchorParent": [
          2.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-2-lock",
        "name": "container 2 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-yellow",
        "anchorParent": [
          6.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
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

### 连续维修路径（h3-automated-cargo-terminal-access）

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
          13.96,
          2.8000000000000003,
          -0.14500000000000002
        ],
        "end": [
          -0.14500000000000002,
          2.8000000000000003,
          -0.14500000000000002
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.4310528337955475
      },
      {
        "id": "path-1",
        "start": [
          -0.14500000000000002,
          10.924999999999999,
          -0.14500000000000002
        ],
        "end": [
          -0.14500000000000002,
          2.8000000000000003,
          -0.14500000000000002
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.4701538383960724
      },
      {
        "id": "path-2",
        "start": [
          -0.14500000000000002,
          2.8000000000000003,
          8.96
        ],
        "end": [
          -0.14500000000000002,
          2.8000000000000003,
          -0.14500000000000002
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
      "A"
    ]
  }
}
```

### 支撑反事实（h3-automated-cargo-terminal-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["floor","rack-a","rack-b","conveyor-a","conveyor-b","gantry","shuttle","lift","robot-a","robot-b","container-red","container-blue","container-yellow"]
- C：["lift","shuttle"]
- D：["gantry"]

```json
{
  "input": {
    "removed": "gantry",
    "roots": [
      "floor"
    ],
    "joints": [
      {
        "id": "rack-a-feet",
        "name": "rack a feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-a",
        "anchorParent": [
          -6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rack-b-feet",
        "name": "rack b feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-b",
        "anchorParent": [
          6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "inbound-drive",
        "name": "inbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-a",
        "anchorParent": [
          0,
          0.49999999999999994,
          -1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "outbound-drive",
        "name": "outbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-b",
        "anchorParent": [
          0,
          0.49999999999999994,
          1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "floor",
        "child": "gantry",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -3.05,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shuttle-slide",
        "name": "shuttle slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "shuttle",
        "anchorParent": [
          0,
          2.95,
          0
        ],
        "anchorChild": [
          0,
          -0.2499999999999991,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4.5,
          4.5
        ]
      },
      {
        "id": "lift-slide",
        "name": "lift slide",
        "type": "prismatic",
        "parent": "shuttle",
        "child": "lift",
        "anchorParent": [
          0,
          -2.05,
          0
        ],
        "anchorChild": [
          0.14500000000000002,
          1.9,
          0.14500000000000002
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4,
          0
        ]
      },
      {
        "id": "robot-a-base",
        "name": "robot a base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-a",
        "anchorParent": [
          -2.5,
          0.8,
          0
        ],
        "anchorChild": [
          -0.6000000000000001,
          -1.75,
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
        "id": "robot-b-base",
        "name": "robot b base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-b",
        "anchorParent": [
          2.5,
          0.8,
          0
        ],
        "anchorChild": [
          0.6000000000000001,
          -1.75,
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
        "id": "container-0-lock",
        "name": "container 0 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-red",
        "anchorParent": [
          -1.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-1-lock",
        "name": "container 1 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-blue",
        "anchorParent": [
          2.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-2-lock",
        "name": "container 2 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-yellow",
        "anchorParent": [
          6.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
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
      "floor",
      "rack-a",
      "rack-b",
      "conveyor-a",
      "conveyor-b",
      "gantry",
      "shuttle",
      "lift",
      "robot-a",
      "robot-b",
      "container-red",
      "container-blue",
      "container-yellow"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-automated-cargo-terminal-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：1.0051
- C：0.0051
- D：0.2051

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0051235174752623834
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0000429754552302113
      },
      {
        "time": 0.20833333333333334,
        "displacement": 3.6256089987148156e-7
      },
      {
        "time": 0.30833333333333335,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 0.5083333333333333,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 0.6083333333333333,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 0.7083333333333334,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 0.8083333333333333,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 1,
        "displacement": 1.0745380149674385e-7
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.0006454478290298199,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-automated-cargo-terminal-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：5
- B：-4.5
- C：0
- D：-5

```json
{
  "input": {
    "joint": "shuttle-slide",
    "limits": [
      -4.5,
      4.5
    ],
    "units": "scene units"
  },
  "answer": {
    "choiceIds": [
      "B",
      "C"
    ]
  }
}
```

### 约束故障诊断（h3-automated-cargo-terminal-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：rack-b-feet
- B：inbound-drive
- C：lift-slide
- D：rack-a-feet

```json
{
  "input": {
    "endpoints": [
      "shuttle",
      "lift"
    ],
    "type": "prismatic",
    "joints": [
      {
        "id": "rack-a-feet",
        "name": "rack a feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-a",
        "anchorParent": [
          -6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rack-b-feet",
        "name": "rack b feet",
        "type": "fixed",
        "parent": "floor",
        "child": "rack-b",
        "anchorParent": [
          6.7,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -2.3375,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "inbound-drive",
        "name": "inbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-a",
        "anchorParent": [
          0,
          0.49999999999999994,
          -1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "outbound-drive",
        "name": "outbound drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "conveyor-b",
        "anchorParent": [
          0,
          0.49999999999999994,
          1.2
        ],
        "anchorChild": [
          0,
          -0.050000000000000044,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "gantry-feet",
        "name": "gantry feet",
        "type": "fixed",
        "parent": "floor",
        "child": "gantry",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -3.05,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "shuttle-slide",
        "name": "shuttle slide",
        "type": "prismatic",
        "parent": "gantry",
        "child": "shuttle",
        "anchorParent": [
          0,
          2.95,
          0
        ],
        "anchorChild": [
          0,
          -0.2499999999999991,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -4.5,
          4.5
        ]
      },
      {
        "id": "lift-slide",
        "name": "lift slide",
        "type": "prismatic",
        "parent": "shuttle",
        "child": "lift",
        "anchorParent": [
          0,
          -2.05,
          0
        ],
        "anchorChild": [
          0.14500000000000002,
          1.9,
          0.14500000000000002
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4,
          0
        ]
      },
      {
        "id": "robot-a-base",
        "name": "robot a base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-a",
        "anchorParent": [
          -2.5,
          0.8,
          0
        ],
        "anchorChild": [
          -0.6000000000000001,
          -1.75,
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
        "id": "robot-b-base",
        "name": "robot b base",
        "type": "revolute",
        "parent": "floor",
        "child": "robot-b",
        "anchorParent": [
          2.5,
          0.8,
          0
        ],
        "anchorChild": [
          0.6000000000000001,
          -1.75,
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
        "id": "container-0-lock",
        "name": "container 0 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-red",
        "anchorParent": [
          -1.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-1-lock",
        "name": "container 1 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-blue",
        "anchorParent": [
          2.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
          -0.5
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "container-2-lock",
        "name": "container 2 lock",
        "type": "fixed",
        "parent": "floor",
        "child": "container-yellow",
        "anchorParent": [
          6.5,
          0.49999999999999994,
          3.5
        ],
        "anchorChild": [
          -1.5,
          -0.3500000000000001,
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
      "C"
    ]
  }
}
```

### 主动检查收益（h3-automated-cargo-terminal-information-gain）

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
    "module": "lift",
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

### 不确定性与弃答（h3-automated-cargo-terminal-abstention）

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

### 观测后信念更新（h3-automated-cargo-terminal-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.25
- B：0.5
- C：0.3333333333333333
- D：0

```json
{
  "input": {
    "module": "lift",
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
    "choiceId": "C"
  }
}
```

### 多目标工程权衡（h3-automated-cargo-terminal-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

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
        "stiffness": 7,
        "mass": 0.5
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 6,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 6,
        "stiffness": 3,
        "mass": 1.6
      },
      {
        "id": "stock-3",
        "cost": 6,
        "stiffness": 5,
        "mass": 1
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

### 依赖装配（h3-automated-cargo-terminal-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:lift",
        "label": "安装 lift",
        "requires": [
          "present:shuttle"
        ],
        "forbids": [
          "present:lift"
        ],
        "adds": [
          "present:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift",
          "visible": true
        }
      },
      {
        "id": "place:rack-b",
        "label": "安装 rack-b",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:rack-b"
        ],
        "adds": [
          "present:rack-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-b",
          "visible": true
        }
      },
      {
        "id": "place:container-blue",
        "label": "安装 container-blue",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:container-blue"
        ],
        "adds": [
          "present:container-blue"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue",
          "visible": true
        }
      },
      {
        "id": "place:conveyor-b",
        "label": "安装 conveyor-b",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:conveyor-b"
        ],
        "adds": [
          "present:conveyor-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "conveyor-b",
          "visible": true
        }
      },
      {
        "id": "place:container-red",
        "label": "安装 container-red",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:container-red"
        ],
        "adds": [
          "present:container-red"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-red",
          "visible": true
        }
      },
      {
        "id": "place:robot-b",
        "label": "安装 robot-b",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:robot-b"
        ],
        "adds": [
          "present:robot-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b",
          "visible": true
        }
      },
      {
        "id": "place:floor",
        "label": "安装 floor",
        "requires": [],
        "forbids": [
          "present:floor"
        ],
        "adds": [
          "present:floor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "floor",
          "visible": true
        }
      },
      {
        "id": "place:container-yellow",
        "label": "安装 container-yellow",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:container-yellow"
        ],
        "adds": [
          "present:container-yellow"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow",
          "visible": true
        }
      },
      {
        "id": "place:gantry",
        "label": "安装 gantry",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:gantry"
        ],
        "adds": [
          "present:gantry"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry",
          "visible": true
        }
      },
      {
        "id": "place:conveyor-a",
        "label": "安装 conveyor-a",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:conveyor-a"
        ],
        "adds": [
          "present:conveyor-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "conveyor-a",
          "visible": true
        }
      },
      {
        "id": "place:shuttle",
        "label": "安装 shuttle",
        "requires": [
          "present:gantry"
        ],
        "forbids": [
          "present:shuttle"
        ],
        "adds": [
          "present:shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle",
          "visible": true
        }
      },
      {
        "id": "place:robot-a",
        "label": "安装 robot-a",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:robot-a"
        ],
        "adds": [
          "present:robot-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "robot-a",
          "visible": true
        }
      },
      {
        "id": "place:rack-a",
        "label": "安装 rack-a",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:rack-a"
        ],
        "adds": [
          "present:rack-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "rack-a",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:floor",
      "present:rack-a",
      "present:rack-b",
      "present:conveyor-a",
      "present:conveyor-b",
      "present:gantry",
      "present:shuttle",
      "present:lift",
      "present:robot-a",
      "present:robot-b",
      "present:container-red",
      "present:container-blue",
      "present:container-yellow"
    ],
    "budget": 13,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:floor",
      "place:rack-b",
      "place:container-blue",
      "place:conveyor-b",
      "place:container-red",
      "place:robot-b",
      "place:container-yellow",
      "place:gantry",
      "place:conveyor-a",
      "place:shuttle",
      "place:lift",
      "place:robot-a",
      "place:rack-a"
    ]
  }
}
```

### 依赖拆解（h3-automated-cargo-terminal-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:floor",
      "present:rack-a",
      "present:rack-b",
      "present:conveyor-a",
      "present:conveyor-b",
      "present:gantry",
      "present:shuttle",
      "present:lift",
      "present:robot-a",
      "present:robot-b",
      "present:container-red",
      "present:container-blue",
      "present:container-yellow"
    ],
    "initialModules": [
      "floor",
      "rack-a",
      "rack-b",
      "conveyor-a",
      "conveyor-b",
      "gantry",
      "shuttle",
      "lift",
      "robot-a",
      "robot-b",
      "container-red",
      "container-blue",
      "container-yellow"
    ],
    "actions": [
      {
        "id": "remove:conveyor-b",
        "label": "拆除 conveyor-b",
        "requires": [
          "present:conveyor-b"
        ],
        "forbids": [],
        "adds": [
          "removed:conveyor-b"
        ],
        "deletes": [
          "present:conveyor-b"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "conveyor-b",
          "visible": false
        }
      },
      {
        "id": "remove:container-blue",
        "label": "拆除 container-blue",
        "requires": [
          "present:container-blue"
        ],
        "forbids": [],
        "adds": [
          "removed:container-blue"
        ],
        "deletes": [
          "present:container-blue"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue",
          "visible": false
        }
      },
      {
        "id": "remove:robot-a",
        "label": "拆除 robot-a",
        "requires": [
          "present:robot-a"
        ],
        "forbids": [],
        "adds": [
          "removed:robot-a"
        ],
        "deletes": [
          "present:robot-a"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "robot-a",
          "visible": false
        }
      },
      {
        "id": "remove:container-yellow",
        "label": "拆除 container-yellow",
        "requires": [
          "present:container-yellow"
        ],
        "forbids": [],
        "adds": [
          "removed:container-yellow"
        ],
        "deletes": [
          "present:container-yellow"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow",
          "visible": false
        }
      },
      {
        "id": "remove:gantry",
        "label": "拆除 gantry",
        "requires": [
          "present:gantry"
        ],
        "forbids": [
          "present:shuttle"
        ],
        "adds": [
          "removed:gantry"
        ],
        "deletes": [
          "present:gantry"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gantry",
          "visible": false
        }
      },
      {
        "id": "remove:shuttle",
        "label": "拆除 shuttle",
        "requires": [
          "present:shuttle"
        ],
        "forbids": [
          "present:lift"
        ],
        "adds": [
          "removed:shuttle"
        ],
        "deletes": [
          "present:shuttle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle",
          "visible": false
        }
      },
      {
        "id": "remove:floor",
        "label": "拆除 floor",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:rack-a",
          "present:rack-b",
          "present:conveyor-a",
          "present:conveyor-b",
          "present:gantry",
          "present:robot-a",
          "present:robot-b",
          "present:container-red",
          "present:container-blue",
          "present:container-yellow"
        ],
        "adds": [
          "removed:floor"
        ],
        "deletes": [
          "present:floor"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "floor",
          "visible": false
        }
      },
      {
        "id": "remove:robot-b",
        "label": "拆除 robot-b",
        "requires": [
          "present:robot-b"
        ],
        "forbids": [],
        "adds": [
          "removed:robot-b"
        ],
        "deletes": [
          "present:robot-b"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b",
          "visible": false
        }
      },
      {
        "id": "remove:conveyor-a",
        "label": "拆除 conveyor-a",
        "requires": [
          "present:conveyor-a"
        ],
        "forbids": [],
        "adds": [
          "removed:conveyor-a"
        ],
        "deletes": [
          "present:conveyor-a"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "conveyor-a",
          "visible": false
        }
      },
      {
        "id": "remove:rack-b",
        "label": "拆除 rack-b",
        "requires": [
          "present:rack-b"
        ],
        "forbids": [],
        "adds": [
          "removed:rack-b"
        ],
        "deletes": [
          "present:rack-b"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rack-b",
          "visible": false
        }
      },
      {
        "id": "remove:container-red",
        "label": "拆除 container-red",
        "requires": [
          "present:container-red"
        ],
        "forbids": [],
        "adds": [
          "removed:container-red"
        ],
        "deletes": [
          "present:container-red"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container-red",
          "visible": false
        }
      },
      {
        "id": "remove:lift",
        "label": "拆除 lift",
        "requires": [
          "present:lift"
        ],
        "forbids": [],
        "adds": [
          "removed:lift"
        ],
        "deletes": [
          "present:lift"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lift",
          "visible": false
        }
      },
      {
        "id": "remove:rack-a",
        "label": "拆除 rack-a",
        "requires": [
          "present:rack-a"
        ],
        "forbids": [],
        "adds": [
          "removed:rack-a"
        ],
        "deletes": [
          "present:rack-a"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "rack-a",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:container-yellow",
      "removed:container-blue",
      "removed:container-red",
      "removed:robot-b",
      "removed:robot-a",
      "removed:lift",
      "removed:shuttle",
      "removed:gantry",
      "removed:conveyor-b",
      "removed:conveyor-a",
      "removed:rack-b",
      "removed:rack-a",
      "removed:floor"
    ],
    "budget": 13,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:conveyor-b",
      "remove:container-blue",
      "remove:robot-a",
      "remove:container-yellow",
      "remove:robot-b",
      "remove:conveyor-a",
      "remove:rack-b",
      "remove:container-red",
      "remove:lift",
      "remove:shuttle",
      "remove:gantry",
      "remove:rack-a",
      "remove:floor"
    ]
  }
}
```

### 承载维修（h3-automated-cargo-terminal-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:lift",
      "closed:lift"
    ],
    "initialModules": [
      "floor",
      "rack-a",
      "rack-b",
      "conveyor-a",
      "conveyor-b",
      "gantry",
      "shuttle",
      "lift",
      "robot-a",
      "robot-b",
      "container-red",
      "container-blue",
      "container-yellow"
    ],
    "actions": [
      {
        "id": "release:lift",
        "label": "release lift",
        "requires": [
          "done:close:lift"
        ],
        "forbids": [
          "done:release:lift"
        ],
        "adds": [
          "done:release:lift",
          "repaired:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "support:lift",
        "label": "support lift",
        "requires": [
          "fault:lift"
        ],
        "forbids": [
          "done:support:lift"
        ],
        "adds": [
          "done:support:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "close:lift",
        "label": "close lift",
        "requires": [
          "done:verify:lift"
        ],
        "forbids": [
          "done:close:lift"
        ],
        "adds": [
          "done:close:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "replace:lift",
        "label": "replace lift",
        "requires": [
          "done:remove:lift"
        ],
        "forbids": [
          "done:replace:lift"
        ],
        "adds": [
          "done:replace:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift",
          "visible": true
        }
      },
      {
        "id": "verify:lift",
        "label": "verify lift",
        "requires": [
          "done:replace:lift"
        ],
        "forbids": [
          "done:verify:lift"
        ],
        "adds": [
          "done:verify:lift"
        ],
        "deletes": [
          "fault:lift"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "remove:lift",
        "label": "remove lift",
        "requires": [
          "done:open:lift"
        ],
        "forbids": [
          "done:remove:lift"
        ],
        "adds": [
          "done:remove:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift",
          "visible": false
        }
      },
      {
        "id": "open:lift",
        "label": "open lift",
        "requires": [
          "done:support:lift"
        ],
        "forbids": [
          "done:open:lift"
        ],
        "adds": [
          "done:open:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      }
    ],
    "goalFacts": [
      "repaired:lift"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:lift",
      "open:lift",
      "remove:lift",
      "replace:lift",
      "verify:lift",
      "close:lift",
      "release:lift"
    ]
  }
}
```

### 复合编辑验证（h3-automated-cargo-terminal-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:lift",
      "closed:lift"
    ],
    "initialModules": [
      "floor",
      "rack-a",
      "rack-b",
      "conveyor-a",
      "conveyor-b",
      "gantry",
      "shuttle",
      "lift",
      "robot-a",
      "robot-b",
      "container-red",
      "container-blue",
      "container-yellow"
    ],
    "actions": [
      {
        "id": "release:lift",
        "label": "release lift",
        "requires": [
          "done:close:lift"
        ],
        "forbids": [
          "done:release:lift"
        ],
        "adds": [
          "done:release:lift",
          "repaired:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "support:lift",
        "label": "support lift",
        "requires": [
          "fault:lift"
        ],
        "forbids": [
          "done:support:lift"
        ],
        "adds": [
          "done:support:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "close:lift",
        "label": "close lift",
        "requires": [
          "done:verify:lift"
        ],
        "forbids": [
          "done:close:lift"
        ],
        "adds": [
          "done:close:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "verify:lift",
        "label": "verify lift",
        "requires": [
          "done:recolor:lift"
        ],
        "forbids": [
          "done:verify:lift"
        ],
        "adds": [
          "done:verify:lift"
        ],
        "deletes": [
          "fault:lift"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "open:lift",
        "label": "open lift",
        "requires": [
          "done:support:lift"
        ],
        "forbids": [
          "done:open:lift"
        ],
        "adds": [
          "done:open:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "recolor:lift",
        "label": "recolor lift",
        "requires": [
          "done:open:lift"
        ],
        "forbids": [
          "done:recolor:lift"
        ],
        "adds": [
          "done:recolor:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift",
          "color": "#ea7635"
        }
      }
    ],
    "goalFacts": [
      "repaired:lift"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:lift",
      "open:lift",
      "recolor:lift",
      "verify:lift",
      "close:lift",
      "release:lift"
    ]
  }
}
```

### 跨区域联合维修（h3-automated-cargo-terminal-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:robot-b",
      "closed:robot-b",
      "fault:container-red",
      "closed:container-red",
      "fault:container-blue",
      "closed:container-blue",
      "fault:container-yellow",
      "closed:container-yellow"
    ],
    "initialModules": [
      "floor",
      "rack-a",
      "rack-b",
      "conveyor-a",
      "conveyor-b",
      "gantry",
      "shuttle",
      "lift",
      "robot-a",
      "robot-b",
      "container-red",
      "container-blue",
      "container-yellow"
    ],
    "actions": [
      {
        "id": "replace:container-yellow",
        "label": "replace container-yellow",
        "requires": [
          "done:remove:container-yellow"
        ],
        "forbids": [
          "done:replace:container-yellow"
        ],
        "adds": [
          "done:replace:container-yellow"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow",
          "visible": true
        }
      },
      {
        "id": "open:robot-b",
        "label": "open robot-b",
        "requires": [
          "done:support:robot-b"
        ],
        "forbids": [
          "done:open:robot-b"
        ],
        "adds": [
          "done:open:robot-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b"
        }
      },
      {
        "id": "remove:container-blue",
        "label": "remove container-blue",
        "requires": [
          "done:open:container-blue"
        ],
        "forbids": [
          "done:remove:container-blue"
        ],
        "adds": [
          "done:remove:container-blue"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue",
          "visible": false
        }
      },
      {
        "id": "support:container-blue",
        "label": "support container-blue",
        "requires": [
          "fault:container-blue"
        ],
        "forbids": [
          "done:support:container-blue"
        ],
        "adds": [
          "done:support:container-blue"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue"
        }
      },
      {
        "id": "open:container-blue",
        "label": "open container-blue",
        "requires": [
          "done:support:container-blue"
        ],
        "forbids": [
          "done:open:container-blue"
        ],
        "adds": [
          "done:open:container-blue"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue"
        }
      },
      {
        "id": "close:container-yellow",
        "label": "close container-yellow",
        "requires": [
          "done:verify:container-yellow"
        ],
        "forbids": [
          "done:close:container-yellow"
        ],
        "adds": [
          "done:close:container-yellow"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow"
        }
      },
      {
        "id": "support:robot-b",
        "label": "support robot-b",
        "requires": [
          "fault:robot-b"
        ],
        "forbids": [
          "done:support:robot-b"
        ],
        "adds": [
          "done:support:robot-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b"
        }
      },
      {
        "id": "verify:container-yellow",
        "label": "verify container-yellow",
        "requires": [
          "done:replace:container-yellow"
        ],
        "forbids": [
          "done:verify:container-yellow"
        ],
        "adds": [
          "done:verify:container-yellow"
        ],
        "deletes": [
          "fault:container-yellow"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow"
        }
      },
      {
        "id": "remove:container-yellow",
        "label": "remove container-yellow",
        "requires": [
          "done:open:container-yellow"
        ],
        "forbids": [
          "done:remove:container-yellow"
        ],
        "adds": [
          "done:remove:container-yellow"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow",
          "visible": false
        }
      },
      {
        "id": "release:container-blue",
        "label": "release container-blue",
        "requires": [
          "done:close:container-blue"
        ],
        "forbids": [
          "done:release:container-blue"
        ],
        "adds": [
          "done:release:container-blue",
          "repaired:container-blue"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue"
        }
      },
      {
        "id": "verify:container-red",
        "label": "verify container-red",
        "requires": [
          "done:replace:container-red"
        ],
        "forbids": [
          "done:verify:container-red"
        ],
        "adds": [
          "done:verify:container-red"
        ],
        "deletes": [
          "fault:container-red"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container-red"
        }
      },
      {
        "id": "close:robot-b",
        "label": "close robot-b",
        "requires": [
          "done:verify:robot-b"
        ],
        "forbids": [
          "done:close:robot-b"
        ],
        "adds": [
          "done:close:robot-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b"
        }
      },
      {
        "id": "verify:robot-b",
        "label": "verify robot-b",
        "requires": [
          "done:replace:robot-b"
        ],
        "forbids": [
          "done:verify:robot-b"
        ],
        "adds": [
          "done:verify:robot-b"
        ],
        "deletes": [
          "fault:robot-b"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b"
        }
      },
      {
        "id": "release:container-red",
        "label": "release container-red",
        "requires": [
          "done:close:container-red"
        ],
        "forbids": [
          "done:release:container-red"
        ],
        "adds": [
          "done:release:container-red",
          "repaired:container-red"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-red"
        }
      },
      {
        "id": "remove:robot-b",
        "label": "remove robot-b",
        "requires": [
          "done:open:robot-b"
        ],
        "forbids": [
          "done:remove:robot-b"
        ],
        "adds": [
          "done:remove:robot-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b",
          "visible": false
        }
      },
      {
        "id": "support:container-red",
        "label": "support container-red",
        "requires": [
          "fault:container-red"
        ],
        "forbids": [
          "done:support:container-red"
        ],
        "adds": [
          "done:support:container-red"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-red"
        }
      },
      {
        "id": "close:container-blue",
        "label": "close container-blue",
        "requires": [
          "done:verify:container-blue"
        ],
        "forbids": [
          "done:close:container-blue"
        ],
        "adds": [
          "done:close:container-blue"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue"
        }
      },
      {
        "id": "support:container-yellow",
        "label": "support container-yellow",
        "requires": [
          "fault:container-yellow"
        ],
        "forbids": [
          "done:support:container-yellow"
        ],
        "adds": [
          "done:support:container-yellow"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow"
        }
      },
      {
        "id": "remove:container-red",
        "label": "remove container-red",
        "requires": [
          "done:open:container-red"
        ],
        "forbids": [
          "done:remove:container-red"
        ],
        "adds": [
          "done:remove:container-red"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-red",
          "visible": false
        }
      },
      {
        "id": "release:robot-b",
        "label": "release robot-b",
        "requires": [
          "done:close:robot-b"
        ],
        "forbids": [
          "done:release:robot-b"
        ],
        "adds": [
          "done:release:robot-b",
          "repaired:robot-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b"
        }
      },
      {
        "id": "verify:container-blue",
        "label": "verify container-blue",
        "requires": [
          "done:replace:container-blue"
        ],
        "forbids": [
          "done:verify:container-blue"
        ],
        "adds": [
          "done:verify:container-blue"
        ],
        "deletes": [
          "fault:container-blue"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue"
        }
      },
      {
        "id": "replace:robot-b",
        "label": "replace robot-b",
        "requires": [
          "done:remove:robot-b"
        ],
        "forbids": [
          "done:replace:robot-b"
        ],
        "adds": [
          "done:replace:robot-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b",
          "visible": true
        }
      },
      {
        "id": "open:container-yellow",
        "label": "open container-yellow",
        "requires": [
          "done:support:container-yellow"
        ],
        "forbids": [
          "done:open:container-yellow"
        ],
        "adds": [
          "done:open:container-yellow"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow"
        }
      },
      {
        "id": "open:container-red",
        "label": "open container-red",
        "requires": [
          "done:support:container-red"
        ],
        "forbids": [
          "done:open:container-red"
        ],
        "adds": [
          "done:open:container-red"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-red"
        }
      },
      {
        "id": "close:container-red",
        "label": "close container-red",
        "requires": [
          "done:verify:container-red"
        ],
        "forbids": [
          "done:close:container-red"
        ],
        "adds": [
          "done:close:container-red"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-red"
        }
      },
      {
        "id": "replace:container-blue",
        "label": "replace container-blue",
        "requires": [
          "done:remove:container-blue"
        ],
        "forbids": [
          "done:replace:container-blue"
        ],
        "adds": [
          "done:replace:container-blue"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue",
          "visible": true
        }
      },
      {
        "id": "replace:container-red",
        "label": "replace container-red",
        "requires": [
          "done:remove:container-red"
        ],
        "forbids": [
          "done:replace:container-red"
        ],
        "adds": [
          "done:replace:container-red"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-red",
          "visible": true
        }
      },
      {
        "id": "release:container-yellow",
        "label": "release container-yellow",
        "requires": [
          "done:close:container-yellow"
        ],
        "forbids": [
          "done:release:container-yellow"
        ],
        "adds": [
          "done:release:container-yellow",
          "repaired:container-yellow"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow"
        }
      }
    ],
    "goalFacts": [
      "repaired:robot-b",
      "repaired:container-red",
      "repaired:container-blue",
      "repaired:container-yellow"
    ],
    "budget": 28,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:container-blue",
      "open:container-blue",
      "remove:container-blue",
      "support:robot-b",
      "open:robot-b",
      "remove:robot-b",
      "support:container-red",
      "support:container-yellow",
      "replace:robot-b",
      "verify:robot-b",
      "close:robot-b",
      "release:robot-b",
      "open:container-yellow",
      "remove:container-yellow",
      "replace:container-yellow",
      "verify:container-yellow",
      "close:container-yellow",
      "open:container-red",
      "remove:container-red",
      "replace:container-blue",
      "verify:container-blue",
      "close:container-blue",
      "release:container-blue",
      "replace:container-red",
      "verify:container-red",
      "close:container-red",
      "release:container-red",
      "release:container-yellow"
    ]
  }
}
```

### 多工位资源调度（h3-automated-cargo-terminal-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "floor",
        "duration": 3,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "rack-a",
        "duration": 2,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "rack-b",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "conveyor-a",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "conveyor-b",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "gantry",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      },
      {
        "id": "job-6",
        "module": "shuttle",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-4"
        ]
      },
      {
        "id": "job-7",
        "module": "lift",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-5"
        ]
      },
      {
        "id": "job-8",
        "module": "robot-a",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-6"
        ]
      },
      {
        "id": "job-9",
        "module": "robot-b",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-7"
        ]
      }
    ],
    "deadline": 13
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 3,
      "job-3": 2,
      "job-4": 6,
      "job-5": 4,
      "job-6": 8,
      "job-7": 6,
      "job-8": 11,
      "job-9": 7
    }
  }
}
```

### 检查后条件策略（h3-automated-cargo-terminal-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "lift",
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

### 局部坐标变换（h3-automated-cargo-terminal-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[0,1.2,-1]
- B：[0.71,2.2,1.71]
- C：[-0.29,1.2,0.71]
- D：[0.145,-1.6,-0.855]

```json
{
  "input": {
    "localPoint": [
      0.14500000000000002,
      -1.6,
      -0.855
    ],
    "rotationXYZW": [
      0,
      1,
      0,
      6.123233995736766e-17
    ],
    "translation": [
      -0.14500000000000002,
      2.8000000000000003,
      -0.14500000000000002
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-automated-cargo-terminal-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[-6,11]
- B：[11,5]
- C：[5,6]
- D：[0,0]

```json
{
  "input": {
    "view": "side",
    "point": [
      5,
      11,
      -6
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 空间相对关系（h3-automated-cargo-terminal-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：equal
- B：greater
- C：less

```json
{
  "input": {
    "A": {
      "id": "floor",
      "position": [
        0,
        0.2,
        0
      ]
    },
    "B": {
      "id": "container-yellow",
      "position": [
        8,
        1.05,
        4
      ]
    },
    "axis": "y"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 约束自由度（h3-automated-cargo-terminal-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：0
- B：1
- C：3
- D：6

```json
{
  "input": {
    "joint": {
      "id": "container-1-lock",
      "name": "container 1 lock",
      "type": "fixed",
      "parent": "floor",
      "child": "container-blue",
      "anchorParent": [
        2.5,
        0.49999999999999994,
        3.5
      ],
      "anchorChild": [
        -1.5,
        -0.3500000000000001,
        -0.5
      ],
      "axis": [
        0,
        1,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 维修间隙预算（h3-automated-cargo-terminal-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "lift",
    "aperture": 0.7,
    "toolWidth": 0.65,
    "eachSideMargin": 0.05
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-automated-cargo-terminal-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,-4,0]
- B：[0,0,-24]
- C：[0,0,24]
- D：[0,0,0]

```json
{
  "input": {
    "module": "lift",
    "lever": [
      4,
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
    "choiceId": "B"
  }
}
```

### 非均匀先验更新（h3-automated-cargo-terminal-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0
- B：1
- C：0.2857142857142857
- D：0.16666666666666666

```json
{
  "input": {
    "module": "lift",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      5,
      2,
      5
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

### 风险最小决策（h3-automated-cargo-terminal-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.7,
    "repairCost": 1,
    "failureLoss": 16,
    "module": "lift"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-automated-cargo-terminal-trace-threshold）

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
        "displacement": 0.0051235174752623834
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0000429754552302113
      },
      {
        "time": 0.20833333333333334,
        "displacement": 3.6256089987148156e-7
      },
      {
        "time": 0.30833333333333335,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 0.5083333333333333,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 0.6083333333333333,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 0.7083333333333334,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 0.8083333333333333,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 1.0745380149674385e-7
      },
      {
        "time": 1,
        "displacement": 1.0745380149674385e-7
      }
    ],
    "threshold": 0.004098813980209907
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-automated-cargo-terminal-guarded-repair）

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
        "id": "release:lift",
        "label": "release lift",
        "requires": [
          "done:relock:lift"
        ],
        "forbids": [
          "done:release:lift"
        ],
        "adds": [
          "done:release:lift",
          "ready:lift",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "relock:lift",
        "label": "relock lift",
        "requires": [
          "done:verify:lift"
        ],
        "forbids": [
          "done:relock:lift"
        ],
        "adds": [
          "done:relock:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "verify:lift",
        "label": "verify lift",
        "requires": [
          "done:replace:lift"
        ],
        "forbids": [
          "done:verify:lift"
        ],
        "adds": [
          "done:verify:lift"
        ],
        "deletes": [
          "fault:lift",
          "misaligned:lift"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "replace:lift",
        "label": "replace lift",
        "requires": [
          "done:unlock:lift"
        ],
        "forbids": [
          "done:replace:lift"
        ],
        "adds": [
          "done:replace:lift"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "unlock:lift",
        "label": "unlock lift",
        "requires": [
          "done:support:lift"
        ],
        "forbids": [
          "done:unlock:lift"
        ],
        "adds": [
          "done:unlock:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "support:lift",
        "label": "support lift",
        "requires": [
          "done:isolate:lift"
        ],
        "forbids": [
          "done:support:lift"
        ],
        "adds": [
          "done:support:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "isolate:lift",
        "label": "isolate lift",
        "requires": [
          "tool:free",
          "fault:lift"
        ],
        "forbids": [
          "done:isolate:lift"
        ],
        "adds": [
          "done:isolate:lift"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:lift"
    ],
    "initialModules": [
      "floor",
      "rack-a",
      "rack-b",
      "conveyor-a",
      "conveyor-b",
      "gantry",
      "shuttle",
      "lift",
      "robot-a",
      "robot-b",
      "container-red",
      "container-blue",
      "container-yellow"
    ],
    "goalFacts": [
      "ready:lift"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:lift",
      "support:lift",
      "unlock:lift",
      "replace:lift",
      "verify:lift",
      "relock:lift",
      "release:lift"
    ]
  }
}
```

### 失败状态回退（h3-automated-cargo-terminal-rollback）

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
        "id": "resume:lift",
        "label": "resume lift",
        "requires": [
          "done:verify:lift"
        ],
        "forbids": [
          "done:resume:lift"
        ],
        "adds": [
          "done:resume:lift",
          "ready:lift",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "verify:lift",
        "label": "verify lift",
        "requires": [
          "done:align:lift"
        ],
        "forbids": [
          "done:verify:lift"
        ],
        "adds": [
          "done:verify:lift"
        ],
        "deletes": [
          "fault:lift",
          "misaligned:lift"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      },
      {
        "id": "align:lift",
        "label": "align lift",
        "requires": [
          "done:undo:lift"
        ],
        "forbids": [
          "done:align:lift"
        ],
        "adds": [
          "done:align:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift",
          "visible": true
        }
      },
      {
        "id": "undo:lift",
        "label": "undo lift",
        "requires": [
          "done:isolate:lift"
        ],
        "forbids": [
          "done:undo:lift"
        ],
        "adds": [
          "done:undo:lift"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "lift",
          "visible": false
        }
      },
      {
        "id": "isolate:lift",
        "label": "isolate lift",
        "requires": [
          "tool:free",
          "fault:lift"
        ],
        "forbids": [
          "done:isolate:lift"
        ],
        "adds": [
          "done:isolate:lift"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "lift"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:lift",
      "misaligned:lift"
    ],
    "initialModules": [
      "floor",
      "rack-a",
      "rack-b",
      "conveyor-a",
      "conveyor-b",
      "gantry",
      "shuttle",
      "lift",
      "robot-a",
      "robot-b",
      "container-red",
      "container-blue",
      "container-yellow"
    ],
    "goalFacts": [
      "ready:lift"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:lift",
      "undo:lift",
      "align:lift",
      "verify:lift",
      "resume:lift"
    ]
  }
}
```

### 共享工具协同维修（h3-automated-cargo-terminal-resource-repair）

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
        "id": "release:container-yellow",
        "label": "release container-yellow",
        "requires": [
          "done:relock:container-yellow"
        ],
        "forbids": [
          "done:release:container-yellow"
        ],
        "adds": [
          "done:release:container-yellow",
          "ready:container-yellow",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow"
        }
      },
      {
        "id": "relock:container-yellow",
        "label": "relock container-yellow",
        "requires": [
          "done:verify:container-yellow"
        ],
        "forbids": [
          "done:relock:container-yellow"
        ],
        "adds": [
          "done:relock:container-yellow"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow"
        }
      },
      {
        "id": "verify:container-yellow",
        "label": "verify container-yellow",
        "requires": [
          "done:replace:container-yellow"
        ],
        "forbids": [
          "done:verify:container-yellow"
        ],
        "adds": [
          "done:verify:container-yellow"
        ],
        "deletes": [
          "fault:container-yellow",
          "misaligned:container-yellow"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow"
        }
      },
      {
        "id": "replace:container-yellow",
        "label": "replace container-yellow",
        "requires": [
          "done:unlock:container-yellow"
        ],
        "forbids": [
          "done:replace:container-yellow"
        ],
        "adds": [
          "done:replace:container-yellow"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "container-yellow"
        }
      },
      {
        "id": "unlock:container-yellow",
        "label": "unlock container-yellow",
        "requires": [
          "done:support:container-yellow"
        ],
        "forbids": [
          "done:unlock:container-yellow"
        ],
        "adds": [
          "done:unlock:container-yellow"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow"
        }
      },
      {
        "id": "support:container-yellow",
        "label": "support container-yellow",
        "requires": [
          "done:isolate:container-yellow"
        ],
        "forbids": [
          "done:support:container-yellow"
        ],
        "adds": [
          "done:support:container-yellow"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow"
        }
      },
      {
        "id": "isolate:container-yellow",
        "label": "isolate container-yellow",
        "requires": [
          "tool:free",
          "fault:container-yellow"
        ],
        "forbids": [
          "done:isolate:container-yellow"
        ],
        "adds": [
          "done:isolate:container-yellow"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container-yellow"
        }
      },
      {
        "id": "release:container-blue",
        "label": "release container-blue",
        "requires": [
          "done:relock:container-blue"
        ],
        "forbids": [
          "done:release:container-blue"
        ],
        "adds": [
          "done:release:container-blue",
          "ready:container-blue",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue"
        }
      },
      {
        "id": "relock:container-blue",
        "label": "relock container-blue",
        "requires": [
          "done:verify:container-blue"
        ],
        "forbids": [
          "done:relock:container-blue"
        ],
        "adds": [
          "done:relock:container-blue"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue"
        }
      },
      {
        "id": "verify:container-blue",
        "label": "verify container-blue",
        "requires": [
          "done:replace:container-blue"
        ],
        "forbids": [
          "done:verify:container-blue"
        ],
        "adds": [
          "done:verify:container-blue"
        ],
        "deletes": [
          "fault:container-blue",
          "misaligned:container-blue"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue"
        }
      },
      {
        "id": "replace:container-blue",
        "label": "replace container-blue",
        "requires": [
          "done:unlock:container-blue"
        ],
        "forbids": [
          "done:replace:container-blue"
        ],
        "adds": [
          "done:replace:container-blue"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "container-blue"
        }
      },
      {
        "id": "unlock:container-blue",
        "label": "unlock container-blue",
        "requires": [
          "done:support:container-blue"
        ],
        "forbids": [
          "done:unlock:container-blue"
        ],
        "adds": [
          "done:unlock:container-blue"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue"
        }
      },
      {
        "id": "support:container-blue",
        "label": "support container-blue",
        "requires": [
          "done:isolate:container-blue"
        ],
        "forbids": [
          "done:support:container-blue"
        ],
        "adds": [
          "done:support:container-blue"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue"
        }
      },
      {
        "id": "isolate:container-blue",
        "label": "isolate container-blue",
        "requires": [
          "tool:free",
          "fault:container-blue"
        ],
        "forbids": [
          "done:isolate:container-blue"
        ],
        "adds": [
          "done:isolate:container-blue"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container-blue"
        }
      },
      {
        "id": "release:container-red",
        "label": "release container-red",
        "requires": [
          "done:relock:container-red"
        ],
        "forbids": [
          "done:release:container-red"
        ],
        "adds": [
          "done:release:container-red",
          "ready:container-red",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-red"
        }
      },
      {
        "id": "relock:container-red",
        "label": "relock container-red",
        "requires": [
          "done:verify:container-red"
        ],
        "forbids": [
          "done:relock:container-red"
        ],
        "adds": [
          "done:relock:container-red"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-red"
        }
      },
      {
        "id": "verify:container-red",
        "label": "verify container-red",
        "requires": [
          "done:replace:container-red"
        ],
        "forbids": [
          "done:verify:container-red"
        ],
        "adds": [
          "done:verify:container-red"
        ],
        "deletes": [
          "fault:container-red",
          "misaligned:container-red"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container-red"
        }
      },
      {
        "id": "replace:container-red",
        "label": "replace container-red",
        "requires": [
          "done:unlock:container-red"
        ],
        "forbids": [
          "done:replace:container-red"
        ],
        "adds": [
          "done:replace:container-red"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "container-red"
        }
      },
      {
        "id": "unlock:container-red",
        "label": "unlock container-red",
        "requires": [
          "done:support:container-red"
        ],
        "forbids": [
          "done:unlock:container-red"
        ],
        "adds": [
          "done:unlock:container-red"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-red"
        }
      },
      {
        "id": "support:container-red",
        "label": "support container-red",
        "requires": [
          "done:isolate:container-red"
        ],
        "forbids": [
          "done:support:container-red"
        ],
        "adds": [
          "done:support:container-red"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container-red"
        }
      },
      {
        "id": "isolate:container-red",
        "label": "isolate container-red",
        "requires": [
          "tool:free",
          "fault:container-red"
        ],
        "forbids": [
          "done:isolate:container-red"
        ],
        "adds": [
          "done:isolate:container-red"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container-red"
        }
      },
      {
        "id": "release:robot-b",
        "label": "release robot-b",
        "requires": [
          "done:relock:robot-b"
        ],
        "forbids": [
          "done:release:robot-b"
        ],
        "adds": [
          "done:release:robot-b",
          "ready:robot-b",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b"
        }
      },
      {
        "id": "relock:robot-b",
        "label": "relock robot-b",
        "requires": [
          "done:verify:robot-b"
        ],
        "forbids": [
          "done:relock:robot-b"
        ],
        "adds": [
          "done:relock:robot-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b"
        }
      },
      {
        "id": "verify:robot-b",
        "label": "verify robot-b",
        "requires": [
          "done:replace:robot-b"
        ],
        "forbids": [
          "done:verify:robot-b"
        ],
        "adds": [
          "done:verify:robot-b"
        ],
        "deletes": [
          "fault:robot-b",
          "misaligned:robot-b"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b"
        }
      },
      {
        "id": "replace:robot-b",
        "label": "replace robot-b",
        "requires": [
          "done:unlock:robot-b"
        ],
        "forbids": [
          "done:replace:robot-b"
        ],
        "adds": [
          "done:replace:robot-b"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "robot-b"
        }
      },
      {
        "id": "unlock:robot-b",
        "label": "unlock robot-b",
        "requires": [
          "done:support:robot-b"
        ],
        "forbids": [
          "done:unlock:robot-b"
        ],
        "adds": [
          "done:unlock:robot-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b"
        }
      },
      {
        "id": "support:robot-b",
        "label": "support robot-b",
        "requires": [
          "done:isolate:robot-b"
        ],
        "forbids": [
          "done:support:robot-b"
        ],
        "adds": [
          "done:support:robot-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b"
        }
      },
      {
        "id": "isolate:robot-b",
        "label": "isolate robot-b",
        "requires": [
          "tool:free",
          "fault:robot-b"
        ],
        "forbids": [
          "done:isolate:robot-b"
        ],
        "adds": [
          "done:isolate:robot-b"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "robot-b"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:robot-b",
      "fault:container-red",
      "fault:container-blue",
      "fault:container-yellow"
    ],
    "initialModules": [
      "floor",
      "rack-a",
      "rack-b",
      "conveyor-a",
      "conveyor-b",
      "gantry",
      "shuttle",
      "lift",
      "robot-a",
      "robot-b",
      "container-red",
      "container-blue",
      "container-yellow"
    ],
    "goalFacts": [
      "ready:robot-b",
      "ready:container-red",
      "ready:container-blue",
      "ready:container-yellow"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:container-yellow",
      "support:container-yellow",
      "unlock:container-yellow",
      "replace:container-yellow",
      "verify:container-yellow",
      "relock:container-yellow",
      "release:container-yellow",
      "isolate:container-blue",
      "support:container-blue",
      "unlock:container-blue",
      "replace:container-blue",
      "verify:container-blue",
      "relock:container-blue",
      "release:container-blue",
      "isolate:container-red",
      "support:container-red",
      "unlock:container-red",
      "replace:container-red",
      "verify:container-red",
      "relock:container-red",
      "release:container-red",
      "isolate:robot-b",
      "support:robot-b",
      "unlock:robot-b",
      "replace:robot-b",
      "verify:robot-b",
      "relock:robot-b",
      "release:robot-b"
    ]
  }
}
```

### 预算约束检查策略（h3-automated-cargo-terminal-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "lift",
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
