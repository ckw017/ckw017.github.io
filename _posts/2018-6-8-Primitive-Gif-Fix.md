---
layout: post
img: /images/primitive-fix/campanile.gif
title: Fix for "exit status 4" when writing Primitive Gif
tags: Go Bugfix 2018
excerpt_separator: <!--more-->
---

This is just a quick fix for a problem I ran into while trying to use [Primitive](https://github.com/fogleman/primitive)
on Windows. While trying to create a gif, you might run into a message like this:

```bash
writing test.gif
2018/06/08 14:07:20 exit status 4
```

<!--more-->

1. Make sure that you have [ImageMagick]([https://www.imagemagick.org/script/download.php) installed.

2. Locate the "utils.go" file in the source for primitive. On my computer it was located at `C:\Users\Me\go\src\github.com\fogleman\primitive\primitive\utils.go`

3. Look for this section:
	```
		args := []string{
		"-loop", "0",
		"-delay", fmt.Sprint(delay),
		filepath.Join(dir, "*.png"),
		"-delay", fmt.Sprint(lastDelay - delay),
		filepath.Join(dir, fmt.Sprintf("%06d.png", len(frames)-1)),
		path,
	}
	cmd := exec.Command("convert", args...)
	```
4. Move `"convert"` to the beginning of args, and change the command name to `"magick"`
	```
		args := []string{
		"convert",
		"-loop", "0",
		"-delay", fmt.Sprint(delay),
		filepath.Join(dir, "*.png"),
		"-delay", fmt.Sprint(lastDelay - delay),
		filepath.Join(dir, fmt.Sprintf("%06d.png", len(frames)-1)),
		path,
	}
	cmd := exec.Command("magick", args...)
	```

5. Reinstall primitive with `go install github.com/fogleman/primitive` (or whatever your path is in go\src\)

Basically, to create the gifs primitive tries to use the `magick convert` command.
However, windows has a default command called `convert` that gets used instead.
These changes should fix the problem.

![](/images/primitive-fix/campanile.jpg)
![](/images/primitive-fix/campanile.gif)