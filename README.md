# Golden Frame

[![](https://img.shields.io/pypi/v/golden-frame)](https://pypi.org/project/golden-frame)
[![](https://img.shields.io/pypi/dm/golden-frame)](https://pypi.org/project/golden-frame)

"กรอบทอง Generator"

## Example

<img src="https://github.com/Leomotors/golden-frame/raw/main/golden_frame/assets/golden_frame.png" width=200 /> **+**
<img src="https://github.com/Leomotors/golden-frame/raw/main/example/MasterIceZ.jpg" width = 200 /> **=**
<img src="https://github.com/Leomotors/golden-frame/raw/main/example/New-MasterIceZ.png" width=200 />

PS. The original picture of golden frame is K-Pop Star (Search: กรอบทอง ทรงพระเจริญ in Google, there are many variant)

### Command for Above Example

```bash
golden-frame build golden_frame.png example/MasterIceZ.jpg --output=example/New-MasterIceZ.png
```

### Other commands

Use `golden-frame --help`

## Adding Images

Currently, to add images, add them directly in assets folder.

You can get its location with this command

```python
import pkg_resources
pkg_resources.resource_filename("golden_frame", "assets")
```

Note that this is temporary can be overwrite when installing new version.

file_name.json Schema

```json
{
  "name": "Golden Frame ทพจร",
  "pos": [
    [122, 122],
    [620, 122],
    [620, 844],
    [112, 844]
  ]
}
```

Position is from Top-Left rotate clockwise.  
Reminder that x goes from left to right and y from top to bottom

## TODO: { flex: true }

Adding this properties allow images to be stretch into the same aspect ratio as the input image
