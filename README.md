# Golden Frame

[![](https://img.shields.io/pypi/v/golden-frame)](https://pypi.org/project/golden-frame)
[![](https://img.shields.io/pypi/dm/golden-frame)](https://pypi.org/project/golden-frame)

"กรอบทอง Generator"

## Examples

<img src="https://github.com/Leomotors/golden-frame/raw/main/golden_frame/assets/golden_frame.png" width=200 /> **+**
<img src="https://github.com/Leomotors/golden-frame/raw/main/example/MasterIceZ.jpg" width = 200 /> **=**
<img src="https://github.com/Leomotors/golden-frame/raw/main/example/New-MasterIceZ.png" width=200 />

<img src="https://github.com/Leomotors/golden-frame/raw/main/golden_frame/assets/wessuwan.png" width=200 /> **+**
<img src="https://github.com/Leomotors/golden-frame/raw/main/example/honami-stella.jpg" width = 200 /> **=**
<img src="https://github.com/Leomotors/golden-frame/raw/main/example/honami-wessuwan.png" width=200 />

### Command for Above Examples

```bash
golden-frame build golden_frame.png example/MasterIceZ.jpg --output=example/New-MasterIceZ.png

golden-frame build wessuwan.png example/honami-stella.jpg --output=example/honami-wessuwan.png
```

### Other commands

Use `golden-frame --help` or `golden-frame build help`

## Adding Images

Currently, to add images, add them directly in assets folder.

You can get its location with this command

```python
import os
from pkg_resources import get_distribution
location = get_distribution("golden-frame").location
ASSET_PATH = os.path.join(location, "golden_frame/assets")
print(ASSET_PATH)
```

Note that this is temporary and can be overwrite when installing new version.

`file_name.json` Schema

```jsonc
{
  "name": "Golden Frame ทพจร",
  "pos": [
    [122, 122],
    [620, 122],
    [620, 844],
    [112, 844]
  ],
  // Optional, for image scaling to ensure good quality
  "defaultMultiplier": 2
}
```

Position is from Top-Left rotate clockwise.  
Reminder that x goes from left to right and y from top to bottom

## Live Demo

https://golden-frame.leomotors.me (Repo: https://github.com/leomotors/golden-frame-web)

## Coming Soon { flex: true }

Adding this properties allow images to be stretch into the same aspect ratio as the input image
