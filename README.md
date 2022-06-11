# Golden Frame

[![](https://img.shields.io/pypi/v/golden-frame)](https://pypi.org/project/golden-frame)
[![](https://img.shields.io/pypi/dm/golden-frame)](https://pypi.org/project/golden-frame)

"กรอบทอง Generator"

## Example

<img src="https://github.com/Leomotors/golden-frame/raw/main/golden_frame/assets/golden_frame.png" width=200 /> **+**
<img src="https://github.com/Leomotors/golden-frame/raw/main/example/zhongxina_before.jpg" width = 200 /> **=**
<img src="https://github.com/Leomotors/golden-frame/raw/main/example/zhongxina_after.png" width=200 />

PS. The original picture of golden frame is K-Pop Star (Search: กรอบทอง ทรงพระเจริญ in Google, there are many variant)

### Command for Above Example

```bash
golden-frame build golden_frame.png example/zhongxina_before.jpg --output=example/zhongxina_after.png
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
  "pos": "122,122,620,844"
}
```

pos => x1,y1,x2,y2 ; Position to put pictures on, you can get these info using Paint
